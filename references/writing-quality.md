# Writing an article worth reading

Accuracy is necessary but not sufficient. A draft that only avoids unsupported claims reads as a cautious summary; reviewers reject those too. Use the evidence you retained to make the article specific, concrete and memorable. Caution limits what you claim, not how vividly you show what is supported.

## Make every main point concrete

- Back each main claim with a concrete, verified artefact the reader can see: a short code excerpt (5–15 lines, trimmed with `…`), a data structure, a command and its output, a configuration diff, a number, or a commit. Cite its exact file and line or commit.
- Include **at least one figure or excerpt** that shows the central mechanism (an architecture or sequence diagram, a state machine, or the key code path). Draw diagrams from the inspected code, not from intuition. Count it against the venue's visual allowance.
- Prefer one worked example followed end to end (an input, what the system does, the result) over several abstract descriptions.

## Mine the history, carefully

- Read the commit log, changelog, issues and design documents for **decisions that changed**: reverts, rewrites, removed features, fixes after incidents, abandoned approaches. Why something was undone is often the most useful lesson for practitioners.
- Tell that story only from what the records show. Verify order from the commit graph (`git log --topo-order`, merge parents, tags), not commit timestamps alone, which can be rewritten. Quote commit titles exactly; mark translations as translations.
- Do not supply motives, user reactions or timelines the records do not state. Write "the commit message says" or "the change removed", not "the team realised".
- When a commit's size illustrates a design change, exclude lockfiles, generated and vendored files (`git diff --stat -- . ':!package-lock.json'` and similar), and report net rather than gross line changes, or label which one you use.

## Compare real alternatives

- Name two or three alternatives practitioners actually use for the same problem (competing tools, frameworks, built-in features or manual practice). Compare them on the same few criteria in one table or paragraph: what each costs, what it guarantees, when it is the better choice.
- Say when the described approach is the wrong choice. A counterexample makes the recommendation credible.

## Write lessons that could only come from this work

- For each lesson or actionable insight, ask: could this sentence be pasted unchanged into an article about a different project? If yes, rewrite it until it names the concrete condition, mechanism or trade-off this work revealed.
- A good lesson has three parts: the situation, the decision and the observed consequence or cost.

## Shape

- Open with a concrete scene of the reader's problem (a failure, a constraint, a surprising cost), then state the contribution in one sentence.
- Give each section one point. Cut sidebars and lists that repeat the body.
- Keep limitations specific and near the claims they qualify, not only in a final section.

## Self-review before export

Read the draft once as a reviewer and check:

1. Does each main section contain at least one concrete artefact with a precise source?
2. Is there a figure or excerpt that shows the mechanism?
3. Does the article use at least one verified change or failure from the project's history?
4. Are alternatives compared on the same criteria, including when not to use this approach?
5. Does every lesson pass the "different project" test?
6. Is every motive, causal story and date supported by a record, and is every quotation exact?

Revise the draft for any "no" that the evidence can fix. Report remaining gaps rather than filling them with generic prose.
