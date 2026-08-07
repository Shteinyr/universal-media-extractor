# Windows Production Build Path

Status: planning/readiness document. No Windows installer implementation was added in this pass.

## Goal

Prepare the path for a future Windows 10/11 x64 desktop build of Universal Media Extractor without changing the current macOS/dev workflow.

## Target Behavior

Future Windows build should:

- launch without a terminal window;
- start and stop the local backend with the desktop app lifecycle;
- bind only to `127.0.0.1`;
- open the same static UI inside a desktop shell;
- use Windows-safe output paths and filenames;
- save outputs under the user-selected folder or a default user Downloads folder;
- reveal saved files in File Explorer;
- preserve SQLite-backed job/history data across app restarts.

## Candidate Packaging Path

Recommended path for first Windows beta:

1. Validate the current Python backend and static UI on Windows.
2. Use PyInstaller or an equivalent Python desktop packaging tool for the app bundle.
3. Bundle runtime dependencies needed by the app.
4. Confirm `yt-dlp`, `ffmpeg`/`ffprobe`, and Whisper strategy for Windows:
   - bundled binaries, or
   - first-run dependency check with install instructions.
5. Build a signed installer:
   - EXE or MSI for direct download first;
   - MSIX later for Microsoft Store evaluation.
6. Test install, launch, uninstall, output folders, and update behavior on Windows 10/11 x64.

## Required Future Inputs

- Windows build machine or CI runner.
- Code-signing certificate.
- Installer tooling decision.
- Antivirus false-positive mitigation notes.
- Windows privacy/support copy.
- Store policy review if Microsoft Store is pursued.

## Validation Matrix

Future Windows QA must cover:

- clean install;
- launch from Start Menu/Desktop shortcut;
- local UI opens without terminal;
- URL analyze/download/transcribe on authorized media;
- local file analyze/transcribe;
- batch import/download;
- cancel/retry recovery;
- reveal in File Explorer;
- uninstall leaves user output files intact;
- 200% display scaling;
- narrow and maximized window layouts;
- non-admin user account.

## Current Status

Prepared:

- cross-platform backend structure;
- static UI;
- SQLite job/history system;
- output templates and safe filename handling;
- reveal/open abstraction in backend services;
- public docs and limitations copy.

Not prepared yet:

- Windows production bundle;
- Windows installer;
- Windows code signing;
- Windows runtime dependency packaging;
- Microsoft Store package;
- Windows-specific QA proof.
