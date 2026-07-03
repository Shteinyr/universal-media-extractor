"""In-memory job service for future route polling."""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4

from universal_media_extractor.models import ErrorState, Job
from universal_media_extractor.models.job import JobStatus


TERMINAL_STATUSES: set[JobStatus] = {"succeeded", "failed", "cancelled"}


class JobService:
    """Minimal in-memory job registry."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._processes: dict[str, subprocess.Popen[Any]] = {}
        self._lock = Lock()

    def create_job(self, task_type: str, payload: dict[str, Any]) -> Job:
        """Create a queued job."""

        job = Job(
            job_id=f"job-{uuid4().hex}",
            task_type=task_type,
            status="queued",
            current_step="queued",
            payload=dict(payload),
        )
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> Job | None:
        """Return a job by ID, if it exists."""

        with self._lock:
            return self._jobs.get(job_id)

    def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        error: ErrorState | None = None,
        *,
        current_step: str | None = None,
        progress_percent: float | None = None,
        result: Any | None = None,
    ) -> Job:
        """Update job status and optional error."""

        job = self._require_job(job_id)
        now = datetime.now(timezone.utc)
        update: dict[str, Any] = {
            "status": status,
            "error": error,
            "updated_at": now,
        }
        if current_step is not None:
            update["current_step"] = current_step
        if progress_percent is not None:
            update["progress_percent"] = progress_percent
        if result is not None:
            update["result"] = result
        if status == "running" and job.started_at is None:
            update["started_at"] = now
        if status in TERMINAL_STATUSES:
            update["finished_at"] = now
        updated = job.model_copy(
            update=update
        )
        with self._lock:
            self._jobs[job_id] = updated
        return updated

    def update_job_step(
        self,
        job_id: str,
        current_step: str,
        progress_percent: float | None = None,
    ) -> Job:
        """Update a running job's current step."""

        job = self._require_job(job_id)
        update: dict[str, Any] = {
            "current_step": current_step,
            "updated_at": datetime.now(timezone.utc),
        }
        if progress_percent is not None:
            update["progress_percent"] = progress_percent
        updated = job.model_copy(update=update)
        with self._lock:
            self._jobs[job_id] = updated
        return updated

    def finish_job(self, job_id: str, result: Any) -> Job:
        """Mark a job succeeded with a serialized result."""

        return self.update_job_status(
            job_id,
            "succeeded",
            current_step="succeeded",
            progress_percent=100,
            result=result,
        )

    def fail_job(self, job_id: str, error: ErrorState, result: Any | None = None) -> Job:
        """Mark a job failed with error and optional partial result."""

        return self.update_job_status(
            job_id,
            "failed",
            error=error,
            current_step="failed",
            result=result,
        )

    def cancel_job(self, job_id: str) -> Job:
        """Request cancellation for a non-terminal job."""

        job = self._require_job(job_id)
        if job.status in TERMINAL_STATUSES:
            return job
        if job.status == "queued":
            updated = job.model_copy(
                update={
                    "status": "cancelled",
                    "cancel_requested": True,
                    "current_step": "cancelled",
                    "finished_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                }
            )
        else:
            process = self.get_subprocess(job_id)
            if process is not None and process.poll() is not None:
                updated = job.model_copy(
                    update={
                        "current_step": "cancel requested after subprocess finished",
                        "updated_at": datetime.now(timezone.utc),
                    }
                )
                with self._lock:
                    self._jobs[job_id] = updated
                return updated

            updated = job.model_copy(
                update={
                    "cancel_requested": True,
                    "current_step": "cancel requested",
                    "updated_at": datetime.now(timezone.utc),
                }
            )
        with self._lock:
            self._jobs[job_id] = updated
        if job.status == "running":
            self._try_stop_registered_process(job_id)
            return self.get_job(job_id) or updated
        return updated

    def register_subprocess(self, job_id: str, process: subprocess.Popen[Any]) -> None:
        """Associate a currently running subprocess with a job."""

        self._require_job(job_id)
        with self._lock:
            self._processes[job_id] = process

    def clear_subprocess(
        self,
        job_id: str,
        process: subprocess.Popen[Any] | None = None,
    ) -> None:
        """Remove a job subprocess reference when it has finished."""

        with self._lock:
            current = self._processes.get(job_id)
            if process is None or current is process:
                self._processes.pop(job_id, None)

    def get_subprocess(self, job_id: str) -> subprocess.Popen[Any] | None:
        """Return the registered subprocess for a job, if any."""

        with self._lock:
            return self._processes.get(job_id)

    def is_cancel_requested(self, job_id: str) -> bool:
        """Return whether a job has an active cancellation request."""

        job = self.get_job(job_id)
        return bool(job and job.cancel_requested)

    def _try_stop_registered_process(self, job_id: str) -> None:
        process = self.get_subprocess(job_id)
        if process is None:
            self._record_cancel_limitation(
                job_id,
                "Cancel was requested, but no active subprocess was registered at that moment.",
            )
            return
        if process.poll() is not None:
            return

        try:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
        except Exception as exc:  # pragma: no cover - defensive OS/process safety
            self._record_cancel_limitation(
                job_id,
                f"Cancel was requested, but the subprocess could not be stopped: {exc}",
            )
            return

        job = self.get_job(job_id)
        if job and job.status not in TERMINAL_STATUSES:
            updated = job.model_copy(
                update={
                    "status": "cancelled",
                    "cancel_requested": True,
                    "current_step": "cancelled",
                    "finished_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                }
            )
            with self._lock:
                self._jobs[job_id] = updated

    def _record_cancel_limitation(self, job_id: str, details: str) -> None:
        job = self.get_job(job_id)
        if job is None or job.status in TERMINAL_STATUSES:
            return
        updated = job.model_copy(
            update={
                "cancel_requested": True,
                "current_step": "cancel requested",
                "error": ErrorState(
                    code="unknown_error",
                    message="Cancel was requested but could not immediately stop active work.",
                    technical_details=details,
                    recoverable=True,
                ),
                "updated_at": datetime.now(timezone.utc),
            }
        )
        with self._lock:
            self._jobs[job_id] = updated

    def _require_job(self, job_id: str) -> Job:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                raise KeyError(f"Job not found: {job_id}")
            return job
