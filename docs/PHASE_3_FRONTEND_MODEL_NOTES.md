# Phase 3 Frontend Model Notes

Date: 2026-05-29

## Scope

These are notes for future frontend behavior. No frontend was created in Phase 3.

## Before Analysis

The UI should show:

- URL input or local file input;
- local-only status indicator;
- short rights reminder;
- disabled process/download controls;
- dependency status if available in future phases.

The UI should not show media selectors until an `AnalyzeResult` exists.

## During Analysis

Future behavior:

- show "Analyzing source";
- disable URL/file changes or ask before replacing current analysis;
- show source URL;
- do not imply download has started;
- show cancellable state only after backend supports cancellation.

## After Successful Analysis

Use `AnalyzeResult`:

- Header: `title`, `duration_label`, `thumbnail_url`, source badge from `source_type`.
- Source card: `webpage_url`, `extractor`, uploader/channel, availability, access state.
- Audio selector: `media_options.audio`.
- Video selector: `media_options.combined` and `media_options.video`.
- Subtitles selector: `subtitles` and `automatic_captions`.
- Metadata panel: selected `metadata` fields.
- Warnings block: all `warnings`, sorted by severity.
- Legal/safety confirmation: `legal_safety`.

## Available Actions

Before user confirms rights:

- analyze another source;
- inspect metadata;
- inspect formats;
- choose intended output;
- cannot download/process.

After `legal_safety.user_confirmed_rights == true` in a future implementation:

- process selected output;
- download/extract selected media;
- transcribe if audio path exists or future pipeline can extract audio.

Phase 3 does not implement these actions.

## Disabled Elements

Disable:

- process/download buttons if `user_confirmed_rights` is false;
- audio choices if `media_options.audio` is empty;
- video choices if both `media_options.video` and `media_options.combined` are empty;
- subtitles selector if both `subtitles` and `automatic_captions` are empty;
- advanced process options if the selected option has `is_downloadable=false`;
- all process actions if `errors` contains a blocking error.

## Warnings Display

Always show:

- `platform_terms_warning`;
- `best_effort_extractor`;
- blocking or recoverable errors.

Show contextual warnings near affected controls:

- `no_subtitles` near subtitles selector;
- `no_automatic_captions` near captions selector;
- `format_size_unknown` near media option size column;
- `analysis_only_not_download_tested` in debug/proof phases or pre-MVP builds.

## Simple Mode

Simple mode should present task-oriented choices:

- best audio;
- mp3;
- m4a;
- wav;
- mp4 720p;
- mp4 1080p;
- best available.

Simple choices map to backend policies, not necessarily one native source format. For example, `mp3` may select best audio and later require `ffmpeg` conversion.

Simple mode should hide:

- raw `format_id`;
- protocol;
- exact codecs;
- exact bitrates;
- raw extractor details.

## Advanced Mode

Advanced mode should show:

- `format_id`;
- container/ext;
- audio/video codecs;
- bitrate;
- sample rate;
- FPS;
- resolution;
- filesize/filesize_approx;
- protocol;
- merge requirement;
- per-option warnings.

Advanced mode should still use `display_label` as the primary label and reveal details in columns or expanded rows.

## Empty States

| State | UI Copy / Behavior |
|---|---|
| No subtitles | Show "No manual subtitles detected." Disable manual subtitle download. |
| No automatic captions | Show "No automatic captions detected." Disable automatic captions download. |
| No video formats | Show "No video formats detected." Disable video output choices. |
| No audio formats | Show "No audio formats detected." Disable audio/transcript choices. |
| Unsupported link | Show error summary and ask user for a supported public URL or local file. |
| Login/cookies needed | Show recoverable warning; state that cookies/login are future manual options. |
| Source analysis failed | Show error message, technical details toggle, and retry if recoverable. |

## Result Preview

Before processing, the UI should show:

- selected output type;
- selected media option label;
- whether merge/conversion will be required;
- estimated output size if known;
- subtitle/caption selection;
- legal confirmation status;
- warnings that affect the selected option.

## Frontend Stability Rules

- Depend on normalized `AnalyzeResult`, never raw `yt-dlp` JSON.
- Treat nulls and empty arrays as valid states.
- Use `warnings` and `errors` arrays for state, not string matching raw CLI output.
- Keep raw metadata behind an advanced/debug disclosure.
- Do not enable download/process until legal confirmation is true.

