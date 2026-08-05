# Commercial Block 6: Output Templates And Duplicate Handling

## Status

Completed for GitHub issue #11: `[P0] Add output templates and duplicate handling`.

## What Changed

Commercial Block 6 gives URL downloads beta-ready output naming controls without changing the main media pipeline.

The download UI now includes:

- `Name template` for the result folder name;
- `If exists` duplicate behavior;
- `Reveal in Finder` for managed output folders;
- existing `Save to` and `Format` controls remain unchanged.

The default template is:

```text
{title}
```

This keeps normal output folders readable, for example:

```text
~/Downloads/Universal Media Extractor/Terence Tao on How AI Is Changing Mathematics
```

## Supported Template Tokens

URL download output folder templates support these tokens:

- `{source}` - source host such as `youtube.com` or `soundcloud.com`;
- `{channel}` - uploader/channel name when available from analysis;
- `{date}` - current UTC date in `YYYY-MM-DD` format;
- `{title}` - analyzed source title;
- `{project}` - optional project name field in the API contract;
- `{playlist_index}` - optional zero-padded playlist index such as `007`.

The first public UI exposes the compact template field but does not add a full template builder. Advanced users can type supported tokens directly.

## Safety

Rendered output names are sanitized for macOS and Windows:

- path separators are removed;
- Windows-reserved filename characters are removed;
- control characters are removed;
- trailing spaces/dots are removed;
- reserved Windows device names such as `CON` are made safe;
- output folders must remain inside the selected output base directory.

`yt-dlp` commands now include:

```text
--windows-filenames
```

This keeps downloaded media filenames closer to cross-platform-safe behavior.

## Duplicate Policies

`DownloadRequest.duplicate_policy` supports:

- `rename` - default; creates `Title`, then `Title 2`, `Title 3`, etc.;
- `skip` - returns a `skipped` `DownloadResult` and does not run `yt-dlp`;
- `overwrite` - removes the existing managed output folder and recreates it before download.

The UI labels these as:

- `Rename copy`;
- `Skip`;
- `Overwrite`.

The default is `rename` to avoid accidental data loss.

## Reveal Output

The API now exposes:

```text
POST /outputs/{output_id}/reveal
```

It only works for managed direct output folders under the configured output base. It asks the OS to reveal/open the folder using:

- macOS: `open <folder>`;
- Windows: `explorer <folder>`;
- Linux fallback: `xdg-open <folder>`.

The subprocess call uses a list of arguments and `shell=False`.

## What Did Not Change

This block does not add:

- batch processing;
- Archive Pack execution;
- new downloader engines;
- auth, payments, licensing, or packaging;
- new roadmap blocks;
- arbitrary filesystem browsing from the browser UI.

Udemy Course Mode remains internal/experimental and is not the target of this public output-template pass.

## Verification

Targeted verification:

```bash
node --check src/universal_media_extractor/static/app.js
.venv/bin/python -m pytest tests/test_output_manager.py tests/test_download_service.py tests/test_api_app.py -q
```

Expected focused result during implementation:

```text
70 passed
```

Full suite must also pass before closing the GitHub issue.
