# UI/UX Reference Screen Map

Date: 2026-08-07

Purpose: map competitor visual patterns to the screens Universal Media Extractor likely needs.

This is not an implementation plan. It is input for GPT Pro analysis before `Public Beta UI / UX Finalization`.

## Screen 1: Start / Input

Competitor patterns:

- Cobalt: one dominant paste field.
- Downie: pasteboard, drag/drop, browser extension entry.
- 4K Video Downloader Plus: copy link, paste into app, download.
- yt-dlp.app: paste URL, no command line.

Our required logic:

- Link mode;
- File mode;
- Batch mode;
- Course mode hidden in public builds;
- local-only status should be quiet;
- no long explanatory text.

Question for GPT Pro:

```text
Should the first screen be one universal input that accepts URL/file/batch,
or should it keep explicit Link / File / Batch modes?
```

## Screen 2: Analysis Result / Source Card

Competitor patterns:

- thumbnail + title + source + duration;
- simple status;
- no raw extractor details in primary card.

Our required logic:

- title;
- thumbnail;
- duration;
- uploader/source;
- source URL;
- warnings/errors;
- open source link if useful.

Question for GPT Pro:

```text
What minimum source info should be visible before choosing output?
```

## Screen 3: Output Choice

Competitor patterns:

- Smart Mode / one-click preferences;
- quality presets;
- output format;
- destination folder;
- subtitles as simple option.

Our required logic:

- Audio / Video / Subtitles;
- video means merged video+audio;
- output formats:
  - audio: M4A, MP3, WAV;
  - video: MP4, MKV, WEBM;
  - subtitles: SRT, VTT;
- hide video below 1080p in the normal UI;
- dedupe user-facing options.

Question for GPT Pro:

```text
Should output be presented as tabs, cards, segmented presets, or a compact dropdown?
```

## Screen 4: Download / Working State

Competitor patterns:

- queue/list row;
- progress/status;
- cancel;
- no verbose logs by default.

Our required logic:

- background job;
- progress if available;
- current step;
- cancel request;
- failed/succeeded states;
- diagnostics if failed.

Question for GPT Pro:

```text
How much progress detail should a non-technical user see?
```

## Screen 5: Saved Result

Competitor patterns:

- downloaded item in list/library;
- open/reveal file;
- clear finished;
- history.

Our required logic:

- show saved file name;
- show output folder;
- reveal/copy path;
- transcribe if media file has audio;
- show only selected transcript format;
- copy transcript if available.

Question for GPT Pro:

```text
Should success state be a large result card or a compact row in a local library?
```

## Screen 6: Transcription

Competitor patterns:

- Buzz: import -> model/options -> transcript viewer/export.
- MacWhisper: drag/drop -> process -> export.

Our required logic:

- post-processing only;
- Whisper model selector;
- transcript format selector;
- Transcribe button;
- saved transcript;
- copy transcript;
- no AI summary in public beta.

Question for GPT Pro:

```text
Should transcription live in the main flow, a result action, or a separate file-processing mode?
```

## Screen 7: Batch

Competitor patterns:

- SnapDownloader bulk URLs;
- MediaHuman list queue;
- 4K download management;
- Stacher library/queue.

Our required logic:

- paste list;
- import text file;
- analyze playlist/select items;
- choose preset;
- queue;
- controlled concurrency;
- retry failed.

Question for GPT Pro:

```text
How should batch be introduced without making the core single-link flow feel complex?
```

## Screen 8: Recent Results / Library

Competitor patterns:

- Stacher Library;
- MediaHuman main list;
- 4K easy download management;
- Downie history.

Our required logic:

- output index;
- recent results;
- safe delete;
- reveal/copy output path;
- file badges.

Question for GPT Pro:

```text
Should Recent results return to the visible UI for public beta,
or stay hidden until a stronger library view exists?
```

## Screen 9: Errors / Diagnostics

Competitor patterns:

- simple error first;
- support link/logs/details secondary.

Our required logic:

- normalized user-facing error;
- short recovery action;
- collapsible technical details;
- copy diagnostics;
- no sensitive data leakage.

Question for GPT Pro:

```text
Where should diagnostics live so normal users are not scared, but support remains possible?
```

## Screen 10: Settings

Competitor patterns:

- output folder;
- default format/quality;
- engine update;
- language/theme;
- auth/private sources;
- advanced CLI settings.

Our current status:

- no full settings page yet;
- save location exists inline;
- public beta may need only small preferences, not full settings.

Question for GPT Pro:

```text
What settings are required for public beta, and what should wait?
```
