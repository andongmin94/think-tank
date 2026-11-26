"""The people-facing CLI: relative paths, plain summaries, safe defaults."""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "think_tank.py"
sys.path.insert(0, str(ROOT / "scripts"))

import think_tank  # noqa: E402


def run(*args, cwd):
    return subprocess.run([sys.executable, str(CLI), "--lang", "en", *args], cwd=cwd, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=180, check=False)


def filled(path: Path) -> Path:
    text = path.read_text(encoding="utf-8")
    text = text.replace("<actual tool and version>", "an AI writing assistant").replace(
        "<affected sections>", "the Introduction section")
    target = path.with_name("filled.md")
    target.write_text(re.sub(r"<([^<>]+)>", lambda match: match[1], text), encoding="utf-8")
    return target


def test_new_check_and_docx_export_with_relative_paths(tmp_path):
    created = run("new", "article.md", cwd=tmp_path)
    assert created.returncode == 0, created.stderr
    assert (tmp_path / "article.md").read_text(encoding="utf-8").startswith("# <Article title>")

    unfilled = run("check", "article.md", cwd=tmp_path)
    assert unfilled.returncode == 1
    assert "[X] unfilled_slots" in unfilled.stdout and "How to fix:" in unfilled.stdout

    manuscript = filled(tmp_path / "article.md")
    checked = run("check", manuscript.name, cwd=tmp_path)
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert "0 to fix" in checked.stdout and "not scientific approval" in checked.stdout

    exported = run("export", manuscript.name, "--docx-only", cwd=tmp_path)
    assert exported.returncode == 0, exported.stdout + exported.stderr
    folders = [path for path in tmp_path.iterdir() if path.is_dir() and path.name.startswith("filled-ieee-software-")]
    assert len(folders) == 1 and (folders[0] / "manuscript-ieee-software.docx").is_file()
    assert "not rendered (--docx-only)" in exported.stdout


def test_new_refuses_to_overwrite(tmp_path):
    (tmp_path / "article.md").write_text("mine\n", encoding="utf-8")
    result = run("new", "article.md", cwd=tmp_path)
    assert result.returncode == 2 and "already exists" in result.stderr
    assert (tmp_path / "article.md").read_text(encoding="utf-8") == "mine\n"


def test_missing_file_is_explained_without_a_traceback(tmp_path):
    result = run("check", "missing.md", cwd=tmp_path)
    assert result.returncode == 2
    assert "File not found" in result.stderr and "Traceback" not in result.stderr


def test_json_mode_keeps_the_full_machine_report(tmp_path):
    run("new", "article.md", cwd=tmp_path)
    result = run("check", "article.md", "--json", cwd=tmp_path)
    report = json.loads(result.stdout)
    assert report["mode"] == "skill_read_only_preflight" and report["fixes"]


def test_doctor_reports_capabilities(tmp_path):
    result = run("doctor", cwd=tmp_path)
    assert result.returncode in {0, 1}
    assert "Check manuscripts:" in result.stdout and "Export Word (DOCX):" in result.stdout


@pytest.mark.parametrize("locale_name,expected", [("ko_KR", "ko"), ("Korean_Korea", "ko"), ("en_US", "en"), (None, "en")])
def test_language_follows_the_locale_unless_overridden(monkeypatch, locale_name, expected):
    monkeypatch.delenv("THINK_TANK_LANG", raising=False)
    monkeypatch.delenv("LANG", raising=False)
    monkeypatch.setattr(think_tank.locale, "getlocale", lambda: (locale_name, None))
    assert think_tank._language(None) == expected
    assert think_tank._language("en") == "en"
    monkeypatch.setenv("THINK_TANK_LANG", "ko")
    assert think_tank._language(None) == "ko"


def test_both_languages_define_every_message():
    assert set(think_tank.TEXT["en"]) == set(think_tank.TEXT["ko"])


def test_report_rendering_lists_fixes_before_pending():
    report = {"items": [{"id": "keywords", "status": "failed", "reason": "Add keywords."},
                        {"id": "author_photo", "status": "pending", "reason": "Get a photo."},
                        {"id": "abstract", "status": "passed", "reason": "ok"}],
              "fixes": [{"id": "keywords", "how_to_fix": "Add a Keywords: line.", "example": "Keywords: a; b; c"}]}
    text = think_tank.render_report(report, think_tank.TEXT["en"], "Check")
    assert text.index("[X] keywords") < text.index("[ ] author_photo")
    assert "1 to fix, 1 need a person, 1 passed" in text and "Keywords: a; b; c" in text
