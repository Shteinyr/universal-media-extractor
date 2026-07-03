# Roadmap Governance

Date: 2026-05-30

## Current Rule

Do not create new Phase numbering unless the user explicitly authorizes it.

Work is now organized as larger blocks. Microsteps, implementation slices, proofs, and polish passes should be recorded as tasks inside the active block rather than as new phases.

Follow `docs/ROADMAP_V2.md` unless the user explicitly changes the roadmap.

Codex recommendations are recommendations only, not roadmap decisions.

Any roadmap change must be presented to the user as a recommendation and must wait for user confirmation.

Do not create new Blocks without explicit user approval.

If a task is a subtask inside the current block, do not promote it into a new block.

## Legacy Phase Notes

Phase 13 through Phase 15 are considered subitems of the completed analysis-only block:

- static analysis-only UI;
- UI polish/accessibility;
- error-state refinement/testing.

## Completed Blocks

Blocks 1-11 are completed:

- Block 1. Analysis Foundation.
- Block 2. Download + Output Pipeline.
- Block 3. Whisper + Transcript Pipeline.
- Block 4. Processing UI + MVP Flow.
- Block 5. MVP Readiness Review.
- Block 6. Job / Progress / Cancel.
- Block 7. Local File Input.
- Block 8. Cleanup / Output Management.
- Block 9. Real Progress / Subprocess Cancellation Hardening.
- Block 10. Browser Verification / UI QA Tooling.
- Block 11. Desktop Wrapper.

## Current Next Planned Block

The current next planned block is:

```text
Block 12. Chrome Extension
```

Do not start Block 12 until the user explicitly confirms it.

## Constraints To Preserve

- Keep the app local-only.
- Do not add online service behavior.
- Do not add auth, database, cookies/login, Chrome extension, local file upload, AI summary, or batch processing unless explicitly authorized in a later block.
- Block 6 authorized a minimal in-memory job/poll/cancel layer for download and transcription only.
- Block 7 authorized local audio/video file upload, ffprobe metadata, and local transcription through the existing job/transcription system.
- Block 8 authorized indexing and safe deletion of user outputs under `outputs/` only.
- Block 9 authorized practical progress parsing and active subprocess cancellation hardening for the existing job system only.
- Block 10 authorized minimal browser verification tooling and screenshot smoke checks only.
- Block 11 authorized a minimal `pywebview` desktop wrapper only.
- Download/process actions must require `user_confirmed_rights=true`.
- Do not automatically delete `proof/`; it is a development proof artifact area.
- Record block-level decisions, proofs, and limitations in project markdown files.
- After each completed block, update `PROJECT_STATE.md`, `CHANGELOG.md`, `README.md`, and relevant docs.
