"""Safe yt-dlp URL analysis wrapper.

This module only performs metadata analysis with ``yt-dlp --simulate
--dump-json``. It does not download media, choose formats, invoke ffmpeg,
run Whisper, or expose FastAPI routes.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from universal_media_extractor.models import (
    AccessState,
    AnalyzeResult,
    ErrorState,
    LegalSafetyState,
)
from universal_media_extractor.normalizers import normalize_ytdlp_info


RIGHTS_CONFIRMATION_TEXT = (
    "I confirm that I own this media or have the necessary rights to download, "
    "extract, convert, and/or transcribe it locally."
)


def analyze_url_with_ytdlp(
    url: str,
    *,
    timeout_seconds: int = 60,
    raw_output_dir: Path | None = None,
) -> AnalyzeResult:
    """Analyze a URL with yt-dlp without downloading media."""

    command = ["yt-dlp", "--simulate", "--dump-json", url]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        return _error_result(
            url,
            ErrorState(
                code="timeout",
                message="yt-dlp analysis timed out.",
                technical_details=_compact_details(getattr(exc, "stderr", None)),
                recoverable=True,
                suggested_user_action="Try again later or use a shorter/public source.",
            ),
        )
    except FileNotFoundError:
        return _error_result(
            url,
            ErrorState(
                code="ytdlp_not_found",
                message="yt-dlp was not found on PATH.",
                technical_details=None,
                recoverable=True,
                suggested_user_action="Install yt-dlp or fix PATH, then retry analysis.",
            ),
        )

    if completed.returncode != 0:
        stderr = completed.stderr or completed.stdout
        return _error_result(
            url,
            _classify_ytdlp_error(stderr, completed.returncode),
        )

    try:
        raw = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return _error_result(
            url,
            ErrorState(
                code="invalid_output",
                message="yt-dlp returned invalid JSON.",
                technical_details=str(exc),
                recoverable=True,
                suggested_user_action="Retry analysis or inspect yt-dlp output.",
            ),
        )

    if not isinstance(raw, dict):
        return _error_result(
            url,
            ErrorState(
                code="invalid_output",
                message="yt-dlp JSON output was not an object.",
                technical_details=f"Output type: {type(raw).__name__}",
                recoverable=True,
                suggested_user_action="Retry analysis or inspect yt-dlp output.",
            ),
        )

    raw_reference_path = _save_raw_json(raw, raw_output_dir) if raw_output_dir else None
    return normalize_ytdlp_info(raw, raw_reference_path=raw_reference_path)


def _save_raw_json(raw: dict[str, Any], raw_output_dir: Path) -> str:
    raw_output_dir.mkdir(parents=True, exist_ok=True)
    media_id = _safe_filename(str(raw.get("id") or "unknown"))
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = raw_output_dir / f"ytdlp_{media_id}_{timestamp}.json"
    path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _classify_ytdlp_error(stderr: str | None, returncode: int) -> ErrorState:
    details = _compact_details(stderr)
    haystack = (stderr or "").lower()

    if "unsupported url" in haystack or "no suitable extractor" in haystack:
        return ErrorState(
            code="unsupported_source",
            message="This source is not supported by yt-dlp.",
            technical_details=details,
            recoverable=False,
            suggested_user_action="Use a supported public URL or choose a local file.",
        )
    if "timed out" in haystack or "timeout" in haystack:
        return ErrorState(
            code="network_error",
            message="yt-dlp reported a network timeout.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Check network access and retry.",
        )
    if "unable to download webpage" in haystack or "network" in haystack:
        return ErrorState(
            code="network_error",
            message="yt-dlp could not access the source.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Check the URL and network access, then retry.",
        )
    if "login" in haystack or "sign in" in haystack or "private" in haystack:
        return ErrorState(
            code="login_required",
            message="This source appears to require login or private access.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Use a public URL or wait for future manual login/cookies support.",
        )
    if "cookies" in haystack or "cookie" in haystack:
        return ErrorState(
            code="cookies_required",
            message="This source appears to require cookies.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Use a public URL or wait for future manual cookies support.",
        )

    return ErrorState(
        code="extractor_failed",
        message="yt-dlp analysis failed.",
        technical_details=details or f"yt-dlp exited with code {returncode}.",
        recoverable=True,
        suggested_user_action="Retry analysis or inspect the URL/source availability.",
    )


def _error_result(url: str, error: ErrorState) -> AnalyzeResult:
    return AnalyzeResult(
        schema_version="1.0",
        analysis_id=f"error-{error.code}",
        source_url=url,
        source_type="url",
        extractor=None,
        extractor_key=None,
        title=None,
        duration_seconds=None,
        duration_label=None,
        thumbnail_url=None,
        webpage_url=None,
        uploader=None,
        availability="unknown",
        access_state=AccessState(availability="unknown"),
        errors=[error],
        legal_safety=LegalSafetyState(
            user_confirmed_rights=False,
            confirmation_text=RIGHTS_CONFIRMATION_TEXT,
            required_before_download=True,
            required_before_transcription=True,
            accepted_at=None,
        ),
        raw_reference_path=None,
        analyzed_at=datetime.now(timezone.utc),
    )


def _compact_details(value: Any, max_length: int = 1200) -> str | None:
    if value is None:
        return None
    text = value.decode("utf-8", errors="replace") if isinstance(value, bytes) else str(value)
    text = text.strip()
    if not text:
        return None
    return text[:max_length]


def _safe_filename(value: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)
    return safe or "unknown"
