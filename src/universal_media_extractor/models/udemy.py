"""Udemy course export models."""

from __future__ import annotations

from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, field_validator, model_validator

from universal_media_extractor.models.analyze import (
    ContractModel,
    ErrorState,
    WarningState,
)


UdemyCourseStatus = Literal["succeeded", "failed", "blocked", "cancelled"]
UdemyCourseQuality = Literal["best", "1080", "720", "480"]
UdemyCourseOutputFormat = Literal["mp4", "mkv", "webm"]
UdemyAuthSource = Literal["chrome", "manual_cookies"]


class UdemyLectureOption(ContractModel):
    """One lecture discovered during course analysis."""

    lecture_id: str | None = Field(default=None)
    title: str = Field(min_length=1)
    section_title: str | None = Field(default=None)
    section_index: int | None = Field(default=None, ge=0)
    lecture_index: int | None = Field(default=None, ge=0)
    duration_seconds: float | None = Field(default=None, ge=0)
    webpage_url: str | None = Field(default=None)
    is_downloadable: bool | None = Field(default=None)


class UdemyCourseSection(ContractModel):
    """A normalized Udemy course section."""

    title: str = Field(min_length=1)
    section_index: int = Field(ge=0)
    lectures: list[UdemyLectureOption] = Field(default_factory=list)


class UdemyCourseAnalyzeRequest(ContractModel):
    """Request to inspect a Udemy course without downloading media."""

    course_url: str = Field(min_length=1)
    auth_source: UdemyAuthSource = "chrome"
    cookies_path: str | None = Field(default=None)

    @field_validator("course_url", mode="after")
    @classmethod
    def validate_udemy_url(cls, value: str) -> str:
        stripped = value.strip()
        parsed = urlparse(stripped)
        if parsed.scheme not in {"http", "https"} or "udemy." not in parsed.netloc:
            raise ValueError("Enter a valid Udemy course URL.")
        return stripped

    @field_validator("cookies_path", mode="after")
    @classmethod
    def strip_cookies_path(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @model_validator(mode="after")
    def require_manual_cookies_path(self) -> "UdemyCourseAnalyzeRequest":
        if self.auth_source == "manual_cookies" and not self.cookies_path:
            raise ValueError("Manual cookies mode requires a cookies.txt path.")
        return self


class UdemyCourseAnalyzeResult(ContractModel):
    """Normalized result of a Udemy course analysis attempt."""

    status: UdemyCourseStatus
    course_url: str
    course_title: str | None = Field(default=None)
    extractor: str | None = Field(default=None)
    sections: list[UdemyCourseSection] = Field(default_factory=list)
    lecture_count: int = Field(default=0, ge=0)
    output_base_dir: str | None = Field(default=None)
    raw_reference_path: str | None = Field(default=None)
    errors: list[ErrorState] = Field(default_factory=list)
    warnings: list[WarningState] = Field(default_factory=list)


class UdemyCourseDownloadRequest(ContractModel):
    """Request to download a user-owned Udemy course best-effort."""

    course_url: str = Field(min_length=1)
    auth_source: UdemyAuthSource = "chrome"
    cookies_path: str | None = Field(default=None)
    user_confirmed_rights: bool = False
    output_base_dir: str | None = Field(default=None)
    course_title: str | None = Field(default=None)
    quality: UdemyCourseQuality = "best"
    output_format: UdemyCourseOutputFormat = "mp4"
    include_subtitles: bool = True
    include_resources: bool = False
    lecture_limit: int | None = Field(default=None, ge=1)

    @field_validator("course_url", mode="after")
    @classmethod
    def validate_udemy_url(cls, value: str) -> str:
        stripped = value.strip()
        parsed = urlparse(stripped)
        if parsed.scheme not in {"http", "https"} or "udemy." not in parsed.netloc:
            raise ValueError("Enter a valid Udemy course URL.")
        return stripped

    @field_validator("cookies_path", mode="after")
    @classmethod
    def strip_cookies_path(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @field_validator("output_base_dir", "course_title", mode="after")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @model_validator(mode="after")
    def require_manual_cookies_path(self) -> "UdemyCourseDownloadRequest":
        if self.auth_source == "manual_cookies" and not self.cookies_path:
            raise ValueError("Manual cookies mode requires a cookies.txt path.")
        return self


class UdemyCourseDownloadResult(ContractModel):
    """Result of a Udemy course download attempt."""

    status: UdemyCourseStatus
    course_url: str
    course_title: str | None = Field(default=None)
    output_dir: str | None = Field(default=None)
    downloaded_files: list[str] = Field(default_factory=list)
    metadata_path: str | None = Field(default=None)
    log_path: str | None = Field(default=None)
    errors: list[ErrorState] = Field(default_factory=list)
    warnings: list[WarningState] = Field(default_factory=list)
