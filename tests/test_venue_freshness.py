"""Every venue guide records when its official rules were checked."""
import importlib.util
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("venue_freshness", ROOT / "dev" / "venue_freshness.py")
freshness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(freshness)


def test_both_date_styles_are_read():
    assert freshness.checked_date("Official sources — checked 2026-11-06") == date(2026, 11, 6)
    assert freshness.checked_date("limits were checked on October 18, 2026; later checked 2026-11-01") == date(2026, 11, 1)
    assert freshness.checked_date("no date here") is None


def test_every_offered_venue_has_a_dated_guide():
    rows = freshness.report(date(2026, 12, 1), max_age=3650)
    missing = [row["venue"] for row in rows if row["checked"] is None]
    assert missing == []


def test_old_checks_are_flagged(tmp_path):
    (tmp_path / "ieee-software.md").write_text("checked 2026-01-01", encoding="utf-8")
    rows = {row["venue"]: row for row in freshness.report(date(2026, 12, 1), 180, references=tmp_path)}
    assert rows["ieee-software"]["stale"] and rows["ieee-software"]["age_days"] == 334
    assert rows["joss"]["stale"] and rows["joss"]["checked"] is None
