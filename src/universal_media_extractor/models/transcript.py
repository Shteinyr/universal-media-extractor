"""Transcription request/result models."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from universal_media_extractor.models.analyze import (
    ContractModel,
    ErrorState,
    WarningState,
)


SourceMediaKind = Literal["audio", "video", "unknown"]
TranscriptFormat = Literal["txt", "md", "json"]
TranscriptionStatus = Literal[
    "queued",
    "running",
    "succeeded",
    "failed",
    "cancelled",
    "blocked",
]


class TranscriptionRequest(ContractModel):
    """Request to transcribe a local audio/video file."""

    input_file_path: str = Field(min_length=1)
    user_confirmed_rights: bool = False
    output_dir: str | None = Field(default=None)
    model: str = Field(default="tiny", min_length=1)
    language: str | None = Field(default=None)
    source_kind: SourceMediaKind = "unknown"
    transcript_format: TranscriptFormat = "txt"

    @field_validator("input_file_path", "model", mode="after")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("language", mode="after")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class TranscriptionResult(ContractModel):
    """Result of a local Whisper transcription attempt."""

    job_id: str | None = Field(default=None)
    status: TranscriptionStatus
    input_file_path: str
    output_dir: str | None = Field(default=None)
    transcript_txt_path: str | None = Field(default=None)
    transcript_md_path: str | None = Field(default=None)
    transcript_json_path: str | None = Field(default=None)
    transcript_format: TranscriptFormat | None = Field(default=None)
    summary_prompt_path: str | None = Field(default=None)
    transcript_text: str | None = Field(default=None)
    transcript_file_text: str | None = Field(default=None)
    summary_prompt_text: str | None = Field(default=None)
    extracted_audio_path: str | None = Field(default=None)
    log_path: str | None = Field(default=None)
    errors: list[ErrorState] = Field(default_factory=list)
    warnings: list[WarningState] = Field(default_factory=list)
