# Project State

## Goal

Universal Media Extractor & Transcriber is intended to be a local web app with a Python backend and browser UI. It should accept a URL or local audio/video file, analyze available media variants, let the user choose outputs, download or extract media locally, optionally transcribe audio through a local Whisper CLI, and save structured results.

## Current Stage

Blocks 1-11 completed. Roadmap v2 documented. GPT Pro commercial strategy imported. Commercial Foundation issues #1-#5 are completed. Commercial Block 2 issues #6-#7 are completed. Commercial Block 3 issue #9 is completed. Commercial Block 4 issue #8 is completed. Commercial Block 5 issue #10 is completed. Commercial Block 6 issue #11 is completed. Commercial Blocks 7-10 prepared macOS packaging/public release readiness up to the Apple Developer ID blocker. Commercial Block 11 prepared the founder launch surface around issues #19-#21. Commercial Block 12 prepared payment provider pre-approval and licensing model docs for issues #22-#23. Recommended next work remains Public Beta Readiness from the GitHub commercial roadmap, not automatic Chrome Extension work. After Block 12, real checkout/licensing remains gated by provider approval and user business details.

## Already Installed And Reported By User

- Homebrew 5.1.14
- Python 3.14.4 / 3.14.5
- ffmpeg 8.1.1
- yt-dlp 2026.03.17
- openai-whisper 20250625
- `ffmpeg -version` works
- `yt-dlp --version` works
- `whisper --help` works

## Decisions

- Start as a local web app only.
- Consider desktop packaging later.
- Consider Chrome extension integration later.
- Do not use paid APIs at the start.
- Do not build an online service at the start.
- Main local processing path under audit: `yt-dlp` + `ffmpeg` + Whisper CLI.
- Commercial direction: local media downloader and organizer for macOS and Windows.
- Public product should not promise universal site support or bypass platform restrictions.
- Udemy Course mode should remain internal/experimental unless separately approved.
- Public commercial builds should set `UME_PUBLIC_PRODUCT_MODE=1` to hide Course Mode.

## Constraints

- No MVP, backend, frontend, web UI, extension, or desktop wrapper during Phase 0.
- No real media downloads during Phase 0.
- No mass link checks.
- No paid external APIs.
- Use official docs first.
- Treat CLI/API capability as separate from UI capability.

## Current Status

Analysis-only block completed through the former Phase 15 work. The user has requested no further Phase numbering unless explicitly authorized.

Block 2 Download + Output Pipeline completed.

Block 3 Whisper + Transcript Pipeline completed.

Block 4 Processing UI + MVP Flow completed.

Block 5 MVP Integration / Readiness Review completed.

Block 6 Job / Progress / Cancel completed.

Block 7 Local File Input completed.

Block 8 Cleanup / Output Management completed.

Block 9 Real Progress / Subprocess Cancellation Hardening completed.

Block 10 Browser Verification / UI QA Tooling completed.

Block 11 Desktop Wrapper completed.

Udemy Course Offline Export initial implementation completed as a user-approved feature block without renumbering Roadmap v2. The app now has `Course mode`, `POST /udemy/analyze`, and `POST /udemy/download`. This path uses `yt-dlp` with Chrome session auth by default and manual `cookies.txt` as an advanced fallback. It does not store credentials, does not copy cookies into outputs, and does not implement DRM/key/CAPTCHA/paywall bypass.

Udemy Course mode was refined after user testing. The UI no longer rewrites Udemy lecture/player URLs into clean `/course/<slug>/` URLs, because the tested clean course URL failed in `yt-dlp` with `Unable to extract course id` while the lecture/player URL returned the full course playlist. Failed Udemy analysis now saves redacted diagnostic artifacts and the UI can show collapsible technical details for errors.

Roadmap v2 documented in `docs/ROADMAP_V2.md`.

Previous Roadmap v2 next planned block was Block 12. Chrome Extension. The imported commercial strategy recommends deferring extension work and prioritizing commercial readiness: public product boundary, production packaging, persistent jobs/history, batch, presets, diagnostics, security, website, and licensing.

Do not start a new commercial implementation block until the user explicitly confirms.

Commercial strategy docs:

- `docs/UNIVERSAL_MEDIA_EXTRACTOR_PRODUCT_STRATEGY.md`
- `docs/COMMERCIALIZATION_EXECUTION_PLAN.md`
- `docs/GITHUB_COMMERCIAL_BACKLOG.md`

GitHub commercial roadmap board: `https://github.com/users/Shteinyr/projects/7`. It contains 40 issues across 8 milestones.

Commercial Foundation issues #1-#5 are completed and documented in:

- `docs/PUBLIC_PRODUCT_BOUNDARY.md`
- `docs/LEGAL_SAFE_PRODUCT_COPY.md`
- `docs/EULA_DRAFT.md`
- `docs/PRIVACY_POLICY_DRAFT.md`
- `docs/REFUND_POLICY_DRAFT.md`
- `docs/PUBLIC_KNOWN_LIMITATIONS.md`

Commercial Block 2 issues #6-#7 add normalized errors and safe diagnostics, documented in `docs/COMMERCIAL_BLOCK_2_ERRORS_DIAGNOSTICS.md`.

Commercial Block 3 issue #9 replaces public technical format selection with preset-based output selection, documented in `docs/COMMERCIAL_BLOCK_3_PRESET_OUTPUT_SELECTION.md`.

Commercial Block 4 issue #8 hardens localhost security with a random UI/backend session token, strict local host/origin checks, explicit CORS policy, upload size limits, and preserved path/CLI/log safety boundaries. It is documented in `docs/COMMERCIAL_BLOCK_4_LOCALHOST_SECURITY.md`.

Commercial Block 5 issue #10 replaces runtime-only app jobs with SQLite-backed local job history. Jobs survive restart, interrupted queued/running jobs recover to a failed recoverable state, failed jobs can be retried, and terminal history can be cleared without deleting output files. It is documented in `docs/COMMERCIAL_BLOCK_5_SQLITE_JOBS_HISTORY.md`.

Commercial Block 6 issue #11 adds URL output folder templates, macOS/Windows-safe output names, duplicate policies (`rename`, `skip`, `overwrite`), and reveal-in-Finder/Explorer for managed outputs. It is documented in `docs/COMMERCIAL_BLOCK_6_OUTPUT_TEMPLATES_DUPLICATES.md`.

Commercial Block 10 prepares macOS public release docs and validation gates around issues #13/#14. It adds `docs/MACOS_PUBLIC_RELEASE_CHECKLIST.md`, `docs/APPLE_DEVELOPER_ACCOUNT_SETUP.md`, `docs/MACOS_RELEASE_VALIDATION_CHECKLIST.md`, `docs/MACOS_SIGNING_NOTARIZATION_TROUBLESHOOTING.md`, and `scripts/notarize_macos_dmg.py`. Issues #13/#14 remain open because real Developer ID signing/notarization and Gatekeeper validation require Apple Developer Program access and local Keychain credentials from the user.

Commercial Block 11 prepares the public founder launch surface for issues #19-#21: static landing page in `site/`, `docs/FOUNDER_LAUNCH_SITE_COPY.md`, `docs/BETA_ONBOARDING_COPY.md`, `docs/PRICING_AND_PLANS.md`, and `docs/SUPPORT_PAGE_DRAFT.md`. Issues #19, #20, and #21 are closed and marked Done in the project. No checkout, license activation, Apple signing, Windows build, or new product feature was added.

Commercial Block 12 prepares payment provider pre-approval and licensing model drafts for issues #22-#23. It adds Lemon Squeezy pre-approval copy, Stripe fallback risk review, a 3-device/offline-grace licensing model draft, and a user decision checklist. No checkout, payment provider API, webhook, license server, or license enforcement code was added.


`PROJECT_CONTEXT.md` now exists as the long-term project context file. Read it before large tasks and update it after completed large blocks.

Block 11 created `scripts/run_desktop.py` using `pywebview`. The launcher starts the existing FastAPI app locally on `127.0.0.1`, opens the static UI in a desktop window, chooses the next local port if `8000` is busy, and shuts down its owned backend after the window closes. Browser mode through `scripts/run_api.py` remains unchanged.

Verdict: CONDITIONAL GO.

The project is technically feasible as a local, single-user, best-effort media extractor and transcriber using `yt-dlp`, `ffmpeg`, and local Whisper CLI. It is not feasible as a guaranteed universal downloader for every website or every protected/authenticated source.

Current MVP works for:

- URL -> Analyze -> Download -> Transcribe -> Result.
- Local file -> Analyze -> Transcribe -> Result.
- Udemy course URL + Chrome session -> Analyze course -> Download course best-effort.
- Udemy lecture/player URL + Chrome session -> Analyze course playlist -> Download course best-effort.

Phase 1 created `.venv`, installed minimal backend dependencies, created `requirements.txt`, and recorded environment/proof check documentation.

Phase 2 analyzed `https://youtu.be/UUdxAp3kuKA` with `yt-dlp` without downloading media. Raw analysis files were saved under `proof/phase_2/`. The URL resolved successfully as YouTube video `Showreel`, duration 39 seconds, with audio-only, video-only, and combined video+audio formats. No subtitles or automatic captions were found.

Phase 3 defined a normalized future `AnalyzeResult` data contract based on the real Phase 2 `yt-dlp` output. It created a valid sample normalized JSON result and backend/frontend model notes. No application code was created.

Phase 4 created Pydantic v2 models for the analyze-result contract under `src/universal_media_extractor/models/analyze.py` and tests under `tests/test_analyze_models.py`. The Phase 3 sample JSON validates successfully.

Phase 5 created `normalize_ytdlp_info(raw, raw_reference_path=None)` under `src/universal_media_extractor/normalizers/ytdlp.py`. It converts an already-loaded `yt-dlp --dump-json` dictionary into `AnalyzeResult` without calling `yt-dlp`, downloading media, or creating backend routes.

Phase 6 created `analyze_url_with_ytdlp(url, timeout_seconds=60, raw_output_dir=None)` under `src/universal_media_extractor/analyzers/ytdlp.py`. It safely calls `yt-dlp --simulate --dump-json URL` with `subprocess.run(..., shell=False)`, maps errors into `AnalyzeResult.errors`, optionally saves raw JSON only when requested, and passes successful raw output into the Phase 5 normalizer. Automated tests mock subprocess and do not hit the network.

Phase 7 ran `scripts/manual_analyze_url.py` against `https://youtu.be/UUdxAp3kuKA` with `--raw-output-dir proof/phase_7`. The command completed successfully with `errors=[]`, returned a normalized `AnalyzeResult`, and saved raw analysis JSON to `proof/phase_7/ytdlp_UUdxAp3kuKA_20260529T081128Z.json`. No media download or Whisper run was performed.

Phase 8 documented the future service layer without creating FastAPI routes, backend app code, frontend code, downloader code, transcription code, media downloads, or Whisper runs. It defined planned services, draft API endpoints, future frontend flow, and a strict first-MVP boundary.

Phase 9 created minimal service-layer interfaces and tests without creating FastAPI routes, backend app, frontend, downloader, transcription module, media downloads, or Whisper runs. The new services are `AnalyzeService`, `OutputManager`, `SafetyService`, and in-memory `JobService`; a small Pydantic `Job` model was added.

Phase 10 created a minimal analysis-only FastAPI backend with `/health`, `/analyze`, and `/jobs/{job_id}`. The run script binds Uvicorn only to `127.0.0.1`. Tests mock the analysis service and do not call the network, download media, or run Whisper.

Phase 11 manually ran the real local API and called `POST /analyze` on the user-authorized URL `https://youtu.be/UUdxAp3kuKA`. The endpoint returned a normalized `AnalyzeResult` for `Showreel`, job status `succeeded`, zero errors, and the same expected media option groups. No media download or Whisper run was performed.

Phase 12 planned the first frontend UI as an analysis-result display only interface based on the real Phase 11 API response. No frontend app or UI code was created. The recommended first prototype approach is static HTML/CSS/vanilla JS connected to the existing `POST /analyze` endpoint.

Phase 13 created a minimal static HTML/CSS/vanilla JS UI served by the existing FastAPI backend at `http://127.0.0.1:8000/`. The UI supports paste URL, analyze, loading state, result summary, media format groups, empty subtitles/captions states, warnings, and errors. It does not include download, Whisper/transcription, local file upload, settings, auth, database, cookies/login, extension, or desktop wrapper.

Phase 14 polished the existing static analysis-only UI without adding features. It improved visual hierarchy, spacing, keyboard/focus handling, aria status/error states, reduced-motion handling, empty thumbnail handling, and responsive behavior. No backend API changes were made.

Phase 15 refined analysis-only UI/API error states without adding product features. The UI now distinguishes empty URL, invalid URL, API unavailable, API error response, and analyzer errors. The API now rejects malformed non-http(s) URLs with `422` before calling the analyzer. Analyzer errors remain in `AnalyzeResult.errors` and failed job state.

Block 2 added a user-confirmed selected-format download path. `DownloadService` calls `yt-dlp` through `subprocess.run([...], shell=False)` only after `user_confirmed_rights=true`, writes structured output folders, and returns `DownloadResult`. The local API now exposes `POST /download`, and the static UI can select an analyzed format, require rights confirmation, start the download, and show output paths/errors. One manual proof downloaded audio-only format `140` from the user-owned test URL into `proof/download_block/`.

Block 3 added local transcription for already downloaded audio/video files. `TranscriptionService` can run Whisper CLI on audio files, extract audio from video through `ffmpeg`, write transcript artifacts into the existing output structure, and return `TranscriptionResult`. The local API now exposes `POST /transcribe`, and the static UI can transcribe the downloaded file after a successful download. Manual proof transcribed the downloaded Showreel audio-only file and created `transcript.txt`, `transcript.md`, `transcript.json`, and `summary_prompt.md`.

Block 4 unified the static UI into the intended MVP flow: Analyze -> Select format -> Confirm rights -> Download -> Transcribe -> Result. It added a visible flow tracker, clearer selected-format state, Whisper model selector, generated-files result card, transcript preview, and copy actions for transcript, summary prompt, and output path. It reused existing `/analyze`, `/download`, and `/transcribe` endpoints.

Block 5 performed a readiness review and smoke test for the current MVP without adding new product features. The full local API flow was verified on the user-authorized URL: analyze -> download audio-only format `140` -> transcribe with Whisper model `tiny` -> verify output files. Readiness documentation and known limitations were added.

Block 6 converted `/download` and `/transcribe` into background in-memory jobs. The UI now polls `GET /jobs/{job_id}`, shows coarse job status/current step, and offers best-effort cancel buttons. Cancellation marks queued jobs immediately and sets `cancel_requested=true` for running jobs, but it does not forcibly kill active `yt-dlp`, `ffmpeg`, or Whisper subprocesses.

Block 7 added local file input. The UI now has URL mode and Local file mode. Local files are copied into project-local output folders, inspected with `ffprobe` through `POST /local/analyze`, and transcribed through job-based `POST /local/transcribe` using the existing `TranscriptionService`. Local mode does not use `yt-dlp` or remote URLs.

Block 8 added output indexing and safe delete for user results under `outputs/`. The UI now has a `Recent results` block. `proof/` remains a development artifact area and is not indexed or automatically deleted.

Block 9 hardened progress and cancellation for existing download/transcription jobs. Active `yt-dlp`, `ffmpeg`, and Whisper subprocesses can now be registered against a job and cancellation attempts to terminate them. Download parses practical `yt-dlp` percent lines when available; transcription uses honest step-based progress without fake Whisper percentages. Manual proof artifacts are under `proof/block_9/`.

Block 10 added minimal Python Playwright browser verification tooling. `scripts/browser_smoke.py` can open the local UI, run the default analysis-only flow, verify `Showreel` and format groups, and save screenshots under `proof/block_10/`. Normal `pytest` does not run browser automation.

UI simplification pass completed after Block 10 without creating a new roadmap block. The format selector now starts with `Audio`, `Video`, and `Subtitles`; detailed technical format rows are hidden from the main UI. Audio rows show only container and approximate size. Video rows show container, quality, and size, and hide variants below `1080p`.

UI dedup fix completed after the simplification pass without creating a new roadmap block. User-facing Audio, Video, and Subtitles options are now deduplicated in the frontend mapping layer before rendering. Video rows collapse by container and quality, subtitles collapse by language and manual/automatic type, and subtitle file formats are merged into a single option.

v0 UI reference port completed after the dedup fix without creating a new roadmap block. The downloaded v0 project was audited as a Next.js/React/Tailwind/shadcn reference, but the main project stayed FastAPI plus static HTML/CSS/vanilla JS. The current UI now uses a compact downloader/file-manager layout inspired by the reference while preserving the existing API and MVP flows.

Download/transcription UI simplification completed after the v0 reference port without creating a new roadmap block. The visible rights confirmation checkboxes were removed from the static UI. The existing backend contract is preserved by sending `user_confirmed_rights=true` from the simplified button actions, while the UI now enables download when an output is selected.

Video download behavior updated after the simplified download action without creating a new roadmap block. The `Video` UI choice now downloads the selected video stream together with the best available audio stream as one merged output file. Subtitle downloads still do not reveal the Whisper transcription panel.

Download location and format settings completed as a small UX refinement without creating a new roadmap block. URL downloads now default to `~/Downloads/Universal Media Extractor`, and the download card exposes compact `Save to` and `Format` fields. Format choices are Video `MP4`/`MKV`/`WEBM`, Audio `M4A`/`MP3`/`WAV`, and Subtitles `SRT`/`VTT`. URL result folders are named from the source title when available, the selected output file is saved directly inside that folder, service artifacts go to hidden `.metadata`/`.logs`, and `Recent results` follows the selected output base after a download request.

Transcript output simplification completed as a small UX refinement without creating a new roadmap block. The UI now lets the user choose exactly one transcript format per run: `TXT`, `Markdown`, or `JSON`. The selected transcript is saved directly into the same result folder as the downloaded/local media, while Whisper intermediate files and logs are kept in hidden service folders. The generated files UI now shows only the folder, media file, and selected transcript instead of all transcript formats and long technical paths.

Final UI cleanup completed after Block 11 without creating a new roadmap block. Visible development-oriented sidebar areas were removed or visually hidden: header description, input helper text, backend status, MVP flow checklist, and Recent results. The core URL/local file -> analyze -> download -> transcribe -> result flow remains unchanged.

Development `.app` launcher completed after Block 11 without creating a new roadmap block. `scripts/build_dev_app.py` creates `build/dev/Universal Media Extractor Dev.app`, a minimal macOS bundle that points back to the current project folder and runs `.venv/bin/python scripts/run_desktop.py`. Code changes are picked up on the next app launch as long as the project path and `.venv` remain in place.

The development `.app` now uses a tiny compiled Mach-O launcher in `Contents/MacOS/UniversalMediaExtractorDev` plus `Contents/Resources/launcher.zsh`. This fixed Finder/LaunchServices startup from `/Applications`.

## Confirmed Capabilities

- `yt-dlp` can list formats, dump JSON metadata, list subtitles, simulate analysis, use cookies, extract audio, merge formats, and emit progress.
- `yt-dlp` successfully analyzed the user-provided URL without downloading media and produced raw JSON, format list, and subtitle list outputs.
- A stable analyze-result contract has been documented for source summary, media options, subtitles, metadata, warnings, errors, and legal/safety confirmation.
- Pydantic models now validate the normalized analyze-result sample and can export/import JSON.
- The Phase 2 raw `yt-dlp` JSON now normalizes into `AnalyzeResult`, preserving title, duration, extractor, thumbnail, grouped media options, empty subtitles/captions, warnings, and raw artifact reference.
- A backend-ready CLI analysis wrapper can call yt-dlp in analysis-only mode and return `AnalyzeResult` without exposing routes.
- The manual analysis script has been verified on the user-provided URL in analysis-only mode.
- A future service-layer boundary is documented: `AnalyzeService`, minimal `OutputManager`, minimal `JobService`, and minimal `SafetyService` are the first MVP services; download/transcription/local-file metadata remain later.
- Minimal service-layer code now exists for URL analysis orchestration, analysis artifact directory creation, legal/safety confirmation state, and in-memory job status.
- The full test suite passes after Phase 10: 31 tests passed.
- A local-only FastAPI backend now exists for analysis-only URL flow.
- Runtime health proof confirmed `GET /health` on `http://127.0.0.1:8765/health`.
- Manual API proof confirmed `POST /analyze` on `http://127.0.0.1:8000/analyze` works for the user-authorized URL.
- Manual API proof confirmed `GET /jobs/{job_id}` returns the in-memory job while the server is running.
- Frontend scope is now planned for a first analysis viewer: paste URL, call `POST /analyze`, display normalized `AnalyzeResult`, warnings, errors, and format groups.
- Recommended frontend approach for Phase 13 is static HTML/CSS/vanilla JS served locally, not a Vite app yet.
- Static analysis-only UI now exists and is served from `/`.
- Automated tests pass after Phase 15: 36 tests passed.
- Live HTTP proof confirmed `/`, `/static/app.js`, and `/analyze` work on `127.0.0.1:8000`.
- UI accessibility basics now include visible labels, `aria-describedby`, `role="status"`, `role="alert"`, `aria-busy`, `:focus-visible`, skip link, and reduced-motion support.
- UI/API error states now cover empty URL, invalid URL, API unavailable, API error responses, unsupported source, login required, cookies required, analyzer failure, and neutral subtitle/caption empty states.
- Roadmap governance now uses large blocks instead of new Phase numbers unless the user explicitly authorizes new Phase numbering.
- Download models now exist: `DownloadRequest`, `DownloadResult`, `DownloadMode`, and `DownloadStatus`.
- `DownloadService` can run a selected-format `yt-dlp` download after rights confirmation.
- Download output directories now use `media/`, `metadata/`, and `logs/` subfolders.
- `POST /download` exists for local-only selected-format downloads.
- Static UI now supports selecting a format row, confirming rights, downloading the selected format, and displaying output paths.
- Automated tests pass after Block 2: 43 tests passed.
- Manual proof confirmed audio-only format `140` downloaded successfully from the user-owned URL into `proof/download_block/20260529T092713Z_UUdxAp3kuKA/`.
- Transcription models now exist: `TranscriptionRequest`, `TranscriptionResult`, `SourceMediaKind`, and `TranscriptionStatus`.
- `TranscriptionService` can run local Whisper CLI after rights confirmation.
- Video transcription path can extract audio to `media/extracted_audio.wav` through `ffmpeg` before Whisper.
- `POST /transcribe` exists for local-only file transcription.
- Static UI now exposes a transcript panel after successful download.
- Transcript output structure now includes `transcripts/transcript.txt`, `transcripts/transcript.md`, `transcripts/transcript.json`, and `transcripts/summary_prompt.md`.
- Automated tests pass after Block 3: 49 tests passed.
- Manual proof confirmed the downloaded Showreel audio-only file transcribed successfully with Whisper model `tiny`.
- Static UI now presents a single end-to-end MVP flow from URL analysis through generated transcript artifacts.
- UI now includes a Whisper model selector: `tiny`, `base`, `small`, `medium`, and `turbo/default`.
- UI generated-files card now shows output directory, media file, transcript files, summary prompt, and transcript preview.
- UI result actions now include copy transcript, copy summary prompt, and copy output path.
- `TranscriptionResult` now includes `transcript_text` and `summary_prompt_text` so browser UI can preview/copy content without native filesystem access.
- Automated tests pass after Block 4: 49 tests passed.
- Manual end-to-end API proof confirmed analyze -> download format `140` -> transcribe model `tiny` -> transcript artifacts under `proof/block_4/`.
- MVP smoke test passed in Block 5 using the full flow and proof artifacts under `proof/block_5/`.
- Output review confirmed media, metadata, logs, transcript files, and `summary_prompt.md` exist.
- README now includes quick start, MVP flow, output location, and MVP limitations.
- `docs/MVP_KNOWN_LIMITATIONS.md` now records current known limits.
- `docs/BLOCK_5_MVP_READINESS_REVIEW.md` records smoke test commands, results, and proof artifacts.
- In-memory jobs now include `current_step`, optional `progress_percent`, `started_at`, `finished_at`, `result`, `error`, and `cancel_requested`.
- `POST /download` now returns a `Job` and stores serialized `DownloadResult` in `job.result`.
- `POST /transcribe` now returns a `Job` and stores serialized `TranscriptionResult` in `job.result`.
- `POST /jobs/{job_id}/cancel` now exists for best-effort cancellation.
- Static UI now polls `GET /jobs/{job_id}` for download/transcription and shows job status, current step, errors, and cancel actions.
- Automated tests pass after Block 6: 51 tests passed.
- Manual API proof confirmed job-based analyze -> download format `140` -> transcribe model `tiny` -> transcript artifacts under `proof/block_6/`.
- Local file models now exist: `LocalFileAnalyzeResult`, `LocalFileStreamInfo`, and `LocalMediaType`.
- `LocalFileMetadataService` can inspect uploaded local audio/video files with `ffprobe`.
- `POST /local/analyze` saves an uploaded file under `outputs/local_<timestamp>_<safe_filename>/source/` and returns metadata.
- `POST /local/transcribe` creates an in-memory transcription job for a saved local file reference.
- Static UI now supports URL mode and Local file mode.
- Local file mode shows metadata, codec/stream info, rights confirmation, Whisper model selection, transcription job status, transcript preview, and generated files.
- Automated tests pass after Block 7: 59 tests passed.
- Manual proof confirmed a synthetic local WAV can be analyzed and transcribed, with transcript artifacts under `outputs/local_20260530T134814Z_synthetic_sine/`.
- Output models now exist: `OutputSummary`, `OutputListResult`, and `OutputDeleteResult`.
- `OutputManager` can list, summarize, and safely delete direct user output folders under `outputs/`.
- `GET /outputs`, `GET /outputs/{output_id}`, and `DELETE /outputs/{output_id}` are implemented.
- Static UI now shows `Recent results` with media/transcript/prompt badges, size, file count, copy path, and delete.
- Automated tests pass after Block 8: 68 tests passed.
- Manual proof confirmed a dedicated dummy output was deleted and real output `outputs/local_20260530T134814Z_synthetic_sine/` remained intact.
- Active subprocess tracking now exists for running download/transcription jobs.
- Download jobs now parse practical `yt-dlp` progress percent output when available.
- Transcription jobs now expose honest steps: `preparing_transcription`, `extracting_audio`, `running_whisper`, and `generating_transcript_files`.
- Cancellation now attempts to terminate or kill a registered active subprocess.
- Automated tests pass after Block 9: 73 tests passed.
- Manual proof confirmed URL analyze -> download format `140` -> transcribe model `tiny` -> transcript artifacts under `proof/block_9/outputs/`.
- Controlled cancellation proof confirmed a registered synthetic `sleep 30` subprocess was terminated and job status became `cancelled`.
- Python Playwright is installed in `.venv` as `playwright==1.60.0`.
- Playwright Chromium browser binaries were installed and headless Chromium launch was verified.
- `scripts/browser_smoke.py` exists for manual/dev browser smoke checks.
- Browser smoke proof confirmed the local UI loads at `127.0.0.1:8000`, analyzes the user URL, displays `Showreel`, and shows audio/video/combined groups.
- Block 10 screenshots exist under `proof/block_10/ui_initial.png` and `proof/block_10/ui_analyze_result.png`.
- `pywebview==6.2.1` is installed in `.venv`.
- `scripts/run_desktop.py` exists for desktop mode.
- `scripts/build_dev_app.py` exists for building a development `.app` launcher.
- Desktop wrapper proof confirmed the app opens in a pywebview window and shuts down its owned backend after close.
- Development `.app` proof confirmed `open -W "build/dev/Universal Media Extractor Dev.app" --args --smoke-seconds 3` launches and exits cleanly.
- `/Applications/Universal Media Extractor Dev.app` was refreshed from the latest dev bundle and verified through macOS `open`.
- Browser mode remains available through `scripts/run_api.py`.
- Block 11 browser proof screenshots exist under `proof/block_11/browser_smoke/`.
- Simplified format selection UI now uses `Audio`, `Video`, and `Subtitles` category tabs.
- Audio rows now hide codecs, bitrates, ids, and repeated `audio only` labels.
- Video rows now hide codecs, fps, ids, and variants below `1080p`.
- UI simplification proof screenshots exist under `proof/ui_simplification/`.
- User-facing format options now deduplicate repeated Audio, Video, and Subtitle rows before rendering.
- Video duplicates are collapsed by container and visible quality, with known file size and recommended options preferred.
- Subtitle duplicates are collapsed by language and manual/automatic type, with subtitle file formats merged into one option.
- UI dedup proof screenshots exist under `proof/ui_dedup_fix/`.
- The v0 UI reference was audited from `/Users/aleksandr/Documents/Codex/universal-media-extractor/media-extractor-ui`.
- The main app UI now adopts the v0-inspired compact sidebar and centered work area without adding Next.js, React, Tailwind, shadcn/ui, or a new frontend build.
- v0 UI port proof screenshots exist under `proof/v0_ui_port/`.
- Visible rights confirmation checkboxes were removed from the current UI; download now starts from the selected output button once a format is selected.
- `ffmpeg`/`ffprobe` can inspect, extract, convert, and emit machine-readable progress.
- Whisper CLI can transcribe local audio and write `txt`, `vtt`, `srt`, `tsv`, `json`, or all outputs.
- Uvicorn can bind to `127.0.0.1` for local-only backend access.
- FastAPI supports file uploads and generated OpenAPI docs; background tasks exist but heavy work should use explicit subprocess/job management.
- pywebview now wraps the existing local web app in a desktop window through `scripts/run_desktop.py`.
- Chrome Native Messaging can connect an extension to a native host later, but requires user/installer setup and extension permissions.

## Blockers And Limits

- `yt-dlp` source support is not guaranteed; sites change and local extractor list includes broken entries.
- Platform terms, especially YouTube, may restrict downloading and automated access.
- Cookies/login may be required for some sources and must be user-controlled.
- DRM/CAPTCHA/paywall bypass is out of scope.
- Long-file Whisper transcription may be slow on CPU.
- Large media files can consume significant disk space.
- FastAPI/Uvicorn/Pydantic/python-multipart/aiofiles are installed inside the project `.venv`.
- `pywebview==6.2.1` is installed in `.venv` for the Block 11 desktop wrapper.
- Local Python `urllib.request` HTTPS certificate verification failed against PyPI, while `curl` and `pip` worked; future Python HTTPS code should account for certificates.
- Phase 2 proved URL analysis only; it did not prove download, merge, conversion, transcription, progress parsing, cancellation, or app-level local-only binding.
- The Phase 2 URL has no subtitles or automatic captions.
- Some format sizes are unknown in `yt-dlp` output.
- Phase 4 implemented only Pydantic models and tests; no FastAPI routes, backend app, frontend, downloader, transcription module, media download, or Whisper run.
- Phase 5 implemented only a normalizer/parser and tests; no CLI orchestration, FastAPI routes, backend app, frontend, downloader, transcription module, media download, or Whisper run.
- Error mapping for failed `yt-dlp` commands is not implemented yet; Phase 5 handles successful raw JSON normalization.
- Phase 6 implemented only a CLI analysis wrapper and manual script; no FastAPI routes, backend app, frontend, downloader, transcription module, media download, or Whisper run.
- Phase 6 tests mock subprocess; real network behavior was not re-tested.
- Error classification is conservative and based on `yt-dlp` stderr text.
- Phase 7 proves analysis only; it still does not prove download, merge, conversion, transcription, progress tracking, cancellation, FastAPI routes, or UI.
- Phase 8 is documentation only; it does not prove actual FastAPI route behavior, UI behavior, job execution, cancellation, download, transcription, or output generation.
- The first MVP boundary is deliberately limited to URL analysis and result display, with no download or Whisper in the first UI prototype.
- Phase 9 service interfaces are minimal and in-memory only; they do not implement background execution, persistent storage, route handlers, UI, real cancellation of subprocesses, progress tracking, download, transcription, or local-file metadata.
- Phase 10 API is analysis-only and synchronous; it does not implement frontend, downloader, media download, Whisper, auth, database, cookies/login, cancellation route, progress tracking, or persistent jobs.
- `httpx2==2.2.0` is now installed and recorded because the current Starlette TestClient requires it.
- Phase 11 proves the local API analyze path only; it does not prove download, merge, conversion, transcription, progress tracking, cancellation, frontend behavior, desktop packaging, extension integration, auth, database, or cookies/login.
- Jobs remain in-memory and are lost when the API server stops.
- Phase 12 is planning only; frontend implementation, browser verification, and actual UI behavior are not yet proven.
- Phase 13, if authorized, must remain analysis-result display only and must not add download, Whisper, local file upload, auth, database, cookies/login, settings, extension, or desktop wrapper.
- Phase 13 UI behavior was verified through HTTP/API checks. Browser/Playwright screenshot proof was not created at that time because Browser/Playwright was not available in the local toolchain.
- The UI is intentionally minimal and does not yet include persistent state, routing, advanced accessibility audit, visual regression checks, cancellation, progress tracking, or processing actions.
- Phase 14 did not add new functionality; it only polished the existing analysis-only UI.
- Browser/Playwright screenshot verification was unavailable during earlier analysis UI phases; Block 10 later added Playwright smoke tooling.
- Phase 15 did not add product functionality; it only refined error handling for the analysis-only UI/API.
- Frontend error checks are still covered through static asset inspection and live HTTP/API checks, not a browser automation framework.
- Block 2 download is synchronous; no progress stream, active subprocess cancellation, or background download worker exists yet.
- Block 2 manual proof covered only audio-only format `140`; combined/video download and subtitle download still need focused proof checks before being treated as broadly verified.
- Downloads can consume disk space and must remain user-confirmed.
- `yt-dlp` download behavior remains best-effort and subject to platform restrictions.
- Block 3 transcription is synchronous; no progress stream, active subprocess cancellation, or background worker exists yet.
- First UI transcription uses model `tiny` for speed, so transcript quality may be low.
- Block 3 manual proof covered audio-only transcription; real video transcription with ffmpeg extraction is tested with mocks but not manually proofed on a real video file.
- Long Whisper jobs can be slow on CPU and may block the synchronous API request.
- Block 4 did not add visual browser automation proof because local Playwright/browser automation was unavailable (`playwright` module not found).
- Browser UI cannot open local output folders directly; it shows/copies the output path instead.
- Block 4 keeps download/transcription synchronous and does not add progress/cancel.
- Block 5 did not perform visual browser interaction proof because local Playwright/browser automation was unavailable at that time.
- Current MVP is ready only as a local single-user best-effort tool, not as a robust public service or guaranteed universal extractor.
- Block 6 jobs are in-memory and are lost when the API server stops.
- Job progress is still polling-based and in-memory, but Block 9 now parses practical `yt-dlp` percent output when available.
- Whisper progress remains step-based; the app does not fake Whisper percentages.
- Cancellation is still best-effort, but Block 9 now attempts to terminate/kill a registered active subprocess.
- Browser visual verification for Block 6 was blocked by the Browser plugin local URL security policy, so API/manual proof was used.
- Local file mode copies the selected file into the project output folder; it does not maintain a persistent library/history.
- Block 7 proof used a synthetic sine wave; it proves local file handling and artifact generation, not speech transcription quality.
- Local file transcription jobs remain in-memory and cancellation remains best-effort.
- Output delete is limited to direct folders inside `outputs/` and rejects traversal/unsafe ids.
- `proof/` is not managed by the output index and is not cleaned automatically.
- There is no batch delete, output search/filtering, old transcript preview, or desktop/native folder opening.
- Jobs remain in-memory and are lost when the API server stops.
- Subprocess cancellation depends on the active process being registered at the moment cancel is requested.
- Some `yt-dlp` outputs do not expose granular percent until completion.
- Browser visual verification now exists as a manual/dev smoke script, not as ordinary `pytest`.
- Browser smoke requires installed Playwright Chromium binaries and a running backend on `127.0.0.1:8000`.
- Desktop wrapper exists for local use through `pywebview`, and a development `.app` launcher exists. Packaged/signed/notarized `.app` distribution is not implemented.
- Desktop wrapper GUI interaction is not part of ordinary `pytest`; the Block 11 proof used a short pywebview smoke and browser smoke for UI behavior.

## Next Steps

- Stop after Block 11.
- Wait for explicit user confirmation before starting Block 12.
- Follow `docs/ROADMAP_V2.md` unless the user explicitly changes it.
- Treat Codex roadmap suggestions as recommendations only, not decisions.
- Do not add AI summary API, Chrome extension, packaged desktop distribution, auth, database, cookies/login, online service behavior, batch processing, advanced download hardening, external queue, persistent local file library/history, automatic proof cleanup, output batch delete, output search/filtering, persistent job storage, or new roadmap blocks until explicitly authorized in a future block.

- Diagnostics bundles now redact cookies, tokens, passwords, transcripts, full URLs, and local paths by default.

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
