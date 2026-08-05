# Commercial Block 12: Payment Provider Pre-Approval And Licensing Prep

Status: completed as planning/pre-approval package. No checkout, provider API integration, license server, or license enforcement code was added.

GitHub issues:

- #22 `[P0] Prepare licensing model` - closed / Done
- #23 `[P0] Prepare payment provider pre-approval` - closed / Done

## Goal

Prepare the product for payment-provider review and future licensing implementation before any real checkout work starts.

## Scope Completed

- Lemon Squeezy pre-approval request draft.
- Stripe fallback risk review notes.
- Licensing model draft for desktop activation.
- User decision checklist before real payment/licensing integration.
- Documentation test coverage for the new commercial docs.

## Official Sources Checked

- Lemon Squeezy prohibited products: `https://docs.lemonsqueezy.com/help/getting-started/prohibited-products`
- Lemon Squeezy merchant of record: `https://docs.lemonsqueezy.com/help/payments/merchant-of-record`
- Lemon Squeezy license keys: `https://docs.lemonsqueezy.com/help/licensing/generating-license-keys`
- Lemon Squeezy license activation API: `https://docs.lemonsqueezy.com/api/license-api/activate-license-key`
- Lemon Squeezy license validation API: `https://docs.lemonsqueezy.com/api/license-api/validate-license-key`
- Stripe prohibited and restricted businesses: `https://stripe.com/legal/restricted-businesses`
- Stripe Services Agreement: `https://stripe.com/ssa`

## Key Findings

- Lemon Squeezy explicitly supports digital goods such as software/SaaS, and its merchant-of-record model can handle payments, tax, refunds, chargebacks, and PCI burden.
- Lemon Squeezy also prohibits products/content without proper IP rights and products restricted by payment partners, so this product needs pre-approval before checkout.
- Stripe has explicit IP infringement and facilitation risk language; downloader positioning must remain legal-safe and user-rights-first.
- Lemon Squeezy license keys support activation limits and license validity windows, which fits the initial `3 devices + update entitlement` model.

## Product Boundary For Provider Review

Position as:

```text
Local Media Downloader & Organizer for macOS and Windows
```

Do not position as:

- universal downloader;
- paid-course downloader;
- DRM bypass tool;
- paywall/login/CAPTCHA bypass tool;
- file hosting or cyberlocker;
- cloud extraction service.

## New Documents

- `docs/LEMON_SQUEEZY_PREAPPROVAL_REQUEST.md`
- `docs/STRIPE_FALLBACK_RISK_REVIEW.md`
- `docs/LICENSING_MODEL_DRAFT.md`
- `docs/PAYMENT_LICENSING_USER_DECISIONS.md`

## What Is Intentionally Not Implemented

- Checkout buttons or payment links.
- Lemon Squeezy API calls.
- Stripe API calls.
- Webhooks.
- License server.
- Activation UI.
- License enforcement in the desktop app.
- Production installer/signing changes.
- Website deployment or pricing checkout.

## Recommended Next Gate

Before checkout implementation, the user needs to provide business/account details and receive provider approval or at least written risk confirmation.

Until then, the product can continue improving beta readiness without collecting payments.
