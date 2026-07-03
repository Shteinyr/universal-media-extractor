# Phase 15 Error-State Refinement

Date: 2026-05-29

## Scope

Phase 15 refined error states for the existing analysis-only UI/API without adding product features.

Not added:

- download;
- Whisper/transcription;
- local file upload;
- extension;
- desktop wrapper;
- auth/database/cookies;
- settings page;
- React/Vite;
- external CDN/assets;
- new notification/toast/modal system;
- media processing actions.

## Error States Covered

Frontend:

- empty URL;
- invalid URL;
- API unavailable/network failure;
- API error response;
- `AnalyzeResult.errors`;
- unsupported source;
- login required;
- cookies required;
- generic analyzer failure;
- retry by pressing `Analyze` again.

Backend/API:

- empty URL returns `422` before analyzer is called;
- invalid non-http(s) URL returns `422` before analyzer is called;
- analyzer errors are preserved in `AnalyzeResult.errors`;
- job state becomes `failed` when analyzer errors exist.

Not errors:

- no subtitles;
- no automatic captions;
- warnings such as `format_size_unknown`;
- platform/best-effort warnings.

These remain warnings or empty states in the UI.

## Changes Made

### Frontend

File: `src/universal_media_extractor/static/app.js`

Changes:

- added explicit empty URL handling before fetch;
- improved invalid URL message;
- separated API error responses from API unavailable/network failures;
- added `normalizeNetworkError`;
- improved parsing of FastAPI validation errors from `detail`;
- added code-specific messages and suggested actions for:
  - `unsupported_source`;
  - `login_required`;
  - `cookies_required`;
  - `network_error`;
  - `timeout`;
  - `ytdlp_not_found`;
  - `extractor_failed`;
  - `invalid_output`;
- kept warnings and errors rendered separately;
- kept subtitles/captions empty states neutral.

### Backend/API

File: `src/universal_media_extractor/api/schemas.py`

Changes:

- added a Pydantic v2 `field_validator` for `AnalyzeRequest.url`;
- URL must parse as `http` or `https` with a network location;
- invalid values raise `ValueError("Enter a valid http or https URL.")`;
- this prevents analyzer calls for malformed URLs.

### Tests

File: `tests/test_api_app.py`

Added/updated checks:

- static JS includes error-state strings;
- empty URL returns `422` and does not call the analyze service;
- invalid URL returns `422` and does not call the analyze service;
- login-required analyzer error becomes a failed job while preserving `AnalyzeResult.errors`.

## Verification

Automated tests:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
36 passed
```

Live HTTP/API checks with backend on `127.0.0.1:8000`:

- `GET /` returned the UI;
- `GET /static/app.js` returned JavaScript with refined error handling;
- `POST /analyze` with `not-a-url` returned `422`;
- real `POST /analyze` for `https://youtu.be/UUdxAp3kuKA` returned:
  - job status `succeeded`;
  - title `Showreel`;
  - zero errors;
  - expected warnings;
  - subtitles `0`;
  - automatic captions `0`.

Proof files:

- `proof/phase_15/ui_initial.html`
- `proof/phase_15/app.js`
- `proof/phase_15/invalid_url_response.json`
- `proof/phase_15/invalid_url_status.txt`
- `proof/phase_15/analyze_response.json`
- `proof/phase_15/analyze_response_pretty.json`

## Manual Check Notes

Useful manual checks:

- submit empty input and expect `URL required`;
- submit `not-a-url` and expect `Invalid URL`;
- stop backend, open already-loaded UI, submit a valid URL, and expect `API unavailable`;
- submit `https://youtu.be/UUdxAp3kuKA` and expect the normal `Showreel` result;
- confirm warnings are in the warnings panel, not the errors panel;
- confirm empty subtitles/captions are neutral empty states.

Browser/Playwright screenshot verification was still unavailable in the local toolchain.

## What Did Not Change

- `AnalyzeResult` contract;
- endpoint path `/analyze`;
- response model shape;
- local-only backend binding;
- analyzer command behavior;
- media processing behavior;
- static UI architecture.

## Remaining Limits

- no browser automation screenshots;
- no JS unit-test framework;
- no offline UI mock mode;
- no cancellation/progress tracking;
- no persistent jobs;
- no download/transcription/local-file flows.
