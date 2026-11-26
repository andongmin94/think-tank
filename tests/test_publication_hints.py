"""Repair hints point at Markdown the checker actually accepts."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from _publication_checks import validate_manuscript  # noqa: E402
from _publication_hints import FIX_HINTS  # noqa: E402

FILLED = {
    "<One paragraph stating the problem, the supported contribution and the main evidence.>":
        "Teams reuse research prototypes on newer runtimes and meet failures that installation does not reveal. "
        "This article reports one such case and the decisions it required.",
    "<Claim supported by the cited source>": "Pinned serialization libraries can break on newer interpreters",
    "<actual tool and version>": "an AI assistant",
    "<affected sections>": "the Introduction and Discussion sections",
}


def _fill(example: str) -> str:
    for slot, text in FILLED.items():
        example = example.replace(slot, text)
    return re.sub(r"<([^<>]+)>", lambda match: match[1].replace(" ", "-"), example)


def _manuscript() -> str:
    hint = {key: _fill(value["example"]) for key, value in FIX_HINTS.items()}
    return "\n\n".join([
        "# Porting a Research Prototype",
        hint["abstract"],
        hint["keywords"],
        "## Problem",
        hint["citation_references"],
        "## Lessons",
        hint["actionable_insights"],
        hint["ai_disclosure"],
        hint["reference_count"],
    ]) + "\n"


def test_examples_satisfy_the_checks_they_describe():
    report = validate_manuscript(_manuscript(), "ieee-software")
    status = {item["id"]: item["status"] for item in report["items"]}
    for identifier in ("keywords", "reference_count", "citation_references", "actionable_insights",
                       "ai_disclosure", "placeholders", "escaped_prose"):
        assert status.get(identifier) == "passed", (identifier, report["blockers"])
    assert report["fixes"] == [fix for fix in report["fixes"] if fix["id"] not in
                               {"keywords", "reference_count", "actionable_insights", "ai_disclosure"}]


def test_failed_checks_carry_repair_guidance():
    report = validate_manuscript("# Title\n\n## Abstract\n\nShort.\n\n1. A numbered insight.\n", "ieee-software")
    fixes = {fix["id"]: fix for fix in report["fixes"]}
    for identifier in ("reference_count", "actionable_insights", "ai_disclosure", "keywords"):
        assert identifier in fixes, (identifier, sorted(fixes))
        assert fixes[identifier]["how_to_fix"] and fixes[identifier]["reason"]
    assert "- <" in fixes["actionable_insights"]["example"]


def test_hints_do_not_assert_facts():
    for identifier, hint in FIX_HINTS.items():
        assert hint["how_to_fix"], identifier
        assert not re.search(r"\b(?:TODO|TBD|FIXME)\b", hint["example"]), identifier
        assert not re.search(r"\b(?:ChatGPT|Claude|Copilot|Gemini)\b", hint["example"]), identifier


def test_skeleton_has_every_structure_the_checker_parses():
    skeleton = (Path(__file__).resolve().parents[1] / "assets/examples/ieee-software-skeleton.md").read_text(encoding="utf-8")
    report = validate_manuscript(skeleton, "ieee-software")
    status = {item["id"]: item["status"] for item in report["items"]}
    for identifier in ("keywords", "reference_count", "citation_references", "actionable_insights",
                       "ai_disclosure", "placeholders", "escaped_prose"):
        assert status.get(identifier) == "passed", (identifier, report["blockers"])
