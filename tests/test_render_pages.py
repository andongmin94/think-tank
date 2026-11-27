"""Source PDF pages render to PNG for reading tables and figures."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

import render_pages  # noqa: E402
from test_artifact_checks import make_pdf  # noqa: E402


@pytest.mark.parametrize("spec,total,expected", [(None, 3, [1, 2, 3]), ("2", 3, [2]), ("1,3", 3, [1, 3]),
                                                 ("2-3,2", 4, [2, 3]), (" 1 - 2 ", 2, [1, 2])])
def test_page_specs(spec, total, expected):
    assert render_pages.parse_pages(spec, total) == expected


@pytest.mark.parametrize("spec,message", [("0", "Invalid"), ("3-1", "Invalid"), ("a", "Unreadable"), ("5", "does not exist")])
def test_bad_page_specs(spec, message):
    with pytest.raises(ValueError, match=message):
        render_pages.parse_pages(spec, 4)


def test_too_many_pages_need_a_selection():
    with pytest.raises(ValueError, match="at most"):
        render_pages.parse_pages(None, render_pages.MAX_PAGES + 1)


def test_renders_selected_pages_with_manifest(tmp_path):
    pdf = make_pdf(tmp_path / "paper.pdf", ["Intro", "Table 1 accuracy 0.91", "Figure 2"])
    before = pdf.read_bytes()
    result = render_pages.render(pdf, tmp_path / "pages", pages="2-3", scale=1)
    assert result["pages"] == [2, 3]
    manifest = json.loads((tmp_path / "pages" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["total_pages"] == 3 and [row["page"] for row in manifest["pages"]] == [2, 3]
    from PIL import Image
    with Image.open(tmp_path / "pages" / "page-002.png") as image:
        assert image.size == (612, 792)
        assert image.getextrema() != ((255, 255), (255, 255), (255, 255))  # text was drawn
    assert pdf.read_bytes() == before


def test_existing_output_folder_is_refused(tmp_path):
    pdf = make_pdf(tmp_path / "paper.pdf", ["x"])
    (tmp_path / "pages").mkdir()
    with pytest.raises(ValueError, match="already exists"):
        render_pages.render(pdf, tmp_path / "pages")


def test_cli_reports_errors_without_traceback(tmp_path):
    pdf = make_pdf(tmp_path / "paper.pdf", ["x"])
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_pages.py"), str(pdf), "--pages", "9",
                             "--output-dir", str(tmp_path / "out")], capture_output=True, text=True, timeout=60)
    assert result.returncode == 2 and "does not exist" in result.stderr and "Traceback" not in result.stderr
    assert not (tmp_path / "out").exists()
