import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pydantic import ValidationError

from universal_media_extractor.models import BatchCreateRequest, BatchDownloadItemRequest


def test_batch_create_request_defaults_to_one_worker():
    request = BatchCreateRequest(
        items=[BatchDownloadItemRequest(source_url="https://example.com/video")],
        user_confirmed_rights=True,
    )

    assert request.preset == "best_video"
    assert request.concurrency == 1
    assert request.items[0].selected is True


def test_batch_request_limits_concurrency():
    try:
        BatchCreateRequest(
            items=[BatchDownloadItemRequest(source_url="https://example.com/video")],
            user_confirmed_rights=True,
            concurrency=10,
        )
    except ValidationError as exc:
        assert "concurrency" in str(exc)
    else:
        raise AssertionError("concurrency above the local limit should fail")


def test_batch_item_requires_http_url():
    try:
        BatchDownloadItemRequest(source_url="not-a-url")
    except ValidationError as exc:
        assert "source_url" in str(exc)
    else:
        raise AssertionError("invalid URL should fail validation")
