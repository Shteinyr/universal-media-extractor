# Phase 1 Environment Setup

Date: 2026-05-29

## Scope

Phase 1 prepared the local Python environment only. No backend app, frontend, routes, downloader module, transcription module, Chrome extension, or desktop wrapper was created.

## Commands Executed

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install fastapi 'uvicorn[standard]' pydantic python-multipart aiofiles
.venv/bin/python --version
.venv/bin/python -m pip --version
.venv/bin/python -m pip freeze
.venv/bin/python - <<'PY'
import fastapi, uvicorn, pydantic, multipart, aiofiles
print('fastapi', fastapi.__version__)
print('uvicorn', uvicorn.__version__)
print('pydantic', pydantic.__version__)
print('python-multipart import ok')
print('aiofiles import ok')
PY
```

## Python Environment

- Virtual environment path: `/Users/aleksandr/Documents/Codex/Projects/universal-media-extractor/.venv`
- Virtual environment Python: `Python 3.14.4`
- Virtual environment pip: `pip 26.1.1`

## Installed Direct Dependencies

These are the dependencies intentionally added for the future local backend:

- `fastapi==0.136.3`
- `uvicorn[standard]==0.48.0`
- `pydantic==2.13.4`
- `python-multipart==0.0.29`
- `aiofiles==25.1.0`

## Installed Transitive Dependencies

Observed via `.venv/bin/python -m pip freeze`:

- `annotated-doc==0.0.4`
- `annotated-types==0.7.0`
- `anyio==4.13.0`
- `click==8.4.1`
- `h11==0.16.0`
- `httptools==0.8.0`
- `idna==3.17`
- `pydantic_core==2.46.4`
- `python-dotenv==1.2.2`
- `PyYAML==6.0.3`
- `starlette==1.2.0`
- `typing-inspection==0.4.2`
- `typing_extensions==4.15.0`
- `uvloop==0.22.1`
- `watchfiles==1.2.0`
- `websockets==16.0`

## Tool Versions Found

- System Python: `Python 3.14.4`
- Virtualenv Python: `Python 3.14.4`
- `ffmpeg`: `8.1.1`
- `ffprobe`: `8.1.1`
- `yt-dlp`: `2026.03.17`
- Whisper CLI: available at `/Users/aleksandr/.local/bin/whisper`; help command works.

## Tool Paths Found

- `python3`: `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`
- `ffmpeg`: `/opt/homebrew/bin/ffmpeg`
- `ffprobe`: `/opt/homebrew/bin/ffprobe`
- `yt-dlp`: `/opt/homebrew/bin/yt-dlp`
- `whisper`: `/Users/aleksandr/.local/bin/whisper`

## Recreate / Repeat Commands

From `/Users/aleksandr/Documents/Codex/Projects/universal-media-extractor`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

## Notes

- `requirements.txt` contains only the direct Phase 1 dependencies requested for the local backend.
- The environment setup did not create any application code.
- During install, pip printed cache deserialization warnings, but dependency installation completed successfully.

