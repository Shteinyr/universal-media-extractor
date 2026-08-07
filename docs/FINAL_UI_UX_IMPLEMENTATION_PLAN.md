# Final UI/UX Implementation Plan

Date: 2026-08-07

Source spec:

- `docs/UNIVERSAL_MEDIA_EXTRACTOR_FINAL_UI_UX_COMMERCIAL_SPEC.md`

This document turns the GPT Pro final UI/UX commercial spec into executable project work. It does not implement UI/backend changes.

## Decision

The GPT Pro final spec is accepted as the current UI/UX direction for public beta planning, but it is not an automatic permission to rewrite the whole product in one pass.

Recommended final product structure:

```text
New task -> Queue -> Library -> Settings
```

Important implications:

- `Link / File / Batch` should no longer be the primary user mental model.
- The first public screen should be a unified `New task` composer.
- Course/Udemy is internal/experimental and must not appear in public commercial builds.
- Video presets must represent one final playable file with video plus audio.
- Main UI must stay preset-driven and avoid raw engine details.

## First Executable Block

First implementation block:

```text
Public Beta UI/UX Refactor Block 1
```

Included tasks:

1. Public build Course surface removal hardening.
2. Backend source-of-truth audit and endpoint inventory.
3. Universal New Task composer.
4. Stable semantic preset resolver.

Why these four together:

- They address the biggest GPT Pro conflicts before visual polish.
- They do not require Apple Developer Program access.
- They do not require payments, licensing, or installers.
- They produce the largest visible improvement toward the final public beta product.
- They create the foundation for later Queue/Library and Settings work.

## Later Tasks

Do after Block 1:

1. Durable Queue and Library finalization.
2. Native filesystem integration.
3. Unified progress, cancel, retry, and recovery.
4. Error normalization and diagnostics final pass.
5. Result and local transcription UX final pass.
6. Commercial desktop readiness final pass.

## GitHub Tracking

Old closed GitHub issues remain closed. They represented earlier acceptance criteria that were completed at that time.

The GPT Pro final spec creates stricter public-beta tasks. These should be tracked as new issues linked to the earlier work where relevant.

Tracker issue:

```text
#41 [UI/UX] Final public beta UX refactor tracker
```

Milestone:

```text
Public Beta Readiness
```

Created GitHub issues:

| Issue | Priority | Planned order | Track |
| --- | --- | --- | --- |
| #41 `[UI/UX] Final public beta UX refactor tracker` | P0 | Tracker | Strategy |
| #42 `[P0] Public build Course surface removal hardening` | P0 | Block 1 | Security |
| #43 `[P0] Backend source-of-truth audit and endpoint inventory` | P0 | Block 1 | QA |
| #44 `[P0] Universal New Task composer` | P0 | Block 1 | Strategy |
| #45 `[P0] Stable semantic preset resolver` | P0 | Block 1 | Presets |
| #46 `[P0] Durable Queue and Library finalization` | P0 | Later | Jobs |
| #47 `[P0] Native filesystem integration` | P0 | Later | Output |
| #48 `[P0] Unified progress, cancel, retry, recovery` | P0 | Later | Jobs |
| #49 `[P0] Error normalization and diagnostics final pass` | P0 | Later | Diagnostics |
| #50 `[P1] Result and local transcription UX final pass` | P1 | Later | Output |
| #51 `[P1] Commercial desktop readiness final pass` | P1 | Later | Packaging |

## Block 1 Acceptance Criteria

- Public mode has no visible or reachable Course/Udemy surface.
- Current backend/source-of-truth docs match the actual implementation.
- First screen uses `New task`, not top-level Link/File/Batch mode tabs.
- Single URL routes to URL analysis.
- Local audio/video file routes to local file analysis.
- Multiple URLs route to batch review.
- Invalid input shows a visible inline error.
- Video presets are unique, honest, and user-facing.
- `Smaller video` is replaced with a clearer `Up to 720p` concept.
- Video output is one playable video+audio file where supported.
- Main UI does not show raw stream IDs, codec strings, or raw CLI details.

## Verification Commands For Block 1

```bash
node --check src/universal_media_extractor/static/app.js
node --check src/universal_media_extractor/static/option_normalizer.js
.venv/bin/python -m pytest -q
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/final_ui_ux_refactor_block_1
```

## Out Of Scope For Block 1

- Native filesystem bridge.
- Windows installer.
- Apple signing/notarization.
- Licensing/payments.
- Full Queue/Library rewrite.
- AI summary.
- Chrome extension.
- Public Course/Udemy support.
