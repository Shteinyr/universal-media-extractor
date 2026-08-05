# Commercial Block 14: Public Beta UI Readiness

Date: 2026-08-05

## Purpose

Polish the existing static UI toward a clearer public beta surface without adding new product features, changing API contracts, or changing the roadmap.

## What Improved

- Reworked the left input-mode tabs into a compact 2x2 layout: Link, File, Batch, and Course.
- Kept `Course` visible only for internal builds and labeled it as internal/experimental in the UI copy.
- Shortened the empty and loading states so they explain the local workflow without long helper text.
- Reduced developer-oriented wording in result states:
  - `Status: succeeded` became `Download saved`, `Transcript saved`, or `Course saved`.
  - raw job wording is hidden behind simpler `Working`, `Saved`, `Needs attention`, and `Cancelled` labels.
  - progress now renders visually instead of as a noisy `Progress: N%` line.
- Made download/transcript result cards more compact by showing file/folder names in the main UI while preserving full paths in tooltips and copy/reveal actions.
- Made batch queue rows easier to scan by hiding job IDs and showing human status labels.
- Kept technical error details available through collapsible details, but made the primary error title more user-facing.
- Updated browser smoke expectations to match the new UI labels.

## UI Flows Checked

- Initial local UI loads.
- URL analysis for the user-authorized Showreel test URL renders presets and source summary.
- Batch mode can import pasted URLs and render the queue setup state.
- Existing API/static tests still pass.

## Proof Artifacts

Screenshots:

- `proof/commercial_block_14_ui_readiness/ui_initial.png`
- `proof/commercial_block_14_ui_readiness/ui_analyze_result.png`
- `proof/commercial_block_14_ui_readiness/ui_batch_import.png`

Commands:

```bash
node --check src/universal_media_extractor/static/app.js
python3 -m py_compile scripts/browser_smoke.py
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn universal_media_extractor.api.app:app --app-dir src --host 127.0.0.1 --port 8010
.venv/bin/python scripts/browser_smoke.py --base-url http://127.0.0.1:8010/ --proof-dir proof/commercial_block_14_ui_readiness
```

Test result:

```text
195 passed
```

## Not Changed

- No new backend endpoints.
- No API contract changes.
- No React, Vite, CDN, or frontend build system.
- No checkout/licensing.
- No Apple/Windows installer work.
- No Chrome extension.
- No AI summary.
- No roadmap changes.

## Remaining Limitations

- This is still a developer/local beta UI, not final branded launch design.
- Course mode remains internal/experimental and is hidden from public commercial builds.
- Browser smoke covers smoke-level UI behavior, not full automated visual regression.
- Advanced details still exist for support/debugging but are intentionally not the primary UI path.
