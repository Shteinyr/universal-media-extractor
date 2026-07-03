# Capability Requirements

Date: 2026-05-29

Criticality values: `critical`, `important`, `optional`.

| Capability | Why Needed | Criticality | Performer | Required Data | Required Permissions | Tool / Service | Can Omit? | If Missing |
|---|---|---:|---|---|---|---|---|---|
| Paste URL | Start URL workflow | critical | UI / user | URL | none | local web UI | no | URL workflow impossible |
| Choose local file | Start file workflow | critical | UI / user | file path/upload | local file read | browser file picker / backend | no | local workflow impossible |
| Analyze URL via `yt-dlp` | Determine support and metadata | critical | CLI / local script | URL, optional cookies | network access | `yt-dlp -j`, `-F`, `--list-subs` | no for URL mode | URL mode blind |
| Determine source support | Avoid false promises | critical | `yt-dlp` / local script | URL | network access | extractor result/errors | no | user sees unreliable failures |
| Get metadata | Naming, preview, archive | critical | `yt-dlp` / `ffprobe` | URL or file | network/file read | `yt-dlp -j`, `ffprobe` | partial | weak output structure |
| List audio formats | Let user choose audio | critical | `yt-dlp` | URL | network | `-F`, JSON `formats` | no for URL mode | no controlled audio download |
| List video formats | Let user choose video | critical | `yt-dlp` | URL | network | `-F`, JSON `formats` | no for URL mode | no controlled video download |
| List subtitles | Subtitle output | important | `yt-dlp` | URL | network | `--list-subs`, JSON subtitles | yes | subtitle feature absent |
| Download audio-only | Core extraction output | critical | `yt-dlp` / `ffmpeg` | URL, format choice | network/write | `-x`, `-f ba`, postprocess | no | no URL audio extraction |
| Download video-only | Advanced media output | important | `yt-dlp` | URL, format choice | network/write | `-f bv` | yes | video-only feature absent |
| Download video+audio | Common download output | critical | `yt-dlp` + `ffmpeg` | URL, format choice | network/write | `-f bv+ba/b`, merge | no for media download | cannot save normal videos |
| Download subtitles | User-selected captions | important | `yt-dlp` | URL, lang/format | network/write | `--write-subs`, `--write-auto-subs` | yes | no caption extraction |
| Convert via `ffmpeg` | Normalize outputs | critical | CLI / local script | input media, target format | file read/write | `ffmpeg` | no | many outputs inconsistent |
| Transcribe local audio via Whisper CLI | Main transcript feature | critical | Whisper CLI | audio path, model, language | file read/write, model cache | `whisper` | no for transcript mode | no local transcription |
| Extract audio from local video | Prepare video transcription | critical | `ffmpeg` | video file | file read/write | `ffmpeg -map a` | no | local video transcript broken |
| Transcribe local video via `ffmpeg` + Whisper | Local video workflow | critical | local script / CLI | video file | file read/write | `ffmpeg`, `whisper` | no | local video use case weak |
| Save output structure | Usable result | critical | local script | job id, names, files | disk write | filesystem | no | outputs messy/untrusted |
| Create `transcript.txt` | Simple transcript | critical | Whisper / local script | Whisper output | disk write | `whisper -f txt/all` | no | no plain transcript |
| Create `transcript.md` | Human-readable artifact | important | local script | transcript text, metadata | disk write | local script | yes | less convenient output |
| Create `transcript.json` | Structured transcript | critical | Whisper | audio path | disk write | `whisper -f json/all` | no | no structured transcript |
| Create `summary_prompt.md` | Future AI summary handoff | optional | local script | transcript metadata | disk write | local script | yes | future AI step manual |
| Create `metadata.json` | Reproducibility | critical | `yt-dlp` / `ffprobe` / script | metadata | disk write | local script | no | poor auditability |
| Job status | User can monitor long tasks | critical | backend / local script | process state | none | process manager | no | long jobs feel broken |
| Cancel job | Stop bad/long jobs | critical | backend / Python process | process pid/group | process control | Python `subprocess` | no | runaway jobs possible |
| Retry job | Recover from transient errors | important | backend / user | previous job config | network/file | local script | yes | user restarts manually |
| Error handling | Explain failures | critical | backend / local script | stderr, exit codes | none | CLI return codes | no | unsafe/unusable |
| Local-only security | Avoid exposing local file operations | critical | backend config | bind host, CORS policy | network binding | Uvicorn/FastAPI config | no | security risk |
| Dependency checks | Avoid mysterious failures | critical | local script | CLI paths/versions | execute CLIs | `which`, `--version`, `--help` | no | brittle setup |
| Future desktop packaging | Convenience after MVP | optional | pywebview / packager | app URL/assets | OS GUI | pywebview | yes | still usable in browser |
| Future Chrome extension button | Send current page | optional | Chrome extension / native host | current tab URL | extension permissions, native host registration | Chrome Native Messaging | yes | URL paste remains manual |

