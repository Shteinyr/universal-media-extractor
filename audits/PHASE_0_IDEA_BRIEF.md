# Phase 0 Idea Brief

Date: 2026-05-29

## What The User Wants

The user wants a local browser-based app that accepts either a URL or a local audio/video file, analyzes what can be extracted, lets the user choose outputs, processes everything locally, and writes structured result files.

## Expected End Result

A local workflow:

`URL or local file -> analyze -> choose audio/video/subtitles/transcript -> process -> receive organized output files`

Expected outputs include extracted media, subtitles, metadata, transcripts, and prompt-ready markdown artifacts.

## Target Users

- Primary: one local desktop user.
- Secondary future users: technically comfortable users who can install local CLI dependencies.
- Not targeted at Phase 0: hosted SaaS users, multi-user teams, or public online service users.

## Scale

- Phase 0: feasibility only.
- Intended MVP scale: single-user local jobs, one URL or file at a time.
- Future optional scale: batch processing and job history.

## Required Data

- URL or local file path.
- User-selected desired outputs.
- Source metadata from `yt-dlp` or `ffprobe`.
- Available formats/subtitles when a URL is supported.
- Local dependency versions.
- Output directory and job status data.

## Required System Actions

- Validate input type.
- Analyze URL support and available formats.
- Analyze local files without `yt-dlp`.
- Download or extract chosen streams.
- Convert media through `ffmpeg`.
- Transcribe audio through local Whisper CLI.
- Save outputs in a structured directory.
- Report progress, errors, cancellation, and retry state.

## Actions To Automate

- CLI dependency checks.
- Source analysis.
- Format/subtitle listing.
- Media extraction/conversion.
- Transcript generation.
- Metadata and output manifest creation.
- Status and progress collection.

## Manual Actions The User Wants To Avoid

- Manually copying `yt-dlp` format codes.
- Manually writing `ffmpeg` commands.
- Manually extracting audio before transcription.
- Manually organizing output folders.
- Manually converting Whisper output into project files.

## Success Criteria

- Critical capabilities are possible locally with no paid API requirement.
- URL support is transparent and best-effort, not silently assumed.
- The app can process local files even when URL extraction fails.
- The app can produce stable structured outputs.
- Risks, legal/platform limits, and performance limits are explicit.

## Failure Criteria

- Cannot list formats before downloading.
- Cannot process local files without URL extraction.
- Cannot run local transcription.
- Cannot keep the backend local-only.
- Requires paid APIs for core workflow.
- Platform restrictions make the core use case broadly unusable.

