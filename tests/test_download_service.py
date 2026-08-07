import subprocess
import sys
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.models import DownloadRequest
from universal_media_extractor.services.download_service import (
    DownloadService,
    _parse_ytdlp_progress_line,
)


class FakePopen:
    def __init__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        self.stdout = StringIO(kwargs.pop("output", "[download] 100.0% of 1.00MiB\n"))
        self.returncode = kwargs.pop("returncode", 0)
        self.terminated = False
        self.killed = False

    def poll(self):
        if self.stdout.tell() == len(self.stdout.getvalue()):
            return self.returncode
        return None

    def wait(self, timeout=None):
        return self.returncode

    def terminate(self):
        self.terminated = True
        self.returncode = -15

    def kill(self):
        self.killed = True
        self.returncode = -9


def _request(tmp_path, *, user_confirmed_rights=True):
    return DownloadRequest(
        source_url="https://youtu.be/UUdxAp3kuKA",
        format_id="140",
        mode="audio",
        user_confirmed_rights=user_confirmed_rights,
        output_base_dir=str(tmp_path),
        source_title="Showreel",
    )


def test_download_service_builds_safe_ytdlp_command(monkeypatch, tmp_path):
    calls = {}

    def fake_popen(command, **kwargs):
        calls["command"] = command
        calls["kwargs"] = kwargs
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fake_popen,
    )

    result = DownloadService(timeout_seconds=5).download_media(_request(tmp_path))

    assert result.status == "succeeded"
    assert calls["command"][0] == "yt-dlp"
    assert "-f" in calls["command"]
    assert "140" in calls["command"]
    assert "--simulate" not in calls["command"]
    assert "--windows-filenames" in calls["command"]
    assert calls["kwargs"]["shell"] is False
    assert result.output_dir is not None
    assert Path(result.output_dir).name == "Showreel"
    assert (Path(result.output_dir) / ".metadata").is_dir()
    assert (Path(result.output_dir) / ".logs").is_dir()
    assert str(Path(result.output_dir) / "%(title).200B [%(id)s].%(ext)s") in calls["command"]
    assert Path(result.metadata_path).name == "download_result.json"
    assert Path(result.log_path).name == "download.log"


def test_download_service_passes_output_template_and_duplicate_policy(monkeypatch, tmp_path):
    def fake_popen(command, **kwargs):
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fake_popen,
    )

    request = DownloadRequest(
        source_url="https://youtu.be/UUdxAp3kuKA",
        format_id="140",
        mode="audio",
        user_confirmed_rights=True,
        output_base_dir=str(tmp_path),
        source_title="Showreel",
        output_template="{source} - {channel} - {date} - {playlist_index} - {title}",
        duplicate_policy="rename",
        channel_name="Demo Channel",
        playlist_index=3,
    )

    result = DownloadService().download_media(request)

    assert result.status == "succeeded"
    assert result.output_dir is not None
    assert "youtu.be" in Path(result.output_dir).name
    assert "Demo Channel" in Path(result.output_dir).name
    assert "003" in Path(result.output_dir).name
    assert "Showreel" in Path(result.output_dir).name


def test_download_service_duplicate_policy_skip_does_not_run_ytdlp(monkeypatch, tmp_path):
    (tmp_path / "Showreel").mkdir()

    def fail_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen must not be called")

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fail_popen,
    )

    request = _request(tmp_path)
    request.duplicate_policy = "skip"
    result = DownloadService().download_media(request)

    assert result.status == "skipped"
    assert result.output_dir == str((tmp_path / "Showreel").resolve())
    assert result.downloaded_files == []


def test_download_service_expands_user_output_folder(monkeypatch, tmp_path):
    calls = {}
    home_dir = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home_dir))

    def fake_popen(command, **kwargs):
        calls["command"] = command
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fake_popen,
    )

    request = DownloadRequest(
        source_url="https://youtu.be/UUdxAp3kuKA",
        format_id="140",
        mode="audio",
        user_confirmed_rights=True,
        output_base_dir="~/Downloads/Universal Media Extractor",
        source_title="Showreel",
    )

    result = DownloadService().download_media(request)

    assert result.status == "succeeded"
    assert Path(result.output_dir).is_relative_to(home_dir.resolve())
    assert str(home_dir.resolve()) in " ".join(calls["command"])


def test_download_service_returns_clear_error_for_unwritable_output_base(monkeypatch, tmp_path):
    not_a_folder = tmp_path / "not-a-folder"
    not_a_folder.write_text("file", encoding="utf-8")

    def fail_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen must not be called")

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fail_popen,
    )

    request = _request(tmp_path)
    request.output_base_dir = str(not_a_folder)
    result = DownloadService().download_media(request)

    assert result.status == "failed"
    assert result.errors[0].code == "permission_denied"
    assert "not a folder" in result.errors[0].message


def test_download_service_does_not_run_without_confirmation(monkeypatch, tmp_path):
    def fail_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen must not be called")

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fail_popen,
    )

    result = DownloadService().download_media(
        _request(tmp_path, user_confirmed_rights=False)
    )

    assert result.status == "blocked"
    assert result.errors
    assert result.output_dir is None


def test_download_service_records_ytdlp_error(monkeypatch, tmp_path):
    def fake_popen(command, **kwargs):
        return FakePopen(command, output="format missing", returncode=1, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fake_popen,
    )

    result = DownloadService().download_media(_request(tmp_path))

    assert result.status == "failed"
    assert result.errors[0].code == "extractor_failed"
    assert "format missing" in result.errors[0].technical_details


def test_download_service_video_mode_downloads_video_with_audio(monkeypatch, tmp_path):
    calls = {}

    def fake_popen(command, **kwargs):
        calls["command"] = command
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fake_popen,
    )

    request = DownloadRequest(
        source_url="https://youtu.be/UUdxAp3kuKA",
        format_id="137",
        mode="video",
        user_confirmed_rights=True,
        output_base_dir=str(tmp_path),
        source_title="Showreel",
    )
    result = DownloadService().download_media(request)

    assert result.status == "succeeded"
    assert "-f" in calls["command"]
    assert "137+bestaudio/best" in calls["command"]
    assert "137" in result.selected_format_id


def test_download_service_combined_mode_can_remux_container(monkeypatch, tmp_path):
    calls = {}

    def fake_popen(command, **kwargs):
        calls["command"] = command
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fake_popen,
    )

    request = DownloadRequest(
        source_url="https://youtu.be/UUdxAp3kuKA",
        format_id="95",
        mode="combined",
        user_confirmed_rights=True,
        output_base_dir=str(tmp_path),
        source_title="Showreel",
        output_format="mkv",
    )
    result = DownloadService().download_media(request)

    assert result.status == "succeeded"
    assert "95" in calls["command"]
    assert "--merge-output-format" in calls["command"]
    assert "mkv" in calls["command"]
    assert "--remux-video" in calls["command"]


def test_download_service_subtitle_mode_uses_skip_download(monkeypatch, tmp_path):
    calls = {}

    def fake_popen(command, **kwargs):
        calls["command"] = command
        return FakePopen(command, output="subs", **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.download_service.subprocess.Popen",
        fake_popen,
    )

    request = DownloadRequest(
        source_url="https://youtu.be/UUdxAp3kuKA",
        format_id="en",
        mode="subtitles",
        user_confirmed_rights=True,
        output_base_dir=str(tmp_path),
    )
    result = DownloadService().download_media(request)

    assert result.status == "succeeded"
    assert "--skip-download" in calls["command"]
    assert "--write-subs" in calls["command"]
    assert "--sub-langs" in calls["command"]


def test_ytdlp_progress_parser_reads_percent_and_postprocessing():
    assert _parse_ytdlp_progress_line("[download]  42.7% of 3.00MiB at 1.00MiB/s") == (
        "downloading",
        42.7,
    )
    assert _parse_ytdlp_progress_line("[Merger] Merging formats into file.mp4") == (
        "merging_or_postprocessing",
        None,
    )
    assert _parse_ytdlp_progress_line("plain text") == (None, None)
