# Phase 3 Backend Model Notes

Date: 2026-05-29

## Scope

These are notes for a future backend implementation. No backend code was created in Phase 3.

## Future Model Strategy

Use Pydantic v2 models for:

- `AnalyzeResult`;
- `UploaderInfo`;
- `AccessState`;
- `MediaOptions`;
- `MediaOption`;
- `SubtitleOption`;
- `WarningState`;
- `ErrorState`;
- `LegalSafetyState`.

FastAPI should expose the analyze response through a response model so it can validate and serialize output and generate OpenAPI schema.

## Fields To Take Directly From `yt-dlp`

Use direct mappings when present:

- `original_url` -> `source_url`;
- `extractor` -> `extractor`;
- `extractor_key` -> `extractor_key`;
- `title` -> `title`;
- `duration` -> `duration_seconds`;
- `thumbnail` -> `thumbnail_url`;
- `webpage_url` -> `webpage_url`;
- `uploader`, `uploader_id`, `uploader_url`;
- `channel`, `channel_id`, `channel_url`;
- `availability`;
- `is_live`;
- `live_status`;
- `age_limit`;
- `_has_drm`;
- `playable_in_embed`;
- `subtitles`;
- `automatic_captions`;
- selected metadata such as `upload_date`, `timestamp`, `description`, `tags`, `categories`, `license`, `view_count`, `like_count`, `comment_count`.

## Fields To Compute

- `schema_version`: fixed by the app contract, starting at `1.0`.
- `analysis_id`: local generated ID, not from `yt-dlp`.
- `source_type`: derive from `extractor` or source mode. For YouTube, normalize to `youtube`; for local file, use `local_file`.
- `duration_label`: format seconds as `H:MM:SS` or `M:SS`.
- `access_state.login_required`: derive from extractor errors or future known error parsing.
- `access_state.cookies_required`: derive from extractor errors or user settings; do not auto-read cookies.
- `media_options`: derive from raw `formats`.
- `is_default_recommended`: derive using app recommendation rules.
- `requires_merge`: true for video-only options when the user wants a final playable video with audio.
- `display_label`: generate for UI; do not make frontend build labels from raw fields.
- `warnings`: derive from missing subtitles/captions, unknown sizes, source type, and analysis mode.
- `errors`: derive from failed CLI command, invalid JSON, unsupported source, login/cookie errors, or blocked source.

## Format Grouping Rules

Ignore helper/storyboard formats for media selectors:

- formats with both `vcodec == "none"` and `acodec == "none"`;
- storyboard/image-only formats such as `mhtml`.

Classify remaining formats:

- `audio`: `acodec` exists and is not `none`, while `vcodec` is missing or `none`;
- `video`: `vcodec` exists and is not `none`, while `acodec` is missing or `none`;
- `combined`: both `vcodec` and `acodec` exist and neither is `none`.

Normalize fields:

- `container` and `ext` from raw `ext`;
- `audio_codec` from `acodec`, but convert `none` to null;
- `video_codec` from `vcodec`, but convert `none` to null;
- `bitrate` from `tbr`;
- `audio_bitrate` from `abr`;
- `video_bitrate` from `vbr`;
- `sample_rate` from `asr`;
- `filesize` and `filesize_approx` as byte counts;
- `quality_label` from `format_note` or resolution.

## Recommended Defaults

Initial recommendation rules:

- Best audio: highest practical audio bitrate with common container preference. For Phase 2 sample, `140` is recommended over `251` because `251` reports very low bitrate despite "medium" note.
- Best video-only: highest resolution/FPS with known downloadable protocol. For Phase 2 sample, `137` is best video-only.
- Best combined: prefer combined format near 720p for simple mode to reduce file size and avoid merge. For Phase 2 sample, `95` is recommended for `mp4_720p`; `96` is available for 1080p.
- Best available: prefer combined 720p unless the user explicitly chooses 1080p or advanced mode.

Recommendation rules should be documented and deterministic, but not hard-coded to YouTube IDs.

## Missing Field Handling

The backend must not assume presence of:

- exact filesize;
- approximate filesize;
- thumbnails;
- uploader/channel;
- subtitles/captions;
- FPS;
- width/height;
- language;
- license;
- view/like/comment counts.

Use nulls and warnings rather than throwing errors for optional missing fields. Throw or return blocking errors only when analysis itself fails or no usable media option exists for the requested action.

## Raw Artifact Reference

Store the raw `yt-dlp` JSON under a proof/job-specific path and set:

- `raw_reference_path`: relative project path or future job artifact path.

Do not embed the full raw JSON in `AnalyzeResult`. It is too large and too unstable for the UI contract.

## Keeping UI Stable When `yt-dlp` Changes

- Treat raw `yt-dlp` as untrusted external shape.
- Keep the normalized contract stable across extractor changes.
- Preserve unknown raw fields only in raw artifacts.
- Add warnings when expected fields disappear.
- Use `schema_version` for contract changes.
- Make frontend depend only on normalized fields.
- Store `extractor`, `extractor_key`, and raw reference for debugging regressions.

## Error Mapping Notes

Future backend should map CLI failures into `ErrorState`:

- `unsupported_source`: extractor cannot identify or handle URL.
- `network_error`: connection, timeout, DNS, or transient HTTP failure.
- `login_required`: source reports private/auth/login requirement.
- `cookies_required`: source likely needs user-provided cookies.
- `extractor_failed`: extractor matched but failed.
- `invalid_output`: CLI returned malformed JSON.
- `timeout`: analysis exceeded local time limit.

Every error should include `recoverable` and `suggested_user_action`.

