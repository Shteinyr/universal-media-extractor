#!/usr/bin/env python3
"""Store Apple notarytool credentials in the macOS Keychain."""

from __future__ import annotations

import argparse
import shlex
import subprocess


DEFAULT_PROFILE = "UME_NOTARY"


def main() -> int:
    args = parse_args()
    command = build_store_credentials_command(
        profile=args.profile,
        apple_id=args.apple_id,
        team_id=args.team_id,
    )
    print(format_command(command))
    if not args.dry_run:
        subprocess.run(command, check=True)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a notarytool keychain profile without storing secrets in the project.",
    )
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--apple-id", required=True, help="Apple ID email used for notarization.")
    parser.add_argument("--team-id", required=True, help="Apple Developer Team ID.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def build_store_credentials_command(*, profile: str, apple_id: str, team_id: str) -> list[str]:
    return [
        "xcrun",
        "notarytool",
        "store-credentials",
        profile,
        "--apple-id",
        apple_id,
        "--team-id",
        team_id,
    ]


def format_command(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


if __name__ == "__main__":
    raise SystemExit(main())
