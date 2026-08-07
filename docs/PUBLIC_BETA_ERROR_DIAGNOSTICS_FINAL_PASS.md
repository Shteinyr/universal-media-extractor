# Public Beta Error Diagnostics Final Pass

Date: 2026-08-07

GitHub issue: [#49 Error normalization and diagnostics final pass](https://github.com/Shteinyr/universal-media-extractor/issues/49)

## Summary

This pass completes the public-beta error and diagnostics hardening layer. It keeps raw CLI output available only as technical details, expands regression coverage for planned public error categories, and verifies that copied diagnostics contain useful environment context while redacting sensitive user data.

No new product features, endpoints, telemetry, upload behavior, checkout, installer work, roadmap changes, or UI redesign were added.

## Covered Error Categories

The shared CLI error normalizer now has explicit tests for:

- `drm_protected`
- `login_required`
- `cookies_required`
- `region_restricted`
- `private_or_deleted`
- `no_requested_format`
- `network_error`
- `disk_full`
- `permission_denied`
- `engine_outdated`

Protected/access-required categories do not suggest bypassing DRM, sign-in, cookies, paywalls, or platform restrictions.

## UI Behavior

The static UI maps normalized error codes to short user-facing messages and keeps raw technical output behind `Technical details`.

The browser smoke script now captures an invalid URL state before running the normal analysis proof. This verifies that invalid user input is visible in the UI without making an API request.

## Diagnostics Behavior

Diagnostics bundles identify:

- app version;
- OS name/version/architecture;
- Python version;
- local media engine versions;
- normalized error;
- redacted job payload/result summary;
- redacted logs.

Diagnostics redaction removes:

- cookies;
- tokens;
- authorization headers;
- transcript text;
- summary prompt text;
- full URLs;
- local macOS paths;
- local Windows paths.

Diagnostics remain local-only. The app does not upload diagnostics automatically.

## Proof

Browser screenshots:

- `proof/error_diagnostics_final_pass/ui_initial.png`
- `proof/error_diagnostics_final_pass/ui_invalid_url.png`
- `proof/error_diagnostics_final_pass/ui_analyze_result.png`
- `proof/error_diagnostics_final_pass/ui_output_selected.png`
- `proof/error_diagnostics_final_pass/ui_library.png`

## Verification

Commands run:

```bash
node --check src/universal_media_extractor/static/app.js
python3 -m py_compile scripts/browser_smoke.py
.venv/bin/python -m pytest tests/test_error_mapping.py tests/test_diagnostics_service.py tests/test_api_app.py -q
.venv/bin/python -m pytest -q
env UME_PUBLIC_PRODUCT_MODE=1 .venv/bin/python scripts/run_api.py
.venv/bin/python scripts/browser_smoke.py --proof-dir proof/error_diagnostics_final_pass
```

Results:

- JS syntax check passed.
- Browser smoke script compile check passed.
- Focused tests passed: `72 passed`.
- Full pytest passed outside sandbox: `230 passed`.
- Browser smoke passed and created screenshots.

## Not Implemented

- Remote telemetry.
- Automatic diagnostics upload.
- New error-reporting backend service.
- New product flow.
- New roadmap block.
