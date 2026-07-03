import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.services.local_file_metadata_service import (
    LocalFileMetadataService,
)


def test_local_file_metadata_service_uses_ffprobe(monkeypatch, tmp_path):
    input_file = tmp_path / "audio.wav"
    input_file.write_bytes(b"audio")
    output_dir = tmp_path / "output"
    (output_dir / "metadata").mkdir(parents=True)
    (output_dir / "logs").mkdir(parents=True)
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=json.dumps(
                {
                    "format": {
                        "duration": "2.5",
                        "format_name": "wav",
                        "format_long_name": "WAV / WAVE",
                    },
                    "streams": [
                        {
                            "index": 0,
                            "codec_type": "audio",
                            "codec_name": "pcm_s16le",
                            "duration": "2.5",
                            "sample_rate": "16000",
                            "channels": 1,
                        }
                    ],
                }
            ),
            stderr="",
        )

    monkeypatch.setattr(
        "universal_media_extractor.services.local_file_metadata_service.subprocess.run",
        fake_run,
    )

    result = LocalFileMetadataService().analyze_file(
        input_file,
        original_filename="audio.wav",
        output_dir=output_dir,
    )

    assert result.filename == "audio.wav"
    assert result.media_type == "audio"
    assert result.duration_seconds == 2.5
    assert result.streams[0].codec_name == "pcm_s16le"
    assert calls[0][0][0] == "ffprobe"
    assert calls[0][1]["shell"] is False
    assert (output_dir / "metadata" / "local_file_analysis.json").exists()


def test_local_file_metadata_service_handles_invalid_file(tmp_path):
    result = LocalFileMetadataService().analyze_file(
        tmp_path / "missing.wav",
        original_filename="missing.wav",
    )

    assert result.media_type == "unknown"
    assert result.errors[0].code == "invalid_input_file"
