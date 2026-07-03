# Phase 8 MVP Boundary

Date: 2026-05-29

## MVP Includes

The first MVP is intentionally narrow:

- local web app;
- backend bound only to `127.0.0.1`;
- URL analyze;
- normalized `AnalyzeResult`;
- UI for displaying analyze result;
- audio/video/combined/subtitle selectors as read-only or non-processing controls;
- warnings and errors display;
- legal/safety confirmation state display;
- no download on the first UI prototype;
- no Whisper on the first UI prototype.

## MVP Does Not Include

- download;
- transcription;
- media conversion;
- audio extraction;
- Chrome extension;
- desktop wrapper;
- online service;
- authentication;
- database;
- cookies/login;
- batch processing;
- history;
- AI summary;
- paid APIs or subscriptions.

## Why This Boundary Exists

The project has proven URL analysis and normalization, but it has not yet proven:

- safe download execution;
- merge/conversion behavior;
- progress parsing;
- cancellation;
- Whisper performance on real media;
- local-file metadata flow;
- FastAPI route behavior;
- frontend behavior.

The first MVP should therefore prove the narrowest user-visible loop:

```text
URL -> analyze -> normalized result -> display options/warnings/errors
```

It should not imply that download or transcription are available until those capabilities pass their own proof phases.

## Stop Gate For Expanding MVP

Do not add download/transcription to MVP until separate phases prove:

- user confirmation gate;
- output directory safety;
- selected format handling;
- process progress;
- cancellation;
- failure cleanup;
- disk-space risk handling;
- platform terms warnings.

## Phase 8 Decision

Proceed toward a first UI prototype only as an analysis viewer, not as a downloader/transcriber.
