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

from universal_media_extractor.error_mapping import compact_details, normalize_cli_error
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
                technical_details=compact_details(getattr(exc, "stderr", None)),
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
    haystack = (stderr or "").lower()
    if "unsupported url" in haystack or "no suitable extractor" in haystack:
        return ErrorState(
            code="unsupported_source",
            message="This source is not supported by yt-dlp.",
            technical_details=compact_details(stderr),
            recoverable=False,
            suggested_user_action="Use a supported public URL or choose a local file.",
        )
    return normalize_cli_error(
        stderr or f"yt-dlp exited with code {returncode}.",
        default_code="extractor_failed",
        default_message="yt-dlp analysis failed.",
        default_suggested_user_action="Retry analysis or inspect the URL/source availability.",
        engine="yt-dlp",
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


def _safe_filename(value: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)
    return safe or "unknown"
