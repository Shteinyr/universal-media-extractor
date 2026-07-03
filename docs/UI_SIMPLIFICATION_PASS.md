# UI Simplification Pass

Date: 2026-05-30

## Status

Completed.

This pass simplifies the existing static UI without adding backend features, changing API contracts, changing the roadmap, or adding new processing behavior.

## What Changed

- The format area is now organized around three simple choices:
  - `Audio`
  - `Video`
  - `Subtitles`
- Format options are hidden until the user picks one of those categories.
- The left input copy is shorter.
- The warning panel now hides technical analysis-only/no-subtitle/no-size warnings and shows only short user-facing notes.
- The existing MVP flow is preserved:

```text
Analyze -> Select format -> Confirm rights -> Download -> Transcribe -> Result
```

## Audio Selection

Audio rows now show only:

- container/format, such as `M4A` or `WEBM`;
- approximate file size when available;
- a small `Recommended` badge when the option is recommended.

Hidden from audio rows:

- codec labels like `mp4a.40.2`;
- repeated `audio only` text;
- bitrate details;
- format id;
- long `yt-dlp` display labels.

Example:

```text
M4A · 616.91 KB
WEBM · 17.48 KB
```

## Video Selection

Video rows now show only:

- container/format, such as `MP4` or `WEBM`;
- quality, such as `1080p`;
- approximate file size when available;
- a small `Recommended` badge when available.

Video options below `1080p` are hidden from the UI.

Hidden from video rows:

- codec labels;
- fps;
- long technical display labels;
- low-resolution variants below `1080p`;
- repeated badges and id pills.

## Subtitles Selection

Subtitles are shown in the same simplified chooser.

If subtitle options exist, the UI shows:

- language;
- manual or automatic type;
- a short formats line if formats are available.

If no subtitles exist, the UI shows a short empty state:

```text
No subtitles found.
```

## What Did Not Change

- No backend endpoints were changed.
- No download/transcription logic changed.
- No data models changed.
- No desktop wrapper was added.
- No Chrome extension was added.
- No AI summary API was added.
- No batch processing was added.
- No React/Vite/CDN or new frontend framework was added.
- No roadmap block was created or changed.

## Verification

Tests:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
73 passed
```

Browser smoke:

```bash
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/ui_simplification
```

Proof artifacts:

```text
proof/ui_simplification/ui_initial.png
proof/ui_simplification/ui_analyze_result.png
```

Verified:

- local UI opens;
- URL analysis works;
- `Showreel` appears;
- `Audio`, `Video`, and `Subtitles` category tabs work;
- audio options render as short labels;
- video options are filtered to `1080p` or higher;
- subtitle empty state is short;
- no download/transcribe is run by the default browser smoke.
