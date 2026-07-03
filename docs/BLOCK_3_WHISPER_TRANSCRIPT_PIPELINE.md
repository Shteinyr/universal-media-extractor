# Block 3 Whisper + Transcript Pipeline

Date: 2026-05-30

## Scope

Block 3 adds local transcription for already downloaded audio/video files.

Implemented flow:

```text
downloaded audio/video file -> optional ffmpeg audio extraction -> Whisper CLI -> transcript artifacts -> summary_prompt.md
```

This block does not add AI summary API calls, Chrome extension, desktop wrapper, batch processing, cookies/login, or advanced download hardening.

## Implemented

- `TranscriptionRequest`, `TranscriptionResult`, `SourceMediaKind`, and `TranscriptionStatus` models.
- `TranscriptionService.transcribe_file(request)`.
- `POST /transcribe` endpoint.
- Video input support through `ffmpeg` extraction to `media/extracted_audio.wav`.
- Audio input support through direct Whisper CLI transcription.
- Static UI extension after successful download:
  - show transcript panel;
  - transcribe the first downloaded file;
  - show transcript artifact paths and errors.
- Tests for audio transcription, video audio extraction, safety blocking, Whisper failure, API behavior, and output structure.

## Output Structure

For downloaded files, transcription artifacts are written into the same output directory:

```text
outputs/<timestamp>_<safe_title_or_video_id>/
  media/
    <downloaded media>
    extracted_audio.wav        # only for video inputs
  metadata/
    download_request.json
    download_result.json
    transcription_request.json
    transcription_result.json
  logs/
    download.log
    transcription.log
  transcripts/
    transcript.txt
    transcript.md
    transcript.json
    summary_prompt.md
    <whisper native files>
```

## CLI Behavior

Whisper command shape:

```bash
whisper "<audio-file>" --model tiny --output_dir "<output>/transcripts" --output_format all
```

Video audio extraction command shape:

```bash
ffmpeg -y -i "<video-file>" -vn -ac 1 -ar 16000 -acodec pcm_s16le "<output>/media/extracted_audio.wav"
```

Context7/OpenAI Whisper docs confirmed local CLI transcription and output directory/output format support. Context7/FFmpeg docs and local `ffmpeg -h` output confirmed the relevant audio extraction flags.

## Safety

- Transcription is blocked unless `user_confirmed_rights=true`.
- `ffmpeg` and `whisper` are called with subprocess list arguments and `shell=False`.
- No external paid API is used.
- No AI summary is generated; only `summary_prompt.md` is created as a local prompt artifact.
- No cookies, credentials, tokens, auth, or database storage are added.

## Manual Proof

Input file:

```text
proof/download_block/20260529T092713Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a
```

API call:

```bash
POST http://127.0.0.1:8000/transcribe
```

Request:

```json
{
  "input_file_path": "/Users/aleksandr/Documents/Codex/Projects/universal-media-extractor/proof/download_block/20260529T092713Z_UUdxAp3kuKA/media/Showreel [UUdxAp3kuKA].m4a",
  "user_confirmed_rights": true,
  "model": "tiny",
  "source_kind": "audio"
}
```

Result:

- status: `succeeded`;
- errors: `[]`;
- output dir: `proof/download_block/20260529T092713Z_UUdxAp3kuKA`;
- transcript txt: `transcripts/transcript.txt`;
- transcript md: `transcripts/transcript.md`;
- transcript json: `transcripts/transcript.json`;
- summary prompt: `transcripts/summary_prompt.md`;
- log: `logs/transcription.log`.

The test audio produced a very short transcript (`You`). This proves the local pipeline and artifact generation, not transcript quality.

Proof files:

- `proof/transcript_block/transcribe_response.json`;
- `proof/transcript_block/transcribe_response_pretty.json`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/transcript.txt`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/transcript.md`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/transcript.json`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/transcripts/summary_prompt.md`;
- `proof/download_block/20260529T092713Z_UUdxAp3kuKA/logs/transcription.log`.

## Automated Verification

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
49 passed
```

## Not Implemented

- AI summary generation;
- background transcription jobs;
- progress streaming;
- active cancellation;
- transcript editing;
- model selection UI;
- local file upload;
- batch processing;
- Chrome extension;
- desktop wrapper;
- cookies/login;
- advanced download hardening.

## Remaining Risks

- Whisper quality depends on model size, audio quality, language, and CPU/GPU availability.
- The first UI uses model `tiny` for speed; quality may be low.
- Long files can take a long time on CPU.
- Video proof is covered by mocked tests, but not by a real manual video transcription proof in this block.
