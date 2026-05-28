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
    repo = root / "repo" if (root / "repo").exists() else root
    required = [
        root / "AGENTS.md",
        repo / "PROJECT.md",
        repo / "INDEX.md",
        repo / "STATUS.md",
        repo / "_templates",
        repo / "archive",
        repo / "archive" / "MANIFEST.md",
        repo / "specs",
        repo / "tasks",
        repo / "decisions",
        repo / "learnings",
        repo / "skills",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        return fail(f"missing required repo artifacts: {', '.join(missing)}")

    status = (repo / "STATUS.md").read_text()
    index_text = (repo / "INDEX.md").read_text()
    agents_text = (root / "AGENTS.md").read_text()
    task_files = list((repo / "tasks").glob("*.md"))
    learning_files = list((repo / "learnings").glob("*.md"))
    skill_files = list((repo / "skills").glob("*.md")) + list((repo / "skills").glob("*/SKILL.md"))

    if "## Current Focus" not in status or "## Next Steps" not in status:
        return fail("STATUS.md is missing current focus or next steps")

    if "## Tasks" not in index_text:
        return fail("INDEX.md is missing task index")

    if (
        "## Project-System Governance" not in agents_text
        or "external `project-system` skill" not in agents_text
        or "file contracts, task execution, write-back, archive control, and completion checks" not in agents_text
        or "## Project Skills Routing" not in agents_text
        or "Read a project skill when the active task, spec, ADR, or learning references it." not in agents_text
        or "OpenAI/Codex-style directories with `SKILL.md` frontmatter" not in agents_text
        or "Never leave root `AGENTS.md` without a project-system governance section." not in agents_text
    ):
        return fail("AGENTS.md does not protect project-system governance")

    if "project-system-meta" in index_text:
        return fail("INDEX.md still registers removed project-system-meta skill")

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
