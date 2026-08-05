import importlib.util
import plistlib
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_macos_app.py"
SPEC_PATH = ROOT / "packaging" / "macos" / "universal_media_extractor_macos.spec"


def load_build_macos_app_module():
    spec = importlib.util.spec_from_file_location("build_macos_app_for_tests", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_minimal_project(root: Path, spec_path: Path | None = None) -> Path:
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "run_desktop.py").write_text("print('desktop')\n")
    static_dir = root / "src" / "universal_media_extractor" / "static"
    static_dir.mkdir(parents=True)
    (static_dir / "index.html").write_text("<html></html>\n")
    if spec_path is None:
        spec_path = root / "packaging" / "macos" / "universal_media_extractor_macos.spec"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text("# spec\n")
    return spec_path


def make_fake_app_bundle(app_path: Path, module) -> None:
    contents = app_path / "Contents"
    (contents / "MacOS").mkdir(parents=True)
    (contents / "Resources").mkdir(parents=True)
    static_dir = contents / "Frameworks" / "universal_media_extractor" / "static"
    static_dir.mkdir(parents=True)
    (contents / "MacOS" / "Universal Media Extractor").write_text("#!/bin/sh\n")
    (static_dir / "index.html").write_text("<html></html>\n")
    plist = {
        "CFBundleIdentifier": module.BUNDLE_IDENTIFIER,
        "CFBundlePackageType": "APPL",
    }
    (contents / "Info.plist").write_bytes(plistlib.dumps(plist))


def test_build_macos_app_import_does_not_create_bundle(tmp_path):
    module = load_build_macos_app_module()

    assert module.APP_NAME == "Universal Media Extractor.app"
    assert not (tmp_path / module.APP_NAME).exists()


def test_build_pyinstaller_command_uses_list_args():
    module = load_build_macos_app_module()

    command = module.build_pyinstaller_command(
        spec_path=Path("app.spec"),
        dist_dir=Path("dist"),
        work_dir=Path("work"),
        clean=True,
    )

    assert command[:3] == [sys.executable, "-m", "PyInstaller"]
    assert "--noconfirm" in command
    assert "--clean" in command
    assert all(isinstance(part, str) for part in command)


def test_validate_build_inputs_rejects_missing_entrypoint(tmp_path, monkeypatch):
    module = load_build_macos_app_module()
    spec_path = tmp_path / "packaging" / "macos" / "app.spec"
    spec_path.parent.mkdir(parents=True)
    spec_path.write_text("# spec\n")
    monkeypatch.setattr(module, "pyinstaller_version", lambda: "6.21.0")

    with pytest.raises(FileNotFoundError, match="run_desktop.py"):
        module.validate_build_inputs(
            project_root=tmp_path,
            spec_path=spec_path,
            allow_non_macos=True,
        )


def test_validate_app_bundle_accepts_expected_structure(tmp_path):
    module = load_build_macos_app_module()
    app_path = tmp_path / module.APP_NAME
    make_fake_app_bundle(app_path, module)

    module.validate_app_bundle(app_path)


def test_build_macos_app_runs_pyinstaller_without_shell(tmp_path, monkeypatch):
    module = load_build_macos_app_module()
    project_root = tmp_path / "project"
    spec_path = make_minimal_project(project_root)
    dist_dir = tmp_path / "dist"
    work_dir = tmp_path / "work"
    calls = []

    monkeypatch.setattr(module, "pyinstaller_version", lambda: "6.21.0")

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        make_fake_app_bundle(dist_dir / module.APP_NAME, module)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    app_path = module.build_macos_app(
        project_root=project_root,
        spec_path=spec_path,
        dist_dir=dist_dir,
        work_dir=work_dir,
        allow_non_macos=True,
    )

    assert app_path == dist_dir / module.APP_NAME
    assert calls
    command, kwargs = calls[0]
    assert command[:3] == [sys.executable, "-m", "PyInstaller"]
    assert str(spec_path) in command
    assert kwargs["cwd"] == project_root
    assert kwargs["check"] is True
    assert kwargs["env"]["PYINSTALLER_CONFIG_DIR"] == str(work_dir.parent / "pyinstaller-config")
    assert "shell" not in kwargs


def test_ad_hoc_codesign_uses_list_args(monkeypatch, tmp_path):
    module = load_build_macos_app_module()
    calls = []
    monkeypatch.setattr(module.shutil, "which", lambda name: "/usr/bin/codesign")
    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda command, **kwargs: calls.append((command, kwargs)) or subprocess.CompletedProcess(command, 0),
    )

    module.ad_hoc_codesign(tmp_path / module.APP_NAME)

    command, kwargs = calls[0]
    assert command[:4] == ["/usr/bin/codesign", "--force", "--deep", "--sign"]
    assert "shell" not in kwargs
    assert kwargs["check"] is True


def test_macos_spec_declares_app_bundle_and_static_assets():
    text = SPEC_PATH.read_text()

    assert "BUNDLE(" in text
    assert "universal_media_extractor/static" in text
    assert "com.shteinyr.universal-media-extractor" in text
