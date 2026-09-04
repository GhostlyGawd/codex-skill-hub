# Project State Curator — Implementation Task List

Version: 1.0  
Status: Complete  
Date: 2026-09-04  
Work ID: `project-state-curator`

Specification: [Specification version 1.0](../../specs/project-state-curator/spec.md)  
Task-list validation: [Historical task-list validation](../../validations/project-state-curator/2026-09-04-02-task-list.md)

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | Select the git-backed repository. | `GhostlyGawd/codex-skill-hub` | Repository selection was confirmed. | None | Done | Pull request 1 and merge commit `75d57ec8a52f49eadd007fb7206880f27c7884aa` verify the target. |
| 0.2 | Inspect repository instructions and skill locations. | `skills/project-state-curator/` | No conflicting package was found. | 0.1 | Done | The merged tree contains one package at the output path. |
| 0.3 | Record the implementation baseline. | Feature branch baseline | User work was preserved. | 0.2 | Done | Pull request 1 contains only the skill and evaluation scope. |
| 1.1 | Initialize the minimal skill package. | `skills/project-state-curator/` | Required files exist and no unused resource directory exists. | 0.3 | Done | The output has `SKILL.md` and `agents/openai.yaml`. |
| 1.2 | Apply the interface metadata rules. | `skills/project-state-curator/agents/openai.yaml` | Metadata agrees with the skill and automatic discovery remains enabled. | 1.1 | Done | The merged metadata has display text and no explicit-only policy. |
| 1.3 | Write concise skill instructions. | `skills/project-state-curator/SKILL.md` | Instructions cover routing, evidence, state updates, and scope limits. | 1.2 | Done | Instruction trace in `evaluations/project-state-curator/self-evaluation.md` verifies coverage. |
| 1.4 | Set minimal user-facing metadata. | `skills/project-state-curator/agents/openai.yaml` | Display values match the purpose. | 1.3 | Done | The merged metadata names Project State Curator and its state purpose. |
| 1.5 | Remove generated placeholders. | Minimal skill package | No unused file or placeholder remains. | 1.4 | Done | Package inspection found two required files only. |
| 2.1 | Run the structural validator. | Validator result | `quick_validate.py` exits successfully. | 1.5 | Done | `evaluations/project-state-curator/self-evaluation.md` records structural validator Pass. |
| 2.2 | Review routing quality. | Routing review | Multi-step cases match and the one-step case does not match. | 2.1 | Done | Cases T1 and T8 pass by instruction trace. |
| 2.3 | Review scope and evidence instructions. | Instruction review | Required invariants are present. | 2.2 | Done | Cases T2 through T10 map to explicit instructions. |
| 2.4 | Correct demonstrated defects. | Validated package candidate | Structural and instruction checks pass again. | 2.3 | Done | No demonstrated defect required a package change. |
| 3.1 | Create isolated scenario designs. | `evaluations/project-state-curator/cases.md` | Ten cases are independent in their stated inputs. | 2.4 | Done | Cases T1 through T10 define separate starting artifacts. |
| 3.2 | Write realistic requests and inputs. | `evaluations/project-state-curator/cases.md` | Inputs do not disclose an intended answer. | 3.1 | Done | Each case gives a request or observed state only. |
| 3.3 | Write observable result rubrics. | `evaluations/project-state-curator/cases.md` | Rubrics check state, activation, preservation, or evidence. | 3.2 | Done | Each case contains observable pass checks. |
| 3.4 | Mark release-blocking cases. | Evaluation manifest | T1, T2, T3, T7, T8, T9, and T10 are release-blocking. | 3.3 | Done | The release gate lists all seven cases. |
| 4.1 | Run the initial instruction-trace evaluation. | `evaluations/project-state-curator/self-evaluation.md` | All ten results link to instruction evidence. | 3.4 | Done | The scorecard contains T1 through T10. |
| 4.2 | Score each result. | Evaluation scorecard | Each result cites observable expected behavior. | 4.1 | Done | The scorecard records ten passes and expected results. |
| 4.3 | Apply the initial release gate. | Gate decision | Blocking cases and at least nine total cases pass. | 4.2 | Done | Seven of seven blocking and ten of ten total cases pass. |
| 5.1 | Group demonstrated failures. | Failure analysis | Each change would map to observed evidence. | 4.3 | Done | No demonstrated failure was present. |
| 5.2 | Make one focused revision or record no change. | No-change decision | No speculative rule is added. | 5.1 | Done | The evaluation records a no-change decision. |
| 5.3 | Re-run structural and instruction validation. | Validated final package | Both checks pass. | 5.2 | Done | Structural validation and the instruction trace pass. |
| 5.4 | Re-run all behavioral checks. | Final scorecard | All ten cases pass. | 5.3 | Done | Final score is 10 of 10. |
| 6.1 | Review the final diff and evidence. | Review record | Only intended skill and evaluation files changed. | 5.4 | Done | Pull request 1 provides the reviewed change set. |
| 6.2 | Update backlog and project state. | Current status records | Status and residual risk agree with evidence. | 6.1 | Done | This migration reconciles `BACKLOG.md` and `STATE.md`. |
| 6.3 | Commit validated work. | Commit `0be4979d9d4b7a2af57bc493d69e70e2b50804ec` | The commit contains the reviewed files. | 6.2 | Done | The feature commit is recorded in the historical state input. |
| 6.4 | Sync through the selected workflow. | Pull request 1 | GitHub shows the pull request merged. | 6.3 | Done | Merge commit is `75d57ec8a52f49eadd007fb7206880f27c7884aa`. |

## Historical note

The original task list showed repository selection as blocked. The user selected the repository and the work merged. That dependency is resolved and is not current.
