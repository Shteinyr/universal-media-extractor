# macOS Public Release Checklist

Purpose: one checklist for producing a direct-distribution macOS release of Universal Media Extractor.

This checklist assumes the public channel is direct download through a website/GitHub release, not the Mac App Store.

## Current Status

Completed:

- Production-foundation `.app` build script exists.
- Signing readiness script exists.
- App signing script exists.
- App notarization helper exists.
- DMG build script exists.
- DMG notarization helper exists.
- Install/uninstall notes exist.
- Local unsigned DMG proof and checksum path exist.

Blocked:

- Apple Developer Program membership and Developer ID signing identity are not available to Codex.
- Final signed/notarized `.app` and public DMG cannot be produced yet.

## Required Release Inputs

From Apple/user:

- Active Apple Developer Program membership.
- Team ID.
- Apple ID email with permission to notarize for the team.
- Installed `Developer ID Application` certificate.
- Exact signing identity string.
- Notary keychain profile name, recommended `UME_NOTARY`.
- App-specific password entered interactively when storing notary credentials.

From product/repo:

- Release version.
- Release notes.
- Public known limitations.
- Privacy policy, EULA, refund/support links.
- Final website/download destination.

Never commit:

- Apple ID password.
- App-specific password.
- Private signing key.
- `.p8` API key.
- Keychain exports.

## Preflight

Run tests:

```bash
.venv/bin/python -m pytest -q
node --check src/universal_media_extractor/static/app.js
```

Build production `.app`:

```bash
.venv/bin/python scripts/build_macos_app.py
```

Check signing readiness:

```bash
.venv/bin/python scripts/check_macos_signing_readiness.py
```

Expected before final release:

- `Developer ID Application` identity is found.
- `xcrun notarytool` is available.
- `xcrun stapler` is available.
- `spctl` is available.
- App bundle exists.
- Entitlements file exists.

## One-Time Apple Setup

Follow `docs/APPLE_DEVELOPER_ACCOUNT_SETUP.md`.

Expected local verification:

```bash
security find-identity -v -p codesigning
.venv/bin/python scripts/check_macos_signing_readiness.py
```

## Public Release Build Flow

1. Build production `.app`:

```bash
.venv/bin/python scripts/build_macos_app.py
```

2. Sign `.app` with Developer ID and hardened runtime:

```bash
.venv/bin/python scripts/sign_macos_app.py \
  --identity "Developer ID Application: Company Name (TEAMID)"
```

3. Optional app notarization validation path:

```bash
.venv/bin/python scripts/notarize_macos_app.py \
  --keychain-profile UME_NOTARY
```

4. Build DMG from the signed app:

```bash
.venv/bin/python scripts/build_macos_dmg.py \
  --sign-identity "Developer ID Application: Company Name (TEAMID)"
```

5. Submit, staple, and assess the DMG:

```bash
.venv/bin/python scripts/notarize_macos_dmg.py \
  --keychain-profile UME_NOTARY
```

6. Regenerate/check SHA-256 checksum if the DMG changed after stapling.

7. Validate with `docs/MACOS_RELEASE_VALIDATION_CHECKLIST.md`.

## Release Artifact Checklist

Required:

- `Universal Media Extractor.dmg`
- `Universal Media Extractor.dmg.sha256`
- Release notes.
- Minimum macOS version note.
- Apple Silicon support note.
- Install/uninstall instructions.
- Known limitations link.
- Privacy policy link.
- EULA link.
- Support/contact link.

Optional for beta:

- Build log summary.
- Smoke test screenshot.
- Changelog excerpt.

## GitHub Issue Closure Gate

Do not close #13 until:

- Developer ID signing succeeds.
- Hardened Runtime is enabled.
- Notarization succeeds.
- Gatekeeper launch check passes.

Do not close #14 until:

- Public DMG contains the signed/notarized app.
- DMG is signed/notarized/stapled.
- Install/uninstall instructions are verified.
- Checksum is generated for the final artifact.
