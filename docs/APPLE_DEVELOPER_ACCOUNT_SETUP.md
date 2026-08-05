# Apple Developer Account Setup

Purpose: show exactly what the user must do before Codex can finish public macOS signing and notarization.

## What Apple Requires

For direct macOS distribution outside the Mac App Store, Apple expects Developer ID signing and notarization. Apple Developer Program enrollment is required to create Developer ID certificates.

Official references:

- Enrollment: https://developer.apple.com/programs/enroll/
- Developer ID: https://developer.apple.com/developer-id/
- Developer ID certificates: https://developer.apple.com/help/account/certificates/create-developer-id-certificates/
- Notarization workflow: https://developer.apple.com/documentation/security/customizing-the-notarization-workflow

## Step 1: Enroll

Choose one path:

- Individual / sole proprietor.
- Organization.

Individual enrollment requires an Apple Account with two-factor authentication and legal identity details.

Organization enrollment requires legal authority, legal entity details, D-U-N-S Number, work email, phone, and a public website associated with the organization.

Apple Developer Program membership is paid yearly. Apple currently lists the membership as 99 USD per membership year, with local pricing shown during enrollment.

## Step 2: Find Team ID

After enrollment:

1. Sign in to Apple Developer.
2. Open membership/account details.
3. Copy the 10-character Team ID.

Record locally for release commands:

```text
TEAM_ID=<your team id>
```

Do not commit this to repo files unless intentionally public.

## Step 3: Create Developer ID Application Certificate

Use Apple Developer account:

1. Open Certificates, Identifiers & Profiles.
2. Open Certificates.
3. Add a certificate.
4. Under Software, choose Developer ID.
5. Choose `Developer ID Application`.
6. Follow Apple's certificate signing request flow.
7. Download the `.cer` file.
8. Double-click it to install into Keychain Access.

Apple notes that `Developer ID Application` signs Mac apps and disk images; `Developer ID Installer` is for installer packages.

## Step 4: Verify Certificate Locally

Run:

```bash
security find-identity -v -p codesigning
```

Expected to see a line like:

```text
"Developer ID Application: Company Name (TEAMID)"
```

Then run:

```bash
cd "/Users/aleksandr/Developer/Codex/Projects/Universal Media Extractor"
.venv/bin/python scripts/check_macos_signing_readiness.py
```

Expected:

- Developer ID Application identity found.
- Signing/notarization tools found.

## Step 5: Create App-Specific Password

For Apple ID based notarization, create an app-specific password for `notarytool`.

Use it only when prompted by `notarytool store-credentials`.

Never send it to Codex in chat and never put it in a file.

## Step 6: Store Notary Credentials In Keychain

Run:

```bash
cd "/Users/aleksandr/Developer/Codex/Projects/Universal Media Extractor"
.venv/bin/python scripts/store_macos_notary_credentials.py \
  --apple-id "APPLE_ID_EMAIL" \
  --team-id "TEAMID" \
  --profile UME_NOTARY
```

The command prompts interactively for the app-specific password. The script does not accept a password argument and does not write credentials into the project.

## Data Codex Needs Later

Safe to provide:

- Apple ID email used for notarization.
- Team ID.
- Signing identity string from `security find-identity`.
- Notary keychain profile name, for example `UME_NOTARY`.

Do not provide:

- Apple ID password.
- App-specific password.
- `.p8` private key.
- Keychain export.
- Certificate private key.

## Ready Signal For Codex

Send something like:

```text
Apple Developer setup is ready.
Team ID: XXXXXXXX
Signing identity: Developer ID Application: Name (TEAMID)
Notary keychain profile: UME_NOTARY
Proceed with macOS signing/notarization validation.
```

Then Codex can attempt the real #13/#14 validation flow.
