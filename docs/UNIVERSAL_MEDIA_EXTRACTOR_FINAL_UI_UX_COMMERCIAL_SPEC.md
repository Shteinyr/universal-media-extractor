# Universal Media Extractor  
## Финальная UI/UX-спецификация публичной beta и коммерческой упаковки

**Дата:** 7 августа 2026  
**Продукт:** `Universal Media Extractor`  
**Публичная категория:** `Local Media Downloader & Organizer for macOS and Windows`  
**Статус документа:** продуктовая и инженерная спецификация; не подтверждает фактическую готовность backend-функций, которые не были проверены end-to-end.

---

## Основание анализа и уровень доказательности

Анализ выполнен на основе:

- `UI_UX_GPT_PRO_CONTEXT_PACK.md`;
- `UI_UX_COMPETITOR_VISUAL_LOGIC_PACK.md`;
- `UI_UX_OUR_APP_VISUAL_LOGIC_PACK.md`;
- `PRODUCT_FUNCTIONALITY_OVERVIEW.md`;
- 26 конкурентных и референсных продуктов;
- 26 скриншотов конкурентов;
- 6 скриншотов текущего Universal Media Extractor;
- актуальных официальных страниц, документации, GitHub-репозиториев, цен и правил площадок на 7 августа 2026 года.

### Что подтверждено скриншотами текущего приложения

Пакет подтверждает визуальное состояние следующих экранов:

- начальный экран;
- результат анализа URL;
- выбранный output;
- режим локального файла;
- режим Batch;
- состояние с некорректным URL.

Скриншоты были получены в analysis-only режиме. Фактическое скачивание, транскрипция, progress, финальный result, полноценная Library и Settings этим пакетом не подтверждены. Поэтому рекомендации по ним являются целевой спецификацией, а не описанием уже проверенной реализации.

### Критический конфликт исходных документов

Два документа расходятся по фактической готовности продукта:

- пакет от **7 августа 2026** указывает `SQLite job history`, Library и реализованный Batch flow;
- функциональный обзор от **5 августа 2026** указывает, что jobs хранятся только в памяти, database и batch processing не реализованы.

До UI-финализации инженер должен определить один фактический источник истины, проверить текущий код и провести end-to-end тесты. В этом документе Batch и Library описаны как обязательная целевая архитектура публичной beta, но не считаются автоматически готовыми.

---

## Независимый аудит текущего интерфейса

### Что уже работает визуально

- Сдержанная тёмная палитра подходит desktop utility.
- Акцентный цвет используется умеренно.
- Карточка проанализированного медиа компактна и понятна.
- Технические `format_id`, codec strings и raw `yt-dlp` output не вынесены в основной UI.
- Output представлен человеческими названиями, а не CLI-командами.
- Выбранный preset визуально различим.
- Базовая сетка, границы и интервалы последовательны.
- Приложение уже выглядит ближе к локальному инструменту, чем к web-маркетинговому dashboard.

### Что делает продукт похожим на незавершённый dev utility

1. **`Link / File / Batch` оформлены как режимы верхнего уровня.** Пользователь обязан сначала понять внутреннюю структуру приложения, хотя приложение само может определить тип входа.
2. **`Course · internal` виден в публичном shell.** В коммерческой сборке его не должно быть ни в DOM, ни в меню, ни в Settings, ни в доступных API-маршрутах.
3. **Слева занято около 280 px под режимы и формы**, но основная часть окна остаётся почти пустой.
4. **Большая пустая карточка `Add a source` создаёт ощущение незаконченного продукта.** Она не даёт дополнительной функции и растягивает минимальный workflow.
5. **Library закреплена мёртвой нижней полосой на каждом экране.** Это не полноценная навигация и не полезный summary.
6. **HTML file input выглядит браузерно**, а не как desktop control. Нужен native file picker и drag-and-drop.
7. **Локальный файл требует отдельного `Analyze local file`.** Выбор файла уже является достаточным намерением; анализ должен запускаться автоматически.
8. **Batch содержит четыре разрозненных действия:** `Import URLs`, `Paste`, `Text file`, `Analyze playlist`. Это одна задача, разбитая на внутренние команды.
9. **`Best video`, `1080p video` и `Smaller video` на скриншоте разрешаются в одинаковые `MP4 · 1080p · 12 MB`.** Это разрушает доверие к presets. Нужна динамическая дедупликация.
10. **`Smaller video at 1080p or higher` семантически противоречив.** «Меньше» должно означать конкретный предел — например, до 720p.
11. **После выбора output появляется отдельная большая карточка Download**, вызывающая вертикальный скачок. Лучше использовать стабильную нижнюю action bar.
12. **Save path выглядит как редактируемое текстовое поле.** Путь должен быть read-only с native `Change…`.
13. **Постоянный Warnings-блок повторяет юридическую оговорку после каждого анализа.** Такие правила должны находиться в onboarding/Terms/Help; на рабочем экране показываются только контекстные предупреждения.
14. **`ui_invalid_url_error.png` визуально не показывает ошибку.** Некорректный URL остаётся в поле без понятного сообщения и действия.
15. **Нет доказательств светлой темы, keyboard navigation, масштабирования, screen-reader labels, progress/result states и восстановления после перезапуска.**

---

## Синтез конкурентного поля

### Общий вывод

Universal Media Extractor не должен пытаться победить количеством сайтов, форматов, AI-модулей или технических настроек. В этих направлениях уже существуют:

- зрелые платные downloaders;
- бесплатные и open-source `yt-dlp` GUI;
- специализированные transcription apps;
- крупные all-in-one media suites.

Коммерческое преимущество UME должно строиться на сочетании:

```text
простое добавление источника
→ понятный результат вместо stream list
→ надёжная очередь
→ аккуратные локальные файлы
→ полезная Library
→ необязательная локальная транскрипция
→ человеческие ошибки и быстрые engine updates
```

### Сравнение всех изученных продуктов

| Продукт / референс | Что у него сильнее текущего UME | Что использовать в UME | Что не переносить |
|---|---|---|---|
| 4K Video Downloader Plus | Зрелая упаковка, Smart Mode, playlist/channel scale, понятные лицензии | Повторяемый preset, Free → paid scale, один ясный default workflow | Private/proxy claims, обещание широкой гарантированной поддержки |
| Downie | Нативная компактность, drag/paste, browser integration, частые fixes | Utility-first shell, минимум действий, post-processing после download | «Скачать со всего интернета», user-guided extraction как beta-core |
| SnapDownloader | Batch, scheduler, queue, one-click mode, коммерческая зрелость | Batch как платная продуктивность, saved preset | Proxy/private browser, перегруженная матрица функций |
| PullTube | Drag-and-drop, лёгкое audio conversion, trim | Drop-first interaction, compact Mac utility feel | Trim/editor до проверки основного спроса |
| MediaHuman | Сильная list/queue модель, locate/open actions | Строка задачи, `Show in Finder/Explorer`, понятное row menu | Плотная панель инструментов и множество мелких controls |
| Parabolic | Бесплатный прямой `yt-dlp` GUI, concurrent downloads | Активная очередь, metadata/subtitle support за GUI | Raw engine concepts в основном UI |
| Stacher | Ближайший конкурент: URL bar, Library, premium organization | Library как отдельная ценность, paid workflow layer | Developer-tool эстетика и engine-oriented settings |
| Cobalt | Минимальный первый экран и короткие ошибки | Input-first композиция, один главный action | Web/cloud framing и отсутствие desktop organization |
| Buzz | Полноценный transcript result и export | Текст как читаемый артефакт, а не только path | Полный transcription workstation |
| MacWhisper | Сильная local/privacy упаковка, polished transcript viewer | Точная privacy copy, понятный result/export | Meeting/dictation/AI-suite scope |
| yt-dlp.app | Разделяет app update и engine update | Engine status/update как support-функция | Слишком широкие legal/fair-use формулировки |
| Wondershare UniConverter | Presets, support center, activation, mature checkout | Коммерческая уверенность, support surface | Toolbox из десятков модулей |
| VideoProc | Форматные presets и коммерческая подача | Outcome language вместо codec language | AI media suite |
| HitPaw Univd | Планы, team packaging, conversion presets | Понятные paid tiers позднее | Credits, AI/editor bloat |
| JDownloader | Persistent queue, packages, retry/resume | Надёжность очереди и группировка batch | Plugin-heavy power-user complexity |
| Any Video Converter | Free/Pro boundaries, batch, local processing | Paid boundary по масштабу и автоматизации | AI creation suite |
| ClipGrab | Очень простая модель input → format → download | Минимальное количество решений | Устаревший visual language |
| Tartube | Архив, duplicate avoidance, organized folders | Duplicate detection и batch groups | Архиватор каналов как публичный core |
| YT DLP GUI | Presets, history, update checker, readable errors | Plain-language wrapper, presets, diagnostics | Непроверенные широкие claims |
| Open Video Downloader | Современный cross-platform GUI, queue, import TXT/CSV, clipboard, auto-updates | Прямая проверка конкурентного parity: queue, imports, engine update обязательны | Authentication/cookie power features в public beta |
| Vividl | Простой Windows workflow, parallel jobs, clipboard auto-import | Windows-native ожидания, compact list | Показ всех доступных форматов |
| MeTube | Чистая queue architecture, playlist/channel handling | Batch review и очередь как отдельный рабочий слой | Self-hosted subscription/archive scope |
| HandBrake | Сильная модель `source → preset → queue` | Preset first, advanced quality отдельно | Codec-heavy configuration в основной форме |
| Shutter Encoder | Огромная мощность FFmpeg, queue, saved presets, transcription | Advanced/support как отдельный слой, saved presets позднее | Плотность функций и прямые команды |
| Aiko | Минимальный локальный transcription flow и честная privacy copy | On-device framing и простая настройка качества | Превращение UME в самостоятельный transcription product |
| LosslessCut | Чёткая ценность локальной utility, free direct + paid store convenience | Доверие, direct distribution, простая paid convenience model | «Swiss army knife» feature expansion |

### Дополнительные конкуренты и референсы, найденные вне переданного пакета

1. **Open Video Downloader** — наиболее важный новый direct competitor. В актуальном проекте есть cross-platform installers, queue, import URL lists, playlist selection, output templates, automatic app/engine updates и Microsoft Store build.
2. **Vividl** — полезный Windows-reference: URL → metadata → quality/format → parallel queue.
3. **MeTube** — не desktop competitor, но сильный референс для batch/queue separation и playlist review.
4. **HandBrake** — эталон разделения простого preset workflow и advanced encoding.
5. **Shutter Encoder** — отрицательный и положительный референс одновременно: мощность должна существовать, но быть спрятана от первого экрана.
6. **Aiko** — точная модель local transcription и privacy language без cloud promise.
7. **LosslessCut** — доказательство модели, где direct build остаётся доступным, а store build продаёт доверие, подпись, updates и удобство установки.

---

# 1. Executive recommendation

## Финальное решение

Публичную beta следует выпускать только после **структурной переупаковки UI и проверки reliability layer**.

Финальная модель продукта:

```text
New task
  → one universal source input
  → source auto-detection
  → outcome preset
  → Queue
  → Result
  → Library
```

### Главные решения

| Вопрос | Финальное решение |
|---|---|
| Link / File / Batch modes | Убрать как top-level modes. Оставить один `New task` и автоопределение источника |
| Первый экран | Компактный source composer, native file action, secondary batch action, последние 3 результата только при наличии |
| Library | Отдельный постоянный пункт навигации; не footer и не часть первого workflow |
| Batch | Secondary entry из New task; после добавления становится Queue workflow |
| Transcription | Для скачанного медиа — result action; для локального файла — primary action после выбора файла |
| Output selection | Segmented `Video / Audio / Subtitles` + compact radio rows |
| Format | Показывать внутри preset summary; override переносится в `Options` |
| Save location | Read-only path + `Change…` непосредственно перед primary action |
| Video meaning | Любой video preset означает один финальный воспроизводимый файл с video + audio |
| Public Course mode | Полностью удалить из public build |
| Commercial model | Free public beta → постоянный Free + one-time Pro |
| Основная paid value | Batch, playlists, concurrency, unlimited Library, Smart Presets, organization, advanced local transcription |
| Distribution | Signed direct installers; Microsoft Store позднее; Mac App Store не считать базовым каналом |

## Ключевой продуктовый принцип

Пользователь покупает не `yt-dlp` и не список сайтов. Он покупает:

- отсутствие терминала;
- предсказуемый результат;
- понятную очередь;
- чистые файлы;
- восстановление после ошибок;
- быстрые engine updates;
- порядок в сохранённых материалах.

---

# 2. Финальная информационная архитектура

## 2.1. Основная навигация

```text
Universal Media Extractor
├── New task
├── Queue
├── Library
└── Settings
```

Дополнительно через системное меню приложения:

```text
Help
├── Supported sources and limitations
├── Troubleshooting
├── Check for app updates
├── Check media engine
├── Open logs folder
├── Report a problem
└── About
```

После коммерческого запуска в нижней части sidebar:

```text
Upgrade
License status
```

В public beta `Upgrade` отсутствует.

## 2.2. Что не является отдельным разделом

- `Link` — тип источника, а не раздел.
- `File` — способ добавления источника, а не раздел.
- `Batch` — количество задач, а не раздел.
- `Transcription` — действие над local/saved media, а не отдельный продукт.
- `Course` — internal feature, отсутствует в public build.
- `History` — часть Library, отдельный пункт не нужен.
- `Outputs` — технический термин, пользователю показывается Library/Files.

## 2.3. Правила маршрутизации universal input

| Вход | Автоматический маршрут |
|---|---|
| Один корректный URL | URL analysis → output selection |
| Несколько URL в clipboard/input | Batch review |
| Playlist URL | Playlist review → item selection |
| Один локальный audio/video file | Local media summary → Transcribe |
| Несколько локальных файлов | Batch transcription не в beta; показать ограничение и предложить выбрать один |
| Некорректный текст | Inline validation без backend request |
| Protected/login-only source | Normalized error; никаких cookie/login controls в public build |

## 2.4. App shell

**Рекомендуемый default window:** `1120 × 760`  
**Минимальный размер:** `920 × 640`  
**Sidebar:** `184–192 px`  
**Main content:** до `920 px`, top-aligned, padding `24 px`  
**Native window chrome:** сохранить; не строить custom browser-like titlebar в beta.

Sidebar:

- product icon + short name;
- `New task`;
- `Queue` с badge активных/failed;
- `Library`;
- нижний блок `Settings`;
- после launch — `Upgrade` или license state.

Никаких source forms внутри sidebar.

---

# 3. Screen-by-screen UX spec

## 3.1. First-run readiness

### Цель

Подготовить media engine без технического onboarding и не заставлять пользователя понимать `yt-dlp`, `ffmpeg` или Whisper.

### Поведение

При первом запуске приложение выполняет silent preflight:

- доступна ли output folder;
- доступен ли media engine;
- доступен ли `ffmpeg`;
- доступна ли запись в temp/output;
- текущие версии app/engine.

Если всё готово — сразу открыть `New task`.

Если media engine отсутствует или повреждён — показать blocking setup:

```text
Preparing media tools
Universal Media Extractor needs a local media engine before it can start.

[ progress ]
Downloading required components…

Cancel
```

После завершения:

```text
Media tools are ready.
[Continue]
```

Whisper model не загружается при первом запуске. Он запрашивается только при первой транскрипции с точным размером загрузки, который приложение получает из собственного manifest.

### Не показывать

- terminal commands;
- package names;
- Python environment;
- raw component URLs;
- login/account;
- длинное onboarding-слайдшоу.

---

## 3.2. Global shell

### Sidebar

```text
[icon] Universal Media Extractor

New task
Queue                         2
Library

Settings
```

### Main header

Каждый раздел имеет короткий title:

- `New task`
- `Queue`
- `Library`
- `Settings`

Дополнительный action размещается справа только при необходимости:

- Queue: `Clear completed`
- Library: search + sort
- Settings: отсутствует
- New task: отсутствует

### Keyboard shortcuts

| Action | macOS | Windows |
|---|---|---|
| New task | `⌘N` | `Ctrl+N` |
| Focus source field | `⌘L` | `Ctrl+L` |
| Choose local file | `⌘O` | `Ctrl+O` |
| Settings | `⌘,` | `Ctrl+,` |
| Open Library | `⌘2` | `Ctrl+2` |
| Open Queue | `⌘1` | `Ctrl+1` |
| Close details/sheet | `Esc` | `Esc` |

---

## 3.3. New task — первый экран

### Финальный layout

```text
New task

┌──────────────────────────────────────────────────────────────┐
│ Paste a supported media link                                 │
│ [ Paste a media link........................ ] [Get options] │
│                                                              │
│ [Choose file…]     Add multiple links                        │
│                                                              │
│ Downloads and processing run on this computer.               │
└──────────────────────────────────────────────────────────────┘

Recent results
[optional compact list of up to 3 items]
```

### Точные controls

1. Single-line URL input.
2. Primary button `Get options`.
3. Secondary button `Choose file…`.
4. Tertiary text action `Add multiple links`.
5. Маленькая local-first строка.
6. Recent results показываются только если Library непустая.

### Input behavior

- URL вставляется стандартным paste.
- `Enter` запускает `Get options`.
- При multi-line paste приложение определяет несколько URL и показывает:
  `12 links detected — Review batch`.
- При drag local file main area становится drop target:
  `Drop audio or video to continue`.
- При drag text/URL можно принять URL.
- Ошибка валидации показывается прямо под input, а не toast.

### Empty state

Не использовать большую пустую панель. Первый экран должен занимать верхние 250–350 px, а не имитировать dashboard.

### Exact copy

```text
Title: New task
Input label: Media link
Placeholder: Paste a media link
Primary: Get options
Secondary: Choose file…
Tertiary: Add multiple links
Privacy line: Downloads and processing run on this computer.
```

---

## 3.4. URL analysis result

### Layout

```text
[thumbnail]  Title
             source · duration · uploader
             [More •••]

Output
[Video] [Audio] [Subtitles]

(o) Best available
    One playable file with video and audio
    MP4 preferred · 2160p · ~420 MB

( ) Up to 1080p
    One playable file with video and audio
    MP4 preferred · ~150 MB

( ) Up to 720p
    Smaller playable file with video and audio
    MP4 preferred · ~70 MB

[Options ▾]

───────────────────────────────────────────────────────────────
Save to  Downloads/Universal Media Extractor       [Change…]
Selected: Best available · MP4 preferred · 2160p
                                              [Download]
```

### Media summary

Показывать:

- thumbnail;
- title;
- duration;
- uploader/channel, если доступно;
- source domain;
- warning badge только при реальной проблеме.

`Open source page` переносится в `•••` menu или secondary link внутри details. Он не должен конкурировать с output selection.

### Output category control

Использовать compact segmented control:

```text
Video | Audio | Subtitles
```

Не использовать:

- пять смешанных cards разных типов;
- command-style picker;
- длинный dropdown всех streams;
- raw technical rows.

### Sticky action bar

После выбора preset action bar остаётся в одном месте. Не создавать новую большую Download-карточку ниже.

Action bar содержит:

- выбранный outcome;
- save location;
- `Options`;
- primary `Download`.

---

## 3.5. Local file intake

### До выбора

На `New task` пользователь нажимает `Choose file…` или перетаскивает файл.

Использовать native file dialog с фильтром поддерживаемых audio/video types. Не показывать браузерный `Choose File / No file chosen`.

### После выбора

Анализ начинается автоматически.

```text
[media icon/thumbnail] Interview.mov
22:14 · Video · 1.4 GB

Transcribe locally
Language       Auto-detect
Quality        Balanced
Output         Text
Save to        Next to original file          [Change…]

[Transcribe]
```

### Важное архитектурное изменение

Для desktop build локальный файл не следует без необходимости копировать целиком в managed output. Рекомендуемое поведение:

- читать source in-place;
- временное extracted audio хранить в app temp;
- transcript сохранять рядом с original либо в выбранную папку;
- удалить temp после успешного завершения;
- копировать source только если пользователь явно выбрал `Organize a copy in Library`.

Если backend пока способен только копировать файл, UI обязан честно показать это до начала процесса.

### Quality profiles

Публичные названия:

- `Fast`
- `Balanced` — default
- `More accurate`

Технический Whisper model показывается только в `Advanced`. Mapping должен определяться платформой и доступной памятью.

### Output formats

В текущем коде подтверждены:

- TXT;
- Markdown;
- JSON.

Public beta:

- `Text (.txt)` — default;
- `Markdown (.md)`;
- `JSON` — только Advanced.

`SRT/VTT transcription export` нельзя заявлять, пока он не реализован и не протестирован. Это не то же самое, что скачивание source subtitles.

---

## 3.6. Add multiple links / Batch composer

### Entry

`Add multiple links` открывает отдельный screen или sheet, а не новый top-level mode.

```text
Add multiple links

[ multiline textarea                                      ]
[ one URL per line                                        ]

[Paste] [Import text file…]

12 valid · 1 duplicate · 2 invalid

[Cancel]                                      [Review 12 links]
```

### После Review

```text
Batch review

Output preset
[Video]  Up to 1080p                         [Change]

Save to
Downloads/Universal Media Extractor          [Change…]

Items
[x] Title / URL                         Ready
[x] Title / URL                         Ready
[ ] Invalid URL                         Needs attention

Concurrency is managed automatically.

[Back]                                  [Start 11 downloads]
```

### Правила

- Удалять точные duplicate URLs до queue с понятным summary.
- Для playlist URL сначала показать список items и count.
- Один shared preset применяется ко всей batch в beta.
- Per-item override отложить.
- Concurrency не показывать в основном flow; default хранится в Settings.
- `Analyze playlist` как отдельная кнопка удалить.
- `Import URLs`, `Paste`, `Text file` объединить в composer.

---

## 3.7. Queue

### Назначение

Queue — operational screen для queued/running/failed tasks. Она не является Library.

### Layout

```text
Queue                                      [Clear completed]

Active 2 · Waiting 4 · Failed 1

[thumb] Title
        Downloading video · 62%
        18.4 MB/s · 00:42 remaining
        [Cancel]

[icon]  Title
        Waiting
        [Remove]

[icon]  Title
        Failed · Connection interrupted
        [Retry] [Details]

Completed
[compact collapsed rows]
```

### Row contents

- thumbnail или media type icon;
- title, если получен, иначе hostname/short URL;
- stage;
- honest progress;
- speed/ETA только если данные устойчивы;
- compact actions.

### Allowed row actions

| State | Actions |
|---|---|
| queued | `Remove` |
| running | `Cancel` |
| canceling | disabled `Canceling…` |
| failed | `Retry`, `Details`, `Remove` |
| completed | `Open`, `Show in…`, `Remove from Queue` |
| cancelled | `Retry`, `Remove` |

`Clear completed` удаляет строки из Queue, но не файлы и не Library records.

### Persistence

После restart:

- queued tasks восстанавливаются;
- running task становится `Interrupted`;
- пользователь видит `Retry`;
- completed results остаются в Library;
- failed diagnostics не теряются.

---

## 3.8. Library

### Решение

Library — отдельный screen, всегда доступный через sidebar. Не footer и не modal.

### Layout

```text
Library

[Search files and results…]       [All ▾] [Newest ▾]

All | Media | Transcripts | Failed

[thumb] Title
        Video · MP4 · 1080p · 152 MB
        Today, 11:42
                                        [Open] [•••]

[icon]  Interview transcript
        Text · 24 KB
        Yesterday
                                        [Open] [•••]
```

### Row actions

`•••` menu:

- `Open file`;
- `Show in Finder` / `Show in File Explorer`;
- `Open source page`, если есть;
- `Transcribe locally`, если есть audio;
- `Copy path`;
- `Copy source link`;
- `Remove from Library`;
- `Delete files from disk…`.

### Delete semantics

Два разных действия обязательны:

1. `Remove from Library` — удаляет только index record.
2. `Delete files from disk…` — удаляет managed output после confirmation.

Confirmation показывает:

- точный folder path;
- количество файлов;
- общий размер;
- предупреждение, что действие необратимо.

Нельзя объединять эти действия.

### Missing file state

Если файл перемещён или удалён вне приложения:

```text
File not found
The file may have been moved or deleted.

[Locate file…] [Remove from Library]
```

### Free / Pro

- Free: последние 20 results.
- Pro: unlimited Library, search, filters, batch groups и сохранённые presets.

Search не должен отправлять данные в облако.

---

## 3.9. Download result

### Цель

Финальный state должен говорить «файл готов», а не показывать technical job output.

```text
Download complete

[thumbnail] Showreel.mp4
            MP4 · 1080p · 152 MB
            Downloads/Universal Media Extractor/Showreel/

[Open file] [Show in Finder] [Transcribe locally] [•••]
```

### Primary action

- macOS/Windows: `Open file`.

### Secondary actions

- `Show in Finder` / `Show in File Explorer`;
- `Transcribe locally`;
- `Copy path`;
- `Open source page`;
- `View details`.

### Details disclosure

Показывать по запросу:

- selected preset;
- final format;
- duration;
- source;
- created time;
- warnings;
- technical log link.

Не показывать raw command в основном result.

---

## 3.10. Transcription progress and result

### Progress

```text
Transcribing locally

Interview.mov
Preparing audio…
[ indeterminate progress ]

The file stays on this computer.

[Cancel]
```

Если можно честно определить segment/duration progress, использовать determinate progress. Иначе не показывать искусственные проценты.

### Result

```text
Transcript ready

Interview.txt
22:14 · Text

[ transcript preview, selectable ]

[Copy transcript] [Open file] [Show in Finder] [Export…]
```

### Preview

- selectable text;
- search по transcript можно отложить;
- не строить full editor в beta;
- max preview size ограничить, но весь файл остаётся доступен;
- если preview truncated, показать `Open full transcript`.

---

## 3.11. Error surface

Ошибки не должны оставлять пустой main panel.

### Inline input error

```text
Enter a complete http:// or https:// link.
```

Фокус остаётся в input. Backend request не выполняется.

### Operational error card

```text
This link could not be checked

Connection interrupted before the source responded.

[Try again] [Copy diagnostics]

Technical details ▾
```

### Правила

- Один human title.
- Одна короткая причина.
- Одно рекомендуемое действие.
- Secondary diagnostics.
- Raw details collapsed.
- Toast не используется как единственный носитель ошибки.
- Error state сохраняется в Queue/Library history.

---

## 3.12. Settings

Разделы:

```text
General
Downloads
Transcription
Library
Appearance
Privacy & Updates
Advanced & Support
License
```

Подробная модель приведена в разделе 9.

---

## 3.13. Upgrade sheet

Появляется только после public beta и только при осознанном вызове Pro feature.

```text
Batch downloads are available in Pro

Process URL lists and playlists in one queue, retry failed items,
and keep all results in Library.

One-time license · 3 personal devices

[Not now] [Upgrade to Pro]
```

Не показывать:

- launch modal;
- countdown;
- «осталось N downloads»;
- upgrade banner во время error/progress;
- блокировку уже начатой задачи;
- fake discount.

---


## 3.14. Visual system and interaction direction

### Общий характер

```text
Compact desktop utility
+ local file-manager/downloader logic
+ restrained native surfaces
- marketing dashboard
- developer console
- oversized cards
```

Интерфейс должен ощущаться как инструмент, который можно держать открытым рядом с Finder/File Explorer, а не как web-приложение с hero-блоками.

### Layout

- постоянный левый sidebar `184–192 px`;
- topbar не использовать как основную навигацию;
- main content top-aligned;
- content max width `920 px`;
- default window `1120 × 760`;
- vertical scroll появляется только при реальном содержимом;
- sticky bottom action bar используется только на screen с pending primary action;
- Queue/Library используют full-width list;
- Settings — two-column preferences;
- modal только для irreversible/multi-item confirmation;
- sheets/popovers — для Options, Upgrade и short task details.

### Density

Default density — компактная, но не «табличная»:

- base spacing unit: `4 px`;
- common gaps: `8 / 12 / 16 / 24 px`;
- control height: `34–36 px`;
- primary input height: `40 px`;
- list row: `56–64 px`;
- sidebar row: `36–40 px`;
- card radius: `8–10 px`;
- outer panel padding: `16–20 px`;
- maximum one nested card level.

Не использовать большие 32–48 px внутренние отступы, которые превращают utility в dashboard.

### Cards versus lists

Cards применяются только для:

- universal source composer;
- analyzed media summary;
- single result/error;
- first-run readiness.

Lists применяются для:

- output presets;
- Queue;
- Library;
- Batch review;
- model management.

Нельзя превращать каждый item в отдельную плавающую карточку.

### Typography

Использовать OS system font.

| Role | Size / weight |
|---|---|
| Screen title | 20–22 px, semibold |
| Section title | 14–15 px, semibold |
| Body / control | 13–14 px, regular |
| Row metadata | 12 px, regular |
| Helper / caption | 11–12 px, regular |
| Monospace | Только paths/error codes в Technical details |

Правила:

- sentence case;
- не использовать all caps;
- один screen title;
- не дублировать title внутри первой card;
- paths middle-truncated;
- filenames preserve extension.

### Semantic color tokens

Конкретные значения могут быть адаптированы под platform rendering, но структура должна быть фиксированной.

Dark:

```text
background          #111315
sidebar             #15181B
surface             #1A1E22
surface-raised      #20252A
border              #2B3137
text-primary        #F1F3F5
text-secondary      #A6AFB8
text-muted          #78828C
accent              #6F91B5
accent-soft         rgba(accent, 0.14)
success             muted green
warning             muted amber
danger              muted red
```

Light:

```text
background          #F5F6F7
sidebar             #ECEFF1
surface             #FFFFFF
surface-raised      #F9FAFB
border              #D7DCE1
text-primary        #171A1D
text-secondary      #56606A
text-muted          #7A858F
accent              #4F7399
accent-soft         rgba(accent, 0.10)
```

Использовать semantic tokens, а не hard-coded colors по компонентам. Accent не должен быть ярко-синим «SaaS CTA». Success/warning/danger не используются как decoration.

### Icons

- один outline icon set;
- 16 px в controls, 18–20 px в sidebar;
- icon всегда имеет visible label для важных actions;
- icon-only допускается только для повторяемого `•••`, close и reveal с tooltip/accessibility label;
- platform-specific Finder/File Explorer icon/label допустим.

### Selection and focus

- selected preset: border + soft background + radio state;
- selected nav: soft background + text weight;
- focus ring 2 px, видимый в dark/light;
- hover не является единственным состоянием;
- keyboard selection mirrors pointer behavior;
- disabled control всегда имеет explanation.

### Empty states

Empty state — компактная строка/панель с действием, без иллюстрации:

Queue:

```text
No active tasks
New downloads and transcriptions will appear here.
[New task]
```

Library:

```text
No saved results yet
Completed files and transcripts will appear here.
[New task]
```

Subtitles:

```text
No source subtitles were found.
[Choose Audio] [Choose Video]
```

### Animation

- 120–180 ms for hover/selection/sheet;
- no spring/bounce;
- progress spinner respects Reduce Motion;
- list insertion may fade/slide ≤8 px;
- completion does not use confetti;
- layout should not jump when selecting a preset.

### Accessibility

- all controls reachable by keyboard;
- visible labels, not placeholder-only;
- screen-reader announcement for analysis/progress/completion/error;
- progress exposes stage/value;
- radio rows use actual semantic radio behavior;
- color never carries state alone;
- hit targets ≥32×32 px desktop;
- text remains usable at OS scaling 200%;
- thumbnail decorative alt suppressed; meaningful title read once;
- error focus moves to error summary, not Technical details.

### Responsive window behavior

At minimum width `920 px`:

- sidebar remains visible;
- metadata/path shorten;
- right-side row metadata may move below title;
- action bar stacks save location above button;
- no horizontal scrolling.

Below minimum width, app prevents further resize rather than collapsing into a mobile layout. Mobile/responsive web design is not a beta goal.


---

# 4. Полная карта кнопок и действий

## 4.1. Primary buttons

| Label | Screen | Условие | Результат |
|---|---|---|---|
| `Get options` | New task | Валидный single URL | Запускает analysis |
| `Review links` | Batch composer | Есть ≥2 валидных URL | Открывает batch review |
| `Start N downloads` | Batch review | Есть выбранные ready items | Создаёт queue tasks |
| `Download` | Output selection | Выбран доступный preset и writable folder | Ставит задачу в Queue |
| `Transcribe` | Local file | Файл проанализирован и model доступна/может быть загружена | Запускает local transcription |
| `Open file` | Download result | Final file существует | Открывает default OS app |
| `Copy transcript` | Transcript result | Transcript готов | Копирует полный текст |
| `Retry` | Failed task | Ошибка retryable | Создаёт повторную попытку |
| `Update engine and retry` | Engine error | Доступен update | Обновляет media engine и повторяет |
| `Upgrade to Pro` | Upgrade sheet | После beta | Открывает secure external checkout |

## 4.2. Secondary buttons

| Label | Назначение |
|---|---|
| `Choose file…` | Native local file picker |
| `Change…` | Native folder picker |
| `Paste` | Вставить clipboard в batch composer |
| `Import text file…` | Импорт `.txt`/`.csv` со списком URL |
| `Show in Finder` / `Show in File Explorer` | Показать final file |
| `Transcribe locally` | Начать secondary transcription для saved media |
| `Open source page` | Открыть original URL |
| `Open folder` | Открыть output directory |
| `Export…` | Экспортировать transcript в поддерживаемый формат |
| `Locate file…` | Связать Library record с перемещённым файлом |
| `Not now` | Закрыть upgrade sheet |

## 4.3. Destructive actions

| Label | Поведение |
|---|---|
| `Cancel` | Останавливает active task best-effort; app-managed partial files очищаются |
| `Cancel remaining` | Останавливает queued/running items batch |
| `Delete files from disk…` | Confirmation с path/count/size |
| `Clear temporary files…` | Confirmation, не затрагивает final outputs |
| `Reset settings…` | Confirmation и список сбрасываемых параметров |
| `Deactivate license` | Confirmation, не удаляет приложение или файлы |

`Remove from Queue` и `Remove from Library` не являются destructive для файлов и не должны быть красными.

## 4.4. Copy / reveal actions

- `Copy path`;
- `Copy source link`;
- `Copy transcript`;
- `Copy diagnostics`;
- `Show in Finder`;
- `Show in File Explorer`;
- `Open logs folder`.

После copy показывать короткий non-blocking toast:

```text
Path copied
Transcript copied
Diagnostics copied
```

## 4.5. Retry / cancel actions

- `Retry`;
- `Retry failed`;
- `Retry all failed`;
- `Cancel`;
- `Cancel remaining`;
- `Remove queued item`.

Не добавлять `Pause`, пока backend не умеет корректный resume.

## 4.6. Advanced / support actions

- `Options`;
- `Technical details`;
- `Check for app updates`;
- `Check media engine`;
- `Open logs folder`;
- `Copy diagnostics`;
- `Report a problem`;
- `View limitations`;
- `Manage transcription models`.

## 4.7. Кнопки, которые нужно убрать или скрыть

- `Analyze local file`;
- `Analyze playlist`;
- отдельные `Import URLs` и `Text file` рядом с `Paste`;
- `Course`;
- `Chrome session`;
- `Manual cookies`;
- main-screen `Format` dropdown;
- main-screen Whisper model names;
- `Advanced save options` в основном flow;
- raw `Clear`/`Reset` без понятного объекта;
- любые кнопки, раскрывающие CLI arguments;
- повторяющиеся `Recommended` badges в одной категории.



# 5. Финальные core user flows

## 5.1. Общая state machine

Все типы задач должны использовать одну модель состояний:

```text
idle
→ validating
→ analyzing
→ ready
→ queued
→ running
→ post_processing
→ completed

                    ↘ failed
                    ↘ cancelled
```

Технические состояния не должны показываться пользователю буквально. UI переводит их в понятные этапы:

| Backend / internal | User-facing stage |
|---|---|
| `validating` | `Checking input…` |
| `analyzing` | `Checking source…` или `Reading file…` |
| `queued` | `Waiting` |
| download video stream | `Downloading video…` |
| download audio stream | `Downloading audio…` |
| merge/remux | `Combining video and audio…` |
| audio conversion | `Converting audio…` |
| subtitle write/convert | `Saving subtitles…` |
| file finalization | `Saving file…` |
| model download | `Preparing transcription model…` |
| audio extraction | `Preparing audio…` |
| Whisper | `Transcribing locally…` |
| completed | `Saved` / `Transcript ready` |
| failed | Нормализованное human-readable error |
| cancelled | `Cancelled` |

Правила:

- `ready` существует только после успешного анализа и до постановки задачи в Queue.
- `post_processing` обязателен как отдельное внутреннее состояние: нельзя показывать `100%` во время merge/conversion.
- Один UI-компонент задачи используется в single и batch flows.
- Completed job не исчезает автоматически из Queue до закрытия текущей сессии; затем остаётся в Library.
- После перезапуска interrupted task получает статус `Interrupted`, а не продолжает выглядеть как `Running`.

## 5.2. Первый запуск приложения

1. App проверяет writable default folder, наличие `ffmpeg/ffprobe`, состояние media engine и доступность выбранного transcription model.
2. Проверка выполняется без модального onboarding.
3. При готовности открывается `New task`.
4. Под source composer показывается одна строка:
   ```text
   Downloads and transcription run locally on this computer.
   ```
5. Если компонент отсутствует, показывается readiness card только для необходимой функции:
   ```text
   Media tools need to be prepared
   Universal Media Extractor will install the components required
   to analyze and save supported media.
   [Prepare tools]
   ```
6. До нажатия `Prepare tools` никакая крупная модель Whisper не загружается.
7. Terms/rights notice показывается один раз при первом фактическом Download:
   ```text
   Only save media you own or are permitted to use.
   [Cancel] [Continue]
   ```
   Согласие хранится локально. Оно не повторяется на каждом экране.

## 5.3. Один URL: скачивание видео

Целевой путь:

```text
New task
→ paste URL
→ Get options
→ media summary
→ Video / Best available selected
→ Download
→ Queue progress
→ Saved result
```

Пошагово:

1. Пользователь вставляет URL.
2. Поле валидирует схему и структуру локально.
3. `Get options` становится active.
4. Enter запускает analysis.
5. На время анализа input остаётся видимым; button превращается в `Checking…` со spinner.
6. После анализа:
   - title, source, duration и thumbnail появляются над controls;
   - `Video` активен по умолчанию;
   - первый уникальный video preset выбран;
   - save folder берётся из Settings.
7. Пользователь нажимает `Download`.
8. Задача сразу появляется в Queue.
9. Main panel может:
   - автоматически открыть Queue для первой задачи;
   - либо оставить компактный progress card на текущем экране.  
   Финальное решение: **для первой задачи оставить inline progress; при двух и более задачах открыть Queue**.
10. На завершении показывается:
    ```text
    Saved
    <filename>.mp4 · 12 MB
    [Open file] [Show in Finder]
    ```
11. Secondary actions: `Transcribe locally`, `Copy path`, `Open source page`.
12. Следующая новая задача доступна без очистки Library.

Целевое количество решений после вставки ссылки: **не более трёх** — проверить источник, выбрать outcome, скачать.

## 5.4. Один URL: audio-only

```text
Paste URL
→ Get options
→ Audio
→ M4A · Recommended
→ Download
→ Saved
```

Поведение:

1. После analysis пользователь выбирает segment `Audio`.
2. Default — `M4A · Recommended`, если source и conversion path поддерживают его.
3. `MP3 · Most compatible` и `WAV · For editing · Large file` доступны ниже.
4. Для WAV показывается оценка размера, если она вычислима; иначе `Large file`.
5. Main action остаётся `Download`, а не `Convert`.
6. После завершения result card показывает фактический формат и размер.
7. `Transcribe locally` доступен как result action.
8. Original video не хранится, если он использовался только как временный source и workflow завершён успешно.

## 5.5. Один URL: source subtitles

```text
Paste URL
→ Get options
→ Subtitles
→ select language and source type
→ SRT
→ Download subtitles
```

Поведение:

- Segment называется `Subtitles`, не `Transcript`.
- Каждая строка: язык, `Manual` или `Auto-generated`, доступность.
- Если для языка есть manual и auto, manual располагается первой.
- Default output: SRT.
- VTT находится в `Options`.
- Можно выбрать несколько языков только в Pro либо позднее; beta может поддерживать один язык за задачу.
- Если subtitles отсутствуют:
  ```text
  No source subtitles were found.
  You can download the media and create a local transcript instead.
  [Choose Audio] [Choose Video]
  ```
- Нельзя называть созданную Whisper-расшифровку «downloaded subtitles».

## 5.6. Локальный файл: транскрипция

```text
New task
→ Choose file… / drop file
→ automatic local analysis
→ transcription setup
→ Transcribe
→ progress
→ transcript result
```

Пошагово:

1. Пользователь перетаскивает audio/video file или нажимает `Choose file…`.
2. App получает native filesystem path; браузерного upload-контрола нет.
3. `ffprobe` запускается автоматически.
4. UI показывает:
   - filename;
   - audio/video;
   - duration;
   - size;
   - при video — `Audio will be prepared locally before transcription`.
5. Default quality: `Balanced`.
6. Default language: `Auto-detect`.
7. Default transcript format: `Text (.txt)`.
8. Default save destination:
   - `Next to original file`, если directory writable;
   - иначе configured UME folder.
9. Если модель ещё не установлена, рядом с profile показывается:
   ```text
   Download required · <actual model size>
   ```
10. `Transcribe` запускает model preparation при явном согласии.
11. Source media не копируется в UME output по умолчанию.
12. Временное extracted audio удаляется после успешной транскрипции; при ошибке — по cleanup policy.
13. Result:
   - preview;
   - `Copy transcript`;
   - `Open transcript`;
   - `Show in Finder/File Explorer`;
   - `Export…`, если доступны дополнительные форматы.

Нельзя обещать SRT/VTT export для local Whisper, пока это не реализовано и не проверено. В исходном описании подтверждены TXT, Markdown и JSON.

## 5.7. Batch URL processing

Entry:

```text
New task
→ Add multiple links
→ paste/import list
→ Review links
→ choose preset for all
→ Start N downloads
→ Queue
```

Пошагово:

1. Secondary action `Add multiple links` раскрывает batch composer.
2. Textarea принимает:
   - по одному URL в строке;
   - pasted clipboard;
   - `.txt`;
   - `.csv` с обнаружением URL columns.
3. Client-side parser:
   - удаляет пустые строки;
   - нормализует whitespace;
   - схлопывает exact duplicates;
   - помечает invalid rows.
4. `Review links` запускает параллельный ограниченный analysis.
5. Review table показывает:
   - checkbox;
   - title/source;
   - status;
   - duration;
   - warning;
   - selected common preset.
6. Playlist URL после analysis разворачивается в selectable items, но не начинает download автоматически.
7. Default selection — все successfully analyzed items.
8. Один общий preset применяется ко всем, где доступен.
9. Недоступные items получают fallback suggestion или status `Preset unavailable`.
10. В public beta per-item format customization не требуется.
11. `Start N downloads` создаёт group и tasks.
12. Queue показывает group header:
    ```text
    Batch · 18 items
    7 completed · 2 running · 8 waiting · 1 failed
    ```
13. Failed items не блокируют остальные.
14. После завершения доступны `Retry failed` и `Show results in Library`.

Правила ограничения:

- Free после коммерческого запуска не получает Batch либо получает пробный batch из 3 items один раз; предпочтительно **полностью оставить Batch в Pro**, чтобы граница была простой.
- Public beta получает Batch целиком для проверки reliability.
- Concurrency default: 2; допустимый range Pro: 1–4.
- Unlimited concurrency не предлагать: источники, сеть и disk I/O делают это ненадёжным.

## 5.8. Playlist URL

Playlist — не отдельный режим.

```text
Paste playlist URL
→ Get options
→ detected collection
→ Review N items
→ select items
→ common output preset
→ Start N downloads
```

Если пользователь Free:

```text
This link contains 24 items.
Single-item downloads are available in Free. Batch collections require Pro.

[Choose one item] [Upgrade to Pro]
```

Во время public beta paywall отсутствует.

## 5.9. Failed source

Flow:

```text
Analyze
→ normalized failure
→ one recommended action
→ optional diagnostics
```

Примеры:

### Unsupported / changed source

```text
This source is not currently supported

The site may have changed or this type of link may not be available.

[Check for engine update] [Copy diagnostics]
```

### Access required

```text
This source requires access

Universal Media Extractor does not bypass sign-in, private access,
paywalls, CAPTCHA, or other source restrictions.

[Open source page] [Copy diagnostics]
```

### Protected media

```text
This media is protected

Protected media cannot be processed by Universal Media Extractor.

[Choose another source]
```

После ошибки:

- URL остаётся в input;
- user can edit and retry;
- failed analysis сохраняется только в diagnostics/recent attempts, но не засоряет Library media list;
- task-level failure сохраняется в Queue/Library для batch;
- technical details раскрываются только по запросу.

## 5.10. Saved result

Flow:

```text
Task completed
→ result card
→ Open / Reveal / Transcribe / Copy path
→ Library record
```

Result card содержит только итоговые артефакты, а не request metadata и logs:

```text
Saved
Video · MP4 · 1080p · 12 MB
My video.mp4

[Open file] [Show in Finder]
Transcribe locally · Copy path · Open source page
```

Если создано несколько файлов, например subtitle package:

```text
Saved 2 subtitle files
English · SRT
Russian · SRT

[Open folder]
```

Metadata/logs скрыты под `Details` или доступны через support actions.

## 5.11. Повтор задачи из Library

```text
Library item
→ More
→ Download again
→ New task prefilled with source and prior preset
```

Не запускать повтор автоматически. Это важно, потому что source availability и output options могли измениться.

## 5.12. Keyboard and drag/drop flows

Минимальные shortcuts:

| Shortcut | Action |
|---|---|
| `Cmd/Ctrl + L` | Focus source input |
| `Cmd/Ctrl + V` в empty New task | Paste and validate |
| `Cmd/Ctrl + O` | Choose local file |
| `Cmd/Ctrl + Shift + V` | Open batch composer and paste |
| `Cmd/Ctrl + ,` | Settings |
| `Cmd/Ctrl + K` | Focus Library search |
| `Esc` | Close sheet/details; не отменяет active job без confirmation |
| `Space` on selected completed item | Quick preview/open, только если platform convention позволяет |

Drop behavior:

- один local file → local transcription flow;
- один `.txt/.csv` → batch import preview;
- URL text → URL flow;
- несколько media files → beta показывает `Multiple local files are not supported yet`, без молчаливого игнорирования.

---

# 6. Output preset model

## 6.1. Основной принцип

Пользователь выбирает **результат**, а не container/codec/stream.

Иерархия:

```text
Output category
→ Human preset
→ Optional advanced override
```

Main UI:

```text
[ Video ] [ Audio ] [ Subtitles ]

○ Best available             MP4 preferred · video + audio
○ Up to 1080p                MP4 preferred · video + audio
○ Up to 720p                 Smaller file · video + audio
```

Не показывать:

- `format_id`;
- raw codec;
- stream count;
- audio/video stream pairing;
- bitrate;
- protocol;
- extractor key;
- `bestvideo+bestaudio`;
- длинный список разрешений, если три presets решают задачу.

## 6.2. Video presets

Фиксированные semantic IDs:

| ID | UI label | Selection rule | User promise |
|---|---|---|---|
| `video_best` | `Best available` | Наивысшее доступное качество, которое можно финализировать в один playable file | Максимальное доступное качество |
| `video_1080` | `Up to 1080p` | Лучшее качество `≤1080p` | Ограничение по высоте, один файл |
| `video_720` | `Up to 720p` | Лучшее качество `≤720p` | Более компактный файл, один файл |

Динамическая дедупликация обязательна:

1. Resolver вычисляет фактический stream plan для каждого semantic preset.
2. Если два presets разрешаются в один и тот же video/audio pair и container outcome, UI оставляет один.
3. Если source максимум 720p:
   - показать `Best available · 720p`;
   - скрыть `Up to 1080p` и `Up to 720p` как дубли.
4. Если source максимум 1080p:
   - показать `Best available · 1080p`;
   - показать `Up to 720p`, если он действительно отличается;
   - скрыть `Up to 1080p`.
5. Если source 4K:
   - показать все три уникальных outcomes.
6. Если exact size неизвестен, не выдумывать. Показывать resolution/container без размера.
7. Если размер оценочный, использовать `~`:
   ```text
   MP4 · 1080p · ~95 MB
   ```

Каждая video row содержит постоянную подпись:

```text
One playable file with video and audio
```

Это должно быть правдой на уровне engine contract. Если MP4 без перекодирования невозможен:

- `Auto` может выбрать MKV;
- UI заранее пишет `MKV required for this source`;
- нельзя завершить задачу двумя отдельными файлами, если пользователь выбрал обычный Video preset.

## 6.3. Video container behavior

Main default:

```text
Container: Auto
```

Логика `Auto`:

1. MP4 preferred, когда selected streams можно безопасно merge/remux.
2. MKV fallback, когда MP4 несовместим без дорогого/рискованного transcoding.
3. WEBM только при явном advanced selection либо когда source naturally requires it и outcome понятен.
4. Фактический container показывается до запуска, если его можно определить; иначе — после finalization.

Advanced override:

```text
Options
Container
○ Auto · Recommended
○ MP4
○ MKV
○ WEBM
```

При выборе incompatible override UI блокирует action с объяснением либо предлагает fallback. Silent failure запрещён.

## 6.4. Audio presets

| ID | UI label | Format | Purpose |
|---|---|---|---|
| `audio_m4a` | `M4A · Recommended` | M4A/AAC where possible | Хорошее качество и размер |
| `audio_mp3` | `MP3 · Most compatible` | MP3 | Максимальная совместимость |
| `audio_wav` | `WAV · For editing` | PCM WAV | Монтаж/архив, большой файл |

Правила:

- M4A selected by default.
- `Original audio` не показывать в beta: его поведение непредсказуемо для обычного пользователя.
- Lossless claims запрещены, если source уже lossy.
- WAV copy:
  ```text
  Uncompressed output. It will not restore quality lost in the source.
  ```
  Это предотвращает ложное обещание «улучшения качества».
- Bitrate selector не нужен в beta.
- Audio normalization, trimming and metadata editor — later.

## 6.5. Source subtitle presets

UI category:

```text
Subtitles
```

Row fields:

- language display name;
- language code secondary;
- badge `Manual` / `Auto-generated`;
- estimated/known format availability;
- selection radio or checkbox.

Default:

```text
Format: SRT
```

Optional under `Options`:

```text
VTT
```

Rules:

- manual before auto;
- deduplicate by language + type;
- do not expose every source-internal subtitle extension;
- converted output status must say `Converted to SRT`;
- if conversion fails, keep original only when this is clearly reported;
- subtitles are their own task and do not silently download video.

## 6.6. Local transcript presets

Public, non-technical quality profiles:

| Profile | Internal mapping | Copy |
|---|---|---|
| `Fast` | Smallest supported model suitable for product baseline | Fastest, lower accuracy |
| `Balanced` | Product default | Best default for most recordings |
| `More accurate` | Larger local model | Slower, uses more memory and disk |

Model mapping must be platform-aware and stored in configuration, not hard-coded in UI copy. Technical model names (`tiny`, `base`, `small`, `medium`, `turbo`) appear only in Advanced.

Confirmed output formats from current product source:

- Text `.txt`;
- Markdown `.md`;
- JSON `.json`.

Recommended beta default: TXT. Markdown can be a normal secondary option. JSON belongs in Advanced. SRT/VTT transcription output must be omitted until implementation and QA confirm timestamped output.

## 6.7. Preset row component specification

Each row:

```text
┌──────────────────────────────────────────────────────────┐
│ ○  Up to 1080p                             MP4 · ~95 MB │
│    One playable file with video and audio               │
└──────────────────────────────────────────────────────────┘
```

Dimensions:

- minimum row height: 56 px;
- horizontal padding: 14–16 px;
- radio hit area: at least 32×32 px;
- whole row clickable;
- title 13–14 px semibold;
- metadata 12 px regular;
- helper 11–12 px muted;
- selected row: subtle accent border and background, not filled saturated card;
- disabled row: reason always visible or available via tooltip/focus description.

Badges allowed:

- `Recommended`;
- `Manual`;
- `Auto-generated`;
- `Pro`;
- `Unavailable`.

No more than one promotional badge per row.

## 6.8. Save location placement

Save location appears in sticky action bar **after output selection and before action**:

```text
Save to  ~/Downloads/Universal Media Extractor        Change…
                                                    [Download]
```

Rules:

- path is read-only;
- truncate middle, preserve final folder;
- full path in tooltip and accessibility label;
- `Change…` opens native folder picker;
- chosen one-off folder applies to current task only;
- user can select `Use as default` inside native-result sheet, not in main screen;
- invalid/non-writable folder detected before queuing;
- external/removable drive disconnect produces a specific error.

## 6.9. Filename behavior

Default template internal:

```text
{title}
```

File collision default:

```text
Keep both
```

Examples:

```text
My video.mp4
My video 2.mp4
```

Settings/Pro later:

- `{title}`;
- `{source}`;
- `{channel}`;
- `{date}`;
- `{playlist_index}`;
- `{resolution}`.

Main UI never exposes a raw template string.

## 6.10. Preset resolver acceptance criteria

- No two visible rows produce the same semantic outcome.
- All Video presets produce one playable final file.
- Main flow never exposes stream IDs.
- Unknown sizes are omitted, not represented as zero.
- Estimated sizes carry `~`.
- Selected preset remains stable while changing save folder.
- Re-analysis invalidates stale preset data safely.
- A source update cannot leave a previously selected unavailable row silently active.
- Exact final container/size/path are written back to Result and Library.

---

# 7. Library and history model

## 7.1. Queue and Library are different products

```text
Queue = operational work
Library = durable record of completed/failed work and saved artifacts
```

Do not combine them into one ambiguous `History` view.

### Queue owns

- waiting;
- running;
- post-processing;
- interrupted;
- failed tasks requiring action;
- current-session completed tasks;
- batch groups;
- cancel/retry.

### Library owns

- completed media;
- completed transcripts;
- durable failed records, if user chooses to view them;
- source and output metadata;
- file existence;
- open/reveal/delete/repeat;
- search/filter.

## 7.2. Persistence requirement

Persistent Queue/Library is P0 for a paid desktop utility.

Minimum durable schema:

```text
task
- id
- group_id nullable
- source_type: url | local_file
- source_url nullable
- source_path nullable
- source_display
- title
- thumbnail_path/url nullable
- task_type: media | subtitles | transcription
- preset_id
- preset_snapshot_json
- requested_output_folder
- status
- user_stage
- progress nullable
- created_at
- started_at nullable
- completed_at nullable
- error_code nullable
- error_summary nullable
- diagnostics_ref nullable
- retry_of nullable

artifact
- id
- task_id
- role: media | subtitle | transcript | metadata | log
- path
- display_name
- media_type
- container_or_format
- size_bytes nullable
- duration_seconds nullable
- managed_by_app
- exists_last_checked
- created_at

batch_group
- id
- display_name
- source_kind
- total_count
- created_at
```

SQLite is appropriate. The app must use migrations and transactions. A JSON output index alone is not sufficient for reliable restart recovery.

## 7.3. Conflict to resolve before implementation

Source documents disagree:

- one pack says SQLite history and Batch already exist;
- another says jobs are in-memory, database and Batch are not implemented.

Required engineering action:

1. inspect current repository;
2. identify authoritative branch/commit;
3. run restart tests;
4. document actual schema/endpoints;
5. align product docs;
6. only then estimate UI work.

Until this is done, no claim such as `Your queue is safely restored` may appear publicly.

## 7.4. Library screen layout

Header:

```text
Library                                      Search
[All] [Media] [Transcripts] [Failed]
```

List row:

```text
[thumbnail/icon] Title
                 Video · MP4 · 1080p · 12 MB
                 Saved Aug 7 · ~/Downloads/…
                                   [Open] [Reveal] [•••]
```

Responsive behavior:

- ≥1040 px: optional metadata columns;
- 920–1039 px: compact rows;
- no card mosaic;
- thumbnails fixed 64×40 or 56×56 for audio/transcript;
- one-line title with tooltip;
- path only secondary and middle-truncated.

Sort:

- newest first default;
- name;
- size;
- source;
- status.

Search:

- title;
- filename;
- source domain;
- transcript filename;
- batch name.

Do not index full transcript content in beta unless performance and privacy are explicitly designed.

## 7.5. Filters and status

Primary filters:

- `All`;
- `Media`;
- `Transcripts`;
- `Failed`.

Optional later:

- source;
- date;
- file type;
- batch;
- missing files.

Status labels:

- `Saved`;
- `Transcript ready`;
- `Failed`;
- `Missing`;
- `Deleted`;
- `Interrupted`.

A completed record whose file is gone becomes `Missing`; it is not silently deleted.

## 7.6. Library actions

Primary row action:

- `Open`.

Secondary:

- `Show in Finder` / `Show in File Explorer`;
- `Copy path`;
- `Open source page`;
- `Transcribe locally`;
- `Download again`;
- `Locate file…`;
- `Remove from Library`;
- `Delete files from disk…`.

Rules:

- `Remove from Library` does not touch files.
- `Delete files from disk…` is available only for managed outputs inside approved output roots.
- External local files are never deleted by UME through Library.
- Deleting a media artifact does not automatically delete transcript unless user selects both.
- Confirmation states exact files/count/size/path.

## 7.7. Missing and moved files

When file check fails:

```text
File not found

It may have been moved or deleted outside Universal Media Extractor.

[Locate file…] [Remove from Library]
```

`Locate file…`:

- opens native file picker;
- verifies likely type;
- updates artifact path;
- never silently copies the file.

Filesystem monitoring can be postponed; check existence when Library loads and before an action.

## 7.8. Batch groups in Library

Batch completion creates a collapsible group:

```text
Research references · 18 items
17 saved · 1 failed · 1.8 GB
```

Opening group filters list to those items. Individual files remain normal Library records.

Do not create deeply nested virtual folders in UI. Physical folder organization may follow a group naming rule.

## 7.9. Retention

Public beta:

- unlimited records locally;
- no cloud sync;
- no automatic deletion of final output;
- app-managed temporary files cleaned automatically.

Commercial Free:

- last 20 Library records visible;
- older files remain on disk;
- before hiding old records, app clearly states:
  ```text
  Your files are not deleted. Pro keeps an unlimited searchable Library.
  ```

Pro:

- unlimited local Library;
- search/filter;
- batch groups.

A hidden-history limit must never make files inaccessible or appear deleted.

## 7.10. Interrupted task recovery

At app startup:

1. tasks persisted as `running`/`post_processing` become `interrupted`;
2. partial files are inspected;
3. app determines:
   - safe retry from beginning;
   - safe resume, only if engine reliably supports it;
   - cleanup required.
4. UI:
   ```text
   Download was interrupted when the app closed.
   [Retry] [Remove]
   ```
5. Do not claim resume unless byte-range continuation has been tested per task type.
6. If final output exists and passes basic validation, reconcile as completed rather than duplicating it.

## 7.11. Library acceptance criteria

- Closing and reopening app does not lose task records.
- Completed files open from Library after restart.
- Missing files get explicit state.
- Removing a record never deletes external files.
- Safe delete cannot escape configured managed roots.
- Batch items remain individually actionable.
- Search stays responsive with at least 10,000 records.
- Paths and URLs are not sent off-device by Library.
- Free limit affects UI history only, never stored files.



# 8. Error, progress and result model

## 8.1. Основная иерархия состояния

Каждая задача имеет ровно одну dominant state surface:

```text
Ready
Progress
Success
Error
Cancelled
Interrupted
```

Нельзя одновременно показывать:

- большую progress card и отдельный технический job panel;
- success и unresolved warning одного уровня;
- generic error toast без состояния в main panel;
- `100%` и продолжать merge/conversion неопределённое время.

## 8.2. Progress component

Single task:

```text
Downloading video
My video
42% · 18.4 MB of ~44 MB · 6.2 MB/s

[████████░░░░░░░░░░]

Combining video and audio will follow.
                                              Cancel
```

Batch row:

```text
My video                     Downloading · 42%        Cancel
Another clip                 Waiting                  Remove
Podcast episode              Converting audio…        Cancel
```

Rules:

- determinate progress only when backend has reliable total;
- unknown total → indeterminate bar + downloaded bytes/time;
- speed/ETA optional and shown only when stable;
- stage label is more important than raw percentage;
- during merge/conversion use indeterminate stage, not frozen 100%;
- no fake smooth animation that masks stalls;
- elapsed time may appear after 10 seconds;
- cancel remains visible but secondary;
- OS notification only on completion/failure and only if enabled;
- app close with active tasks triggers:
  ```text
  2 tasks are still running.
  [Keep app open] [Cancel tasks and quit]
  ```
  Background/menu-bar operation can be postponed.

## 8.3. Error taxonomy

Backend should return stable codes; UI maps them to human copy. Raw CLI messages never become the primary error.

| Code | User title | Default explanation | Primary action |
|---|---|---|---|
| `INVALID_INPUT` | `Enter a valid link` | `Use a complete http:// or https:// address.` | Focus input |
| `UNSUPPORTED_SOURCE` | `This source is not currently supported` | `This type of link cannot be processed with the current media engine.` | `Check for engine update` |
| `SOURCE_UNAVAILABLE` | `This media is unavailable` | `The source was removed, restricted, or did not return media.` | `Open source page` |
| `ACCESS_REQUIRED` | `This source requires access` | `The public app does not bypass sign-in or private access.` | `Open source page` |
| `PROTECTED_MEDIA` | `This media is protected` | `Protected media cannot be processed.` | `Choose another source` |
| `REGION_RESTRICTED` | `This media is not available from your location` | `Universal Media Extractor does not bypass regional restrictions.` | `Open source page` |
| `RATE_LIMITED` | `The source temporarily refused the request` | `Try again later. Repeated retries may make the delay longer.` | `Try again later` |
| `NETWORK_ERROR` | `Connection interrupted` | `Check your connection and try again.` | `Retry` |
| `ENGINE_OUTDATED` | `The media engine may be out of date` | `An update may restore support for this source.` | `Update engine and retry` |
| `DISK_PERMISSION` | `The selected folder cannot be written to` | `Choose another folder or update its permissions.` | `Choose folder` |
| `DISK_FULL` | `Not enough free space` | `Free disk space or choose another destination.` | `Choose folder` |
| `PATH_TOO_LONG` | `The file path is too long` | `Choose a shorter destination or filename.` | `Choose folder` |
| `DOWNLOAD_FAILED` | `Download could not be completed` | `The source stopped responding or the media stream changed.` | `Retry` |
| `FINALIZATION_FAILED` | `The file could not be finalized` | `Download finished, but video and audio could not be combined.` | `Retry` |
| `SUBTITLE_UNAVAILABLE` | `These subtitles are no longer available` | `Choose another language or create a local transcript.` | `Choose output` |
| `LOCAL_FILE_UNREADABLE` | `This file could not be read` | `The file may be damaged or use an unsupported media format.` | `Choose another file` |
| `MODEL_MISSING` | `A transcription model is required` | `Download the selected local model before transcribing.` | `Download model` |
| `MODEL_LOAD_FAILED` | `The transcription model could not be loaded` | `Check free memory and reinstall the model.` | `Manage models` |
| `TRANSCRIPTION_FAILED` | `Transcription could not be completed` | `The audio could not be processed with the selected model.` | `Retry` |
| `TASK_INTERRUPTED` | `The task was interrupted` | `The app closed before processing finished.` | `Retry` |
| `UNKNOWN_ERROR` | `Something went wrong` | `Copy diagnostics to include with a support request.` | `Retry` |

## 8.4. Error card hierarchy

```text
[warning/error icon] This source is not currently supported

This type of link cannot be processed with the current media engine.

[Check for engine update]   Copy diagnostics

Technical details ▾
```

Visual rules:

- red is reserved for destructive failure, not every warning;
- source/access limitations can use neutral amber;
- title 14–15 px semibold;
- explanation max two short sentences;
- primary action left;
- diagnostics as text button;
- technical disclosure last;
- never show a wall of stderr by default.

## 8.5. Diagnostics model

`Copy diagnostics` should produce a redacted structured block:

```text
Universal Media Extractor diagnostics
App version: 0.x.x
OS: macOS 26.x / Windows 11
Architecture: arm64 / x64
Media engine version: …
FFmpeg version: …
Task type: URL analysis
Error code: ENGINE_OUTDATED
Source domain: example.com
Source URL included: no
Timestamp: ISO-8601
Correlation ID: local-random-id
Relevant log excerpt: <redacted>
```

Privacy rules:

- full source URL excluded by default;
- query parameters and tokens always redacted;
- filesystem username replaced with `~`;
- cookies, headers, passwords and browser data never included;
- user may opt in to `Include source URL` before copying;
- diagnostics remain local until user explicitly sends them;
- `Report a problem` opens a local preview before external mail/web action.

Technical details may show:

- stable error code;
- engine exit code;
- sanitized final lines;
- artifact/log location.

Do not expose the full command with tokens or cookies.

## 8.6. Warnings

Warnings are contextual, dismissible where appropriate, and do not look like failures.

Examples:

```text
Estimated size is unavailable for this source.
```

```text
Auto-generated subtitles may contain errors.
```

```text
This output will use MKV because the selected streams are not compatible with MP4.
```

```text
Transcription may be slow on this computer with the More accurate profile.
```

Do not repeat a generic rights disclaimer after every analysis. It belongs to onboarding, Terms, Help and the first confirmed Download action.

## 8.7. Success result hierarchy

Primary success:

```text
Saved
My video.mp4
Video · MP4 · 1080p · 12 MB

[Open file] [Show in Finder]
```

Secondary actions:

```text
Transcribe locally · Copy path · Open source page
```

Tertiary disclosure:

```text
Details ▾
```

Details may include:

- source;
- actual preset;
- final path;
- duration;
- created date;
- warnings;
- task ID;
- logs.

Never headline the result with:

- `Job succeeded`;
- raw output directory;
- request JSON;
- extractor name;
- command line.

## 8.8. Transcript result hierarchy

```text
Transcript ready
Interview.txt · 48 KB · English detected

[Copy transcript] [Open transcript]
Show in Finder · Export…
```

Preview:

- selectable text;
- search within preview optional later;
- max rendered preview size to protect memory;
- when truncated:
  ```text
  Previewing the first 50,000 characters.
  [Open full transcript]
  ```
- no rich editor in beta;
- no cloud summary CTA;
- no AI chat panel.

## 8.9. Cancel behavior

- `Cancel` is immediate for a single task; no modal unless app cannot safely clean partials.
- Button changes to `Cancelling…`.
- Backend sends termination, waits for cleanup, and persists final status.
- App-managed partial files are removed or placed in a clearly marked temp area.
- Final files that already validated are not deleted merely because a trailing metadata step was cancelled.
- Batch `Cancel remaining` requires confirmation because it affects multiple tasks:
  ```text
  Cancel 11 waiting or running tasks?
  Completed files will be kept.
  [Keep running] [Cancel remaining]
  ```
- Cancelled task can be retried.

## 8.10. Error/progress/result acceptance criteria

- Invalid URL gets inline feedback without backend call.
- Every backend error maps to a stable error code.
- Protected/access-required errors never suggest bypass actions.
- No progress bar reaches 100% before final file validation.
- App restart never leaves a permanent `Running` state.
- Copy diagnostics contains no secrets and no full URL by default.
- Completed result has a working Open/Reveal action.
- Failed Batch item does not stop the group.
- Errors remain understandable without opening Technical details.
- Result copy reports actual output, not requested output.

---

# 9. Settings and advanced model

## 9.1. Settings architecture

```text
Settings
├── General
├── Downloads
├── Transcription
├── Library
├── Appearance
├── Privacy & Updates
├── Advanced & Support
└── License
```

Use a native-feeling two-column preference layout on desktop:

- section navigation: 160–180 px;
- content width: 560–680 px;
- row labels left, controls right where platform-appropriate;
- no dashboard metrics;
- changes save immediately unless a restart is required;
- destructive/reset actions remain at section bottom.

## 9.2. General

| Setting | Default | Notes |
|---|---|---|
| Default save folder | `~/Downloads/Universal Media Extractor` | Native folder picker |
| When a filename exists | `Keep both` | Options: Replace only with explicit confirmation; Skip |
| Show completion notifications | On | Uses OS notification permission |
| Open app to | `New task` | Option: Queue when active tasks exist |
| Confirm before quitting with active tasks | On | Cannot be disabled until background mode exists |

Do not show:

- local backend address;
- port;
- API token;
- working directory;
- CLI path.

## 9.3. Downloads

| Setting | Default | Tier |
|---|---|---|
| Default output | `Video · Best available` | Free |
| Preferred video container | `Auto · MP4 preferred` | Free |
| Default audio format | `M4A` | Free |
| Default subtitle format | `SRT` | Free |
| Concurrent tasks | `2` | Pro; beta unlocked |
| Temporary file cleanup | `After successful completion` | Free |
| Check source options before every download | On | Free |
| Smart Presets | Off / manage | Pro later |
| Naming rules | `{title}` via friendly builder | Pro later |
| Folder organization | `One folder per item` / simple choices | Pro later |

Media components status in this section:

```text
Media engine                 Current · 2026.xx.xx
FFmpeg                       Installed · 8.x
[Check for updates]
```

Separate:

- App version;
- media engine version;
- FFmpeg version.

`yt-dlp` may be named in Technical details/About, but normal settings may use `Media engine`.

## 9.4. Transcription

| Setting | Default | Notes |
|---|---|---|
| Quality profile | `Balanced` | Human names |
| Language | `Auto-detect` | Per-task override |
| Default output | `Text (.txt)` | Markdown optional |
| Save local transcripts | `Next to original when possible` | Clear fallback |
| Keep extracted audio | Off | Advanced |
| Model storage | Platform app data directory | Show used disk |
| Hardware acceleration | `Automatic` | Only if genuinely supported |

Model management:

```text
Fast               Installed · 145 MB          Remove
Balanced           Not installed               Download
More accurate      Not installed               Download
```

The actual sizes must be calculated from shipped model manifests and platform variant. Do not hard-code guessed sizes.

Advanced model mapping:

```text
Show technical model names
Fast: …
Balanced: …
More accurate: …
```

This disclosure belongs in Advanced, not main flow.

## 9.5. Library

| Setting | Default |
|---|---|
| Show failed tasks in Library | On |
| Check for moved/missing files when Library opens | On |
| Keep completed tasks in Queue until app closes | On |
| Remove Library record when managed files are deleted | Ask |
| Clear temporary files older than | 7 days |

Actions:

- `Open Library folder`;
- `Rebuild Library index…`;
- `Clear missing records…`;
- `Clear temporary files…`.

`Rebuild Library index` must not scan the whole computer. It only scans configured managed output roots.

## 9.6. Appearance

- Theme: `System`, `Light`, `Dark`;
- Density: one supported default in beta; do not add Compact/Comfortable until UI is stable;
- Reduce motion: follow OS;
- system typography:
  - macOS: San Francisco/system;
  - Windows: Segoe UI/system;
- avoid bundling a custom font unless licensing and rendering are justified.

Dark and light themes must use semantic tokens, not separate ad hoc CSS.

Minimum contrast:

- WCAG AA for text and controls;
- focus rings visible in both themes;
- selected preset not indicated by color alone.

## 9.7. Privacy & Updates

Privacy summary:

```text
Media processing
Runs on this computer.

Your media files
Are not uploaded to Universal Media Extractor servers.

Network access
Used to inspect/download a source, check updates, and activate a license.
```

Controls:

| Setting | Default |
|---|---|
| Automatically check for app updates | On |
| Automatically check media engine updates | On |
| Download updates automatically | Off or platform updater convention |
| Anonymous diagnostics/telemetry | Off in beta unless a separate explicit system is implemented |
| Include source URL in copied diagnostics | Off |

If analytics is later introduced:

- explicit disclosure;
- event inventory;
- no source URLs, filenames, transcript text or local paths;
- opt-out;
- privacy policy update.

Update UX:

```text
Application
Version 1.0.0 · Up to date

Media engine
Version 2026.xx.xx · Update available
[Update engine]
```

Engine update must be atomic:

1. download;
2. verify integrity/signature/hash;
3. stage;
4. swap;
5. rollback on failure;
6. record version.

## 9.8. Advanced & Support

Allowed:

- `Copy system diagnostics`;
- `Open logs folder`;
- `Check media engine`;
- `Reset media engine…`;
- `View supported sources and limitations`;
- `View open-source licenses`;
- `Reset settings…`;
- `Rebuild Library index…`;
- technical model mapping;
- optional custom output root behavior.

Not allowed in public beta:

- raw `yt-dlp` arguments;
- arbitrary executable paths without a deliberate expert mode;
- cookies import;
- browser session extraction;
- proxy fields;
- authentication credentials;
- Course/Udemy toggle;
- DRM-related controls;
- arbitrary FFmpeg command line.

A hidden developer build may retain internal controls behind compile-time/build flags. They must not be shipped dormant in public binaries if they expand policy/security risk.

## 9.9. License

After monetization:

```text
Universal Media Extractor Pro
Licensed to: <email or masked license identity>
Devices: 1 of 3
Feature updates through: Aug 7, 2027

[Manage license] [Deactivate this device]
```

Free:

```text
Universal Media Extractor Free
Single downloads and basic local tools.

[Upgrade to Pro]
```

Rules:

- app remains usable offline after activation grace check;
- no mandatory account for basic local utility;
- activation failure never blocks access to user files;
- licensing server receives no media URLs or file metadata;
- license cache is signed and stored in OS-appropriate secure storage;
- device limit handling provides self-service deactivate where possible.

## 9.10. Settings acceptance criteria

- Every main-flow default can be changed without exposing technical jargon.
- Changing default folder verifies write access.
- App and engine versions are visibly separate.
- Removing a model states freed disk space and does not delete transcripts.
- Privacy page accurately lists every network call.
- Public build contains no Course/auth/cookies controls.
- Settings persist after restart and migrate safely across versions.
- Reset does not delete Library/files without separate confirmation.
- Keyboard navigation and screen-reader labels work across all controls.

---

# 10. Commercial packaging and public framing

## 10.1. Product category

Do not sell the product as a generic «universal downloader». Sell it as a focused desktop utility:

```text
Universal Media Extractor
Local Media Downloader & Organizer for macOS and Windows
```

Recommended one-line promise:

```text
Save supported media links as clean video, audio, or subtitle files.
Keep results organized and transcribe locally when needed.
```

Recommended local-first block:

```text
Downloads, conversion, and transcription run on your computer.
Universal Media Extractor does not upload your media to its own servers.
```

Recommended limitations block:

```text
Source availability is best-effort and can change.
Protected, restricted, or unsupported media cannot be processed.
```

Recommended responsible-use line:

```text
Use Universal Media Extractor only for media you own or are permitted to save.
```

## 10.2. Naming risk

`Universal Media Extractor` is acceptable as a brand but creates an expectation of universal source coverage. Every product surface should qualify it with:

- `supported media links`;
- `best-effort source support`;
- `availability can change`.

Before a large paid launch, consider a less absolute brand name. This is not required for beta, but the decision should be made before reviews and SEO permanently attach «Universal» to promises the product cannot control.

## 10.3. Public beta model

Recommended public beta:

- duration: **8–12 weeks**, or longer until exit criteria are met;
- price: free;
- all intended public-beta features unlocked;
- no usage countdown;
- no fake “lifetime beta deal” urgency;
- feedback/report action inside app;
- signed/notarized installers;
- explicit `Beta` version label;
- no Course/Udemy mode;
- no cookies/private-access workflows;
- no claim of production-grade source coverage.

Why all beta features should be unlocked:

- Batch/Queue/Library are the highest-risk workflows and require real use;
- locking them would prevent validation;
- monetization before restart recovery and engine update reliability would create support/refund risk.

## 10.4. Beta exit criteria

Commercial launch begins only when all criteria hold:

### Reliability

- signed installers launch cleanly on supported macOS and Windows versions;
- app-start success ≥99% across controlled and beta telemetry/support sample;
- no known data-loss bug;
- Queue/Library persist across normal restart;
- interrupted tasks are reconciled;
- safe deletion is path-contained;
- update rollback works;
- disk-full and permission errors are normalized.

### Source test corpus

Maintain a dated reproducible corpus of allowed/public test sources.

Target:

- ≥90% successful analyze-and-save completion on currently supported, non-protected, non-restricted test cases;
- failures classified correctly;
- engine update restores known fixable regressions;
- no unsupported source is advertised as guaranteed.

This percentage is an internal release gate, not a public universal success claim.

### UX

- first single-video task completes without documentation in moderated tests;
- users understand that Video means one video+audio file;
- no duplicate visible presets;
- invalid URL error is visible and actionable;
- Open/Reveal works after completion;
- Batch failed items can be retried;
- main flow exposes no raw technical fields.

### Commercial readiness

- Terms, Privacy, EULA and open-source notices reviewed;
- payment provider approves the exact product category;
- refund and support policy published;
- license activation/deactivation tested;
- update entitlement behavior documented;
- website claims match app behavior.

## 10.5. Permanent Free / Pro boundary

### Public beta

Everything below is unlocked for testing.

### Free after launch

| Capability | Free |
|---|---|
| Single URL analysis/download | Yes |
| One active task | Yes |
| Video presets | Best / 1080 / 720 where unique |
| Audio | M4A / MP3; WAV may remain Free |
| Source subtitles | One language per task |
| Local file transcription | Fast profile |
| Transcript output | TXT and Markdown |
| Library | Last 20 records |
| Open/reveal/copy path | Yes |
| App and critical engine/security updates | Yes |
| Diagnostics | Yes |
| Batch/playlists | No |
| Custom naming/folder rules | No |
| Concurrent tasks | No |
| Smart Presets | No |

### Pro

| Capability | Pro |
|---|---|
| Batch URL lists | Yes |
| Playlist item selection | Yes |
| Concurrent tasks | Up to 4 |
| Unlimited local Library | Yes |
| Search and filters | Yes |
| Batch groups and retry failed | Yes |
| Smart Presets | Yes |
| Custom naming rules | Yes |
| Folder organization rules | Yes |
| Advanced container override | Yes |
| Balanced / More accurate transcription | Yes, after validation |
| Additional transcript exports | Only implemented/tested formats |
| Priority diagnostics/support | Yes |
| Personal devices | 3 |

The best paid boundary is **scale, repeatability and organization**, not basic media quality. Artificially limiting 1080p or putting essential bug fixes behind payment would weaken trust.

## 10.6. Pricing recommendation

Current official market references reviewed on 7 August 2026 place focused desktop utilities roughly across:

- Downie: about `$19.99` permanent license;
- 4K Video Downloader Plus: about `$25` Personal lifetime and `$45` Pro lifetime, with a lower annual tier;
- SnapDownloader: about `$39.99` one-time and `$29.99` annual;
- MacWhisper Pro: about `€64` one-time;
- adjacent focused utilities such as Permute: about `$14.99` permanent.

Recommended launch:

```text
Founder Pro
$24 one-time
First 500 paid users or a defined launch window
3 personal devices
12 months of feature updates
```

Standard:

```text
Pro
$39 one-time
3 personal devices
12 months of feature updates
```

Optional renewal:

```text
Feature update renewal
$19/year
```

Important entitlement rule:

- the purchased version continues working;
- critical compatibility, media-engine and security updates must not be withheld solely because the feature-update period ended;
- renewal covers new app features and major-version upgrades;
- this distinction must be stated plainly.

No subscription at launch. A subscription is difficult to justify for a local utility without ongoing cloud cost or continuous service value.

Business/team plan should be postponed until there is demand for:

- centralized license management;
- deployment;
- invoice/procurement;
- priority support;
- commercial device count.

## 10.7. Upgrade surfaces

After beta only.

Allowed:

1. permanent `Upgrade` item at sidebar bottom;
2. small `Pro` badge beside a locked feature;
3. contextual sheet after user invokes Batch, Smart Preset or advanced Library;
4. License section in Settings;
5. website comparison.

Not allowed:

- launch modal;
- timer;
- flashing banner;
- blocking result access;
- limiting access to files the user already created;
- repeated prompt after dismissal;
- “only 2 downloads left” coercion;
- fake discount;
- Pro prompt during failure.

Upgrade copy should describe the attempted workflow:

```text
Process multiple links with Pro

Build a queue, retry failed items, and keep an unlimited searchable Library.

$39 one-time · 3 personal devices
[Not now] [Upgrade to Pro]
```

## 10.8. Distribution recommendation

### Primary launch channel

Direct signed installers:

- macOS: signed and notarized DMG/PKG;
- Windows: signed EXE/MSIX;
- automatic app updater;
- separate verified media-engine updater;
- public checksums/release notes;
- clear supported OS/architecture.

Why direct-first:

- faster source-engine fixes;
- one product build;
- external checkout and licensing control;
- fewer store-policy ambiguities;
- easier beta distribution.

### Mac App Store

Do not treat Mac App Store as launch channel for the full downloader. Apple App Review Guideline 5.2.3 restricts downloading/converting media from third-party sources without explicit authorization. Even if technical sandboxing were solved, review risk remains material.

Possible future path:

- a separate local-file transcription/conversion edition with no URL downloader;
- only after commercial validation;
- only if maintaining two product boundaries is worthwhile.

### Microsoft Store

Possible later. Microsoft Store supports packaged/unpackaged desktop app models, but UME should first prove:

- signing;
- updater strategy;
- binary/media-engine update compliance;
- policy approval;
- parity with direct build.

Open Video Downloader’s official documentation notes that its Store build can lag and does not use the same `yt-dlp` auto-update path. This reinforces direct distribution as the reliability baseline.

### Setapp

Potential later channel for macOS after:

- product stability;
- native-feeling polish;
- support capacity;
- economics comparison with direct sales.

Do not make Setapp a dependency for initial monetization.

## 10.9. Payment and licensing

Before integration, send the exact product description, screenshots and EULA to the chosen merchant/payment provider for written category approval. Downloader-related products can receive additional scrutiny.

Recommended checkout model:

```text
Website
→ external hosted checkout
→ license key/email delivery
→ app activation
```

Requirements:

- seller-of-record/tax handling evaluated;
- refund mechanism;
- license API and offline grace;
- webhook signature validation;
- no media/source data in commerce system;
- no card handling inside app;
- license state not coupled to Library/file access.

Do not assume a provider is acceptable merely because it supports software licensing. Obtain approval for this exact use case.

## 10.10. Public claims: allowed

Allowed when implemented and verified:

- `Runs locally on macOS and Windows`;
- `No media upload to our servers`;
- `Save video, audio, or source subtitles from supported links`;
- `Create local transcripts from audio and video`;
- `Organized local output`;
- `Batch queues and retry in Pro`;
- `Best-effort source support`;
- `One playable video file with audio`;
- `Signed desktop app`;
- `No paid transcription API required`.

Qualify local privacy: source download itself necessarily contacts the source, and update/license checks may contact UME infrastructure.

## 10.11. Public claims: prohibited or unsafe

Do not use:

- `downloads everything`;
- `download any video`;
- `all websites`;
- `1000+ sites`, unless maintained and tested with exact methodology;
- `universal support`;
- `private video downloader`;
- `bypass login`;
- `bypass CAPTCHA`;
- `bypass paywall`;
- `remove DRM`;
- `download protected content`;
- `anonymous downloader`;
- `100% legal`;
- `fair use guaranteed`;
- `unlimited`, when source limits or product limits exist;
- `offline downloader` for URL work;
- `lossless audio`, when transcoding a lossy source;
- `AI-powered`, merely because Whisper runs locally;
- `no internet required`, except for local file transcription after required models are installed;
- public Udemy/Course support.

## 10.12. Public website structure

Minimal launch site:

1. Hero: product/category/OS downloads.
2. Three-step workflow:
   ```text
   Add a supported link
   Choose video, audio, or subtitles
   Save and organize locally
   ```
3. Local-first privacy.
4. Screenshots: New task, Queue, Result, Library.
5. Feature boundary: single, batch, local transcription.
6. Known limitations.
7. Free vs Pro.
8. FAQ:
   - supported sources;
   - protected/restricted media;
   - local processing;
   - app vs media-engine updates;
   - where files are saved;
   - refunds/license devices.
9. Download and system requirements.
10. Terms/Privacy/Open-source notices.

Do not lead with a giant site-logo grid. It creates an implicit guarantee that the product cannot control.

## 10.13. Commercial acceptance criteria

- Basic Free workflow is genuinely useful.
- Pro value is visible without degrading Free reliability.
- No paywall blocks existing files or diagnostics.
- Checkout/product description has provider approval.
- Critical compatibility fixes remain available.
- Website, app and EULA use the same source limitations.
- App accurately describes local/network behavior.
- Price and update entitlement are understandable before purchase.
- Store builds, if added, disclose feature/update differences.



# 11. Что удалить из текущего приложения

## 11.1. Из public build полностью

1. `Course · internal`.
2. Udemy-specific navigation, copy, routes and feature flags.
3. Chrome session controls.
4. Manual cookies selector/import.
5. Auth/cookies fallback instructions.
6. Any public promise of course-platform support.
7. Dormant UI or API endpoints that could be re-enabled from DevTools in a public build.
8. Source-specific logic that creates a material policy/security surface but is not part of the approved public product.

Для internal development допускается отдельный build target/repository configuration. Простого `display:none` недостаточно.

## 11.2. Из main navigation

- `Link`;
- `File`;
- `Batch`;
- footer `Library`;
- отдельный `History`;
- отдельный `Transcription`;
- technical `Outputs`.

Заменить на:

```text
New task
Queue
Library
Settings
```

## 11.3. Из первого экрана

- огромную пустую карточку `Add a source`;
- постоянную legal/warnings card;
- selector режимов;
- raw HTML file input;
- `Analyze local file`;
- `Analyze playlist`;
- четыре конкурирующие batch actions;
- output format dropdown;
- Whisper model selector;
- transcript format selector до появления local file;
- editable save-path field;
- technical engine status, если всё исправно;
- пустую Library strip;
- большие marketing-style illustration/empty state.

## 11.4. Из output selection

- повторяющиеся presets, разрешающиеся в один результат;
- `Smaller video at 1080p or higher`;
- длинные списки source formats;
- raw resolution rows без outcome logic;
- codec/bitrate/format IDs;
- отдельный format dropdown, дублирующий preset;
- `Recommended` на нескольких rows;
- неопределённый `Best` без показанного фактического resolution после analysis;
- возможность выбрать Video, которая сохраняет video/audio отдельными files без явного expert workflow.

## 11.5. Из result/progress

- `Job succeeded`;
- raw job ID как главный текст;
- backend step names;
- technical output directory как primary result;
- request/result JSON в normal view;
- logs card по умолчанию;
- 100% progress до merge/finalization;
- toast-only failure;
- non-functional `Pause`;
- кнопки `Copy output path` как primary вместо Open/Reveal;
- repeated rights warning after completion.

## 11.6. Из public copy

- «любые медиа»;
- «практически из любых сервисов»;
- гарантированный список сайтов;
- private/login/cookies framing;
- DRM/CAPTCHA/paywall language, кроме ясного описания того, что app это **не поддерживает**;
- `AI transcription`, если это лишь локальный Whisper workflow и AI не является коммерческой ценностью;
- `cloud-free` без оговорки о network requests к source/update/license;
- «100% offline»;
- `unlimited`.

---

# 12. Что сохранить

## 12.1. Product foundations

- local-first architecture;
- local FastAPI/backend isolation;
- no cloud media upload;
- `yt-dlp` as replaceable media engine;
- `ffmpeg/ffprobe` for local media work;
- local Whisper transcription;
- predictable output base;
- structured artifacts and logs;
- normalized errors;
- best-effort cancel;
- safe managed-output deletion;
- local session/origin protections;
- no paid transcription API dependency.

## 12.2. UX foundations

- restrained dark visual foundation;
- compact desktop utility character;
- clear media summary with title/thumbnail/duration/source;
- concise human-facing output rows;
- selected-row state;
- separation of technical details from main UI;
- one selected transcript output per run;
- copy transcript;
- reveal/open output;
- source subtitles as a distinct output type;
- post-download transcription as optional;
- visible known limitations.

## 12.3. Product logic

- `Analyze → choose clean output → save locally`;
- video + best compatible audio merged into one file;
- audio-only extraction;
- SRT/VTT source subtitle handling where implemented;
- local video → extract audio → Whisper;
- output index/Library concept;
- job-based execution;
- cancellation and retry;
- diagnostics artifacts;
- format deduplication intent.

## 12.4. Visual language to retain and refine

- neutral graphite surfaces;
- limited accent color;
- 1 px dividers;
- compact controls;
- no gradients;
- no decorative illustrations;
- no marketing dashboard cards;
- no developer console aesthetic.

Add:

- light/system theme;
- OS system fonts;
- clearer focus states;
- responsive window behavior;
- native file/folder dialogs;
- stable action bar;
- list-first Queue/Library.

---

# 13. Что отложить

## 13.1. До завершения public beta

- browser extension;
- clipboard auto-watch;
- menu-bar/background mode;
- scheduling;
- watch folders;
- per-item Batch presets;
- pause/resume;
- drag URLs directly from every browser;
- custom naming builder;
- Smart Presets;
- multiple subtitle languages per task;
- full transcript search/editor;
- rich media preview/player;
- tags/favorites;
- cloud sync;
- account system;
- Business/Team plan;
- Mac App Store variant;
- Setapp;
- Microsoft Store;
- localization beyond the first validated languages.

## 13.2. После подтверждения downloader PMF

- trim/cut;
- chapters;
- thumbnail/metadata editor;
- audio normalization;
- device/social export presets;
- channel subscriptions;
- archive/watch source;
- duplicate-by-media-ID detection across sources;
- hardware tuning UI;
- custom folder rules;
- scheduled Batch;
- import/export Library;
- browser extension.

## 13.3. Отдельный продуктовый трек, не downloader beta

- meeting recording;
- dictation;
- speaker diarization;
- transcript editor;
- AI summary/chat;
- cloud collaboration;
- translation workflows;
- team transcript workspace.

Транскрипция в UME должна оставаться useful secondary workflow, пока данные не покажут самостоятельный спрос.

## 13.4. Не включать без отдельного legal/product approval

- public Course/Udemy mode;
- cookies import;
- browser session access;
- private content;
- authenticated platform browsing;
- proxy/geo workflows;
- CAPTCHA handling;
- paywall handling;
- DRM/key workflows;
- source-specific scraping outside the approved engine boundary;
- public claims about educational-platform archiving.

---

# 14. Top 10 implementation priorities

Приоритеты расположены по зависимости и риску, а не по визуальной заметности.

## P0.1. Зафиксировать public product boundary и удалить Course surface

### Реализация

- создать public build configuration;
- исключить Course/Udemy routes, controls, strings, assets and settings;
- исключить cookies/session dependencies;
- проверить packaged binary/static bundle;
- добавить automated test, что запрещённые labels/routes отсутствуют.

### Acceptance criteria

- `Course`, `Udemy`, `cookies`, `Chrome session`, `manual cookies` не находятся в public UI bundle;
- public API не отвечает на internal course endpoints;
- website/Help/diagnostics не обещают course support;
- internal build остаётся отдельно управляемым, если он нужен.

## P0.2. Установить фактический backend source of truth

### Реализация

- сверить ветку/commit с документами от 5 и 7 августа;
- проверить SQLite;
- проверить Batch;
- проверить output index;
- проверить restart persistence;
- обновить architecture docs и endpoint inventory.

### Acceptance criteria

- одна датированная спецификация соответствует текущему коду;
- restart test определяет судьбу queued/running/completed tasks;
- нет противоречия «SQLite есть / database нет»;
- product UI не проектируется на отсутствующие endpoints без явно созданных backend tasks.

## P0.3. Построить universal `New task` composer

### Реализация

- заменить Link/File/Batch tabs;
- single URL input;
- native `Choose file…`;
- `Add multiple links`;
- input parser/router;
- inline validation;
- compact top-aligned first screen;
- first-run readiness state.

### Acceptance criteria

- один URL открывает URL analysis;
- local media opens automatic file analysis;
- multiple URLs route to Batch review;
- `.txt/.csv` routes to Batch import;
- invalid URL shows inline error;
- keyboard shortcuts and drag/drop work;
- no empty 600 px card.

## P0.4. Реализовать stable semantic preset resolver

### Реализация

- semantic preset IDs;
- source-aware resolution;
- dynamic deduplication;
- one-file video contract;
- honest estimated sizes;
- Auto container/fallback;
- distinction between source subtitles and transcripts.

### Acceptance criteria

- screenshot case with three identical `1080p · 12 MB` rows becomes one unique row;
- `Smaller` заменён на `Up to 720p`;
- Video always yields one playable file or fails before misleading success;
- no raw stream details in main UI;
- resolver has unit tests for 720p, 1080p, 4K, audio-only, incompatible container and missing size cases.

## P0.5. Сделать Queue/Library durable

### Реализация

- SQLite schema/migrations;
- transactional task/artifact writes;
- restart reconciliation;
- Queue groups;
- Library records;
- missing-file state;
- safe deletion;
- current-session completed handling.

### Acceptance criteria

- 10 queued tasks survive app restart as waiting/interrupted records;
- completed artifact opens after restart;
- interrupted task can retry;
- external file cannot be deleted through managed-output delete;
- path traversal tests pass;
- Library handles 10,000 synthetic records responsively.

## P0.6. Native filesystem integration

### Реализация

- pywebview/native bridge for file/folder pickers;
- in-place local file analysis;
- writable-folder checks;
- OS-specific Reveal/Open;
- drag/drop paths;
- removable-drive handling;
- path normalization.

### Acceptance criteria

- no browser-style file upload control;
- 20 GB local video is not copied merely to analyze/transcribe;
- transcript can save next to source when permitted;
- `Show in Finder/File Explorer` selects actual file;
- Windows Unicode/long-path and macOS permission cases are tested;
- app never exposes arbitrary filesystem delete.

## P0.7. Unified Queue progress, cancel, retry and recovery

### Реализация

- normalized task stages;
- determinate/indeterminate progress;
- subprocess cancellation;
- temp cleanup;
- retry relationships;
- batch failure isolation;
- quit-with-active-tasks dialog.

### Acceptance criteria

- percentage never reaches final success before validation;
- merge/conversion gets its own stage;
- cancel reaches terminal state;
- failed one of 20 Batch items does not stop the rest;
- app crash/restart converts stale running state to interrupted;
- no `Pause` is shown without tested resume.

## P0.8. Error normalization and privacy-safe diagnostics

### Реализация

- stable error codes;
- mapping layer;
- inline validation;
- error cards;
- context actions;
- sanitized diagnostics;
- engine-update retry;
- support export.

### Acceptance criteria

- each planned error category has fixture/test;
- raw stderr is collapsed;
- URL/path/token redaction tests pass;
- protected/access-required errors never suggest bypass;
- invalid URL state is visible in screenshot/automated UI test;
- support can identify app/engine version from copied diagnostics.

## P1.9. Result and secondary local transcription flow

### Реализация

- saved result card;
- Open/Reveal;
- `Transcribe locally`;
- quality profiles;
- on-demand model management;
- preview/copy/export;
- local temp cleanup.

### Acceptance criteria

- result says actual filename/container/size/path;
- local source is not duplicated by default;
- first model download shows actual disk/network requirement;
- transcript text is copyable and persistent;
- only implemented formats appear;
- transcription failure never corrupts saved media.

## P1.10. Commercial desktop readiness

### Реализация

- Settings;
- app updater;
- atomic media-engine updater;
- signed/notarized macOS package;
- signed Windows installer;
- License section;
- contextual Pro gates disabled in beta;
- light/dark/system;
- accessibility;
- release QA matrix;
- public documentation.

### Acceptance criteria

- clean install/uninstall/update on supported OS matrix;
- app and engine can update independently;
- failed update rolls back;
- no unsigned helper executable;
- keyboard-only core flow passes;
- 200% Windows scaling and macOS window resizing pass;
- Free/Pro feature flags cannot hide or delete files;
- beta build contains no paywall;
- Privacy page matches observed network traffic.

---

# 15. Risks and non-goals

## 15.1. Product risks

### 1. Source volatility

`yt-dlp`-based support changes whenever external platforms change. The product cannot guarantee permanent support.

Mitigation:

- dated source test corpus;
- separate engine updater;
- normalized `engine outdated` state;
- best-effort wording;
- no site-count headline;
- rapid rollback.

### 2. Reliability gap hidden by visual polish

The supplied screenshots validate mainly analysis UI, not full download/transcription/restart behavior. A polished shell could create false confidence.

Mitigation:

- beta exit gates;
- end-to-end fixtures;
- crash/restart tests;
- artifact validation;
- no paid launch before durable Queue.

### 3. Conflicting internal documentation

Disagreement about Batch, SQLite and job persistence can produce incorrect engineering estimates and UI dependencies.

Mitigation:

- repository audit as P0;
- generated API/schema inventory;
- docs versioned with commit;
- one owner/source of truth.

### 4. Legal, store and payment-provider scrutiny

Downloader category carries platform, copyright and commerce risk even without bypass features.

Mitigation:

- narrow public claims;
- no Course/auth/proxy/private workflows;
- direct-first distribution;
- legal review;
- written provider approval;
- takedown/support process;
- no claims of legality for user actions.

### 5. `Universal` expectation risk

Brand name may cause users to assume every site is supported.

Mitigation:

- persistent subtitle `supported media`;
- limitations page;
- no logo wall;
- consider rename before scale.

### 6. Engine and binary supply-chain risk

Downloading executable components creates security expectations.

Mitigation:

- pin trusted release source;
- checksum/signature verification;
- atomic update;
- rollback;
- version visibility;
- open-source notices/SBOM;
- no arbitrary binary download.

### 7. Cross-platform packaging risk

Python, pywebview, FFmpeg, Whisper models and native bridges may behave differently across macOS Intel/Apple Silicon and Windows x64/ARM.

Mitigation:

- explicit supported matrix;
- platform-specific packages;
- automated install/smoke;
- native dialog/path tests;
- avoid promising Windows ARM until verified.

### 8. Local compute and disk cost

Whisper and media conversion may be slow, memory-heavy and storage-heavy.

Mitigation:

- quality profiles;
- actual model sizes;
- disk preflight;
- honest progress;
- automatic temp cleanup;
- no speed claims without benchmarks.

### 9. Antivirus and trust

Bundled downloaders/media executables can trigger reputation warnings.

Mitigation:

- code signing;
- stable publisher identity;
- minimal bundled executables;
- malware scanning;
- reproducible release process;
- public checksums;
- avoid obfuscation.

### 10. Support burden

External source breakage can be mistaken for app failure and create high support volume.

Mitigation:

- engine update action;
- status/known limitations page;
- diagnostics;
- source-domain aggregation without URLs only if consented;
- clear retry guidance;
- support policy.

### 11. Privacy overclaim

Local media processing does not mean no network activity. URL analysis/download, update checks and license activation use network.

Mitigation:

- precise Privacy page;
- enumerate calls;
- telemetry off in beta;
- no source URL in diagnostics;
- packet-level release verification.

### 12. Weak paid conversion

Free/open-source alternatives are strong. Users will not pay merely for a GUI around `yt-dlp`.

Mitigation:

- sell reliability, queue, organization and updates;
- useful permanent Free;
- Pro scale workflows;
- founder pricing;
- measure activation/retention before expanding.

### 13. Feature creep

Transcription, conversion, editing and course workflows can turn the app into an incoherent suite.

Mitigation:

- public product boundary;
- roadmap gates;
- downloader-organizer core;
- separate validation for transcription expansion;
- postpone editor/AI suite.

## 15.2. Commercial non-goals for public beta

UME public beta is **not**:

- an online downloader website;
- a hosted SaaS;
- a cloud transcription service;
- a DRM remover;
- a paywall/CAPTCHA/login bypass tool;
- a private media access tool;
- a proxy/VPN/geo-unblocking tool;
- a course piracy/archive product;
- a full media converter;
- a video editor;
- a transcript editor;
- a meeting recorder;
- an AI summarizer/chat app;
- a channel surveillance/archive service;
- a team collaboration workspace;
- a browser automation tool.

## 15.3. Technical non-goals for public beta

- arbitrary CLI arguments;
- arbitrary FFmpeg pipelines;
- plugins;
- user scripts;
- browser-cookie extraction;
- cloud storage integrations;
- cloud sync;
- account system;
- remote task execution;
- mobile apps;
- server mode;
- NAS/self-hosted edition;
- pause/resume unless proven;
- background daemon/menu bar unless fully designed.

## 15.4. Definition of done for public beta UI

Public beta UI is ready when:

1. public build contains only approved features;
2. one universal source composer routes correctly;
3. first single-link task needs no documentation;
4. presets are unique and outcome-based;
5. Video produces one playable file;
6. Queue survives restart;
7. Library opens actual outputs;
8. errors are human and actionable;
9. diagnostics are redacted;
10. native file/folder dialogs work;
11. local transcription is secondary and honest;
12. no unsupported transcript format is shown;
13. light/dark/system and keyboard navigation work;
14. signed installers and update paths pass;
15. all screenshots and public copy match the shipped build.

---

# Финальная инженерная схема

```text
App shell
├── New task
│   ├── Universal source composer
│   │   ├── URL
│   │   ├── Local file
│   │   └── Multiple links
│   ├── Source analysis
│   ├── Outcome presets
│   │   ├── Video
│   │   ├── Audio
│   │   └── Source subtitles
│   └── Sticky save/action bar
├── Queue
│   ├── Single tasks
│   ├── Batch groups
│   ├── Progress stages
│   ├── Cancel
│   └── Retry/recovery
├── Library
│   ├── Media
│   ├── Transcripts
│   ├── Failed/missing
│   ├── Open/reveal
│   └── Safe delete/repeat
└── Settings
    ├── Defaults
    ├── Downloads
    ├── Transcription
    ├── Library
    ├── Appearance
    ├── Privacy & Updates
    ├── Advanced & Support
    └── License
```

Commercial layer after beta:

```text
Free
├── single tasks
├── basic presets
├── one active task
├── basic local transcription
└── last 20 Library records

Pro · $39 one-time
├── Batch/playlists
├── concurrency
├── unlimited searchable Library
├── Smart Presets
├── naming/folder rules
├── advanced containers
└── advanced validated local transcription
```

---

# Источники

## Переданные материалы

- `[F1] UI_UX_GPT_PRO_CONTEXT_PACK.md`, 7 августа 2026.
- `[F2] UI_UX_COMPETITOR_VISUAL_LOGIC_PACK.md`, 7 августа 2026.
- `[F3] UI_UX_OUR_APP_VISUAL_LOGIC_PACK.md`, 7 августа 2026.
- `[F4] PRODUCT_FUNCTIONALITY_OVERVIEW.md`, 5 августа 2026.
- `[F5] competitors.zip`: 26 captured competitor/reference screenshots.
- `[F6] our_app.zip`: 6 current-product screenshots.

## Официальные конкурентные источники из переданного pack

- 4K Video Downloader Plus: `https://www.4kdownload.com/products/videodownloader`
- Downie: `https://software.charliemonroe.net/downie/`
- SnapDownloader: `https://snapdownloader.com/features`
- PullTube: `https://setapp.com/apps/pulltube`
- MediaHuman: `https://www.mediahuman.com/howto/user-interface-in-detail5.html`
- Parabolic: `https://github.com/NickvisionApps/Parabolic`
- Stacher: `https://www.stacher.io/`
- cobalt: `https://cobalt.tools/`
- Buzz: `https://github.com/chidiwilliams/buzz`
- MacWhisper: `https://www.macwhisper.com/`
- yt-dlp.app: `https://dlp.yt/download`
- Wondershare UniConverter: `https://uniconverter.wondershare.com/`
- VideoProc: `https://www.videoproc.com/`
- HitPaw Univd: `https://videoconverter.hitpaw.com/`
- JDownloader: `https://jdownloader.org/home/features`
- Any Video Converter: `https://www.any-video-converter.com/index.html`
- ClipGrab: `https://clipgrab.de/update/en`
- Tartube: `https://github.com/axcore/tartube`
- YT DLP GUI: `https://ytdlpgui.com/`

## Дополнительные официальные источники

- Open Video Downloader: `https://github.com/StefanLobbenmeier/youtube-dl-gui`
- Vividl: `https://github.com/Bluegrams/Vividl`
- MeTube: `https://github.com/alexta69/metube`
- HandBrake documentation: `https://handbrake.fr/docs/`
- Shutter Encoder documentation: `https://www.shutterencoder.com/documentation/`
- Aiko: `https://sindresorhus.com/aiko`
- LosslessCut: `https://github.com/mifi/lossless-cut`

## Цены и коммерческие условия, проверенные 7 августа 2026

- 4K Video Downloader Plus pricing: `https://www.4kdownload.com/buy/videodownloader`
- SnapDownloader pricing: `https://snapdownloader.com/buy`
- Downie pricing: `https://software.charliemonroe.net/help/basic/product_pricing.html`
- MacWhisper: `https://www.macwhisper.com/`
- Permute pricing: `https://software.charliemonroe.net/help/basic/product_pricing.html`

Цены могут меняться. Они используются как рыночный ориентир, а не как гарантированная текущая цена после даты документа.

## Platform and distribution rules

- Apple App Review Guidelines: `https://developer.apple.com/app-store/review/guidelines/`
- Microsoft Store Policies: `https://learn.microsoft.com/windows/apps/publish/store-policies`
- Microsoft Store desktop packaging overview: `https://learn.microsoft.com/windows/apps/distribute-through-store/how-to-distribute-your-win32-app-through-microsoft-store`
- Lemon Squeezy prohibited products: `https://www.lemonsqueezy.com/help/getting-started/prohibited-products`
- Stripe Tax for digital products/software: `https://docs.stripe.com/tax/tax-codes`

---

# Итоговое решение

**Утвердить направление, но не полировать текущую структуру.**

Нужно заменить текущий mode-based UI на один universal source workflow, вынести Queue и Library в самостоятельные рабочие разделы, сделать presets outcome-based, а транскрипцию — вторичным локальным действием. Коммерческий запуск оправдан только после persistent Queue, restart recovery, engine update и подписанных installers.

Целевая платная ценность:

```text
не «скачивает всё»
а
«надёжно превращает поддерживаемые источники
в понятные локальные файлы и управляемую очередь»
```
