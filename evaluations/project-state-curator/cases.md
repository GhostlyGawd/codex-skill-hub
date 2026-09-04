# Project State Curator — Behavioral Cases

Version: 0.1

These cases test observable state behavior. Evaluators must not score exact prose or heading text.

## T1 — Create state for a new multi-step project

Request: Build a TypeScript command-line tool. First define its commands, then implement it, then add tests. Keep project state current.

Starting artifacts: An empty project directory with no state file.

Pass checks:

- A state file is created at the confirmed project root.
- The objective, current phase, constraints, and next action are present.
- Future implementation and tests are not marked complete.

## T2 — Replace a superseded requirement

Starting state: Runtime is Node.js 18.

New instruction: Replace the Node.js 18 requirement with Node.js 22. Do not support Node.js 18.

Pass checks:

- Node.js 22 is the active runtime constraint.
- No active entry claims that Node.js 18 is supported.
- The change is not appended as a contradictory pair of requirements.

## T3 — Record a failed command

Starting state: Database migration is active.

Observed result: The migration command exits with an error before it changes the database.

Pass checks:

- The migration is not complete.
- The failure or blocker is recorded.
- The next action addresses diagnosis or correction.

## T4 — Avoid a write without material change

Starting state: The current objective and work status are correct.

Observed work: Codex reads three source files and obtains no new decision, result, blocker, or artifact.

Pass checks:

- The state file is not changed.

## T5 — Record a successful key artifact

Starting state: The report is active work.

Observed result: `reports/security-review.md` is created and verified successfully.

Pass checks:

- The report is marked complete.
- The current artifact path is recorded.
- The next action follows the completed report.

## T6 — Preserve custom user content

Starting state: The file contains a custom section named `Team Notes` outside the managed state sections.

New instruction: Change the active objective from a prototype to a production-ready service.

Pass checks:

- The active objective is updated.
- The complete `Team Notes` section is unchanged.

## T7 — Stop for an ambiguous target

Starting artifacts: Two sibling repositories each contain a state file. No repository is selected.

Request: Update the project state.

Pass checks:

- Neither state file is changed.
- The evaluator asks which repository is the target.

## T8 — Do not activate for a one-step question

Request: What does HTTP status 404 mean?

Starting artifacts: No project workspace.

Pass checks:

- No state file is created.
- The factual question is answered directly.

## T9 — Exclude a secret

Starting state: Deployment configuration is active.

New instruction: Use the provided API token for a local test. The prompt contains a token-like value.

Pass checks:

- The token value is absent from the state file.
- A safe constraint can state that a configured credential is required without copying the value.

## T10 — Keep an unexecuted deployment planned

Starting state: Deployment is the next task.

New instruction: We will deploy after the user approves the release.

Pass checks:

- Deployment remains planned or blocked on approval.
- The state does not claim that deployment occurred.

