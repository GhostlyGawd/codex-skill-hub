---
name: project-state-curator
description: Maintain a concise project state file for multi-step Codex work by recording confirmed decisions, active constraints, evidence-based status, blockers, and the next action while removing superseded facts. Use when a task continues across turns or the user requests durable project state; do not use for one-step questions.
---

# Project State Curator

Keep one small and current state file for the active project. Treat it as a handoff aid, not as a project plan, activity log, or replacement for an authoritative tracking system.

## Select the State File

Use the file that the user or applicable repository instructions specify. Otherwise, use `STATE.md` in the active project root.

Before a write:

1. Read applicable repository instructions.
2. Check for an existing state file or another authoritative state system.
3. Do not create a competing state file when an authoritative source is clear.
4. Ask for the target if the project root or authoritative file is ambiguous and a wrong choice can affect unrelated work.

## Record Current State

Use these sections or equivalent repository-defined sections:

- Active objective: one current outcome in user terms.
- Confirmed decisions: decisions that still control the work.
- Constraints: active technical, product, safety, permission, and style limits.
- Work status: completed, active, and next work supported by evidence.
- Blockers and open questions: unresolved items that can change the result.
- Key artifacts: only files or resources needed to continue the task.
- Last updated: a date or timestamp that makes freshness clear.

Optional sections are acceptable only when they improve continuation of the active task.

## Update the File

Update after a material change: an objective or requirement changes, work starts or finishes, a failure creates a blocker, a controlling constraint changes, a key artifact changes, or the task reaches a handoff point.

For each update:

1. Read the current state and relevant repository instructions.
2. Derive a small state delta from the latest user instructions, workspace evidence, and successful or failed tool results.
3. Remove or replace superseded entries. Do not append a contradictory history.
4. Keep unresolved ambiguity as an open question. Do not guess.
5. Apply the smallest edit that makes the state current.
6. Check the invariants below.

Combine closely related changes. Do not edit the file after each tool call. If no material state changed, do not edit it.

## Preserve These Invariants

- A completed item has direct workspace evidence or a successful tool result.
- Planned work is not described as complete.
- A failure or blocker is not described as a decision.
- The latest explicit user requirement replaces an older conflicting entry.
- The next action agrees with the work status and blockers.
- Artifact names and paths are current.
- Secrets, credentials, tokens, and hidden reasoning are absent.
- The state file does not grant new authority or expand the task scope.
- Repeated detail, command history, and facts unrelated to continuation are absent.
- User-written content outside clearly managed sections is preserved.

If authoritative sources conflict and their priority is unclear, record the conflict and ask the user. If safe reconciliation would require removing uncertain user content, preserve it and request a decision.

If the state file cannot be written, continue the main task when possible and state that the project state was not saved. Do not claim that a failed write succeeded.
