# Alternatives Check

Date: 2026-05-29

## Alternative 1: `yt-dlp` + OpenAI Whisper CLI

- What it is: URL extraction/download through `yt-dlp`, media conversion through `ffmpeg`, transcription through local `whisper`.
- Official docs checked: yt-dlp README, FFmpeg docs, OpenAI Whisper CLI source/help.
- Covers critical capabilities: yes for best-effort URL support, local media extraction, local transcription, structured outputs.
- CLI/API/SDK: CLI-first; Python wrapper possible later.
- Cost: free/open-source, local CPU/GPU cost only.
- Complexity: medium.
- Risks: platform ToS, cookies/login, broken extractors, Whisper CPU speed, disk usage.
- Verdict: suitable as the primary starting approach, but only with explicit best-effort URL support.

## Alternative 2: `yt-dlp` + `faster-whisper`

- What it is: Keep `yt-dlp`/`ffmpeg`, replace OpenAI Whisper CLI with `faster-whisper` using CTranslate2.
- Official docs checked: https://github.com/SYSTRAN/faster-whisper
- Covers critical capabilities: yes for transcription engine; does not change URL extraction risk.
- CLI/API/SDK: Python API. The project README points to related CLIs such as `whisper-ctranslate2`, but `faster-whisper` itself is primarily a library.
- Cost: free/open-source; GPU acceleration has CUDA/cuDNN requirements, CPU mode exists.
- Complexity: medium-high because it adds Python integration and model/runtime decisions.
- Risks: Python wheel compatibility, PyAV/CTranslate2 dependencies, model downloads, GPU setup if desired.
- Verdict: good future performance alternative; not necessary for Phase 1 if the installed Whisper CLI is acceptable.

## Alternative 3: `whisper.cpp`

- What it is: C/C++ local Whisper inference implementation using ggml models.
- Official docs checked: https://github.com/ggml-org/whisper.cpp
- Covers critical capabilities: yes for local transcription, after building/downloading ggml models.
- CLI/API/SDK: CLI build plus libraries/bindings.
- Cost: free/open-source.
- Complexity: medium-high because it requires build tooling, model format management, and separate CLI integration.
- Risks: build/packaging friction, model conversion/download, output format parity needs verification.
- Verdict: strong fallback if Python Whisper performance or dependency weight becomes a blocker.

## Alternative 4: `ffmpeg` + Separate Transcription Engine

- What it is: Use `ffmpeg` for all local audio extraction/normalization, then send normalized audio to a chosen local STT engine.
- Official docs checked for base layer: FFmpeg docs.
- Covers critical capabilities: yes for local files; URL capabilities still require `yt-dlp` or another extractor.
- CLI/API/SDK: depends on engine.
- Cost: can remain free if local engine is open-source.
- Complexity: medium to high.
- Risks: different timestamp/output schemas; quality/performance varies.
- Verdict: valid architecture fallback, but not a better primary path until a specific engine is selected.

## Alternative 5: Online Transcription API

- What it is: Use paid hosted transcription for audio after extraction.
- Official pricing was not selected for implementation because the user explicitly wants no new paid subscriptions in the core path.
- Covers critical capabilities: potentially yes for transcription, not URL extraction.
- CLI/API/SDK: cloud API.
- Cost: paid/usage-based.
- Complexity: medium; requires keys, privacy and billing controls.
- Risks: privacy, recurring cost, network dependency, data retention terms.
- Verdict: not suitable as the starting approach. Keep only as future optional fallback if local transcription is too slow or inaccurate.

## Alternative Verdict

The primary `yt-dlp` + `ffmpeg` + OpenAI Whisper CLI path is the simplest viable local approach already available in the environment. The best technical fallback is `faster-whisper` for performance, followed by `whisper.cpp` for a non-Python transcription runtime.

