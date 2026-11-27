# Standalone research and document tools

Resolve this skill's directory from the loaded `SKILL.md`. Scripts find assets relative to themselves, so the installed package can be copied elsewhere. Keep user research and output outside the installed skill.

## Runtime and source work

- Research and write with ordinary agent search, repository, browser and file tools. Retain the inspected revision and original source/document bytes. Do not execute the input project unless authorized. Canonical authored Markdown is enough; no research-response schema wraps the article.
- Python version, interpreter, dependencies and per-task prerequisites (Pandoc, Word automation): [runtime.md](runtime.md#locate-and-use-the-installed-skill). Inspect actual dependencies before installing anything; a missing component is a reported preparation issue.
- Word for Mac: quit Word before export; the tools stage exact copies in Word's sandbox container and never save the document. A statistic Word for Mac cannot provide is reported as a failed native measurement, never estimated.

Run a script's `--help` before using unfamiliar options. Replace `$python`, `$skillDirectory`, `$manuscript` and `$newOutputDirectory` below with the resolved executable and absolute paths. Do not use common system environment names for task variables.

## Manuscript preflight and official export

`scripts/export_manuscript.py` prepares and exports a completed Markdown manuscript deterministically; it writes no scientific prose.

```powershell
& $python "$skillDirectory/scripts/export_manuscript.py" preflight --manuscript $manuscript --venue ieee-software
& $python "$skillDirectory/scripts/export_manuscript.py" export --manuscript $manuscript --venue ieee-software --output-dir $newOutputDirectory
```

| Venue identifier | Template/input | Export |
| --- | --- | --- |
| `ieee-software`, `ieee-security-privacy` | Retained official DOCX | DOCX and native Word PDF |
| `joss` | Authored YAML Markdown, `paper.bib`, local figures | Submission source package |

- The retained template must match the recorded publisher SHA-256; templates are never fetched or replaced by a generic substitute. IEEE Access and JORS are not offered because they always charge an article processing charge.
- Use each venue's own template. Word `preflight` reads the manuscript and checks the template without launching Word.
- Word `export` needs a new output directory. It retains exact Markdown bytes, produces DOCX, renders that saved DOCX through hidden read-only Word to PDF, measures native counts, and retains conversion/format/provenance reports and all-page PNGs.
- A failed export keeps its directory for diagnosis; never overwrite it or reuse an earlier export as a success.

**`--docx-only`** (editable DOCX without Word; not accepted for JOSS): add it explicitly to `export`. Same official-template converter; retains source, DOCX, conversion receipts, read-only preflight report, provenance and manifest. It never attempts native Word/PDF or silently recovers from a failed native export. Exit 0: manuscript preflight passed. Exit 1: DOCX and reports created, manuscript checks failed. Exit 2: input/conversion error. `content_format_passed` and `submission_ready` stay false; native measurement and page review stay pending.

**Images.** Export retains local relative images recognized by the converter's Markdown reader, reference-style images included. The source root is the manuscript directory, or the one existing absolute `--resource-dir`. Files are copied byte for byte to the same relative paths beside the retained `manuscript.md`; the converter reads the copies and the manifest records their hashes. Originals and Markdown bytes stay unchanged. Rejected: missing files, symlinks, absolute or escaping paths, external image URLs, Windows-incompatible filenames, case-insensitive file/directory collisions, collisions with generated output paths.

**Moving an export.** Keep the whole directory to re-export its retained manuscript and images with the same converter and required official template; the original resource directory is no longer needed. Raw HTML/TeX assets are not collected; templates, Pandoc, Word and fonts are not redistributed (separate prerequisites). A later bundle still copies only selected files, so select each intended figure.

**Conversion failures.** Conversion warnings stop the export, including Pandoc replacing a missing figure with its description. Embedded common raster images are checked for readable structure. Repair the reported input in a new revision; a retained partial DOCX is a failed output. These checks prove neither visual fidelity nor every vector format: inspect all final pages ([exact-file verification](#exact-file-verification)).

**Figure size.** Body figures shrink proportionally to the publisher's column width and printable page height; smaller ones are never enlarged. Bytes are kept, but labels may become unreadable: check final size during page review.

**Options.**

- `--profile ABSOLUTE_FILE` (Word venues): the multi-author profile or generated `authors.json` from [`submission_support.py authors`](researcher-convenience.md#reuse-author-and-coauthor-facts). Missing author facts are reported, checking identity fields within each author's own byline block and order. Both IEEE magazines require biographies. The manuscript must already carry the author blocks; export never inserts them from metadata. Field presence proves neither accuracy nor consent.
- `--pandoc ABSOLUTE_EXECUTABLE`: an existing Pandoc binary; otherwise an available installation is resolved. Diagnostics and conversion verify the actual Pandoc identity.
- If Word, Pandoc or required assets are unavailable, never silently replace the publisher-template export with a generic alternative.

**Results.** Exit status separates passed content-format checks, a completed report with failed checks, and input/conversion errors; read `--help` and the actual result. Failed checks with repair guidance appear in `fixes` with `how_to_fix` and an accepted Markdown `example` (syntax only, never facts). A passing format report is not scientific approval; `submission_ready: false` can remain while author information, declarations, page approval or current guidance checks are pending.

[quickstart.md](quickstart.md) walks through one preflight-and-export cycle from [the IEEE Software skeleton](../assets/examples/ieee-software-skeleton.md). For people, `scripts/think_tank.py` (`doctor`, `new`, `check`, `export`) wraps these tools with relative paths, automatic new output folders and plain-language summaries; its `--json` output is the same report.

## JOSS source export

Read [JOSS guidance](joss.md) first: it holds the `paper.md` YAML and section rules, citation and `nocite` checks, image collection limits and the no-Word/no-Inara scope. `--profile` and `--template` are unsupported for JOSS.

```powershell
& $python "$skillDirectory/scripts/export_manuscript.py" preflight --manuscript $manuscript --venue joss
& $python "$skillDirectory/scripts/export_manuscript.py" export --manuscript $manuscript --venue joss --bibliography $bibliography --output-dir $newOutputDirectory
```

- The bibliography defaults to sibling `paper.bib`; `--bibliography ABSOLUTE_FILE` selects a BibTeX file preserved as `paper.bib`. `--resource-dir ABSOLUTE_DIRECTORY` resolves local images from another retained source directory.
- Checked inputs (`paper.md`, `paper.bib`, referenced figures) are preserved with hashes in the new output directory.
- [BibTeX/RIS/CSL-JSON import](researcher-convenience.md#import-bibtex-ris-or-csl-json-into-the-existing-metadata-workflow) is a separate metadata tool; RIS is not a JOSS submission bibliography.

**`%` comments.** BibTeX import and JOSS source checks accept `%` line comments at field/value syntax boundaries, following [Pandoc's reader behavior](https://github.com/jgm/pandoc/blob/3.9/src/Text/Pandoc/Citeproc/BibTeX.hs#L878-L907); this does not promise universal or classical BibTeX support. Inside braced or quoted values, the importer preserves `%`, `\%` and URL percent escapes. Imported entries keep `source.raw`; JOSS export keeps the original `paper.bib` bytes. A later [Pandoc CSL conversion interprets LaTeX in text fields](https://pandoc.org/MANUAL.html#specifying-bibliographic-data), so an unescaped `%` there can hide the following text; source preservation does not establish rendered output.

**Metrics.** `metrics.citation_keys` is the sorted unique body identifiers; `metrics.reference_count` is the total bibliography record count, not a rendered-bibliography count.

**Scope.** No DOCX or PDF is produced. Report completed source checks separately from unperformed rendering and visual inspection. Bundle roles: [JOSS bundle](researcher-convenience.md#assemble-an-explicit-submission-file-bundle). `finalize_submission.py` applies to native Word reports and rejects JOSS; never create a synthetic Word/PDF report for a source package.

## Host-prepared CS manuscripts

- Editable DOCX: [EMSE Research Articles](emse.md), [SPE](spe.md), [SCP OSP](scico-osp.md), [JSS](jsys.md), [IST](ist.md).
- Initial-review PDF in the official style: [JMLR MLOSS](jmlr-mloss.md) (cover letter kept separate), [ASE](ase.md), [JStatSoft](jstatsoft.md).
- Before converting, check the Markdown against the venue's countable rules: `python scripts/think_tank.py check paper.md --venue ist` (abstract and keyword limits, structured abstract, highlights, word budget, required statement sections). Rules not countable from Markdown (templates, page limits, licences, declarations) are listed as pending.
- These routes use neither the journal-specific `export_manuscript.py` converters nor the native Word finalizer.

After successful host conversion and inspection of the output against the authored inputs, record exact versions with `record-conversion`, listing all actual authored inputs: the evidence-bound manuscript, any separate LaTeX source, bibliography and figures. For a Markdown manuscript with a host-prepared TeX source:

```sh
python /path/to/think-tank/scripts/submission_support.py record-conversion --root /work/article --inputs paper.md paper.tex paper.bib --file paper.pdf --output-dir /work/article/conversion-1
```

For EMSE, select the DOCX with `--file paper.docx`. Include figure files in `--inputs` when used. The command writes `conversion.json` and a manifest to a new directory; it neither copies nor converts files. It records a host-declared relationship, not proof that a build occurred or that every dependency was listed. Never record an old output against edited sources: regenerate first. A matching snapshot does not replace content or page review.

In the `bundle` plan, set `venue_id: emse` or `jmlr-mloss`, keep the evidence-bound `manuscript`, and select the output as `editable_docx` or `review_pdf`, `conversion-1/conversion.json` as `conversion_record`, and every recorded input at the same root-relative path: `bibliography`, `latex_source`, `figure`, or `conversion_input` for other authored dependencies.

- The bundle requires exactly one record per prepared output, checks its input/output hashes against the selected files, and flags selected manuscript, bibliography, LaTeX and figure inputs missing from the record.
- Missing records, unselected inputs and changed bytes become explicit gaps; a supplied `draft` becomes `incomplete`.
- After an input changes, rebuild the output, make a new record and bundle the new files together. Existing records stay unchanged.
- It checks the required output role and extension; a nonexistent selected file is an input error. It does not inspect layout, run TeX, verify the declared conversion or certify eligibility.
- Exit 0 means copies and reports were created, even if the checklist records stale output. Always read `missing_evidence` and `draft_status`; `submission_ready` stays false.

## Public ORCID facts

Read `scripts/lookup_orcid.py --help`, then give an ORCID identifier or accepted public profile URL. The helper requests public ORCID records and normalizes available names, affiliations, emails and biography material. It does not access private account data or establish consent. Keep returned provenance and missing fields; never infer an email, current role, degree or approval from absence. Multiple public affiliations or contacts need the author's selection for the paper.

## Research and submission files

[researcher-convenience.md](researcher-convenience.md) covers the environment diagnostic, status/continuation snapshots, literature cards, evidence links, `research_workspace.py impact`, comparisons, editorial reports, coauthor/anonymous drafts, reviewer responses, submission bundles and `finalize_submission.py check` (Word exports only; separate from uploading or acceptance). Apply the selected venue's policy before preparing responses (JOSS: [no AI-written editor/reviewer conversations](joss.md#limits-and-human-decisions)).

## Exact-file verification

Retained templates and acquisition metadata are in `assets/templates/`; verify the selected asset hash against its provenance. JOSS includes the MIT-licensed Inara source example with its license notice. A template proves the bytes used, not current rules, proprietary font availability or acceptance.

After export, inspect every PNG of the exact final PDF at readable original size: source-derived title and author layout, column order, technical notation, table captions/continuations, references, glyphs, clipping, page furniture and final-page balance. Native bounds and glyph checks cannot replace this. Record the PDF and ordered page-image hashes, reviewer and limitations separately from human author approval.

When correcting layout or a local factual issue, keep the earlier output and review binding; re-render and inspect all pages of the new output. An older review never covers changed bytes. Deliver content recommendation, measured format results, page observations, missing human items and actual submission status as separate facts.
