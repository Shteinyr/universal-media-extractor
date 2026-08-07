# UI/UX Product Function Inventory

Date: 2026-08-07

Purpose: describe the current product logic and available functions before `Public Beta UI / UX Finalization`.

This is the source inventory for GPT Pro. It should help decide which controls belong in the public UI, which belong in advanced/support areas, and which should stay hidden from public builds.

## Product Positioning

Public positioning:

```text
Local Media Downloader & Organizer for macOS and Windows
```

The product should not be positioned as:

- universal guaranteed downloader;
- DRM bypass tool;
- paywall/login/CAPTCHA bypass tool;
- public Udemy course downloader;
- cloud transcription product;
- AI summary product.

## Core Public User Promise

```text
Turn a supported media link or local media file into organized local files.
```

User value:

- paste a link or choose a file;
- see clean output choices;
- download or process locally;
- get files in a predictable folder;
- avoid terminal commands;
- keep media local.

## Current Runtime Surfaces

- Browser mode: `.venv/bin/python scripts/run_api.py`, then open `http://127.0.0.1:8000/`.
- Desktop mode: `.venv/bin/python scripts/run_desktop.py`.
- Development `.app`: `build/dev/Universal Media Extractor Dev.app`, built by `scripts/build_dev_app.py`.

## Current Public Modes

### URL Mode

Flow:

```text
Paste URL -> Analyze -> Choose output preset -> Download -> optional Transcribe -> Result
```

Current functions:

- analyze URL through `yt-dlp`;
- show title, thumbnail, duration, source/uploader;
- show simplified output choices;
- download audio/video/subtitles;
- save to selected output folder;
- choose output format;
- transcribe downloaded audio/video;
- show saved file/folder;
- copy transcript;
- copy output path;
- reveal managed output folder where supported.

Supported output categories:

- Audio;
- Video;
- Subtitles.

Supported output formats:

- Audio: M4A, MP3, WAV;
- Video: MP4, MKV, WEBM;
- Subtitles: SRT, VTT.

Important behavior:

- Video should mean video plus audio in one final container.
- User should not need to understand `format_id`.
- User should not see codec strings in the main flow.

### Local File Mode

Flow:

```text
Choose local audio/video -> Analyze local file -> Transcribe -> Result
```

Current functions:

- upload local audio/video file to local backend;
- store a local working copy;
- analyze file with `ffprobe`;
- detect media type;
- show duration/codec basics;
- transcribe audio directly;
- extract audio from video with `ffmpeg`, then transcribe;
- choose Whisper model;
- choose exactly one transcript format;
- save transcript near output.

Transcript formats:

- TXT;
- Markdown;
- JSON.

### Batch Mode

Flow:

```text
Paste list / import text -> prepare queue -> choose preset -> start batch -> monitor jobs -> retry failed
```

Current functions:

- paste multiple URLs;
- import from text file;
- clipboard/text import support;
- playlist detection and selection;
- controlled concurrency;
- child download jobs;
- retry failed items;
- cancel queue best-effort;
- batch status polling.

Public UI risk:

- Batch is valuable, but it can overwhelm first-time users.
- It should likely be a separate mode or secondary tab, not mixed with the first URL download flow.

### Course Mode / Udemy Mode

Internal/experimental flow:

```text
Udemy lecture/player URL -> Chrome session auth -> Analyze course -> Download course
```

Current functions:

- use Chrome session via `yt-dlp --cookies-from-browser chrome`;
- advanced manual `cookies.txt` fallback;
- analyze course playlist;
- show sections/lectures;
- choose quality/container;
- download best-effort;
- save course folder structure.

Public product rule:

- Course mode is internal/experimental.
- It should be hidden from public commercial builds and public marketing unless separately approved.

## Jobs / Progress / Cancel

Current functions:

- background jobs for download/transcription/batch;
- SQLite-backed job history;
- status polling;
- current step;
- progress where practical;
- cancel request;
- retry failed jobs;
- failed-job diagnostics.

User-facing principle:

- Show human states: Working, Saved, Needs attention, Cancelled.
- Hide raw job IDs unless diagnostics/support is open.

## Output Management

Current functions:

- default output folder: `~/Downloads/Universal Media Extractor`;
- user can change save location;
- output folder templates;
- duplicate handling;
- managed output index;
- recent results;
- safe delete managed outputs;
- reveal/copy output path.

User-facing principle:

- Show folder/file names first.
- Full paths only in copy/reveal/tooltip/support details.

## Diagnostics / Errors

Current functions:

- normalized user-facing errors;
- technical details collapsible;
- redacted diagnostics bundle;
- no cookies/tokens/transcripts/private paths in diagnostics;
- no-store headers for sensitive local endpoints;
- local session token.

Error categories to show simply:

- Source unavailable;
- Login required;
- DRM/protected content;
- Network issue;
- Disk/write issue;
- Engine outdated;
- Unsupported source;
- Analysis failed;
- Download failed;
- Transcription failed.

## Likely Public UI Controls

Primary:

- mode selector: Link, File, Batch;
- URL input;
- file picker;
- Analyze;
- output preset selector;
- save location;
- output format selector;
- Download;
- Transcribe;
- cancel for active long task;
- retry failed;
- open/reveal/copy output;
- copy transcript.

Secondary:

- Whisper model;
- transcript format;
- recent results/history;
- batch import source;
- diagnostics copy.

Advanced / hidden:

- raw format IDs;
- codec strings;
- bitrate internals;
- CLI logs;
- raw yt-dlp JSON;
- manual cookies path;
- proxy/cookies/private-source options;
- Udemy Course mode in public builds.
