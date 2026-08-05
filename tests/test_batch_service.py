import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.models import (
    BatchCreateRequest,
    BatchDownloadItemRequest,
    DownloadResult,
    ErrorState,
)
from universal_media_extractor.services.batch_service import BatchService
from universal_media_extractor.services.job_service import JobService


class FakeDownloadService:
    def __init__(self):
        self.active = 0
        self.max_active = 0
        self.lock = threading.Lock()
        self.calls = []
        self.failed_once = set()

    def download_media(self, request, *, job_service=None, job_id=None):
        with self.lock:
            self.active += 1
            self.max_active = max(self.max_active, self.active)
            self.calls.append(request)
        time.sleep(0.03)
        with self.lock:
            self.active -= 1
        if "fail-once" in request.source_url and request.source_url not in self.failed_once:
            self.failed_once.add(request.source_url)
            return DownloadResult(
                job_id=job_id,
                status="failed",
                source_url=request.source_url,
                selected_format_id=request.format_id,
                errors=[ErrorState(code="network_error", message="Temporary failure.", recoverable=True)],
            )
        return DownloadResult(
            job_id=job_id,
            status="succeeded",
            source_url=request.source_url,
            selected_format_id=request.format_id,
            output_dir="/tmp/out",
            downloaded_files=["/tmp/out/media/file.mp4"],
        )


def wait_for_batch(service, batch_id, timeout=2.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        batch = service.get_batch(batch_id)
        if batch.status in {"succeeded", "failed", "cancelled"}:
            return batch
        time.sleep(0.01)
    raise AssertionError("batch did not finish")


def test_import_urls_reports_invalid_lines_and_duplicates(tmp_path):
    service = BatchService(job_service=JobService(tmp_path / "jobs.sqlite3"), download_service=FakeDownloadService())

    result = service.import_urls("https://a.test/one\nnot url\nWatch https://a.test/one now\nhttps://b.test/two")

    assert result.urls == ["https://a.test/one", "https://b.test/two"]
    assert result.duplicate_count == 1
    assert result.invalid_lines[0].line_number == 2


def test_batch_runs_with_controlled_concurrency(tmp_path):
    fake = FakeDownloadService()
    service = BatchService(job_service=JobService(tmp_path / "jobs.sqlite3"), download_service=fake)
    request = BatchCreateRequest(
        items=[BatchDownloadItemRequest(source_url=f"https://example.test/{i}") for i in range(5)],
        user_confirmed_rights=True,
        concurrency=2,
        preset="audio_m4a",
    )

    batch = service.create_batch(request)
    final = wait_for_batch(service, batch.batch_id)

    assert final.status == "succeeded"
    assert final.succeeded_count == 5
    assert fake.max_active <= 2
    assert all(call.mode == "audio" for call in fake.calls)
    assert all(call.output_format == "m4a" for call in fake.calls)


def test_batch_requires_rights_confirmation(tmp_path):
    fake = FakeDownloadService()
    service = BatchService(job_service=JobService(tmp_path / "jobs.sqlite3"), download_service=fake)

    batch = service.create_batch(BatchCreateRequest(items=[BatchDownloadItemRequest(source_url="https://example.test/1")]))

    assert batch.status == "failed"
    assert batch.errors[0].code == "rights_confirmation_required"
    assert fake.calls == []


def test_retry_failed_items_reuses_batch_settings(tmp_path):
    fake = FakeDownloadService()
    service = BatchService(job_service=JobService(tmp_path / "jobs.sqlite3"), download_service=fake)
    request = BatchCreateRequest(
        items=[BatchDownloadItemRequest(source_url="https://example.test/fail-once")],
        user_confirmed_rights=True,
        concurrency=1,
        preset="audio_mp3",
    )

    batch = service.create_batch(request)
    failed = wait_for_batch(service, batch.batch_id)
    assert failed.status == "failed"

    service.retry_failed_items(batch.batch_id)
    retried = wait_for_batch(service, batch.batch_id)

    assert retried.status == "succeeded"
    assert retried.succeeded_count == 1
    assert fake.calls[-1].output_format == "mp3"
