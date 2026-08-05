# Decisions

## 2026-05-29

- Start with a local web app rather than an online service.
- Use local processing as the default direction: `yt-dlp` for URL analysis/download, `ffmpeg` for media conversion/extraction, and local Whisper CLI for transcription.
- Do not use paid APIs at the start.
- Defer desktop wrapper until after local web-app feasibility is proven.
- Defer Chrome extension integration until after local app feasibility is proven.
- Do not begin implementation until the Phase 0 audit ends with GO or CONDITIONAL GO.
- Phase 0 verdict is CONDITIONAL GO.
- The project must not claim guaranteed universal URL support; it must present URL extraction as best-effort support through `yt-dlp`.
- Cookies/login handling must be optional, explicit, and user-controlled.
- DRM, CAPTCHA, paywall bypass, and unauthorized access are out of scope.
- Local-file processing remains a core capability even when URL extraction fails.
- Future performance alternatives are `faster-whisper` and `whisper.cpp`, not paid APIs by default.
- User accepted the CONDITIONAL GO constraints and authorized Phase 1 environment setup/proof checks only.
- Cookies/login are future manual options and are not part of Phase 1.
- Phase 1 must not create backend app code, frontend code, routes, UI, downloader module, transcription module, Chrome extension, or desktop wrapper.
- Phase 3 data contract uses a normalized `AnalyzeResult` instead of exposing raw `yt-dlp` JSON directly to the future UI.
- Future FastAPI analyze responses should use Pydantic response models for validation, serialization, and OpenAPI schema generation.
- Raw `yt-dlp` JSON should be stored as an artifact and referenced through `raw_reference_path`, not embedded in the main response.
- Future download/process actions must require `legal_safety.user_confirmed_rights == true`.
- Phase 4 models use Pydantic v2 with `extra="forbid"` to keep the normalized API contract stable.
- Phase 4 adds `pytest` as a development/test dependency.
- Phase 4 does not authorize FastAPI app creation or routes; it implements models only.
- Phase 5 normalizer is pure with respect to media operations: it accepts an already-loaded raw `yt-dlp` dict and does not call CLI tools, download media, or write artifacts.
- Phase 5 keeps raw `yt-dlp` JSON outside `AnalyzeResult`, using only `raw_reference_path`.
- Phase 5 groups formats into audio-only, video-only, and combined options while ignoring storyboard/helper formats.
- Phase 6 analyzer may call `yt-dlp` only as `yt-dlp --simulate --dump-json URL`.
- Phase 6 analyzer must use subprocess list arguments with `shell=False`.
- Phase 6 analyzer saves raw JSON only when `raw_output_dir` is explicitly provided.
- Phase 6 manual script exists for explicit user-authorized manual proof only and was not run during implementation.
- Phase 7 manually verified the safe analyzer wrapper on the user-authorized URL and still performed analysis only.
- Phase 8 defines services before routes: `AnalyzeService`, minimal `OutputManager`, minimal `JobService`, and minimal `SafetyService` are the first MVP service boundary.
- Phase 8 keeps `DownloadService`, `TranscriptionService`, `LocalFileMetadataService`, and advanced `SettingsService` for later phases.
- The first MVP UI boundary is analysis display only: URL analyze, normalized result, warnings/errors, and no download or Whisper on the first UI prototype.
- Future API endpoints are draft-only until explicitly authorized; no FastAPI app or routes exist after Phase 8.
- Phase 10 FastAPI backend is local-only and must be run through Uvicorn bound to `127.0.0.1`.
- Phase 10 API is limited to analysis-only routes: `/health`, `/analyze`, and `/jobs/{job_id}`.
- Phase 10 does not add auth, database, cookies/login, downloader, transcription, frontend, extension, desktop wrapper, or online service behavior.
- Phase 12 frontend plan keeps the first UI as analysis-result display only: paste URL, analyze, show normalized result.
- Phase 12 recommends static HTML/CSS/vanilla JS for the first UI prototype to avoid build tooling and keep the first loop minimal.
- Phase 13, if authorized, must not add download, Whisper, local file upload, settings page, auth, database, cookies/login, extension, desktop wrapper, or advanced styling overwork.
- After Phase 15, new work must use large blocks rather than new Phase numbers unless the user explicitly authorizes new Phase numbering.
- Phase 13 through Phase 15 are treated as subitems of the completed analysis-only block.
- Block 2 is the approved Download + Output Pipeline block.
- Download/process actions must require `user_confirmed_rights=true`.
- `DownloadService` uses `yt-dlp` through subprocess list arguments with `shell=False`.
- Download outputs are stored in structured folders with `media/`, `metadata/`, and `logs/`.
- Block 2 does not add Whisper/transcription, local file upload, cookies/login, auth, database, extension, desktop wrapper, online service behavior, or AI summary.
- Block 3 is the approved Whisper + Transcript Pipeline block.
- Transcription/process actions must require `user_confirmed_rights=true`.
- `TranscriptionService` uses local Whisper CLI through subprocess list arguments with `shell=False`.
- Video transcription uses local `ffmpeg` audio extraction before Whisper.
- Transcript artifacts are stored in the existing output directory under `transcripts/`.
- Block 3 creates `summary_prompt.md` only; it does not call an AI summary API.
- Block 3 does not add Chrome extension, desktop wrapper, batch processing, cookies/login, auth, database, online service behavior, or advanced download hardening.
- Block 4 is the approved Processing UI + MVP Flow block.
- Block 4 must unify the existing UI around Analyze -> Select format -> Confirm rights -> Download -> Transcribe -> Result.
- Block 4 reuses existing `/analyze`, `/download`, and `/transcribe`; no new endpoint is needed for the MVP flow.
- Browser UI cannot open local folders directly; it should show and copy output paths instead of adding desktop/native behavior.
- `TranscriptionResult` may include transcript and summary prompt text so the static browser UI can preview/copy generated content.
- Block 4 does not add job/progress/cancel, batch processing, Chrome extension, desktop wrapper, AI summary API, auth/database/cookies, React/Vite, CDN assets, advanced download hardening, or roadmap changes.
- Block 5 is the approved MVP Integration / Readiness Review block.
- Block 5 is a review/readiness block, not a feature block.
- Block 5 may fix only obvious text/flow bugs and documentation mismatches.
- The current MVP remains a local single-user best-effort tool.
- Browser screenshot/interaction proof is not required when browser automation is unavailable, but the limitation must be recorded.
- Further roadmap blocks require explicit user authorization.
- Block 6 is the approved Job / Progress / Cancel block.
- Block 6 changes `/download` and `/transcribe` to return in-memory `Job` objects and run the long operation in a local background thread.
- Block 6 keeps jobs in-memory only; no Redis, Celery, database, external queue, auth, cookies, or online service behavior is added.
- Block 6 cancellation is best-effort: queued jobs can be cancelled immediately, running jobs set `cancel_requested=true`, and active subprocesses are not forcibly killed yet.
- Block 6 progress is coarse status/current-step polling, not parsed `yt-dlp`, `ffmpeg`, or Whisper progress output.
- Block 7 is the approved Local File Input block.
- Local file mode must not use `yt-dlp` or remote URLs.
- Local file analysis uses `ffprobe` only and must not run Whisper.
- Local file transcription reuses the existing in-memory job system and `TranscriptionService`.
- Uploaded local files are copied into project output folders under `outputs/local_<timestamp>_<safe_filename>/`.
- Block 7 does not add batch, extension, desktop wrapper, AI summary API, auth/database/cookies, external queue, React/Vite/CDN, advanced cancellation, or roadmap changes.
- Block 8 is the approved Cleanup / Output Management block.
- User outputs are direct folders under `outputs/`; development proof artifacts under `proof/` are not user outputs.
- Safe delete accepts only an `output_id` direct folder name, never an arbitrary absolute path.
- Safe delete must keep the resolved target inside `outputs/` and must not delete `proof/`, the project root, or the `outputs/` root.
- Block 8 does not add batch deletion, automatic proof cleanup, desktop/native folder opening, auth/database/cookies, external queues, React/Vite/CDN, advanced progress parsing, or roadmap changes.
- Roadmap v2 is documented in `docs/ROADMAP_V2.md`.
- Blocks 1-8 are completed.
- The current next planned block is Block 9. Real Progress / Subprocess Cancellation Hardening, but it must not start without explicit user confirmation.
- Do not create new Phase numbering.
- Do not create new Blocks without explicit user approval.
- Codex recommendations are recommendations only, not roadmap decisions.
- Codex may suggest alternatives if it sees a blocker, risk, or better path.
- Any roadmap change must be presented to the user as a recommendation and must wait for user confirmation.
- If a task is a subtask inside the current block, do not promote it into a new block.
- Follow Roadmap v2 unless the user explicitly changes it.
- Block 9 is the approved Real Progress / Subprocess Cancellation Hardening block.
- Block 9 keeps the existing in-memory job architecture and does not add Redis, Celery, database, external queue, or persistent job storage.
- Running download/transcription jobs may register exactly one active subprocess at a time for cancellation.
- Cancellation remains best-effort but now attempts `terminate()` and then `kill()` when a registered subprocess does not stop promptly.
- If the active subprocess already finished, cancellation must not convert a nearly finished job into cancelled.
- Download progress may parse `yt-dlp` percent when available; missing granular CLI progress must be shown honestly as step-based progress.
- Whisper progress must not be faked; transcription uses honest steps such as `running_whisper` and `generating_transcript_files`.
- Block 9 does not add batch, extension, desktop wrapper, AI summary API, auth/database/cookies, React/Vite/CDN, browser verification tooling, or roadmap changes.
- Block 10 is the approved Browser Verification / UI QA Tooling block.
- Block 10 uses Python Playwright inside the existing `.venv` as the minimal browser automation path.
- Browser smoke is a separate manual/dev command and must not be part of ordinary `pytest`.
- Default browser smoke is analysis-only and must not download or transcribe.
- Optional full-flow browser smoke may exist only behind an explicit `--full-flow` flag.
- Block 10 does not add React, Vite, CDN assets, API changes, download/transcribe logic changes, desktop wrapper, Chrome extension, AI summary API, auth/database/cookies, or roadmap changes.
- Block 11 is the approved Desktop Wrapper block.
- Block 11 uses `pywebview` as a lightweight native window around the existing local FastAPI/static UI app.
- Block 11 keeps browser mode through `scripts/run_api.py` unchanged.
- The desktop launcher starts Uvicorn programmatically on `127.0.0.1` and chooses the next free local port if `8000` is busy.
- Block 11 does not create a signed/notarized `.app`, installer, Chrome extension, Electron app, React/Vite/Next rewrite, AI summary API, batch processing, cookies/login, auth/database, or roadmap change.
- Udemy Course Offline Export was approved by the user as a feature block after Block 11 without renumbering Roadmap v2.
- Udemy course support is `yt-dlp` first and best-effort.
- `Puyodead1/udemy-downloader` was studied as a reference, but is not vendored or shipped in the app because its DRM/decryption-key oriented behavior is outside this app's safety boundary.
- Udemy mode uses Chrome session auth by default and may use a manual user-provided `cookies.txt` path only as an advanced fallback for the current operation.
- The app must not store Udemy passwords, bearer tokens, or cookies in output metadata/logs.
- Udemy mode must not implement DRM bypass, decryption-key handling, CAPTCHA bypass, paywall bypass, or unauthorized access.
- Udemy downloads use the existing local job/poll/cancel system and subprocess list arguments with `shell=False`.
- Udemy Course mode should use Chrome session auth by default via `yt-dlp --cookies-from-browser chrome`.
- Manual `cookies.txt` remains available only as an advanced fallback for cases where browser-cookie access is unavailable.

## 2026-08-05 - Commercial Foundation

- Public product positioning is fixed as `Local Media Downloader & Organizer for macOS and Windows`.
- Public copy must not promise universal website support or DRM/paywall/CAPTCHA/login bypass.
- Udemy Course Mode remains internal/experimental and must be hidden from public builds/marketing unless separately approved.
- Public commercial builds can set `UME_PUBLIC_PRODUCT_MODE=1` to hide Course Mode in the static UI by default.
- Legal, privacy, refund, and public limitation documents are product drafts and must be reviewed before paid public launch.
- Next commercial work should come from the GitHub commercial roadmap, not ad hoc feature expansion.

## 2026-08-05 - Commercial Block 2 Errors And Diagnostics

- Public beta errors should lead with stable user-facing categories, not raw CLI text.
- Technical CLI output may remain available as collapsible/redacted diagnostics.
- Diagnostics bundles are local JSON responses only; they do not upload support data.
- Diagnostics must exclude cookies, tokens, passwords, transcripts, full URLs, and local filesystem paths by default.
- Commercial Block 2 intentionally does not start payments, stores, signing, packaging, SQLite jobs/history, batch, licensing, or roadmap changes.

## 2026-08-05 - Preset-Based Output Selection

- Public URL output selection should use clear presets instead of raw technical `yt-dlp` format rows.
- The main UI should hide `format_id`, codec strings, fps details, and duplicate stream rows by default.
- Internal download behavior should still preserve the selected `format_id` for `/download`.
- `Archive Pack` is allowed as a visible disabled planned preset, but real Archive Pack execution requires later queue/batch/history work and is not part of Commercial Block 3.

## 2026-08-05 - Localhost Security Hardening

- Protected API operations require an in-memory random session token between the static UI and backend.
- `/config` is the only endpoint that exposes the token to the same-origin UI; the token is not stored in localStorage or files.
- Non-local `Host`/`Origin` requests are rejected and CORS uses explicit local-only settings.
- Local uploads have a size cap and partial oversized uploads are removed.
- Path access remains constrained to managed output operations; arbitrary CLI argument passthrough remains out of scope.


## 2026-08-05 - SQLite Jobs And History

- App-level jobs should persist locally in SQLite at `data/jobs.sqlite3` for the current development product.
- `JobService()` can still run in-memory when no database path is supplied for isolated service tests and narrow usage.
- Queued/running jobs found on startup are not resumed automatically; they recover to a clear failed, recoverable `interrupted` state.
- Retry creates a new job with the original payload and links it through `retry_of_job_id`.
- Clearing history removes terminal job records only and must not delete output files.


## 2026-08-05 - Output Templates And Duplicate Handling

- Public beta URL downloads should default to readable title-based output folders.
- Advanced naming should use a limited safe template vocabulary: `{source}`, `{channel}`, `{date}`, `{title}`, `{project}`, and `{playlist_index}`.
- User-facing output folder names must be sanitized for macOS and Windows.
- Duplicate behavior defaults to `rename` to avoid accidental data loss.
- `skip` must not run `yt-dlp` when the target output already exists.
- `overwrite` is explicit and only applies inside the managed output base.
- Revealing folders is limited to managed direct output folders and uses OS commands with `shell=False`.

## 2026-08-05 - macOS Production Foundation

- macOS production foundation uses PyInstaller with a checked-in spec file.
- The production-foundation `.app` bundles the Python app/runtime but does not yet include Developer ID signing, notarization, or a DMG installer.
- GUI launches prepend standard Homebrew/system CLI paths so external media engines can be found from Finder-launched apps.
- Public distribution work remains split into separate signing/notarization and installer tasks.

## 2026-08-05 - macOS Signing Readiness

- macOS signing readiness uses Developer ID only for public direct distribution.
- Hardened Runtime is enabled through `codesign --options runtime --timestamp`.
- Notarization uses `xcrun notarytool`, not deprecated `altool`.
- Notary credentials should be stored in macOS Keychain via a named profile; passwords and private keys must not be committed or passed through project files.
- `packaging/macos/entitlements.plist` remains empty until a real signed build proves a specific entitlement is necessary.

## 2026-08-05 - macOS DMG Installer Readiness

- macOS DMG readiness uses a drag-to-Applications layout: app bundle plus `Applications -> /Applications` symlink.
- Local proof DMGs may be unsigned/unnotarized, but public release DMGs must contain a signed/notarized app and should be signed, notarized, stapled, verified, and published with SHA-256 checksum.
- DMG installer work remains separate from Windows packaging, payments, website, and product features.

## 2026-08-05 - macOS Public Release Prep

- Direct public macOS distribution remains gated by an Apple Developer Program account, Developer ID Application certificate, and notarytool credentials.
- The public artifact should be the outermost signed/notarized/stapled DMG, not an unsigned local proof DMG.
- Notary credentials must be stored in macOS Keychain through a profile such as `UME_NOTARY`; passwords and private keys must not be committed or shared in chat.
- Issues #13 and #14 must remain open until real Developer ID signing, notarization, stapling, and Gatekeeper validation pass.
- Udemy Course Mode remains hidden from public commercial builds unless separately approved.

## 2026-08-05 - Founder Launch Surface

- Public founder launch surface should use the existing safe positioning: `Local Media Downloader & Organizer for macOS and Windows`.
- The first public site is a static no-checkout draft under `site/`.
- Public site copy must show best-effort source limitations before download CTAs.
- Udemy Course Mode must not be advertised on the public founder launch site.
- Free / Founder Pro / Pro / Business terms remain drafts until payment provider approval and licensing design are complete.
