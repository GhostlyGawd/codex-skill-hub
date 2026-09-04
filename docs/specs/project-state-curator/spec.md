# Project State Curator — Specification

Version: 1.0  
Status: Implemented  
Date: 2026-09-04  
Work ID: `project-state-curator`

Specification validation: [Historical specification validation](../../validations/project-state-curator/2026-09-04-01-specification.md)  
Implementation validation: [Migration and implementation validation](../../validations/project-state-curator/2026-09-04-03-migration.md)  
Task list: [Implementation tasks](../../plans/project-state-curator/tasks.md)  
Skill package: [SKILL.md](../../../skills/project-state-curator/SKILL.md)  
Evaluation evidence: [Evaluation directory](../../../evaluations/project-state-curator/)

## Purpose

`project-state-curator` keeps a small, accurate state file during multi-step Codex work. It records the current objective, confirmed decisions, active constraints, work status, blockers, and next action. It removes facts that later evidence makes stale.

## Users and use cases

Use the skill when a task continues across turns, when requirements can change, when work stops at a blocker, or when the user asks for durable project state.

Do not use the skill for a one-step factual question, a short read-only inspection with no durable state, or a project that already has another user-selected authoritative state system.

## Required behavior

- Use the state file that the user or repository instructions specify. Otherwise, use `STATE.md` in the active project root.
- Keep one current objective, confirmed decisions, constraints, work status, blockers and open questions, key artifacts, and a freshness date.
- Update only after a material change.
- Use direct workspace or tool evidence for completion claims.
- Remove or replace superseded entries instead of keeping a contradiction.
- Keep unresolved ambiguity as an open question. Do not guess.
- Preserve user content outside clearly managed sections.
- Exclude secrets, credentials, tokens, and hidden reasoning.
- Do not use the state file to grant authority or expand task scope.

## Failure behavior

- Ask for the target before a write when the project root or authoritative state file is ambiguous.
- Preserve uncertain user content when reconciliation could remove it.
- If a write fails, do not claim that the file is current.

## Package design

The implemented package contains only `SKILL.md` and `agents/openai.yaml`. Behavioral fixtures remain outside the package.

## Acceptance criteria

- The package passes `quick_validate.py`.
- All ten behavioral cases have results.
- All release-blocking cases pass.
- All ten cases pass after the revision decision.
- The package contains no unused resources or placeholders.
- The implementation is stored in git and merged through the selected repository workflow.

## Implementation evidence

Pull request 1 merged the package to `main` at commit `75d57ec8a52f49eadd007fb7206880f27c7884aa`. The evaluation reports 10 of 10 cases passing by instruction trace. This evaluation is non-independent. Automatic routing and generated output can vary across independent model runs.

## Historical dependency

The original version 0.1 specification required selection of a git-backed target. The user selected `GhostlyGawd/codex-skill-hub`, and pull request 1 resolved this dependency. It is not a current blocker.
