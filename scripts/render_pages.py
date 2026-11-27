"""Render pages of a source PDF to PNG images so tables, figures and equations can be read as images.

    python scripts/render_pages.py paper.pdf --pages 3,5-7 --output-dir pages/

Text extraction loses table structure, chart values and layout. Rendering the
pages and reading the images keeps them. Uses the bundled pypdfium2; no
browser, model or network. Writes a new folder with one PNG per page and a
manifest recording the source hash and page numbers, so values read from an
image can be cited to an exact page.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _publication_files import digest_file, ensure_unlinked  # noqa: E402

MAX_PAGES = 30


def parse_pages(spec: str | None, total: int) -> list[int]:
    """'3,5-7' -> [3, 5, 6, 7]; None -> every page up to the limit."""
    if not spec:
        pages = list(range(1, total + 1))
    else:
        pages = []
        for part in spec.split(","):
            match = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+)\s*)?", part)
            if not match:
                raise ValueError(f"Unreadable page range: {part!r}; use for example 3,5-7")
            start, end = int(match[1]), int(match[2] or match[1])
            if start < 1 or end < start:
                raise ValueError(f"Invalid page range: {part.strip()}")
            pages.extend(range(start, end + 1))
        pages = list(dict.fromkeys(pages))
    beyond = [page for page in pages if page > total]
    if beyond:
        raise ValueError(f"The PDF has {total} pages; requested page {beyond[0]} does not exist")
    if len(pages) > MAX_PAGES:
        raise ValueError(f"Render at most {MAX_PAGES} pages per call; choose the pages with tables or figures")
    return pages


def render(pdf: Path, output_dir: Path, *, pages: str | None = None, scale: float = 2.0) -> dict:
    pdf, output_dir = pdf.absolute(), output_dir.absolute()
    ensure_unlinked(pdf)
    ensure_unlinked(output_dir)
    if pdf.suffix.lower() != ".pdf" or not pdf.is_file():
        raise ValueError("Give an existing .pdf file")
    if output_dir.exists():
        raise ValueError("The output folder already exists; choose a new folder")
    if not 1 <= scale <= 4:
        raise ValueError("--scale must be between 1 and 4")
    import pypdfium2
    source_sha = digest_file(pdf)
    document = pypdfium2.PdfDocument(str(pdf))
    try:
        selected = parse_pages(pages, len(document))
        output_dir.mkdir(parents=True)
        rows = []
        for number in selected:
            image = document[number - 1].render(scale=scale).to_pil()
            target = output_dir / f"page-{number:03d}.png"
            image.save(target, format="PNG")
            rows.append({"page": number, "path": target.name, "size_px": list(image.size),
                         "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
        total = len(document)
    finally:
        document.close()
    if digest_file(pdf) != source_sha:
        raise ValueError("The PDF changed while it was being rendered")
    manifest = {"source": str(pdf), "source_sha256": source_sha, "total_pages": total, "scale": scale,
                "pages": rows, "scope": "Images of the source pages for reading tables, figures and equations. "
                "Values read from an image are transcriptions; cite the page and check them against the image."}
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"output_dir": str(output_dir), "pages": [row["page"] for row in rows], "source_sha256": source_sha}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--pages", help=f"Pages such as 3,5-7 (default: all, at most {MAX_PAGES})")
    parser.add_argument("--output-dir", type=Path, required=True, help="New folder for the PNG pages")
    parser.add_argument("--scale", type=float, default=2.0, help="Pixel density multiplier, 1-4 (default 2)")
    args = parser.parse_args(argv)
    try:
        result = render(args.pdf, args.output_dir, pages=args.pages, scale=args.scale)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
