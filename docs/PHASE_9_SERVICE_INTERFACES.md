# Phase 9 Service Interfaces

Date: 2026-05-29

## Scope

Phase 9 created minimal service-layer interfaces and tests without creating a FastAPI app, routes, frontend, downloader, transcription module, media download, Whisper run, MVP, extension, or desktop wrapper.

The goal is to give future FastAPI routes a small business-logic layer to call instead of calling analyzers and utility code directly.

## Services Created

### AnalyzeService

File: `src/universal_media_extractor/services/analyze_service.py`

Public method:

```python
analyze_url(url: str, raw_output_dir: Path | None = None) -> AnalyzeResult
```

What it does:

- wraps the existing safe `analyze_url_with_ytdlp`;
- returns `AnalyzeResult`;
- passes through optional `raw_output_dir`;
- performs analysis only.

What it does not do:

- no download;
- no Whisper;
- no format selection;
- no backend route;
- no network access in tests.

### SafetyService

File: `src/universal_media_extractor/services/safety_service.py`

Public methods:

```python
build_default_legal_state() -> LegalSafetyState
require_rights_confirmation(user_confirmed_rights: bool) -> bool
```

What it does:

- builds the default legal/safety state used before protected operations;
- returns whether the user has confirmed rights.

What it does not do:

- no UI;
- no persistence;
- no download/transcription enforcement beyond the boolean gate.

### OutputManager

File: `src/universal_media_extractor/services/output_manager.py`

Public method:

```python
create_analysis_output_dir(base_dir: Path, source_id: str | None = None) -> Path
```

What it does:

- creates a timestamped local directory for analysis artifacts;
- sanitizes `source_id` for use in the directory name;
- keeps the created directory inside `base_dir`.

What it does not do:

- no media save;
- no download;
- no cleanup/retention policy;
- no arbitrary filesystem browsing.

### JobService

File: `src/universal_media_extractor/services/job_service.py`

Public methods:

```python
create_job(task_type, payload) -> Job
get_job(job_id) -> Job | None
update_job_status(job_id, status, error=None) -> Job
cancel_job(job_id) -> Job
```

What it does:

- creates in-memory jobs;
- supports statuses `queued`, `running`, `succeeded`, `failed`, and `cancelled`;
- updates status and optional error;
- cancels non-terminal jobs.

What it does not do:

- no database;
- no background worker;
- no subprocess ownership;
- no progress tracking yet;
- no retry logic yet.

## Job Model

File: `src/universal_media_extractor/models/job.py`

Created Pydantic v2 model:

- `Job`
- `JobStatus`

Fields:

- `job_id`
- `task_type`
- `status`
- `payload`
- `created_at`
- `updated_at`
- `error`

The model is intentionally small and in-memory friendly. It can later be reused by a future `GET /jobs/{job_id}` route.

## Future FastAPI Usage

Future routes should call services like this:

- `POST /analyze` calls `OutputManager` to create a raw artifact directory, then calls `AnalyzeService.analyze_url(...)`;
- `POST /analyze` may create a `Job` through `JobService` before analysis starts;
- protected future actions call `SafetyService.require_rights_confirmation(...)` before download, conversion, extraction, or transcription;
- `GET /jobs/{job_id}` reads from `JobService`.

Routes should not call `yt-dlp` directly.

## Tests Added

Files:

- `tests/test_analyze_service.py`
- `tests/test_output_manager.py`
- `tests/test_safety_service.py`
- `tests/test_job_service.py`

Coverage:

- `AnalyzeService` calls the analyzer via mock and returns `AnalyzeResult`;
- `OutputManager` creates a safe analysis output directory;
- `SafetyService` builds legal state and requires confirmation;
- `JobService` creates jobs, updates status, cancels jobs, and reports missing jobs.

## Verification

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
26 passed
```

## Preserved Limits

- No FastAPI app.
- No routes.
- No frontend.
- No downloader.
- No transcription module.
- No media download.
- No Whisper run.
- No MVP.
- No Chrome extension.
- No desktop wrapper.
- No database or persistent storage.
