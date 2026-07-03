# Block 8. Cleanup / Output Management

Date: 2026-05-30

## Status

Completed.

Block 8 adds a small output index and safe delete flow for user results under `outputs/`.

It does not scan or delete `proof/`.

## Implemented

- Added output models:
  - `OutputSummary`;
  - `OutputListResult`;
  - `OutputDeleteResult`.
- Extended `OutputManager` with:
  - `list_outputs(outputs_base_dir)`;
  - `summarize_output(outputs_base_dir, output_id)`;
  - `delete_output(outputs_base_dir, output_id)`.
- Added API endpoints:
  - `GET /outputs`;
  - `GET /outputs/{output_id}`;
  - `DELETE /outputs/{output_id}`.
- Added a static UI `Recent results` block.
- Added output path copy and safe delete actions in the UI.

## Output Index

Only direct subfolders of the configured `outputs/` folder are considered user outputs.

`proof/` is not part of the output index. It remains a development artifact area for manual proof files and should only be cleaned manually or by a future explicit development cleanup command.

For each output, the index returns:

- `output_id`;
- `output_dir`;
- `created_at`;
- `source_type`: `url`, `local_file`, or `unknown`;
- `title_or_filename`;
- `has_media`;
- `has_transcript`;
- `has_summary_prompt`;
- `total_size_bytes`;
- `files_count`;
- `last_modified_at`.

## Safe Delete

Delete accepts only `output_id`, which is the direct folder name under `outputs/`.

Safety rules:

- no arbitrary absolute path input;
- no path traversal;
- no slash/backslash in `output_id`;
- cannot delete `outputs/` root;
- cannot delete project root;
- cannot delete `proof/`;
- resolved target must stay inside configured `outputs/`;
- target must be a directory.

Blocked or missing targets return a structured API error.

## UI

The static UI now shows `Recent results` in the left panel.

For each recent output it shows:

- title or filename;
- source type;
- created time;
- size;
- file count;
- badges for media/transcript/prompt;
- `Copy path`;
- `Delete`.

The UI remains intentionally small. It does not preview old transcripts or become a file manager.

## Tests

Command:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
68 passed
```

Coverage added:

- list outputs;
- summarize local-file output;
- summarize URL output;
- detect media/transcript/prompt;
- compute total size and files count;
- safe delete inside `outputs/`;
- block path traversal;
- block outputs root deletion;
- `GET /outputs`;
- `GET /outputs/{output_id}`;
- `DELETE /outputs/{output_id}`;
- UI static labels and endpoint wiring for `Recent results`.

## Manual Proof

Manual proof used a dedicated dummy output:

```text
outputs/block8_dummy_output/
```

Flow:

```text
GET /health
GET /outputs
GET /outputs/block8_dummy_output
DELETE /outputs/block8_dummy_output
GET /outputs
verify real output still exists
```

Proof artifacts:

```text
proof/block_8/health.json
proof/block_8/outputs_before_delete.json
proof/block_8/dummy_detail_before_delete.json
proof/block_8/dummy_delete_result.json
proof/block_8/outputs_after_delete.json
proof/block_8/manual_review.json
```

Manual review confirmed:

- dummy output existed before delete;
- dummy output was deleted;
- dummy output disappeared from `/outputs`;
- real output `outputs/local_20260530T134814Z_synthetic_sine/` still exists;
- real transcript file still exists.

## Not Included

- Automatic `proof/` cleanup.
- Batch deletion.
- Output search/filtering.
- Transcript preview for old outputs.
- Desktop/native folder opening.
- Chrome extension.
- Desktop wrapper.
- AI summary API.
- Auth/database/cookies.
- Redis/Celery/external queue.
- React/Vite/CDN.
- Advanced progress parsing.
- Roadmap changes.
