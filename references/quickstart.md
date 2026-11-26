# Quickstart: check and export one manuscript

This walks a person (or an agent) through the file tools once, from a fresh install to an editable IEEE Software DOCX. It does not write the article; the host agent does that from real evidence.

## 1. Prepare the local Python

Use the local Python 3.11+ on `PATH` (`python`; on macOS usually `python3`). From the installed skill directory:

```sh
python -m pip install -r requirements.txt
```

## 2. Check the environment (optional)

```sh
python scripts/environment_check.py --output-dir /absolute/new/env-report
```

Exit 0 means native Word export is available on this machine (Windows with Word, or macOS with Word). Exit 1 only means native Word/PDF is unavailable; DOCX export, checks and bundles still work.

## 3. Start from the skeleton

Copy [`assets/examples/ieee-software-skeleton.md`](../assets/examples/ieee-software-skeleton.md) outside the skill directory and replace every `<...>` slot with real content. Leave a slot unfilled only as a pending item in the checklist, never as invented text.

## 4. Preflight and read the fixes

```sh
python scripts/export_manuscript.py preflight --manuscript /absolute/article.md --venue ieee-software
```

Exit 0 means the structural checks passed. Exit 1 prints a report: `blockers` says what failed, and `fixes` gives each failed check a `how_to_fix` and an `example` in Markdown the checker accepts. Repair the manuscript and run preflight again.

## 5. Export

```sh
python scripts/export_manuscript.py export --manuscript /absolute/article.md --venue ieee-software --output-dir /absolute/new/export --docx-only
```

`--docx-only` produces the official-template DOCX without Microsoft Word. Without it, the tool also renders a PDF through the installed Word (Windows or macOS) and measures native counts. Inspect every PDF page yourself; a passing report is not scientific approval or author consent.

## Where to go next

- Full tool contracts: [tools.md](tools.md)
- Venue rules: [ieee-software.md](ieee-software.md) and the other venue guides
- Host installation: [runtime.md](runtime.md)
