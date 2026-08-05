# Commercial Block 8: macOS Signing / Notarization Readiness

Status: readiness prepared; issue #13 remains open because a real Apple Developer ID certificate and notarization credentials are required to complete notarization.

GitHub issue: #13 `[P0] Add macOS signing and notarization`.

## Goal

Prepare the reproducible signing and notarization path for the macOS app built in Commercial Block 7. This block intentionally does not perform real Developer ID signing because the local machine does not currently have a `Developer ID Application` identity available in Keychain.

## Official Requirements Checked

Apple documents the direct-distribution macOS path as Developer ID signing plus notarization. Current Apple documentation confirms these requirements:

- Direct distribution outside the Mac App Store should use a Developer ID certificate and notarization.
- Hardened Runtime must be enabled for apps submitted for notarization.
- Apple notarization now uses `notarytool`; `altool` notarization uploads are no longer accepted.
- Custom workflows use `xcrun notarytool submit ... --keychain-profile ... --wait`, then `xcrun stapler staple`, then validation.
- Apple requires a valid Developer ID certificate, secure timestamp, hardened runtime, and properly formatted entitlements.

Primary sources:

- Apple: Notarizing macOS software before distribution: https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
- Apple: Customizing the notarization workflow: https://developer.apple.com/documentation/security/customizing-the-notarization-workflow
- Apple Xcode Help: Distribute outside the Mac App Store: https://help.apple.com/xcode/mac/current/en.lproj/dev033e997ca.html
- Apple Xcode Help: Enable hardened runtime: https://help.apple.com/xcode/mac/current/en.lproj/devf87a2ac8f.html
- Apple Developer ID support: https://developer.apple.com/support/developer-id/

PyInstaller docs confirm macOS `.app` bundle support, Info.plist customization, macOS code-signing support, signing identity options, entitlements file support, and target architecture options.

## Files Added

- `packaging/macos/entitlements.plist`
- `scripts/check_macos_signing_readiness.py`
- `scripts/store_macos_notary_credentials.py`
- `scripts/sign_macos_app.py`
- `scripts/notarize_macos_app.py`
- `tests/test_macos_signing_readiness.py`

## Current Readiness Result

Command:

```bash
.venv/bin/python scripts/check_macos_signing_readiness.py --json
```

Result: not ready.

Confirmed available:

- macOS host;
- Apple Silicon arm64 host;
- `codesign`;
- `xcrun notarytool`;
- `xcrun stapler`;
- `spctl`;
- active Xcode command line tools;
- built app bundle;
- entitlements file.

Missing:

- `Developer ID Application` certificate in the available macOS keychains.

Proof artifact:

```text
proof/commercial_block_8_macos_signing_readiness/readiness_check.json
```

## Data Needed From Apple Developer Account

To complete issue #13 later, the owner needs:

- active Apple Developer Program membership;
- Team ID;
- Apple ID email that can notarize for the team;
- app-specific password for notarization, or another Apple-supported notarytool credential method;
- `Developer ID Application` certificate installed in Keychain;
- signing identity string, for example `Developer ID Application: Company Name (TEAMID)`;
- notarytool keychain profile name, recommended: `UME_NOTARY`.

Do not commit passwords, private keys, cookies, or notarization credentials to the repository.

## Future Signing Flow

Build the app:

```bash
.venv/bin/python scripts/build_macos_app.py
```

Check readiness:

```bash
.venv/bin/python scripts/check_macos_signing_readiness.py
```

Store notarization credentials in Keychain. This prompts for the app-specific password interactively; the password is not passed as a command argument and is not saved in project files:

```bash
.venv/bin/python scripts/store_macos_notary_credentials.py \
  --apple-id "APPLE_ID_EMAIL" \
  --team-id "TEAMID" \
  --profile UME_NOTARY
```

Sign with Developer ID and Hardened Runtime:

```bash
.venv/bin/python scripts/sign_macos_app.py \
  --identity "Developer ID Application: Company Name (TEAMID)"
```

Notarize, staple, and assess with Gatekeeper:

```bash
.venv/bin/python scripts/notarize_macos_app.py \
  --keychain-profile UME_NOTARY
```

Dry-run commands are available for review:

```bash
.venv/bin/python scripts/sign_macos_app.py \
  --identity "Developer ID Application: Company Name (TEAMID)" \
  --dry-run

.venv/bin/python scripts/notarize_macos_app.py --dry-run
```

## Hardened Runtime

The signing script uses:

```text
codesign --options runtime --timestamp
```

`packaging/macos/entitlements.plist` is intentionally empty for now. Add entitlements only if a real signed build proves the app requires them. This keeps the public build tighter and avoids unnecessary hardened runtime exceptions.

## Gatekeeper Validation

The notarization script validates with:

```bash
xcrun stapler validate "build/macos/dist/Universal Media Extractor.app"
spctl --assess --type execute --verbose=4 "build/macos/dist/Universal Media Extractor.app"
```

Before public release, also test a quarantined downloaded build on a clean macOS user account.

## What Was Not Done

- No real Developer ID signing was performed.
- No notarization submission was performed.
- No Gatekeeper pass was claimed.
- No DMG installer work was started.
- No Windows build, payments, website, Chrome extension, AI summary, batch, or product feature work was added.

## Why Issue #13 Remains Open

Acceptance criteria require notarization success and Gatekeeper launch check. Current evidence proves the workflow is ready, but not that Apple notarization has succeeded. The blocking missing item is an installed `Developer ID Application` certificate and notarytool credentials from the Apple Developer account.
