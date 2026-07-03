#!/usr/bin/env python3
"""Run the local-only analysis API."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import uvicorn


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local-only analysis API.")
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Local port to bind on 127.0.0.1.",
    )
    args = parser.parse_args()

    uvicorn.run(
        "universal_media_extractor.api.app:app",
        host="127.0.0.1",
        port=args.port,
        log_level="info",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
