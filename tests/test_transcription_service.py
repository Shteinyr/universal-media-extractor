import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.models import TranscriptionRequest
from universal_media_extractor.services.job_service import JobService
from universal_media_extractor.services.transcription_service import (
    TranscriptionService,
    _cancelled_result as cancelled_transcription_result,
)


def _write_whisper_outputs(command):
    output_dir = Path(command[command.index("--output_dir") + 1])
    input_path = Path(command[1])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{input_path.stem}.txt").write_text("Hello from Showreel.", encoding="utf-8")
    (output_dir / f"{input_path.stem}.json").write_text(
        json.dumps({"text": "Hello from Showreel.", "segments": []}),
        encoding="utf-8",
    )


class FakePopen:
    def __init__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        self.returncode = kwargs.pop("returncode", 0)
        self.stdout_text = kwargs.pop("stdout_text", "ok")
        self.stderr_text = kwargs.pop("stderr_text", "")
        self.terminated = False
        self.killed = False

    def communicate(self, timeout=None):
        if self.command[0] == "ffmpeg":
            Path(self.command[-1]).write_bytes(b"wav")
        if self.command[0] == "whisper" and self.returncode == 0:
            _write_whisper_outputs(self.command)
        return self.stdout_text, self.stderr_text

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        return self.returncode

    def terminate(self):
        self.terminated = True
        self.returncode = -15

    def kill(self):
        self.killed = True
        self.returncode = -9


def test_transcription_service_transcribes_audio_with_whisper(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    input_file = media_dir / "Showreel.m4a"
    input_file.write_bytes(b"audio")
    calls = []

    def fake_popen(command, **kwargs):
        calls.append((command, kwargs))
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.transcription_service.subprocess.Popen",
        fake_popen,
    )

    result = TranscriptionService(timeout_seconds=5).transcribe_file(
        TranscriptionRequest(
            input_file_path=str(input_file),
            user_confirmed_rights=True,
            model="tiny",
        )
    )

    assert result.status == "succeeded"
    assert calls[0][0][0] == "whisper"
    assert calls[0][1]["shell"] is False
    assert Path(result.transcript_txt_path).read_text(encoding="utf-8") == "Hello from Showreel."
    assert result.transcript_md_path is None
    assert result.transcript_json_path is None
    assert result.transcript_format == "txt"
    assert result.transcript_file_text == "Hello from Showreel."
    assert result.summary_prompt_path is None
    assert Path(result.log_path).name == "transcription.log"


def test_transcription_service_uses_download_root_for_user_facing_file(monkeypatch, tmp_path):
    output_dir = tmp_path / "Showreel"
    (output_dir / ".metadata").mkdir(parents=True)
    (output_dir / ".logs").mkdir()
    input_file = output_dir / "Showreel.m4a"
    input_file.write_bytes(b"audio")

    def fake_popen(command, **kwargs):
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.transcription_service.subprocess.Popen",
        fake_popen,
    )

    result = TranscriptionService(timeout_seconds=5).transcribe_file(
        TranscriptionRequest(
            input_file_path=str(input_file),
            user_confirmed_rights=True,
            model="tiny",
        )
    )

    assert result.status == "succeeded"
    assert result.output_dir == str(output_dir.resolve())
    assert Path(result.log_path).parent.name == ".logs"
    assert (output_dir / "transcript.txt").is_file()
    assert not (output_dir / "transcripts").exists()
    assert not (output_dir / "metadata").exists()
    assert not (output_dir / "logs").exists()


def test_transcription_service_saves_only_selected_markdown(monkeypatch, tmp_path):
    input_file = tmp_path / "clip.m4a"
    input_file.write_bytes(b"audio")

    def fake_popen(command, **kwargs):
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.transcription_service.subprocess.Popen",
        fake_popen,
    )

    result = TranscriptionService(timeout_seconds=5).transcribe_file(
        TranscriptionRequest(
            input_file_path=str(input_file),
            user_confirmed_rights=True,
            transcript_format="md",
        )
    )

    assert result.status == "succeeded"
    assert result.transcript_txt_path is None
    assert Path(result.transcript_md_path).name == "transcript.md"
    assert result.transcript_json_path is None
    assert result.transcript_format == "md"
    assert result.transcript_file_text.startswith("# Transcript")
    assert "Hello from Showreel." in result.transcript_file_text
    assert (Path(result.output_dir) / "transcript.md").is_file()
    assert not (Path(result.output_dir) / "transcript.txt").exists()
    assert not (Path(result.output_dir) / "transcript.json").exists()


def test_transcription_service_saves_only_selected_json(monkeypatch, tmp_path):
    input_file = tmp_path / "clip.m4a"
    input_file.write_bytes(b"audio")

    def fake_popen(command, **kwargs):
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.transcription_service.subprocess.Popen",
        fake_popen,
    )

    result = TranscriptionService(timeout_seconds=5).transcribe_file(
        TranscriptionRequest(
            input_file_path=str(input_file),
            user_confirmed_rights=True,
            transcript_format="json",
        )
    )

    assert result.status == "succeeded"
    assert result.transcript_txt_path is None
    assert result.transcript_md_path is None
    assert Path(result.transcript_json_path).name == "transcript.json"
    assert result.transcript_format == "json"
    assert json.loads(result.transcript_file_text)["text"] == "Hello from Showreel."
    assert (Path(result.output_dir) / "transcript.json").is_file()


def test_transcription_service_does_not_run_without_confirmation(monkeypatch, tmp_path):
    input_file = tmp_path / "audio.m4a"
    input_file.write_bytes(b"audio")

    def fail_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen must not be called")

    monkeypatch.setattr(
        "universal_media_extractor.services.transcription_service.subprocess.Popen",
        fail_popen,
    )

    result = TranscriptionService().transcribe_file(
        TranscriptionRequest(input_file_path=str(input_file), user_confirmed_rights=False)
    )

    assert result.status == "blocked"
    assert result.errors[0].code == "rights_confirmation_required"


def test_transcription_service_extracts_audio_for_video(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    input_file = media_dir / "clip.mp4"
    input_file.write_bytes(b"video")
    calls = []

    def fake_popen(command, **kwargs):
        calls.append(command)
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.transcription_service.subprocess.Popen",
        fake_popen,
    )

    result = TranscriptionService().transcribe_file(
        TranscriptionRequest(
            input_file_path=str(input_file),
            user_confirmed_rights=True,
            source_kind="video",
        )
    )

    assert result.status == "succeeded"
    assert calls[0][0] == "ffmpeg"
    assert "-vn" in calls[0]
    assert calls[1][0] == "whisper"
    assert result.extracted_audio_path.endswith("extracted_audio.wav")


def test_transcription_service_records_whisper_failure(monkeypatch, tmp_path):
    input_file = tmp_path / "audio.m4a"
    input_file.write_bytes(b"audio")

    def fake_popen(command, **kwargs):
        return FakePopen(command, returncode=1, stderr_text="boom", **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.transcription_service.subprocess.Popen",
        fake_popen,
    )

    result = TranscriptionService().transcribe_file(
        TranscriptionRequest(input_file_path=str(input_file), user_confirmed_rights=True)
    )

    assert result.status == "failed"
    assert result.errors[0].code == "transcription_failed"
    assert "boom" in result.errors[0].technical_details
    assert input_file.exists()
    assert input_file.read_bytes() == b"audio"


def test_transcription_service_updates_step_based_job_status(monkeypatch, tmp_path):
    input_file = tmp_path / "audio.m4a"
    input_file.write_bytes(b"audio")

    monkeypatch.setattr(
        "universal_media_extractor.services.transcription_service.subprocess.Popen",
        lambda command, **kwargs: FakePopen(command, **kwargs),
    )

    job_service = JobService()
    job = job_service.create_job("transcribe", {})
    job_service.update_job_status(job.job_id, "running")

    result = TranscriptionService().transcribe_file(
        TranscriptionRequest(input_file_path=str(input_file), user_confirmed_rights=True),
        job_service=job_service,
        job_id=job.job_id,
    )

    updated = job_service.get_job(job.job_id)
    assert result.status == "succeeded"
    assert updated.current_step == "generating_transcript_files"
    assert updated.stage == "saving"
    assert updated.progress_mode == "indeterminate"
    assert updated.progress_percent == 90


def test_cancelled_transcription_cleans_safe_work_files(tmp_path):
    output_dir = tmp_path / "output"
    work_dir = output_dir / ".work"
    work_dir.mkdir(parents=True)
    extracted_audio = work_dir / "extracted_audio.wav"
    extracted_audio.write_bytes(b"wav")
    keep_file = output_dir / "source.m4a"
    keep_file.write_bytes(b"audio")
    request = TranscriptionRequest(
        input_file_path=str(keep_file),
        user_confirmed_rights=True,
    )

    result = cancelled_transcription_result(
        request,
        output_dir,
        output_dir / ".logs" / "transcription.log",
        output_dir / ".metadata" / "transcription_result.json",
        extracted_audio_path=extracted_audio,
    )

    assert result.status == "cancelled"
    assert not extracted_audio.exists()
    assert not work_dir.exists()
    assert keep_file.exists()
