# Phase 8 Frontend Flow Draft

Date: 2026-05-29

## Scope

This document describes the future UI flow only. No frontend is created in Phase 8.

The first UI prototype should display URL analysis results only. It should not download media or run Whisper.

## 1. Start Screen

Purpose: accept a source for analysis.

UI elements:

- URL input;
- disabled or later placeholder for local file picker;
- analyze button;
- short local-only/status indicator;
- rights reminder text, not yet blocking analysis.

Available action:

- analyze URL.

Disabled actions:

- download;
- transcribe;
- batch;
- extension send-to-app.

## 2. Analyze State

Purpose: show that URL analysis is running.

UI elements:

- current source URL;
- spinner or progress state;
- job status if job-backed;
- cancel button only if cancellation is supported by the current job layer.

Warnings:

- analysis does not mean download support is proven;
- source support is best-effort.

## 3. Analyze Result

Purpose: present normalized `AnalyzeResult`.

Header fields:

- title;
- duration;
- thumbnail;
- extractor/source type;
- uploader/channel when available.

Source fields:

- source URL;
- webpage URL;
- availability/access state;
- raw artifact reference for developer/debug mode only.

Selectors:

- audio options;
- video-only options;
- combined video+audio options;
- subtitles;
- automatic captions.

Warnings block:

- no subtitles;
- no automatic captions;
- format size unknown;
- platform terms warning;
- best-effort extractor;
- analysis-only not download-tested.

## 4. User Selects Action

Purpose: choose a future operation.

First UI prototype behavior:

- selectors may be visible;
- processing actions remain disabled;
- the UI can show how options would map to future actions.

Future actions:

- download audio;
- download video;
- download subtitles;
- extract audio from local video;
- transcribe audio/video.

## 5. Legal Confirmation

Purpose: block protected operations until the user confirms rights.

State fields:

- `legal_safety.user_confirmed_rights`;
- `legal_safety.confirmation_text`;
- `legal_safety.required_before_download`;
- `legal_safety.required_before_transcription`.

First UI prototype behavior:

- show confirmation state;
- do not start protected processing because download/transcription are out of MVP.

Future behavior:

- require checked confirmation before download, conversion, extraction, or transcription.

## 6. Start Processing

Purpose: start future protected work after confirmation.

First UI prototype behavior:

- not available.

Future behavior:

- create a job;
- pass selected media/subtitle/transcript options;
- start backend processing.

## 7. Job Progress

Purpose: display progress for long-running tasks.

First UI prototype behavior:

- only analysis job status may be shown.

Future behavior:

- show queued/running/succeeded/failed/cancelled;
- show progress percentage or current stage;
- allow cancellation where supported;
- show retry when recoverable.

## 8. Result Card

Purpose: show completed local outputs.

First UI prototype behavior:

- show analysis result only.

Future behavior:

- show output directory;
- list generated files;
- open local folder or copy path;
- show transcript files and metadata files.

## 9. Error States

Unsupported source:

- show a blocking message;
- suggest trying a public supported URL or later local-file path.

Login/cookies required:

- show that the source requires access not implemented in MVP;
- do not ask for credentials in the app.

Network or timeout:

- show recoverable retry state.

No audio/video/subtitles:

- keep available selectors enabled;
- disable missing selector groups;
- explain the empty state from warnings.

Analyzer failed:

- show error message and suggested user action;
- keep technical details collapsed.

Missing dependency:

- show missing tool name;
- suggest environment repair before retry.

## First Prototype Rule

The first frontend should be an analysis viewer, not a downloader/transcriber. It should make the future workflow visible without enabling actions that have not passed later safety proofs.
