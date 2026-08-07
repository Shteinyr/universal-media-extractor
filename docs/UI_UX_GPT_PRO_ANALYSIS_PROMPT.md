# GPT Pro Analysis Prompt

Use this prompt after uploading:

1. `docs/UI_UX_GPT_PRO_CONTEXT_PACK.md`
2. `docs/UI_UX_COMPETITOR_VISUAL_LOGIC_PACK.md`
3. `proof/ui_ux_gpt_pro_pack/competitors/`
4. `docs/UI_UX_OUR_APP_VISUAL_LOGIC_PACK.md`
5. `proof/ui_ux_gpt_pro_pack/our_app/`

## Prompt

You are a senior product designer, UX researcher, and commercial desktop software strategist.

Analyze the attached context for Universal Media Extractor and its competitors.

Universal Media Extractor is intended to become a paid local desktop utility for macOS and Windows:

```text
Local Media Downloader & Organizer for macOS and Windows
```

It is not an online downloader service, not a cloud transcription product, and not a DRM/paywall/CAPTCHA/login bypass product.

Current core product flows:

```text
Link -> Analyze -> Choose output -> Download -> optional Transcribe -> Result
Local file -> Analyze -> Transcribe -> Result
Batch list -> Import/select -> Download queue -> Retry failed
```

Internal/experimental flow:

```text
Udemy/Course mode
```

Udemy/Course mode must remain hidden from public commercial positioning unless separately approved.

## Your Tasks

1. Study the competitor pack and screenshots.
2. Study the current Universal Media Extractor pack and screenshots.
3. Find 3-7 additional relevant competitors or references yourself, prioritizing:
   - desktop video downloaders;
   - yt-dlp GUIs;
   - media converters;
   - local transcription apps;
   - local-first file/media utilities.
4. Compare all competitors against Universal Media Extractor.
5. Recommend the final public beta UI/UX structure.
6. Recommend the commercial packaging and public product framing.

## Questions To Answer

### Product Structure

- Should the app use explicit `Link / File / Batch` modes, or one universal source input?
- What should the first screen show?
- What should be removed from the first screen?
- Should Library/history be visible by default, hidden, or placed in a separate screen?
- Should transcription live in the main flow, in result actions, or as a separate mode?

### Output Selection

- What exact output presets should exist?
- Should output choice be cards, segmented tabs, dropdowns, rows, or a compact command-style picker?
- Where should save location appear?
- Where should output format appear?
- How should subtitles be represented?
- How should video imply one final video+audio file?

### Workflow

- Define the ideal flow for a first-time user downloading one video.
- Define the ideal flow for audio-only download.
- Define the ideal flow for local file transcription.
- Define the ideal flow for batch URL processing.
- Define the ideal flow for a failed source.
- Define the ideal flow for a saved result.

### Buttons And Actions

Create a complete button/action map:

- primary buttons;
- secondary buttons;
- destructive buttons;
- copy/reveal actions;
- retry/cancel actions;
- advanced/support actions;
- buttons to remove or hide.

### Visual Direction

Recommend a visual direction:

- layout;
- density;
- sidebar/topbar decision;
- card/list usage;
- typography hierarchy;
- dark/light behavior;
- empty states;
- result states;
- progress states;
- error states.

The preferred direction is compact, local, file-manager/downloader style. Avoid marketing-dashboard UI, developer console UI, and large technical format lists.

### Commercial UX

Recommend:

- Free vs Pro boundary;
- upgrade surfaces;
- what should be public beta only;
- what should be Pro later;
- how to frame local-first privacy;
- how to frame limitations safely;
- what public claims must be avoided.

Do not recommend positioning the product as "downloads everything" or as bypassing DRM, private access, CAPTCHA, login, paywalls, or platform rules.

## Required Output

Return a structured report with:

1. Executive recommendation.
2. Final information architecture.
3. Screen-by-screen UX spec.
4. Button/action map.
5. Final core user flows.
6. Output preset model.
7. Library/history model.
8. Error/progress/result model.
9. Settings/advanced model.
10. Commercial packaging recommendations.
11. What to remove from the current app.
12. What to keep.
13. What to postpone.
14. Top 10 implementation priorities.
15. Risks and non-goals.

Be specific enough that an engineer can implement the UI without guessing.
