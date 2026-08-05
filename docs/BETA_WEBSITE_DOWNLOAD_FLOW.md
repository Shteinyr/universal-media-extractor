# Beta Website / Download Flow

Status: public beta packaging draft. No production website, checkout, licensing, installer signing, or core app behavior was changed.

## Purpose

This document defines the public beta website and download flow for Universal Media Extractor. It is meant to be reused later in the real landing page, release page, onboarding copy, support page, and public beta announcement.

The goal is to make the product understandable before the user downloads it:

- what the app does;
- who it is for;
- what platforms are planned;
- what is available now versus later;
- what the app does not promise;
- how beta users should safely start;
- how support and diagnostics should work.

## Public Positioning

Product name:

```text
Universal Media Extractor
```

Category:

```text
Local Media Downloader & Organizer for macOS and Windows
```

Short promise:

```text
Save accessible media, audio, subtitles, and transcripts into organized local folders without uploading source files to a cloud service.
```

One-line website description:

```text
A local desktop app for analyzing media links and local files, saving clean outputs, and creating local Whisper transcripts when you need them.
```

## Audience

Primary users:

- creators archiving their own videos, audio, and captions;
- editors who need clean local media files for projects;
- students and researchers saving allowed reference material for offline work;
- knowledge workers who need local transcripts without cloud upload;
- small teams that prefer local processing and predictable output folders.

The product is not positioned for piracy, bypassing platform restrictions, or downloading protected content.

## Website Information Architecture

Recommended first public beta site structure:

1. Hero
2. How it works
3. Core workflows
4. Download / beta availability
5. Privacy and local processing
6. Limitations and source support
7. Plans / early access
8. Support and diagnostics
9. Legal footer

Do not create a complex marketing site before signed builds and provider approval are ready. The first version should be clear, conservative, and trust-building.

## Hero Section Draft

Eyebrow:

```text
Local Media Downloader & Organizer
```

Headline:

```text
Save media locally. Keep it organized.
```

Subheadline:

```text
Analyze a link or local file, choose a clean output, save allowed media, and create local transcripts when you need them.
```

Primary CTA before installers exist:

```text
Join the beta
```

Primary CTA after a signed build exists:

```text
Download for macOS
```

Secondary CTA:

```text
View limitations
```

Trust note:

```text
No source media upload is required. Processing runs on your computer.
```

## How It Works Section

Recommended copy:

```text
1. Paste a supported link or choose a local audio/video file.
2. The app analyzes available outputs before saving anything.
3. Choose Video, Audio, Subtitles, or Transcript.
4. Save files into an organized local folder.
5. Transcribe locally with Whisper when useful.
```

Keep the flow product-level. Do not expose `yt-dlp`, `ffmpeg`, or Whisper implementation details in the primary marketing sections except in a small technical note.

## Core Workflow Cards

### Analyze Before Saving

```text
Inspect a supported media link or local file before download or transcription.
```

### Download Organized Outputs

```text
Save video, audio, or subtitles into readable local folders with safe names and duplicate handling.
```

### Transcribe Locally

```text
Create TXT, Markdown, or JSON transcripts with local Whisper processing.
```

### Keep Control

```text
Choose the source, output folder, format, and transcript format. Files stay on your computer by default.
```

## Download Section

The download section must be honest about the current build state.

### Current Public Beta State

```text
Public beta builds are being prepared. The current app runs locally for development and testing, but public installers are not ready yet.
```

### macOS Copy

Before Developer ID signing and notarization:

```text
macOS Apple Silicon beta is planned after Developer ID signing and notarization are complete.
```

After a signed build exists:

```text
Download the signed macOS beta. Requires macOS on Apple Silicon. Intel support can be evaluated separately.
```

Button states:

- `Join beta` while installers are not ready;
- `Download macOS Beta` when signed/notarized artifact exists;
- `View release notes` for GitHub release artifacts;
- `Report an issue` for beta feedback.

### Windows Copy

Before Windows build exists:

```text
Windows beta is planned after the macOS public beta path is stable.
```

After a Windows build exists:

```text
Download the Windows beta for Windows 10/11 x64.
```

Button states:

- `Join Windows waitlist` before build;
- `Download Windows Beta` when installer exists;
- `Follow Windows progress` while packaging is being prepared.

## Early Access / Waitlist CTA

Use this before checkout/licensing exists:

```text
Want to test the beta? Join the early access list and get notified when signed macOS and Windows builds are ready.
```

CTA label options:

- `Join beta list`
- `Get beta updates`
- `Request early access`

Fields for a simple waitlist form later:

- email;
- platform: macOS / Windows / both;
- use case: creator / editor / student / researcher / business / other;
- optional feedback text.

Do not collect payment information until the payment provider path is approved.

## Plans Section Copy

Current public copy should describe pricing as draft or upcoming, not active checkout.

```text
Pricing is being prepared for a founder beta. Checkout and license activation are not live yet.
```

Draft plan labels:

- Free: test basic local workflows;
- Founder Pro: early discounted Pro access once builds and checkout are ready;
- Pro: full single-user local workflow;
- Business: business terms and support path.

Avoid saying that paid plans are purchasable until checkout and licensing actually exist.

## Privacy / No-Cloud Copy

Primary copy:

```text
Universal Media Extractor is local-first. Media processing runs on your computer, and source files are not uploaded to a cloud service by default.
```

Support copy:

```text
If you share diagnostics, use the redacted diagnostics bundle. Do not share passwords, cookies, tokens, transcripts, private URLs, or local file paths.
```

Website bullets:

- local FastAPI backend bound to `127.0.0.1`;
- local static UI / desktop wrapper;
- downloads and transcripts saved on the user's machine;
- diagnostics are redacted by default;
- no stored passwords or account credentials.

Do not promise that third-party engines never make network requests. URL analysis/download by definition contacts the source platform.

## Limitations Copy

Required limitation block:

```text
Use Universal Media Extractor only with media you own, created, or have permission to download and process. Source support is best-effort and may change when platforms change. The app does not bypass DRM, CAPTCHA, paywalls, login restrictions, regional restrictions, or access controls.
```

Short version for footer or download page:

```text
Best-effort source support. No DRM, CAPTCHA, paywall, login, or access-control bypass.
```

## Support / Diagnostics Copy

Support section:

```text
If a job fails, copy the redacted diagnostics bundle from the app and include it with your beta report. Diagnostics are designed to avoid cookies, tokens, transcripts, full URLs, and private local paths.
```

Recommended support links:

- Known Limitations;
- Privacy;
- EULA;
- Refund Policy;
- GitHub Issues or beta feedback form;
- Release notes.

Support should help with:

- installation;
- launch failures;
- local server/app behavior;
- output folder issues;
- normalized errors;
- diagnostics bundles;
- source compatibility where allowed and practical.

Support should not help with:

- DRM bypass;
- CAPTCHA bypass;
- paywall bypass;
- extracting cookies/tokens/keys;
- downloading content without permission.

## Internal / Experimental Feature Boundary

Udemy Course Mode remains internal/experimental and should not be used in public website promises.

Public site should not say:

- `Download Udemy courses`;
- `Download paid courses`;
- `Works with every learning platform`;
- `Bypass login or course restrictions`.

If Course Mode is available in internal builds, it should remain hidden in public builds with:

```bash
UME_PUBLIC_PRODUCT_MODE=1
```

## Copy To Avoid

Do not use:

- `downloads everything`;
- `universal downloader for any site`;
- `works with every website`;
- `download any paid course`;
- `bypass restrictions`;
- `guaranteed platform support`;
- `unlimited batch processing` before public beta validation;
- `AI summaries included` before a real AI summary feature exists.

## Public Beta Download Flow

### Before Builds Are Ready

1. User lands on website.
2. User sees macOS/Windows beta status.
3. User joins early access / waitlist.
4. User can read limitations, privacy, support, and roadmap status.
5. No installer download is shown as available.

### After macOS Signed Build Exists

1. User clicks `Download macOS Beta`.
2. Download page shows version, date, checksum, system requirements, and limitations.
3. User downloads signed/notarized `.dmg`.
4. User opens the app and sees onboarding / local-first safety copy.
5. User starts with one small link or file.
6. If a job fails, user copies diagnostics and reports beta feedback.

### After Windows Build Exists

1. User clicks `Download Windows Beta`.
2. Download page shows version, date, checksum, Windows 10/11 x64 requirements, and limitations.
3. User downloads signed installer when available.
4. User follows the same first-run beta onboarding and diagnostics path.

## Download Page Checklist

Each public build download page should include:

- product version;
- release date;
- platform and architecture;
- file size;
- checksum;
- signed/notarized status for macOS;
- signed installer status for Windows;
- system requirements;
- known limitations link;
- privacy link;
- support/diagnostics link;
- changelog/release notes link;
- uninstall instructions link.

## Website Sections Ready For Transfer

Recommended transfer order into a real site:

1. Hero from this doc.
2. How it works.
3. Core workflow cards.
4. Download/beta availability.
5. Privacy/no-cloud.
6. Limitations.
7. Plans/early access.
8. Support/diagnostics.
9. Footer legal links.

## Current Implementation Note

A static founder launch site draft already exists under:

```text
site/
```

This document does not deploy it or turn it into a production website. It defines the public beta copy and download logic that can later be applied to that site or another hosting target.

## Verification

Docs-only block. No core app code was changed.

Recommended verification:

```bash
git diff --check
git diff --stat
```
