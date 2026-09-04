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
- `repository-governance`: Feature commit `2d2bec66099d6b6e70ce5541a3df05c82dbb3ae4` with tree `c9cba765815c5ff8f22eb9f179e5d5ded454e7dc` is on `feat/repository-governance`. Ready pull request 2 is open, and workflow run `33913148787` completed successfully. No merge occurred. Full enforcement remains blocked because `main` has no active rule and no exposed tool can configure it.
- `bug-repro-builder` and `change-impact-mapper`: Backlog.

## Blockers and open questions

- No active rule protects `main`: the branch reports `protected: false`, protection reports disabled, required checks are empty, and repository rulesets are empty. The classic protection-detail request returned 403, but this does not replace the available no-rule evidence.
- Branch-rule mutation is not available in this workspace. An administrator or an authorized GitHub tool must require `repository-governance` on `main` and block direct unvalidated pushes.
- Pull request 2 is ready and its workflow run succeeded. The exact required-check rule and direct-push block are still absent. No post-merge evidence exists because the pull request is not merged.

## Key artifacts

- [Backlog](BACKLOG.md)
- [Roadmap](ROADMAP.md)
- [Governance specification](docs/specs/repository-governance/spec.md)
- [Governance task list](docs/plans/repository-governance/tasks.md)
- [Repository validator](tools/validate_repository.py)
- [Ready pull request 2](https://github.com/GhostlyGawd/codex-skill-hub/pull/2)

## Next action

Have an administrator or authorized GitHub tool configure the required `main` rule. Then inspect the rule before any merge and confirm that it requires `repository-governance` and blocks direct unvalidated pushes.

## Last updated

2026-09-04 UTC
