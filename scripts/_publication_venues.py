"""The supported article categories and the official guidance actually checked."""

CS_GUIDANCE = "https://www.computer.org/publications/author-resources"
AI_GUIDANCE = "https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/"
SOFTWARE_GUIDANCE = "https://www.computer.org/digital-library/magazines/so/cfp-ieee-software"
SP_GUIDANCE = "https://www.computer.org/digital-library/magazines/sp/cfp-real-world-security-impact"

VENUE_RULES = {
    "ieee-software": {
        "publication": "IEEE Software", "output": "word", "checked_at": "2026-10-18",
        "source_urls": [SOFTWARE_GUIDANCE, CS_GUIDANCE, AI_GUIDANCE],
        "citation_style": "superscript_outside_punctuation", "biographies": True,
        "limits": {"word_count_scope": "body_excluding_references_and_bios", "max_words": 4200,
                   "max_abstract_words": 150, "max_references": 15, "visual_word_cost": 250,
                   "min_keywords": 3, "max_keywords": 8, "insight_count": 3},
        "writer_targets": {"abstract_words": 130, "whole_words": [3200, 3800]},
    },
    "ieee-security-privacy": {
        "publication": "IEEE Security & Privacy", "output": "word", "checked_at": "2026-10-18",
        "source_urls": [SP_GUIDANCE, CS_GUIDANCE, AI_GUIDANCE],
        "citation_style": "bracketed_inside_punctuation", "biographies": True,
        "limits": {"word_count_scope": "whole_article", "min_words": 4900, "max_words": 7200,
                   "max_abstract_words": 50, "max_references": 15, "visual_word_cost": 250,
                   "min_keywords": 3, "max_keywords": 8},
        "writer_targets": {"abstract_words": 45, "whole_words": [5400, 6500]},
    },
    "joss": {
        "publication": "Journal of Open Source Software", "output": "markdown-bibtex", "checked_at": "2026-11-02",
        "source_urls": ["https://joss.readthedocs.io/en/latest/paper.html",
                        "https://joss.readthedocs.io/en/latest/submitting.html"],
        "citation_style": "apa_author_date", "biographies": False,
        "limits": {"min_words": 750, "max_words": 1750},
    },
}

EXPORT_VENUES = tuple(VENUE_RULES)
WORD_VENUES = tuple(venue for venue in EXPORT_VENUES if VENUE_RULES[venue]["output"] == "word")

# These venues accept a host-prepared manuscript. They do not use a retained
# Word template or the JOSS adapter. Roles refer to the private preparation bundle.
PREPARED_MANUSCRIPTS = {"emse": ("editable_docx", ".docx"),
                        "jmlr-mloss": ("review_pdf", ".pdf")}
VENUES = (*EXPORT_VENUES, *PREPARED_MANUSCRIPTS)
