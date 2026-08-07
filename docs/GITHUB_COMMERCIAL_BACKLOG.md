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
- Commercial Foundation issues #1-#5, Commercial Block 2 issues #6-#7, Commercial Block 3 issue #9, Commercial Block 4 issue #8, Commercial Block 5 issue #10, and Commercial Block 6 issue #11 are completed and should be tracked as `Done`.
- Commercial Blocks 7-10 prepared macOS production/signing/DMG/public release readiness. Issues #13 and #14 remain open and `In Progress` because final acceptance needs Apple Developer ID credentials and real notarization/Gatekeeper validation.
- Commercial Block 11 prepares the founder launch surface for issues #19-#21: landing page, beta onboarding, and Free / Founder Pro / Pro / Business plan documentation.
- GPT Pro final UI/UX commercial spec was imported after the first UI/UX research pack. New stricter final-public-beta issues #41-#51 were created under the `Public Beta Readiness` milestone and added to the Project. Old closed issues remain closed; #41-#51 represent the next stricter UI/UX readiness layer.

## GPT Pro Final UI/UX Issues

Source:

- `docs/UNIVERSAL_MEDIA_EXTRACTOR_FINAL_UI_UX_COMMERCIAL_SPEC.md`
- `docs/FINAL_UI_UX_IMPLEMENTATION_PLAN.md`

Tracker:

- #41 `[UI/UX] Final public beta UX refactor tracker`

First executable block completed:

- #42 `[P0] Public build Course surface removal hardening`
- #43 `[P0] Backend source-of-truth audit and endpoint inventory`
- #44 `[P0] Universal New Task composer`
- #45 `[P0] Stable semantic preset resolver`

Result: implemented in Public Beta UI/UX Refactor Block 1 and documented in `docs/PUBLIC_BETA_UI_UX_REFACTOR_BLOCK_1.md` plus `docs/PUBLIC_BETA_BACKEND_SOURCE_OF_TRUTH.md`.

Completed follow-up issues:

- #46 `[P0] Durable Queue and Library finalization`

Result: implemented and documented in `docs/PUBLIC_BETA_DURABLE_QUEUE_LIBRARY.md`.

Remaining follow-up issues:

- #47 `[P0] Native filesystem integration`
- #48 `[P0] Unified progress, cancel, retry, recovery`
- #49 `[P0] Error normalization and diagnostics final pass`
- #50 `[P1] Result and local transcription UX final pass`
- #51 `[P1] Commercial desktop readiness final pass`

All #41-#51 issues are in GitHub Project #7. After Public Beta UI/UX Refactor Block 1:

- #42-#45 have `Roadmap Status=Done` and `Status=Done`.
- #46 has `Roadmap Status=Done` and `Status=Done`.
- #47-#51 remain follow-up public beta readiness work.
- `Release=Public Beta` remains the release target for this UI/UX issue group.

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



## Commercial Foundation Completion

Completed issue set:

- #1 `[Strategy] Commercialization roadmap tracker`
- #2 `[P0] Define public product boundary and positioning`
- #3 `[P0] Hide Udemy Course Mode from public commercial builds`
- #4 `[P0] Prepare legal-safe product copy`
- #5 `[P0] Prepare EULA, privacy policy, refund policy, known limitations`

Evidence files:

- `docs/PUBLIC_PRODUCT_BOUNDARY.md`
- `docs/LEGAL_SAFE_PRODUCT_COPY.md`
- `docs/EULA_DRAFT.md`
- `docs/PRIVACY_POLICY_DRAFT.md`
- `docs/REFUND_POLICY_DRAFT.md`
- `docs/PUBLIC_KNOWN_LIMITATIONS.md`

Implementation evidence for #3:

- `GET /config` exposes `public_product_mode` and `course_mode_enabled`.
- Static UI hides Course Mode when `course_mode_enabled=false`.
- Public builds can set `UME_PUBLIC_PRODUCT_MODE=1`.


## Commercial Block 2 Completion

Completed issue set:

- #6 `[P0] Normalize user-facing errors`
- #7 `[P0] Add diagnostics bundle`

Evidence files:

- `src/universal_media_extractor/error_mapping.py`
- `src/universal_media_extractor/models/diagnostics.py`
- `src/universal_media_extractor/services/diagnostics_service.py`
- `docs/COMMERCIAL_BLOCK_2_ERRORS_DIAGNOSTICS.md`
- `tests/test_error_mapping.py`
- `tests/test_diagnostics_service.py`

API evidence:

- `GET /diagnostics/jobs/{job_id}` returns a local redacted diagnostics JSON bundle.

## Commercial Block 3 Completion

Completed issue:

- `#9 [P0] Replace technical format selection with presets`

Result:

- Public URL output selection now uses presets instead of raw technical streams.
- Presets: `Best Video`, `1080p`, `Smaller Video`, `Audio M4A`, `Audio MP3`, `Subtitles`, and disabled planned `Archive Pack`.
- Technical stream details are hidden by default and available through `Advanced details`.
- Existing internal `/download` behavior still receives the selected `format_id`.

Documentation:

- `docs/COMMERCIAL_BLOCK_3_PRESET_OUTPUT_SELECTION.md`

## Commercial Block 4 Completion

Completed issue:

- `#8 [P0] Harden localhost security`

Result:

- Protected API calls require a random local session token.
- CORS/origin/host checks are local-only and explicit.
- CSRF risk is reduced by avoiding cookies and requiring a custom session-token header.
- Local upload size limits exist.
- Existing path constraints, CLI allowlists, and diagnostics redaction remain in place.

Documentation:

- `docs/COMMERCIAL_BLOCK_4_LOCALHOST_SECURITY.md`


## Commercial Block 5 Completion

Completed issue:

- `#10 [P0] Add SQLite-backed persistent jobs and history`

Result:

- Jobs persist to local SQLite.
- Status, progress, error, result, timestamps, and retry linkage are saved.
- Queued/running jobs from a previous app run recover to a clear failed/interrupted state.
- Failed jobs can be retried.
- Terminal job history can be cleared without deleting output files.

Documentation:

- `docs/COMMERCIAL_BLOCK_5_SQLITE_JOBS_HISTORY.md`

## Commercial Block 7 - macOS Production Build Foundation

- GitHub issue #12: `[P0] Build production macOS Apple Silicon app`.
- Status: completed foundation.
- Added PyInstaller `.app` build script/spec and smoke-verified `build/macos/dist/Universal Media Extractor.app`.
- Signing/notarization (#13) and DMG installer (#14) remain separate roadmap tasks.

## Commercial Block 8 - macOS Signing / Notarization Readiness

- GitHub issue #13: `[P0] Add macOS signing and notarization`.
- Status: readiness prepared, issue remains open.
- Added scripts/docs for Developer ID signing, hardened runtime, notarytool credentials, notarization, stapling, and Gatekeeper assessment.
- Current blocker: no `Developer ID Application` certificate is installed in Keychain.
- DMG installer remains separate issue #14.

## Commercial Block 9 - macOS DMG Installer Readiness

- GitHub issue #14: `[P0] Create macOS DMG installer`.
- Status: readiness prepared, issue remains open.
- Added DMG build script, tests, install/uninstall docs, checksum generation, and local unsigned DMG proof.
- Current blocker: final public DMG must include a signed/notarized app, which depends on issue #13.

## Commercial Block 12 Completion Notes

Issues #22 and #23 are covered by:

- `docs/COMMERCIAL_BLOCK_12_PAYMENT_LICENSING_PREP.md`
- `docs/LEMON_SQUEEZY_PREAPPROVAL_REQUEST.md`
- `docs/STRIPE_FALLBACK_RISK_REVIEW.md`
- `docs/LICENSING_MODEL_DRAFT.md`
- `docs/PAYMENT_LICENSING_USER_DECISIONS.md`

Implementation remains intentionally blocked until provider approval and user business details are available.
