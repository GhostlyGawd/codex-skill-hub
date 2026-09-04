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

Governance remains in [ready pull request 2](https://github.com/GhostlyGawd/codex-skill-hub/pull/2), not merged. Status stays `Blocked` because `main` has no active protection or required check. Early preflight and unchanged-blocker controls are prepared; activation requires the [one-time administrator setup](docs/runbooks/github-enforcement-setup.md). See the live PR for its current head and checks; historical successes do not satisfy a later head's merge gate.
