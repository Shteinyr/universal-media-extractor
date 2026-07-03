import importlib.util
import plistlib
import stat
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_dev_app.py"


def load_build_dev_app_module():
    spec = importlib.util.spec_from_file_location("build_dev_app_for_tests", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_dev_app_import_does_not_create_bundle(tmp_path):
    module = load_build_dev_app_module()

    assert module.APP_NAME == "Universal Media Extractor Dev.app"
    assert not (tmp_path / module.APP_NAME).exists()


def test_build_dev_app_creates_minimal_bundle(tmp_path):
    module = load_build_dev_app_module()
    if module.find_compiler() is None:
        pytest.skip("A local C compiler is required to build the dev .app.")

    project_root = tmp_path / "project"
    (project_root / "scripts").mkdir(parents=True)
    (project_root / "scripts" / "run_desktop.py").write_text("print('desktop')\n")
    output_dir = tmp_path / "build" / "dev"

    app_path = module.build_dev_app(project_root=project_root, output_dir=output_dir)

    assert app_path == output_dir / "Universal Media Extractor Dev.app"
    plist_path = app_path / "Contents" / "Info.plist"
    launcher_path = app_path / "Contents" / "MacOS" / "UniversalMediaExtractorDev"
    shell_launcher_path = app_path / "Contents" / "Resources" / "launcher.zsh"
    c_source_path = app_path / "Contents" / "Resources" / "launcher.c"
    assert plist_path.is_file()
    assert launcher_path.is_file()
    assert shell_launcher_path.is_file()
    assert c_source_path.is_file()
    assert launcher_path.stat().st_mode & stat.S_IXUSR

    plist = plistlib.loads(plist_path.read_bytes())
    assert plist["CFBundleExecutable"] == "UniversalMediaExtractorDev"
    assert plist["CFBundlePackageType"] == "APPL"
    assert plist["CFBundleDisplayName"] == "Universal Media Extractor Dev"

    launcher = shell_launcher_path.read_text()
    assert str(project_root) in launcher
    assert ".venv/bin/python" in launcher
    assert "scripts/run_desktop.py" in launcher
    assert "exec \"$PYTHON\" \"$DESKTOP_SCRIPT\" \"$@\"" in launcher

    c_source = c_source_path.read_text()
    assert "Resources/launcher.zsh" in c_source
    assert "execv(\"/bin/zsh\"" in c_source


def test_build_dev_app_rejects_missing_desktop_launcher(tmp_path):
    module = load_build_dev_app_module()
    project_root = tmp_path / "project"
    project_root.mkdir()

    try:
        module.build_dev_app(project_root=project_root, output_dir=tmp_path / "out")
    except FileNotFoundError as exc:
        assert "run_desktop.py" in str(exc)
    else:
        raise AssertionError("Expected missing run_desktop.py to fail.")
