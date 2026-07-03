import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.models import AnalyzeResult

SAMPLE_PATH = ROOT / "docs" / "PHASE_3_SAMPLE_ANALYZE_RESULT.json"


def load_sample() -> dict:
    return json.loads(SAMPLE_PATH.read_text())


def test_phase_3_sample_validates_as_analyze_result() -> None:
    result = AnalyzeResult.model_validate(load_sample())

    assert result.title == "Showreel"
    assert result.source_type == "youtube"
    assert result.extractor == "youtube"
    assert result.duration_seconds == 39
    assert result.raw_reference_path == "proof/phase_2/url_analysis_raw.json"


def test_media_option_groups_validate_without_shape_loss() -> None:
    result = AnalyzeResult.model_validate(load_sample())

    assert len(result.media_options.audio) == 3
    assert len(result.media_options.video) == 4
    assert len(result.media_options.combined) == 5
    assert result.media_options.audio[1].format_id == "140"
    assert result.media_options.video[-1].resolution == "1920x1080"
    assert result.media_options.combined[3].warnings == ["format_size_unknown"]


def test_empty_subtitles_and_automatic_captions_are_valid() -> None:
    result = AnalyzeResult.model_validate(load_sample())

    assert result.subtitles == []
    assert result.automatic_captions == []


def test_warnings_validate_with_expected_codes() -> None:
    result = AnalyzeResult.model_validate(load_sample())
    warning_codes = {warning.code for warning in result.warnings}

    assert "no_subtitles" in warning_codes
    assert "no_automatic_captions" in warning_codes
    assert "platform_terms_warning" in warning_codes
    assert "best_effort_extractor" in warning_codes


def test_analyze_result_exports_back_to_json() -> None:
    result = AnalyzeResult.model_validate(load_sample())

    exported = result.model_dump_json()
    reparsed = AnalyzeResult.model_validate_json(exported)

    assert reparsed.analysis_id == result.analysis_id
    assert len(reparsed.media_options.audio) == 3
    assert reparsed.legal_safety.required_before_download is True
    assert reparsed.legal_safety.user_confirmed_rights is False
