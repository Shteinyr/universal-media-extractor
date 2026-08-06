# Public Beta QA Round

Date: 2026-08-06
Base commit tested: `71321cb`
Status: passed with notes.

## Purpose

Public beta readiness QA pass for the current local product. This was a quality block, not a feature block.

No roadmap changes, checkout/licensing, installer/signing, Chrome extension, AI summary, React/Vite/CDN, or broad redesign were added.

## Environment

Working directory:

```text
/Users/aleksandr/Developer/Codex/Projects/Universal Media Extractor
```

Local backend:

```text
http://127.0.0.1:8000/
```

Test source:

```text
https://youtu.be/UUdxAp3kuKA
```

Local file source: synthetic 1-second sine-wave WAV generated with `ffmpeg` under `proof/public_beta_qa_round/`.

## Automated Checks

| Check | Result |
| --- | --- |
| `node --check src/universal_media_extractor/static/app.js` | pass |
| `.venv/bin/python -m pytest -q` | pass, `196 passed` |
| `scripts/browser_smoke.py --proof-dir proof/public_beta_qa_round` | pass |

## Flow Results

| Flow | Result | Evidence |
| --- | --- | --- |
| App launch in browser mode | pass | `ui_initial.png` |
| `/health`, `/config`, static UI | pass | `config_redacted.json`, browser smoke |
| Protected API requires session token | pass | QA script assertion |
| Static JS no-store header | pass | QA script assertion |
| URL analyze on user-owned YouTube test URL | pass | `url_analyze_response.json` |
| URL audio download | pass | `audio_download_job_final.json` |
| URL audio transcription | pass | `audio_transcribe_job_final.json` |
| URL video download | pass | `video_download_job_final.json` |
| Local synthetic audio analyze | pass | `local_analyze_response.json` |
| Local synthetic audio transcribe | pass | `local_transcribe_job_final.json` |
| Batch import/list with one safe URL | pass | `batch_import_response.json` |
| Batch single-item audio download | pass | `batch_job_final.json` |
| Failed-job diagnostics endpoint | pass | `diagnostics_response.json` |
| Diagnostics redaction | pass | QA script assertion |
| Output index and safe delete | pass | `outputs_before_delete.json`, `dummy_delete_response.json`, `outputs_after_delete.json` |
| Public mode hides Course mode | pass | `tests/test_api_app.py::test_config_endpoint_hides_course_mode_in_public_product_mode` |

## UI Review

Checked through browser smoke and current static UI assertions:

- initial state loads;
- URL mode is available;
- output presets are visible after analysis;
- result card renders analyzed source;
- browser screenshots are saved;
- internal Course mode remains hidden in public product mode by tested `/config` behavior;
- no new misleading public copy was introduced in this block.

Manual visual areas still worth validating with real beta users:

- Batch mode with longer user-provided lists;
- narrow-window layout;
- failed download/transcription copy in real-world platform failures;
- final screenshots for public website after UI finalization.

## Bugs / Risks Found

No product blocker or runtime regression was found during this QA round.

Two temporary QA proof-script expectations were corrected while running the checks:

- HTTP headers can arrive lowercased through Python's response mapping;
- `/outputs` returns an `outputs` array and safe delete returns `status: deleted`.

These were proof-script issues, not product bugs.

## Proof Artifacts

Primary proof directory:

```text
proof/public_beta_qa_round/
```

Key artifacts:

- `ui_initial.png`
- `ui_analyze_result.png`
- `qa_summary.json`
- `url_analyze_response.json`
- `audio_download_job_final.json`
- `audio_transcribe_job_final.json`
- `video_download_job_final.json`
- `local_analyze_response.json`
- `local_transcribe_job_final.json`
- `batch_job_final.json`
- `diagnostics_response.json`
- `dummy_delete_response.json`

## Not In This Block

- No new product feature.
- No checkout/licensing.
- No installer/signing.
- No Chrome extension.
- No AI summary.
- No React/Vite/CDN.
- No roadmap change.
- No mass download.
- No DRM/login/paywall/protected-source success testing.

## Remaining Follow-Up

Recommended next work:

1. Public Beta UI / UX Finalization, using this QA pass as the baseline.
2. macOS signed release unblock after Apple Developer Program access.
3. Windows Production Foundation if cross-platform packaging should move in parallel.
4. Archive Pack remains planned but was not part of this QA pass.
