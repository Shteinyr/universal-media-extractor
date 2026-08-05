"""Managed local output directory helpers."""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from urllib.parse import urlparse

from universal_media_extractor.models import (
    OutputDeleteResult,
    OutputListResult,
    OutputSummary,
)


class OutputManager:
    """Create safe local artifact directories."""

    def create_analysis_output_dir(
        self, base_dir: Path, source_id: str | None = None
    ) -> Path:
        """Create a directory for analysis artifacts only."""

        base_path = base_dir.expanduser().resolve()
        safe_source_id = _safe_slug_part(source_id or "unknown")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        unique_suffix = uuid4().hex[:8]
        dirname = f"analysis_{safe_source_id}_{timestamp}_{unique_suffix}"
        output_dir = (base_path / dirname).resolve()

        if not output_dir.is_relative_to(base_path):
            raise ValueError("Output directory must stay inside base_dir.")

        output_dir.mkdir(parents=True, exist_ok=False)
        return output_dir

    def create_download_output_dir(
        self,
        base_dir: Path,
        source_id: str | None = None,
        source_title: str | None = None,
        *,
        source_url: str | None = None,
        output_template: str | None = None,
        duplicate_policy: str = "rename",
        project_name: str | None = None,
        channel_name: str | None = None,
        playlist_index: int | None = None,
    ) -> Path:
        """Create a user-facing directory for one download attempt."""

        base_path = base_dir.expanduser().resolve()
        dirname = render_output_template(
            output_template or "{title}",
            {
                "source": _source_name(source_url, source_id),
                "channel": channel_name or "",
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "title": source_title or source_id or "download",
                "project": project_name or "",
                "playlist_index": _format_playlist_index(playlist_index),
            },
        )
        output_dir = _apply_duplicate_policy(base_path, dirname, duplicate_policy)

        if not output_dir.is_relative_to(base_path):
            raise ValueError("Output directory must stay inside base_dir.")

        output_dir.mkdir(parents=True, exist_ok=False)
        (output_dir / ".metadata").mkdir(parents=True, exist_ok=True)
        (output_dir / ".logs").mkdir(parents=True, exist_ok=True)
        return output_dir

    def create_local_file_output_dir(
        self, base_dir: Path, filename: str | None = None
    ) -> Path:
        """Create a structured directory for one local file workflow."""

        base_path = base_dir.expanduser().resolve()
        safe_filename = _safe_slug_part(Path(filename or "local_file").stem)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dirname = f"local_{timestamp}_{safe_filename}"
        output_dir = (base_path / dirname).resolve()
        if output_dir.exists():
            output_dir = (base_path / f"{dirname}_{uuid4().hex[:8]}").resolve()

        if not output_dir.is_relative_to(base_path):
            raise ValueError("Output directory must stay inside base_dir.")

        (output_dir / "source").mkdir(parents=True, exist_ok=False)
        (output_dir / "media").mkdir(parents=True, exist_ok=True)
        (output_dir / "metadata").mkdir(parents=True, exist_ok=True)
        (output_dir / "logs").mkdir(parents=True, exist_ok=True)
        (output_dir / "transcripts").mkdir(parents=True, exist_ok=True)
        return output_dir

    def ensure_transcription_output_structure(self, output_dir: Path) -> Path:
        """Ensure an output directory can hold transcription artifacts."""

        output_path = output_dir.expanduser().resolve()
        if (output_path / ".metadata").is_dir():
            (output_path / ".metadata").mkdir(parents=True, exist_ok=True)
            (output_path / ".logs").mkdir(parents=True, exist_ok=True)
            (output_path / ".work").mkdir(parents=True, exist_ok=True)
        else:
            (output_path / "media").mkdir(parents=True, exist_ok=True)
            (output_path / "metadata").mkdir(parents=True, exist_ok=True)
            (output_path / "logs").mkdir(parents=True, exist_ok=True)
        return output_path

    def list_outputs(self, outputs_base_dir: Path) -> OutputListResult:
        """List direct user output folders under outputs_base_dir."""

        base_path = outputs_base_dir.expanduser().resolve()
        if not base_path.exists():
            return OutputListResult(outputs_base_dir=str(base_path), outputs=[])
        summaries = [
            self.summarize_output(base_path, item.name)
            for item in sorted(base_path.iterdir(), key=lambda path: path.name)
            if item.is_dir()
        ]
        summaries.sort(key=lambda item: item.last_modified_at, reverse=True)
        return OutputListResult(outputs_base_dir=str(base_path), outputs=summaries)

    def summarize_output(self, outputs_base_dir: Path, output_id: str) -> OutputSummary:
        """Summarize one safe output directory by id."""

        output_dir = _resolve_output_id(outputs_base_dir, output_id)
        if not output_dir.is_dir():
            raise FileNotFoundError(f"Output not found: {output_id}")

        files = sorted(path for path in output_dir.rglob("*") if path.is_file())
        total_size = sum(path.stat().st_size for path in files)
        modified_times = [path.stat().st_mtime for path in files]
        modified_times.append(output_dir.stat().st_mtime)
        created_at = _created_at_from_name(output_dir.name) or datetime.fromtimestamp(
            output_dir.stat().st_ctime, timezone.utc
        )
        last_modified_at = datetime.fromtimestamp(max(modified_times), timezone.utc)
        source_type, title_or_filename = _source_info(output_dir)

        return OutputSummary(
            output_id=output_dir.name,
            output_dir=str(output_dir),
            created_at=created_at,
            source_type=source_type,
            title_or_filename=title_or_filename or output_dir.name,
            has_media=_has_download_files(output_dir)
            or _has_files(output_dir / "media")
            or _has_files(output_dir / "source"),
            has_transcript=any(
                (output_dir / name).is_file()
                or (output_dir / "transcripts" / name).is_file()
                for name in ("transcript.txt", "transcript.md", "transcript.json")
            ),
            has_summary_prompt=(output_dir / "summary_prompt.md").is_file()
            or (output_dir / "transcripts" / "summary_prompt.md").is_file(),
            total_size_bytes=total_size,
            files_count=len(files),
            last_modified_at=last_modified_at,
        )

    def delete_output(self, outputs_base_dir: Path, output_id: str) -> OutputDeleteResult:
        """Safely delete one direct child of outputs_base_dir."""

        try:
            output_dir = _resolve_output_id(outputs_base_dir, output_id)
        except ValueError as exc:
            return OutputDeleteResult(
                output_id=output_id,
                status="blocked",
                message=str(exc),
            )

        if not output_dir.exists():
            return OutputDeleteResult(
                output_id=output_id,
                status="not_found",
                output_dir=str(output_dir),
                message="Output was not found.",
            )
        if not output_dir.is_dir():
            return OutputDeleteResult(
                output_id=output_id,
                status="blocked",
                output_dir=str(output_dir),
                message="Output target is not a directory.",
            )
        shutil.rmtree(output_dir)
        return OutputDeleteResult(
            output_id=output_id,
            status="deleted",
            output_dir=str(output_dir),
            message="Output deleted.",
        )


WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}
TEMPLATE_TOKEN_RE = re.compile(r"\{(source|channel|date|title|project|playlist_index)\}")
UNSAFE_FILENAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def render_output_template(template: str, context: dict[str, str]) -> str:
    """Render a direct output folder name from supported template tokens."""

    def replace(match: re.Match[str]) -> str:
        return context.get(match.group(1), "")

    rendered = TEMPLATE_TOKEN_RE.sub(replace, template.strip() or "{title}")
    return _safe_path_part(rendered or context.get("title", "download"))


def _safe_path_part(value: str) -> str:
    normalized = value.replace("/", " - ").replace("\\", " - ")
    normalized = UNSAFE_FILENAME_RE.sub(" ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip(" ._")
    safe = normalized or "unknown"
    if safe.upper() in WINDOWS_RESERVED_NAMES:
        safe = f"{safe}_file"
    return safe[:120].rstrip(" .") or "unknown"


def _safe_slug_part(value: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)
    return (safe.strip("_") or "unknown")[:80]


def _apply_duplicate_policy(base_path: Path, dirname: str, duplicate_policy: str) -> Path:
    output_dir = (base_path / dirname).resolve()
    if not output_dir.exists():
        return output_dir
    if duplicate_policy == "skip":
        raise FileExistsError(str(output_dir))
    if duplicate_policy == "overwrite":
        if output_dir == base_path or not output_dir.is_relative_to(base_path):
            raise ValueError("Output directory must stay inside base_dir.")
        if output_dir.is_dir():
            shutil.rmtree(output_dir)
        else:
            output_dir.unlink()
        return output_dir

    stem = dirname
    for index in range(2, 1000):
        candidate = (base_path / f"{stem} {index}").resolve()
        if not candidate.exists():
            return candidate
    return (base_path / f"{stem} {uuid4().hex[:8]}").resolve()


def _source_name(source_url: str | None, source_id: str | None) -> str:
    if source_url:
        host = urlparse(source_url).netloc.lower()
        return host.removeprefix("www.") or source_id or "source"
    return source_id or "source"


def _format_playlist_index(value: int | None) -> str:
    if value is None:
        return ""
    return f"{value:03d}"


def _resolve_output_id(outputs_base_dir: Path, output_id: str) -> Path:
    if not output_id or output_id in {".", ".."}:
        raise ValueError("Unsafe output id.")
    if "/" in output_id or "\\" in output_id:
        raise ValueError("Output id must be a direct folder name.")
    base_path = outputs_base_dir.expanduser().resolve()
    output_dir = (base_path / output_id).resolve()
    if output_dir == base_path or not output_dir.is_relative_to(base_path):
        raise ValueError("Output path must stay inside outputs directory.")
    return output_dir


def _created_at_from_name(name: str) -> datetime | None:
    parts = name.split("_")
    candidates = []
    if name.startswith("local_") and len(parts) >= 2:
        candidates.append(parts[1])
    if parts:
        candidates.append(parts[0])
    for candidate in candidates:
        try:
            return datetime.strptime(candidate, "%Y%m%dT%H%M%SZ").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue
    return None


def _source_info(output_dir: Path) -> tuple[str, str | None]:
    local_metadata = _read_json(output_dir / "metadata" / "local_file_analysis.json")
    if local_metadata:
        return "local_file", local_metadata.get("filename")

    download_request = _read_json(output_dir / ".metadata" / "download_request.json") or _read_json(
        output_dir / "metadata" / "download_request.json"
    )
    if download_request:
        source_url = download_request.get("source_url")
        return "url", download_request.get("source_title") or _title_from_download_output(output_dir) or source_url

    if output_dir.name.startswith("local_"):
        return "local_file", output_dir.name.split("_", 2)[-1] if "_" in output_dir.name else output_dir.name
    return "unknown", output_dir.name


def _title_from_download_output(output_dir: Path) -> str | None:
    first_file = next(iter(_download_files(output_dir)), None)
    if first_file is None:
        return None
    return first_file.stem


def _read_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _has_files(path: Path) -> bool:
    return path.exists() and any(item.is_file() for item in path.rglob("*"))


def _has_download_files(output_dir: Path) -> bool:
    return any(_download_files(output_dir))


def _download_files(output_dir: Path) -> list[Path]:
    return sorted(
        item
        for item in output_dir.iterdir()
        if item.is_file() and not item.name.startswith(".")
    )
