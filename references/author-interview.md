# Author interview: first-hand reasons the records do not hold

Repositories record what changed, rarely why. When the person asking for the article built the project, their reasons, rejected options, incidents and user feedback are often the strongest material for a practitioner article. Collect them explicitly instead of guessing or leaving the "why" out.

## When to interview

Interview only when the user is an author or maintainer of the inspected project and agrees to answer. Never interview on behalf of someone else or present another person's motives.

## Prepare questions from evidence gaps

After reading the repository and drafting the outline, list the places where the article needs a reason or experience the records cannot supply. Ask 5–8 short, specific questions anchored to verified evidence, for example:

- "Commit 09ba995 adopted a framework-first design and fddec97 removed it twelve days later. What made you reverse it?"
- "Which bug or incident cost you the most time, and what did you change afterwards?"
- "Who uses the tool, and what feedback changed the design?"
- "Which alternative did you consider seriously, and why did you not choose it?"
- "What would you do differently if you started again?"

Name the commit, file or behaviour in each question so the answer attaches to a record. Do not ask leading questions that suggest the answer.

## Follow up once on thin answers

Short answers ("I just did it", "don't know", "people like it") are common and give the article little. After the first round, ask **one** follow-up round for the answers that matter most to the outline, at most three questions, each narrower and easier to answer than the original:

- Ask for one concrete instance: "Can you name one problem the framework-first design caused, or one thing you wanted to try with it?"
- Offer the records as memory aids: "Commit 05c968b removed the lock module; do you remember a failure or a maintenance cost behind that?"
- Ask for evidence, not opinion: "Where did the positive feedback come from (issues, messages, downloads)? May the article mention it?"

Accept "don't know" after the follow-up and leave the gap. Do not push further or rephrase until an answer fits the story.

## Record and use the answers

- Save the questions and the author's answers verbatim with the date in the working folder (for example `author-interview.md`) and add each used statement to the evidence ledger with kind `author_stated`, distinct from source-declared, observed, measured and derived claims.
- In the article, attribute these statements to the authors ("we chose…", "we removed it because…"), and never present them as independently verified facts. Keep the record they explain cited next to them.
- If an answer conflicts with the repository, report the conflict to the user and do not silently prefer either.
- Leave unanswered questions as gaps. Do not fill them with plausible motives.
- Author statements are not consent to publish personal data, other people's names or private feedback; ask before including them.
