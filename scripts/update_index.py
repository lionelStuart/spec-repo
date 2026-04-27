#!/usr/bin/env python3

from pathlib import Path
import argparse
import re
import sys


SECTION_HEADERS = {
    "specs": "## Specs",
    "tasks": "## Tasks",
}


TABLE_HEADERS = {
    "specs": "| ID | File | Status | Tags | Depends On |",
    "tasks": "| ID | File | Status | Spec | Depends On |",
}


DIVIDER = "| --- | --- | --- | --- | --- |"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add or refresh specs/tasks rows in INDEX.md.")
    parser.add_argument("repo", help="Target repository path")
    parser.add_argument("kind", choices=["specs", "tasks"], help="Index section to update")
    parser.add_argument("item_id", help="Item ID, for example SPEC-002 or TASK-003")
    parser.add_argument("file", help="Relative file path, for example specs/SPEC-002-foo.md")
    parser.add_argument("--status", default="draft", help="Status column value")
    parser.add_argument("--tags", default="-", help="Tags column for specs")
    parser.add_argument("--spec", default="-", help="Spec column for tasks")
    parser.add_argument("--depends-on", default="-", help="Depends On column value")
    return parser.parse_args()


def ensure_index(repo: Path) -> Path:
    index_path = repo / "INDEX.md"
    if not index_path.exists():
        index_path.write_text(
            "# Index\n\n"
            "## Specs\n\n"
            f"{TABLE_HEADERS['specs']}\n"
            f"{DIVIDER}\n\n"
            "## Tasks\n\n"
            f"{TABLE_HEADERS['tasks']}\n"
            f"{DIVIDER}\n"
        )
    return index_path


def build_row(args: argparse.Namespace) -> str:
    if args.kind == "specs":
        return f"| {args.item_id} | `{args.file}` | {args.status} | {args.tags} | {args.depends_on} |"
    return f"| {args.item_id} | `{args.file}` | {args.status} | {args.spec} | {args.depends_on} |"


def replace_or_insert_section(text: str, kind: str, row: str, item_id: str) -> str:
    header = SECTION_HEADERS[kind]
    table_header = TABLE_HEADERS[kind]
    pattern = rf"({re.escape(header)}\n\n{re.escape(table_header)}\n{re.escape(DIVIDER)}\n)(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.S)
    if not match:
        block = f"{header}\n\n{table_header}\n{DIVIDER}\n{row}\n"
        if not text.endswith("\n"):
            text += "\n"
        return text + "\n" + block

    body = match.group(2)
    lines = [line for line in body.splitlines() if line.strip()]
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith(f"| {item_id} |"):
            new_lines.append(row)
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(row)

    replacement = match.group(1) + "\n".join(new_lines) + "\n"
    start, end = match.span()
    return text[:start] + replacement + text[end:]


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    index_path = ensure_index(repo)
    text = index_path.read_text()
    row = build_row(args)
    updated = replace_or_insert_section(text, args.kind, row, args.item_id)
    index_path.write_text(updated)
    print(index_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
