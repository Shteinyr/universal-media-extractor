import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from universal_media_extractor.services.output_manager import OutputManager, render_output_template


def test_output_manager_creates_analysis_output_dir(tmp_path):
    output_dir = OutputManager().create_analysis_output_dir(
        tmp_path, source_id="../bad source"
    )

    assert output_dir.exists()
    assert output_dir.is_dir()
    assert output_dir.parent == tmp_path.resolve()
    assert output_dir.name.startswith("analysis_bad_source_")


def test_output_manager_creates_download_output_structure(tmp_path):
    output_dir = OutputManager().create_download_output_dir(
        tmp_path, source_id="../video id", source_title="My Video"
    )

    assert output_dir.exists()
    assert output_dir.parent == tmp_path.resolve()
    assert output_dir.name == "My Video"
    assert (output_dir / ".metadata").is_dir()
    assert (output_dir / ".logs").is_dir()
    assert not (output_dir / "media").exists()
    assert not (output_dir / "metadata").exists()
    assert not (output_dir / "logs").exists()


def test_render_output_template_supports_public_tokens_and_safe_names():
    rendered = render_output_template(
        "{project} / {source} / {channel} / {date} / {playlist_index} / {title}",
        {
            "project": "Client:Course",
            "source": "youtube.com",
            "channel": "Channel<Name>",
            "date": "2026-08-05",
            "playlist_index": "007",
            "title": "CON",
        },
    )

    assert rendered == "Client Course - youtube.com - Channel Name - 2026-08-05 - 007 - CON"
    assert all(char not in rendered for char in r'<>:"/\|?*')


def test_download_output_template_uses_context_tokens(tmp_path):
    output_dir = OutputManager().create_download_output_dir(
        tmp_path,
        source_id="abc123",
        source_title="Episode: Intro/Setup",
        source_url="https://www.youtube.com/watch?v=abc123",
        output_template="{project} - {source} - {channel} - {date} - {playlist_index} - {title}",
        project_name="Training",
        channel_name="Creator/Channel",
        playlist_index=7,
    )

    assert output_dir.exists()
    assert output_dir.parent == tmp_path.resolve()
    assert "Training" in output_dir.name
    assert "youtube.com" in output_dir.name
    assert "Creator - Channel" in output_dir.name
    assert "007" in output_dir.name
    assert "Episode Intro - Setup" in output_dir.name


def test_download_output_duplicate_policy_renames_by_default(tmp_path):
    first = OutputManager().create_download_output_dir(tmp_path, source_title="Showreel")
    second = OutputManager().create_download_output_dir(tmp_path, source_title="Showreel")

    assert first.name == "Showreel"
    assert second.name == "Showreel 2"


def test_download_output_duplicate_policy_skips_existing(tmp_path):
    OutputManager().create_download_output_dir(tmp_path, source_title="Showreel")

    with pytest.raises(FileExistsError):
        OutputManager().create_download_output_dir(
            tmp_path,
            source_title="Showreel",
            duplicate_policy="skip",
        )


def test_download_output_duplicate_policy_overwrites_existing(tmp_path):
    first = OutputManager().create_download_output_dir(tmp_path, source_title="Showreel")
    marker = first / "old.txt"
    marker.write_text("old", encoding="utf-8")

    second = OutputManager().create_download_output_dir(
        tmp_path,
        source_title="Showreel",
        duplicate_policy="overwrite",
    )

    assert second == first
    assert not marker.exists()
    assert (second / ".metadata").is_dir()
    assert (second / ".logs").is_dir()


def test_download_output_reserved_windows_name_is_made_safe(tmp_path):
    output_dir = OutputManager().create_download_output_dir(tmp_path, source_title="CON")

    assert output_dir.name == "CON_file"


def test_output_manager_ensures_transcription_output_structure(tmp_path):
    output_dir = OutputManager().ensure_transcription_output_structure(tmp_path / "job")

    assert output_dir.exists()
    assert (output_dir / "media").is_dir()
    assert (output_dir / "metadata").is_dir()
    assert (output_dir / "logs").is_dir()


def test_output_manager_ensures_hidden_transcription_artifacts_for_download_output(tmp_path):
    output_dir = tmp_path / "Showreel"
    (output_dir / ".metadata").mkdir(parents=True)

    ensured = OutputManager().ensure_transcription_output_structure(output_dir)

    assert ensured == output_dir.resolve()
    assert (output_dir / ".metadata").is_dir()
    assert (output_dir / ".logs").is_dir()
    assert (output_dir / ".work").is_dir()
    assert not (output_dir / "transcripts").exists()
    assert not (output_dir / "metadata").exists()
    assert not (output_dir / "logs").exists()


def test_output_manager_creates_local_file_output_structure(tmp_path):
    output_dir = OutputManager().create_local_file_output_dir(
        tmp_path, filename="../My Clip.wav"
    )

    assert output_dir.exists()
    assert output_dir.parent == tmp_path.resolve()
    assert output_dir.name.startswith("local_")
    assert output_dir.name.endswith("_My_Clip")
    assert (output_dir / "source").is_dir()
    assert (output_dir / "media").is_dir()
    assert (output_dir / "metadata").is_dir()
    assert (output_dir / "logs").is_dir()
    assert (output_dir / "transcripts").is_dir()


def test_output_manager_lists_outputs_and_detects_artifacts(tmp_path):
    output_dir = tmp_path / "local_20260530T134814Z_sample"
    (output_dir / "source").mkdir(parents=True)
    (output_dir / "metadata").mkdir()
    (output_dir / "transcripts").mkdir()
    (output_dir / "source" / "sample.wav").write_bytes(b"abc")
    (output_dir / "metadata" / "local_file_analysis.json").write_text(
        '{"filename": "sample.wav"}',
        encoding="utf-8",
    )
    (output_dir / "transcripts" / "transcript.txt").write_text("hello", encoding="utf-8")
    (output_dir / "transcripts" / "summary_prompt.md").write_text("prompt", encoding="utf-8")

    result = OutputManager().list_outputs(tmp_path)

    assert len(result.outputs) == 1
    summary = result.outputs[0]
    assert summary.output_id == output_dir.name
    assert summary.source_type == "local_file"
    assert summary.title_or_filename == "sample.wav"
    assert summary.has_media is True
    assert summary.has_transcript is True
    assert summary.has_summary_prompt is True
    assert summary.files_count == 4
    assert summary.total_size_bytes == len(b"abc") + len("hello") + len("prompt") + len('{"filename": "sample.wav"}')


def test_output_manager_summarizes_url_output(tmp_path):
    output_dir = tmp_path / "Showreel"
    (output_dir / ".metadata").mkdir(parents=True)
    (output_dir / ".logs").mkdir()
    (output_dir / "Showreel [UUdxAp3kuKA].m4a").write_bytes(b"audio")
    (output_dir / ".metadata" / "download_request.json").write_text(
        '{"source_url": "https://youtu.be/UUdxAp3kuKA", "source_title": "Showreel"}',
        encoding="utf-8",
    )

    summary = OutputManager().summarize_output(tmp_path, output_dir.name)

    assert summary.source_type == "url"
    assert summary.title_or_filename == "Showreel"
    assert summary.has_media is True
    assert summary.has_transcript is False


def test_output_manager_safe_delete_inside_outputs(tmp_path):
    output_dir = tmp_path / "local_20260530T134814Z_delete_me"
    output_dir.mkdir()
    (output_dir / "file.txt").write_text("delete", encoding="utf-8")

    result = OutputManager().delete_output(tmp_path, output_dir.name)

    assert result.status == "deleted"
    assert not output_dir.exists()


def test_output_manager_safe_delete_refuses_path_traversal(tmp_path):
    outside = tmp_path.parent / "outside-output-delete-test"
    outside.mkdir(exist_ok=True)

    result = OutputManager().delete_output(tmp_path, "../outside-output-delete-test")

    assert result.status == "blocked"
    assert outside.exists()


def test_output_manager_safe_delete_refuses_outputs_root(tmp_path):
    result = OutputManager().delete_output(tmp_path, ".")

    assert result.status == "blocked"
    assert tmp_path.exists()


def test_output_manager_validate_output_base_expands_and_checks_writable(monkeypatch, tmp_path):
    home_dir = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home_dir))

    result = OutputManager().validate_output_base_dir(Path("~/Downloads/Universal Media Extractor"))

    assert result == (home_dir / "Downloads" / "Universal Media Extractor").resolve()
    assert result.is_dir()


def test_output_manager_resolve_reveal_path_prefers_primary_file(tmp_path):
    output_dir = tmp_path / "Showreel"
    output_dir.mkdir()
    media_file = output_dir / "Showreel.m4a"
    media_file.write_bytes(b"audio")

    result = OutputManager().resolve_reveal_path(tmp_path, "Showreel")

    assert result == media_file.resolve()


def test_output_manager_resolve_reveal_path_falls_back_to_folder(tmp_path):
    output_dir = tmp_path / "Empty"
    output_dir.mkdir()

    result = OutputManager().resolve_reveal_path(tmp_path, "Empty")

    assert result == output_dir.resolve()


def test_output_manager_resolve_reveal_path_refuses_traversal(tmp_path):
    with pytest.raises(ValueError):
        OutputManager().resolve_reveal_path(tmp_path, "../outside")
