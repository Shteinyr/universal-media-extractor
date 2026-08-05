# Universal Media Extractor — Полное описание функционала продукта

Дата актуализации: 2026-08-05

## 1. Что это за продукт

Universal Media Extractor — локальное приложение для анализа, скачивания, извлечения и транскрибации медиа. Оно помогает пользователю работать с видео, аудио, субтитрами, локальными файлами и доступными ему учебными курсами без облачного backend, платных API и отправки медиа на сторонние сервисы.

Приложение работает как local-first utility:

```text
пользовательский интерфейс
  -> локальный backend на 127.0.0.1
  -> yt-dlp / ffmpeg / ffprobe / Whisper CLI
  -> локальные output-папки на компьютере пользователя
```

Главная идея продукта: заменить ручную работу с командной строкой (`yt-dlp`, `ffmpeg`, `ffprobe`, Whisper) на понятный пользовательский интерфейс.

## 2. Для кого продукт

Продукт полезен для:

- контент-мейкеров;
- монтажёров;
- подкастеров;
- преподавателей;
- студентов;
- исследователей;
- маркетологов;
- людей, которые работают с обучающими материалами;
- пользователей, которым нужно сохранять доступный им контент офлайн;
- пользователей, которым нужно быстро получить текстовую расшифровку аудио или видео.

## 3. Какие задачи решает

Приложение помогает:

- понять, какие форматы доступны у медиа-ссылки;
- выбрать, что именно нужно получить: аудио, видео или субтитры;
- скачать выбранный результат в понятную папку;
- сохранить видео вместе с аудио одним файлом;
- скачать только аудиодорожку;
- конвертировать аудио в популярный формат;
- скачать субтитры, если они доступны;
- обработать локальный audio/video файл;
- извлечь аудио из локального видео;
- сделать транскрипт через локальный Whisper;
- хранить результаты в структурированной папке;
- видеть статус длинных задач;
- отменять текущие задачи best-effort;
- работать с Udemy-курсами, доступными в аккаунте пользователя, через Chrome session.

## 4. Основные режимы работы

### 4.1. URL Mode

Режим для работы с публичной или доступной медиа-ссылкой.

Сценарий:

```text
URL -> Analyze -> Select output -> Download -> optional Transcribe -> Result
```

Что умеет:

- принимать http/https URL;
- анализировать источник через `yt-dlp`;
- получать название, длительность, thumbnail, uploader/channel, extractor;
- показывать доступные audio/video/subtitle варианты;
- группировать варианты по типам: Audio, Video, Subtitles;
- скрывать технический шум из UI;
- скачивать выбранный результат;
- сохранять результат в output-папку;
- запускать транскрипцию после скачивания аудио или видео с аудио.

### 4.2. Local File Mode

Режим для работы с файлом на компьютере пользователя.

Сценарий:

```text
Local audio/video file -> Analyze local file -> Transcribe -> Result
```

Что умеет:

- принимать локальный audio/video файл через upload в UI;
- сохранять рабочую копию файла в локальную output-папку;
- анализировать файл через `ffprobe`;
- определять тип файла: audio / video / unknown;
- получать длительность, размер, codec info, streams;
- транскрибировать audio напрямую через Whisper;
- для video извлекать аудио через `ffmpeg`, затем отправлять в Whisper;
- сохранять результат транскрипции рядом с output.

### 4.3. Course Mode / Udemy Mode

Режим для скачивания доступных пользователю Udemy-курсов.

Сценарий:

```text
Udemy lecture/player URL -> Analyze course -> Download course
```

Что умеет:

- принимать Udemy URL;
- лучше всего работает с URL из открытого плеера лекции: `/course/<slug>/learn/lecture/<id>`;
- использовать Chrome session через `yt-dlp --cookies-from-browser chrome`;
- использовать manual `cookies.txt` как advanced fallback;
- анализировать курс как playlist;
- получать список секций и лекций;
- выбирать качество: Best, 1080p, 720p, 480p;
- выбирать контейнер: MP4, MKV, WEBM;
- скачивать курс в структурированную папку;
- сохранять субтитры, если они доступны;
- сохранять лог и metadata.

Ограничения Udemy Mode:

- приложение не хранит логины и пароли;
- приложение не копирует cookies в output;
- приложение не обходит DRM;
- приложение не обходит CAPTCHA, paywall, access restrictions;
- Udemy support является best-effort;
- часть курсов или лекций может не скачиваться из-за DRM, ограничений Udemy или изменений в `yt-dlp`.

## 5. Медиа-сервисы и источники

### 5.1. Фактически подтверждённые / реализованные источники

- YouTube: анализ, выбор форматов, скачивание, транскрипция.
- Udemy: Course Mode через Chrome session / manual cookies fallback, best-effort.
- Local audio files: анализ и транскрипция.
- Local video files: анализ, извлечение аудио и транскрипция.
- Direct/generic media URLs: best-effort через `yt-dlp`, если источник поддерживается.

### 5.2. Источники через общий yt-dlp механизм

URL Mode технически работает через `yt-dlp`. Поэтому приложение потенциально может работать с любыми источниками, которые поддерживает текущая установленная версия `yt-dlp`, если источник не требует неподдерживаемую авторизацию, не защищён DRM и доступен сети.

Примеры таких источников:

- YouTube;
- Vimeo;
- SoundCloud;
- TikTok;
- X / Twitter;
- Facebook Video;
- Instagram;
- Twitch;
- Dailymotion;
- Reddit video;
- Bilibili;
- Bandcamp;
- Mixcloud;
- PeerTube;
- TED;
- другие `yt-dlp`-supported websites.

Важно: этот список не означает гарантированную поддержку каждого URL. Для каждого сервиса поддержка зависит от:

- текущей версии `yt-dlp`;
- публичности ссылки;
- доступности metadata;
- ограничений платформы;
- DRM;
- региона;
- login/cookies;
- изменений API на стороне сервиса.

### 5.3. SoundCloud

SoundCloud поддерживается через общий `yt-dlp` путь, но есть важные ограничения:

- публичные и незашифрованные треки могут анализироваться и скачиваться;
- часть треков может быть недоступна;
- DRM/protected треки не скачиваются;
- если `yt-dlp` возвращает `This video is DRM protected`, приложение не будет обходить защиту.

## 6. Анализ URL

Endpoint:

```text
POST /analyze
```

Что делает:

- принимает URL;
- создаёт analysis job;
- запускает `yt-dlp --simulate --dump-json`;
- не скачивает медиа на этапе анализа;
- сохраняет raw artifact в `proof/api`;
- нормализует результат в `AnalyzeResult`;
- возвращает данные для UI.

Данные, которые может вернуть анализ:

- source URL;
- source type;
- extractor / extractor key;
- title;
- duration;
- thumbnail;
- webpage URL;
- uploader/channel;
- availability/access state;
- audio options;
- video options;
- combined options;
- subtitles;
- automatic captions;
- metadata;
- warnings;
- errors;
- raw reference path;
- analyzed timestamp.

## 7. Выбор форматов в UI

UI специально упрощён для обычного пользователя.

Пользователь сначала выбирает тип результата:

- Audio;
- Video;
- Subtitles.

### Audio options

Показываются кратко:

```text
M4A · 1.69 MB
WEBM · 650 KB
```

Технические детали вроде codec strings, bitrate, language, `mp4a.40.2` скрыты из основного UI.

### Video options

Показываются кратко:

```text
MP4 · 1080p · 95 MB
WEBM · 2160p · 91 MB
```

Особенности:

- видео ниже 1080p скрывается из основного UI;
- дубли пользовательских вариантов схлопываются;
- Video mode скачивает видео вместе с best audio в один итоговый файл.

### Subtitles options

Показываются кратко:

```text
EN · Auto captions
RU · Manual subtitles
```

Особенности:

- одинаковые subtitle entries схлопываются по язык + тип;
- несколько форматов субтитров не превращаются в дубли;
- если субтитров нет, UI показывает короткий empty state.

## 8. Скачивание медиа

Endpoint:

```text
POST /download
```

Что умеет:

- скачивать выбранный audio format;
- скачивать выбранный video format вместе с best audio;
- скачивать combined format;
- скачивать subtitles;
- сохранять результат в выбранную output-папку;
- логировать процесс в `.logs/download.log`;
- сохранять request/result metadata;
- запускаться как background job;
- показывать статус в UI;
- поддерживать best-effort cancel.

Поддерживаемые output formats:

- Audio: M4A, MP3, WAV;
- Video: MP4, MKV, WEBM;
- Subtitles: SRT, VTT.

Техническая логика:

- audio использует `yt-dlp -x --audio-format <format>`;
- video использует выбранный video format + `bestaudio/best`;
- video/combined может remux/merge в MP4/MKV/WEBM;
- subtitles используют `--skip-download`, `--write-subs`, `--write-auto-subs`, `--convert-subs`.

## 9. Транскрипция

Endpoint:

```text
POST /transcribe
POST /local/transcribe
```

Что умеет:

- запускать локальный Whisper CLI;
- транскрибировать скачанный audio file;
- транскрибировать local audio file;
- для video сначала извлекать audio через `ffmpeg`;
- запускать Whisper на extracted audio;
- сохранять выбранный формат транскрипта;
- возвращать transcript text в API/UI;
- показывать статус job;
- поддерживать best-effort cancel.

Whisper model selection:

- tiny;
- base;
- small;
- medium;
- turbo/default, если доступно в установленном Whisper CLI.

Transcript output formats:

- TXT;
- Markdown;
- JSON.

Фактическая текущая реализация сохраняет один выбранный формат транскрипта за запуск. В older docs проекта также описывался `summary_prompt.md`; в текущем коде поля для summary prompt есть в модели/UI, но фактическая генерация summary prompt не является активной основной функцией текущей версии.

## 10. Локальный анализ файлов

Endpoint:

```text
POST /local/analyze
```

Что умеет:

- принимать uploaded local file;
- сохранять файл в local output structure;
- запускать `ffprobe`;
- определять media type;
- получать stream info;
- возвращать normalized metadata.

Возвращаемые данные:

- filename;
- saved path;
- output directory;
- media type;
- duration;
- size bytes;
- format name;
- format long name;
- streams;
- codec type;
- codec name;
- width/height для video;
- sample rate/channels для audio;
- errors/warnings.

## 11. Udemy Course Export

Endpoints:

```text
POST /udemy/analyze
POST /udemy/download
```

Что умеет:

- анализировать Udemy course/lecture URL;
- использовать Chrome session как основной способ доступа;
- использовать manual cookies.txt как fallback;
- возвращать sections и lectures;
- скачивать курс через `yt-dlp`;
- сохранять лекции по секциям;
- выбирать качество;
- выбирать контейнер;
- скачивать субтитры;
- ограничивать количество лекций через internal option `lecture_limit` в модели;
- сохранять request/result/log artifacts.

Auth sources:

- `chrome`: `yt-dlp --cookies-from-browser chrome`;
- `manual_cookies`: `yt-dlp --cookies <path>`.

Safety:

- cookies path редактируется в логах;
- cookies не копируются в output;
- passwords не принимаются;
- DRM/key extraction не реализованы.

## 12. Jobs, Progress, Cancel

Endpoints:

```text
GET /jobs/{job_id}
POST /jobs/{job_id}/cancel
```

Что умеет:

- создавать in-memory jobs;
- хранить task type;
- хранить payload;
- хранить status;
- хранить current step;
- хранить progress percent, если его можно честно получить;
- хранить result;
- хранить error;
- регистрировать активный subprocess;
- пытаться остановить subprocess при cancel.

Статусы:

- queued;
- running;
- succeeded;
- failed;
- cancelled.

Важно:

- jobs хранятся только в памяти;
- после перезапуска backend история jobs пропадает;
- cancel best-effort, потому что внешние CLI-процессы не всегда завершаются мгновенно.

## 13. Output Management

Endpoints:

```text
GET /outputs
GET /outputs/{output_id}
DELETE /outputs/{output_id}
```

Что умеет:

- создавать безопасные output-папки;
- создавать папки для analysis artifacts;
- создавать папки для downloads;
- создавать папки для local file workflows;
- обеспечивать структуру для transcription artifacts;
- индексировать recent results;
- показывать output summary;
- считать размер output;
- считать количество файлов;
- определять, есть ли media;
- определять, есть ли transcript;
- определять, есть ли summary prompt marker;
- безопасно удалять managed output.

Удаление ограничено:

- только direct child folders внутри configured output base;
- path traversal блокируется;
- произвольные системные папки удалить нельзя.

## 14. Output structure

Default output base:

```text
~/Downloads/Universal Media Extractor
```

URL download output:

```text
~/Downloads/Universal Media Extractor/<safe_source_title>/
  media/result files or direct downloaded file
  .metadata/
    download_request.json
    download_result.json
  .logs/
    download.log
```

Local file output:

```text
~/Downloads/Universal Media Extractor/local_<timestamp>_<safe_filename>/
  source/
  media/
  metadata/
  logs/
  transcripts/
```

Udemy output:

```text
~/Downloads/Universal Media Extractor/Udemy/<course_name>/
  01 - Section/
    001 - Lecture.mp4
    001 - Lecture.srt
  .metadata/
    udemy_download_request.json
    udemy_download_result.json
  .logs/
    udemy_download.log
```

## 15. Safety and local-only behavior

Продукт построен с ограничениями:

- backend слушает только `127.0.0.1`;
- приложение не является online service;
- приложение не добавляет user accounts;
- приложение не добавляет auth/database;
- приложение не отправляет медиа в облако;
- приложение не использует paid API;
- Whisper работает локально;
- download/process защищены backend-полем `user_confirmed_rights`;
- UI упрощён, но backend safety contract сохранён;
- cookies/passwords не сохраняются;
- DRM обход не реализован.

## 16. UI-функционал

Текущий интерфейс:

- compact downloader/file-manager style;
- URL mode;
- Local file mode;
- Course mode;
- URL input;
- local file picker;
- Udemy course URL input;
- Chrome session / manual cookies selector;
- Analyze button;
- media summary card;
- thumbnail;
- title;
- duration;
- uploader/source info;
- output selector;
- concise format rows;
- format deduplication;
- Save to field;
- output format selector;
- Download selected button;
- Course download controls;
- Whisper model selector;
- transcript format selector;
- Transcribe button;
- job status;
- result card;
- generated files;
- copy transcript;
- copy output path;
- technical details for errors;
- warnings/errors panels.

## 17. Desktop / запуск приложения

Текущие способы запуска:

### Browser mode

```bash
.venv/bin/python scripts/run_api.py
```

Открыть:

```text
http://127.0.0.1:8000/
```

### Desktop mode

```bash
.venv/bin/python scripts/run_desktop.py
```

Что делает:

- запускает FastAPI backend локально;
- открывает UI в desktop window через `pywebview`;
- выбирает свободный локальный порт, если 8000 занят;
- при закрытии окна останавливает backend, которым владеет.

### Development `.app` launcher

Есть script:

```bash
.venv/bin/python scripts/build_dev_app.py
```

Он создаёт development `.app`, привязанный к локальной папке проекта и `.venv`. Это не финальный installer.

## 18. Browser verification / QA

Есть browser smoke script:

```bash
.venv/bin/python scripts/browser_smoke.py
```

Что проверяет:

- открытие UI;
- initial state;
- analyze flow;
- отображение результата;
- screenshot artifacts.

Обычные тесты не запускают browser smoke автоматически.

## 19. API endpoints

Список текущих endpoints:

```text
GET    /
GET    /health
POST   /analyze
POST   /download
POST   /transcribe
POST   /local/analyze
POST   /local/transcribe
POST   /udemy/analyze
POST   /udemy/download
GET    /jobs/{job_id}
POST   /jobs/{job_id}/cancel
GET    /outputs
GET    /outputs/{output_id}
DELETE /outputs/{output_id}
```

## 20. Технологический стек

Backend:

- Python;
- FastAPI;
- Uvicorn;
- Pydantic v2;
- python-multipart;
- aiofiles.

Frontend:

- static HTML;
- CSS;
- vanilla JavaScript;
- no React;
- no Vite;
- no CDN.

Media tooling:

- yt-dlp;
- ffmpeg;
- ffprobe;
- OpenAI Whisper CLI.

Desktop / QA:

- pywebview;
- Python Playwright.

## 21. Что продукт не делает

Не реализовано:

- cloud backend;
- online SaaS;
- user accounts;
- auth system;
- database;
- paid API integration;
- AI summary API;
- batch processing;
- Chrome extension;
- final packaged/signed/notarized installer;
- DRM bypass;
- CAPTCHA bypass;
- paywall bypass;
- password login inside app;
- storing cookies;
- guaranteed support for all websites.

## 22. Ключевые ограничения

- URL support is best-effort through `yt-dlp`.
- Если сайт меняет API, анализ/скачивание может временно ломаться.
- Некоторые источники требуют cookies/login.
- Некоторые источники защищены DRM и не поддерживаются.
- SoundCloud DRM/protected tracks не скачиваются.
- Udemy support зависит от Chrome session, cookies validity и ограничений Udemy.
- Whisper качество зависит от модели и качества аудио.
- Большие файлы могут обрабатываться долго.
- Jobs не сохраняются после перезапуска backend.
- Desktop `.app` сейчас development-style, не полноценный installer.

## 23. Короткое позиционирование

Universal Media Extractor — локальный инструмент для людей, которые работают с видео, аудио и учебными материалами. Он позволяет анализировать медиа-ссылки, выбирать нужный output, скачивать доступные форматы, обрабатывать локальные файлы и создавать транскрипты через локальный Whisper без облачных сервисов и платных API.

## 24. Полезная формула продукта

```text
Analyze media -> choose clean output -> download locally -> transcribe locally -> keep organized results
```

Или по-русски:

```text
Проанализировать источник -> выбрать нужный результат -> сохранить файл -> сделать текстовую расшифровку -> получить аккуратную папку с материалами
```
