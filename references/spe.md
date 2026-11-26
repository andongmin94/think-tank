# Software: Practice and Experience — Research Article

Choose `spe` for a paper about practical experience with software systems: designing, building, operating or evolving real software, including an open-source system and the lessons it taught. The editors reject many submissions as out of scope without review, so map the contribution to a topic in the journal's aims and scope before drafting.

## Official sources — checked 2026-11-26

- [Author guidelines](https://onlinelibrary.wiley.com/page/journal/1097024x/homepage/forauthors.html), read directly in a browser (automated fetches are refused).

Recheck the aims and scope page and the article category before the actual submission.

## Initial manuscript

- **Free Format** submission: one editable file with the abstract, introduction, methods, results and conclusions; references may be in any style for review. Word (`.doc`/`.docx`) or LaTeX are accepted; LaTeX users upload a single PDF as the main document for review and the TeX sources at revision.
- Abstract structured (introduction, methods, results, conclusion) or unstructured; up to seven keywords; a short informative title without abbreviations.
- Research Articles require the journal's **Submission Topic and Scope Form**. A cover letter naming the matching aims-and-scope topic is encouraged.
- Title page with every co-author's affiliation and email, an ORCID for the submitting author, a **data availability statement** and a **conflict of interest disclosure**.
- An extended conference paper needs significant additions and a separate document explaining the differences.
- No journal-specific AI-use policy was found on the page read; record actual assistance and confirm Wiley's current policy before submission.

## Fees

Publishing is free on the subscription route: without the open access option the corresponding author signs a copyright transfer agreement. Open access is optional and paid.

## Prepare files

Write the Markdown manuscript from evidence, convert it to an editable DOCX (`pandoc paper.md -o paper.docx`) or compile LaTeX to a review PDF, and inspect it. Bundle with `submission_support.py bundle`: the Markdown as `manuscript`, the DOCX as `editable_docx`, and the recorded `conversion.json` as `conversion_record`. Keep the scope form, cover letter, author facts and declarations as pending items unless the authors supply them.
