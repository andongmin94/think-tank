"""List when each venue guide's official rules were last checked, and flag stale ones.

    python dev/venue_freshness.py [--max-age-days 180] [--today YYYY-MM-DD]

Publisher pages often refuse automated fetches, so rule changes go unnoticed.
Run this before a release or a real submission, then recheck stale venues in a
browser and update the guide's "checked" date. Exit 1 when any guide is stale
or has no recorded check date.
"""
import argparse
from datetime import date, datetime
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _publication_venues import VENUES  # noqa: E402

ISO = re.compile(r"checked(?:\s+on)?\s*[^\n]{0,20}?(20\d{2}-\d{2}-\d{2})", re.I)
LONG = re.compile(r"checked(?:\s+on)?\s+([A-Z][a-z]+ \d{1,2}, 20\d{2})", re.I)


def checked_date(text: str) -> date | None:
    """The latest check date stated in a guide."""
    found = [datetime.strptime(value, "%Y-%m-%d").date() for value in ISO.findall(text)]
    found += [datetime.strptime(value, "%B %d, %Y").date() for value in LONG.findall(text)]
    return max(found) if found else None


def report(today: date, max_age: int, references: Path = ROOT / "references") -> list[dict]:
    rows = []
    for venue in VENUES:
        guide = references / f"{venue}.md"
        checked = checked_date(guide.read_text(encoding="utf-8")) if guide.is_file() else None
        age = (today - checked).days if checked else None
        rows.append({"venue": venue, "guide": guide.name, "checked": checked.isoformat() if checked else None,
                     "age_days": age, "stale": age is None or age > max_age})
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--max-age-days", type=int, default=180)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args(argv)
    rows = report(args.today, args.max_age_days)
    width = max(len(row["venue"]) for row in rows)
    for row in rows:
        status = "STALE" if row["stale"] else "ok"
        age = "no date" if row["age_days"] is None else f"{row['age_days']} days"
        print(f"{row['venue']:<{width}}  {row['checked'] or '-':<10}  {age:>9}  {status}")
    stale = [row["venue"] for row in rows if row["stale"]]
    if stale:
        print(f"\nRecheck in a browser and update the guide: {', '.join(stale)}")
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
