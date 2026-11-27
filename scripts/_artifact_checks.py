"""Checks on files beside the manuscript: licence, compiled PDF, LaTeX source, replication script.

Each function reads only the files it is given and never runs project code.
A check that cannot decide returns "pending" with the reason, never a guess.
"""
import json
from pathlib import Path
import re

# Licence identifiers we can recognise from common licence texts or metadata.
_TEXT_SIGNATURES = (
    ("AGPL-3.0", r"GNU AFFERO GENERAL PUBLIC LICENSE\s+Version 3"),
    ("LGPL-3.0", r"GNU LESSER GENERAL PUBLIC LICENSE\s+Version 3"),
    ("LGPL-2.1", r"GNU LESSER GENERAL PUBLIC LICENSE\s+Version 2\.1"),
    ("GPL-3.0", r"GNU GENERAL PUBLIC LICENSE\s+Version 3"),
    ("GPL-2.0", r"GNU GENERAL PUBLIC LICENSE\s+Version 2"),
    ("Apache-2.0", r"Apache License\s+Version 2\.0"),
    ("MPL-2.0", r"Mozilla Public License,?\s+(Version|v\.?)\s*2\.0"),
    ("EPL-2.0", r"Eclipse Public License\s*-?\s*v\s*2\.0"),
    ("BSD-3-Clause", r"Redistribution and use in source and binary forms[\s\S]{0,1500}Neither the name"),
    ("BSD-2-Clause", r"Redistribution and use in source and binary forms"),
    ("MIT", r"Permission is hereby granted, free of charge, to any person obtaining a copy"),
    ("ISC", r"Permission to use, copy, modify, and(/or)? distribute this software for any purpose"),
    ("Unlicense", r"This is free and unencumbered software released into the public domain"),
)
OSI_APPROVED = {"AGPL-3.0", "LGPL-3.0", "LGPL-2.1", "GPL-3.0", "GPL-2.0", "Apache-2.0", "MPL-2.0", "EPL-2.0",
                "BSD-3-Clause", "BSD-2-Clause", "MIT", "ISC", "Unlicense"}
# FSF list of GPL-compatible free software licences (Apache-2.0 with GPL-3 only).
GPL_COMPATIBLE = {"GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0", "AGPL-3.0", "MIT", "BSD-2-Clause", "BSD-3-Clause",
                  "ISC", "Apache-2.0", "MPL-2.0", "Unlicense"}
_LICENSE_FILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENCE.md", "COPYING", "COPYING.md")


def _normalise(identifier: str) -> str | None:
    value = identifier.strip().upper().replace(" ", "-")
    aliases = {"GPL-2": "GPL-2.0", "GPL-2.0-ONLY": "GPL-2.0", "GPL-2.0-OR-LATER": "GPL-2.0", "GPL-2.0+": "GPL-2.0",
               "GPL-3": "GPL-3.0", "GPL-3.0-ONLY": "GPL-3.0", "GPL-3.0-OR-LATER": "GPL-3.0", "GPL-3.0+": "GPL-3.0",
               "GPL-(>=-2)": "GPL-2.0", "GPL-(>=-3)": "GPL-3.0", "GPL-(>=2)": "GPL-2.0", "GPL-(>=3)": "GPL-3.0",
               "LGPL-2.1-ONLY": "LGPL-2.1", "LGPL-2.1-OR-LATER": "LGPL-2.1", "LGPL-3.0-ONLY": "LGPL-3.0",
               "LGPL-3.0-OR-LATER": "LGPL-3.0", "AGPL-3.0-ONLY": "AGPL-3.0", "AGPL-3.0-OR-LATER": "AGPL-3.0",
               "APACHE-2.0": "Apache-2.0", "MIT": "MIT", "ISC": "ISC", "MPL-2.0": "MPL-2.0", "BSD-2-CLAUSE": "BSD-2-Clause",
               "BSD-3-CLAUSE": "BSD-3-Clause", "UNLICENSE": "Unlicense", "EPL-2.0": "EPL-2.0"}
    return aliases.get(value) or aliases.get(value.split("+")[0].split("|")[0])


def detect_license(repo: Path) -> tuple[str | None, str]:
    """(SPDX-like identifier or None, where it was found)."""
    for name in ("package.json",):
        path = repo / name
        if path.is_file():
            try:
                value = json.loads(path.read_text(encoding="utf-8")).get("license")
            except (ValueError, OSError):
                value = None
            if isinstance(value, str) and _normalise(value):
                return _normalise(value), f"{name} license field"
    description = repo / "DESCRIPTION"
    if description.is_file():
        match = re.search(r"(?mi)^License:\s*(.+)$", description.read_text(encoding="utf-8", errors="replace"))
        if match:
            first = re.split(r"\s*\|\s*", match[1].strip())[0]
            if _normalise(first):
                return _normalise(first), "DESCRIPTION License field"
    pyproject = repo / "pyproject.toml"
    if pyproject.is_file():
        match = re.search(r'(?m)^license\s*=\s*(?:\{\s*text\s*=\s*)?"([^"]+)"', pyproject.read_text(encoding="utf-8", errors="replace"))
        if match and _normalise(match[1]):
            return _normalise(match[1]), "pyproject.toml license"
    for name in _LICENSE_FILES:
        path = repo / name
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            for identifier, pattern in _TEXT_SIGNATURES:
                if re.search(pattern, text, re.I):
                    return identifier, name
            return None, f"{name} (unrecognised text)"
    return None, "no licence file or metadata found"


def license_item(repo: Path, requirement: str) -> dict:
    found, where = detect_license(repo)
    allowed = GPL_COMPATIBLE if requirement == "gpl_compatible" else OSI_APPROVED
    label = "GPL-2, GPL-3 or a GPL-compatible licence" if requirement == "gpl_compatible" else "an OSI-approved licence"
    if found is None:
        return {"status": "pending", "reason": f"Could not identify the licence ({where}); confirm it is {label}."}
    if found in allowed:
        return {"status": "passed", "reason": f"Licence {found} from {where} is {label}."}
    return {"status": "failed", "reason": f"Licence {found} from {where} is not {label}."}


REPLICATION_NAMES = re.compile(r"(?i)^(replication|reproduce|reproduction|article|code|replicate)[\w-]*\.(r|py|jl|m|do|sas|sh)$")


def replication_item(folder: Path) -> dict:
    candidates = sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*")
                        if p.is_file() and REPLICATION_NAMES.match(p.name) and ".git" not in p.parts)
    if candidates:
        return {"status": "passed", "reason": "Replication script found: " + ", ".join(candidates[:3]) +
                ". Running it is a separate, authorized step."}
    return {"status": "failed", "reason": "No standalone replication script found (for example replication.R or replication.py)."}


TEX_TEMPLATES = {
    "sn-jnl": (r"\\documentclass(\[[^\]]*\])?\{sn-jnl\}", "\\documentclass{sn-jnl} (Springer Nature template)"),
    "jss": (r"\\documentclass(\[[^\]]*\])?\{jss\}", "\\documentclass[article]{jss} (JSS style)"),
    "jmlr2e": (r"\\usepackage(\[[^\]]*\])?\{jmlr2e\}", "\\usepackage{jmlr2e} (JMLR style)"),
}


def tex_item(tex: Path, template: str) -> dict:
    pattern, label = TEX_TEMPLATES[template]
    source = re.sub(r"(?m)(?<!\\)%.*$", "", tex.read_text(encoding="utf-8", errors="replace"))
    if re.search(pattern, source):
        return {"status": "passed", "reason": f"LaTeX source uses {label}."}
    return {"status": "failed", "reason": f"LaTeX source does not use {label}."}


def pdf_pages_item(pdf: Path, max_text_pages: int) -> dict:
    """Pages before the references heading must not exceed the limit."""
    import pypdfium2
    document = pypdfium2.PdfDocument(str(pdf))
    try:
        total = len(document)
        references_page = None
        for index in range(total):
            page = document[index]
            text = page.get_textpage().get_text_range()
            if re.search(r"(?mi)^\s*(references|bibliography)\s*$", text):
                references_page = index + 1
                break
    finally:
        document.close()
    if references_page is None:
        status = "passed" if total <= max_text_pages else "pending"
        return {"status": status, "reason": f"{total} pages; no References heading found, so the text/references split "
                                             f"could not be measured (limit {max_text_pages} pages of text)."}
    text_pages = references_page if references_page > 1 else 1
    # References starting mid-page: that page still contains text.
    ok = text_pages <= max_text_pages
    return {"status": "passed" if ok else "failed",
            "reason": f"References begin on page {references_page} of {total}; text uses {text_pages} page(s), "
                      f"limit {max_text_pages}."}
