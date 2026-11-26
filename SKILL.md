---
name: think-tank
description: Draft, revise or review software-repository papers with traceable evidence. Use for journal selection, manuscript writing, bibliography checks, or submission-file preparation.
---

# Think Tank

Research and write in the current conversation. The scripts collect, inspect and package authored files; they do not choose a contribution or write a paper. Deliver one useful article supported by the available evidence, not a plan or a promised future result.

## Runtime

Use the same instructions in Claude Code, Claude.ai or another Agent Skills host. For installation or missing prerequisites, read [runtime.md](references/runtime.md). Resolve tool paths from this installed skill directory, not from the input repository. No provider API key or separate model runner is required. For the four official-template Word routes, use `export --docx-only` when editable DOCX is needed without native Word. Follow the venue guide for other formats; if the required tools are unavailable, deliver the incomplete source bundle. Leave Word/PDF verification pending.

## Choose the requested path

- **New repository to draft:** follow [repository-to-draft.md](references/repository-to-draft.md). Read the actual sources, compare three supported venue/article-type candidates by evidence fit, then write and package one draft. Use [contribution-selection.md](references/contribution-selection.md) only when the research question is unclear.
- **Continue or revise:** start from retained material and the requested change. Revisit changed sources and affected claims, not the entire research workflow. Preserve prior versions and review hashes.
- **Review:** use [research-and-review.md](references/research-and-review.md). Assess contribution, evidence, comparison and readability. Distinguish publication as written, revision severity and submission suitability; scores are not targets or acceptance probabilities. When an independent review is in scope, use at most one, on the exact manuscript and relevant evidence. Preserve unfavorable findings; do not automatically redraft or rerate.
- **Prepare files only:** use the relevant command from [tools.md](references/tools.md) or [researcher-convenience.md](references/researcher-convenience.md). Do not restart venue selection, research or full-article review for an export, bibliography import or bundle request.

Read detailed references only for the active task. Continuation, author-profile, anonymity, response-letter, environment and final-preparation helpers are optional tools, not mandatory stages.

## Evidence and writing

Read consequential code, README, tests, retained experiments and nearby primary literature before making claims. Retain the inspected commit, exact source witnesses, URLs, dates and hashes. Identify partial reading or inaccessible sources; an abstract is not a full paper. Distinguish source-declared, statically observed, measured, derived and proposed claims using the existing evidence ledger. A matching hash or quote does not establish truth, novelty or runtime behavior.

Write in English unless requested otherwise. Lead with the reader's problem, the supported contribution, competent alternatives, evidence and limitations. Remove repetition and defensive framing without hiding uncertainty. Keep collection logs, scores and missing author details outside the article. Do not invent results, adoption, citations, quotations, author facts, funding, consent or model identity. Deliver supported prose with an explicit incomplete status when evidence is missing, rather than padding or fabricating a finished study.

Caution limits what you claim, not how concretely you show what is supported. Before drafting, read [writing-quality.md](references/writing-quality.md): make each main point concrete with a verified code excerpt, figure, number or commit; mine the project's history for decisions that changed; compare real alternatives on the same criteria; write lessons that could only come from this work; and run its self-review before export.

## Venue and output

| Venue guide | Appropriate contribution | Output route |
| --- | --- | --- |
| [IEEE Software](references/ieee-software.md) | Practitioner decisions, alternatives and lessons | Retained official DOCX, native Word/PDF |
| [IEEE Security & Privacy](references/ieee-security-privacy.md) | Substantive security/privacy contribution | Retained official DOCX, native Word/PDF |
| [JOSS](references/joss.md) | Research software with demonstrated use/development | Authored Markdown, BibTeX and local figures |
| [Empirical Software Engineering](references/emse.md) | Empirical or replication study with an assessable design, observations and analysis | Author-prepared editable DOCX; no journal Word template |
| [JMLR MLOSS](references/jmlr-mloss.md) | Open ML implementation with demonstrated community and distinct software contribution | Official-style LaTeX → review PDF; separate cover letter |
| [Software: Practice and Experience](references/spe.md) | Practical experience building or operating real software systems | Author-prepared editable DOCX (or LaTeX PDF); scope form |
| [Science of Computer Programming OSP](references/scico-osp.md) | The software itself: an open-licensed tool with a short description | Official OSP Word/LaTeX template |
| [Journal of Systems and Software](references/jsys.md) | Evidence-backed SE research, In Practice industry reports, new ideas | Author-prepared editable DOCX or LaTeX; highlights |
| [Information and Software Technology](references/ist.md) | Research or experience improving development practice; systematic reviews | Author-prepared editable DOCX; structured abstract |
| [Automated Software Engineering](references/ase.md) | Automated SE techniques and tools with evaluation | Springer Nature LaTeX → review PDF |
| [Journal of Statistical Software](references/jstatsoft.md) | GPL-compatible statistical software with replication materials | JSS-style LaTeX → review PDF; replication script |

Every supported venue has a route to publish without a mandatory fee; do not recommend venues that always charge an article processing charge. Choose by contribution and evidence, not impact factor. A generic application is not automatically research software; topic labels are not approved-journal lists. Verify current official article rules and template provenance directly, including licensing and AI policy. Retained templates do not prove current compliance. For JOSS, automated review is author-side diagnostics only; publication verdicts belong to humans, and editor/reviewer conversations must not be AI-written except for translation.

## Preserve and deliver

Keep original data, manuscripts, reviews, failures and historical counts unchanged. Work outside the installed skill in a new output directory. Do not modify or execute the input repository without authorization. Reuse the existing evidence and preparation reports; do not create parallel catalogs, controllers or repeated status documents. Rerun checks only for changed inputs, a new failure or a concrete unresolved concern.

Deliver editable source, bibliography, needed figures and a checklist with the source revision, actual checks and unresolved evidence. Include requested exports only when actually produced. Record real AI assistance and review scope. Hash consistency, scientific assessment, format checks, visual inspection and human approval are separate: none substitutes for another. Inspect every page of a final PDF; unavailable Word/Inara rendering remains unverified. The native Word finalizer applies only to its four official-template venues.

Leave author identity/consent, eligibility, ethics, rights, funding/conflicts and data/code availability pending without genuine confirmation. ORCID data is not consent. Do not publish, upload, submit or contact others without separate authorization. Stop after the requested draft, revision, review or preparation bundle; do not start another improvement cycle.
