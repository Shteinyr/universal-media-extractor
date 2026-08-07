# Public Beta Progress, Cancel, Retry, Recovery

Date: 2026-08-07

GitHub issue: #48 `[P0] Unified progress, cancel, retry, recovery`

## Summary

This block unifies job progress semantics across URL download, transcription, and batch queue execution without adding a new queue backend or new product features.

The app now exposes stable user-facing job stages and an explicit progress mode:

- `stage`: normalized lifecycle stage for UI and API consumers.
- `progress_mode`: `determinate` only when the app has a real percentage, otherwise `indeterminate`.

Legacy `current_step` is kept for compatibility and diagnostics.

## Normalized Stages

Supported public stages:

- `queued`
- `preparing`
- `validating`
- `analyzing`
- `downloading`
- `merging`
- `converting`
- `extracting_audio`
- `transcribing`
- `saving`
- `completed`
- `failed`
- `cancelling`
- `cancelled`
- `interrupted`

## Progress Rules

Determinate progress is shown only when the value represents real progress:

- `yt-dlp` download percent lines set `stage=downloading` and `progress_mode=determinate`.
- successful terminal jobs set `stage=completed`, `progress_mode=determinate`, `progress_percent=100`.

Indeterminate progress is used for stages where the app does not have a reliable percentage:

- queued/preparing/validating;
- merge/remux/post-processing;
- ffmpeg audio extraction;
- Whisper transcription;
- transcript/result file writing;
- cancellation and interruption states.

This avoids fake progress for long-running Whisper or ffmpeg work.

## Cancel Behavior

Cancellation remains best-effort because the app delegates work to local subprocesses.

Implemented behavior:

- queued jobs immediately become terminal `cancelled`;
- running jobs move to `cancelling` and request subprocess termination;
- registered `yt-dlp`, `ffmpeg`, and Whisper subprocesses are terminated, then killed if they do not exit promptly;
- cancelled download jobs clean safe temporary files such as `.part`, `.tmp`, `.temp`, and `.ytdl`;
- cancelled transcription jobs clean the local work folder and extracted temporary audio where safe.

The app does not expose Pause because true resume is not implemented or verified for every source.

## Retry And Recovery

Implemented behavior:

- failed jobs can be retried through the existing job retry endpoint;
- queued/running jobs persisted in SQLite are converted to a failed, recoverable `interrupted` state at app startup;
- queued/running batch groups persisted in SQLite are converted to failed/recoverable interruption states at app startup;
- retry failed batch items preserves the original batch settings when the saved request snapshot is available;
- an unexpected failure in one batch item is isolated to that item and does not stop unrelated queued/running items.

## UI Behavior

The static UI now reads `stage` and `progress_mode`.

- Determinate progress bar is shown only for `progress_mode=determinate`.
- Running/queued indeterminate work uses a subtle indeterminate bar.
- User-facing stage labels are short: `Downloading`, `Merging`, `Extracting audio`, `Transcribing`, `Saving files`, `Cancelling`, etc.
- Failed or cancelled background jobs keep the existing local `Copy diagnostics` action.

## Not Implemented

- true resumable downloads for every source;
- Pause action;
- external queue systems such as Redis or Celery;
- exact Whisper progress parsing;
- guaranteed cleanup of every source-specific temporary artifact.

## Verification

Commands:

```bash
node --check src/universal_media_extractor/static/app.js
node --check src/universal_media_extractor/static/option_normalizer.js
.venv/bin/python -m pytest tests/test_job_service.py tests/test_download_service.py tests/test_transcription_service.py tests/test_batch_service.py -q
.venv/bin/python -m pytest -q
UME_PUBLIC_PRODUCT_MODE=1 .venv/bin/python scripts/run_api.py
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/unified_progress_recovery
```

Results:

- focused tests: `45 passed`;
- full test suite: `220 passed`;
- browser smoke passed in public product mode.

Proof screenshots:

- `proof/unified_progress_recovery/ui_initial.png`
- `proof/unified_progress_recovery/ui_analyze_result.png`
- `proof/unified_progress_recovery/ui_output_selected.png`
- `proof/unified_progress_recovery/ui_library.png`
