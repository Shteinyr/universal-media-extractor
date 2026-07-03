"""Output index models."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field

from universal_media_extractor.models.analyze import ContractModel


OutputSourceType = Literal["url", "local_file", "unknown"]
OutputDeleteStatus = Literal["deleted", "not_found", "blocked"]


class OutputSummary(ContractModel):
    """Summary for one user output directory."""

    output_id: str = Field(min_length=1)
    output_dir: str
    created_at: datetime
    source_type: OutputSourceType = "unknown"
    title_or_filename: str | None = Field(default=None)
    has_media: bool = False
    has_transcript: bool = False
    has_summary_prompt: bool = False
    total_size_bytes: int = Field(default=0, ge=0)
    files_count: int = Field(default=0, ge=0)
    last_modified_at: datetime


class OutputListResult(ContractModel):
    """List of user outputs under the configured outputs directory."""

    outputs_base_dir: str
    outputs: list[OutputSummary] = Field(default_factory=list)


class OutputDeleteResult(ContractModel):
    """Safe delete result for one output directory."""

    output_id: str
    status: OutputDeleteStatus
    output_dir: str | None = Field(default=None)
    message: str
