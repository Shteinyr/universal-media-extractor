# v0 UI Port

Date: 2026-05-30

## Status

Completed as a UI refinement of the current MVP.

This is not a new roadmap block. The working app remains the existing FastAPI backend with a static HTML/CSS/vanilla JS frontend.

## What Was Taken From v0

The downloaded v0 UI was used as a UX reference, not as production code.

Transferred patterns:

- compact desktop utility layout;
- fixed left sidebar with app title, mode switch, input, backend status, flow, and recent results;
- central working area for the active media item and processing cards;
- concise media item card;
- segmented output selector for `Audio`, `Video`, and `Subtitles`;
- compact selectable output rows;
- short download/transcription/result panels;
- file-manager-like generated files and recent outputs;
- darker local-utility visual tone.

## What Was Not Ported

- No Next.js app was copied.
- No React components were added to the main project.
- No Tailwind build step was added.
- No shadcn/ui or Radix components were installed.
- No lucide-react runtime was added.
- No Vercel analytics was added.
- No mock data replaced real API data.
- No backend endpoints or processing services were changed.

## Why Vanilla Stayed

The current MVP already has a working local-only FastAPI backend and static UI connected to real endpoints. Replacing it with the v0 project would introduce a separate frontend stack and mock state while risking the working flows.

The safer path was to translate v0's layout ideas into the existing static files:

- `index.html` keeps the existing DOM IDs used by `app.js`;
- `styles.css` now carries the compact downloader/file-manager visual system;
- `app.js` keeps the same API calls and job polling, with only a small UX adjustment to show the first available output group after analysis.

## UI Changes

- The left panel now behaves like a compact app sidebar.
- The main panel is a focused work area instead of a broad dashboard.
- The empty state is shorter and more task-oriented.
- The media card is tighter and more file-item-like.
- Output selector remains `Audio / Video / Subtitles`, but now opens the first available group by default.
- Format rows remain short and deduplicated:
  - audio: `M4A · 1.69 MB`;
  - video: `MP4 · 1080p · 13.29 MB`;
  - subtitles: `EN · Auto captions`.
- Recent results are visually compact file rows.
- Download, transcription, warnings, errors, and result files are visually quieter.

## Preserved Behavior

The following flows and endpoints were preserved:

- `POST /analyze`;
- `POST /download`;
- `POST /transcribe`;
- `GET /jobs/{job_id}`;
- `POST /jobs/{job_id}/cancel`;
- `GET /outputs`;
- `DELETE /outputs/{output_id}`;
- URL flow;
- local file flow;
- job polling;
- cancel buttons;
- recent results;
- safe delete;
- copy transcript / summary prompt / output path.

## Verification

Commands:

```bash
node --check src/universal_media_extractor/static/app.js
node --check src/universal_media_extractor/static/option_normalizer.js
.venv/bin/python -m pytest -q
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/v0_ui_port
```

Result:

```text
76 passed
Browser smoke completed
```

Additional browser proof screenshots:

```text
proof/v0_ui_port/ui_initial.png
proof/v0_ui_port/ui_analyze_result.png
proof/v0_ui_port/ui_output_selector.png
proof/v0_ui_port/ui_recent_results.png
```

The backend was stopped after verification.

## Limitations

- The UI is still static HTML/CSS/vanilla JS.
- No dedicated visual regression suite was added.
- No native folder opening was added.
- No desktop wrapper, extension, batch mode, cookies/login, auth/database, or AI summary was added.
- The v0 reference path differs from the user-provided path on disk; this is recorded in `docs/V0_UI_REFERENCE_AUDIT.md`.
