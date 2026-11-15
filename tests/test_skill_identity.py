"""The installed research skill has one current public identity."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_think_tank_skill_identity():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    metadata = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "name: think-tank" in skill.split("---", 2)[1].splitlines()
    assert "# Think Tank" in skill.splitlines()
    assert 'display_name: "Think Tank"' in metadata
    assert "$think-tank" in metadata
    assert readme.startswith("# Think Tank\n")
    assert ".codex/skills/think-tank" in readme
    assert "$think-tank" in readme
    for source in (skill, metadata, readme):
        assert "$paper-factory" not in source
        assert ".codex/skills/paper-factory" not in source
