import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.analyzers import analyze_url_with_ytdlp
from universal_media_extractor.models import AnalyzeResult

RAW_PATH = ROOT / "proof" / "phase_2" / "url_analysis_raw.json"


def raw_json_text() -> str:
    return RAW_PATH.read_text()


def completed(stdout: str = "", stderr: str = "", returncode: int = 0):
    return subprocess.CompletedProcess(
        args=["yt-dlp", "--simulate", "--dump-json", "https://example.test/video"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_successful_dump_json_returns_analyze_result() -> None:
    with patch("subprocess.run", return_value=completed(stdout=raw_json_text())):
        result = analyze_url_with_ytdlp("https://example.test/video")

    assert isinstance(result, AnalyzeResult)
    assert result.title == "Showreel"
    assert result.extractor == "youtube"
    assert result.errors == []


def test_raw_json_is_saved_when_output_dir_is_provided(tmp_path: Path) -> None:
    with patch("subprocess.run", return_value=completed(stdout=raw_json_text())):
        result = analyze_url_with_ytdlp(
            "https://example.test/video",
            raw_output_dir=tmp_path,
        )

    assert result.raw_reference_path is not None
    saved_path = Path(result.raw_reference_path)
    assert saved_path.exists()
    assert saved_path.parent == tmp_path
    assert json.loads(saved_path.read_text())["title"] == "Showreel"


def test_timeout_becomes_error_state() -> None:
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("yt-dlp", 1)):
        result = analyze_url_with_ytdlp("https://example.test/video", timeout_seconds=1)

    assert result.errors
    assert result.errors[0].code == "timeout"
    assert result.errors[0].recoverable is True


def test_invalid_json_becomes_error_state() -> None:
    with patch("subprocess.run", return_value=completed(stdout="{not-json")):
        result = analyze_url_with_ytdlp("https://example.test/video")

    assert result.errors
    assert result.errors[0].code == "invalid_output"


def test_non_zero_exit_becomes_error_state() -> None:
    with patch(
        "subprocess.run",
        return_value=completed(stderr="ERROR: Unsupported URL", returncode=1),
    ):
        result = analyze_url_with_ytdlp("https://example.test/video")

    assert result.errors
    assert result.errors[0].code == "unsupported_source"


def test_ytdlp_not_found_becomes_error_state() -> None:
    with patch("subprocess.run", side_effect=FileNotFoundError()):
        result = analyze_url_with_ytdlp("https://example.test/video")

    assert result.errors
    assert result.errors[0].code == "ytdlp_not_found"
    assert result.errors[0].recoverable is True


def test_command_is_analysis_only_and_does_not_use_shell() -> None:
    with patch("subprocess.run", return_value=completed(stdout=raw_json_text())) as run:
        analyze_url_with_ytdlp("https://example.test/video", timeout_seconds=7)

    args, kwargs = run.call_args
    command = args[0]
    assert command == [
        "yt-dlp",
        "--simulate",
        "--dump-json",
        "https://example.test/video",
    ]
    assert "--format" not in command
    assert "-f" not in command
    assert "--no-simulate" not in command
    assert kwargs["shell"] is False
    assert kwargs["timeout"] == 7
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True
