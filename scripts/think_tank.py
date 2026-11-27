"""Think Tank for people: start, check and export a manuscript in plain language.

    python scripts/think_tank.py doctor
    python scripts/think_tank.py new article.md
    python scripts/think_tank.py check article.md
    python scripts/think_tank.py export article.md --docx-only

Relative paths are fine, output folders are created for you, and results are
summarised instead of printed as JSON. Add --json for the full machine report.
The underlying export_manuscript.py and environment_check.py are unchanged.
"""
import argparse
import json
import locale
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from _publication_venues import PREPARED_MANUSCRIPTS, VENUES  # noqa: E402

SKELETONS = {"ieee-software": SKILL / "assets/examples/ieee-software-skeleton.md"}
DEFAULT_VENUE = "ieee-software"

TEXT = {
    "en": {
        "check_title": "Check: {venue} | {file}",
        "export_title": "Export: {venue} | {file}",
        "summary": "{failed} to fix, {pending} need a person, {passed} passed",
        "fix_header": "Fix these",
        "pending_header": "Needs a person (not a format error)",
        "how": "How to fix",
        "example": "Example",
        "all_good": "All format checks passed. This is not scientific approval or author consent.",
        "next_fix": "Next: fix the items above, then run check again.",
        "created": "Created {file} from the {venue} skeleton. Replace every <...> slot with real content.",
        "no_skeleton": "No skeleton for {venue} yet. Follow references/{venue}.md instead.",
        "exists": "{file} already exists; choose a new file name.",
        "outputs": "Output folder",
        "docx": "Word file (DOCX)",
        "pdf": "PDF",
        "pdf_none": "not rendered (--docx-only)",
        "inspect": "Open the PDF and check every page yourself.",
        "doctor_title": "Environment check",
        "can_check": "Check manuscripts",
        "can_docx": "Export Word (DOCX)",
        "can_pdf": "Export PDF through Microsoft Word",
        "yes": "yes",
        "no": "no",
        "missing": "Missing",
        "install": "Install the document packages: python -m pip install -r requirements.txt",
        "word_hint": "PDF export needs Microsoft Word on Windows or macOS; --docx-only works without it.",
        "error": "Error",
        "not_found": "File not found: {file}",
        "no_export": "{venue} has no official Word template here; prepare its DOCX or PDF as described in references/{venue}.md, then bundle it.",
    },
    "ko": {
        "check_title": "검사: {venue} | {file}",
        "export_title": "출력: {venue} | {file}",
        "summary": "고칠 것 {failed}개, 사람 확인 필요 {pending}개, 통과 {passed}개",
        "fix_header": "고쳐야 할 것",
        "pending_header": "사람이 확인할 것 (형식 오류 아님)",
        "how": "고치는 법",
        "example": "예시",
        "all_good": "형식 검사를 모두 통과했어요. 학술적 승인이나 저자 동의를 뜻하지는 않아요.",
        "next_fix": "다음: 위 항목을 고친 뒤 check를 다시 실행하세요.",
        "created": "{venue} 뼈대로 {file}을(를) 만들었어요. <...> 자리를 모두 실제 내용으로 바꾸세요.",
        "no_skeleton": "{venue}용 뼈대는 아직 없어요. references/{venue}.md 안내를 따르세요.",
        "exists": "{file}이(가) 이미 있어요. 새 파일 이름을 쓰세요.",
        "outputs": "출력 폴더",
        "docx": "Word 파일(DOCX)",
        "pdf": "PDF",
        "pdf_none": "만들지 않음 (--docx-only)",
        "inspect": "PDF를 열어 모든 페이지를 직접 확인하세요.",
        "doctor_title": "환경 점검",
        "can_check": "원고 검사",
        "can_docx": "Word(DOCX) 출력",
        "can_pdf": "Microsoft Word로 PDF 출력",
        "yes": "가능",
        "no": "불가",
        "missing": "없음",
        "install": "문서 패키지를 설치하세요: python -m pip install -r requirements.txt",
        "word_hint": "PDF 출력은 Windows나 macOS의 Microsoft Word가 필요해요. --docx-only는 Word 없이 돼요.",
        "error": "오류",
        "not_found": "파일을 찾을 수 없어요: {file}",
        "no_export": "{venue}는 여기서 공식 Word 템플릿으로 출력하지 않아요. references/{venue}.md 안내대로 DOCX나 PDF를 준비한 뒤 묶으세요.",
    },
}


def _language(requested: str | None) -> str:
    if requested in TEXT:
        return requested
    configured = os.environ.get("THINK_TANK_LANG", "")
    if configured in TEXT:
        return configured
    name = (locale.getlocale()[0] or os.environ.get("LANG", "")).casefold()
    return "ko" if name.startswith(("ko", "korean")) else "en"


def _console() -> None:
    # Never crash a terminal that cannot show a character; replace it instead.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass


def _path(value: str) -> Path:
    # absolute(), not resolve(): the tools still refuse symlinked paths themselves.
    return Path(value).expanduser().absolute()


def _default_output(manuscript: Path, venue: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return manuscript.parent / f"{manuscript.stem}-{venue}-{stamp}"


def _indent(text: str, prefix: str = "      ") -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def render_report(report: dict, words: dict, title: str) -> str:
    items = report.get("items") or []
    failed = [item for item in items if item.get("status") == "failed"]
    pending = [item for item in items if item.get("status") == "pending"]
    passed = [item for item in items if item.get("status") == "passed"]
    if not items:  # Reports without item rows still list their blockers.
        failed = [{"id": "check", "reason": reason} for reason in report.get("blockers", [])]
    fixes = {fix["id"]: fix for fix in report.get("fixes", [])}
    lines = [title, words["summary"].format(failed=len(failed), pending=len(pending), passed=len(passed)), ""]
    if failed:
        lines.append(f"[{words['fix_header']}]")
        for item in failed:
            lines.append(f"  [X] {item['id']}: {item['reason']}")
            fix = fixes.get(item["id"])
            if fix:
                lines.append(f"      {words['how']}: {fix['how_to_fix']}")
                if fix["example"]:
                    lines.append(f"      {words['example']}:")
                    lines.append(_indent(fix["example"], "        "))
        lines.append("")
    if pending:
        lines.append(f"[{words['pending_header']}]")
        lines.extend(f"  [ ] {item['id']}: {item['reason']}" for item in pending)
        lines.append("")
    lines.append(words["next_fix"] if failed else words["all_good"])
    return "\n".join(lines)


def _doctor(words: dict) -> int:
    from environment_check import diagnose
    result = diagnose()
    missing = [row["name"] for row in result["packages"] if row["status"] != "detected" and row.get("required_for_export")]
    pandoc = result["pandoc"]["status"] == "detected"
    word = result["word"].get("status") == "detected"
    can_docx = not missing and pandoc
    lines = [words["doctor_title"],
             f"  Python {result['python']['version']} ({result['python']['executable']})",
             f"  Pandoc: {result['pandoc'].get('version') or words['missing']}",
             f"  Microsoft Word: {result['word'].get('version') or result['word'].get('status')}",
             "",
             f"  {words['can_check']}: {words['yes'] if not missing else words['no']}",
             f"  {words['can_docx']}: {words['yes'] if can_docx else words['no']}",
             f"  {words['can_pdf']}: {words['yes'] if result['native_export_prerequisites_detected'] else words['no']}"]
    if missing:
        lines += ["", f"  {words['missing']}: {', '.join(missing)}", f"  {words['install']}"]
    if not word:
        lines += ["", f"  {words['word_hint']}"]
    print("\n".join(lines))
    return 0 if can_docx else 1


def _new(args, words: dict) -> int:
    target = _path(args.manuscript)
    skeleton = SKELETONS.get(args.venue)
    if skeleton is None:
        print(words["no_skeleton"].format(venue=args.venue), file=sys.stderr)
        return 2
    if target.exists():
        print(words["exists"].format(file=target), file=sys.stderr)
        return 2
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(skeleton, target)
    print(words["created"].format(file=target, venue=args.venue))
    return 0


def _check(args, words: dict) -> int:
    manuscript = _path(args.manuscript)
    if args.venue in PREPARED_MANUSCRIPTS:
        from _prepared_checks import validate_prepared
        report = validate_prepared(manuscript.read_text(encoding="utf-8-sig"), args.venue,
                                   repo=_path(args.repo) if args.repo else None,
                                   pdf=_path(args.pdf) if args.pdf else None,
                                   tex=_path(args.tex) if args.tex else None)
    else:
        if args.repo or args.pdf or args.tex:
            raise ValueError("--repo, --pdf and --tex apply to venues prepared outside the IEEE/JOSS exporters")
        from export_manuscript import preflight
        report = preflight(manuscript, args.venue)
    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        print(render_report(report, words, words["check_title"].format(venue=args.venue, file=manuscript.name)))
    passed = report.get("prefilter_passed", report.get("source_package_passed", not report.get("blockers")))
    return 0 if passed else 1


def _export(args, words: dict) -> int:
    if args.venue in PREPARED_MANUSCRIPTS:
        print(words["no_export"].format(venue=args.venue), file=sys.stderr)
        return 2
    from export_manuscript import export
    manuscript = _path(args.manuscript)
    output = _path(args.out) if args.out else _default_output(manuscript, args.venue)
    result = export(manuscript, args.venue, output, docx_only=args.docx_only)
    report = json.loads(Path(result["format_report"]).read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print(render_report(report, words, words["export_title"].format(venue=args.venue, file=manuscript.name)))
        print()
        print(f"{words['outputs']}: {result['output_dir']}")
        print(f"  {words['docx']}: {result['docx']}")
        print(f"  {words['pdf']}: {result['pdf'] or words['pdf_none']}")
        if result["pdf"]:
            print(words["inspect"])
    passed = result.get("prefilter_passed") if args.docx_only else result.get("content_format_passed",
                                                                               result.get("source_package_passed"))
    return 0 if passed else 1


def main(argv: list[str] | None = None) -> int:
    _console()
    parser = argparse.ArgumentParser(prog="think_tank", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lang", choices=sorted(TEXT), help="Message language (default: system locale)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Show what this computer can do")
    for name, help_text in (("new", "Start a manuscript from a skeleton"),
                            ("check", "Check a manuscript and explain how to fix problems"),
                            ("export", "Create the official-template Word file (and PDF with Word)")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("manuscript", help="Markdown manuscript (.md); relative paths are fine")
        command.add_argument("--venue", choices=VENUES, default=DEFAULT_VENUE,
                             help=f"Target venue (default: {DEFAULT_VENUE})")
        if name in {"check", "export"}:
            command.add_argument("--json", action="store_true", help="Print the full machine-readable report")
        if name == "check":
            command.add_argument("--repo", help="Software repository folder: licence and replication-script checks")
            command.add_argument("--pdf", help="Compiled PDF: page-limit check")
            command.add_argument("--tex", help="LaTeX source: official template check")
        if name == "export":
            command.add_argument("--out", help="New output folder (default: next to the manuscript, timestamped)")
            command.add_argument("--docx-only", action="store_true", help="Skip Microsoft Word; create DOCX only")
    args = parser.parse_args(argv)
    words = TEXT[_language(args.lang)]
    try:
        if args.command == "doctor":
            return _doctor(words)
        if args.command == "new":
            return _new(args, words)
        if args.command == "check":
            return _check(args, words)
        return _export(args, words)
    except FileNotFoundError as exc:
        print(words["not_found"].format(file=exc.filename or exc), file=sys.stderr)
        return 2
    except (OSError, ValueError, ImportError) as exc:
        print(f"{words['error']}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
