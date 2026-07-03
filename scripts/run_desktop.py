#!/usr/bin/env python3
"""Run Universal Media Extractor in a local desktop window."""

from __future__ import annotations

import argparse
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


def main() -> int:
    args = parse_args()
    port = find_available_port(
        host=args.host,
        preferred_port=args.port,
        max_port=args.max_port,
    )
    app_url = f"http://{args.host}:{port}/"
    health_url = f"http://{args.host}:{port}/health"

    server, thread = start_backend(args.host, port)
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
    return parser.parse_args()


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


def start_backend(host: str, port: int) -> tuple[uvicorn.Server, Thread]:
    """Start the FastAPI backend on localhost in a background thread."""

    from universal_media_extractor.api.app import create_app

    config = uvicorn.Config(
        create_app(),
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

    window = webview.create_window(
        WINDOW_TITLE,
        app_url,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=WINDOW_MIN_SIZE,
        background_color="#111315",
    )

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
