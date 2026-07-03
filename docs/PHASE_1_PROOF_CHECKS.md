# Phase 1 Proof Checks

Date: 2026-05-29

## Scope

Only minimal safe checks were performed. No media was downloaded, no test URL was invented, and no app code was created.

## Checks Performed

| Check | Command | Result |
|---|---|---|
| System Python available | `python3 --version` | Works: `Python 3.14.4` |
| Virtualenv Python available | `.venv/bin/python --version` | Works: `Python 3.14.4` |
| FastAPI import | `.venv/bin/python -c "import fastapi"` | Works: `0.136.3` |
| Uvicorn import | `.venv/bin/python -c "import uvicorn"` | Works: `0.48.0` |
| Pydantic import | `.venv/bin/python -c "import pydantic"` | Works: `2.13.4` |
| `python-multipart` import | `.venv/bin/python -c "import multipart"` | Works |
| `aiofiles` import | `.venv/bin/python -c "import aiofiles"` | Works |
| `ffmpeg` available | `ffmpeg -version` | Works: `8.1.1` |
| `ffprobe` available | `ffprobe -version` | Works: `8.1.1` |
| `yt-dlp` version | `yt-dlp --version` | Works: `2026.03.17` |
| `yt-dlp` help | `yt-dlp --help` | Works; help text printed |
| Whisper CLI help | `whisper --help` | Works; CLI usage printed |

## What Works

- The project has a local `.venv`.
- Minimal backend dependencies install and import successfully under Python 3.14.4.
- `ffmpeg`, `ffprobe`, `yt-dlp`, and Whisper CLI are present on PATH.
- `yt-dlp --help` is available, confirming the CLI is callable.
- `whisper --help` is available, confirming the CLI is callable.

## What Was Not Checked

- `yt-dlp -F` / list formats against a real URL was not checked because the user did not provide a test link.
- No URL metadata extraction was run.
- No media download was run.
- No local audio/video transcription was run.
- No long-file performance test was run.
- No backend server was created or started.
- No browser UI was created.

## What Requires A Test Link From The User

To safely test URL analysis in Phase 2, the user should provide one legally permitted public test URL. The first URL proof should use analysis-only commands such as:

```bash
yt-dlp --simulate --list-formats "<USER_PROVIDED_URL>"
yt-dlp --simulate --dump-json "<USER_PROVIDED_URL>"
```

No test URL should be guessed automatically.

## Remaining Risks

- Source support remains best-effort and site-dependent.
- Some sources may require cookies/login, which is not implemented in Phase 1 and remains future/manual only.
- DRM, CAPTCHA, paywall, and unauthorized access remain out of scope.
- Whisper performance on CPU is still unbenchmarked.
- Large file disk usage and cleanup behavior are not yet tested.
- No app-level local-only binding has been tested because backend implementation has not started.

