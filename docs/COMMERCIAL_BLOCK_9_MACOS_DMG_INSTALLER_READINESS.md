# Commercial Block 9: macOS DMG Installer Readiness

Status: readiness prepared; issue #14 remains open because the public DMG acceptance criteria require a signed/notarized app inside the DMG.

GitHub issue: #14 `[P0] Create macOS DMG installer`.

## Goal

Prepare a reproducible macOS DMG installer artifact from the current production-foundation `.app`, without starting Windows, payments, website, Chrome extension, AI summary, batch, or product feature work.

## Official Requirements Checked

Apple documentation for direct macOS distribution confirms the DMG path:

- Create a source directory for the disk image volume.
- Populate it with the files to distribute; use `ditto`/symlink-preserving behavior when scripting.
- Use `hdiutil create -srcfolder ... -o ...` to create the disk image.
- For distribution DMGs, use a read-only zip-compressed UDIF image (`UDZO`).
- Sign the DMG with a Developer ID Application identity.
- If distributing directly, notarize the outermost container users receive. For a DMG, that means notarize the DMG.
- Staple the notarization ticket to the DMG so Gatekeeper can validate it offline.
- Verify disk image integrity with `hdiutil verify`.

Primary sources:

- Apple: Packaging Mac software for distribution: https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution
- Apple: Notarizing macOS software before distribution: https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
- Apple: Customizing the notarization workflow: https://developer.apple.com/documentation/security/customizing-the-notarization-workflow

## Files Added

- `scripts/build_macos_dmg.py`
- `tests/test_build_macos_dmg.py`

## Local DMG Artifact

Built local unsigned proof artifact:

```text
build/macos/dmg/Universal Media Extractor.dmg
build/macos/dmg/Universal Media Extractor.dmg.sha256
```

Proof report:

```text
proof/commercial_block_9_macos_dmg_readiness/dmg_build_report.md
```

## Current DMG Layout

The DMG staging folder contains:

```text
Universal Media Extractor.app
Applications -> /Applications
```

This gives the user the familiar drag-to-Applications installation pattern.

## Build Commands

Build the `.app` first:

```bash
.venv/bin/python scripts/build_macos_app.py
```

Build local unsigned DMG proof:

```bash
.venv/bin/python scripts/build_macos_dmg.py
```

Dry-run command review:

```bash
.venv/bin/python scripts/build_macos_dmg.py --dry-run
```

Optional future DMG signing command path, after Developer ID is available:

```bash
.venv/bin/python scripts/build_macos_dmg.py \
  --sign-identity "Developer ID Application: Company Name (TEAMID)"
```

## Public Release Flow Later

A public release DMG should use this order:

1. Build production `.app`.
2. Sign `.app` with Developer ID and Hardened Runtime.
3. Verify app signature.
4. Build DMG from the signed app.
5. Sign DMG with Developer ID Application identity.
6. Submit the DMG to Apple notarization via `notarytool`.
7. Staple the ticket to the DMG.
8. Validate stapling and Gatekeeper assessment.
9. Publish DMG plus checksum.

The current script covers steps 4 and checksum generation, plus optional DMG signing command construction. Steps 2, 3, 5, 6, 7, and 8 depend on Apple Developer ID readiness from issue #13.

## Install Instructions

For a signed/notarized public DMG:

1. Open `Universal Media Extractor.dmg`.
2. Drag `Universal Media Extractor.app` to `Applications`.
3. Open the app from `Applications`.
4. On first launch, macOS should identify it as notarized by the developer.

For the current local unsigned proof DMG, macOS may show security warnings. This is expected and is not a public distribution artifact.

## Uninstall Instructions

To uninstall the app later:

1. Quit Universal Media Extractor.
2. Delete `/Applications/Universal Media Extractor.app`.
3. Optional user data cleanup:
   - `~/Library/Application Support/Universal Media Extractor`
   - `~/Downloads/Universal Media Extractor`

Deleting user data also removes job history, analysis cache, and downloaded/transcribed outputs stored in those folders.

## Checksums

The script writes a SHA-256 checksum beside the DMG:

```text
build/macos/dmg/Universal Media Extractor.dmg.sha256
```

Future release pages should publish both the DMG and checksum.

## Why Issue #14 Remains Open

Issue #14 acceptance criteria require:

- DMG contains the signed/notarized app;
- install instructions are clear;
- uninstall behavior is documented;
- checksum/release artifact is produced.

This block satisfies installer readiness, local unsigned DMG proof, documentation, and checksum generation. It does not satisfy the first acceptance item because issue #13 is still blocked by missing Apple Developer ID certificate/notarization credentials.

## Not Included

- No signed/notarized public DMG was produced.
- No Windows build.
- No payments.
- No website.
- No new product features.
- No Chrome extension.
- No AI summary.
- No batch processing.
