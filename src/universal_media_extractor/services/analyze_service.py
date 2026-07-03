"""Business service for URL analysis."""

from __future__ import annotations

from pathlib import Path

from universal_media_extractor.analyzers.ytdlp import analyze_url_with_ytdlp
from universal_media_extractor.models import AnalyzeResult


class AnalyzeService:
    """Thin service wrapper around the safe yt-dlp analyzer."""

    def analyze_url(
        self, url: str, raw_output_dir: Path | None = None
    ) -> AnalyzeResult:
        """Analyze a URL without downloading media or invoking Whisper."""

        return analyze_url_with_ytdlp(url, raw_output_dir=raw_output_dir)
