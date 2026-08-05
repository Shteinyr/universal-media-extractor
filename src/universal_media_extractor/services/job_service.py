"""Job service with optional SQLite-backed local history."""

from __future__ import annotations

import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4

from universal_media_extractor.models import ErrorState, Job
from universal_media_extractor.models.job import JobStatus


TERMINAL_STATUSES: set[JobStatus] = {"succeeded", "failed", "cancelled"}
ACTIVE_STATUSES: set[JobStatus] = {"queued", "running"}


class JobService:
    """Local job registry with optional persistent SQLite storage."""

    def __init__(self, db_path: Path | None = None) -> None:
        self._jobs: dict[str, Job] = {}
        self._processes: dict[str, subprocess.Popen[Any]] = {}
        self._lock = Lock()
        self._db_path = db_path.expanduser().resolve() if db_path else None
        if self._db_path is not None:
            self._init_db()
            self._load_jobs_from_db()
            self.recover_interrupted_jobs()

    @property
    def db_path(self) -> Path | None:
        """Return the SQLite database path when persistence is enabled."""

        return self._db_path

    def create_job(
        self,
        task_type: str,
        payload: dict[str, Any],
        *,
        retry_of_job_id: str | None = None,
    ) -> Job:
        """Create a queued job."""

        job = Job(
            job_id=f"job-{uuid4().hex}",
            task_type=task_type,
            status="queued",
            current_step="queued",
            payload=dict(payload),
            retry_of_job_id=retry_of_job_id,
        )
        with self._lock:
            self._jobs[job.job_id] = job
            self._persist_job_locked(job)
        return job

    def get_job(self, job_id: str) -> Job | None:
        """Return a job by ID, if it exists."""

        with self._lock:
            return self._jobs.get(job_id)

    def list_jobs(
        self,
        *,
        limit: int = 100,
        status: JobStatus | None = None,
    ) -> list[Job]:
        """Return recent jobs sorted newest first."""

        with self._lock:
            jobs = list(self._jobs.values())
        if status is not None:
            jobs = [job for job in jobs if job.status == status]
        jobs.sort(key=lambda job: job.created_at, reverse=True)
        return jobs[: max(0, limit)]

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
        updated = job.model_copy(update=update)
        with self._lock:
            self._jobs[job_id] = updated
            self._persist_job_locked(updated)
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
            self._persist_job_locked(updated)
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

    def retry_job(self, job_id: str) -> Job:
        """Create a new queued job from a failed job's original payload."""

        failed_job = self._require_job(job_id)
        if failed_job.status != "failed":
            raise ValueError("Only failed jobs can be retried.")
        return self.create_job(
            failed_job.task_type,
            dict(failed_job.payload),
            retry_of_job_id=failed_job.job_id,
        )

    def clear_history(self) -> int:
        """Remove terminal jobs from history without touching output files."""

        with self._lock:
            terminal_ids = [
                job_id
                for job_id, job in self._jobs.items()
                if job.status in TERMINAL_STATUSES
            ]
            for job_id in terminal_ids:
                self._jobs.pop(job_id, None)
                self._processes.pop(job_id, None)
            self._delete_jobs_locked(terminal_ids)
            return len(terminal_ids)

    def recover_interrupted_jobs(self) -> int:
        """Convert persisted queued/running jobs into clear failed states on startup."""

        now = datetime.now(timezone.utc)
        recovered = 0
        with self._lock:
            for job_id, job in list(self._jobs.items()):
                if job.status not in ACTIVE_STATUSES:
                    continue
                recovered += 1
                updated = job.model_copy(
                    update={
                        "status": "failed",
                        "current_step": "interrupted",
                        "progress_percent": job.progress_percent,
                        "error": ErrorState(
                            code="unknown_error",
                            message="Job was interrupted before it finished.",
                            technical_details="The app stopped while this job was queued or running.",
                            recoverable=True,
                            suggested_user_action="Retry the job if the source and files are still available.",
                        ),
                        "finished_at": now,
                        "updated_at": now,
                        "cancel_requested": False,
                    }
                )
                self._jobs[job_id] = updated
                self._persist_job_locked(updated)
        return recovered

    def cancel_job(self, job_id: str) -> Job:
        """Request cancellation for a non-terminal job."""

        job = self._require_job(job_id)
        if job.status in TERMINAL_STATUSES:
            return job
        now = datetime.now(timezone.utc)
        if job.status == "queued":
            updated = job.model_copy(
                update={
                    "status": "cancelled",
                    "cancel_requested": True,
                    "current_step": "cancelled",
                    "finished_at": now,
                    "updated_at": now,
                }
            )
        else:
            process = self.get_subprocess(job_id)
            if process is not None and process.poll() is not None:
                updated = job.model_copy(
                    update={
                        "current_step": "cancel requested after subprocess finished",
                        "updated_at": now,
                    }
                )
                with self._lock:
                    self._jobs[job_id] = updated
                    self._persist_job_locked(updated)
                return updated

            updated = job.model_copy(
                update={
                    "cancel_requested": True,
                    "current_step": "cancel requested",
                    "updated_at": now,
                }
            )
        with self._lock:
            self._jobs[job_id] = updated
            self._persist_job_locked(updated)
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
                self._persist_job_locked(updated)

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
            self._persist_job_locked(updated)

    def _require_job(self, job_id: str) -> Job:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                raise KeyError(f"Job not found: {job_id}")
            return job

    def _init_db(self) -> None:
        assert self._db_path is not None
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self._db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    task_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    job_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at DESC)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)"
            )

    def _load_jobs_from_db(self) -> None:
        if self._db_path is None or not self._db_path.exists():
            return
        with sqlite3.connect(self._db_path) as connection:
            rows = connection.execute("SELECT job_json FROM jobs").fetchall()
        loaded: dict[str, Job] = {}
        for (job_json,) in rows:
            try:
                job = Job.model_validate_json(job_json)
            except Exception:
                continue
            loaded[job.job_id] = job
        with self._lock:
            self._jobs = loaded

    def _persist_job_locked(self, job: Job) -> None:
        if self._db_path is None:
            return
        with sqlite3.connect(self._db_path) as connection:
            connection.execute(
                """
                INSERT INTO jobs (job_id, task_type, status, created_at, updated_at, job_json)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    task_type=excluded.task_type,
                    status=excluded.status,
                    created_at=excluded.created_at,
                    updated_at=excluded.updated_at,
                    job_json=excluded.job_json
                """,
                (
                    job.job_id,
                    job.task_type,
                    job.status,
                    job.created_at.isoformat(),
                    job.updated_at.isoformat(),
                    job.model_dump_json(),
                ),
            )

    def _delete_jobs_locked(self, job_ids: list[str]) -> None:
        if self._db_path is None or not job_ids:
            return
        with sqlite3.connect(self._db_path) as connection:
            connection.executemany(
                "DELETE FROM jobs WHERE job_id = ?",
                [(job_id,) for job_id in job_ids],
            )
