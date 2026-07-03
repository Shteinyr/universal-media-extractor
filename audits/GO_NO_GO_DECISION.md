# GO / NO-GO Decision

Date: 2026-05-29

## 1. Is The Idea Feasible?

Verdict: **CONDITIONAL GO**

The idea is technically and economically feasible as a local, single-user, best-effort media extractor and transcriber using available local tools. It is not feasible as a guaranteed universal downloader for all sites.

## 2. Can The Original Idea Be Fully Implemented?

Partially.

The local app workflow can be implemented. The word "universal" must be constrained because URL source support depends on `yt-dlp` extractors, platform changes, authentication, cookies, legal rights, and site terms.

## 3. Confirmed Critical Capabilities

- URL analysis through `yt-dlp` for supported sources.
- Format listing before download through `yt-dlp -F` and JSON metadata.
- Audio-only, video-only, video+audio, and subtitle operations where the source supports them.
- Local file analysis and conversion through `ffprobe`/`ffmpeg`.
- Local transcription through Whisper CLI.
- Structured output files through local scripts.
- Local-only backend binding through Uvicorn `127.0.0.1`.
- Process cancellation and status tracking in principle through Python subprocess management and CLI progress output.

## 4. Critical Capabilities Not Fully Confirmed

- Real-world success rate across target sites, because no representative URL test set was run in Phase 0.
- Long-file transcription performance, because no long media benchmark was run.
- Python 3.14 runtime behavior for future app dependencies in this exact venv, because FastAPI/Uvicorn/pywebview are not installed.
- Whisper progress granularity, because Whisper CLI progress is less structured than `yt-dlp` and `ffmpeg`.

## 5. Critical Capabilities Unavailable

- Guaranteed support for every website.
- Guaranteed support for login/CAPTCHA/DRM/paywalled sources.
- Automatic legal/terms compliance for arbitrary URLs.
- Safe automatic browser-cookie extraction without explicit user permission.

## 6. What Can Be Done Through CLI

- `yt-dlp`: analyze, list formats/subtitles, download, extract audio, merge, write metadata, use cookies, show progress.
- `ffmpeg`/`ffprobe`: inspect local media, extract streams, convert formats, emit progress.
- `whisper`: transcribe local audio files and emit `txt`, `vtt`, `srt`, `tsv`, `json`, or all formats.

## 7. What Can Be Done Through Local Scripts

- Orchestrate CLI calls.
- Track jobs and subprocesses.
- Parse JSON/progress logs.
- Create structured folders and markdown artifacts.
- Clean partial files.
- Validate dependencies.
- Enforce local-only security defaults.

## 8. What Is Only UI

- File picker interaction.
- User choices among formats/subtitles/models.
- Human-readable progress and error recovery.
- Manual confirmation for cookies or platform-sensitive actions.

## 9. What Is Manual

- Choosing legally permitted inputs.
- Providing cookies or local files.
- Responding to macOS/browser permission prompts.
- Installing future Chrome Native Messaging host/extension.
- Accepting CPU transcription speed limits or choosing an alternative engine.

## 10. What Is Impossible Or Not Found

- Reliable automation of DRM, CAPTCHA, paywall, or blocked login flows.
- A guarantee that every `yt-dlp` listed extractor works on any given day.
- A no-risk way to download arbitrary YouTube content under platform terms.

## 11. Risks That Can Kill The Project

- The product promise remains "universal" instead of "best-effort local extraction for supported sources."
- The user expects reliable YouTube downloading despite terms and technical countermeasures.
- Local CPU Whisper is too slow for the user's file lengths.
- Disk usage becomes uncontrolled for large videos/intermediates.
- Cookies/login handling creates privacy or security exposure.
- Python 3.14 dependency compatibility causes setup friction.

## 12. Is Another Approach Needed?

No immediate replacement is needed. The primary local approach is viable. Alternative engines such as `faster-whisper` or `whisper.cpp` should remain available if performance or packaging becomes a blocker.

## 13. Should The Project Continue?

Yes, but only as **CONDITIONAL GO**:

- local-first;
- no paid APIs in the core;
- best-effort URL support;
- explicit legal/platform warnings;
- local files fully supported;
- cookies optional and user-controlled;
- no implementation until the user accepts these constraints.

## 14. Next Minimal Safe Step

Ask the user to accept or reject the CONDITIONAL GO constraints. If accepted, the next phase should be planning only, not immediate coding, with a narrow MVP scope and a small user-approved test matrix.

