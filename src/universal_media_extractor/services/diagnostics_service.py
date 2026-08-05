"""Safe diagnostics bundle generation for local jobs."""

from __future__ import annotations

import platform
import re
import subprocess
import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from universal_media_extractor.error_mapping import normalize_cli_error
from universal_media_extractor.models import DiagnosticBundle, DiagnosticLog, ErrorState, Job

VersionRunner = Callable[[list[str]], str | None]

SENSITIVE_KEY_RE = re.compile(r"(cookie|token|authorization|password|secret|bearer|keyring)", re.I)
PATH_KEY_RE = re.compile(r"(path|dir|file|folder)", re.I)
URL_KEY_RE = re.compile(r"(^url$|_url$|url_|source_url|course_url|webpage_url)", re.I)
TRANSCRIPT_KEY_RE = re.compile(r"(transcript_text|summary_prompt_text)", re.I)
URL_RE = re.compile(r"https?://[^\s\"'<>]+")
MAC_PATH_RE = re.compile(r"(?<![\w:])(?:~|/Users|/private|/var|/tmp)/[^\s\"'<>]+")
WIN_PATH_RE = re.compile(r"[A-Za-z]:\\[^\s\"'<>]+")
SECRET_LINE_RE = re.compile(r"(?im)^.*(?:cookie|token|authorization|password|secret|bearer|keyring).*$")


class DiagnosticsService:
    """Build redacted diagnostics that can be inspected before sharing."""

    def __init__(
        self,
        *,
        version_runner: VersionRunner | None = None,
        max_log_chars: int = 8000,
    ) -> None:
        self.version_runner = version_runner or _run_version_command
        self.max_log_chars = max_log_chars

    def build_job_bundle(self, job: Job, *, app_version: str) -> DiagnosticBundle:
        """Create a redacted diagnostics bundle for one in-memory job."""

        result = _as_mapping(job.result)
        error = _extract_error(job, result)
        log_paths = _extract_log_paths(result)
        logs = [self._read_redacted_log(path) for path in log_paths]

        return DiagnosticBundle(
            app_version=app_version,
            os_name=platform.system() or "unknown",
            os_version=platform.release() or "",
            architecture=platform.machine() or "",
            python_version=sys.version.split()[0],
            engine_versions=self._engine_versions(),
            job_id=job.job_id,
            task_type=job.task_type,
            job_status=job.status,
            current_step=job.current_step,
            extractor_type=_extract_extractor_type(job, result),
            normalized_error=error,
            redacted_payload=redact_value(job.payload),
            redacted_result_summary=_summarize_result(result),
            redacted_logs=logs,
        )

    def _engine_versions(self) -> dict[str, str | None]:
        return {
            "yt-dlp": self.version_runner(["yt-dlp", "--version"]),
            "ffmpeg": self.version_runner(["ffmpeg", "-version"]),
            "whisper": self.version_runner(["whisper", "--help"]),
        }

    def _read_redacted_log(self, path: Path) -> DiagnosticLog:
        name = path.name or "log"
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return DiagnosticLog(
                name=name,
                content=redact_text(f"Unable to read log: {exc}"),
                truncated=False,
            )
        truncated = len(content) > self.max_log_chars
        excerpt = content[-self.max_log_chars :] if truncated else content
        return DiagnosticLog(name=name, content=redact_text(excerpt), truncated=truncated)


def redact_value(value: Any) -> Any:
    """Return value with secrets, transcripts, full URLs, and local paths redacted."""

    if isinstance(value, Mapping):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if SENSITIVE_KEY_RE.search(key_text):
                redacted[key_text] = "<redacted-secret>"
            elif TRANSCRIPT_KEY_RE.search(key_text):
                redacted[key_text] = "<redacted-transcript>"
            elif URL_KEY_RE.search(key_text) or PATH_KEY_RE.search(key_text):
                redacted[key_text] = redact_text(str(item)) if item is not None else None
            else:
                redacted[key_text] = redact_value(item)
        return redacted
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, tuple):
        return [redact_value(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def redact_text(value: str) -> str:
    text = str(value)
    text = SECRET_LINE_RE.sub("<redacted-secret-line>", text)
    text = URL_RE.sub(_redact_url_match, text)
    text = MAC_PATH_RE.sub("<redacted-path>", text)
    text = WIN_PATH_RE.sub("<redacted-path>", text)
    return text


def _redact_url_match(match: re.Match[str]) -> str:
    parsed = urlparse(match.group(0))
    host = parsed.netloc or "url"
    return f"<redacted-url:{host}>"


def _run_version_command(command: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            shell=False,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    output = (completed.stdout or completed.stderr or "").strip()
    if not output:
        return None
    return output.splitlines()[0][:160]


def _as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    return {}


def _extract_error(job: Job, result: Mapping[str, Any]) -> ErrorState | None:
    raw_error = job.error
    if raw_error is None:
        errors = result.get("errors")
        if isinstance(errors, list) and errors:
            try:
                raw_error = ErrorState.model_validate(errors[0])
            except Exception:
                raw_error = None
    if raw_error is None:
        return None
    if raw_error.code in {
        "drm_protected",
        "region_restricted",
        "private_or_deleted",
        "no_requested_format",
        "disk_full",
        "permission_denied",
        "engine_outdated",
        "login_required",
        "cookies_required",
        "network_error",
        "unsupported_source",
    }:
        return raw_error.model_copy(update={"technical_details": redact_text(raw_error.technical_details or "") or None})
    normalized = normalize_cli_error(
        raw_error.technical_details,
        default_code=raw_error.code,
        default_message=raw_error.message,
        default_suggested_user_action=raw_error.suggested_user_action or "Retry or inspect diagnostics.",
        default_recoverable=raw_error.recoverable,
        engine="unknown",
    )
    return normalized.model_copy(update={"technical_details": redact_text(normalized.technical_details or "") or None})


def _extract_log_paths(result: Mapping[str, Any]) -> list[Path]:
    paths: list[Path] = []
    log_path = result.get("log_path")
    if isinstance(log_path, str) and log_path:
        paths.append(Path(log_path).expanduser())
    return paths


def _extract_extractor_type(job: Job, result: Mapping[str, Any]) -> str | None:
    if isinstance(result.get("extractor"), str):
        return result["extractor"]
    if job.task_type.startswith("udemy"):
        return "udemy"
    if job.task_type in {"download", "analyze_url"}:
        return "yt-dlp"
    if job.task_type == "transcribe":
        return "whisper"
    return None


def _summarize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    if not result:
        return {}
    allowed_keys = {
        "status",
        "selected_format_id",
        "course_title",
        "lecture_count",
        "current_step",
        "progress_percent",
        "errors",
        "warnings",
    }
    summary = {key: result.get(key) for key in allowed_keys if key in result}
    if "downloaded_files" in result:
        files = result.get("downloaded_files") or []
        summary["downloaded_file_count"] = len(files) if isinstance(files, list) else 0
    for key in ["transcript_txt_path", "transcript_md_path", "transcript_json_path", "summary_prompt_path"]:
        if result.get(key):
            summary[key] = "<redacted-path>"
    return redact_value(summary)
