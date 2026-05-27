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
        repo / "skills" / "project-system-meta/SKILL.md",
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
        "## Protected Meta Skill Link" not in agents_text
        or "Required meta skill: `repo/skills/project-system-meta/SKILL.md`" not in agents_text
        or "Discoverable skill directory: `repo/skills/project-system-meta/`" not in agents_text
        or "OpenAI/Codex-style meta skill directory" not in agents_text
        or "operating skill for this project" not in agents_text
        or "Never leave root `AGENTS.md` without a required meta skill link." not in agents_text
    ):
        return fail("AGENTS.md does not protect the project-system meta skill link")

    if "skills/project-system-meta/SKILL.md" not in index_text:
        return fail("INDEX.md does not register the project-system meta skill")

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
