"""New venue selection must not inherit another journal's limits or output type."""

import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import _publication_checks as checks
import export_manuscript as exporter
import submission_support as support


def article(abstract_words=150, reference_count=1, keyword_count=3):
    return ("# A Research Software Study\n\n"
            "Alice Research | Research Lab | alice@example.org\n\n## Abstract\n\n" +
            " ".join(["word"] * abstract_words) + "\n\nKeywords: " +
            "; ".join(f"term{i}" for i in range(keyword_count)) +
            "\n\n## (1) Overview\n\nA documented software problem. [1]\n\n"
            "### Implementation and architecture\n\nThe repository provides modules.\n\n"
            "### Quality control\n\nRecorded test results describe the checks.\n\n"
            "## Availability\n\nThe actual archived version is identified.\n\n"
            "## Reuse potential\n\nDocumented users can adapt the software.\n\n"
            "## Competing interests\n\nThe supplied declaration is retained.\n\n"
            "## Acknowledgments\n\nOpenAI Codex assisted with drafting throughout this article.\n\n"
            "## References\n\n" + "\n\n".join(
                f"[{i}] Source Authors. Retained reference {i}. 2025."
                for i in range(1, reference_count + 1)))


def status(result, name):
    return next(row["status"] for row in result["items"] if row["id"] == name)


@pytest.mark.parametrize("venue", ["ieee-access", "jors"])
def test_venues_with_mandatory_publication_fees_are_not_offered(tmp_path, venue):
    # IEEE Access and JORS always charge an article processing charge; the
    # skill only targets venues with a fee-free publication route.
    assert venue not in exporter.EXPORT_VENUES and venue not in support.VENUES
    with pytest.raises(ValueError):
        checks.validate_manuscript(article(), venue)


@pytest.mark.parametrize("venue", ["ieee-software", "ieee-security-privacy", "joss"])
def test_submission_bundle_accepts_each_new_venue_and_keeps_pending(tmp_path, venue):
    root = tmp_path / "sources"
    root.mkdir()
    (root / "paper.md").write_text("Supplied manuscript", encoding="utf-8")
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"venue_id": venue, "title": "Supplied study",
                               "files": [{"role": "manuscript", "path": "paper.md"}]}), encoding="utf-8")
    result = support.prepare_bundle(plan, root, tmp_path / "bundle")
    assert result["venue_id"] == venue
    assert not result["submission_ready"] and not result["actual_submission_performed"]
    if venue == "joss":
        assert any("paper.bib" in value for value in result["pending"])


def test_new_cli_routes_source_export_and_rejects_word_profile(tmp_path, monkeypatch, capsys):
    import _publication_joss
    source, output = tmp_path / "paper.md", tmp_path / "bundle"
    calls = []
    def export(path, folder, **kwargs):
        calls.append((path, folder, kwargs))
        return {"source_package_passed": True, "publisher_pdf_rendered": False}
    monkeypatch.setattr(_publication_joss, "export", export)
    assert exporter.main(["export", "--venue", "joss", "--manuscript", str(source), "--output-dir", str(output)]) == 0
    assert calls[0][:2] == (source, output)
    assert not json.loads(capsys.readouterr().out)["publisher_pdf_rendered"]
    assert exporter.main(["preflight", "--venue", "joss", "--manuscript", str(source), "--profile", "authors.json"]) == 2
    assert "do not apply" in capsys.readouterr().err


@pytest.mark.parametrize('venue,role,suffix', [('emse', 'editable_docx', '.docx'), ('jmlr-mloss', 'review_pdf', '.pdf')])
def test_prepared_cs_bundle_needs_the_selected_format_and_conversion_record(tmp_path, venue, role, suffix):
    root = tmp_path / 'sources'
    root.mkdir()
    source = root / 'paper.md'
    source.write_text('# Draft', encoding='utf-8')
    prepared = root / ('prepared' + suffix)
    prepared.write_bytes(b'Supplied fixture; the bundler does not validate the document format.')
    plan = {'venue_id': venue, 'title': 'Formatting demonstration', 'draft_status': 'draft',
            'article_type': 'Research Article' if venue == 'emse' else 'MLOSS', 'guidance_status': 'verified',
            'files': [{'role': 'manuscript', 'path': source.name}, {'role': 'supplement', 'path': prepared.name}]}
    plan_path = root / 'plan.json'
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    missing = support.prepare_bundle(plan_path, root, tmp_path / 'without-manuscript')
    assert any(role in gap and suffix in gap for gap in missing['missing_evidence'])
    assert missing['draft_status'] == 'incomplete'
    plan['files'][1]['role'] = role
    plan['recommendation_status'] = 'not_recommended'
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    supplied = support.prepare_bundle(plan_path, root, tmp_path / 'supplied')
    assert not any(role in gap and suffix in gap for gap in supplied['missing_evidence'])
    assert any('conversion_record' in gap for gap in supplied['missing_evidence'])
    assert (tmp_path / 'supplied' / 'files' / prepared.name).read_bytes() == prepared.read_bytes()
    assert supplied['recommendation_status'] == 'not_recommended'
    assert 'Recommendation: **not recommended**' in (tmp_path / 'supplied' / 'checklist.md').read_text(encoding='utf-8')
    assert not supplied['submission_ready'] and not supplied['actual_submission_performed']
    assert venue not in exporter.EXPORT_VENUES
