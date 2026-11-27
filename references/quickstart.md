# Quickstart: check and export one manuscript

This walks a person through the file tools once, from a fresh install to an editable IEEE Software DOCX. It does not write the article; the host agent does that from real evidence. Every command runs from the installed skill directory; relative paths are fine.

## 1. Prepare the local Python

Use the local Python 3.11+ on `PATH` (`python`; on macOS usually `python3`).

```sh
python -m pip install -r requirements.txt
python scripts/think_tank.py doctor
```

`doctor` says whether this computer can check manuscripts, export Word (DOCX) and render a PDF through Microsoft Word (Windows or macOS). Without Word, everything except the PDF still works.

## 2. Start from the skeleton

```sh
python scripts/think_tank.py new article.md
```

Replace every `<...>` slot with real content. An unfilled slot is reported by `check`; leave missing facts as pending in the checklist, never as invented text.

## 3. Check and fix

```sh
python scripts/think_tank.py check article.md
```

The summary separates **Fix these** (each with how to fix and a Markdown example the checker accepts) from **Needs a person** (author identity, photo, declarations: confirmations, not format errors). Exit 0 means the format checks passed; 1 means something to fix; 2 means the command could not run.

## 4. Export

```sh
python scripts/think_tank.py export article.md             # DOCX, plus PDF through Microsoft Word
python scripts/think_tank.py export article.md --docx-only # DOCX without Word
```

A new folder `article-ieee-software-<date>-<time>` is created next to the manuscript. Inspect every PDF page yourself; a passing report is not scientific approval or author consent.

## Options

- `--venue ieee-security-privacy` selects another venue. `check` works for all eleven venues (add `--repo`, `--pdf` or `--tex` to also check the licence, replication script, page limit and LaTeX template); `export` covers the two IEEE magazines and JOSS, and the other venues' guides describe how to prepare their DOCX or PDF.
- `--json` prints the full machine-readable report.
- `--lang ko|en` overrides the message language (default: system locale, or `THINK_TANK_LANG`).

The underlying tools (`export_manuscript.py`, `environment_check.py`) keep their exact contracts for agents; see [tools.md](tools.md). Venue rules are in [ieee-software.md](ieee-software.md) and the other venue guides; host installation is in [runtime.md](runtime.md).
