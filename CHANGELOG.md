# Changelog

## 2026-08-05 - Commercial Block 2 Errors And Diagnostics Foundation

- Added normalized user-facing error categories for DRM, login/cookies, region restriction, private/deleted sources, missing formats, network, disk, permission, and outdated engines.
- Added `src/universal_media_extractor/error_mapping.py` for shared CLI error normalization.
- Added diagnostics bundle models and `DiagnosticsService`.
- Added `GET /diagnostics/jobs/{job_id}` for inspectable local support bundles.
- Redacted cookies, tokens, transcripts, full URLs, and local paths from diagnostics by default.
- Added tests for error mapping, diagnostics redaction, and diagnostics API behavior.
- Created `docs/COMMERCIAL_BLOCK_2_ERRORS_DIAGNOSTICS.md`.

## 2026-08-05 - Commercial Foundation

- Completed the first commercial foundation work for issues #1-#5.
- Added public product boundary and positioning documentation.
- Added legal-safe product copy guidance.
- Added draft EULA, privacy policy, refund policy, and public known limitations.
- Added `/config` with public product/course mode flags.
- Added UI support to hide Udemy Course Mode for public commercial builds.
- Documented that Udemy remains internal/experimental and is not part of public positioning.

## 2026-08-05 - GitHub Commercial Roadmap Setup

- Created GitHub Project: `https://github.com/users/Shteinyr/projects/7`.
- Linked the Project to `Shteinyr/universal-media-extractor`.
- Created 8 commercial roadmap milestones.
- Created roadmap labels for priority, track, and release.
- Created 40 roadmap issues from the commercial plan.
- Added all 40 issues to the Project.
- Created and populated Project fields: `Priority`, `Track`, `Release`, and `Roadmap Status`.

## 2026-08-05 - Commercial Strategy Import

- Saved the GPT Pro strategy document into `docs/UNIVERSAL_MEDIA_EXTRACTOR_PRODUCT_STRATEGY.md`.
- Created `docs/COMMERCIALIZATION_EXECUTION_PLAN.md` with the commercial execution direction.
- Created `docs/GITHUB_COMMERCIAL_BACKLOG.md` with 18 ready-to-create GitHub issues.
- Recorded that the public commercial product should be positioned as a local media downloader and organizer, not a universal downloader for every site.
- Recorded that Udemy Course mode should stay internal/experimental unless separately approved for public release.
- GitHub issue/project creation was blocked because the GitHub connector returned `403` and local `gh` auth has an invalid token.

## 2026-06-13 - Udemy Lecture URL Analysis Fix

- Diagnosed the user-tested Udemy course failure.
- Found that the clean `/course/final-cut-pro-x-10/` URL fails in `yt-dlp` with `Unable to extract course id`.
- Verified that the opened lecture/player URL analyzes successfully and returns the course playlist.
- Stopped rewriting Udemy lecture URLs into clean course URLs in the UI.
- Added Udemy analysis failure diagnostics with redacted command/stdout/stderr artifacts.
- Added collapsible technical details for UI error panels.
- Added tests for failed Udemy diagnostics and lecture URL title fallback.
- Updated Udemy docs and README with the recommended lecture/player URL workflow.

## 2026-06-13 - Udemy Chrome Session Simplification

- Simplified Course mode so normal users can choose `Chrome session` instead of manually providing `cookies.txt`.
- Updated Udemy analyze/download contracts with `auth_source`.
- Default Udemy auth now uses `yt-dlp --cookies-from-browser chrome`.
- Kept `Manual cookies.txt` as an advanced fallback.
- Improved Udemy login/cookies/DRM error messages.
- Updated tests and documentation for the new default flow.

## 2026-06-13 - Udemy Course Offline Export

- User approved development of Udemy course offline export based on the reviewed plan.
- Added Udemy course Pydantic models.
- Added `UdemyCourseService` with `yt-dlp` analyze/download wrappers.
- Added `POST /udemy/analyze` and `POST /udemy/download`.
- Added `Course mode` to the static UI with Udemy URL, manual cookies path, quality, container, subtitle toggle, and course download job polling.
- Kept credentials safety boundary: no password fields, no stored cookies, no DRM/key/CAPTCHA/paywall bypass.
- Created `docs/UDEMY_COURSE_EXPORT.md`.
- Added mocked service/API tests for Udemy analyze/download behavior.

## 2026-05-31 - Block 11 Context File

- User authorized Block 11 Desktop Wrapper.
- Created `PROJECT_CONTEXT.md` as the long-term project context file for large tasks and post-block updates.
- Updated `AGENTS.md` so future large tasks must read `PROJECT_CONTEXT.md` and completed large blocks must update it.
- Marked Block 11 as current in project memory before implementation.

## 2026-05-31 - Block 11 Desktop Wrapper

- Checked current `pywebview`, Uvicorn, PyInstaller, and FastAPI static-file documentation through Context7/official sources.
- Installed `pywebview==6.2.1` in `.venv` and added it to `requirements.txt`.
- Created `scripts/run_desktop.py`.
- The desktop launcher starts the existing FastAPI app on `127.0.0.1`, prefers port `8000`, falls back to the next local port through `8020`, and opens the current static UI in a `pywebview` window.
- Preserved browser mode through `scripts/run_api.py`.
- Added `tests/test_desktop_launcher.py`.
- Created `docs/BLOCK_11_DESKTOP_WRAPPER_FEASIBILITY.md` and `docs/BLOCK_11_DESKTOP_WRAPPER.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 85 passed.
- Ran desktop smoke with `.venv/bin/python scripts/run_desktop.py --smoke-seconds 3`; result: desktop UI opened on `127.0.0.1:8001` because `8000` was busy, then the owned backend shut down.
- Verified browser mode health on a separate local port.
- Ran browser smoke proof under `proof/block_11/browser_smoke/`.

## 2026-05-31 - Final UI Cleanup

- User requested removing no-longer-needed visible sidebar areas after successful testing.
- Hid the header description, URL helper copy, visible backend status, MVP flow checklist, and Recent results panel.
- Kept the existing core UI flow and backend behavior unchanged.
- Created `docs/UI_FINAL_CLEANUP_PASS.md`.
- Ran `node --check` on static JavaScript files.
- Ran `.venv/bin/python -m pytest -q`; result: 85 passed.
- Ran browser smoke proof under `proof/final_ui_cleanup/`.

## 2026-06-03 - Development App Bundle

- User approved the Development Mode app bundle plan.
- Created `scripts/build_dev_app.py`.
- The script builds `build/dev/Universal Media Extractor Dev.app`.
- The generated `.app` contains a minimal `Info.plist` and `Contents/MacOS/UniversalMediaExtractorDev` shell launcher.
- The launcher points back to the current project folder and runs `.venv/bin/python scripts/run_desktop.py`, so code changes are picked up on the next app launch.
- Added `tests/test_build_dev_app.py`.
- Ran targeted app bundle tests; result: 6 passed.
- Built the development `.app` and verified its `Info.plist` and executable structure.
- Ran `open -W "build/dev/Universal Media Extractor Dev.app" --args --smoke-seconds 3`; result: app launched and exited cleanly.
- Ran `.venv/bin/python -m pytest -q`; result: 88 passed.
- Created `docs/DEV_APP_BUNDLE.md`.
- Reworked the dev `.app` launcher from a shell-script `CFBundleExecutable` into a compiled Mach-O launcher that calls `Contents/Resources/launcher.zsh`, because Finder/LaunchServices did not reliably start the shell-script executable.
- Refreshed `/Applications/Universal Media Extractor Dev.app` from the rebuilt dev bundle.
- Verified `/Applications/Universal Media Extractor Dev.app` with `open -W ... --args --smoke-seconds 3`; result: launch completed with exit code 0.

## 2026-05-29

- Created Phase 0 project directory structure.
- Created initial project memory files.
- Started feasibility, capability, and risk audit.
- Verified local CLI availability and relevant help/version output for `yt-dlp`, `ffmpeg`, `ffprobe`, `whisper`, and Python.
- Checked current official documentation through Context7 and official web sources.
- Created Phase 0 audit files under `audits/`.
- Recorded final Phase 0 verdict: CONDITIONAL GO.
- Updated project memory with confirmed capabilities, blockers, constraints, and next safe step.
- User accepted the Phase 0 CONDITIONAL GO constraints.
- Created project virtual environment at `.venv`.
- Installed minimal local backend dependencies: FastAPI, Uvicorn standard extras, Pydantic, python-multipart, and aiofiles.
- Created `requirements.txt`.
- Created `docs/PHASE_1_ENVIRONMENT_SETUP.md`.
- Created `docs/PHASE_1_PROOF_CHECKS.md`.
- Verified `ffmpeg`, `ffprobe`, `yt-dlp`, Whisper CLI, system Python, virtualenv Python, and installed dependency imports.
- Did not run URL format listing because no user-provided test URL was supplied.
- User accepted Phase 1 and provided a user-owned test URL for safe analysis.
- Created `proof/phase_2/`.
- Ran `yt-dlp --simulate --dump-json` for `https://youtu.be/UUdxAp3kuKA` and saved `proof/phase_2/url_analysis_raw.json`.
- Ran `yt-dlp --list-formats` for the same URL and saved `proof/phase_2/list_formats_raw.txt`.
- Ran `yt-dlp --list-subs` for the same URL and saved `proof/phase_2/list_subs_raw.txt`.
- Created `docs/PHASE_2_URL_PROOF_CHECK.md`.
- Created `docs/PHASE_2_UI_DATA_MODEL_NOTES.md`.
- Confirmed no media download was performed in Phase 2.
- User accepted Phase 2 and authorized Phase 3 analyze-result data contract work.
- Checked current FastAPI and Pydantic documentation through Context7 for response models and nested model/schema behavior.
- Created `docs/PHASE_3_ANALYZE_DATA_CONTRACT.md`.
- Created `docs/PHASE_3_SAMPLE_ANALYZE_RESULT.json`.
- Created `docs/PHASE_3_BACKEND_MODEL_NOTES.md`.
- Created `docs/PHASE_3_FRONTEND_MODEL_NOTES.md`.
- Validated `docs/PHASE_3_SAMPLE_ANALYZE_RESULT.json` as JSON.
- Confirmed Phase 3 did not create backend app, frontend, routes, downloader/transcription modules, extension, wrapper, media download, or Whisper run.
- User accepted Phase 3 and authorized Phase 4 Pydantic model creation only.
- Checked current Pydantic and FastAPI documentation through Context7 before implementation.
- Installed `pytest==9.0.3` in `.venv` and added it to `requirements.txt`.
- Created `src/universal_media_extractor/__init__.py`.
- Created `src/universal_media_extractor/models/__init__.py`.
- Created `src/universal_media_extractor/models/analyze.py`.
- Created `tests/test_analyze_models.py`.
- Created `docs/PHASE_4_MODEL_IMPLEMENTATION.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 5 passed.
- User accepted Phase 4 and authorized Phase 5 yt-dlp raw JSON normalizer creation only.
- Created `src/universal_media_extractor/normalizers/__init__.py`.
- Created `src/universal_media_extractor/normalizers/ytdlp.py`.
- Created `tests/test_ytdlp_normalizer.py`.
- Created `docs/PHASE_5_YTDLP_NORMALIZER.md`.
- Implemented `normalize_ytdlp_info(raw, raw_reference_path=None) -> AnalyzeResult`.
- Ran `.venv/bin/python -m pytest -q`; result: 11 passed.
- User accepted Phase 5 and authorized Phase 6 CLI analysis wrapper creation only.
- Created `src/universal_media_extractor/analyzers/__init__.py`.
- Created `src/universal_media_extractor/analyzers/ytdlp.py`.
- Created `tests/test_ytdlp_analyzer.py`.
- Created `scripts/manual_analyze_url.py` but did not run it.
- Created `docs/PHASE_6_YTDLP_ANALYZER.md`.
- Added `ytdlp_not_found` to `ErrorCode`.
- Implemented `analyze_url_with_ytdlp(url, timeout_seconds=60, raw_output_dir=None) -> AnalyzeResult`.
- Ran `.venv/bin/python -m pytest -q`; result: 18 passed.
- User accepted Phase 6 and authorized Phase 7 manual analysis proof for `https://youtu.be/UUdxAp3kuKA`.
- Ran `.venv/bin/python scripts/manual_analyze_url.py "https://youtu.be/UUdxAp3kuKA" --raw-output-dir proof/phase_7`.
- Saved raw analysis artifact `proof/phase_7/ytdlp_UUdxAp3kuKA_20260529T081128Z.json`.
- Created `docs/PHASE_7_MANUAL_ANALYZE_PROOF.md`.
- Confirmed manual script returned `AnalyzeResult` with `errors=[]` and no media download or Whisper run.
- User accepted Phase 7 and authorized Phase 8 service-layer planning only.
- Created `docs/PHASE_8_SERVICE_LAYER_PLAN.md`.
- Created `docs/PHASE_8_API_DRAFT.md`.
- Created `docs/PHASE_8_FRONTEND_FLOW_DRAFT.md`.
- Created `docs/PHASE_8_MVP_BOUNDARY.md`.
- Documented planned services, draft API endpoints, future UI flow, and strict first-MVP boundary.
- Confirmed Phase 8 did not create FastAPI app, routes, frontend, downloader, transcription module, media download, Whisper run, extension, or desktop wrapper.
- User accepted Phase 8 and authorized Phase 9 minimal service interfaces without FastAPI routes.
- Created `src/universal_media_extractor/services/__init__.py`.
- Created `src/universal_media_extractor/services/analyze_service.py`.
- Created `src/universal_media_extractor/services/output_manager.py`.
- Created `src/universal_media_extractor/services/safety_service.py`.
- Created `src/universal_media_extractor/services/job_service.py`.
- Created `src/universal_media_extractor/models/job.py`.
- Updated `src/universal_media_extractor/models/__init__.py` to export job models.
- Created `tests/test_analyze_service.py`.
- Created `tests/test_output_manager.py`.
- Created `tests/test_safety_service.py`.
- Created `tests/test_job_service.py`.
- Created `docs/PHASE_9_SERVICE_INTERFACES.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 26 passed.
- Confirmed Phase 9 did not create FastAPI app, routes, frontend, downloader, transcription module, media download, Whisper run, MVP, extension, or desktop wrapper.
- User accepted Phase 9 and authorized Phase 10 analysis-only FastAPI routes with local-only binding.
- Checked current FastAPI, Uvicorn, and Pydantic documentation through Context7 before implementation.
- Created `src/universal_media_extractor/api/__init__.py`.
- Created `src/universal_media_extractor/api/app.py`.
- Created `src/universal_media_extractor/api/schemas.py`.
- Created `scripts/run_api.py`.
- Created `tests/test_api_app.py`.
- Updated `src/universal_media_extractor/services/output_manager.py` to add unique suffixes and truncate sanitized source IDs for analysis artifact directories.
- Added `httpx2==2.2.0` to `requirements.txt` for the current Starlette TestClient.
- Created `docs/PHASE_10_ANALYSIS_API.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 31 passed.
- Ran `scripts/run_api.py` on port 8765 and verified `GET /health` at `http://127.0.0.1:8765/health`; then stopped the server.
- Confirmed Phase 10 did not create frontend, downloader, media download, Whisper run, Chrome extension, desktop wrapper, online service, auth, database, or cookies/login.
- User accepted Phase 10 and authorized Phase 11 manual API proof for `POST /analyze`.
- Ran `.venv/bin/python scripts/run_api.py` on `127.0.0.1:8000`.
- Verified `GET /health` and saved `proof/phase_11/health_response.json`.
- Called `POST /analyze` for `https://youtu.be/UUdxAp3kuKA` and saved `proof/phase_11/analyze_response.json` plus a pretty-printed copy.
- Verified the API returned job status `succeeded`, title `Showreel`, duration `39.0`, extractor `youtube`, 3 audio-only options, 4 video-only options, 5 combined options, no subtitles, no automatic captions, and zero errors.
- Verified `GET /jobs/{job_id}` and saved `proof/phase_11/job_response.json` plus a pretty-printed copy.
- The API saved raw `yt-dlp --simulate --dump-json` analysis JSON under `proof/api/`.
- Created `docs/PHASE_11_MANUAL_API_ANALYZE_PROOF.md`.
- Stopped the API server after the proof.
- Confirmed Phase 11 did not create frontend, downloader, media download, Whisper run, extension, desktop wrapper, auth, database, or cookies/login.
- User accepted Phase 11 and authorized Phase 12 frontend planning only.
- Read the real Phase 11 API response from `proof/phase_11/analyze_response_pretty.json`.
- Created `docs/PHASE_12_FRONTEND_ANALYSIS_UI_PLAN.md`.
- Created `docs/PHASE_12_UI_COMPONENT_MAP.md`.
- Created `docs/PHASE_12_FRONTEND_SCOPE_BOUNDARY.md`.
- Recommended static HTML/CSS/vanilla JS for the first analysis-only UI prototype.
- Confirmed Phase 12 did not create frontend app files, UI code, downloader, media download, Whisper run, extension, desktop wrapper, auth, database, cookies/login, or API changes.
- User accepted Phase 12 and authorized Phase 13 minimal static analysis-only UI.
- Created `src/universal_media_extractor/static/index.html`.
- Created `src/universal_media_extractor/static/styles.css`.
- Created `src/universal_media_extractor/static/app.js`.
- Updated `src/universal_media_extractor/api/app.py` to serve `GET /` and `/static/*`.
- Updated `tests/test_api_app.py` to verify static index and JavaScript availability.
- Created `docs/PHASE_13_STATIC_ANALYSIS_UI.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 33 passed.
- Ran the backend at `127.0.0.1:8000` and verified `/health`, `/`, `/static/app.js`, and real `POST /analyze` for `https://youtu.be/UUdxAp3kuKA`.
- Saved Phase 13 proof files under `proof/phase_13/`.
- Browser/Playwright screenshot proof was not created because Browser/Playwright was not available in the local toolchain.
- Confirmed Phase 13 did not add download, Whisper/transcription, local file upload, extension, desktop wrapper, auth, database, cookies/login, settings page, React, Vite, CDN, or external asset bundle.
- User accepted Phase 13 and authorized Phase 14 UI polish/accessibility pass without new features.
- Updated `src/universal_media_extractor/static/index.html` with skip link, `aria-describedby`, status/error roles, and cleaner loading copy.
- Updated `src/universal_media_extractor/static/styles.css` with improved spacing, focus-visible states, reduced-motion handling, responsive refinements, compact format lists, and clearer warning/error styling.
- Updated `src/universal_media_extractor/static/app.js` with `aria-busy`, empty thumbnail handling, and format-group visual state hooks.
- Created `docs/PHASE_14_UI_POLISH_ACCESSIBILITY.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 33 passed.
- Ran the backend at `127.0.0.1:8000` and verified `/`, `/static/styles.css`, `/static/app.js`, and real `POST /analyze` for `https://youtu.be/UUdxAp3kuKA`.
- Saved Phase 14 proof files under `proof/phase_14/`.
- Confirmed Browser/Playwright screenshot verification was unavailable because Playwright and browser command-line binaries were missing.
- Confirmed Phase 14 did not add download, Whisper/transcription, local file upload, extension, desktop wrapper, auth, database, cookies/login, settings page, React, Vite, CDN, external assets, or backend API changes.
- User accepted Phase 14 and authorized Phase 15 error-state refinement/testing.
- Updated `src/universal_media_extractor/static/app.js` to distinguish empty URL, invalid URL, API unavailable, API error responses, and analyzer errors.
- Added code-specific frontend messages for unsupported source, login required, cookies required, network error, timeout, missing yt-dlp, extractor failure, and invalid analyzer output.
- Updated `src/universal_media_extractor/api/schemas.py` with Pydantic v2 URL validation for `AnalyzeRequest.url`.
- Updated `tests/test_api_app.py` for empty URL, invalid URL, login-required analyzer error, and static JS error-state text checks.
- Created `docs/PHASE_15_ERROR_STATE_REFINEMENT.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 36 passed.
- Ran the backend at `127.0.0.1:8000` and verified `/`, `/static/app.js`, invalid URL `422`, and real `POST /analyze` for `https://youtu.be/UUdxAp3kuKA`.
- Saved Phase 15 proof files under `proof/phase_15/`.
- Confirmed Phase 15 did not add download, Whisper/transcription, local file upload, extension, desktop wrapper, auth, database, cookies/login, settings page, React, Vite, CDN, external assets, or media processing.
- User requested no new Phase numbering; future work should be organized by larger blocks.
- Created `docs/ROADMAP_GOVERNANCE.md`.
- Started and completed Block 2 Download + Output Pipeline.
- Created `src/universal_media_extractor/models/download.py`.
- Created `src/universal_media_extractor/services/download_service.py`.
- Updated `src/universal_media_extractor/services/output_manager.py` with download output directory creation.
- Updated `src/universal_media_extractor/api/app.py` and `src/universal_media_extractor/api/schemas.py` with `POST /download`.
- Updated static UI files to support format selection, rights confirmation, selected-format download, and download result display.
- Added tests for download service, download API behavior, and download output structure.
- Created `docs/BLOCK_2_DOWNLOAD_OUTPUT_PIPELINE.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 43 passed.
- Ran one user-authorized manual audio-only download proof for `https://youtu.be/UUdxAp3kuKA`, format `140`, into `proof/download_block/`.
- Confirmed the manual proof created `proof/download_block/20260529T092713Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a`.
- Confirmed Block 2 did not run Whisper, create transcription, add local file upload, extension, desktop wrapper, auth, database, cookies/login, online service behavior, or AI summary.
- User authorized Block 3 Whisper + Transcript Pipeline.
- Checked current OpenAI Whisper and FFmpeg documentation through Context7, plus local `whisper --help`/`ffmpeg` help output.
- Created `src/universal_media_extractor/models/transcript.py`.
- Created `src/universal_media_extractor/services/transcription_service.py`.
- Updated `src/universal_media_extractor/api/app.py` and `src/universal_media_extractor/api/schemas.py` with `POST /transcribe`.
- Updated `src/universal_media_extractor/services/output_manager.py` to ensure transcription output structure.
- Updated static UI files to show a transcript panel after successful download and call `/transcribe`.
- Added tests for transcription service, ffmpeg extraction path, rights-confirmation blocking, Whisper failure handling, API behavior, and output structure.
- Created `docs/BLOCK_3_WHISPER_TRANSCRIPT_PIPELINE.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 49 passed.
- Ran real manual transcription proof on the downloaded Showreel audio-only file using Whisper model `tiny`.
- Confirmed transcript artifacts were created under `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/`.
- Confirmed Block 3 did not add AI summary API, Chrome extension, desktop wrapper, batch processing, cookies/login, auth, database, online service behavior, or advanced download hardening.
- User accepted Block 3 and authorized Block 4 Processing UI + MVP Flow.
- Updated `src/universal_media_extractor/static/index.html` with MVP flow tracker, selected-format summary, Whisper model selector, generated-files card, transcript preview, and copy action buttons.
- Updated `src/universal_media_extractor/static/app.js` to manage the end-to-end UI flow, selected format state, download/transcribe states, model selection, transcript preview, and clipboard actions.
- Updated `src/universal_media_extractor/static/styles.css` for the flow tracker, selector, generated-files card, preview, and action buttons.
- Updated `TranscriptionResult` to include `transcript_text` and `summary_prompt_text` for browser preview/copy behavior.
- Updated API/static tests for Block 4 UI labels and transcription content fields.
- Created `docs/BLOCK_4_PROCESSING_UI_MVP_FLOW.md`.
- Updated `docs/ROADMAP_GOVERNANCE.md` to reflect Block 4 as the latest approved block.
- Ran `.venv/bin/python -m pytest -q`; result: 49 passed.
- Ran manual end-to-end API proof on `https://youtu.be/UUdxAp3kuKA`: analyze, download audio-only format `140`, transcribe with Whisper model `tiny`, and verify generated transcript artifacts.
- Saved Block 4 proof artifacts under `proof/block_4/`.
- Confirmed visual browser automation was unavailable because the `playwright` module was not found.
- Confirmed Block 4 did not add job/progress/cancel, batch processing, extension, desktop wrapper, AI summary API, auth/database/cookies, React/Vite, CDN assets, advanced download hardening, or roadmap changes.
- User authorized Block 5 MVP Integration / Readiness Review.
- Ran `.venv/bin/python -m pytest -q`; result: 49 passed.
- Started the backend on `127.0.0.1:8000` for MVP smoke testing.
- Fetched `/` and `/static/app.js` as UI smoke artifacts.
- Ran manual MVP smoke test on `https://youtu.be/UUdxAp3kuKA`: analyze, download audio-only format `140`, transcribe with Whisper model `tiny`, and verify transcript outputs.
- Verified output structure includes media, metadata, logs, `transcript.txt`, `transcript.md`, `transcript.json`, and `summary_prompt.md`.
- Saved Block 5 proof artifacts under `proof/block_5/`.
- Stopped the backend after the smoke test.
- Fixed only readiness text mismatches: replaced stale `later phase` UI wording, removed stale README `next phase` wording, and updated roadmap governance to Block 5.
- Created `docs/MVP_KNOWN_LIMITATIONS.md`.
- Created `docs/BLOCK_5_MVP_READINESS_REVIEW.md`.
- Updated README with Quick Start, MVP flow, output location, and current limitations.
- Confirmed Block 5 did not add new features, job/progress/cancel, batch, extension, desktop wrapper, AI summary API, auth/database/cookies, React/Vite/CDN, advanced download hardening, or roadmap changes.
- User authorized Block 6 Job / Progress / Cancel for long-running download/transcription.
- Extended `Job` with current step, optional progress, result, started/finished timestamps, and cancellation state.
- Hardened `JobService` with lock-protected in-memory state and helpers for running, finishing, failing, step updates, and cancellation.
- Updated `POST /download` and `POST /transcribe` to return `Job` and run local operations in background threads.
- Added `POST /jobs/{job_id}/cancel`.
- Updated the static UI to poll `GET /jobs/{job_id}`, show job status/current step, and expose cancel buttons for download/transcription jobs.
- Updated API/static tests for job-based download/transcription behavior and cancel endpoint behavior.
- Created `docs/BLOCK_6_JOB_PROGRESS_CANCEL.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 51 passed.
- Ran manual job-based API proof on `https://youtu.be/UUdxAp3kuKA`: analyze, download audio-only format `140`, poll download job, transcribe with Whisper model `tiny`, poll transcribe job, and verify transcript outputs.
- Saved Block 6 proof artifacts under `proof/block_6/`.
- Confirmed Browser visual verification was attempted but blocked by Browser plugin local URL security policy.
- Confirmed Block 6 did not add batch, extension, desktop wrapper, AI summary API, auth/database/cookies, Redis/Celery/external queue, React/Vite/CDN, advanced download hardening, or roadmap changes.
- User authorized Block 7 Local File Input.
- Added `LocalFileAnalyzeResult`, `LocalFileStreamInfo`, and `LocalMediaType`.
- Added `LocalFileMetadataService` using `ffprobe`.
- Added local output directory creation under `outputs/local_<timestamp>_<safe_filename>/`.
- Added `POST /local/analyze` for uploaded local file metadata analysis.
- Added `POST /local/transcribe` for job-based transcription of a saved local file reference.
- Updated the static UI with URL mode and Local file mode.
- Added local metadata display, local rights confirmation, local Whisper model selection, and local transcription job polling.
- Added tests for local file metadata service, local output structure, local upload analysis, local transcription jobs, invalid local files, and static UI wiring.
- Ran `.venv/bin/python -m pytest -q`; result: 59 passed.
- Created a synthetic 2-second sine-wave WAV under `proof/block_7/` and used it for manual local file proof.
- Verified `/local/analyze` and `/local/transcribe` on the synthetic WAV; transcript artifacts were created under `outputs/local_20260530T134814Z_synthetic_sine/`.
- Created `docs/BLOCK_7_LOCAL_FILE_INPUT.md`.
- Confirmed Block 7 did not add batch, extension, desktop wrapper, AI summary API, auth/database/cookies, Redis/Celery/external queue, React/Vite/CDN, advanced cancellation, or roadmap changes.
- User authorized Block 8 Cleanup / Output Management.
- Added output models: `OutputSummary`, `OutputListResult`, and `OutputDeleteResult`.
- Extended `OutputManager` with output listing, output summary, and safe delete methods.
- Added local API endpoints `GET /outputs`, `GET /outputs/{output_id}`, and `DELETE /outputs/{output_id}`.
- Added a static UI `Recent results` block with output badges, copy path, and delete actions.
- Added tests for output indexing, artifact detection, total size/files count, safe delete, unsafe delete blocking, API endpoints, and UI static labels.
- Ran `.venv/bin/python -m pytest -q`; result: 68 passed.
- Ran manual proof with a dedicated dummy output under `outputs/block8_dummy_output/`.
- Confirmed the dummy output was deleted through `DELETE /outputs/block8_dummy_output`.
- Confirmed existing real output `outputs/local_20260530T134814Z_synthetic_sine/` and its transcript were not damaged.
- Saved Block 8 proof artifacts under `proof/block_8/`.
- Created `docs/BLOCK_8_OUTPUT_MANAGEMENT.md`.
- Confirmed Block 8 did not add batch deletion, automatic proof cleanup, extension, desktop wrapper, AI summary API, auth/database/cookies, Redis/Celery/external queue, React/Vite/CDN, advanced progress parsing, or roadmap changes.
- Created `docs/ROADMAP_V2.md`.
- Updated roadmap governance after Block 8 completion.
- Recorded Blocks 1-8 as completed.
- Recorded Block 9 Real Progress / Subprocess Cancellation Hardening as the current next planned block, not started.
- Recorded that Codex recommendations are recommendations only and roadmap changes require user confirmation.
- Confirmed this documentation update did not start a new functional block or change implementation code.
- User authorized Block 9 Real Progress / Subprocess Cancellation Hardening.
- Added active subprocess tracking to `JobService`.
- Updated job cancellation to attempt `terminate()` and fallback `kill()` for registered running subprocesses.
- Updated `DownloadService` to use `subprocess.Popen([...], shell=False)`, register active `yt-dlp`, parse practical `yt-dlp` progress lines, and update job steps.
- Updated `TranscriptionService` to use `subprocess.Popen([...], shell=False)`, register active `ffmpeg`/Whisper subprocesses, and update honest step-based transcription states.
- Updated static UI job rendering to show progress percent when present and hide cancel actions outside queued/running states.
- Added/updated tests for subprocess cancellation, kill fallback, already-finished subprocess handling, `yt-dlp` progress parsing, transcription step updates, API job context, and UI progress labels.
- Ran `.venv/bin/python -m pytest -q`; result: 73 passed.
- Ran manual Block 9 proof on `https://youtu.be/UUdxAp3kuKA`: analyze, download audio-only format `140`, transcribe with Whisper model `tiny`, verify output files, and save artifacts under `proof/block_9/`.
- Ran controlled cancellation proof with `/bin/sh -c "sleep 30"` and confirmed the registered subprocess stopped with return code `-15`.
- Created `docs/BLOCK_9_PROGRESS_CANCELLATION_HARDENING.md`.
- Updated Roadmap v2/governance and project memory to mark Blocks 1-9 completed and Block 10 as next planned, not started.
- Confirmed Block 9 did not add batch, extension, desktop wrapper, AI summary API, auth/database/cookies, Redis/Celery/external queue, React/Vite/CDN, browser verification tooling, persistent job storage, or roadmap changes.
- User authorized Block 10 Browser Verification / UI QA Tooling.
- Checked Playwright tooling availability; Python Playwright was missing, while Node/npx was available.
- Checked current Playwright Python documentation through Context7.
- Installed `playwright==1.60.0` in `.venv` and added it to `requirements.txt`.
- Installed Playwright Chromium browser binaries through `.venv/bin/python -m playwright install chromium`.
- Verified `.venv/bin/python -m playwright --version`; result: `Version 1.60.0`.
- Verified headless Chromium can launch from the current Mac environment.
- Created `scripts/browser_smoke.py` as a standalone Playwright smoke script.
- Ran `.venv/bin/python -m pytest -q`; result: 73 passed.
- Ran the backend on `127.0.0.1:8000` and executed `.venv/bin/python scripts/browser_smoke.py`.
- Confirmed browser smoke opened the local UI, filled the user URL, clicked Analyze, waited for `Showreel`, verified audio/video/combined groups, and saved screenshots.
- Saved Block 10 screenshots under `proof/block_10/`.
- Created `docs/BLOCK_10_BROWSER_VERIFICATION.md`.
- Updated Roadmap v2/governance and project memory to mark Blocks 1-10 completed and Block 11 as next planned, not started.
- Confirmed Block 10 did not add download/transcribe changes, API changes, desktop wrapper, Chrome extension, React/Vite/CDN, AI summary API, auth/database/cookies, or roadmap changes.
- User requested a UI simplification pass without starting a new roadmap block.
- Simplified the static format selection UI into `Audio`, `Video`, and `Subtitles` categories.
- Hid format options until the user chooses an output category.
- Simplified audio rows to container plus approximate file size.
- Simplified video rows to container, quality, and approximate file size.
- Hid video options below `1080p` in the UI.
- Simplified subtitle empty state and compacted user-facing warnings.
- Updated `scripts/browser_smoke.py` to verify the simplified category tabs.
- Created `docs/UI_SIMPLIFICATION_PASS.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 73 passed.
- Ran browser smoke with `--proof-dir proof/ui_simplification` and saved updated screenshots.
- Confirmed this pass did not change backend endpoints, models, download/transcription logic, desktop wrapper, extension, AI summary, batch processing, React/Vite/CDN, or roadmap.

## 2026-05-30 - UI Dedup Fix

- User requested a bugfix / UX refinement to remove duplicate Video and Subtitles options without creating a new roadmap block.
- Added `src/universal_media_extractor/static/option_normalizer.js` for user-facing Audio / Video / Subtitles option normalization.
- Connected the static UI to deduplicated format picker data without changing backend endpoints or API contracts.
- Collapsed video rows by user-facing container and quality, keeping one best option per row.
- Kept video options below `1080p` hidden from the UI.
- Collapsed subtitles/captions by language and manual/automatic type.
- Merged multiple subtitle formats into one option instead of rendering duplicate rows.
- Added UI helper tests for duplicated video options and duplicated subtitle options.
- Updated static endpoint tests for the new normalizer asset.
- Created `docs/UI_DEDUP_FIX.md`.
- Ran `.venv/bin/python -m pytest -q`; result: 76 passed.
- Ran a Playwright browser proof against `http://127.0.0.1:8000/` and saved screenshots under `proof/ui_dedup_fix/`.
- Confirmed the Showreel UI now shows one visible video option for `MP4 · 1080p · 12.23 MB` and no duplicate subtitle rows.

## 2026-05-30 - v0 UI Reference Port

- User requested a UI refinement using the downloaded v0 project as a visual reference, not a new roadmap block.
- Found the v0 reference at `/Users/aleksandr/Documents/Codex/universal-media-extractor/media-extractor-ui`; the user-provided path under `Projects/universal-media-extractor` was not present.
- Audited the v0 project as a Next.js App Router / React / TypeScript / Tailwind / shadcn-style UI with mock data.
- Checked current Next.js, Tailwind, and shadcn/ui structure notes through Context7 before making the transfer decision.
- Created `docs/V0_UI_REFERENCE_AUDIT.md`.
- Kept the main app as FastAPI plus static HTML/CSS/vanilla JS.
- Reworked `src/universal_media_extractor/static/styles.css` into a compact downloader/file-manager layout inspired by the v0 sidebar/main-content structure.
- Updated small UI copy in `index.html` without changing endpoint wiring.
- Updated `app.js` so the first available output category opens after analysis instead of leaving the selector empty.
- Preserved existing `/analyze`, `/download`, `/transcribe`, `/jobs`, `/outputs`, URL flow, local file flow, job polling, cancel, safe delete, and copy actions.
- Created `docs/V0_UI_PORT.md`.
- Ran `node --check` on `app.js` and `option_normalizer.js`.
- Ran `.venv/bin/python -m pytest -q`; result: 76 passed.
- Ran browser smoke against `http://127.0.0.1:8000/` and saved screenshots under `proof/v0_ui_port/`.
- Saved additional UI proof screenshots for output selector and recent results.

## 2026-05-30 - Simplified Download Action UI

- User requested removing the visible confirmation step from the download card.
- Removed the visible rights confirmation checkbox from the URL download panel.
- Removed the visible rights confirmation checkbox from local file transcription panel.
- Kept the existing backend request contract by sending `user_confirmed_rights=true` from simplified UI actions.
- Updated the flow checklist to remove the `Confirm rights` step.
- Download button is now enabled after selecting an output option.

## 2026-05-30 - Video-Only Transcription Guard

- User reported a transcription failure after downloading a `Video only` MP4 option.
- Confirmed the downloaded file has no audio stream, so `ffmpeg` audio extraction cannot succeed.
- Updated the static UI so successful video-only and subtitles downloads do not reveal the Whisper transcription panel.
- Added a concise download hint telling the user to choose `Audio` when they want a transcript.
- Added a static JS regression assertion for the video-only transcription guard.
- Ran `node --check` on static JavaScript files.
- Ran `.venv/bin/python -m pytest -q`; result: 76 passed.
- Saved proof screenshot under `proof/transcription_video_only_guard/`.

## 2026-05-30 - Video Downloads Include Audio

- User clarified that every `Video` download must be a single merged video+audio file.
- Updated `DownloadService` so `mode=video` uses `selected_format_id+bestaudio/best` instead of downloading a silent video-only stream.
- Added output container handling for `mode=video` and `mode=combined` through `--merge-output-format` and `--remux-video`.
- Updated the UI helper text from `Video only` to `Downloads with audio`.
- Allowed the Transcribe panel after successful `Video` downloads because the downloaded output should now include audio.
- Added a regression test for the yt-dlp video+audio format selector.

## 2026-05-30 - Output Format Selector

- User requested choosing common output formats instead of accepting whatever container yt-dlp picks.
- Added a `Format` selector to the download card.
- Added Video choices: `MP4`, `MKV`, `WEBM`.
- Added Audio choices: `M4A`, `MP3`, `WAV`.
- Added Subtitle choices: `SRT`, `VTT`.
- Added `DownloadRequest.output_format` and backend command mapping for video remux, audio extraction/conversion, and subtitle conversion.

## 2026-05-30 - Transcript Output Simplification

- User requested a much smaller transcript result UI and saving only one selected transcript format.
- Added transcript format selectors for URL and local file transcription: `TXT`, `Markdown`, and `JSON`.
- Added `TranscriptionRequest.transcript_format` and local transcription request support.
- Updated `TranscriptionService` to save only the selected transcript format into the result folder.
- Moved Whisper intermediate output into hidden `.work/whisper`.
- Removed automatic `summary_prompt.md` generation from normal transcription output.
- Simplified transcript/result rendering to show only status, saved transcript filename, folder, media file, and selected transcript.
- Added regression tests for single-format transcript output.

## 2026-05-30 - Download Location Setting

- User requested saving downloads to the standard Downloads folder or changing the target on demand.
- Changed the default URL download base folder to `~/Downloads/Universal Media Extractor`.
- Added a compact `Save to` field to the download card.
- Sent the selected output base folder through the existing `DownloadRequest.output_base_dir` contract.
- Updated `/download` so `Recent results` follows the selected output base folder.
- Added `DownloadRequest.source_title` so URL download result folders can be named from the video/audio title.
- Moved URL download media/subtitle files directly into the result folder instead of a visible `media/` subfolder.
- Moved URL download service artifacts into hidden `.metadata` and `.logs` folders.
- Created `docs/DOWNLOAD_LOCATION_SETTINGS.md`.


## 2026-08-05 - Commercial Block 3 Preset Output Selection

- Replaced the public URL output picker with preset-based choices: `Best Video`, `1080p`, `Smaller Video`, `Audio M4A`, `Audio MP3`, `Subtitles`, and disabled planned `Archive Pack`.
- Kept raw `format_id` values internal while preserving existing `/download` behavior.
- Moved technical stream rows behind an `Advanced details` disclosure.
- Added frontend normalizer tests for preset construction, missing preset states, and internal id preservation.
- Updated browser smoke script to verify presets instead of old Audio/Video/Subtitles tabs.
- Created `docs/COMMERCIAL_BLOCK_3_PRESET_OUTPUT_SELECTION.md`.
- Verified with `node --check` for static JS files and `.venv/bin/python -m pytest -q`; result: 111 passed.
- Verified browser smoke on `127.0.0.1:8766`; screenshots saved under `proof/commercial_block_3_presets/`.


## 2026-08-05 - Commercial Block 4 Localhost Security Hardening

- Added a random session token to the local FastAPI app and exposed it to the same-origin UI through `/config`.
- Updated static UI requests to send `X-UME-Session-Token` on protected API calls without storing it persistently.
- Added local host/origin checks and explicit local-only CORS settings.
- Added a default local upload size limit and partial-file cleanup for oversized uploads.
- Added API tests for missing/invalid token, rejected cross-origin requests, local-origin success, CORS preflight, and upload size limits.
- Created `docs/COMMERCIAL_BLOCK_4_LOCALHOST_SECURITY.md`.
- Verified with `node --check src/universal_media_extractor/static/app.js`.
- Verified with Python py_compile for API schemas, API app, and API tests.
- Verified with `.venv/bin/python -m pytest -q`; result: 117 passed.
- Verified browser smoke on `127.0.0.1:8766`; screenshots saved under `proof/commercial_block_4_security/`.


## 2026-08-05 - Commercial Block 5 SQLite Jobs And History

- Added optional SQLite persistence to `JobService` and enabled it for the FastAPI app at `data/jobs.sqlite3`.
- Added persisted job fields for status, progress, error, result, timestamps, and retry linkage.
- Added startup recovery for interrupted queued/running jobs.
- Added `GET /jobs`, `POST /jobs/{job_id}/retry`, and `DELETE /jobs/history`.
- Added tests for restart persistence, error/progress/result persistence, interrupted recovery, retry, and clear-history behavior.
- Created `docs/COMMERCIAL_BLOCK_5_SQLITE_JOBS_HISTORY.md`.
- Verified with targeted API/job tests; result: 57 passed.
- Verified with `.venv/bin/python -m pytest -q`; result: 129 passed.
- Verified static JS with `node --check src/universal_media_extractor/static/app.js`.


## 2026-08-05 - Commercial Block 6 Output Templates And Duplicate Handling

- Added `DownloadRequest.output_template`, `duplicate_policy`, `project_name`, `channel_name`, and `playlist_index`.
- Added output folder template rendering with `{source}`, `{channel}`, `{date}`, `{title}`, `{project}`, and `{playlist_index}` tokens.
- Added macOS/Windows-safe output folder sanitization and `--windows-filenames` for `yt-dlp` downloads.
- Added duplicate handling: `rename`, `skip`, and `overwrite`.
- Added `POST /outputs/{output_id}/reveal` for managed output folders.
- Added compact UI controls for name template, duplicate behavior, and Reveal in Finder.
- Added regression tests for templates, duplicate policies, safe reveal, and download command safety.
- Created `docs/COMMERCIAL_BLOCK_6_OUTPUT_TEMPLATES_DUPLICATES.md`.
