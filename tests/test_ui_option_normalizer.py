import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
NORMALIZER_PATH = ROOT / "src" / "universal_media_extractor" / "static" / "option_normalizer.js"


def _run_node(script: str) -> None:
    if shutil.which("node") is None:
        pytest.skip("node is not available for static UI helper tests")
    completed = subprocess.run(
        ["node", "-e", script],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr


def test_video_options_are_deduplicated_for_user_facing_picker() -> None:
    script = f"""
      const assert = require("assert");
      const normalizer = require({json.dumps(str(NORMALIZER_PATH))});
      const result = {{
        media_options: {{
          combined: [
            {{ format_id: "95", type: "combined", ext: "mp4", height: 1080, resolution: "1920x1080" }},
            {{ format_id: "96", type: "combined", ext: "mp4", height: 1080, filesize_approx: 13935575 }},
            {{ format_id: "313", type: "video", ext: "webm", height: 2160, filesize_approx: 96075000 }}
          ],
          video: [
            {{ format_id: "137", type: "video", ext: "mp4", height: 1080, filesize_approx: 13935575 }},
            {{ format_id: "136", type: "video", ext: "mp4", height: 720, filesize_approx: 7000000 }},
            {{ format_id: "315", type: "video", ext: "webm", height: 2160 }}
          ],
          audio: []
        }},
        subtitles: [],
        automatic_captions: []
      }};
      const data = normalizer.buildFormatPickerData(result);
      assert.strictEqual(data.video.length, 2);
      assert.deepStrictEqual(data.video.map((option) => `${{option.ext}}:${{option.height}}`).sort(), [
        "mp4:1080",
        "webm:2160"
      ]);
      assert.strictEqual(data.video.find((option) => option.ext === "mp4").format_id, "96");
      assert.ok(data.video.every((option) => option.height >= 1080));
    """
    _run_node(script)


def test_subtitle_options_are_deduplicated_by_language_and_type() -> None:
    script = f"""
      const assert = require("assert");
      const normalizer = require({json.dumps(str(NORMALIZER_PATH))});
      const result = {{
        media_options: {{ audio: [], video: [], combined: [] }},
        subtitles: [
          {{ language: "en", type: "manual", formats: ["vtt", "srt"] }},
          {{ language: "EN", type: "manual", formats: ["json3", "vtt"] }}
        ],
        automatic_captions: [
          {{ language: "en", type: "automatic", formats: ["vtt"] }},
          {{ language: "en", type: "automatic", formats: ["srv1", "vtt"] }},
          {{ language: "ru", type: "automatic", formats: ["vtt"] }}
        ]
      }};
      const data = normalizer.buildFormatPickerData(result);
      assert.strictEqual(data.subtitles.length, 3);
      const manualEn = data.subtitles.find((option) => option.language === "en" && option.subtitle_type === "manual");
      const autoEn = data.subtitles.find((option) => option.language === "en" && option.subtitle_type === "automatic");
      const autoRu = data.subtitles.find((option) => option.language === "ru" && option.subtitle_type === "automatic");
      assert.deepStrictEqual(manualEn.formats, ["json3", "srt", "vtt"]);
      assert.deepStrictEqual(autoEn.formats, ["srv1", "vtt"]);
      assert.ok(autoRu);
      assert.strictEqual(manualEn.selection_id, "subtitles:manual:en");
      assert.strictEqual(autoEn.selection_id, "subtitles:automatic:en");
    """
    _run_node(script)



def test_presets_hide_technical_formats_and_keep_internal_ids() -> None:
    script = f"""
      const assert = require("assert");
      const normalizer = require({json.dumps(str(NORMALIZER_PATH))});
      const result = {{
        media_options: {{
          combined: [
            {{ format_id: "96", type: "combined", ext: "mp4", height: 1080, filesize_approx: 13935575 }},
            {{ format_id: "315", type: "video", ext: "webm", height: 2160, filesize_approx: 96075000 }}
          ],
          video: [
            {{ format_id: "137", type: "video", ext: "mp4", height: 1080, filesize_approx: 13935575 }}
          ],
          audio: [
            {{ format_id: "140", type: "audio", ext: "m4a", filesize_approx: 1226833, is_default_recommended: true }},
            {{ format_id: "251", type: "audio", ext: "webm", filesize_approx: 450000 }}
          ]
        }},
        subtitles: [{{ language: "en", type: "manual", formats: ["vtt", "srt"] }}],
        automatic_captions: []
      }};
      const data = normalizer.buildPresetPickerData(result);
      const labels = data.presets.map((preset) => preset.preset_label);
      assert.deepStrictEqual(labels, [
        "Best Video",
        "1080p",
        "Smaller Video",
        "Audio M4A",
        "Audio MP3",
        "Subtitles",
        "Archive Pack"
      ]);
      assert.ok(data.presets.every((preset) => !preset.preset_label.includes(preset.format_id || "__missing__")));
      assert.strictEqual(data.presets.find((preset) => preset.preset_id === "audio_m4a").format_id, "140");
      assert.strictEqual(data.presets.find((preset) => preset.preset_id === "audio_m4a").preset_output_format, "m4a");
      assert.strictEqual(data.presets.find((preset) => preset.preset_id === "audio_mp3").format_id, "140");
      assert.strictEqual(data.presets.find((preset) => preset.preset_id === "audio_mp3").preset_output_format, "mp3");
      assert.strictEqual(data.presets.find((preset) => preset.preset_id === "subtitles").format_id, "en");
      assert.strictEqual(data.presets.find((preset) => preset.preset_id === "archive_pack").preset_available, false);
    """
    _run_node(script)


def test_presets_mark_missing_options_unavailable() -> None:
    script = f"""
      const assert = require("assert");
      const normalizer = require({json.dumps(str(NORMALIZER_PATH))});
      const data = normalizer.buildPresetPickerData({{
        media_options: {{ audio: [], video: [], combined: [] }},
        subtitles: [],
        automatic_captions: []
      }});
      assert.strictEqual(data.presets.length, 7);
      assert.ok(data.presets.every((preset) => preset.preset_available === false));
      assert.strictEqual(data.presets.find((preset) => preset.preset_id === "subtitles").preset_description, "No subtitles found.");
    """
    _run_node(script)
