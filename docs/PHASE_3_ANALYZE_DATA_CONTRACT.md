# Phase 3 Analyze Data Contract

Date: 2026-05-29

## Scope

This document defines the future normalized response contract for an analyze operation. It is based on the real Phase 2 `yt-dlp` proof for `https://youtu.be/UUdxAp3kuKA`.

No backend app, frontend, route, downloader module, transcription module, media download, Whisper run, Chrome extension, desktop wrapper, or MVP implementation was created in Phase 3.

## Documentation Basis

Context7 was used for FastAPI and Pydantic.

- FastAPI docs confirm response models can be declared with Pydantic models through return type annotations or `response_model`, enabling validation, serialization, filtering, and OpenAPI schema generation.
- Pydantic v2 docs confirm nested models, lists, optional fields, validation, `model_dump()`, and `model_json_schema()` support.

Future implementation should define this contract as nested Pydantic v2 models and use it as the FastAPI response model for the analyze endpoint.

## Design Principles

- Normalize `yt-dlp` output so the UI does not depend on raw extractor internals.
- Preserve enough fields for advanced users and future processing.
- Never assume every field exists; `yt-dlp` metadata varies by source.
- Separate audio-only, video-only, and combined video+audio options.
- Keep legal/safety confirmation separate from analysis. Analysis can happen before confirmation; download/process must require confirmation.
- Keep a path to the raw artifact for debugging and reproducibility.

## Main Model: `AnalyzeResult`

Recommended fields:

| Field | Type | Required | Notes |
|---|---|---:|---|
| `schema_version` | string | yes | Start with `1.0`. Lets UI handle future changes. |
| `analysis_id` | string | yes | Local generated ID for this analysis. |
| `source_url` | string | yes | User-submitted URL or local file identifier. |
| `source_type` | string | yes | `url`, `local_file`, or source-specific normalized type such as `youtube`. |
| `extractor` | string or null | no | Raw extractor name, e.g. `youtube`. |
| `extractor_key` | string or null | no | Raw extractor key, e.g. `Youtube`. |
| `title` | string or null | no | Display title. |
| `duration_seconds` | number or null | no | Numeric duration if known. |
| `duration_label` | string or null | no | UI-friendly duration, e.g. `0:39`. |
| `thumbnail_url` | string or null | no | Primary thumbnail URL if available. |
| `webpage_url` | string or null | no | Canonical source URL from extractor. |
| `uploader` | object or null | no | Normalized uploader/channel data. |
| `availability` | string or null | no | Example: `public`, `unlisted`, `private`, source-dependent. |
| `access_state` | object | yes | Derived access flags and safety signals. |
| `media_options` | object | yes | Grouped audio/video/combined options. |
| `subtitles` | list[`SubtitleOption`] | yes | Manual subtitle tracks. Empty if none. |
| `automatic_captions` | list[`SubtitleOption`] | yes | Auto-caption tracks. Empty if none. |
| `metadata` | object | yes | Stable selected metadata, not full raw dump. |
| `warnings` | list[`WarningState`] | yes | User-facing warnings. |
| `errors` | list[`ErrorState`] | yes | Recoverable or blocking errors. Empty on success. |
| `legal_safety` | object | yes | Confirmation state required before download/process. |
| `raw_reference_path` | string or null | no | Local path to raw analysis artifact. |
| `analyzed_at` | string | yes | ISO-8601 timestamp. |

### `UploaderInfo`

| Field | Type | Notes |
|---|---|---|
| `name` | string or null | From `uploader` or `channel`. |
| `id` | string or null | From `uploader_id` or `channel_id`. |
| `url` | string or null | From `uploader_url` or `channel_url`. |
| `channel_name` | string or null | Source channel name when available. |
| `channel_id` | string or null | Source channel ID when available. |
| `channel_url` | string or null | Source channel URL when available. |

### `AccessState`

| Field | Type | Notes |
|---|---|---|
| `availability` | string or null | Raw or normalized availability. |
| `is_live` | boolean | True for live streams. |
| `live_status` | string or null | Raw live state. |
| `age_limit` | integer or null | Age gate indicator when available. |
| `has_drm` | boolean or null | From `_has_drm` where available. |
| `login_required` | boolean | Derived from extractor errors or metadata. |
| `cookies_required` | boolean | Derived; Phase 3 sample is false. |
| `playable_in_embed` | boolean or null | Source field if present. |

## Model: `MediaOptions`

| Field | Type | Notes |
|---|---|---|
| `audio` | list[`MediaOption`] | Audio-only formats. |
| `video` | list[`MediaOption`] | Video-only formats. |
| `combined` | list[`MediaOption`] | Formats containing both audio and video. |
| `recommended` | object | Recommended IDs for simple mode. |

## Model: `MediaOption`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `id` | string | yes | Stable app-side ID, usually same as `format_id`. |
| `format_id` | string | yes | Raw `yt-dlp` format ID. |
| `type` | string | yes | `audio`, `video`, or `combined`. |
| `container` | string or null | no | Same as `ext`, e.g. `mp4`, `m4a`, `webm`. |
| `ext` | string or null | no | Raw extension. |
| `codec` | string or null | no | Primary codec summary for compact display. |
| `audio_codec` | string or null | no | Raw `acodec`. |
| `video_codec` | string or null | no | Raw `vcodec`. |
| `resolution` | string or null | no | `audio only`, `640x360`, etc. |
| `width` | integer or null | no | Video width. |
| `height` | integer or null | no | Video height. |
| `fps` | number or null | no | Frames per second. |
| `bitrate` | number or null | no | Prefer `tbr`; for audio-only can equal `abr`; for video-only can equal `vbr`. |
| `audio_bitrate` | number or null | no | `abr`. |
| `video_bitrate` | number or null | no | `vbr`. |
| `sample_rate` | integer or null | no | `asr`. |
| `audio_channels` | integer or null | no | Number of audio channels. |
| `filesize` | integer or null | no | Exact bytes if available. |
| `filesize_approx` | integer or null | no | Approx bytes if available. |
| `language` | string or null | no | Track language if present. |
| `protocol` | string or null | no | `https`, `m3u8_native`, etc. |
| `dynamic_range` | string or null | no | `SDR`, `HDR`, etc. |
| `quality_label` | string or null | no | `144p`, `medium`, etc. |
| `is_default_recommended` | boolean | yes | Backend-selected default for the group. |
| `is_downloadable` | boolean | yes | False for storyboards or unsupported helper formats. |
| `requires_merge` | boolean | yes | True for video-only when final output needs audio. |
| `display_label` | string | yes | Ready-to-render UI label. |
| `warnings` | list[string] | yes | Per-option warning codes. |

## Model: `SubtitleOption`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `language` | string | yes | Language code such as `en`. |
| `language_label` | string or null | no | Human-friendly label when known. |
| `type` | string | yes | `manual` or `automatic`. |
| `formats` | list[string] | yes | Examples: `srt`, `vtt`, `json3`, `srv1`, `srv2`, `srv3`, `ttml`. |
| `is_available` | boolean | yes | True when there is at least one format. |
| `display_label` | string | yes | UI label. |

## Model: `WarningState`

Warning codes should be stable strings; messages can be localized later.

| Code | Meaning |
|---|---|
| `unsupported_source` | The extractor cannot handle the URL/source. |
| `login_required` | Source appears to require login. |
| `cookies_may_be_required` | Source may require user-provided cookies. |
| `no_subtitles` | No manual subtitles found. |
| `no_automatic_captions` | No automatic captions found. |
| `no_audio_formats` | No audio-only formats found. |
| `no_video_formats` | No video-only formats found. |
| `platform_terms_warning` | User must respect platform terms and rights. |
| `format_size_unknown` | At least one option lacks exact/approx size. |
| `best_effort_extractor` | Extractor support is best-effort and may change. |
| `analysis_only_not_download_tested` | Analysis succeeded but download/process was not tested. |

Recommended fields:

| Field | Type |
|---|---|
| `code` | string |
| `message` | string |
| `severity` | `info`, `warning`, or `blocking` |
| `related_field` | string or null |

## Model: `ErrorState`

| Field | Type | Notes |
|---|---|---|
| `code` | string | Stable error code, e.g. `unsupported_source`, `network_error`, `extractor_failed`. |
| `message` | string | User-facing message. |
| `technical_details` | string or null | Short stderr/detail excerpt, not giant logs. |
| `recoverable` | boolean | Whether retry/user action can help. |
| `suggested_user_action` | string or null | Example: provide a public URL or local file. |

## Legal / Safety Confirmation State

Required before any download or process action:

| Field | Type | Notes |
|---|---|---|
| `user_confirmed_rights` | boolean | Must be true before download/process. |
| `confirmation_text` | string | UI text shown to user. |
| `required_before_download` | boolean | Always true for URL sources. |
| `required_before_transcription` | boolean | True if processing downloaded/extracted media. |
| `accepted_at` | string or null | Set only after user confirms. |

## UI Mapping

### Header Card

- `title`
- `duration_label`
- `thumbnail_url`
- `source_type`
- primary warning count

### Source Card

- `source_url`
- `webpage_url`
- `extractor`
- `uploader.name`
- `uploader.channel_name`
- `availability`
- `access_state`

### Audio Selector

- `media_options.audio`
- show `display_label`, codec, bitrate, sample rate, approximate size
- disable if list is empty or source has blocking errors

### Video Selector

- `media_options.video`
- `media_options.combined`
- simple mode should prefer combined options when no merge is needed
- advanced mode should expose exact `format_id`, codecs, protocol, FPS, size

### Subtitles Selector

- `subtitles`
- `automatic_captions`
- show empty state when both lists are empty

### Warnings Block

- `warnings`
- `legal_safety`
- show `platform_terms_warning` and `best_effort_extractor` clearly before process/download controls

### Disabled States

Disable download/process controls when:

- `errors` contains blocking error;
- `legal_safety.user_confirmed_rights` is false;
- selected option has `is_downloadable=false`;
- selected media category is empty;
- source requires login/cookies and no manual support is enabled.

### Result Preview

Before processing:

- selected media option;
- expected output type;
- estimated size when known;
- subtitle/caption choice if available;
- raw metadata link/path for debug.

## Simple Mode vs Advanced Mode

### Simple Mode

Simple mode should hide raw `format_id` details and offer intent-driven choices:

- best audio;
- mp3;
- m4a;
- wav;
- mp4 720p;
- mp4 1080p;
- best available.

Simple mode maps user choices to normalized options and future processing policies. Example: `mp3` may choose best audio input and later convert through `ffmpeg`; it is not necessarily a native source format.

### Advanced Mode

Advanced mode should show:

- real `format_id` from `yt-dlp`;
- container/ext;
- codec;
- bitrate;
- filesize/filesize_approx;
- FPS;
- resolution;
- protocol;
- merge requirement;
- per-option warnings.

## Empty States

| Situation | UI Behavior |
|---|---|
| No subtitles | Show "No manual subtitles detected" and disable manual subtitles selector. |
| No automatic captions | Show "No automatic captions detected" and disable auto captions selector. |
| No video formats | Disable video output choices and show warning `no_video_formats`. |
| No audio formats | Disable audio/transcript choices and show warning `no_audio_formats`. |
| Unsupported link | Show blocking error with suggested user action. |
| Login/cookies needed | Show recoverable error/warning; cookies are future manual option, not automatic. |
| Source analysis failed | Show error summary, technical details excerpt, retry option if recoverable. |

## Phase 3 Contract Verdict

The future analyze response should be a normalized Pydantic/FastAPI response model centered on `AnalyzeResult`, not a direct pass-through of `yt-dlp` raw JSON. The raw JSON should remain available by reference for debugging.

