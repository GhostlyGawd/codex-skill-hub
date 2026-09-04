# Codex Skill Backlog

Updated: 2026-09-04

| Batch | Priority | Work ID | Purpose | Status | Specification | Tasks | Latest validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | `project-state-curator` | Keep concise project state current during multi-step work. | Done | [Specification](docs/specs/project-state-curator/spec.md) | [Tasks](docs/plans/project-state-curator/tasks.md) | [Migration and implementation validation](docs/validations/project-state-curator/2026-09-04-03-migration.md) |
| 1 | 2 | `bug-repro-builder` | Convert an incomplete bug report into a minimal reproduction and test command. | Backlog | — | — | — |
| 1 | 3 | `change-impact-mapper` | Find files, APIs, tests, and users affected by a proposed change. | Backlog | — | — | — |
| Governance | 1 | `repository-governance` | Keep project-control artifacts synchronized and enforce repository checks. | Blocked | [Specification](docs/specs/repository-governance/spec.md) | [Tasks](docs/plans/repository-governance/tasks.md) | — |
| Later | 4 | `implementation-verifier` | Build and run a verification plan for a change. | Backlog | — | — | — |
| Later | 5 | `issue-to-work-plan` | Convert an issue into ordered tasks and acceptance criteria. | Backlog | — | — | — |
| Later | 6 | `dependency-upgrade-scout` | Review an upgrade and identify breaking changes. | Backlog | — | — | — |
| Later | 7 | `log-evidence-analyzer` | Build an evidence-based event timeline from logs. | Backlog | — | — | — |
| Later | 8 | `review-comment-resolver` | Group and resolve code-review comments. | Backlog | — | — | — |
| Later | 9 | `docs-code-consistency-checker` | Compare documentation with code and commands. | Backlog | — | — | — |
| Later | 10 | `safe-data-migration-planner` | Plan migration, rollback, and validation steps. | Backlog | — | — | — |

Governance evidence: `feat/repository-governance` exists from verified `main` commit `75d57ec8a52f49eadd007fb7206880f27c7884aa`. Inspection found no active protection, required check, or repository ruleset on `main`. Status stays `Blocked` until an active rule is configured and verified.
