# macOS Signing / Notarization Troubleshooting

Purpose: quick fixes for common macOS direct-distribution failures.

Official source: https://developer.apple.com/documentation/Security/resolving-common-notarization-issues

## Developer ID Application Identity Missing

Symptom:

```text
Developer ID Application identity is missing
```

Check:

```bash
security find-identity -v -p codesigning
```

Likely cause:

- Certificate was not created.
- Certificate was downloaded but not installed.
- Certificate is installed in another keychain.
- Account role does not allow creating Developer ID certificates.

Fix:

- Create/install `Developer ID Application` certificate.
- Double-click downloaded `.cer`.
- Verify it appears under My Certificates in Keychain Access.

## Wrong Certificate Type

Symptom:

```text
The binary is not signed with a valid Developer ID certificate.
```

Likely cause:

- App was signed with Apple Development, Mac App Distribution, self-signed, or Developer ID Installer certificate.

Fix:

- Use `Developer ID Application` for `.app`, Mach-O binaries, and DMG signing.
- Use `Developer ID Installer` only for installer packages.

## Invalid Signature

Symptom:

```text
The signature of the binary is invalid.
```

Likely cause:

- Files changed after signing.
- Nested binary was unsigned.
- Bundle was copied by a tool that damaged metadata.

Fix:

```bash
codesign --verify --deep --strict --verbose=4 "build/macos/dist/Universal Media Extractor.app"
```

Rebuild, sign last, then package the signed app into the DMG.

## Hardened Runtime Missing

Symptom:

```text
The executable does not have the hardened runtime enabled.
```

Fix:

- Use the project signing script, which includes:

```text
codesign --options runtime --timestamp
```

Validate:

```bash
codesign -dvvv "build/macos/dist/Universal Media Extractor.app" 2>&1 | grep runtime
```

## Notary Credentials Missing

Symptom:

```text
No Keychain password item found
Must provide credentials
```

Fix:

```bash
.venv/bin/python scripts/store_macos_notary_credentials.py \
  --apple-id "APPLE_ID_EMAIL" \
  --team-id "TEAMID" \
  --profile UME_NOTARY
```

Then retry with:

```bash
.venv/bin/python scripts/notarize_macos_dmg.py --keychain-profile UME_NOTARY
```

## Invalid Team ID Or Access

Symptom:

```text
Invalid or inaccessible developer team ID
```

Likely cause:

- Wrong Team ID.
- Apple ID is not on the team.
- Membership expired.
- Team role lacks certificate/notarization access.

Fix:

- Confirm Team ID in Apple Developer membership details.
- Confirm the Apple ID has access to the Developer Program team.
- Re-run `store-credentials`.

## Notarization Rejected

Symptom:

```text
status: Invalid
```

Fix:

1. Fetch the notary log:

```bash
xcrun notarytool log SUBMISSION_ID --keychain-profile UME_NOTARY notary_log.json
```

2. Fix every reported item.
3. Rebuild from clean source.
4. Re-sign.
5. Re-notarize.

Common reasons:

- invalid code signature;
- missing hardened runtime;
- unsigned nested binary;
- unsupported old SDK;
- entitlements mismatch.

## Stapler Fails

Symptom:

```text
stapler: ticket not found
```

Likely cause:

- Notarization was not accepted.
- Stapling the wrong file.
- Trying to staple before Apple has published the ticket.

Fix:

- Confirm the submitted artifact was accepted.
- Staple the same public artifact users receive: the DMG.
- Retry after a short wait if the accepted ticket is not visible yet.

## Gatekeeper Rejects DMG

Symptom:

```text
spctl --assess --type open ... rejected
```

Fix:

```bash
xcrun stapler validate "build/macos/dmg/Universal Media Extractor.dmg"
codesign --verify --verbose=2 "build/macos/dmg/Universal Media Extractor.dmg"
spctl --assess --type open --verbose=4 "build/macos/dmg/Universal Media Extractor.dmg"
```

Rebuild/re-sign/re-notarize if validation fails.

## App Works From Terminal But Not Finder

Symptom:

- App opens from `scripts/run_desktop.py`, but packaged `.app` cannot find `yt-dlp`, `ffmpeg`, or `whisper`.

Likely cause:

- Finder-launched apps do not inherit shell `PATH`.

Fix:

- Confirm `scripts/run_desktop.py` production launch still prepends standard CLI paths.
- Verify CLI discovery from the packaged app smoke test.

## DMG Creation Fails

Symptom:

```text
hdiutil create failed
```

Likely cause:

- Existing locked DMG.
- App is still running.
- Staging folder cannot be overwritten.
- Not enough disk space.

Fix:

- Quit the app.
- Remove old local build artifacts if safe.
- Rebuild app, then DMG.
- Verify available disk space.

## Gatekeeper Warning Still Appears On Downloaded Build

Likely cause:

- DMG was not stapled.
- Browser/download added quarantine and Gatekeeper cannot reach online ticket.
- User is opening an older unsigned build.

Fix:

- Validate stapling on the final DMG.
- Re-download the exact final artifact.
- Test on a clean machine/account.

## Notary Service Timeout Or Server Error

Likely cause:

- Apple notary service delay/outage.
- Network issue.

Fix:

- Retry later.
- Check Apple Developer System Status.
- Use `notarytool history --keychain-profile UME_NOTARY` to inspect submissions.

## Safety Notes

- Do not paste passwords into issue comments, docs, or chat.
- Do not commit private keys or Keychain exports.
- Do not add entitlements unless the signed build proves they are required.
- Keep Udemy Course Mode hidden from public commercial builds unless separately approved.
