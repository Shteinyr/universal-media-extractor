# UI/UX Competitor Visual Audit

Date: 2026-08-07

Purpose: collect visual and UX reference material before `Public Beta UI / UX Finalization`.

This is a research artifact only. It does not change the roadmap and does not implement UI changes.

## Source Priority

The GPT Pro strategy file is the baseline source and must not be ignored:

- `docs/UNIVERSAL_MEDIA_EXTRACTOR_PRODUCT_STRATEGY.md`

Competitors listed there are treated as the required research set. Additional products are included only as supplemental references.

## Required Competitor Set From GPT Pro

| Product | Category | Why It Matters | Official / Primary Visual Reference |
| --- | --- | --- | --- |
| 4K Video Downloader Plus | Paid downloader | Mature commercial downloader with presets, smart mode, library, playlist/channel flows, subtitles, licensing tiers. | https://www.4kdownload.com/products/videodownloader |
| Downie | Paid macOS downloader | Native Mac utility, polished minimal download queue, browser extension workflow, history/support surface. | https://software.charliemonroe.net/help/downie/overview.html |
| SnapDownloader | Paid downloader | Power-user downloader with bulk, scheduler, one-click mode, quality/output controls, dark-mode positioning. | https://snapdownloader.com/features |
| PullTube | Paid macOS downloader | Mac-first drag/drop, browser extension, trim-before-download, simple conversion controls. | https://setapp.com/apps/pulltube |
| MediaHuman YouTube Downloader | Paid/free utility | Clear toolbar model: paste link, start all, remove, format/resolution selectors, tracking, locate file. | https://www.mediahuman.com/howto/user-interface-in-detail5.html |
| Parabolic | Free/open-source yt-dlp GUI | Direct free competitor for basic GUI over `yt-dlp`; useful for settings/dialog density and open-source ergonomics. | https://github.com/NickvisionApps/Parabolic |
| Cobalt | Free web downloader | Extremely low-friction paste-link web UX; useful for input-first simplicity and no-install expectation. | https://cobalt.tools/about/general |
| Stacher | Free/premium yt-dlp GUI | Very close product shape: desktop yt-dlp GUI, library, settings, metadata, queue, pro mode. | https://www.stacher.io/ |
| Buzz | Free/open-source transcription | Shows how local transcription apps structure import, model settings, progress, transcript viewer/export. | https://github.com/chidiwilliams/buzz |
| MacWhisper | Paid transcription | Mature transcription-first app with drag/drop, model choice, export, meeting capture, AI features. | https://www.macwhisper.com/ |

## Supplemental References Found During Search

| Product | Category | Why It Was Added | Official / Primary Reference |
| --- | --- | --- | --- |
| yt-dlp.app | Free/open-source yt-dlp GUI | Directly overlaps with our technical foundation and claims zero setup, self-updating engine, playlists, cookie import, quality badges. | https://yt-dlp.app/ |
| Wondershare UniConverter | All-in-one media toolbox | Useful for studying feature navigation across converter, downloader, compressor, editor, subtitles, AI tools. | https://uniconverter.wondershare.com/ |
| VideoProc Converter / VideoProc | All-in-one media toolbox | Useful for observing toolbox-style packaging: converter, downloader, recorder, AI tools, batch processing. | https://www.videoproc.com/ |
| HitPaw Video Converter / Univd | All-in-one media toolbox | Useful for common mass-market flow language: add URL/file, choose format, start, batch, subtitles, converter presets. | https://www.hitpaw.com/video-converter.html |

## Visual Patterns To Study

- Input-first workflow: paste URL or drop file first, then analyze/parse, then choose output.
- Presets instead of raw formats: Smart Mode, One-Click Mode, quality presets, output format selectors.
- Queue/library as product value: status, retry, history, reveal/open result.
- Download result as a saved file, not a technical job.
- Transcription as post-processing after a file exists.
- Safety/legal copy present but quiet; full details belong in support/limitations docs.

## What Not To Copy

- Proxy/geobypass claims from competitor pages.
- “Download everything / any site / any protected content” language.
- Huge all-in-one toolbox navigation from UniConverter/HitPaw/VideoProc.
- Long technical option grids.
- Public Udemy/course downloader positioning.
- UI that exposes raw engine arguments to normal users.

## Recommended Visual Direction

```text
Compact local desktop utility
File-manager/downloader style
Input-first
Preset-driven
Queue/history aware
Plain language errors
Advanced details hidden
```

Useful adjectives:

- local;
- clean;
- practical;
- trustworthy;
- compact;
- file-oriented;
- not "AI magic";
- not "hacker tool".
