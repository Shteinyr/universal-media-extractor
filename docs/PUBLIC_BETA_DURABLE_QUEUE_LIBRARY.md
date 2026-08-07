# Public Beta Durable Queue And Library

Date: 2026-08-07

GitHub issue:

- #46 `[P0] Durable Queue and Library finalization`

## Result

Queue and Library are now durable enough for public beta.

The app keeps Queue and Library responsibilities separate:

- Queue tracks batch groups, batch items, status, retry state, and interrupted work.
- Library indexes saved output folders and exposes copy/reveal/delete actions for managed outputs.

## Durable Queue

Batch groups are persisted in the same local SQLite file used by job history.

Default storage:

```text
data/jobs.sqlite3
```

When a custom output base dir is configured, the database path can resolve under:

```text
<output_base_dir>/.ume/jobs.sqlite3
```

Stored queue data:

- batch id;
- status;
- preset;
- mode;
- concurrency;
- batch items;
- child job ids;
- item results/errors;
- original batch request for retry.

New endpoint:

```text
GET /batch
```

This returns recent persisted batch groups. Existing endpoints remain:

- `POST /batch`
- `GET /batch/{batch_id}`
- `POST /batch/{batch_id}/retry-failed`
- `POST /batch/{batch_id}/cancel`

## Restart Recovery

On app startup:

- completed batches remain available;
- queued/running batches are converted to `failed`;
- queued/running items become failed with a recoverable interruption error;
- original batch request settings are kept so failed items can be retried.

This avoids showing stale `running` work after the app was closed.

## Library

Library remains output-folder based.

Implemented:

- `GET /outputs` lists saved managed output folders after restart;
- `GET /outputs/{output_id}` summarizes a managed output folder;
- `POST /outputs/{output_id}/reveal` asks the OS to reveal a managed output;
- `DELETE /outputs/{output_id}` safely deletes only a direct managed output folder.

Safe delete behavior was preserved. The app still does not accept arbitrary paths for deletion.

## Missing File State

Batch item snapshots now expose:

```text
output_missing: true / false
```

If a saved result path from a batch item no longer exists, the UI shows `Output missing`. This is informational and non-destructive; the app does not delete or rewrite batch history automatically.

## UI Changes

The Library surface now contains two distinct sections:

- Queue: recent persisted batch groups, status, counts, preset, view, and retry failed action;
- Files: saved output folders from the output index.

Opening a queue group shows the batch details in the main Queue panel. Failed queue groups can be retried after restart when the original request snapshot is available.

## Verification

Commands run:

```bash
node --check src/universal_media_extractor/static/app.js
node --check src/universal_media_extractor/static/option_normalizer.js
python3 -m py_compile scripts/browser_smoke.py
.venv/bin/python -m pytest tests/test_api_app.py tests/test_batch_service.py -q
.venv/bin/python -m pytest -q
UME_PUBLIC_PRODUCT_MODE=1 .venv/bin/python scripts/run_api.py
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/durable_queue_library
```

Results:

- JS syntax checks passed.
- Browser smoke script compiles.
- Targeted API/batch tests passed: `60 passed`.
- Full pytest passed: `204 passed`.
- Browser smoke passed in public product mode.

Proof screenshots:

- `proof/durable_queue_library/ui_initial.png`
- `proof/durable_queue_library/ui_analyze_result.png`
- `proof/durable_queue_library/ui_output_selected.png`
- `proof/durable_queue_library/ui_library.png`

## Not Changed

- No licensing/payments.
- No installer/signing/notarization.
- No native filesystem bridge.
- No AI summary.
- No Chrome extension.
- No public Course/Udemy support.
- No React/Vite/CDN.
- No roadmap change.
- No Redis/Celery/external queue.
- Backend remains local-only.
