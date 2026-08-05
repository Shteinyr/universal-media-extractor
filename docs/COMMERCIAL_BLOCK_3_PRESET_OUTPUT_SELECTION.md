# Commercial Block 3: Preset Output Selection

## Status

Completed.

GitHub issue: `#9 [P0] Replace technical format selection with presets`.

## Goal

Replace the public, user-facing technical format picker with simple output presets suitable for a commercial desktop utility.

The app should no longer ask a normal user to choose from raw `yt-dlp` streams, codec labels, or `format_id` values. Those details remain internal and are available only through an advanced disclosure when needed for diagnostics or support.

## Implemented Presets

The URL analysis UI now renders these presets after `/analyze` succeeds:

- `Best Video`
- `1080p`
- `Smaller Video`
- `Audio M4A`
- `Audio MP3`
- `Subtitles`
- `Archive Pack`

Unavailable presets remain visible but disabled with a short reason. This keeps the product model stable while avoiding fake capabilities.

## Preset Behavior

`Best Video`:

- chooses the highest available video option at `1080p` or higher;
- preserves the internal `format_id` for `/download`;
- selects a safe output container based on the source stream.

`1080p`:

- chooses a `1080p` video option when available;
- prefers user-friendly video output;
- keeps raw stream details hidden from the main UI.

`Smaller Video`:

- chooses the smallest known video option at `1080p` or higher;
- falls back safely when sizes are unknown.

`Audio M4A`:

- prefers an available M4A audio stream;
- falls back to the best audio stream when needed;
- requests `m4a` output.

`Audio MP3`:

- uses the best available audio stream;
- requests `mp3` output.

`Subtitles`:

- prefers manual subtitles over automatic captions;
- uses one deduplicated language/type option;
- requests `srt` output.

`Archive Pack`:

- shown as a disabled planned preset;
- not implemented as a real action yet because it requires multi-output orchestration, queue/history behavior, and clearer retry semantics;
- should be implemented later as a separate product feature, not as a hidden batch workflow inside this issue.

## Hidden Technical Details

The main UI hides:

- raw `format_id` values;
- codec strings;
- fps details;
- repeated technical stream rows;
- raw `yt-dlp` labels.

Advanced stream details remain available behind the `Advanced details` disclosure. This is intended for support/debugging, not normal use.

## Internal Download Behavior

Existing download behavior is preserved:

- `/download` still receives the selected internal `format_id`;
- `mode` remains `audio`, `video`, `combined`, or `subtitles`;
- `output_format` is derived from the selected preset;
- backend safety confirmation remains preserved by the existing request contract.

## Files Changed

- `src/universal_media_extractor/static/index.html`
- `src/universal_media_extractor/static/styles.css`
- `src/universal_media_extractor/static/app.js`
- `src/universal_media_extractor/static/option_normalizer.js`
- `scripts/browser_smoke.py`
- `tests/test_ui_option_normalizer.py`

## Verification

Targeted checks:

```bash
node --check src/universal_media_extractor/static/app.js
node --check src/universal_media_extractor/static/option_normalizer.js
.venv/bin/python -m pytest tests/test_ui_option_normalizer.py tests/test_api_app.py::test_static_javascript_is_available -q
```

Final verification:

```bash
.venv/bin/python -m pytest -q
# 111 passed

.venv/bin/python scripts/browser_smoke.py --base-url http://127.0.0.1:8766/ --proof-dir proof/commercial_block_3_presets
# Browser smoke completed
```

Proof screenshots:

- `proof/commercial_block_3_presets/ui_initial.png`
- `proof/commercial_block_3_presets/ui_analyze_result.png`

## Not Included

- No backend route redesign.
- No batch processing.
- No Archive Pack execution.
- No SQLite jobs/history.
- No payment/licensing/store work.
- No React/Vite/CDN/frontend stack change.
- No roadmap changes.
