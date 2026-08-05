"""Job models for service-layer orchestration and local history."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from universal_media_extractor.models.analyze import ErrorState


JobStatus = Literal["queued", "running", "succeeded", "failed", "cancelled"]


class Job(BaseModel):
    """Local job state for long-running operations."""

    model_config = ConfigDict(extra="forbid")

    job_id: str = Field(min_length=1)
    task_type: str = Field(min_length=1)
    status: JobStatus = Field(default="queued")
    current_step: str | None = Field(default=None)
    progress_percent: float | None = Field(default=None, ge=0, le=100)
    payload: dict[str, Any] = Field(default_factory=dict)
    result: Any | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = Field(default=None)
    finished_at: datetime | None = Field(default=None)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error: ErrorState | None = Field(default=None)
    cancel_requested: bool = Field(default=False)
    retry_of_job_id: str | None = Field(default=None)


class JobHistoryResult(BaseModel):
    """Persistent local job history response."""

    model_config = ConfigDict(extra="forbid")

    jobs: list[Job] = Field(default_factory=list)


class JobHistoryClearResult(BaseModel):
    """Result of clearing terminal job history without deleting output files."""

    model_config = ConfigDict(extra="forbid")

    cleared_count: int = Field(ge=0)
    remaining_count: int = Field(ge=0)
    files_deleted: bool = False
