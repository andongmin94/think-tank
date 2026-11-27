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
    "unfilled_slots": {
        "how_to_fix": "Replace every <...> slot copied from the skeleton with real, verified content, or remove the sentence; list anything still missing as pending in the checklist.",
        "example": "",
    },
    "structured_abstract": {
        "how_to_fix": "Write the abstract as five labelled parts in this order: Context, Objectives, Methods, Results, Conclusion.",
        "example": "## Abstract\n\nContext: <the problem setting>\n\nObjectives: <what the study set out to do>\n\nMethods: <how>\n\nResults: <what was found>\n\nConclusion: <what it means>",
    },
    "highlights": {
        "how_to_fix": "Add a '## Highlights' section with 3–5 bullets of at most 85 characters each (spaces included); submit it as a separate file named with 'highlights'.",
        "example": "## Highlights\n\n- <Novel result in at most 85 characters>\n- <Second result>\n- <Method or evidence>",
    },
    "statements_and_declarations": {
        "how_to_fix": "Add a '## Statements and Declarations' section with the competing-interest, funding and other statements the journal lists, using the authors' actual answers.",
        "example": "## Statements and Declarations\n\nCompeting interests: <the authors' actual statement>\n\nFunding: <actual funding, or none>",
    },
    "data_availability": {
        "how_to_fix": "Add a data availability statement saying where the data, code and other evidence can be accessed, or why access is restricted.",
        "example": "## Data Availability\n\n<Where the evidence is archived, with a persistent identifier, or the actual restriction.>",
    },
    "competing_interests": {
        "how_to_fix": "Add a declaration of competing interests with the authors' actual answer.",
        "example": "## Declaration of Competing Interest\n\n<The authors' actual declaration.>",
    },
    "ai_declaration": {
        "how_to_fix": "Add Elsevier's separate section declaring the generative AI tools actually used and why, stating that the authors reviewed the output.",
        "example": "## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process\n\nDuring the preparation of this work the author(s) used <actual tool> to <actual purpose>. After using this tool, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the published article.",
    },
    "escaped_prose": {
        "how_to_fix": "Replace literal '\\n' sequences with real line breaks; the manuscript was probably pasted from an escaped string.",
        "example": "",
    },
    "word_count": {
        "how_to_fix": "Bring the estimate within the venue limit by cutting repetition, not evidence; each table or figure counts as a fixed word allowance.",
        "example": "",
    },
}


def fixes_for(items: list[dict]) -> list[dict]:
    """Repair guidance for every failed item that has one, in report order."""
    return [{"id": item["id"], "reason": item["reason"], **FIX_HINTS[item["id"]]}
            for item in items if item["status"] == "failed" and item["id"] in FIX_HINTS]
