#!/usr/bin/env python3
"""Build a production-foundation macOS .app bundle with PyInstaller."""

from __future__ import annotations

import argparse
import os
import platform
import plistlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "Universal Media Extractor.app"
BUNDLE_IDENTIFIER = "com.shteinyr.universal-media-extractor"
SPEC_PATH = ROOT / "packaging" / "macos" / "universal_media_extractor_macos.spec"
DIST_DIR = ROOT / "build" / "macos" / "dist"
WORK_DIR = ROOT / "build" / "macos" / "work"


def main() -> int:
    args = parse_args()
    app_path = build_macos_app(
        project_root=args.project_root.resolve(),
        spec_path=args.spec_file.resolve(),
        dist_dir=args.dist_dir.resolve(),
        work_dir=args.work_dir.resolve(),
        clean=args.clean,
        allow_non_macos=args.allow_non_macos,
        ad_hoc_sign=args.ad_hoc_sign,
    )
    print(f"macOS app created: {app_path}")
    print(f'Run smoke with: open -W "{app_path}" --args --smoke-seconds 3')
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the production-foundation macOS .app bundle.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=ROOT,
        help="Project root to build.",
    )
    parser.add_argument(
        "--spec-file",
        type=Path,
        default=SPEC_PATH,
        help="PyInstaller spec file.",
    )
    parser.add_argument(
        "--dist-dir",
        type=Path,
        default=DIST_DIR,
        help="PyInstaller dist output directory.",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=WORK_DIR,
        help="PyInstaller work directory.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_false",
        dest="clean",
        help="Do not clean PyInstaller work before building.",
    )
    parser.add_argument(
        "--ad-hoc-sign",
        action="store_true",
        help="Apply local ad-hoc codesign after build. This is not Developer ID signing/notarization.",
    )
    parser.add_argument(
        "--allow-non-macos",
        action="store_true",
        help="Test helper: allow command construction on non-macOS hosts.",
    )
    parser.set_defaults(clean=True)
    return parser.parse_args()


def build_macos_app(
    *,
    project_root: Path,
    spec_path: Path,
    dist_dir: Path,
    work_dir: Path,
    clean: bool = True,
    allow_non_macos: bool = False,
    ad_hoc_sign: bool = False,
) -> Path:
    """Run PyInstaller and validate the resulting macOS app bundle."""

    validate_build_inputs(
        project_root=project_root,
        spec_path=spec_path,
        allow_non_macos=allow_non_macos,
    )
    command = build_pyinstaller_command(
        spec_path=spec_path,
        dist_dir=dist_dir,
        work_dir=work_dir,
        clean=clean,
    )
    env = os.environ.copy()
    config_dir = work_dir.parent / "pyinstaller-config"
    config_dir.mkdir(parents=True, exist_ok=True)
    env["PYINSTALLER_CONFIG_DIR"] = str(config_dir)
    subprocess.run(command, cwd=project_root, check=True, env=env)
    app_path = dist_dir / APP_NAME
    validate_app_bundle(app_path)
    if ad_hoc_sign:
        ad_hoc_codesign(app_path)
    return app_path


def validate_build_inputs(
    *,
    project_root: Path,
    spec_path: Path,
    allow_non_macos: bool = False,
) -> None:
    """Fail early when the local host cannot produce the intended macOS bundle."""

    if not allow_non_macos and sys.platform != "darwin":
        raise RuntimeError("macOS production app builds must run on macOS.")
    if not allow_non_macos and platform.machine() != "arm64":
        raise RuntimeError("This build target is Apple Silicon arm64.")
    if not (project_root / "scripts" / "run_desktop.py").is_file():
        raise FileNotFoundError("scripts/run_desktop.py is required for the app entrypoint.")
    if not (project_root / "src" / "universal_media_extractor" / "static" / "index.html").is_file():
        raise FileNotFoundError("Static UI assets are required for the app bundle.")
    if not spec_path.is_file():
        raise FileNotFoundError(f"PyInstaller spec file not found: {spec_path}")
    pyinstaller_version()


def pyinstaller_version() -> str:
    """Return the installed PyInstaller version or raise a useful error."""

    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(
            "PyInstaller is required. Run `.venv/bin/python -m pip install -r requirements-packaging.txt`."
        ) from exc
    return result.stdout.strip()


def build_pyinstaller_command(
    *,
    spec_path: Path,
    dist_dir: Path,
    work_dir: Path,
    clean: bool = True,
) -> list[str]:
    """Build the PyInstaller command as list args."""

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(spec_path),
        "--noconfirm",
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(work_dir),
    ]
    if clean:
        command.append("--clean")
    return command


def validate_app_bundle(app_path: Path) -> None:
    """Check the expected macOS bundle structure after PyInstaller finishes."""

    contents_dir = app_path / "Contents"
    plist_path = contents_dir / "Info.plist"
    executable_path = contents_dir / "MacOS" / "Universal Media Extractor"
    resources_dir = contents_dir / "Resources"
    static_index = contents_dir / "Frameworks" / "universal_media_extractor" / "static" / "index.html"

    if not app_path.is_dir():
        raise FileNotFoundError(f"App bundle was not created: {app_path}")
    if not plist_path.is_file():
        raise FileNotFoundError(f"Info.plist missing: {plist_path}")
    if not executable_path.is_file():
        raise FileNotFoundError(f"Executable missing: {executable_path}")
    if not resources_dir.is_dir():
        raise FileNotFoundError(f"Resources directory missing: {resources_dir}")
    if not static_index.is_file():
        raise FileNotFoundError(f"Static UI was not bundled: {static_index}")

    plist = plistlib.loads(plist_path.read_bytes())
    if plist.get("CFBundleIdentifier") != BUNDLE_IDENTIFIER:
        raise ValueError("Unexpected bundle identifier in Info.plist.")
    if plist.get("CFBundlePackageType") != "APPL":
        raise ValueError("Bundle is not marked as a macOS application.")


def ad_hoc_codesign(app_path: Path) -> None:
    """Apply local ad-hoc signing. This is not notarization."""

    codesign = shutil.which("codesign")
    if not codesign:
        raise RuntimeError("codesign was not found.")
    subprocess.run(
        [codesign, "--force", "--deep", "--sign", "-", str(app_path)],
        check=True,
    )


if __name__ == "__main__":
    raise SystemExit(main())
