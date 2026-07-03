# Universal Media Extractor & Transcriber - Codex Instructions

## Permanent Project Rules

- Always read `PROJECT_STATE.md` before starting work in this project.
- Before every large task, read `PROJECT_CONTEXT.md` if it exists.
- Do not rely only on chat context; persist important facts in project markdown files.
- After every meaningful stage, update `PROJECT_STATE.md` and `CHANGELOG.md`.
- After every completed large block, update `PROJECT_CONTEXT.md`.
- Do not touch unrelated files.
- Do not start implementation without an explicit GO from the user.
- Use Context7 MCP for current documentation about libraries, frameworks, SDKs, APIs, CLI tools, and cloud services.
- Prefer official documentation and primary sources for feasibility decisions.
- Record constraints, decisions, risks, and blockers in markdown files.
- During Phase 0, create only markdown files and the allowed `audits/` and `docs/` directories.

## Current Stop Gate

Implementation, MVP planning, backend code, frontend code, web UI, Chrome extension code, desktop wrapper code, and media downloading are blocked until the user explicitly gives one of:

- GO
- CONDITIONAL GO

If the decision is NO-GO or NEED USER DECISION, continue only with research, clarification, or alternative analysis.
