#!/usr/bin/env python3
"""Sign the macOS app bundle with Developer ID and hardened runtime."""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP_PATH = ROOT / "build" / "macos" / "dist" / "Universal Media Extractor.app"
DEFAULT_ENTITLEMENTS = ROOT / "packaging" / "macos" / "entitlements.plist"


def main() -> int:
    args = parse_args()
    commands = [
        build_codesign_command(
            app_path=args.app_path,
            identity=args.identity,
            entitlements_path=args.entitlements,
        ),
        build_codesign_verify_command(args.app_path),
        build_codesign_display_command(args.app_path),
    ]
    for command in commands:
        print(format_command(command))
        if not args.dry_run:
            subprocess.run(command, check=True)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sign the macOS .app with Developer ID.")
    parser.add_argument("--app-path", type=Path, default=DEFAULT_APP_PATH)
    parser.add_argument("--entitlements", type=Path, default=DEFAULT_ENTITLEMENTS)
    parser.add_argument(
        "--identity",
        required=True,
        help='Developer ID Application identity, for example: Developer ID Application: Name (TEAMID)',
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them.")
    return parser.parse_args()


def build_codesign_command(*, app_path: Path, identity: str, entitlements_path: Path) -> list[str]:
    return [
        "codesign",
        "--force",
        "--deep",
        "--options",
        "runtime",
        "--timestamp",
        "--sign",
        identity,
        "--entitlements",
        str(entitlements_path),
        str(app_path),
    ]


def build_codesign_verify_command(app_path: Path) -> list[str]:
    return ["codesign", "--verify", "--deep", "--strict", "--verbose=2", str(app_path)]


def build_codesign_display_command(app_path: Path) -> list[str]:
    return ["codesign", "--display", "--verbose=4", str(app_path)]


def format_command(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


if __name__ == "__main__":
    raise SystemExit(main())
