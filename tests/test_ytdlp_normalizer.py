import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.models import AnalyzeResult
from universal_media_extractor.normalizers import normalize_ytdlp_info

RAW_PATH = ROOT / "proof" / "phase_2" / "url_analysis_raw.json"


def load_raw() -> dict:
    return json.loads(RAW_PATH.read_text())


def test_ytdlp_raw_json_normalizes_to_analyze_result() -> None:
    result = normalize_ytdlp_info(
        load_raw(), raw_reference_path="proof/phase_2/url_analysis_raw.json"
    )

    assert isinstance(result, AnalyzeResult)
    assert result.raw_reference_path == "proof/phase_2/url_analysis_raw.json"


def test_showreel_core_metadata_is_normalized() -> None:
    result = normalize_ytdlp_info(load_raw())

    assert result.title == "Showreel"
    assert result.duration_seconds == 39
    assert result.duration_label == "0:39"
    assert result.extractor == "youtube"
    assert result.extractor_key == "Youtube"
    assert result.source_type == "youtube"
    assert result.thumbnail_url


def test_media_options_are_grouped() -> None:
    result = normalize_ytdlp_info(load_raw())

    assert len(result.media_options.audio) == 3
    assert len(result.media_options.video) == 4
    assert len(result.media_options.combined) == 5
    assert result.media_options.recommended.best_audio_format_id == "140"
    assert result.media_options.recommended.best_video_format_id == "137"
    assert result.media_options.recommended.best_combined_format_id == "95"


def test_subtitles_and_automatic_captions_are_empty_for_showreel() -> None:
    result = normalize_ytdlp_info(load_raw())

    assert result.subtitles == []
    assert result.automatic_captions == []


def test_expected_warnings_are_present() -> None:
    result = normalize_ytdlp_info(load_raw())
    warning_codes = {warning.code for warning in result.warnings}

    assert "no_subtitles" in warning_codes
    assert "no_automatic_captions" in warning_codes
    assert "platform_terms_warning" in warning_codes
    assert "best_effort_extractor" in warning_codes
    assert "analysis_only_not_download_tested" in warning_codes


def test_normalized_result_exports_and_revalidates_as_json() -> None:
    result = normalize_ytdlp_info(load_raw())

    exported = result.model_dump_json()
    reparsed = AnalyzeResult.model_validate_json(exported)

    assert reparsed.title == "Showreel"
    assert len(reparsed.media_options.audio) == 3
    assert reparsed.legal_safety.user_confirmed_rights is False

