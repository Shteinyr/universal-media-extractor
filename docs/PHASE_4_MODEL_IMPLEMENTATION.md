# Phase 4 Model Implementation

Date: 2026-05-29

## Scope

Phase 4 created Pydantic v2 models for the Phase 3 analyze-result data contract and tests that validate the normalized Phase 3 sample JSON.

No backend app, FastAPI routes, frontend, downloader module, transcription module, media download, Whisper run, MVP, Chrome extension, or desktop wrapper was created.

## Documentation Checked

Context7 was used before implementation:

- Pydantic docs: `BaseModel`, `ConfigDict`, optional/null fields, validation with `model_validate_json()`, and serialization with `model_dump_json()`.
- FastAPI docs: response models can be declared with Pydantic models through return annotations or `response_model`, enabling validation, serialization, filtering, and OpenAPI schema generation.

## Models Created

File: `src/universal_media_extractor/models/analyze.py`

- `AnalyzeResult`
- `MediaOptions`
- `MediaOption`
- `SubtitleOption`
- `WarningState`
- `ErrorState`
- `LegalSafetyState`
- `UploaderInfo`
- `AccessState`
- `RecommendedOptions`, a small helper model for `media_options.recommended`

## Validated Field Areas

- Source identity: `source_url`, `source_type`, `extractor`, `extractor_key`, `title`, `duration_seconds`, `thumbnail_url`, `webpage_url`.
- Uploader/channel fields through `UploaderInfo`.
- Access fields through `AccessState`.
- Grouped media options: `audio`, `video`, `combined`, and `recommended`.
- Per-format fields including `format_id`, media type, container/ext, codecs, resolution, FPS, bitrate, sizes, protocol, merge requirement, and `display_label`.
- Subtitle and automatic caption lists.
- Stable warning and error states.
- Legal/safety confirmation with `user_confirmed_rights` and `required_before_download`.
- `raw_reference_path` instead of embedding raw `yt-dlp` JSON.
- `analyzed_at` as a datetime-compatible field.

## Constraints And Compromises

- Models use `extra="forbid"` to keep the normalized contract stable and prevent accidental raw `yt-dlp` pass-through.
- Some fields accept source-specific strings beyond known literals, such as `availability` and `live_status`, because extractors can return values outside the current known set.
- `source_type` is constrained to `url`, `local_file`, `youtube`, or `unknown` for now. Add new source types intentionally as support expands.
- `metadata` remains a dictionary because selected metadata can vary by source, but the full raw JSON is still excluded.
- `RecommendedOptions` was added to formalize the `recommended` object from the Phase 3 sample.

## Tests Added

File: `tests/test_analyze_models.py`

The tests:

- load `docs/PHASE_3_SAMPLE_ANALYZE_RESULT.json`;
- validate it through `AnalyzeResult`;
- confirm audio/video/combined groups validate;
- confirm empty `subtitles` and `automatic_captions` arrays are valid;
- confirm warnings validate with expected stable codes;
- confirm the model exports to JSON and validates again.

## Future `/analyze` Usage

When backend routes are authorized, the future analyze endpoint should return `AnalyzeResult` as its response model. The backend should normalize raw `yt-dlp` or `ffprobe` output into these models, store raw artifacts separately, and provide only `raw_reference_path` in the response.

## Not Implemented

- No `/analyze` route.
- No FastAPI app.
- No CLI orchestration.
- No `yt-dlp` parsing module.
- No downloader.
- No transcription module.
- No UI.
- No media download or Whisper run.

