# Public Beta Native Filesystem Integration

Date: 2026-08-07

GitHub issue: #47 Native filesystem integration.

## Summary

Native filesystem integration is implemented for the public beta desktop flow without changing the roadmap or adding installer/licensing/payment scope.

The app still runs a local-only FastAPI backend on `127.0.0.1`, but desktop mode can now use native file and folder pickers through the existing `pywebview` shell. Browser mode remains supported with the existing upload input and typed save path.

## What Changed

- Added a small `pywebview` JavaScript bridge in `scripts/run_desktop.py`.
- Added native desktop actions:
  - choose a local media file;
  - choose an output folder.
- Added `POST /local/analyze-path` for desktop-selected files.
- Local file path analysis can inspect a user-selected file in place instead of copying a large file just to run `ffprobe`.
- Local transcription can process an external selected file only when a managed output folder is already attached.
- Output base folders are resolved, created, and checked for write access before downloads start.
- The default save location remains user-friendly:

```text
~/Downloads/Universal Media Extractor
```

- The UI keeps the short default path visible instead of replacing it with a long absolute path on startup.
- Result reveal now targets the primary saved result file when one exists, or the output folder as fallback.
- Safe delete and reveal remain limited to direct managed output folders.

## User-Facing Behavior

Desktop app:

- `Choose file` opens a native file picker.
- `Choose` near `Save to` opens a native folder picker.
- `Reveal` opens Finder/Explorer for the result file when possible.
- `Copy path` copies the full path when the user explicitly asks for it.

Browser app:

- Local files still use browser upload.
- Save location can still be typed manually.
- Reveal still uses the backend-managed local reveal endpoint.

## Safety Boundary

Implemented safety constraints:

- `shell=False` is preserved for OS reveal commands.
- `DELETE /outputs/{output_id}` accepts only a direct managed output id, not arbitrary paths.
- `POST /outputs/{output_id}/reveal` accepts only a direct managed output id.
- Output base folder changes are validated with a write probe.
- Invalid output base paths return a clear error before starting `yt-dlp`.
- Desktop-selected external files are allowed for metadata analysis, but transcription requires a managed output directory.
- The app does not expose arbitrary filesystem delete.
- Cookies, tokens, auth, and cloud upload are not added.

## API Changes

New public endpoint:

```text
POST /local/analyze-path
```

Request:

```json
{
  "file_path": "/absolute/path/to/local-media-file.mp4"
}
```

Response:

```text
LocalFileAnalyzeResult
```

Notes:

- This endpoint is intended for desktop mode where a native picker returns a local path.
- It rejects missing paths.
- It does not upload or copy the source file merely for analysis.
- It still creates a managed output folder for metadata/transcription artifacts.

Updated endpoint behavior:

- `GET /config` includes the configured output base directory for backend awareness.
- `POST /download` validates a user-provided output base directory before creating a job.
- `POST /local/transcribe` allows external source files only with a managed output directory.
- `POST /outputs/{output_id}/reveal` now reveals the primary result file when available.

## What Did Not Change

- No licensing or payments.
- No installer, signing, or notarization.
- No AI summary API.
- No Chrome extension.
- No public Course/Udemy support.
- No React, Vite, CDN, or frontend stack migration.
- No roadmap changes.
- No database rewrite.
- No broad redesign.

## Verification

Automated checks:

```bash
node --check src/universal_media_extractor/static/app.js
node --check src/universal_media_extractor/static/option_normalizer.js
.venv/bin/python -m pytest -q
```

Browser smoke:

```bash
UME_PUBLIC_PRODUCT_MODE=1 .venv/bin/python scripts/run_api.py
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/native_filesystem_integration
```

Expected proof screenshots:

- `proof/native_filesystem_integration/ui_initial.png`
- `proof/native_filesystem_integration/ui_analyze_result.png`
- `proof/native_filesystem_integration/ui_output_selected.png`
- `proof/native_filesystem_integration/ui_library.png`

## Remaining Limitations

- Native picker actions are available only in desktop mode.
- Browser mode cannot provide a real native folder picker through normal web APIs.
- Reveal/Open depends on the operating system accepting `open`, `explorer`, or `xdg-open`.
- macOS privacy permissions may still require user approval for some external folders.
- Windows long-path and Unicode edge cases are documented as release-validation concerns and should be checked during Windows production packaging.
