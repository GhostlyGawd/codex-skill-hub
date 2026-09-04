# Repository work instructions

## Read before work

Read [README.md](README.md), [STATE.md](STATE.md), [BACKLOG.md](BACKLOG.md), [ROADMAP.md](ROADMAP.md), and the specification and task list for the active work ID. Read applicable validation reports. The merged default branch is canonical; local files and an open pull request are proposed changes.

## Check capabilities before implementation

Before implementation or external writes, use the connected GitHub tools for a read-only preflight:

- Confirm the repository, default branch, base commit, current pull-request head, and unrelated changes.
- Inspect effective branch protections and required checks. Record the branch, rule identifiers, check names, source, and UTC time.
- Check that the available connector can perform each required operation, including rule inspection, any necessary rule update, feature-branch writes, and merge.
- Distinguish the user's repository permissions from connector permissions. Repository administrator access does not prove that the connector has administration scope or a callable rule-update operation.
- Treat a denied or unreadable protection endpoint as unknown for that endpoint. Do not infer a missing rule from the denial. Use other authorized read-only evidence only for facts that it directly proves.

If a required capability or effective protection is missing or unknown, stop the affected operation. Name the exact missing capability and administrator action in current state and the task list. Keep the work `Blocked`. Do not use a browser fallback, discover alternate credentials, weaken controls, or merge to bypass the blocker. The user's merge authorization does not supply connector permissions.

Use [the enforcement setup runbook](docs/runbooks/github-enforcement-setup.md) when a repository administrator must configure the rule. A ruleset JSON file proves intended configuration only. It does not prove live enforcement.

## Resume a blocked task

First repeat only the read-only check for the named external blocker. If the blocker is unchanged, retain it and report the required action once. Do not repeat the full test suite, renumber tasks, redesign the plan, or create another validation report only because the user says to continue.

An evidence-only update records new observations or task status within the approved scope. Keep task IDs and dependencies stable. Reconcile affected current state, backlog, roadmap, and task evidence in the same change. Do not leave an obsolete dependency in a current evidence cell. Keep completed local output distinct from delivery that is still blocked.

A scope change alters requirements, dependencies, acceptance criteria, or behavior. Update the affected specification and plan, then validate the changed parts. Do not represent a scope change as a status-only update.

Reports already merged into the default branch are immutable. Preserve historical findings. Add a new report only for a new validation result or a necessary correction, and identify the earlier evidence. Historical reports do not control current task status.

## Validate and merge

Use ready pull requests, never drafts. The user authorizes autonomous merge after all delivery gates pass. Before merge:

- Confirm that the pull request contains only approved changes and that related artifacts agree.
- Run the repository tests and full-tree validation after relevant changes. Use base/head validation to check the complete proposed change and historical report preservation.
- Confirm all required checks passed for the exact current pull-request head and required base. An earlier head's success is not sufficient.
- Read back effective protections for the target branch. Confirm the required pull request, `repository-governance` check, strict up-to-date policy, no bypass actors, and force-push and deletion blocks. Preserve stronger existing controls.
- Do not merge if a required check or protection is missing, pending, failed, or unknown. Do not bypass review or other stronger rules.

After merge, verify the merged commit and default-branch check. Reconcile current status from evidence. A merge does not authorize publication, deployment, or skill installation.

## Label validation evidence correctly

Separate structural validation, instruction trace, executed behavioral testing, and independent evaluation. A structural check or instruction trace is not executed behavioral testing. Do not label a self-evaluation independent. Record the actual method, artifact version or commit, commands, results, and limits. Retain residual risks until new evidence resolves them.
