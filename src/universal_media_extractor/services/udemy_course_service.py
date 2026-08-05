"""Udemy course analysis/download service.

This service is intentionally best-effort and does not implement DRM bypass,
decryption-key handling, credential storage, or CAPTCHA/paywall bypass.
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from universal_media_extractor.error_mapping import normalize_cli_error
from universal_media_extractor.models import (
    ErrorState,
    UdemyCourseAnalyzeRequest,
    UdemyCourseAnalyzeResult,
    UdemyCourseDownloadRequest,
    UdemyCourseDownloadResult,
    UdemyCourseSection,
    UdemyLectureOption,
    WarningState,
)
from universal_media_extractor.services.download_service import (
    DEFAULT_OUTPUT_BASE_DIR,
    _parse_ytdlp_progress_line,
    _stop_process,
)
from universal_media_extractor.services.output_manager import OutputManager
from universal_media_extractor.services.safety_service import SafetyService

if TYPE_CHECKING:
    from universal_media_extractor.services.job_service import JobService


DEFAULT_UDEMY_TIMEOUT_SECONDS = 3600
UDEMY_OUTPUT_BASE_DIR = DEFAULT_OUTPUT_BASE_DIR / "Udemy"
UDEMY_PROGRESS_RE = re.compile(r"\[download\]\s+([0-9]+(?:\.[0-9]+)?)%")


class UdemyCourseService:
    """Analyze and download Udemy courses through yt-dlp."""

    def __init__(
        self,
        *,
        safety_service: SafetyService | None = None,
        output_manager: OutputManager | None = None,
        timeout_seconds: int = DEFAULT_UDEMY_TIMEOUT_SECONDS,
    ) -> None:
        self.safety_service = safety_service or SafetyService()
        self.output_manager = output_manager or OutputManager()
        self.timeout_seconds = timeout_seconds

    def analyze_course(
        self,
        request: UdemyCourseAnalyzeRequest,
        *,
        raw_output_dir: Path | None = None,
    ) -> UdemyCourseAnalyzeResult:
        """Inspect a Udemy course without downloading media."""

        auth = _resolve_auth_args(request.auth_source, request.cookies_path)
        if auth.error is not None:
            return _analyze_failed(
                request,
                auth.error,
            )

        command = _build_analyze_command(request, auth)
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=False,
                timeout=min(self.timeout_seconds, 300),
            )
        except FileNotFoundError as exc:
            return _analyze_failed(
                request,
                ErrorState(
                    code="ytdlp_not_found",
                    message="yt-dlp was not found.",
                    technical_details=str(exc),
                    recoverable=True,
                    suggested_user_action="Install yt-dlp or check PATH, then retry.",
                ),
            )
        except subprocess.TimeoutExpired as exc:
            return _analyze_failed(
                request,
                ErrorState(
                    code="timeout",
                    message="Udemy course analysis timed out.",
                    technical_details=_compact_details(exc.stdout or exc.stderr),
                    recoverable=True,
                    suggested_user_action="Retry with a stable connection.",
                ),
            )

        raw_reference_path: str | None = None
        if raw_output_dir is not None:
            raw_output_dir.mkdir(parents=True, exist_ok=True)
            raw_reference_path = str(raw_output_dir / "udemy_course_raw.json")

        if completed.returncode != 0:
            if raw_reference_path:
                _write_analyze_failure_artifact(
                    Path(raw_reference_path),
                    command=command,
                    auth=auth,
                    returncode=completed.returncode,
                    stdout=completed.stdout,
                    stderr=completed.stderr,
                )
            return _analyze_failed(
                request,
                _error_from_output(completed.stdout, completed.stderr),
                raw_reference_path=raw_reference_path,
            )

        try:
            raw = json.loads(completed.stdout)
        except json.JSONDecodeError:
            return _analyze_failed(
                request,
                ErrorState(
                    code="invalid_output",
                    message="yt-dlp returned invalid Udemy course JSON.",
                    technical_details=_compact_details(completed.stdout),
                    recoverable=True,
                    suggested_user_action="Retry. If it repeats, the Udemy extractor may have changed.",
                ),
                raw_reference_path=raw_reference_path,
            )

        if raw_reference_path:
            Path(raw_reference_path).write_text(
                json.dumps(raw, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        return _normalize_course_info(
            raw,
            request=request,
            raw_reference_path=raw_reference_path,
        )

    def download_course(
        self,
        request: UdemyCourseDownloadRequest,
        *,
        job_service: "JobService | None" = None,
        job_id: str | None = None,
    ) -> UdemyCourseDownloadResult:
        """Download a Udemy course through yt-dlp if user rights are confirmed."""

        if not self.safety_service.require_rights_confirmation(
            request.user_confirmed_rights
        ):
            return UdemyCourseDownloadResult(
                status="blocked",
                course_url=request.course_url,
                course_title=request.course_title,
                errors=[
                    ErrorState(
                        code="rights_confirmation_required",
                        message="Rights confirmation is required before course download.",
                        recoverable=True,
                        suggested_user_action="Confirm you have the right to download/process this course, then retry.",
                    )
                ],
            )

        auth = _resolve_auth_args(request.auth_source, request.cookies_path)
        if auth.error is not None:
            return UdemyCourseDownloadResult(
                status="failed",
                course_url=request.course_url,
                course_title=request.course_title,
                errors=[auth.error],
            )

        _update_job_step(job_service, job_id, "preparing_udemy_download", 0)
        output_base_dir = (
            Path(request.output_base_dir)
            if request.output_base_dir
            else UDEMY_OUTPUT_BASE_DIR
        )
        output_dir = self.output_manager.create_download_output_dir(
            output_base_dir,
            source_id=_course_slug_from_url(request.course_url),
            source_title=request.course_title,
        )
        metadata_path = output_dir / ".metadata" / "udemy_download_result.json"
        request_path = output_dir / ".metadata" / "udemy_download_request.json"
        log_path = output_dir / ".logs" / "udemy_download.log"
        request_path.write_text(
            _safe_request_json(request),
            encoding="utf-8",
        )

        command = _build_download_command(request, auth, output_dir)
        _write_log_header(log_path, command, auth)
        result = self._run_download(
            command,
            request,
            output_dir,
            metadata_path,
            log_path,
            job_service=job_service,
            job_id=job_id,
        )
        metadata_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        return result

    def _run_download(
        self,
        command: list[str],
        request: UdemyCourseDownloadRequest,
        output_dir: Path,
        metadata_path: Path,
        log_path: Path,
        *,
        job_service: "JobService | None" = None,
        job_id: str | None = None,
    ) -> UdemyCourseDownloadResult:
        process: subprocess.Popen[str] | None = None
        output_lines: list[str] = []
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=False,
                bufsize=1,
            )
        except FileNotFoundError as exc:
            return _download_failed(
                request,
                output_dir,
                metadata_path,
                log_path,
                ErrorState(
                    code="ytdlp_not_found",
                    message="yt-dlp was not found.",
                    technical_details=str(exc),
                    recoverable=True,
                    suggested_user_action="Install yt-dlp or check PATH, then retry.",
                ),
            )

        if job_service and job_id:
            job_service.register_subprocess(job_id, process)

        deadline = time.monotonic() + self.timeout_seconds
        timed_out = False
        try:
            stdout = process.stdout
            while True:
                if job_service and job_id and job_service.is_cancel_requested(job_id):
                    _stop_process(process)
                    return _download_cancelled(request, output_dir, metadata_path, log_path)

                if time.monotonic() > deadline:
                    timed_out = True
                    _stop_process(process)
                    break

                line = stdout.readline() if stdout is not None else ""
                if line:
                    output_lines.append(line)
                    _append_log_text(log_path, _redact_sensitive(line))
                    step, percent = _parse_udemy_progress_line(line)
                    if step:
                        _update_job_step(job_service, job_id, step, percent)
                    continue

                if process.poll() is not None:
                    break
                time.sleep(0.05)

            if stdout is not None:
                remaining = stdout.read()
                if remaining:
                    output_lines.append(remaining)
                    _append_log_text(log_path, _redact_sensitive(remaining))
            returncode = process.wait(timeout=2)
        finally:
            if job_service and job_id and process is not None:
                job_service.clear_subprocess(job_id, process)

        stdout_text = "".join(output_lines)
        downloaded_files = _list_course_files(output_dir)
        if timed_out:
            return _download_failed(
                request,
                output_dir,
                metadata_path,
                log_path,
                ErrorState(
                    code="timeout",
                    message="Udemy course download timed out.",
                    technical_details=_compact_details(stdout_text),
                    recoverable=True,
                    suggested_user_action="Retry later or lower quality.",
                ),
                downloaded_files=downloaded_files,
            )

        if returncode != 0:
            if job_service and job_id and job_service.is_cancel_requested(job_id):
                return _download_cancelled(
                    request,
                    output_dir,
                    metadata_path,
                    log_path,
                    downloaded_files=downloaded_files,
                )
            return _download_failed(
                request,
                output_dir,
                metadata_path,
                log_path,
                _error_from_output(stdout_text, None),
                downloaded_files=downloaded_files,
            )

        _update_job_step(job_service, job_id, "saving_metadata", 99)
        return UdemyCourseDownloadResult(
            status="succeeded",
            course_url=request.course_url,
            course_title=request.course_title,
            output_dir=str(output_dir),
            downloaded_files=[str(path) for path in downloaded_files],
            metadata_path=str(metadata_path),
            log_path=str(log_path),
            warnings=_download_warnings(request),
        )


def _build_analyze_command(
    request: UdemyCourseAnalyzeRequest,
    auth: "_UdemyAuthArgs",
) -> list[str]:
    return [
        "yt-dlp",
        "--dump-single-json",
        "--flat-playlist",
        *auth.command_args,
        request.course_url,
    ]


def _build_download_command(
    request: UdemyCourseDownloadRequest,
    auth: "_UdemyAuthArgs",
    output_dir: Path,
) -> list[str]:
    command = [
        "yt-dlp",
        "--newline",
        "--ignore-errors",
        *auth.command_args,
        "-P",
        str(output_dir),
        "-o",
        "%(chapter_number|00)s - %(chapter|Course)s/%(playlist_index)03d - %(title).180B.%(ext)s",
        "-f",
        _format_selector(request.quality),
        "--merge-output-format",
        request.output_format,
        "--remux-video",
        request.output_format,
    ]
    if request.include_subtitles:
        command.extend(
            [
                "--write-subs",
                "--write-auto-subs",
                "--sub-format",
                "srt/best",
                "--convert-subs",
                "srt",
            ]
        )
    if request.lecture_limit:
        command.extend(["--playlist-end", str(request.lecture_limit)])
    command.append(request.course_url)
    return command


def _format_selector(quality: str) -> str:
    if quality == "best":
        return "bestvideo+bestaudio/best"
    return f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best"


def _normalize_course_info(
    raw: dict[str, Any],
    *,
    request: UdemyCourseAnalyzeRequest,
    raw_reference_path: str | None,
) -> UdemyCourseAnalyzeResult:
    entries = raw.get("entries") if isinstance(raw.get("entries"), list) else []
    sections_by_title: dict[str, UdemyCourseSection] = {}
    flat_lectures: list[UdemyLectureOption] = []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            continue
        title = entry.get("title") or entry.get("display_id") or f"Lecture {index}"
        section_title = entry.get("chapter") or entry.get("section") or "Course"
        section_number = _int_or_none(entry.get("chapter_number")) or 1
        lecture = UdemyLectureOption(
            lecture_id=str(entry.get("id")) if entry.get("id") is not None else None,
            title=str(title),
            section_title=str(section_title),
            section_index=section_number,
            lecture_index=index,
            duration_seconds=_float_or_none(entry.get("duration")),
            webpage_url=entry.get("webpage_url") or entry.get("url"),
            is_downloadable=True,
        )
        flat_lectures.append(lecture)
        section = sections_by_title.get(lecture.section_title or "Course")
        if section is None:
            section = UdemyCourseSection(
                title=lecture.section_title or "Course",
                section_index=section_number,
            )
            sections_by_title[section.title] = section
        section.lectures.append(lecture)

    return UdemyCourseAnalyzeResult(
        status="succeeded",
        course_url=request.course_url,
        course_title=_course_title_from_raw_or_url(raw, request.course_url),
        extractor=raw.get("extractor") or raw.get("extractor_key") or "udemy",
        sections=sorted(sections_by_title.values(), key=lambda section: section.section_index),
        lecture_count=len(flat_lectures),
        raw_reference_path=raw_reference_path,
        warnings=_analysis_warnings(),
    )


def _analysis_warnings() -> list[WarningState]:
    return [
        WarningState(
            code="platform_terms_warning",
            message="Udemy downloads are best-effort and must respect your rights and Udemy restrictions.",
        ),
        WarningState(
            code="best_effort_extractor",
            message="Some courses or lectures may be unavailable because of DRM, expired cookies, or platform changes.",
        ),
    ]


def _download_warnings(request: UdemyCourseDownloadRequest) -> list[WarningState]:
    warnings = _analysis_warnings()
    if request.include_resources:
        warnings.append(
            WarningState(
                code="best_effort_extractor",
                message="Resource attachment download is best-effort in the yt-dlp path and may not include every course asset.",
            )
        )
    return warnings


def _analyze_failed(
    request: UdemyCourseAnalyzeRequest,
    error: ErrorState,
    *,
    raw_reference_path: str | None = None,
) -> UdemyCourseAnalyzeResult:
    return UdemyCourseAnalyzeResult(
        status="failed",
        course_url=request.course_url,
        raw_reference_path=raw_reference_path,
        errors=[error],
    )


def _download_failed(
    request: UdemyCourseDownloadRequest,
    output_dir: Path,
    metadata_path: Path,
    log_path: Path,
    error: ErrorState,
    *,
    downloaded_files: list[Path] | None = None,
) -> UdemyCourseDownloadResult:
    return UdemyCourseDownloadResult(
        status="failed",
        course_url=request.course_url,
        course_title=request.course_title,
        output_dir=str(output_dir),
        downloaded_files=[str(path) for path in (downloaded_files or [])],
        metadata_path=str(metadata_path),
        log_path=str(log_path),
        errors=[error],
    )


def _download_cancelled(
    request: UdemyCourseDownloadRequest,
    output_dir: Path,
    metadata_path: Path,
    log_path: Path,
    *,
    downloaded_files: list[Path] | None = None,
) -> UdemyCourseDownloadResult:
    return UdemyCourseDownloadResult(
        status="cancelled",
        course_url=request.course_url,
        course_title=request.course_title,
        output_dir=str(output_dir),
        downloaded_files=[str(path) for path in (downloaded_files or [])],
        metadata_path=str(metadata_path),
        log_path=str(log_path),
    )


class _UdemyAuthArgs:
    def __init__(
        self,
        *,
        command_args: list[str] | None = None,
        redacted_label: str = "[chrome-session]",
        error: ErrorState | None = None,
    ) -> None:
        self.command_args = command_args or []
        self.redacted_label = redacted_label
        self.error = error


def _resolve_auth_args(auth_source: str, cookies_path: str | None) -> _UdemyAuthArgs:
    if auth_source == "manual_cookies":
        path = _validated_cookies_path(cookies_path)
        if path is None:
            return _UdemyAuthArgs(error=_cookies_missing_error(cookies_path))
        return _UdemyAuthArgs(
            command_args=["--cookies", str(path)],
            redacted_label="[redacted-cookies]",
        )
    return _UdemyAuthArgs(
        command_args=["--cookies-from-browser", "chrome"],
        redacted_label="[chrome-session]",
    )


def _cookies_missing_error(cookies_path: str | None) -> ErrorState:
    return ErrorState(
        code="cookies_required",
        message="Manual cookies.txt file is missing or unreadable.",
        technical_details=f"Cookies file was not found or is not readable: {cookies_path}",
        recoverable=True,
        suggested_user_action="Use Chrome session mode, or choose a readable cookies.txt file in advanced manual mode.",
    )


def _error_from_output(stdout: str | bytes | None, stderr: str | bytes | None) -> ErrorState:
    details = _compact_details("\n".join(filter(None, [_ensure_text(stdout), _ensure_text(stderr)])))
    lowered = (details or "").lower()
    if "drm" in lowered or "encrypted" in lowered or "decryption" in lowered:
        return ErrorState(
            code="drm_protected",
            message="This lecture appears protected.",
            technical_details=details,
            recoverable=False,
            suggested_user_action="The app does not bypass DRM. Use Udemy's official offline options for protected lectures.",
        )
    if (
        "login" in lowered
        or "sign in" in lowered
        or "authenticated" in lowered
        or "not enrolled" in lowered
        or "purchased" in lowered
    ):
        return ErrorState(
            code="login_required",
            message="Udemy did not allow access with the current Chrome session.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Open Udemy in Chrome, make sure you are signed in, then try again.",
        )
    if (
        "cookie" in lowered
        or "browser" in lowered
        or "keyring" in lowered
        or "403" in lowered
        or "forbidden" in lowered
        or "unable to download webpage" in lowered
        or "http error 401" in lowered
    ):
        return ErrorState(
            code="cookies_required",
            message="Chrome session is unavailable or Udemy rejected it.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Open Chrome, sign in to Udemy, then retry. If macOS blocks Chrome cookies, use Advanced manual cookies.txt.",
        )
    normalized = normalize_cli_error(
        details,
        default_code="extractor_failed",
        default_message="Udemy course extraction failed.",
        default_suggested_user_action="Retry later, or test a single lecture first. Details are saved in the proof/api artifact.",
        engine="udemy",
    )
    if normalized.code == "engine_outdated":
        return ErrorState(
            code="engine_outdated",
            message="Udemy course extraction may require a media engine update.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Update yt-dlp and retry with the Udemy lecture URL from the course player.",
        )
    return normalized


def _parse_udemy_progress_line(line: str) -> tuple[str | None, float | None]:
    step, percent = _parse_ytdlp_progress_line(line)
    if step:
        return step, percent
    if "[download]" in line:
        match = UDEMY_PROGRESS_RE.search(line)
        if match:
            return "downloading_course", min(float(match.group(1)), 100.0)
    if "Downloading video" in line or "lecture" in line.lower():
        return "downloading_course", None
    return None, None


def _update_job_step(
    job_service: "JobService | None",
    job_id: str | None,
    current_step: str,
    progress_percent: float | None = None,
) -> None:
    if job_service is None or job_id is None:
        return
    try:
        job_service.update_job_step(job_id, current_step, progress_percent)
    except KeyError:
        return


def _validated_cookies_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        return None
    return path


def _safe_request_json(request: UdemyCourseDownloadRequest) -> str:
    data = request.model_dump()
    if data.get("cookies_path"):
        data["cookies_path"] = "[redacted]"
    return json.dumps(data, ensure_ascii=False, indent=2)


def _write_log_header(log_path: Path, command: list[str], auth: _UdemyAuthArgs) -> None:
    log_path.write_text(
        "Command:\n"
        + json.dumps(_redact_command(command, auth), ensure_ascii=False, indent=2)
        + "\n\nstdout:\n",
        encoding="utf-8",
    )


def _write_analyze_failure_artifact(
    path: Path,
    *,
    command: list[str],
    auth: _UdemyAuthArgs,
    returncode: int,
    stdout: str | bytes | None,
    stderr: str | bytes | None,
) -> None:
    payload = {
        "status": "failed",
        "returncode": returncode,
        "command": _redact_command(command, auth),
        "stdout": _redact_sensitive(_ensure_text(stdout)),
        "stderr": _redact_sensitive(_ensure_text(stderr)),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _redact_command(command: list[str], auth: _UdemyAuthArgs) -> list[str]:
    redacted: list[str] = []
    skip_next = False
    for index, item in enumerate(command):
        if skip_next:
            skip_next = False
            continue
        redacted.append(item)
        if item in {"--cookies", "--cookies-from-browser"} and index + 1 < len(command):
            redacted.append(auth.redacted_label)
            skip_next = True
    return redacted


def _append_log_text(log_path: Path, text: str) -> None:
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _redact_sensitive(text: str) -> str:
    return re.sub(r"(Bearer\s+)[A-Za-z0-9._-]+", r"\1[redacted]", text)


def _list_course_files(output_dir: Path) -> list[Path]:
    if not output_dir.exists():
        return []
    return sorted(
        path
        for path in output_dir.rglob("*")
        if path.is_file() and not any(part.startswith(".") for part in path.relative_to(output_dir).parts)
    )


def _course_slug_from_url(url: str) -> str:
    try:
        parts = [part for part in urlparse(url).path.split("/") if part]
    except ValueError:
        parts = []
    if "course" in parts:
        course_index = parts.index("course")
        if course_index + 1 < len(parts):
            return parts[course_index + 1]
    return parts[-1] if parts else "udemy_course"


def _course_title_from_raw_or_url(raw: dict[str, Any], url: str) -> str | None:
    title = raw.get("title") or raw.get("playlist_title")
    if title:
        return str(title)
    slug = _course_slug_from_url(url)
    if not slug or slug == "udemy_course":
        return None
    words = [part for part in re.split(r"[-_]+", slug) if part]
    return " ".join(word.upper() if len(word) == 1 else word.capitalize() for word in words)


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _ensure_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _compact_details(value: str | bytes | None) -> str | None:
    text = _ensure_text(value).strip()
    if not text:
        return None
    return _redact_sensitive(text[-2000:])
