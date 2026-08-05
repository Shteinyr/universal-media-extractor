# MVP Known Limitations

Date: 2026-05-30

## Source Support

- URL extraction is best-effort through `yt-dlp`.
- Supported sites can change or break without changes in this app.
- The app is not a guaranteed universal downloader.
- DRM, CAPTCHA, paywalls, private content, and login-only sources are out of scope.
- Cookies/login are not implemented in the MVP.
- Users are responsible for confirming they have the right to download/process media.

## Download/Processing

- Downloads run as in-memory local jobs.
- There is no persistent job queue, retry queue, or persistent history.
- Progress uses status/current-step polling and parses practical `yt-dlp` percent output when available.
- Some `yt-dlp` sources expose little or no granular percent before completion.
- Cancellation is best-effort but now attempts to terminate the active `yt-dlp` subprocess when registered.
- Large files can take a long time and consume significant disk space.
- The first proof path focuses on audio-only format `140`; video/combined/subtitle modes are implemented but need more real-source proof before being considered robust.

## Local Files

- Local file mode copies the selected file into the project output folder.
- Local file metadata is based on `ffprobe`; unsupported/corrupt files may return limited metadata or errors.
- There is no persistent local file library, history, deduplication, or cleanup policy yet.
- The Block 7 manual proof used a synthetic sine-wave file, so it proves the pipeline rather than speech transcript quality.

## Transcription

- Whisper quality depends on the selected model, language, source audio quality, and hardware.
- The default `tiny` model is fast but can produce low-quality transcripts.
- Larger Whisper models may be slower.
- Transcription runs as an in-memory local job with honest step-based status.
- Whisper percent is not faked; the UI shows `running_whisper` instead of made-up progress.
- Cancellation is best-effort but now attempts to terminate active `ffmpeg` or Whisper subprocesses when registered.
- Real video transcription through ffmpeg extraction is covered by tests, but not yet manually proofed with a real video file.
- No AI summary is generated. Current normal transcription saves one selected transcript format per run and does not call an AI summary API.

## UI And Runtime

- The MVP is a local single-user web app bound to `127.0.0.1`.
- Browser UI cannot open a local output folder directly; it shows/copies the path.
- Browser screenshot verification now exists as a manual/dev Playwright smoke script.
- Browser smoke is not part of ordinary `pytest`; it requires the backend to be running and Playwright Chromium to be installed.
- The UI is static HTML/CSS/vanilla JS; there is no React/Vite build system.
- A local desktop wrapper exists through `pywebview`, but there is no packaged/signed/notarized `.app` or installer.
- There is no Chrome extension, auth, database, batch processing, or online service.

## Outputs And Cleanup

- `outputs/` contains user results and is managed by Recent results.
- `proof/` contains development proof artifacts and is not listed or deleted automatically.
- Safe delete only removes direct folders inside `outputs/`.
- There is no batch delete, search/filtering, retention policy, output archiving, or automatic cleanup yet.
- Old transcript preview is not loaded in Recent results.

## Security Boundary

- The backend is intended for local-only use.
- Do not expose the backend port to the public internet.
- The MVP does not store credentials, cookies, API keys, or login tokens.
- Download/transcription actions require `user_confirmed_rights=true`.


## Public Commercial Boundary

- Public positioning is `Local Media Downloader & Organizer for macOS and Windows`.
- Udemy Course Mode is internal/experimental and should be hidden from public builds/marketing unless separately approved.
- Public builds can set `UME_PUBLIC_PRODUCT_MODE=1` to hide Course Mode in the UI.
- Public copy must not promise guaranteed source support or DRM/CAPTCHA/paywall/login bypass.
