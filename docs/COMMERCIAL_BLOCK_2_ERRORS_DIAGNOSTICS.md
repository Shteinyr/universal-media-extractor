# Commercial Block 2: Errors + Diagnostics Foundation

Date: 2026-08-05

GitHub issues:

- #6 `[P0] Normalize user-facing errors`
- #7 `[P0] Add diagnostics bundle`

## Goal

Move the product closer to public beta readiness by replacing raw CLI failures with understandable categories and by adding a safe diagnostics bundle that can be inspected before sharing with support.

## Normalized Error Categories

The app now maps representative local engine output into stable `ErrorState.code` values:

- `drm_protected` - content appears protected by DRM/encryption;
- `login_required` - account access/sign-in is required;
- `cookies_required` - browser session or cookies are needed;
- `region_restricted` - media is not available in the current region;
- `private_or_deleted` - source is private, deleted, 404, or unavailable;
- `no_requested_format` - selected output format is unavailable;
- `network_error` - timeout, connection, or source reachability issue;
- `disk_full` - local disk has insufficient space;
- `permission_denied` - local filesystem permission/path access problem;
- `engine_outdated` - local media engine likely needs an update;
- existing fallback categories remain for unsupported source, missing tools, invalid input/output, timeout, transcription failure, and unknown errors.

## Where Mapping Is Applied

- URL analysis through `yt-dlp`;
- selected-format downloads through `yt-dlp`;
- Udemy course analyze/download errors;
- local transcription and ffmpeg audio extraction failures;
- diagnostics bundle normalization for already failed jobs.

## Diagnostics Bundle

Endpoint:

```text
GET /diagnostics/jobs/{job_id}
```

The endpoint returns a JSON `DiagnosticBundle` for an existing in-memory job.

Included:

- app version;
- OS name/version;
- CPU architecture;
- Python version;
- engine versions for `yt-dlp`, `ffmpeg`, and `whisper` when available;
- job id, task type, status, current step;
- extractor type when inferable;
- normalized error;
- redacted payload summary;
- redacted result summary;
- redacted log excerpts.

Excluded/redacted by default:

- cookies;
- tokens;
- passwords;
- auth headers;
- transcripts and summary prompt text;
- full URLs;
- local filesystem paths.

## Inspect Before Sharing

A user or support operator can open the diagnostics endpoint in the local browser or through curl and inspect the JSON before sending it anywhere.

Example:

```bash
curl "http://127.0.0.1:8000/diagnostics/jobs/<job_id>"
```

The endpoint does not upload data. It only returns a local JSON response.

## What Did Not Change

- No payments, stores, signing, packaging, SQLite jobs/history, licensing, batch, or roadmap changes.
- No remote support upload.
- No cloud diagnostics service.
- No storage of credentials/cookies/tokens.
- No DRM/CAPTCHA/paywall/login bypass.

## Verification

Targeted verification:

```bash
.venv/bin/python -m pytest tests/test_error_mapping.py tests/test_diagnostics_service.py tests/test_api_app.py tests/test_download_service.py tests/test_udemy_course_service.py tests/test_ytdlp_analyzer.py tests/test_transcription_service.py -q
```

Result during implementation:

```text
68 passed
```
