# Research, revision, and assessment

## Make the additional value inspectable

- Pick a question the material can answer and a decision that matters to the intended reader. Read enough to establish central behavior, normal reachability, guards, counterexamples and boundaries. Record why cases were chosen. A bounded source construction can be valuable without being an execution, exhaustive survey or prevalence evidence.
- If angles compete, use the worked example in [contribution-selection.md](contribution-selection.md). Reuse retained reading and witnesses to drop unsupported or low-value questions before writing.
- Test the contribution against the closest existing method at its strongest (guarantees, assumptions), applied fairly to the same cases. Say what it already establishes, what the article adds, and whether that changes a decision. Agreement with established guidance is a result; never weaken a baseline to manufacture novelty.
- State the supported result and the reader's decision plainly before committing to a full article. A narrow case justifies an integration lesson only if it differs from a polished restatement of familiar advice. If value stays unclear, narrow or reconsider; accurate citations and a filled template are not a submission recommendation.
- Separate source-declared behavior, static and executed observations, interpretation and hypothetical applications. A recorded expectation does not establish runtime harm; a worked policy is not an implemented, safe or effective fix. Missing external evidence or an inaccessible paper is a research limitation, not the project's demonstrated ceiling; reviewers must keep the two apart too.

Revisions should fix real inference or adoption problems: a missing premise, unfair comparison, unexplained state transition, ambiguous result, needed failure condition, or unlocatable evidence. A new study (execution, another independent case, measurements, a maintainer response) is different. More prose, checks or a higher rating are not new evidence.

## Write for a reader, then freeze

Abstract: the problem, what was actually done, the supported result, why it changes a decision. Call a static study static; do not turn the conclusion into a catalogue of unclaimed discoveries. Introduce concrete actors, state changes and consequences before abstractions (e.g., membership, restoration authority). Use technical terms for precision; word lists and AI-detection scores establish neither authorship nor quality.

One author editorial pass, then freeze for independent review:

- Can the venue's intended reader restate the problem, principal result, added value over existing work and practical consequence?
- Lead with source findings and the conditions under which they hold; cut openings that defend an interpretation before its evidence.
- Once a case or comparison shows the added value, cut later announcements that it is a contribution or lesson.
- Consolidate conclusions and advice unless a passage adds a new premise, mechanism, consequence or action, however reworded. Keep a useful actionable recap.
- If the central result cannot be explained clearly, fix that before export instead of adding defensive prose.

Qualifications:

- General scope goes in the method; consequential limits in the limitations discussion.
- Keep a local qualification wherever removing it would overstate a source-derived finding, proposed design or empirical support. Consolidation must not turn a hypothetical repair into an implemented result or imply unperformed execution.
- Keep counterexamples and qualifications that change a claim's reach or the reader's decision, and useful case controls and refusal conditions (they test the argument). Cut anticipated-objection rebuttals that add no evidence or reasoning.

The venue-required AI-use acknowledgment names the actual tool, affected material or sections, and extent of assistance, truthfully and proportionately. Methodological facts such as unexecuted code belong in the study description, not repeated there unless needed to describe the assistance. Never conceal AI-generated material, relabel extensive generation as grammar correction, or invent human work.

## Evidence-grounded review criteria

Judge the strongest useful manuscript the inspected project and primary evidence support, and its actual fit for the selected venue. Criteria are review dimensions, not numerical targets, publisher peer review or an acceptance predictor.

- Needed: a worthwhile supported contribution, adequate evidence, a coherent argument for the intended reader. No detected error is not enough.
- Material difficulty understanding the central result, or repetition obscuring its value, warrants `revise_before_submission` even with correct claims.
- The quality target is an internal recommendation to publish as written; minor revision falls short. Decide whether claims and venue need further central evidence, a consequential comparison, a redesigned study or substantial rewriting, versus localized corrections. Execution restrictions or narrow scope do not make an essential gap nonblocking; a static method does not automatically need experiments for every bounded claim.

| Criterion | What the reviewer judges |
| --- | --- |
| `contribution` | A specific, consequential advance in readers' decisions beyond existing guidance; not a polished restatement. |
| `evidence` | Accurate, adequate, inspectable support for central claims; scope and confidence match what was actually observed. |
| `method` | A traceable procedure, selection rationale, counterexamples and meaningful checks another reader can follow. |
| `comparison` | Fair comparison with the closest existing work and alternatives, grounded in actual primary bodies, identifying the added value. |
| `practical_value` | Usable decisions, worked cases, costs, failure conditions and residual risks for the intended practitioner. |
| `logic` | Evidence supports the argument and conclusions; no unsupported generalization or hidden premise. |
| `presentation` | The intended reader can restate the central problem, result and practical consequence; prose and visuals are precise and economical, not obscured by repetitive caveats or conclusions. |
| `venue_fit` | A compelling feature article for the selected magazine's audience, scope and applicable article requirements. |
| `limitations` | Specific, consequential limits and alternatives integrated into claims and advice. |

## One independent review

Give a separate reviewer the complete frozen article, relevant raw sources and primary bodies, exact exported files when available, and this rubric. Withhold prior ratings, desired scores and preferred winners unless the user asked for a comparison needing them. The reviewer checks the claims, not just the author's evidence summary.

- One bounded pass of complementary scrutiny: no automatic model-to-model revision loop; two agreeing models do not establish research validity.
- Review argument and reader comprehension directly; never ask the critic to make the article seem human-written.
- Name a specific second model only when its actual use is established.

The single assessment:

- covers all nine criteria with uncertainty, short literal article anchors, evidence-based reasons and consequential remaining improvements;
- leads with internal `publication_recommendation` and `as_written_publication_target_met`; `no_major_revision_target_met` is a separate diagnostic;
- keeps the separate `recommendation` (`consider_submission`, `revise_before_submission`, `not_recommended`) for preparation tools, explaining submission suitability for the audience and article category;
- lists essential factual, citation or source defects separately; any one blocks an unqualified recommendation to consider submission;
- separates blocking issues from useful future research, without manufacturing observations or novelty.

| Internal publication recommendation | Meaning for the exact reviewed article |
| --- | --- |
| `accept` | Contribution, evidence, comparisons and presentation warrant publication as written; no required revision. |
| `minor_revision` | Only identified, localized corrections remain (no new central evidence, consequential comparison, redesigned study or substantial rewriting); list them explicitly. |
| `major_revision` | At least one such substantive change is needed before recommending publication; state the unmet need and why it matters to the current claim. |
| `reject` | Contribution, evidence or venue fit does not justify recommending publication; distinguish a different study from revising this article. |

- `as_written_publication_target_met`: true only for `accept`. `no_major_revision_target_met`: true only for `accept` or `minor_revision`.
- No label is a publisher decision, first-round acceptance prediction or probability.
- Older reviews without these judgments stay unassessed against the stronger target; never relabel a legacy `consider_submission` or passing format/final-preparation report as meeting it.

Scores are optional (when useful or requested): integers 0–10 on all nine criteria, with uncertainty and evidence. They never set readiness by threshold or override an essential defect. A displayed mean uses all nine unrounded scores, no favorable subset. Keep the original assessment and reviewed article/output hashes, scored or not. One-pass reviewers are not a controlled paired comparison; a score change proves neither improvement nor deterioration. Never call a replacement reviewer for a preferred result.

Agent review is separate from human author approval and publisher peer review. If it is unavailable or interrupted, report its actual status; never invent an assessment or pass off self-review as independent. Keep outcomes separate ([delivery record](#evidence-and-delivery-record)). After the one review, deliver and stop rewriting or rating, except the single revision below for drafting requests.

## One revision after review (drafting requests)

When the user asked for a draft, make exactly one revision after the review, then stop:

- Keep the reviewed draft, its hash and the review unchanged; write the revision as a new file.
- Make every localized correction the review identifies that retained evidence supports: wrong or stretched claims, table cells not backed by an actual run, numbers mixing gross and net or including generated files, quotations stretched beyond their words, missing baselines, rule violations, placeholders, unclear structure. Re-verify each changed claim against its source, log or interview record.
- Never add unsupported claims to satisfy a reviewer. A change needing new evidence (measurement, interview answer, unreadable source) stays an explicit open item.
- Log each finding with the change made or why it stays open.
- Rerun deterministic checks (preflight, editorial checks, evidence ledger) on the revision. No second review or self-rerating; report the revision as unreviewed unless the user asks for another review.

## Evidence and delivery record

Use ordinary files in a fresh research directory. Record source revision and byte hashes, retained primary-body identities and reading scope, exact article/export/review hashes, actual helper outcomes, known model identity and unresolved limits. Existing counts and failures stay historical. Current model use is not zero just because no API instrumentation exists.

Put long command recipes, source witnesses and auxiliary policy calculations in an identified companion; the article must still make its argument without the companion substituting for a missing result. Preserve original licenses when redistributing repository sources; respect third-party paper redistribution rights.

Preparation gaps sit beside the manuscript. Never invent affiliation, contact, biography, photograph, funding, conflicts, rights, originality, author responsibility or approval to pass a check. Content recommendation, native format compliance, page inspection, human/administrative preparation, actual submission and acceptance are separate facts; administrative completion and submission do not establish acceptance.
