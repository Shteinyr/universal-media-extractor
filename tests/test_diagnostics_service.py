import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.models import ErrorState, Job
from universal_media_extractor.services.diagnostics_service import DiagnosticsService, redact_text, redact_value


def version_runner(command):
    return {
        "yt-dlp": "2026.03.17",
        "ffmpeg": "ffmpeg version 8.1.1",
        "whisper": "usage: whisper",
    }.get(command[0])


def test_diagnostics_bundle_redacts_sensitive_payload_result_and_logs(tmp_path):
    log_path = tmp_path / "download.log"
    log_path.write_text(
        "Command with https://example.com/private/video?id=secret\n"
        "cookies_path=/Users/aleksandr/secrets/cookies.txt\n"
        "Authorization: Bearer very-secret-token\n"
        "Output /Users/aleksandr/Downloads/video.mp4\n",
        encoding="utf-8",
    )
    error = ErrorState(
        code="extractor_failed",
        message="Raw failure.",
        technical_details="ERROR: This video is DRM protected at https://example.com/private/video",
        recoverable=True,
    )
    job = Job(
        job_id="job-test",
        task_type="download",
        status="failed",
        current_step="failed",
        payload={
            "source_url": "https://example.com/private/video?id=secret",
            "cookies_path": "/Users/aleksandr/secrets/cookies.txt",
        },
        result={
            "status": "failed",
            "source_url": "https://example.com/private/video?id=secret",
            "downloaded_files": ["/Users/aleksandr/Downloads/video.mp4"],
            "log_path": str(log_path),
            "transcript_text": "private transcript",
            "errors": [error.model_dump(mode="json")],
        },
        error=error,
        created_at=datetime.now(timezone.utc),
    )

    bundle = DiagnosticsService(version_runner=version_runner).build_job_bundle(
        job,
        app_version="0.1.0",
    )

    dumped = bundle.model_dump_json()
    assert bundle.app_version == "0.1.0"
    assert bundle.os_name
    assert bundle.python_version
    assert bundle.normalized_error.code == "drm_protected"
    assert bundle.engine_versions["yt-dlp"] == "2026.03.17"
    assert bundle.engine_versions["ffmpeg"] == "ffmpeg version 8.1.1"
    assert bundle.engine_versions["whisper"] == "usage: whisper"
    assert len(bundle.redacted_logs) == 1
    assert bundle.redacted_logs[0].name == "download.log"
    assert "example.com/private" not in dumped
    assert "/Users/aleksandr" not in dumped
    assert "cookies.txt" not in dumped
    assert "very-secret-token" not in dumped
    assert "private transcript" not in dumped
    assert "<redacted-url:example.com>" in dumped
    assert "<redacted-path>" in dumped
    assert "<redacted-secret" in dumped
    assert "sharing_note" in dumped


def test_redact_helpers_remove_full_urls_paths_and_transcripts():
    assert redact_text("Open https://host.test/path?a=1 and /Users/aleksandr/file") == "Open <redacted-url:host.test> and <redacted-path>"
    assert redact_text("token=abc123") == "<redacted-secret-line>"
    assert redact_text("C:\\Users\\alex\\Downloads\\clip.mp4") == "<redacted-path>"
    value = redact_value({
        "source_url": "https://host.test/path?a=1",
        "output_dir": "/Users/aleksandr/Downloads/out",
        "transcript_text": "secret words",
        "authorization": "Bearer token",
        "nested": {
            "webpage_url": "https://example.test/private?id=secret",
            "summary_prompt_text": "private prompt",
        },
    })
    assert value["source_url"] == "<redacted-url:host.test>"
    assert value["output_dir"] == "<redacted-path>"
    assert value["transcript_text"] == "<redacted-transcript>"
    assert value["authorization"] == "<redacted-secret>"
    assert value["nested"]["webpage_url"] == "<redacted-url:example.test>"
    assert value["nested"]["summary_prompt_text"] == "<redacted-transcript>"
