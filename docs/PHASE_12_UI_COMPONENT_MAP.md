# Phase 12 UI Component Map

Date: 2026-05-29

## Scope

This document maps future UI components/sections for an analysis-result display only interface. It is a planning artifact; no frontend code is created in Phase 12.

## AppShell

Purpose:

- provide the single-screen layout;
- keep local utility styling consistent;
- hold left input panel and right result panel.

Contains:

- app title;
- local-only status;
- `UrlInputPanel`;
- result area.

Does not contain:

- settings page;
- routing;
- download/transcription controls.

## UrlInputPanel

Purpose:

- collect URL input;
- display short analysis-only/legal notes.

Fields:

- URL text input;
- current backend base URL note: `http://127.0.0.1:8000`;
- supported-source best-effort note.

States:

- idle;
- analyzing;
- API unavailable;
- validation error.

## AnalyzeButton

Purpose:

- start the `POST /analyze` request.

States:

- enabled when a non-empty URL is present;
- disabled while analyzing;
- label changes from `Analyze` to `Analyzing...`.

Does not do:

- download;
- transcribe;
- select formats.

## SourceSummaryCard

Purpose:

- display high-level source details from `AnalyzeResult`.

Fields:

- `thumbnail_url`;
- `title`;
- `duration_label` or formatted `duration_seconds`;
- `extractor`;
- `source_type`;
- `webpage_url`;
- `uploader.name`;
- `uploader.channel_name`;
- `availability`.

Phase 11 expected display:

- `Showreel`;
- `0:39`;
- `youtube`;
- `Aleksandr Shtein`;
- YouTube thumbnail.

## FormatGroup

Purpose:

- group media options by type.

Groups:

- audio-only;
- video-only;
- combined video+audio;
- subtitles;
- automatic captions.

Behavior:

- show count;
- show `EmptyState` when list is empty;
- render each media row through `FormatOptionRow`.

## FormatOptionRow

Purpose:

- display one `MediaOption` compactly.

Fields:

- `display_label`;
- `format_id`;
- `type`;
- `ext` or `container`;
- `resolution`;
- `audio_codec`;
- `video_codec`;
- `filesize` or `filesize_approx`;
- recommended badge when `is_default_recommended` is true.

Behavior:

- display-only in Phase 13;
- no checkbox;
- no download button;
- no process button.

## WarningsPanel

Purpose:

- display `AnalyzeResult.warnings`.

Phase 11 warning examples:

- `no_subtitles`;
- `no_automatic_captions`;
- `format_size_unknown`;
- `platform_terms_warning`;
- `best_effort_extractor`;
- `analysis_only_not_download_tested`.

Behavior:

- group info and warning severity visually;
- keep warnings visible but not alarming unless blocking severity appears.

## ErrorsPanel

Purpose:

- display `AnalyzeResult.errors` and job errors.

Fields:

- `code`;
- `message`;
- `suggested_user_action`;
- optional collapsed `technical_details`.

Visibility:

- hidden when there are no errors;
- prominent when analysis fails.

## EmptyState

Purpose:

- avoid blank sections when an option group is empty.

Examples:

- `No manual subtitles detected.`
- `No automatic captions detected.`
- `No audio formats detected.`
- `No video formats detected.`

Tone:

- neutral;
- source-specific;
- no overpromising.

## RawMetadataToggle Later

Purpose:

- developer/debug view for raw normalized metadata.

Phase 13 status:

- later only;
- do not show raw JSON by default;
- do not embed raw `yt-dlp` JSON.

Future behavior:

- show normalized response JSON;
- show `raw_reference_path` as developer detail;
- keep technical metadata collapsed.
