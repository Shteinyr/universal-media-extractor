# Commercial Block 5: SQLite Jobs And History

## Status

Completed.

GitHub issue: `#10 [P0] Add SQLite-backed persistent jobs and history`.

## Goal

Replace runtime-only job state with local persistent job history suitable for public beta readiness.

This is still a local single-user implementation. It does not add external queues, Redis, Celery, accounts, cloud sync, or batch processing.

## Implemented

### SQLite-Backed Job Storage

`JobService` now supports optional SQLite persistence through a `db_path` argument.

The FastAPI app enables persistence by default with:

```text
data/jobs.sqlite3
```

The file is a local runtime artifact and is ignored by git.

Persisted job data includes:

- `job_id`;
- `task_type`;
- `status`;
- `current_step`;
- `progress_percent`;
- `payload`;
- `result`;
- `error`;
- timestamps;
- `cancel_requested`;
- `retry_of_job_id`.

### Restart Recovery

When a persisted `JobService` starts, previously `queued` or `running` jobs are recovered into a clear failed state:

```text
status: failed
current_step: interrupted
error.code: unknown_error
recoverable: true
```

This avoids showing stale jobs as still running after the app was closed or crashed.

### History API

New endpoints:

```text
GET /jobs
POST /jobs/{job_id}/retry
DELETE /jobs/history
```

Existing endpoints remain:

```text
GET /jobs/{job_id}
POST /jobs/{job_id}/cancel
GET /diagnostics/jobs/{job_id}
```

### Retry

Failed jobs can be retried. Retry creates a new queued job with the original task type and payload, sets `retry_of_job_id`, and starts the known operation again for supported task types:

- `analyze_url`;
- `download`;
- `transcribe`;
- `udemy_download`.

Retry is rejected for non-failed jobs.

### Clear History

`DELETE /jobs/history` removes terminal job records from SQLite and memory:

- `succeeded`;
- `failed`;
- `cancelled`.

It does not delete downloaded media, transcript files, logs, metadata, or output folders.

Running jobs remain in history.

## Files Changed

- `src/universal_media_extractor/models/job.py`
- `src/universal_media_extractor/models/__init__.py`
- `src/universal_media_extractor/services/job_service.py`
- `src/universal_media_extractor/api/app.py`
- `tests/test_job_service.py`
- `tests/test_api_app.py`
- `.gitignore`
- project documentation and memory files

## Verification

Targeted checks:

```bash
python3 -m py_compile src/universal_media_extractor/models/job.py src/universal_media_extractor/services/job_service.py src/universal_media_extractor/api/app.py tests/test_job_service.py tests/test_api_app.py
.venv/bin/python -m pytest tests/test_job_service.py tests/test_api_app.py -q
node --check src/universal_media_extractor/static/app.js
.venv/bin/python -m pytest -q
```

Results:

- Targeted API/job tests: `57 passed`.
- Full test suite: `129 passed`.
- Static JS syntax check passed.

Acceptance coverage:

- Jobs survive restart: covered by `test_job_service_persists_jobs_across_instances` and API restart test.
- Status/progress/error/result persist: covered by `test_job_service_persists_error_and_progress`.
- Failed jobs can be retried: covered by service and API retry tests.
- History can be cleared without deleting files: covered by service and API clear-history tests.
- Interrupted jobs recover clearly: covered by `test_job_service_recovers_interrupted_jobs_on_startup` and API restart test.

## Not Included

- No batch processing.
- No external queue.
- No Redis/Celery.
- No accounts/cloud sync.
- No packaging/signing/payment work.
- No new roadmap block.
- No major UI redesign.
