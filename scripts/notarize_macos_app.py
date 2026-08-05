#!/usr/bin/env python3
"""Prepare, submit, staple, and assess a signed macOS app bundle."""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP_PATH = ROOT / "build" / "macos" / "dist" / "Universal Media Extractor.app"
DEFAULT_ARCHIVE_PATH = ROOT / "build" / "macos" / "notarization" / "Universal Media Extractor.zip"
DEFAULT_NOTARY_LOG = ROOT / "build" / "macos" / "notarization" / "notary_log.json"


def main() -> int:
    args = parse_args()
    args.archive_path.parent.mkdir(parents=True, exist_ok=True)
    commands = [build_archive_command(app_path=args.app_path, archive_path=args.archive_path)]
    if not args.prepare_only:
        commands.extend(
            [
                build_notary_submit_command(
                    archive_path=args.archive_path,
                    keychain_profile=args.keychain_profile,
                    timeout=args.timeout,
                ),
                build_stapler_staple_command(args.app_path),
                build_stapler_validate_command(args.app_path),
                build_gatekeeper_assess_command(args.app_path),
            ]
        )
    for command in commands:
        print(format_command(command))
        if not args.dry_run:
            subprocess.run(command, check=True)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notarize and staple a signed macOS app bundle.")
    parser.add_argument("--app-path", type=Path, default=DEFAULT_APP_PATH)
    parser.add_argument("--archive-path", type=Path, default=DEFAULT_ARCHIVE_PATH)
    parser.add_argument("--notary-log", type=Path, default=DEFAULT_NOTARY_LOG)
    parser.add_argument("--keychain-profile", default="UME_NOTARY", help="notarytool keychain profile name.")
    parser.add_argument("--timeout", default="30m", help="notarytool wait timeout.")
    parser.add_argument("--prepare-only", action="store_true", help="Create the notarization zip only.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them.")
    return parser.parse_args()


def build_archive_command(*, app_path: Path, archive_path: Path) -> list[str]:
    return ["ditto", "-c", "-k", "--keepParent", str(app_path), str(archive_path)]


def build_store_credentials_command(*, profile: str, apple_id: str, team_id: str) -> list[str]:
    return ["xcrun", "notarytool", "store-credentials", profile, "--apple-id", apple_id, "--team-id", team_id]


def build_notary_submit_command(*, archive_path: Path, keychain_profile: str, timeout: str) -> list[str]:
    return [
        "xcrun",
        "notarytool",
        "submit",
        str(archive_path),
        "--keychain-profile",
        keychain_profile,
        "--wait",
        "--timeout",
        timeout,
        "--output-format",
        "json",
    ]


def build_notary_log_command(*, submission_id: str, keychain_profile: str, log_path: Path) -> list[str]:
    return ["xcrun", "notarytool", "log", submission_id, "--keychain-profile", keychain_profile, str(log_path)]


def build_stapler_staple_command(app_path: Path) -> list[str]:
    return ["xcrun", "stapler", "staple", str(app_path)]


def build_stapler_validate_command(app_path: Path) -> list[str]:
    return ["xcrun", "stapler", "validate", str(app_path)]


def build_gatekeeper_assess_command(app_path: Path) -> list[str]:
    return ["spctl", "--assess", "--type", "execute", "--verbose=4", str(app_path)]


def format_command(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


if __name__ == "__main__":
    raise SystemExit(main())
