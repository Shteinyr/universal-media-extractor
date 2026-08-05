# Commercial Block 7: macOS Production Build Foundation

Status: completed foundation.

GitHub issue: #12 `[P0] Build production macOS Apple Silicon app`.

## What Was Implemented

- Added a PyInstaller-based macOS production app build script: `scripts/build_macos_app.py`.
- Added macOS PyInstaller spec: `packaging/macos/universal_media_extractor_macos.spec`.
- Added packaging dependency pin: `requirements-packaging.txt`.
- Updated `scripts/run_desktop.py` with production runtime paths for frozen `.app` launches.
- Added Finder-safe CLI path setup so GUI launches can find Homebrew tools such as `yt-dlp`, `ffmpeg`, and `whisper`.
- Kept the backend local-only on `127.0.0.1`.
- Kept browser/dev launch paths unchanged.

## Build Output

Production-foundation app bundle:

```text
build/macos/dist/Universal Media Extractor.app
```

This is a local production-foundation `.app`, not a signed/notarized public installer.

## Runtime Paths

In production desktop mode:

- app data: `~/Library/Application Support/Universal Media Extractor`;
- raw analysis artifacts: `~/Library/Application Support/Universal Media Extractor/analysis`;
- job database: `~/Library/Application Support/Universal Media Extractor/jobs.sqlite3`;
- user outputs: `~/Downloads/Universal Media Extractor`.

In dev mode, existing project defaults remain unchanged.

## Commands

Install packaging dependency:

```bash
.venv/bin/python -m pip install -r requirements-packaging.txt
```

Build macOS app:

```bash
.venv/bin/python scripts/build_macos_app.py
```

Run smoke check:

```bash
open -W "build/macos/dist/Universal Media Extractor.app" --args --smoke-seconds 3
```

Direct executable smoke, useful for captured logs:

```bash
"build/macos/dist/Universal Media Extractor.app/Contents/MacOS/Universal Media Extractor" --smoke-seconds 3
```

## Verification

Executed successfully:

```bash
.venv/bin/python -m py_compile scripts/run_desktop.py scripts/build_macos_app.py
.venv/bin/python -m pytest tests/test_build_macos_app.py -q
.venv/bin/python scripts/build_macos_app.py
open -W "build/macos/dist/Universal Media Extractor.app" --args --smoke-seconds 3
"build/macos/dist/Universal Media Extractor.app/Contents/MacOS/Universal Media Extractor" --smoke-seconds 3
```

The direct executable smoke confirmed backend startup on `127.0.0.1`, UI URL creation, and backend shutdown after the pywebview smoke window closed.

## Not Included

- Apple Developer ID signing. Tracked separately by issue #13.
- Notarization. Tracked separately by issue #13.
- DMG installer. Tracked separately by issue #14.
- Windows build.
- Payment/licensing/website work.
- Bundling external media engines into the app. The GUI app currently expects `yt-dlp`, `ffmpeg`, and `whisper` to be available from standard Homebrew/system CLI paths.

## Remaining Production Risks

- Public distribution still requires signing, notarization, and installer work.
- A user machine without Homebrew CLI dependencies will need either dependency installation instructions or a later bundled-engine strategy.
- Some macOS security prompts may appear when first running locally built unsigned apps.
