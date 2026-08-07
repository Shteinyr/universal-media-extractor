# GPT Pro Brief: Public Beta UI / UX Finalization

Date: 2026-08-07

## Task For GPT Pro

Analyze the current Universal Media Extractor product logic and competitor visual references. Recommend a final public beta UI/UX structure:

- what screens should exist;
- what buttons should exist;
- what should be primary vs secondary;
- what should be hidden in advanced/support;
- the correct user flow sequence;
- the best layout for desktop utility usage;
- what should be removed from the public UI before beta.

## Product

Name:

```text
Universal Media Extractor
```

Public positioning:

```text
Local Media Downloader & Organizer for macOS and Windows
```

Core idea:

```text
Turn supported media links and local media files into organized local output files.
```

## What The App Does Today

Core flows:

```text
URL -> Analyze -> Choose output -> Download -> optional Transcribe -> Result
Local file -> Analyze -> Transcribe -> Result
Batch list -> Import/select -> Download queue -> Retry failed
```

Internal/experimental flow:

```text
Udemy lecture/player URL -> Chrome session -> Analyze course -> Download course
```

Udemy/Course mode is not part of public commercial positioning.

## Public Feature Set

Include in public beta UI:

- Link/URL mode;
- local file mode;
- batch mode;
- analyze URL;
- analyze local file;
- output presets;
- audio download;
- video download as video+audio merged file;
- subtitles download when available;
- output format selection;
- output location;
- background job status;
- cancel/retry where available;
- transcription as post-processing;
- transcript format selection;
- recent/history/output management if it can be presented cleanly;
- safe delete/reveal/copy path;
- normalized errors;
- diagnostics copy for failed jobs.

Hide or de-emphasize:

- Course/Udemy mode in public builds;
- raw `yt-dlp` format IDs;
- codec strings;
- bitrate internals;
- CLI flags;
- proxy/geobypass concepts;
- manual cookies;
- raw logs;
- raw JSON;
- legal paragraphs in primary flow.

## Competitors To Consider

Mandatory from GPT Pro strategy:

- 4K Video Downloader Plus;
- Downie;
- SnapDownloader;
- PullTube;
- MediaHuman YouTube Downloader;
- Parabolic;
- Cobalt;
- Stacher;
- Buzz;
- MacWhisper.

Supplemental:

- yt-dlp.app;
- Wondershare UniConverter;
- VideoProc;
- HitPaw Video Converter / Univd.

## Design Direction

Preferred direction:

```text
Compact local desktop utility
Downloader/file-manager style
Input-first
Preset-driven
Low technical noise
Clear saved-file result
Advanced details hidden
```

Avoid:

- marketing-dashboard feel;
- developer console feel;
- giant technical format lists;
- overdecorated landing-page UI;
- large visible warnings;
- pretending to support every site.

## Key UX Decisions Needed From GPT Pro

1. Should the first screen use one universal input, or keep explicit `Link / File / Batch` modes?
2. How should output presets be represented: cards, segmented controls, dropdowns, or compact rows?
3. Should `Recent results` be visible in the main UI or moved into a separate Library/History screen?
4. Should transcription be a post-download action, separate mode, or folded into result actions?
5. What should the exact button sequence be for a normal user?
6. What text should be visible on the first screen?
7. What user-facing errors should be shown, and where should technical details live?
8. Which settings are required before public beta?
9. How should batch be introduced without confusing single-link users?
10. What should be removed before beta to make the app feel finished?

## Current Candidate Flow

```text
1. Add source
   - Paste link
   - Choose file
   - Batch import

2. Analyze
   - Show media summary
   - Show source availability/errors

3. Choose output
   - Best video
   - 1080p video
   - Smaller video
   - Audio
   - Subtitles

4. Choose save options
   - destination folder
   - output format

5. Download / Process
   - working state
   - cancel if running

6. Result
   - saved file
   - reveal/copy path
   - transcribe if applicable
   - retry if failed

7. Transcribe
   - model
   - transcript format
   - save transcript
   - copy transcript
```

## Important Product Constraints

- Local-only backend.
- No cloud upload.
- No paid API required.
- No user accounts in the app.
- No DRM bypass.
- No CAPTCHA/paywall/login bypass.
- Best-effort source support.
- Public builds hide Course/Udemy mode.
- Transcription runs locally through Whisper CLI.

## Files To Read Together With This Brief

- `docs/UI_UX_COMPETITOR_VISUAL_AUDIT.md`
- `docs/UI_UX_PRODUCT_FUNCTION_INVENTORY.md`
- `docs/UI_UX_REFERENCE_SCREEN_MAP.md`
- `docs/PRODUCT_FUNCTIONALITY_OVERVIEW.md`
- `docs/PUBLIC_PRODUCT_BOUNDARY.md`
- `docs/PUBLIC_KNOWN_LIMITATIONS.md`
- `docs/COMMERCIAL_BLOCK_14_PUBLIC_BETA_UI_READINESS.md`
- `docs/PUBLIC_BETA_QA_ROUND.md`
