# Journal of Statistical Software — Article or Code Snippet

Choose `jstatsoft` for **statistical software**: an article describing a comprehensive open-source implementation, compared with other open-source implementations and demonstrated on a non-trivial case study. Methodological innovations without such software, and software without an article, are out of scope.

## Official sources — checked 2026-11-26

- [About](https://www.jstatsoft.org/about), [Information for authors](https://www.jstatsoft.org/authors), [Mission](https://www.jstatsoft.org/mission), [Style guide](https://www.jstatsoft.org/style), [Submission guide](https://www.jstatsoft.org/guides/submission).

## Initial manuscript

- Article types: articles and **code snippets** for smaller code projects (special issues and reviews are by invitation).
- The code must be licensed under **GPL-2, GPL-3 or a GPL-compatible licence**; other licences are not considered. Any high-level language; packaging, help files and installation are expected for package systems. Availability in a standard repository (CRAN, PyPI, Bioconductor) is preferred.
- Written in **LaTeX with the JSS style** (`\documentclass[article]{jss}`, or `codesnippet`), using pdfLaTeX, and submitted as PDF; follow the style guide's `\proglang`, `\pkg` and `\code` markup. Templates are linked from the style guide.
- **Replication materials are mandatory**: a standalone, commented script reproducing every result (about one hour on a normal PC, otherwise a quicker companion script), data where possible, fixed random seeds, and preferably an output log. Reviewers check reproducibility before acceptance.
- No page limit; manuscripts over 30 pages take longer to review. Two reviewers assess both the article and the software.
- No AI-use or competing-interest policy was found on the pages read; record actual assistance and confirm with the editors.

## Fees

**No author fees and no subscription fees**; articles are open access under CC BY.

## Prepare files

Compile the JSS-style LaTeX, run the replication script from a clean environment and record its output. Bundle the source as `manuscript` (plus `latex_source`), the compiled PDF as `review_pdf`, the replication script and data as `supplement`, and the `conversion.json` as `conversion_record`.
