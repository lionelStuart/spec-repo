#!/usr/bin/env python3

from pathlib import Path
import argparse
import datetime as dt
import re
import shutil
import sys


ACTIVE_STATUSES = {"draft", "ready", "doing", "active", "blocked"}
ARCHIVABLE_TASK_STATUSES = {"done", "canceled"}
ARCHIVABLE_SPEC_STATUSES = {"done", "superseded", "deprecated"}
DEFAULT_RECENT_KEEP = {
    "tasks": 5,
    "specs": 3,
}

SECTION_HEADERS = {
    "tasks": "## Tasks",
    "specs": "## Specs",
}

ARCHIVE_HEADERS = {
    "tasks": "## Archived Tasks",
    "specs": "## Archived Specs",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive a completed task or spec from active project memory.")
    parser.add_argument("repo", help="Target repo directory, for example ./repo")
    parser.add_argument("kind", choices=["tasks", "specs"], help="Item kind to archive")
    parser.add_argument("item_id", help="Item ID, for example TASK-001 or SPEC-001")
    parser.add_argument("--reason", default="no longer recent or active", help="Archive reason")
    parser.add_argument("--keep-recent", type=int, help="Number of inactive items to keep in active INDEX.md before archiving")
    parser.add_argument("--force", action="store_true", help="Archive even when status, dependency, or recent-retention checks would block it")
    return parser.parse_args()


def parse_table_rows(index_text: str, section: str) -> tuple[list[str], list[dict[str, str]]]:
    pattern = rf"{re.escape(section)}\n\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, index_text, re.S)
    if not match:
        return [], []
    lines = [line for line in match.group(1).splitlines() if line.strip()]
    rows: list[dict[str, str]] = []
    for line in lines:
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] in {"ID", "---"}:
            continue
        if len(cells) >= 5:
            rows.append(
                {
                    "id": cells[0],
                    "file": cells[1],
                    "status": cells[2],
                    "fourth": cells[3],
                    "depends_on": cells[4],
                    "line": line,
                }
            )
    return lines, rows


def find_row(index_text: str, kind: str, item_id: str) -> dict[str, str] | None:
    _, rows = parse_table_rows(index_text, SECTION_HEADERS[kind])
    for row in rows:
        if row["id"] == item_id:
            return row
    return None


def inactive_rows(index_text: str, kind: str) -> list[dict[str, str]]:
    allowed = ARCHIVABLE_TASK_STATUSES if kind == "tasks" else ARCHIVABLE_SPEC_STATUSES
    _, rows = parse_table_rows(index_text, SECTION_HEADERS[kind])
    return [row for row in rows if row["status"].lower() in allowed]


def recent_retention_blockers(index_text: str, kind: str, item_id: str, keep_recent: int) -> list[str]:
    if keep_recent <= 0:
        return []

    inactive = inactive_rows(index_text, kind)
    recent = inactive[-keep_recent:]
    if any(row["id"] == item_id for row in recent):
        return [
            f"{item_id} is within the most recent {keep_recent} inactive {kind}; keep recent completed work in active memory"
        ]
    return []


def active_dependents(index_text: str, item_id: str) -> list[str]:
    dependents: list[str] = []
    _, task_rows = parse_table_rows(index_text, SECTION_HEADERS["tasks"])
    for row in task_rows:
        status = row["status"].lower()
        if status in ACTIVE_STATUSES and item_id in {part.strip(" `") for part in row["depends_on"].split(",")}:
            dependents.append(row["id"])
    return dependents


def active_tasks_for_spec(index_text: str, spec_id: str) -> list[str]:
    tasks: list[str] = []
    _, task_rows = parse_table_rows(index_text, SECTION_HEADERS["tasks"])
    for row in task_rows:
        if row["status"].lower() in ACTIVE_STATUSES and row["fourth"] == spec_id:
            tasks.append(row["id"])
    return tasks


def remove_index_row(index_text: str, kind: str, item_id: str) -> str:
    section = SECTION_HEADERS[kind]
    pattern = rf"({re.escape(section)}\n\n)(.*?)(?=\n## |\Z)"
    match = re.search(pattern, index_text, re.S)
    if not match:
        return index_text
    lines = match.group(2).splitlines()
    kept = [line for line in lines if not line.startswith(f"| {item_id} |")]
    replacement = match.group(1) + "\n".join(kept).rstrip() + "\n"
    return index_text[: match.start()] + replacement + index_text[match.end() :]


def ensure_manifest(repo: Path) -> Path:
    manifest = repo / "archive" / "MANIFEST.md"
    if not manifest.exists():
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            "# Archive Manifest\n\n"
            "## Archived Specs\n\n"
            "| ID | File | Final Status | Archived Date | Reason |\n"
            "| --- | --- | --- | --- | --- |\n\n"
            "## Archived Tasks\n\n"
            "| ID | File | Final Status | Archived Date | Reason |\n"
            "| --- | --- | --- | --- | --- |\n"
        )
    return manifest


def append_manifest_row(manifest: Path, kind: str, row: dict[str, str], archived_file: str, reason: str) -> None:
    text = manifest.read_text()
    header = ARCHIVE_HEADERS[kind]
    archive_row = f"| {row['id']} | `{archived_file}` | {row['status']} | {dt.date.today().isoformat()} | {reason} |"
    pattern = rf"({re.escape(header)}\n\n\| ID \| File \| Final Status \| Archived Date \| Reason \|\n\| --- \| --- \| --- \| --- \| --- \|\n)(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.S)
    if not match:
        if not text.endswith("\n"):
            text += "\n"
        text += f"\n{header}\n\n| ID | File | Final Status | Archived Date | Reason |\n| --- | --- | --- | --- | --- |\n{archive_row}\n"
    else:
        body = match.group(2)
        lines = [line for line in body.splitlines() if line.strip() and not line.startswith(f"| {row['id']} |")]
        lines.append(archive_row)
        text = text[: match.start()] + match.group(1) + "\n".join(lines) + "\n" + text[match.end() :]
    manifest.write_text(text)


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    index_path = repo / "INDEX.md"
    if not index_path.exists():
        print("Error: INDEX.md is missing.", file=sys.stderr)
        return 1

    index_text = index_path.read_text()
    row = find_row(index_text, args.kind, args.item_id)
    if row is None:
        print(f"Error: {args.item_id} is not listed in INDEX.md {SECTION_HEADERS[args.kind]}.", file=sys.stderr)
        return 1

    status = row["status"].lower()
    allowed = ARCHIVABLE_TASK_STATUSES if args.kind == "tasks" else ARCHIVABLE_SPEC_STATUSES
    if status not in allowed and not args.force:
        print(f"Error: {args.item_id} status is {row['status']}; expected one of {', '.join(sorted(allowed))}.", file=sys.stderr)
        return 1

    blockers = active_dependents(index_text, args.item_id)
    if args.kind == "specs":
        blockers.extend(active_tasks_for_spec(index_text, args.item_id))
    keep_recent = DEFAULT_RECENT_KEEP[args.kind] if args.keep_recent is None else args.keep_recent
    blockers.extend(recent_retention_blockers(index_text, args.kind, args.item_id, keep_recent))
    if blockers and not args.force:
        print(f"Error: {args.item_id} cannot be archived yet: {', '.join(sorted(set(blockers)))}.", file=sys.stderr)
        return 1

    source = repo / row["file"]
    if not source.exists():
        print(f"Error: listed file does not exist: {row['file']}", file=sys.stderr)
        return 1

    archive_rel = Path("archive") / args.kind / source.name
    archive_path = repo / archive_rel
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if archive_path.exists():
        print(f"Error: archive target already exists: {archive_rel}", file=sys.stderr)
        return 1

    shutil.move(str(source), str(archive_path))
    index_path.write_text(remove_index_row(index_text, args.kind, args.item_id))
    manifest = ensure_manifest(repo)
    append_manifest_row(manifest, args.kind, row, archive_rel.as_posix(), args.reason)
    print(archive_rel.as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
