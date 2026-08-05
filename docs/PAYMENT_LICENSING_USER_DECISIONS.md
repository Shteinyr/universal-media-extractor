# Payment And Licensing User Decisions

Status: required before real checkout or licensing implementation.

## Provider Decisions

- Confirm first payment provider: Lemon Squeezy or Stripe.
- Confirm whether Lemon Squeezy pre-approval was requested.
- Confirm whether provider approved the product category.
- Confirm whether checkout can start in test mode after approval.

## Business Details Needed

- Legal seller name.
- Country/jurisdiction.
- Business address for provider onboarding.
- Support email.
- Public website domain.
- Privacy policy URL.
- EULA URL.
- Refund policy URL.
- Known limitations URL.

## Pricing Decisions

- Confirm final Free / Founder Pro / Pro / Business prices.
- Confirm currency for founder launch.
- Confirm whether Founder Pro is time-limited, quantity-limited, or both.
- Confirm included update period.
- Confirm annual renewal price and wording.
- Confirm refund window; current draft assumes 14 days.

## Licensing Decisions

- Confirm 3-device limit for Pro/Founder Pro.
- Confirm Business device/seat limit.
- Confirm 30-day offline grace period.
- Confirm deactivate-device behavior.
- Confirm whether users keep the last eligible version after update entitlement expires.
- Confirm whether license keys are handled by Lemon Squeezy or a custom license server.

## Product Boundary Decisions

- Confirm Udemy Course Mode remains hidden from public commercial builds.
- Confirm no public promise for DRM/CAPTCHA/paywall/login bypass.
- Confirm no hosted extraction service.
- Confirm no user media upload by default.

## Implementation Gate

Do not implement checkout, webhooks, license server, activation UI, or license enforcement until these decisions are answered and provider approval is recorded.
