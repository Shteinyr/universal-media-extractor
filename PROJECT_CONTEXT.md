# Project Context

## Project Identity

- Name: Universal Media Extractor.
- Working directory: `/Users/aleksandr/Developer/Codex/Projects/Universal Media Extractor`.
- Product: local media downloader/transcriber for URLs and local audio/video files.
- Current status: Blocks 1-11 completed; Udemy Course Offline Export with Chrome session auth added and refined after real user testing; commercial strategy imported; GitHub roadmap created; Commercial Foundation issues #1-#5 completed; Commercial Block 2 issues #6-#7 completed for normalized errors and diagnostics foundation.
- Roadmap source: `docs/ROADMAP_V2.md`.
- Commercial strategy source: `docs/UNIVERSAL_MEDIA_EXTRACTOR_PRODUCT_STRATEGY.md`.
- GitHub commercial roadmap board: `https://github.com/users/Shteinyr/projects/7`.

## Product Goal

Universal Media Extractor is a local, single-user media utility.

Primary flows:

- URL -> Analyze -> Download -> Transcribe -> Result.
- Local file -> Analyze -> Transcribe -> Result.
- Udemy lecture/player URL + Chrome session -> Analyze course playlist -> Download course.

The product should help a user inspect available outputs, choose a clear result, save files locally, and optionally create a local Whisper transcript without paid APIs or cloud processing.

Commercial direction after GPT Pro strategy review:

- position as `Local Media Downloader & Organizer for macOS and Windows`;
- sell installation, organization, presets, history, batch, compatibility updates, diagnostics, and local processing rather than merely `yt-dlp` execution;
- keep Udemy Course mode internal/experimental for now and hidden from public builds/marketing;
- avoid public claims around universal source support, DRM, paywall, CAPTCHA, or login bypass;
- prepare direct website distribution first, Microsoft Store later, and avoid Mac App Store for the full downloader.

## Core Principles

- Local-first.
- Single-user.
- Best-effort source support through `yt-dlp`.
- No paid APIs by default.
- No online service behavior.
- No external data sending.
- Backend binds only to `127.0.0.1`.
- Download/process actions preserve rights-confirmation requirements in the backend contract.
- No DRM, CAPTCHA, paywall, login, or platform restriction bypass.
- Udemy support uses Chrome session auth by default, keeps manual cookies as advanced fallback, and must not store credentials or bypass DRM. Public builds hide Course Mode by setting `UME_PUBLIC_PRODUCT_MODE=1`.
- Codex recommendations are recommendations only, not roadmap decisions.

## Current Architecture

- Python backend.
- FastAPI local API.
- Uvicorn local server.
- Static vanilla HTML/CSS/JS frontend.
- `yt-dlp` for URL analysis/download.
- `ffmpeg`/`ffprobe` for media metadata, extraction, and conversion.
- Whisper CLI for local transcription.
- In-memory job system for download/transcription.
- Output indexing and safe delete for managed result folders.
- Python Playwright for manual/dev browser smoke checks.
- `pywebview` for the local desktop wrapper.
- Udemy course analyze/download service through `yt-dlp`.
- Shared error normalization and local redacted diagnostics bundles for failed jobs.

## Completed Roadmap

- Block 1. Analysis Foundation - done.
- Block 2. Download + Output Pipeline - done.
- Block 3. Whisper + Transcript Pipeline - done.
- Block 4. Processing UI + MVP Flow - done.
- Block 5. MVP Readiness Review - done.
- Block 6. Job / Progress / Cancel - done.
- Block 7. Local File Input - done.
- Block 8. Cleanup / Output Management - done.
- Block 9. Real Progress / Subprocess Cancellation Hardening - done.
- Block 10. Browser Verification / UI QA Tooling - done.
- Block 11. Desktop Wrapper - done.

## Latest Completed Block

Udemy Course Offline Export initial implementation - done.

Result: the app has Course mode plus `POST /udemy/analyze` and `POST /udemy/download`. It uses `yt-dlp --cookies-from-browser chrome` by default, with manual `cookies.txt` only as an advanced fallback. It does not store passwords/cookies and does not implement DRM/key/CAPTCHA/paywall bypass.

User testing showed that some clean Udemy `/course/<slug>/` URLs can fail in `yt-dlp` with `Unable to extract course id`, while the URL from an opened course lecture/player can return the full course playlist. The UI must preserve pasted lecture/player URLs and not rewrite them into clean course URLs.

Desktop command:

```bash
.venv/bin/python scripts/run_desktop.py
```

The wrapper starts Uvicorn on `127.0.0.1`, opens the actual UI in a native window, and shuts down its owned backend when the window closes.

Udemy command path is documented in `docs/UDEMY_COURSE_EXPORT.md`.

## Planned Next Block

Commercial Foundation and Commercial Block 2 Errors + Diagnostics Foundation are completed. The previous Roadmap v2 next block was Block 12 Chrome Extension, but commercialization strategy now recommends prioritizing Public Beta Readiness before extension work.

Recommended next user-approved commercial block:

```text
Public Beta Readiness
```

Candidate issues: normalized user-facing errors, diagnostics bundle, localhost security hardening, preset-based output selection, SQLite-backed jobs/history, and output templates.

Do not start the next block until the user explicitly confirms.

## Later / Optional

- Batch processing.
- Cookies/login manual mode.
- AI summary API.
- Presets.
- History/search.
- Advanced settings.
- Output retention policy.
- Advanced cleanup policies.

## Current Working Commands

Run browser mode:

```bash
cd "/Users/aleksandr/Developer/Codex/Projects/Universal Media Extractor"
.venv/bin/python scripts/run_api.py
```

Open:

```text
http://127.0.0.1:8000/
```

Run tests:

```bash
.venv/bin/python -m pytest -q
```

Run browser smoke:

```bash
.venv/bin/python scripts/browser_smoke.py
```

Run desktop mode:

```bash
.venv/bin/python scripts/run_desktop.py
```

Build development `.app` launcher:

```bash
.venv/bin/python scripts/build_dev_app.py
open "build/dev/Universal Media Extractor Dev.app"
```

The dev `.app` can also be copied to `/Applications`; it remains tied to this project folder and `.venv`.

## Important Existing Behavior

- UI is simplified into a compact downloader/file-manager style.
- Final UI cleanup hides development-oriented sidebar areas: visible backend status, MVP flow checklist, repeated helper copy, and Recent results.
- URL downloads default to `~/Downloads/Universal Media Extractor`.
- The download card has editable `Save to` and `Format` controls.
- Video output downloads selected video together with best available audio into one final file.
- Audio output downloads/extracts audio-only results.
- Subtitles output downloads subtitles/captions and should not show transcription as the next action.
- Transcription requires an audio file or a video file with an audio track.
- Transcript output saves one selected format per run: `TXT`, `Markdown`, or `JSON`.
- Video options below `1080p` are hidden in the main UI.
- User-facing video and subtitle options are deduplicated before rendering.
- Recent results work for the configured output base.
- Safe delete is constrained to managed output folders.
- `proof/` is development evidence and is not indexed as user output.

## Key Files

- `src/universal_media_extractor/api/app.py`
- `scripts/run_api.py`
- `scripts/run_desktop.py`
- `scripts/build_dev_app.py`
- `src/universal_media_extractor/static/index.html`
- `src/universal_media_extractor/static/styles.css`
- `src/universal_media_extractor/static/app.js`
- `src/universal_media_extractor/services/job_service.py`
- `src/universal_media_extractor/services/download_service.py`
- `src/universal_media_extractor/services/transcription_service.py`
- `src/universal_media_extractor/services/output_manager.py`
- `src/universal_media_extractor/services/local_file_metadata_service.py`

## Governance

- Do not create new Phase numbering.
- Do not create new Blocks without explicit user approval.
- If Codex sees a better path, blocker, or risk, it may recommend a change, but must not change the roadmap itself.
- Follow `docs/ROADMAP_V2.md` unless the user explicitly changes it.
- Before every large task, read `PROJECT_CONTEXT.md`.
- After every completed block, update `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`, `CHANGELOG.md`, `README.md`, and relevant docs.


## Commercial Foundation Docs

- `docs/PUBLIC_PRODUCT_BOUNDARY.md`
- `docs/LEGAL_SAFE_PRODUCT_COPY.md`
- `docs/EULA_DRAFT.md`
- `docs/PRIVACY_POLICY_DRAFT.md`
- `docs/REFUND_POLICY_DRAFT.md`
- `docs/PUBLIC_KNOWN_LIMITATIONS.md`

These documents close GitHub issues #1-#5 and define the public product boundary for future website, packaging, and beta work.


## Commercial Block 2 Docs

- `docs/COMMERCIAL_BLOCK_2_ERRORS_DIAGNOSTICS.md`

This document closes GitHub issues #6-#7 and defines the first public-beta diagnostics boundary.
