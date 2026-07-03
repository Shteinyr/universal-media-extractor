# v0 UI Reference Audit

Date: 2026-05-30

## Status

Completed before the UI port.

This audit treats the downloaded v0 UI as a visual and UX reference only. It does not create a new roadmap block and does not replace the working FastAPI/static frontend app.

## Location

Expected user-provided path:

```text
/Users/aleksandr/Documents/Codex/Projects/universal-media-extractor/media-extractor-ui
```

Actual path found locally:

```text
/Users/aleksandr/Documents/Codex/universal-media-extractor/media-extractor-ui
```

The reference was read from the actual path above.

## Stack Found

The v0 project is a separate frontend app using:

- Next.js App Router with `app/layout.tsx` and `app/page.tsx`;
- React 19 components;
- TypeScript;
- Tailwind CSS v4;
- shadcn/ui-style component source under `components/ui/`;
- Radix UI dependencies;
- lucide-react icons;
- Vercel analytics dependency;
- mock data and simulated state.

Key files:

- `components/media-extractor/media-extractor-app.tsx`
- `components/media-extractor/sidebar.tsx`
- `components/media-extractor/main-content.tsx`
- `components/media-extractor/media-card.tsx`
- `components/media-extractor/output-selector.tsx`
- `components/media-extractor/options-list.tsx`
- `components/media-extractor/download-panel.tsx`
- `components/media-extractor/transcription-panel.tsx`
- `components/media-extractor/result-panel.tsx`
- `components/media-extractor/mock-data.ts`
- `app/globals.css`

## Documentation Notes

Context7 confirmed that Next.js App Router projects organize shared UI through `app/layout.tsx` and pages through `app/page.tsx`, with React components composing the interface.

Context7 confirmed Tailwind is utility-first styling in markup/class names, so the reference layout should be translated into plain CSS rules for the current static UI rather than copied as Tailwind utilities.

Context7 confirmed shadcn/ui is open component source built with TypeScript, Tailwind CSS, and Radix/Radix-like primitives. That makes it useful as a pattern reference, but copying it directly would import a React/Tailwind/Radix component architecture that the current MVP does not need.

## Useful UX Patterns

- Fixed compact sidebar instead of a large marketing-like intro panel.
- Small title bar and mode toggle.
- Input and Analyze action grouped tightly.
- Local backend status as a small utility status row.
- Flow checklist as a compact progress rail.
- Recent results as compact file rows with badges/actions.
- Main content centered with a narrow working column.
- Media item card with thumbnail, title, source, duration, uploader, and source link.
- Output selector as a segmented `Audio / Video / Subtitles` control.
- Format options as single-line selectable rows.
- Download, transcription, and result panels as short task cards.
- Result files displayed like a small file manager grid/list.

## Not Portable Directly

- The Next.js app itself is mock-driven and does not call the real FastAPI endpoints.
- React state and components are not copied into the current vanilla JS app.
- Tailwind class strings are not copied directly.
- shadcn/ui components are not installed or imported into the main project.
- lucide-react icons are not imported because the current app has no React build step.
- Vercel analytics is not carried over.
- The v0 mock data is not used for real app state.

## Current Vanilla UI Boundary

The main project remains:

- FastAPI backend;
- static HTML/CSS/vanilla JS frontend;
- current local-only endpoints:
  - `POST /analyze`;
  - `POST /download`;
  - `POST /transcribe`;
  - `GET /jobs/{job_id}`;
  - `POST /jobs/{job_id}/cancel`;
  - `GET /outputs`;
  - `DELETE /outputs/{output_id}`;
  - local file endpoints.

## Transfer Decision

Transfer the UX structure and visual density, not the framework:

- keep existing IDs and JS wiring;
- restyle the layout as a compact downloader/file-manager utility;
- keep simplified/deduplicated output options;
- preserve URL and local file flows;
- preserve job polling, cancel, recent results, safe delete, and copy actions.
