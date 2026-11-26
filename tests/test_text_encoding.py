"""Text I/O does not depend on the locale.

Without an explicit encoding, Python 3.11-3.14 on Windows uses the ANSI code
page (for example cp949 on Korean systems) for files and redirected console
streams, so UTF-8 text fails or is garbled. Files name UTF-8; console JSON is
ASCII-escaped so any decoder reads it.
"""
import ast
import json
import os
import subprocess
import sys
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


def _prints_non_ascii_json(tree):
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print"):
            continue
        for argument in ast.walk(node):
            if (isinstance(argument, ast.Call) and isinstance(argument.func, ast.Attribute)
                    and argument.func.attr == "dumps"):
                flags = {keyword.arg: keyword.value for keyword in argument.keywords}
                value = flags.get("ensure_ascii")
                if isinstance(value, ast.Constant) and value.value is False:
                    yield node.lineno


@pytest.mark.parametrize("source", sorted((ROOT / "scripts").glob("*.py")), ids=lambda path: path.name)
def test_console_json_is_ascii_escaped(source):
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    assert list(_prints_non_ascii_json(tree)) == []


def test_cli_error_with_non_ascii_path_survives_a_narrow_console(tmp_path):
    missing = tmp_path / "Erdős–Rényi.bib"
    environment = {key: value for key, value in os.environ.items() if not key.startswith("PYTHONUTF8")}
    environment["PYTHONIOENCODING"] = "ascii"  # Stands in for cp949/cp1252 consoles on every platform.
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/import_references.py"), "--input", str(missing),
         "--output-dir", str(tmp_path / "out")],
        capture_output=True, env=environment, timeout=30)
    assert b"Traceback" not in result.stderr
    assert result.returncode == 2
    assert result.stderr.isascii()
    assert "error" in json.loads(result.stderr.decode("ascii"))
