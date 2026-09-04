#!/usr/bin/env python3
"""Validate codex-skill-hub governance artifacts without changing the repository."""

from __future__ import annotations

import argparse
import datetime as dt
import io
import os
import re
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


WORK_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"(?i)(?<![a-z])(TBD|TODO|FIXME)(?![a-z])|<work-id>")

BACKLOG_STATUSES = {"Backlog", "Ready", "In progress", "Review", "Blocked", "Done"}
ROADMAP_STATUSES = {"Planned", "Active", "Blocked", "Complete"}
ROADMAP_MAP = {
    "Backlog": "Planned",
    "Ready": "Planned",
    "In progress": "Active",
    "Review": "Active",
    "Blocked": "Blocked",
    "Done": "Complete",
}
TASK_STATUSES = {"Pending", "Ready", "In progress", "Blocked", "Done"}
SPEC_STATUSES = {"Draft for validation", "Validated", "Implemented", "Superseded"}
PLAN_STATUSES = {"Draft for validation", "Validated", "Active", "Complete", "Superseded"}
REPORT_RESULTS = {"Pass", "Pass with residual risk", "Fail"}

BACKLOG_COLUMNS = [
    "Batch", "Priority", "Work ID", "Purpose", "Status", "Specification", "Tasks", "Latest validation"
]
ROADMAP_COLUMNS = ["Batch", "Order", "Work ID", "Status", "Specification"]
TASK_COLUMNS = ["ID", "Task", "Output", "Verification", "Depends on", "Status", "Evidence"]
STATE_SECTIONS = [
    "Current objective", "Confirmed decisions", "Constraints", "Work status",
    "Blockers and open questions", "Key artifacts", "Next action", "Last updated",
]


@dataclass(order=True)
class Finding:
    level: str
    check_id: str
    path: str
    message: str


def clean(value: str) -> str:
    value = value.strip().rstrip()
    if value.endswith("  "):
        value = value[:-2].rstrip()
    if len(value) >= 2 and value[0] == value[-1] == "`":
        value = value[1:-1]
    return value.strip()


def parse_metadata(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines()[1:40]:
        if line.startswith("## "):
            break
        match = re.match(r"^([A-Za-z][A-Za-z -]+):\s*(.*?)\s*$", line)
        if match:
            result[match.group(1)] = clean(match.group(2))
    return result


def parse_tables(text: str) -> list[tuple[list[str], list[dict[str, str]]]]:
    lines = text.splitlines()
    tables: list[tuple[list[str], list[dict[str, str]]]] = []
    index = 0
    while index + 1 < len(lines):
        if "|" not in lines[index] or "|" not in lines[index + 1]:
            index += 1
            continue
        header = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        divider = [cell.strip() for cell in lines[index + 1].strip().strip("|").split("|")]
        if len(header) < 2 or len(header) != len(divider) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in divider):
            index += 1
            continue
        rows: list[dict[str, str]] = []
        index += 2
        while index < len(lines) and lines[index].strip().startswith("|"):
            cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
            if len(cells) == len(header):
                rows.append(dict(zip(header, cells)))
            index += 1
        tables.append((header, rows))
    return tables


def find_table(text: str, required: list[str]) -> tuple[list[str], list[dict[str, str]]] | None:
    for header, rows in parse_tables(text):
        if all(column in header for column in required):
            return header, rows
    return None


def all_table_rows(text: str, required: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for header, table_rows in parse_tables(text):
        if all(column in header for column in required):
            rows.extend(table_rows)
    return rows


def strip_fenced_code(text: str) -> str:
    output: list[str] = []
    fenced = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced and "Placeholder values such as" not in line:
            output.append(line)
    return "\n".join(output)


def exact_path_exists(root: Path, path: Path) -> bool:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    current = root.resolve()
    for part in relative.parts:
        try:
            names = {entry.name for entry in current.iterdir()}
        except OSError:
            return False
        if part not in names:
            return False
        current = current / part
    return current.exists()


def link_targets(text: str) -> list[str]:
    targets: list[str] = []
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip().split()[0].strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        targets.append(target.split("#", 1)[0])
    return targets


def linked_paths(root: Path, source: Path, text: str) -> set[Path]:
    result: set[Path] = set()
    for target in link_targets(text):
        if target:
            result.add((source.parent / target).resolve())
    return result


def report_order(path: Path) -> tuple[str, int, str]:
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-(\d+)-(.+)\.md", path.name)
    if not match:
        return ("0000-00-00", -1, path.name)
    return (match.group(1), int(match.group(2)), match.group(3))


def report_has_blocking_finding(text: str) -> bool:
    patterns = (
        r"\bblocking (?:finding|defect|issue|risk)s? (?:remain|remains|exist|exists|is unresolved)",
        r"\bunresolved blocking (?:finding|defect|issue|risk)",
        r"^###?\s+blocking (?:finding|defect|issue)",
    )
    for line in text.splitlines():
        lowered = line.lower()
        if "no blocking" in lowered or "without a blocking" in lowered or "no unresolved blocking" in lowered:
            continue
        if any(re.search(pattern, line, re.I) for pattern in patterns):
            return True
    return False


def has_artifact_identity(text: str) -> bool:
    match = re.search(r"(?im)^Validated artifacts?:\s*(.+)$", text)
    if not match:
        return False
    value = match.group(1)
    return bool(
        re.search(r"\bversion\s+\d+\.\d+(?:\.\d+)?\b", value, re.I)
        or re.search(r"\b[0-9a-f]{40}(?:[0-9a-f]{24})?\b", value, re.I)
        or re.search(r"\b(?:git )?tree\b", value, re.I)
    )


class Validator:
    def __init__(
        self,
        root: Path,
        changed: list[tuple[str, str, str | None]] | None = None,
        base_backlog_statuses: dict[str, str] | None = None,
        base_completed_skills: set[str] | None = None,
    ):
        self.root = root.resolve()
        self.changed = changed
        self.base_backlog_statuses = base_backlog_statuses or {}
        self.base_completed_skills = base_completed_skills or set()
        self.findings: list[Finding] = []
        self.texts: dict[Path, str] = {}
        self.specs: dict[str, tuple[Path, dict[str, str], str]] = {}
        self.plans: dict[str, tuple[Path, dict[str, str], str, list[dict[str, str]]]] = {}
        self.reports: dict[str, list[tuple[Path, dict[str, str], str]]] = {}
        self.backlog_rows: dict[str, dict[str, str]] = {}
        self.roadmap_rows: dict[str, dict[str, str]] = {}

    def add(self, check_id: str, path: str | Path, message: str, level: str = "ERROR") -> None:
        try:
            display = str(Path(path).resolve().relative_to(self.root)) if isinstance(path, Path) else path
        except ValueError:
            display = str(path)
        self.findings.append(Finding(level, check_id, display, message))

    def read(self, path: Path) -> str:
        if path not in self.texts:
            try:
                self.texts[path] = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                self.add("GOV-READ", path, f"cannot read UTF-8 text: {error}")
                self.texts[path] = ""
        return self.texts[path]

    def validate(self) -> list[Finding]:
        self.check_structure()
        self.collect_documents()
        self.check_documents()
        self.check_links()
        self.check_placeholders()
        self.check_backlog_and_roadmap()
        self.check_plans()
        self.check_spec_evidence()
        self.check_reports()
        self.check_delivery()
        if self.changed is not None:
            self.check_synchronization()
        return sorted(self.findings)

    def check_structure(self) -> None:
        required = [
            "STATE.md", "BACKLOG.md", "ROADMAP.md", "README.md", "docs/specs", "docs/plans",
            "docs/validations", "evaluations", "skills", "tools/validate_repository.py",
            "tests/repository_validation", ".github/pull_request_template.md",
            ".github/workflows/validate-repository.yml",
        ]
        for name in required:
            if not (self.root / name).exists():
                self.add("GOV-STRUCTURE", name, "required canonical path is missing")
        state = self.root / "STATE.md"
        if state.is_file():
            headings = {match.group(1).strip() for match in re.finditer(r"(?m)^##\s+(.+?)\s*$", self.read(state))}
            for section in STATE_SECTIONS:
                if section not in headings:
                    self.add("GOV-STATE-SECTIONS", state, f"missing required section: {section}")
        roadmap = self.root / "ROADMAP.md"
        if roadmap.is_file():
            text = self.read(roadmap)
            if not re.search(r"(?im)^Current batch:\s*\S", text):
                self.add("GOV-ROADMAP-CONTROLS", roadmap, "current batch is missing")
            completion = re.search(r"(?ims)^##\s+Batch completion rules\s*$([\s\S]*)", text)
            if not completion or not re.search(r"(?m)^-\s+\S", completion.group(1)):
                self.add("GOV-ROADMAP-CONTROLS", roadmap, "batch completion rules are missing")

    def collect_documents(self) -> None:
        for path in sorted((self.root / "docs/specs").glob("*/spec.md")) if (self.root / "docs/specs").exists() else []:
            text = self.read(path)
            meta = parse_metadata(text)
            work_id = meta.get("Work ID", "")
            self.specs[work_id] = (path, meta, text)
            if clean(work_id) != path.parent.name:
                self.add("GOV-WORK-ID", path, "Work ID must match the parent directory")
        for path in sorted((self.root / "docs/plans").glob("*/tasks.md")) if (self.root / "docs/plans").exists() else []:
            text = self.read(path)
            meta = parse_metadata(text)
            work_id = meta.get("Work ID", "")
            table = find_table(text, TASK_COLUMNS)
            rows = all_table_rows(text, TASK_COLUMNS) if table else []
            self.plans[work_id] = (path, meta, text, rows)
            if clean(work_id) != path.parent.name:
                self.add("GOV-WORK-ID", path, "Work ID must match the parent directory")
        for path in sorted((self.root / "docs/validations").glob("*/*.md")) if (self.root / "docs/validations").exists() else []:
            text = self.read(path)
            meta = parse_metadata(text)
            work_id = meta.get("Work ID", "")
            self.reports.setdefault(work_id, []).append((path, meta, text))
            if clean(work_id) != path.parent.name:
                self.add("GOV-WORK-ID", path, "Work ID must match the parent directory")

    def check_documents(self) -> None:
        for collection, kind in ((self.specs, "specification"), (self.plans, "task list")):
            for work_id, item in collection.items():
                path, meta, text = item[:3]
                for field in ("Version", "Status", "Date", "Work ID"):
                    if not meta.get(field):
                        self.add("GOV-METADATA", path, f"missing {field} metadata")
                if meta.get("Version") and not VERSION_RE.fullmatch(meta["Version"]):
                    self.add("GOV-METADATA", path, "Version must use a numeric semantic version")
                if meta.get("Date"):
                    self.check_date(path, meta["Date"])
                if work_id and not WORK_ID_RE.fullmatch(work_id):
                    self.add("GOV-WORK-ID", path, "Work ID has an invalid format")
                allowed = SPEC_STATUSES if kind == "specification" else PLAN_STATUSES
                if meta.get("Status") and meta["Status"] not in allowed:
                    self.add("GOV-STATUS", path, f"invalid {kind} status {meta['Status']!r}")
        for reports in self.reports.values():
            for path, meta, _ in reports:
                for field in ("Version", "Date", "Work ID", "Result", "Evaluator"):
                    if not meta.get(field):
                        self.add("GOV-METADATA", path, f"missing {field} metadata")
                if meta.get("Version") and not VERSION_RE.fullmatch(meta["Version"]):
                    self.add("GOV-METADATA", path, "Version must use a numeric semantic version")
                if meta.get("Date"):
                    self.check_date(path, meta["Date"])
                if meta.get("Result") and meta["Result"] not in REPORT_RESULTS:
                    self.add("GOV-STATUS", path, f"invalid validation result {meta['Result']!r}")

    def check_date(self, path: Path, value: str) -> None:
        if not DATE_RE.fullmatch(value):
            self.add("GOV-DATE", path, "Date must use YYYY-MM-DD")
            return
        try:
            dt.date.fromisoformat(value)
        except ValueError:
            self.add("GOV-DATE", path, "Date must be a real calendar date")

    def check_links(self) -> None:
        for path in sorted(self.root.rglob("*.md")):
            if ".git" in path.parts:
                continue
            text = self.read(path)
            for target in link_targets(text):
                candidate = path.parent / target
                if not exact_path_exists(self.root, candidate):
                    self.add("GOV-LINK", path, f"relative link target does not exist with exact case: {target}")

    def check_placeholders(self) -> None:
        paths = [self.root / name for name in ("STATE.md", "BACKLOG.md", "ROADMAP.md")]
        paths += [item[0] for item in self.specs.values()]
        paths += [item[0] for item in self.plans.values()]
        for path in paths:
            if path.exists() and PLACEHOLDER_RE.search(strip_fenced_code(self.read(path))):
                self.add("GOV-PLACEHOLDER", path, "active or completed artifact contains a forbidden placeholder")

    def check_backlog_and_roadmap(self) -> None:
        backlog = self.root / "BACKLOG.md"
        roadmap = self.root / "ROADMAP.md"
        if not backlog.exists() or not roadmap.exists():
            return
        backlog_text = self.read(backlog)
        roadmap_text = self.read(roadmap)
        btable = find_table(backlog_text, BACKLOG_COLUMNS)
        rtable = find_table(roadmap_text, ROADMAP_COLUMNS)
        if not btable:
            self.add("GOV-TABLE", backlog, "backlog table is missing required columns")
            return
        if btable[0][: len(BACKLOG_COLUMNS)] != BACKLOG_COLUMNS:
            self.add("GOV-TABLE", backlog, "required backlog columns are missing or renamed")
        if not rtable:
            self.add("GOV-TABLE", roadmap, "roadmap table is missing required columns")
            return
        if rtable[0][: len(ROADMAP_COLUMNS)] != ROADMAP_COLUMNS:
            self.add("GOV-TABLE", roadmap, "required roadmap columns are missing or renamed")
        for row in btable[1]:
            work_id = clean(row["Work ID"])
            if work_id in self.backlog_rows:
                self.add("GOV-DUPLICATE-WORK", backlog, f"duplicate Work ID {work_id}")
            self.backlog_rows[work_id] = row
            if not WORK_ID_RE.fullmatch(work_id):
                self.add("GOV-WORK-ID", backlog, f"invalid backlog Work ID {work_id!r}")
            if row["Status"] not in BACKLOG_STATUSES:
                self.add("GOV-STATUS", backlog, f"invalid backlog status {row['Status']!r}")
        for row in rtable[1]:
            work_id = clean(row["Work ID"])
            if work_id in self.roadmap_rows:
                self.add("GOV-DUPLICATE-WORK", roadmap, f"duplicate Work ID {work_id}")
            self.roadmap_rows[work_id] = row
            if row["Status"] not in ROADMAP_STATUSES:
                self.add("GOV-STATUS", roadmap, f"invalid roadmap status {row['Status']!r}")
        for work_id, brow in self.backlog_rows.items():
            rrow = self.roadmap_rows.get(work_id)
            if not rrow:
                self.add("GOV-ROADMAP", roadmap, f"missing roadmap entry for {work_id}")
                continue
            expected = ROADMAP_MAP.get(brow["Status"])
            if expected and rrow["Status"] != expected:
                self.add("GOV-ROADMAP-STATUS", roadmap, f"{work_id} must be {expected} for backlog status {brow['Status']}")
            status = brow["Status"]
            if status != "Backlog" and work_id not in self.specs:
                self.add("GOV-BACKLOG-LINK", backlog, f"{work_id} needs a current specification")
            if status != "Backlog" and work_id in self.specs:
                expected = self.specs[work_id][0].resolve()
                if expected not in linked_paths(self.root, backlog, brow["Specification"]):
                    self.add("GOV-BACKLOG-LINK", backlog, f"{work_id} must link to its current specification")
            if status in {"In progress", "Review", "Blocked", "Done"} and work_id not in self.plans:
                self.add("GOV-BACKLOG-LINK", backlog, f"{work_id} needs a task list")
            if status in {"In progress", "Review", "Blocked", "Done"} and work_id in self.plans:
                expected = self.plans[work_id][0].resolve()
                if expected not in linked_paths(self.root, backlog, brow["Tasks"]):
                    self.add("GOV-BACKLOG-LINK", backlog, f"{work_id} must link to its current task list")
            if status in {"In progress", "Review", "Blocked", "Done"}:
                expected = self.specs.get(work_id, (None,))[0]
                if expected and expected.resolve() not in linked_paths(self.root, roadmap, rrow["Specification"]):
                    self.add("GOV-ROADMAP-LINK", roadmap, f"{work_id} must link to its current specification")
            if status in {"Review", "Done"}:
                targets = linked_paths(self.root, backlog, brow["Latest validation"])
                latest = self.latest_delivery_report(work_id)
                if not latest or latest.resolve() not in targets or not self.is_passing_report(latest, work_id):
                    self.add("GOV-LATEST-VALIDATION", backlog, f"{work_id} needs a linked passing latest validation report")
            if status == "Review" and work_id in self.plans and any(task["Status"] == "In progress" for task in self.plans[work_id][3]):
                self.add("GOV-REVIEW", backlog, f"{work_id} cannot enter Review while a task is In progress")

    def check_plans(self) -> None:
        for work_id, (path, meta, text, rows) in self.plans.items():
            table = find_table(text, TASK_COLUMNS)
            if not table:
                self.add("GOV-TABLE", path, "task table is missing required columns")
                continue
            if table[0][: len(TASK_COLUMNS)] != TASK_COLUMNS:
                self.add("GOV-TABLE", path, "required task columns are missing or renamed")
            by_id = {row["ID"]: row for row in rows}
            active = [row for row in rows if row["Status"] == "In progress"]
            if len(active) > 1 and any("Parallel: Yes" not in row["Task"] for row in active):
                self.add("GOV-TASK-CONCURRENCY", path, "concurrent active tasks must each include Parallel: Yes")
            for row in rows:
                task_id = row["ID"]
                status = row["Status"]
                if status not in TASK_STATUSES:
                    self.add("GOV-STATUS", path, f"task {task_id} has invalid status {status!r}")
                dependencies = [] if row["Depends on"] == "None" else [part.strip() for part in row["Depends on"].split(",")]
                for dependency in dependencies:
                    if dependency not in by_id:
                        self.add("GOV-TASK-DEPENDENCY", path, f"task {task_id} has unknown dependency {dependency}")
                    elif status == "Done" and by_id[dependency]["Status"] != "Done":
                        self.add("GOV-TASK-DEPENDENCY", path, f"done task {task_id} has incomplete dependency {dependency}")
                    elif status == "Ready" and by_id[dependency]["Status"] != "Done":
                        self.add("GOV-TASK-DEPENDENCY", path, f"ready task {task_id} has incomplete dependency {dependency}")
                if status == "Done":
                    if self.empty_evidence(row["Output"]) or self.empty_evidence(row["Verification"]) or self.empty_evidence(row["Evidence"]):
                        self.add("GOV-TASK-EVIDENCE", path, f"done task {task_id} needs output and verification evidence")
            visiting: set[str] = set()
            visited: set[str] = set()

            def visit(task_id: str) -> None:
                if task_id in visiting:
                    self.add("GOV-TASK-CYCLE", path, f"task dependency cycle includes {task_id}")
                    return
                if task_id in visited:
                    return
                visiting.add(task_id)
                row = by_id[task_id]
                dependencies = [] if row["Depends on"] == "None" else [part.strip() for part in row["Depends on"].split(",")]
                for dependency in dependencies:
                    if dependency in by_id:
                        visit(dependency)
                visiting.remove(task_id)
                visited.add(task_id)

            for task_id in by_id:
                visit(task_id)
            if meta.get("Status") == "Complete" and any(row["Status"] != "Done" for row in rows):
                self.add("GOV-PLAN-COMPLETE", path, "complete task list has an unfinished task")
            if meta.get("Status") in {"Validated", "Active", "Complete"} and not self.has_linked_passing_report(path, text, work_id, "task"):
                self.add("GOV-PLAN-VALIDATION", path, "task-list status requires a linked passing task-list validation report")

    @staticmethod
    def empty_evidence(value: str) -> bool:
        value = clean(value)
        return not value or value in {"—", "-", "None"} or bool(PLACEHOLDER_RE.search(value))

    def check_spec_evidence(self) -> None:
        for work_id, (path, meta, text) in self.specs.items():
            status = meta.get("Status")
            if status in {"Validated", "Implemented"} and not self.has_linked_passing_report(path, text, work_id, "spec"):
                self.add("GOV-SPEC-VALIDATION", path, "validated specification needs a linked passing specification validation report")
            if status == "Implemented":
                targets = linked_paths(self.root, path, text)
                latest = self.latest_delivery_report(work_id)
                if not latest or latest.resolve() not in targets or not self.is_passing_report(latest, work_id):
                    self.add("GOV-SPEC-IMPLEMENTED", path, "implemented specification needs a linked passing implementation report")

    def has_linked_passing_report(self, path: Path, text: str, work_id: str, kind: str) -> bool:
        for target in linked_paths(self.root, path, text):
            if self.is_passing_report(target, work_id):
                if kind == "spec" and "specification" not in target.name:
                    continue
                if kind == "task" and "task-list" not in target.name:
                    continue
                return True
        return False

    def is_passing_report(self, path: Path, work_id: str) -> bool:
        if not path.is_file() or "docs/validations" not in path.as_posix():
            return False
        meta = parse_metadata(self.read(path))
        text = self.read(path)
        return (
            meta.get("Work ID") == work_id
            and meta.get("Result") in {"Pass", "Pass with residual risk"}
            and not report_has_blocking_finding(text)
            and has_artifact_identity(text)
        )

    def latest_delivery_report(self, work_id: str) -> Path | None:
        applicable = [
            path for path, _, _ in self.reports.get(work_id, [])
            if any(kind in path.stem for kind in ("implementation", "migration", "delivery"))
        ]
        return max(applicable, key=report_order) if applicable else None

    def check_reports(self) -> None:
        for work_id, reports in self.reports.items():
            for path, meta, text in reports:
                lowered = text.lower()
                for section, terms in {
                    "method": ("## method", "## validation method"),
                    "evidence": ("## evidence", "evidence"),
                    "findings": ("## findings", "finding"),
                    "residual risks": ("## residual risks", "## residual risk"),
                }.items():
                    if not any(term in lowered for term in terms):
                        self.add("GOV-REPORT-CONTENT", path, f"validation report is missing {section}")
                if meta.get("Result") == "Fail" and "blocking" not in lowered:
                    self.add("GOV-REPORT-CONTENT", path, "failed report must identify its blocking finding")
                if meta.get("Result") in {"Pass", "Pass with residual risk"}:
                    if report_has_blocking_finding(text):
                        self.add("GOV-REPORT-RESULT", path, "passing report states that a blocking finding remains")
                    if not has_artifact_identity(text):
                        self.add("GOV-REPORT-ARTIFACT", path, "passing report must identify an artifact version or git tree")

    def check_delivery(self) -> None:
        state_text = self.read(self.root / "STATE.md") if (self.root / "STATE.md").exists() else ""
        for work_id, row in self.backlog_rows.items():
            status = row["Status"]
            plan = self.plans.get(work_id)
            spec = self.specs.get(work_id)
            if status == "Done":
                if not plan or any(task["Status"] != "Done" for task in plan[3]):
                    self.add("GOV-DONE-TASKS", "BACKLOG.md", f"{work_id} is Done but its tasks are not all Done")
                if not spec or spec[1].get("Status") != "Implemented":
                    self.add("GOV-DONE-SPEC", "BACKLOG.md", f"{work_id} is Done but its specification is not Implemented")
                skill_dir = self.root / "skills" / work_id
                if skill_dir.exists():
                    if not (skill_dir / "SKILL.md").is_file():
                        self.add("GOV-DONE-IMPLEMENTATION", "BACKLOG.md", f"{work_id} is Done but skill implementation is missing")
                    evaluation_dir = self.root / "evaluations" / work_id
                    if not (evaluation_dir / "cases.md").is_file() or not any(p.name != "cases.md" for p in evaluation_dir.glob("*.md")):
                        self.add("GOV-DONE-EVALUATION", "BACKLOG.md", f"{work_id} is Done but evaluation evidence is missing")
            if status == "Blocked":
                has_blocked_task = bool(plan and any(task["Status"] == "Blocked" for task in plan[3]))
                state_has_blocker = bool(re.search(rf"(?m)^.*{re.escape(work_id)}.*block", state_text, re.I))
                if not has_blocked_task or not state_has_blocker:
                    self.add("GOV-BLOCKER", "STATE.md", f"{work_id} needs a named blocker in state and its task list")

    def check_synchronization(self) -> None:
        assert self.changed is not None
        paths = {new or old for status, old, new in self.changed for _ in [0]}
        changes = [(status, old, new) for status, old, new in self.changed]
        new_skills = {PurePosixPath(new or old).parts[1] for status, old, new in changes if status.startswith("A") and re.fullmatch(r"skills/[^/]+/SKILL\.md", new or old)}
        skill_changes = {PurePosixPath(new or old).parts[1] for status, old, new in changes if (new or old).startswith("skills/") and PurePosixPath(new or old).parts[1] not in new_skills}
        eval_changes = {PurePosixPath(new or old).parts[1] for status, old, new in changes if (new or old).startswith("evaluations/")}
        validation_changes = {PurePosixPath(new or old).parts[2] for status, old, new in changes if (new or old).startswith("docs/validations/") and len(PurePosixPath(new or old).parts) > 2 and status.startswith("A")}
        for work_id in sorted(self.base_completed_skills):
            missing: list[str] = []
            skill_file = self.root / "skills" / work_id / "SKILL.md"
            evaluation_dir = self.root / "evaluations" / work_id
            cases_file = evaluation_dir / "cases.md"
            result_files = [path for path in evaluation_dir.glob("*.md") if path.name != "cases.md"] if evaluation_dir.is_dir() else []
            spec = self.specs.get(work_id)
            spec_targets = linked_paths(self.root, spec[0], spec[2]) if spec else set()
            if not skill_file.is_file():
                missing.append(f"skills/{work_id}/SKILL.md")
            if not cases_file.is_file():
                missing.append(f"evaluations/{work_id}/cases.md")
            if not result_files:
                missing.append(f"evaluations/{work_id}/<result>.md")
            if not spec or skill_file.resolve() not in spec_targets:
                missing.append("specification link to the skill package")
            if not spec or not any(
                target == evaluation_dir.resolve() or evaluation_dir.resolve() in target.parents
                for target in spec_targets
            ):
                missing.append("specification link to evaluation evidence")
            if missing:
                self.add(
                    "GOV-COMPLETED-SKILL-PRESERVATION",
                    f"skills/{work_id}",
                    "completed skill evidence from the merge base must be preserved; missing " + ", ".join(missing),
                )
        for skill_id in new_skills:
            for required, exists in {
                "specification": skill_id in self.specs,
                "task list": skill_id in self.plans,
                "evaluation cases": (self.root / "evaluations" / skill_id / "cases.md").is_file(),
                "validation report": skill_id in validation_changes,
                "backlog row": skill_id in self.backlog_rows,
                "roadmap entry": skill_id in self.roadmap_rows,
                "current state": skill_id in self.read(self.root / "STATE.md"),
            }.items():
                if not exists:
                    self.add("GOV-SYNC-NEW-SKILL", f"skills/{skill_id}", f"new skill needs synchronized {required}")
        for skill_id in skill_changes:
            if skill_id not in eval_changes or skill_id not in validation_changes:
                self.add("GOV-SYNC-SKILL", f"skills/{skill_id}", "skill behavior change needs updated evaluation and a new validation report")
        for skill_id in eval_changes - skill_changes - new_skills:
            explicit_result = any(
                (new or old).startswith(f"evaluations/{skill_id}/")
                and PurePosixPath(new or old).name != "cases.md"
                for status, old, new in changes
            )
            if skill_id not in validation_changes and not explicit_result:
                self.add("GOV-SYNC-EVALUATION", f"evaluations/{skill_id}", "evaluation-only change needs a new validation report or explicit result report")
        governance_triggers = {
            "tools/validate_repository.py", ".github/pull_request_template.md",
            ".github/workflows/validate-repository.yml",
        }
        governance = bool(paths & governance_triggers) or any(path.startswith("docs/specs/repository-governance/") for path in paths)
        if governance:
            required_groups = {
                "governance specification": any(path.startswith("docs/specs/repository-governance/") for path in paths),
                "validator tests": any(path.startswith("tests/repository_validation/") for path in paths),
                "new governance validation": "repository-governance" in validation_changes,
            }
            for label, present in required_groups.items():
                if not present:
                    self.add("GOV-SYNC-GOVERNANCE", "docs/specs/repository-governance/spec.md", f"governance change needs synchronized {label}")
        for work_id, row in self.backlog_rows.items():
            old_status = self.base_backlog_statuses.get(work_id)
            new_status = row["Status"]
            if old_status == new_status:
                continue
            plan = self.plans.get(work_id)
            spec = self.specs.get(work_id)
            if new_status == "In progress":
                active_task = bool(plan and any(task["Status"] == "In progress" for task in plan[3]))
                if not spec or spec[1].get("Status") not in {"Validated", "Implemented"} or not active_task:
                    self.add("GOV-SYNC-WORK-START", "BACKLOG.md", f"{work_id} start needs a validated specification and active task")
            if new_status == "Blocked":
                has_blocked_task = bool(plan and any(task["Status"] == "Blocked" for task in plan[3]))
                if not has_blocked_task:
                    self.add("GOV-SYNC-WORK-BLOCKED", "BACKLOG.md", f"{work_id} blocked status needs a blocked task")


def backlog_statuses(text: str) -> dict[str, str]:
    table = find_table(text, BACKLOG_COLUMNS)
    if not table:
        return {}
    return {clean(row["Work ID"]): row["Status"] for row in table[1]}


def completed_skill_ids(root: Path, ref: str, statuses: dict[str, str]) -> set[str]:
    listing = str(git(root, "ls-tree", "-r", "--name-only", ref))
    evidence_ids: set[str] = set()
    for line in listing.splitlines():
        match = re.fullmatch(r"skills/([^/]+)/SKILL\.md", line)
        if match:
            evidence_ids.add(match.group(1))
            continue
        match = re.fullmatch(r"evaluations/([^/]+)/[^/]+\.md", line)
        if match:
            evidence_ids.add(match.group(1))
    return {work_id for work_id in evidence_ids if statuses.get(work_id) == "Done"}


def git(root: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise ValueError(result.stderr.decode("utf-8", "replace").strip() or "git command failed")
    return result.stdout if binary else result.stdout.decode("utf-8", "replace")


def parse_changed(root: Path, base: str, head: str) -> list[tuple[str, str, str | None]]:
    output = str(git(root, "diff", "--name-status", "--find-renames", base, head, "--"))
    changes: list[tuple[str, str, str | None]] = []
    for line in output.splitlines():
        parts = line.split("\t")
        if not parts:
            continue
        status = parts[0]
        if status.startswith("R") and len(parts) == 3:
            changes.append((status, parts[1], parts[2]))
        elif len(parts) == 2:
            changes.append((status, parts[1], None))
    return changes


def check_immutability(changes: list[tuple[str, str, str | None]]) -> list[Finding]:
    findings: list[Finding] = []
    for status, old, new in changes:
        if old.startswith("docs/validations/") and not status.startswith("A"):
            action = "renamed" if status.startswith("R") else "deleted" if status.startswith("D") else "modified"
            findings.append(Finding("ERROR", "GOV-IMMUTABLE", old, f"existing validation report was {action}"))
    return findings


def extract_ref(root: Path, ref: str, destination: Path) -> None:
    archive = git(root, "archive", "--format=tar", ref, binary=True)
    assert isinstance(archive, bytes)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as handle:
        for member in handle.getmembers():
            target = (destination / member.name).resolve()
            if destination.resolve() not in target.parents and target != destination.resolve():
                raise ValueError("git archive contains an unsafe path")
        handle.extractall(destination, filter="data")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true", help="validate the current tree")
    mode.add_argument("--base", help="base git reference for pull-request validation")
    parser.add_argument("--head", help="head git reference; requires --base")
    args = parser.parse_args(argv)
    if args.base and not args.head:
        parser.error("--base requires --head")
    if args.head and not args.base:
        parser.error("--head requires --base")
    return args


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv if argv is not None else sys.argv[1:])
    except SystemExit as error:
        return 0 if error.code == 0 else 2
    root = Path.cwd().resolve()
    if not (root / "tools/validate_repository.py").is_file():
        print("ERROR GOV-COMMAND .: current directory is not a repository root")
        print("Summary: 1 error, 0 warnings")
        return 2
    findings: list[Finding]
    if args.all:
        findings = Validator(root).validate()
    else:
        try:
            git(root, "rev-parse", "--verify", f"{args.base}^{{commit}}")
            git(root, "rev-parse", "--verify", f"{args.head}^{{commit}}")
            merge_base = str(git(root, "merge-base", args.base, args.head)).strip()
            if not merge_base:
                raise ValueError("base and head do not have a merge base")
            changes = parse_changed(root, merge_base, args.head)
            with tempfile.TemporaryDirectory(prefix="codex-governance-") as temp:
                head_root = Path(temp)
                extract_ref(root, args.head, head_root)
                try:
                    base_backlog = str(git(root, "show", f"{merge_base}:BACKLOG.md"))
                except ValueError:
                    base_backlog = ""
                base_statuses = backlog_statuses(base_backlog)
                base_skills = completed_skill_ids(root, merge_base, base_statuses)
                findings = Validator(head_root, changes, base_statuses, base_skills).validate()
            findings.extend(check_immutability(changes))
            findings.sort()
        except (OSError, ValueError) as error:
            print(f"ERROR GOV-GIT .: {error}")
            print("Summary: 1 error, 0 warnings")
            return 2
    for finding in findings:
        print(f"{finding.level} {finding.check_id} {finding.path}: {finding.message}")
    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARNING" for item in findings)
    print(f"Summary: {errors} error{'s' if errors != 1 else ''}, {warnings} warning{'s' if warnings != 1 else ''}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
