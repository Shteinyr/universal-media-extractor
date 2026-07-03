# Block 7. Local File Input

Date: 2026-05-30

## Status

Completed.

Block 7 adds a local-file flow that does not use `yt-dlp` or a remote URL:

```text
Local audio/video file -> ffprobe metadata -> Whisper job -> transcript/result
```

## Implemented

- Added local file models:
  - `LocalFileAnalyzeResult`
  - `LocalFileStreamInfo`
  - `LocalMediaType`
- Added `LocalFileMetadataService` using `ffprobe`.
- Added `OutputManager.create_local_file_output_dir(...)`.
- Added `POST /local/analyze`.
- Added `POST /local/transcribe`.
- Added UI mode switch:
  - URL mode;
  - Local file mode.
- Added local file metadata card in the UI.
- Added local file transcription action with Whisper model selection.
- Reused the existing in-memory job system for local transcription.
- Reused the existing `TranscriptionService` for audio and video transcription.

## Endpoints

### `POST /local/analyze`

Accepts one uploaded file as multipart form data:

```text
file=<audio/video file>
```

Behavior:

- creates a project-local output directory;
- saves the uploaded file under `source/`;
- runs `ffprobe`;
- returns normalized metadata;
- does not run Whisper;
- does not call `yt-dlp`;
- does not send the file to external services.

Returned metadata includes:

- original filename;
- saved internal path;
- output directory;
- media type: `audio`, `video`, or `unknown`;
- duration;
- size in bytes;
- format name;
- stream codec data;
- warnings/errors.

### `POST /local/transcribe`

Accepts JSON referencing the saved file from `/local/analyze`:

```json
{
  "saved_file_path": "/absolute/path/to/source/file.wav",
  "output_dir": "/absolute/path/to/output",
  "user_confirmed_rights": true,
  "model": "tiny",
  "source_kind": "audio"
}
```

Behavior:

- creates an in-memory `transcribe` job;
- accepts only a saved file path that exists inside the configured output folder;
- runs the existing transcription pipeline in a background thread;
- audio files go directly to Whisper;
- video files use the existing ffmpeg audio extraction path before Whisper;
- final result is available through `GET /jobs/{job_id}`.

## Output Structure

Local file workflows use:

```text
outputs/local_<timestamp>_<safe_filename>/
  source/
    <uploaded original file copy>
  media/
    extracted_audio.wav        # only for video inputs
  metadata/
    local_file_analysis.json
    transcription_request.json
    transcription_result.json
  logs/
    local_file_analysis.log
    transcription.log
  transcripts/
    transcript.txt
    transcript.md
    transcript.json
    summary_prompt.md
    <whisper native files>
```

## UI Behavior

Local file mode provides:

- file picker for audio/video;
- selected file name/size;
- `Analyze local file`;
- metadata card;
- rights confirmation checkbox;
- Whisper model selector;
- `Transcribe local file`;
- local transcription job status;
- transcript preview;
- generated files card;
- copy transcript, copy summary prompt, and copy output path.

## Safety

- Files stay local.
- No external API is used.
- No remote URL is accepted in local mode.
- `yt-dlp` is not used for local mode.
- Backend remains local-only.
- Transcription requires `user_confirmed_rights=true`.
- Uploaded files are copied only into the project output structure.
- `/local/transcribe` rejects saved file paths outside the configured output folder.

## Tests

Command:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
59 passed
```

Coverage added:

- local file metadata service with mocked `ffprobe`;
- invalid local file metadata handling;
- local output structure creation;
- `/local/analyze` upload behavior;
- `/local/analyze` empty upload rejection;
- `/local/transcribe` job behavior with mocked transcription service;
- `/local/transcribe` missing file rejection;
- `/local/transcribe` rejection for paths outside the configured output folder;
- static UI labels and endpoint wiring.

## Manual Proof

Created a synthetic local audio file:

```bash
ffmpeg -y -f lavfi -i sine=frequency=440:duration=2 -ac 1 -ar 16000 proof/block_7/synthetic_sine.wav
```

Proof flow:

```text
GET /health
POST /local/analyze with synthetic_sine.wav
POST /local/transcribe with saved_file_path from analysis
poll GET /jobs/{job_id}
verify transcript artifacts
```

Proof artifacts:

```text
proof/block_7/health.json
proof/block_7/synthetic_sine.wav
proof/block_7/local_analyze_response.json
proof/block_7/local_transcribe_job_start.json
proof/block_7/local_transcribe_job_final.json
proof/block_7/output_review.json
```

Output:

```text
outputs/local_20260530T134814Z_synthetic_sine/
```

Verified files:

```text
outputs/local_20260530T134814Z_synthetic_sine/source/synthetic_sine.wav
outputs/local_20260530T134814Z_synthetic_sine/transcripts/transcript.txt
outputs/local_20260530T134814Z_synthetic_sine/transcripts/transcript.md
outputs/local_20260530T134814Z_synthetic_sine/transcripts/transcript.json
outputs/local_20260530T134814Z_synthetic_sine/transcripts/summary_prompt.md
```

The synthetic sine wave is not speech, so transcript quality is not meaningful. This proof verifies local file handling, metadata extraction, Whisper execution, job polling, and artifact generation.

## Not Included

- Batch processing.
- Chrome extension.
- Desktop wrapper.
- AI summary API.
- Auth/database/cookies.
- Redis/Celery/external queue.
- React/Vite/CDN.
- Advanced cancellation.
- Roadmap changes.
- Advanced local file library/history.
- Direct folder opening from browser.
