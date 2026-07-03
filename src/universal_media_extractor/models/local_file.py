"""Local file analysis models."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from universal_media_extractor.models.analyze import (
    ContractModel,
    ErrorState,
    WarningState,
)


LocalMediaType = Literal["audio", "video", "unknown"]


class LocalFileStreamInfo(ContractModel):
    """One ffprobe stream summary for a local media file."""

    index: int | None = Field(default=None)
    codec_type: str | None = Field(default=None)
    codec_name: str | None = Field(default=None)
    duration_seconds: float | None = Field(default=None)
    width: int | None = Field(default=None)
    height: int | None = Field(default=None)
    sample_rate: int | None = Field(default=None)
    channels: int | None = Field(default=None)
    bit_rate: int | None = Field(default=None)


class LocalFileAnalyzeResult(ContractModel):
    """Normalized metadata result for one uploaded local file."""

    filename: str
    saved_path: str | None = Field(default=None)
    output_dir: str | None = Field(default=None)
    media_type: LocalMediaType = "unknown"
    duration_seconds: float | None = Field(default=None)
    size_bytes: int | None = Field(default=None)
    format_name: str | None = Field(default=None)
    format_long_name: str | None = Field(default=None)
    streams: list[LocalFileStreamInfo] = Field(default_factory=list)
    errors: list[ErrorState] = Field(default_factory=list)
    warnings: list[WarningState] = Field(default_factory=list)
