# Phase 7 Manual Analyze Proof

Date: 2026-05-29

## Scope

Phase 7 ran the user-authorized manual analysis script against the user-provided URL. This proof used analysis mode only.

No FastAPI app, routes, frontend, downloader, media download, Whisper run, MVP, extension, or desktop wrapper was created or run.

## Command Executed

```bash
.venv/bin/python scripts/manual_analyze_url.py "https://youtu.be/UUdxAp3kuKA" --raw-output-dir proof/phase_7
```

## Result

- Exit code: `0`
- Source URL: `https://youtu.be/UUdxAp3kuKA`
- Title: `Showreel`
- Duration: `39` seconds
- Extractor: `youtube`
- Errors: none
- Audio-only options: 3
- Video-only options: 4
- Combined video+audio options: 5
- Subtitles: none
- Automatic captions: none
- Media download performed: `no`
- Whisper run: `no`

## Raw Artifact

- `proof/phase_7/ytdlp_UUdxAp3kuKA_20260529T081128Z.json`
- Size: about 55 KiB

The raw artifact is `yt-dlp --simulate --dump-json` output saved by the analyzer wrapper because `--raw-output-dir proof/phase_7` was provided.

## Warnings Returned

- `no_subtitles`
- `no_automatic_captions`
- `format_size_unknown`
- `platform_terms_warning`
- `best_effort_extractor`
- `analysis_only_not_download_tested`

## Limitations

- This proof confirms real URL analysis through the wrapper.
- It does not test media download, merging, conversion, transcription, progress tracking, cancellation, FastAPI routes, or UI.
- YouTube support remains best-effort and subject to platform changes.

