"""Download service for selected yt-dlp formats."""

from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import parse_qs, urlparse

from universal_media_extractor.error_mapping import normalize_cli_error
from universal_media_extractor.models import DownloadRequest, DownloadResult, ErrorState
from universal_media_extractor.services.output_manager import OutputManager
from universal_media_extractor.services.safety_service import SafetyService

if TYPE_CHECKING:
    from universal_media_extractor.services.job_service import JobService


DEFAULT_OUTPUT_BASE_DIR = Path.home() / "Downloads" / "Universal Media Extractor"
DEFAULT_DOWNLOAD_TIMEOUT_SECONDS = 600
YTDLP_PROGRESS_RE = re.compile(r"\[download\]\s+([0-9]+(?:\.[0-9]+)?)%")
VIDEO_OUTPUT_FORMATS = {"mp4", "mkv", "webm"}
AUDIO_OUTPUT_FORMATS = {"m4a", "mp3", "wav"}
SUBTITLE_OUTPUT_FORMATS = {"srt", "vtt"}


class DownloadService:
    """Run a single local yt-dlp download after rights confirmation."""

    def __init__(
        self,
        *,
        safety_service: SafetyService | None = None,
        output_manager: OutputManager | None = None,
        timeout_seconds: int = DEFAULT_DOWNLOAD_TIMEOUT_SECONDS,
    ) -> None:
        self.safety_service = safety_service or SafetyService()
        self.output_manager = output_manager or OutputManager()
        self.timeout_seconds = timeout_seconds

    def download_media(
        self,
        request: DownloadRequest,
        *,
        job_service: "JobService | None" = None,
        job_id: str | None = None,
    ) -> DownloadResult:
        """Download the selected format or return a blocked/failed result."""

        if not self.safety_service.require_rights_confirmation(
            request.user_confirmed_rights
        ):
            return DownloadResult(
                status="blocked",
                source_url=request.source_url,
                selected_format_id=request.format_id,
                errors=[
                    ErrorState(
                        code="unknown_error",
                        message="Rights confirmation is required before download.",
                        recoverable=True,
                        suggested_user_action="Confirm you have the right to download/process this media, then retry.",
                    )
                ],
            )

        _update_job_step(job_service, job_id, "preparing_download", 0)
        output_base_dir = (
            Path(request.output_base_dir)
            if request.output_base_dir
            else DEFAULT_OUTPUT_BASE_DIR
        )
        output_dir = self.output_manager.create_download_output_dir(
            output_base_dir,
            source_id=_source_id_from_url(request.source_url),
            source_title=request.source_title,
        )
        metadata_dir = output_dir / ".metadata"
        log_path = output_dir / ".logs" / "download.log"
        request_path = metadata_dir / "download_request.json"
        result_path = metadata_dir / "download_result.json"

        request_path.write_text(request.model_dump_json(indent=2), encoding="utf-8")

        command = _build_ytdlp_command(request, output_dir)
        _write_log_header(log_path, command)

        result = self._run_download(
            command,
            request,
            output_dir,
            log_path,
            result_path,
            job_service=job_service,
            job_id=job_id,
        )
        result_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        return result

    def _run_download(
        self,
        command: list[str],
        request: DownloadRequest,
        output_dir: Path,
        log_path: Path,
        result_path: Path,
        *,
        job_service: "JobService | None" = None,
        job_id: str | None = None,
    ) -> DownloadResult:
        _update_job_step(job_service, job_id, "downloading", 0)
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
            return _failed_result(
                request,
                output_dir,
                log_path,
                result_path,
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
                    return _cancelled_result(request, output_dir, log_path, result_path)

                if time.monotonic() > deadline:
                    timed_out = True
                    _stop_process(process)
                    break

                line = stdout.readline() if stdout is not None else ""
                if line:
                    output_lines.append(line)
                    _append_log_text(log_path, line)
                    step, percent = _parse_ytdlp_progress_line(line)
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
                    _append_log_text(log_path, remaining)
                    for line in remaining.splitlines():
                        step, percent = _parse_ytdlp_progress_line(line)
                        if step:
                            _update_job_step(job_service, job_id, step, percent)
            returncode = process.wait(timeout=2)
        finally:
            if job_service and job_id and process is not None:
                job_service.clear_subprocess(job_id, process)

        stdout_text = "".join(output_lines)

        if timed_out:
            return _failed_result(
                request,
                output_dir,
                log_path,
                result_path,
                ErrorState(
                    code="timeout",
                    message="Download timed out.",
                    technical_details=_compact_details(stdout_text),
                    recoverable=True,
                    suggested_user_action="Retry later or choose a smaller format.",
                ),
            )

        downloaded_files = _list_downloaded_files(output_dir)
        if returncode != 0:
            if job_service and job_id and job_service.is_cancel_requested(job_id):
                return _cancelled_result(
                    request,
                    output_dir,
                    log_path,
                    result_path,
                    downloaded_files=downloaded_files,
                )
            return _failed_result(
                request,
                output_dir,
                log_path,
                result_path,
                normalize_cli_error(
                    stdout_text,
                    default_code="extractor_failed",
                    default_message="yt-dlp download failed.",
                    default_suggested_user_action="Check that the selected format is still available and retry.",
                    engine="yt-dlp",
                ),
                downloaded_files=downloaded_files,
            )

        _update_job_step(job_service, job_id, "saving_metadata", 99)
        return DownloadResult(
            status="succeeded",
            source_url=request.source_url,
            selected_format_id=request.format_id,
            output_dir=str(output_dir),
            downloaded_files=[str(path) for path in downloaded_files],
            metadata_path=str(result_path),
            log_path=str(log_path),
        )


def _build_ytdlp_command(request: DownloadRequest, output_dir: Path) -> list[str]:
    output_template = str(output_dir / "%(title).200B [%(id)s].%(ext)s")
    command = [
        "yt-dlp",
        "--no-playlist",
        "--newline",
        "-o",
        output_template,
    ]

    if request.mode == "subtitles":
        subtitle_format = _safe_output_format(
            request.output_format,
            SUBTITLE_OUTPUT_FORMATS,
            default="srt",
        )
        return [
            *command,
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            request.format_id,
            "--sub-format",
            f"{subtitle_format}/best",
            "--convert-subs",
            subtitle_format,
            request.source_url,
        ]

    format_selector = request.format_id
    postprocess_args: list[str] = []
    if request.mode in {"video", "combined"}:
        if request.mode == "video":
            format_selector = f"{request.format_id}+bestaudio/best"
        video_format = _safe_output_format(
            request.output_format,
            VIDEO_OUTPUT_FORMATS,
            default="mp4",
        )
        postprocess_args = [
            "--merge-output-format",
            video_format,
            "--remux-video",
            video_format,
        ]
    elif request.mode == "audio" and request.output_format:
        audio_format = _safe_output_format(
            request.output_format,
            AUDIO_OUTPUT_FORMATS,
            default="m4a",
        )
        postprocess_args = [
            "-x",
            "--audio-format",
            audio_format,
        ]

    return [
        *command,
        "-f",
        format_selector,
        *postprocess_args,
        request.source_url,
    ]


def _safe_output_format(
    requested: str | None,
    allowed: set[str],
    *,
    default: str,
) -> str:
    if requested in allowed:
        return requested
    return default


def _write_log_header(log_path: Path, command: list[str]) -> None:
    log_path.write_text(
        "Command:\n"
        + json.dumps(command, ensure_ascii=False, indent=2)
        + "\n\nstdout:\n",
        encoding="utf-8",
    )


def _append_log(log_path: Path, stdout: str | bytes | None, stderr: str | bytes | None) -> None:
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(_ensure_text(stdout))
        handle.write("\n\nstderr:\n")
        handle.write(_ensure_text(stderr))
        handle.write("\n")


def _append_log_text(log_path: Path, text: str) -> None:
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _ensure_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _failed_result(
    request: DownloadRequest,
    output_dir: Path,
    log_path: Path,
    result_path: Path,
    error: ErrorState,
    *,
    downloaded_files: list[Path] | None = None,
) -> DownloadResult:
    return DownloadResult(
        status="failed",
        source_url=request.source_url,
        selected_format_id=request.format_id,
        output_dir=str(output_dir),
        downloaded_files=[str(path) for path in (downloaded_files or [])],
        metadata_path=str(result_path),
        log_path=str(log_path),
        errors=[error],
    )


def _cancelled_result(
    request: DownloadRequest,
    output_dir: Path,
    log_path: Path,
    result_path: Path,
    *,
    downloaded_files: list[Path] | None = None,
) -> DownloadResult:
    return DownloadResult(
        status="cancelled",
        source_url=request.source_url,
        selected_format_id=request.format_id,
        output_dir=str(output_dir),
        downloaded_files=[str(path) for path in (downloaded_files or [])],
        metadata_path=str(result_path),
        log_path=str(log_path),
    )


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


def _parse_ytdlp_progress_line(line: str) -> tuple[str | None, float | None]:
    """Return a job step and optional percent parsed from one yt-dlp output line."""

    if "[Merger]" in line or "Merging formats" in line or "Deleting original file" in line:
        return "merging_or_postprocessing", None
    if "[download]" in line:
        match = YTDLP_PROGRESS_RE.search(line)
        if match:
            return "downloading", min(float(match.group(1)), 100.0)
        if "Destination:" in line or "has already been downloaded" in line:
            return "downloading", None
    if "[ExtractAudio]" in line or "[Metadata]" in line or "[VideoRemuxer]" in line:
        return "merging_or_postprocessing", None
    return None, None


def _stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)


def _list_downloaded_files(output_dir: Path) -> list[Path]:
    if not output_dir.exists():
        return []
    return sorted(
        path
        for path in output_dir.iterdir()
        if path.is_file() and not path.name.startswith(".")
    )


def _compact_details(value: str | bytes | None) -> str | None:
    text = _ensure_text(value).strip()
    if not text:
        return None
    return text[-2000:]


def _source_id_from_url(url: str) -> str:
    parsed = urlparse(url)
    query_id = parse_qs(parsed.query).get("v", [None])[0]
    if query_id:
        return query_id
    path_part = parsed.path.strip("/").split("/")[-1]
    return path_part or parsed.netloc or "download"
