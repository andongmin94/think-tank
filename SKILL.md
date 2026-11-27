---
name: think-tank
description: Draft, revise or review software-repository papers with traceable evidence. Use for journal selection, manuscript writing, bibliography checks, or submission-file preparation.
---

# Think Tank

Research and write in the current conversation. Scripts collect, inspect and package authored files; they never choose a contribution or write the paper. Deliver one useful article the evidence supports, not a plan or a promised result.

## Runtime

Works in Claude Code, Claude.ai or any Agent Skills host, with no provider API key or separate model runner. Resolve tool paths from this installed skill directory, not the input repository. Installation, prerequisites and the `export --docx-only` fallback without native Word: [runtime.md](references/runtime.md). If a venue's tools are unavailable, deliver the incomplete source bundle and leave Word/PDF verification pending.

## Choose the requested path

- **New repository to draft:** follow [repository-to-draft.md](references/repository-to-draft.md): read actual sources, compare three supported venue/article-type candidates by evidence fit, write, take one independent review, make **one revision**, package. Use [contribution-selection.md](references/contribution-selection.md) only when the research question is unclear.
- **Continue or revise:** start from retained material and the requested change; revisit only changed sources and affected claims. Preserve prior versions and review hashes.
- **Review:** follow [research-and-review.md](references/research-and-review.md): at most one independent review, on the exact manuscript and relevant evidence. Preserve unfavorable findings; never automatically redraft or rerate.
- **Prepare files only:** run the relevant command from [tools.md](references/tools.md) or [researcher-convenience.md](references/researcher-convenience.md). Never restart venue selection, research or full review for an export, bibliography import or bundle.

Read references only for the active task. Continuation, author-profile, anonymity, response-letter, environment and final-preparation helpers are optional, not stages.

## Evidence and writing

- Before claiming, read consequential code, README, tests, retained experiments and nearby primary literature. Retain the inspected commit, exact source witnesses, URLs, dates and hashes.
- Flag partial reading and inaccessible sources; an abstract is not a full paper.
- Text extraction mangles tables, charts and equations. When a claim depends on one in a source PDF, render that page with `scripts/render_pages.py paper.pdf --pages N --output-dir NEW` and read the image; transcribe the values you use with their page numbers into a notes file and cite it in the evidence ledger.
- Label each claim's basis in the existing evidence ledger ([kinds](references/researcher-convenience.md#link-manuscript-claims-to-actual-evidence)). A matching hash or quote does not establish truth, novelty or runtime behavior.
- Write in English unless asked otherwise. Lead with the reader's problem, the supported contribution, competent alternatives, evidence and limitations. Cut repetition and defensive framing without hiding uncertainty. Keep collection logs, scores and missing author details out of the article.
- Never invent results, adoption, citations, quotations, author facts, funding, consent or model identity. When evidence is missing, deliver supported prose marked incomplete, not padding or a fabricated study.
- Caution limits what you claim, not how concretely you show it. Before drafting, read and follow [writing-quality.md](references/writing-quality.md), including its self-review before export.
- Optional: interview the user about reasons and rejected options only if they built the project and agree ([author-interview.md](references/author-interview.md)); measure central claims in an isolated copy only with explicit execution authorization ([measurement.md](references/measurement.md)).

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

- Every supported venue has a fee-free route; never recommend venues that always charge an article processing charge. Choose by contribution and evidence, not impact factor.
- A generic application is not automatically research software; topic labels are not approved-journal lists.
- Verify current official rules and template provenance directly, including licensing and AI policy; retained templates do not prove current compliance.
- JOSS: automated review is author-side diagnostics only; humans give verdicts; no AI-written editor/reviewer conversations except translation ([joss.md](references/joss.md#limits-and-human-decisions)).

## Preserve and deliver

- Keep original data, manuscripts, reviews, failures and historical counts unchanged. Work in a new output directory outside the installed skill. Never modify or execute the input repository without authorization.
- Reuse the existing evidence and preparation reports; no parallel catalogs, controllers or repeated status documents. Rerun checks only for changed inputs, a new failure or a concrete unresolved concern.
- Deliver editable source, bibliography, needed figures and a checklist (source revision, actual checks, unresolved evidence). Include exports only when actually produced. Record real AI assistance and review scope.
- Hash consistency, scientific assessment, format checks, visual inspection and human approval are separate; none substitutes for another. Inspect every page of a final PDF ([how](references/tools.md#exact-file-verification)); unavailable Word/Inara rendering stays unverified. The native Word finalizer applies only to the two IEEE magazine venues with retained official templates.
- Without genuine confirmation, leave author identity/consent, eligibility, ethics, rights, funding/conflicts and data/code availability pending. ORCID data is not consent.
- Never publish, upload, submit or contact others without separate authorization. Stop after the requested draft (with its one post-review revision), revision, review or bundle; start no further improvement cycle.
