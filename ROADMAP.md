# Codex Skill Roadmap

Current batch: Governance prerequisite, then Batch 1.

The governance feature branch exists from verified `main` commit `75d57ec8a52f49eadd007fb7206880f27c7884aa`. Inspection found no active `main` rule or required check. The governance item stays `Blocked` at the rule-configuration gate.

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
