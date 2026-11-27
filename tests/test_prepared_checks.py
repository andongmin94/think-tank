"""Countable rules for host-prepared venues pass compliant drafts and catch breaches."""
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _prepared_checks import PREPARED_RULES, validate_prepared  # noqa: E402
from _publication_hints import FIX_HINTS  # noqa: E402
from _publication_venues import PREPARED_MANUSCRIPTS  # noqa: E402

STATEMENT_TEXT = {
    "statements_and_declarations": "## Statements and Declarations\n\nCompeting interests: The authors declare none.\n",
    "data_availability": "## Data Availability\n\nThe evidence is archived with the repository at a fixed commit.\n",
    "competing_interests": "## Declaration of Competing Interest\n\nThe authors declare no competing interests.\n",
    "ai_declaration": ("## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process\n\n"
                       "During the preparation of this work the authors used an AI assistant to edit the text.\n"),
}


def compliant(venue: str) -> str:
    rules = PREPARED_RULES[venue]
    low, high = rules.get("abstract_words", (120, 120))
    words = max(low, min(high, 160))
    if "structured_abstract" in rules:
        abstract = "\n\n".join(f"{label}: " + " ".join(["word"] * 30) for label in
                               ("Context", "Objectives", "Methods", "Results", "Conclusion"))
    else:
        abstract = " ".join(["word"] * words)
    parts = ["# A Study", "## Abstract", abstract]
    if "keywords" in rules:
        count = rules["keywords"][0] if rules["keywords"][0] > 1 else 3
        parts.append("Keywords: " + "; ".join(f"term{i}" for i in range(count)))
    if "highlights" in rules:
        parts += ["## Highlights", "- First short finding\n- Second short finding\n- Third short finding"]
    parts += ["## Introduction", "Body text."]
    parts += [STATEMENT_TEXT[identifier] for identifier, _, _ in rules.get("statements", ())]
    return "\n\n".join(parts) + "\n"


def status(report, identifier):
    return [item["status"] for item in report["items"] if item["id"] == identifier]


@pytest.mark.parametrize("venue", sorted(PREPARED_RULES))
def test_compliant_draft_passes_every_countable_rule(venue):
    report = validate_prepared(compliant(venue), venue)
    assert report["prefilter_passed"], report["blockers"]
    assert report["pending"], "venue-specific human checks must stay visible"


def test_every_prepared_venue_has_rules():
    assert set(PREPARED_RULES) == set(PREPARED_MANUSCRIPTS)


@pytest.mark.parametrize("venue", [v for v, r in PREPARED_RULES.items() if r.get("statements")])
def test_missing_statements_are_caught(venue):
    draft = compliant(venue)
    for text in STATEMENT_TEXT.values():
        draft = draft.replace(text, "")
    report = validate_prepared(draft, venue)
    for identifier, _, _ in PREPARED_RULES[venue]["statements"]:
        assert status(report, identifier) == ["failed"], identifier
        assert any(fix["id"] == identifier for fix in report["fixes"]), identifier


def test_ist_structured_abstract_and_word_limit():
    draft = compliant("ist").replace("Methods: ", "Approach: ")
    report = validate_prepared(draft, "ist")
    assert status(report, "structured_abstract") == ["failed"] and "Method" in report["blockers"][0]
    long = compliant("ist").replace("Body text.", " ".join(["word"] * 14900) + "\n\n| a | b |\n| --- | --- |\n| 1 | 2 |")
    assert status(validate_prepared(long, "ist"), "word_count") == ["failed"]


def test_highlights_count_and_length():
    long = "- " + "x" * 86
    draft = compliant("jsys").replace("- Third short finding", long)
    report = validate_prepared(draft, "jsys")
    assert status(report, "highlights") == ["failed"] and "86 chars" in " ".join(report["blockers"])
    missing = re.sub(r"## Highlights\n\n(- .*\n)+", "", compliant("jsys"))
    assert status(validate_prepared(missing, "jsys"), "highlights") == ["failed"]
    assert status(validate_prepared(re.sub(r"## Highlights\n\n(- .*\n)+", "", compliant("ist")), "ist"),
                  "highlights") == ["passed"]


@pytest.mark.parametrize("venue,count,expected", [("ase", 3, "failed"), ("ase", 4, "passed"), ("ase", 7, "failed"),
                                                  ("emse", 6, "passed"), ("jsys", 8, "failed")])
def test_keyword_ranges(venue, count, expected):
    draft = re.sub(r"(?m)^Keywords:.*$", "Keywords: " + "; ".join(f"k{i}" for i in range(count)), compliant(venue))
    assert status(validate_prepared(draft, venue), "keywords") == [expected]


@pytest.mark.parametrize("venue,words,expected", [("ase", 149, "failed"), ("ase", 250, "passed"),
                                                  ("emse", 251, "failed"), ("scico-osp", 251, "failed")])
def test_abstract_ranges(venue, words, expected):
    draft = compliant(venue)
    draft = re.sub(r"## Abstract\n\n.*?\n\n", "## Abstract\n\n" + " ".join(["w"] * words) + "\n\n", draft, flags=re.S)
    assert status(validate_prepared(draft, venue), "abstract") == [expected]


@pytest.mark.parametrize("identifier", ["structured_abstract", "highlights", "statements_and_declarations",
                                        "data_availability", "competing_interests", "ai_declaration"])
def test_new_hints_examples_satisfy_their_checks(identifier):
    venue = {"structured_abstract": "ist", "highlights": "jsys", "statements_and_declarations": "ase",
             "data_availability": "ase", "competing_interests": "jsys", "ai_declaration": "jsys"}[identifier]
    example = re.sub(r"<([^<>]+)>", lambda m: m[1].replace(" ", "-")[:20], FIX_HINTS[identifier]["example"])
    draft = compliant(venue)
    draft = draft.replace(STATEMENT_TEXT.get(identifier, "@@none@@"), "")
    if identifier == "highlights":
        draft = re.sub(r"## Highlights\n\n(- .*\n)+", "", draft)
    if identifier == "structured_abstract":
        draft = re.sub(r"## Abstract\n\n.*?\n\nKeywords", "Keywords", draft, flags=re.S)
    report = validate_prepared(draft + "\n" + example + "\n", venue)
    assert status(report, identifier) == ["passed"], report["blockers"]


def test_cli_checks_prepared_venue_and_explains_export(tmp_path):
    (tmp_path / "paper.md").write_text(compliant("ist"), encoding="utf-8")
    run = lambda *a: subprocess.run([sys.executable, str(ROOT / "scripts" / "think_tank.py"), "--lang", "en", *a],
                                    cwd=tmp_path, capture_output=True, encoding="utf-8", errors="replace", timeout=60)
    checked = run("check", "paper.md", "--venue", "ist")
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert "Needs a person" in checked.stdout
    exported = run("export", "paper.md", "--venue", "ist")
    assert exported.returncode == 2 and "references/ist.md" in exported.stderr
