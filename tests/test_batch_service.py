import sys
import sqlite3
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.models import (
    Batch,
    BatchCreateRequest,
    BatchDownloadItemRequest,
    BatchItem,
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


def test_batch_video_720p_preset_uses_honest_height_cap(tmp_path):
    fake = FakeDownloadService()
    service = BatchService(job_service=JobService(tmp_path / "jobs.sqlite3"), download_service=fake)
    request = BatchCreateRequest(
        items=[BatchDownloadItemRequest(source_url="https://example.test/video")],
        user_confirmed_rights=True,
        preset="video_720p",
    )

    batch = service.create_batch(request)
    final = wait_for_batch(service, batch.batch_id)

    assert final.status == "succeeded"
    assert fake.calls[-1].mode == "combined"
    assert "height<=720" in fake.calls[-1].format_id
    assert fake.calls[-1].output_format == "mp4"


def test_completed_batch_persists_across_service_restart(tmp_path):
    db_path = tmp_path / "jobs.sqlite3"
    fake = FakeDownloadService()
    service = BatchService(job_service=JobService(db_path), download_service=fake, db_path=db_path)
    request = BatchCreateRequest(
        items=[BatchDownloadItemRequest(source_url="https://example.test/video")],
        user_confirmed_rights=True,
        preset="audio_m4a",
    )

    batch = service.create_batch(request)
    final = wait_for_batch(service, batch.batch_id)

    reloaded = BatchService(job_service=JobService(db_path), download_service=fake, db_path=db_path)
    restored = reloaded.get_batch(final.batch_id)

    assert restored is not None
    assert restored.status == "succeeded"
    assert restored.succeeded_count == 1
    assert reloaded.list_batches()[0].batch_id == final.batch_id


def test_interrupted_batch_recovers_to_retryable_failed_state(tmp_path):
    db_path = tmp_path / "jobs.sqlite3"
    service = BatchService(job_service=JobService(db_path), download_service=FakeDownloadService(), db_path=db_path)
    request = BatchCreateRequest(
        items=[BatchDownloadItemRequest(source_url="https://example.test/video")],
        user_confirmed_rights=True,
        preset="audio_m4a",
    )
    interrupted = Batch(
        batch_id="batch-interrupted",
        status="running",
        preset="audio_m4a",
        mode="audio",
        concurrency=1,
        items=[
            BatchItem(
                item_id="item-0001",
                order=1,
                source_url="https://example.test/video",
                status="running",
            )
        ],
    )
    _insert_batch_snapshot(db_path, interrupted, request)

    recovered_service = BatchService(job_service=JobService(db_path), download_service=FakeDownloadService(), db_path=db_path)
    recovered = recovered_service.get_batch("batch-interrupted")

    assert recovered is not None
    assert recovered.status == "failed"
    assert recovered.items[0].status == "failed"
    assert recovered.items[0].error is not None
    assert recovered.items[0].error.recoverable is True

    recovered_service.retry_failed_items("batch-interrupted")
    retried = wait_for_batch(recovered_service, "batch-interrupted")

    assert retried.status == "succeeded"
    assert retried.succeeded_count == 1


def test_batch_snapshot_marks_missing_output_non_destructively(tmp_path):
    db_path = tmp_path / "jobs.sqlite3"
    missing_dir = tmp_path / "deleted-output"
    batch = Batch(
        batch_id="batch-missing-output",
        status="succeeded",
        preset="audio_m4a",
        mode="audio",
        concurrency=1,
        items=[
            BatchItem(
                item_id="item-0001",
                order=1,
                source_url="https://example.test/video",
                status="succeeded",
                result=DownloadResult(
                    status="succeeded",
                    source_url="https://example.test/video",
                    selected_format_id="bestaudio",
                    output_dir=str(missing_dir),
                    downloaded_files=[str(missing_dir / "media" / "file.m4a")],
                ),
            )
        ],
    )
    request = BatchCreateRequest(
        items=[BatchDownloadItemRequest(source_url="https://example.test/video")],
        user_confirmed_rights=True,
        preset="audio_m4a",
    )
    service = BatchService(job_service=JobService(db_path), download_service=FakeDownloadService(), db_path=db_path)
    _insert_batch_snapshot(db_path, batch, request)

    reloaded = BatchService(job_service=JobService(db_path), download_service=FakeDownloadService(), db_path=db_path)
    restored = reloaded.get_batch("batch-missing-output")

    assert restored is not None
    assert restored.items[0].output_missing is True
    assert not missing_dir.exists()


def _insert_batch_snapshot(db_path: Path, batch: Batch, request: BatchCreateRequest) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            INSERT INTO batches (batch_id, status, created_at, updated_at, batch_json, request_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                batch.batch_id,
                batch.status,
                batch.created_at.isoformat() if batch.created_at else datetime.now(timezone.utc).isoformat(),
                batch.updated_at.isoformat() if batch.updated_at else datetime.now(timezone.utc).isoformat(),
                batch.model_dump_json(),
                request.model_dump_json(),
            ),
        )
