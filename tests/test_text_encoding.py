"""Text file I/O names its encoding, so results do not depend on the locale.

Without an explicit encoding, Python 3.11-3.14 on Windows uses the ANSI code
page (for example cp949 on Korean systems) and fails or garbles UTF-8 text.
"""
import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = sorted((ROOT / "scripts").glob("*.py")) + sorted((ROOT / "tests").glob("*.py"))


def _missing_encoding(tree):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        keywords = {keyword.arg for keyword in node.keywords}
        if "encoding" in keywords or None in keywords:
            continue
        if node.func.attr == "read_text" and not node.args:
            yield node.lineno, "read_text"
        elif node.func.attr == "write_text" and len(node.args) < 2:
            yield node.lineno, "write_text"


@pytest.mark.parametrize("source", SOURCES, ids=lambda path: f"{path.parent.name}/{path.name}")
def test_text_io_names_its_encoding(source):
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    assert list(_missing_encoding(tree)) == []
