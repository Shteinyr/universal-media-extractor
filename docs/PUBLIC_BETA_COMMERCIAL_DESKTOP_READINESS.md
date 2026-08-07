# Public Beta Commercial Desktop Readiness

Status: issue #51 implementation/readiness pass.

## Scope

This pass closes the final public-beta desktop readiness layer after the main beta UX work.

It does not add checkout, licensing, automatic updates, public Course/Udemy support, Windows installer implementation, or a new roadmap block.

## What Changed

- Added a compact public-beta `Settings` surface to the static UI.
- Settings now reflect implemented behavior instead of future-only promises:
  - default downloads folder;
  - preset-first output selection;
  - system light/dark appearance;
  - app updates prepared but not automatic in beta;
  - media engine updates tracked separately;
  - local-first privacy wording.
- Added system appearance CSS support through semantic light/dark tokens.
- Added keyboard shortcuts:
  - `Cmd/Ctrl+K` focuses `New task`;
  - `Cmd/Ctrl+,` opens `Settings`.
- Extended browser smoke tooling with desktop readiness checks:
  - keyboard analyze flow;
  - light theme rendering;
  - high-DPI screenshot;
  - narrow window resize / no horizontal overflow check.
- Added update-path documentation separating app updates from media-engine updates.
- Added Windows production build path documentation.

## Acceptance Criteria Review

| Requirement | Status | Evidence |
| --- | --- | --- |
| Settings are coherent and match implemented behavior | Done | UI Settings only exposes current beta defaults and prepared-but-not-automatic update status. |
| App update and media-engine update plans are separated | Done | `docs/APP_AND_MEDIA_ENGINE_UPDATE_PLAN.md`. |
| macOS build is signed/notarized when Apple credentials are available | Prepared / externally blocked | Existing scripts/docs remain ready; real signing/notarization requires Apple Developer ID credentials. |
| Windows installer path is prepared and validated later | Prepared | `docs/WINDOWS_PRODUCTION_BUILD_PATH.md`. |
| License section exists only when licensing is ready | Done | Public UI does not include a License section. |
| Light/dark/system appearance is handled | Done | CSS uses system appearance media query and semantic tokens. |
| Keyboard-only core flow passes | Done | Browser smoke `--desktop-readiness` verifies keyboard-driven analyze flow. |
| High-DPI/window resizing QA passes | Done | Browser smoke captures high-DPI light screenshot and checks narrow viewport overflow. |
| Public docs, privacy, limitations, and support copy match observed behavior | Done | README and release/readiness docs keep updater/licensing/installers marked as not implemented or externally blocked. |

## Desktop Readiness Boundaries

Ready for public beta preparation:

- local desktop wrapper lifecycle;
- local-only backend binding;
- public-mode Course hiding;
- native file/folder picking in desktop mode;
- reveal saved outputs;
- SQLite job/history persistence;
- diagnostics redaction;
- macOS production build foundation;
- DMG/signing/notarization scripts and checklists.

Not ready for paid public distribution:

- final Developer ID signed/notarized macOS app;
- public notarized DMG;
- Windows x64 installer;
- license activation/enforcement;
- automatic app updater;
- atomic media-engine updater;
- payment checkout.

## Verification Commands

```bash
node --check src/universal_media_extractor/static/app.js
node --check src/universal_media_extractor/static/option_normalizer.js
.venv/bin/python -m pytest -q
```

Result:

- `node --check src/universal_media_extractor/static/app.js` passed.
- `node --check src/universal_media_extractor/static/option_normalizer.js` passed.
- `python3 -m py_compile scripts/browser_smoke.py scripts/run_desktop.py scripts/build_macos_app.py` passed.
- `.venv/bin/python -m pytest -q` passed outside sandbox with `232 passed`.

Browser proof command:

```bash
.venv/bin/python scripts/browser_smoke.py \
  --proof-dir proof/commercial_desktop_readiness_final_pass \
  --desktop-readiness
```

Result: browser smoke passed in public product mode. It did not run download or transcription.

## Proof Artifacts

Expected proof directory:

```text
proof/commercial_desktop_readiness_final_pass/
```

Expected screenshots:

- `ui_initial.png`
- `ui_invalid_url.png`
- `ui_analyze_result.png`
- `ui_output_selected.png`
- `ui_library.png`
- `ui_light_hidpi_initial.png`
- `ui_keyboard_analyze_result.png`
- `ui_settings_keyboard.png`
- `ui_narrow_resize.png`

## Not Changed

- No backend download/transcription behavior changed.
- No public Course/Udemy support added.
- No checkout or license activation added.
- No automatic updater added.
- No Windows installer implementation added.
- No roadmap change made.
