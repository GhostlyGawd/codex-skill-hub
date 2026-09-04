# Repository Governance — Scoped Preflight Amendment Review

Version: 1.0  
Date: 2026-09-04  
Work ID: `repository-governance`  
Result: Pass with residual risk  
Evaluator: Independent Codex subagent `/root/validate_preflight_fix`

Validated artifacts: [Specification version 0.3](../../specs/repository-governance/spec.md), [task list version 0.9](../../plans/repository-governance/tasks.md), and the exact local amendment files identified below.

## Scope and result

The specification amendment, supplemental decomposition, and prepared local prevention controls pass this scoped review. No blocking finding applies to this amendment. This is not a new full implementation or delivery result. [Report 11](2026-09-04-11-implementation.md) remains the latest implementation report: local implementation Pass, overall enforcement Fail at V3. Governance remains `Blocked`; no import, rule activation, merge, or final-head CI success is claimed here.

The version 0.2 specification and version 0.8 task-list historical validations are retained. This review covers specification section 24, the version 0.9 supplemental checklist, and narrow current-evidence corrections. It does not reopen every previously accepted design decision.

## Method

- Independently read the repository work instructions, current state/backlog/roadmap, README, relevant specification and task-list controls, report 11, workflow, ruleset template, runbook, and template tests.
- Check the amended design before accepting the prepared outputs. Verify that P1 through P5 have explicit outputs, observable checks, and acyclic dependencies, with live enforcement kept outside local completion.
- Compare the ruleset's fields with [GitHub's ruleset API documentation](https://docs.github.com/en/rest/repos/rules) and the setup procedure with [GitHub's import and enforcement guidance](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository), inspected 2026-09-04 UTC. This is a documentation comparison, not a successful GitHub import.
- Execute the complete local standard-library test suite. Verify full-tree structure after adding this report and validation metadata.
- Record SHA-256 identities after specification/plan validation metadata and supplemental completion updates. Review historical/current evidence distinctions. Make no external mutation and no skill behavioral-testing claim.

## Evidence

| Requirement | Inspected evidence | Result |
| --- | --- | --- |
| Early capability check | `AGENTS.md` requires repository/base/head and capability/protection inspection before affected work. It separates user permissions from connector capability and treats denied evidence as unknown. | Pass by instruction review |
| Permission and protection stop | Instructions prohibit alternate credential discovery, browser fallback, control weakening, and merge bypass. | Pass by instruction review |
| Unchanged-blocker resume | Instructions require only relevant read-only preflight when the external blocker is unchanged, without full test/report/plan churn. | Pass by instruction review |
| Evidence synchronization | State, backlog, roadmap, and plan keep V3 unresolved. Task 2.1 no longer cites task 1.3 as incomplete; task 6.6 acknowledges report 11 and completed version 0.8 validation. Tasks 6.1, 6.2, and 6.4 distinguish prior checks from current-head evidence. Task 0.1 now labels version 0.2 as historical. | Pass |
| Plan boundaries | Original task IDs, dependencies, and statuses are unchanged. Supplemental P1–P5 alone are completed after scoped verification; their bullet statuses are manually reviewed, not parsed by the validator. | Pass with stated limit |
| Template settings | Active branch rule targets only `refs/heads/main`, has no bypass or exclusions, requires a PR and exact strict status check, permits zero approvals for the new solo rule, resolves review threads, blocks force push/deletion, and does not add an update lock. | Pass by inspection and six tests |
| Setup safeguards | Runbook requires plan support, preservation of stronger rules, active setup, and sufficient authorized read-back. It does not equate a saved/imported file with enforcement. | Pass by instruction review |
| Test suite | `python -m unittest discover -s tests/repository_validation -v`, started 2026-09-04T22:54:27Z. | Exit 0; 36 tests passed in 2.654 seconds, including six new template tests and all 30 existing tests. |
| Full-tree check | `python tools/validate_repository.py --all` on the completed local amendment after excluding the leftover scratch fixture described below. | Exit 0; 0 errors and 0 warnings. Independently rerun after the root's matching successful check. |

Root-provided live evidence, not independently repeated by this evaluator: at 2026-09-04T22:55:03.019Z, authorized GET responses for `repos/GhostlyGawd/codex-skill-hub/branches/main` and `repos/GhostlyGawd/codex-skill-hub/rulesets` reported `main` at `75d57ec8a52f49eadd007fb7206880f27c7884aa`, `protected: false`, protection disabled, empty required contexts/checks with enforcement level `off`, and an empty ruleset list. This supports retaining V3. No rule-write operation is exposed in the current connection, as reported by the root's capability inspection.

The first full-tree run at 2026-09-04T22:57:38Z exited 1 on two broken links inside the preexisting scratch test fixture directory `governance-tests-xqdbcas6`, which is not part of the proposed repository change. The root moved that exact fixture directory recoverably outside the repository mirror; no candidate or historical report was deleted. The subsequent full-tree checks passed. This was test-workspace contamination, not an ignored candidate finding.

## Artifact identities

These SHA-256 values identify the final reviewed local files, not a published Git commit. The report itself is excluded to avoid a self-hash cycle.

| Artifact | SHA-256 |
| --- | --- |
| Specification version 0.3 | `9b38adb5904ca3ba2421e72f35fec20cdcc84d2d691c9d1cfc35c31e019120d9` |
| Task list version 0.9 | `f68aa4916410d3948c92497e371c73b1bc2b6a01761eae380c69384621d34eba` |
| `AGENTS.md` | `014075c58b9085122d81b1cc66828950b54f696b32b2841274c6c4217159e430` |
| `README.md` | `08cef961e47a583955df22ba9606110be71dd138e6bd285714e38ba3dd42032f` |
| `STATE.md` | `2eba2019f32f6a4052767d46ce8e4201704bfcefb69f4c3a851b27b6fab27f6f` |
| `BACKLOG.md` | `c1687f8287204b16397c257d9dd5318ae59b4097af09e352713328e048742f90` |
| `ROADMAP.md` | `46b99eab47844aa6230654aefe22e9a295b010d8dabbdb28fdca8fbc9320ce1a` |
| `config/main-ruleset.json` | `c832530fd898a8311bc14ee5497fafb11b1a6737629bb41d84fce9e715f91f9e` |
| `tests/repository_validation/test_ruleset_template.py` | `00d6db906080bda8444b83e93f5deedcece9153f437e106e9b58d2259e98be12` |
| Setup runbook | `727eaa1662cad99d931773ca8a676461a42b596cad3b2695d9b59af522aad1e7` |

## Findings

The amendment addresses late capability discovery and unnecessary repeat work with explicit instructions, supported by a tested setup template. It does not grant missing administration capability. Prepared output acceptance is recorded after review; no claim is made that the original preparation occurred only after this review.

Historical reports were not edited by this evaluator. Report 11 retains its original result and context. This local mirror has no git metadata; comparison with the actual default-branch report content and complete proposed diff remains a publication/CI gate, not a result established by this review.

The six new tests assert intended configuration. They do not exercise live GitHub enforcement, future agent compliance, or skill behavior. The manually reviewed supplemental checklist is not a new machine-enforced task model.

## Residual risks

| Risk | Effect | Next control |
| --- | --- | --- |
| V3 is still unresolved. | Required governance checks and direct-push protection are not active; delivery cannot complete. | Administrator activates the rule; obtain sufficient authorized read-back and exact-head checks before merge. |
| Read-back may omit bypass actors without ruleset write access. | Even a successful administrator import may not provide enough connector evidence to verify the empty bypass list. | Retain `Blocked` on incomplete evidence; obtain an authorized inspection source. GitHub documents this limit in its ruleset GET endpoint. |
| Instructions depend on agent compliance; bullet checklist status is manually reviewed. | A future agent can disregard early checks or repeat unnecessary work. | Read `AGENTS.md` at startup and independently review scoped status transitions; do not describe this as automatic live enforcement. |
| The template omits optional status-check integration binding. | The context name alone does not bind the check to a particular app. | Verify the expected workflow/check provenance at the exact-head merge gate; preserve stronger live source restrictions. |
| Local checks do not validate later commits or the live import. | A subsequent file change or rejected import invalidates assumed readiness. | Run the existing workflow on the published exact head and read effective rules before delivery. |
| Administrators can later alter protections. | Enforcement can drift after setup. | Recheck effective controls before each merge. |

## Decision

Accept only the bounded specification, decomposition, and local prevention amendment. Set specification version 0.3 and task list version 0.9 to `Validated`; retain all original delivery task statuses and keep V3, backlog, and roadmap `Blocked`. No additional full validation cycle is justified solely by another unchanged-blocker resume.
