import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS_SCRIPT = ROOT / "scripts" / "check_macos_signing_readiness.py"
SIGN_SCRIPT = ROOT / "scripts" / "sign_macos_app.py"
NOTARIZE_SCRIPT = ROOT / "scripts" / "notarize_macos_app.py"
STORE_CREDENTIALS_SCRIPT = ROOT / "scripts" / "store_macos_notary_credentials.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_developer_id_application_identities():
    module = load_module(READINESS_SCRIPT, "readiness_for_tests")
    output = '''
  1) ABC123 "Developer ID Application: Example LLC (TEAM123456)"
  2) DEF456 "Apple Development: Example"
     2 valid identities found
'''

    identities = module.parse_developer_id_application_identities(output)

    assert len(identities) == 1
    assert "Developer ID Application" in identities[0]


def test_readiness_run_command_never_uses_shell(monkeypatch):
    module = load_module(READINESS_SCRIPT, "readiness_shell_for_tests")
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, "/usr/bin/tool\n", "")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    module.run_command(["xcrun", "--find", "notarytool"])

    command, kwargs = calls[0]
    assert command == ["xcrun", "--find", "notarytool"]
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True
    assert kwargs["check"] is False
    assert "shell" not in kwargs


def test_codesign_command_enables_hardened_runtime_and_timestamp():
    module = load_module(SIGN_SCRIPT, "sign_for_tests")

    command = module.build_codesign_command(
        app_path=Path("App.app"),
        identity="Developer ID Application: Example LLC (TEAM123456)",
        entitlements_path=Path("entitlements.plist"),
    )

    assert command[:2] == ["codesign", "--force"]
    assert "--deep" in command
    assert command[command.index("--options") + 1] == "runtime"
    assert "--timestamp" in command
    assert "--entitlements" in command
    assert command[-1] == "App.app"


def test_codesign_verify_command_is_strict():
    module = load_module(SIGN_SCRIPT, "sign_verify_for_tests")

    command = module.build_codesign_verify_command(Path("App.app"))

    assert command == ["codesign", "--verify", "--deep", "--strict", "--verbose=2", "App.app"]


def test_notarization_archive_command_uses_ditto_keep_parent():
    module = load_module(NOTARIZE_SCRIPT, "notarize_archive_for_tests")

    command = module.build_archive_command(app_path=Path("App.app"), archive_path=Path("App.zip"))

    assert command == ["ditto", "-c", "-k", "--keepParent", "App.app", "App.zip"]


def test_store_credentials_command_does_not_include_password():
    module = load_module(NOTARIZE_SCRIPT, "notarize_credentials_for_tests")

    command = module.build_store_credentials_command(
        profile="UME_NOTARY",
        apple_id="alex@example.com",
        team_id="TEAM123456",
    )

    assert command == [
        "xcrun",
        "notarytool",
        "store-credentials",
        "UME_NOTARY",
        "--apple-id",
        "alex@example.com",
        "--team-id",
        "TEAM123456",
    ]
    assert "--password" not in command


def test_notary_submit_uses_keychain_profile_and_wait():
    module = load_module(NOTARIZE_SCRIPT, "notarize_submit_for_tests")

    command = module.build_notary_submit_command(
        archive_path=Path("App.zip"),
        keychain_profile="UME_NOTARY",
        timeout="30m",
    )

    assert command[:3] == ["xcrun", "notarytool", "submit"]
    assert "--keychain-profile" in command
    assert "UME_NOTARY" in command
    assert "--wait" in command
    assert "--output-format" in command
    assert "json" in command


def test_stapler_and_gatekeeper_commands():
    module = load_module(NOTARIZE_SCRIPT, "notarize_validate_for_tests")

    assert module.build_stapler_staple_command(Path("App.app")) == ["xcrun", "stapler", "staple", "App.app"]
    assert module.build_stapler_validate_command(Path("App.app")) == ["xcrun", "stapler", "validate", "App.app"]
    assert module.build_gatekeeper_assess_command(Path("App.app")) == [
        "spctl",
        "--assess",
        "--type",
        "execute",
        "--verbose=4",
        "App.app",
    ]


def test_format_command_quotes_spaces():
    module = load_module(SIGN_SCRIPT, "sign_format_for_tests")

    formatted = module.format_command(["codesign", "--sign", "Developer ID Application: Example", "App.app"])

    assert "'Developer ID Application: Example'" in formatted


def test_store_credentials_script_does_not_accept_password():
    module = load_module(STORE_CREDENTIALS_SCRIPT, "store_credentials_for_tests")

    command = module.build_store_credentials_command(
        profile="UME_NOTARY",
        apple_id="alex@example.com",
        team_id="TEAM123456",
    )

    assert command == [
        "xcrun",
        "notarytool",
        "store-credentials",
        "UME_NOTARY",
        "--apple-id",
        "alex@example.com",
        "--team-id",
        "TEAM123456",
    ]
    assert "--password" not in command
