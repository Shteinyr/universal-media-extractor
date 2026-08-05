# Licensing Model Draft

Status: draft. No license server, provider API integration, activation UI, or enforcement code is implemented.

## Goals

- Simple individual license.
- 3-device activation for Pro/Founder Pro by default.
- Offline-friendly desktop usage.
- Clear update entitlement.
- User-controlled device deactivation.
- Low support burden for founder launch.

## Product Plans

| Plan | License Behavior |
| --- | --- |
| Free | No license key required; feature limits later. |
| Founder Pro | License key; 3 devices; included compatibility-update period. |
| Pro | License key; 3 devices; included compatibility-update period. |
| Business | License key; device/seat limit to be finalized before sale. |

## License Key

Initial recommendation:

- Use provider-issued license keys if Lemon Squeezy is approved.
- Generate one unique license key per purchase.
- Store only the local activation cache in the app.
- Do not store media history, URLs, transcripts, cookies, or source files in licensing systems.

Lemon Squeezy is a good first candidate because its licensing docs support license validity windows and activation limits.

## Device Limit

Default:

```text
3 active devices per Pro / Founder Pro license
```

Device identity should be privacy-preserving:

- local random device id generated at first activation;
- device label such as `Aleksandr's MacBook Pro`;
- no hardware serial number unless absolutely necessary and disclosed.

## Activation Flow Draft

1. User installs the desktop app.
2. User enters license key.
3. App sends license key plus local device label to the license validation/activation endpoint.
4. Server/provider returns:
   - license status;
   - plan;
   - activation id;
   - update entitlement end date;
   - device limit;
   - optional customer email.
5. App stores a local signed entitlement cache.

## Offline Entitlement

After successful activation, the app should continue working offline using a local signed cache.

Recommended first policy:

- Pro features work offline for the last known valid entitlement.
- App attempts validation when internet is available.
- Offline use does not require media files to leave the machine.

## Grace Period

Recommended first policy:

```text
30 days grace after the last successful validation
```

During grace:

- existing activated Pro features keep working;
- the app shows a gentle notice if validation has not happened for a while;
- no hard failure while the user is offline inside the grace period.

After grace:

- keep core free features available;
- ask the user to connect briefly and validate the license;
- do not delete outputs or transcripts.

## Deactivate Device

Needed behavior:

- In-app `Deactivate this device`.
- Deactivation frees one activation.
- If the provider supports license instances, store the provider instance id locally.
- If deactivation fails offline, queue a local pending deactivation and ask the user to retry online.

## Update Entitlement

Purchase should grant app usage plus compatibility updates for a defined period.

Recommended rule:

- Customer keeps the last eligible version after the update period expires.
- New compatibility/media-engine updates after expiration require renewal.
- Existing local output files and transcripts remain usable.
- Security-critical fixes may be handled separately by policy later.

This prevents `subscription-or-nothing` pressure while still supporting recurring compatibility work.

## License State Model

Suggested future local state:

- `license_key_hash`
- `plan`
- `status`
- `activation_id`
- `device_label`
- `activated_at`
- `last_validated_at`
- `grace_expires_at`
- `update_entitlement_expires_at`
- `max_activations`
- `signature`

Do not store raw license keys in plaintext if avoidable. Prefer Keychain/Credential Manager for secrets and signed local cache for entitlement state.

## Enforcement Boundary

First implementation should gate commercial features, not punish the user's local files.

Never:

- delete outputs after license expiry;
- block access to already generated files;
- phone home with media URLs/transcripts;
- silently upload diagnostics.

## Open Decisions

- Exact included update period: 12 months recommended, but not confirmed.
- Founder Pro update period: same as Pro or longer?
- Business device/seat policy.
- Whether Lemon Squeezy license API is enough or a small custom license server is needed.
- Where license state lives on macOS/Windows.
- Whether Free limits are enforced locally or only through distribution.
