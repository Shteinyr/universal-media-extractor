# Block 6. Job / Progress / Cancel

Date: 2026-05-30

## Status

Completed.

Block 6 converts long-running download and transcription actions from direct synchronous API responses into in-memory jobs with polling and best-effort cancellation.

The MVP flow remains:

```text
URL -> Analyze -> Select format -> Confirm rights -> Download -> Transcribe -> Result
```

## Implemented

- Extended the in-memory `Job` model with:
  - `current_step`
  - `progress_percent`
  - `started_at`
  - `finished_at`
  - `payload`
  - `result`
  - `error`
  - `cancel_requested`
- Hardened `JobService` with lock-protected in-memory state.
- Added job helpers for running, step updates, success, failure, and cancellation.
- Changed `POST /download` to start a background job and return `Job`.
- Changed `POST /transcribe` to start a background job and return `Job`.
- Kept `GET /jobs/{job_id}` for polling job state.
- Added `POST /jobs/{job_id}/cancel`.
- Updated the static UI to:
  - show download job status;
  - poll `/jobs/{job_id}`;
  - show transcription job status;
  - show cancel buttons while jobs are active;
  - render `job.result` when jobs succeed;
  - render `job.error` when jobs fail.

## API Behavior

### `POST /download`

Starts a local download job and returns the created job. The actual download runs in a background daemon thread.

The job result is a serialized `DownloadResult` stored in `job.result`.

### `POST /transcribe`

Starts a local transcription job and returns the created job. The actual Whisper/ffmpeg work runs in a background daemon thread.

The job result is a serialized `TranscriptionResult` stored in `job.result`.

### `GET /jobs/{job_id}`

Returns current in-memory job state.

### `POST /jobs/{job_id}/cancel`

Requests cancellation.

For queued jobs, the job is marked `cancelled` immediately.

For running jobs, `cancel_requested=true` is set. The current subprocess is not forcibly killed in Block 6. After the running operation returns, the job runner checks `cancel_requested` and marks the job `cancelled` instead of `succeeded`.

## Cancellation Limitation

Block 6 does not store active subprocess handles inside the job registry and does not kill active `yt-dlp`, `ffmpeg`, or Whisper processes.

Cancellation is therefore best-effort:

- reliable before a job starts;
- visible to the UI while a job is running;
- honored after the current subprocess completes;
- not guaranteed to stop CPU/network/disk work immediately.

This preserves a simple local architecture and avoids unsafe process handling before a more deliberate worker design exists.

## Progress Behavior

Progress is currently coarse:

- `queued`
- `running`
- `current_step`: `downloading` or `transcribing`
- `succeeded`
- `failed`
- `cancelled`

`progress_percent` is set to `0` when a job starts and `100` when it succeeds. It does not parse `yt-dlp` or Whisper progress output yet.

## Safety

- Download still requires `user_confirmed_rights=true`.
- Transcription still requires `user_confirmed_rights=true`.
- Backend remains local-only through `scripts/run_api.py` binding to `127.0.0.1`.
- No cookies, login tokens, auth, database, Redis, Celery, or external queue were added.
- No AI summary API was added.

## Tests

Command:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
51 passed
```

Coverage added/updated:

- `/download` returns a job and stores final `DownloadResult` in `job.result`.
- `/transcribe` returns a job and stores final `TranscriptionResult` in `job.result`.
- rights-confirmation failure becomes a failed job with structured error and blocked result.
- queued job cancellation marks the job `cancelled`.
- missing cancel target returns 404.
- static UI still exposes expected flow and job polling code.

## Manual Proof

Server command:

```bash
.venv/bin/python scripts/run_api.py
```

User-authorized URL:

```text
https://youtu.be/UUdxAp3kuKA
```

Proof flow:

```text
GET /health
POST /analyze
POST /download format_id=140
poll GET /jobs/{download_job_id}
POST /transcribe model=tiny
poll GET /jobs/{transcribe_job_id}
verify output files
```

Proof artifacts:

```text
proof/block_6/health.json
proof/block_6/analyze_response.json
proof/block_6/download_job_start.json
proof/block_6/download_job_final.json
proof/block_6/transcribe_job_start.json
proof/block_6/transcribe_job_final.json
proof/block_6/output_review.json
proof/block_6/outputs/
```

Verified output files:

```text
proof/block_6/outputs/20260530T133510Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a
proof/block_6/outputs/20260530T133510Z_UUdxAp3kuKA/transcripts/transcript.txt
proof/block_6/outputs/20260530T133510Z_UUdxAp3kuKA/transcripts/transcript.md
proof/block_6/outputs/20260530T133510Z_UUdxAp3kuKA/transcripts/transcript.json
proof/block_6/outputs/20260530T133510Z_UUdxAp3kuKA/transcripts/summary_prompt.md
```

Browser visual verification was attempted through the Codex Browser plugin, but the local URL was blocked by the browser security policy. API/manual proof was used instead.

## Not Included

- Batch processing.
- Chrome extension.
- Desktop wrapper.
- AI summary API.
- Auth/database/cookies.
- Redis/Celery/external queue.
- React/Vite/CDN.
- Advanced download hardening.
- Immediate active subprocess termination.
- Fine-grained progress parsing.
- Roadmap changes.
