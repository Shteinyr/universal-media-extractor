# UI Dedup Fix

Date: 2026-05-30

## Status

Completed.

This is a bugfix / UX refinement inside the current product. It does not create a new roadmap block, change backend endpoints, change API contracts, or add new features.

## Cause

`yt-dlp` can expose several raw formats that are technically different but look identical to a normal user. Examples:

- multiple `mp4` video rows at the same visible quality, such as `1080p`;
- one variant with size and another without size;
- separate subtitle format entries such as `vtt`, `srt`, `json3`, and `srv1` for the same language/type.

The simplified UI was rendering these raw entries too directly, so users could see repeated options like `MP4 · 1080p`.

## Video Deduplication

The UI now builds user-facing video options before rendering.

Video options are considered duplicates when they share:

- user-facing mode: `video`;
- container / extension, such as `mp4` or `webm`;
- visible quality, such as `1080p` or `2160p`.

Only one row is shown for each unique container + quality pair.

When several raw formats map to the same user-facing row, the chosen option prefers:

1. a known `filesize` or `filesize_approx`;
2. a recommended option;
3. a more complete option, with combined video+audio preferred when otherwise equal;
4. the first stable option.

Video options below `1080p` remain hidden from the UI.

## Audio Deduplication

Audio options are deduplicated by:

- user-facing mode: `audio`;
- container / extension;
- approximate size bucket.

This keeps short rows such as:

```text
M4A · 1.69 MB
WEBM · 650 KB
```

## Subtitle Deduplication

Subtitles and automatic captions are normalized into one row per:

- language code / display language;
- subtitle type: manual or automatic.

Multiple subtitle file formats no longer create duplicate rows. Instead, formats are merged into a short helper line for the same option.

Examples:

```text
EN · Manual subtitles
EN · Auto captions
RU · Auto captions
```

Manual subtitles and automatic captions for the same language remain separate options.

## Implementation Notes

- Added `src/universal_media_extractor/static/option_normalizer.js`.
- `index.html` loads the normalizer before `app.js`.
- `app.js` keeps rendering and selection behavior, but receives already deduplicated user-facing options.
- Subtitle rows use a separate `selection_id` for UI highlighting so manual and automatic captions for the same language do not visually collide.

## What Did Not Change

- No backend endpoints changed.
- No Pydantic models changed.
- No `yt-dlp`, download, transcription, job, output, or local file behavior changed.
- No roadmap block was created or changed.
- No React/Vite/CDN or new frontend framework was added.

## Verification

Targeted tests:

```bash
.venv/bin/python -m pytest tests/test_ui_option_normalizer.py tests/test_api_app.py::test_static_index_is_available tests/test_api_app.py::test_static_javascript_is_available tests/test_api_app.py::test_static_option_normalizer_is_available -q
```

Result:

```text
5 passed
```

Full suite:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
76 passed
```

Browser proof:

```bash
custom Playwright check against http://127.0.0.1:8000/
```

Proof screenshots:

```text
proof/ui_dedup_fix/video_dedup.png
proof/ui_dedup_fix/subtitles_dedup.png
proof/ui_dedup_fix/ui_dedup_observed.txt
```

Observed labels for the user-authorized test URL:

```text
video_labels=['MP4 · 1080p · 12.23 MB']
subtitle_labels=[]
```
