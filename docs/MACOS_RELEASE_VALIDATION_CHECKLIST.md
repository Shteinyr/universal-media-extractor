# macOS Release Validation Checklist

Purpose: verify a signed/notarized Universal Media Extractor `.app` and public DMG before release.

## Build Validation

- Run full tests:

```bash
.venv/bin/python -m pytest -q
```

- Run static JavaScript syntax check:

```bash
node --check src/universal_media_extractor/static/app.js
```

- Build app:

```bash
.venv/bin/python scripts/build_macos_app.py
```

- Confirm app exists:

```bash
test -d "build/macos/dist/Universal Media Extractor.app"
```

## Signed App Validation

- Sign app:

```bash
.venv/bin/python scripts/sign_macos_app.py \
  --identity "Developer ID Application: Company Name (TEAMID)"
```

- Verify signature:

```bash
codesign --verify --deep --strict --verbose=2 \
  "build/macos/dist/Universal Media Extractor.app"
```

- Confirm Hardened Runtime:

```bash
codesign -dvvv "build/macos/dist/Universal Media Extractor.app" 2>&1 | grep runtime
```

- Confirm expected identity:

```bash
codesign -dvvv "build/macos/dist/Universal Media Extractor.app" 2>&1 | grep "Developer ID Application"
```

## App Smoke Validation

Run the signed app locally before DMG packaging:

```bash
open "build/macos/dist/Universal Media Extractor.app"
```

Check:

- Window opens.
- Local backend starts.
- UI loads.
- `Analyze` works on a safe public test URL.
- No terminal window is required.
- Closing the app stops the owned backend.

## DMG Build Validation

- Build signed DMG:

```bash
.venv/bin/python scripts/build_macos_dmg.py \
  --sign-identity "Developer ID Application: Company Name (TEAMID)"
```

- Verify DMG integrity:

```bash
hdiutil verify "build/macos/dmg/Universal Media Extractor.dmg"
```

- Verify DMG signature:

```bash
codesign --verify --verbose=2 "build/macos/dmg/Universal Media Extractor.dmg"
```

## DMG Notarization Validation

For direct distribution, Apple recommends notarizing the outermost container. For the public download, that is the DMG.

```bash
.venv/bin/python scripts/notarize_macos_dmg.py \
  --keychain-profile UME_NOTARY
```

Check:

- `notarytool submit` returns accepted status.
- `xcrun stapler staple` succeeds for the DMG.
- `xcrun stapler validate` succeeds for the DMG.
- `spctl --assess --type open --verbose=4` accepts the DMG.

## Installed App Validation

On a clean macOS user account or second Mac if available:

1. Open the DMG.
2. Drag app to `/Applications`.
3. Launch from `/Applications`.
4. Confirm Gatekeeper presents the expected notarized-developer dialog or opens without blocking.
5. Confirm the app can find required local CLIs:
   - `yt-dlp`
   - `ffmpeg`
   - `ffprobe`
   - `whisper`
6. Run a safe analysis-only smoke.
7. Run one small download/transcribe smoke only with authorized media.

## Release Page Validation

Before publishing:

- Final DMG exists.
- Final `.sha256` matches the final DMG after stapling.
- Release notes are present.
- EULA link is present.
- Privacy policy link is present.
- Known limitations link is present.
- Product copy does not promise universal source support.
- Product copy does not promise DRM/paywall/CAPTCHA/login bypass.
- Udemy Course mode is hidden from public commercial builds unless separately approved.

## Pass / Fail Gate

Pass only when:

- Tests pass.
- App is Developer ID signed.
- App passes signature verification.
- DMG is signed.
- DMG is notarized and stapled.
- Gatekeeper accepts the DMG.
- Installed app launches from `/Applications`.
- Smoke test passes.

Fail if:

- Any notarization issue remains unresolved.
- Gatekeeper blocks the artifact.
- The app only works from terminal but not Finder.
- The release artifact has no checksum.
- Public copy overpromises unsupported media/platform behavior.
