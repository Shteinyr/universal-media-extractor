# Public Beta UI/UX Refactor Block 1

Date: 2026-08-07

GitHub issues:

- #42 `[P0] Public build Course surface removal hardening`
- #43 `[P0] Backend source-of-truth audit and endpoint inventory`
- #44 `[P0] Universal New Task composer`
- #45 `[P0] Stable semantic preset resolver`

## Result

Public Beta UI/UX Refactor Block 1 is implemented.

The public UI now starts from one `New task` composer instead of forcing the user to think in separate URL/File/Batch modes. Course/Udemy remains internal/experimental and is absent from the public static UI bundle and public product-mode API.

## Course/Public Boundary

Public static UI no longer contains user-facing Course/Udemy/cookie/Chrome-session surfaces.

Public product mode:

```bash
UME_PUBLIC_PRODUCT_MODE=1 .venv/bin/python scripts/run_api.py
```

In this mode:

- `/udemy/analyze` is not registered;
- `/udemy/download` is not registered;
- `/config` reports public product mode and disabled Course mode.

Internal Course mode can still exist for local/experimental builds, but it is not part of public positioning.

## New Task Composer

The composer routes input by content:

- one URL -> normal URL analyze through `/analyze`;
- local audio/video file -> local metadata analyze through `/local/analyze`;
- multiple URLs -> batch import/review through `/batch/import`;
- `.txt` or `.csv` URL list -> batch import/review through `/batch/import`;
- empty or invalid input -> inline composer error.

The large empty first-screen card was replaced with a smaller `New task` empty state.

## Semantic Presets

The public preset resolver now uses stable semantic IDs:

- `best_video` -> Best video;
- `video_1080p` -> 1080p video;
- `video_720p` -> Up to 720p;
- `audio_m4a` -> Audio M4A;
- `audio_mp3` -> Audio MP3;
- `subtitles` -> Subtitles.

`Smaller video` was replaced with the clearer `Up to 720p`. The backend keeps legacy `smaller_video` as a compatibility alias for older batch payloads.

User-facing presets are deduped so repeated equivalent video/audio options do not appear as duplicate choices. The main UI keeps raw stream IDs, codec strings, and raw CLI details out of the normal selection surface.

## Video Behavior

Public video presets represent a playable video result where supported. Download selection still relies on `yt-dlp`/`ffmpeg` availability and may fail clearly if the source cannot provide or combine the requested result.

## Backend Inventory

The current source-of-truth backend inventory is documented in:

- `docs/PUBLIC_BETA_BACKEND_SOURCE_OF_TRUTH.md`

Key clarification: SQLite jobs/history exists, but this is not a full product database. Batch group state remains in-memory and is a follow-up for durable Queue/Library work.

## Verification

Commands run:

```bash
node --check src/universal_media_extractor/static/app.js
node --check src/universal_media_extractor/static/option_normalizer.js
.venv/bin/python -m pytest tests/test_batch_service.py tests/test_ui_option_normalizer.py tests/test_api_app.py -q
.venv/bin/python -m pytest -q
UME_PUBLIC_PRODUCT_MODE=1 .venv/bin/python scripts/run_api.py
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/final_ui_ux_refactor_block_1
```

Results:

- JS syntax checks passed.
- Targeted tests passed: `62 passed`.
- Full pytest passed outside sandbox: `200 passed`.
- Browser smoke passed in public product mode.

Proof screenshots:

- `proof/final_ui_ux_refactor_block_1/ui_initial.png`
- `proof/final_ui_ux_refactor_block_1/ui_analyze_result.png`
- `proof/final_ui_ux_refactor_block_1/ui_output_selected.png`

## Not Changed

- No native filesystem bridge.
- No installer/signing/notarization.
- No licensing/payments.
- No full Queue/Library rewrite.
- No AI summary.
- No Chrome extension.
- No public Course/Udemy support.
- No React/Vite/CDN migration.
- No roadmap change.
