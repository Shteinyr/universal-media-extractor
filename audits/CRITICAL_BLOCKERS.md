# Critical Blockers

Date: 2026-05-29

| Blocker Question | Confirmed? | Source / Evidence | Criticality | Workaround | Workaround Reliability | Continue? |
|---|---|---|---:|---|---|---|
| Can URLs be reliably analyzed through `yt-dlp`? | partially confirmed | yt-dlp supports JSON/listing, but supported-sites docs say not all listed sites are guaranteed and sites change | critical | Best-effort analysis with explicit errors | medium | yes, with scope limits |
| Can formats be listed before download? | confirmed | yt-dlp README/help: `-F --list-formats` simulates unless `--no-simulate` | critical | Use JSON `formats` plus `-F` fallback | high | yes |
| Can audio-only be downloaded? | confirmed | yt-dlp README/help: `-x --extract-audio`, `-f ba` | critical | Use `ffmpeg` postprocessing | high if source works | yes |
| Can video+audio be downloaded? | confirmed | yt-dlp README/help: format selection and `--merge-output-format`; requires ffmpeg for merge | critical | Select best combined or merge best video/audio | high if source works | yes |
| Can subtitles be downloaded? | confirmed | yt-dlp README/help: `--write-subs`, `--write-auto-subs`, `--list-subs`, `--sub-langs` | important | Use auto-subs if user allows | medium | yes |
| Can local files work without `yt-dlp`? | confirmed | ffmpeg/ffprobe installed and official docs support file inputs | critical | Analyze via `ffprobe`, extract via `ffmpeg` | high | yes |
| Can transcription run via local Whisper CLI? | confirmed | `whisper --help`; OpenAI Whisper CLI source | critical | Use `whisper` with output dir/format | high, subject to performance | yes |
| Can long files be processed? | partially confirmed | Whisper supports files and clips; ffmpeg supports long media; no local long-file benchmark run | critical | Chunk with ffmpeg, use smaller model, resume by segments | medium | yes, with performance warning |
| Can process cancellation work? | confirmed in principle | Python subprocess docs expose `terminate()` and `kill()`; process groups need implementation care | critical | Track process groups and cleanup partials | medium-high | yes |
| Can progress be tracked? | confirmed | yt-dlp `--progress-template`; ffmpeg `-progress pipe:1`; Whisper verbose output less structured | critical | Parse yt-dlp/ffmpeg; Whisper progress may be coarse | medium | yes |
| Can backend stay on `127.0.0.1`? | confirmed | Uvicorn docs default host is `127.0.0.1`; explicit host supported | critical | Always bind loopback and restrict CORS | high | yes |
| Are there YouTube/platform limits? | confirmed | YouTube Terms restrict downloading/automated access except permitted cases; yt-dlp docs warn site support breaks | critical | User-provided rights, clear disclaimers, no bypass promises | legal reliability low | conditional |
| Are cookies/login sometimes needed? | confirmed | yt-dlp README/help supports cookies and browser cookies; FAQ/wiki discuss auth | critical for some sources | User-provided cookies/manual auth | medium-low | conditional |
| Can some yt-dlp supported sites fail? | confirmed | supported-sites docs explicitly say not guaranteed; local extractor list includes `CURRENTLY BROKEN` entries | critical | Detect and report unsupported/broken source | medium | yes, with best-effort wording |
| Are some actions impossible to automate? | confirmed | Login/CAPTCHA/DRM/rights authorization cannot be safely automated | critical | Ask user to provide accessible URL/file or cookies where lawful | low-medium | conditional |
| macOS permission risk? | partially confirmed | Local file access and browser uploads need user-selected files; cookies/keychain access may require OS prompts | important | Use file picker; avoid reading browser cookies by default | medium | yes |
| Python 3.14 compatibility risk? | partially confirmed | PyPI metadata allows current libs, but local FastAPI/Uvicorn/pywebview are not installed; Python urllib SSL failed | important | Use venv; pin versions; fix certs or use `certifi`/CLI tools | medium | yes |
| Whisper CPU performance risk? | confirmed | Whisper CLI defaults to CPU locally; long media can be slow | critical | Smaller model, chunking, faster-whisper/whisper.cpp optional | medium | yes, with expectation setting |
| File size and disk space risk? | confirmed | Local disk has about 201 GiB free; downloads/intermediates can be huge | critical | Estimate sizes, quotas, cleanup partials | high | yes |

## Blocker Verdict

No hard technical blocker was found for a local single-user tool. The major blocker is product-scope truthfulness: the app cannot honestly be “universal” in the sense of guaranteed support for all URLs or all platforms. It can be a best-effort local extractor/transcriber with clear source support checks, local-file fallback, user-controlled cookies, and legal/platform warnings.

