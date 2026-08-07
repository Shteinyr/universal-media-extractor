# Project Context

## Project Identity

- Name: Universal Media Extractor.
- Working directory: `/Users/aleksandr/Developer/Codex/Projects/Universal Media Extractor`.
- Product: local media downloader/transcriber for URLs and local audio/video files.
- Current status: Blocks 1-11 completed; Udemy Course Offline Export with Chrome session auth added and refined after real user testing; commercial strategy imported; GitHub roadmap created; Commercial Foundation issues #1-#5 completed; Commercial Blocks 2-14 completed/prepared across diagnostics, presets, localhost security, SQLite jobs/history, output templates, macOS packaging readiness, founder launch surface, and payment/licensing pre-approval docs, batch queue foundation, and public beta UI readiness. Public Beta QA Round, Public Beta UI / UX Finalization Implementation, Public Beta UI/UX Refactor Block 1, Durable Queue/Library finalization, and Native filesystem integration are completed.
- Roadmap source: `docs/ROADMAP_V2.md`.
- Commercial strategy source: `docs/UNIVERSAL_MEDIA_EXTRACTOR_PRODUCT_STRATEGY.md`.
- GitHub commercial roadmap board: `https://github.com/users/Shteinyr/projects/7`.

## Product Goal

Universal Media Extractor is a local, single-user media utility.

Primary flows:

- URL -> Analyze -> Download -> Transcribe -> Result.
- Local file -> Analyze -> Transcribe -> Result.
- Udemy lecture/player URL + Chrome session -> Analyze course playlist -> Download course.

The product should help a user inspect available outputs, choose a clear result, save files locally, and optionally create a local Whisper transcript without paid APIs or cloud processing.

Commercial direction after GPT Pro strategy review:

- position as `Local Media Downloader & Organizer for macOS and Windows`;
- sell installation, organization, presets, history, batch, compatibility updates, diagnostics, and local processing rather than merely `yt-dlp` execution;
- keep Udemy Course mode internal/experimental for now and hidden from public builds/marketing;
- avoid public claims around universal source support, DRM, paywall, CAPTCHA, or login bypass;
- prepare direct website distribution first, Microsoft Store later, and avoid Mac App Store for the full downloader.

## Core Principles

- Local-first.
- Single-user.
- Best-effort source support through `yt-dlp`.
- No paid APIs by default.
- No online service behavior.
- No external data sending.
- Backend binds only to `127.0.0.1`.
- Download/process actions preserve rights-confirmation requirements in the backend contract.
- No DRM, CAPTCHA, paywall, login, or platform restriction bypass.
- Udemy support uses Chrome session auth by default, keeps manual cookies as advanced fallback, and must not store credentials or bypass DRM. Public builds hide Course Mode by setting `UME_PUBLIC_PRODUCT_MODE=1`.
- Codex recommendations are recommendations only, not roadmap decisions.

## Current Architecture

- Python backend.
- FastAPI local API.
- Uvicorn local server.
- Static vanilla HTML/CSS/JS frontend.
- `yt-dlp` for URL analysis/download.
- `ffmpeg`/`ffprobe` for media metadata, extraction, and conversion.
- Whisper CLI for local transcription.
- SQLite-backed persistent job system for download/transcription history and durable batch queue snapshots.
- Output indexing and safe delete for managed result folders.
- Python Playwright for manual/dev browser smoke checks.
- `pywebview` for the local desktop wrapper.
- Udemy course analyze/download service through `yt-dlp`.
- Shared error normalization and local redacted diagnostics bundles for failed jobs.
- Local API security middleware with random session token, local origin/host checks, explicit CORS policy, and upload size cap.

## Completed Roadmap

- Block 1. Analysis Foundation - done.
- Block 2. Download + Output Pipeline - done.
- Block 3. Whisper + Transcript Pipeline - done.
- Block 4. Processing UI + MVP Flow - done.
- Block 5. MVP Readiness Review - done.
- Block 6. Job / Progress / Cancel - done.
- Block 7. Local File Input - done.
- Block 8. Cleanup / Output Management - done.
- Block 9. Real Progress / Subprocess Cancellation Hardening - done.
- Block 10. Browser Verification / UI QA Tooling - done.
- Block 11. Desktop Wrapper - done.

## Latest Completed Block

Native filesystem integration - done.

Created doc:

- `docs/PUBLIC_BETA_NATIVE_FILESYSTEM_INTEGRATION.md`

Result: issue #47 is implemented. Desktop mode exposes native file/folder pickers through the existing `pywebview` wrapper. Desktop-selected local files can be analyzed in place through `POST /local/analyze-path` without copying large media only for metadata. Downloads validate user-selected output folders before starting. Reveal/Open remains limited to managed output ids and prefers the primary result file where available. The main UI keeps the short default save path instead of expanding it into a long absolute path on startup.

Verification:

- `node --check src/universal_media_extractor/static/app.js`;
- `node --check src/universal_media_extractor/static/option_normalizer.js`;
- `.venv/bin/python -m pytest tests/test_api_app.py tests/test_output_manager.py tests/test_download_service.py tests/test_desktop_launcher.py -q` -> `94 passed` plus one sandbox-only socket permission failure;
- `.venv/bin/python -m pytest -q` outside sandbox -> `216 passed`;
- `.venv/bin/python scripts/browser_smoke.py --proof-dir proof/native_filesystem_integration`.

Proof screenshots:

- `proof/native_filesystem_integration/ui_initial.png`
- `proof/native_filesystem_integration/ui_analyze_result.png`
- `proof/native_filesystem_integration/ui_output_selected.png`
- `proof/native_filesystem_integration/ui_library.png`

Previous completed block:

Durable Queue and Library finalization - done.

Created doc:

- `docs/PUBLIC_BETA_DURABLE_QUEUE_LIBRARY.md`

Result: issue #46 is implemented. Queue and Library responsibilities are separated. Queue now persists batch group snapshots in SQLite, exposes `GET /batch`, recovers interrupted queued/running batches into failed/recoverable states on startup, preserves retry settings, and marks missing output paths as `output_missing`. Library remains output-folder based through `/outputs` and now shows separate Queue and Files sections in the UI.

Verification:

- `node --check src/universal_media_extractor/static/app.js`;
- `node --check src/universal_media_extractor/static/option_normalizer.js`;
- `python3 -m py_compile scripts/browser_smoke.py`;
- `.venv/bin/python -m pytest tests/test_api_app.py tests/test_batch_service.py -q` -> `60 passed`;
- `.venv/bin/python -m pytest -q` -> `204 passed`;
- `.venv/bin/python scripts/browser_smoke.py --proof-dir proof/durable_queue_library`.

Proof screenshots:

- `proof/durable_queue_library/ui_initial.png`
- `proof/durable_queue_library/ui_analyze_result.png`
- `proof/durable_queue_library/ui_output_selected.png`
- `proof/durable_queue_library/ui_library.png`

Previous completed block:

Public Beta UI/UX Refactor Block 1 - done.

Created docs:

- `docs/PUBLIC_BETA_UI_UX_REFACTOR_BLOCK_1.md`
- `docs/PUBLIC_BETA_BACKEND_SOURCE_OF_TRUTH.md`

Result: issues #42-#45 are implemented. Public mode hides Course/Udemy/cookies/Chrome-session surfaces and does not register internal Course endpoints. The public UI now starts from a single `New task` composer that routes one URL, local files, multiple links, and `.txt/.csv` URL lists. Output choices use stable semantic presets: Best video, 1080p video, Up to 720p, Audio M4A, Audio MP3, and Subtitles.

Verification:

- `node --check src/universal_media_extractor/static/app.js`;
- `node --check src/universal_media_extractor/static/option_normalizer.js`;
- `.venv/bin/python -m pytest tests/test_batch_service.py tests/test_ui_option_normalizer.py tests/test_api_app.py -q` -> `62 passed`;
- `.venv/bin/python -m pytest -q` -> `200 passed`;
- `.venv/bin/python scripts/browser_smoke.py --proof-dir proof/final_ui_ux_refactor_block_1`.

Proof screenshots:

- `proof/final_ui_ux_refactor_block_1/ui_initial.png`
- `proof/final_ui_ux_refactor_block_1/ui_analyze_result.png`
- `proof/final_ui_ux_refactor_block_1/ui_output_selected.png`

Previous completed block:

Public Beta UI / UX Finalization Implementation - done.

Created doc:

- `docs/PUBLIC_BETA_UI_UX_FINALIZATION_IMPLEMENTATION.md`

Result: the static UI now follows the approved blueprint without adding backend/API scope or roadmap changes. The first screen is source-first, URL presets are user-facing, save options appear only after output selection, advanced save controls are collapsed, Local file metadata is simplified, Recent results moved to a collapsed Library surface, and browser smoke now captures initial, analyzed, and output-selected states.

Verification:

- `node --check src/universal_media_extractor/static/app.js`;
- `node --check src/universal_media_extractor/static/option_normalizer.js`;
- `python3 -m py_compile scripts/browser_smoke.py`;
- `.venv/bin/python -m pytest -q` -> `196 passed`;
- browser smoke proof under `proof/public_beta_ui_ux_finalization/`.

Previous completed block:

Public Beta QA Round - done.

## Latest UX Blueprint

Public Beta UI / UX Finalization Blueprint - done.

Created doc:

- `docs/PUBLIC_BETA_UI_UX_FINALIZATION_BLUEPRINT.md`

Final UI direction: compact local desktop downloader/file-manager utility. Public beta structure should use clear `Link / File / Batch` modes, keep Course/Udemy hidden in public builds, lead with source input, then output presets, save options, honest processing state, saved result, and optional post-processing transcription.

## Latest Research Package

UI/UX Research / Context Pack for GPT Pro - done.

Created docs:

- `docs/UI_UX_COMPETITOR_VISUAL_AUDIT.md`
- `docs/UI_UX_PRODUCT_FUNCTION_INVENTORY.md`
- `docs/UI_UX_REFERENCE_SCREEN_MAP.md`
- `docs/UI_UX_GPT_PRO_BRIEF.md`
- `docs/UI_UX_GPT_PRO_CONTEXT_PACK.md`
- `docs/UI_UX_COMPETITOR_VISUAL_LOGIC_PACK.md`
- `docs/UI_UX_OUR_APP_VISUAL_LOGIC_PACK.md`
- `docs/UI_UX_GPT_PRO_ANALYSIS_PROMPT.md`

The GPT Pro strategy competitor list is the required baseline and must not be ignored during UI finalization. Supplemental references may be used only to improve visual/flow judgment, not to change roadmap scope. Public screenshots and current app screenshots are saved under `proof/ui_ux_gpt_pro_pack/`.

## Latest GPT Pro Final UI/UX Spec Tracking

GPT Pro final UI/UX commercial spec is imported and tracked.

Docs:

- `docs/UNIVERSAL_MEDIA_EXTRACTOR_FINAL_UI_UX_COMMERCIAL_SPEC.md`
- `docs/FINAL_UI_UX_IMPLEMENTATION_PLAN.md`

GitHub:

- #41 `[UI/UX] Final public beta UX refactor tracker`
- #42 `[P0] Public build Course surface removal hardening`
- #43 `[P0] Backend source-of-truth audit and endpoint inventory`
- #44 `[P0] Universal New Task composer`
- #45 `[P0] Stable semantic preset resolver`
- #46-#51 later follow-up final UI/UX readiness tasks

Public Beta UI/UX Refactor Block 1 issues #42-#45 are completed; follow-up issues #46-#51 remain later public beta readiness work.

Result: the current beta baseline passed browser/API/local-file/batch/diagnostics/output QA. Verified JS syntax, `196 passed`, browser smoke screenshots, URL analyze/download/transcribe, local synthetic file analyze/transcribe, one-item batch download, diagnostics redaction, output safe delete, and public mode Course hiding. No blocker product bug was found. Documented in `docs/PUBLIC_BETA_QA_ROUND.md`.

Previous completed block: Beta Website / Download Flow - done.

Result: the public beta website/download packaging is documented without deploying a production site or changing core app code. The doc defines public positioning, landing sections, download CTA states, macOS/Windows availability copy, early-access/waitlist flow, limitations, privacy/no-cloud copy, and support diagnostics messaging. Documented in `docs/BETA_WEBSITE_DOWNLOAD_FLOW.md`.

Previous completed block: Public Beta Security / Diagnostics / QA Review - done.

Result: local beta security and support readiness were tightened without roadmap changes. `/config` and diagnostics responses now use no-store headers, non-local Host rejection has regression coverage, and failed/cancelled background jobs can copy the existing redacted diagnostics bundle from the UI. Documented in `docs/PUBLIC_BETA_SECURITY_DIAGNOSTICS_QA_REVIEW.md`.

Previous completed block: Commercial Block 14: Public Beta UI Readiness / User-Facing UX Pass - done.

Result: the existing static UI was polished for a clearer public beta surface without new product features or API changes. Mode tabs, empty/loading states, download/transcript status cards, batch item rows, progress display, and primary error titles are now more user-facing. Proof screenshots are under `proof/commercial_block_14_ui_readiness/`.

Previous completed block: Commercial Block 13: Batch Queue Foundation + Playlist/Clipboard Import - done.

Result: Batch mode supports textarea/clipboard/text-file URL import, safe flat playlist analysis with item selection, controlled concurrency, child download jobs, queue status polling, cancellation request, and retry failed items. Archive Pack remains planned/disabled and issue #29 stays open.

Previous completed block:

Commercial Block 12: Payment Provider Pre-Approval And Licensing Prep - done.

Result: Lemon Squeezy pre-approval request, Stripe fallback risk review, licensing model draft, and user decision checklist are prepared. Issues #22 and #23 are closed and marked Done in the GitHub Project. No checkout, webhooks, license server, license activation UI, or license enforcement code was added.

Previous completed block:

Commercial Block 11: Founder Launch Surface - done.

Result: public static site, founder launch copy, beta onboarding copy, draft pricing/plans, and support page draft are prepared. GitHub issues #19, #20, and #21 are closed and marked Done in the project. No checkout, license activation, Apple signing, Windows build, or new downloader feature was added.

Previous completed block:

Commercial Block 10: macOS Public Release Prep - prepared.

Result: public macOS release checklist, Apple Developer setup guide, signed/notarized app and DMG validation checklist, and troubleshooting guide are documented. A DMG notarization helper exists for the later real Apple Developer ID flow. GitHub issues #13 and #14 remain open because final acceptance requires a real Developer ID Application certificate, notary credentials, successful notarization, stapling, and Gatekeeper validation.

Previous completed block:

Commercial Block 6: Output Templates And Duplicate Handling - done.

Result: URL downloads now support output folder templates with `{source}`, `{channel}`, `{date}`, `{title}`, `{project}`, and `{playlist_index}` tokens. User-facing folder names are sanitized for macOS/Windows. Duplicate behavior supports `rename`, `skip`, and `overwrite`; skip avoids running `yt-dlp`. Managed outputs can be revealed through `POST /outputs/{output_id}/reveal` and the UI exposes a Reveal action.

Previous completed block: Commercial Block 5: SQLite Jobs And History - done.

Result: job state now persists to local SQLite at `data/jobs.sqlite3`. Jobs survive restart, interrupted queued/running jobs recover to a failed recoverable state, failed jobs can be retried through `POST /jobs/{job_id}/retry`, and terminal history can be cleared through `DELETE /jobs/history` without deleting output files.

Commercial Block 4 remains completed: protected local API calls require an in-memory random session token, the backend rejects non-local hosts/origins, CORS is local-only, and upload limits are enforced. Commercial Block 3 remains completed: the public URL output picker shows presets instead of raw technical stream rows, while internal `format_id` values stay available for `/download`.

Udemy Course Offline Export remains completed as an internal/experimental feature. The UI must preserve pasted Udemy lecture/player URLs and not rewrite them into clean course URLs.

Desktop command:

```bash
.venv/bin/python scripts/run_desktop.py
```

The wrapper starts Uvicorn on `127.0.0.1`, opens the actual UI in a native window, and shuts down its owned backend when the window closes.

Udemy command path is documented in `docs/UDEMY_COURSE_EXPORT.md`.

## Planned Next Block

Commercial Blocks 1-14 are completed or prepared except for externally blocked Apple/payment work and the still-open Archive Pack execution issue. The previous Roadmap v2 next block was Block 12 Chrome Extension, but commercialization strategy now recommends prioritizing Public Beta Readiness before extension work.

Recommended next user-approved commercial block, depending on user readiness:

```text
Unified progress, cancel, retry, recovery
```

Candidate direction: continue with issue #48 to refine long-running task behavior. If Apple Developer Program access and signing credentials are ready, macOS signed public beta release validation can be chosen instead.

Do not start the next block until the user explicitly confirms. Do not start checkout or licensing enforcement until payment provider approval and user business details are ready.

## Later / Optional

- Archive Pack execution.
- Persistent parent batch history if needed.
- Cookies/login manual mode.
- AI summary API.
- Presets are implemented for the main URL output selector; saved presets and Archive Pack execution remain later.
- History/search.
- Advanced settings.
- Output retention policy.
- Advanced cleanup policies.

## Current Working Commands

Run browser mode:

```bash
cd "/Users/aleksandr/Developer/Codex/Projects/Universal Media Extractor"
.venv/bin/python scripts/run_api.py
```

Open:

```text
http://127.0.0.1:8000/
```

Run tests:

```bash
.venv/bin/python -m pytest -q
```

Run browser smoke:

```bash
.venv/bin/python scripts/browser_smoke.py
```

Run desktop mode:

```bash
.venv/bin/python scripts/run_desktop.py
```

Build development `.app` launcher:

```bash
.venv/bin/python scripts/build_dev_app.py
open "build/dev/Universal Media Extractor Dev.app"
```

The dev `.app` can also be copied to `/Applications`; it remains tied to this project folder and `.venv`.

## Important Existing Behavior

- UI is simplified into a compact downloader/file-manager style.
- URL output selection now uses public presets instead of raw technical stream rows.
- Final UI cleanup hides development-oriented sidebar areas: visible backend status, MVP flow checklist, repeated helper copy, and Recent results.
- URL downloads default to `~/Downloads/Universal Media Extractor`.
- URL downloads support output folder templates and duplicate policies: rename, skip, overwrite.
- The download card has editable `Save to` and `Format` controls.
- Video output downloads selected video together with best available audio into one final file.
- Audio output downloads/extracts audio-only results.
- Subtitles output downloads subtitles/captions and should not show transcription as the next action.
- Transcription requires an audio file or a video file with an audio track.
- Transcript output saves one selected format per run: `TXT`, `Markdown`, or `JSON`.
- Technical stream rows are hidden from the main UI and available under `Advanced details`.
- Video options below `1080p` are hidden in advanced details.
- User-facing video and subtitle options are deduplicated before preset construction.
- Recent results work for the configured output base.
- Safe delete is constrained to managed output folders.
- `proof/` is development evidence and is not indexed as user output.

## Key Files

- `src/universal_media_extractor/api/app.py`
- `scripts/run_api.py`
- `scripts/run_desktop.py`
- `scripts/build_dev_app.py`
- `src/universal_media_extractor/static/index.html`
- `src/universal_media_extractor/static/styles.css`
- `src/universal_media_extractor/static/app.js`
- `src/universal_media_extractor/services/job_service.py`
- `src/universal_media_extractor/services/download_service.py`
- `src/universal_media_extractor/services/transcription_service.py`
- `src/universal_media_extractor/services/output_manager.py`
- `src/universal_media_extractor/services/local_file_metadata_service.py`

## Governance

- Do not create new Phase numbering.
- Do not create new Blocks without explicit user approval.
- If Codex sees a better path, blocker, or risk, it may recommend a change, but must not change the roadmap itself.
- Follow `docs/ROADMAP_V2.md` unless the user explicitly changes it.
- Before every large task, read `PROJECT_CONTEXT.md`.
- After every completed block, update `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`, `CHANGELOG.md`, `README.md`, and relevant docs.


## Commercial Foundation Docs

- `docs/PUBLIC_PRODUCT_BOUNDARY.md`
- `docs/LEGAL_SAFE_PRODUCT_COPY.md`
- `docs/EULA_DRAFT.md`
- `docs/PRIVACY_POLICY_DRAFT.md`
- `docs/REFUND_POLICY_DRAFT.md`
- `docs/PUBLIC_KNOWN_LIMITATIONS.md`

These documents close GitHub issues #1-#5 and define the public product boundary for future website, packaging, and beta work.


## Commercial Block 2 Docs

- `docs/COMMERCIAL_BLOCK_2_ERRORS_DIAGNOSTICS.md`

This document closes GitHub issues #6-#7 and defines the first public-beta diagnostics boundary.


## Commercial Block 3 Docs

- `docs/COMMERCIAL_BLOCK_3_PRESET_OUTPUT_SELECTION.md`

This document closes GitHub issue #9 and defines the first public preset-based output selection layer.


## Commercial Block 4 Docs

- `docs/COMMERCIAL_BLOCK_4_LOCALHOST_SECURITY.md`

This document closes GitHub issue #8 and defines the first public-beta localhost API security boundary.


## Commercial Block 5 Docs

- `docs/COMMERCIAL_BLOCK_5_SQLITE_JOBS_HISTORY.md`

This document closes GitHub issue #10 and defines the first public-beta persistent jobs/history boundary.

## 2026-08-05 - Commercial Block 7 macOS Production Build Foundation

- Added PyInstaller macOS production-foundation build support.
- `scripts/build_macos_app.py` builds `build/macos/dist/Universal Media Extractor.app`.
- `scripts/run_desktop.py` now supports production runtime paths and Finder-safe CLI path setup.
- Production desktop data uses `~/Library/Application Support/Universal Media Extractor`; user outputs default to `~/Downloads/Universal Media Extractor`.
- Verification confirmed the built app starts the local backend, opens the desktop UI, and stops the backend after close.
- Apple Developer ID signing/notarization and DMG installer are separate next packaging tasks, not part of this block.
- Next recommended commercial block: issue #13, macOS signing and notarization, but do not start it without explicit user approval.

## 2026-08-05 - Commercial Block 8 macOS Signing / Notarization Readiness

- Prepared Developer ID signing and notarization readiness without performing real signing.
- Added readiness/preflight script, signing script, notarytool credential helper, notarization/stapling script, and empty hardened-runtime entitlements file.
- Official Apple docs confirm Developer ID signing, Hardened Runtime, `notarytool`, stapling, and Gatekeeper validation are required for direct macOS distribution.
- Current local readiness check passes for Xcode tools and the built `.app`, but fails because no `Developer ID Application` certificate is available in Keychain.
- Issue #13 must remain open until Apple Developer ID certificate and notarytool credentials are available and notarization/Gatekeeper checks actually pass.
- DMG installer remains separate issue #14; no Windows, payments, website, or product feature work was started.

## 2026-08-05 - Commercial Block 9 macOS DMG Installer Readiness

- Prepared local DMG installer readiness without signed/notarized public distribution.
- Added `scripts/build_macos_dmg.py` to stage the app with an `/Applications` symlink, create a UDZO DMG, verify it with `hdiutil`, and write a SHA-256 checksum.
- Built local unsigned proof DMG at `build/macos/dmg/Universal Media Extractor.dmg`.
- Created proof report under `proof/commercial_block_9_macos_dmg_readiness/`.
- Added install/uninstall/checksum/release-flow docs in `docs/COMMERCIAL_BLOCK_9_MACOS_DMG_INSTALLER_READINESS.md`.
- Issue #14 remains open because public acceptance requires the DMG to contain a signed/notarized app, which depends on issue #13 Apple Developer ID readiness.

## 2026-08-05 - Commercial Block 10 macOS Public Release Prep

- Added the public macOS release checklist.
- Added the Apple Developer account setup guide with required user-provided data and secret-handling boundaries.
- Added signed/notarized app and DMG validation checklist.
- Added signing/notarization/Gatekeeper troubleshooting guide.
- Added `scripts/notarize_macos_dmg.py` for later DMG notarization command execution.
- Issues #13 and #14 remain open because final acceptance is blocked by Apple Developer ID credentials and real notarization validation.

## 2026-08-05 - Commercial Block 11 Founder Launch Surface

- Added `site/` static public landing page with macOS/Windows beta sections, limitations, legal/support links, and plan summaries.
- Added `docs/FOUNDER_LAUNCH_SITE_COPY.md`.
- Added `docs/BETA_ONBOARDING_COPY.md`.
- Added `docs/PRICING_AND_PLANS.md`.
- Added `docs/SUPPORT_PAGE_DRAFT.md`.
- Added `tests/test_founder_launch_site.py` for public site/copy regression coverage.
- Kept payments, checkout, license activation, Apple signing, Windows build, batch, AI summary, and new downloader features out of scope.
