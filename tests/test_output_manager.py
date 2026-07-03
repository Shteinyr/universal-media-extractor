from universal_media_extractor.services.output_manager import OutputManager


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
    assert output_dir.name == "My_Video"
    assert (output_dir / ".metadata").is_dir()
    assert (output_dir / ".logs").is_dir()
    assert not (output_dir / "media").exists()
    assert not (output_dir / "metadata").exists()
    assert not (output_dir / "logs").exists()


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
