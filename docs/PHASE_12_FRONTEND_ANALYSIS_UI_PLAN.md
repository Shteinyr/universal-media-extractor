# Phase 12 Frontend Analysis UI Plan

Date: 2026-05-29

## Scope

Phase 12 plans the first analysis-result display UI only. It does not create a frontend app, UI code, downloader, media download, Whisper run, extension, desktop wrapper, auth, database, cookies, or API changes.

The plan is based on the real Phase 11 API response in:

```text
proof/phase_11/analyze_response_pretty.json
```

## 1. Goal Of The First UI

The first UI should let the user:

- open a local web app;
- paste a URL;
- click `Analyze`;
- see a normalized `AnalyzeResult`;
- understand available audio/video/subtitle options;
- see warnings and errors clearly.

The first UI must not:

- download media;
- transcribe media;
- select final processing actions;
- ask for cookies/login;
- expose online-service behavior.

The intended loop is:

```text
Open local UI -> paste URL -> Analyze -> display normalized result
```

## 2. Layout

Design direction:

- minimalist local utility;
- Finder/Raycast/Linear-style calm work surface;
- dense, readable, and practical rather than marketing-like;
- auto light/dark can come later;
- one simple screen for the first prototype.

Recommended layout:

- left panel: URL input, Analyze button, local-only status, legal/safety note;
- right panel: result card, format groups, warnings, errors;
- no settings clutter;
- no landing page;
- no hero section;
- no decorative cards or promotional copy.

The interface should feel like a quiet local tool for inspecting media source capabilities.

## 3. First Screen

Visible before analysis:

- project title: `Universal Media Extractor`;
- URL input;
- `Analyze` button;
- short supported-sources note: analysis is best-effort through local `yt-dlp`;
- local-only note: backend expected at `127.0.0.1`;
- legal note: analysis does not download media.

Do not include:

- settings page;
- downloader controls;
- transcription controls;
- cookies/login controls;
- local file upload;
- batch controls;
- extension entry points.

## 4. Loading State

State name: `analyzing`.

Behavior:

- show the URL being analyzed;
- disable the Analyze button;
- keep the input readable;
- show a simple loading indicator;
- do not show fake percent progress;
- optionally show text: `Analyzing source...`;
- if the request is slow, keep the UI steady rather than adding speculative stages.

The backend is synchronous in Phase 10/11, so the UI should treat `POST /analyze` as a request/response operation for the first prototype.

## 5. Result State

Show these fields from `result`:

- `thumbnail_url`;
- `title`;
- `duration_label` or `duration_seconds`;
- `source_type`;
- `extractor`;
- `extractor_key`;
- `webpage_url`;
- `uploader.name`;
- `uploader.channel_name`;
- `availability`;
- `access_state`.

For the Phase 11 proof response, the UI should display:

- title: `Showreel`;
- duration: `0:39`;
- extractor: `youtube`;
- uploader: `Aleksandr Shtein`;
- thumbnail: YouTube maxres thumbnail;
- audio formats: `3`;
- video-only formats: `4`;
- combined formats: `5`;
- subtitles: empty;
- automatic captions: empty.

Result sections:

- source summary card;
- audio formats group;
- video-only formats group;
- combined video+audio formats group;
- subtitles empty state;
- automatic captions empty state;
- warnings panel;
- errors panel only if `errors.length > 0`.

## 6. Format Display

For each `MediaOption`, show:

- `display_label`;
- `format_id`;
- `type`;
- `ext` or `container`;
- `resolution` for video/combined options;
- `audio_codec`;
- `video_codec`;
- `filesize` or `filesize_approx` if available;
- `is_default_recommended` badge when true.

Recommended display order:

1. Recommended option first if present.
2. Then sort by practical quality:
   - audio: bitrate or original order;
   - video/combined: height then fps.
3. Keep advanced codec details secondary but visible in a compact row.

Do not include download/select buttons in Phase 13. Rows may look selectable later, but no processing action should be enabled.

## 7. Empty States

No subtitles:

- show a neutral empty row: `No manual subtitles detected.`

No automatic captions:

- show a neutral empty row: `No automatic captions detected.`

Unsupported source:

- show a blocking error from `result.errors`;
- suggest trying a public supported URL;
- do not claim universal support.

Login/cookies required:

- show that the source requires access not implemented in this prototype;
- do not ask for credentials;
- do not provide a cookies upload UI.

Analysis failed:

- show `ErrorState.message`;
- show `suggested_user_action` when present;
- keep `technical_details` collapsed or hidden in the first prototype.

## 8. Legal And Safety

Show a small note near the Analyze button:

```text
Analysis only. This does not download media.
```

Also show:

```text
Download or processing actions, when added later, will require confirmation that you own the media or have the rights to process it.
```

Do not show a confirmation checkbox yet unless it is visually marked as future-only. The first UI has no protected action to confirm.

## 9. API Integration

Frontend calls:

```http
POST http://127.0.0.1:8000/analyze
Content-Type: application/json
```

Request shape:

```json
{
  "source_type": "url",
  "url": "https://youtu.be/UUdxAp3kuKA",
  "user_confirmed_rights": false
}
```

Response shape:

```json
{
  "job": {
    "job_id": "job-...",
    "task_type": "analyze_url",
    "status": "succeeded",
    "payload": {},
    "created_at": "...",
    "updated_at": "...",
    "error": null
  },
  "result": {
    "schema_version": "1.0",
    "analysis_id": "...",
    "source_url": "...",
    "title": "...",
    "media_options": {},
    "warnings": [],
    "errors": []
  }
}
```

Error handling:

- network failure: show `Local API is not reachable. Start the backend on 127.0.0.1.`;
- HTTP validation error: show invalid URL/request message;
- `result.errors.length > 0`: show source-level errors and mark result as failed;
- `job.status === "failed"`: show job error summary;
- keep raw technical details out of the main view.

Backend base URL:

- default run config: `http://127.0.0.1:8000`;
- `scripts/run_api.py` supports `--port`, so the UI should eventually keep base URL configurable in code;
- Phase 10 runtime health proof used port `8765` only for a temporary health check;
- Phase 11 manual API proof used the default `8000`.

No mismatch blocks Phase 13. The recommended first UI should target `http://127.0.0.1:8000`.

## 10. Tech Decision

Recommendation: static HTML/CSS/vanilla JS served by FastAPI static files in a later phase.

Why:

- lowest dependency cost;
- no build pipeline;
- enough for one screen and one `fetch()` call;
- easy to keep local-only;
- can be served by the existing FastAPI process later;
- keeps Phase 13 focused on validating the real API-to-display loop.

Alternative: small Vite app.

Trade-offs:

- better developer experience once UI grows;
- adds Node/tooling and a separate dev server;
- more moving parts than needed for a first analysis-only prototype.

Decision for Phase 13 planning:

- start with static HTML/CSS/vanilla JS;
- defer Vite until the UI needs state management, routing, component tooling, or a more complex app surface.

## 11. Acceptance Criteria For Future Phase 13

Future Phase 13 is acceptable only if:

- user can open a local UI;
- user can paste a URL;
- user can click Analyze;
- UI calls the real `POST /analyze`;
- UI displays the real `AnalyzeResult`;
- UI shows source summary, media format groups, warnings, empty subtitles/captions states, and errors if present;
- no media download happens;
- Whisper does not run;
- existing tests still pass;
- Browser check screenshot is captured if available;
- backend remains local-only on `127.0.0.1`.

## Phase 12 Stop Gate

Stop after planning. Do not create frontend files until Phase 13 is explicitly authorized.
