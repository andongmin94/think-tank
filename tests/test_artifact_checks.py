"""Licence, compiled PDF, LaTeX template and replication-script checks."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import _artifact_checks as artifacts  # noqa: E402
from _prepared_checks import validate_prepared  # noqa: E402

GPL3 = "                    GNU GENERAL PUBLIC LICENSE\n                       Version 3, 29 June 2007\n"
MIT = "MIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software\n"
PROPRIETARY = "Copyright (c) 2026 Example Corp. All rights reserved. No redistribution.\n"


def make_pdf(path: Path, pages: list[str]) -> Path:
    """A minimal valid PDF whose pages carry the given lines of text."""
    objects = ["<< /Type /Catalog /Pages 2 0 R >>", None, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    kids = []
    for text in pages:
        lines = "".join(f"({line}) Tj 0 -20 Td " for line in text.split("\n"))
        stream = f"BT /F1 12 Tf 72 720 Td {lines}ET"
        objects.append(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")
        content = len(objects)
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R >> >> "
                       f"/Contents {content} 0 R >>")
        kids.append(f"{len(objects)} 0 R")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>"
    body, offsets = b"%PDF-1.4\n", []
    for number, obj in enumerate(objects, 1):
        offsets.append(len(body))
        body += f"{number} 0 obj\n{obj}\nendobj\n".encode("latin-1")
    xref = len(body)
    body += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    body += "".join(f"{offset:010d} 00000 n \n" for offset in offsets).encode()
    body += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.write_bytes(body)
    return path


@pytest.mark.parametrize("files,expected", [
    ({"LICENSE": GPL3}, "GPL-3.0"),
    ({"LICENSE.md": MIT}, "MIT"),
    ({"package.json": json.dumps({"license": "Apache-2.0"})}, "Apache-2.0"),
    ({"DESCRIPTION": "Package: x\nLicense: GPL (>= 2)\n"}, "GPL-2.0"),
    ({"pyproject.toml": '[project]\nlicense = { text = "BSD-3-Clause" }\n'}, "BSD-3-Clause"),
    ({"LICENSE": PROPRIETARY}, None),
    ({}, None),
])
def test_license_detection(tmp_path, files, expected):
    for name, text in files.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    assert artifacts.detect_license(tmp_path)[0] == expected


@pytest.mark.parametrize("license_text,requirement,status", [
    (GPL3, "gpl_compatible", "passed"), (MIT, "gpl_compatible", "passed"), (MIT, "osi", "passed"),
    (PROPRIETARY, "gpl_compatible", "pending"),
])
def test_license_requirements(tmp_path, license_text, requirement, status):
    (tmp_path / "LICENSE").write_text(license_text, encoding="utf-8")
    assert artifacts.license_item(tmp_path, requirement)["status"] == status


def test_non_compatible_license_fails(tmp_path):
    (tmp_path / "package.json").write_text(json.dumps({"license": "EPL-2.0"}), encoding="utf-8")
    assert artifacts.license_item(tmp_path, "gpl_compatible")["status"] == "failed"
    assert artifacts.license_item(tmp_path, "osi")["status"] == "passed"


def test_replication_script(tmp_path):
    assert artifacts.replication_item(tmp_path)["status"] == "failed"
    (tmp_path / "inst").mkdir()
    (tmp_path / "inst" / "replication.R").write_text("set.seed(1)\n", encoding="utf-8")
    result = artifacts.replication_item(tmp_path)
    assert result["status"] == "passed" and "inst/replication.R" in result["reason"]


@pytest.mark.parametrize("template,source,status", [
    ("sn-jnl", "\\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}\n", "passed"),
    ("sn-jnl", "% \\documentclass{sn-jnl}\n\\documentclass{article}\n", "failed"),
    ("jss", "\\documentclass[article]{jss}\n", "passed"),
    ("jmlr2e", "\\documentclass{article}\n\\usepackage{jmlr2e}\n", "passed"),
    ("jmlr2e", "\\documentclass{article}\n", "failed"),
])
def test_tex_template(tmp_path, template, source, status):
    tex = tmp_path / "paper.tex"
    tex.write_text(source, encoding="utf-8")
    assert artifacts.tex_item(tex, template)["status"] == status


@pytest.mark.parametrize("pages,status", [
    (["Intro", "Method", "Results", "Discussion\nReferences\n[1] A"], "passed"),
    (["Intro", "Method", "Results", "Discussion", "More\nReferences\n[1] A"], "failed"),
    (["One page only"], "passed"),
    (["a", "b", "c", "d", "e"], "pending"),
])
def test_pdf_text_pages(tmp_path, pages, status):
    pdf = make_pdf(tmp_path / "paper.pdf", pages)
    assert artifacts.pdf_pages_item(pdf, 4)["status"] == status


def test_supplied_files_replace_pending_items(tmp_path):
    draft = "# Pkg\n\n## Abstract\n\nAn R package.\n\n## Body\n\nText.\n"
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "LICENSE").write_text(GPL3, encoding="utf-8")
    (repo / "replication.R").write_text("set.seed(1)\n", encoding="utf-8")
    tex = tmp_path / "paper.tex"
    tex.write_text("\\documentclass[article]{jss}\n", encoding="utf-8")
    without = validate_prepared(draft, "jstatsoft")
    assert {i["id"]: i["status"] for i in without["items"]}["license"] == "pending"
    checked = validate_prepared(draft, "jstatsoft", repo=repo, tex=tex)
    status = {i["id"]: i["status"] for i in checked["items"]}
    assert status["license"] == status["replication_script"] == status["tex_template"] == "passed"
    assert checked["prefilter_passed"]
    (repo / "replication.R").unlink()
    failed = validate_prepared(draft, "jstatsoft", repo=repo, tex=tex)
    assert not failed["prefilter_passed"] and any(f["id"] == "replication_script" for f in failed["fixes"])


def test_cli_accepts_files_and_rejects_them_for_exporter_venues(tmp_path):
    (tmp_path / "paper.md").write_text("# T\n\n## Abstract\n\nText.\n", encoding="utf-8")
    make_pdf(tmp_path / "paper.pdf", ["a", "b\nReferences\n[1] x"])
    (tmp_path / "paper.tex").write_text("\\usepackage{jmlr2e}\n", encoding="utf-8")
    run = lambda *a: subprocess.run([sys.executable, str(ROOT / "scripts" / "think_tank.py"), "--lang", "en", *a],
                                    cwd=tmp_path, capture_output=True, encoding="utf-8", errors="replace", timeout=60)
    ok = run("check", "paper.md", "--venue", "jmlr-mloss", "--pdf", "paper.pdf", "--tex", "paper.tex")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    wrong = run("check", "paper.md", "--venue", "ieee-software", "--pdf", "paper.pdf")
    assert wrong.returncode == 2 and "apply to venues" in wrong.stderr
