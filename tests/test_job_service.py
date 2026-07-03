import pytest

from universal_media_extractor.models import ErrorState, Job
from universal_media_extractor.services.job_service import JobService


class FakeProcess:
    def __init__(self, *, running=True, wait_raises=False):
        self.running = running
        self.wait_raises = wait_raises
        self.terminated = False
        self.killed = False

    def poll(self):
        return None if self.running else 0

    def terminate(self):
        self.terminated = True

    def kill(self):
        self.killed = True
        self.running = False

    def wait(self, timeout=None):
        if self.wait_raises and not self.killed:
            import subprocess

            raise subprocess.TimeoutExpired("fake", timeout or 0)
        self.running = False
        return 0


def test_job_service_creates_job():
    service = JobService()

    job = service.create_job("analyze_url", {"url": "https://example.test/video"})

    assert isinstance(job, Job)
    assert job.job_id.startswith("job-")
    assert job.task_type == "analyze_url"
    assert job.status == "queued"
    assert job.payload == {"url": "https://example.test/video"}
    assert service.get_job(job.job_id) == job


def test_job_service_updates_status_with_error():
    service = JobService()
    job = service.create_job("analyze_url", {})
    error = ErrorState(
        code="timeout",
        message="Timed out.",
        recoverable=True,
    )

    updated = service.update_job_status(job.job_id, "failed", error=error)

    assert updated.status == "failed"
    assert updated.error == error
    assert updated.updated_at >= job.updated_at


def test_job_service_cancels_non_terminal_job():
    service = JobService()
    job = service.create_job("analyze_url", {})

    cancelled = service.cancel_job(job.job_id)

    assert cancelled.status == "cancelled"


def test_job_service_stops_registered_running_process():
    service = JobService()
    job = service.create_job("download", {})
    service.update_job_status(job.job_id, "running")
    process = FakeProcess()
    service.register_subprocess(job.job_id, process)

    cancelled = service.cancel_job(job.job_id)

    assert process.terminated is True
    assert cancelled.status == "cancelled"
    assert cancelled.current_step == "cancelled"


def test_job_service_kills_process_when_terminate_wait_times_out():
    service = JobService()
    job = service.create_job("download", {})
    service.update_job_status(job.job_id, "running")
    process = FakeProcess(wait_raises=True)
    service.register_subprocess(job.job_id, process)

    cancelled = service.cancel_job(job.job_id)

    assert process.terminated is True
    assert process.killed is True
    assert cancelled.status == "cancelled"


def test_job_service_does_not_cancel_when_registered_process_already_finished():
    service = JobService()
    job = service.create_job("download", {})
    service.update_job_status(job.job_id, "running")
    process = FakeProcess(running=False)
    service.register_subprocess(job.job_id, process)

    updated = service.cancel_job(job.job_id)

    assert updated.status == "running"
    assert updated.cancel_requested is False
    assert updated.current_step == "cancel requested after subprocess finished"


def test_job_service_missing_job_raises_key_error():
    service = JobService()

    with pytest.raises(KeyError):
        service.update_job_status("missing", "running")
