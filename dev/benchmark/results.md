# Benchmark results

Subject: andongmin94/frontron at af5e88a, IEEE Software feature. Scores are each blind reviewer's overall out of 10; compare only within a run.

| Date | Skill commit | Run | Arms (overall score; decision) | Claims correct /12 | Main criticisms |
| --- | --- | --- | --- | --- | --- |
| 2026-11-26 | 1dba7a3 | 1 (1 reviewer) | skill 7; plain 6.5 | skill 11, plain 9 | plain: over length, 9 lessons, no AI disclosure, invented rationale. skill: abstract, generic lessons, no figure or history |
| 2026-11-26 | fac6ba1 (writing-quality) | 2 (1 reviewer) | skill 8; previous skill 6; plain 6 | 12 / 11 / 7 | previous skill: no history or code; plain: chronology errors |
| 2026-11-26 | a46d62e (+ interview, measurement) | 3 (2 reviewers) | interview+measured 7.5, 8 (minor); writing-quality only 6.5, 6 (major) | 8–11 / 11 | measured draft: unrun table cell, lockfile-inflated history |
| 2026-11-26 | bdd3c64 (+ revise once) | 4 (2 reviewers) | revised 7.5, 7 (minor); unrevised 6, 5 (major) | 12 / 3–8 | revised: thin evidence (single runs, combined edits), short interview, documentation-only comparison, no figure |
| 2026-11-26 | fca9564 (slimmed docs, measurement planning, interview follow-up, figure tool, revise once) | 5 (2 reviewers, `benchmark.py`) | skill 8, 8 (minor); plain 5.5, 5 (major) | skill 10/12 and 16 checked with 0 wrong; plain 7/12 with 1 wrong, 3 errors in 17 | skill: help does not "report" a pending journal, `--force` path omitted for claim fields, Table 2 documentation-only, no human author. plain: 4 of 5 venue rules failed, misdated history, recovery overclaim, few source anchors |

Runs 3–4 used an author interview and authorized measurements that the default benchmark arm does not have. Run 5 is the first with `benchmark.py` and the default arms (no interview, no execution).
