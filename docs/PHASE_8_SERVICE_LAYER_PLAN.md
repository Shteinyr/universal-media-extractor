# Phase 8 Service Layer Plan

Date: 2026-05-29

## Scope

Phase 8 defines the future service layer for the local web app without creating a FastAPI app, routes, frontend, downloader, transcription module, media downloads, Whisper runs, MVP, extension, or desktop wrapper.

The current code already has:

- normalized analyze-result models;
- a pure `yt-dlp` raw JSON normalizer;
- a safe URL analysis wrapper around `yt-dlp --simulate --dump-json`.

The service layer should sit between future FastAPI routes and lower-level analyzers/normalizers.

## Services Needed

### AnalyzeService

Purpose: analyze user-provided sources and return normalized `AnalyzeResult`.

Initial responsibilities:

- validate that the source is a URL;
- call `analyze_url_with_ytdlp(url, raw_output_dir=...)`;
- return `AnalyzeResult`;
- preserve analyzer errors in `AnalyzeResult.errors`;
- avoid download/process actions.

Future responsibilities:

- dispatch local-file analysis to `LocalFileMetadataService`;
- apply settings such as timeout and raw artifact location;
- attach job context if analysis becomes asynchronous.

### LocalFileMetadataService

Purpose: inspect local audio/video files without using `yt-dlp`.

Future responsibilities:

- call `ffprobe` safely with subprocess list arguments;
- extract duration, streams, codecs, container, size, and metadata;
- return a normalized local-file analyze result.

Phase 8 status: later service, not part of the first MVP slice.

### DownloadService

Purpose: download or extract selected media outputs after explicit user confirmation.

Future responsibilities:

- call `yt-dlp` only after `legal_safety.user_confirmed_rights == true`;
- support selected audio/video/subtitle formats;
- report progress;
- support cancellation;
- write files only inside managed output directories.

Phase 8 status: later service. It is explicitly out of the first UI prototype.

### TranscriptionService

Purpose: run local transcription after media/audio is available.

Future responsibilities:

- extract audio through `ffmpeg` when needed;
- run Whisper CLI or a future local transcription engine;
- create transcript outputs such as `txt`, `md`, `json`, and prompt files;
- report progress and errors through jobs.

Phase 8 status: later service. Whisper must not run in this phase.

### OutputManager

Purpose: create and manage predictable local output folders.

Minimal MVP responsibilities:

- create a per-job output directory;
- create a raw-analysis artifact directory;
- return safe local paths to the caller;
- prevent path traversal and writes outside the project/output root.

Future responsibilities:

- create structured result folders;
- manage metadata files;
- expose local paths for completed outputs;
- provide cleanup or retention rules.

### JobService

Purpose: track long-running or user-visible operations.

Minimal MVP responsibilities:

- create an in-memory job record;
- track status, timestamps, task type, payload summary, result, and errors;
- allow status updates;
- expose a job for polling by future UI.

Future responsibilities:

- run background processes;
- cancellation;
- retries;
- progress events;
- persistence if needed.

### SettingsService

Purpose: centralize local settings.

Initial future responsibilities:

- read fixed defaults for timeout, output root, raw artifact root, and local-only host;
- expose values to services without hardcoding in route handlers.

Advanced responsibilities:

- user-editable settings;
- per-tool executable paths;
- retention limits;
- future cookies path if manually enabled by the user.

Phase 8 status: advanced settings are later.

### SafetyService

Purpose: keep local-only and legal/safety gates explicit.

Minimal MVP responsibilities:

- require `user_confirmed_rights` before any download or processing action;
- provide a stable confirmation text;
- reject protected operations when confirmation is missing.

Future responsibilities:

- enforce local-only backend binding expectations;
- centralize CORS policy guidance;
- block cookies/login features unless explicitly enabled later;
- record safety warnings in job/result state.

## MVP Services

The first MVP should include only:

- `AnalyzeService`
- `OutputManager` minimal
- `JobService` minimal
- `SafetyService` minimal

These are enough for a local UI prototype that analyzes a URL and displays the normalized result without downloading or transcribing anything.

## Later Services

Leave these for later phases:

- `DownloadService`
- `TranscriptionService`
- `LocalFileMetadataService`
- advanced `SettingsService`

## Method Contracts

### AnalyzeService

```python
analyze_url(url: str, raw_output_dir: Path | None = None) -> AnalyzeResult
```

Expected behavior:

- calls the existing safe analyzer wrapper;
- performs analysis only;
- returns `AnalyzeResult` whether analysis succeeds or fails;
- uses `AnalyzeResult.errors` for recoverable or blocking failures.

### JobService

```python
create_job(task_type: str, payload: dict) -> Job
get_job(job_id: str) -> Job | None
update_job_status(job_id: str, status: str, *, result=None, errors=None, progress=None) -> Job
```

Expected behavior:

- create a stable job ID;
- store task type and small payload summary;
- keep result references rather than huge raw blobs;
- expose job state to future API/UI.

### OutputManager

```python
create_output_dir(job_id: str, *, kind: str = "analysis") -> Path
```

Expected behavior:

- create directories under a configured local output/proof root;
- never write outside the configured root;
- return a path suitable for raw artifacts or future output files.

### SafetyService

```python
require_user_rights_confirmation(user_confirmed_rights: bool) -> None
```

Expected behavior:

- allow analysis without confirmation;
- require confirmation before download, conversion, extraction, or transcription;
- fail with a user-readable recoverable error when confirmation is missing.

## Job Lifecycle

Allowed statuses:

- `queued`
- `running`
- `succeeded`
- `failed`
- `cancelled`

Recommended state fields:

- `job_id`
- `task_type`
- `status`
- `created_at`
- `started_at`
- `finished_at`
- `progress`
- `payload_summary`
- `result`
- `errors`
- `output_dir`

## Error Flow

Analyzer errors should remain visible in two places:

- inside `AnalyzeResult.errors`;
- inside the enclosing job errors if the analysis is job-backed.

The UI should treat `AnalyzeResult.errors` as source-level failures and job errors as execution-level failures.

Recoverable errors include:

- timeout;
- temporary network failure;
- cookies/login needed when a future manual option exists;
- invalid extractor output where retry may help;
- missing local executable after installation/PATH fix.

Non-recoverable or currently blocked errors include:

- unsupported source with no local-file alternative;
- DRM, CAPTCHA, paywall, or auth bypass requirements;
- user rights confirmation missing for protected operations.

## Local-Only Safety

Future backend constraints:

- bind only to `127.0.0.1`;
- use minimal CORS, ideally only the local frontend origin;
- do not open the server to LAN or public interfaces;
- do not store cookies, logins, tokens, or session secrets in Phase 8/MVP;
- do not implement cookies/login in the first MVP;
- require `legal_safety.user_confirmed_rights == true` before download or processing;
- keep all generated files under managed local output directories.

## Phase 8 Non-Goals

- No FastAPI app.
- No routes.
- No frontend.
- No downloader.
- No transcription.
- No media download.
- No Whisper run.
- No MVP implementation.
- No extension.
- No desktop wrapper.
