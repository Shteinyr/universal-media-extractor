# Phase 10 Analysis-Only FastAPI API

Date: 2026-05-29

## Scope

Phase 10 created a minimal FastAPI backend for URL analysis only.

Created:

- FastAPI app;
- Pydantic request/response schemas;
- local-only run script;
- API tests.

Not created:

- frontend;
- downloader;
- media download;
- Whisper/transcription;
- Chrome extension;
- desktop wrapper;
- online service;
- auth;
- database;
- cookies/login.

## Context7 Documentation Checked

Checked current docs for:

- FastAPI app/path operations, request/response models, and `TestClient`;
- Uvicorn programmatic run with `host="127.0.0.1"`;
- Pydantic v2 `BaseModel`, defaults, `Literal` fields, and serialization.

## Files Created

- `src/universal_media_extractor/api/__init__.py`
- `src/universal_media_extractor/api/app.py`
- `src/universal_media_extractor/api/schemas.py`
- `scripts/run_api.py`
- `tests/test_api_app.py`

## Files Updated

- `src/universal_media_extractor/services/output_manager.py`
- `requirements.txt`

`OutputManager` now adds a short unique suffix to analysis artifact directories and truncates sanitized source IDs to avoid long/colliding directory names.

`httpx2==2.2.0` was added because the installed Starlette `TestClient` requires `httpx2` or `httpx` to run API tests.

## Endpoints Implemented

### `GET /health`

Response:

```json
{
  "status": "ok",
  "service": "universal-media-extractor",
  "mode": "local-only"
}
```

Purpose:

- prove the local backend is alive;
- expose only static health information.

### `POST /analyze`

Request:

```json
{
  "source_type": "url",
  "url": "https://example.com/video",
  "user_confirmed_rights": false
}
```

Response:

```json
{
  "job": "Job",
  "result": "AnalyzeResult"
}
```

Behavior:

- creates an in-memory `analyze_url` job;
- creates a local analysis artifact directory;
- calls `AnalyzeService.analyze_url(...)`;
- returns normalized `AnalyzeResult`;
- marks job `succeeded` when `AnalyzeResult.errors` is empty;
- marks job `failed` when analyzer errors are present;
- does not download media;
- does not run Whisper.

### `GET /jobs/{job_id}`

Response:

```json
{
  "job_id": "job-...",
  "task_type": "analyze_url",
  "status": "queued | running | succeeded | failed | cancelled",
  "payload": {},
  "created_at": "...",
  "updated_at": "...",
  "error": null
}
```

Behavior:

- returns an in-memory job if it exists;
- returns `404` for missing jobs;
- does not use a database.

## Local-Only Binding

Run script:

```bash
.venv/bin/python scripts/run_api.py --port 8000
```

The script calls Uvicorn with:

```python
host="127.0.0.1"
```

It does not expose a host argument and does not bind to `0.0.0.0`.

## Verification

Automated tests:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
31 passed
```

Runtime health proof:

```bash
.venv/bin/python scripts/run_api.py --port 8765
curl -sS http://127.0.0.1:8765/health
```

Response:

```json
{"status":"ok","service":"universal-media-extractor","mode":"local-only"}
```

The server was stopped after the health check.

## Tests Added

File: `tests/test_api_app.py`

Coverage:

- `/health` returns the local-only status payload;
- `/analyze` calls the analysis service through a mock and returns `AnalyzeResult`;
- analyzer errors are preserved in both `AnalyzeResult.errors` and job error state;
- `/jobs/{job_id}` returns an existing job;
- `/jobs/{job_id}` returns `404` for missing jobs.

The tests do not call the network, do not run `yt-dlp`, do not download media, and do not run Whisper.

## Remaining Limits

- `/analyze` is synchronous and minimal.
- Jobs are in-memory only.
- No cancellation route is implemented.
- No progress tracking exists.
- No frontend exists.
- No downloader or transcription path exists.
- Real `/analyze` requests will call `yt-dlp --simulate --dump-json` through the existing safe analyzer wrapper.
