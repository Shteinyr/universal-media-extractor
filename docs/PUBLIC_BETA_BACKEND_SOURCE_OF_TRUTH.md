# Public Beta Backend Source Of Truth

Date: 2026-08-07

This inventory records the actual backend state after the Public Beta UI/UX Refactor Block 1 work. It resolves the product-doc ambiguity around SQLite/database state and public/internal Course mode.

## Public Product Mode

Public commercial/beta builds should run with:

```bash
UME_PUBLIC_PRODUCT_MODE=1 .venv/bin/python scripts/run_api.py
```

In public product mode:

- Course/Udemy routes are not registered.
- `/config` returns `public_product_mode=true` and `course_mode_enabled=false`.
- The static UI bundle does not expose Course, Udemy, browser-cookie, Chrome session, or manual cookie surfaces.

Internal/local experimental builds may still enable Course mode outside public positioning.

## Endpoint Inventory

Public mode endpoints:

- `GET /`
- `GET /config`
- `GET /health`
- `POST /analyze`
- `POST /batch/import`
- `POST /playlists/analyze`
- `POST /batch`
- `GET /batch`
- `GET /batch/{batch_id}`
- `POST /batch/{batch_id}/retry-failed`
- `POST /batch/{batch_id}/cancel`
- `POST /download`
- `POST /transcribe`
- `POST /local/analyze`
- `POST /local/analyze-path`
- `POST /local/transcribe`
- `GET /outputs`
- `GET /outputs/{output_id}`
- `POST /outputs/{output_id}/reveal`
- `DELETE /outputs/{output_id}`
- `GET /jobs`
- `DELETE /jobs/history`
- `POST /jobs/{job_id}/retry`
- `GET /jobs/{job_id}`
- `POST /jobs/{job_id}/cancel`
- `GET /diagnostics/jobs/{job_id}`

Internal Course mode additionally registers:

- `POST /udemy/analyze`
- `POST /udemy/download`

## Persistence State

SQLite is used for jobs/history and durable batch queue snapshots.

- `JobService` is backed by `data/jobs.sqlite3` by default, or by `<output_base_dir>/.ume/jobs.sqlite3` when `UME_OUTPUT_BASE_DIR` is set.
- Jobs survive app restart.
- Queued/running jobs found at startup are recovered into a failed, recoverable `interrupted` state.
- Failed jobs can be retried.
- Terminal job history can be cleared without deleting output files.
- Batch groups survive app restart.
- Queued/running batch groups found at startup are recovered into a failed, recoverable interruption state.
- Failed batch items can be retried when the original request snapshot is available.

SQLite is not yet a full product database.

- Output library/search is folder-index based, not database-backed.
- Settings, licensing, accounts, payments, and user profiles are not stored in SQLite.

## Batch State

Batch support now has durable queue snapshots for public beta.

- Multiple URLs can be imported from text or `.txt/.csv`.
- Batch items create normal download jobs.
- Child jobs are persisted through SQLite.
- Batch groups are persisted through SQLite.
- Recent batch groups are listed through `GET /batch`.
- Interrupted queued/running batches recover to failed/retryable states after restart.
- Batch item snapshots expose `output_missing` when a previously saved output path no longer exists.

The remaining Queue/Library follow-up is deeper product UX, not basic durability.

## Outputs

Outputs are stored as managed local folders under the configured output base directory.

Implemented:

- output index through `GET /outputs`;
- output detail through `GET /outputs/{output_id}`;
- safe delete through `DELETE /outputs/{output_id}`;
- reveal request through `POST /outputs/{output_id}/reveal`;
- reveal prefers the primary result file when available and falls back to the output folder;
- path validation so arbitrary paths cannot be deleted through output APIs.

Default user output base:

```text
~/Downloads/Universal Media Extractor
```

The backend resolves and validates user-selected output folders before starting downloads.

## Native Filesystem Integration

Issue #47 adds desktop filesystem convenience without broad filesystem access.

Implemented:

- desktop mode exposes native file/folder pickers through the existing `pywebview` shell;
- `POST /local/analyze-path` lets desktop-selected files be analyzed in place with `ffprobe`;
- browser mode continues to use upload input and typed save paths;
- the main UI keeps the short default save path instead of showing long absolute paths on startup;
- copy/reveal actions remain user-triggered;
- reveal/delete remain constrained to direct managed output folders.

Not implemented:

- arbitrary filesystem delete;
- browser-native folder picker;
- cloud file provider integration;
- installer-level macOS/Windows permission setup.

## Diagnostics

Diagnostics are local and redacted.

Implemented:

- `GET /diagnostics/jobs/{job_id}`;
- redaction of cookies, tokens, transcripts, full URLs, and local paths;
- no-store cache headers for diagnostics responses.

Diagnostics are for support/debugging, not telemetry. No diagnostics are uploaded by the app.

## Security Boundary

Implemented:

- backend binds to `127.0.0.1`;
- local session token required for protected requests from the static UI;
- strict local host/origin checks;
- explicit CORS policy;
- local upload size limits;
- no stored credentials;
- no cloud processing.

Not implemented:

- external auth;
- online accounts;
- remote dashboard;
- license enforcement;
- payment checkout.

## Follow-Ups

- Progress/cancel/retry recovery can be refined further for long-running media processes.
- Native filesystem edge cases should be rechecked during Windows production packaging.
