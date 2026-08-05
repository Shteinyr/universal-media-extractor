# Commercialization Execution Plan

Source strategy document: `docs/UNIVERSAL_MEDIA_EXTRACTOR_PRODUCT_STRATEGY.md`

## Decision

Universal Media Extractor should move from a working local MVP toward a commercial desktop utility.

Recommended product category:

```text
Local Media Downloader & Organizer for macOS and Windows
```

Recommended promise:

```text
Save accessible videos, audio, and subtitles locally in clean formats without uploading media to the cloud.
```

The product should not be positioned as a universal downloader for every website. It should be positioned as a local workflow for saving, organizing, and processing media that the user has the right to access.

## Current Product Baseline

Already working:

- URL analysis through `yt-dlp`.
- Local file metadata through `ffprobe`.
- URL download through `yt-dlp`.
- Audio/video/subtitle output selection.
- Local transcription through Whisper CLI.
- Video audio extraction through `ffmpeg`.
- Local output folders.
- Job polling, progress, and cancel.
- Output management and safe delete.
- Browser UI.
- Development desktop wrapper through `pywebview`.
- Udemy Course mode as an internal/best-effort feature through Chrome session auth.

## Commercial Direction

The paid value should not be “a GUI over yt-dlp”.

The paid value should be:

- no-terminal installation;
- stable installers for macOS and Windows;
- organized output folders;
- clean presets instead of technical format lists;
- queue, batch, retry, and history;
- safe diagnostics;
- compatibility updates;
- local transcription as an optional Pro workflow;
- privacy-first local processing.

## Public Product Boundary

For the public commercial product:

- Keep URL/local file workflows.
- Keep local-only processing.
- Keep media download, subtitles, conversion, and organization.
- Keep transcription as an optional Pro feature.
- Keep support for best-effort public/access-authorized sources.
- Hide or remove Udemy Course mode from public builds and marketing.
- Do not advertise protected/authenticated course export.
- Do not bypass DRM, CAPTCHA, paywalls, login restrictions, or platform access controls.

## P0 Work Before Paid Version

### 1. Production Packaging

macOS:

- Apple Silicon build first.
- Signed `.app`.
- Hardened runtime.
- Notarization.
- `.dmg` installer.
- Correct uninstall behavior.
- Update check mechanism.

Windows:

- Windows 10/11 x64 build.
- Signed installer.
- Correct uninstall.
- EXE/MSI for direct site distribution.
- MSIX package for Microsoft Store later.

### 2. Persistent Jobs And History

Replace in-memory jobs with SQLite-backed history:

- job records survive restart;
- status, progress, error, result, and timestamps persist;
- retry failed tasks;
- delete history separately from files;
- recover interrupted jobs safely.

### 3. Queue And Batch

Add paid-differentiating workflow:

- multiple URLs;
- clipboard/text import;
- playlist analysis;
- select playlist items;
- controlled concurrency;
- pause/resume;
- retry failed;
- stable task order.

### 4. Preset-Based Output Selection

Replace user-facing technical formats with presets:

- Best Video;
- 1080p;
- Smaller Video;
- Audio M4A;
- Audio MP3;
- Subtitles;
- Archive Pack.

Advanced technical details can remain hidden behind an advanced panel.

### 5. Media Engine Updates

Separate app version from media engine version:

- signed engine manifest;
- verified hashes;
- stable and compatibility channels;
- rollback to previous engine;
- safe update storage outside signed app bundle where required.

### 6. Normalized Errors

Show user-friendly errors:

- Source not supported;
- Login required;
- Content unavailable in region;
- DRM-protected;
- Private or deleted;
- No requested format;
- Network interrupted;
- Disk full;
- Permission denied;
- Engine update required.

Technical logs should stay collapsible and redacted.

### 7. Diagnostics Bundle

Add one safe support bundle:

- app version;
- `yt-dlp` version;
- OS and architecture;
- extractor type;
- normalized error;
- redacted logs;
- no cookies;
- no full source URL by default;
- no local paths by default.

### 8. Output Templates

Add configurable naming:

```text
{source}/{channel}/{date} - {title}
{project}/{playlist_index} - {title}
```

Required behavior:

- safe filenames;
- duplicate detection;
- overwrite/skip/rename;
- reveal result in Finder/Explorer;
- move result.

### 9. Licensing

Minimal commercial licensing:

- license key;
- 3 device activations for Pro;
- offline signed entitlement;
- grace period;
- deactivate device;
- app keeps working on last eligible version after update period expires.

### 10. Localhost Security

Production local backend must add:

- random session token between UI and backend;
- strict CORS/origin allowlist;
- CSRF protection;
- upload size limits;
- safe path validation;
- no arbitrary CLI argument passthrough;
- cookie/secret redaction in all logs.

## P1 After Pro Launch

- Clipboard watcher.
- Deep links.
- Trim before export.
- Metadata embedding.
- Subtitle embedding.
- Persistent library.
- Controlled authenticated sources only after policy/legal review.

## P2 After Usage Data

- AI summary API.
- Browser companion extension.
- Advanced retention policies.
- Additional localization.
- Business/enterprise workflows.

## Distribution Plan

Primary channel:

- own website;
- signed macOS and Windows downloads;
- release notes;
- checksums;
- privacy policy;
- EULA;
- support page;
- known limitations;
- source support status.

Secondary channel:

- Microsoft Store after direct Windows beta.

Not recommended for the full downloader:

- Mac App Store;
- Chrome Web Store as the main distribution path.

Possible later:

- Setapp after macOS stability and retention are proven;
- Homebrew Cask;
- winget;
- Product Hunt;
- creator/editor/researcher communities.

## Monetization Plan

Recommended model:

- Free plan;
- Founder Pro;
- Pro;
- Business.

Suggested pricing from strategy:

- Free: `$0`;
- Founder Pro: `$24`;
- Pro: `$39`;
- Updates renewal: `$19/year`;
- Business: `$99`.

Payment approach:

- do not use Paddle;
- request written pre-approval from Lemon Squeezy;
- request Stripe risk confirmation as fallback;
- do not integrate checkout before category approval.

## GitHub Tracking Structure

Recommended GitHub issue groups:

- Strategy;
- Packaging;
- Security;
- Jobs/History;
- Batch/Queue;
- Presets;
- Diagnostics;
- Output Management;
- Website;
- Monetization;
- Distribution;
- Legal/Compliance.

GitHub Project board status:

- `gh` CLI token is currently invalid locally.
- `gh project` requires a token with `project` scope.
- Until re-authentication is done, track execution through GitHub issues and this document.

## Immediate Next Step

Create GitHub issues for the P0 commercialization backlog, then decide the first implementation block:

```text
Commercial Block 1: Public Product Boundary + Positioning Cleanup
```

This should hide/remove risky public-facing Udemy positioning, define Free/Pro boundaries, and prepare the product for packaging work.
