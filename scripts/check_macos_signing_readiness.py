#!/usr/bin/env python3
"""Check local readiness for Developer ID signing and notarization."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP_PATH = ROOT / "build" / "macos" / "dist" / "Universal Media Extractor.app"
DEFAULT_ENTITLEMENTS = ROOT / "packaging" / "macos" / "entitlements.plist"


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str

    def as_dict(self) -> dict[str, object]:
        return {"name": self.name, "ok": self.ok, "detail": self.detail}


def main() -> int:
    args = parse_args()
    results = run_readiness_checks(
        app_path=args.app_path,
        entitlements_path=args.entitlements,
    )
    payload = {
        "ready": all(result.ok for result in results),
        "checks": [result.as_dict() for result in results],
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for result in results:
            status = "ok" if result.ok else "missing"
            print(f"[{status}] {result.name}: {result.detail}")
        print(f"ready: {str(payload['ready']).lower()}")
    return 0 if payload["ready"] else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check macOS signing/notarization readiness.")
    parser.add_argument("--app-path", type=Path, default=DEFAULT_APP_PATH)
    parser.add_argument("--entitlements", type=Path, default=DEFAULT_ENTITLEMENTS)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser.parse_args()


def run_readiness_checks(*, app_path: Path, entitlements_path: Path) -> list[CheckResult]:
    return [
        check_macos(),
        check_architecture(),
        check_tool("codesign", "codesign command"),
        check_xcrun_tool("notarytool"),
        check_xcrun_tool("stapler"),
        check_tool("spctl", "Gatekeeper assessment command"),
        check_xcode_select(),
        check_developer_id_identity(),
        check_path(app_path, "app bundle"),
        check_path(entitlements_path, "entitlements file"),
    ]


def check_macos() -> CheckResult:
    return CheckResult("macOS host", sys.platform == "darwin", sys.platform)


def check_architecture() -> CheckResult:
    machine = platform.machine()
    return CheckResult("Apple Silicon arm64 host", machine == "arm64", machine)


def check_tool(tool: str, label: str) -> CheckResult:
    path = shutil.which(tool)
    return CheckResult(label, path is not None, path or f"{tool} not found")


def check_xcrun_tool(tool: str) -> CheckResult:
    result = run_command(["xcrun", "--find", tool])
    detail = result.stdout.strip() or result.stderr.strip() or f"xcrun could not find {tool}"
    return CheckResult(f"xcrun {tool}", result.returncode == 0, detail)


def check_xcode_select() -> CheckResult:
    result = run_command(["xcode-select", "-p"])
    detail = result.stdout.strip() or result.stderr.strip() or "xcode-select path unavailable"
    return CheckResult("active Xcode command line tools", result.returncode == 0, detail)


def check_developer_id_identity() -> CheckResult:
    result = run_command(["security", "find-identity", "-v", "-p", "codesigning"])
    output = f"{result.stdout}\n{result.stderr}"
    identities = parse_developer_id_application_identities(output)
    if identities:
        return CheckResult("Developer ID Application identity", True, f"{len(identities)} found")
    return CheckResult(
        "Developer ID Application identity",
        False,
        "No Developer ID Application certificate found in available keychains.",
    )


def check_path(path: Path, label: str) -> CheckResult:
    exists = path.exists()
    return CheckResult(label, exists, str(path) if exists else f"missing: {path}")


def parse_developer_id_application_identities(output: str) -> list[str]:
    return [
        line.strip()
        for line in output.splitlines()
        if "Developer ID Application:" in line
    ]


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, capture_output=True, text=True, check=False)
    except OSError as exc:
        return subprocess.CompletedProcess(command, 127, "", str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
