# Block 4 Processing UI + MVP Flow

Date: 2026-05-30

## Scope

Block 4 turns the existing analysis, download, and transcription pieces into one understandable MVP UI flow:

```text
Analyze -> Select format -> Confirm rights -> Download -> Transcribe -> Result
```

This block does not add job/progress/cancel, batch processing, Chrome extension, desktop wrapper, AI summary API, auth/database/cookies, React/Vite, CDN assets, advanced download hardening, or roadmap changes.

## Implemented

### Unified UI Flow

The static UI now has a visible MVP flow tracker:

- Analyze;
- Select format;
- Confirm rights;
- Download;
- Transcribe;
- Result.

The tracker updates as the user analyzes a URL, selects a format row, confirms rights, downloads a file, transcribes it, and reaches the generated-files result card.

### Selected Format State

Format rows are already clickable and now show clearer downstream state:

- selected row remains visually highlighted;
- selected format summary appears in the download card;
- `Download selected` stays disabled until a format is selected;
- `Download selected` stays disabled until rights are confirmed;
- selecting a different format resets previous download/transcript result state.

### Whisper Model Selector

The transcript card now includes a Whisper model selector:

- `tiny` - default, fastest;
- `base`;
- `small`;
- `medium`;
- `turbo/default`.

The existing `/transcribe` request already accepted a `model` field, so no new endpoint was needed.

### Transcription Action

After successful download, the UI shows:

- downloaded media file name;
- selected Whisper model;
- `Transcribe` button;
- transcription status/result details.

### Result Card

After successful transcription, the UI shows a generated-files card with:

- output directory;
- media file;
- `transcript.txt`;
- `transcript.md`;
- `transcript.json`;
- `summary_prompt.md`;
- transcript preview;
- `Copy transcript`;
- `Copy summary prompt`;
- `Copy output path`.

Opening a local folder directly from the browser is intentionally not implemented. The UI exposes and copies the output path instead.

## API Integration

Block 4 reuses existing endpoints:

- `POST /analyze`;
- `POST /download`;
- `POST /transcribe`.

No new endpoint was added.

The transcription result model now includes:

- `transcript_text`;
- `summary_prompt_text`.

These fields allow the browser UI to preview/copy generated content without needing filesystem access or a native desktop bridge.

## Error States Preserved

The UI still handles:

- analyze errors;
- download errors;
- transcription errors;
- API unavailable;
- rights not confirmed;
- no selected format;
- missing media file;
- validation/API error responses.

## Manual Verification

Automated tests:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
49 passed
```

Manual API proof on the user-authorized URL:

```text
https://youtu.be/UUdxAp3kuKA
```

Steps performed:

1. `POST /analyze`
2. selected audio-only format `140`
3. `POST /download` with `user_confirmed_rights=true`
4. `POST /transcribe` with model `tiny`
5. verified generated transcript files exist

Proof directory:

```text
proof/block_4/
```

Key proof artifacts:

- `proof/block_4/analyze_response.json`;
- `proof/block_4/analyze_response_pretty.json`;
- `proof/block_4/download_response.json`;
- `proof/block_4/download_response_pretty.json`;
- `proof/block_4/transcribe_response.json`;
- `proof/block_4/transcribe_response_pretty.json`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/transcripts/transcript.txt`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/transcripts/transcript.md`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/transcripts/transcript.json`;
- `proof/block_4/20260530T132006Z_UUdxAp3kuKA/transcripts/summary_prompt.md`.

Visual browser verification was not performed because local Playwright/browser automation was unavailable in this environment (`playwright` module not found).

## Not Included

- job/progress/cancel;
- batch processing;
- Chrome extension;
- desktop wrapper;
- AI summary API;
- auth/database/cookies;
- React/Vite;
- CDN/external assets;
- advanced download hardening;
- native open-folder action.

## Remaining Limits

- Download and transcription remain synchronous local API calls.
- Long downloads/transcriptions can block until the request completes.
- Transcript quality still depends on the selected Whisper model and source audio quality.
- The UI can copy generated content returned by `/transcribe`, but it cannot open local folders without a future desktop/native bridge.
