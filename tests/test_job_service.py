import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

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
    assert job.stage == "queued"
    assert job.progress_mode == "indeterminate"
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
    assert updated.stage == "failed"
    assert updated.progress_mode == "indeterminate"
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
    assert cancelled.stage == "cancelled"


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
    assert updated.stage == "cancelling"


def test_job_service_missing_job_raises_key_error():
    service = JobService()

    with pytest.raises(KeyError):
        service.update_job_status("missing", "running")



def test_job_service_persists_jobs_across_instances(tmp_path):
    db_path = tmp_path / "jobs.sqlite3"
    service = JobService(db_path)
    job = service.create_job("download", {"format_id": "140"})
    service.update_job_step(job.job_id, "downloading", 42)
    service.finish_job(job.job_id, {"output_dir": str(tmp_path / "output")})

    reloaded = JobService(db_path)
    persisted = reloaded.get_job(job.job_id)

    assert persisted is not None
    assert persisted.status == "succeeded"
    assert persisted.current_step == "succeeded"
    assert persisted.stage == "completed"
    assert persisted.progress_mode == "determinate"
    assert persisted.progress_percent == 100
    assert persisted.result == {"output_dir": str(tmp_path / "output")}



def test_job_service_persists_error_and_progress(tmp_path):
    db_path = tmp_path / "jobs.sqlite3"
    service = JobService(db_path)
    job = service.create_job("download", {"format_id": "140"})
    service.update_job_status(job.job_id, "running", current_step="downloading", progress_percent=64)
    service.fail_job(
        job.job_id,
        ErrorState(code="network_error", message="Network failed.", recoverable=True),
        result={"status": "failed"},
    )

    reloaded = JobService(db_path)
    persisted = reloaded.get_job(job.job_id)

    assert persisted is not None
    assert persisted.status == "failed"
    assert persisted.progress_percent == 64
    assert persisted.error is not None
    assert persisted.error.code == "network_error"
    assert persisted.result == {"status": "failed"}


def test_job_service_recovers_interrupted_jobs_on_startup(tmp_path):
    db_path = tmp_path / "jobs.sqlite3"
    service = JobService(db_path)
    queued = service.create_job("download", {"format_id": "140"})
    running = service.create_job("transcribe", {"input_file_path": "audio.m4a"})
    service.update_job_status(running.job_id, "running", current_step="running_whisper", progress_percent=35)

    reloaded = JobService(db_path)

    recovered_queued = reloaded.get_job(queued.job_id)
    recovered_running = reloaded.get_job(running.job_id)
    assert recovered_queued is not None
    assert recovered_running is not None
    assert recovered_queued.status == "failed"
    assert recovered_queued.current_step == "interrupted"
    assert recovered_queued.stage == "interrupted"
    assert recovered_queued.progress_mode == "indeterminate"
    assert recovered_queued.error is not None
    assert recovered_queued.error.recoverable is True
    assert recovered_running.status == "failed"
    assert recovered_running.current_step == "interrupted"
    assert recovered_running.stage == "interrupted"
    assert recovered_running.progress_percent == 35


def test_job_service_marks_only_real_download_progress_as_determinate():
    service = JobService()
    download = service.create_job("download", {})
    transcribe = service.create_job("transcribe", {})
    service.update_job_status(download.job_id, "running")
    service.update_job_status(transcribe.job_id, "running")

    download = service.update_job_step(download.job_id, "downloading", 64)
    transcribe = service.update_job_step(transcribe.job_id, "running_whisper", 35)

    assert download.stage == "downloading"
    assert download.progress_mode == "determinate"
    assert transcribe.stage == "transcribing"
    assert transcribe.progress_mode == "indeterminate"


def test_job_service_lists_recent_jobs_newest_first(tmp_path):
    service = JobService(tmp_path / "jobs.sqlite3")
    first = service.create_job("download", {"n": 1})
    second = service.create_job("download", {"n": 2})

    jobs = service.list_jobs()

    assert [job.job_id for job in jobs[:2]] == [second.job_id, first.job_id]
    assert service.list_jobs(limit=1)[0].job_id == second.job_id


def test_job_service_retry_failed_job_creates_new_queued_job(tmp_path):
    service = JobService(tmp_path / "jobs.sqlite3")
    failed = service.create_job("download", {"format_id": "140"})
    service.fail_job(
        failed.job_id,
        ErrorState(code="network_error", message="Network failed.", recoverable=True),
    )

    retried = service.retry_job(failed.job_id)

    assert retried.job_id != failed.job_id
    assert retried.retry_of_job_id == failed.job_id
    assert retried.task_type == "download"
    assert retried.payload == {"format_id": "140"}
    assert retried.status == "queued"


def test_job_service_retry_requires_failed_job(tmp_path):
    service = JobService(tmp_path / "jobs.sqlite3")
    job = service.create_job("download", {})

    with pytest.raises(ValueError):
        service.retry_job(job.job_id)


def test_job_service_clear_history_keeps_active_jobs_and_files(tmp_path):
    db_path = tmp_path / "jobs.sqlite3"
    output_file = tmp_path / "output" / "media.m4a"
    output_file.parent.mkdir()
    output_file.write_bytes(b"media")
    service = JobService(db_path)
    failed = service.create_job("download", {"output_dir": str(output_file.parent)})
    running = service.create_job("download", {"format_id": "140"})
    service.fail_job(
        failed.job_id,
        ErrorState(code="network_error", message="Network failed.", recoverable=True),
    )
    service.update_job_status(running.job_id, "running")

    cleared = service.clear_history()

    assert cleared == 1
    assert service.get_job(failed.job_id) is None
    assert service.get_job(running.job_id) is not None
    assert output_file.exists()
    reloaded = JobService(db_path)
    assert reloaded.get_job(failed.job_id) is None
