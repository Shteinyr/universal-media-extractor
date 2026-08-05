# Stripe Fallback Risk Review

Status: draft. Stripe is a fallback path only. Do not integrate Stripe checkout until this risk review is resolved.

## Purpose

Assess whether Universal Media Extractor can safely use Stripe if Lemon Squeezy is not approved or not suitable.

## Official Sources Checked

- Stripe prohibited and restricted businesses: `https://stripe.com/legal/restricted-businesses`
- Stripe Services Agreement: `https://stripe.com/ssa`

## Fit

The acceptable framing is downloadable desktop software for local media organization and transcription.

The risky framing is any product that appears to enable unauthorized distribution, copyright infringement, DRM bypass, paywall bypass, or third-party content resale.

## Main Stripe Risks

| Risk | Why It Matters | Mitigation |
| --- | --- | --- |
| Intellectual property facilitation | Stripe prohibits products/services that infringe or facilitate infringement. | Public copy must focus on user-authorized, accessible media and local organization. |
| Misleading downloader claims | Claims like `downloads everything` can look deceptive or abusive. | Use best-effort source support and explicit limitations. |
| Cyberlocker / hosted content risk | Hosted file-sharing services are restricted/high risk. | The product must remain local desktop software, not hosted extraction or file sharing. |
| Authenticated/paid course claims | Public Udemy/course downloader positioning increases compliance risk. | Keep Udemy internal/experimental and hidden from public builds/marketing. |
| Chargebacks/refunds | Source support can break due third-party changes. | Refund copy must disclose best-effort source support clearly before purchase. |

## Required Public Copy Before Stripe Review

- Product: `Local Media Downloader & Organizer for macOS and Windows`.
- Required limitation: no DRM, CAPTCHA, paywall, login restriction, or platform access-control bypass.
- Required user-rights statement: users must own, create, or have permission to download/process media.
- Required privacy statement: local processing, no media upload by default.
- Required support statement: source support is best-effort and may change.

## Questions To Send To Stripe

1. Is selling this local desktop utility acceptable under Stripe's restricted business policy?
2. Does the product need a restricted-business review because it can save media from user-provided URLs?
3. Are the current copy boundaries sufficient to avoid IP-facilitation concerns?
4. Are one-time software licenses with optional annual update renewals acceptable?
5. Is additional disclosure needed for best-effort support of third-party sources?

## Stripe Go / No-Go Criteria

Go only if:

- Stripe confirms the product category is acceptable, or no additional review is required after accurate disclosure.
- Public copy does not advertise protected-source or unauthorized-use behavior.
- The product does not store or distribute third-party media.
- Legal/refund/privacy docs are live before checkout.

No-go if:

- Stripe classifies the product as infringement facilitation.
- Stripe requires removal of core URL-download functionality.
- Compliance review requires guarantees the product cannot honestly provide.

## Current Decision

Use Stripe only as fallback. Prefer Lemon Squeezy first because merchant-of-record handling and built-in license keys better match the first founder launch.
