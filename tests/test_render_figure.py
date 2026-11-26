"""SVG figures render to PNG through an installed browser, safely."""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import render_figure  # noqa: E402

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
       '<rect width="100%" height="100%" fill="#ffffff"/><rect x="10" y="10" width="60" height="30" fill="#1f77b4"/>'
       '<text x="12" y="70" font-size="14">init</text></svg>')


def svg_file(tmp_path, width=200, height=100, body=None):
    path = tmp_path / "figure.svg"
    path.write_text(body or SVG.format(w=width, h=height), encoding="utf-8")
    return path


@pytest.mark.parametrize("attrs,expected", [('width="300" height="120"', (300, 120)),
                                            ('width="300px" height="120px"', (300, 120)),
                                            ('viewBox="0 0 640 360"', (640, 360))])
def test_svg_size_reads_dimensions(tmp_path, attrs, expected):
    path = svg_file(tmp_path, body=f'<svg xmlns="http://www.w3.org/2000/svg" {attrs}></svg>')
    assert render_figure.svg_size(path) == expected


def test_svg_without_size_is_rejected(tmp_path):
    path = svg_file(tmp_path, body='<svg xmlns="http://www.w3.org/2000/svg" width="50%"></svg>')
    with pytest.raises(ValueError, match="width and height or a viewBox"):
        render_figure.svg_size(path)


def test_existing_png_is_never_overwritten(tmp_path):
    svg = svg_file(tmp_path)
    png = tmp_path / "figure.png"
    png.write_bytes(b"keep")
    with pytest.raises(ValueError, match="already exists"):
        render_figure.render(svg, png)
    assert png.read_bytes() == b"keep"


def test_browser_failure_is_reported(tmp_path, monkeypatch):
    monkeypatch.setattr(render_figure, "find_browser", lambda explicit=None: Path(sys.executable))
    monkeypatch.setattr(render_figure.subprocess, "run",
                        lambda command, **kw: subprocess.CompletedProcess(command, 1, "", "GPU process crashed"))
    with pytest.raises(ValueError, match="did not produce a screenshot"):
        render_figure.render(svg_file(tmp_path), tmp_path / "out.png")
    assert not (tmp_path / "out.png").exists()


def test_real_render_when_a_browser_is_installed(tmp_path):
    try:
        render_figure.find_browser()
    except ValueError:
        pytest.skip("No Chrome, Edge or Chromium installed")
    result = render_figure.render(svg_file(tmp_path, 200, 100), tmp_path / "figure.png", scale=2)
    from PIL import Image
    with Image.open(tmp_path / "figure.png") as image:
        assert image.size == (400, 200)
        assert image.getpixel((5, 5))[:3] == (255, 255, 255)
    assert result["size_px"] == [400, 200]
