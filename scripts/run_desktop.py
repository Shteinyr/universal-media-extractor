#!/usr/bin/env python3
"""Run Universal Media Extractor in a local desktop window."""

from __future__ import annotations

import argparse
import os
import socket
import sys
import time
from pathlib import Path
from threading import Thread
from urllib.error import URLError
from urllib.request import urlopen

import uvicorn


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_MAX_PORT = 8020
WINDOW_TITLE = "Universal Media Extractor"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 820
WINDOW_MIN_SIZE = (980, 680)
APP_SUPPORT_DIR = (
    Path.home() / "Library" / "Application Support" / "Universal Media Extractor"
)
DESKTOP_CLI_PATHS = (
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/usr/bin",
    "/bin",
    "/usr/sbin",
    "/sbin",
)

MEDIA_FILE_TYPES = (
    "Media files (*.mp3;*.m4a;*.wav;*.aac;*.flac;*.ogg;*.opus;*.mp4;*.m4v;*.mov;*.mkv;*.webm;*.avi)",
    "All files (*.*)",
)


class DesktopFilesystemApi:
    """Small pywebview bridge for native local file/folder selection."""

    def __init__(self) -> None:
        self.window: object | None = None

    def set_window(self, window: object) -> None:
        self.window = window

    def choose_output_folder(self) -> str | None:
        """Return one native-selected folder path, or None when cancelled."""

        return self._choose_dialog("folder")

    def choose_local_file(self) -> str | None:
        """Return one native-selected media file path, or None when cancelled."""

        return self._choose_dialog("open")

    def _choose_dialog(self, dialog_kind: str) -> str | None:
        if self.window is None:
            return None
        try:
            import webview
        except ImportError:
            return None

        dialog_type = (
            webview.FileDialog.FOLDER
            if dialog_kind == "folder"
            else webview.FileDialog.OPEN
        )
        kwargs = {
            "dialog_type": dialog_type,
            "directory": str(Path.home()),
            "allow_multiple": False,
        }
        if dialog_kind == "open":
            kwargs["file_types"] = MEDIA_FILE_TYPES
        result = self.window.create_file_dialog(**kwargs)
        if not result:
            return None
        return str(result[0])


def main() -> int:
    args = parse_args()
    ensure_cli_search_path()
    port = find_available_port(
        host=args.host,
        preferred_port=args.port,
        max_port=args.max_port,
    )
    app_url = f"http://{args.host}:{port}/"
    health_url = f"http://{args.host}:{port}/health"

    runtime_paths = resolve_runtime_paths(
        profile=args.profile,
        app_data_dir=args.app_data_dir,
    )
    server, thread = start_backend(args.host, port, **runtime_paths)
    try:
        wait_for_backend(health_url, timeout_seconds=args.startup_timeout)
        print(f"Desktop UI: {app_url}")
        return open_desktop_window(app_url, smoke_seconds=args.smoke_seconds)
    finally:
        stop_backend(server, thread)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local FastAPI app inside a pywebview desktop window.",
    )
    parser.add_argument(
        "--host",
        default=HOST,
        choices=[HOST],
        help="Local host to bind. Only 127.0.0.1 is supported.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Preferred local port.",
    )
    parser.add_argument(
        "--max-port",
        type=int,
        default=DEFAULT_MAX_PORT,
        help="Highest local port to try if the preferred port is busy.",
    )
    parser.add_argument(
        "--startup-timeout",
        type=float,
        default=15.0,
        help="Seconds to wait for the local backend to become healthy.",
    )
    parser.add_argument(
        "--smoke-seconds",
        type=float,
        default=None,
        help="Development proof helper: close the desktop window after N seconds.",
    )
    parser.add_argument(
        "--profile",
        choices=["dev", "production"],
        default="production" if is_frozen_app() else "dev",
        help="Runtime profile. Frozen macOS bundles default to production.",
    )
    parser.add_argument(
        "--app-data-dir",
        type=Path,
        default=None,
        help="Production profile app data directory. Defaults to ~/Library/Application Support/Universal Media Extractor.",
    )
    return parser.parse_args()


def is_frozen_app() -> bool:
    """Return True when running from a frozen app bundle."""

    return bool(getattr(sys, "frozen", False))


def resolve_runtime_paths(
    *,
    profile: str,
    app_data_dir: Path | None = None,
) -> dict[str, Path | None]:
    """Resolve backend storage locations for dev vs production desktop runs."""

    if profile != "production":
        return {
            "raw_output_base_dir": None,
            "output_base_dir": None,
            "job_db_path": None,
        }

    base_dir = (app_data_dir or APP_SUPPORT_DIR).expanduser().resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    return {
        "raw_output_base_dir": base_dir / "analysis",
        "output_base_dir": Path.home() / "Downloads" / "Universal Media Extractor",
        "job_db_path": base_dir / "jobs.sqlite3",
    }


def ensure_cli_search_path() -> None:
    """Make Homebrew/system CLIs discoverable when launched from Finder."""

    existing_paths = [path for path in os.environ.get("PATH", "").split(os.pathsep) if path]
    merged_paths: list[str] = []
    for path in (*DESKTOP_CLI_PATHS, *existing_paths):
        if path not in merged_paths:
            merged_paths.append(path)
    os.environ["PATH"] = os.pathsep.join(merged_paths)


def find_available_port(
    *,
    host: str = HOST,
    preferred_port: int = DEFAULT_PORT,
    max_port: int = DEFAULT_MAX_PORT,
) -> int:
    """Return the first bindable localhost port in the requested range."""

    if preferred_port > max_port:
        raise ValueError("preferred_port must be less than or equal to max_port.")

    for port in range(preferred_port, max_port + 1):
        if is_port_available(host, port):
            return port
    raise RuntimeError(
        f"No available local port found from {preferred_port} to {max_port}."
    )


def is_port_available(host: str, port: int) -> bool:
    """Check whether a local TCP port can be bound."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def start_backend(
    host: str,
    port: int,
    *,
    raw_output_base_dir: Path | None = None,
    output_base_dir: Path | None = None,
    job_db_path: Path | None = None,
) -> tuple[uvicorn.Server, Thread]:
    """Start the FastAPI backend on localhost in a background thread."""

    from universal_media_extractor.api.app import create_app

    config = uvicorn.Config(
        create_app(
            raw_output_base_dir=raw_output_base_dir,
            output_base_dir=output_base_dir,
            job_db_path=job_db_path,
        ),
        host=host,
        port=port,
        log_level="info",
        access_log=False,
    )
    server = uvicorn.Server(config)
    thread = Thread(target=server.run, name="ume-desktop-backend", daemon=True)
    thread.start()
    return server, thread


def wait_for_backend(url: str, *, timeout_seconds: float = 15.0) -> None:
    """Wait until the local backend responds to /health."""

    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=1.0) as response:
                if response.status == 200:
                    return
        except (OSError, URLError) as exc:
            last_error = exc
        time.sleep(0.1)
    raise RuntimeError(f"Backend did not become ready at {url}") from last_error


def stop_backend(server: uvicorn.Server, thread: Thread, *, timeout_seconds: float = 5.0) -> None:
    """Ask Uvicorn to stop and wait briefly for the backend thread."""

    server.should_exit = True
    thread.join(timeout=timeout_seconds)


def open_desktop_window(app_url: str, *, smoke_seconds: float | None = None) -> int:
    """Open the current local UI in a pywebview window."""

    try:
        import webview
    except ImportError as exc:
        print(
            "pywebview is not installed. Run "
            "`.venv/bin/python -m pip install -r requirements.txt`.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    desktop_api = DesktopFilesystemApi()
    window = webview.create_window(
        WINDOW_TITLE,
        app_url,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=WINDOW_MIN_SIZE,
        background_color="#111315",
        js_api=desktop_api,
    )
    desktop_api.set_window(window)

    if smoke_seconds is not None:
        webview.start(_close_after_delay, args=(window, smoke_seconds))
    else:
        webview.start()
    return 0


def _close_after_delay(window: object, seconds: float) -> None:
    """Close pywebview after a short delay for manual smoke automation."""

    def closer() -> None:
        time.sleep(max(0.1, seconds))
        destroy = getattr(window, "destroy", None)
        if callable(destroy):
            destroy()

    Thread(target=closer, name="ume-desktop-smoke-close", daemon=True).start()


if __name__ == "__main__":
    raise SystemExit(main())
