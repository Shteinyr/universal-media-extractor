#!/usr/bin/env python3
"""Submit, staple, and assess a signed macOS DMG for public distribution."""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DMG_PATH = ROOT / "build" / "macos" / "dmg" / "Universal Media Extractor.dmg"


def main() -> int:
    args = parse_args()
    commands = [
        build_notary_submit_command(
            dmg_path=args.dmg_path,
            keychain_profile=args.keychain_profile,
            timeout=args.timeout,
        ),
        build_stapler_staple_command(args.dmg_path),
        build_stapler_validate_command(args.dmg_path),
        build_gatekeeper_assess_command(args.dmg_path),
    ]
    for command in commands:
        print(format_command(command))
        if not args.dry_run:
            subprocess.run(command, check=True)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notarize and staple a signed macOS DMG.")
    parser.add_argument("--dmg-path", type=Path, default=DEFAULT_DMG_PATH)
    parser.add_argument("--keychain-profile", default="UME_NOTARY", help="notarytool keychain profile name.")
    parser.add_argument("--timeout", default="30m", help="notarytool wait timeout.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them.")
    return parser.parse_args()


def build_notary_submit_command(*, dmg_path: Path, keychain_profile: str, timeout: str) -> list[str]:
    return [
        "xcrun",
        "notarytool",
        "submit",
        str(dmg_path),
        "--keychain-profile",
        keychain_profile,
        "--wait",
        "--timeout",
        timeout,
        "--output-format",
        "json",
    ]


def build_stapler_staple_command(dmg_path: Path) -> list[str]:
    return ["xcrun", "stapler", "staple", str(dmg_path)]


def build_stapler_validate_command(dmg_path: Path) -> list[str]:
    return ["xcrun", "stapler", "validate", str(dmg_path)]


def build_gatekeeper_assess_command(dmg_path: Path) -> list[str]:
    return ["spctl", "--assess", "--type", "open", "--verbose=4", str(dmg_path)]


def format_command(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


if __name__ == "__main__":
    raise SystemExit(main())
