# Phase 5 yt-dlp Normalizer

Date: 2026-05-29

## Scope

Phase 5 created a parser/normalizer that converts an already-loaded `yt-dlp --dump-json` dictionary into the normalized `AnalyzeResult` Pydantic model.

No FastAPI app, routes, frontend, downloader module, media download, Whisper run, MVP, Chrome extension, or desktop wrapper was created. The normalizer does not call `yt-dlp`; it only works with an existing raw dictionary.

## Implemented

File: `src/universal_media_extractor/normalizers/ytdlp.py`

Public function:

```python
normalize_ytdlp_info(raw: dict, raw_reference_path: str | None = None) -> AnalyzeResult
```

Helper behavior:

- determine `source_type`;
- extract uploader/channel data;
- extract access and availability fields;
- group formats into audio-only, video-only, and combined video+audio;
- build UI `display_label` strings;
- determine recommended options;
- extract manual subtitles;
- extract automatic captions;
- build warnings;
- safely handle missing fields with nulls, empty arrays, and warnings.

## Normalized Fields

Direct or normalized mappings include:

- source identity: `source_url`, `source_type`, `extractor`, `extractor_key`;
- display metadata: `title`, `duration_seconds`, `duration_label`, `thumbnail_url`, `webpage_url`;
- uploader/channel: `uploader`, `uploader_id`, `uploader_url`, `channel`, `channel_id`, `channel_url`;
- access state: `availability`, `is_live`, `live_status`, `age_limit`, `_has_drm`, `playable_in_embed`;
- media options: `format_id`, type, container/ext, codecs, resolution, dimensions, FPS, bitrate, sizes, protocol, merge requirement;
- subtitles and automatic captions;
- selected metadata such as upload date, timestamp, tags, categories, license, and counts;
- raw artifact reference via `raw_reference_path`.

## Format Grouping

The normalizer skips helper/storyboard formats such as `mhtml` and formats with no audio and no video codec.

Formats are grouped as:

- `audio`: has audio codec and no video codec;
- `video`: has video codec and no audio codec;
- `combined`: has both audio and video codecs.

For the Phase 2 `Showreel` sample, the normalizer finds:

- 3 audio-only options;
- 4 video-only options;
- 5 combined video+audio options.

## Display Labels

Display labels are generated in the backend/normalizer so the future UI can render stable labels without knowing raw `yt-dlp` field details.

Labels include:

- container/ext;
- quality or resolution;
- audio/video role;
- FPS where relevant;
- bitrate where relevant;
- exact or approximate size when available;
- `size unknown` when neither `filesize` nor `filesize_approx` is present.

## Recommended Options

The initial recommendation strategy is deterministic:

- best audio: highest practical audio bitrate, with common audio containers preferred;
- best video-only: highest height/FPS/bitrate;
- best combined: prefer a combined 720p option when available, otherwise highest video score;
- simple mode defaults include best audio, m4a, 720p, 1080p, and best available when matching options exist.

For the Phase 2 sample:

- best audio: `140`;
- best video-only: `137`;
- best combined: `95`.

## Warnings Added

The normalizer can add:

- `no_subtitles`;
- `no_automatic_captions`;
- `no_audio_formats`;
- `no_video_formats`;
- `format_size_unknown`;
- `platform_terms_warning`;
- `best_effort_extractor`;
- `analysis_only_not_download_tested`.

For the Phase 2 sample, required warnings are present:

- `no_subtitles`;
- `no_automatic_captions`;
- `platform_terms_warning`;
- `best_effort_extractor`;
- `analysis_only_not_download_tested`.

## Tests Added

File: `tests/test_ytdlp_normalizer.py`

The tests:

- load `proof/phase_2/url_analysis_raw.json`;
- normalize it with `normalize_ytdlp_info`;
- assert the result is an `AnalyzeResult`;
- verify title, duration, extractor, source type, and thumbnail;
- verify audio/video/combined groups;
- verify empty subtitles and automatic captions;
- verify warnings;
- export to JSON and revalidate through `AnalyzeResult`.

## Limitations

- No `yt-dlp` command execution is implemented.
- No URL analysis orchestration is implemented.
- No local-file or `ffprobe` normalizer exists yet.
- No FastAPI route or app exists.
- Login/cookies detection remains basic and conservative; cookies are still a future manual option.
- Error mapping from real CLI failures is not implemented because Phase 5 only normalizes successful raw JSON.
- The normalizer is based on one real YouTube proof sample and should be hardened with more user-approved samples later.

