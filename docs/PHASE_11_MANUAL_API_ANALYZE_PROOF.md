# Phase 11 Manual API Analyze Proof

Date: 2026-05-29

## Scope

Phase 11 manually verified the real local API endpoint `POST /analyze` on the user-authorized URL.

No frontend, downloader, media download, Whisper run, Chrome extension, desktop wrapper, auth, database, or cookies/login was created or used.

## Source

- URL: `https://youtu.be/UUdxAp3kuKA`
- User confirmed this is their video in an earlier phase.
- Operation authorized: analysis only.

## Backend Command

```bash
.venv/bin/python scripts/run_api.py
```

Backend binding:

- `http://127.0.0.1:8000`
- local-only

The server was stopped after the proof.

## Requests Performed

### Health Check

```bash
curl -sS http://127.0.0.1:8000/health
```

Response saved:

- `proof/phase_11/health_response.json`

Response:

```json
{"status":"ok","service":"universal-media-extractor","mode":"local-only"}
```

### Analyze Request

```bash
curl -sS -X POST http://127.0.0.1:8000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"source_type":"url","url":"https://youtu.be/UUdxAp3kuKA","user_confirmed_rights":false}'
```

Responses saved:

- `proof/phase_11/analyze_response.json`
- `proof/phase_11/analyze_response_pretty.json`

### Job Request

```bash
curl -sS http://127.0.0.1:8000/jobs/{job_id}
```

Responses saved:

- `proof/phase_11/job_id.txt`
- `proof/phase_11/job_response.json`
- `proof/phase_11/job_response_pretty.json`

## Result Summary

- HTTP `/health`: `200 OK`
- HTTP `/analyze`: `200 OK`
- HTTP `/jobs/{job_id}`: `200 OK`
- Job status: `succeeded`
- Job task type: `analyze_url`
- Analyze errors: `0`
- Title: `Showreel`
- Duration: `39.0` seconds
- Extractor: `youtube`
- Audio-only options: `3`
- Video-only options: `4`
- Combined video+audio options: `5`
- Subtitles: `0`
- Automatic captions: `0`

## Raw Artifact

The API created a raw analysis artifact through the existing safe analyzer wrapper:

```text
proof/api/analysis_https___youtu_be_UUdxAp3kuKA_20260529T084217Z_c80cb81f/ytdlp_UUdxAp3kuKA_20260529T084220Z.json
```

Approximate size: `55 KiB`.

This artifact is `yt-dlp --simulate --dump-json` output. It is not a media download.

## Safety Confirmation

- Media download performed: `no`
- Whisper run: `no`
- Downloader created/used: `no`
- Frontend created: `no`
- Cookies/login used: `no`
- Auth/database added: `no`
- Server exposed beyond localhost: `no`

## What This Proves

- The local FastAPI app starts on `127.0.0.1`.
- `GET /health` works.
- `POST /analyze` calls the real analysis path.
- The API returns normalized `AnalyzeResult`.
- The API persists raw analysis JSON as an artifact.
- The job record can be retrieved through `GET /jobs/{job_id}` while the server is running.

## Remaining Limits

- This proves analysis only.
- It does not prove media download, merge, conversion, transcription, progress tracking, cancellation, frontend behavior, desktop packaging, extension integration, auth, database, or cookies/login.
- Jobs are still in-memory and disappear when the server stops.
- Real URL support remains best-effort through `yt-dlp`.
