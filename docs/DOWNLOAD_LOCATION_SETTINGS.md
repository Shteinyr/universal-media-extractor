# Download Location Settings

This is a small UX refinement, not a new roadmap block.

## What Changed

- URL downloads now default to `~/Downloads/Universal Media Extractor`.
- The download card has a compact `Save to` text field.
- The download card has a `Format` selector:
  - Video: `MP4`, `MKV`, `WEBM`;
  - Audio: `M4A`, `MP3`, `WAV`;
  - Subtitles: `SRT`, `VTT`.
- The user can change the output base folder before clicking `Download selected`.
- After a custom download path is submitted, `Recent results` uses that selected base folder for output listing.
- The backend creates a user-facing folder named from the source title when the UI provides it.
- The selected download file is written directly inside that folder.
- Service artifacts are kept in hidden folders so Finder normally shows only the selected output file:

```text
<selected folder>/<safe source title>/
  <source title> [id].mp4|m4a|webm|vtt
  .metadata/
  .logs/
```

## Why

The previous default wrote URL downloads to the project-local `outputs/` folder. That is useful for development, but less natural for regular use. A Downloads-based default is easier to find and matches normal desktop expectations.

The first Downloads implementation still exposed technical `media/`, `metadata/`, and `logs/` folders in Finder. The current behavior keeps the user-selected output visible and hides service artifacts in dot folders.

For video output, the `Video` choice downloads the selected video stream together with the best available audio stream and asks `yt-dlp`/ffmpeg to produce the selected container where possible. `MP4` is the default because it is the most common playback format. `MKV` is available as a more flexible merge container. `WEBM` is available for web/open codec workflows.

## Browser Limitation

A static browser UI cannot reliably choose or reveal an arbitrary local folder path through a native folder picker without a desktop wrapper or additional browser-specific permissions. For now, the simplest local-only approach is an editable path field.

## What Did Not Change

- No roadmap block was added.
- No desktop wrapper was added.
- No Chrome extension was added.
- No backend auth/database/cookies were added.
- Download artifacts still include media, metadata, and logs.

## Transcript Output

Transcription now saves one selected transcript format per run:

- `TXT`;
- `Markdown`;
- `JSON`.

The selected transcript file is written directly into the same result folder as the media file. Whisper intermediate files are kept under hidden `.work/whisper`, and transcription logs/metadata are kept under hidden `.logs` and `.metadata`.
