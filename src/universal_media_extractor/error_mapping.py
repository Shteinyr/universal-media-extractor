"""Normalize raw local engine errors into user-facing categories."""

from __future__ import annotations

from typing import Literal

from universal_media_extractor.models import ErrorState

EngineName = Literal["yt-dlp", "ffmpeg", "whisper", "udemy", "unknown"]


def normalize_cli_error(
    text: str | bytes | None,
    *,
    default_code: str = "extractor_failed",
    default_message: str = "Media operation failed.",
    default_suggested_user_action: str = "Retry or choose another source/output.",
    default_recoverable: bool = True,
    engine: EngineName = "unknown",
) -> ErrorState:
    """Map noisy CLI output to a stable, user-facing ErrorState."""

    details = compact_details(text)
    lowered = (details or "").lower()

    if _contains_any(lowered, ["drm", "encrypted", "decryption", "protected content"]):
        return ErrorState(
            code="drm_protected",
            message="This media appears to be DRM-protected.",
            technical_details=details,
            recoverable=False,
            suggested_user_action="The app does not bypass DRM. Use an official offline option if one is available.",
        )

    if _contains_any(lowered, ["not available in your country", "geo-restricted", "geo restricted", "region", "country"]):
        return ErrorState(
            code="region_restricted",
            message="This media is not available in the current region.",
            technical_details=details,
            recoverable=False,
            suggested_user_action="Try a source that is available in your region.",
        )

    if _contains_any(lowered, ["no space left on device", "disk full", "not enough space"]):
        return ErrorState(
            code="disk_full",
            message="There is not enough disk space to finish this operation.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Free disk space or choose another output folder, then retry.",
        )

    if _contains_any(lowered, ["permission denied", "operation not permitted", "access denied", "read-only file system"]):
        return ErrorState(
            code="permission_denied",
            message="The app does not have permission to write or read the selected path.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Choose a different folder or grant file access, then retry.",
        )

    if _contains_any(lowered, ["requested format is not available", "format not available", "format not found", "no video formats", "no audio formats", "no requested formats"]):
        return ErrorState(
            code="no_requested_format",
            message="The requested output format is not available for this source.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Analyze again and choose another output option.",
        )

    if _contains_any(lowered, ["private video", "this video is private", "has been removed", "deleted", "not found", "404", "does not exist", "unavailable"]):
        return ErrorState(
            code="private_or_deleted",
            message="This source is private, deleted, or no longer available.",
            technical_details=details,
            recoverable=False,
            suggested_user_action="Check the source page or use another link.",
        )

    if _contains_any(lowered, ["login", "sign in", "sign-in", "authenticated", "not enrolled", "purchased", "premium"]):
        return ErrorState(
            code="login_required",
            message="This source requires account access.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Use a public source or an explicitly supported private-session flow. The app does not bypass sign-in or access restrictions.",
        )

    if _contains_any(lowered, ["cookie", "cookies", "keyring", "browser", "http error 401", "http error 403", "forbidden"]):
        return ErrorState(
            code="cookies_required",
            message="This source requires a browser session or cookies.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Use an explicitly supported browser-session/manual-cookie flow only if you have access. The app does not bypass protected sources.",
        )

    if _contains_any(lowered, ["timed out", "timeout", "connection reset", "connection aborted", "temporary failure", "network", "unable to download webpage"]):
        return ErrorState(
            code="network_error",
            message="The app could not reach the source reliably.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Check the URL and network connection, then retry.",
        )

    if _contains_any(lowered, ["older than 90 days", "please update", "update yt-dlp", "unable to extract", "failed to extract"]):
        engine_label = engine if engine != "unknown" else "media engine"
        return ErrorState(
            code="engine_outdated",
            message=f"The {engine_label} extractor may be outdated for this source.",
            technical_details=details,
            recoverable=True,
            suggested_user_action="Update the local media engine and retry.",
        )

    return ErrorState(
        code=default_code,
        message=default_message,
        technical_details=details,
        recoverable=default_recoverable,
        suggested_user_action=default_suggested_user_action,
    )


def compact_details(value: str | bytes | None, max_length: int = 1200) -> str | None:
    if value is None:
        return None
    text = value.decode("utf-8", errors="replace") if isinstance(value, bytes) else str(value)
    text = text.strip()
    if not text:
        return None
    return text[-max_length:]


def _contains_any(value: str, needles: list[str]) -> bool:
    return any(needle in value for needle in needles)
