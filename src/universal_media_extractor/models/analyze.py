"""Analyze-result Pydantic models.

These models intentionally represent the normalized contract from Phase 3.
They do not embed raw yt-dlp output; callers should store raw artifacts
separately and point to them with ``raw_reference_path``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


SourceType = Literal["url", "local_file", "youtube", "unknown"]
MediaType = Literal["audio", "video", "combined"]
SubtitleType = Literal["manual", "automatic"]
WarningSeverity = Literal["info", "warning", "blocking"]
AvailabilityState = Literal[
    "public",
    "unlisted",
    "private",
    "premium_only",
    "subscriber_only",
    "needs_auth",
    "unknown",
]
LiveStatus = Literal[
    "not_live",
    "is_live",
    "is_upcoming",
    "was_live",
    "post_live",
    "unknown",
]
WarningCode = Literal[
    "unsupported_source",
    "login_required",
    "cookies_may_be_required",
    "no_subtitles",
    "no_automatic_captions",
    "no_audio_formats",
    "no_video_formats",
    "platform_terms_warning",
    "format_size_unknown",
    "best_effort_extractor",
    "analysis_only_not_download_tested",
]
ErrorCode = Literal[
    "unsupported_source",
    "network_error",
    "login_required",
    "cookies_required",
    "drm_protected",
    "region_restricted",
    "private_or_deleted",
    "no_requested_format",
    "disk_full",
    "permission_denied",
    "engine_outdated",
    "ytdlp_not_found",
    "ffmpeg_not_found",
    "whisper_not_found",
    "extractor_failed",
    "transcription_failed",
    "invalid_input_file",
    "rights_confirmation_required",
    "invalid_output",
    "timeout",
    "unknown_error",
]


class ContractModel(BaseModel):
    """Base config for stable API contract models."""

    model_config = ConfigDict(extra="forbid")


class UploaderInfo(ContractModel):
    """Normalized uploader/channel metadata."""

    name: str | None = Field(default=None)
    id: str | None = Field(default=None)
    url: str | None = Field(default=None)
    channel_name: str | None = Field(default=None)
    channel_id: str | None = Field(default=None)
    channel_url: str | None = Field(default=None)


class AccessState(ContractModel):
    """Source availability and access signals."""

    availability: AvailabilityState | str | None = Field(default=None)
    is_live: bool = Field(default=False)
    live_status: LiveStatus | str | None = Field(default=None)
    age_limit: int | None = Field(default=None, ge=0)
    has_drm: bool | None = Field(default=None)
    login_required: bool = Field(default=False)
    cookies_required: bool = Field(default=False)
    playable_in_embed: bool | None = Field(default=None)


class MediaOption(ContractModel):
    """A single normalized media format option."""

    id: str = Field(min_length=1)
    format_id: str = Field(min_length=1)
    type: MediaType
    container: str | None = Field(default=None)
    ext: str | None = Field(default=None)
    codec: str | None = Field(default=None)
    audio_codec: str | None = Field(default=None)
    video_codec: str | None = Field(default=None)
    resolution: str | None = Field(default=None)
    width: int | None = Field(default=None, ge=0)
    height: int | None = Field(default=None, ge=0)
    fps: float | None = Field(default=None, ge=0)
    bitrate: float | None = Field(default=None, ge=0)
    audio_bitrate: float | None = Field(default=None, ge=0)
    video_bitrate: float | None = Field(default=None, ge=0)
    sample_rate: int | None = Field(default=None, ge=0)
    audio_channels: int | None = Field(default=None, ge=0)
    filesize: int | None = Field(default=None, ge=0)
    filesize_approx: int | None = Field(default=None, ge=0)
    language: str | None = Field(default=None)
    protocol: str | None = Field(default=None)
    dynamic_range: str | None = Field(default=None)
    quality_label: str | None = Field(default=None)
    is_default_recommended: bool = Field(default=False)
    is_downloadable: bool = Field(default=True)
    requires_merge: bool = Field(default=False)
    display_label: str = Field(min_length=1)
    warnings: list[WarningCode] = Field(default_factory=list)


class RecommendedOptions(ContractModel):
    """Recommended format IDs for simple UI choices."""

    best_audio_format_id: str | None = Field(default=None)
    best_video_format_id: str | None = Field(default=None)
    best_combined_format_id: str | None = Field(default=None)
    simple_mode_defaults: dict[str, str] = Field(default_factory=dict)


class MediaOptions(ContractModel):
    """Grouped media options for selectors."""

    audio: list[MediaOption] = Field(default_factory=list)
    video: list[MediaOption] = Field(default_factory=list)
    combined: list[MediaOption] = Field(default_factory=list)
    recommended: RecommendedOptions = Field(default_factory=RecommendedOptions)


class SubtitleOption(ContractModel):
    """A normalized subtitle or automatic-caption track."""

    language: str = Field(min_length=1)
    language_label: str | None = Field(default=None)
    type: SubtitleType
    formats: list[str] = Field(default_factory=list)
    is_available: bool = Field(default=True)
    display_label: str = Field(min_length=1)


class WarningState(ContractModel):
    """A stable warning for UI display."""

    code: WarningCode
    message: str = Field(min_length=1)
    severity: WarningSeverity = Field(default="warning")
    related_field: str | None = Field(default=None)


class ErrorState(ContractModel):
    """A recoverable or blocking analysis error."""

    code: ErrorCode
    message: str = Field(min_length=1)
    technical_details: str | None = Field(default=None)
    recoverable: bool = Field(default=False)
    suggested_user_action: str | None = Field(default=None)


class LegalSafetyState(ContractModel):
    """User confirmation required before download or processing."""

    user_confirmed_rights: bool = Field(default=False)
    confirmation_text: str = Field(min_length=1)
    required_before_download: bool = Field(default=True)
    required_before_transcription: bool = Field(default=True)
    accepted_at: datetime | None = Field(default=None)


class AnalyzeResult(ContractModel):
    """Normalized analyze result returned by a future analyze endpoint."""

    schema_version: str = Field(default="1.0")
    analysis_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    source_type: SourceType
    extractor: str | None = Field(default=None)
    extractor_key: str | None = Field(default=None)
    title: str | None = Field(default=None)
    duration_seconds: float | None = Field(default=None, ge=0)
    duration_label: str | None = Field(default=None)
    thumbnail_url: str | None = Field(default=None)
    webpage_url: str | None = Field(default=None)
    uploader: UploaderInfo | None = Field(default=None)
    availability: AvailabilityState | str | None = Field(default=None)
    access_state: AccessState = Field(default_factory=AccessState)
    media_options: MediaOptions = Field(default_factory=MediaOptions)
    subtitles: list[SubtitleOption] = Field(default_factory=list)
    automatic_captions: list[SubtitleOption] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    warnings: list[WarningState] = Field(default_factory=list)
    errors: list[ErrorState] = Field(default_factory=list)
    legal_safety: LegalSafetyState
    raw_reference_path: str | None = Field(default=None)
    analyzed_at: datetime
