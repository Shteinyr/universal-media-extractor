import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.error_mapping import normalize_cli_error


def assert_error(text, code):
    error = normalize_cli_error(text, engine="yt-dlp")
    assert error.code == code
    assert error.message
    return error


def test_error_mapping_drm():
    error = assert_error("ERROR: This video is DRM protected", "drm_protected")
    assert error.recoverable is False


def test_error_mapping_login_and_cookies():
    assert_error("Please sign in to confirm your age", "login_required")
    assert_error("HTTP Error 403 Forbidden; cookies required", "cookies_required")


def test_error_mapping_region_private_deleted_and_no_format():
    assert_error("This video is not available in your country", "region_restricted")
    assert_error("HTTP Error 404: Not Found", "private_or_deleted")
    assert_error("requested format is not available", "no_requested_format")


def test_error_mapping_network_disk_permission_engine_outdated():
    assert_error("Unable to download webpage: timed out", "network_error")
    assert_error("No space left on device", "disk_full")
    assert_error("Permission denied: /Users/aleksandr/Downloads", "permission_denied")
    assert_error("WARNING: Your yt-dlp version is older than 90 days", "engine_outdated")
