# Block 9. Real Progress / Subprocess Cancellation Hardening

Date: 2026-05-30

## Status

Completed.

Block 9 hardens the existing in-memory job system for long-running local subprocesses. It does not add a persistent queue, new product flow, batch processing, desktop wrapper, extension, auth, database, cookies/login, or AI summary.

## Implemented

- Added active subprocess tracking to `JobService`.
- `cancel_job(...)` now attempts to stop a registered running subprocess.
- `DownloadService` now runs `yt-dlp` through `subprocess.Popen([...], shell=False)`.
- `DownloadService` registers the active `yt-dlp` process against the job.
- `DownloadService` parses practical `yt-dlp` output lines for:
  - `downloading`;
  - optional percent from `[download] ...%`;
  - `merging_or_postprocessing`.
- `TranscriptionService` now runs `ffmpeg` and Whisper through `subprocess.Popen([...], shell=False)`.
- `TranscriptionService` registers active `ffmpeg`/Whisper subprocesses against the job.
- Transcription now updates honest step-based job states.
- The static UI now displays:
  - `current_step`;
  - `progress_percent` when present;
  - cancel actions only while a job is `queued` or `running`;
  - clearer cancel-request text.

## Progress Behavior

Download jobs use these steps where applicable:

```text
preparing_download
downloading
merging_or_postprocessing
saving_metadata
succeeded
failed
cancelled
```

`yt-dlp` percent is parsed when a line exposes a `[download] ...%` value. If the selected source or `yt-dlp` output does not expose granular percent before completion, the job still reports honest step state and finishes at `100`.

Transcription jobs use these steps:

```text
preparing_transcription
extracting_audio
running_whisper
generating_transcript_files
succeeded
failed
cancelled
```

Whisper does not provide a stable machine-readable percent in the current integration, so the UI does not fake Whisper progress. It shows current step and only uses coarse step percentages.

## Cancellation Behavior

`JobService` now keeps a private in-memory map of active subprocess handles by `job_id`.

When `POST /jobs/{job_id}/cancel` is called:

- queued jobs are marked `cancelled`;
- terminal jobs are returned unchanged;
- running jobs set `cancel_requested=true`;
- if an active subprocess is registered, the service calls `terminate()`;
- if the process does not exit promptly, the service calls `kill()`;
- if no active subprocess is registered at that instant, the job records a limitation in `job.error`.

If a subprocess has already finished, cancellation does not force the final result to become cancelled.

## API / UI

No new endpoints were added.

Existing endpoints remain:

- `POST /download`
- `POST /transcribe`
- `POST /local/transcribe`
- `GET /jobs/{job_id}`
- `POST /jobs/{job_id}/cancel`

The UI still uses polling. It now shows a visible progress line when `progress_percent` is present.

## Tests

Command:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
73 passed
```

Coverage added/updated:

- cancel queued job;
- cancel running job with registered mocked subprocess;
- `terminate()` is called;
- `kill()` is called when terminate wait times out;
- already-finished subprocess does not force cancellation;
- `yt-dlp` progress parser reads percent and postprocessing lines;
- transcription updates step-based job status;
- API fake services receive job context;
- static UI exposes progress/cancel display labels.

## Manual Proof

Server command:

```bash
.venv/bin/python scripts/run_api.py
```

User-authorized URL:

```text
https://youtu.be/UUdxAp3kuKA
```

Manual flow:

```text
GET /health
POST /analyze
POST /download format_id=140
poll GET /jobs/{download_job_id}
POST /transcribe model=tiny
poll GET /jobs/{transcribe_job_id}
verify output files
controlled cancel proof with /bin/sh -c "sleep 30"
```

Proof artifacts:

```text
proof/block_9/health.json
proof/block_9/analyze_response.json
proof/block_9/download_job_start.json
proof/block_9/download_job_snapshots.json
proof/block_9/download_job_final.json
proof/block_9/transcribe_job_start.json
proof/block_9/transcribe_job_snapshots.json
proof/block_9/transcribe_job_final.json
proof/block_9/manual_review.json
proof/block_9/controlled_cancel_proof.json
proof/block_9/outputs/
```

Verified output:

```text
proof/block_9/outputs/20260530T142433Z_UUdxAp3kuKA/
```

Verified files:

```text
media/Showreel [UUdxAp3kuKA].m4a
transcripts/transcript.txt
transcripts/transcript.md
transcripts/transcript.json
transcripts/summary_prompt.md
```

Controlled cancellation proof used a synthetic `sleep 30` subprocess, not media work. It was terminated with return code `-15` and the job was marked `cancelled`.

## Not Included

- Batch processing.
- Chrome extension.
- Desktop wrapper.
- AI summary API.
- Auth/database/cookies.
- Redis/Celery/external queue.
- React/Vite/CDN.
- Browser verification tooling.
- Persistent job storage.
- Advanced download hardening.
- Roadmap changes.
