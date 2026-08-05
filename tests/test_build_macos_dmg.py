import importlib.util
import plistlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_macos_dmg.py"


def load_build_dmg_module():
    spec = importlib.util.spec_from_file_location("build_macos_dmg_for_tests", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_fake_app_bundle(app_path: Path, module) -> None:
    contents = app_path / "Contents"
    (contents / "MacOS").mkdir(parents=True)
    (contents / "Resources").mkdir(parents=True)
    (contents / "MacOS" / "Universal Media Extractor").write_text("#!/bin/sh\n")
    plist = {
        "CFBundleIdentifier": module.BUNDLE_IDENTIFIER,
        "CFBundlePackageType": "APPL",
    }
    (contents / "Info.plist").write_bytes(plistlib.dumps(plist))


def test_build_macos_dmg_import_does_not_create_artifact(tmp_path):
    module = load_build_dmg_module()

    assert module.APP_NAME == "Universal Media Extractor.app"
    assert not (tmp_path / "Universal Media Extractor.dmg").exists()


def test_prepare_staging_copies_app_and_applications_symlink(tmp_path):
    module = load_build_dmg_module()
    app_path = tmp_path / module.APP_NAME
    make_fake_app_bundle(app_path, module)
    staging_dir = tmp_path / "staging"

    module.prepare_staging(app_path=app_path, staging_dir=staging_dir)

    assert (staging_dir / module.APP_NAME / "Contents" / "Info.plist").is_file()
    applications_link = staging_dir / "Applications"
    assert applications_link.is_symlink()
    assert applications_link.readlink() == Path("/Applications")


def test_hdiutil_create_command_uses_read_only_udzo():
    module = load_build_dmg_module()

    command = module.build_hdiutil_create_command(
        staging_dir=Path("staging"),
        dmg_path=Path("App.dmg"),
        volume_name="Universal Media Extractor",
    )

    assert command == [
        "hdiutil",
        "create",
        "-volname",
        "Universal Media Extractor",
        "-srcfolder",
        "staging",
        "-ov",
        "-format",
        "UDZO",
        "App.dmg",
    ]


def test_codesign_dmg_command_uses_developer_id_identity_and_identifier():
    module = load_build_dmg_module()

    command = module.build_codesign_dmg_command(
        dmg_path=Path("App.dmg"),
        identity="Developer ID Application: Example LLC (TEAM123456)",
    )

    assert command[:3] == ["codesign", "--force", "--timestamp"]
    assert "Developer ID Application: Example LLC (TEAM123456)" in command
    assert f"{module.BUNDLE_IDENTIFIER}.dmg" in command
    assert command[-1] == "App.dmg"


def test_stapler_and_spctl_dmg_commands():
    module = load_build_dmg_module()

    assert module.build_stapler_dmg_command(Path("App.dmg")) == ["xcrun", "stapler", "staple", "App.dmg"]
    assert module.build_spctl_dmg_assess_command(Path("App.dmg")) == [
        "spctl",
        "--assess",
        "--type",
        "open",
        "--verbose=4",
        "App.dmg",
    ]


def test_write_sha256_file(tmp_path):
    module = load_build_dmg_module()
    dmg_path = tmp_path / "App.dmg"
    dmg_path.write_bytes(b"hello")

    checksum_path = module.write_sha256_file(dmg_path)

    assert checksum_path == tmp_path / "App.dmg.sha256"
    assert checksum_path.read_text().endswith("  App.dmg\n")
    assert checksum_path.read_text().startswith("2cf24dba5fb0a30e")


def test_build_dmg_runs_hdiutil_without_shell(tmp_path, monkeypatch):
    module = load_build_dmg_module()
    app_path = tmp_path / module.APP_NAME
    make_fake_app_bundle(app_path, module)
    dmg_path = tmp_path / "out" / "App.dmg"
    staging_dir = tmp_path / "staging"
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        if command[:2] == ["hdiutil", "create"]:
            dmg_path.write_bytes(b"dmg")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    result = module.build_dmg(
        app_path=app_path,
        dmg_path=dmg_path,
        staging_dir=staging_dir,
        allow_non_macos=True,
    )

    assert result == dmg_path
    assert [call[0][0] for call in calls] == ["hdiutil", "hdiutil"]
    assert all("shell" not in kwargs for _, kwargs in calls)
    assert all(kwargs["check"] is True for _, kwargs in calls)


def test_build_dmg_dry_run_still_prepares_staging_without_subprocess(tmp_path, monkeypatch):
    module = load_build_dmg_module()
    app_path = tmp_path / module.APP_NAME
    make_fake_app_bundle(app_path, module)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))

    module.build_dmg(
        app_path=app_path,
        dmg_path=tmp_path / "App.dmg",
        staging_dir=tmp_path / "staging",
        allow_non_macos=True,
        dry_run=True,
    )

    assert (tmp_path / "staging" / module.APP_NAME).is_dir()
    assert calls == []


def test_validate_dmg_inputs_rejects_unexpected_bundle_identifier(tmp_path):
    module = load_build_dmg_module()
    app_path = tmp_path / module.APP_NAME
    make_fake_app_bundle(app_path, module)
    plist_path = app_path / "Contents" / "Info.plist"
    plist_path.write_bytes(plistlib.dumps({"CFBundleIdentifier": "bad.id"}))

    try:
        module.validate_dmg_inputs(app_path=app_path, allow_non_macos=True)
    except ValueError as exc:
        assert "bundle identifier" in str(exc)
    else:
        raise AssertionError("Expected unexpected bundle identifier to fail.")


def test_format_command_quotes_spaces():
    module = load_build_dmg_module()

    formatted = module.format_command(["hdiutil", "create", "Universal Media Extractor.dmg"])

    assert "'Universal Media Extractor.dmg'" in formatted
