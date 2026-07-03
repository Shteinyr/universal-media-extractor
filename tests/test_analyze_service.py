from datetime import datetime, timezone
from pathlib import Path

from universal_media_extractor.models import (
    AccessState,
    AnalyzeResult,
    LegalSafetyState,
)
from universal_media_extractor.services.analyze_service import AnalyzeService


def test_analyze_service_calls_analyzer(monkeypatch):
    expected = AnalyzeResult(
        analysis_id="youtube-test",
        source_url="https://example.test/video",
        source_type="url",
        extractor="test",
        access_state=AccessState(availability="public"),
        legal_safety=LegalSafetyState(
            confirmation_text="confirm",
            user_confirmed_rights=False,
        ),
        analyzed_at=datetime.now(timezone.utc),
    )
    calls = {}

    def fake_analyzer(url, *, raw_output_dir=None):
        calls["url"] = url
        calls["raw_output_dir"] = raw_output_dir
        return expected

    monkeypatch.setattr(
        "universal_media_extractor.services.analyze_service.analyze_url_with_ytdlp",
        fake_analyzer,
    )

    raw_output_dir = Path("proof/test")
    result = AnalyzeService().analyze_url(
        "https://example.test/video", raw_output_dir=raw_output_dir
    )

    assert result is expected
    assert calls == {
        "url": "https://example.test/video",
        "raw_output_dir": raw_output_dir,
    }
