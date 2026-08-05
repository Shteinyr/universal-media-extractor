# Commercial Block 10: macOS Public Release Prep

Status: prepared; issues #13 and #14 remain open because final acceptance requires Apple Developer ID access.

GitHub issues:

- #13 `[P0] Add macOS signing and notarization`
- #14 `[P0] Create macOS DMG installer`

## Goal

Prepare the complete public macOS release checklist around the current production `.app`, signing, notarization, and DMG installer path without purchasing Apple Developer Program membership or using private credentials.

## What Was Prepared

- Public release checklist: `docs/MACOS_PUBLIC_RELEASE_CHECKLIST.md`
- Apple Developer setup guide: `docs/APPLE_DEVELOPER_ACCOUNT_SETUP.md`
- Signed/notarized app and DMG validation checklist: `docs/MACOS_RELEASE_VALIDATION_CHECKLIST.md`
- Troubleshooting guide: `docs/MACOS_SIGNING_NOTARIZATION_TROUBLESHOOTING.md`
- DMG notarization helper: `scripts/notarize_macos_dmg.py`
- Tests for DMG notarization command construction: `tests/test_notarize_macos_dmg.py`

## Official Sources Checked

- Apple Developer Program enrollment: https://developer.apple.com/programs/enroll/
- Apple Developer ID overview: https://developer.apple.com/developer-id/
- Apple Developer ID certificates: https://developer.apple.com/help/account/certificates/create-developer-id-certificates/
- Apple packaging guidance: https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution
- Apple notarization guidance: https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
- Apple custom notarization workflow: https://developer.apple.com/documentation/security/customizing-the-notarization-workflow
- Apple common notarization issues: https://developer.apple.com/documentation/Security/resolving-common-notarization-issues
- Apple notarytool migration note: https://developer.apple.com/documentation/technotes/tn3147-migrating-to-the-latest-notarization-tool

## Current Readiness

Ready locally:

- Build production-foundation `.app` with PyInstaller.
- Check signing/notarization tool readiness.
- Build local unsigned DMG with checksum.
- Construct Developer ID signing command.
- Construct app notarization command.
- Construct DMG notarization command.
- Document install/uninstall, validation, and troubleshooting.

Blocked externally:

- Active Apple Developer Program membership.
- `Developer ID Application` certificate in Keychain.
- Notary credentials stored in Keychain profile.
- Real Apple notarization submission.
- Gatekeeper validation of signed/notarized distributed artifact.

## Issue Crosswalk

Issue #13 acceptance:

- Developer ID signing path is documented: ready.
- Hardened runtime is enabled in signing script: ready.
- Notarization succeeds: blocked by Apple Developer ID credentials.
- Gatekeeper launch check passes: blocked until signed/notarized artifact exists.

Issue #14 acceptance:

- DMG contains the signed/notarized app: blocked by #13.
- Install instructions are clear: ready.
- Uninstall behavior is documented: ready.
- Checksum/release artifact is produced: local unsigned proof ready; public release checksum still needs final signed/notarized DMG.

## Verification Performed

Completed for this block:

```bash
.venv/bin/python -m pytest -q  # 173 passed
node --check src/universal_media_extractor/static/app.js
.venv/bin/python scripts/notarize_macos_dmg.py --dry-run
```

## What Was Not Done

- No Apple Developer Program enrollment.
- No real certificate creation.
- No password, key, or private credential storage.
- No real signing/notarization claim.
- No Windows build.
- No payments, website, product features, Chrome extension, AI summary, or batch work.

## Next Gate

To finish #13/#14 later, the user must complete Apple Developer account setup and provide the non-secret release parameters listed in `docs/APPLE_DEVELOPER_ACCOUNT_SETUP.md`.
