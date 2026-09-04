# Repository Governance — Corrected Implementation Revalidation

Version: 1.0  
Date: 2026-09-04  
Work ID: `repository-governance`  
Result: Fail  
Evaluator: Independent Codex subagent

Validated artifacts: [Specification version 0.2](../../specs/repository-governance/spec.md), [task list version 0.3](../../plans/repository-governance/tasks.md), and the corrected local candidate files present at 2026-09-04T19:26:41Z UTC. The local folder has no git metadata, so no candidate commit or tree SHA is available. Before this report was added, the sorted file-hash manifest had SHA-256 `1a7c7bb4654df2cc0af658eebf7b03fd9ef8827b3b0bf40b74799fb418738935`.

This report follows and preserves the immutable [failed implementation validation](2026-09-04-03-implementation.md) and [task-list version 0.3 validation](2026-09-04-04-task-list.md). It does not overwrite either report.

This report becomes immutable when it first enters the default branch.

## Method

The evaluator:

- Verified the exact task-list SHA-256 supplied for version 0.3.
- Read the corrected validator, all 28 unit tests, the state, backlog, roadmap, specification, task list, workflow, template, README, migrated evidence, and earlier reports.
- Ran full-tree validation.
- Ran the 28-test suite twice.
- Ran the ten N1–N10 regression tests separately.
- Confirmed G1–G15 through the named fixture tests.
- Ran the `project-state-curator` structural validator.
- Tested newest delivery-report precedence.
- Tested completion of non-skill work.
- Added one independent base/head test for deletion of a completed skill and its evaluation evidence.
- Used read-only GitHub connector calls. The evaluator made no GitHub mutation.

## Scope and identity

| Artifact | SHA-256 or identity | Result |
| --- | --- | --- |
| Task list version 0.3 | `f4fa90dd288aacfccccedf18a25a3098f5cbc6d4944a436bf629e8f16b6387d8` | Exact match |
| Validator | `fa603b8eddf50a44b4189cc838a934558d69558284f6a5060cee745e2e60c53c` | Inspected |
| Unit tests | `e2bc08a8456c8f472d77cf514bcc46286f986a73ee79cfc88b6b45d19c8d4967` | Inspected |
| Failed implementation report | `1fddff76790b48466397c36a0cfa0ccebcad652e7094791801ac5e896d409089` | Preserved |
| Task-list revalidation | `8d268ba3dbd96f5e68c307c13a3d2aa4975114b95077f4a8eff028e729e4882e` | Preserved |

## Local evidence

| Check | Command or method | Result | Evidence |
| --- | --- | --- | --- |
| Full-tree validation | `python tools/validate_repository.py --all` | Pass | Exit 0; 0 errors and 0 warnings at 2026-09-04T19:26:41Z. |
| Full unit suite, run 1 | `python -m unittest discover -s tests/repository_validation -v` | Pass | 28 tests passed in 2.495 seconds. |
| Full unit suite, run 2 | Same command | Pass | 28 tests passed in 2.442 seconds at 2026-09-04T19:26:44Z. |
| N1–N10 suite | `python -m unittest tests.repository_validation.test_validator.IndependentFindingRegressionTests -v` | Pass | 10 tests passed in 0.654 seconds. N1–N9 failed for their required check IDs. N10 passed. |
| G1–G15 | Named `ValidatorFixtureTests` in both full runs | Pass | All 15 required cases passed. G4, G7, and G8 include their required variants. |
| Contract tests | Three named `ValidatorContractTests` in both full runs | Pass | Invalid commands, aggregation, read-only behavior, and multi-class change handling passed. |
| Skill structure | `python /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/project-state-curator` | Pass | Exit 0; `Skill is valid!` |
| N1 — state sections | Regression test | Pass | Missing sections produce `GOV-STATE-SECTIONS`. |
| N2 — roadmap controls | Regression test | Pass | Missing current batch or completion rules produce `GOV-ROADMAP-CONTROLS`. |
| N3 — backlog links | Regression test | Pass | Missing specification or task-list links produce `GOV-BACKLOG-LINK`. |
| N4 — roadmap link | Regression test | Pass | A missing completed-item specification link produces `GOV-ROADMAP-LINK`. |
| N5 — passing report with blocker | Regression test | Pass | The invalid report produces `GOV-REPORT-RESULT`. |
| N6 — newest failed delivery report | Regression test and code inspection | Pass | The newer failure overrides the older pass and produces `GOV-LATEST-VALIDATION`. `latest_delivery_report` orders dated sequence names. |
| N7 — impossible calendar date | Regression test | Pass | The invalid date produces `GOV-DATE`. |
| N8 — review with active task | Regression test | Pass | The invalid state produces `GOV-REVIEW`. |
| N9 — report without artifact identity | Regression test | Pass | The invalid report produces `GOV-REPORT-ARTIFACT`. |
| N10 — completed non-skill work | Regression test | Pass with defect noted below | A `Done` item without a skill directory or evaluation directory exits 0. This supports non-skill work, but the test has no persistent work-type marker. |

## Status review

Current statuses are honest for the available evidence:

- `STATE.md`, `BACKLOG.md`, and `ROADMAP.md` show repository governance as blocked.
- Task-list version 0.3 is `Validated`, not `Active` or `Complete`.
- Tasks 0.1–0.5 and 1.1 are `Done`.
- Task 1.2 is `Ready`.
- Tasks 1.3 and 6.5 are `Blocked` on live GitHub controls.
- Later local outputs are provisional and their task rows remain `Pending`.
- The governance specification is `Validated`, not `Implemented`.
- `project-state-curator` remains `Done`, with its historical dependency resolved and its self-evaluation labeled non-independent.

The task-list hash mismatch from finding V2 is closed. The new task-list validation names and matches the exact version 0.3 file.

## Additional independent defect test

The evaluator created a valid temporary git repository with a completed skill named `alpha`. The base contained its skill package and evaluation evidence. The head then:

- Deleted `skills/alpha/`.
- Deleted `evaluations/alpha/`.
- Removed the skill and evaluation links from the implemented specification.
- Added a new passing implementation report.
- Updated the backlog and specification to the new report.
- Kept unrelated files below `skills/` and `evaluations/` so the canonical root directories still existed.

Command: `python tools/validate_repository.py --base <base> --head <head>`.

Observed result: exit 0 with 0 errors and 0 warnings.

Expected result: exit 1 because a completed skill cannot lose its implementation and evaluation evidence.

Cause: `check_delivery` decides that work is a skill only when `skills/<work-id>/` exists in the head tree. After the directory is deleted, the validator treats the item as non-skill work. The N10 fixture uses the same absence rule, so it does not prove a safe distinction between skill work and non-skill work.

## Live GitHub evidence

| Control | Result | Evidence |
| --- | --- | --- |
| Repository | Proven | Read-only repository metadata returned `GhostlyGawd/codex-skill-hub`. |
| Default branch | Proven | Repository metadata returned `main`. |
| Governance feature branch | Not present at inspection time | Read-only branch search returned no `feat/repository-governance` branch. |
| Governance pull request | Not present at inspection time | Read-only pull-request search returned no open pull request. |
| Pull-request workflow run | Not proven | No governance pull request exists. |
| Default-branch workflow run | Not proven | The corrected workflow is not on the default branch. |
| Required check `repository-governance` | Not proven | No live run exposes the check. |
| Branch rule or ruleset | Not proven | Available connector calls do not read branch protection. Repository metadata cannot prove it. |
| Direct-push block | Not proven | This needs an active rule and read-only rule evidence. |

## Blocking findings

### V4 — Completed skill deletion is accepted

The corrected validator supports completed non-skill work, but it has no reliable work-type rule. It infers non-skill work from the absence of the skill directory. A base/head change can delete a completed skill and all evaluation evidence and still pass after it adds a new report.

Effect: a `Done` skill can lose the implementation and evidence that section 16.2 requires the validator to protect.

Required action: add a persistent work-type signal or a base-aware rule. A completed item explicitly identified as a skill must require `skills/<work-id>/SKILL.md`, evaluation cases, and evaluation results. An explicitly identified non-skill governance item must use its own implementation requirements. Add one negative completed-skill deletion test and keep a distinct positive non-skill completion test.

### V3 — Live GitHub enforcement is not proven

The feature branch, pull request, workflow runs, required check, branch rule, and direct-push block do not yet have live evidence. The acceptance criteria for enforced delivery are not complete.

Required action: after V4 is corrected and revalidated, create the feature branch and ready pull request. Prove the workflow on its exact head. Configure or obtain administrator configuration for the rule. Read back the active rule. Do not merge until it requires `repository-governance` and blocks direct unvalidated pushes.

## Findings closed

| Earlier finding | Result | Evidence |
| --- | --- | --- |
| V1 — N1–N9 false negatives | Closed for the nine named cases | All nine negative regressions now fail with stable check IDs. The full 28-test suite passed twice. V4 is a separate work-type defect found during this revalidation. |
| V2 — task-list identity and status | Closed | Version 0.3 has the exact validated hash and uses honest provisional statuses. |
| V3 — live enforcement | Open | No live enforcement evidence exists. |

## Residual risks

| Risk | Effect | Next control |
| --- | --- | --- |
| Administrators can change or bypass GitHub branch rules. | Repository files cannot make protection permanent. | Read the active rule before merge and add a periodic audit if needed. |
| Markdown parsing can miss semantic contradictions. | Correct structure can contain stale prose. | Add a regression test for each demonstrated parser miss. |
| Skill behavior evidence is self-evaluated. | Routing and generated state quality can vary. | Run an independent forward evaluation before a stronger behavior claim. |
| Status evidence depends on the writer. | A correct format can contain an incorrect claim. | Require direct commit, workflow, rule, command, or file evidence. |
| The local folder has no git metadata. | This report cannot validate the actual feature-branch diff or merge-base immutability against GitHub. | Repeat base/head validation on the pushed branch. |

## Decision

The corrected local implementation fails revalidation. The requested 28 tests pass twice, G1–G15 pass, N1–N10 pass, newest delivery-report precedence works, completed non-skill work is accepted, task-list version 0.3 has the exact validated hash, and current statuses are honest. However, the non-skill support uses unsafe absence-based classification and permits deletion of a completed skill. Live GitHub enforcement is also unproven.

Do not set governance to `Implemented`, `Complete`, or `Done`. Do not merge. Correct V4, add a new immutable implementation validation report, and then complete the live controls for V3.
