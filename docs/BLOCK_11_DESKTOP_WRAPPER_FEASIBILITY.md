# Block 11. Desktop Wrapper Feasibility

Date: 2026-05-31

## Status

Feasible for a development/local desktop wrapper.

Chosen approach: `pywebview` wrapping the existing local FastAPI app.

This block does not replace the backend, does not replace the static frontend, and does not add Electron, React, Vite, Next.js, Chrome extension, AI summary, batch, auth/database/cookies, or roadmap changes.

## Documentation Checked

Context7 / official sources checked:

- `pywebview`: `/r0x0r/pywebview`.
- Uvicorn: `/kludex/uvicorn`.
- PyInstaller: `/websites/pyinstaller_en_stable`.
- FastAPI static files official documentation: `https://fastapi.tiangolo.com/tutorial/static-files/`.

Relevant findings:

- `pywebview.create_window(title, url, width, height, min_size=...)` can open a local URL in a native desktop window.
- `webview.start()` starts the GUI event loop.
- Uvicorn can be run programmatically with `uvicorn.Config` and `uvicorn.Server`.
- FastAPI already serves the current static UI through `StaticFiles` and `/`.
- PyInstaller can create macOS `.app` bundles later, but packaging/signing/notarization should be treated as a separate hardening task.

## Environment Check

Current Python:

```text
Python 3.14.4
```

Installed desktop dependency:

```text
pywebview==6.2.1
```

Transitive macOS GUI dependencies installed by pip include PyObjC Cocoa/WebKit/Quartz packages.

PyInstaller is not installed in this block because packaging is only a feasibility note, not a deliverable.

## Selected Architecture

The wrapper starts an in-process Uvicorn server bound to localhost:

```text
127.0.0.1:<available_port>
```

Then it opens that URL in a `pywebview` window.

Browser mode remains separate:

```bash
.venv/bin/python scripts/run_api.py
```

Desktop mode:

```bash
.venv/bin/python scripts/run_desktop.py
```

## Port Handling

The launcher prefers `127.0.0.1:8000`.

If port `8000` is busy, it scans the local range up to `8020` and opens the desktop UI on the first available local port.

Observed proof:

```text
8000 was already busy.
Desktop wrapper selected 8001.
Desktop UI opened at http://127.0.0.1:8001/.
Backend on 8001 shut down after the desktop window closed.
```

## Shutdown Behavior

The launcher owns the Uvicorn `Server` instance and runs it in a background thread.

When `pywebview.start()` returns after the window closes, the launcher sets:

```python
server.should_exit = True
```

Then it waits briefly for the backend thread.

This is adequate for local development. Production packaging may need more lifecycle hardening.

## Risks

- GUI automation inside `pywebview` is not part of normal `pytest`.
- The wrapper depends on macOS WebKit/PyObjC working in the local Python environment.
- If the backend has a long-running active job during window close, job subprocess behavior remains governed by the existing job/cancel logic.
- A signed/notarized `.app` is not produced in this block.
- Packaging may require extra PyInstaller hooks/data collection for static files, CLIs, and pywebview dependencies.

## Verdict

`pywebview` is suitable for Block 11 as a lightweight local desktop wrapper.

The core app stays FastAPI + static HTML/CSS/JS. Desktop packaging into a distributable `.app` should be handled later as a dedicated packaging/signing task if the user approves it.
