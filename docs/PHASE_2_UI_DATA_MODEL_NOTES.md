# Phase 2 UI Data Model Notes

Date: 2026-05-29

## Scope

These notes describe what future UI screens should display from `yt-dlp` URL analysis. No UI was created in Phase 2.

## Source Summary

Recommended fields:

- `source_type`: derived from `extractor` / `extractor_key`, for example `youtube`.
- `source_url`: original submitted URL.
- `canonical_url`: `webpage_url`.
- `id`: source media ID.
- `title`: display title.
- `duration_seconds`: numeric duration.
- `duration_label`: human-friendly duration.
- `thumbnail_url`: primary thumbnail.
- `availability`: if present.
- `is_live` / `live_status`: for live or scheduled sources.

## Audio Options

Each audio option should include:

- `format_id`;
- `ext`;
- `audio_codec`;
- `audio_bitrate`;
- `sample_rate`;
- `audio_channels`;
- `language`, if available;
- `filesize` or `filesize_approx`, if available;
- `protocol`;
- `quality_label` or `format_note`;
- warning if size is unknown.

For the Phase 2 URL, audio-only options found:

- `139` m4a, `mp4a.40.5`, low, ~49k;
- `140` m4a, `mp4a.40.2`, medium, ~130k;
- `251` webm, `opus`, medium, ~4k.

## Video Options

Each video-only option should include:

- `format_id`;
- `ext`;
- `resolution`;
- `width`;
- `height`;
- `fps`;
- `video_codec`;
- `video_bitrate`;
- `dynamic_range`, if available;
- `filesize` or `filesize_approx`, if available;
- `protocol`;
- `quality_label` or `format_note`.

For the Phase 2 URL, video-only options found:

- `160` mp4, 144p;
- `134` mp4, 360p;
- `136` mp4, 720p;
- `137` mp4, 1080p.

## Combined Video+Audio Options

The UI should separate combined video+audio options from video-only and audio-only options because they do not require a separate merge step.

Each combined option should include:

- `format_id`;
- `ext`;
- `resolution`;
- `fps`;
- `video_codec`;
- `audio_codec`;
- `total_bitrate`;
- `filesize` or `filesize_approx`, if available;
- `protocol`;
- warning if size is unknown.

For the Phase 2 URL, combined options found:

- `91` mp4, 144p;
- `93` mp4, 360p;
- `18` mp4, 360p;
- `95` mp4, 720p;
- `96` mp4, 1080p.

## Subtitle Options

Recommended fields:

- `language_code`;
- `language_label`, if available;
- `kind`: manual subtitle or automatic caption;
- available file extensions, such as `vtt`, `srt`, `json3`, if present;
- source URL should not be shown by default unless in an advanced/debug panel.

For the Phase 2 URL:

- manual subtitles: none;
- automatic captions: none.

The UI needs a clear empty state: "No subtitles or automatic captions detected."

## Metadata Panel

Recommended metadata fields:

- uploader/channel name and URL;
- upload date or timestamp;
- description;
- tags/categories;
- view/like/comment counts if present;
- license;
- age limit;
- `_has_drm`;
- extractor and extractor version/debug info in an advanced panel.

## Warnings

The UI should reserve a warning area for:

- best-effort source support;
- platform restrictions and user responsibility;
- login/cookies required, when detected in future phases;
- no subtitles found;
- unknown filesize;
- live stream or unavailable media state;
- age-restricted/private/DRM indicators;
- analysis succeeded but download not yet tested.

## Future UI Shape

The future analyze result screen should be structured as:

1. Source summary with thumbnail, title, duration, and source domain.
2. Tabs or grouped sections for audio, video-only, combined video+audio, subtitles, and metadata.
3. Warnings shown near the top, not hidden in logs.
4. Raw metadata available only in an advanced/debug section.

