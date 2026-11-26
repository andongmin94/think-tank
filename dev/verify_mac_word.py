"""Verify the macOS Microsoft Word route on a real Mac.

CI runners have no Microsoft Word, so the AppleScript renderer can only be
proven on a Mac with Word installed. Quit Word, then run from the repository:

    python3 dev/verify_mac_word.py

It exports a filled copy of the IEEE Software skeleton through native Word
into a new temporary folder, then prints a summary and writes
verify-mac-word.json next to the outputs. Nothing in the repository changes.
"""
import json
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=600, check=False)


def filled_manuscript() -> str:
    skeleton = (REPO / "assets/examples/ieee-software-skeleton.md").read_text(encoding="utf-8")
    skeleton = skeleton.replace("<actual tool and version>", "a verification script").replace(
        "<affected sections>", "the test sections")
    return re.sub(r"<([^<>]+)>", lambda match: match[1].replace("e.g.", "for example"), skeleton)


def main() -> int:
    if sys.platform != "darwin":
        print("Run this on macOS with Microsoft Word installed.")
        return 2
    work = Path(tempfile.mkdtemp(prefix="think-tank-mac-word-"))
    summary = {"python": platform.python_version(), "macos": platform.mac_ver()[0], "work": str(work)}

    env = run(str(SCRIPTS / "environment_check.py"), "--output-dir", str(work / "environment"))
    report = work / "environment" / "environment.json"
    environment = json.loads(report.read_text(encoding="utf-8")) if report.is_file() else {}
    summary["environment_exit"] = env.returncode
    summary["word"] = environment.get("word")
    summary["osascript"] = environment.get("osascript")
    summary["prerequisites_detected"] = environment.get("native_export_prerequisites_detected")

    manuscript = work / "article.md"
    manuscript.write_text(filled_manuscript(), encoding="utf-8")
    export = run(str(SCRIPTS / "export_manuscript.py"), "export", "--manuscript", str(manuscript),
                 "--venue", "ieee-software", "--output-dir", str(work / "export"))
    summary["export_exit"] = export.returncode
    summary["export_stderr"] = export.stderr[-2000:]
    out = work / "export"
    pdfs = sorted(out.glob("*.pdf")) if out.is_dir() else []
    summary["pdf"] = str(pdfs[0]) if pdfs else None
    receipts = out / "conversion-receipts.json"
    if receipts.is_file():
        rendering = json.loads(receipts.read_text(encoding="utf-8")).get("pdf", {}).get("word_rendering", {})
        summary["pdf_engine"] = rendering.get("engine")
        summary["pdf_word_details"] = rendering.get("word")
    format_report = out / "format-report.json"
    if format_report.is_file():
        data = json.loads(format_report.read_text(encoding="utf-8"))
        native = next((item for item in data.get("items", []) if item["id"] == "native_word"), None)
        summary["native_word_item"] = native
        summary["native_metrics"] = data.get("metrics", {}).get("native_word")

    (work / "verify-mac-word.json").write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=True))
    rendered = bool(summary.get("pdf"))
    measured = bool(summary.get("native_metrics"))
    print(f"\nPDF rendered: {rendered}  Native counts measured: {measured}")
    print(f"Open the PDF and check every page: {summary.get('pdf')}")
    return 0 if rendered and measured else 1


if __name__ == "__main__":
    raise SystemExit(main())
