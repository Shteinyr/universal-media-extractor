# Roadmap v2

Date: 2026-05-30

## Status

Blocks 1-11 are completed.

The current next planned block is Block 12, but it must not start until the user explicitly confirms it.

## Core Roadmap

### Block 1. Analysis Foundation - Done

- URL analyze.
- `AnalyzeResult` models.
- `yt-dlp` normalizer.
- analyzer wrapper.
- FastAPI `/analyze`.
- analysis-only UI.

### Block 2. Download + Output Pipeline - Done

- selected format download.
- safety confirmation.
- output structure.
- `/download`.

### Block 3. Whisper + Transcript Pipeline - Done

- Whisper CLI transcription.
- video -> audio extraction.
- transcript files.
- `summary_prompt.md`.
- `/transcribe`.

### Block 4. Processing UI + MVP Flow - Done

- unified UI flow.
- Analyze -> Download -> Transcribe -> Result.
- format selection.
- transcript preview.
- copy actions.

### Block 5. MVP Readiness Review - Done

- full MVP smoke test.
- output review.
- known limitations.
- README readiness.

### Block 6. Job / Progress / Cancel - Done

- job-based download/transcription.
- polling.
- cancel flag.
- current step/status.

### Block 7. Local File Input - Done

- URL mode / local file mode.
- local file metadata via `ffprobe`.
- local file transcription.
- local output structure.

### Block 8. Cleanup / Output Management - Done

- output index.
- recent results.
- safe delete.
- `/outputs` endpoints.
- proof separation.

### Block 9. Real Progress / Subprocess Cancellation Hardening - Done

- real progress parsing from `yt-dlp`, `ffmpeg`, and Whisper where practical.
- stronger subprocess cancellation.
- clearer long-running task behavior.

### Block 10. Browser Verification / UI QA Tooling - Done

- Playwright/browser setup if possible.
- local UI visual smoke tests.
- screenshots.
- manual fallback if browser tooling remains blocked.

### Block 11. Desktop Wrapper - Done

- package local web-app as desktop app.
- likely `pywebview` or equivalent.
- no rewrite of core.

### Block 12. Chrome Extension - Planned

- "Send current page to app".
- local app connection.
- no media extraction inside extension.

## Later / Optional

These are not in the core roadmap unless the user explicitly promotes them:

- batch processing.
- cookies/login manual mode.
- AI summary API.
- presets.
- history/search.
- advanced settings.
- output retention policy.
- advanced cleanup policies.

## Current MVP

The MVP currently works for:

- URL -> Analyze -> Download -> Transcribe -> Result.
- Local file -> Analyze -> Transcribe -> Result.

## Governance

- Do not create new Phase numbering.
- Do not create new Blocks without explicit user approval.
- Codex recommendations are recommendations only, not roadmap decisions.
- Codex may suggest alternatives when it sees a blocker, risk, or better path.
- Any roadmap change must be presented to the user as a recommendation and must wait for user confirmation.
- After each completed block, update `PROJECT_STATE.md`, `CHANGELOG.md`, `README.md`, and relevant docs.
- If a task is a subtask inside the current block, do not promote it into a new block.
- Follow Roadmap v2 unless the user explicitly changes it.
