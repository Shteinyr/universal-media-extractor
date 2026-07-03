"""Safety and legal-confirmation helpers."""

from __future__ import annotations

from universal_media_extractor.models import LegalSafetyState
from universal_media_extractor.normalizers.ytdlp import RIGHTS_CONFIRMATION_TEXT


class SafetyService:
    """Centralize simple safety gates for protected operations."""

    def build_default_legal_state(self) -> LegalSafetyState:
        """Return the default legal/safety state for analyze results."""

        return LegalSafetyState(
            user_confirmed_rights=False,
            confirmation_text=RIGHTS_CONFIRMATION_TEXT,
            required_before_download=True,
            required_before_transcription=True,
            accepted_at=None,
        )

    def require_rights_confirmation(self, user_confirmed_rights: bool) -> bool:
        """Return True only when the user has confirmed rights."""

        return bool(user_confirmed_rights)
