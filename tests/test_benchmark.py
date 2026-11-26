"""The benchmark's deterministic steps: prepare, blind and reveal."""
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("benchmark", ROOT / "dev" / "benchmark" / "benchmark.py")
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)


def git(cwd, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                           "-c", "commit.gpgSign=false", *args], cwd=cwd, capture_output=True, text=True,
                          check=True).stdout.strip()


@pytest.fixture
def subject(tmp_path):
    repo = tmp_path / "subject-src"
    repo.mkdir()
    git(repo, "init", "--quiet")
    (repo / "README.md").write_text("tool\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "--quiet", "-m", "init")
    return repo, git(repo, "rev-parse", "HEAD")


def test_prepare_blind_reveal_round_trip(tmp_path, subject):
    repo, commit = subject
    run = tmp_path / "run"
    meta = bench.prepare(run, ["skill", "plain"], str(repo), commit, "python")
    assert meta["commit"] == commit and (run / "subject" / "README.md").is_file()
    skill_prompt = (run / "prompts" / "arm-skill.md").read_text(encoding="utf-8")
    plain_prompt = (run / "prompts" / "arm-plain.md").read_text(encoding="utf-8")
    assert "Think Tank" in skill_prompt and "Think Tank" not in plain_prompt
    assert str(run / "arms" / "plain" / "article.md") in plain_prompt
    assert "{" not in skill_prompt.replace("{}", "")

    with pytest.raises(ValueError, match="not finished"):
        bench.blind(run)
    for arm in ("skill", "plain"):
        (run / "arms" / arm / "article.md").write_text(f"# draft from {arm}\n", encoding="utf-8")
    result = bench.blind(run, seed=7)
    assert result["letters"] == ["P", "Q"]
    reviewer = (run / "prompts" / "reviewer-1.md").read_text(encoding="utf-8")
    assert "arms" not in reviewer and "plain" not in reviewer  # reviewers cannot see which arm is which
    assert str(run / "review" / "P.md") in reviewer and "{" not in reviewer
    key = bench.reveal(run)
    assert sorted(key.values()) == ["plain", "skill"]
    for letter, arm in key.items():
        assert (run / "review" / f"{letter}.md").read_text(encoding="utf-8") == f"# draft from {arm}\n"


def test_prepare_refuses_existing_folder_and_unknown_arm(tmp_path, subject):
    repo, commit = subject
    (tmp_path / "taken").mkdir()
    with pytest.raises(ValueError, match="already exists"):
        bench.prepare(tmp_path / "taken", ["skill"], str(repo), commit, "python")
    with pytest.raises(ValueError, match="Unknown arms"):
        bench.prepare(tmp_path / "new", ["magic"], str(repo), commit, "python")


def test_config_pins_a_full_commit():
    config = json.loads((ROOT / "dev" / "benchmark" / "config.json").read_text(encoding="utf-8"))
    assert len(config["commit"]) == 40 and set(config["default_arms"]) <= set(config["arms"])
