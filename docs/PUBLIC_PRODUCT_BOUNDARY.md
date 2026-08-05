# Public Product Boundary

Date: 2026-08-05

## Public Positioning

Universal Media Extractor is a local desktop utility for macOS and Windows.

Public category:

```text
Local Media Downloader & Organizer for macOS and Windows
```

Public promise:

```text
Save accessible media, audio, subtitles, and transcripts locally in organized folders without uploading files to a cloud service.
```

The product must not be described as a universal downloader for every website. Source support is best-effort and depends on available local engines such as `yt-dlp`, `ffmpeg`, and Whisper.

## Who It Is For

- creators archiving their own videos, audio, and captions;
- researchers and students saving allowed learning/reference material for offline work;
- editors and knowledge workers who need clean local media files and transcripts;
- teams that prefer local processing over cloud upload.

## Public Product Includes

- local macOS/Windows desktop app direction;
- URL analysis for supported public or access-authorized sources;
- local audio/video/subtitle download where supported and allowed;
- local file analysis and transcription;
- local Whisper transcription;
- organized output folders;
- copyable transcript/output paths;
- best-effort jobs, progress, cancellation, and output management.

## Public Product Does Not Include Or Promise

- guaranteed support for every website;
- DRM bypass;
- CAPTCHA bypass;
- paywall bypass;
- unauthorized login/session access;
- downloading content the user does not have rights to use;
- cloud-hosted extraction service;
- storing account passwords, cookies, tokens, or DRM keys.

## Internal / Experimental Features

Udemy Course Mode is internal/experimental. It may remain available in local development builds, but it must not be advertised on the public website or positioned as a guaranteed commercial feature unless separately approved.

Current safety boundary for Udemy mode:

- Chrome session auth can be used locally through `yt-dlp --cookies-from-browser chrome`;
- manual `cookies.txt` can exist only as an advanced fallback;
- the app does not store passwords/cookies/tokens in outputs;
- the app does not bypass DRM, CAPTCHA, paywalls, or platform restrictions;
- support remains best-effort and may fail for some courses or lectures.

## Public Build Control

The app now exposes a local `/config` endpoint with:

```json
{
  "public_product_mode": false,
  "course_mode_enabled": true
}
```

For public commercial builds, set:

```bash
UME_PUBLIC_PRODUCT_MODE=1
```

Default behavior in public product mode: Course Mode is hidden from the static UI unless explicitly re-enabled for an internal build.

## Draft Plan Boundaries

Free:

- URL/local file analysis;
- limited single-item downloads;
- basic organized outputs;
- clear best-effort source limits.

Founder Pro / Pro:

- unlimited single-user local workflows within fair-use limits;
- local transcription;
- presets;
- queue/batch once implemented;
- history/retry once implemented;
- compatibility updates during the active update period.

Business:

- business license terms;
- more devices/seats;
- priority support;
- documented deployment/support workflow;
- no cloud upload by default.

These commercial boundaries are draft positioning only. Payments, licensing enforcement, and store distribution are not implemented yet.
