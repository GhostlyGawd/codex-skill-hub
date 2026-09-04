from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_VALIDATOR = Path(__file__).resolve().parents[2] / "tools" / "validate_repository.py"


STATE = """# Repository State

## Current objective

Maintain alpha.

## Confirmed decisions

- Alpha is complete.

## Constraints

- Use repository checks.

## Work status

- `alpha`: Done.

## Blockers and open questions

- None.

## Key artifacts

- [Backlog](BACKLOG.md)

## Next action

Select the next work item.

## Last updated

2026-09-04 UTC
"""

BACKLOG = """# Backlog

| Batch | Priority | Work ID | Purpose | Status | Specification | Tasks | Latest validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | `alpha` | Maintain state. | Done | [Specification](docs/specs/alpha/spec.md) | [Tasks](docs/plans/alpha/tasks.md) | [Implementation](docs/validations/alpha/2026-09-04-03-implementation.md) |
"""

ROADMAP = """# Roadmap

Current batch: 1.

| Batch | Order | Work ID | Status | Specification |
| --- | --- | --- | --- | --- |
| 1 | 1 | `alpha` | Complete | [Specification](docs/specs/alpha/spec.md) |

## Batch completion rules

- Batch 1 is complete when alpha is complete.
"""

SPEC = """# Alpha Specification

Version: 1.0
Status: Implemented
Date: 2026-09-04
Work ID: `alpha`

Specification validation: [Report](../../validations/alpha/2026-09-04-01-specification.md)
Implementation validation: [Report](../../validations/alpha/2026-09-04-03-implementation.md)
Task list: [Tasks](../../plans/alpha/tasks.md)
Skill: [Package](../../../skills/alpha/SKILL.md)
Evaluation: [Cases](../../../evaluations/alpha/cases.md)

## Purpose

Maintain alpha state.
"""

PLAN = """# Alpha Tasks

Version: 1.0
Status: Complete
Date: 2026-09-04
Work ID: `alpha`

Specification: [Specification](../../specs/alpha/spec.md)
Task-list validation: [Report](../../validations/alpha/2026-09-04-02-task-list.md)

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 | Build alpha. | `skills/alpha/SKILL.md` | Package exists. | None | Done | Validator reported Pass. |
"""

REPORT = """# {title}

Version: 1.0
Date: 2026-09-04
Work ID: `alpha`
Result: Pass
Evaluator: Independent test evaluator

Validated artifact: alpha version 1.0.

## Method

Inspect the artifact.

## Evidence

The required output exists.

## Findings

No blocking finding exists.

## Residual risks

No material residual risk was found.
"""


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_valid_repo(root: Path) -> None:
    write(root, "STATE.md", STATE)
    write(root, "BACKLOG.md", BACKLOG)
    write(root, "ROADMAP.md", ROADMAP)
    write(root, "README.md", "# Fixture\n")
    write(root, "docs/specs/alpha/spec.md", SPEC)
    write(root, "docs/plans/alpha/tasks.md", PLAN)
    write(root, "docs/validations/alpha/2026-09-04-01-specification.md", REPORT.format(title="Specification Validation"))
    write(root, "docs/validations/alpha/2026-09-04-02-task-list.md", REPORT.format(title="Task-List Validation"))
    write(root, "docs/validations/alpha/2026-09-04-03-implementation.md", REPORT.format(title="Implementation Validation"))
    write(root, "evaluations/alpha/cases.md", "# Cases\n")
    write(root, "evaluations/alpha/results.md", "# Results\n")
    write(root, "skills/alpha/SKILL.md", "---\nname: alpha\ndescription: Maintain alpha.\n---\n\n# Alpha\n")
    write(root, "skills/alpha/agents/openai.yaml", "interface:\n  display_name: Alpha\n")
    write(root, ".github/pull_request_template.md", "# Ready pull request\n")
    write(root, ".github/workflows/validate-repository.yml", "name: validation\n")
    write(root, "tests/repository_validation/__init__.py", '"""Fixture tests."""\n')
    (root / "tools").mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_VALIDATOR, root / "tools/validate_repository.py")


def make_valid_non_skill_repo(root: Path) -> None:
    work_id = "repository-governance"
    write(
        root,
        "STATE.md",
        """# Repository State

## Current objective

Maintain repository governance.

## Confirmed decisions

- Repository governance is complete.

## Constraints

- Keep validation deterministic.

## Work status

- `repository-governance`: Done.

## Blockers and open questions

- None.

## Key artifacts

- [Validator](tools/validate_repository.py)

## Next action

Select the next work item.

## Last updated

2026-09-04 UTC
""",
    )
    write(
        root,
        "BACKLOG.md",
        """# Backlog

| Batch | Priority | Work ID | Purpose | Status | Specification | Tasks | Latest validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Governance | 1 | `repository-governance` | Enforce repository controls. | Done | [Specification](docs/specs/repository-governance/spec.md) | [Tasks](docs/plans/repository-governance/tasks.md) | [Implementation](docs/validations/repository-governance/2026-09-04-03-implementation.md) |
""",
    )
    write(
        root,
        "ROADMAP.md",
        """# Roadmap

Current batch: Governance.

| Batch | Order | Work ID | Status | Specification |
| --- | --- | --- | --- | --- |
| Governance | 1 | `repository-governance` | Complete | [Specification](docs/specs/repository-governance/spec.md) |

## Batch completion rules

- Governance is complete when the validator and evidence pass.
""",
    )
    write(root, "README.md", "# Non-skill governance fixture\n")
    write(
        root,
        "docs/specs/repository-governance/spec.md",
        """# Repository Governance Specification

Version: 1.0
Status: Implemented
Date: 2026-09-04
Work ID: `repository-governance`

Specification validation: [Report](../../validations/repository-governance/2026-09-04-01-specification.md)
Implementation validation: [Report](../../validations/repository-governance/2026-09-04-03-implementation.md)
Task list: [Tasks](../../plans/repository-governance/tasks.md)
Implementation: [Validator](../../../tools/validate_repository.py)

## Purpose

Enforce repository governance with a deterministic validator.
""",
    )
    write(
        root,
        "docs/plans/repository-governance/tasks.md",
        """# Repository Governance Tasks

Version: 1.0
Status: Complete
Date: 2026-09-04
Work ID: `repository-governance`

Specification: [Specification](../../specs/repository-governance/spec.md)
Task-list validation: [Report](../../validations/repository-governance/2026-09-04-02-task-list.md)

| ID | Task | Output | Verification | Depends on | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 | Build the repository validator. | `tools/validate_repository.py` | Validator exits successfully. | None | Done | Full repository validation reported Pass. |
""",
    )
    report = REPORT.format(title="{title}").replace("Work ID: `alpha`", f"Work ID: `{work_id}`")
    report = report.replace("alpha version 1.0", f"{work_id} version 1.0")
    write(root, "docs/validations/repository-governance/2026-09-04-01-specification.md", report.format(title="Specification Validation"))
    write(root, "docs/validations/repository-governance/2026-09-04-02-task-list.md", report.format(title="Task-List Validation"))
    write(root, "docs/validations/repository-governance/2026-09-04-03-implementation.md", report.format(title="Implementation Validation"))
    (root / "skills").mkdir(parents=True, exist_ok=True)
    (root / "evaluations").mkdir(parents=True, exist_ok=True)
    write(root, ".github/pull_request_template.md", "# Ready pull request\n")
    write(root, ".github/workflows/validate-repository.yml", "name: validation\n")
    write(root, "tests/repository_validation/__init__.py", '"""Fixture tests."""\n')
    (root / "tools").mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_VALIDATOR, root / "tools/validate_repository.py")


def run_validator(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    validator = root / "tools/validate_repository.py"
    if not validator.is_file():
        validator = SOURCE_VALIDATOR
    return subprocess.run(
        [sys.executable, str(validator), *args], cwd=root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def init_git(root: Path) -> str:
    git(root, "init", "-q")
    git(root, "config", "user.name", "Validator Test")
    git(root, "config", "user.email", "validator@example.invalid")
    git(root, "add", ".")
    git(root, "commit", "-qm", "base")
    return git(root, "rev-parse", "HEAD")


class ValidatorFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="governance-tests-")
        self.root = Path(self.temp.name)
        make_valid_repo(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assert_check(self, result: subprocess.CompletedProcess[str], check_id: str, code: int = 1) -> None:
        self.assertEqual(result.returncode, code, result.stdout)
        self.assertIn(check_id, result.stdout)

    def replace(self, relative: str, old: str, new: str) -> None:
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def test_g1_complete_synchronized_repository_passes(self) -> None:
        result = run_validator(self.root, "--all")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_g2_done_backlog_with_unfinished_task_fails(self) -> None:
        self.replace("docs/plans/alpha/tasks.md", "| Done | Validator reported Pass. |", "| Pending | Waiting for work. |")
        self.assert_check(run_validator(self.root, "--all"), "GOV-DONE-TASKS")

    def test_g3_roadmap_backlog_conflict_fails(self) -> None:
        self.replace("ROADMAP.md", "| Complete |", "| Active |")
        self.assert_check(run_validator(self.root, "--all"), "GOV-ROADMAP-STATUS")

    def test_g4_broken_or_wrong_case_link_fails(self) -> None:
        for target in ("missing.md", "docs/specs/Alpha/spec.md"):
            with self.subTest(target=target):
                original = (self.root / "ROADMAP.md").read_text(encoding="utf-8")
                self.replace("ROADMAP.md", "docs/specs/alpha/spec.md", target)
                self.assert_check(run_validator(self.root, "--all"), "GOV-LINK")
                (self.root / "ROADMAP.md").write_text(original, encoding="utf-8")

    def test_g5_forbidden_placeholder_fails(self) -> None:
        write(self.root, "STATE.md", STATE + "\nTODO\n")
        self.assert_check(run_validator(self.root, "--all"), "GOV-PLACEHOLDER")

    def test_g6_modified_validation_report_fails(self) -> None:
        base = init_git(self.root)
        write(self.root, "docs/validations/alpha/2026-09-04-01-specification.md", REPORT.format(title="Changed Specification Validation"))
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "modify report")
        head = git(self.root, "rev-parse", "HEAD")
        self.assert_check(run_validator(self.root, "--base", base, "--head", head), "GOV-IMMUTABLE")

    def test_g7_deleted_or_renamed_validation_report_fails(self) -> None:
        for action in ("delete", "rename"):
            with self.subTest(action=action):
                case = self.root / action
                case.mkdir()
                make_valid_repo(case)
                base = init_git(case)
                source = case / "docs/validations/alpha/2026-09-04-01-specification.md"
                if action == "delete":
                    source.unlink()
                else:
                    source.rename(source.with_name("2026-09-04-04-specification.md"))
                git(case, "add", "-A")
                git(case, "commit", "-qm", action)
                head = git(case, "rev-parse", "HEAD")
                self.assert_check(run_validator(case, "--base", base, "--head", head), "GOV-IMMUTABLE")

    def test_g8_new_skill_missing_specification_or_evaluation_fails(self) -> None:
        variants = {
            "specification": [("evaluations/beta/cases.md", "# Cases\n")],
            "evaluation": [("docs/specs/beta/spec.md", SPEC.replace("alpha", "beta").replace("Alpha", "Beta"))],
        }
        for name, extras in variants.items():
            with self.subTest(name=name):
                case = self.root / name
                case.mkdir()
                make_valid_repo(case)
                base = init_git(case)
                write(case, "skills/beta/SKILL.md", "---\nname: beta\ndescription: Test beta.\n---\n")
                for relative, content in extras:
                    write(case, relative, content)
                git(case, "add", ".")
                git(case, "commit", "-qm", "new beta")
                head = git(case, "rev-parse", "HEAD")
                result = run_validator(case, "--base", base, "--head", head)
                self.assert_check(result, "GOV-SYNC-NEW-SKILL")
                self.assertIn(name, result.stdout)

    def test_g9_skill_change_without_new_validation_fails(self) -> None:
        base = init_git(self.root)
        write(self.root, "skills/alpha/SKILL.md", (self.root / "skills/alpha/SKILL.md").read_text() + "\nNew behavior.\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "change behavior")
        head = git(self.root, "rev-parse", "HEAD")
        self.assert_check(run_validator(self.root, "--base", base, "--head", head), "GOV-SYNC-SKILL")

    def test_g10_new_correction_preserves_old_report_passes(self) -> None:
        base = init_git(self.root)
        write(self.root, "docs/validations/alpha/2026-09-04-04-correction.md", REPORT.format(title="Correction Validation"))
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "add correction")
        head = git(self.root, "rev-parse", "HEAD")
        result = run_validator(self.root, "--base", base, "--head", head)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_g11_blocked_work_without_named_state_blocker_fails(self) -> None:
        self.replace("BACKLOG.md", "| Done |", "| Blocked |")
        self.replace("ROADMAP.md", "| Complete |", "| Blocked |")
        self.replace("docs/plans/alpha/tasks.md", "| Done | Validator reported Pass. |", "| Blocked | External dependency is unavailable. |")
        self.assert_check(run_validator(self.root, "--all"), "GOV-BLOCKER")

    def test_g12_complete_work_with_evidence_passes(self) -> None:
        result = run_validator(self.root, "--all")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_g13_validated_spec_without_passing_report_fails(self) -> None:
        self.replace("docs/specs/alpha/spec.md", "Status: Implemented", "Status: Validated")
        self.replace("docs/specs/alpha/spec.md", "Specification validation: [Report](../../validations/alpha/2026-09-04-01-specification.md)", "Specification validation: unavailable")
        self.assert_check(run_validator(self.root, "--all"), "GOV-SPEC-VALIDATION")

    def test_g14_done_task_without_output_or_evidence_fails(self) -> None:
        self.replace("docs/plans/alpha/tasks.md", "| `skills/alpha/SKILL.md` | Package exists. |", "| — | — |")
        self.assert_check(run_validator(self.root, "--all"), "GOV-TASK-EVIDENCE")

    def test_g15_parallel_marker_is_required(self) -> None:
        self.replace("BACKLOG.md", "| Done |", "| In progress |")
        self.replace("ROADMAP.md", "| Complete |", "| Active |")
        self.replace("docs/plans/alpha/tasks.md", "Status: Complete", "Status: Active")
        self.replace(
            "docs/plans/alpha/tasks.md",
            "| 1.1 | Build alpha. | `skills/alpha/SKILL.md` | Package exists. | None | Done | Validator reported Pass. |",
            "| 1.1 | Parallel: Yes. Build alpha. | `skills/alpha/SKILL.md` | Package exists. | None | In progress | Work started. |\n"
            "| 1.2 | Check alpha. | `skills/alpha/SKILL.md` | Package exists. | None | In progress | Work started. |",
        )
        self.assert_check(run_validator(self.root, "--all"), "GOV-TASK-CONCURRENCY")


class IndependentFindingRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="governance-regressions-")
        self.root = Path(self.temp.name)
        make_valid_repo(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assert_check(self, result: subprocess.CompletedProcess[str], check_id: str, code: int = 1) -> None:
        self.assertEqual(result.returncode, code, result.stdout)
        self.assertIn(check_id, result.stdout)

    def replace(self, relative: str, old: str, new: str) -> None:
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def test_n1_missing_state_sections_fails(self) -> None:
        write(self.root, "STATE.md", "# State\n\nState data without required sections.\n")
        self.assert_check(run_validator(self.root, "--all"), "GOV-STATE-SECTIONS")

    def test_n2_roadmap_controls_are_required(self) -> None:
        variants = {
            "current batch": ROADMAP.replace("Current batch: 1.\n\n", ""),
            "completion rules": ROADMAP.split("\n## Batch completion rules", 1)[0] + "\n",
        }
        for name, content in variants.items():
            with self.subTest(name=name):
                write(self.root, "ROADMAP.md", content)
                self.assert_check(run_validator(self.root, "--all"), "GOV-ROADMAP-CONTROLS")
                write(self.root, "ROADMAP.md", ROADMAP)

    def test_n3_backlog_specification_and_task_links_are_required(self) -> None:
        variants = {
            "specification": "[Specification](docs/specs/alpha/spec.md)",
            "task list": "[Tasks](docs/plans/alpha/tasks.md)",
        }
        for name, old in variants.items():
            with self.subTest(name=name):
                write(self.root, "BACKLOG.md", BACKLOG.replace(old, "—"))
                self.assert_check(run_validator(self.root, "--all"), "GOV-BACKLOG-LINK")
                write(self.root, "BACKLOG.md", BACKLOG)

    def test_n4_completed_roadmap_specification_link_is_required(self) -> None:
        write(self.root, "ROADMAP.md", ROADMAP.replace("[Specification](docs/specs/alpha/spec.md)", "—"))
        self.assert_check(run_validator(self.root, "--all"), "GOV-ROADMAP-LINK")

    def test_n5_passing_report_cannot_keep_blocking_finding(self) -> None:
        path = self.root / "docs/validations/alpha/2026-09-04-03-implementation.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nA blocking finding remains.\n", encoding="utf-8")
        self.assert_check(run_validator(self.root, "--all"), "GOV-REPORT-RESULT")

    def test_n6_newer_failed_implementation_overrides_old_pass(self) -> None:
        failed = REPORT.format(title="Later Implementation Validation").replace("Result: Pass", "Result: Fail")
        failed = failed.replace("No blocking finding exists.", "A blocking finding remains.")
        failed = failed.replace("alpha version 1.0", "alpha version 1.1")
        write(self.root, "docs/validations/alpha/2026-09-04-04-implementation.md", failed)
        self.assert_check(run_validator(self.root, "--all"), "GOV-LATEST-VALIDATION")

    def test_n7_impossible_calendar_date_fails(self) -> None:
        self.replace("docs/specs/alpha/spec.md", "Date: 2026-09-04", "Date: 2026-99-99")
        self.assert_check(run_validator(self.root, "--all"), "GOV-DATE")

    def test_n8_review_cannot_have_in_progress_task(self) -> None:
        self.replace("BACKLOG.md", "| Done |", "| Review |")
        self.replace("ROADMAP.md", "| Complete |", "| Active |")
        self.replace("docs/plans/alpha/tasks.md", "Status: Complete", "Status: Active")
        self.replace("docs/plans/alpha/tasks.md", "| Done | Validator reported Pass. |", "| In progress | Work is active. |")
        self.assert_check(run_validator(self.root, "--all"), "GOV-REVIEW")

    def test_n9_passing_report_needs_artifact_identity(self) -> None:
        path = self.root / "docs/validations/alpha/2026-09-04-01-specification.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("Validated artifact: alpha version 1.0.\n\n", "")
        path.write_text(text, encoding="utf-8")
        self.assert_check(run_validator(self.root, "--all"), "GOV-REPORT-ARTIFACT")

    def test_n10_done_non_skill_work_does_not_need_skill_package(self) -> None:
        shutil.rmtree(self.root / "skills/alpha")
        shutil.rmtree(self.root / "evaluations/alpha")
        spec = (self.root / "docs/specs/alpha/spec.md").read_text(encoding="utf-8")
        spec = spec.replace("Skill: [Package](../../../skills/alpha/SKILL.md)\n", "")
        spec = spec.replace("Evaluation: [Cases](../../../evaluations/alpha/cases.md)\n", "")
        (self.root / "docs/specs/alpha/spec.md").write_text(spec, encoding="utf-8")
        result = run_validator(self.root, "--all")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_t6_non_skill_work_is_non_skill_from_initial_creation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="governance-non-skill-") as temp:
            root = Path(temp)
            make_valid_non_skill_repo(root)
            self.assertFalse((root / "skills/repository-governance").exists())
            self.assertFalse((root / "evaluations/repository-governance").exists())
            spec = (root / "docs/specs/repository-governance/spec.md").read_text(encoding="utf-8")
            tasks = (root / "docs/plans/repository-governance/tasks.md").read_text(encoding="utf-8")
            self.assertNotIn("skills/", spec)
            self.assertNotIn("evaluations/", spec)
            self.assertNotIn("skills/", tasks)
            self.assertIn("tools/validate_repository.py", spec)
            self.assertIn("tools/validate_repository.py", tasks)
            result = run_validator(root, "--all")
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_v4_base_completed_skill_cannot_be_reclassified_by_deletion(self) -> None:
        write(self.root, "skills/other/SKILL.md", "---\nname: other\ndescription: Keep root present.\n---\n")
        write(self.root, "evaluations/other/notes.md", "# Keep evaluation root present\n")
        base = init_git(self.root)
        shutil.rmtree(self.root / "skills/alpha")
        shutil.rmtree(self.root / "evaluations/alpha")
        spec_path = self.root / "docs/specs/alpha/spec.md"
        spec = spec_path.read_text(encoding="utf-8")
        spec = spec.replace("Skill: [Package](../../../skills/alpha/SKILL.md)\n", "")
        spec = spec.replace("Evaluation: [Cases](../../../evaluations/alpha/cases.md)\n", "")
        spec = spec.replace("2026-09-04-03-implementation.md", "2026-09-04-04-implementation.md")
        spec_path.write_text(spec, encoding="utf-8")
        write(
            self.root,
            "BACKLOG.md",
            BACKLOG.replace("2026-09-04-03-implementation.md", "2026-09-04-04-implementation.md"),
        )
        write(
            self.root,
            "docs/validations/alpha/2026-09-04-04-implementation.md",
            REPORT.format(title="Replacement Implementation Validation").replace("alpha version 1.0", "alpha version 1.1"),
        )
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "delete completed skill evidence")
        head = git(self.root, "rev-parse", "HEAD")
        self.assert_check(
            run_validator(self.root, "--base", base, "--head", head),
            "GOV-COMPLETED-SKILL-PRESERVATION",
        )


class ValidatorContractTests(unittest.TestCase):
    def test_invalid_root_and_git_ref_exit_two(self) -> None:
        with tempfile.TemporaryDirectory() as empty:
            result = run_validator(Path(empty), "--all")
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("GOV-COMMAND", result.stdout)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_valid_repo(root)
            init_git(root)
            result = run_validator(root, "--base", "missing", "--head", "HEAD")
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("GOV-GIT", result.stdout)

    def test_findings_aggregate_and_run_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_valid_repo(root)
            write(root, "STATE.md", STATE + "\nTODO\n")
            write(root, "ROADMAP.md", ROADMAP.replace("| Complete |", "| Active |"))
            before = {p.relative_to(root): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}
            result = run_validator(root, "--all")
            after = {p.relative_to(root): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            self.assertIn("GOV-PLACEHOLDER", result.stdout)
            self.assertIn("GOV-ROADMAP-STATUS", result.stdout)

    def test_multi_class_change_applies_each_rule(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_valid_repo(root)
            base = init_git(root)
            write(root, "skills/alpha/SKILL.md", (root / "skills/alpha/SKILL.md").read_text() + "\nChanged.\n")
            write(root, "tools/validate_repository.py", (root / "tools/validate_repository.py").read_text() + "\n# Candidate governance change.\n")
            git(root, "add", ".")
            git(root, "commit", "-qm", "multi class")
            head = git(root, "rev-parse", "HEAD")
            result = run_validator(root, "--base", base, "--head", head)
            self.assertIn("GOV-SYNC-SKILL", result.stdout)
            self.assertIn("GOV-SYNC-GOVERNANCE", result.stdout)


if __name__ == "__main__":
    unittest.main()
