"""Local FastAPI app.

This API exposes local URL analysis and user-confirmed selected-format
downloads/transcription. It does not manage cookies, provide auth/database
features, or run as an online service.
"""

from __future__ import annotations

import os
import secrets
from pathlib import Path
from threading import Thread
from typing import Any, Callable

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from universal_media_extractor.api.schemas import (
    AnalyzeRequest,
    AppConfigResponse,
    AnalyzeResponse,
    DownloadRequest,
    HealthResponse,
    LocalFileTranscriptionRequest,
    TranscriptionRequest,
    UdemyCourseAnalyzeRequest,
    UdemyCourseAnalyzeResponse,
    UdemyCourseDownloadRequest,
)
from universal_media_extractor.models import (
    DiagnosticBundle,
    ErrorState,
    Job,
    JobHistoryClearResult,
    JobHistoryResult,
    JobStatus,
    LocalFileAnalyzeResult,
    OutputDeleteResult,
    OutputListResult,
    OutputSummary,
    UdemyCourseAnalyzeResult,
)
from universal_media_extractor.services import (
    AnalyzeService,
    DiagnosticsService,
    DownloadService,
    JobService,
    LocalFileMetadataService,
    OutputManager,
    TranscriptionService,
    UdemyCourseService,
)

DEFAULT_RAW_OUTPUT_BASE_DIR = Path("proof/api")
DEFAULT_OUTPUT_BASE_DIR = Path.home() / "Downloads" / "Universal Media Extractor"
DEFAULT_JOB_DB_PATH = Path("data/jobs.sqlite3")
DEFAULT_MAX_UPLOAD_BYTES = 2 * 1024 * 1024 * 1024
SECURITY_HEADER_NAME = "x-ume-session-token"
LOCAL_ORIGIN_REGEX = r"^https?://(127\.0\.0\.1|localhost|\[::1\])(:\d+)?$"
STATIC_DIR = Path(__file__).resolve().parents[1] / "static"

def create_app(
    raw_output_base_dir: Path | None = None,
    output_base_dir: Path | None = None,
    *,
    session_token: str | None = None,
    max_upload_bytes: int | None = None,
    job_db_path: Path | None = None,
) -> FastAPI:
    """Create the analysis-only FastAPI app."""

    app = FastAPI(
        title="Universal Media Extractor",
        description="Local-only analysis API for Universal Media Extractor.",
        version="0.1.0",
    )
    app.state.analyze_service = AnalyzeService()
    app.state.download_service = DownloadService()
    app.state.diagnostics_service = DiagnosticsService()
    app.state.transcription_service = TranscriptionService()
    app.state.udemy_course_service = UdemyCourseService()
    app.state.local_file_metadata_service = LocalFileMetadataService()
    app.state.output_manager = OutputManager()
    app.state.raw_output_base_dir = raw_output_base_dir or DEFAULT_RAW_OUTPUT_BASE_DIR
    app.state.output_base_dir = output_base_dir or DEFAULT_OUTPUT_BASE_DIR
    app.state.job_db_path = _resolve_job_db_path(
        job_db_path=job_db_path,
        raw_output_base_dir=raw_output_base_dir,
        output_base_dir=output_base_dir,
    )
    app.state.job_service = JobService(app.state.job_db_path)
    app.state.session_token = session_token or secrets.token_urlsafe(32)
    app.state.max_upload_bytes = max_upload_bytes or DEFAULT_MAX_UPLOAD_BYTES

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=LOCAL_ORIGIN_REGEX,
        allow_credentials=False,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["content-type", SECURITY_HEADER_NAME],
    )

    @app.middleware("http")
    async def enforce_local_security(request: Request, call_next):
        if not _is_allowed_host(request.headers.get("host", "")):
            return JSONResponse(
                status_code=403,
                content={"detail": "Only localhost requests are allowed."},
            )
        if not _is_allowed_origin(request.headers.get("origin")):
            return JSONResponse(
                status_code=403,
                content={"detail": "Origin is not allowed."},
            )
        if _requires_session_token(request):
            provided_token = request.headers.get(SECURITY_HEADER_NAME, "")
            if not secrets.compare_digest(provided_token, app.state.session_token):
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Local session token is required."},
                )
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", response_class=FileResponse)
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/config", response_model=AppConfigResponse)
    def config() -> AppConfigResponse:
        public_mode = _read_bool_env("UME_PUBLIC_PRODUCT_MODE", default=False)
        course_default = not public_mode
        return AppConfigResponse(
            public_product_mode=public_mode,
            course_mode_enabled=_read_bool_env("UME_ENABLE_COURSE_MODE", default=course_default),
            session_token=app.state.session_token,
        )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse()

    @app.post("/analyze", response_model=AnalyzeResponse)
    def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
        job_service: JobService = app.state.job_service
        output_manager: OutputManager = app.state.output_manager
        analyze_service: AnalyzeService = app.state.analyze_service

        job = job_service.create_job(
            "analyze_url",
            {
                "source_type": request.source_type,
                "url": request.url,
                "user_confirmed_rights": request.user_confirmed_rights,
            },
        )
        job_service.update_job_status(job.job_id, "running")

        raw_output_dir = output_manager.create_analysis_output_dir(
            Path(app.state.raw_output_base_dir),
            source_id=request.url,
        )
        result = analyze_service.analyze_url(
            request.url,
            raw_output_dir=raw_output_dir,
        )

        final_status = "failed" if result.errors else "succeeded"
        final_error = result.errors[0] if result.errors else None
        job = job_service.update_job_status(
            job.job_id,
            final_status,
            error=final_error,
        )
        return AnalyzeResponse(job=job, result=result)

    @app.post("/download", response_model=Job)
    def download(request: DownloadRequest) -> Job:
        job_service: JobService = app.state.job_service
        download_service: DownloadService = app.state.download_service
        if request.output_base_dir:
            app.state.output_base_dir = Path(request.output_base_dir).expanduser().resolve()
        job = job_service.create_job("download", request.model_dump())
        _start_background_job(
            job_service,
            job.job_id,
            initial_step="preparing_download",
            operation=lambda: download_service.download_media(
                request,
                job_service=job_service,
                job_id=job.job_id,
            ),
        )
        return job_service.get_job(job.job_id) or job

    @app.post("/udemy/analyze", response_model=UdemyCourseAnalyzeResponse)
    def udemy_analyze(request: UdemyCourseAnalyzeRequest) -> UdemyCourseAnalyzeResponse:
        output_manager: OutputManager = app.state.output_manager
        udemy_course_service: UdemyCourseService = app.state.udemy_course_service
        raw_output_dir = output_manager.create_analysis_output_dir(
            Path(app.state.raw_output_base_dir),
            source_id=request.course_url,
        )
        result: UdemyCourseAnalyzeResult = udemy_course_service.analyze_course(
            request,
            raw_output_dir=raw_output_dir,
        )
        return UdemyCourseAnalyzeResponse(result=result)

    @app.post("/udemy/download", response_model=Job)
    def udemy_download(request: UdemyCourseDownloadRequest) -> Job:
        job_service: JobService = app.state.job_service
        udemy_course_service: UdemyCourseService = app.state.udemy_course_service
        if request.output_base_dir:
            app.state.output_base_dir = Path(request.output_base_dir).expanduser().resolve()
        job = job_service.create_job("udemy_download", request.model_dump())
        _start_background_job(
            job_service,
            job.job_id,
            initial_step="preparing_udemy_download",
            operation=lambda: udemy_course_service.download_course(
                request,
                job_service=job_service,
                job_id=job.job_id,
            ),
        )
        return job_service.get_job(job.job_id) or job

    @app.post("/transcribe", response_model=Job)
    def transcribe(request: TranscriptionRequest) -> Job:
        job_service: JobService = app.state.job_service
        transcription_service: TranscriptionService = app.state.transcription_service
        job = job_service.create_job("transcribe", request.model_dump())
        _start_background_job(
            job_service,
            job.job_id,
            initial_step="preparing_transcription",
            operation=lambda: transcription_service.transcribe_file(
                request,
                job_service=job_service,
                job_id=job.job_id,
            ),
        )
        return job_service.get_job(job.job_id) or job

    @app.post("/local/analyze", response_model=LocalFileAnalyzeResult)
    async def local_analyze(file: UploadFile = File(...)) -> LocalFileAnalyzeResult:
        if not file.filename:
            raise HTTPException(status_code=400, detail="A local file is required.")

        output_manager: OutputManager = app.state.output_manager
        metadata_service: LocalFileMetadataService = app.state.local_file_metadata_service
        output_dir = output_manager.create_local_file_output_dir(
            Path(app.state.output_base_dir),
            filename=file.filename,
        )
        saved_path = output_dir / "source" / _safe_filename(file.filename)
        size = await _save_upload(file, saved_path, max_bytes=app.state.max_upload_bytes)
        if size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        return metadata_service.analyze_file(
            saved_path,
            original_filename=file.filename,
            output_dir=output_dir,
        )

    @app.post("/local/transcribe", response_model=Job)
    def local_transcribe(request: LocalFileTranscriptionRequest) -> Job:
        saved_path = Path(request.saved_file_path).expanduser().resolve()
        if not saved_path.is_file():
            raise HTTPException(status_code=400, detail="Saved local file was not found.")
        output_base = Path(app.state.output_base_dir).expanduser().resolve()
        if not saved_path.is_relative_to(output_base):
            raise HTTPException(
                status_code=400,
                detail="Saved local file must be inside the configured output folder.",
            )

        job_service: JobService = app.state.job_service
        transcription_service: TranscriptionService = app.state.transcription_service
        transcript_request = TranscriptionRequest(
            input_file_path=str(saved_path),
            output_dir=request.output_dir,
            user_confirmed_rights=request.user_confirmed_rights,
            model=request.model,
            language=request.language,
            source_kind=request.source_kind,
            transcript_format=request.transcript_format,
        )
        job = job_service.create_job("transcribe", request.model_dump())
        _start_background_job(
            job_service,
            job.job_id,
            initial_step="preparing_transcription",
            operation=lambda: transcription_service.transcribe_file(
                transcript_request,
                job_service=job_service,
                job_id=job.job_id,
            ),
        )
        return job_service.get_job(job.job_id) or job

    @app.get("/outputs", response_model=OutputListResult)
    def list_outputs() -> OutputListResult:
        output_manager: OutputManager = app.state.output_manager
        return output_manager.list_outputs(Path(app.state.output_base_dir))

    @app.get("/outputs/{output_id}", response_model=OutputSummary)
    def get_output(output_id: str) -> OutputSummary:
        output_manager: OutputManager = app.state.output_manager
        try:
            return output_manager.summarize_output(Path(app.state.output_base_dir), output_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from None
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Output not found.") from None

    @app.delete("/outputs/{output_id}", response_model=OutputDeleteResult)
    def delete_output(output_id: str) -> OutputDeleteResult:
        output_manager: OutputManager = app.state.output_manager
        result = output_manager.delete_output(Path(app.state.output_base_dir), output_id)
        if result.status == "blocked":
            raise HTTPException(status_code=400, detail=result.message)
        if result.status == "not_found":
            raise HTTPException(status_code=404, detail=result.message)
        return result

    @app.get("/jobs", response_model=JobHistoryResult)
    def list_jobs(limit: int = 100, status: JobStatus | None = None) -> JobHistoryResult:
        job_service: JobService = app.state.job_service
        return JobHistoryResult(jobs=job_service.list_jobs(limit=limit, status=status))

    @app.delete("/jobs/history", response_model=JobHistoryClearResult)
    def clear_job_history() -> JobHistoryClearResult:
        job_service: JobService = app.state.job_service
        cleared_count = job_service.clear_history()
        remaining_count = len(job_service.list_jobs(limit=10_000))
        return JobHistoryClearResult(
            cleared_count=cleared_count,
            remaining_count=remaining_count,
            files_deleted=False,
        )

    @app.post("/jobs/{job_id}/retry", response_model=Job)
    def retry_job(job_id: str) -> Job:
        job_service: JobService = app.state.job_service
        try:
            retried = job_service.retry_job(job_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Job not found.") from None
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from None
        _start_retry_job(app, retried)
        return job_service.get_job(retried.job_id) or retried

    @app.get("/jobs/{job_id}", response_model=Job)
    def get_job(job_id: str) -> Job:
        job_service: JobService = app.state.job_service
        job = job_service.get_job(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found.")
        return job

    @app.post("/jobs/{job_id}/cancel", response_model=Job)
    def cancel_job(job_id: str) -> Job:
        job_service: JobService = app.state.job_service
        try:
            return job_service.cancel_job(job_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Job not found.") from None

    @app.get("/diagnostics/jobs/{job_id}", response_model=DiagnosticBundle)
    def job_diagnostics(job_id: str) -> DiagnosticBundle:
        job_service: JobService = app.state.job_service
        diagnostics_service: DiagnosticsService = app.state.diagnostics_service
        job = job_service.get_job(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found.")
        return diagnostics_service.build_job_bundle(job, app_version=app.version)

    return app

def _resolve_job_db_path(
    *,
    job_db_path: Path | None,
    raw_output_base_dir: Path | None,
    output_base_dir: Path | None,
) -> Path:
    if job_db_path is not None:
        return job_db_path
    if raw_output_base_dir is not None:
        return Path(raw_output_base_dir) / "jobs.sqlite3"
    if output_base_dir is not None:
        return Path(output_base_dir) / ".ume" / "jobs.sqlite3"
    return DEFAULT_JOB_DB_PATH

def _requires_session_token(request: Request) -> bool:
    if request.method == "OPTIONS":
        return False
    path = request.url.path
    if path in {"/", "/health", "/config", "/favicon.ico"}:
        return False
    return not path.startswith("/static/")

def _is_allowed_host(host_header: str) -> bool:
    host = host_header.rsplit(":", 1)[0].strip().lower()
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    return host in {"127.0.0.1", "localhost", "::1", "testserver"}

def _is_allowed_origin(origin: str | None) -> bool:
    if not origin:
        return True
    from urllib.parse import urlparse

    parsed = urlparse(origin)
    return parsed.scheme in {"http", "https"} and parsed.hostname in {"127.0.0.1", "localhost", "::1"}

def _read_bool_env(name: str, *, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}

app = create_app()

async def _save_upload(file: UploadFile, destination: Path, *, max_bytes: int) -> int:
    """Save an UploadFile to a local destination with a strict size cap."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    try:
        with destination.open("wb") as handle:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    handle.close()
                    destination.unlink(missing_ok=True)
                    raise HTTPException(status_code=413, detail="Uploaded file is too large.")
                handle.write(chunk)
    finally:
        await file.close()
    return total

def _safe_filename(filename: str) -> str:
    path_name = Path(filename).name
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in path_name)
    return (safe.strip("._") or "local_file")[:160]

def _start_retry_job(app: FastAPI, job: Job) -> None:
    """Restart a failed job using its persisted task type and payload."""

    job_service: JobService = app.state.job_service

    try:
        if job.task_type == "analyze_url":
            request = AnalyzeRequest.model_validate(job.payload)
            output_manager: OutputManager = app.state.output_manager
            analyze_service: AnalyzeService = app.state.analyze_service

            def operation() -> Any:
                raw_output_dir = output_manager.create_analysis_output_dir(
                    Path(app.state.raw_output_base_dir),
                    source_id=request.url,
                )
                return analyze_service.analyze_url(request.url, raw_output_dir=raw_output_dir)

            _start_background_job(
                job_service,
                job.job_id,
                initial_step="preparing_analysis",
                operation=operation,
            )
            return

        if job.task_type == "download":
            request = DownloadRequest.model_validate(job.payload)
            if request.output_base_dir:
                app.state.output_base_dir = Path(request.output_base_dir).expanduser().resolve()
            download_service: DownloadService = app.state.download_service
            _start_background_job(
                job_service,
                job.job_id,
                initial_step="preparing_download",
                operation=lambda: download_service.download_media(
                    request,
                    job_service=job_service,
                    job_id=job.job_id,
                ),
            )
            return

        if job.task_type == "udemy_download":
            request = UdemyCourseDownloadRequest.model_validate(job.payload)
            if request.output_base_dir:
                app.state.output_base_dir = Path(request.output_base_dir).expanduser().resolve()
            udemy_course_service: UdemyCourseService = app.state.udemy_course_service
            _start_background_job(
                job_service,
                job.job_id,
                initial_step="preparing_udemy_download",
                operation=lambda: udemy_course_service.download_course(
                    request,
                    job_service=job_service,
                    job_id=job.job_id,
                ),
            )
            return

        if job.task_type == "transcribe":
            if "input_file_path" in job.payload:
                request = TranscriptionRequest.model_validate(job.payload)
            else:
                local_request = LocalFileTranscriptionRequest.model_validate(job.payload)
                request = TranscriptionRequest(
                    input_file_path=local_request.saved_file_path,
                    output_dir=local_request.output_dir,
                    user_confirmed_rights=local_request.user_confirmed_rights,
                    model=local_request.model,
                    language=local_request.language,
                    source_kind=local_request.source_kind,
                    transcript_format=local_request.transcript_format,
                )
            transcription_service: TranscriptionService = app.state.transcription_service
            _start_background_job(
                job_service,
                job.job_id,
                initial_step="preparing_transcription",
                operation=lambda: transcription_service.transcribe_file(
                    request,
                    job_service=job_service,
                    job_id=job.job_id,
                ),
            )
            return

        job_service.fail_job(
            job.job_id,
            ErrorState(
                code="unknown_error",
                message="This job type cannot be retried yet.",
                recoverable=False,
            ),
        )
    except Exception as exc:
        job_service.fail_job(
            job.job_id,
            ErrorState(
                code="unknown_error",
                message="Retry job could not be started.",
                technical_details=str(exc),
                recoverable=True,
            ),
        )

def _start_background_job(
    job_service: JobService,
    job_id: str,
    *,
    initial_step: str,
    operation: Callable[[], Any],
) -> None:
    """Run a local operation in a daemon thread and store its result in a job."""

    def runner() -> None:
        current = job_service.get_job(job_id)
        if current is None or current.status == "cancelled":
            return
        job_service.update_job_status(
            job_id,
            "running",
            current_step=initial_step,
            progress_percent=0,
        )
        try:
            result = operation()
        except Exception as exc:  # pragma: no cover - defensive safety net
            job_service.fail_job(
                job_id,
                ErrorState(
                    code="unknown_error",
                    message="Background job failed.",
                    technical_details=str(exc),
                    recoverable=True,
                ),
            )
            return

        result_data = (
            result.model_dump(mode="json")
            if hasattr(result, "model_dump")
            else result
        )
        refreshed = job_service.get_job(job_id)
        if refreshed and refreshed.cancel_requested:
            job_service.update_job_status(
                job_id,
                "cancelled",
                current_step="cancelled",
                result=result_data,
            )
            return
        if getattr(result, "status", None) == "cancelled":
            job_service.update_job_status(
                job_id,
                "cancelled",
                current_step="cancelled",
                result=result_data,
            )
            return
        errors = getattr(result, "errors", []) or []
        if errors:
            error = errors[0]
            job_service.fail_job(job_id, error, result=result_data)
            return
        job_service.finish_job(job_id, result_data)

    Thread(target=runner, daemon=True).start()
