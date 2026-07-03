# Project Memory Requirements

Date: 2026-05-29

## Goal

Keep project knowledge durable outside the chat context so future Codex sessions do not accidentally start implementation, repeat research, or lose Phase 0 constraints.

## Required Structure

| Path | Purpose | Update Rule |
|---|---|---|
| `AGENTS.md` | Persistent Codex instructions and stop gate | Update when project rules change |
| `PROJECT_STATE.md` | Short current memory and status | Read before work; update after meaningful stages |
| `DECISIONS.md` | Decision log | Append when user or audit makes a durable decision |
| `CHANGELOG.md` | Chronological change history | Update after file changes or project stages |
| `README.md` | Public-facing short project description | Update when project status changes |
| `audits/` | Feasibility, capability, risk audit artifacts | Add immutable-ish audit docs; revise only with dated notes |
| `docs/` | Future specs, source notes, user docs | Use after Phase 0 if user authorizes planning |

## Memory Rules

- Do not rely only on chat context.
- Record sources for feasibility claims.
- Separate confirmed, partial, blocked, and unknown capabilities.
- Record user decisions before changing scope.
- Keep implementation plans out of Phase 0 unless the user gives GO or CONDITIONAL GO.

## Recommended Future Additions

Only after the user authorizes the next phase:

- `docs/SCOPE.md`
- `docs/LEGAL_AND_PLATFORM_LIMITS.md`
- `docs/DEPENDENCY_MATRIX.md`
- `docs/TEST_STRATEGY.md`
- `docs/OUTPUT_STRUCTURE.md`

These are not created now because Phase 0 should stop at audit and decision.

