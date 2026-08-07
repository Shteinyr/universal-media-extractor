# Public Beta Result And Local Transcription UX Final Pass

Date: 2026-08-07

GitHub issue: [#50 Result and local transcription UX final pass](https://github.com/Shteinyr/universal-media-extractor/issues/50)

## Summary

This pass makes saved results and local transcription feel like a clean product action instead of a technical subprocess panel.

No AI summary API, transcription editor/workbench, new roadmap block, checkout, installer work, or backend architecture rewrite was added.

## Result Card

Saved result UI now shows user-facing file information:

- actual filename;
- container/extension;
- file size when the backend can stat the saved file;
- output location;
- selected transcript file.

The backend now includes `downloaded_file_details` in `DownloadResult` so the UI does not need to guess filename/container/size from raw paths when metadata is available.

## Transcription UX

The transcription action is now labeled as `Transcribe locally`.

Transcription controls are shown/enabled only when the selected output or local file can be transcribed:

- URL flow: audio, video, and combined media outputs can open transcription.
- Subtitle-only outputs do not open transcription.
- Local file flow: only analyzed `audio` or `video` files enable local transcription; `unknown` media stays disabled.

Whisper model copy now explains the tradeoff:

- smaller models are faster but rougher;
- larger models can take more time and disk space;
- larger models usually improve quality.

## Transcript Output

The app still saves one selected transcript format per transcription run:

- TXT;
- Markdown;
- JSON.

Only implemented transcript formats are shown. SRT/VTT/editor formats are not exposed.

`TranscriptionResult` now records:

- `transcript_format`;
- `transcript_file_text`.

The `Copy` action copies the selected transcript output content when available. The button label reflects the selected output format, for example `Copy TXT`.

Transcript preview remains readable by using the plain transcript text even when the selected output file is Markdown or JSON.

## Data Safety

Transcription failure does not modify or delete the saved media file. Tests cover failed transcription preserving the input media bytes.

Cancelled transcription may clean only safe temporary work files, not user-visible completed media.

## Verification

Commands run:

```bash
node --check src/universal_media_extractor/static/app.js
python3 -m py_compile scripts/browser_smoke.py src/universal_media_extractor/models/download.py src/universal_media_extractor/models/transcript.py src/universal_media_extractor/services/download_service.py src/universal_media_extractor/services/transcription_service.py
.venv/bin/python -m pytest tests/test_download_service.py tests/test_transcription_service.py tests/test_api_app.py -q
.venv/bin/python -m pytest -q
env UME_PUBLIC_PRODUCT_MODE=1 .venv/bin/python scripts/run_api.py
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/result_transcription_ux_final_pass --full-flow
```

Results:

- JS syntax check passed.
- Python compile checks passed.
- Focused tests passed: `78 passed`.
- Full pytest passed outside sandbox: `231 passed`.
- Browser full-flow smoke passed in public product mode.

## Proof

Screenshots:

- `proof/result_transcription_ux_final_pass/ui_initial.png`
- `proof/result_transcription_ux_final_pass/ui_invalid_url.png`
- `proof/result_transcription_ux_final_pass/ui_analyze_result.png`
- `proof/result_transcription_ux_final_pass/ui_output_selected.png`
- `proof/result_transcription_ux_final_pass/ui_download_result.png`
- `proof/result_transcription_ux_final_pass/ui_transcribe_result.png`
- `proof/result_transcription_ux_final_pass/ui_library.png`

## Not Implemented

- AI summary API.
- Transcript editor/workbench.
- Multi-format transcript export in one run.
- New transcription models beyond existing Whisper CLI model names.
- Remote telemetry or cloud processing.
