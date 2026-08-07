"""Batch queue models for multiple URL downloads."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import Field, field_validator

from universal_media_extractor.models.analyze import ContractModel, ErrorState, WarningState
from universal_media_extractor.models.download import DownloadMode, DownloadResult, DuplicatePolicy


BatchImportSource = Literal["textarea", "clipboard", "text_file"]
BatchStatus = Literal["queued", "running", "succeeded", "failed", "cancelled"]
BatchItemStatus = Literal["queued", "running", "succeeded", "failed", "cancelled", "skipped"]
BatchPreset = Literal[
    "best_video",
    "video_1080p",
    "video_720p",
    "smaller_video",
    "audio_m4a",
    "audio_mp3",
    "subtitles",
    "archive_pack",
]


class BatchInvalidLine(ContractModel):
    line_number: int
    text: str
    reason: str


class BatchUrlImportRequest(ContractModel):
    text: str = Field(min_length=1)
    source: BatchImportSource = "textarea"


class BatchUrlImportResult(ContractModel):
    source: BatchImportSource = "textarea"
    urls: list[str] = Field(default_factory=list)
    invalid_lines: list[BatchInvalidLine] = Field(default_factory=list)
    duplicate_count: int = 0


class PlaylistAnalyzeRequest(ContractModel):
    source_url: str

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: str) -> str:
        value = value.strip()
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("source_url must be an http or https URL")
        return value


class PlaylistItem(ContractModel):
    item_id: str
    title: str | None = None
    url: str | None = None
    duration_seconds: float | None = None
    playlist_index: int | None = None
    selected: bool = True
    warnings: list[WarningState] = Field(default_factory=list)


class PlaylistAnalyzeResult(ContractModel):
    source_url: str
    is_playlist: bool = False
    title: str | None = None
    extractor: str | None = None
    item_count: int = 0
    items: list[PlaylistItem] = Field(default_factory=list)
    warnings: list[WarningState] = Field(default_factory=list)
    errors: list[ErrorState] = Field(default_factory=list)
    raw_reference_path: str | None = None
    analyzed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BatchDownloadItemRequest(ContractModel):
    source_url: str
    source_title: str | None = None
    playlist_index: int | None = None
    selected: bool = True

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: str) -> str:
        value = value.strip()
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("source_url must be an http or https URL")
        return value


class BatchCreateRequest(ContractModel):
    items: list[BatchDownloadItemRequest] = Field(min_length=1)
    preset: BatchPreset = "best_video"
    user_confirmed_rights: bool = False
    output_base_dir: str | None = None
    output_template: str = "{title}"
    duplicate_policy: DuplicatePolicy = "rename"
    concurrency: int = Field(default=1, ge=1, le=3)


class BatchItem(ContractModel):
    item_id: str
    order: int
    source_url: str
    source_title: str | None = None
    playlist_index: int | None = None
    status: BatchItemStatus = "queued"
    job_id: str | None = None
    result: DownloadResult | None = None
    error: ErrorState | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Batch(ContractModel):
    batch_id: str
    status: BatchStatus = "queued"
    preset: BatchPreset = "best_video"
    mode: DownloadMode = "combined"
    concurrency: int = 1
    items: list[BatchItem] = Field(default_factory=list)
    total_count: int = 0
    queued_count: int = 0
    running_count: int = 0
    succeeded_count: int = 0
    failed_count: int = 0
    cancelled_count: int = 0
    skipped_count: int = 0
    warnings: list[WarningState] = Field(default_factory=list)
    errors: list[ErrorState] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
