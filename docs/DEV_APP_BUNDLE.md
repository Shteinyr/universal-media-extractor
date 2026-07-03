# Development App Bundle

Date: 2026-06-03

## Status

Completed as a development workflow refinement.

This is not a final installer and not a production distribution package.

## What It Builds

Created:

```text
scripts/build_dev_app.py
```

The script creates:

```text
build/dev/Universal Media Extractor Dev.app
```

The generated `.app` is a minimal macOS application bundle:

```text
Universal Media Extractor Dev.app/
  Contents/
    Info.plist
    MacOS/
      UniversalMediaExtractorDev
    Resources/
      launcher.zsh
      launcher.c
```

## How It Works

The `.app` does not copy the backend, frontend, services, or dependencies into the bundle.

Instead, its launcher points back to the current project folder:

```text
/Users/aleksandr/Documents/Codex/Projects/universal-media-extractor
```

It runs:

```bash
.venv/bin/python scripts/run_desktop.py
```

This means code changes are picked up the next time the `.app` starts, as long as the project folder and `.venv` remain in place.

`Contents/MacOS/UniversalMediaExtractorDev` is a tiny compiled launcher. This is intentional: Finder/LaunchServices is more reliable with a Mach-O executable than with a shell script as the main app executable.

## Build

From the project root:

```bash
.venv/bin/python scripts/build_dev_app.py
```

## Run

From the project root:

```bash
open "build/dev/Universal Media Extractor Dev.app"
```

Copy to Applications for convenient use:

```bash
rm -rf "/Applications/Universal Media Extractor Dev.app"
cp -R "build/dev/Universal Media Extractor Dev.app" "/Applications/Universal Media Extractor Dev.app"
open "/Applications/Universal Media Extractor Dev.app"
```

Development smoke:

```bash
open -W "build/dev/Universal Media Extractor Dev.app" --args --smoke-seconds 3
```

The app forwards arguments to `scripts/run_desktop.py`, so this smoke command opens the desktop UI briefly and exits automatically.

## Verification

Commands:

```bash
.venv/bin/python -m pytest tests/test_build_dev_app.py tests/test_desktop_launcher.py -q
.venv/bin/python scripts/build_dev_app.py
open -W "build/dev/Universal Media Extractor Dev.app" --args --smoke-seconds 3
.venv/bin/python -m pytest -q
```

Results:

```text
6 passed
Development app created: build/dev/Universal Media Extractor Dev.app
open smoke completed
88 passed
```

No extra backend remained listening on `127.0.0.1:8001` after the smoke run.

After the LaunchServices fix, the app was copied to `/Applications` and verified with:

```bash
open -W "/Applications/Universal Media Extractor Dev.app" --args --smoke-seconds 3
```

Result: the app launched through macOS `open` and exited cleanly.

## Limitations

- The dev `.app` is tied to this exact project path.
- If the project folder moves, the dev `.app` must be rebuilt.
- If `.venv` is missing, the dev `.app` shows an error and exits.
- This is not suitable for other users or another machine.
- It is not signed, notarized, packaged as `.dmg`, or self-contained.
- Final distributable packaging remains a separate future packaging task.
