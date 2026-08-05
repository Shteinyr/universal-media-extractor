# Commercial Block 4: Localhost Security Hardening

## Status

Completed.

GitHub issue: `#8 [P0] Harden localhost security`.

## Goal

Make the local FastAPI API safer for production desktop use while keeping the app local-only and avoiding auth/database/cookie storage.

The goal is not multi-user authentication. The app is still a single-user local desktop utility. The hardening added here protects the localhost API from accidental cross-origin browser access and from unbounded local upload behavior.

## Implemented Controls

### Random Session Token

`create_app()` now creates a random session token with `secrets.token_urlsafe(32)` unless a test explicitly supplies one.

The static UI fetches `/config`, stores the token in memory, and sends it on protected API calls using:

```text
X-UME-Session-Token
```

The token is not persisted to localStorage, files, or logs.

Public endpoints that do not require the token:

- `GET /`
- `GET /static/*`
- `GET /health`
- `GET /config`
- `OPTIONS` preflight requests

Protected endpoints include analysis, download, transcription, local file, Udemy, jobs, diagnostics, outputs, cancel, and delete operations.

### Strict Local Origin And Host Checks

The API now rejects non-local `Host` and `Origin` headers before route handling.

Allowed browser origins are limited to local HTTP origins such as:

- `http://127.0.0.1:<port>`
- `http://localhost:<port>`
- `http://[::1]:<port>`

Cross-origin requests from non-local websites are rejected with `403`.

FastAPI `CORSMiddleware` is configured with an explicit local origin regex, explicit methods, and explicit headers. It does not use wildcard origins.

### CSRF Risk Reduction

The app does not use cookies for API authorization. State-changing and sensitive local API operations require a custom session-token header.

A malicious external website cannot read `/config` due to CORS and cannot send the custom token header in a browser request unless it passes the local origin policy.

### Upload Size Limit

Local file upload now enforces `max_upload_bytes` with a default cap:

```text
2 GiB
```

Tests can override the cap via `create_app(max_upload_bytes=...)`.

If an upload exceeds the cap, the API returns `413` and removes the partial uploaded file.

### File Path Constraints

Existing path constraints remain active:

- uploaded local files are saved under the managed output folder using sanitized filenames;
- local transcription accepts only saved files inside the configured output base;
- output listing/detail/delete operate on managed output IDs, not arbitrary absolute paths;
- safe delete refuses path traversal and refuses deleting the outputs root.

User-selected output folders remain supported by design, but read/delete operations are constrained to the configured output base and managed output IDs.

### No Arbitrary CLI Arguments From Frontend

The frontend still cannot send arbitrary command-line arguments.

Backend request models expose controlled fields only:

- URL/source fields;
- selected internal `format_id`;
- bounded mode/output format values handled by service allowlists;
- transcription model/format fields handled by service-level command builders;
- Udemy quality/output options handled through predefined schema fields.

Subprocess calls continue to use list arguments and `shell=False`.

### Secret Redaction

Commercial Block 2 diagnostics redaction remains in place:

- cookies;
- tokens;
- authorization headers;
- passwords;
- bearer strings;
- local paths;
- transcripts;
- full URLs.

Block 4 adds no new credential storage and does not log the session token.

## Files Changed

- `src/universal_media_extractor/api/app.py`
- `src/universal_media_extractor/api/schemas.py`
- `src/universal_media_extractor/static/app.js`
- `tests/test_api_app.py`
- project documentation and memory files

## Verification

Targeted checks:

```bash
python3 -m py_compile src/universal_media_extractor/api/app.py src/universal_media_extractor/api/schemas.py tests/test_api_app.py
node --check src/universal_media_extractor/static/app.js
.venv/bin/python -m pytest tests/test_api_app.py -q
```

Full verification:

```bash
node --check src/universal_media_extractor/static/app.js
python3 -m py_compile src/universal_media_extractor/api/app.py src/universal_media_extractor/api/schemas.py tests/test_api_app.py
.venv/bin/python -m pytest -q
.venv/bin/python scripts/browser_smoke.py --base-url http://127.0.0.1:8766/ --proof-dir proof/commercial_block_4_security
```

Results:

- `117 passed` for the full pytest suite.
- Browser smoke completed successfully against the session-token UI.
- Screenshots saved under `proof/commercial_block_4_security/`.

## Not Included

- No user accounts.
- No database-backed sessions.
- No cloud auth.
- No persistent token storage.
- No payment/licensing work.
- No packaging/signing/store work.
- No roadmap changes.
