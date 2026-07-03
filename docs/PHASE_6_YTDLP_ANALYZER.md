# Phase 6 yt-dlp Analyzer Wrapper

Date: 2026-05-29

## Scope

Phase 6 created a safe CLI analysis wrapper around `yt-dlp --simulate --dump-json`.

No FastAPI app, routes, frontend, downloader module, media download, Whisper run, MVP, Chrome extension, or desktop wrapper was created. Tests mock subprocess and do not call the network.

## Implemented

File: `src/universal_media_extractor/analyzers/ytdlp.py`

Public function:

```python
analyze_url_with_ytdlp(
    url: str,
    *,
    timeout_seconds: int = 60,
    raw_output_dir: Path | None = None,
) -> AnalyzeResult
```

Behavior:

- calls `yt-dlp` with list arguments only;
- uses `shell=False`;
- uses only `--simulate --dump-json`;
- captures stdout/stderr;
- applies timeout;
- parses stdout as JSON;
- optionally saves raw JSON only when `raw_output_dir` is provided;
- passes the raw dict to `normalize_ytdlp_info`;
- returns `AnalyzeResult`.

## Command Shape

The analyzer uses exactly this base command:

```bash
yt-dlp --simulate --dump-json URL
```

It does not use:

- `--format`;
- `-f`;
- `--no-simulate`;
- media download commands;
- Whisper;
- ffmpeg.

## Error Handling

The analyzer maps failures to `AnalyzeResult.errors` using `ErrorState`.

Handled cases:

- unsupported source -> `unsupported_source`;
- timeout -> `timeout`;
- network access failure -> `network_error`;
- login/private source -> `login_required`;
- cookies needed -> `cookies_required`;
- generic non-zero extractor failure -> `extractor_failed`;
- invalid JSON -> `invalid_output`;
- `yt-dlp` missing on PATH -> `ytdlp_not_found`.

The failed `AnalyzeResult` still includes:

- `source_url`;
- `source_type="url"`;
- `access_state`;
- `legal_safety`;
- `analyzed_at`;
- `errors`.

## Raw JSON Artifacts

Raw JSON is saved only when `raw_output_dir` is passed.

The analyzer does not store cookies, login data, tokens, or raw JSON inside `AnalyzeResult`. Successful results only reference saved raw output through `raw_reference_path`.

## Tests Added

File: `tests/test_ytdlp_analyzer.py`

Tests:

- successful mocked `yt-dlp --dump-json` returns `AnalyzeResult`;
- raw JSON saves into `raw_output_dir`;
- timeout becomes `ErrorState`;
- invalid JSON becomes `ErrorState`;
- non-zero yt-dlp exit becomes `ErrorState`;
- missing `yt-dlp` becomes `ErrorState`;
- command is analysis-only and uses `shell=False`.

## Verification

```bash
.venv/bin/python -m pytest -q
```

Result: 18 passed.

## Manual Script

Created:

```bash
scripts/manual_analyze_url.py
```

Manual usage when explicitly authorized:

```bash
.venv/bin/python scripts/manual_analyze_url.py "URL" --raw-output-dir proof/manual
```

The script was not run during Phase 6.

## Limitations

- No FastAPI route or app exists.
- No frontend exists.
- No downloader exists.
- No media download is performed.
- No Whisper/transcription path is implemented.
- Error classification is conservative and based on stderr text.
- Real network behavior is not tested in automated tests.

