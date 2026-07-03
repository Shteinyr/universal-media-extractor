import json
import sys
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.models import (
    UdemyCourseAnalyzeRequest,
    UdemyCourseDownloadRequest,
)
from universal_media_extractor.services.udemy_course_service import UdemyCourseService


class FakePopen:
    def __init__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        self.stdout = StringIO("[download] 100.0% of 1.00MiB\n")
        self.returncode = 0
        output_dir = Path(command[command.index("-P") + 1])
        lecture_dir = output_dir / "01 - Intro"
        lecture_dir.mkdir(parents=True, exist_ok=True)
        (lecture_dir / "001 - Welcome.mp4").write_bytes(b"video")

    def poll(self):
        if self.stdout.tell() == len(self.stdout.getvalue()):
            return self.returncode
        return None

    def wait(self, timeout=None):
        return self.returncode

    def terminate(self):
        self.returncode = -15

    def kill(self):
        self.returncode = -9


def _cookies(tmp_path: Path) -> Path:
    path = tmp_path / "cookies.txt"
    path.write_text("# Netscape HTTP Cookie File\n", encoding="utf-8")
    return path


def test_udemy_analyze_defaults_to_chrome_session(monkeypatch, tmp_path):
    calls = {}
    raw = {
        "title": "Python Course",
        "extractor": "udemy:course",
        "entries": [
            {
                "id": "101",
                "title": "Welcome",
                "chapter": "Intro",
                "chapter_number": 1,
                "duration": 60,
                "webpage_url": "https://www.udemy.com/course/python/learn/lecture/101",
            },
            {
                "id": "102",
                "title": "Setup",
                "chapter": "Intro",
                "chapter_number": 1,
            },
        ],
    }

    def fake_run(command, **kwargs):
        calls["command"] = command
        calls["kwargs"] = kwargs

        class Completed:
            returncode = 0
            stdout = json.dumps(raw)
            stderr = ""

        return Completed()

    monkeypatch.setattr(
        "universal_media_extractor.services.udemy_course_service.subprocess.run",
        fake_run,
    )

    result = UdemyCourseService().analyze_course(
        UdemyCourseAnalyzeRequest(
            course_url="https://www.udemy.com/course/python/",
        ),
        raw_output_dir=tmp_path / "raw",
    )

    assert result.status == "succeeded"
    assert result.course_title == "Python Course"
    assert result.lecture_count == 2
    assert result.sections[0].title == "Intro"
    assert calls["command"][0] == "yt-dlp"
    assert "--dump-single-json" in calls["command"]
    assert "--flat-playlist" in calls["command"]
    assert "--cookies-from-browser" in calls["command"]
    assert "chrome" in calls["command"]
    assert calls["kwargs"]["shell"] is False
    assert Path(result.raw_reference_path).is_file()


def test_udemy_analyze_manual_mode_requires_readable_cookies(monkeypatch, tmp_path):
    def fail_run(*args, **kwargs):
        raise AssertionError("subprocess.run must not be called")

    monkeypatch.setattr(
        "universal_media_extractor.services.udemy_course_service.subprocess.run",
        fail_run,
    )

    result = UdemyCourseService().analyze_course(
        UdemyCourseAnalyzeRequest(
            course_url="https://www.udemy.com/course/python/",
            auth_source="manual_cookies",
            cookies_path=str(tmp_path / "missing.txt"),
        )
    )

    assert result.status == "failed"
    assert result.errors[0].code == "cookies_required"


def test_udemy_analyze_failure_saves_redacted_diagnostics(monkeypatch, tmp_path):
    def fake_run(command, **kwargs):
        class Completed:
            returncode = 1
            stdout = ""
            stderr = "ERROR: Unable to download webpage: HTTP Error 403: Forbidden"

        return Completed()

    monkeypatch.setattr(
        "universal_media_extractor.services.udemy_course_service.subprocess.run",
        fake_run,
    )

    result = UdemyCourseService().analyze_course(
        UdemyCourseAnalyzeRequest(
            course_url="https://www.udemy.com/course/python/",
        ),
        raw_output_dir=tmp_path / "raw",
    )

    assert result.status == "failed"
    assert result.errors[0].code == "cookies_required"
    artifact = Path(result.raw_reference_path)
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    assert payload["returncode"] == 1
    assert "HTTP Error 403" in payload["stderr"]
    assert "[chrome-session]" in payload["command"]
    assert "chrome" not in payload["command"]


def test_udemy_analyze_derives_course_title_from_lecture_url(monkeypatch, tmp_path):
    raw = {
        "extractor": "udemy:course",
        "entries": [
            {
                "title": "Welcome",
                "chapter": "Intro",
                "chapter_number": 1,
                "url": "https://www.udemy.com/course/learn/v4/t/lecture/101",
            }
        ],
    }

    def fake_run(command, **kwargs):
        class Completed:
            returncode = 0
            stdout = json.dumps(raw)
            stderr = ""

        return Completed()

    monkeypatch.setattr(
        "universal_media_extractor.services.udemy_course_service.subprocess.run",
        fake_run,
    )

    result = UdemyCourseService().analyze_course(
        UdemyCourseAnalyzeRequest(
            course_url="https://www.udemy.com/course/final-cut-pro-x-10/learn/lecture/24161484",
        ),
        raw_output_dir=tmp_path / "raw",
    )

    assert result.status == "succeeded"
    assert result.course_title == "Final Cut Pro X 10"
    assert result.lecture_count == 1


def test_udemy_manual_model_requires_cookies_path():
    try:
        UdemyCourseAnalyzeRequest(
            course_url="https://www.udemy.com/course/python/",
            auth_source="manual_cookies",
        )
    except ValueError as exc:
        assert "Manual cookies mode requires" in str(exc)
    else:
        raise AssertionError("manual cookies mode must require cookies_path")


def test_udemy_download_defaults_to_chrome_session_and_redacts_log(monkeypatch, tmp_path):
    calls = {}

    def fake_popen(command, **kwargs):
        calls["command"] = command
        calls["kwargs"] = kwargs
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.udemy_course_service.subprocess.Popen",
        fake_popen,
    )

    result = UdemyCourseService(timeout_seconds=5).download_course(
        UdemyCourseDownloadRequest(
            course_url="https://www.udemy.com/course/python/",
            user_confirmed_rights=True,
            output_base_dir=str(tmp_path / "downloads"),
            course_title="Python Course",
            quality="720",
            output_format="mp4",
            include_subtitles=True,
            lecture_limit=1,
        )
    )

    assert result.status == "succeeded"
    assert calls["command"][0] == "yt-dlp"
    assert calls["kwargs"]["shell"] is False
    assert "--cookies-from-browser" in calls["command"]
    assert "chrome" in calls["command"]
    assert "--playlist-end" in calls["command"]
    assert "1" in calls["command"]
    assert "bestvideo[height<=720]+bestaudio/best[height<=720]/best" in calls["command"]
    assert result.downloaded_files
    log_text = Path(result.log_path).read_text(encoding="utf-8")
    assert "[chrome-session]" in log_text


def test_udemy_download_manual_mode_uses_cookies_file(monkeypatch, tmp_path):
    cookies = _cookies(tmp_path)
    calls = {}

    def fake_popen(command, **kwargs):
        calls["command"] = command
        return FakePopen(command, **kwargs)

    monkeypatch.setattr(
        "universal_media_extractor.services.udemy_course_service.subprocess.Popen",
        fake_popen,
    )

    result = UdemyCourseService(timeout_seconds=5).download_course(
        UdemyCourseDownloadRequest(
            course_url="https://www.udemy.com/course/python/",
            auth_source="manual_cookies",
            cookies_path=str(cookies),
            user_confirmed_rights=True,
            output_base_dir=str(tmp_path / "downloads"),
        )
    )

    assert result.status == "succeeded"
    assert "--cookies" in calls["command"]
    assert str(cookies.resolve()) in calls["command"]
    log_text = Path(result.log_path).read_text(encoding="utf-8")
    assert str(cookies.resolve()) not in log_text
    assert "[redacted-cookies]" in log_text


def test_udemy_download_does_not_run_without_rights_confirmation(monkeypatch, tmp_path):
    def fail_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen must not be called")

    monkeypatch.setattr(
        "universal_media_extractor.services.udemy_course_service.subprocess.Popen",
        fail_popen,
    )

    result = UdemyCourseService().download_course(
        UdemyCourseDownloadRequest(
            course_url="https://www.udemy.com/course/python/",
            user_confirmed_rights=False,
        )
    )

    assert result.status == "blocked"
    assert result.errors[0].code == "rights_confirmation_required"
