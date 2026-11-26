You are an independent reviewer comparing manuscript drafts ({LETTERS}) written for an {VENUE} feature article about the open-source repository {REPOSITORY}. You do not know how any was produced; judge only the text and its evidence.

Read only these files, the repository and the web (for reference checks); images a draft references are next to it at the referenced path:
{DRAFTS}
- Repository at the described commit (read-only): {SUBJECT}
Do not open other folders under {RUN}.

Evaluate every draft on the same criteria with concrete evidence:
1. Factual accuracy: verify 12 specific technical or historical claims per draft against the repository (git log --topo-order, git show --numstat, grep, read). Classify correct / partly / unsupported or wrong with file:line or commit evidence. Check that table cells reflect what was actually run or read, quotes are exact, and commit sizes are not inflated by lockfiles or generated files.
2. Reference integrity: does each reference exist with the stated metadata and support its use?
3. Venue rules: {RULES}. Report met / not met with counts.
4. Overclaiming, unsupported motives, placeholders.
5. Reading quality 1–10: concreteness, evidence strength, use of history, comparison with real alternatives, specificity of lessons, would you keep reading. Use the full scale; 9–10 only for work an editor would accept with minor revisions.

End with a comparison table, an overall score out of 10 per draft, a ranking, and the top three fixes for each. Be strict and specific.
