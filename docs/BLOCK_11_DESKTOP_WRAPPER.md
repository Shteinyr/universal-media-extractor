# Block 11. Desktop Wrapper

Date: 2026-05-31

## Status

Completed.

Block 11 adds a local desktop launcher for the existing app. It keeps the current FastAPI backend, static vanilla UI, and browser mode.

## What Was Added

Created:

```text
scripts/run_desktop.py
```

The script:

- finds an available local port, preferring `8000`;
- starts the existing FastAPI app through Uvicorn on `127.0.0.1`;
- opens the actual app URL in a `pywebview` desktop window;
- uses the existing dark static UI;
- shuts down the owned backend after the window closes;
- does not open an external browser.

Window settings:

```text
Title: Universal Media Extractor
Initial size: 1280x820
Minimum size: 980x680
```

Dependency added:

```text
pywebview==6.2.1
```

## Run Desktop App

From the project root:

```bash
cd /Users/aleksandr/Documents/Codex/Projects/universal-media-extractor
.venv/bin/python scripts/run_desktop.py
```

If `8000` is busy, the script chooses the next free local port through `8020` and opens the desktop window on that actual port.

Development proof helper:

```bash
.venv/bin/python scripts/run_desktop.py --smoke-seconds 3
```

This opens the desktop window briefly and closes it automatically. It is for local proof only.

## Run Browser Mode

Browser mode is unchanged:

```bash
cd /Users/aleksandr/Documents/Codex/Projects/universal-media-extractor
.venv/bin/python scripts/run_api.py
```

Open:

```text
http://127.0.0.1:8000/
```

## Verification

Tests:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
85 passed
```

Desktop smoke:

```bash
.venv/bin/python scripts/run_desktop.py --smoke-seconds 3
```

Result:

```text
Desktop UI: http://127.0.0.1:8001/
```

`8001` was selected because `8000` was already occupied. The backend on `8001` was stopped after the desktop window closed.

Browser mode health proof:

```bash
.venv/bin/python scripts/run_api.py --port 8766
```

Then `/health` returned:

```json
{"status":"ok","service":"universal-media-extractor","mode":"local-only"}
```

Browser UI smoke proof:

```bash
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/block_11/browser_smoke
```

Screenshots:

```text
proof/block_11/browser_smoke/ui_initial.png
proof/block_11/browser_smoke/ui_analyze_result.png
```

## What Works

- Desktop window opens the current local UI.
- Backend remains local-only on `127.0.0.1`.
- Existing browser mode still works.
- Existing URL/local-file/download/transcribe/recent-results code paths are reused.
- No second backend is started on an occupied port.
- The owned desktop backend is stopped after the desktop window closes in the smoke proof.

## Not Included

- No signed `.app`.
- No notarization.
- No installer.
- No Electron.
- No Chrome extension.
- No React/Vite/Next rewrite.
- No auth/database/cookies.
- No batch processing.
- No AI summary API.
- No backend API changes.
- No roadmap changes.

## Packaging Note

PyInstaller can create macOS `.app` bundles, but a polished distributable app needs a separate packaging task:

- collect static files correctly;
- verify pywebview/PyObjC bundling;
- decide whether CLIs such as `yt-dlp`, `ffmpeg`, and `whisper` are bundled or treated as external dependencies;
- add signing/notarization if distributing outside the local machine.
