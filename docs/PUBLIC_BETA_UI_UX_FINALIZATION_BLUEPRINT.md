# Public Beta UI / UX Finalization Blueprint

Date: 2026-08-07

Status: blueprint only. No product code, API, roadmap, or feature scope was changed.

## Purpose

This document defines the final public beta UI/UX direction for Universal Media Extractor before implementation.

It is based on:

- GPT Pro commercial strategy;
- competitor visual audit;
- current product function inventory;
- reference screen map;
- public product boundary;
- public beta QA results.

The goal is to make the product feel like a finished local desktop utility, not a developer prototype or raw `yt-dlp` wrapper.

## Product Frame

Public positioning:

```text
Local Media Downloader & Organizer for macOS and Windows
```

Primary public promise:

```text
Turn supported media links and local media files into organized local output files.
```

The UI must not imply:

- guaranteed support for every site;
- DRM bypass;
- CAPTCHA, paywall, login, region, or platform-restriction bypass;
- public Udemy/course download support;
- cloud processing;
- AI summary as a core feature.

## Final Screen Structure

### 1. Add Source

Primary screen and default start state.

Visible sections:

- source input area;
- source type selector;
- primary `Analyze` action;
- small local/privacy status if needed;
- empty state that explains the next action in one short sentence.

Source types:

- `Link`;
- `File`;
- `Batch`.

Hidden from public builds:

- `Course` / Udemy mode.

Decision:

Use explicit `Link / File / Batch` modes instead of one universal input for public beta.

Reason:

- A universal input is elegant but creates unclear behavior for files, batches, and links.
- Explicit modes make the current product capabilities understandable without adding help text.
- This follows the clarity of downloader tools while preserving room for batch as a paid/Pro differentiator.

### 2. Source Summary

Appears after successful analysis.

Visible fields:

- thumbnail or simple placeholder;
- title or filename;
- source/service label;
- duration if known;
- uploader/channel if available;
- `Open source` link only for URL mode;
- one-line availability note only if something needs attention.

Hidden by default:

- extractor internals;
- raw URL details;
- technical metadata;
- raw JSON path;
- job ID.

### 3. Choose Output

The output selector is the main decision point after analysis.

Recommended public presets:

- `Best video`;
- `1080p video`;
- `Smaller video`;
- `Audio only`;
- `Subtitles`.

Mode-specific behavior:

- Video means one final playable file with video plus audio.
- Audio means audio-only output.
- Subtitles means subtitle file only, when available.
- Transcript is not an initial output choice for URL mode; it appears after a media file exists.

Format details:

- Video formats: MP4, MKV, WEBM.
- Audio formats: M4A, MP3, WAV.
- Subtitle formats: SRT, VTT.

Display principle:

- Show preset name and likely result.
- Hide `format_id`, codec strings, bitrate internals, and raw stream details.
- If technical details are needed, put them behind `Details` or diagnostics.

### 4. Save Options

Save options should be compact and near the action they affect.

Visible fields:

- `Save to`;
- output format;
- duplicate policy only if it already exists and can be shown simply.

Recommended default:

```text
~/Downloads/Universal Media Extractor
```

Preferred copy:

- `Save to`;
- `Format`;
- `Use source title for folder name`.

Avoid:

- long filesystem paths in the primary UI;
- visible `.metadata` / `.logs`;
- folder templates in the main flow.

### 5. Processing State

Used for analysis, download, transcription, and batch jobs.

Visible fields:

- human status: `Analyzing`, `Downloading`, `Transcribing`, `Saved`, `Needs attention`, `Cancelled`;
- current step only when useful;
- progress bar only when progress is real enough;
- `Cancel` for active long-running jobs;
- `Retry` for failed recoverable jobs.

Hidden by default:

- raw subprocess output;
- technical logs;
- job IDs;
- exact CLI command.

Decision:

Progress should be honest, not theatrical.

If exact progress is unavailable, show current step and activity state rather than fake percentages.

### 6. Saved Result

This is the most important success state.

Visible fields:

- saved file name;
- output folder name;
- file type badge;
- size if available;
- `Reveal`;
- `Copy path`;
- `Transcribe` if media has audio;
- `Retry` only for failed result.

Hidden by default:

- full absolute paths;
- metadata files;
- logs;
- all transcript formats if only one was selected.

Decision:

Success should look like a file manager result, not a report.

### 7. Transcription

Transcription is post-processing, not the first product promise.

Appears after:

- URL download saved an audio file;
- URL download saved video with audio;
- local file analysis found audio/video suitable for transcription.

Visible fields:

- Whisper model;
- transcript format;
- `Transcribe`;
- saved transcript file;
- transcript preview;
- `Copy transcript`;
- `Reveal`;
- `Copy path`.

Model options:

- tiny;
- base;
- small;
- medium;
- turbo/default.

Transcript formats:

- TXT;
- Markdown;
- JSON.

Decision:

The user chooses one transcript format per run. The UI should not show all possible transcript files after every run.

### 8. Batch Queue

Batch should be present but separated from the single-link path.

Visible fields:

- textarea for URL list;
- paste/import controls;
- playlist/item selection if detected;
- preset selector;
- queue list;
- per-item status;
- `Start batch`;
- `Cancel`;
- `Retry failed`.

Default posture:

- make batch discoverable;
- do not make it the default first-time experience.

### 9. Library / History

Recent results should become a proper secondary surface, not a cluttered sidebar block.

Recommended public beta structure:

- primary screen: current task;
- secondary screen or drawer: `Library` / `History`.

Visible fields:

- result title;
- source type;
- saved date;
- file badges: media, subtitle, transcript;
- size if available;
- `Reveal`;
- `Copy path`;
- `Delete`.

Safety:

- delete only managed outputs;
- destructive action must remain visually separated;
- confirm or undo for delete if implementation allows.

### 10. Errors / Diagnostics

Errors must be plain-language first.

Visible fields:

- short error title;
- one-sentence explanation;
- next action;
- `Retry` if recoverable;
- `Copy diagnostics` if useful;
- collapsible `Technical details`.

Recommended user-facing categories:

- Source unavailable;
- Login required;
- Protected content;
- Network issue;
- No downloadable media found;
- Output folder issue;
- Engine update needed;
- Transcription failed;
- Unsupported file;
- Unknown error.

Diagnostics rules:

- never show cookies, tokens, full private URLs, transcripts, or sensitive local paths in public diagnostics;
- technical details stay collapsed by default.

## Main User Chains

### Link Flow

```text
Open app
-> Link
-> Paste URL
-> Analyze
-> See source summary
-> Choose output preset
-> Choose format/save location if needed
-> Download
-> See saved result
-> Optional Transcribe
-> Copy/reveal output
```

### Local File Flow

```text
Open app
-> File
-> Choose audio/video file
-> Analyze file
-> See file summary
-> Optional Transcribe
-> Choose model and transcript format
-> See saved transcript
-> Copy/reveal output
```

### Batch Flow

```text
Open app
-> Batch
-> Paste/import URLs
-> Analyze/prepare list
-> Select items if applicable
-> Choose preset
-> Start batch
-> Monitor queue
-> Retry failed if needed
-> Open Library/History
```

## Buttons And Primary Actions

### Global / Navigation

- `Link`;
- `File`;
- `Batch`;
- `Library`;
- `Settings` only if a minimal settings surface is implemented;
- `Help` / `Support` only if it opens docs/support copy.

### Link Mode

- `Analyze`;
- `Download`;
- `Cancel`;
- `Retry`;
- `Reveal`;
- `Copy path`;
- `Transcribe`;
- `Copy transcript`;
- `Copy diagnostics`.

### File Mode

- `Choose file`;
- `Analyze file`;
- `Transcribe`;
- `Cancel`;
- `Reveal`;
- `Copy path`;
- `Copy transcript`;
- `Copy diagnostics`.

### Batch Mode

- `Paste`;
- `Import text file`;
- `Analyze list` or `Prepare queue`;
- `Select all`;
- `Clear`;
- `Start batch`;
- `Cancel`;
- `Retry failed`;
- `Reveal`;
- `Copy diagnostics`.

### Library / History

- `Reveal`;
- `Copy path`;
- `Delete`;
- `Retry` where recoverable;
- `Clear completed` only if already supported safely.

## Advanced / Internal Areas

Advanced/support can include:

- technical details;
- redacted diagnostics;
- engine version;
- output templates;
- duplicate policy;
- raw file/service metadata summary;
- manual cookie path only for internal/experimental workflows;
- Course/Udemy mode only outside public builds.

Advanced/support must not include:

- password fields;
- token storage;
- DRM bypass;
- proxy/geobypass;
- raw cookie export as a normal public flow;
- unsupported “download everything” claims.

## What To Remove From Main UI

- Course/Udemy mode in public builds.
- Raw format IDs.
- Codec strings such as `mp4a.40.2`.
- Long bitrate/fps/audio-language descriptions.
- Raw CLI logs.
- Full absolute paths as primary content.
- Developer phrases like `job_id`, `extractor`, `raw artifact`, `stderr`.
- Summary prompt marker unless summary prompt is an actual active user-facing feature.
- Long legal paragraphs.
- Empty helper blocks that repeat the obvious.

## What Must Stay Visible

- Source input.
- Analyze action.
- Source summary.
- Output presets.
- Save location.
- Output format.
- Download/process action.
- Honest progress/state.
- Saved result.
- Reveal/copy output.
- Plain-language errors.
- Diagnostics access for failed jobs.
- Transcript action after a suitable file exists.

## Public Build Course Mode Rule

Public builds must set:

```text
UME_PUBLIC_PRODUCT_MODE=1
```

Expected behavior:

- hide Course/Udemy mode from main navigation;
- hide Udemy copy from public UI;
- do not advertise course export;
- keep internal code path available only if separately enabled for development/internal testing.

## Competitor Patterns To Borrow

From 4K Video Downloader Plus:

- Smart Mode concept: reusable output preferences.
- Management/library value.
- Simple copy/paste/download story.

From Downie:

- Mac utility feel.
- Fast handoff from browser/pasteboard to app.
- Download queue/history without overwhelming the user.

From SnapDownloader:

- One-click mode.
- Batch and queue as power features.
- Clear format/quality choices.

From PullTube:

- Short path from link to saved file.
- Mac-first feel.
- Trim/convert as later post-processing, not first-screen noise.

From MediaHuman:

- Toolbar/list mental model.
- Locate/reveal downloaded file.
- Format/resolution defaults.

From Stacher and Parabolic:

- GUI over `yt-dlp` can be valuable if it hides command complexity.
- Advanced engine options should not dominate the default surface.

From Cobalt:

- Low-friction paste-first UX.
- Minimal copy.

From Buzz and MacWhisper:

- Transcription belongs to a file-processing workflow.
- Model/export settings should be available but contained.

## Patterns Not To Copy

- Proxy/geobypass claims.
- Huge all-in-one toolbox navigation.
- Paid-course download positioning.
- “Supports everything” promises.
- Large technical settings panels in the default experience.
- Long lists of raw formats.
- Public manual-cookies workflow.
- AI feature creep before the core downloader is polished.

## Suggested Information Architecture

```text
Main window
  Source rail / top mode switch
    Link
    File
    Batch
  Work area
    Empty state
    Source summary
    Output choice
    Job state
    Saved result
  Secondary
    Library / History
    Settings
    Diagnostics
```

Implementation can choose sidebar or top tabs, but hierarchy should stay:

```text
Source first -> Output second -> Result third
```

## Acceptance Criteria For Next Implementation Block

The next UI implementation block is acceptable only if:

- no backend feature scope is added;
- public mode hides Course/Udemy mode;
- `Link / File / Batch` are clear and not mixed;
- initial screen has one obvious next action;
- URL flow can be completed without seeing raw technical formats;
- video output is described as a playable video file with audio;
- save location and format are easy to find but compact;
- transcript controls appear only after a file exists or local file is selected;
- user selects exactly one transcript format per transcription;
- progress states are honest and not fake;
- errors show plain-language cause and next step;
- technical details are collapsed by default;
- Library/History does not clutter the first action path;
- responsive layout has no horizontal overflow;
- keyboard focus and labels remain accessible;
- existing tests pass;
- browser smoke screenshots are updated after implementation.

## Non-Goals For Next Implementation Block

- No checkout or licensing.
- No installer/signing changes.
- No Chrome extension.
- No AI summary.
- No new backend service.
- No new API endpoint unless absolutely required for existing UI logic.
- No React/Vite/CDN migration.
- No public Course/Udemy marketing.
- No advanced source-auth workflows.
