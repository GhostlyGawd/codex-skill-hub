# Repository State

## Current objective

Implement and validate repository governance for `GhostlyGawd/codex-skill-hub`.

## Confirmed decisions

- The latest merged content on the GitHub default branch is canonical.
- Pull requests must be ready for review. Do not use draft pull requests.
- Validated pull requests can be merged without a separate user confirmation.
- Validation reports become immutable when they enter the default branch.
- `project-state-curator` is complete and was merged in pull request 1.

## Constraints

- Use the stable required check name `repository-governance`.
- Preserve historical evidence and its original context.
- Keep the existing self-evaluation labeled as non-independent.
- Do not publish, deploy, or install a skill as part of governance work.

## Work status

- `project-state-curator`: Done on `main` at commit `75d57ec8a52f49eadd007fb7206880f27c7884aa`.
- `repository-governance`: Branch `feat/repository-governance` was created from verified `main` commit `75d57ec8a52f49eadd007fb7206880f27c7884aa`. Inspection found that `main` is not protected, has no required checks, and has no repository ruleset. Full enforcement remains blocked because no exposed tool can configure the required rule.
- `bug-repro-builder` and `change-impact-mapper`: Backlog.

## Blockers and open questions

- No active rule protects `main`: the branch reports `protected: false`, protection reports disabled, required checks are empty, and repository rulesets are empty. The classic protection-detail request returned 403, but this does not replace the available no-rule evidence.
- Branch-rule mutation is not available in this workspace. An administrator or an authorized GitHub tool must require `repository-governance` on `main` and block direct unvalidated pushes.
- The ready pull request, workflow run, required-check result, and post-merge result still need live GitHub evidence.

## Key artifacts

- [Backlog](BACKLOG.md)
- [Roadmap](ROADMAP.md)
- [Governance specification](docs/specs/repository-governance/spec.md)
- [Governance task list](docs/plans/repository-governance/tasks.md)
- [Repository validator](tools/validate_repository.py)

## Next action

Have an administrator or authorized GitHub tool configure the required `main` rule, then inspect the rule and record its required check and direct-push controls.

## Last updated

2026-09-04 UTC
