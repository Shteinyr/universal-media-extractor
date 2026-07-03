# Block 2 Download + Output Pipeline

Date: 2026-05-29

## Scope

Block 2 adds a local, user-confirmed download path for a selected `yt-dlp` format and writes a structured output folder.

This block keeps the existing local-only app boundary. It does not add Whisper, transcription, local file upload, Chrome extension, desktop wrapper, auth, database, cookies/login, online service behavior, or AI summary.

## Implemented

- `DownloadRequest`, `DownloadResult`, `DownloadMode`, and `DownloadStatus` models.
- `DownloadService.download_media(request)`.
- Structured output directory creation through `OutputManager.create_download_output_dir(...)`.
- `POST /download` endpoint.
- Minimal static UI extension:
  - select a format row after analysis;
  - confirm rights with a checkbox;
  - click `Download selected`;
  - show status, output directory, files, errors, and warnings.
- Tests for service safety, command construction, API behavior, and existing static UI availability.

## Supported Download Modes

- `audio`: passes the selected `format_id` to `yt-dlp -f`.
- `video`: passes the selected `format_id` to `yt-dlp -f`.
- `combined`: passes the selected `format_id` to `yt-dlp -f`.
- `subtitles`: uses `--skip-download --write-subs --write-auto-subs --sub-langs <format_id> --sub-format best`.

The first manual proof covered audio-only format `140`.

## Output Structure

Each confirmed download creates:

```text
outputs/<timestamp>_<safe_title_or_video_id>/
  media/
  metadata/
    download_request.json
    download_result.json
  logs/
    download.log
```

When a custom `output_base_dir` is supplied, the same structure is created under that base directory.

## Safety Checks

- Download is blocked unless `user_confirmed_rights=true`.
- If rights confirmation is missing, `DownloadService` returns `DownloadResult(status="blocked")` and does not call `yt-dlp`.
- `yt-dlp` is called through `subprocess.run([...], shell=False)`.
- No credentials, cookies, tokens, or login data are stored.
- No Whisper or transcription post-processing is started.

## yt-dlp Command Shape

Media download:

```bash
yt-dlp --no-playlist --newline -o "<output>/media/%(title).200B [%(id)s].%(ext)s" -f "<format_id>" "<source_url>"
```

Subtitle mode:

```bash
yt-dlp --no-playlist --newline -o "<output>/media/%(title).200B [%(id)s].%(ext)s" --skip-download --write-subs --write-auto-subs --sub-langs "<language>" --sub-format best "<source_url>"
```

Current yt-dlp documentation confirms `-f/--format`, output templates, subtitle options, and `--skip-download` behavior.

## Verification

Automated tests:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
43 passed
```

Manual proof download:

- source URL: `https://youtu.be/UUdxAp3kuKA`;
- selected format: `140`;
- mode: `audio`;
- confirmation: `user_confirmed_rights=true`;
- status: `succeeded`;
- output base: `proof/download_block/`;
- downloaded file: `proof/download_block/20260529T092713Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a`;
- file size: about 617 KiB.

Proof files:

- `proof/download_block/download_response.json`;
- `proof/download_block/download_response_pretty.json`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/metadata/download_request.json`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/metadata/download_result.json`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/logs/download.log`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a`.

## Not Implemented

- background download jobs;
- progress streaming;
- cancellation of an active download subprocess;
- retry UI;
- Whisper/transcription;
- audio conversion;
- local file upload;
- cookies/login;
- database or persistent job history;
- Chrome extension;
- desktop wrapper.

## Remaining Risks

- `yt-dlp` support is best-effort and may fail as platforms change.
- Some sources require login, cookies, CAPTCHA, DRM handling, or platform-specific permissions; these remain out of scope.
- Large downloads can consume disk space.
- Combined/video downloads may require `ffmpeg` merge behavior from yt-dlp and should be manually proofed in a later block before promising the flow.
