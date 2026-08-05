import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "notarize_macos_dmg.py"


def load_module():
    spec = importlib.util.spec_from_file_location("notarize_macos_dmg_for_tests", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["notarize_macos_dmg_for_tests"] = module
    spec.loader.exec_module(module)
    return module


def test_notary_submit_uses_dmg_keychain_profile_and_wait():
    module = load_module()

    command = module.build_notary_submit_command(
        dmg_path=Path("Universal Media Extractor.dmg"),
        keychain_profile="UME_NOTARY",
        timeout="45m",
    )

    assert command[:3] == ["xcrun", "notarytool", "submit"]
    assert "Universal Media Extractor.dmg" in command
    assert "--keychain-profile" in command
    assert "UME_NOTARY" in command
    assert "--wait" in command
    assert "--timeout" in command
    assert "45m" in command
    assert "--output-format" in command
    assert "json" in command


def test_dmg_stapler_and_gatekeeper_commands():
    module = load_module()

    assert module.build_stapler_staple_command(Path("App.dmg")) == ["xcrun", "stapler", "staple", "App.dmg"]
    assert module.build_stapler_validate_command(Path("App.dmg")) == ["xcrun", "stapler", "validate", "App.dmg"]
    assert module.build_gatekeeper_assess_command(Path("App.dmg")) == [
        "spctl",
        "--assess",
        "--type",
        "open",
        "--verbose=4",
        "App.dmg",
    ]


def test_main_dry_run_does_not_run_subprocess(monkeypatch, tmp_path):
    module = load_module()
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "notarize_macos_dmg.py",
            "--dmg-path",
            str(tmp_path / "App.dmg"),
            "--dry-run",
        ],
    )

    assert module.main() == 0
    assert calls == []


def test_main_runs_commands_without_shell(monkeypatch, tmp_path):
    module = load_module()
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "notarize_macos_dmg.py",
            "--dmg-path",
            str(tmp_path / "App.dmg"),
            "--keychain-profile",
            "UME_NOTARY",
        ],
    )

    assert module.main() == 0
    assert [call[0][0] for call in calls] == ["xcrun", "xcrun", "xcrun", "spctl"]
    assert all("shell" not in kwargs for _, kwargs in calls)
    assert all(kwargs["check"] is True for _, kwargs in calls)
