"""The macOS Word route stages exact copies, never saves, and reports gaps.

Microsoft Word is not available on CI runners, so osascript is replaced by a
fake that behaves like the AppleScript renderer. Real rendering is verified
separately with dev/verify_mac_word.py on a Mac with Word.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import _publication_templates as templates  # noqa: E402

FULL_METRICS = {"pages": 4, "whole_words": 1200, "abstract_words": 90, "reference_count": 3,
                "reference_heading_found": True, "body_words": 1000, "body_table_words": 0, "body_tables": 0,
                "tables": 0, "figures": 1, "body_figures": 1, "read_only": True, "missing_template_fonts": [],
                "version": "16.99", "platform": "macOS"}


@pytest.fixture
def mac(tmp_path, monkeypatch):
    staging = tmp_path / "container-cache"
    staging.mkdir()
    monkeypatch.setattr(templates, "word_backend", lambda: "macos")
    monkeypatch.setattr(templates, "_mac_staging_root", lambda: staging)
    calls = []

    def fake_osascript(metrics):
        def run(command, **kwargs):
            calls.append(command)
            assert command[0] == "osascript" and command[1].endswith("render-word-mac.applescript")
            mode, source, target = command[2], Path(command[3]), command[4]
            assert source.is_relative_to(staging), "Word must only see a copy inside its sandbox container"
            if mode == "render":
                Path(target).write_bytes(b"%PDF-1.7 fake")
                return subprocess.CompletedProcess(command, 0, json.dumps({"read_only": True, "pages": 4}), "")
            return subprocess.CompletedProcess(command, 0, json.dumps(metrics), "")
        return run

    return staging, calls, fake_osascript


def test_pdf_is_rendered_from_a_staged_copy_and_staging_is_removed(tmp_path, monkeypatch, mac):
    staging, calls, fake = mac
    monkeypatch.setattr(templates.subprocess, "run", fake(FULL_METRICS))
    docx, pdf = tmp_path / "article.docx", tmp_path / "article.pdf"
    docx.write_bytes(b"docx bytes")
    result = templates.word_pdf(docx, pdf, venue_id="ieee-software")
    assert pdf.read_bytes() == b"%PDF-1.7 fake"
    assert docx.read_bytes() == b"docx bytes"
    assert result["engine"].startswith("Microsoft Word for Mac") and result["read_only"] is True
    assert calls[0][5:8] == ["ReferenceHead", "Bib_entry", "Abstract—"]
    assert list(staging.iterdir()) == []


def test_complete_metrics_are_returned(tmp_path, monkeypatch, mac):
    _, _, fake = mac
    monkeypatch.setattr(templates.subprocess, "run", fake(FULL_METRICS))
    docx = tmp_path / "article.docx"
    docx.write_bytes(b"docx bytes")
    measured = templates.measure_word(docx, venue_id="ieee-security-privacy")
    assert measured["metrics"]["body_words"] == 1000 and measured["source_unchanged"] is True


def test_missing_statistics_fail_instead_of_being_estimated(tmp_path, monkeypatch, mac):
    _, _, fake = mac
    partial = {key: value for key, value in FULL_METRICS.items() if key not in {"body_words", "abstract_words"}}
    monkeypatch.setattr(templates.subprocess, "run", fake(partial))
    docx = tmp_path / "article.docx"
    docx.write_bytes(b"docx bytes")
    with pytest.raises(ValueError, match="incomplete .*abstract_words.*body_words"):
        templates.measure_word(docx)


def test_word_errors_are_reported(tmp_path, monkeypatch, mac):
    monkeypatch.setattr(templates.subprocess, "run",
                        lambda command, **kw: subprocess.CompletedProcess(command, 1, "", "Quit Microsoft Word first"))
    docx = tmp_path / "article.docx"
    docx.write_bytes(b"docx bytes")
    with pytest.raises(ValueError, match="Quit Microsoft Word first"):
        templates.word_pdf(docx, tmp_path / "out.pdf")
    assert not (tmp_path / "out.pdf").exists()


def test_other_platforms_name_both_supported_systems(tmp_path, monkeypatch):
    monkeypatch.setattr(templates, "word_backend", lambda: None)
    docx = tmp_path / "article.docx"
    docx.write_bytes(b"docx bytes")
    with pytest.raises(ValueError, match="Windows or macOS"):
        templates.word_pdf(docx, tmp_path / "out.pdf")
    with pytest.raises(ValueError, match="Windows or macOS"):
        templates.measure_word(docx)
