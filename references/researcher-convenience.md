# Researcher convenience tools

Use these tools only for the requested task; check each one's `--help`. Python 3.11+ on `PATH` ([runtime](tools.md#runtime-and-source-work)). For every tool:

- Inputs are explicit local files; no model or submission portal is called. Output goes to a new directory outside the installed skill; inputs stay unchanged.
- Checks cover files, hashes and quotes only: no scientific evidence, certified truth, quality or novelty, author approval or acceptance.
- Missing, changed or mismatched items are reported and stay pending. Never repair, substitute or manufacture inputs or records to pass.
- Reports are dated snapshots: after changes make a new one, never edit the old. Old reviews and scores stay bound to their reviewed hashes and never cover changed bytes.
- Keep author profiles private and outside the distributed package.

## Continue research on another PC or conversation

`scripts/research_workspace.py checkpoint --root ROOT --state STATE_JSON --output-dir NEW` captures listed files, decisions and next steps portably. State: `project`, `question`, `decisions`, `next_steps`, `constraints`, `historical_counts`, root-relative `files`. Historical counters are supplied facts: never invent model totals or treat a saved limit as authorization for new calls. Select only needed material; never credentials or an entire private account directory.

`resume --checkpoint CHECKPOINT_DIRECTORY` verifies captured files and reads the context; no research, no state rewrite. To move PCs, copy the whole folder (paths stay relative) and give the agent its path. Missing or changed material never permits a substitute source or restarted study. Still read the relevant actual sources, not only the summary.

`scripts/environment_check.py --output-dir NEW [--pandoc EXISTING_ABSOLUTE_EXECUTABLE]` reports Python, document package versions, a Pandoc probe, Word automation prerequisites (Windows PowerShell and Word registration, or macOS osascript and the Word application bundle) and both retained template hashes. Run it from the installed skill.

- Exit 0: prerequisites detected. Exit 1: missing or incompatible prerequisites recorded. Exit 2: invalid input or report failure.
- Installs nothing, launches no Word, connects no accounts, inspects no credentials. Registration proves neither licensing nor native rendering.
- A Pandoc executable can replace optional `pypandoc_binary`; final export still needs page and font checks.

## See current research status

`research_workspace.py status --root ROOT --state STATE_JSON --output-dir NEW` writes a Markdown summary and full JSON inventory. State: `project`, `question`, root-relative `current_manuscript`, `artifacts`, `remaining_tasks`, verbatim `historical_counts`. Artifact: distinct `id`, `role`, root-relative `path`, expected `sha256`, optional `manuscript_sha256` of the manuscript it covers. Take bindings from actual records or manifests; never attach today's manuscript hash to make an old review current.

States: `current` (bytes and binding match), `stale` (other manuscript version), `changed`, `missing`, `unbound` (no manuscript association; valid for a source). They describe files and versions only.

## Retain reusable primary-literature reading cards

`scripts/literature_cards.py prepare --root ROOT --cards CARDS_JSON --output-dir NEW` takes `{cards: [...]}`. Card: `id`, `title`, `url`, `question`, `method`, `results`, `limitations`, `relevance`, `reading_scope`, `read_sections`, `unread_sections`, `source`, `witnesses`.

- Fill fields from the actual reading, unknowns included. `reading_scope`: `full_body`, `selected_sections`, `abstract_only` or `metadata_only`. State what was and was not read; metadata and abstracts do not substitute for the body.
- `source`: root-relative `path` and `sha256` of the retained original, plus `text_path` and `text_sha256` of the text checked (a text source may reuse both).
- Witness: `start_line`, `end_line`, exact complete-line `quote`, optional `pages` (not checked against PDF pages).

Interpretation, identity and reading completeness are never certified. Exit 1: binding issues recorded. Reuse cards to compare methods, assumptions and limits; reopen the body when a new question needs more reading.

## Link manuscript claims to actual evidence

`research_workspace.py evidence --root ROOT --ledger LEDGER_JSON --output-dir NEW` records exact source witnesses. Ledger: root-relative `manuscript`, `claims`. Claim: `id`, `claim`, `kind`, literal `manuscript_quote`, `sources`. Source: root-relative `path`, `start_line`, `end_line`, literal `quote`, optional `sha256`.

`kind` is the claim's actual basis: `source_declared`, `observed_static`, `derived`, `proposed`, `measured`, or `author_stated` ([author interview](author-interview.md); the interview record is the source). A proposed policy is not an evaluated fix; `measured` needs real retained measurements.

- The report records the manuscript snapshot hash used to locate quotations.
- A verified quote/hash only proves the witness is locatable; judge support yourself.
- Put lengthy details in the companion; pinpoint consequential evidence in the article.
- Repeated witnesses share one snapshot; all selected sources (initially missing ones too) are rechecked before writing. A change during inspection is an error: finish the intended version, then report anew.

## Compare revisions and inspect manuscript consistency

`research_workspace.py impact --root ROOT --evidence PRIOR_EVIDENCE_JSON --output-dir NEW` compares a retained generated `evidence.json` with current source bytes and manuscript quotations. Options: `--manuscript ROOT_RELATIVE_MD` (revised manuscript); `--focus FOCUS_JSON` with `{question, claim_ids: [...], source_paths: [...]}` (explicit new-question reading choices). Reports: changed/missing sources with all dependent claims (even if the old quote remains), absent manuscript quotations, previously unverified bindings, and unchanged literal bindings eligible for reuse.

- Revisit affected claims; reuse unchanged witnesses without rereading unrelated bodies. An unchanged binding proves neither claim truth nor an answered new question.
- Focus selections are supplied judgment, not semantic relevance, and need relevant reading even when hashes match.
- No cache database, counter reset or study. Exit 0: snapshot prepared, even when it finds review work.

`research_workspace.py compare --before BEFORE_MD --after AFTER_MD --output-dir NEW` keeps an exact diff and structural summary. It does not infer improvement or recompute old scores. Use it to explain actual changes and open issues to the author.

`scripts/editorial_checks.py check --manuscript MANUSCRIPT_MD --output-dir NEW` checks citation/reference structure, repeated identifiers, table/figure callouts and selected editorial consistency. Optional `--references-json FILE`: metadata records (`id`, `title`, `doi`, `authors`, `year`, `url`), treated as supplied, not verified. Resolve uncertain DOI/title/author details against primary records and retain those retrievals separately. Offline: no publisher request; cannot catch every retraction or validate identity.

- Separate definite structural findings from heuristics (acronym first use, naming, caption matching, possible duplicate titles), which need contextual review; code, symbols and official names can be legitimate exceptions.
- Never auto-edit the manuscript or block delivery on a heuristic.
- Native format and exact-file page checks stay with the official exporter.

### Import BibTeX, RIS or CSL-JSON into the existing metadata workflow

`scripts/import_references.py --input BIB_RIS_OR_CSL_JSON --output-dir NEW` reads UTF-8 and writes `references.json`, `import-report.json`, `import-report.md`. Extension picks the format: `.bib`/`.bibtex`, `.ris`, `.json` (CSL); else `--format bibtex|ris|csl-json`. Use absolute paths. BibTeX uses `pyparsing` (`requirements.txt`); CSL-JSON the standard JSON parser. No network lookup, completion, deduplication or manuscript edit.

```sh
python scripts/import_references.py --input /work/sources.bib --output-dir /work/imported
python scripts/editorial_checks.py check --manuscript /work/article.md --references-json /work/imported/references.json --output-dir /work/editorial
```

Output is the list `--references-json` accepts, with positive integer `id`s in input order from 1. If manuscript numbering differs, pass `--reference-ids` in input order: one unique positive integer per record, else rejected before output. Findings use these numbers. Confirm the mapping yourself; it is never inferred from titles, DOIs or keys. First record → `[2]`, second → `[1]`:

```sh
python scripts/import_references.py --input /work/sources.bib --reference-ids 2 1 --output-dir /work/imported
```

Records keep `source.raw` (CSL reserialized: fields kept, whitespace not), `source.format`, and any BibTeX key, RIS `ID` or CSL `id` in `source.key`. Duplicate keys and incomplete or empty records are kept separately. The input SHA-256 is in the report.

Only supplied `title`, `authors`, `year`, `doi`, `url` are mapped; nothing (century, current year, missing fact) is inferred. Conflicting repeated fields: first value mapped, conflict reported.

- **BibTeX:** braced/quoted, nested-brace and multiline values, `#` concatenation, string definitions present before use. TeX markup and the original `author` string are not rewritten. Undefined strings: reported, field unmapped. Years other than one four-digit year: kept in the record with a warning.
- **RIS:** `TI`/`T1`, ordered `AU`/`A1`, `PY`/`Y1`, `DO`, `UR`; other tags stay in `source.raw`. `2024/10/02/` gives `2024`; other dates stay in the record with a warning.
- **CSL-JSON:** array of objects, incomplete ones included. Maps `title`, `DOI`, `URL` strings. Ordered `author`: `literal`, or `given`, `dropping-particle`, `non-dropping-particle`, `family`, `suffix` joined in that order with spaces; missing parts not filled (literal comparison form, not CSL rendering). One `issued.date-parts` date gives its four-digit year; month/day stay in the record. Ranges, free-text and `circa` dates: unmapped, year warning. Missing/null fields stay missing; unsupported values stay in the object with `unmapped_csl_metadata` suggestions. Source `id` never selects a reference number.

```json
[{"id":"source-key","title":"Supplied title","author":[{"given":"Min","family":"Kim"},{"literal":"Research Group"}],"issued":{"date-parts":[[2024,10,2]]}}]
```

```sh
python scripts/import_references.py --input /work/sources.json --format csl-json --reference-ids 3 --output-dir /work/imported-csl
```

Reports use the existing `structural_findings` and `manual_review_suggestions` lists (`code`, `reference_id` when applicable, `detail`).

- Missing metadata, unmapped years/strings and numbering checks are advisory; a malformed DOI is kept and reported as `malformed_metadata_doi`.
- Exit 0: prepared, findings included. Exit 2: invalid input or output failure.
- Rejected before output: unparseable BibTeX/JSON, non-object CSL entries, RIS records without `ER`.
- No verification of publication identity, author names or DOI resolution. Review with the later editorial report.

BibTeX syntax errors report where parsing stopped (may follow the missing token) once an entry or field has started: one-based line and column in characters (tab = 1, UTF-8 BOM excluded). Import, JOSS preflight and JOSS source export share this validation.

## Reuse author and coauthor facts

Save an explicit profile outside the skill; supply it per paper. `scripts/submission_support.py authors --profile PROFILE_JSON --manuscript MANUSCRIPT_MD --output-dir NEW` validates order and facts and writes a new Markdown author block/biographies plus a missing-information report. Profile: `authors` (`id`, `author`, `contributions`), `order`, optional `corresponding_author` ID, `funding`, `conflicts`. `author` uses the exporter fields: names, affiliation, department, city/country, email, ORCID, biography, factual `biography_details`.

- Gather facts with the [ORCID helper](tools.md#public-orcid-facts); the author picks the submission affiliation/contact. No end date does not prove a current appointment.
- Contributions are supplied text, not a certified taxonomy or coauthor agreement.
- Order, corresponding author, funding/conflicts, rights and final approval need genuine confirmation per paper. Never insert unconfirmed choices or treat a field's presence as consent.

Wrap the byline in `<!-- think-tank:authors:start -->` / `<!-- think-tank:authors:end -->`. Ambiguous unmarked material before Abstract is refused; inspect it and mark only the known author block in a new copy. Never put unrelated prose in the slot. Reruns replace only the slot and the biography section.

Export with the generated `authors.json` via `export_manuscript.py ... --profile AUTHORS_JSON` ([options](tools.md#manuscript-preflight-and-official-export)). Both share one multi-author contract and report every author's missing fields, biography details included; the exporter never rewrites the byline. Author material changes bytes: keep the scientific version/review binding; recheck output and venue word counts. A saved profile enters a checkpoint or bundle only when explicitly selected.

For relative media such as `![Figure](figure.png)`, pass the original directory (one existing absolute path) as `--resource-dir` when exporting the prepared copy from a new folder; preparation leaves media and links unchanged. For `/work/source/article.md` with `/work/source/figure.png`:

```sh
python scripts/export_manuscript.py export --manuscript /work/prepared/manuscript.md --profile /work/prepared/authors.json --resource-dir /work/source --venue ieee-software --output-dir /work/exported
```

Image copying, moved re-exports and rejected inputs: [Word export image requirements](tools.md#manuscript-preflight-and-official-export).

## Prepare an anonymous draft only when appropriate

`authors ... --anonymous` also writes a separate draft without the author block and biographies. Use only when requested or the verified article category requires anonymity. Read residual-identifier findings; inspect self-identifying prose, acknowledgments, citations, source URLs, supplements and file names. Targeted text removal only: not anonymization, no DOCX/PDF metadata scrubbing.

`submission_support.py metadata --file ACTUAL_DOCX_OR_PDF [--profile PROFILE_JSON] --output-dir NEW` reports possible supplied-identity matches in native metadata, plus comments/tracked-change residue for DOCX (PDF: exposed metadata fields only). It neither removes nor rules out identifiers in content, attachments or images. After an anonymous export, inspect this report and the pages before calling it fit for anonymous review; clean metadata is not anonymity approval.

## Respond to actual reviewer comments

`submission_support.py responses --comments COMMENTS_JSON --before BEFORE_MD --after AFTER_MD --output-dir NEW` prepares a response letter and anchor report. `comments` entry: `id`, actual `comment`, `status` (`pending`, `addressed`, `not_changed`), honest `response`, `changes` with exact revised-text `quote`s and optional section labels.

- It checks only that quoted revised text exists, not reviewer satisfaction, soundness or executed work. `not_changed` needs an explanation.
- Check summary counts (pending, incomplete responses, missing anchors). `response_draft_complete` = preparation checks passed, never scientific resolution. No anchors: `all_change_anchors_present` is null, not success. Exit 0: report prepared, possibly with unfinished work.
- Draft from the actual change and evidence; keep disagreements and open requests explicit. Never manufacture reviewer comments, completed experiments or acknowledgments.
- A response letter is not a new full assessment and does not authorize sending.

## Assemble an explicit submission-file bundle

`submission_support.py bundle --root ROOT --plan PLAN_JSON --output-dir NEW` copies only selected root-relative files, records hashes and writes a checklist. Plan: `venue_id`, `title`, `files` (`role`, `path`), optional `cover_letter.text`, supplied `declarations`. Select the manuscript and required photographs, figures or companion; read the pending/required checklist (a successful copy can leave it incomplete). Editorial approval is never inferred.

- **EMSE, JMLR MLOSS:** after generating and inspecting the output, follow [conversion recording](tools.md#host-prepared-cs-manuscripts); select the `conversion_record`, output and every authored input. Stale or incomplete bindings are reported; no converter runs.
- **JOSS:** `paper.md` as `manuscript`, `paper.bib` as `bibliography`, each referenced local figure. Source bundle only; the native Word finalizer does not apply.

`declarations`: text or null for `originality`, `rights`, `author_approval`, `funding`, `conflicts`, `ai_disclosure`. Text like “Author must confirm” never checks off approval. Optional `confirmations` per declaration hold actual author records: `confirmed: true`, `confirmed_by`, timezone-aware `confirmed_at`, `declaration_sha256` of the exact UTF-8 statement, `files: [{path, sha256}, ...]` matching the report's entire `approval_files`.

- Paths are final bundle-relative: `files/<selected path>`, plus generated `cover-letter.md` when present. Its exact UTF-8 bytes and final newline count; editing it invalidates old confirmations. Select a cover-letter file or give generated text, not both.
- Record confirmations only from genuine confirmation. The helper does not authenticate them and never marks submission complete.

Draft any cover letter in the conversation from the actual article, fit and supplied facts; never add unsupported novelty, exclusive-submission, consent, rights, funding or approval declarations. The checklist is a preparation aid, not publisher certification: confirm article category, portal requirements and source rights at submission. No profile/credential directory is found or copied implicitly. Login, upload, author approval, submission and receipt need separate authorization and real outcomes.

## Reconcile final preparation records

`scripts/finalize_submission.py check --root ROOT --record RECORD_JSON --output-dir NEW` combines existing reports and chosen files into one final status (no Word, new review or submission). Record keys, exactly: `venue_id`, `manuscript`, `docx`, `pdf`, `format_report`, `visual_review`, `bundle_report`, `scientific_review`, `pages`, `confirmations`. File fields are root-relative; the three review/bundle fields may be null when absent; `pages` lists ordered PNG paths. Keep everything under one explicit root, using new copies rather than changing old reports.

In the final bundle, the evidence-bound canonical Markdown is `manuscript`, its exact verified DOCX `editable_docx`, any verified PDF `review_pdf`; they must match the record.

Rechecked:

- native/template/file bindings and the supplied all-page visual record;
- the bundle's current `approval_files`;
- each author's recorded completeness; byline and biography checks must both be present and passed;
- a scientific assessment of the exact manuscript/venue. Any recorded `docx_sha256`/`pdf_sha256` must match the exports; a manuscript-only assessment need not claim native files. An earlier review is not current merely because only author preparation changed the file hash.

Format, page inspection, administrative preparation and scientific recommendation are reported separately.

`confirmations` may hold `author_identity`, `current_guidance`, `required_files` and, for Software, `author_photo`. Each needs an actual `statement` under the declaration contract above, bound to the full final bundle scope. Each named author needs a photo selection; the person confirms identity and rights. A current-guidance record is supplied evidence: the helper neither browses the publisher nor authenticates people.

A bundle recording `not_recommended` or `conditional` stays pending even when all file, format and author records pass. Reassess the venue before a new bundle; keep the old decision.

`submission_ready` can turn true when all exact-file records pass: preparation per those records, not acceptance or submission. `actual_submission_performed` stays false. Exit 0: prepared. Exit 1: pending items. Exit 2: invalid inputs or changed-file race. Read the separate states; a genuine later confirmation resolves an old exporter `pending` flag.
