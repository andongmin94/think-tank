"""Blind draft benchmark: prepare runs, hide which draft is which, reveal afterwards.

    python dev/benchmark/benchmark.py prepare RUN_DIR [--arms skill,plain] [--subject PATH_OR_URL] [--commit SHA]
    python dev/benchmark/benchmark.py blind RUN_DIR
    python dev/benchmark/benchmark.py reveal RUN_DIR

`prepare` creates RUN_DIR with a pinned checkout of the subject repository, one
output folder per arm, and ready-to-use prompts for each arm and for two blind
reviewers. Give each prompt to a separate agent (for example a Claude Code
subagent or `claude -p`); see README.md. `blind` copies the finished drafts
under random letters for the reviewers; `reveal` prints which letter was which.
Nothing here calls a model, so the deterministic parts stay reproducible.
"""
import argparse
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1]
CONFIG = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
LETTERS = "PQRSTUVW"


def _git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout.strip()


def _fill(template: str, values: dict) -> str:
    for key, value in values.items():
        template = template.replace("{" + key + "}", str(value))
    return template


def prepare(run: Path, arms: list[str], subject: str, commit: str, python: str) -> dict:
    run = run.absolute()
    if run.exists():
        raise ValueError(f"{run} already exists; choose a new run folder")
    unknown = [arm for arm in arms if arm not in CONFIG["arms"]]
    if unknown:
        raise ValueError(f"Unknown arms: {', '.join(unknown)} (known: {', '.join(CONFIG['arms'])})")
    (run / "prompts").mkdir(parents=True)
    checkout = run / "subject"
    _git("clone", "--quiet", subject, str(checkout))
    _git("checkout", "--quiet", commit, cwd=checkout)
    values = {"SUBJECT": checkout, "VENUE": CONFIG["venue"], "REPOSITORY": CONFIG["repository"],
              "SKILL": SKILL, "PYTHON": python, "RUN": run}
    for arm in arms:
        out = run / "arms" / arm
        out.mkdir(parents=True)
        body = _fill((HERE / "prompts" / "arm.md").read_text(encoding="utf-8"), {**values, "OUTPUT": out / "article.md"})
        extra = HERE / "prompts" / f"arm-{arm}.md"
        if extra.is_file():
            body += "\n" + _fill(extra.read_text(encoding="utf-8"), {**values, "OUTPUT": out / "article.md"})
        (run / "prompts" / f"arm-{arm}.md").write_text(body, encoding="utf-8")
    meta = {"repository": CONFIG["repository"], "subject": subject, "commit": _git("rev-parse", "HEAD", cwd=checkout),
            "venue": CONFIG["venue"], "arms": arms, "skill_commit": _git("rev-parse", "HEAD", cwd=SKILL)}
    (run / "run.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def blind(run: Path, seed: int | None = None) -> dict:
    run = run.absolute()
    meta = json.loads((run / "run.json").read_text(encoding="utf-8"))
    drafts = {arm: run / "arms" / arm / "article.md" for arm in meta["arms"]}
    missing = [arm for arm, path in drafts.items() if not path.is_file()]
    if missing:
        raise ValueError(f"Drafts not finished for: {', '.join(missing)}")
    review = run / "review"
    if review.exists():
        raise ValueError("Blind copies already exist; reveal or use a new run")
    (review / "figures").mkdir(parents=True)
    order = list(drafts)
    random.Random(seed).shuffle(order)
    key = {}
    for letter, arm in zip(LETTERS, order, strict=False):  # more letters than arms
        shutil.copyfile(drafts[arm], review / f"{letter}.md")
        figures = drafts[arm].parent / "figures"
        if figures.is_dir():
            for figure in figures.iterdir():
                if figure.is_file():
                    shutil.copyfile(figure, review / "figures" / figure.name)
        key[letter] = arm
    (run / "key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    letters = ", ".join(sorted(key))
    values = {"DRAFTS": "\n".join(f"- {review / (letter + '.md')}" for letter in sorted(key)),
              "LETTERS": letters, "SUBJECT": run / "subject", "VENUE": meta["venue"],
              "REPOSITORY": meta["repository"], "RUN": run, "RULES": CONFIG["venue_rules"]}
    for name in ("reviewer-1.md", "reviewer-2.md"):
        (run / "prompts" / name).write_text(_fill((HERE / "prompts" / name).read_text(encoding="utf-8"), values),
                                            encoding="utf-8")
    return {"letters": sorted(key), "reviewer_prompts": [str(run / "prompts" / n) for n in ("reviewer-1.md", "reviewer-2.md")]}


def reveal(run: Path) -> dict:
    return json.loads((run.absolute() / "key.json").read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("prepare")
    p.add_argument("run", type=Path)
    p.add_argument("--arms", default=",".join(CONFIG["default_arms"]))
    p.add_argument("--subject", default=CONFIG["subject_url"])
    p.add_argument("--commit", default=CONFIG["commit"])
    p.add_argument("--python", default=sys.executable, help="Python with the skill's requirements, for the skill arm")
    b = commands.add_parser("blind")
    b.add_argument("run", type=Path)
    b.add_argument("--seed", type=int)
    r = commands.add_parser("reveal")
    r.add_argument("run", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare(args.run, [a.strip() for a in args.arms.split(",") if a.strip()],
                             args.subject, args.commit, args.python)
        elif args.command == "blind":
            result = blind(args.run, args.seed)
        else:
            result = reveal(args.run)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
