# Authorized measurement: numbers you observed yourself

By default the skill reads the input project and never executes it. Citing a project's own test reports is weaker evidence than running them. When the user explicitly authorizes execution, measure the claims the article depends on and report them with kind `measured`.

## Scope of the authorization

- Get explicit permission for execution, naming the project. Permission to read is not permission to run.
- Run only in an isolated copy (a fresh clone in the working folder or a container), never in the user's checkout. Do not publish, push, release, sign in, or change global configuration. Installing the project's declared dependencies is part of running it; say so.
- Skip steps that take unreasonably long or need credentials, hardware or paid services, and record why.

## What to measure

Choose measurements that test the article's central claims, for example:

- the project's own test and verification commands (pass/fail counts, duration);
- an end-to-end run on a realistic fresh input (files created or changed, whether a removal restores the original bytes, with hashes before and after);
- behaviour under the failure or conflict cases the article discusses, with the tool's exact messages;
- cheap quantities such as command duration, files written, artefact sizes.

## Record and report

- For every measurement keep the exact command, the commit, OS and tool versions, the date, the raw output log and a short results table. Store them in the working folder and add each used result to the evidence ledger with kind `measured`.
- In the article, state the environment and the number of runs; do not generalise one machine or one sample project to all users. Distinguish your measurements from numbers the project reports.
- Report failures and surprises honestly, including measurements that contradict the documentation. Never edit the project to make a measurement pass.
- Put in a results table only what was actually run. If a cell comes from a dry run, a different scenario or the project's documentation, label it so or leave it empty. Isolate conditions you report separately (one user edit at a time); if two edits were made together, say so and do not split them into separate rows.
- State which commit or baseline every cited run belongs to, especially when a project's own validation predates the commit you analyse.
