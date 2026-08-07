# UI/UX GPT Pro Context Pack

Date: 2026-08-07

Purpose: package competitor visual references, competitor product logic, and the current Universal Media Extractor state for GPT Pro analysis before another UI/product finalization pass.

This is a research artifact only. It does not change product code, backend logic, frontend behavior, or the roadmap.

## What This Pack Contains

Load these markdown files into GPT Pro together:

1. `docs/UI_UX_GPT_PRO_CONTEXT_PACK.md` - this index and upload guide.
2. `docs/UI_UX_COMPETITOR_VISUAL_LOGIC_PACK.md` - competitor-by-competitor visual and flow notes.
3. `docs/UI_UX_OUR_APP_VISUAL_LOGIC_PACK.md` - current Universal Media Extractor product and UI logic.
4. `docs/UI_UX_GPT_PRO_ANALYSIS_PROMPT.md` - the prompt to paste into GPT Pro.

Attach or reference these screenshot folders:

```text
proof/ui_ux_gpt_pro_pack/competitors/
proof/ui_ux_gpt_pro_pack/our_app/
```

## Screenshot Inventory

### Competitors

```text
proof/ui_ux_gpt_pro_pack/competitors/
  4k-video-downloader-plus/
  downie/
  snapdownloader/
  pulltube/
  mediahuman/
  parabolic/
  stacher/
  cobalt/
  buzz/
  macwhisper/
  ytdlp-app/
  wondershare-uniconverter/
  videoproc/
  hitpaw-univd/
  additional-competitors/
```

The screenshots are public product-page, docs-page, GitHub, or pricing-page references. They are visual references for structure, density, flow language, and commercial packaging. They are not app installs and not endorsements.

Known screenshot gap:

- `yt-dlp.app` FAQ screenshot timed out during capture. The main download/product screenshot is present, and the FAQ remains linked in the competitor pack.

### Our App

```text
proof/ui_ux_gpt_pro_pack/our_app/
  ui_initial.png
  ui_analyze_result.png
  ui_output_selected.png
  ui_local_file_mode.png
  ui_batch_mode.png
  ui_invalid_url_error.png
```

Our app screenshots were captured from the local FastAPI/static UI. The browser smoke used analysis-only mode by default and did not perform media download or transcription.

## Recommended GPT Pro Upload Order

1. Upload this file first.
2. Upload `docs/UI_UX_COMPETITOR_VISUAL_LOGIC_PACK.md`.
3. Upload competitor screenshot folders or a zip of `proof/ui_ux_gpt_pro_pack/competitors/`.
4. Upload `docs/UI_UX_OUR_APP_VISUAL_LOGIC_PACK.md`.
5. Upload our app screenshots or a zip of `proof/ui_ux_gpt_pro_pack/our_app/`.
6. Upload `docs/UI_UX_GPT_PRO_ANALYSIS_PROMPT.md`.
7. Paste the prompt from `docs/UI_UX_GPT_PRO_ANALYSIS_PROMPT.md` as the active instruction.

## What GPT Pro Should Produce

Ask GPT Pro for:

- final public beta app information architecture;
- screen-by-screen UX spec;
- button/action map;
- exact user flow sequence;
- recommended visual direction;
- what belongs in the main UI vs advanced/support;
- how to structure Link / File / Batch flows;
- how Library/history should work;
- how errors, diagnostics, progress, and results should be shown;
- what commercial packaging and upgrade surfaces should exist;
- what public claims must be avoided.

## Research Boundaries

- Use official product pages, official docs, GitHub pages, and public screenshots first.
- Do not install paid competitor apps without explicit user approval.
- Do not copy competitor UI directly.
- Do not position Universal Media Extractor as a universal downloader or DRM/login/paywall bypass tool.
- Keep Udemy/Course mode as internal/experimental, not a public commercial promise.

## Related Existing Project Docs

These existing docs were used as baseline context:

- `docs/UI_UX_COMPETITOR_VISUAL_AUDIT.md`
- `docs/UI_UX_PRODUCT_FUNCTION_INVENTORY.md`
- `docs/UI_UX_REFERENCE_SCREEN_MAP.md`
- `docs/UI_UX_GPT_PRO_BRIEF.md`
- `docs/PRODUCT_FUNCTIONALITY_OVERVIEW.md`
- `docs/PUBLIC_PRODUCT_BOUNDARY.md`
- `docs/PUBLIC_KNOWN_LIMITATIONS.md`
- `docs/PUBLIC_BETA_QA_ROUND.md`
- `docs/PUBLIC_BETA_UI_UX_FINALIZATION_BLUEPRINT.md`
- `docs/PUBLIC_BETA_UI_UX_FINALIZATION_IMPLEMENTATION.md`

## Validation Notes

The pack was validated by checking:

```bash
find proof/ui_ux_gpt_pro_pack -type f
ls docs/UI_UX_*GPT_PRO* docs/UI_UX_*VISUAL_LOGIC*
```

No product code was changed for this research pack.
