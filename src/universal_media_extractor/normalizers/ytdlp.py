"""Normalize yt-dlp info JSON into the stable AnalyzeResult contract."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from universal_media_extractor.models import (
    AccessState,
    AnalyzeResult,
    LegalSafetyState,
    MediaOption,
    MediaOptions,
    SubtitleOption,
    UploaderInfo,
    WarningState,
)
from universal_media_extractor.models.analyze import RecommendedOptions, WarningCode


RIGHTS_CONFIRMATION_TEXT = (
    "I confirm that I own this media or have the necessary rights to download, "
    "extract, convert, and/or transcribe it locally."
)


def normalize_ytdlp_info(
    raw: dict[str, Any], raw_reference_path: str | None = None
) -> AnalyzeResult:
    """Convert a yt-dlp ``--dump-json`` dictionary into ``AnalyzeResult``.

    This function is pure with respect to media handling: it does not call
    yt-dlp, download media, invoke ffmpeg, run Whisper, or persist raw JSON.
    """

    media_options = _extract_media_options(raw.get("formats") or [])
    subtitles = _extract_subtitles(raw.get("subtitles") or {}, subtitle_type="manual")
    automatic_captions = _extract_subtitles(
        raw.get("automatic_captions") or {}, subtitle_type="automatic"
    )
    warnings = _build_warnings(media_options, subtitles, automatic_captions)

    return AnalyzeResult(
        schema_version="1.0",
        analysis_id=_build_analysis_id(raw),
        source_url=_first_string(raw.get("original_url"), raw.get("webpage_url")) or "unknown",
        source_type=_determine_source_type(raw),
        extractor=_as_optional_string(raw.get("extractor")),
        extractor_key=_as_optional_string(raw.get("extractor_key")),
        title=_as_optional_string(raw.get("title")),
        duration_seconds=_as_optional_number(raw.get("duration")),
        duration_label=_format_duration(raw.get("duration")),
        thumbnail_url=_as_optional_string(raw.get("thumbnail")),
        webpage_url=_as_optional_string(raw.get("webpage_url")),
        uploader=_extract_uploader(raw),
        availability=_as_optional_string(raw.get("availability")),
        access_state=_extract_access_state(raw),
        media_options=media_options,
        subtitles=subtitles,
        automatic_captions=automatic_captions,
        metadata=_extract_metadata(raw, ignored_format_ids=_ignored_format_ids(raw)),
        warnings=warnings,
        errors=[],
        legal_safety=LegalSafetyState(
            user_confirmed_rights=False,
            confirmation_text=RIGHTS_CONFIRMATION_TEXT,
            required_before_download=True,
            required_before_transcription=True,
            accepted_at=None,
        ),
        raw_reference_path=raw_reference_path,
        analyzed_at=datetime.now(timezone.utc),
    )


def _determine_source_type(raw: dict[str, Any]) -> str:
    extractor_key = _as_optional_string(raw.get("extractor_key")) or ""
    extractor = _as_optional_string(raw.get("extractor")) or ""
    original_url = _as_optional_string(raw.get("original_url")) or ""

    source_hint = f"{extractor_key} {extractor}".lower()
    if "youtube" in source_hint:
        return "youtube"
    if original_url.startswith("file://"):
        return "local_file"
    if original_url:
        return "url"
    return "unknown"


def _extract_uploader(raw: dict[str, Any]) -> UploaderInfo | None:
    fields = {
        "name": _first_string(raw.get("uploader"), raw.get("channel")),
        "id": _first_string(raw.get("uploader_id"), raw.get("channel_id")),
        "url": _first_string(raw.get("uploader_url"), raw.get("channel_url")),
        "channel_name": _as_optional_string(raw.get("channel")),
        "channel_id": _as_optional_string(raw.get("channel_id")),
        "channel_url": _as_optional_string(raw.get("channel_url")),
    }
    if not any(fields.values()):
        return None
    return UploaderInfo(**fields)


def _extract_access_state(raw: dict[str, Any]) -> AccessState:
    return AccessState(
        availability=_as_optional_string(raw.get("availability")),
        is_live=bool(raw.get("is_live") or False),
        live_status=_as_optional_string(raw.get("live_status")),
        age_limit=_as_optional_int(raw.get("age_limit")),
        has_drm=_as_optional_bool(raw.get("_has_drm")),
        login_required=False,
        cookies_required=False,
        playable_in_embed=_as_optional_bool(raw.get("playable_in_embed")),
    )


def _extract_media_options(formats: list[dict[str, Any]]) -> MediaOptions:
    audio: list[MediaOption] = []
    video: list[MediaOption] = []
    combined: list[MediaOption] = []

    for item in formats:
        if not isinstance(item, dict) or _is_helper_format(item):
            continue

        media_type = _classify_format(item)
        if media_type is None:
            continue

        option = _build_media_option(item, media_type)
        if media_type == "audio":
            audio.append(option)
        elif media_type == "video":
            video.append(option)
        else:
            combined.append(option)

    recommended = _build_recommended_options(audio, video, combined)
    audio = _mark_recommended(audio, recommended.best_audio_format_id)
    video = _mark_recommended(video, recommended.best_video_format_id)
    combined = _mark_recommended(combined, recommended.best_combined_format_id)

    return MediaOptions(
        audio=audio,
        video=video,
        combined=combined,
        recommended=recommended,
    )


def _classify_format(item: dict[str, Any]) -> str | None:
    acodec = _as_optional_string(item.get("acodec"))
    vcodec = _as_optional_string(item.get("vcodec"))
    has_audio = bool(acodec and acodec != "none")
    has_video = bool(vcodec and vcodec != "none")

    if has_audio and not has_video:
        return "audio"
    if has_video and not has_audio:
        return "video"
    if has_audio and has_video:
        return "combined"
    return None


def _build_media_option(item: dict[str, Any], media_type: str) -> MediaOption:
    format_id = str(item.get("format_id") or item.get("format") or "unknown")
    ext = _as_optional_string(item.get("ext"))
    acodec = _clean_codec(item.get("acodec"))
    vcodec = _clean_codec(item.get("vcodec"))
    filesize = _as_optional_int(item.get("filesize"))
    filesize_approx = _as_optional_int(item.get("filesize_approx"))
    warnings: list[WarningCode] = []
    if filesize is None and filesize_approx is None:
        warnings.append("format_size_unknown")

    return MediaOption(
        id=format_id,
        format_id=format_id,
        type=media_type,  # type: ignore[arg-type]
        container=ext,
        ext=ext,
        codec=_summarize_codec(acodec, vcodec, media_type),
        audio_codec=acodec,
        video_codec=vcodec,
        resolution=_as_optional_string(item.get("resolution")),
        width=_as_optional_int(item.get("width")),
        height=_as_optional_int(item.get("height")),
        fps=_as_optional_number(item.get("fps")),
        bitrate=_as_optional_number(item.get("tbr")),
        audio_bitrate=_as_optional_number(item.get("abr")),
        video_bitrate=_as_optional_number(item.get("vbr")),
        sample_rate=_as_optional_int(item.get("asr")),
        audio_channels=_as_optional_int(item.get("audio_channels")),
        filesize=filesize,
        filesize_approx=filesize_approx,
        language=_as_optional_string(item.get("language")),
        protocol=_as_optional_string(item.get("protocol")),
        dynamic_range=_as_optional_string(item.get("dynamic_range")),
        quality_label=_quality_label(item),
        is_default_recommended=False,
        is_downloadable=True,
        requires_merge=media_type == "video",
        display_label=_build_display_label(item, media_type, ext),
        warnings=warnings,
    )


def _build_recommended_options(
    audio: list[MediaOption], video: list[MediaOption], combined: list[MediaOption]
) -> RecommendedOptions:
    best_audio = _best_by_score(audio, _audio_score)
    best_video = _best_by_score(video, _video_score)
    best_combined = _best_combined(combined)
    combined_720 = _best_matching_height(combined, 720)
    combined_1080 = _best_matching_height(combined, 1080)
    m4a_audio = _best_by_score(
        [option for option in audio if option.ext == "m4a"], _audio_score
    )

    simple_defaults: dict[str, str] = {}
    if best_audio:
        simple_defaults["best_audio"] = best_audio.format_id
    if m4a_audio:
        simple_defaults["m4a"] = m4a_audio.format_id
    if combined_720:
        simple_defaults["mp4_720p"] = combined_720.format_id
    if combined_1080:
        simple_defaults["mp4_1080p"] = combined_1080.format_id
    if best_combined:
        simple_defaults["best_available"] = best_combined.format_id

    return RecommendedOptions(
        best_audio_format_id=best_audio.format_id if best_audio else None,
        best_video_format_id=best_video.format_id if best_video else None,
        best_combined_format_id=best_combined.format_id if best_combined else None,
        simple_mode_defaults=simple_defaults,
    )


def _extract_subtitles(
    raw_subtitles: dict[str, Any], subtitle_type: str
) -> list[SubtitleOption]:
    options: list[SubtitleOption] = []
    for language, entries in sorted(raw_subtitles.items()):
        if not isinstance(entries, list) or not entries:
            continue
        formats = sorted(
            {
                str(entry.get("ext"))
                for entry in entries
                if isinstance(entry, dict) and entry.get("ext")
            }
        )
        if not formats:
            continue
        kind = "automatic" if subtitle_type == "automatic" else "manual"
        options.append(
            SubtitleOption(
                language=str(language),
                language_label=None,
                type=kind,  # type: ignore[arg-type]
                formats=formats,
                is_available=True,
                display_label=f"{language} {kind} captions ({', '.join(formats)})",
            )
        )
    return options


def _build_warnings(
    media_options: MediaOptions,
    subtitles: list[SubtitleOption],
    automatic_captions: list[SubtitleOption],
) -> list[WarningState]:
    warnings: list[WarningState] = []
    if not subtitles:
        warnings.append(
            WarningState(
                code="no_subtitles",
                message="No manual subtitles were detected for this source.",
                severity="info",
                related_field="subtitles",
            )
        )
    if not automatic_captions:
        warnings.append(
            WarningState(
                code="no_automatic_captions",
                message="No automatic captions were detected for this source.",
                severity="info",
                related_field="automatic_captions",
            )
        )
    if not media_options.audio:
        warnings.append(
            WarningState(
                code="no_audio_formats",
                message="No audio-only formats were detected for this source.",
                severity="warning",
                related_field="media_options.audio",
            )
        )
    if not media_options.video:
        warnings.append(
            WarningState(
                code="no_video_formats",
                message="No video-only formats were detected for this source.",
                severity="warning",
                related_field="media_options.video",
            )
        )
    if any(
        "format_size_unknown" in option.warnings
        for option in [
            *media_options.audio,
            *media_options.video,
            *media_options.combined,
        ]
    ):
        warnings.append(
            WarningState(
                code="format_size_unknown",
                message=(
                    "Some media options do not expose an exact or approximate "
                    "size during analysis."
                ),
                severity="warning",
                related_field="media_options",
            )
        )

    warnings.extend(
        [
            WarningState(
                code="platform_terms_warning",
                message=(
                    "Only process media you own or have rights to process, "
                    "and follow platform terms."
                ),
                severity="warning",
                related_field="legal_safety",
            ),
            WarningState(
                code="best_effort_extractor",
                message=(
                    "Source support is best-effort and may change when the "
                    "platform changes."
                ),
                severity="warning",
                related_field="extractor",
            ),
            WarningState(
                code="analysis_only_not_download_tested",
                message=(
                    "This result proves analysis only; download, merge, "
                    "conversion, and transcription were not tested."
                ),
                severity="info",
                related_field="raw_reference_path",
            ),
        ]
    )
    return warnings


def _extract_metadata(
    raw: dict[str, Any], ignored_format_ids: list[str]
) -> dict[str, Any]:
    return {
        "id": raw.get("id"),
        "upload_date": raw.get("upload_date"),
        "timestamp": raw.get("timestamp"),
        "description": raw.get("description"),
        "tags": raw.get("tags") or [],
        "categories": raw.get("categories") or [],
        "license": raw.get("license"),
        "view_count": raw.get("view_count"),
        "like_count": raw.get("like_count"),
        "comment_count": raw.get("comment_count"),
        "format_count": len(raw.get("formats") or []),
        "raw_storyboard_format_ids_ignored_for_media_options": ignored_format_ids,
    }


def _build_analysis_id(raw: dict[str, Any]) -> str:
    source_type = _determine_source_type(raw)
    media_id = _as_optional_string(raw.get("id")) or "unknown"
    return f"{source_type}-{media_id}"


def _is_helper_format(item: dict[str, Any]) -> bool:
    ext = _as_optional_string(item.get("ext"))
    note = (_as_optional_string(item.get("format_note")) or "").lower()
    acodec = _as_optional_string(item.get("acodec"))
    vcodec = _as_optional_string(item.get("vcodec"))
    return ext == "mhtml" or note == "storyboard" or (
        acodec == "none" and vcodec == "none"
    )


def _ignored_format_ids(raw: dict[str, Any]) -> list[str]:
    ignored: list[str] = []
    for item in raw.get("formats") or []:
        if isinstance(item, dict) and _is_helper_format(item):
            format_id = _as_optional_string(item.get("format_id"))
            if format_id:
                ignored.append(format_id)
    return ignored


def _mark_recommended(
    options: list[MediaOption], recommended_format_id: str | None
) -> list[MediaOption]:
    if recommended_format_id is None:
        return options
    return [
        option.model_copy(
            update={"is_default_recommended": option.format_id == recommended_format_id}
        )
        for option in options
    ]


def _best_by_score(
    options: list[MediaOption], score_func: Any
) -> MediaOption | None:
    if not options:
        return None
    return max(options, key=score_func)


def _audio_score(option: MediaOption) -> tuple[float, int]:
    container_preference = 1 if option.ext in {"m4a", "mp3", "wav"} else 0
    bitrate = option.audio_bitrate or option.bitrate or 0
    return (bitrate, container_preference)


def _video_score(option: MediaOption) -> tuple[int, float, float]:
    return (option.height or 0, option.fps or 0, option.bitrate or 0)


def _best_combined(options: list[MediaOption]) -> MediaOption | None:
    preferred_720 = _best_matching_height(options, 720)
    if preferred_720:
        return preferred_720
    return _best_by_score(options, _video_score)


def _best_matching_height(
    options: list[MediaOption], height: int
) -> MediaOption | None:
    matching = [option for option in options if option.height == height]
    return _best_by_score(matching, _video_score)


def _build_display_label(
    item: dict[str, Any], media_type: str, ext: str | None
) -> str:
    ext_label = ext or "unknown"
    size_label = _format_size(
        _as_optional_int(item.get("filesize"))
        or _as_optional_int(item.get("filesize_approx"))
    )
    fps = _as_optional_number(item.get("fps"))
    fps_label = f" - {fps:g} fps" if fps else ""
    bitrate = _as_optional_number(item.get("tbr"))
    bitrate_label = f" - {bitrate:.0f} kbps" if bitrate else ""
    quality = _quality_label(item)
    resolution = _as_optional_string(item.get("resolution"))

    if media_type == "audio":
        codec = _clean_codec(item.get("acodec")) or "audio"
        quality_part = f" {quality}" if quality else ""
        audio_bitrate = _as_optional_number(item.get("abr")) or bitrate
        audio_rate = f" - {audio_bitrate:.0f} kbps" if audio_bitrate else ""
        return f"{ext_label} {codec} audio{quality_part}{audio_rate} - {size_label}"

    if media_type == "video":
        quality_part = quality or resolution or "video"
        return f"{ext_label} {quality_part} video-only{fps_label} - {size_label}"

    quality_part = quality or resolution or "video"
    return f"{ext_label} {quality_part} with audio{fps_label}{bitrate_label} - {size_label}"


def _quality_label(item: dict[str, Any]) -> str | None:
    note = _as_optional_string(item.get("format_note"))
    if note and note != "Default":
        return note
    height = _as_optional_int(item.get("height"))
    if height:
        return f"{height}p"
    return _as_optional_string(item.get("resolution"))


def _summarize_codec(
    acodec: str | None, vcodec: str | None, media_type: str
) -> str | None:
    if media_type == "audio":
        return acodec
    if media_type == "video":
        return vcodec
    if acodec and vcodec:
        return f"{vcodec} + {acodec}"
    return vcodec or acodec


def _clean_codec(value: Any) -> str | None:
    text = _as_optional_string(value)
    if not text or text == "none":
        return None
    return text


def _format_duration(value: Any) -> str | None:
    seconds = _as_optional_int(value)
    if seconds is None:
        return None
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def _format_size(size: int | None) -> str:
    if size is None:
        return "size unknown"
    units = ["B", "KiB", "MiB", "GiB"]
    value = float(size)
    unit = units[0]
    for unit in units:
        if value < 1024 or unit == units[-1]:
            break
        value /= 1024
    if unit == "B":
        return f"{int(value)} {unit}"
    return f"~{value:.2f} {unit}"


def _first_string(*values: Any) -> str | None:
    for value in values:
        text = _as_optional_string(value)
        if text:
            return text
    return None


def _as_optional_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _as_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_optional_number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_optional_bool(value: Any) -> bool | None:
    if value is None:
        return None
    return bool(value)

