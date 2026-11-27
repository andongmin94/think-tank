"""Countable rules for venues whose manuscripts the host prepares itself.

These venues have no retained Word template, so there is no native export or
Word measurement. The checks below cover what the official guidance states and
Markdown can show: abstract and keyword limits, structured abstracts,
highlights, word budgets and required statement sections. Everything else in
the venue guide stays a pending human or host check. Rules are taken from the
guide files in references/ and carry the date they were checked.
"""
import re

from _publication_checks import EDITORIAL_MARKERS, SKELETON_SLOT, _parts, _words
from _publication_hints import fixes_for
from _publication_text import mask_code, mask_inline_markup

ELSEVIER_STATEMENTS = (
    ("competing_interests", r"(declaration of )?competing interests?|conflicts? of interest",
     "a declaration of competing interests"),
    ("ai_declaration", r"generative ai|ai[- ]assisted",
     "a 'Declaration of generative AI and AI-assisted technologies in the manuscript preparation process' section"),
)

PREPARED_RULES = {
    "emse": {
        "publication": "Empirical Software Engineering", "guide": "references/emse.md", "checked_at": "2026-11-06",
        "abstract_words": (150, 250), "keywords": (4, 6),
        "statements": (("statements_and_declarations", r"statements and declarations", "a 'Statements and Declarations' section"),
                       ("data_availability", r"data availability", "a data availability statement")),
        "pending": ["Document substantive LLM use in the Methods (or a suitable) section.",
                    "Confirm competing-interest and funding statements with every author."],
    },
    "jmlr-mloss": {
        "publication": "JMLR Machine Learning Open Source Software", "guide": "references/jmlr-mloss.md",
        "checked_at": "2026-11-06",
        "pending": ["Check the compiled JMLR-style PDF: at most four pages of text plus references.",
                    "Supply the separate cover letter naming track, version, repository, licence and community evidence."],
    },
    "spe": {
        "publication": "Software: Practice and Experience", "guide": "references/spe.md", "checked_at": "2026-11-26",
        "keywords": (1, 7),
        "statements": (("data_availability", r"data availability", "a data availability statement"),
                       ("competing_interests", r"conflicts? of interest|competing interests?", "a conflict of interest disclosure")),
        "pending": ["Complete the Submission Topic and Scope Form for Research Articles.",
                    "Confirm Wiley's current AI-use policy; none was found on the journal page."],
    },
    "scico-osp": {
        "publication": "Science of Computer Programming (Original Software Publication)", "guide": "references/scico-osp.md",
        "checked_at": "2026-11-26", "abstract_words": (1, 250), "keywords": (1, 7),
        "highlights": {"required": True, "count": (3, 5), "max_chars": 85},
        "statements": ELSEVIER_STATEMENTS,
        "pending": ["Fill the official OSP template (about six pages) without changing its formatting.",
                    "Confirm the software uses a recognised (for example OSI-approved) licence and include its documentation."],
    },
    "jsys": {
        "publication": "Journal of Systems and Software", "guide": "references/jsys.md", "checked_at": "2026-11-26",
        "abstract_words": (1, 250), "keywords": (1, 7),
        "highlights": {"required": True, "count": (3, 5), "max_chars": 85},
        "statements": ELSEVIER_STATEMENTS,
        "pending": ["Deposit or explain research data and decide on the Open Science Initiative."],
    },
    "ist": {
        "publication": "Information and Software Technology", "guide": "references/ist.md", "checked_at": "2026-11-26",
        "keywords": (1, 7), "structured_abstract": ("context", "objectives?", "methods?", "results?", "conclusions?"),
        "highlights": {"required": False, "count": (3, 5), "max_chars": 85},
        "word_limit": {"max": 15000, "visual_cost": 200, "scope": "whole manuscript including references and appendices",
                       "note": "Research Papers; systematic reviews allow 20,000 and Short Communications 2,500."},
        "statements": ELSEVIER_STATEMENTS,
        "pending": ["Disclose funding sources and their role."],
    },
    "ase": {
        "publication": "Automated Software Engineering", "guide": "references/ase.md", "checked_at": "2026-11-26",
        "abstract_words": (150, 250), "keywords": (4, 6),
        "statements": (("statements_and_declarations", r"statements and declarations", "a 'Statements and Declarations' section"),
                       ("data_availability", r"data availability", "a data availability statement")),
        "pending": ["Compile with the Springer Nature LaTeX template (sn-jnl) and submit sources with the PDF.",
                    "Document substantive LLM use in the Methods (or a suitable) section."],
    },
    "jstatsoft": {
        "publication": "Journal of Statistical Software", "guide": "references/jstatsoft.md", "checked_at": "2026-11-26",
        "pending": ["Confirm the code is licensed GPL-2, GPL-3 or GPL-compatible.",
                    "Supply a standalone replication script reproducing every result, with seeds and output.",
                    "Write in LaTeX with the JSS style and compare against existing open-source implementations."],
    },
}


def _item(identifier, status, reason, *, stage="manuscript"):
    return {"id": identifier, "label": identifier.replace("_", " "), "status": status, "stage": stage, "reason": reason}


def _section(parts: dict[str, str], pattern: str) -> tuple[str, str] | None:
    """The first level-2 section whose heading matches, as (heading, body)."""
    for heading, body in parts.items():
        if re.search(pattern, heading, re.I):
            return heading, body
    return None


def _labelled(prose: str, pattern: str) -> bool:
    """A statement given as a bold or plain label paragraph instead of a heading."""
    return re.search(rf"(?mi)^\s*(\*\*|__)?\s*({pattern})\b[^\n]*?[:.]", prose) is not None


def validate_prepared(markdown: str, venue_id: str) -> dict:
    """Checks a Markdown manuscript against the venue's countable rules."""
    if venue_id not in PREPARED_RULES:
        raise ValueError(f"No prepared-manuscript rules for {venue_id}")
    rules = PREPARED_RULES[venue_id]
    parts = _parts(markdown)
    prose = mask_code(markdown)
    items, metrics = [], {}

    abstract = re.sub(r"(?mi)^Keywords:.*$", "", parts.get("abstract", "")).strip()
    metrics["abstract_words_estimate"] = _words(mask_inline_markup(abstract))
    if "abstract_words" in rules:
        low, high = rules["abstract_words"]
        words = metrics["abstract_words_estimate"]
        items.append(_item("abstract", "passed" if abstract and low <= words <= high else "failed",
                           f"Abstract estimate {words} words; {rules['publication']} asks for {low}–{high}."
                           if low > 1 else f"Abstract estimate {words} words; at most {high} allowed."))
    elif not abstract and venue_id not in {"jmlr-mloss", "jstatsoft"}:
        items.append(_item("abstract", "failed", "Add a '## Abstract' section."))

    if "structured_abstract" in rules:
        missing = [label.rstrip("s?").title() for label in rules["structured_abstract"]
                   if not re.search(rf"(?mi)^\s*(\*\*|__)?\s*{label}\s*(\*\*|__)?\s*:", abstract)]
        items.append(_item("structured_abstract", "failed" if missing else "passed",
                           "Structured abstract labels missing: " + ", ".join(missing) + "."
                           if missing else "Structured abstract has Context, Objectives, Methods, Results and Conclusion."))

    keyword_lines = re.findall(r"(?mi)^Keywords:\s*(.+)$", prose)
    keywords = [term.strip() for line in keyword_lines for term in re.split(r"[;,]", line) if term.strip()]
    metrics["keywords"] = keywords
    if "keywords" in rules:
        low, high = rules["keywords"]
        items.append(_item("keywords", "passed" if low <= len(set(k.casefold() for k in keywords)) <= high else "failed",
                           f"Found {len(keywords)} keywords; {rules['publication']} asks for {low}–{high} in a 'Keywords:' line."))

    if "highlights" in rules:
        spec = rules["highlights"]
        found = _section(parts, r"^highlights$")
        bullets = re.findall(r"(?m)^\s*[-*+]\s+(.+?)\s*$", found[1]) if found else []
        metrics["highlights"] = bullets
        low, high = spec["count"]
        long = [b for b in bullets if len(b) > spec["max_chars"]]
        if not found:
            items.append(_item("highlights", "failed" if spec["required"] else "passed",
                               f"Add a '## Highlights' section with {low}–{high} bullets of at most {spec['max_chars']} characters "
                               "(submitted as a separate file)." if spec["required"] else "Highlights are optional for this venue."))
        else:
            ok = low <= len(bullets) <= high and not long
            detail = f"{len(bullets)} highlights; {low}–{high} needed, each at most {spec['max_chars']} characters including spaces."
            if long:
                detail += " Too long: " + "; ".join(f"{len(b)} chars" for b in long) + "."
            items.append(_item("highlights", "passed" if ok else "failed", detail))

    if "word_limit" in rules:
        spec = rules["word_limit"]
        tables = len(re.findall(r"(?m)^\|?\s*:?-{3,}.*\|.*$", prose))
        figures = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", prose))
        estimate = _words(markdown) + spec["visual_cost"] * (tables + figures)
        metrics["word_count_estimate"] = estimate
        items.append(_item("word_count", "passed" if estimate <= spec["max"] else "failed",
                           f"Estimate {estimate} words ({spec['scope']}, {spec['visual_cost']} per table or figure); "
                           f"limit {spec['max']:,}. {spec['note']}"))

    for identifier, pattern, label in rules.get("statements", ()):
        present = _section(parts, pattern) is not None or _labelled(prose, pattern)
        items.append(_item(identifier, "passed" if present else "failed",
                           f"Include {label}." if not present else f"Found {label}."))

    body = "\n".join(text for heading, text in parts.items() if heading not in {"references"})
    items.append(_item("placeholders", "failed" if EDITORIAL_MARKERS.search(body) else "passed",
                       "Resolve TODO/TBD/FIXME and placeholder markers."))
    slots = list(dict.fromkeys(SKELETON_SLOT.findall(prose)))
    items.append(_item("unfilled_slots", "failed" if slots else "passed",
                       f"Replace {len(slots)} unfilled skeleton slot(s), for example " + ", ".join(slots[:3]) + "."
                       if slots else "No unfilled skeleton slots remain."))
    items.append(_item("escaped_prose", "failed" if re.search(r"\\n(?:\\n|## |[-*] |Keywords:)", prose) else "passed",
                       "Use real paragraph breaks in prose."))
    for note in rules.get("pending", []):
        items.append(_item("venue_requirement", "pending", note, stage="submission"))
    items.append(_item("author_declarations", "pending",
                       "Authors must confirm identity, originality, rights, AI use and every declaration.", stage="submission"))

    failed = [item for item in items if item["status"] == "failed"]
    return {"venue_id": venue_id, "publication": rules["publication"], "checked_at": rules["checked_at"],
            "guide": rules["guide"], "mode": "prepared_manuscript_preflight", "items": items, "metrics": metrics,
            "blockers": [item["reason"] for item in failed], "fixes": fixes_for(items),
            "pending": [item["reason"] for item in items if item["status"] == "pending"],
            "prefilter_passed": not failed, "native_word_measured": False, "scientific_merit_assessed": False,
            "scope": "Countable rules from the venue guide only; layout, page limits, templates and human declarations "
                     "are checked by the host and the authors."}
