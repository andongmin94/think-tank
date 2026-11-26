# Blind draft benchmark

Checks whether a change to the skill makes its drafts better or worse, using the same request every time and reviewers who do not know which draft came from where. Run it after substantial changes to `SKILL.md`, the writing guidance or the drafting tools, not after every edit: one run costs roughly 30–60 minutes and several hundred thousand model tokens.

## What it compares

The default subject is `andongmin94/frontron` at a pinned commit (see `config.json`), written up as an IEEE Software feature. Arms:

- `skill` — an agent that follows this skill (no author interview, no execution).
- `plain` — the same request with no skill, as a control.

Each arm gets the identical request (`prompts/arm.md`); the skill arm also gets `prompts/arm-skill.md`. Two reviewers with different roles score the drafts blind.

## Run

From the skill repository, with the local Python:

```sh
python dev/benchmark/benchmark.py prepare ../bench-2026-12-01
```

This clones the subject at the pinned commit and writes `prompts/arm-skill.md` and `prompts/arm-plain.md` into the run folder. Give each arm prompt to a **separate, fresh agent** at the same time (for example two Claude Code subagents, or `claude -p "$(cat prompts/arm-skill.md)"` in two terminals). When both drafts exist:

```sh
python dev/benchmark/benchmark.py blind ../bench-2026-12-01
```

This copies the drafts as random letters into `review/` and writes `prompts/reviewer-1.md` and `prompts/reviewer-2.md`. Give each to a separate fresh agent. Read both reports, then:

```sh
python dev/benchmark/benchmark.py reveal ../bench-2026-12-01
```

Record the outcome in `results.md`: date, skill commit, each reviewer's overall score and decision per arm, claims correct of 12, rule compliance, and the reviewers' main criticisms.

## Reading the results

- Compare arms **within one run**. Scores drift between runs because reviewers grow stricter when they see stronger alternatives.
- One run is one sample. Treat a difference of a point or less as noise unless both reviewers agree and the criticisms explain it.
- The reviewers are also models; their factual checks (claims verified against the repository) are more reliable than their scores.
