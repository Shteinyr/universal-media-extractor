"""Safe diagnostics bundle models."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import Field

from universal_media_extractor.models.analyze import ContractModel, ErrorState


class DiagnosticLog(ContractModel):
    """One redacted log excerpt included in a diagnostics bundle."""

    name: str = Field(min_length=1)
    content: str = ""
    truncated: bool = False


class DiagnosticBundle(ContractModel):
    """Redacted support bundle that users can inspect before sharing."""

    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    app_version: str = Field(min_length=1)
    os_name: str = Field(min_length=1)
    os_version: str = ""
    architecture: str = ""
    python_version: str = ""
    engine_versions: dict[str, str | None] = Field(default_factory=dict)
    job_id: str = Field(min_length=1)
    task_type: str = Field(min_length=1)
    job_status: str = Field(min_length=1)
    current_step: str | None = None
    extractor_type: str | None = None
    normalized_error: ErrorState | None = None
    redacted_payload: dict = Field(default_factory=dict)
    redacted_result_summary: dict = Field(default_factory=dict)
    redacted_logs: list[DiagnosticLog] = Field(default_factory=list)
    excluded_by_default: list[str] = Field(default_factory=lambda: [
        "cookies",
        "tokens",
        "passwords",
        "transcripts",
        "full_urls",
        "local_paths",
    ])
    sharing_note: str = "Inspect this redacted bundle before sharing it with support."
