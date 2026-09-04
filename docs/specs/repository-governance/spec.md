# Repository Governance and Artifact Synchronization — Specification

Version: 0.2  
Status: Validated  
Date: 2026-09-04  
Work ID: `repository-governance`

Specification validation: [2026-09-04-01-specification.md](../../validations/repository-governance/2026-09-04-01-specification.md)

Task list: [Implementation task list](../../plans/repository-governance/tasks.md)

## 1. Purpose

This system keeps the planning, implementation, evaluation, and status artifacts in `codex-skill-hub` consistent. It makes the default branch on GitHub the canonical source for project facts. It also blocks a pull request when required artifacts are missing, stale, invalid, or inconsistent.

## 2. Current problem

The repository contains the merged `project-state-curator` skill and its evaluation files. Related planning files are outside the repository. Those files still contain old status data:

- The backlog says that `project-state-curator` is in progress.
- The task list says that repository selection is blocked.
- The specification says that implementation has no selected repository.
- There is no canonical roadmap file.
- There is no automated consistency check.
- There is no repository check that controls merge eligibility.

This separation creates several sources of truth. It can cause later work to use stale facts.

## 3. Goals

The system must:

- Keep all durable project-control artifacts in the repository.
- Make the GitHub default branch the canonical source.
- Give each skill or governance change one stable work ID.
- Link backlog, roadmap, specification, task, evaluation, and validation data.
- Use a small set of defined status values.
- Preserve validation evidence after it enters the default branch.
- Require status updates in the same pull request as the related work.
- Run deterministic checks for structure, links, status, evidence, and synchronization.
- Block merge when a required check fails.
- Keep current state small and remove superseded facts.
- Support ready pull requests. Do not require draft pull requests.

## 4. Non-goals

The system must not:

- Replace GitHub history with a second history system.
- Store secrets, credentials, access tokens, or hidden reasoning.
- Record every command or temporary observation.
- Change files in an unrelated repository.
- Publish a skill to an external registry.
- Merge a pull request when a required check fails or does not run.
- Treat a self-evaluation as an independent model evaluation.
- Rewrite a validation report that is already on the default branch.
- Infer completion from a plan or an open pull request.

## 5. Terms

| Term | Meaning |
| --- | --- |
| Canonical source | The source that controls when two copies conflict. |
| Default branch | The GitHub branch that GitHub marks as the repository default. It is currently expected to be `main`. |
| Work ID | A stable lowercase identifier that uses letters, numbers, and hyphens. A skill normally uses its skill name. |
| Active work | Work with backlog status `Ready`, `In progress`, `Review`, or `Blocked`. |
| Validation report | A dated, evidence-based result for one defined validation activity. |
| Synchronized pull request | A pull request that updates all artifacts required by its change type. |

## 6. Source-of-truth rules

1. The latest merged content on the GitHub default branch is the canonical source for repository state.
2. A local checkout is a working copy. It is not canonical until its commit is merged into the default branch.
3. A pull request shows the proposed state after merge. A `Done` value in the pull request becomes canonical only when the pull request merges.
4. Files outside the repository are temporary inputs. They must not control future work after migration.
5. `STATE.md` is the canonical short handoff for the current objective, decisions, constraints, blockers, and next action.
6. `BACKLOG.md` is the canonical list of work items and their delivery status.
7. `ROADMAP.md` is the canonical delivery order and batch view.
8. A work specification controls the approved scope and acceptance criteria for its work ID.
9. A work task list controls the execution steps and task status for its work ID.
10. A validation report records the result at one point in time. It does not control current status.
11. When canonical artifacts conflict, the most recent explicit user instruction controls. The pull request must reconcile all affected artifacts before merge.

## 7. Canonical file structure

The repository must use this structure:

```text
STATE.md
BACKLOG.md
ROADMAP.md
README.md
docs/
  specs/
    <work-id>/
      spec.md
  plans/
    <work-id>/
      tasks.md
  validations/
    <work-id>/
      <yyyy-mm-dd>-<sequence>-<kind>.md
evaluations/
  <skill-id>/
    cases.md
    <evaluation-report>.md
skills/
  <skill-id>/
    SKILL.md
    agents/
      openai.yaml
tools/
  validate_repository.py
tests/
  repository_validation/
.github/
  pull_request_template.md
  workflows/
    validate-repository.yml
```

Additional files are permitted when a specification requires them. They must not duplicate a canonical artifact.

## 8. Common document metadata

Each specification, task list, and validation report must have these fields directly below its title:

```text
Version: <semantic version>
Date: <YYYY-MM-DD>
Work ID: <work-id>
```

A specification must also have a `Status` field. A task list must also have a `Status` field. A validation report must instead have `Result` and `Evaluator` fields.

Rules:

- `Work ID` must match the parent directory name.
- `Date` must use ISO 8601 date format and the date in UTC.
- `Version` must use `major.minor` or `major.minor.patch` format.
- A link to another repository artifact must use a relative Markdown link.
- A referenced local file must exist with the exact letter case.
- Placeholder values such as `TBD`, `TODO`, `FIXME`, and `<work-id>` are not permitted in active or completed artifacts. Code examples in a specification are exempt.

### 8.1 Required table columns

`BACKLOG.md` must use these columns for each work row:

```text
Batch | Priority | Work ID | Purpose | Status | Specification | Tasks | Latest validation
```

`ROADMAP.md` must use these columns for each work row:

```text
Batch | Order | Work ID | Status | Specification
```

Each task table must use these columns:

```text
ID | Task | Output | Verification | Depends on | Status | Evidence
```

The validator can permit additional columns. It must not permit the removal or renaming of a required column.

## 9. Status models

### 9.1 Backlog status

`BACKLOG.md` must use only these values:

| Status | Meaning | Required condition |
| --- | --- | --- |
| `Backlog` | The idea is recorded but not scheduled. | No active task is required. |
| `Ready` | Scope is clear enough to start. | A current specification exists. |
| `In progress` | Implementation or evaluation is active. | A task list exists and at least one task is `In progress`. |
| `Review` | Implementation is complete and validation is active. | No implementation task is `In progress`. |
| `Blocked` | A named dependency stops active work. | `STATE.md` and the task list name the blocker. |
| `Done` | All acceptance criteria passed and the delivery is merged. | All tasks are `Done`, required validation passed, and implementation exists. |

Only one backlog row can use a given work ID.

### 9.2 Task status

A task list must use only these values:

| Status | Meaning |
| --- | --- |
| `Pending` | An earlier task must finish first. |
| `Ready` | Dependencies are complete and work can start. |
| `In progress` | Work is active. |
| `Blocked` | A named dependency stops the task. |
| `Done` | The output exists and its verification passed. |

The `Depends on` value must be `None` or a comma-separated list of task IDs in the same task list. At most one task for one work ID can be `In progress`, unless each concurrent task includes `Parallel: Yes` in its task text. A `Done` task must have a non-placeholder output path or identifier and a non-placeholder verification result in `Evidence`. A task cannot be `Done` when one of its dependencies is not `Done`.

A task list must not use the merge of its current pull request as a task that must be `Done` before merge. Merge is a delivery gate in section 15, not a pre-merge task.

### 9.3 Specification status

A specification must use only these values:

- `Draft for validation`
- `Validated`
- `Implemented`
- `Superseded`

`Implemented` requires a passing implementation validation report. `Superseded` requires a relative link to the replacement specification or version.

`Validated` requires a specification validation report with result `Pass` or `Pass with residual risk` and no blocking finding. The specification must link to that report. `Implemented` also requires the `Validated` condition.

### 9.4 Task-list document status

A task-list document must use only these values:

- `Draft for validation`
- `Validated`
- `Active`
- `Complete`
- `Superseded`

`Complete` requires every task to be `Done`. `Superseded` requires a relative link to the replacement task list or version.

`Validated` requires a task-list validation report with result `Pass` or `Pass with residual risk` and no blocking finding. The task list must link to that report. `Active` and `Complete` also require the `Validated` condition.

### 9.5 Validation result

A validation report must use only these result values:

- `Pass`
- `Pass with residual risk`
- `Fail`

A report with a blocking finding must use `Fail`. A residual risk must state its effect and the next control. A passing report must identify the artifact version or git tree that it validated. A later failure for the same validation kind prevents completion until a newer passing report resolves it.

## 10. Required artifact links

Each row in `BACKLOG.md` must contain:

- Work ID.
- Purpose.
- Batch or priority.
- Current status.
- A relative link to the current specification when status is not `Backlog`.
- A relative link to the task list when status is `In progress`, `Review`, `Blocked`, or `Done`.
- A relative link to the latest validation report when status is `Review` or `Done`.

Each active or completed roadmap item must identify its backlog row by work ID and link to its specification. Each specification must link to its task list after task decomposition. Each task list must link back to its specification. A completed skill specification must also link to the skill package and evaluation directory.

For `Review` and `Done`, `Latest validation` means the newest applicable delivery or implementation validation report for that work ID. It must not point to a superseded report. A `Done` row requires that report to have result `Pass` or `Pass with residual risk` and no blocking finding.

## 11. `STATE.md` rules

`STATE.md` must contain these sections:

- `Current objective`
- `Confirmed decisions`
- `Constraints`
- `Work status`
- `Blockers and open questions`
- `Key artifacts`
- `Next action`
- `Last updated`

The file must describe only the active work and the next useful action. It must not duplicate the complete backlog, roadmap, task list, or history. It must remove or replace superseded facts. A completed claim must have repository or tool evidence.

## 12. `ROADMAP.md` rules

`ROADMAP.md` must show the planned delivery sequence. It must contain:

- The current batch.
- Ordered work IDs in each batch.
- A roadmap status for each work ID.
- The completion rule for each batch.

Roadmap status must be derived from backlog status:

| Backlog status | Roadmap status |
| --- | --- |
| `Backlog` | `Planned` |
| `Ready` | `Planned` |
| `In progress` | `Active` |
| `Review` | `Active` |
| `Blocked` | `Blocked` |
| `Done` | `Complete` |

The roadmap must not show a completed item as active or planned.

## 13. Validation report immutability

1. A validation report becomes immutable when it first enters the default branch.
2. A later pull request must not modify, rename, or delete that report.
3. A correction requires a new report with a later date or sequence number.
4. The new report must link to the earlier report and state that it supersedes or corrects it.
5. Historical failures must remain in the repository.
6. A report must identify its method, scope, evidence, result, findings, and residual risks.
7. A self-evaluation report must include `Evaluator: Self` or an equivalent explicit value.
8. An independent evaluation report must identify the independent evaluator or execution method.
9. The repository validator must compare the pull request with the default-branch merge base. It must fail when a default-branch validation report is changed, renamed, or deleted.

## 14. Change classes and synchronization rules

The repository validator must classify changed files. One pull request can have more than one class. All applicable rules must pass.

| Change class | Trigger | Required synchronized changes |
| --- | --- | --- |
| New skill | New `skills/<skill-id>/SKILL.md` | Specification, task list, evaluation cases, passing validation report, backlog row, roadmap entry, and current state. |
| Skill behavior | Change in an existing skill package | Updated evaluation evidence, new validation report, and any affected specification or task status. |
| Evaluation only | Change below `evaluations/<skill-id>/` | New validation report or an explicit result report in the evaluation directory. Current status must agree with the result. |
| Work starts | Backlog changes to `In progress` | Validated specification, task list, roadmap `Active`, and current state. |
| Work is blocked | Backlog changes to `Blocked` | Named blocker in task list and current state. Roadmap must show `Blocked`. |
| Work completes | Backlog changes to `Done` | All tasks `Done`, specification `Implemented`, roadmap `Complete`, implementation files, and passing validation report. |
| Governance | Change to canonical rules, workflow, validator, or templates | Governance specification update, validator tests, new validation report, backlog or state update when applicable. |
| Status only | Change only to state, backlog, roadmap, or tasks | Cross-file status rules and evidence links must still pass. |

A pull request must update related status artifacts in the same commit set. A later cleanup pull request is not an acceptable synchronization method.

## 15. Pull request and merge rules

- Pull requests must be ready for review. Automation must not create draft pull requests.
- The pull request body must identify the work ID, change class, specification, validation evidence, residual risks, and status changes.
- The changed files must stay within the stated work scope.
- All required repository checks must complete successfully.
- The branch must be current enough for the validator to compare it with the default branch.
- A merge must use the repository merge policy. Squash merge is acceptable.
- The authorized automation can merge a validated pull request without a separate user confirmation.
- Automation must not merge when a required check fails, is pending, is absent, or cannot inspect the full change.
- A merge must not publish or deploy a skill unless the user separately authorized that action.

For pull-request validation, the head tree is the proposed post-merge repository state. A proposed `Done`, `Implemented`, or `Complete` value is valid only when every other completion condition exists in that head tree and all required checks pass. It does not become canonical until merge.

The GitHub default branch must have a ruleset or branch protection rule. It must require the repository validation check before merge. It must block direct pushes that bypass the pull request and required check. Repository administrators can configure this rule outside the repository, but the rule is part of acceptance. The implementation validation report must record the repository, protected branch, rule identifier, required check name, verification time, and read-only API or tool evidence used to inspect the active rule. A repository file cannot prove that an external rule is active.

## 16. Repository validation tool

The repository must provide `tools/validate_repository.py`. It must use the Python standard library unless the specification for a later version approves a dependency.

### 16.1 Commands

The tool must support:

```text
python tools/validate_repository.py --all
python tools/validate_repository.py --base <git-ref> --head <git-ref>
```

`--all` validates the current repository tree. `--base` and `--head` also enforce changed-file, immutability, and synchronization rules.

### 16.2 Required checks

The tool must:

1. Confirm that required canonical files and directories exist.
2. Confirm that work IDs and directory names are valid and equal where required.
3. Parse required document metadata.
4. Reject invalid status values.
5. Check relative Markdown links and exact path case.
6. Check backlog, roadmap, specification, and task status consistency.
7. Check task dependencies and completion conditions.
8. Check required artifact links for each lifecycle stage.
9. Check that a completed skill has implementation and evaluation evidence.
10. Check that a passing validation report contains method, evidence, result, findings, and risks.
11. Reject forbidden placeholders in active or completed artifacts.
12. Protect immutable validation reports when base and head refs are present.
13. Classify the change and apply all synchronization rules in section 14.
14. Report every detected error in one run when safe to do so.

The tool must be read-only and deterministic. It must not change repository files.

### 16.3 Output and exit codes

Each finding must use this format:

```text
<LEVEL> <CHECK-ID> <path>: <message>
```

The summary must show the number of errors and warnings.

| Exit code | Meaning |
| --- | --- |
| `0` | All required checks passed. Warnings can exist. |
| `1` | One or more repository checks failed. |
| `2` | The command, repository, or git references are invalid. |

Check IDs must stay stable after release. Tests must assert check IDs, not complete prose messages.

## 17. Validator test requirements

Tests must include at least these fixtures:

| ID | Fixture | Expected result |
| --- | --- | --- |
| G1 | Complete and synchronized repository | Pass |
| G2 | Backlog says `Done`, but one task is not `Done` | Fail |
| G3 | Roadmap and backlog statuses conflict | Fail |
| G4 | Artifact link is broken or has wrong case | Fail |
| G5 | Active artifact contains a forbidden placeholder | Fail |
| G6 | Existing validation report is modified | Fail |
| G7 | Existing validation report is deleted or renamed | Fail |
| G8 | New skill has no specification or evaluation | Fail |
| G9 | Skill behavior changes with no new validation evidence | Fail |
| G10 | Valid correction adds a new report and preserves the old report | Pass |
| G11 | Blocked work has no named blocker in current state | Fail |
| G12 | Complete work has all required evidence and links | Pass |
| G13 | Specification is `Validated`, but has no passing specification validation report | Fail |
| G14 | `Done` task has missing output or verification evidence | Fail |
| G15 | Two tasks are `In progress`, but one has no `Parallel: Yes` marker | Fail |

Tests must use temporary git repositories for checks that compare refs. Test data must not change the main repository tree.

## 18. Continuous integration

The repository must provide `.github/workflows/validate-repository.yml`.

The workflow must:

- Run for each pull request that targets the default branch.
- Run for each push to the default branch.
- Check out full git history so base comparison works.
- Set up a supported Python version.
- Run validator unit tests.
- Run `python tools/validate_repository.py --base <base-sha> --head <head-sha>` for pull requests.
- Run `python tools/validate_repository.py --all` for default-branch pushes.
- Use read-only repository permissions.
- Use no stored secret.
- Use concurrency cancellation for an older run on the same pull request.
- Expose one stable required check name: `repository-governance`.

The workflow must fail when a validator command or test fails.

## 19. Pull request template

`.github/pull_request_template.md` must request:

- Work ID.
- Change class or classes.
- Scope summary.
- Links to the specification and task list.
- Validation commands and results.
- Link to the new validation report.
- Backlog, roadmap, task-list, and state updates.
- Residual risks.
- A statement that the pull request is ready and is not a draft.

The template is a review aid. CI must enforce facts that it can determine from files.

## 20. Migration of current artifacts

Migration must occur in one governance pull request.

1. Add the current project state as `/STATE.md`.
2. Replace stale entries. Record that `project-state-curator` is merged and complete.
3. Add the backlog as `/BACKLOG.md`.
4. Change `project-state-curator` to `Done`.
5. Keep `bug-repro-builder` and `change-impact-mapper` in Batch 1 and set their correct current statuses.
6. Add `/ROADMAP.md` with Batch 1 order and derived statuses.
7. Import the current `project-state-curator` specification to `docs/specs/project-state-curator/spec.md`.
8. Reconcile its implementation dependency and set a version and status that match the merged implementation.
9. Import the current task list to `docs/plans/project-state-curator/tasks.md`.
10. Set completed tasks to `Done`. Remove the obsolete start blocker from current status.
11. Import the two existing validation reports without losing their original date, findings, or dependency context. Preserve each original result string in a field named `Original result`. Add the standard `Result` metadata field and map each original non-standard passing result to `Pass with residual risk`. Explain the mapping in the imported report. Do not present the resolved repository-selection dependency as a current blocker.
12. Store the imported reports below `docs/validations/project-state-curator/` with unique dated names that match section 7. Add all required metadata from section 8.
13. Treat those reports as historical evidence after this migration merges.
14. Add a new migration validation report that records the reconciliation and current evidence.
15. Keep the existing skill and evaluation files at their current canonical paths.
16. Add the governance specification, task list, validator, tests, workflow, and pull request template.
17. Add a governance implementation validation report.
18. Update `README.md` with the canonical structure and the local validation command.
19. Remove dependence on the old files outside the repository. Do not delete those external files as part of repository migration.

The migration must preserve the statement that the existing behavioral evaluation was non-independent. It must preserve the residual risk about model routing and output variance.

## 21. Failure behavior

- If a required artifact cannot be reconciled from evidence, mark the work `Blocked`. Name the missing evidence.
- If the default branch cannot be read, do not enforce or claim immutability from an assumed base.
- If the GitHub required check cannot be configured, report the governance system as not fully enforced.
- If a link target is ambiguous, fail validation. Do not guess the target.
- If CI cannot run a required command, fail the workflow.
- If unrelated user changes exist, preserve them and limit the pull request to governance work.

## 22. Acceptance criteria

The implementation is acceptable only when all these conditions are true:

- The canonical structure in section 7 exists.
- All current planning and status artifacts are in the repository.
- `STATE.md`, `BACKLOG.md`, `ROADMAP.md`, the current specifications, and current task lists agree.
- `project-state-curator` is `Done` and has links to its implementation, evaluation, and validation evidence.
- The old repository-selection blocker is not present as a current blocker.
- Historical validation findings remain available and clearly historical.
- Existing validation reports cannot be modified, renamed, or deleted by a pull request without a validator failure.
- The validator passes on the complete migrated repository.
- Validator tests G1 through G12 pass.
- At least one negative fixture proves each major enforcement group: status, link, synchronization, evidence, and immutability.
- The GitHub workflow runs on a pull request and on a default-branch push.
- The workflow exposes the stable check name `repository-governance`.
- The GitHub default branch requires the `repository-governance` check before merge.
- Direct unvalidated pushes to the default branch are blocked by a ruleset or branch protection rule.
- The pull request template contains all fields in section 19.
- The governance pull request is not a draft.
- The governance pull request has no unrelated file change.
- A new governance implementation validation report has result `Pass` or `Pass with residual risk` and has no blocking finding.
- The pull request is merged only after every required check passes.
- The merged default branch passes `python tools/validate_repository.py --all`.

## 23. Residual risks

- Repository administrators can change or bypass GitHub branch rules. Repository files cannot fully prevent this action.
- Markdown parsing can miss semantic contradictions that use valid structure and status values.
- A passing self-evaluation does not prove behavior across independent model runs.
- A status update still depends on accurate evidence from the person or automation that makes the change.

The implementation must record these risks in its validation report. A later control can add an independent evaluation and a periodic branch-rule audit.
