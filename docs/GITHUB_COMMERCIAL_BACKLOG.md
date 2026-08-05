# GitHub Commercial Backlog

Source strategy:

- `docs/UNIVERSAL_MEDIA_EXTRACTOR_PRODUCT_STRATEGY.md`
- `docs/COMMERCIALIZATION_EXECUTION_PLAN.md`

## Current GitHub Status

Repository:

```text
Shteinyr/universal-media-extractor
```

Repository URL:

`https://github.com/Shteinyr/universal-media-extractor`

GitHub Project:

`Universal Media Extractor Commercial Roadmap`

Project URL:

`https://github.com/users/Shteinyr/projects/7`

Created on 2026-08-05 using local `/opt/homebrew/bin/gh`.

Current setup:

- GitHub Project created and linked to the repository.
- 8 milestones created.
- Priority/Track/Release/Roadmap Status fields created.
- 40 roadmap issues created.
- All roadmap issues were added to the Project.
- Project fields were populated through `gh project item-edit`, with `Roadmap Status=Backlog` for all initial items.

## Recommended GitHub Project Fields

Roadmap Status:

- Backlog
- Ready
- In Progress
- Review
- Done
- Blocked

GitHub default Status remains available as `Todo / In Progress / Done`, but roadmap tracking uses `Roadmap Status`.

Priority:

- P0
- P1
- P2

Track:

- Strategy
- Packaging
- Security
- Jobs
- Batch
- Presets
- Diagnostics
- Output
- Website
- Monetization
- Distribution
- Legal

Release:

- Public Beta
- Founder Launch
- Windows Store
- Later

## Issues To Create

### 1. [Strategy] Commercialization roadmap tracker

Priority: P0
Track: Strategy
Release: Public Beta

Description:

Convert the product strategy into executable product, engineering, compliance, and distribution work.

Acceptance criteria:

- Strategy document is saved in the repository.
- Commercial roadmap is summarized in a working execution plan.
- P0/P1/P2 work is tracked in GitHub.
- Risky public positioning is separated from internal experimental features.

### 2. [P0] Define public product boundary and positioning

Priority: P0
Track: Strategy
Release: Public Beta

Description:

Position Universal Media Extractor as a local media downloader and organizer, not as a universal downloader for every site.

Acceptance criteria:

- Product category is defined.
- Main promise is defined.
- Public copy avoids guaranteed source support.
- Public copy avoids DRM/paywall/login bypass claims.
- Free/Pro/Business boundaries are drafted.

### 3. [P0] Hide Udemy Course Mode from public commercial builds

Priority: P0
Track: Legal
Release: Public Beta

Description:

Keep Udemy Course Mode as internal/experimental unless legal and platform risk is separately approved.

Acceptance criteria:

- Public UI/build can hide Course Mode.
- Website does not advertise Udemy course export.
- Docs explain internal/best-effort status.
- No credentials, cookies, DRM keys, or bypass behavior are stored or implemented.

### 4. [P0] Build production macOS Apple Silicon app

Priority: P0
Track: Packaging
Release: Public Beta

Description:

Create a production-grade macOS build for Apple Silicon.

Acceptance criteria:

- App bundle packages runtime correctly.
- Backend launches and stops with app lifecycle.
- App is Developer ID signed.
- Hardened runtime is enabled.
- App is notarized.
- `.dmg` installer is produced.
- Uninstall behavior is documented.

### 5. [P0] Build production Windows x64 installer

Priority: P0
Track: Packaging
Release: Public Beta

Description:

Create a production-grade Windows x64 installer for direct download.

Acceptance criteria:

- Windows app runs without terminal.
- Installer creates Start Menu/Desktop shortcuts.
- Uninstaller works.
- App is signed.
- Output folder behavior works on Windows.
- Windows-specific path and permission tests pass.

### 6. [P0] Add SQLite-backed persistent jobs and history

Priority: P0
Track: Jobs
Release: Public Beta

Description:

Replace in-memory jobs with persistent local job history.

Acceptance criteria:

- Jobs survive restart.
- Status/progress/error/result are persisted.
- Failed jobs can be retried.
- History can be cleared without deleting files.
- Interrupted jobs recover to a clear state.

### 7. [P0] Add queue and batch processing foundation

Priority: P0
Track: Batch
Release: Founder Launch

Description:

Add a queue for multiple URLs and playlist items.

Acceptance criteria:

- User can add multiple URLs.
- User can import URLs from clipboard/text.
- Queue runs with controlled concurrency.
- Failed items can be retried.
- Queue order is visible.
- Pause/resume behavior is defined.

### 8. [P0] Replace technical format selection with presets

Priority: P0
Track: Presets
Release: Public Beta

Description:

Make output selection user-friendly and commercial-grade.

Acceptance criteria:

- Presets exist for Best Video, 1080p, Smaller Video, Audio M4A, Audio MP3, Subtitles, and Archive Pack.
- Technical formats are hidden by default.
- Advanced details remain available only when needed.
- Existing direct format download behavior is preserved internally.

### 9. [P0] Add media engine update channel and rollback

Priority: P0
Track: Packaging
Release: Founder Launch

Description:

Separate app updates from `yt-dlp`/engine compatibility updates.

Acceptance criteria:

- Engine manifest format is defined.
- Downloads are hash-verified.
- Stable and Compatibility channels are planned.
- Rollback to previous engine is possible.
- Engine storage location is safe for signed desktop apps.

### 10. [P0] Normalize user-facing errors

Priority: P0
Track: Diagnostics
Release: Public Beta

Description:

Replace raw CLI failure messages with understandable errors.

Acceptance criteria:

- Errors are mapped to normalized categories.
- Technical logs are collapsible.
- DRM/login/region/private/deleted/no-format/network/disk/permission cases are handled.
- UI gives clear recovery suggestions.

### 11. [P0] Add diagnostics bundle

Priority: P0
Track: Diagnostics
Release: Public Beta

Description:

Create a safe support bundle for debugging failed jobs.

Acceptance criteria:

- Bundle includes app version, engine version, OS/arch, extractor type, normalized error, and redacted logs.
- Bundle excludes cookies, tokens, full URLs, transcripts, and local paths by default.
- User can inspect bundle before sharing.

### 12. [P0] Add output templates and duplicate handling

Priority: P0
Track: Output
Release: Founder Launch

Description:

Let users control output naming and folder structure.

Acceptance criteria:

- Templates support source/channel/date/title/project/playlist index.
- Filenames are safe on macOS and Windows.
- Duplicate behavior supports skip/rename/overwrite.
- User can reveal output in Finder/Explorer.

### 13. [P0] Harden localhost security

Priority: P0
Track: Security
Release: Public Beta

Description:

Make the local API safer for production desktop use.

Acceptance criteria:

- Random session token is required between UI and backend.
- CORS/origin allowlist is strict.
- CSRF risk is addressed.
- Upload size limits exist.
- File path access is constrained.
- Frontend cannot pass arbitrary CLI arguments.
- Secrets are redacted from logs.

### 14. [GTM] Create product landing page

Priority: P0
Track: Website
Release: Public Beta

Description:

Create a public website for the beta and later paid launch.

Acceptance criteria:

- Landing page explains local/private workflow.
- macOS/Windows download sections exist.
- Known limitations are visible.
- Privacy/EULA/refund/support pages are linked.
- CTA supports beta signup/download.

### 15. [Monetization] Prepare licensing and payment approval

Priority: P0
Track: Monetization
Release: Founder Launch

Description:

Prepare payment and licensing path without integrating checkout prematurely.

Acceptance criteria:

- Compliance memo is written.
- Lemon Squeezy pre-approval request is prepared.
- Stripe fallback review is prepared.
- License entitlement model is defined.
- Free/Founder/Pro/Business terms are documented.

### 16. [Distribution] Prepare Microsoft Store path

Priority: P1
Track: Distribution
Release: Windows Store

Description:

Prepare Microsoft Store submission after direct Windows beta proves stable.

Acceptance criteria:

- MSIX package path is defined.
- Store description avoids risky claims.
- Privacy and support links are ready.
- Windows installer telemetry/support issues are reviewed.
- Udemy/internal experimental features are excluded.

### 17. [Legal] Prepare EULA, privacy policy, and limitations docs

Priority: P0
Track: Legal
Release: Public Beta

Description:

Prepare commercial legal surface before beta.

Acceptance criteria:

- EULA draft exists.
- Privacy policy draft exists.
- Refund policy draft exists.
- Known limitations are user-facing.
- Rights/use responsibility onboarding is included.

### 18. [QA] Define beta metrics and feedback loop

Priority: P0
Track: Strategy
Release: Public Beta

Description:

Define what the beta must prove before paid launch.

Acceptance criteria:

- Activation target is defined.
- Successful first job metric is defined.
- Weekly active usage metric is defined.
- Failure categories are tracked.
- Refund/support risk criteria are documented.

