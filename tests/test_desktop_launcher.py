import importlib.util
import socket
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_desktop.py"


def load_run_desktop_module():
    spec = importlib.util.spec_from_file_location("run_desktop_for_tests", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_run_desktop_import_does_not_start_gui():
    module = load_run_desktop_module()

    assert module.WINDOW_TITLE == "Universal Media Extractor"
    assert callable(module.find_available_port)
    assert callable(module.start_backend)


def test_find_available_port_skips_busy_port():
    module = load_run_desktop_module()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        busy_port = sock.getsockname()[1]

        available = module.find_available_port(
            host="127.0.0.1",
            preferred_port=busy_port,
            max_port=busy_port + 2,
        )

    assert available > busy_port


def test_find_available_port_rejects_invalid_range():
    module = load_run_desktop_module()

    try:
        module.find_available_port(preferred_port=9001, max_port=9000)
    except ValueError as exc:
        assert "preferred_port" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid port range.")
