# Pricing And Plans

Status: commercial draft. Payment, checkout, license activation, and entitlement enforcement are not implemented.

## Plan Summary

| Plan | Price | Audience | Position |
| --- | ---: | --- | --- |
| Free | $0 | Trial users | Test local analysis and basic single-item workflows |
| Founder Pro | $24 | Early supporters | Discounted early license while product matures |
| Pro | $39 | Individual power users | Full single-user desktop workflow |
| Business | $99 | Small teams / commercial users | Business license terms and priority support path |

## Free

Price: `$0`

Draft includes:

- URL analysis;
- local file analysis;
- limited single-item download/transcription workflows;
- basic output folders;
- visible limitations;
- no batch/queue promise;
- no priority support.

Purpose:

- prove the app works on the user's machine;
- reduce refund pressure;
- make source limitations visible before purchase.

## Founder Pro

Price: `$24`

Draft includes:

- early discounted Pro access;
- macOS and Windows direct download when builds exist;
- local transcription;
- presets;
- output templates and duplicate handling;
- persistent jobs/history;
- compatibility updates during the founder update period;
- founder feedback channel.

Important:

- do not promise every source works;
- do not promise DRM/paywall/CAPTCHA/login bypass;
- do not process payments until provider approval is complete.

## Pro

Price: `$39`

Renewal model: `$19/year` for compatibility updates after the included update period.

Draft includes:

- single-user local desktop app;
- organized video/audio/subtitle downloads;
- local file transcription;
- URL media transcription;
- output templates;
- persistent jobs/history;
- retry/reveal output behavior;
- future queue/batch features when implemented;
- compatibility updates during active update period.

## Business

Price: `$99`

Draft includes:

- business license terms;
- more devices/seats than Pro after licensing is implemented;
- priority support workflow;
- documented deployment/support guidance;
- local-first processing by default;
- no cloud upload requirement by default.

## Feature Boundary Map

| Capability | Free | Founder Pro | Pro | Business |
| --- | --- | --- | --- | --- |
| URL analyze | Yes | Yes | Yes | Yes |
| Local file analyze | Yes | Yes | Yes | Yes |
| Single-item download | Limited | Yes | Yes | Yes |
| Local transcription | Limited | Yes | Yes | Yes |
| Presets | Basic | Yes | Yes | Yes |
| Output templates | Basic | Yes | Yes | Yes |
| Persistent history | Limited | Yes | Yes | Yes |
| Batch/queue | No | Planned | Planned | Planned |
| Priority support | No | Founder feedback | Standard | Priority |
| Business use terms | No | No | No | Yes |

## Payment Provider Gate

Before integrating checkout:

- request Lemon Squeezy pre-approval;
- request Stripe risk confirmation as fallback;
- confirm public copy does not imply platform bypass;
- confirm refund copy explains best-effort source support.

## Licensing Gate

Do not build license enforcement until:

- payment provider path is approved;
- signed desktop builds exist;
- activation/offline entitlement model is designed;
- privacy policy/EULA language is reviewed.

## Block 12 Payment/Licensing Prep

Commercial Block 12 prepared the provider-review and licensing drafts, but payment remains disabled.

Current planned order:

1. Request Lemon Squeezy pre-approval using `docs/LEMON_SQUEEZY_PREAPPROVAL_REQUEST.md`.
2. Keep Stripe as fallback using `docs/STRIPE_FALLBACK_RISK_REVIEW.md`.
3. Confirm user/business decisions in `docs/PAYMENT_LICENSING_USER_DECISIONS.md`.
4. Only after approval, design the actual checkout/license activation implementation.

Licensing model draft: `docs/LICENSING_MODEL_DRAFT.md`.
