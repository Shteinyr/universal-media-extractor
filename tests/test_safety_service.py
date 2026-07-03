from universal_media_extractor.services.safety_service import SafetyService


def test_safety_service_builds_default_legal_state():
    legal_state = SafetyService().build_default_legal_state()

    assert legal_state.user_confirmed_rights is False
    assert legal_state.required_before_download is True
    assert legal_state.required_before_transcription is True
    assert "rights" in legal_state.confirmation_text.lower()


def test_safety_service_requires_rights_confirmation():
    service = SafetyService()

    assert service.require_rights_confirmation(True) is True
    assert service.require_rights_confirmation(False) is False
