# App And Media Engine Update Plan

Status: planning/readiness document. No updater implementation was added.

## Purpose

Universal Media Extractor has two different update surfaces:

- the desktop application itself;
- the local media engine used for source analysis/download compatibility.

They must remain separate because a safe app update and a fast media compatibility update have different risks, artifacts, validation steps, and rollback behavior.

## Application Updates

Application updates cover:

- FastAPI backend code;
- static UI assets;
- desktop wrapper;
- packaged Python runtime;
- bundled Python dependencies;
- app metadata, signing, and installer files.

Public beta state:

- no automatic app updater is implemented;
- app update UX is limited to documentation/release notes;
- future public installers must be signed and notarized before distribution.

Required future behavior:

- show current app version;
- check an app release manifest;
- download only signed release artifacts;
- never update while download/transcription jobs are running unless the user confirms;
- preserve Library/history and user output files;
- support rollback or reinstall if an app update fails.

## Media Engine Updates

Media engine updates cover:

- `yt-dlp` compatibility;
- `ffmpeg`/`ffprobe` availability/version checks;
- optional Whisper CLI/model compatibility checks.

Public beta state:

- no automatic media-engine updater is implemented;
- diagnostics report installed media engine versions;
- error normalization can identify `engine_outdated` style failures;
- users still update local CLIs manually.

Required future behavior:

1. Download a signed or hash-verified engine artifact.
2. Stage it outside the signed app bundle.
3. Verify integrity before activation.
4. Swap atomically.
5. Keep the previous working version.
6. Roll back automatically if the update fails validation.
7. Record active and previous engine versions in diagnostics.

## Settings Copy

Public UI should use plain labels:

- `App updates`
- `Media engine updates`

Normal settings should not lead with raw tool names like `yt-dlp`. Technical details and diagnostics may name exact tools and versions.

## Privacy Notes

Network activity is allowed for:

- analyzing/downloading a user-provided source URL;
- future app update checks;
- future media engine update checks;
- future license activation, if implemented.

Do not claim the app has no network activity. The correct claim is local-first processing with no default upload of source media files to Universal Media Extractor servers.

## Not Implemented

- automatic app updater;
- automatic media-engine updater;
- update manifest;
- update signing/hash verification;
- rollback code;
- license-entitlement update logic.
