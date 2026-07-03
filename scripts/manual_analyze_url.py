#!/usr/bin/env python3
"""Manual URL analysis helper.

This script is intentionally not run as part of Phase 6. It performs analysis
only through the safe analyzer wrapper when a user explicitly runs it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.analyzers import analyze_url_with_ytdlp


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a URL with yt-dlp safely.")
    parser.add_argument("url", help="URL to analyze without downloading media")
    parser.add_argument(
        "--raw-output-dir",
        type=Path,
        default=None,
        help="Optional directory for raw yt-dlp JSON artifacts",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=60,
        help="yt-dlp analysis timeout in seconds",
    )
    args = parser.parse_args()

    result = analyze_url_with_ytdlp(
        args.url,
        timeout_seconds=args.timeout_seconds,
        raw_output_dir=args.raw_output_dir,
    )
    print(result.model_dump_json(indent=2))
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

