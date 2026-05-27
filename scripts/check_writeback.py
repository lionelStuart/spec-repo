#!/usr/bin/env python3

from pathlib import Path
import argparse
import re
import sys


REQUIRED_STATUS_SECTIONS = [
    "## Current Focus",
    "## Last Completed",
    "## Completion State",
    "## Open Issues",
    "## Last Validation",
    "## Next Steps",
]

REQUIRED_ROADMAP_SECTIONS = [
    "## Current Milestone",
    "## Project Completion Signals",
    "## Milestones",
]

REQUIRED_TASK_SECTIONS = [
    "## Status",
    "## Source",
    "## Goal",
    "## Done Means",
    "## Required Context",
    "## Modify Scope",
    "## Acceptance",
    "## Test Plan",
    "## Progress",
    "## Validation",
    "## Result",
]

PLACEHOLDER_PATTERN = re.compile(r"\[[^\]\n]+\]|YYYY-MM-DD")
INDEX_ROW_PATTERN = re.compile(r"^\|\s*([^|]+?)\s*\|\s*`?([^|`]+)`?\s*\|\s*([^|]+?)\s*\|", re.M)
CONTEXT_REF_PATTERN = re.compile(r"`([^`]+)`")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether project-memory write-back artifacts look complete.")
    parser.add_argument("repo", help="Target repository path")
    parser.add_argument("--task", help="Relative task file path, for example tasks/TASK-002-foo.md")
    return parser.parse_args()


def missing_sections(path: Path, sections: list[str]) -> list[str]:
    text = path.read_text()
    return [section for section in sections if section not in text]


def section_text(text: str, heading: str) -> str:
    pattern = rf"^{re.escape(heading)}\n\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.S | re.M)
    return match.group(1).strip() if match else ""


def parse_index_rows(index_text: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for match in INDEX_ROW_PATTERN.finditer(index_text):
        item_id = match.group(1).strip()
        file_path = match.group(2).strip()
        status = match.group(3).strip()
        if item_id in {"ID", "---"} or file_path == "File":
            continue
        rows[item_id] = {"file": file_path, "status": status}
    return rows


def normalize_repo_ref(repo: Path, ref: str) -> Path | None:
    if ref.startswith("repo/"):
        return repo.parent / ref
    if ref.startswith(("specs/", "tasks/", "decisions/", "learnings/", "skills/")):
        return repo / ref
    if ref in {"PROJECT.md", "STATUS.md", "INDEX.md", "ROADMAP.md", "ARCHITECTURE.md"}:
        return repo / ref
    return None


def contains_template_placeholder(text: str) -> bool:
    for match in PLACEHOLDER_PATTERN.finditer(text):
        token = match.group(0)
        if token in {"[x]", "[ ]"}:
            continue
        return True
    return False


def task_id_from_text(text: str) -> str | None:
    first_line = text.splitlines()[0] if text.splitlines() else ""
    match = re.match(r"#\s+(TASK-\d+):", first_line)
    return match.group(1) if match else None


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    failures: list[str] = []

    status = repo / "STATUS.md"
    index_file = repo / "INDEX.md"
    roadmap = repo / "ROADMAP.md"

    if not status.exists():
        failures.append("STATUS.md is missing")
    else:
        missing = missing_sections(status, REQUIRED_STATUS_SECTIONS)
        if missing:
            failures.append(f"STATUS.md missing sections: {', '.join(missing)}")

    if not index_file.exists():
        failures.append("INDEX.md is missing")
        index_text = ""
        index_rows: dict[str, dict[str, str]] = {}
    else:
        index_text = index_file.read_text()
        index_rows = parse_index_rows(index_text)
        if "## Tasks" not in index_text:
            failures.append("INDEX.md missing ## Tasks section")
        if contains_template_placeholder(index_text):
            failures.append("INDEX.md still contains template placeholders")

    if not roadmap.exists():
        failures.append("ROADMAP.md is missing")
    else:
        missing = missing_sections(roadmap, REQUIRED_ROADMAP_SECTIONS)
        if missing:
            failures.append(f"ROADMAP.md missing sections: {', '.join(missing)}")

    if args.task:
        task_file = repo / args.task
        if not task_file.exists():
            failures.append(f"task file not found: {args.task}")
        else:
            task_text = task_file.read_text()
            missing = missing_sections(task_file, REQUIRED_TASK_SECTIONS)
            if missing:
                failures.append(f"{args.task} missing sections: {', '.join(missing)}")
            if contains_template_placeholder(task_text):
                failures.append(f"{args.task} still contains template placeholders")

            task_id = task_id_from_text(task_text)
            if not task_id:
                failures.append(f"{args.task} does not start with a TASK-NNN heading")
            elif task_id not in index_rows:
                failures.append(f"{args.task} is not listed in INDEX.md")
            else:
                indexed_file = index_rows[task_id]["file"]
                if indexed_file != args.task:
                    failures.append(f"{task_id} INDEX.md file is {indexed_file}, expected {args.task}")
                task_status = section_text(task_text, "## Status").splitlines()[0].strip()
                indexed_status = index_rows[task_id]["status"]
                if task_status and task_status != indexed_status:
                    failures.append(f"{task_id} status mismatch: task has {task_status}, INDEX.md has {indexed_status}")

            required_context = section_text(task_text, "## Required Context")
            for ref in CONTEXT_REF_PATTERN.findall(required_context):
                target = normalize_repo_ref(repo, ref)
                if target and not target.exists():
                    failures.append(f"{args.task} references missing context: {ref}")

            source = section_text(task_text, "## Source").strip("` \n")
            if source and source not in index_rows:
                failures.append(f"{args.task} source spec is not listed in INDEX.md: {source}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: write-back artifacts look structurally complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
