"""Render an authored SVG diagram to a PNG figure with an installed Chrome or Edge.

    python scripts/render_figure.py figure.svg figure.png [--scale 2]

Uses a headless browser that is already installed (no download), a temporary
profile that is deleted afterwards, and never overwrites an existing PNG.
The PNG is checked to have the SVG's size times the scale.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _publication_files import ensure_unlinked  # noqa: E402

_CANDIDATES = {
    "win32": [r"{pf}\Google\Chrome\Application\chrome.exe", r"{pf86}\Google\Chrome\Application\chrome.exe",
              r"{local}\Google\Chrome\Application\chrome.exe", r"{pf86}\Microsoft\Edge\Application\msedge.exe",
              r"{pf}\Microsoft\Edge\Application\msedge.exe"],
    "darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
               "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
               "/Applications/Chromium.app/Contents/MacOS/Chromium"],
}
_LINUX_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge")


def find_browser(explicit: str | None = None) -> Path:
    """An installed Chrome, Edge or Chromium; never downloads one."""
    if explicit:
        path = Path(explicit)
        if not path.is_file():
            raise ValueError(f"Browser not found: {explicit}")
        return path
    if sys.platform == "win32":
        folders = {"pf": os.environ.get("ProgramFiles", r"C:\Program Files"),
                   "pf86": os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                   "local": os.environ.get("LOCALAPPDATA", "")}
        candidates = [Path(item.format(**folders)) for item in _CANDIDATES["win32"]]
    elif sys.platform == "darwin":
        candidates = [Path(item) for item in _CANDIDATES["darwin"]]
    else:
        candidates = [Path(found) for name in _LINUX_NAMES if (found := shutil.which(name))]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise ValueError("No installed Chrome, Edge or Chromium was found; install one or pass --browser")


def _length(value: str | None) -> float | None:
    if not value:
        return None
    match = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*(px)?\s*", value)
    return float(match[1]) if match else None


def svg_size(svg: Path) -> tuple[int, int]:
    """Pixel size from width/height, falling back to the viewBox."""
    root = ET.parse(svg).getroot()
    if not root.tag.endswith("svg"):
        raise ValueError("The input is not an SVG document")
    width, height = _length(root.get("width")), _length(root.get("height"))
    if width is None or height is None:
        box = (root.get("viewBox") or "").replace(",", " ").split()
        if len(box) != 4:
            raise ValueError("The SVG needs numeric width and height or a viewBox")
        width, height = float(box[2]), float(box[3])
    if width <= 0 or height <= 0 or width > 8000 or height > 8000:
        raise ValueError("The SVG size must be positive and at most 8000 px")
    return round(width), round(height)


def render(svg: Path, png: Path, *, scale: float = 2.0, browser: str | None = None) -> dict:
    svg, png = svg.absolute(), png.absolute()
    ensure_unlinked(svg)
    ensure_unlinked(png)
    if svg.suffix.lower() != ".svg" or png.suffix.lower() != ".png":
        raise ValueError("Render an .svg input to a new .png output")
    if png.exists():
        raise ValueError("The PNG already exists; choose a new output path")
    if not 1 <= scale <= 4:
        raise ValueError("--scale must be between 1 and 4")
    width, height = svg_size(svg)
    binary = find_browser(browser)
    with tempfile.TemporaryDirectory(prefix="think-tank-figure-") as temporary:
        page = Path(temporary) / "figure.html"
        page.write_text("<!doctype html><meta charset='utf-8'><style>html,body{margin:0;padding:0;background:#fff}"
                        f"img{{display:block;width:{width}px;height:{height}px}}</style>"
                        f"<img src='{svg.as_uri()}'>", encoding="utf-8")
        shot = Path(temporary) / "shot.png"
        command = [str(binary), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                   "--hide-scrollbars", f"--user-data-dir={Path(temporary) / 'profile'}",
                   f"--force-device-scale-factor={scale}", f"--window-size={width},{height}",
                   f"--screenshot={shot}", page.as_uri()]
        try:
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace",
                                    timeout=120, check=False)
        except subprocess.TimeoutExpired as exc:
            raise ValueError("The headless browser timed out after 120 seconds") from exc
        if result.returncode or not shot.is_file():
            raise ValueError("The headless browser did not produce a screenshot: " + result.stderr[-800:])
        from PIL import Image
        with Image.open(shot) as image:
            actual = image.size
        expected = (round(width * scale), round(height * scale))
        if abs(actual[0] - expected[0]) > 2 or abs(actual[1] - expected[1]) > 2:
            raise ValueError(f"Rendered size {actual} does not match the SVG size {expected}")
        shutil.copyfile(shot, png)
    return {"svg": str(svg), "png": str(png), "size_px": list(actual), "scale": scale,
            "browser": str(binary), "svg_size": [width, height]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("svg", type=Path)
    parser.add_argument("png", type=Path)
    parser.add_argument("--scale", type=float, default=2.0, help="Pixel density multiplier (default 2)")
    parser.add_argument("--browser", help="Path to an installed Chrome, Edge or Chromium")
    args = parser.parse_args(argv)
    try:
        result = render(args.svg, args.png, scale=args.scale, browser=args.browser)
    except (OSError, ValueError, ET.ParseError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
