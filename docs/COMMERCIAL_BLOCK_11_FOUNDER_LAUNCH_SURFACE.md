# Commercial Block 11: Founder Launch Surface

Status: completed.

GitHub issues:

- #19 `[P0] Create product landing page`
- #20 `[P0] Prepare beta onboarding`
- #21 `[P0] Define Free / Founder Pro / Pro / Business plans`

## Goal

Prepare the first public-facing product surface for Universal Media Extractor without starting payments, licensing enforcement, Apple signing, Windows packaging, batch, AI summary, or new downloader features.

## What Was Created

- Static landing page in `site/`
- Public website copy doc: `docs/FOUNDER_LAUNCH_SITE_COPY.md`
- Beta onboarding copy doc: `docs/BETA_ONBOARDING_COPY.md`
- Pricing/plans doc: `docs/PRICING_AND_PLANS.md`
- Support page draft: `docs/SUPPORT_PAGE_DRAFT.md`
- Site regression tests: `tests/test_founder_launch_site.py`

## Public Positioning

```text
Local Media Downloader & Organizer for macOS and Windows
```

Public promise:

```text
Save accessible media, subtitles, and transcripts into organized local folders without uploading source files to a cloud service.
```

## Website Scope

The static site includes:

- local/private workflow explanation;
- macOS and Windows download sections;
- visible limitations;
- privacy, EULA, refund, limitations, and support links;
- beta/download CTA placeholders;
- Free, Founder Pro, Pro, and Business plan summary.

## What Is Intentionally Not On The Public Site

- Udemy Course Mode positioning;
- guaranteed source support claims;
- DRM/paywall/CAPTCHA/login bypass claims;
- checkout/payment integration;
- license key activation;
- Windows installer download before a build exists;
- Apple signed/notarized download before Developer ID is ready.

## Verification

Completed:

```bash
.venv/bin/python -m pytest -q  # 179 passed
node --check src/universal_media_extractor/static/app.js
python3 -m http.server 8767 --directory site
```

Browser proof with Playwright confirmed the landing page and limitations page render.

Proof screenshots:

```text
proof/commercial_block_11_founder_launch_site/landing_page.png
proof/commercial_block_11_founder_launch_site/limitations_page.png
```

Local site preview:

```bash
python3 -m http.server 8767 --directory site
open http://127.0.0.1:8767/
```

## Remaining Follow-Up

- Replace beta/download placeholders with real signed macOS and Windows artifacts when packaging is ready.
- Connect payment/licensing only after payment provider approval.
- Add a real signup channel when the founder beta list is chosen.
