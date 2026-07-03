"""Download request/result models."""

from __future__ import annotations

from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, field_validator

from universal_media_extractor.models.analyze import (
    ContractModel,
    ErrorState,
    WarningState,
)


DownloadMode = Literal["audio", "video", "combined", "subtitles"]
DownloadStatus = Literal[
    "queued",
    "running",
    "succeeded",
    "failed",
    "cancelled",
    "blocked",
]


class DownloadRequest(ContractModel):
    """Request to download one selected media/subtitle option."""

    source_url: str = Field(min_length=1)
    format_id: str = Field(min_length=1)
    mode: DownloadMode
    user_confirmed_rights: bool = False
    output_base_dir: str | None = Field(default=None)
    source_title: str | None = Field(default=None)
    output_format: str | None = Field(default=None)

    @field_validator("source_url", mode="after")
    @classmethod
    def validate_http_url(cls, value: str) -> str:
        parsed = urlparse(value.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Enter a valid http or https URL.")
        return value.strip()

    @field_validator("format_id", mode="after")
    @classmethod
    def strip_format_id(cls, value: str) -> str:
        return value.strip()

    @field_validator("source_title", mode="after")
    @classmethod
    def strip_source_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @field_validator("output_format", mode="after")
    @classmethod
    def normalize_output_format(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip().lower().lstrip(".")
        return stripped or None


class DownloadResult(ContractModel):
    """Result of a local yt-dlp download attempt."""

    job_id: str | None = Field(default=None)
    status: DownloadStatus
    source_url: str
    selected_format_id: str
    output_dir: str | None = Field(default=None)
    downloaded_files: list[str] = Field(default_factory=list)
    metadata_path: str | None = Field(default=None)
    log_path: str | None = Field(default=None)
    errors: list[ErrorState] = Field(default_factory=list)
    warnings: list[WarningState] = Field(default_factory=list)
