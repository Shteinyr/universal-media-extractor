#!/usr/bin/env python3
"""Build a macOS development .app launcher for the current project.

The generated app does not bundle the Python project. It points back to this
working tree and runs `.venv/bin/python scripts/run_desktop.py`.
"""

from __future__ import annotations

import argparse
import plistlib
import shlex
import shutil
import stat
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "Universal Media Extractor Dev.app"
EXECUTABLE_NAME = "UniversalMediaExtractorDev"
BUNDLE_IDENTIFIER = "local.universal-media-extractor.dev"


def main() -> int:
    args = parse_args()
    app_path = build_dev_app(
        project_root=args.project_root.resolve(),
        output_dir=args.output_dir.resolve(),
    )
    print(f"Development app created: {app_path}")
    print(f'Run it with: open "{app_path}"')
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a macOS development .app that launches this project.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=ROOT,
        help="Project root that the generated .app should run.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "build" / "dev",
        help="Directory where the development .app should be generated.",
    )
    return parser.parse_args()


def build_dev_app(*, project_root: Path, output_dir: Path) -> Path:
    """Create a minimal macOS .app bundle that points at project_root."""

    validate_project_root(project_root)
    app_path = output_dir / APP_NAME
    contents_dir = app_path / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"

    if app_path.exists():
        shutil.rmtree(app_path)

    macos_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)
    write_info_plist(contents_dir / "Info.plist")
    write_shell_launcher(resources_dir / "launcher.zsh", project_root)
    write_c_launcher_source(resources_dir / "launcher.c")
    compile_c_launcher(
        source=resources_dir / "launcher.c",
        destination=macos_dir / EXECUTABLE_NAME,
    )
    return app_path


def validate_project_root(project_root: Path) -> None:
    """Check that project_root looks like this application project."""

    if not project_root.is_dir():
        raise FileNotFoundError(f"Project root not found: {project_root}")
    if not (project_root / "scripts" / "run_desktop.py").is_file():
        raise FileNotFoundError(
            f"Desktop launcher not found: {project_root / 'scripts' / 'run_desktop.py'}"
        )


def write_info_plist(destination: Path) -> None:
    """Write the minimal macOS bundle metadata."""

    plist = {
        "CFBundleDevelopmentRegion": "en",
        "CFBundleDisplayName": "Universal Media Extractor Dev",
        "CFBundleExecutable": EXECUTABLE_NAME,
        "CFBundleIdentifier": BUNDLE_IDENTIFIER,
        "CFBundleInfoDictionaryVersion": "6.0",
        "CFBundleName": "Universal Media Extractor Dev",
        "CFBundlePackageType": "APPL",
        "CFBundleShortVersionString": "0.1.0-dev",
        "CFBundleVersion": "1",
        "LSMinimumSystemVersion": "12.0",
        "NSHighResolutionCapable": True,
    }
    with destination.open("wb") as handle:
        plistlib.dump(plist, handle, sort_keys=True)


def write_shell_launcher(destination: Path, project_root: Path) -> None:
    """Write the shell launcher used by the compiled app executable."""

    launcher = f"""#!/bin/zsh
set -euo pipefail

PROJECT_ROOT={shlex.quote(str(project_root))}
PYTHON="$PROJECT_ROOT/.venv/bin/python"
DESKTOP_SCRIPT="$PROJECT_ROOT/scripts/run_desktop.py"

show_error() {{
  local message="$1"
  /usr/bin/osascript - "$message" <<'APPLESCRIPT' >/dev/null 2>&1 || true
on run argv
  display dialog item 1 of argv buttons {{"OK"}} default button "OK" with icon caution
end run
APPLESCRIPT
  echo "$message" >&2
}}

if [[ ! -d "$PROJECT_ROOT" ]]; then
  show_error "Universal Media Extractor project folder was not found: $PROJECT_ROOT"
  exit 1
fi

if [[ ! -x "$PYTHON" ]]; then
  show_error "Python virtual environment was not found: $PYTHON"
  exit 1
fi

if [[ ! -f "$DESKTOP_SCRIPT" ]]; then
  show_error "Desktop launcher was not found: $DESKTOP_SCRIPT"
  exit 1
fi

cd "$PROJECT_ROOT"
exec "$PYTHON" "$DESKTOP_SCRIPT" "$@"
"""
    destination.write_text(launcher, encoding="utf-8")
    current_mode = destination.stat().st_mode
    destination.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def write_c_launcher_source(destination: Path) -> None:
    """Write a tiny macOS executable wrapper source.

    Finder/LaunchServices can be unreliable with a shell script as the main
    CFBundleExecutable. A small compiled executable reliably starts the shell
    launcher from the app's Resources directory.
    """

    source = r'''#include <libgen.h>
#include <limits.h>
#include <mach-o/dyld.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    char executable_path[PATH_MAX];
    uint32_t size = sizeof(executable_path);
    if (_NSGetExecutablePath(executable_path, &size) != 0) {
        fprintf(stderr, "Executable path is too long.\n");
        return 1;
    }

    char resolved_path[PATH_MAX];
    const char *base_path = realpath(executable_path, resolved_path) ? resolved_path : executable_path;

    char executable_copy[PATH_MAX];
    char macos_dir[PATH_MAX];
    char macos_copy[PATH_MAX];
    char contents_path[PATH_MAX];
    snprintf(executable_copy, sizeof(executable_copy), "%s", base_path);
    snprintf(macos_dir, sizeof(macos_dir), "%s", dirname(executable_copy));
    snprintf(macos_copy, sizeof(macos_copy), "%s", macos_dir);
    snprintf(contents_path, sizeof(contents_path), "%s", dirname(macos_copy));

    char script_path[PATH_MAX];
    snprintf(script_path, sizeof(script_path), "%s/Resources/launcher.zsh", contents_path);

    char **exec_args = calloc((size_t)argc + 2, sizeof(char *));
    if (!exec_args) {
        fprintf(stderr, "Unable to allocate launcher arguments.\n");
        return 1;
    }
    exec_args[0] = "/bin/zsh";
    exec_args[1] = script_path;
    for (int index = 1; index < argc; index++) {
        exec_args[index + 1] = argv[index];
    }
    exec_args[argc + 1] = NULL;

    execv("/bin/zsh", exec_args);
    perror("execv");
    free(exec_args);
    return 1;
}
'''
    destination.write_text(source, encoding="utf-8")


def compile_c_launcher(*, source: Path, destination: Path) -> None:
    """Compile the tiny LaunchServices-friendly executable."""

    compiler = find_compiler()
    if compiler is None:
        raise RuntimeError("A C compiler is required to build the development .app.")
    subprocess.run(
        [compiler, "-Os", "-Wall", "-Wextra", "-o", str(destination), str(source)],
        check=True,
    )
    current_mode = destination.stat().st_mode
    destination.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def find_compiler() -> str | None:
    """Return an available local C compiler path."""

    for name in ("clang", "cc"):
        path = shutil.which(name)
        if path:
            return path
    try:
        result = subprocess.run(
            ["/usr/bin/xcrun", "-find", "clang"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    path = result.stdout.strip()
    return path or None


if __name__ == "__main__":
    raise SystemExit(main())
