# Set up GitHub enforcement

This is a one-time repository administrator procedure for `GhostlyGawd/codex-skill-hub`. It describes the intended rule. It does not claim that the rule is active.

## Before setup

1. Confirm that the target repository is `GhostlyGawd/codex-skill-hub` and the target branch is `main`.
2. Inspect existing rules and classic branch protection. Preserve stronger controls. Do not delete a rule to make the import succeed.
3. Confirm that the repository's GitHub plan supports enforcement for its visibility. If the rule cannot be enforced, stop and report that limit. Do not change visibility or the plan without approval.
4. Confirm that the workflow exposes a completed check named `repository-governance`. A local test result does not create this GitHub check.

## Create the rule

Open the repository's **Settings → Rules → Rulesets**. Use the ruleset import option with [config/main-ruleset.json](../../config/main-ruleset.json), or create a branch ruleset with these settings:

| Setting | Required value |
| --- | --- |
| Enforcement | Active |
| Target | Branches; include `refs/heads/main`; no exclusions |
| Bypass list | Empty; no administrator, app, or other bypass actor |
| Pull request | Required before merge |
| Required approving reviews | 0 for the intended solo autonomous workflow |
| Review conversations | Require resolution before merge |
| Status check | `repository-governance` required |
| Branch currency | Require the branch to be up to date before merging |
| Force pushes | Blocked |
| Branch deletion | Blocked |

Use zero approvals only for this new minimum rule. Do not reduce a stronger review requirement in an existing rule. Review all imported values before saving. Save the rule with active enforcement, not evaluation-only or disabled enforcement.

## Verify after setup

Ask Codex to continue. Codex must use authorized read-only GitHub evidence to verify:

- The rule identifier, active enforcement, and exact target branch.
- All effective rules, including the required check, strict branch currency, pull-request requirement, empty bypass list, and force-push and deletion blocks.
- Preservation of stronger existing controls.
- All required check results for the exact current pull-request head.

Record the repository, branch, rule identifier, check names, source, and UTC inspection time in current evidence. Do not close the blocker from the imported file, a successful save, or a green check alone. Do not test enforcement with a direct push, force push, or branch deletion.

If read-back is denied or incomplete, retain the blocker. Repository administrator access and connector administration scope are separate. Do not use another credential or a browser fallback to bypass connector limits.

## Configuration references

GitHub documents [JSON ruleset import and active enforcement](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) and the [ruleset fields](https://docs.github.com/en/rest/repos/rules). The template is checked against those fields; successful import and effective enforcement still require live verification.
