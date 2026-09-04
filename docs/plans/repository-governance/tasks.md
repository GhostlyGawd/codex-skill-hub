# Repository Governance and Artifact Synchronization — Implementation Task List

Version: 0.9  
Status: Validated  
Date: 2026-09-04  
Work ID: `repository-governance`

Specification: [Specification version 0.3](../../specs/repository-governance/spec.md)

Earlier task-list validation: [Version 0.2 validation](../../validations/repository-governance/2026-09-04-02-task-list.md)  
Version 0.3 task-list validation: [Passing report](../../validations/repository-governance/2026-09-04-04-task-list.md)  
Failed version 0.4 task-list validation: [T6 report](../../validations/repository-governance/2026-09-04-06-task-list.md)  
Version 0.5 task-list validation: [Passing report](../../validations/repository-governance/2026-09-04-07-task-list.md)  
Failed version 0.6 task-list validation: [T7 report](../../validations/repository-governance/2026-09-04-08-task-list.md)  
Historical version 0.7 task-list validation: [Passing report](../../validations/repository-governance/2026-09-04-09-task-list.md)  
Failed implementation validations: [First report](../../validations/repository-governance/2026-09-04-03-implementation.md) and [V4 report](../../validations/repository-governance/2026-09-04-05-implementation.md)  
Historical task-list validation: [Version 0.8 validation](../../validations/repository-governance/2026-09-04-10-task-list.md)

Supplemental validation: [Version 0.3 specification and version 0.9 task-list preflight review](../../validations/repository-governance/2026-09-04-12-specification-task-list-preflight.md)

The version 0.8 plan retains its historical validation. The bounded version 0.9 amendment passed the linked independent scoped review. This document is `Validated`, not `Complete`. Existing task IDs, dependencies, and statuses remain unchanged. Supplemental checklist completion is reviewed manually; the current validator does not parse its bullet statuses.

## Execution controls

- Build mode: Autonomous.
- Pull requests: Ready for review. Do not use draft pull requests.
- Git cadence: Make a candidate commit before the pull request. Make later commits only for validation evidence, status reconciliation, or demonstrated defects.
- Verification: Stop external delivery at each checkpoint. Reversible local preparation can continue while an external checkpoint is blocked, but each prepared task stays `Pending` until its dependency chain passes.
- Scope: Change only governance artifacts and the migrated `project-state-curator` planning artifacts.
- Merge: Merge is a delivery gate. It is not a task that must be complete before its own pull request merges.

## Version 0.3 corrections

This version responds to the immutable failed implementation report dated 2026-09-04.

- Add regression work for missing state sections, roadmap controls, control-artifact links, report-result integrity, newest delivery evidence, calendar dates, review status, artifact identity, and non-skill completion.
- Keep local work after task 1.3 as provisional `Pending` work. Local file presence does not satisfy a blocked dependency.
- Keep live branch rules, workflow runs, pull-request delivery, and enforcement evidence blocked or pending until GitHub evidence exists.
- Use a new report for each revalidation. Do not change the failed implementation report.

## Version 0.4 corrections

This version responds to blocking finding V4 in the immutable 2026-09-04 sequence 05 report.

- Add a merge-base-aware completed-skill identity check. A work ID that is `Done` in the base and has skill or evaluation evidence stays a skill in the head.
- Require the head to preserve its skill package, evaluation cases, evaluation result, and specification links.
- Keep genuine non-skill work valid when the base does not identify it as a completed skill.
- Add one negative base/head deletion regression and retain the positive non-skill regression.
- Keep all prepared local work `Pending` behind the blocked external checkpoint. V3 remains open.

## Version 0.5 corrections

This version responds to blocking finding T6 in the immutable 2026-09-04 sequence 06 report.

- Add a separate positive fixture for `repository-governance` as non-skill work from its initial creation.
- Give that fixture only validator, task, specification, and governance validation evidence. It never contains a work-specific skill package, evaluation directory, skill link, or skill output path.
- Keep the V4 negative merge-base test for deletion of a completed skill.
- Keep local results provisional and keep V3 open.

## Version 0.6 reconciliation

This version records completion of live task 1.2 without changing the governance delivery status.

- Record branch `feat/repository-governance` at verified base commit `75d57ec8a52f49eadd007fb7206880f27c7884aa`.
- Set only task 1.2 to `Done` with direct branch evidence.
- Keep task 1.3 and V3 blocked because no exposed tool can inspect or change branch rules.
- Keep all dependent local preparation tasks `Pending`.

## Version 0.7 reconciliation

This version responds to blocking finding T7 and records the live read-only inspection at 2026-09-04T19:43:55Z UTC.

- Record that `main` reports `protected: false`, protection disabled, and no required checks.
- Record that the repository ruleset list is empty.
- Treat the classic protection-detail 403 as an endpoint restriction, not as absence of the other read-only evidence.
- Set task 1.3 to `Done` and task 1.4 to `Ready`.
- Keep task 6.5 and V3 blocked because no exposed tool can configure the missing rule.
- Keep tasks 2.1 and later `Pending`.

## Version 0.8 reconciliation

This version records live feature-branch delivery evidence without claiming merge or branch protection.

- Record feature commit `2d2bec66099d6b6e70ce5541a3df05c82dbb3ae4` and tree `c9cba765815c5ff8f22eb9f179e5d5ded454e7dc`.
- Record ready pull request 2 and successful workflow run `33913148787`, run number 1.
- Keep tasks 6.2 through 6.4 `Pending` because their formal dependency chain is not complete. The output evidence is provisional until tasks 1.4 through 6.1 pass in order.
- Do not claim a merge, active branch rule, required-check rule, direct-push block, or default-branch run.
- Keep task 6.5, V3, backlog, and roadmap `Blocked`.

## Status model

Version 0.9 adds the supplemental checklist below and corrects obsolete current evidence in tasks 2.1, 6.1, and 6.6. Local preparation and historical passing checks do not close the live V3 blocker. Earlier version sections describe historical changes, not current authorization to bypass the preflight.

| Status | Meaning |
| --- | --- |
| `Pending` | An earlier task must finish first. |
| `Ready` | All dependencies are complete. Work can start. |
| `In progress` | Work is active. |
| `Blocked` | A named dependency stops the task. |
| `Done` | The output exists and the verification passed. |

## Phase 0 — Approved design and task validation

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | Write the repository-governance specification. | `docs/specs/repository-governance/spec.md` version 0.2 | The file contains the approved scope, rules, failure behavior, and acceptance criteria. | None | Done | Historical baseline version 0.2 passed report 01; the current file extends that baseline with version 0.3 section 24, reviewed separately in report 12. |
| 0.2 | Validate the specification with an independent subagent. | `docs/validations/repository-governance/2026-09-04-01-specification.md` | The report has result `Pass with residual risk` and has no blocking finding. | 0.1 | Done | The report identifies the evaluator, method, corrections, evidence, and three residual risks. |
| 0.3 | Decompose the validated specification into ordered implementation work. | Initial `docs/plans/repository-governance/tasks.md` version 0.1 | Every implementation area in specification sections 7 through 22 has an output, dependency, and observable verification. | 0.2 | Done | Version 0.1 contained the required task columns, checkpoints, critical path, and delivery gates. |
| 0.4 | Validate this task list with an independent subagent and record demonstrated defects. | `docs/validations/repository-governance/2026-09-04-02-task-list.md` | The report identifies the corrected task-list version 0.2, has result `Pass` or `Pass with residual risk`, and has no blocking finding. | 0.3 | Done | The independent report validates version 0.2 after four narrow corrections and has no blocking finding. |
| 0.5 | Apply only corrections demonstrated during task-list validation and link the passing report. | `docs/plans/repository-governance/tasks.md` version 0.2 | The report records each correction; this file links to the report and has status `Validated`. | 0.4 | Done | Version 0.2 corrects validation-path normalization, deterministic evidence identifiers, complete fixture variants and residual-risk traceability, and branch-rule mutation controls. |

Checkpoint A: The specification and task list have independent passing validation reports. No blocking finding remains.

## Phase 1 — Establish the implementation baseline

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 | Inspect the live GitHub default branch, repository instructions, current files, and open pull requests. | Baseline fields in this task's `Evidence` cell | The evidence names the repository, default branch, head commit, applicable instructions, open pull requests, unrelated changes, inspection time, and read-only tool or API source. | 0.5 | Done | GitHub baseline on 2026-09-04 UTC: `GhostlyGawd/codex-skill-hub`; default `main`; head `75d57ec8a52f49eadd007fb7206880f27c7884aa`; tree `3876c36807edc3834d0b46a5f46c45f4ce6958f1`; verified signature; pull request 1 merged; root `README.md`, `skills/`, `evaluations/`; no repository instruction file reported; connected user has admin and push permission. Read-only GitHub connector evidence was supplied by the baseline subagent. |
| 1.2 | Create branch `feat/repository-governance` from the current default-branch head. | Branch `feat/repository-governance` and its base SHA in this task's `Evidence` cell | The branch base equals the inspected default-branch head and contains no unrelated commit. | 1.1 | Done | On 2026-09-04 UTC, live GitHub task execution created `feat/repository-governance` from verified `main` commit `75d57ec8a52f49eadd007fb7206880f27c7884aa`. No unrelated base commit was introduced. |
| 1.3 | Inspect current GitHub branch rules without changing them. | Branch-rule baseline fields in this task's `Evidence` cell | The evidence names the repository, branch, rule identifier if present, required checks, inspection time, and read-only tool or API source. | 1.2 | Done | `GhostlyGawd/codex-skill-hub`, branch `main`, inspected 2026-09-04T19:43:55Z UTC. `GET /repos/GhostlyGawd/codex-skill-hub/branches/main` reported `protected: false`, protection disabled, and no required checks. `GET /repos/GhostlyGawd/codex-skill-hub/rulesets` returned `[]`; rule identifier: none. The classic protection-detail GET returned 403 and did not erase the branch and ruleset evidence. |
| 1.4 | Normalize both governance validation-report paths and all affected links before the reports become immutable on the default branch. | `docs/validations/repository-governance/2026-09-04-01-specification.md` and `docs/validations/repository-governance/2026-09-04-02-task-list.md` | Both reports preserve their validated content, the old non-canonical paths are absent, and all affected relative links resolve with exact case. | 1.3 | Ready | Dependency 1.3 is complete. Local canonical paths and links are prepared for verification. |

Checkpoint B: The work uses a current branch, the initial external-rule state is known, and the governance design artifacts use canonical paths.

## Phase 2 — Migrate and reconcile project-control artifacts

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1 | Create the canonical current-state file from the external state input. Remove stale facts. | `STATE.md` | The file has all required sections, identifies governance as active work, records that `project-state-curator` is merged, and does not show repository selection as a current blocker. | 1.4 | Pending | Local output is prepared and passed `--all` in report 11. Task 1.3 is complete; formal completion waits for verification of task 1.4. Live enforcement remains blocked separately at task 6.5. |
| 2.2 | Create the canonical backlog from the external backlog input. | `BACKLOG.md` | The table has every required column and one unique row per work ID. `project-state-curator` is `Done`; Batch 1 keeps `bug-repro-builder` and `change-impact-mapper` at evidence-based statuses. | 2.1 | Pending | Local output is prepared: the completed skill is `Done`, both later Batch 1 skills are `Backlog`, and governance is `Blocked`. |
| 2.3 | Create the canonical roadmap and batch completion rules. | `ROADMAP.md` | Each row has the required columns; each status derives from `BACKLOG.md`; Batch 1 order is preserved; and each batch has a completion rule. | 2.2 | Pending | Local output is prepared and its status mapping passes `--all`. |
| 2.4 | Import and reconcile the `project-state-curator` specification. | `docs/specs/project-state-curator/spec.md` | Metadata is canonical, status agrees with the merged implementation, the obsolete repository dependency is historical or removed from current status, and links point to the task list, skill, evaluation, and validation evidence. | 2.3 | Pending | Local version 1.0 is prepared with `Implemented` status and links to tasks, skill, evaluation, and three reports. |
| 2.5 | Import and reconcile the `project-state-curator` task list. | `docs/plans/project-state-curator/tasks.md` | The required columns exist; completed implementation tasks are `Done` with output and verification evidence; the old target-selection blocker is not current; and the file links to its specification. | 2.4 | Pending | Local version 1.0 is prepared with 27 `Done` tasks and evidence from pull request 1 and the retained evaluation. |
| 2.6 | Import the historical `project-state-curator` specification validation. | `docs/validations/project-state-curator/2026-09-04-01-specification.md` | The report preserves its date, findings, dependency context, and original result text; adds `Original result`; maps the standard `Result` to `Pass with residual risk`; explains the mapping; and marks the resolved dependency as historical. | 2.5 | Pending | Local imported report preserves `Original result: Pass with one implementation dependency` and explains its mapping. |
| 2.7 | Import the historical `project-state-curator` task-list validation. | `docs/validations/project-state-curator/2026-09-04-02-task-list.md` | The report preserves its date, findings, dependency context, and original result text; adds `Original result`; maps the standard `Result` to `Pass with residual risk`; explains the mapping; and marks the resolved dependency as historical. | 2.6 | Pending | Local imported report preserves `Original result: Pass with one external start blocker` and explains its mapping. |
| 2.8 | Add migration validation for `project-state-curator`. | `docs/validations/project-state-curator/2026-09-04-03-migration.md` | The report has all required metadata and identifies its method, scope, evidence, result, findings, and residual risks. It checks the imported artifacts against the merged skill and evaluation files and preserves the non-independent evaluation and model-variance residual risk. | 2.7 | Pending | Local migration report is prepared with `Pass with residual risk` and preserves the non-independent evaluation limit. |
| 2.9 | Reconcile links and statuses across all migrated control artifacts. | Synchronized artifacts and the link-and-status matrix in this task's `Evidence` cell | The matrix covers `STATE.md`, `BACKLOG.md`, `ROADMAP.md`, specifications, plans, and validation reports and has no missing artifact, duplicate work ID, stale current blocker, or contradictory status. | 2.8 | Pending | Local matrix: state=present; backlog=present; roadmap=present; specs=2; plans=2; reports=6; duplicate work IDs=0; stale repository-selection blocker=0; `--all` link and status errors=0. |

Checkpoint C: All durable control artifacts are inside the repository. Current status agrees with merged evidence. Historical evidence keeps its original context.

## Phase 3 — Implement the deterministic repository validator

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 | Create the read-only command interface and repository-root checks. | `tools/validate_repository.py` with `--all`, `--base`, and `--head` arguments | Valid arguments select the correct mode. Invalid arguments, repository roots, or git references exit with code 2. The command does not write a file. | 2.9 | Pending | Local validator is prepared; contract tests verify both modes, exit 2, and unchanged fixture files. |
| 3.2 | Parse canonical Markdown metadata, tables, work IDs, versions, dates, and statuses with the Python standard library. | Metadata and table validation functions | Valid documents parse. Missing fields, renamed required columns, invalid formats, invalid work IDs, and invalid statuses produce stable check IDs. | 3.1 | Pending | Local parser functions use only the Python standard library and emit stable `GOV-*` IDs. |
| 3.3 | Validate required paths, exact-case relative links, and forbidden placeholders. | Structure, link, and placeholder checks | Missing canonical paths, broken links, case errors, and forbidden active-artifact placeholders each produce an error. Specification code examples remain exempt. | 3.2 | Pending | Local checks are prepared and fixtures G4 and G5 pass. |
| 3.4 | Validate task dependencies, concurrency markers, output evidence, and completion conditions. | Task-graph and evidence checks | Unknown or incomplete dependencies, cycles, unsupported concurrent work, and `Done` rows without evidence each produce an error. | 3.3 | Pending | Local checks are prepared; G2, G14, and G15 pass. The task graph reports unknown dependencies, incomplete dependencies, and cycles. |
| 3.5 | Validate backlog, roadmap, specification, task-list, and validation-report agreement. | Cross-artifact lifecycle checks | Every status transition and required link in specification sections 9 through 12 either passes or produces a stable check ID. | 3.4 | Pending | Local lifecycle checks are prepared; G2, G3, G11, G12, and G13 pass. |
| 3.6 | Validate skill implementation, evaluation evidence, report contents, and newest applicable validation. | Delivery-evidence checks | Completed work without implementation, evaluation, required report sections, or current passing evidence produces an error. | 3.5 | Pending | Local delivery checks are prepared and G8, G12, and G13 pass. |
| 3.7 | Classify changed files and enforce every applicable synchronization rule. | Change classifier and synchronization checks | Each change class in specification section 14 is recognized. A multi-class change must pass all applicable rules. | 3.6 | Pending | Local changed-file classifier covers new skill, skill behavior, evaluation, governance, and multi-class changes. Contract and G8/G9 tests pass. |
| 3.8 | Protect validation-report immutability by merge-base comparison. | Git comparison checks for `--base` and `--head` | A changed, deleted, or renamed validation report that exists at the merge base produces an error. An unreadable base stops the check with exit code 2. | 3.7 | Pending | Temporary-git tests G6, both G7 variants, G10, and invalid refs pass. |
| 3.9 | Add stable diagnostic output, aggregate findings, and defined exit codes. | Complete validator output contract | Each finding uses `<LEVEL> <CHECK-ID> <path>: <message>`. Safe checks continue after an error. The summary counts errors and warnings. Exit codes are 0, 1, or 2 as specified. | 3.8 | Pending | Local output contract is prepared; aggregation and exit-code tests pass. |

Checkpoint D: The validator covers structure, links, lifecycle, evidence, synchronization, and immutability. It is deterministic and read-only.

## Phase 4 — Build validator fixtures and tests

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 4.1 | Create a standard-library test harness that uses isolated temporary git repositories. | `tests/repository_validation/` test harness and fixture builders | Test setup and teardown leave the main repository unchanged. Ref-comparison tests use real temporary commits. | 3.9 | Pending | Local harness is prepared with temporary directories and real temporary git commits. |
| 4.2 | Add fixtures G1 through G5 for a valid tree, task status, roadmap status, links, and placeholders. | Tests for G1–G5 | G1 exits 0. G2–G5 exit 1 and assert the expected stable check IDs. | 4.1 | Pending | Local G1–G5 fixtures pass, including broken and wrong-case link variants. |
| 4.3 | Add fixtures G6 through G10 for immutable reports and synchronized skill changes. Include deletion and rename variants for G7 and missing-specification and missing-evaluation variants for G8. | Tests for G6–G10 | Every negative variant exits 1 with its expected stable check ID. G10 exits 0 and preserves the earlier report. | 4.2 | Pending | Local G6–G10 fixtures pass; G7 has delete and rename variants, and G8 has missing-specification and missing-evaluation variants. |
| 4.4 | Add fixtures G11 through G15 for blockers, completion, specification evidence, task evidence, and concurrency. | Tests for G11–G15 | G11, G13, G14, and G15 exit 1 with expected check IDs. G12 exits 0. | 4.3 | Pending | Local G11–G15 fixtures pass with the specified positive and negative results. |
| 4.5 | Add focused tests for command errors, finding aggregation, exact-case paths, changed-file multi-class handling, and read-only behavior. | Validator contract regression tests | The tests prove exit code 2 cases, multiple findings in one run, exact-case checks, all-class enforcement, and an unchanged working tree. | 4.4 | Pending | Three local contract tests pass and verify command errors, aggregation, exact case, multi-class checks, and unchanged file hashes. |
| 4.6 | Run the complete G1–G15 and contract test suite and correct demonstrated defects. | Exact command, both run times, exit codes, and summaries in this task's `Evidence` cell | All G1–G15 and contract tests pass in one command. A second run gives the same result. | 4.5 | Pending | Earlier local runs passed 18 tests. Formal completion waits for the blocked dependency chain. |
| 4.7 | Correct independent findings N1–N10 and add regression tests. | `tools/validate_repository.py` and `tests/repository_validation/test_validator.py` | The validator rejects N1–N9, accepts completed non-skill work in N10, retains G1–G15, and the full 28-test suite passes twice. | 4.6 | Pending | Provisional local runs: 28 tests passed at 2026-09-04T19:20:45Z and again at 2026-09-04T19:20:48Z. Formal completion waits for the blocked dependency chain. |
| 4.8 | Correct V4 and T6 with explicit negative and positive work-type fixtures. | `tools/validate_repository.py` and `tests/repository_validation/test_validator.py` | `test_v4_base_completed_skill_cannot_be_reclassified_by_deletion` fails the invalid head with `GOV-COMPLETED-SKILL-PRESERVATION`. `test_t6_non_skill_work_is_non_skill_from_initial_creation` creates governance work with only non-skill outputs and evidence, and `--all` exits 0. All earlier tests pass. | 4.7 | Pending | Provisional local result: 30 tests passed at 2026-09-04T19:36:43Z and again at 2026-09-04T19:36:45Z. Both distinct targeted tests passed at 2026-09-04T19:36:48Z. The positive fixture has no work-specific skill package, evaluation directory, skill link, or skill output identity. Formal completion waits for the blocked dependency chain and version 0.5 validation. |

Checkpoint E: All positive fixtures pass. All negative fixtures fail for the expected stable check IDs. Each major enforcement group has a negative proof.

## Phase 5 — Add continuous integration and contributor controls

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 5.1 | Add the repository validation workflow. | `.github/workflows/validate-repository.yml` | Pull requests to the default branch use full history and `--base`/`--head`; default-branch pushes use `--all`; tests run in both paths; permissions are read-only; no stored secret is used; and the stable job name is `repository-governance`. | 4.8 | Pending | Local workflow is prepared with full history, Python 3.12, read-only contents, concurrency cancellation, both validator modes, tests, and stable job name. |
| 5.2 | Add the ready pull-request template. | `.github/pull_request_template.md` | The template requests every field in specification section 19 and states that the pull request is ready and is not a draft. | 5.1 | Pending | Local template is prepared with all section 19 fields and a ready, non-draft statement. |
| 5.3 | Update contributor guidance. | `README.md` | The README explains the canonical artifact structure, source of truth, local test command, validator commands, pull-request rule, and validation-report immutability. | 5.2 | Pending | Local README is prepared with the canonical structure, commands, ready-PR rule, and immutable-report rule. |
| 5.4 | Run local full-tree validation and the complete test suite. | Exact commands, UTC time, exit codes, and result summaries in this task's `Evidence` cell | Tests pass and `python tools/validate_repository.py --all` exits 0 on the migrated candidate tree. | 5.3 | Pending | Provisional T6-corrected result at 2026-09-04T19:36:48Z: `python tools/validate_repository.py --all` exited 0 with 0 errors and 0 warnings; the two adjacent full-suite runs each passed 30 tests. |

Checkpoint F: The repository can enforce the rules locally and in GitHub Actions. Contributor instructions match the enforced workflow.

## Phase 6 — Prove enforcement and prepare delivery

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 6.1 | Review the candidate diff and record the exact validation commands and results. | Diff scope, commands, UTC time, exit codes, and result summaries in this task's `Evidence` cell | The diff contains only governance work and migrated planning artifacts. All local checks pass. | 5.4 | Pending | Report 11 records a passing full-tree check and two passing 30-test runs for its identified candidate. The feature branch and ready PR 2 exist. This local directory has no `.git` metadata, so exact current base/head diff evidence must come from authorized GitHub inspection and the current workflow. Formal completion still waits for task 5.4; earlier results do not validate later amendments. |
| 6.2 | Commit and push the reviewed candidate only to the governance feature branch. | Remote branch name and candidate commit SHA in this task's `Evidence` cell | The remote branch contains the reviewed tree and is based on the recorded default-branch head or has been safely updated without overwriting unrelated work. | 6.1 | Pending | Historical snapshot in report 11: feature commit `2d2bec66099d6b6e70ce5541a3df05c82dbb3ae4`, tree `c9cba765815c5ff8f22eb9f179e5d5ded454e7dc`. Use [live PR 2](https://github.com/GhostlyGawd/codex-skill-hub/pull/2) for the current head; this snapshot is not later-head evidence. Formal completion waits for task 6.1 and current base/head validation. |
| 6.3 | Open a ready pull request with the required body fields. | Pull-request number and URL in this task's `Evidence` cell | The pull request is not a draft. Its body identifies the work ID, change classes, scope, specification, tasks, validation, status changes, and residual risks. | 6.2 | Pending | Provisional live output: ready, non-draft pull request 2 exists at `https://github.com/GhostlyGawd/codex-skill-hub/pull/2`. Formal completion waits for task 6.2 and verification of all required body fields. |
| 6.4 | Verify the pull-request workflow and stable check name on GitHub. | Workflow run ID, URL, base SHA, head SHA, and check result in this task's `Evidence` cell | The pull request run completes, uses the expected base and head commits, and exposes `repository-governance`. | 6.3 | Pending | Historical snapshot in report 11: workflow `Repository governance`, run `33913148787`, run number 1, succeeded for the report's named head. Use [live PR 2](https://github.com/GhostlyGawd/codex-skill-hub/pull/2) for current checks. Formal completion waits for task 6.3 and exact current base, head, and stable-check evidence; an earlier run cannot satisfy a later head. |
| 6.5 | Configure the minimum required protection for the exact recorded default branch, preserve all stronger existing controls, and inspect the result. Do not delete or weaken an existing rule. | Before-and-after rule identifiers, required checks, UTC time, and read-only inspection source in this task's `Evidence` cell | The active rule requires `repository-governance`, requires a pull request, blocks direct pushes that bypass the check, and preserves every stronger control recorded in task 1.3. | 6.4 | Blocked | Blocker: inspection proved that no active rule protects `main`, and no branch-rule mutation tool is exposed. An administrator or authorized GitHub tool must configure the narrow rule and provide read-back evidence. |
| 6.6 | Revalidate the complete implementation with an independent subagent. Preserve all earlier failed reports. | Existing `docs/validations/repository-governance/2026-09-04-11-implementation.md` and a later implementation report after V3 closure | The later report identifies the validated tree, method, scope, evidence, result, findings, branch-rule evidence, closure of V1–V4, T6, T7, and every residual risk in specification section 23. Result is `Pass` or `Pass with residual risk` with no blocking finding. | 6.5 | Pending | Report 11 exists and records local implementation Pass but overall Fail because V3 remains open. Preserve reports 03, 05, and 11. Version 0.8 task-list validation already passed in report 10. A later full implementation validation waits for live enforcement evidence and must validate the then-current exact head; supplemental amendment review does not close V3. |
| 6.7 | Reconcile proposed final status across `STATE.md`, `BACKLOG.md`, `ROADMAP.md`, the governance specification, and this task list. Run the full local checks again. | Proposed post-merge canonical state | Governance is `Done`/`Complete`/`Implemented` as applicable; all task rows are `Done` with evidence; links select the newest passing reports; the next action starts `bug-repro-builder`; tests pass; and `--all` exits 0. | 6.6 | Pending | Final status depends on passing implementation validation. |

Checkpoint G: The proposed final state is synchronized, independently validated, and protected by an active GitHub rule. Local checks pass.

## Supplemental checklist — Version 0.9 preflight controls

This is bounded local preparation for specification section 24. It does not renumber the existing task graph, complete a blocked dependency, or authorize external writes without the required preflight. Each item remains `Pending` until its own verification is recorded. All items must pass before the amended candidate can pass the final-head gate.

- Done — P1: Review specification section 24 and this checklist with an independent subagent. Output: the design and task-review portion of the linked supplemental report. Verify the limited scope, permission stop conditions, no bypass, explicit outputs, and separation of local acceptance from V3. Dependency: none; this review gates acceptance of prepared outputs below. Evidence: report 12 records scoped design and decomposition acceptance.
- Done — P2: Prepare and verify `AGENTS.md` and `docs/runbooks/github-enforcement-setup.md`. Check every section 24.1 instruction and the administrator procedure. Confirm that unchanged blockers cause no full test or report loop and that the runbook makes no live-enforcement claim. Dependency: P1. Evidence: report 12 maps section 24.1 to the inspected instructions and runbook.
- Done — P3: Prepare and verify `config/main-ruleset.json`. Compare the template with the official GitHub schema and every section 24.2 setting. Preserve stronger existing controls; make no live rule mutation as part of this local step. Dependency: P2. Evidence: report 12 records independent schema comparison and six passing template tests.
- Done — P4: Prepare `tests/repository_validation/test_ruleset_template.py`, run the template tests and existing suite, and run full-tree validation. Record commands, results, file identities, and test limits in the supplemental report. Do not present template tests as live protection or skill behavioral tests. Dependency: P3. Evidence: report 12 records the 36-test suite, full-tree check, and exact local artifact identities.
- Done — P5: Independently validate the prepared instructions, runbook, template, test evidence, and this amended design and checklist. Complete `docs/validations/repository-governance/2026-09-04-12-specification-task-list-preflight.md` with a scoped result. Reconcile current status without closing V3. Set the specification and plan to `Validated` only after the amendment has no blocking finding. Dependency: P4. Evidence: report 12 accepts only this amendment; V3 and the original delivery task statuses remain unchanged.

The supplemental report can contain the sequential design review and output verification as separate scoped sections before it is committed. Do not rewrite an earlier historical report or create extra reports solely to repeat an unchanged blocker.

## Delivery gates

These gates are not task rows. They do not create a pre-merge dependency cycle.

1. Final-head gate: Commit and push the final evidence and status update. Confirm that the pull request has no unrelated file, all required checks pass on the final head, the validator inspects the complete change, and the branch rule is still active.
2. Merge gate: Merge the ready pull request only when the final-head gate passes. Use the repository merge policy. Do not publish or deploy a skill.
3. Default-branch gate: Confirm that GitHub shows the pull request as merged and that the default-branch push workflow completes with check `repository-governance` passing.
4. Canonical-state gate: Run `python tools/validate_repository.py --all` against the merged default-branch tree. It must exit 0.
5. Evidence gate: Record the pull-request number, merge commit, post-merge workflow run, protected-branch rule ID, and UTC verification time in a new report if the pre-merge implementation report cannot contain final facts. Do not modify a report that is already on the default branch.

Checkpoint H: The merged default branch is canonical, passes full validation, and remains protected from direct unvalidated pushes.

## Critical path

`0.1 → 0.2 → 0.3 → 0.4 → 0.5 → 1.1–1.4 → 2.1–2.9 → 3.1–3.9 → 4.1–4.8 → 5.1–5.4 → 6.1–6.7 → Final-head gate → Merge gate → Default-branch gate → Canonical-state gate → Evidence gate`

## Rollback and stop conditions

- Stop before implementation if task-list validation has a blocking finding.
- Stop migration if evidence cannot resolve a current status. Mark the affected work `Blocked` and name the missing evidence in `STATE.md` and its task list.
- Stop immutability checks if the default branch or merge base cannot be read. Do not claim that historical reports are protected.
- Do not change, rename, or delete a validation report that already exists on the default branch. Add a later report to correct it.
- Do not delete the old external planning files. After migration, treat them only as historical inputs.
- Stop the pull request if the branch contains an unrelated change. Remove the unrelated change without discarding user work.
- Stop merge when a required check fails, is pending, is absent, or cannot inspect the full change.
- Stop merge when the active branch rule does not require `repository-governance` or permits a direct unvalidated push.
- If the required branch rule cannot be configured or read back, do not report full enforcement. Set governance to `Blocked` and name the required administrator action in `STATE.md` and this task list.
- If task 6.5 changes the wrong rule or weakens a recorded control, stop delivery and restore the exact task 1.3 rule state with the narrowest corrective update. Inspect and record the restored state. If safe restoration is not possible, do not make another mutation; report the repository as `Blocked` and name the required administrator action.
- If a merged governance change must be reversed, use a new ready pull request that reverts the specific governance commit. Preserve validation history and run all required checks.
- Do not publish, deploy, or install a skill as part of this work.
