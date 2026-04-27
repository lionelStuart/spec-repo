#!/usr/bin/env python3

from pathlib import Path
import sys


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_agent_run_artifacts.py <repo-fixture-path>")
        return 1

    root = Path(sys.argv[1]).resolve()
    required = [
        root / "AGENTS.md",
        root / "PROJECT.md",
        root / "INDEX.md",
        root / "STATUS.md",
        root / "specs",
        root / "tasks",
        root / "decisions",
        root / "learnings",
        root / "skills",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        return fail(f"missing required repo artifacts: {', '.join(missing)}")

    status = (root / "STATUS.md").read_text()
    index_text = (root / "INDEX.md").read_text()
    task_files = list((root / "tasks").glob("*.md"))
    learning_files = list((root / "learnings").glob("*.md"))
    skill_files = list((root / "skills").glob("*.md"))

    if "## Current Focus" not in status or "## Next Steps" not in status:
        return fail("STATUS.md is missing current focus or next steps")

    if "## Tasks" not in index_text:
        return fail("INDEX.md is missing task index")

    if not task_files:
        return fail("no task files found")

    completed_or_active = False
    for task_file in task_files:
        text = task_file.read_text()
        if "## Progress" in text and ("[x]" in text or "doing" in text or "done" in text):
            completed_or_active = True
            break
    if not completed_or_active:
        return fail("task files do not show active or completed progress")

    if not learning_files:
        return fail("no learnings captured")

    if not skill_files:
        return fail("no reusable skills captured")

    print("PASS: agent-run artifact set is structurally complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
