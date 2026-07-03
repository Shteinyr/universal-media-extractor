# Phase 2 URL Proof Check

Date: 2026-05-29

## Scope

Phase 2 performed a safe URL analysis proof check with `yt-dlp`. No media download was authorized or performed. No backend app, frontend, routes, downloader module, transcription module, Chrome extension, desktop wrapper, or Whisper media transcription was created or run.

## Source

- Source URL: `https://youtu.be/UUdxAp3kuKA`
- User confirmation: user stated this is their video.
- Analysis mode: `yt-dlp` metadata/listing only.
- Download performed: `no`

## Commands Executed

```bash
mkdir -p proof/phase_2
yt-dlp --simulate --dump-json "https://youtu.be/UUdxAp3kuKA" > proof/phase_2/url_analysis_raw.json
yt-dlp --list-formats "https://youtu.be/UUdxAp3kuKA" > proof/phase_2/list_formats_raw.txt
yt-dlp --list-subs "https://youtu.be/UUdxAp3kuKA" > proof/phase_2/list_subs_raw.txt
```

Context7 documentation check confirmed that `--dump-json` simulates unless `--no-simulate` is used, `--list-formats` simulates by default unless `--no-simulate` is used, and `--simulate` prevents video download and disk writes.

## Raw Outputs

- `proof/phase_2/url_analysis_raw.json` - 49 KiB
- `proof/phase_2/list_formats_raw.txt` - 2.1 KiB
- `proof/phase_2/list_subs_raw.txt` - 389 B

Only these proof files were written under `proof/phase_2`.

## Extracted Metadata

| Field | Value |
|---|---|
| `id` | `UUdxAp3kuKA` |
| `title` | `Showreel` |
| `duration` | `39` seconds |
| `extractor` | `youtube` |
| `extractor_key` | `Youtube` |
| `webpage_url` | `https://www.youtube.com/watch?v=UUdxAp3kuKA` |
| `thumbnail` | `https://i.ytimg.com/vi/UUdxAp3kuKA/maxresdefault.jpg` |
| `formats` count | `16` |
| `requested_downloads` | `None` |
| subtitles | none |
| automatic captions | none |

## Available Audio Formats

| Format ID | Ext | Audio Codec | Bitrate | Sample Rate | Approx Size | Note |
|---|---|---|---:|---:|---:|---|
| `139` | `m4a` | `mp4a.40.5` | ~49k | 22k | ~233 KiB | low |
| `140` | `m4a` | `mp4a.40.2` | ~130k | 44k | ~617 KiB | medium |
| `251` | `webm` | `opus` | ~4k | 48k | ~17 KiB | medium |

## Available Video-Only Formats

| Format ID | Ext | Resolution | FPS | Video Codec | Bitrate | Approx Size | Note |
|---|---|---:|---:|---|---:|---:|---|
| `160` | `mp4` | `256x144` | 24 | `avc1.4d400c` | ~100k | ~476 KiB | 144p |
| `134` | `mp4` | `640x360` | 24 | `avc1.4d401e` | ~427k | ~1.98 MiB | 360p |
| `136` | `mp4` | `1280x720` | 24 | `avc1.64001f` | ~1582k | ~7.34 MiB | 720p |
| `137` | `mp4` | `1920x1080` | 24 | `avc1.640028` | ~2636k | ~12.23 MiB | 1080p |

## Available Combined Video+Audio Formats

| Format ID | Ext | Resolution | FPS | Video Codec | Audio Codec | Bitrate / Size |
|---|---|---:|---:|---|---|---|
| `91` | `mp4` | `256x144` | 24 | `avc1.4D400C` | `mp4a.40.5` | ~179k / unknown |
| `93` | `mp4` | `640x360` | 24 | `avc1.4D401E` | `mp4a.40.2` | ~766k / unknown |
| `18` | `mp4` | `640x360` | 24 | `avc1.42001E` | `mp4a.40.2` | ~556k / ~2.58 MiB |
| `95` | `mp4` | `1280x720` | 24 | `avc1.64001F` | `mp4a.40.2` | ~2447k / unknown |
| `96` | `mp4` | `1920x1080` | 24 | `avc1.640028` | `mp4a.40.2` | ~4069k / unknown |

## Subtitles And Automatic Captions

`yt-dlp --list-subs` reported:

- no automatic captions;
- no subtitles.

## Fields Available From `yt-dlp`

The raw JSON included UI-relevant top-level fields such as:

- identity: `id`, `display_id`, `title`, `fulltitle`, `webpage_url`, `original_url`;
- source: `extractor`, `extractor_key`, `webpage_url_domain`, `availability`;
- media details: `duration`, `duration_string`, `width`, `height`, `fps`, `resolution`, `aspect_ratio`, `dynamic_range`, `is_live`, `live_status`;
- owner/channel: `uploader`, `uploader_id`, `uploader_url`, `channel`, `channel_id`, `channel_url`;
- assets: `thumbnail`, `thumbnails`;
- formats: `formats`, `format_id`, `format`, `ext`, `vcodec`, `acodec`, `abr`, `vbr`, `tbr`, `filesize_approx`, `protocol`;
- subtitles: `subtitles`, `automatic_captions`, `requested_subtitles`;
- metadata: `description`, `tags`, `categories`, `upload_date`, `timestamp`, `view_count`, `like_count`, `comment_count`;
- safety/status: `_has_drm`, `age_limit`, `playable_in_embed`, `license`.

## Data Suitable For Future UI

- Source summary: extractor, title, duration, thumbnail, original URL.
- Audio options: format ID, extension, codec, bitrate, sample rate, approximate size.
- Video options: format ID, resolution, FPS, codec, bitrate, approximate size.
- Combined options: format ID, resolution, codecs, protocol, approximate size when available.
- Subtitle/caption panel: empty state for this URL.
- Metadata/details panel: uploader/channel, upload date, description, tags, view count, raw metadata availability.
- Warnings panel: best-effort source support, no subtitles found, some sizes unknown, YouTube/platform restrictions still apply.

## Limitations Found

- Some format sizes are unknown in listing output.
- No subtitles or automatic captions were available for this URL.
- `yt-dlp` used YouTube webpage/API/player requests and JS challenge solving to analyze the URL; this reinforces that support can be affected by platform changes.
- This proof checks analysis only. It does not prove actual download, merge, conversion, or transcription behavior.
- YouTube support remains best-effort and subject to platform terms and technical changes.

## Phase 2 Verdict

URL analysis through `yt-dlp` is confirmed for the provided user-owned YouTube URL without downloading media.

