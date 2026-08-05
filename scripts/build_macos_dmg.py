#!/usr/bin/env python3
"""Build a local macOS DMG from the current .app bundle."""

from __future__ import annotations

import argparse
import hashlib
import platform
import plistlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "Universal Media Extractor.app"
VOLUME_NAME = "Universal Media Extractor"
BUNDLE_IDENTIFIER = "com.shteinyr.universal-media-extractor"
DEFAULT_APP_PATH = ROOT / "build" / "macos" / "dist" / APP_NAME
DEFAULT_DMG_DIR = ROOT / "build" / "macos" / "dmg"
DEFAULT_STAGING_DIR = ROOT / "build" / "macos" / "dmg-staging"
DEFAULT_DMG_PATH = DEFAULT_DMG_DIR / "Universal Media Extractor.dmg"


def main() -> int:
    args = parse_args()
    dmg_path = build_dmg(
        app_path=args.app_path.resolve(),
        dmg_path=args.dmg_path.resolve(),
        staging_dir=args.staging_dir.resolve(),
        volume_name=args.volume_name,
        sign_identity=args.sign_identity,
        clean=args.clean,
        allow_non_macos=args.allow_non_macos,
        dry_run=args.dry_run,
    )
    if args.dry_run:
        print(f"DMG dry-run complete: {dmg_path}")
    else:
        checksum_path = write_sha256_file(dmg_path)
        print(f"DMG created: {dmg_path}")
        print(f"SHA-256: {checksum_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local macOS DMG installer artifact.")
    parser.add_argument("--app-path", type=Path, default=DEFAULT_APP_PATH)
    parser.add_argument("--dmg-path", type=Path, default=DEFAULT_DMG_PATH)
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING_DIR)
    parser.add_argument("--volume-name", default=VOLUME_NAME)
    parser.add_argument(
        "--sign-identity",
        default=None,
        help="Optional Developer ID Application identity for signing the DMG. Real public release still requires notarization/stapling.",
    )
    parser.add_argument("--no-clean", action="store_false", dest="clean")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-non-macos", action="store_true", help="Test helper for command construction.")
    parser.set_defaults(clean=True)
    return parser.parse_args()


def build_dmg(
    *,
    app_path: Path,
    dmg_path: Path,
    staging_dir: Path,
    volume_name: str = VOLUME_NAME,
    sign_identity: str | None = None,
    clean: bool = True,
    allow_non_macos: bool = False,
    dry_run: bool = False,
) -> Path:
    validate_dmg_inputs(app_path=app_path, allow_non_macos=allow_non_macos)
    prepare_staging(app_path=app_path, staging_dir=staging_dir, clean=clean)
    dmg_path.parent.mkdir(parents=True, exist_ok=True)
    if dmg_path.exists() and clean:
        dmg_path.unlink()

    commands = [
        build_hdiutil_create_command(
            staging_dir=staging_dir,
            dmg_path=dmg_path,
            volume_name=volume_name,
        )
    ]
    if sign_identity:
        commands.append(build_codesign_dmg_command(dmg_path=dmg_path, identity=sign_identity))
    commands.append(build_hdiutil_verify_command(dmg_path))

    for command in commands:
        print(format_command(command))
        if not dry_run:
            subprocess.run(command, check=True)
    return dmg_path


def validate_dmg_inputs(*, app_path: Path, allow_non_macos: bool = False) -> None:
    if not allow_non_macos and sys.platform != "darwin":
        raise RuntimeError("DMG builds must run on macOS.")
    if not allow_non_macos and platform.machine() != "arm64":
        raise RuntimeError("This DMG target is Apple Silicon arm64.")
    if not app_path.is_dir():
        raise FileNotFoundError(f"App bundle not found: {app_path}")
    plist_path = app_path / "Contents" / "Info.plist"
    executable_path = app_path / "Contents" / "MacOS" / "Universal Media Extractor"
    if not plist_path.is_file():
        raise FileNotFoundError(f"Info.plist missing: {plist_path}")
    if not executable_path.is_file():
        raise FileNotFoundError(f"Executable missing: {executable_path}")
    plist = plistlib.loads(plist_path.read_bytes())
    if plist.get("CFBundleIdentifier") != BUNDLE_IDENTIFIER:
        raise ValueError("Unexpected bundle identifier in app bundle.")


def prepare_staging(*, app_path: Path, staging_dir: Path, clean: bool = True) -> Path:
    if staging_dir.exists() and clean:
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)
    staged_app = staging_dir / app_path.name
    if staged_app.exists() and clean:
        shutil.rmtree(staged_app)
    shutil.copytree(app_path, staged_app, symlinks=True)
    applications_link = staging_dir / "Applications"
    if applications_link.exists() or applications_link.is_symlink():
        applications_link.unlink()
    applications_link.symlink_to("/Applications")
    return staging_dir


def build_hdiutil_create_command(*, staging_dir: Path, dmg_path: Path, volume_name: str) -> list[str]:
    return [
        "hdiutil",
        "create",
        "-volname",
        volume_name,
        "-srcfolder",
        str(staging_dir),
        "-ov",
        "-format",
        "UDZO",
        str(dmg_path),
    ]


def build_hdiutil_verify_command(dmg_path: Path) -> list[str]:
    return ["hdiutil", "verify", str(dmg_path)]


def build_codesign_dmg_command(*, dmg_path: Path, identity: str) -> list[str]:
    return [
        "codesign",
        "--force",
        "--timestamp",
        "--sign",
        identity,
        "-i",
        f"{BUNDLE_IDENTIFIER}.dmg",
        str(dmg_path),
    ]


def build_stapler_dmg_command(dmg_path: Path) -> list[str]:
    return ["xcrun", "stapler", "staple", str(dmg_path)]


def build_spctl_dmg_assess_command(dmg_path: Path) -> list[str]:
    return ["spctl", "--assess", "--type", "open", "--verbose=4", str(dmg_path)]


def write_sha256_file(path: Path) -> Path:
    checksum = sha256_file(path)
    checksum_path = path.with_suffix(path.suffix + ".sha256")
    checksum_path.write_text(f"{checksum}  {path.name}\n")
    return checksum_path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_command(command: list[str]) -> str:
    import shlex

    return " ".join(shlex.quote(part) for part in command)


if __name__ == "__main__":
    raise SystemExit(main())
