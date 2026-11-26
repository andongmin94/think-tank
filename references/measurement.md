# Authorized measurement: numbers you observed yourself

By default the skill reads the input project and never executes it. Citing a project's own test reports is weaker evidence than running them. When the user explicitly authorizes execution, measure the claims the article depends on and report them with kind `measured`.

## Scope of the authorization

- Get explicit permission for execution, naming the project. Permission to read is not permission to run.
- Run only in an isolated copy (a fresh clone in the working folder or a container), never in the user's checkout. Do not publish, push, release, sign in, or change global configuration. Installing declared dependencies is part of running; say so.
- Skip steps that take unreasonably long or need credentials, hardware or paid services, and record why.

## Plan before running

Write `measurement-plan.md` before executing anything:

1. List the article's central claims (from the outline) that a run could confirm or refute.
2. For each claim, design the smallest experiment that would show it: input, steps, what to record, and the result that would contradict it.
3. **Isolate conditions.** One variable per run: one kind of user edit per scenario, each on a fresh copy, so every table row is its own experiment.
4. Include the failure cases the article discusses (interrupted operations, conflicting edits, unsupported setups), not only the happy path. Interrupt the real command (for example, kill the CLI during a write) when the article relies on recovery behaviour.
5. **Repeat timings** at least three times and report the median and range; one run is a smoke check, not a measurement.
6. If execution of an **alternative** is also authorized, run at least one real alternative on the same input and steps, so the comparison is measured, not only documented.

Then run the plan, and record any deviation from it.

## Record and report

- For every measurement keep the exact command, the commit, OS and tool versions, the date, the raw output log and a results table. Store them in the working folder and add each used result to the evidence ledger with kind `measured`.
- In the article, state the environment and the number of runs; do not generalise one machine or one sample project to all users. Distinguish your measurements from numbers the project reports.
- Report failures and surprises honestly, including measurements that contradict the documentation. Never edit the project to make a measurement pass.
- Put in a results table only what was actually run. If a cell comes from a dry run, a different scenario or the project's documentation, label it so or leave it empty. If two conditions were applied together, say so and do not split them into separate rows.
- State which commit or baseline every cited run belongs to, especially when a project's own validation predates the commit you analyse.
