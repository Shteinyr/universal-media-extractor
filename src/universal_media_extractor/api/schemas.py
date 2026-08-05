"""Request and response schemas for the local API."""

from __future__ import annotations

from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator

from universal_media_extractor.models import (
    AnalyzeResult,
    DownloadRequest,
    Job,
    SourceMediaKind,
    TranscriptFormat,
    TranscriptionRequest,
    UdemyCourseAnalyzeRequest,
    UdemyCourseAnalyzeResult,
    UdemyCourseDownloadRequest,
)


class AppConfigResponse(BaseModel):
    """Feature flags for the local static UI."""

    model_config = ConfigDict(extra="forbid")

    service: Literal["universal-media-extractor"] = "universal-media-extractor"
    mode: Literal["local-only"] = "local-only"
    public_product_mode: bool = False
    course_mode_enabled: bool = True


class HealthResponse(BaseModel):
    """Static health response for local backend checks."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"] = "ok"
    service: Literal["universal-media-extractor"] = "universal-media-extractor"
    mode: Literal["local-only"] = "local-only"


class AnalyzeRequest(BaseModel):
    """URL analysis request."""

    model_config = ConfigDict(extra="forbid")

    source_type: Literal["url"] = "url"
    url: str = Field(min_length=1)
    user_confirmed_rights: bool = False

    @field_validator("url", mode="after")
    @classmethod
    def validate_http_url(cls, value: str) -> str:
        parsed = urlparse(value.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Enter a valid http or https URL.")
        return value.strip()


class AnalyzeResponse(BaseModel):
    """Analysis response with a minimal in-memory job and normalized result."""

    model_config = ConfigDict(extra="forbid")

    job: Job
    result: AnalyzeResult


class UdemyCourseAnalyzeResponse(BaseModel):
    """Udemy course analysis response."""

    model_config = ConfigDict(extra="forbid")

    result: UdemyCourseAnalyzeResult


class LocalFileTranscriptionRequest(BaseModel):
    """Request to transcribe a previously uploaded local file."""

    model_config = ConfigDict(extra="forbid")

    saved_file_path: str = Field(min_length=1)
    output_dir: str | None = Field(default=None)
    user_confirmed_rights: bool = False
    model: str = Field(default="tiny", min_length=1)
    language: str | None = Field(default=None)
    source_kind: SourceMediaKind = "unknown"
    transcript_format: TranscriptFormat = "txt"

    @field_validator("saved_file_path", "model", mode="after")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("output_dir", "language", mode="after")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None
