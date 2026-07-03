"""Local file metadata analysis through ffprobe."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from universal_media_extractor.models import (
    ErrorState,
    LocalFileAnalyzeResult,
    LocalFileStreamInfo,
    WarningState,
)


DEFAULT_FFPROBE_TIMEOUT_SECONDS = 60


class LocalFileMetadataService:
    """Inspect one uploaded local media file with ffprobe."""

    def __init__(self, *, timeout_seconds: int = DEFAULT_FFPROBE_TIMEOUT_SECONDS) -> None:
        self.timeout_seconds = timeout_seconds

    def analyze_file(
        self,
        file_path: Path,
        *,
        original_filename: str | None = None,
        output_dir: Path | None = None,
    ) -> LocalFileAnalyzeResult:
        """Return normalized ffprobe metadata for a local file."""

        resolved_path = file_path.expanduser().resolve()
        filename = original_filename or resolved_path.name
        result_path = output_dir / "metadata" / "local_file_analysis.json" if output_dir else None
        log_path = output_dir / "logs" / "local_file_analysis.log" if output_dir else None

        if not resolved_path.is_file():
            result = LocalFileAnalyzeResult(
                filename=filename,
                saved_path=str(resolved_path),
                output_dir=str(output_dir) if output_dir else None,
                errors=[
                    ErrorState(
                        code="invalid_input_file",
                        message="Input file does not exist.",
                        technical_details=str(resolved_path),
                        recoverable=True,
                        suggested_user_action="Choose a valid local audio or video file.",
                    )
                ],
            )
            _write_optional(result_path, result.model_dump_json(indent=2))
            return result

        command = [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(resolved_path),
        ]
        _write_optional(log_path, "Command:\n" + json.dumps(command, indent=2) + "\n\n")

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                shell=False,
            )
        except FileNotFoundError as exc:
            result = _failed_result(
                filename,
                resolved_path,
                output_dir,
                ErrorState(
                    code="ffprobe_not_found",
                    message="ffprobe was not found.",
                    technical_details=str(exc),
                    recoverable=True,
                    suggested_user_action="Install ffmpeg/ffprobe or check PATH, then retry.",
                ),
            )
            _write_optional(result_path, result.model_dump_json(indent=2))
            return result
        except subprocess.TimeoutExpired as exc:
            _append_optional(log_path, _ensure_text(exc.stdout) + "\n" + _ensure_text(exc.stderr))
            result = _failed_result(
                filename,
                resolved_path,
                output_dir,
                ErrorState(
                    code="timeout",
                    message="Local file metadata analysis timed out.",
                    technical_details=_compact_details(exc.stderr or exc.stdout),
                    recoverable=True,
                    suggested_user_action="Try a smaller file or retry.",
                ),
            )
            _write_optional(result_path, result.model_dump_json(indent=2))
            return result

        _append_optional(
            log_path,
            "stdout:\n" + completed.stdout + "\n\nstderr:\n" + completed.stderr + "\n",
        )
        if completed.returncode != 0:
            result = _failed_result(
                filename,
                resolved_path,
                output_dir,
                ErrorState(
                    code="invalid_input_file",
                    message="ffprobe could not inspect this file.",
                    technical_details=_compact_details(completed.stderr),
                    recoverable=True,
                    suggested_user_action="Choose a supported audio or video file.",
                ),
            )
            _write_optional(result_path, result.model_dump_json(indent=2))
            return result

        try:
            raw = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            result = _failed_result(
                filename,
                resolved_path,
                output_dir,
                ErrorState(
                    code="invalid_output",
                    message="ffprobe returned invalid JSON.",
                    technical_details=str(exc),
                    recoverable=True,
                    suggested_user_action="Retry or choose another media file.",
                ),
            )
            _write_optional(result_path, result.model_dump_json(indent=2))
            return result

        result = _normalize_ffprobe(raw, filename, resolved_path, output_dir)
        _write_optional(result_path, result.model_dump_json(indent=2))
        return result


def _normalize_ffprobe(
    raw: dict,
    filename: str,
    resolved_path: Path,
    output_dir: Path | None,
) -> LocalFileAnalyzeResult:
    streams = [_stream_info(item) for item in raw.get("streams", []) if isinstance(item, dict)]
    has_video = any(stream.codec_type == "video" for stream in streams)
    has_audio = any(stream.codec_type == "audio" for stream in streams)
    media_type = "video" if has_video else "audio" if has_audio else "unknown"
    format_info = raw.get("format", {}) if isinstance(raw.get("format"), dict) else {}
    duration = _float_or_none(format_info.get("duration"))
    warnings = []
    if media_type == "unknown":
        warnings.append(
            WarningState(
                code="unsupported_source",
                message="No audio or video stream was detected.",
            )
        )
    return LocalFileAnalyzeResult(
        filename=filename,
        saved_path=str(resolved_path),
        output_dir=str(output_dir) if output_dir else None,
        media_type=media_type,
        duration_seconds=duration,
        size_bytes=resolved_path.stat().st_size,
        format_name=format_info.get("format_name"),
        format_long_name=format_info.get("format_long_name"),
        streams=streams,
        warnings=warnings,
    )


def _stream_info(raw: dict) -> LocalFileStreamInfo:
    return LocalFileStreamInfo(
        index=raw.get("index"),
        codec_type=raw.get("codec_type"),
        codec_name=raw.get("codec_name"),
        duration_seconds=_float_or_none(raw.get("duration")),
        width=raw.get("width"),
        height=raw.get("height"),
        sample_rate=_int_or_none(raw.get("sample_rate")),
        channels=raw.get("channels"),
        bit_rate=_int_or_none(raw.get("bit_rate")),
    )


def _failed_result(
    filename: str,
    resolved_path: Path,
    output_dir: Path | None,
    error: ErrorState,
) -> LocalFileAnalyzeResult:
    return LocalFileAnalyzeResult(
        filename=filename,
        saved_path=str(resolved_path),
        output_dir=str(output_dir) if output_dir else None,
        size_bytes=resolved_path.stat().st_size if resolved_path.exists() else None,
        errors=[error],
    )


def _float_or_none(value: object) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _int_or_none(value: object) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _write_optional(path: Path | None, text: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _append_optional(path: Path | None, text: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _ensure_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _compact_details(value: str | bytes | None) -> str | None:
    text = _ensure_text(value).strip()
    if not text:
        return None
    return text[-2000:]
