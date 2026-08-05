# Public Beta Security / Diagnostics / QA Review

Date: 2026-08-05

## Purpose

Sanity-check and tighten the current public beta readiness baseline without adding new product features, changing roadmap, or changing core API behavior.

Scope:

- localhost/session-token security sanity check;
- diagnostics UX/docs sanity check;
- known limitations and support copy alignment;
- UI/API error behavior sanity check;
- README beta run instructions;
- tests and browser smoke proof.

## Security Sanity Check

Confirmed existing local-only protections:

- backend is intended to bind to `127.0.0.1` through app launch scripts;
- protected API calls require `X-UME-Session-Token`;
- non-local `Host` headers are rejected;
- non-local `Origin` headers are rejected;
- CORS allows only local origins;
- uploads have an explicit size cap;
- static files and `/health` remain public-local, while API actions require the session token.

Tightened in this pass:

- `/config` now returns `Cache-Control: no-store` because it includes the in-memory session token;
- `/diagnostics/...` responses now also receive `Cache-Control: no-store`;
- added regression coverage for non-local Host rejection;
- added regression coverage for no-store behavior.

## Diagnostics UX Check

Existing diagnostics behavior remains redacted by default:

- no cookies;
- no tokens;
- no transcripts;
- no full URLs;
- no local paths.

Tightened in this pass:

- failed/cancelled background job cards now expose a small `Copy diagnostics` support action;
- the action uses the existing `GET /diagnostics/jobs/{job_id}` endpoint;
- copied diagnostics are redacted JSON and are never sent to a cloud service by the app;
- diagnostics endpoint no-store behavior is tested.

## Error Behavior Check

Confirmed and preserved:

- analyzer errors remain represented as `AnalyzeResult.errors`;
- failed jobs keep normalized `ErrorState` details;
- primary UI error labels remain user-facing;
- technical details remain available behind disclosure/details where applicable;
- source support remains best-effort and no DRM/CAPTCHA/paywall/login bypass is promised.

## Docs / Support Alignment

Updated project memory and docs to record the public beta readiness checks. Known limitations now clarify that security and diagnostics have local sanity coverage, but still need external beta validation before paid public release.

## Proof / Verification

Commands:

```bash
node --check src/universal_media_extractor/static/app.js
.venv/bin/python -m pytest tests/test_api_app.py::test_config_endpoint_defaults_to_internal_course_mode tests/test_api_app.py::test_non_local_host_is_rejected_even_with_token tests/test_api_app.py::test_static_javascript_is_available tests/test_api_app.py::test_diagnostics_endpoint_returns_redacted_job_bundle -q
.venv/bin/python -m pytest -q
.venv/bin/python scripts/browser_smoke.py --base-url http://127.0.0.1:8011/ --proof-dir proof/public_beta_security_diagnostics_qa
```

Expected final full test result:

```text
196 passed
```

## Not Changed

- No checkout/licensing.
- No installer/signing.
- No Chrome extension.
- No AI summary.
- No React/Vite/CDN.
- No roadmap changes.
- No new media processing feature.

## Remaining Risk

- This is a local sanity check, not a full external penetration test.
- Browser smoke remains smoke-level, not exhaustive visual regression.
- Public beta should still validate diagnostics/support flows with real failed user jobs.
