"""In-memory batch queue service built on top of existing download jobs."""

from __future__ import annotations

import json
import re
import sqlite3
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock, Thread
from typing import Any
from urllib.parse import urljoin

from universal_media_extractor.error_mapping import compact_details, normalize_cli_error
from universal_media_extractor.models import (
    Batch,
    BatchCreateRequest,
    BatchDownloadItemRequest,
    BatchInvalidLine,
    BatchItem,
    BatchUrlImportResult,
    DownloadRequest,
    ErrorState,
    PlaylistAnalyzeResult,
    PlaylistAnalyzeRequest,
    PlaylistItem,
    WarningState,
)
from universal_media_extractor.services.download_service import DownloadService
from universal_media_extractor.services.job_service import JobService


URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")
TERMINAL_ITEM_STATUSES = {"succeeded", "failed", "cancelled", "skipped"}
TERMINAL_BATCH_STATUSES = {"succeeded", "failed", "cancelled"}
ACTIVE_BATCH_STATUSES = {"queued", "running"}


class BatchService:
    """Run small local download batches with controlled concurrency."""

    def __init__(
        self,
        *,
        job_service: JobService,
        download_service: DownloadService,
        db_path: Path | None = None,
    ) -> None:
        self._job_service = job_service
        self._download_service = download_service
        self._batches: dict[str, Batch] = {}
        self._batch_requests: dict[str, BatchCreateRequest] = {}
        self._lock = Lock()
        self._db_path = db_path.expanduser().resolve() if db_path else job_service.db_path
        if self._db_path is not None:
            self._init_db()
            self._load_batches_from_db()
            self.recover_interrupted_batches()

    def import_urls(self, text: str, *, source: str = "textarea") -> BatchUrlImportResult:
        seen: set[str] = set()
        urls: list[str] = []
        invalid_lines: list[BatchInvalidLine] = []
        duplicate_count = 0

        for line_number, raw_line in enumerate(text.splitlines(), start=1):
            line = raw_line.strip()
            if not line:
                continue
            found = [self._clean_url(match.group(0)) for match in URL_PATTERN.finditer(line)]
            found = [url for url in found if url]
            if not found:
                invalid_lines.append(
                    BatchInvalidLine(
                        line_number=line_number,
                        text=line[:200],
                        reason="No http or https URL found.",
                    )
                )
                continue
            for url in found:
                if url in seen:
                    duplicate_count += 1
                    continue
                seen.add(url)
                urls.append(url)

        return BatchUrlImportResult(
            source=source,
            urls=urls,
            invalid_lines=invalid_lines,
            duplicate_count=duplicate_count,
        )

    def create_batch(self, request: BatchCreateRequest) -> Batch:
        selected_items = [item for item in request.items if item.selected]
        batch = Batch(
            batch_id=f"batch-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            preset=request.preset,
            mode=self._preset_mode(request.preset),
            concurrency=request.concurrency,
            items=[self._new_item(item, order) for order, item in enumerate(selected_items, start=1)],
            total_count=len(selected_items),
        )
        if not request.user_confirmed_rights:
            batch.status = "failed"
            batch.errors = [
                ErrorState(
                    code="rights_confirmation_required",
                    message="Confirm that you have the right to download these URLs before starting a batch.",
                    recoverable=True,
                    suggested_user_action="Enable rights confirmation and start the queue again.",
                )
            ]
            self._refresh_counts(batch)
            self._store(batch)
            return batch
        if request.preset == "archive_pack":
            batch.status = "failed"
            batch.errors = [
                ErrorState(
                    code="unknown_error",
                    message="Archive Pack is planned but not enabled for batch execution yet.",
                    recoverable=False,
                    suggested_user_action="Choose Best Video, Audio, or Subtitles for this batch.",
                )
            ]
            self._refresh_counts(batch)
            self._store(batch)
            return batch
        if not selected_items:
            batch.status = "failed"
            batch.errors = [
                ErrorState(
                    code="invalid_input_file",
                    message="No selected URLs were provided for the batch.",
                    recoverable=True,
                    suggested_user_action="Import URLs and select at least one item.",
                )
            ]
            self._refresh_counts(batch)
            self._store(batch)
            return batch

        self._refresh_counts(batch)
        self._store(batch)
        self._store_request(batch.batch_id, request)
        self._start_runner(batch.batch_id, request)
        return self.get_batch(batch.batch_id) or batch

    def get_batch(self, batch_id: str) -> Batch | None:
        with self._lock:
            batch = self._batches.get(batch_id)
            return self._snapshot(batch) if batch else None

    def list_batches(self, *, limit: int = 50, status: str | None = None) -> list[Batch]:
        with self._lock:
            batches = list(self._batches.values())
        if status is not None:
            batches = [batch for batch in batches if batch.status == status]
        batches.sort(key=lambda batch: batch.created_at, reverse=True)
        return [self._snapshot(batch) for batch in batches[: max(0, limit)]]

    def recover_interrupted_batches(self) -> int:
        now = datetime.now(timezone.utc)
        recovered = 0
        interruption_error = ErrorState(
            code="unknown_error",
            message="Queue was interrupted before it finished.",
            technical_details="The app stopped while this batch was queued or running.",
            recoverable=True,
            suggested_user_action="Retry failed items if the sources are still available.",
        )
        with self._lock:
            for batch_id, batch in list(self._batches.items()):
                if batch.status not in ACTIVE_BATCH_STATUSES:
                    continue
                recovered += 1
                for item in batch.items:
                    if item.status in {"queued", "running"}:
                        item.status = "failed"
                        item.error = interruption_error
                        item.updated_at = now
                batch.status = "failed"
                batch.errors = [interruption_error]
                self._refresh_counts(batch)
                self._persist_batch_locked(batch)
                if batch_id in self._batch_requests:
                    self._persist_request_locked(batch_id, self._batch_requests[batch_id])
        return recovered

    def retry_failed_items(self, batch_id: str) -> Batch:
        with self._lock:
            batch = self._batches.get(batch_id)
            if batch is None:
                raise KeyError(batch_id)
            original_request = self._batch_requests.get(batch_id)
            if original_request is None:
                raise ValueError("Original batch settings are unavailable.")
            failed_items = [item for item in batch.items if item.status == "failed"]
            if not failed_items:
                raise ValueError("Batch has no failed items to retry.")
            for item in failed_items:
                item.status = "queued"
                item.job_id = None
                item.error = None
                item.result = None
                item.updated_at = datetime.now(timezone.utc)
            batch.status = "queued"
            batch.errors = []
            self._refresh_counts(batch)
            self._persist_batch_locked(batch)
            snapshot = batch.model_copy(deep=True)

        request = original_request.model_copy(deep=True)
        self._start_runner(batch_id, request, item_ids={item.item_id for item in failed_items})
        return self.get_batch(batch_id) or snapshot

    def cancel_batch(self, batch_id: str) -> Batch:
        with self._lock:
            batch = self._batches.get(batch_id)
            if batch is None:
                raise KeyError(batch_id)
            for item in batch.items:
                if item.status == "queued":
                    item.status = "cancelled"
                    item.updated_at = datetime.now(timezone.utc)
                if item.status == "running" and item.job_id:
                    try:
                        self._job_service.cancel_job(item.job_id)
                    except KeyError:
                        pass
            batch.status = "cancelled"
            self._refresh_counts(batch)
            self._persist_batch_locked(batch)
            return batch.model_copy(deep=True)

    def _start_runner(
        self,
        batch_id: str,
        request: BatchCreateRequest,
        *,
        item_ids: set[str] | None = None,
    ) -> None:
        Thread(
            target=self._run_batch,
            args=(batch_id, request, item_ids),
            daemon=True,
        ).start()

    def _run_batch(
        self,
        batch_id: str,
        request: BatchCreateRequest,
        item_ids: set[str] | None,
    ) -> None:
        with self._lock:
            batch = self._batches.get(batch_id)
            if batch is None or batch.status == "cancelled":
                return
            batch.status = "running"
            self._refresh_counts(batch)
            self._persist_batch_locked(batch)
            items = [item.model_copy(deep=True) for item in batch.items if item.status == "queued"]
            if item_ids is not None:
                items = [item for item in items if item.item_id in item_ids]

        with ThreadPoolExecutor(max_workers=request.concurrency) as executor:
            futures = {
                executor.submit(self._run_item, batch_id, item, request): item.item_id
                for item in items
            }
            for future in as_completed(futures):
                item_id = futures[future]
                try:
                    future.result()
                except Exception as exc:  # pragma: no cover - defensive worker boundary
                    self._mark_item_failed(
                        batch_id,
                        item_id,
                        ErrorState(
                            code="unknown_error",
                            message="Batch item failed unexpectedly.",
                            technical_details=compact_details(str(exc)),
                            recoverable=True,
                            suggested_user_action="Retry this item after checking the source.",
                        ),
                    )

        with self._lock:
            batch = self._batches.get(batch_id)
            if batch is None:
                return
            self._refresh_counts(batch)
            if batch.status != "cancelled":
                batch.status = "failed" if batch.failed_count else "succeeded"
                batch.updated_at = datetime.now(timezone.utc)
            self._persist_batch_locked(batch)

    def _run_item(self, batch_id: str, item: BatchItem, request: BatchCreateRequest) -> None:
        with self._lock:
            stored = self._find_item(batch_id, item.item_id)
            if stored is None or stored.status != "queued":
                return
            stored.status = "running"
            stored.updated_at = datetime.now(timezone.utc)
            self._refresh_counts(self._batches[batch_id])
            self._persist_batch_locked(self._batches[batch_id])

        download_request = self._download_request_for_item(item, request)
        job = self._job_service.create_job("download", download_request.model_dump())
        self._job_service.update_job_status(
            job.job_id,
            "running",
            current_step="batch_download",
            progress_percent=0,
        )
        with self._lock:
            stored = self._find_item(batch_id, item.item_id)
            if stored:
                stored.job_id = job.job_id
                stored.updated_at = datetime.now(timezone.utc)
                self._persist_batch_locked(self._batches[batch_id])

        try:
            result = self._download_service.download_media(
                download_request,
                job_service=self._job_service,
                job_id=job.job_id,
            )
        except Exception as exc:  # pragma: no cover - defensive service boundary
            error = ErrorState(
                code="unknown_error",
                message="Batch item failed unexpectedly.",
                technical_details=compact_details(str(exc)),
                recoverable=True,
                suggested_user_action="Retry this item after checking the source.",
            )
            self._job_service.fail_job(job.job_id, error)
            self._mark_item_failed(batch_id, item.item_id, error, job_id=job.job_id)
            return
        result_data = result.model_dump(mode="json")
        errors = result.errors or []
        refreshed = self._job_service.get_job(job.job_id)
        if refreshed and refreshed.cancel_requested:
            self._job_service.update_job_status(
                job.job_id,
                "cancelled",
                current_step="cancelled",
                result=result_data,
            )
            item_status = "cancelled"
            error = None
        elif result.status == "cancelled":
            self._job_service.update_job_status(
                job.job_id,
                "cancelled",
                current_step="cancelled",
                result=result_data,
            )
            item_status = "cancelled"
            error = None
        elif result.status == "skipped":
            self._job_service.finish_job(job.job_id, result_data)
            item_status = "skipped"
            error = None
        elif errors:
            error = errors[0]
            self._job_service.fail_job(job.job_id, error, result=result_data)
            item_status = "failed"
        else:
            self._job_service.finish_job(job.job_id, result_data)
            item_status = "succeeded"
            error = None

        with self._lock:
            stored = self._find_item(batch_id, item.item_id)
            batch = self._batches.get(batch_id)
            if stored and batch:
                stored.status = item_status
                stored.result = result
                stored.error = error
                stored.updated_at = datetime.now(timezone.utc)
                self._refresh_counts(batch)
                self._persist_batch_locked(batch)

    def _mark_item_failed(
        self,
        batch_id: str,
        item_id: str,
        error: ErrorState,
        *,
        job_id: str | None = None,
    ) -> None:
        with self._lock:
            stored = self._find_item(batch_id, item_id)
            batch = self._batches.get(batch_id)
            if stored is None or batch is None:
                return
            if stored.status in TERMINAL_ITEM_STATUSES:
                return
            stored.status = "failed"
            stored.job_id = job_id or stored.job_id
            stored.error = error
            stored.updated_at = datetime.now(timezone.utc)
            self._refresh_counts(batch)
            self._persist_batch_locked(batch)

    def _download_request_for_item(self, item: BatchItem, request: BatchCreateRequest) -> DownloadRequest:
        mode, format_id, output_format = self._preset_download_values(request.preset)
        return DownloadRequest(
            source_url=item.source_url,
            source_title=item.source_title,
            playlist_index=item.playlist_index,
            format_id=format_id,
            mode=mode,
            user_confirmed_rights=request.user_confirmed_rights,
            output_base_dir=request.output_base_dir,
            output_template=request.output_template,
            duplicate_policy=request.duplicate_policy,
            output_format=output_format,
        )

    def _new_item(self, request: BatchDownloadItemRequest, order: int) -> BatchItem:
        return BatchItem(
            item_id=f"item-{order:04d}",
            order=order,
            source_url=request.source_url,
            source_title=request.source_title,
            playlist_index=request.playlist_index,
        )

    def _store(self, batch: Batch) -> None:
        with self._lock:
            self._batches[batch.batch_id] = batch
            self._persist_batch_locked(batch)

    def _store_request(self, batch_id: str, request: BatchCreateRequest) -> None:
        with self._lock:
            self._batch_requests[batch_id] = request.model_copy(deep=True)
            self._persist_request_locked(batch_id, self._batch_requests[batch_id])

    def _find_item(self, batch_id: str, item_id: str) -> BatchItem | None:
        batch = self._batches.get(batch_id)
        if batch is None:
            return None
        return next((item for item in batch.items if item.item_id == item_id), None)

    def _refresh_counts(self, batch: Batch) -> None:
        batch.total_count = len(batch.items)
        batch.queued_count = sum(item.status == "queued" for item in batch.items)
        batch.running_count = sum(item.status == "running" for item in batch.items)
        batch.succeeded_count = sum(item.status == "succeeded" for item in batch.items)
        batch.failed_count = sum(item.status == "failed" for item in batch.items)
        batch.cancelled_count = sum(item.status == "cancelled" for item in batch.items)
        batch.skipped_count = sum(item.status == "skipped" for item in batch.items)
        batch.updated_at = datetime.now(timezone.utc)

    def _snapshot(self, batch: Batch) -> Batch:
        snapshot = batch.model_copy(deep=True)
        for item in snapshot.items:
            output_dir = item.result.output_dir if item.result else None
            item.output_missing = bool(output_dir and not Path(output_dir).exists())
        return snapshot

    def _init_db(self) -> None:
        assert self._db_path is not None
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self._db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS batches (
                    batch_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    batch_json TEXT NOT NULL,
                    request_json TEXT
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_batches_created_at ON batches(created_at DESC)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_batches_status ON batches(status)"
            )

    def _load_batches_from_db(self) -> None:
        if self._db_path is None or not self._db_path.exists():
            return
        with sqlite3.connect(self._db_path) as connection:
            rows = connection.execute(
                "SELECT batch_json, request_json FROM batches"
            ).fetchall()
        batches: dict[str, Batch] = {}
        requests: dict[str, BatchCreateRequest] = {}
        for batch_json, request_json in rows:
            try:
                batch = Batch.model_validate_json(batch_json)
            except Exception:
                continue
            batches[batch.batch_id] = batch
            if request_json:
                try:
                    requests[batch.batch_id] = BatchCreateRequest.model_validate_json(request_json)
                except Exception:
                    pass
        with self._lock:
            self._batches = batches
            self._batch_requests = requests

    def _persist_batch_locked(self, batch: Batch) -> None:
        if self._db_path is None:
            return
        request = self._batch_requests.get(batch.batch_id)
        request_json = request.model_dump_json() if request else None
        with sqlite3.connect(self._db_path) as connection:
            connection.execute(
                """
                INSERT INTO batches (batch_id, status, created_at, updated_at, batch_json, request_json)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(batch_id) DO UPDATE SET
                    status=excluded.status,
                    created_at=excluded.created_at,
                    updated_at=excluded.updated_at,
                    batch_json=excluded.batch_json,
                    request_json=COALESCE(excluded.request_json, batches.request_json)
                """,
                (
                    batch.batch_id,
                    batch.status,
                    batch.created_at.isoformat(),
                    batch.updated_at.isoformat(),
                    batch.model_dump_json(),
                    request_json,
                ),
            )

    def _persist_request_locked(self, batch_id: str, request: BatchCreateRequest) -> None:
        if self._db_path is None:
            return
        batch = self._batches.get(batch_id)
        if batch is None:
            return
        with sqlite3.connect(self._db_path) as connection:
            connection.execute(
                """
                INSERT INTO batches (batch_id, status, created_at, updated_at, batch_json, request_json)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(batch_id) DO UPDATE SET
                    request_json=excluded.request_json,
                    status=excluded.status,
                    updated_at=excluded.updated_at,
                    batch_json=excluded.batch_json
                """,
                (
                    batch.batch_id,
                    batch.status,
                    batch.created_at.isoformat(),
                    batch.updated_at.isoformat(),
                    batch.model_dump_json(),
                    request.model_dump_json(),
                ),
            )

    def _preset_mode(self, preset: str) -> str:
        return self._preset_download_values(preset)[0]

    def _preset_download_values(self, preset: str) -> tuple[str, str, str | None]:
        if preset == "audio_m4a":
            return "audio", "bestaudio[ext=m4a]/bestaudio", "m4a"
        if preset == "audio_mp3":
            return "audio", "bestaudio", "mp3"
        if preset == "subtitles":
            return "subtitles", "all", "srt"
        if preset == "video_1080p":
            return "combined", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best", "mp4"
        if preset in {"video_720p", "smaller_video"}:
            return "combined", "bestvideo[height<=720]+bestaudio/best[height<=720]/best", "mp4"
        return "combined", "bestvideo+bestaudio/best", "mp4"

    def _clean_url(self, url: str) -> str:
        return url.rstrip(".,);]")


class PlaylistService:
    """Safe playlist analyzer using yt-dlp flat playlist metadata only."""

    def analyze_playlist(
        self,
        request: PlaylistAnalyzeRequest,
        *,
        timeout_seconds: int = 60,
        raw_output_dir: Path | None = None,
    ) -> PlaylistAnalyzeResult:
        command = [
            "yt-dlp",
            "--simulate",
            "--flat-playlist",
            "--dump-single-json",
            request.source_url,
        ]
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
                shell=False,
            )
        except subprocess.TimeoutExpired as exc:
            return self._error_result(
                request.source_url,
                ErrorState(
                    code="timeout",
                    message="Playlist analysis timed out.",
                    technical_details=compact_details(getattr(exc, "stderr", None)),
                    recoverable=True,
                    suggested_user_action="Retry later or paste individual URLs.",
                ),
            )
        except FileNotFoundError:
            return self._error_result(
                request.source_url,
                ErrorState(
                    code="ytdlp_not_found",
                    message="yt-dlp was not found on PATH.",
                    recoverable=True,
                    suggested_user_action="Install yt-dlp or fix PATH, then retry.",
                ),
            )

        if completed.returncode != 0:
            return self._error_result(
                request.source_url,
                normalize_cli_error(
                    completed.stderr or completed.stdout,
                    default_code="extractor_failed",
                    default_message="Playlist analysis failed.",
                    default_suggested_user_action="Paste individual URLs or retry later.",
                    engine="yt-dlp",
                ),
            )

        try:
            raw = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            return self._error_result(
                request.source_url,
                ErrorState(
                    code="invalid_output",
                    message="yt-dlp returned invalid playlist JSON.",
                    technical_details=str(exc),
                    recoverable=True,
                    suggested_user_action="Paste individual URLs instead.",
                ),
            )

        raw_reference_path = self._save_raw_json(raw, raw_output_dir) if raw_output_dir else None
        entries = raw.get("entries") if isinstance(raw, dict) else None
        if not isinstance(entries, list):
            entries = []
        base_url = raw.get("webpage_url") or request.source_url if isinstance(raw, dict) else request.source_url
        items = [item for item in (self._playlist_item(entry, index, base_url) for index, entry in enumerate(entries, start=1)) if item]
        return PlaylistAnalyzeResult(
            source_url=request.source_url,
            is_playlist=len(items) > 1,
            title=raw.get("title") if isinstance(raw, dict) else None,
            extractor=raw.get("extractor") if isinstance(raw, dict) else None,
            item_count=len(items),
            items=items,
            warnings=[] if items else [
                WarningState(
                    code="best_effort_extractor",
                    message="No playlist items were detected. Paste individual URLs if this source is not a playlist.",
                    severity="info",
                )
            ],
            raw_reference_path=raw_reference_path,
        )

    def _playlist_item(self, entry: Any, index: int, base_url: str) -> PlaylistItem | None:
        if not isinstance(entry, dict):
            return None
        item_url = entry.get("webpage_url") or entry.get("url")
        if isinstance(item_url, str) and item_url and not item_url.startswith(("http://", "https://")):
            item_url = urljoin(base_url, item_url)
        if not isinstance(item_url, str) or not item_url.startswith(("http://", "https://")):
            return None
        item_id = str(entry.get("id") or f"playlist-{index}")
        return PlaylistItem(
            item_id=item_id,
            title=entry.get("title"),
            url=item_url,
            duration_seconds=entry.get("duration"),
            playlist_index=entry.get("playlist_index") or index,
            selected=True,
        )

    def _save_raw_json(self, raw: dict[str, Any], raw_output_dir: Path) -> str:
        raw_output_dir.mkdir(parents=True, exist_ok=True)
        path = raw_output_dir / f"playlist_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)

    def _error_result(self, source_url: str, error: ErrorState) -> PlaylistAnalyzeResult:
        return PlaylistAnalyzeResult(
            source_url=source_url,
            is_playlist=False,
            item_count=0,
            errors=[error],
        )
