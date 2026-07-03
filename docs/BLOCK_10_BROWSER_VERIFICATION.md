# Block 10. Browser Verification / UI QA Tooling

Date: 2026-05-30

## Status

Completed.

Block 10 adds minimal browser verification tooling for the local static UI. It does not add a new frontend stack, React, Vite, CDN assets, API changes, download/transcribe behavior changes, desktop wrapper, Chrome extension, auth/database/cookies, or AI summary.

## Tooling Chosen

Chosen tooling: Python Playwright in the existing project `.venv`.

Reason:

- fits the Python backend project;
- avoids Node project setup and frontend build tooling;
- supports Chromium screenshots and UI interaction from a standalone script;
- can remain a manual/dev smoke command rather than part of normal `pytest`.

Installed dependency:

```text
playwright==1.60.0
```

Browser installed:

```bash
.venv/bin/python -m playwright install chromium
```

Verification:

```bash
.venv/bin/python -m playwright --version
```

Result:

```text
Version 1.60.0
```

Chromium launch check succeeded in headless mode.

## Smoke Script

Created:

```text
scripts/browser_smoke.py
```

The backend must already be running:

```bash
.venv/bin/python scripts/run_api.py
```

Default smoke command:

```bash
.venv/bin/python scripts/browser_smoke.py
```

Default behavior:

- opens `http://127.0.0.1:8000/`;
- captures initial UI screenshot;
- fills `https://youtu.be/UUdxAp3kuKA`;
- clicks `Analyze`;
- waits for `Showreel`;
- verifies audio/video/combined groups are visible;
- captures analyze-result screenshot;
- does not download;
- does not transcribe.

Optional full flow:

```bash
.venv/bin/python scripts/browser_smoke.py --full-flow
```

The full-flow flag is intentionally off by default. If enabled, it may download/transcribe using the current UI flow and create extra screenshots.

## Screenshots

Default screenshots:

```text
proof/block_10/ui_initial.png
proof/block_10/ui_analyze_result.png
```

Optional full-flow screenshots:

```text
proof/block_10/ui_download_result.png
proof/block_10/ui_transcribe_result.png
```

## Manual Proof

Commands:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python scripts/run_api.py
.venv/bin/python scripts/browser_smoke.py
```

Results:

```text
73 passed
Browser smoke completed. Screenshots: /Users/aleksandr/Documents/Codex/Projects/universal-media-extractor/proof/block_10
```

Created screenshots:

```text
proof/block_10/ui_initial.png
proof/block_10/ui_analyze_result.png
```

Confirmed through the browser smoke:

- local UI opens at `http://127.0.0.1:8000/`;
- URL input is visible and fillable;
- `Analyze` button works;
- real API call completes;
- title `Showreel` appears;
- audio formats group appears;
- video-only formats group appears;
- combined formats group appears;
- screenshots can be captured.

The backend was stopped after proof.

## If Browser Automation Is Unavailable

Fallback:

1. Run API tests:

   ```bash
   .venv/bin/python -m pytest -q
   ```

2. Run the backend:

   ```bash
   .venv/bin/python scripts/run_api.py
   ```

3. Open the UI manually:

   ```text
   http://127.0.0.1:8000/
   ```

4. Capture screenshots manually if Playwright browser launch is blocked.

Common blockers:

- Playwright package missing;
- Chromium browser binary not installed;
- macOS browser launch/security restriction;
- backend not running on `127.0.0.1:8000`;
- network/source analysis failure from `yt-dlp`.

## Not Included

- No ordinary `pytest` browser execution.
- No Playwright test framework files.
- No React/Vite/CDN.
- No API changes.
- No download/transcribe logic changes.
- No desktop wrapper.
- No Chrome extension.
- No AI summary API.
- No auth/database/cookies.
- No roadmap changes.
