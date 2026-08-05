"""Local Whisper transcription service."""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from universal_media_extractor.error_mapping import normalize_cli_error
from universal_media_extractor.models import (
    ErrorState,
    TranscriptionRequest,
    TranscriptionResult,
)
from universal_media_extractor.services.output_manager import OutputManager
from universal_media_extractor.services.safety_service import SafetyService

if TYPE_CHECKING:
    from universal_media_extractor.services.job_service import JobService


DEFAULT_TRANSCRIPTION_TIMEOUT_SECONDS = 3600
AUDIO_EXTENSIONS = {".aac", ".aiff", ".flac", ".m4a", ".mp3", ".ogg", ".opus", ".wav", ".wma"}
VIDEO_EXTENSIONS = {".avi", ".m4v", ".mkv", ".mov", ".mp4", ".mpeg", ".mpg", ".webm"}


@dataclass(frozen=True)
class CommandRunResult:
    error: ErrorState | None = None
    cancelled: bool = False


class TranscriptionService:
    """Create transcript artifacts from a local audio or video file."""

    def __init__(
        self,
        *,
        safety_service: SafetyService | None = None,
        output_manager: OutputManager | None = None,
        timeout_seconds: int = DEFAULT_TRANSCRIPTION_TIMEOUT_SECONDS,
    ) -> None:
        self.safety_service = safety_service or SafetyService()
        self.output_manager = output_manager or OutputManager()
        self.timeout_seconds = timeout_seconds

    def transcribe_file(
        self,
        request: TranscriptionRequest,
        *,
        job_service: "JobService | None" = None,
        job_id: str | None = None,
    ) -> TranscriptionResult:
        """Run ffmpeg when needed, then Whisper, then normalize artifacts."""

        if not self.safety_service.require_rights_confirmation(
            request.user_confirmed_rights
        ):
            return TranscriptionResult(
                status="blocked",
                input_file_path=request.input_file_path,
                errors=[
                    ErrorState(
                        code="rights_confirmation_required",
                        message="Rights confirmation is required before transcription.",
                        recoverable=True,
                        suggested_user_action="Confirm you have the right to process this media, then retry.",
                    )
                ],
            )

        _update_job_step(job_service, job_id, "preparing_transcription", 0)
        input_path = Path(request.input_file_path).expanduser().resolve()
        if not input_path.is_file():
            return TranscriptionResult(
                status="failed",
                input_file_path=request.input_file_path,
                errors=[
                    ErrorState(
                        code="invalid_input_file",
                        message="Input file does not exist.",
                        technical_details=str(input_path),
                        recoverable=True,
                        suggested_user_action="Choose a downloaded local media file and retry.",
                    )
                ],
            )

        output_dir = self.output_manager.ensure_transcription_output_structure(
            _resolve_output_dir(input_path, request.output_dir)
        )
        metadata_dir = _artifact_dir(output_dir, "metadata")
        logs_dir = _artifact_dir(output_dir, "logs")
        work_dir = _artifact_dir(output_dir, "work")
        whisper_work_dir = work_dir / "whisper"
        whisper_work_dir.mkdir(parents=True, exist_ok=True)
        log_path = logs_dir / "transcription.log"
        request_path = metadata_dir / "transcription_request.json"
        result_path = metadata_dir / "transcription_result.json"
        request_path.write_text(request.model_dump_json(indent=2), encoding="utf-8")
        log_path.write_text("Transcription log\n\n", encoding="utf-8")

        media_kind = _detect_media_kind(input_path, request.source_kind)
        whisper_input = input_path
        extracted_audio_path: Path | None = None

        if media_kind == "video":
            extracted_audio_path = work_dir / "extracted_audio.wav"
            _update_job_step(job_service, job_id, "extracting_audio", 10)
            ffmpeg_result = self._extract_audio(
                input_path,
                extracted_audio_path,
                log_path,
                job_service=job_service,
                job_id=job_id,
            )
            if ffmpeg_result.cancelled:
                result = _cancelled_result(
                    request,
                    output_dir,
                    log_path,
                    result_path,
                    extracted_audio_path=extracted_audio_path,
                )
                result_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
                return result
            if ffmpeg_result.error is not None:
                result = _failed_result(
                    request,
                    output_dir,
                    log_path,
                    result_path,
                    ffmpeg_result.error,
                    extracted_audio_path=extracted_audio_path,
                )
                result_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
                return result
            whisper_input = extracted_audio_path

        _update_job_step(job_service, job_id, "running_whisper", 35 if media_kind == "video" else 10)
        whisper_result = self._run_whisper(
            whisper_input,
            request,
            whisper_work_dir,
            log_path,
            job_service=job_service,
            job_id=job_id,
        )
        if whisper_result.cancelled:
            result = _cancelled_result(
                request,
                output_dir,
                log_path,
                result_path,
                extracted_audio_path=extracted_audio_path,
            )
            result_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
            return result
        if whisper_result.error is not None:
            result = _failed_result(
                request,
                output_dir,
                log_path,
                result_path,
                whisper_result.error,
                extracted_audio_path=extracted_audio_path,
            )
            result_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
            return result

        _update_job_step(job_service, job_id, "generating_transcript_files", 90)
        artifacts = _normalize_transcript_artifacts(
            whisper_work_dir,
            output_dir,
            source_stem=whisper_input.stem,
            original_input=input_path,
            model=request.model,
            transcript_format=request.transcript_format,
        )
        result = TranscriptionResult(
            status="succeeded",
            input_file_path=str(input_path),
            output_dir=str(output_dir),
            transcript_txt_path=str(artifacts["txt"]) if artifacts.get("txt") else None,
            transcript_md_path=str(artifacts["md"]) if artifacts.get("md") else None,
            transcript_json_path=str(artifacts["json"]) if artifacts.get("json") else None,
            transcript_text=artifacts["transcript_text"],
            extracted_audio_path=str(extracted_audio_path) if extracted_audio_path else None,
            log_path=str(log_path),
        )
        result_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        return result

    def _extract_audio(
        self,
        input_path: Path,
        extracted_audio_path: Path,
        log_path: Path,
        *,
        job_service: "JobService | None" = None,
        job_id: str | None = None,
    ) -> CommandRunResult:
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-acodec",
            "pcm_s16le",
            str(extracted_audio_path),
        ]
        return _run_command(
            command,
            log_path,
            timeout_seconds=self.timeout_seconds,
            not_found_code="ffmpeg_not_found",
            failed_code="transcription_failed",
            failed_message="ffmpeg audio extraction failed.",
            job_service=job_service,
            job_id=job_id,
        )

    def _run_whisper(
        self,
        input_path: Path,
        request: TranscriptionRequest,
        transcripts_dir: Path,
        log_path: Path,
        *,
        job_service: "JobService | None" = None,
        job_id: str | None = None,
    ) -> CommandRunResult:
        command = [
            "whisper",
            str(input_path),
            "--model",
            request.model,
            "--output_dir",
            str(transcripts_dir),
            "--output_format",
            "all",
        ]
        if request.language:
            command.extend(["--language", request.language])
        return _run_command(
            command,
            log_path,
            timeout_seconds=self.timeout_seconds,
            not_found_code="whisper_not_found",
            failed_code="transcription_failed",
            failed_message="Whisper transcription failed.",
            job_service=job_service,
            job_id=job_id,
        )


def _run_command(
    command: list[str],
    log_path: Path,
    *,
    timeout_seconds: int,
    not_found_code: str,
    failed_code: str,
    failed_message: str,
    job_service: "JobService | None" = None,
    job_id: str | None = None,
) -> CommandRunResult:
    _append_log(log_path, "Command:\n" + json.dumps(command, indent=2) + "\n")
    process: subprocess.Popen[str] | None = None
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False,
        )
    except FileNotFoundError as exc:
        return CommandRunResult(
            error=ErrorState(
                code=not_found_code,
                message=f"{command[0]} was not found.",
                technical_details=str(exc),
                recoverable=True,
                suggested_user_action=f"Install {command[0]} or check PATH, then retry.",
            )
        )

    if job_service and job_id:
        job_service.register_subprocess(job_id, process)

    try:
        try:
            stdout, stderr = process.communicate(timeout=timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            _stop_process(process)
            stdout = _ensure_text(exc.stdout)
            stderr = _ensure_text(exc.stderr)
            _append_log(log_path, stdout + "\n" + stderr)
            return CommandRunResult(
                error=ErrorState(
                    code="timeout",
                    message="Transcription timed out.",
                    technical_details=_compact_details(stderr or stdout),
                    recoverable=True,
                    suggested_user_action="Retry with a shorter file or smaller model.",
                )
            )
    finally:
        if job_service and job_id and process is not None:
            job_service.clear_subprocess(job_id, process)

    if job_service and job_id and job_service.is_cancel_requested(job_id):
        _append_log(log_path, "Command cancelled by user request.\n")
        return CommandRunResult(cancelled=True)

    _append_log(log_path, "stdout:\n" + stdout + "\n\nstderr:\n" + stderr + "\n")
    if process.returncode != 0:
        return CommandRunResult(
            error=normalize_cli_error(
                stderr or stdout,
                default_code=failed_code,
                default_message=failed_message,
                default_suggested_user_action="Check the local media file and retry.",
                engine=command[0] if command[0] in {"ffmpeg", "whisper"} else "unknown",
            )
        )
    return CommandRunResult()


def _update_job_step(
    job_service: "JobService | None",
    job_id: str | None,
    current_step: str,
    progress_percent: float | None = None,
) -> None:
    if job_service is None or job_id is None:
        return
    try:
        job_service.update_job_step(job_id, current_step, progress_percent)
    except KeyError:
        return


def _stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)


def _normalize_transcript_artifacts(
    whisper_work_dir: Path,
    output_dir: Path,
    *,
    source_stem: str,
    original_input: Path,
    model: str,
    transcript_format: str,
) -> dict[str, Path]:
    generated_txt = whisper_work_dir / f"{source_stem}.txt"
    generated_json = whisper_work_dir / f"{source_stem}.json"
    transcript_txt = output_dir / "transcript.txt"
    transcript_json = output_dir / "transcript.json"
    transcript_md = output_dir / "transcript.md"

    text = generated_txt.read_text(encoding="utf-8") if generated_txt.exists() else ""
    artifacts: dict[str, Path | str | None] = {
        "txt": None,
        "json": None,
        "md": None,
        "transcript_text": text,
    }

    if transcript_format == "txt":
        transcript_txt.write_text(text, encoding="utf-8")
        artifacts["txt"] = transcript_txt
    elif transcript_format == "json":
        if generated_json.exists():
            shutil.copyfile(generated_json, transcript_json)
        else:
            transcript_json.write_text(
                json.dumps({"text": text, "segments": []}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        artifacts["json"] = transcript_json
    else:
        transcript_md.write_text(
            "# Transcript\n\n"
            f"- Source file: `{original_input.name}`\n"
            f"- Whisper model: `{model}`\n\n"
            "## Text\n\n"
            f"{text.strip()}\n",
            encoding="utf-8",
        )
        artifacts["md"] = transcript_md

    return artifacts


def _resolve_output_dir(input_path: Path, output_dir: str | None) -> Path:
    if output_dir:
        return Path(output_dir)
    if input_path.parent.name == "media":
        return input_path.parent.parent
    if (input_path.parent / ".metadata").is_dir() or (
        input_path.parent / "download_request.json"
    ).is_file():
        return input_path.parent
    return input_path.parent / "transcription_output"


def _artifact_dir(output_dir: Path, name: str) -> Path:
    hidden_dir = output_dir / f".{name}"
    visible_dir = output_dir / name
    path = hidden_dir if hidden_dir.exists() else visible_dir
    path.mkdir(parents=True, exist_ok=True)
    return path


def _detect_media_kind(input_path: Path, requested_kind: str) -> str:
    if requested_kind in {"audio", "video"}:
        return requested_kind
    suffix = input_path.suffix.lower()
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    return "audio"


def _failed_result(
    request: TranscriptionRequest,
    output_dir: Path,
    log_path: Path,
    result_path: Path,
    error: ErrorState,
    *,
    extracted_audio_path: Path | None = None,
) -> TranscriptionResult:
    return TranscriptionResult(
        status="failed",
        input_file_path=request.input_file_path,
        output_dir=str(output_dir),
        extracted_audio_path=str(extracted_audio_path) if extracted_audio_path else None,
        log_path=str(log_path),
        errors=[error],
    )


def _cancelled_result(
    request: TranscriptionRequest,
    output_dir: Path,
    log_path: Path,
    result_path: Path,
    *,
    extracted_audio_path: Path | None = None,
) -> TranscriptionResult:
    return TranscriptionResult(
        status="cancelled",
        input_file_path=request.input_file_path,
        output_dir=str(output_dir),
        extracted_audio_path=str(extracted_audio_path) if extracted_audio_path else None,
        log_path=str(log_path),
    )


def _append_log(log_path: Path, text: str) -> None:
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(text)
        if not text.endswith("\n"):
            handle.write("\n")


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
