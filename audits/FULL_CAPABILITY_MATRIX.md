# Full Capability Matrix

Date: 2026-05-29

Legend: `yes`, `no`, `partial`, `unknown`.

## Source Index

- yt-dlp README: https://github.com/yt-dlp/yt-dlp/blob/master/README.md
- yt-dlp supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
- FFmpeg docs: https://www.ffmpeg.org/ffmpeg.html
- OpenAI Whisper CLI source: https://github.com/openai/whisper/blob/main/whisper/transcribe.py
- FastAPI file uploads: https://fastapi.tiangolo.com/tutorial/request-files/
- FastAPI background tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
- FastAPI features/OpenAPI docs: https://fastapi.tiangolo.com/features/
- Uvicorn settings: https://www.uvicorn.org/settings/
- pywebview architecture: https://pywebview.idepy.com/en/guide/architecture
- Chrome Native Messaging: https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging
- Python subprocess: https://docs.python.org/3/library/subprocess.html
- YouTube Terms of Service PDF: https://yt-terms.static.usercontent.goog/pdf/terms/20231215/en_us_20231215.pdf

## Matrix

| Capability | Criticality | Official CLI | Official API | UI | Browser/Computer Use | Local Script | Codex Tools | Source | Command / API | Permissions | Limits / Pricing / Auth | Bulk | Rollback / Backup | Safety Risks | Difficulty | Verdict |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| Paste URL | critical | no | no | yes | partial | yes | yes | local UI concept | input field | none | no pricing/auth | yes | no state to rollback | malicious URL handling | low | fits |
| Choose local file | critical | no | no | yes | partial | yes | yes | FastAPI UploadFile docs | `UploadFile`, file picker | file read | browser upload size/disk | yes | keep original | private file exposure | medium | fits |
| Analyze URL | critical | yes | partial | no | partial | yes | yes | yt-dlp README | `yt-dlp -j URL` | network | site-specific auth/cookies | partial | save JSON | platform ToS/cookies | medium | partial |
| Determine source support | critical | partial | partial | no | partial | yes | yes | yt-dlp supported sites | extractor result/errors | network | not guaranteed; sites change | partial | save error | false confidence | medium | partial |
| Get URL metadata | critical | yes | partial | no | partial | yes | yes | yt-dlp README | `-j`, `--dump-json` | network | auth/cookies sometimes | partial | `metadata.json` | metadata may be incomplete | medium | fits |
| Get local metadata | critical | yes | no | no | no | yes | yes | FFmpeg docs | `ffprobe -show_format -show_streams -of json` | file read | free/no auth | yes | save JSON | malformed files | low | fits |
| List audio formats | critical | yes | partial | no | no | yes | yes | yt-dlp README | `-F`, JSON `formats` | network | source dependent | partial | save format list | wrong choice can fail | medium | fits |
| List video formats | critical | yes | partial | no | no | yes | yes | yt-dlp README | `-F`, JSON `formats` | network | source dependent | partial | save format list | large files | medium | fits |
| List subtitles | important | yes | partial | no | no | yes | yes | yt-dlp README | `--list-subs`, JSON `subtitles` | network | availability varies | partial | save list | auto-subs quality | medium | fits |
| Download audio-only | critical | yes | partial | no | no | yes | yes | yt-dlp README | `-x`, `-f ba`, `--audio-format` | network/write | auth/cookies, ToS | yes | delete partials, archive info | copyrighted content | medium | partial |
| Download video-only | important | yes | partial | no | no | yes | yes | yt-dlp README | `-f bv` | network/write | source dependent | yes | delete partial | large files | medium | fits |
| Download video+audio | critical | yes | partial | no | no | yes | yes | yt-dlp README | `-f bv+ba/b`, `--merge-output-format` | network/write, ffmpeg | source dependent | yes | delete partial | large files/rights | medium | partial |
| Download subtitles | important | yes | partial | no | no | yes | yes | yt-dlp README | `--write-subs`, `--sub-langs` | network/write | availability/language varies | yes | delete files | wrong language/auto quality | low | fits |
| Convert media | critical | yes | no | no | no | yes | yes | FFmpeg docs | `ffmpeg -i in out` | file read/write | free/no auth | yes | keep original | overwrite/data loss | medium | fits |
| Extract local audio | critical | yes | no | no | no | yes | yes | FFmpeg docs | `ffmpeg -i video -vn audio.wav` | file read/write | free/no auth | yes | keep original | disk usage | low | fits |
| Transcribe local audio | critical | yes | partial Python module | no | no | yes | yes | Whisper source/help | `whisper audio -f all -o out` | file read/write, model cache | free; model download/cache; CPU slow | yes | keep audio, outputs | hallucination/privacy local | medium | fits |
| Transcribe local video | critical | partial | no | no | no | yes | yes | FFmpeg + Whisper docs | extract audio then `whisper` | file read/write | CPU/disk limits | yes | keep intermediates | long runtime | medium | fits |
| Structured output folder | critical | no | no | no | no | yes | yes | Python stdlib | filesystem ops | disk write | disk space | yes | original retained | path traversal if unsafe | low | fits |
| `transcript.txt` | critical | yes | partial | no | no | yes | yes | Whisper source/help | `--output_format txt/all` | disk write | none | yes | regenerate | transcript errors | low | fits |
| `transcript.md` | important | no | no | no | no | yes | yes | local script | transform text | disk write | none | yes | regenerate | formatting errors | low | fits |
| `transcript.json` | critical | yes | partial | no | no | yes | yes | Whisper source/help | `--output_format json/all` | disk write | none | yes | regenerate | large JSON | low | fits |
| `summary_prompt.md` | optional | no | no | no | no | yes | yes | local script | template file | disk write | none | yes | regenerate | accidental data exposure if pasted later | low | fits |
| `metadata.json` | critical | yes | partial | no | no | yes | yes | yt-dlp/ffprobe | `-j`, `ffprobe -of json` | disk write | source dependent | yes | regenerate | sensitive URLs/cookies not stored | low | fits |
| Job status | critical | partial | no | yes | partial | yes | yes | yt-dlp/ffmpeg progress docs | parse stdout/stderr/progress | process read | progress format varies | yes | persist job log | stale status | medium | fits |
| Cancel job | critical | partial | no | yes | partial | yes | yes | Python subprocess docs | `Popen.terminate/kill` | process control | child process groups need care | yes | partial files cleanup | orphan processes | medium | fits |
| Retry job | important | partial | no | yes | partial | yes | yes | yt-dlp retry flags/Python | `--retries`, rerun job | network/file | transient failures remain | yes | keep config/log | duplicate outputs | medium | fits |
| Error handling | critical | partial | no | yes | partial | yes | yes | CLI exit codes/stderr | stderr/return code | none | messages vary by site | yes | save logs | leaking sensitive paths | medium | fits |
| Local-only backend | critical | no | yes | yes | partial | yes | yes | Uvicorn docs | `--host 127.0.0.1` | local port | browser access only; CORS needed | n/a | config rollback | exposed local file ops if misbound | medium | fits |
| Dependency checks | critical | yes | no | yes | no | yes | yes | local CLI help | `which`, `--version`, `--help` | execute binaries | installed versions differ | yes | log versions | PATH spoofing | low | fits |
| Desktop wrapper | optional | no | yes | yes | partial | yes | yes | pywebview docs | `create_window(local_url)` | OS GUI | packaging/signing later | n/a | browser fallback | CSRF/local API | medium | partial |
| Chrome extension button | optional | no | yes | yes | yes | yes | yes | Chrome docs | `runtime.connectNative`, host manifest | extension + host install | 1 MB host-to-Chrome msg, 64 MiB Chrome-to-host msg; registration required | yes | disable extension/manifest | broad URL permissions | high | partial |

## Local Evidence

- `ffmpeg -version`: 8.1.1 works.
- `ffprobe -version`: 8.1.1 works.
- `yt-dlp --version`: 2026.03.17 works.
- `yt-dlp --help`: confirms `-F`, `-j`, `--write-subs`, `--write-auto-subs`, `--progress-template`, `--cookies`, `--cookies-from-browser`, `--simulate`, `--extract-audio`, `--merge-output-format`, `--paths`, `--sub-langs`, retries, and abort flags.
- `yt-dlp --list-extractors`: 1872 entries locally, including entries marked `CURRENTLY BROKEN`.
- `whisper --help`: confirms local CLI accepts audio files, model/device/output directory, `txt/vtt/srt/tsv/json/all`, language, timestamps, threads, clips.
- `python3 --version`: 3.14.4 in current shell.
- Python packages `fastapi`, `uvicorn`, `pywebview` are not installed in the current Python environment.
- PyPI metadata via `curl`: FastAPI 0.136.3 requires Python `>=3.10`; Uvicorn 0.48.0 requires `>=3.10`; pywebview 6.2.1 requires `>=3.8`; openai-whisper 20250625 requires `>=3.8`; faster-whisper 1.2.1 requires `>=3.9`.
- Local Python `urllib.request` HTTPS to PyPI failed with certificate verification error; `curl` and `pip index` worked. Treat this as an environment risk for Python HTTPS code, not a core blocker for CLI-only processing.

