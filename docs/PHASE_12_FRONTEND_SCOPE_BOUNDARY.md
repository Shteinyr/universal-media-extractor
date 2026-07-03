# Phase 12 Frontend Scope Boundary

Date: 2026-05-29

## Phase 13 May Do

If explicitly authorized, Phase 13 may:

- create a minimal static UI;
- connect to the existing `POST /analyze` endpoint;
- show the real analysis result;
- show source summary;
- show audio/video/combined format groups;
- show empty subtitle/caption states;
- show warnings and errors;
- keep backend local-only;
- run existing tests;
- perform a browser screenshot/check if available.

## Phase 13 Must Not Do

Phase 13 must not add:

- download;
- Whisper;
- transcription;
- local file upload;
- desktop wrapper;
- Chrome extension;
- auth;
- database;
- cookies/login;
- settings page;
- batch processing;
- history;
- AI summary;
- paid APIs;
- advanced styling overwork.

## UI Boundary

The first UI is an analysis viewer only.

Allowed loop:

```text
Paste URL -> Analyze -> Display result
```

Forbidden loops:

```text
Paste URL -> Download
Paste URL -> Transcribe
Paste URL -> Select output and process
Upload local file -> Process
Use cookies/login -> Analyze protected source
```

## Technical Boundary

Recommended Phase 13 approach:

- static HTML/CSS/vanilla JS;
- served by FastAPI static files or opened through a minimal local route if explicitly authorized;
- call `http://127.0.0.1:8000/analyze`;
- no Vite unless the user explicitly chooses a build-tool prototype.

## Safety Boundary

The UI must communicate:

- analysis only;
- no media download;
- best-effort source support;
- future download/process actions require rights confirmation.

The UI must not imply:

- universal site support;
- download readiness;
- transcription readiness;
- protected/authenticated source support.
