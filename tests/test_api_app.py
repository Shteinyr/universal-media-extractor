import sys
from datetime import datetime, timezone
from pathlib import Path
import time

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.api.app import create_app
from universal_media_extractor.models import (
    AccessState,
    AnalyzeResult,
    DownloadResult,
    ErrorState,
    LegalSafetyState,
    LocalFileAnalyzeResult,
    TranscriptionResult,
    UdemyCourseAnalyzeResult,
    UdemyCourseDownloadResult,
)


def _analyze_result(url: str, *, errors=None) -> AnalyzeResult:
    return AnalyzeResult(
        analysis_id="test-analysis",
        source_url=url,
        source_type="url",
        extractor="mock",
        access_state=AccessState(availability="public"),
        errors=errors or [],
        legal_safety=LegalSafetyState(
            confirmation_text="I confirm rights.",
            user_confirmed_rights=False,
        ),
        raw_reference_path="proof/api/mock.json",
        analyzed_at=datetime.now(timezone.utc),
    )


def _wait_for_terminal_job(client: TestClient, job_id: str, *, timeout: float = 2.0) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        response = client.get(f"/jobs/{job_id}")
        assert response.status_code == 200
        body = response.json()
        if body["status"] in {"succeeded", "failed", "cancelled"}:
            return body
        time.sleep(0.01)
    raise AssertionError(f"Job {job_id} did not finish before timeout.")


def test_health_endpoint_returns_local_only_status(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "universal-media-extractor",
        "mode": "local-only",
    }


def test_static_index_is_available(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path))

    response = client.get("/")

    assert response.status_code == 200
    assert "Universal Media Extractor" in response.text
    assert "Ready to analyze" in response.text
    assert "MVP flow" in response.text
    assert "Whisper model" in response.text
    assert "Copy transcript" in response.text
    assert "Save to" in response.text
    assert "~/Downloads/Universal Media Extractor" in response.text
    assert "Local file mode" in response.text
    assert "Analyze local file" in response.text
    assert "Course mode" in response.text
    assert "Analyze course" in response.text
    assert "Udemy course export" in response.text
    assert "Chrome session" in response.text
    assert "Manual cookies.txt" in response.text
    assert "Recent results" in response.text
    assert 'src="/static/option_normalizer.js"' in response.text
    assert 'src="/static/app.js"' in response.text


def test_static_javascript_is_available(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path))

    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "POST" in response.text
    assert "/analyze" in response.text
    assert "/download" in response.text
    assert "/transcribe" in response.text
    assert "/local/analyze" in response.text
    assert "/local/transcribe" in response.text
    assert "/udemy/analyze" in response.text
    assert "/udemy/download" in response.text
    assert "/outputs" in response.text
    assert "/jobs/" in response.text
    assert "cancelDownloadButton" in response.text
    assert "cancelTranscribeButton" in response.text
    assert "progress_percent" in response.text
    assert "Progress:" in response.text
    assert "toggleCancelButton" in response.text
    assert "copySummaryButton" in response.text
    assert "selectedFormatSummary" in response.text
    assert "whisperModel.value" in response.text
    assert "URL required" in response.text
    assert "File required" in response.text
    assert "API unavailable" in response.text
    assert "canTranscribeSelectedFormat" in response.text
    assert "Downloads with audio" in response.text
    assert "DEFAULT_DOWNLOAD_OUTPUT_DIR" in response.text
    assert "output_base_dir" in response.text
    assert "source_title" in response.text
    assert "downloadOutputFormatSelect" in response.text
    assert "MP4" in response.text
    assert "courseAuthSourceSelect" in response.text
    assert "cookies_path" in response.text


def test_static_option_normalizer_is_available(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path))

    response = client.get("/static/option_normalizer.js")

    assert response.status_code == 200
    assert "buildFormatPickerData" in response.text
    assert "dedupeSubtitleOptions" in response.text
    assert "MIN_VIDEO_QUALITY" in response.text


def test_analyze_endpoint_uses_service_and_returns_result(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    calls = {}

    class FakeAnalyzeService:
        def analyze_url(self, url, raw_output_dir=None):
            calls["url"] = url
            calls["raw_output_dir"] = raw_output_dir
            return _analyze_result(url)

    app.state.analyze_service = FakeAnalyzeService()
    client = TestClient(app)

    response = client.post(
        "/analyze",
        json={"source_type": "url", "url": "https://example.test/video"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["job"]["task_type"] == "analyze_url"
    assert body["job"]["status"] == "succeeded"
    assert body["result"]["source_url"] == "https://example.test/video"
    assert calls["url"] == "https://example.test/video"
    assert calls["raw_output_dir"].parent == tmp_path.resolve()


def test_analyze_endpoint_rejects_empty_url_without_calling_service(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    calls = {"count": 0}

    class FakeAnalyzeService:
        def analyze_url(self, url, raw_output_dir=None):
            calls["count"] += 1
            return _analyze_result(url)

    app.state.analyze_service = FakeAnalyzeService()
    client = TestClient(app)

    response = client.post("/analyze", json={"source_type": "url", "url": ""})

    assert response.status_code == 422
    assert calls["count"] == 0


def test_analyze_endpoint_rejects_invalid_url_without_calling_service(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    calls = {"count": 0}

    class FakeAnalyzeService:
        def analyze_url(self, url, raw_output_dir=None):
            calls["count"] += 1
            return _analyze_result(url)

    app.state.analyze_service = FakeAnalyzeService()
    client = TestClient(app)

    response = client.post("/analyze", json={"source_type": "url", "url": "not-a-url"})

    assert response.status_code == 422
    assert "Enter a valid http or https URL" in response.text
    assert calls["count"] == 0


def test_analyze_endpoint_marks_login_required_error_as_failed_job(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    error = ErrorState(
        code="login_required",
        message="Login required.",
        recoverable=True,
        suggested_user_action="Use a public URL.",
    )

    class FakeAnalyzeService:
        def analyze_url(self, url, raw_output_dir=None):
            return _analyze_result(url, errors=[error])

    app.state.analyze_service = FakeAnalyzeService()
    client = TestClient(app)

    response = client.post(
        "/analyze",
        json={"source_type": "url", "url": "https://example.test/private"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["job"]["status"] == "failed"
    assert body["job"]["error"]["code"] == "login_required"
    assert body["result"]["errors"][0]["suggested_user_action"] == "Use a public URL."


def test_analyze_endpoint_keeps_analyzer_errors_in_result_and_job(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    error = ErrorState(
        code="unsupported_source",
        message="Unsupported.",
        recoverable=False,
    )

    class FakeAnalyzeService:
        def analyze_url(self, url, raw_output_dir=None):
            return _analyze_result(url, errors=[error])

    app.state.analyze_service = FakeAnalyzeService()
    client = TestClient(app)

    response = client.post(
        "/analyze",
        json={"source_type": "url", "url": "https://example.test/private"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["job"]["status"] == "failed"
    assert body["job"]["error"]["code"] == "unsupported_source"
    assert body["result"]["errors"][0]["code"] == "unsupported_source"


def test_get_job_endpoint_returns_created_job(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)

    class FakeAnalyzeService:
        def analyze_url(self, url, raw_output_dir=None):
            return _analyze_result(url)

    app.state.analyze_service = FakeAnalyzeService()
    client = TestClient(app)
    analyze_response = client.post(
        "/analyze",
        json={"source_type": "url", "url": "https://example.test/video"},
    )
    job_id = analyze_response.json()["job"]["job_id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json()["job_id"] == job_id


def test_get_job_endpoint_returns_404_for_missing_job(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path))

    response = client.get("/jobs/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found."}


def test_download_endpoint_requires_rights_confirmation(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path))

    response = client.post(
        "/download",
        json={
            "source_url": "https://youtu.be/UUdxAp3kuKA",
            "format_id": "140",
            "mode": "audio",
            "user_confirmed_rights": False,
        },
    )

    assert response.status_code == 200
    body = _wait_for_terminal_job(client, response.json()["job_id"])
    assert body["task_type"] == "download"
    assert body["status"] == "failed"
    assert body["error"]["message"] == "Rights confirmation is required before download."
    assert body["result"]["status"] == "blocked"


def test_download_endpoint_uses_service_and_returns_result(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    calls = {}
    custom_output_base = tmp_path / "downloads"

    class FakeDownloadService:
        def download_media(self, request, **kwargs):
            calls["request"] = request
            calls["kwargs"] = kwargs
            return DownloadResult(
                status="succeeded",
                source_url=request.source_url,
                selected_format_id=request.format_id,
                output_dir=str(tmp_path / "output"),
                downloaded_files=[str(tmp_path / "output" / "audio.m4a")],
                metadata_path=str(tmp_path / "output" / ".metadata" / "download_result.json"),
                log_path=str(tmp_path / "output" / ".logs" / "download.log"),
            )

    app.state.download_service = FakeDownloadService()
    client = TestClient(app)

    response = client.post(
        "/download",
        json={
            "source_url": "https://youtu.be/UUdxAp3kuKA",
            "format_id": "140",
            "mode": "audio",
            "user_confirmed_rights": True,
            "output_base_dir": str(custom_output_base),
            "source_title": "Showreel",
        },
    )

    assert response.status_code == 200
    started = response.json()
    assert started["task_type"] == "download"
    body = _wait_for_terminal_job(client, started["job_id"])
    assert body["status"] == "succeeded"
    assert body["result"]["selected_format_id"] == "140"
    assert calls["request"].user_confirmed_rights is True
    assert calls["request"].output_base_dir == str(custom_output_base)
    assert calls["request"].source_title == "Showreel"
    assert app.state.output_base_dir == custom_output_base.resolve()
    assert "job_service" in calls["kwargs"]
    assert calls["kwargs"]["job_id"] == started["job_id"]


def test_transcribe_endpoint_uses_service_and_returns_result(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    calls = {}

    class FakeTranscriptionService:
        def transcribe_file(self, request, **kwargs):
            calls["request"] = request
            calls["kwargs"] = kwargs
            return TranscriptionResult(
                status="succeeded",
                input_file_path=request.input_file_path,
                output_dir=str(tmp_path / "output"),
                transcript_txt_path=str(tmp_path / "output" / "transcripts" / "transcript.txt"),
                transcript_md_path=str(tmp_path / "output" / "transcripts" / "transcript.md"),
                transcript_json_path=str(tmp_path / "output" / "transcripts" / "transcript.json"),
                summary_prompt_path=str(tmp_path / "output" / "transcripts" / "summary_prompt.md"),
                transcript_text="hello",
                summary_prompt_text="# Summary Prompt\n\nhello",
                log_path=str(tmp_path / "output" / "logs" / "transcription.log"),
            )

    app.state.transcription_service = FakeTranscriptionService()
    client = TestClient(app)

    response = client.post(
        "/transcribe",
        json={
            "input_file_path": str(tmp_path / "audio.m4a"),
            "user_confirmed_rights": True,
            "model": "tiny",
        },
    )

    assert response.status_code == 200
    started = response.json()
    assert started["task_type"] == "transcribe"
    body = _wait_for_terminal_job(client, started["job_id"])
    assert body["status"] == "succeeded"
    assert body["result"]["summary_prompt_path"].endswith("summary_prompt.md")
    assert body["result"]["transcript_text"] == "hello"
    assert calls["request"].user_confirmed_rights is True
    assert calls["kwargs"]["job_id"] == started["job_id"]


def test_cancel_job_endpoint_marks_queued_job_cancelled(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    job = app.state.job_service.create_job("download", {"format_id": "140"})
    client = TestClient(app)

    response = client.post(f"/jobs/{job.job_id}/cancel")

    assert response.status_code == 200
    body = response.json()
    assert body["job_id"] == job.job_id
    assert body["status"] == "cancelled"
    assert body["cancel_requested"] is True


def test_cancel_job_endpoint_returns_404_for_missing_job(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path))

    response = client.post("/jobs/missing/cancel")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found."}


def test_local_analyze_endpoint_saves_upload_and_returns_metadata(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path, output_base_dir=tmp_path)
    calls = {}

    class FakeLocalFileMetadataService:
        def analyze_file(self, file_path, *, original_filename=None, output_dir=None):
            calls["file_path"] = file_path
            calls["original_filename"] = original_filename
            calls["output_dir"] = output_dir
            return LocalFileAnalyzeResult(
                filename=original_filename,
                saved_path=str(file_path),
                output_dir=str(output_dir),
                media_type="audio",
                duration_seconds=2.0,
                size_bytes=file_path.stat().st_size,
            )

    app.state.local_file_metadata_service = FakeLocalFileMetadataService()
    client = TestClient(app)

    response = client.post(
        "/local/analyze",
        files={"file": ("sample.wav", b"audio-bytes", "audio/wav")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "sample.wav"
    assert body["media_type"] == "audio"
    assert Path(body["saved_path"]).exists()
    assert calls["original_filename"] == "sample.wav"
    assert calls["output_dir"].name.startswith("local_")


def test_local_analyze_endpoint_rejects_empty_upload(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path, output_base_dir=tmp_path))

    response = client.post(
        "/local/analyze",
        files={"file": ("empty.wav", b"", "audio/wav")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Uploaded file is empty."}


def test_local_transcribe_endpoint_uses_service_and_returns_job(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path, output_base_dir=tmp_path)
    input_file = tmp_path / "audio.wav"
    input_file.write_bytes(b"audio")
    calls = {}

    class FakeTranscriptionService:
        def transcribe_file(self, request, **kwargs):
            calls["request"] = request
            calls["kwargs"] = kwargs
            return TranscriptionResult(
                status="succeeded",
                input_file_path=request.input_file_path,
                output_dir=str(tmp_path / "output"),
                transcript_txt_path=str(tmp_path / "output" / "transcripts" / "transcript.txt"),
                transcript_md_path=str(tmp_path / "output" / "transcripts" / "transcript.md"),
                transcript_json_path=str(tmp_path / "output" / "transcripts" / "transcript.json"),
                summary_prompt_path=str(tmp_path / "output" / "transcripts" / "summary_prompt.md"),
                transcript_text="local hello",
                summary_prompt_text="# Summary Prompt\n\nlocal hello",
                log_path=str(tmp_path / "output" / "logs" / "transcription.log"),
            )

    app.state.transcription_service = FakeTranscriptionService()
    client = TestClient(app)

    response = client.post(
        "/local/transcribe",
        json={
            "saved_file_path": str(input_file),
            "output_dir": str(tmp_path / "output"),
            "user_confirmed_rights": True,
            "model": "tiny",
            "source_kind": "audio",
        },
    )

    assert response.status_code == 200
    started = response.json()
    assert started["task_type"] == "transcribe"
    body = _wait_for_terminal_job(client, started["job_id"])
    assert body["status"] == "succeeded"
    assert body["result"]["transcript_text"] == "local hello"
    assert calls["request"].input_file_path == str(input_file.resolve())
    assert calls["request"].user_confirmed_rights is True
    assert calls["kwargs"]["job_id"] == started["job_id"]


def test_local_transcribe_endpoint_rejects_missing_file(tmp_path):
    client = TestClient(create_app(raw_output_base_dir=tmp_path, output_base_dir=tmp_path))

    response = client.post(
        "/local/transcribe",
        json={
            "saved_file_path": str(tmp_path / "missing.wav"),
            "user_confirmed_rights": True,
            "model": "tiny",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Saved local file was not found."}


def test_local_transcribe_endpoint_rejects_file_outside_output_base(tmp_path):
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    input_file = outside_dir / "audio.wav"
    input_file.write_bytes(b"audio")
    output_base = tmp_path / "outputs"
    output_base.mkdir()
    client = TestClient(
        create_app(raw_output_base_dir=tmp_path, output_base_dir=output_base)
    )

    response = client.post(
        "/local/transcribe",
        json={
            "saved_file_path": str(input_file),
            "user_confirmed_rights": True,
            "model": "tiny",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Saved local file must be inside the configured output folder."
    }


def test_udemy_analyze_endpoint_uses_service(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    calls = {}

    class FakeUdemyCourseService:
        def analyze_course(self, request, *, raw_output_dir=None):
            calls["request"] = request
            calls["raw_output_dir"] = raw_output_dir
            return UdemyCourseAnalyzeResult(
                status="succeeded",
                course_url=request.course_url,
                course_title="Python Course",
                lecture_count=2,
                raw_reference_path=str(raw_output_dir / "udemy_course_raw.json"),
            )

    app.state.udemy_course_service = FakeUdemyCourseService()
    client = TestClient(app)

    response = client.post(
        "/udemy/analyze",
        json={
            "course_url": "https://www.udemy.com/course/python/",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["result"]["course_title"] == "Python Course"
    assert calls["request"].course_url == "https://www.udemy.com/course/python/"
    assert calls["raw_output_dir"].parent == tmp_path.resolve()


def test_udemy_download_endpoint_returns_job_and_result(tmp_path):
    app = create_app(raw_output_base_dir=tmp_path)
    calls = {}

    class FakeUdemyCourseService:
        def download_course(self, request, **kwargs):
            calls["request"] = request
            calls["kwargs"] = kwargs
            return UdemyCourseDownloadResult(
                status="succeeded",
                course_url=request.course_url,
                course_title=request.course_title,
                output_dir=str(tmp_path / "downloads" / "Python Course"),
                downloaded_files=[str(tmp_path / "downloads" / "Python Course" / "001.mp4")],
                metadata_path=str(tmp_path / "downloads" / "Python Course" / ".metadata" / "udemy_download_result.json"),
                log_path=str(tmp_path / "downloads" / "Python Course" / ".logs" / "udemy_download.log"),
            )

    app.state.udemy_course_service = FakeUdemyCourseService()
    client = TestClient(app)

    response = client.post(
        "/udemy/download",
        json={
            "course_url": "https://www.udemy.com/course/python/",
            "user_confirmed_rights": True,
            "course_title": "Python Course",
            "quality": "720",
            "output_format": "mp4",
        },
    )

    assert response.status_code == 200
    started = response.json()
    assert started["task_type"] == "udemy_download"
    body = _wait_for_terminal_job(client, started["job_id"])
    assert body["status"] == "succeeded"
    assert body["result"]["course_title"] == "Python Course"
    assert body["result"]["downloaded_files"][0].endswith("001.mp4")
    assert calls["request"].quality == "720"
    assert calls["kwargs"]["job_id"] == started["job_id"]


def test_outputs_endpoint_lists_outputs(tmp_path):
    output_base = tmp_path / "outputs"
    output_dir = output_base / "local_20260530T134814Z_sample"
    (output_dir / "source").mkdir(parents=True)
    (output_dir / "metadata").mkdir()
    (output_dir / "source" / "sample.wav").write_bytes(b"abc")
    (output_dir / "metadata" / "local_file_analysis.json").write_text(
        '{"filename": "sample.wav"}',
        encoding="utf-8",
    )
    client = TestClient(create_app(raw_output_base_dir=tmp_path, output_base_dir=output_base))

    response = client.get("/outputs")

    assert response.status_code == 200
    body = response.json()
    assert body["outputs_base_dir"] == str(output_base.resolve())
    assert body["outputs"][0]["output_id"] == output_dir.name
    assert body["outputs"][0]["title_or_filename"] == "sample.wav"


def test_output_detail_endpoint_returns_summary(tmp_path):
    output_base = tmp_path / "outputs"
    output_dir = output_base / "local_20260530T134814Z_detail"
    (output_dir / "transcripts").mkdir(parents=True)
    (output_dir / "transcripts" / "summary_prompt.md").write_text("prompt", encoding="utf-8")
    client = TestClient(create_app(raw_output_base_dir=tmp_path, output_base_dir=output_base))

    response = client.get(f"/outputs/{output_dir.name}")

    assert response.status_code == 200
    assert response.json()["has_summary_prompt"] is True


def test_delete_output_endpoint_deletes_dummy_output(tmp_path):
    output_base = tmp_path / "outputs"
    output_dir = output_base / "local_20260530T134814Z_dummy"
    output_dir.mkdir(parents=True)
    (output_dir / "file.txt").write_text("dummy", encoding="utf-8")
    client = TestClient(create_app(raw_output_base_dir=tmp_path, output_base_dir=output_base))

    response = client.delete(f"/outputs/{output_dir.name}")

    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
    assert not output_dir.exists()


def test_delete_output_endpoint_refuses_path_traversal(tmp_path):
    output_base = tmp_path / "outputs"
    output_base.mkdir()
    client = TestClient(create_app(raw_output_base_dir=tmp_path, output_base_dir=output_base))

    response = client.delete("/outputs/..%2Fproof")

    assert response.status_code in {400, 404}
