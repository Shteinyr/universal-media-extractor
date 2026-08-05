# Commercial Block 13: Batch Queue Foundation + Playlist/Clipboard Import

Status: completed for batch queue foundation, playlist selection, URL import, and retry failed items. Archive Pack remains planned/disabled.

## What Was Added

- In-memory `BatchService` on top of the existing `DownloadService` and `JobService`.
- Controlled concurrency for multiple URL downloads, limited to 1-3 workers.
- Batch item lifecycle: queued, running, succeeded, failed, cancelled, skipped.
- URL import from textarea, clipboard, and `.txt` files.
- Invalid lines are reported without blocking valid URLs.
- Duplicate URLs are skipped while preserving first-seen order.
- Safe playlist analysis through `yt-dlp --simulate --flat-playlist --dump-single-json`.
- Playlist item selection before queue start.
- Retry failed batch items while preserving original preset/output settings.
- Optional queue cancellation that delegates to existing job cancellation for running child jobs.
- Compact static UI Batch mode.

## API Endpoints

- `POST /batch/import`
  - Parses text and returns unique URLs, invalid lines, and duplicate count.

- `POST /playlists/analyze`
  - Uses flat playlist metadata only.
  - Does not download media.

- `POST /batch`
  - Starts a batch queue.
  - Requires `user_confirmed_rights=true`.
  - Creates normal child `download` jobs under the existing job system.

- `GET /batch/{batch_id}`
  - Returns current in-memory batch state.

- `POST /batch/{batch_id}/retry-failed`
  - Requeues failed items in the same batch.

- `POST /batch/{batch_id}/cancel`
  - Cancels queued items and requests cancellation for running child jobs.

## UI Flow

1. Select `Batch mode`.
2. Paste URLs, click `Paste`, or import a `.txt` file.
3. Click `Import URLs`, or `Analyze playlist` for playlist URLs.
4. Select/unselect queue items.
5. Choose a preset and concurrency.
6. Click `Start queue`.
7. Watch item statuses.
8. Use `Retry failed` if any items fail.

## Batch Presets

Implemented for batch execution:

- Best Video
- 1080p Video
- Smaller Video
- Audio M4A
- Audio MP3
- Subtitles

Archive Pack is visible as a planned/disabled preset only. It is not executed yet because a real Archive Pack needs a separate multi-output composition flow: video/audio/subtitles/metadata/transcript in one organized result.

## Safety Boundaries

- No DRM, CAPTCHA, paywall, login, or platform restriction bypass.
- No cookies/login expansion.
- No cloud upload.
- No paid APIs.
- Backend remains local-only.
- Downloads still require the backend `user_confirmed_rights=true` contract.
- Batch uses existing `yt-dlp` download behavior and does not add a separate downloader engine.

## Persistence

Batch state is in-memory for now. Child download jobs are persisted in SQLite through the existing `JobService`, but the parent batch queue itself is not restored after restart. Persistent batch history can be added later if needed.

## Tests

Added/updated tests for:

- Batch model validation.
- URL import dedupe and invalid line reporting.
- Controlled concurrency.
- Rights confirmation safety.
- Retry failed items preserving settings.
- API endpoints for import, create batch, playlist analyze, and static UI strings.

Verification commands:

```bash
node --check src/universal_media_extractor/static/app.js
.venv/bin/python -m pytest -q
```

Latest result: `195 passed`.

## Not Included

- Archive Pack execution.
- Persistent parent batch history.
- Payment, checkout, or licensing.
- Desktop packaging changes.
- Chrome extension.
- AI summary.
- External queue systems such as Redis or Celery.
