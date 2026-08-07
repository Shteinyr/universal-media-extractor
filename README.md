# Universal Media Extractor & Transcriber

Status: Commercial strategy imported; Blocks 1-11, Udemy Course Offline Export, Commercial Foundation, Commercial Blocks 2-14, Public Beta QA Round, Public Beta UI / UX Finalization Implementation, Public Beta UI/UX Refactor Block 1, Durable Queue/Library finalization, Native filesystem integration, Unified progress/cancel/retry/recovery, Error diagnostics final pass, Result/transcription UX final pass, and Commercial desktop readiness final pass are completed or prepared as far as possible without external Apple/payment provider access.

This project is evaluating whether a local web app can accept a URL or local audio/video file, analyze available media variants, extract or download selected outputs, transcribe audio locally, and save structured results without paid APIs or cloud services.

Current app status: local-only FastAPI backend with compact public-beta static downloader/file-manager UI, New task composer, URL analysis, preset-based output selection, selected-output download, internal/experimental Udemy course analyze/download mode, local file metadata analysis, desktop-native file/folder picking, Whisper transcription for downloaded/local files, SQLite-backed persistent job history and batch queue snapshots, normalized job stages/progress modes, normalized public-beta error categories, redacted local diagnostics bundles, honest determinate/indeterminate progress display, output templates with duplicate handling, reveal-in-Finder output action, job polling/cancel for download/transcription, practical `yt-dlp` progress parsing, active subprocess cancellation attempts with safe temp cleanup, secondary Library with separate Queue and Files sections, compact public-beta Settings, system light/dark appearance support, local session-token security, strict local origin checks, upload size limits, browser smoke screenshots, desktop wrapper launcher, macOS production `.app` build foundation, macOS signing/notarization readiness docs/scripts, DMG readiness docs/scripts, founder launch static site, beta onboarding copy, draft pricing/plans, payment provider pre-approval package, licensing model draft, user-facing saved result cards with filename/container/size/location, selected-format transcript copy actions, and structured output folders. Public product mode hides Course/Udemy surfaces and does not register Course endpoints. Chrome extension, final signed/notarized public `.app`, automatic app updater, atomic media-engine updater, Windows installer, checkout, license activation/enforcement, auth, stored credentials, online service behavior, external queue, Archive Pack execution, and AI summary are not implemented.

The visible UI has been finalized toward public beta: the sidebar focuses on source mode and input, output presets are user-facing, download options appear only after selecting an output, advanced save controls are collapsed, and Recent results live in a secondary Library surface.

Roadmap note: new work is now organized by larger blocks, not new Phase numbers, unless the user explicitly authorizes new Phase numbering.

Roadmap v2 is recorded in `docs/ROADMAP_V2.md`. Blocks 1-11 are completed. A GPT Pro commercialization strategy is saved in `docs/UNIVERSAL_MEDIA_EXTRACTOR_PRODUCT_STRATEGY.md`, with execution notes in `docs/COMMERCIALIZATION_EXECUTION_PLAN.md` and GitHub issue drafts in `docs/GITHUB_COMMERCIAL_BACKLOG.md`.

Commercial direction: move toward a paid local desktop utility for macOS and Windows. The recommended public positioning is “Local Media Downloader & Organizer,” not “universal downloader for every site.” Udemy Course mode should stay internal/experimental unless separately approved for public release.

GitHub commercial roadmap board: [https://github.com/users/Shteinyr/projects/7](https://github.com/users/Shteinyr/projects/7).

UI/UX research before Public Beta UI / UX Finalization:

- `docs/UI_UX_COMPETITOR_VISUAL_AUDIT.md`
- `docs/UI_UX_PRODUCT_FUNCTION_INVENTORY.md`
- `docs/UI_UX_REFERENCE_SCREEN_MAP.md`
- `docs/UI_UX_GPT_PRO_BRIEF.md`
- `docs/UI_UX_GPT_PRO_CONTEXT_PACK.md`
- `docs/UI_UX_COMPETITOR_VISUAL_LOGIC_PACK.md`
- `docs/UI_UX_OUR_APP_VISUAL_LOGIC_PACK.md`
- `docs/UI_UX_GPT_PRO_ANALYSIS_PROMPT.md`
- screenshots/proof: `proof/ui_ux_gpt_pro_pack/`
- `docs/UNIVERSAL_MEDIA_EXTRACTOR_FINAL_UI_UX_COMMERCIAL_SPEC.md`
- `docs/FINAL_UI_UX_IMPLEMENTATION_PLAN.md`
- `docs/PUBLIC_BETA_UI_UX_FINALIZATION_BLUEPRINT.md`
- `docs/PUBLIC_BETA_UI_UX_FINALIZATION_IMPLEMENTATION.md`

These files preserve the GPT Pro competitor list, add supplemental visual references, map current product functions, package competitor/app screenshots and product logic for GPT Pro, and define the final public beta UI/UX blueprint for the next implementation block.

GPT Pro final UI/UX tracking:

- GitHub tracker: [#41 Final public beta UX refactor tracker](https://github.com/Shteinyr/universal-media-extractor/issues/41)
- Public Beta UI/UX Refactor Block 1: #42, #43, #44, #45 completed.
- Docs: `docs/PUBLIC_BETA_UI_UX_REFACTOR_BLOCK_1.md`, `docs/PUBLIC_BETA_BACKEND_SOURCE_OF_TRUTH.md`.
- Durable Queue/Library finalization: #46 completed.
- Doc: `docs/PUBLIC_BETA_DURABLE_QUEUE_LIBRARY.md`.
- Native filesystem integration: #47 completed.
- Doc: `docs/PUBLIC_BETA_NATIVE_FILESYSTEM_INTEGRATION.md`.
- Unified progress, cancel, retry, recovery: #48 completed.
- Doc: `docs/PUBLIC_BETA_PROGRESS_CANCEL_RETRY_RECOVERY.md`.
- Error normalization and diagnostics final pass: #49 completed.
- Doc: `docs/PUBLIC_BETA_ERROR_DIAGNOSTICS_FINAL_PASS.md`.
- Result and local transcription UX final pass: #50 completed.
- Doc: `docs/PUBLIC_BETA_RESULT_TRANSCRIPTION_UX_FINAL_PASS.md`.
- Commercial desktop readiness final pass: #51 completed.
- Docs: `docs/PUBLIC_BETA_COMMERCIAL_DESKTOP_READINESS.md`, `docs/APP_AND_MEDIA_ENGINE_UPDATE_PLAN.md`, `docs/WINDOWS_PRODUCTION_BUILD_PATH.md`.

Commercial foundation docs:

- `docs/PUBLIC_PRODUCT_BOUNDARY.md`
- `docs/LEGAL_SAFE_PRODUCT_COPY.md`
- `docs/EULA_DRAFT.md`
- `docs/PRIVACY_POLICY_DRAFT.md`
- `docs/REFUND_POLICY_DRAFT.md`
- `docs/PUBLIC_KNOWN_LIMITATIONS.md`
- `docs/COMMERCIAL_BLOCK_2_ERRORS_DIAGNOSTICS.md`
- `docs/COMMERCIAL_BLOCK_3_PRESET_OUTPUT_SELECTION.md`
- `docs/COMMERCIAL_BLOCK_4_LOCALHOST_SECURITY.md`
- `docs/COMMERCIAL_BLOCK_5_SQLITE_JOBS_HISTORY.md`
- `docs/COMMERCIAL_BLOCK_6_OUTPUT_TEMPLATES_DUPLICATES.md`
- `docs/COMMERCIAL_BLOCK_7_MACOS_PRODUCTION_BUILD_FOUNDATION.md`
- `docs/COMMERCIAL_BLOCK_8_MACOS_SIGNING_NOTARIZATION_READINESS.md`
- `docs/COMMERCIAL_BLOCK_9_MACOS_DMG_INSTALLER_READINESS.md`
- `docs/COMMERCIAL_BLOCK_10_MACOS_PUBLIC_RELEASE_PREP.md`
- `docs/MACOS_PUBLIC_RELEASE_CHECKLIST.md`
- `docs/APPLE_DEVELOPER_ACCOUNT_SETUP.md`
- `docs/MACOS_RELEASE_VALIDATION_CHECKLIST.md`
- `docs/MACOS_SIGNING_NOTARIZATION_TROUBLESHOOTING.md`
- `docs/COMMERCIAL_BLOCK_11_FOUNDER_LAUNCH_SURFACE.md`
- `docs/FOUNDER_LAUNCH_SITE_COPY.md`
- `docs/BETA_ONBOARDING_COPY.md`
- `docs/PRICING_AND_PLANS.md`
- `docs/SUPPORT_PAGE_DRAFT.md`
- `docs/COMMERCIAL_BLOCK_12_PAYMENT_LICENSING_PREP.md`
- `docs/LEMON_SQUEEZY_PREAPPROVAL_REQUEST.md`
- `docs/STRIPE_FALLBACK_RISK_REVIEW.md`
- `docs/LICENSING_MODEL_DRAFT.md`
- `docs/PAYMENT_LICENSING_USER_DECISIONS.md`

- `docs/COMMERCIAL_BLOCK_13_BATCH_QUEUE_FOUNDATION.md`
- `docs/COMMERCIAL_BLOCK_14_PUBLIC_BETA_UI_READINESS.md`
- `docs/PUBLIC_BETA_SECURITY_DIAGNOSTICS_QA_REVIEW.md`
- `docs/BETA_WEBSITE_DOWNLOAD_FLOW.md`
- `docs/PUBLIC_BETA_QA_ROUND.md`

Public commercial builds should set `UME_PUBLIC_PRODUCT_MODE=1`. In that mode, internal/experimental Course Mode is hidden from the static UI by default.

Commercial Block 2 adds public-beta error and diagnostics foundations. Failed jobs can be inspected locally through:

```text
GET /diagnostics/jobs/{job_id}
```

Diagnostics are redacted by default: no cookies, tokens, transcripts, full URLs, or local paths. Failed background jobs can expose a local `Copy diagnostics` support action. Details are documented in `docs/COMMERCIAL_BLOCK_2_ERRORS_DIAGNOSTICS.md`.


Commercial Block 4 adds localhost API hardening. The static UI receives a random in-memory session token from `/config` and sends it through `X-UME-Session-Token` for protected API calls. `/config` and diagnostics responses are marked `Cache-Control: no-store`. The API rejects non-local origins/hosts, uses a strict CORS allowlist, and caps local uploads. Details are documented in `docs/COMMERCIAL_BLOCK_4_LOCALHOST_SECURITY.md`.

Commercial Block 5 adds SQLite-backed persistent jobs and local job history. Jobs now survive restart, interrupted active jobs recover to a clear failed state, failed jobs can be retried, and terminal history can be cleared without deleting downloaded files. Details are documented in `docs/COMMERCIAL_BLOCK_5_SQLITE_JOBS_HISTORY.md`.

Commercial Block 6 adds output templates, duplicate handling, cross-platform-safe naming, and reveal-in-Finder/Explorer for managed output folders. Details are documented in `docs/COMMERCIAL_BLOCK_6_OUTPUT_TEMPLATES_DUPLICATES.md`.

Durable project context is recorded in `PROJECT_CONTEXT.md`. Read it before large tasks and update it after completed large blocks.

## Quick Start

From the project directory:

```bash
cd "/Users/aleksandr/Developer/Codex/Projects/Universal Media Extractor"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Required local CLIs:

```bash
ffmpeg -version
yt-dlp --version
whisper --help
```

Run tests:

```bash
.venv/bin/python -m pytest -q
```

Start the local app:

```bash
.venv/bin/python scripts/run_api.py
```

Open:

```text
http://127.0.0.1:8000/
```

## Desktop Mode

Run the desktop wrapper:

```bash
.venv/bin/python scripts/run_desktop.py
```

The wrapper starts the same FastAPI app on `127.0.0.1` and opens the existing UI in a desktop window. If port `8000` is busy, it chooses the next free local port through `8020`.

Desktop mode can use native file/folder pickers. `Choose file` selects a local media file without copying it just to analyze metadata, and `Choose` near `Save to` selects the output folder. Browser mode still uses browser upload and typed save paths.

Development smoke helper:

```bash
.venv/bin/python scripts/run_desktop.py --smoke-seconds 3
```

This opens the desktop window briefly and closes it automatically.

## Development App Bundle

Build a local development `.app` launcher:

```bash
.venv/bin/python scripts/build_dev_app.py
```

Run it:

```bash
open "build/dev/Universal Media Extractor Dev.app"
```

This `.app` does not bundle the project. It points back to this working tree and runs:

```bash
.venv/bin/python scripts/run_desktop.py
```

So code changes are picked up the next time the `.app` starts, as long as the project path and `.venv` stay in place.

For convenient Finder use, copy it to Applications:

```bash
rm -rf "/Applications/Universal Media Extractor Dev.app"
cp -R "build/dev/Universal Media Extractor Dev.app" "/Applications/Universal Media Extractor Dev.app"
```

## macOS Public Release Prep

Production foundation commands:

```bash
.venv/bin/python scripts/build_macos_app.py
.venv/bin/python scripts/check_macos_signing_readiness.py
.venv/bin/python scripts/build_macos_dmg.py
```

Public release signing/notarization is prepared but not complete. It needs an active Apple Developer Program account, a `Developer ID Application` certificate, and notary credentials stored in the macOS Keychain.

Start here:

- `docs/MACOS_PUBLIC_RELEASE_CHECKLIST.md`
- `docs/APPLE_DEVELOPER_ACCOUNT_SETUP.md`
- `docs/MACOS_RELEASE_VALIDATION_CHECKLIST.md`
- `docs/MACOS_SIGNING_NOTARIZATION_TROUBLESHOOTING.md`

Do not ship the unsigned local DMG as a public release.

## Commercial Desktop Readiness

The final public-beta desktop readiness pass is documented in:

```text
docs/PUBLIC_BETA_COMMERCIAL_DESKTOP_READINESS.md
```

Related release-path docs:

- `docs/APP_AND_MEDIA_ENGINE_UPDATE_PLAN.md`
- `docs/WINDOWS_PRODUCTION_BUILD_PATH.md`

Desktop readiness smoke:

```bash
.venv/bin/python scripts/browser_smoke.py \
  --proof-dir proof/commercial_desktop_readiness_final_pass \
  --desktop-readiness
```

This verifies the UI keyboard path, system light theme rendering, high-DPI screenshot, Settings access, and narrow-window overflow. It does not download or transcribe unless `--full-flow` is also passed.

## Public Beta QA Round

The current public beta QA pass is documented in:

```text
docs/PUBLIC_BETA_QA_ROUND.md
```

It verifies browser launch, URL analyze/download/transcribe, local synthetic file analyze/transcribe, one-item batch download, diagnostics redaction, output safe delete, public mode Course hiding, JS syntax, pytest, and browser smoke proof. Proof artifacts are under `proof/public_beta_qa_round/`.

## Beta Website / Download Flow

The public beta website/download flow is documented in:

```text
docs/BETA_WEBSITE_DOWNLOAD_FLOW.md
```

Current public beta packaging stance: use `Join the beta` / early-access CTAs until signed macOS and Windows installers exist. Public copy must stay local-first, limitations-aware, and must not advertise internal/experimental Course Mode. No checkout or license activation is live.

## Founder Launch Static Site

A first public-facing static site draft lives in:

```text
site/index.html
```

Preview locally:

```bash
python3 -m http.server 8767 --directory site
```

Open:

```text
http://127.0.0.1:8767/
```

The site includes the public positioning, macOS/Windows beta sections, visible limitations, support/legal links, and draft Free / Founder Pro / Pro / Business plans. It does not include payment checkout or license activation.

## Payment And Licensing Prep

Commercial Block 12 prepared the payment-provider and licensing documents without integrating checkout or license enforcement:

- `docs/LEMON_SQUEEZY_PREAPPROVAL_REQUEST.md`
- `docs/STRIPE_FALLBACK_RISK_REVIEW.md`
- `docs/LICENSING_MODEL_DRAFT.md`
- `docs/PAYMENT_LICENSING_USER_DECISIONS.md`

- `docs/COMMERCIAL_BLOCK_13_BATCH_QUEUE_FOUNDATION.md`
- `docs/COMMERCIAL_BLOCK_14_PUBLIC_BETA_UI_READINESS.md`
- `docs/PUBLIC_BETA_SECURITY_DIAGNOSTICS_QA_REVIEW.md`

Current decision: request Lemon Squeezy pre-approval first, keep Stripe as fallback, and do not implement checkout/webhooks/license activation until provider approval and user business details are ready.

## Batch Queue

Batch mode can import multiple URLs from textarea, clipboard, or a `.txt` file. It supports controlled concurrency, playlist item selection through safe flat playlist analysis, and retry failed items. Batch downloads use the same local `DownloadService` and persisted child jobs as single URL downloads.

Archive Pack is still planned/disabled; it is not part of the current executable batch flow.

## Browser Smoke Test

Browser verification uses Python Playwright in the project `.venv`.

Install browser binaries after installing requirements:

```bash
.venv/bin/python -m playwright install chromium
```

Run the backend:

```bash
.venv/bin/python scripts/run_api.py
```

In another terminal, run the analysis-only browser smoke:

```bash
.venv/bin/python scripts/browser_smoke.py
```

The default smoke opens the local UI, analyzes `https://youtu.be/UUdxAp3kuKA`, verifies `Showreel` and output presets, and saves:

```text
proof/block_10/ui_initial.png
proof/block_10/ui_analyze_result.png
```

Optional full-flow browser smoke exists behind an explicit flag:

```bash
.venv/bin/python scripts/browser_smoke.py --full-flow
```

The default smoke does not download or transcribe.

## MVP Flow

URL flow:

1. Paste a public media URL.
2. Click `Analyze`.
3. Select an output preset.
4. Click `Download selected` and watch the download job status.
5. If the downloaded output contains audio, choose a Whisper model and transcript format.
6. Click `Transcribe` and watch the transcription job status.
7. Review the saved transcript and copy transcript or output path.

Local file flow:

1. Switch to `Local file mode`.
2. Choose a local audio/video file.
3. Click `Analyze local file`.
4. Choose a Whisper model and transcript format.
5. Click `Transcribe local file`.
6. Review the saved transcript and copy transcript or output path.

Recent results:

- user outputs under `outputs/` are listed in the UI;
- each item can copy its path;
- each item can be safely deleted by output id;
- `proof/` is not listed and is not deleted automatically.

Outputs are written under:

```text
~/Downloads/Universal Media Extractor/<safe_source_title>/
outputs/local_<timestamp>_<safe_filename>/
```

## Udemy Course Mode

Course mode is a local, best-effort export path for Udemy courses you can access in your own account.

Use it from the UI:

1. Choose `Course mode`.
2. Paste a Udemy URL. Prefer the URL from the opened course player, for example `/course/<slug>/learn/lecture/<id>`.
3. Keep `Login source` set to `Chrome session`.
4. Make sure Udemy is open in Chrome and you are signed in.
5. Click `Analyze course`.
6. Choose quality/container and click `Download course`.

Default output:

```text
~/Downloads/Universal Media Extractor/Udemy
```

The app does not store Udemy passwords, does not copy cookies into output folders, and does not bypass DRM/CAPTCHA/paywalls. If Chrome session access is unavailable, Course mode has an advanced `Manual cookies.txt` fallback. Some courses or lectures may be unavailable because of Udemy restrictions, expired cookies, DRM, or extractor changes.

If a clean `/course/<slug>/` URL fails, paste the URL from the opened lecture/player page instead. On the tested course, the clean course URL failed with `Unable to extract course id`, while the lecture URL returned the full course playlist.

The URL download card includes a `Save to` field. Change it before clicking `Download selected` if you want another output base folder. URL downloads put the selected media/subtitle file directly inside the result folder. Service artifacts are stored in hidden `.metadata` and `.logs` folders.

After a download starts with a custom `Save to` folder, `Recent results` uses that folder for listing outputs.

The download card also includes a `Format` selector:

- Video: `MP4` default, `MKV`, `WEBM`;
- Audio: `M4A` default, `MP3`, `WAV`;
- Subtitles: `SRT` default, `VTT`.

When `Video` is selected, the app asks `yt-dlp` to combine the selected video stream with the best available audio stream into one final file.

Transcription saves one selected format per run:

- `TXT` default;
- `Markdown`;
- `JSON`.

The selected transcript file is written directly into the same result folder as the downloaded media. Whisper's intermediate files and logs are kept in hidden service folders.

When proof runs specify a custom output base, outputs are written under that proof directory instead.

## Preset-Based Output Selection

After URL analysis, the public UI shows simple output presets instead of raw technical streams:

- `Best Video`
- `1080p`
- `Smaller Video`
- `Audio M4A`
- `Audio MP3`
- `Subtitles`
- `Archive Pack`

Technical `yt-dlp` stream ids, codec strings, fps details, and duplicate stream rows are hidden from the main UI. The app still keeps the selected internal `format_id` behind the scenes so `/download` can use the existing working backend path.

Unavailable presets are shown as disabled with a short reason. `Archive Pack` is present as a planned disabled preset because real multi-output archive behavior belongs to later queue/batch/history work.

Advanced stream details remain available behind the `Advanced details` disclosure for diagnostics and support.

## UI Reference Port

The downloaded v0 UI project was used only as a visual/UX reference. The main app still uses static HTML/CSS/vanilla JS served by FastAPI.

Transferred UI ideas:

- compact sidebar layout;
- downloader/file-manager style main work area;
- concise media card;
- segmented output selector;
- compact recent results and result files.

No Next.js, React, Tailwind build step, shadcn/ui runtime, or Vercel analytics were added to the main project.

## MVP Limitations

- URL support is best-effort through `yt-dlp`.
- DRM, CAPTCHA, paywall, login-only, and private sources are out of scope.
- Udemy Course mode can use the local Chrome session or an advanced manual `cookies.txt` fallback. The app does not store passwords or copy cookies into outputs.
- Local file mode copies selected files into the project output folder.
- Download/transcription run as in-memory local jobs.
- Job progress uses status/current-step polling and parses practical `yt-dlp` percent output when available.
- Whisper progress is step-based; the UI does not fake Whisper percent.
- Cancel is best-effort and attempts to terminate a registered active `yt-dlp`, `ffmpeg`, or Whisper subprocess.
- Whisper quality depends on model and audio quality; `tiny` is fast but can be poor.
- Browser UI cannot open local folders directly; it shows/copies paths.
- Output delete is limited to direct folders inside `outputs/`.
- `proof/` is a development proof area and is not managed by the UI.
- Desktop wrapper and development `.app` launcher exist for local use, but there is no packaged/signed/notarized distributable `.app` or installer.
- No Chrome extension, auth, database, batch processing, online service, or AI summary API.

See `docs/MVP_KNOWN_LIMITATIONS.md` for the full limitations list.

## Phase 0 Verdict

CONDITIONAL GO.

The core idea is technically feasible as a local, single-user, best-effort extractor/transcriber using `yt-dlp`, `ffmpeg`, and local Whisper CLI. It is not feasible as a guaranteed universal downloader for every website.

Further work remains block-gated: continue only when the user explicitly authorizes the next roadmap block.

Roadmap governance:

- do not create new Phase numbering;
- do not create new Blocks without explicit user approval;
- Codex recommendations are recommendations only, not roadmap decisions;
- follow Roadmap v2 unless the user explicitly changes it.

## Phase 1 Status

The user accepted the CONDITIONAL GO constraints. Phase 1 prepared a local Python virtual environment and verified minimal CLI/tool availability.

- Virtual environment: `.venv`
- Direct dependencies: FastAPI, Uvicorn standard extras, Pydantic, python-multipart, aiofiles
- CLI proof checks: `ffmpeg`, `ffprobe`, `yt-dlp`, and Whisper CLI are available

URL format listing was not tested because no user-provided test URL was supplied.

## Phase 2 Status

The user provided and confirmed ownership of `https://youtu.be/UUdxAp3kuKA`. Phase 2 safely analyzed the URL with `yt-dlp` without downloading media.

Results:

- Source recognized by `yt-dlp` as YouTube.
- Title: `Showreel`
- Duration: 39 seconds
- Formats found: audio-only, video-only, and combined video+audio.
- Subtitles: none.
- Automatic captions: none.

Raw proof outputs are stored in `proof/phase_2/`. Phase 2 did not create application code.

## Phase 3 Status

Phase 3 defined a normalized future `AnalyzeResult` contract for the analyze endpoint and UI. It is based on the real Phase 2 `yt-dlp` output and includes source summary, grouped media options, subtitles, automatic captions, metadata, warnings, errors, and legal/safety confirmation state.

Created documentation:

- `docs/PHASE_3_ANALYZE_DATA_CONTRACT.md`
- `docs/PHASE_3_SAMPLE_ANALYZE_RESULT.json`
- `docs/PHASE_3_BACKEND_MODEL_NOTES.md`
- `docs/PHASE_3_FRONTEND_MODEL_NOTES.md`

No application code has been created yet.

## Phase 4 Status

Phase 4 created Pydantic v2 models for the normalized analyze-result contract and tests that validate the Phase 3 sample JSON.

Created code:

- `src/universal_media_extractor/models/analyze.py`
- `tests/test_analyze_models.py`

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 5 passed.

No FastAPI app, routes, frontend, downloader, transcription module, media download, Whisper run, extension, or desktop wrapper has been created.

## Phase 9 Status

Phase 9 created a minimal service layer without FastAPI routes or frontend code.

Created code:

- `src/universal_media_extractor/services/analyze_service.py`
- `src/universal_media_extractor/services/output_manager.py`
- `src/universal_media_extractor/services/safety_service.py`
- `src/universal_media_extractor/services/job_service.py`
- `src/universal_media_extractor/models/job.py`

Created tests:

- `tests/test_analyze_service.py`
- `tests/test_output_manager.py`
- `tests/test_safety_service.py`
- `tests/test_job_service.py`

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 26 passed.

No FastAPI app, routes, frontend, downloader, transcription module, media download, Whisper run, MVP, extension, desktop wrapper, database, or persistent job storage has been created.

## Phase 10 Status

Phase 10 created a minimal analysis-only FastAPI backend with local-only Uvicorn binding.

Created code:

- `src/universal_media_extractor/api/app.py`
- `src/universal_media_extractor/api/schemas.py`
- `scripts/run_api.py`

Implemented endpoints:

- `GET /health`
- `POST /analyze`
- `GET /jobs/{job_id}`

Run locally:

```bash
.venv/bin/python scripts/run_api.py --port 8000
```

The run script binds to `127.0.0.1` only.

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 31 passed.

Runtime health check was verified at `http://127.0.0.1:8765/health`.

No frontend, downloader, media download, Whisper run, Chrome extension, desktop wrapper, online service, auth, database, or cookies/login has been created.

## Phase 11 Status

Phase 11 manually verified the real local API endpoint `POST /analyze` on the user-authorized URL `https://youtu.be/UUdxAp3kuKA`.

Proof summary:

- backend ran on `http://127.0.0.1:8000`;
- `GET /health` returned local-only status;
- `POST /analyze` returned normalized `AnalyzeResult`;
- job status: `succeeded`;
- title: `Showreel`;
- duration: 39 seconds;
- extractor: `youtube`;
- errors: none;
- media options: 3 audio-only, 4 video-only, 5 combined;
- subtitles and automatic captions: none.

Proof artifacts:

- `proof/phase_11/health_response.json`
- `proof/phase_11/analyze_response.json`
- `proof/phase_11/analyze_response_pretty.json`
- `proof/phase_11/job_response.json`
- `proof/phase_11/job_response_pretty.json`
- `docs/PHASE_11_MANUAL_API_ANALYZE_PROOF.md`

No frontend, downloader, media download, Whisper run, extension, desktop wrapper, auth, database, or cookies/login was created or used.

## Phase 12 Status

Phase 12 planned the first frontend as an analysis-result display only UI based on the real Phase 11 API response.

Planned UI loop:

```text
Paste URL -> Analyze -> Display normalized AnalyzeResult
```

Recommended first frontend approach:

- static HTML/CSS/vanilla JS;
- connect to `POST http://127.0.0.1:8000/analyze`;
- show source summary, thumbnail, output presets, warnings, errors, and empty subtitle/caption states;
- no Vite app yet.

Created documentation:

- `docs/PHASE_12_FRONTEND_ANALYSIS_UI_PLAN.md`
- `docs/PHASE_12_UI_COMPONENT_MAP.md`
- `docs/PHASE_12_FRONTEND_SCOPE_BOUNDARY.md`

No frontend app, UI code, downloader, media download, Whisper run, extension, desktop wrapper, auth, database, cookies/login, or API changes were created.

## Phase 13 Status

Phase 13 created the first static analysis-only UI.

Open locally:

```bash
.venv/bin/python scripts/run_api.py
```

Then open:

```text
http://127.0.0.1:8000/
```

Created UI files:

- `src/universal_media_extractor/static/index.html`
- `src/universal_media_extractor/static/styles.css`
- `src/universal_media_extractor/static/app.js`

Implemented UI loop:

```text
Paste URL -> Analyze -> Display normalized AnalyzeResult
```

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 33 passed.

Live checks confirmed `/`, `/static/app.js`, and `POST /analyze` work on `127.0.0.1:8000`.

No download, Whisper/transcription, local file upload, extension, desktop wrapper, auth, database, cookies/login, settings page, React, Vite, CDN, or external asset bundle was added.

## Phase 14 Status

Phase 14 polished the existing static analysis-only UI without adding new features.

Improved:

- visual hierarchy and spacing;
- compact preset display;
- warning/error separation;
- keyboard focus styles;
- URL input accessibility;
- status/error aria roles;
- loading `aria-busy`;
- reduced-motion support;
- empty thumbnail state;
- narrow layout behavior.

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 33 passed.

Live checks confirmed `/`, `/static/styles.css`, `/static/app.js`, and real `POST /analyze` still work on `127.0.0.1:8000`.

Documentation:

- `docs/PHASE_14_UI_POLISH_ACCESSIBILITY.md`

At the time of Phase 14, Browser/Playwright screenshot verification was not performed because browser automation was unavailable in the local toolchain. Block 10 later added Playwright browser smoke tooling.

No download, Whisper/transcription, local file upload, extension, desktop wrapper, auth, database, cookies/login, settings page, React, Vite, CDN, external assets, or backend API changes were added.

## Phase 15 Status

Phase 15 refined analysis-only error handling without adding new product features.

Covered states:

- empty URL;
- invalid URL;
- API unavailable;
- API validation/error response;
- `AnalyzeResult.errors`;
- unsupported source;
- login required;
- cookies required;
- analyzer failure;
- subtitle/caption empty states as non-errors.

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 36 passed.

Live checks confirmed `/`, `/static/app.js`, invalid URL `422`, and real `POST /analyze` still work on `127.0.0.1:8000`.

Documentation:

- `docs/PHASE_15_ERROR_STATE_REFINEMENT.md`

No download, Whisper/transcription, local file upload, extension, desktop wrapper, auth, database, cookies/login, settings page, React, Vite, CDN, external assets, or media processing was added.

## Block 2 Download + Output Pipeline

Block 2 added selected-format downloads through the existing local-only app.

Implemented:

- `DownloadRequest`, `DownloadResult`, `DownloadMode`, and `DownloadStatus`;
- `DownloadService.download_media(...)`;
- `POST /download`;
- structured output folders with `media/`, `metadata/`, and `logs/`;
- static UI selection of an output preset;
- rights confirmation checkbox before download;
- download result display with output paths and files.

Run locally:

```bash
.venv/bin/python scripts/run_api.py
```

Then open:

```text
http://127.0.0.1:8000/
```

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 43 passed.

Manual proof:

- source: `https://youtu.be/UUdxAp3kuKA`;
- format: `140`;
- mode: audio-only;
- output: `proof/download_block/20260529T092713Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a`.

No Whisper/transcription, local file upload, extension, desktop wrapper, auth, database, cookies/login, online service behavior, or AI summary was added.

## Block 3 Whisper + Transcript Pipeline

Block 3 added local transcription for downloaded audio/video files.

Implemented:

- `TranscriptionRequest`, `TranscriptionResult`, `SourceMediaKind`, and `TranscriptionStatus`;
- `TranscriptionService.transcribe_file(...)`;
- `POST /transcribe`;
- audio -> Whisper CLI -> transcript artifacts;
- video -> ffmpeg extracted audio -> Whisper CLI -> transcript artifacts;
- `transcript.txt`;
- `transcript.md`;
- `transcript.json`;
- `summary_prompt.md`;
- UI transcript panel after successful download.

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 49 passed.

Manual proof:

- input: `proof/download_block/20260529T092713Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a`;
- Whisper model: `tiny`;
- output:
  - `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/transcript.txt`;
  - `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/transcript.md`;
  - `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/transcript.json`;
  - `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/summary_prompt.md`.

No AI summary API, Chrome extension, desktop wrapper, batch processing, cookies/login, auth, database, online service behavior, or advanced download hardening was added.

## Block 4 Processing UI + MVP Flow

Block 4 unified the static UI into the end-to-end MVP flow:

```text
Analyze -> Select preset -> Download -> Transcribe -> Result
```

Implemented:

- visible MVP flow tracker;
- clearer selected output summary;
- disabled download until an output is selected;
- Whisper model selector: `tiny`, `base`, `small`, `medium`, `turbo/default`;
- transcription action after successful download;
- generated-files card;
- transcript preview;
- `Copy text`;
- `Copy prompt`;
- `Copy folder path`.

The UI reuses existing endpoints:

- `POST /analyze`;
- `POST /download`;
- `POST /transcribe`.

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 49 passed.

Manual proof artifacts:

- `proof/block_4/analyze_response_pretty.json`;
- `proof/block_4/download_response_pretty.json`;
- `proof/block_4/transcribe_response_pretty.json`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/transcripts/transcript.txt`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/transcripts/transcript.md`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/transcripts/transcript.json`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/transcripts/summary_prompt.md`.

At the time of Block 4, visual browser automation was unavailable because the local `playwright` module was not found. Block 10 later added Playwright browser smoke tooling.

No job/progress/cancel, batch, Chrome extension, desktop wrapper, AI summary API, auth/database/cookies, React/Vite, CDN assets, advanced download hardening, or roadmap changes were added.

## Block 5 MVP Integration / Readiness Review

Block 5 reviewed the current MVP as a product checkpoint.

Verified flow:

```text
URL -> Analyze -> Select preset -> Download -> Transcribe -> Result
```

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 49 passed.

Manual smoke test:

- source: `https://youtu.be/UUdxAp3kuKA`;
- selected output: audio-only `140`;
- Whisper model: `tiny`;
- output: `proof/block_5/20260530T132548Z_UUdxAp3kuKA/`.

Readiness docs:

- `docs/BLOCK_5_MVP_READINESS_REVIEW.md`;
- `docs/MVP_KNOWN_LIMITATIONS.md`.

Only text/readiness fixes were made. No new product features were added.

## Phase 5 Status

Phase 5 created a pure normalizer for successful `yt-dlp --dump-json` data.

Created code:

- `src/universal_media_extractor/normalizers/ytdlp.py`
- `tests/test_ytdlp_normalizer.py`

The normalizer converts an already-loaded raw `yt-dlp` dictionary into `AnalyzeResult`, grouping formats into audio-only, video-only, and combined video+audio options.

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 11 passed.

No CLI orchestration, FastAPI app, routes, frontend, downloader, transcription module, media download, Whisper run, extension, or desktop wrapper has been created.

## Phase 6 Status

Phase 6 created a safe URL analysis wrapper around `yt-dlp --simulate --dump-json`.

Created code:

- `src/universal_media_extractor/analyzers/ytdlp.py`
- `tests/test_ytdlp_analyzer.py`
- `scripts/manual_analyze_url.py`

The analyzer:

- uses subprocess list arguments with `shell=False`;
- uses only `yt-dlp --simulate --dump-json URL`;
- handles timeout, invalid JSON, non-zero exits, missing `yt-dlp`, and common source/access errors;
- returns `AnalyzeResult`;
- saves raw JSON only when `raw_output_dir` is provided.

Verification:

```bash
.venv/bin/python -m pytest -q
```

Result: 18 passed.

The manual script was created but not run during Phase 6. No FastAPI app, routes, frontend, downloader, media download, Whisper run, extension, or desktop wrapper has been created.

## Phase 7 Status

Phase 7 ran the manual analysis script on the user-authorized URL `https://youtu.be/UUdxAp3kuKA`.

Result:

- analysis succeeded;
- normalized `AnalyzeResult` returned with `errors=[]`;
- raw analysis JSON saved to `proof/phase_7/`;
- no media download was performed;
- Whisper was not run.

No FastAPI app, routes, frontend, downloader, extension, or desktop wrapper has been created.

## Phase 8 Status

Phase 8 documented the future service layer and first MVP boundary without creating backend routes or frontend code.

Created documentation:

- `docs/PHASE_8_SERVICE_LAYER_PLAN.md`
- `docs/PHASE_8_API_DRAFT.md`
- `docs/PHASE_8_FRONTEND_FLOW_DRAFT.md`
- `docs/PHASE_8_MVP_BOUNDARY.md`

Planned first MVP services:

- `AnalyzeService`
- minimal `OutputManager`
- minimal `JobService`
- minimal `SafetyService`

First MVP boundary:

- URL analysis;
- normalized `AnalyzeResult`;
- UI display of analyze result;
- no download in the first UI prototype;
- no Whisper in the first UI prototype.

No FastAPI app, routes, frontend, downloader, transcription module, media download, Whisper run, extension, or desktop wrapper has been created.

## macOS Production-Foundation App Build

Build the local macOS `.app` bundle:

```bash
.venv/bin/python -m pip install -r requirements-packaging.txt
.venv/bin/python scripts/build_macos_app.py
open "build/macos/dist/Universal Media Extractor.app"
```

This bundle is for local production-foundation testing. Public distribution still requires Developer ID signing, notarization, and a DMG/installer.

Docs: `docs/COMMERCIAL_BLOCK_7_MACOS_PRODUCTION_BUILD_FOUNDATION.md`.

## macOS Signing / Notarization Readiness

Check local readiness:

```bash
.venv/bin/python scripts/check_macos_signing_readiness.py
```

Prepare notarytool credentials in Keychain, after Apple Developer account setup:

```bash
.venv/bin/python scripts/store_macos_notary_credentials.py \
  --apple-id "APPLE_ID_EMAIL" \
  --team-id "TEAMID" \
  --profile UME_NOTARY
```

Future signing/notarization flow:

```bash
.venv/bin/python scripts/build_macos_app.py
.venv/bin/python scripts/sign_macos_app.py --identity "Developer ID Application: Company Name (TEAMID)"
.venv/bin/python scripts/notarize_macos_app.py --keychain-profile UME_NOTARY
```

Current blocker: a `Developer ID Application` certificate must be installed in Keychain before real signing/notarization can complete.

Docs: `docs/COMMERCIAL_BLOCK_8_MACOS_SIGNING_NOTARIZATION_READINESS.md`.

## macOS DMG Installer Readiness

Build the app, then create a local DMG proof:

```bash
.venv/bin/python scripts/build_macos_app.py
.venv/bin/python scripts/build_macos_dmg.py
```

Artifacts:

```text
build/macos/dmg/Universal Media Extractor.dmg
build/macos/dmg/Universal Media Extractor.dmg.sha256
```

The current DMG is a local unsigned/unnotarized proof. Public distribution requires the signing/notarization work from issue #13 first.

Docs: `docs/COMMERCIAL_BLOCK_9_MACOS_DMG_INSTALLER_READINESS.md`.
