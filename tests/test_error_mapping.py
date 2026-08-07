import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.error_mapping import normalize_cli_error


def assert_error(text, code):
    error = normalize_cli_error(text, engine="yt-dlp")
    assert error.code == code
    assert error.message
    return error


ERROR_FIXTURES = [
    ("drm_protected", "ERROR: This video is DRM protected"),
    ("login_required", "Please sign in to confirm your age"),
    ("cookies_required", "HTTP Error 403 Forbidden; cookies required"),
    ("region_restricted", "This video is not available in your country"),
    ("private_or_deleted", "HTTP Error 404: Not Found"),
    ("private_or_deleted", "This video is unavailable"),
    ("no_requested_format", "requested format is not available"),
    ("network_error", "Unable to download webpage: timed out"),
    ("disk_full", "No space left on device"),
    ("permission_denied", "Permission denied: /Users/aleksandr/Downloads"),
    ("engine_outdated", "WARNING: Your yt-dlp version is older than 90 days"),
]


@pytest.mark.parametrize(("code", "text"), ERROR_FIXTURES)
def test_error_mapping_planned_public_beta_categories(code, text):
    error = assert_error(text, code)

    assert error.technical_details


def test_error_mapping_protected_and_access_errors_never_suggest_bypass():
    protected_codes = {"drm_protected", "login_required", "cookies_required"}

    for expected_code, text in ERROR_FIXTURES:
        error = normalize_cli_error(text, engine="yt-dlp")
        if expected_code not in protected_codes:
            continue
        action = (error.suggested_user_action or "").lower()
        assert error.code == expected_code
        assert "bypass" not in action.replace("does not bypass", "")
        assert "circumvent" not in action
        assert "crack" not in action


def test_error_mapping_drm_is_not_recoverable():
    error = assert_error("ERROR: This video is DRM protected", "drm_protected")
    assert error.recoverable is False


def test_error_mapping_keeps_tail_of_long_stderr():
    long_stderr = "warning\n" * 500 + "ERROR: requested format is not available"

    error = normalize_cli_error(long_stderr, engine="yt-dlp")

    assert error.code == "no_requested_format"
    assert "requested format is not available" in error.technical_details
