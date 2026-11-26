"""How to repair a failed manuscript check, with Markdown the checks accept.

The examples are syntax only. They show the shape the checker parses; they never
supply facts, citations, tool names or results. Replace every angle-bracket slot
with real, verified content before export. tests/test_publication_hints.py
assembles a manuscript from these examples to keep them accurate.
"""

FIX_HINTS = {
    "abstract": {
        "how_to_fix": "Write one prose paragraph under a '## Abstract' heading, within the venue's word limit and without reference citations.",
        "example": "## Abstract\n\n<One paragraph stating the problem, the supported contribution and the main evidence.>",
    },
    "abstract_structure": {
        "how_to_fix": "Keep the Abstract to a single paragraph without lists, headings or citations; put keywords in their own paragraph after it.",
        "example": "## Abstract\n\n<One paragraph.>\n\nKeywords: <term>; <term>; <term>",
    },
    "keywords": {
        "how_to_fix": "Add one 'Keywords:' paragraph directly after the Abstract, separating distinct terms with semicolons.",
        "example": "Keywords: <term one>; <term two>; <term three>",
    },
    "reference_count": {
        "how_to_fix": "Under a '## References' heading, number entries [1], [2], ... in order, one entry per paragraph separated by blank lines, within the venue maximum.",
        "example": "## References\n\n[1] <Authors>, \"<Title>,\" <Venue>, <Year>.\n\n[2] <Authors>, \"<Title>,\" <Venue>, <Year>.",
    },
    "reference_count_consistency": {
        "how_to_fix": "Make reference labels unique and sequential from [1] with no gaps or duplicates.",
        "example": "[1] <first source>\n\n[2] <second source>",
    },
    "citation_references": {
        "how_to_fix": "Cite with bracketed numbers that match a References entry, such as [1] or [1, 2]; remove citations to missing entries.",
        "example": "<Claim supported by the cited source> [1].",
    },
    "reference_metadata": {
        "how_to_fix": "Give each reference the actual authors, title, venue and year from the source itself; do not invent missing fields.",
        "example": "[1] <Authors>, \"<Title>,\" <Venue>, <Year>, doi:<DOI if it exists>.",
    },
    "actionable_insights": {
        "how_to_fix": "Add exactly one block labelled 'Actionable insights:' (or a heading containing 'Actionable insights') followed directly by exactly three '-' bullets.",
        "example": "Actionable insights:\n\n- <First decision a practitioner can act on.>\n- <Second decision.>\n- <Third decision.>",
    },
    "ai_disclosure": {
        "how_to_fix": "In an Acknowledgments section, name the AI tools actually used, what they did (drafting, editing, analysis) and which parts they affected.",
        "example": "## Acknowledgments\n\nThe authors used <actual tool and version>, a generative AI language model, to draft and edit <affected sections>. The authors reviewed and take responsibility for all text.",
    },
    "placeholders": {
        "how_to_fix": "Remove editorial markers such as TODO, TBD, FIXME and [placeholder]; deliver missing content as pending in the checklist instead of in the article.",
        "example": "",
    },
    "escaped_prose": {
        "how_to_fix": "Replace literal '\\n' sequences with real line breaks; the manuscript was probably pasted from an escaped string.",
        "example": "",
    },
    "word_count": {
        "how_to_fix": "Bring the estimate within the venue limit by cutting repetition, not evidence; each table or figure counts as a fixed word allowance.",
        "example": "",
    },
    "required_sections": {
        "how_to_fix": "Add each missing section as a '## ' heading with real content, using the names the venue guide lists.",
        "example": "## <Required section name>\n\n<Section content from actual evidence.>",
    },
}


def fixes_for(items: list[dict]) -> list[dict]:
    """Repair guidance for every failed item that has one, in report order."""
    return [{"id": item["id"], "reason": item["reason"], **FIX_HINTS[item["id"]]}
            for item in items if item["status"] == "failed" and item["id"] in FIX_HINTS]
