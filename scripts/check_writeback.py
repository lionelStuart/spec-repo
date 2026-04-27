#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys


REQUIRED_STATUS_SECTIONS = [
    "## Current Focus",
    "## Last Completed",
    "## Open Issues",
    "## Next Steps",
]

REQUIRED_TASK_SECTIONS = [
    "## Status",
    "## Source",
    "## Goal",
    "## Progress",
    "## Result",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether project-memory write-back artifacts look complete.")
    parser.add_argument("repo", help="Target repository path")
    parser.add_argument("--task", help="Relative task file path, for example tasks/TASK-002-foo.md")
    return parser.parse_args()


def missing_sections(path: Path, sections: list[str]) -> list[str]:
    text = path.read_text()
    return [section for section in sections if section not in text]


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    failures: list[str] = []

    status = repo / "STATUS.md"
    index_file = repo / "INDEX.md"

    if not status.exists():
        failures.append("STATUS.md is missing")
    else:
        missing = missing_sections(status, REQUIRED_STATUS_SECTIONS)
        if missing:
            failures.append(f"STATUS.md missing sections: {', '.join(missing)}")

    if not index_file.exists():
        failures.append("INDEX.md is missing")
    else:
        if "## Tasks" not in index_file.read_text():
            failures.append("INDEX.md missing ## Tasks section")

    if args.task:
        task_file = repo / args.task
        if not task_file.exists():
            failures.append(f"task file not found: {args.task}")
        else:
            missing = missing_sections(task_file, REQUIRED_TASK_SECTIONS)
            if missing:
                failures.append(f"{args.task} missing sections: {', '.join(missing)}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: write-back artifacts look structurally complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
