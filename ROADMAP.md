# Codex Skill Roadmap

Current batch: Governance prerequisite, then Batch 1.

[Ready pull request 2](https://github.com/GhostlyGawd/codex-skill-hub/pull/2) is not merged. The governance item stays `Blocked` at the `main` rule-configuration gate. The [setup runbook](docs/runbooks/github-enforcement-setup.md) and tested import template address this dependency; repository instructions require early preflight and prevent repeated work for an unchanged blocker. Batch 1's next skill still waits for verified governance delivery.

| Batch | Order | Work ID | Status | Specification |
| --- | --- | --- | --- | --- |
| Governance | 1 | `repository-governance` | Blocked | [Specification](docs/specs/repository-governance/spec.md) |
| 1 | 1 | `project-state-curator` | Complete | [Specification](docs/specs/project-state-curator/spec.md) |
| 1 | 2 | `bug-repro-builder` | Planned | — |
| 1 | 3 | `change-impact-mapper` | Planned | — |
| Later | 4 | `implementation-verifier` | Planned | — |
| Later | 5 | `issue-to-work-plan` | Planned | — |
| Later | 6 | `dependency-upgrade-scout` | Planned | — |
| Later | 7 | `log-evidence-analyzer` | Planned | — |
| Later | 8 | `review-comment-resolver` | Planned | — |
| Later | 9 | `docs-code-consistency-checker` | Planned | — |
| Later | 10 | `safe-data-migration-planner` | Planned | — |

## Batch completion rules

- Governance is complete when local checks pass, the ready pull request merges, and an active rule protects `main` with required check `repository-governance`.
- Batch 1 is complete when all three skills have implemented specifications, complete task lists, and passing validation evidence.
- Later work is complete when each selected skill meets the same delivery evidence rules.
