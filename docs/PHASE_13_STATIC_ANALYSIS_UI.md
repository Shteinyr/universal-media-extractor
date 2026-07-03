# Phase 13 Static Analysis UI

Date: 2026-05-29

## Scope

Phase 13 created the first minimal static UI for the analysis-only scenario:

```text
Paste URL -> Analyze -> Display normalized AnalyzeResult
```

No download, Whisper/transcription, local file upload, Chrome extension, desktop wrapper, auth, database, cookies/login, settings page, build tool, React, Vite, CDN, or external asset bundle was added.

## Created

Static UI files:

- `src/universal_media_extractor/static/index.html`
- `src/universal_media_extractor/static/styles.css`
- `src/universal_media_extractor/static/app.js`

FastAPI static serving:

- `GET /` returns `index.html`;
- `/static/styles.css` serves CSS;
- `/static/app.js` serves JavaScript.

Tests:

- `tests/test_api_app.py` now checks that static index and JS are available.

## How To Open

Start the local backend:

```bash
.venv/bin/python scripts/run_api.py
```

Open:

```text
http://127.0.0.1:8000/
```

The backend remains local-only through `scripts/run_api.py`, which binds Uvicorn to `127.0.0.1`.

## API Endpoint Used

The UI calls:

```http
POST /analyze
Content-Type: application/json
```

Request shape:

```json
{
  "source_type": "url",
  "url": "https://youtu.be/UUdxAp3kuKA",
  "user_confirmed_rights": false
}
```

The JavaScript uses a same-origin request:

```js
fetch(`${API_BASE_URL}/analyze`, ...)
```

where `API_BASE_URL` is an empty string for the current static UI.

## What The UI Shows

Header:

- `Universal Media Extractor`;
- `Analyze media links locally. No download in this mode.`

Input panel:

- URL input;
- `Analyze` button;
- analysis-only hint;
- safety note.

Loading state:

- disabled button;
- `Analyzing...`;
- no fake progress.

Result state:

- thumbnail;
- title;
- duration;
- source/extractor;
- uploader/channel when available;
- audio formats group;
- video-only formats group;
- combined formats group;
- subtitles empty state;
- automatic captions empty state;
- warnings block;
- errors block only when errors exist.

Format rows show:

- `display_label`;
- `format_id`;
- `type`;
- `ext` or `container`;
- `resolution`;
- `audio_codec`;
- `video_codec`;
- `filesize` or `filesize_approx`;
- recommended badge when applicable.

## Error States

The UI handles:

- invalid URL;
- API unavailable;
- failed API response;
- source-level analysis errors from `AnalyzeResult.errors`;
- unsupported source;
- login/cookies-required errors returned by the analyzer.

Technical details are not shown by default.

## Verification

Automated tests:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
33 passed
```

Manual/live checks:

- `GET http://127.0.0.1:8000/health` returned local-only health JSON;
- `GET http://127.0.0.1:8000/` returned the static UI HTML;
- `GET http://127.0.0.1:8000/static/app.js` returned the UI JavaScript;
- live `POST /analyze` for `https://youtu.be/UUdxAp3kuKA` returned:
  - job status `succeeded`;
  - title `Showreel`;
  - zero errors;
  - 3 audio-only formats;
  - 4 video-only formats;
  - 5 combined formats.

Proof files:

- `proof/phase_13/ui_initial.html`
- `proof/phase_13/styles.css`
- `proof/phase_13/app.js`
- `proof/phase_13/analyze_response.json`
- `proof/phase_13/analyze_response_pretty.json`

Screenshot proof:

- `proof/phase_13/ui_initial.png`: not created because Browser/Playwright was not available in the local toolchain.
- `proof/phase_13/ui_result.png`: not created because Browser/Playwright was not available in the local toolchain.

## What Is Not Implemented

- media download;
- Whisper/transcription;
- local file upload;
- format selection for processing;
- settings page;
- history;
- batch processing;
- Chrome extension;
- desktop wrapper;
- auth;
- database;
- cookies/login;
- persistent jobs;
- progress tracking;
- cancellation.

## Safety Notes

- The UI only analyzes the URL and available formats.
- Download and processing actions are not present.
- Future download/process actions must require rights confirmation.
- Source support remains best-effort through `yt-dlp`.
