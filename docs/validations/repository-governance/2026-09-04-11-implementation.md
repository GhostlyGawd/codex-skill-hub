# Repository Governance — Sequence 11 Implementation Revalidation

Version: 1.0  
Date: 2026-09-04  
Work ID: `repository-governance`  
Result: Fail  
Evaluator: Independent Codex subagent

Validated artifacts: [Specification version 0.2](../../specs/repository-governance/spec.md), [task list version 0.8](../../plans/repository-governance/tasks.md), local candidate snapshot SHA-256 `63669ad12dfd3a17d8ea89af37e80c71ee077b6168770a8270e8d97cec10295a`, and live feature tree `c9cba765815c5ff8f22eb9f179e5d5ded454e7dc` at commit `2d2bec66099d6b6e70ce5541a3df05c82dbb3ae4`.

This report follows and preserves validation reports 03 through 10. It does not overwrite or replace them. It becomes immutable when it first enters the default branch.

## Result summary

Local implementation result: Pass.

Live pull-request check result: Pass for feature head `2d2bec66099d6b6e70ce5541a3df05c82dbb3ae4`.

Overall enforcement result: Fail. The sole blocking finding is V3 because `main` is unprotected, has no required check, and has no rule that blocks direct pushes.

## Method

The evaluator:

- Verified task-list version 0.8 by its exact SHA-256.
- Inspected the validator, all test fixtures, current status artifacts, the specification, task list, workflow, pull-request template, README, migrated skill evidence, and reports 03 through 10.
- Ran full-tree validation.
- Ran the full 30-test suite twice.
- Ran the V4 completed-skill deletion test and the T6 genuine non-skill test together.
- Ran the `project-state-curator` package validator.
- Used read-only GitHub calls to inspect pull request 2, its head commit and tree, workflow run `33913148787`, workflow job `101154120077`, `main`, and repository rulesets.
- Made no GitHub mutation.

## Artifact identity and immutability

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| Task list version 0.8 | `1331cedf529a80f21d0b766cb677c8bbf1a4f16c0aab9df5e18d9ddba451a3b4` | Exact match |
| Report 03 | `1fddff76790b48466397c36a0cfa0ccebcad652e7094791801ac5e896d409089` | Present and unchanged during this validation |
| Report 04 | `8d268ba3dbd96f5e68c307c13a3d2aa4975114b95077f4a8eff028e729e4882e` | Present and unchanged during this validation |
| Report 05 | `d444485f962d2c78ec52eb6014a05cc815617bd271cba74046659377de0ac4ff1` | Present and unchanged during this validation |
| Report 06 | `eba3eb83cff9d8d5669458966d49a1c83fbacbaad0dfdc7bc7d19df71e994788` | Present and unchanged during this validation |
| Report 07 | `a63f7262a05569003bf149138a3d1e0ce05978156608bad7e2ca5579111eb1b2` | Present and unchanged during this validation |
| Report 08 | `6822552a784dbbbb04e1375cd52050035895a05dcb8ffb0169a1042a40511a9e` | Present and unchanged during this validation |
| Report 09 | `7e2df7d4d5885d5bf9419594904024fbd1de492a072ade44a4ec817406fc8e0d` | Present and unchanged during this validation |
| Report 10 | `b5d05c85d8fc86e1111ba2d640937d1b5b96f2fa5f6b5adfe0870cbb2d28195c` | Present and unchanged during this validation |

## Local evidence

| Check | Command | Result | Evidence |
| --- | --- | --- | --- |
| Full-tree validator | `python tools/validate_repository.py --all` | Pass | Exit 0; 0 errors and 0 warnings at 2026-09-04T19:56:23Z. |
| Full suite, run 1 | `python -m unittest discover -s tests/repository_validation -v` | Pass | 30 tests passed in 2.582 seconds. |
| Full suite, run 2 | Same command | Pass | 30 tests passed in 2.484 seconds at 2026-09-04T19:56:26Z. |
| V4 and T6 targeted tests | `python -m unittest tests.repository_validation.test_validator.IndependentFindingRegressionTests.test_v4_base_completed_skill_cannot_be_reclassified_by_deletion tests.repository_validation.test_validator.IndependentFindingRegressionTests.test_t6_non_skill_work_is_non_skill_from_initial_creation -v` | Pass | 2 tests passed in 0.174 seconds. |
| Skill package | `python /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/project-state-curator` | Pass | Exit 0; `Skill is valid!` |
| G1–G15 | Named fixture tests in both full runs | Pass | All 15 required fixtures passed, including all required variants. |
| N1–N9 | Named regression tests in both full runs | Pass | Each invalid fixture failed for its stable expected check ID. |
| Newest delivery evidence | N6 regression and code inspection | Pass | A newer failed implementation report overrides an older pass and produces `GOV-LATEST-VALIDATION`. |
| Completed skill preservation | V4 base/head regression | Pass | Deletion and reclassification produce `GOV-COMPLETED-SKILL-PRESERVATION`. |
| Genuine non-skill completion | T6 positive fixture | Pass | Governance work created as non-skill work exits 0 without a skill package or skill evaluation. |
| Status consistency | Manual inspection and full-tree validation | Pass | State, backlog, roadmap, specification, and task list do not claim completed enforcement or merge. |

## Live GitHub evidence

Read-only inspection was current during this validation.

| Control | Result | Evidence |
| --- | --- | --- |
| Feature commit | Pass | `2d2bec66099d6b6e70ce5541a3df05c82dbb3ae4`, tree `c9cba765815c5ff8f22eb9f179e5d5ded454e7dc`, parent `75d57ec8a52f49eadd007fb7206880f27c7884aa`. |
| Pull request 2 | Pass | [Pull request 2](https://github.com/GhostlyGawd/codex-skill-hub/pull/2) is open, ready, not draft, mergeable, based on `main`, headed by the named feature commit, and not merged. |
| Workflow run | Pass | Run `33913148787`, run number 1, is complete with conclusion `success` for the feature head. |
| Stable check job | Pass | Job `101154120077` is named `repository-governance` and completed with conclusion `success`. Its test and pull-request validation steps passed. |
| Default branch | Pass | `main` remains at `75d57ec8a52f49eadd007fb7206880f27c7884aa`. Pull request 2 is not merged. |
| Classic branch status | Fail for enforcement | The branch response reports `protected: false` and `protection.enabled: false`. |
| Required checks | Fail for enforcement | The branch response reports enforcement level `off`, with empty contexts and checks. |
| Repository rulesets | Fail for enforcement | `GET /repos/GhostlyGawd/codex-skill-hub/rulesets` returned `[]`. |
| Direct-push block | Fail for enforcement | No active classic protection or ruleset blocks a direct push. |

The successful workflow is advisory. It does not make the check required.

## Prior finding closure

| Finding | Status | Evidence |
| --- | --- | --- |
| V1 — N1–N9 false negatives | Closed | All named regressions pass in both 30-test runs. |
| V2 — task-list identity and status | Closed | Task list version 0.8 matches SHA-256 `1331cedf529a80f21d0b766cb677c8bbf1a4f16c0aab9df5e18d9ddba451a3b4` and has passing report 10. |
| V4 — completed skill deletion accepted | Closed | The merge-base-aware V4 negative test passes with `GOV-COMPLETED-SKILL-PRESERVATION`. |
| T6 — non-skill positive fixture was not genuine | Closed | The T6 fixture creates non-skill governance work from its first file and passes. |
| T7 — branch inspection blocker was stale | Closed | Read-only inspection now proves the exact no-rule state. Task 1.3 is `Done`, and task 1.4 is `Ready`. |
| V3 — live enforcement absent | Open and blocking | `main` is unprotected, required checks are empty, and the ruleset list is empty. |

## Blocking finding

### V3 — The successful governance check is not required

The workflow and stable job pass on pull request 2, but no GitHub rule requires that check. `main` is not protected, and no ruleset blocks direct unvalidated pushes.

Effect: a user with push or merge authority can bypass the advisory check. Specification sections 15, 18, and 22 are not fully implemented.

Required action: configure the minimum active rule for `main`. It must require a pull request, require check `repository-governance`, and block direct pushes that bypass the check. Preserve any stronger control. Then read the rule back and record its identifier, branch, check, enforcement conditions, inspection source, and UTC time.

V3 is the sole blocking implementation finding in this report.

## Required next actions

1. Have an administrator or authorized GitHub tool configure the required `main` rule.
2. Read back the active rule and confirm the required check and direct-push control.
3. Update the pull-request head with the current task list and sequence 11 report.
4. Run the workflow again on that exact final head.
5. Add a newer implementation validation report that closes V3. Preserve this failed report.
6. Merge only after the rule is active and the final-head check passes.

## Residual risks

| Risk | Effect | Next control |
| --- | --- | --- |
| Administrators can later change or bypass rules. | Enforcement can weaken after validation. | Inspect the active rule before merge and add a periodic audit if needed. |
| Markdown parsing can miss a semantic contradiction. | Correct structure can contain stale meaning. | Add a regression for each demonstrated parser miss. |
| Skill behavior evidence is self-evaluated. | Routing and generated state quality can vary. | Run an independent forward evaluation before a stronger behavior claim. |
| Status evidence depends on the writer. | A valid format can contain an incorrect claim. | Require direct commit, run, rule, command, or file evidence. |
| The local folder has no git metadata. | Local `--base` and `--head` cannot inspect the live feature diff. | Use the successful GitHub run for the current feature head and repeat it after the final evidence commit. |

## Findings

No local validator, test, migration, status, V4, T6, or T7 defect remains in the inspected candidate. The only blocking finding is V3.

## Decision

The local implementation passes. The live workflow and stable job pass on the recorded feature head. Overall repository governance fails enforcement because GitHub does not require the check and does not block direct pushes.

Keep governance `Blocked`. Do not merge pull request 2 until V3 is closed and the exact final head has a successful `repository-governance` check.
