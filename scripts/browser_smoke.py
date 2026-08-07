#!/usr/bin/env python3
"""Minimal browser smoke check for the local static UI.

The backend must already be running on http://127.0.0.1:8000.
Default mode performs analysis only and does not download or transcribe.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, Page, TimeoutError as PlaywrightTimeoutError, sync_playwright


DEFAULT_BASE_URL = "http://127.0.0.1:8000/"
DEFAULT_URL = "https://youtu.be/UUdxAp3kuKA"
DEFAULT_PROOF_DIR = Path("proof/block_10")


def main() -> int:
    args = parse_args()
    proof_dir = args.proof_dir
    proof_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = launch_browser(playwright, headless=not args.headed)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        try:
            run_analysis_smoke(page, args.base_url, args.url, proof_dir)
            if args.full_flow:
                run_full_flow(page, proof_dir)
        finally:
            browser.close()

    print(f"Browser smoke completed. Screenshots: {proof_dir.resolve()}")
    return 0


def launch_browser(playwright, *, headless: bool):
    try:
        return playwright.chromium.launch(headless=headless)
    except PlaywrightError as exc:
        if "Executable doesn't exist" not in str(exc):
            raise
        return playwright.chromium.launch(channel="chrome", headless=headless)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a minimal Playwright smoke check against the local UI.",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--proof-dir", type=Path, default=DEFAULT_PROOF_DIR)
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show the browser window while running the smoke check.",
    )
    parser.add_argument(
        "--full-flow",
        action="store_true",
        help="Also download the selected audio format and transcribe it. Off by default.",
    )
    return parser.parse_args()


def run_analysis_smoke(page: Page, base_url: str, source_url: str, proof_dir: Path) -> None:
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("heading", name="Universal Media Extractor").wait_for(timeout=10_000)
    page.get_by_role("textbox", name="New task").wait_for(timeout=10_000)
    page.screenshot(path=proof_dir / "ui_initial.png", full_page=True)

    page.locator("#url-input").fill(source_url)
    page.locator("#analyze-button").click()
    page.locator("#media-title").get_by_text("Showreel", exact=True).wait_for(timeout=90_000)

    assert_visible_text(page, "Best video")
    assert_visible_text(page, "1080p")
    assert_visible_text(page, "Up to 720p")
    assert_visible_text(page, "Audio M4A")
    assert_visible_text(page, "Subtitles")

    page.screenshot(path=proof_dir / "ui_analyze_result.png", full_page=True)

    page.get_by_role("button", name=re.compile("Best video")).click()
    assert_visible_text(page, "Save to")
    assert_visible_text(page, "Format")
    assert_visible_text(page, "Download")
    page.screenshot(path=proof_dir / "ui_output_selected.png", full_page=True)


def run_full_flow(page: Page, proof_dir: Path) -> None:
    first_audio = page.get_by_role("button", name=re.compile("Audio M4A"))
    first_audio.click()
    page.locator("#download-button").click()
    wait_for_status_text(page, "#download-result", "Download saved", timeout_ms=240_000)
    page.screenshot(path=proof_dir / "ui_download_result.png", full_page=True)

    page.locator("#whisper-model").select_option("tiny")
    page.locator("#transcribe-button").click()
    wait_for_status_text(page, "#transcript-result", "Transcript saved", timeout_ms=900_000)
    assert_visible_text(page, "Saved result")
    assert_visible_text(page, "Copy transcript")
    page.screenshot(path=proof_dir / "ui_transcribe_result.png", full_page=True)


def assert_visible_text(page: Page, text: str) -> None:
    page.get_by_text(text, exact=False).first.wait_for(timeout=10_000)


def wait_for_status_text(page: Page, selector: str, text: str, *, timeout_ms: int) -> None:
    deadline = time.monotonic() + (timeout_ms / 1000)
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            page.locator(selector).get_by_text(text, exact=False).wait_for(timeout=2_000)
            return
        except PlaywrightTimeoutError as exc:
            last_error = exc
    raise TimeoutError(f"Timed out waiting for {text!r} in {selector}") from last_error


if __name__ == "__main__":
    sys.exit(main())
