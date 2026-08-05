# Public Known Limitations

Date: 2026-08-05

## Source Support

Universal Media Extractor uses local media engines such as `yt-dlp`, `ffmpeg`, and Whisper. Source support is best-effort. Websites can change without notice, and a source that worked before may stop working.

## Access Restrictions

The app does not bypass:

- DRM;
- CAPTCHA;
- paywalls;
- login restrictions;
- regional restrictions;
- platform access controls.

Use the app only with media you own, created, or have permission to download and process.

## Authenticated Sources

Authenticated-source workflows are not part of the public product promise. Udemy Course Mode is currently internal/experimental and should not be advertised publicly.

## Transcription Quality

Whisper transcript quality depends on the chosen model, audio quality, language, accents, noise, and machine performance. Small models are faster but less accurate.

## Performance And Disk Space

Large files can take a long time to download, process, merge, or transcribe. They can also consume substantial disk space.

## Current Product Gaps Before Paid Public Beta

- no production signed/notarized macOS installer;
- no production Windows installer;
- SQLite-backed jobs/history exists, but beta UX for browsing/retry/clear still needs real-user validation;
- batch queue foundation exists, but Archive Pack execution and public beta UX validation remain open;
- no paid licensing system;
- no public website/payment flow;
- production diagnostics and localhost security behavior have local sanity coverage, but still need external beta validation.
