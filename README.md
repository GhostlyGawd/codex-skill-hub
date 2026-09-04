# Codex Skill Hub

This repository contains custom Codex skills, their behavioral evaluations, and the project-control evidence used to deliver them.

## Source of truth

The latest merged content on the GitHub default branch is canonical. A local checkout and a pull request are proposed state until the change merges.

Use these root files for current control data:

- `STATE.md`: short current handoff, blockers, and next action.
- `BACKLOG.md`: work items and delivery status.
- `ROADMAP.md`: delivery order and batch status.

Each active work ID has a specification in `docs/specs/<work-id>/`, a task list in `docs/plans/<work-id>/`, and evidence in `docs/validations/<work-id>/`. Skill code stays in `skills/<skill-id>/`. Behavioral cases and results stay in `evaluations/<skill-id>/`.

## Local validation

Run the full test suite:

```bash
python -m unittest discover -s tests/repository_validation -v
```

Validate the current tree:

```bash
python tools/validate_repository.py --all
```

Validate a proposed git change and protect existing validation reports:

```bash
python tools/validate_repository.py --base <base-ref> --head <head-ref>
```

The validator is read-only. Exit code 0 means all required checks passed, 1 means repository checks failed, and 2 means the command, repository, or git references are invalid.

## Pull requests

Read [AGENTS.md](AGENTS.md) before work. Check GitHub capabilities and effective protections before implementation. If setup is missing, use the [enforcement setup runbook](docs/runbooks/github-enforcement-setup.md) and [import template](config/main-ruleset.json). The template tests verify intended settings, not live protection.

Use ready pull requests. Do not use draft pull requests. Update all related status and evidence artifacts in the same pull request. The stable required check name is `repository-governance`.

Do not merge if the check fails, is pending, is absent, or cannot inspect the full change. A merge does not authorize publication, deployment, or skill installation.

## Validation evidence

A report in `docs/validations/` becomes immutable when it enters the default branch. Do not modify, rename, or delete it in a later pull request. Add a new dated report that explains the correction and links to the earlier report.
