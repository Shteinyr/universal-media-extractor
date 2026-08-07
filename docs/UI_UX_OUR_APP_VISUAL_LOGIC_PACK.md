# UI/UX Our App Visual Logic Pack

Date: 2026-08-07

Product: Universal Media Extractor

Public positioning:

```text
Local Media Downloader & Organizer for macOS and Windows
```

This document describes the current product as input for GPT Pro. It is not a new implementation plan.

## Product Purpose

Universal Media Extractor helps a user turn supported media links or local audio/video files into organized local output files.

Core value:

- avoid terminal commands;
- keep processing local;
- inspect available outputs before acting;
- choose a clean result;
- save media/transcripts into predictable folders;
- optionally transcribe locally through Whisper CLI;
- avoid cloud upload and paid APIs.

The product should help:

- creators saving their own uploads;
- editors collecting references they have rights to use;
- educators/students saving allowed learning materials for offline use;
- researchers organizing media references;
- podcasters/transcribers turning audio/video into text;
- local-first users who do not want to upload private media.

## Public Product Boundary

The public product should promise:

- local-first processing;
- best-effort source support;
- organized local output;
- URL download where supported;
- local file transcription;
- batch queue for supported URLs;
- readable errors and diagnostics.

The public product must not promise:

- universal support for every site;
- DRM bypass;
- paywall bypass;
- CAPTCHA bypass;
- login bypass;
- public Udemy/course downloading;
- cloud AI summary;
- hosted online service behavior.

Udemy/Course mode exists in local/internal builds only. It should remain hidden in public commercial builds unless separately approved.

## Current Runtime Surfaces

- Browser mode: run FastAPI and open `http://127.0.0.1:8000/`.
- Desktop mode: `scripts/run_desktop.py` opens the same local UI in a pywebview window.
- Development `.app`: launches current project code and local backend from the existing working tree.

## Current Architecture Summary

- Python backend.
- FastAPI local API.
- Static vanilla HTML/CSS/JS frontend.
- `yt-dlp` for URL analysis/download.
- `ffmpeg`/`ffprobe` for media metadata and audio extraction.
- Whisper CLI for local transcription.
- SQLite job history.
- Local session token between UI and backend.
- Strict local host/origin behavior.
- Outputs default to `~/Downloads/Universal Media Extractor`.

## Current Screenshot References

```text
proof/ui_ux_gpt_pro_pack/our_app/ui_initial.png
proof/ui_ux_gpt_pro_pack/our_app/ui_analyze_result.png
proof/ui_ux_gpt_pro_pack/our_app/ui_output_selected.png
proof/ui_ux_gpt_pro_pack/our_app/ui_local_file_mode.png
proof/ui_ux_gpt_pro_pack/our_app/ui_batch_mode.png
proof/ui_ux_gpt_pro_pack/our_app/ui_invalid_url_error.png
```

## Current Modes

### Link / URL Mode

Current flow:

```text
Paste URL -> Analyze -> Choose preset -> Choose save options -> Download -> optional Transcribe -> Result
```

Current user-facing controls:

- URL input.
- Analyze.
- Output preset selection.
- Save to folder.
- Format selector.
- Download.
- Cancel active job.
- Transcribe.
- Whisper model selector.
- Transcript format selector.
- Copy transcript.
- Copy output path.
- Reveal/open output where supported.

Current output presets:

- Best video.
- 1080p video.
- Smaller video.
- Audio only.
- Subtitles.

Current output formats:

- Video: MP4, MKV, WEBM.
- Audio: M4A, MP3, WAV.
- Subtitles: SRT, VTT.
- Transcript: TXT, Markdown, JSON, one selected format per run.

Important behavior:

- Video download should produce one playable file with video and audio merged where possible.
- Normal users should not see `format_id`, codec strings, raw bitrate, or raw yt-dlp output.
- Download is job-based and can be cancelled best-effort.
- Transcription is post-download and uses local Whisper.

### Local File Mode

Current flow:

```text
Choose local audio/video -> Analyze local file -> Transcribe -> Result
```

Current user-facing controls:

- File picker.
- Analyze local file.
- Whisper model.
- Transcript format.
- Transcribe.
- Copy transcript.
- Copy output path.

Current backend behavior:

- Upload/copy file into local working output.
- Analyze with `ffprobe`.
- Detect audio/video/unknown.
- Audio goes directly to Whisper.
- Video extracts audio through `ffmpeg`, then Whisper.
- Generated transcript is saved next to the media output in the result folder.

### Batch Mode

Current flow:

```text
Paste/import URL list -> prepare queue -> select preset -> start batch -> monitor jobs -> retry failed
```

Current controls:

- Textarea for multiple URLs.
- Paste/import from clipboard or text file.
- Playlist analysis and item selection.
- Preset selection.
- Concurrency.
- Start batch.
- Cancel batch request.
- Retry failed.

Current risk:

- Batch is valuable, but can visually overwhelm the first-time single-link flow.
- GPT Pro should decide whether Batch remains a top-level mode, a secondary mode, or a Library/Queue feature.

### Internal Course / Udemy Mode

Current internal flow:

```text
Udemy lecture/player URL -> Chrome session auth -> Analyze course -> Download course
```

Current controls:

- Course URL.
- Chrome session login source.
- Advanced manual cookies fallback.
- Analyze course.
- Download course.

Public rule:

- Hide this mode from public commercial builds.
- Do not include it in public website claims.
- Do not promise Udemy support.

## Current Result States

### Analysis Result

Shows:

- title;
- thumbnail if available;
- source;
- duration;
- uploader if available;
- output options;
- warnings/errors.

Should avoid:

- raw extractor fields;
- long stream detail lists;
- repeated technical options.

### Download Result

Shows:

- saved output;
- selected media file;
- warnings if the file cannot be transcribed;
- transition to transcription if media has audio.

Current issue to evaluate:

- The result should feel like "your file is saved" rather than "job technical output".

### Transcription Result

Shows:

- selected transcript file;
- transcript preview if available;
- Copy transcript;
- Copy output path.

Current simplification:

- User selects one transcript format before transcription.
- Only the selected transcript is shown prominently.

### Error State

Shows:

- normalized error code/title;
- short explanation;
- suggested action where available;
- collapsible technical details for support.

Current error categories:

- source unavailable;
- login required;
- DRM/protected content;
- network issue;
- disk/write issue;
- engine outdated;
- unsupported source;
- analysis failed;
- download failed;
- transcription failed.

## Current Library / History / Output Management

Current functions:

- SQLite job history.
- Output index.
- Recent results / Library surface.
- Reveal output folder.
- Copy output path.
- Safe delete for managed outputs.
- Failed-job diagnostics copy action.

UX question:

- Should Library be visible in the main app shell, hidden until needed, or become a separate screen?

## Current Settings / Advanced Surfaces

Currently available or planned surfaces:

- output base folder;
- output format;
- duplicate behavior;
- output name templates;
- Whisper model;
- transcript format;
- diagnostics;
- internal Course mode;
- manual cookies fallback for internal mode.

Potential settings for GPT Pro to evaluate:

- default download folder;
- default output preset;
- default transcript format;
- media engine update/check status;
- privacy/local-only note;
- diagnostics export.

## What Feels Raw Today

- The app is functional but still visually closer to a dev utility than a polished commercial desktop app.
- Some flows still reveal backend/job concepts too directly.
- Batch and Library can compete with the main single-link flow.
- Error details are useful but need stronger hierarchy.
- The product needs a clearer first-run mental model.
- The UI needs final decisions on:
  - one universal input vs explicit modes;
  - presets vs tabs/cards/dropdowns;
  - where Library lives;
  - where transcription belongs;
  - how much settings UI is visible;
  - how commercial upgrade surfaces should appear.

## Current Strengths

- Real local MVP exists.
- Link, file, and batch workflows are implemented.
- Outputs are organized into user-visible folders.
- Download/transcription happen locally.
- Backend has local-only security basics.
- Errors are normalized with technical details hidden.
- No paid API required.
- Desktop wrapper exists for development/local use.

## Key Questions For GPT Pro

1. What should the first screen look like for a non-technical user?
2. Should Link / File / Batch stay as modes, or should there be one source input?
3. What exact output presets should be visible?
4. Where should save folder and format selectors appear?
5. Should transcription be a step in the main flow or a result action?
6. Should Library/history be visible by default?
7. How should Batch be introduced without making the app feel complex?
8. What should be hidden in Advanced?
9. What error/progress/result hierarchy would feel commercial and trustworthy?
10. Where, if anywhere, should Free/Pro upgrade prompts appear?
11. What UI should be removed before public beta?
12. What public product copy best communicates local-first value without risky downloader claims?
