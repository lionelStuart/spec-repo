#!/usr/bin/env python3

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    ROOT / "SKILL.md",
    ROOT / "agents" / "openai.yaml",
    ROOT / "assets" / "templates" / "AGENTS.md",
    ROOT / "assets" / "templates" / "PROJECT.md",
    ROOT / "assets" / "templates" / "INDEX.md",
    ROOT / "assets" / "templates" / "STATUS.md",
    ROOT / "assets" / "templates" / "ROADMAP.md",
    ROOT / "assets" / "templates" / "ARCHITECTURE.md",
    ROOT / "assets" / "templates" / "specs" / "SPEC-001-template.md",
    ROOT / "assets" / "templates" / "tasks" / "TASK-001-template.md",
    ROOT / "assets" / "templates" / "decisions" / "ADR-template.md",
    ROOT / "assets" / "templates" / "learnings" / "LEARNING-template.md",
    ROOT / "assets" / "templates" / "skills" / "SKILL-template.md",
]


REQUIRED_SKILL_PHRASES = [
    "Read in this order:",
    "Write Back State",
    "Do not finish a task without writing back state.",
    "Start implementation without an active task when the work spans more than a trivial edit.",
]


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        return fail(f"missing required files: {', '.join(missing)}")

    skill_md = (ROOT / "SKILL.md").read_text()
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill_md:
            return fail(f"SKILL.md missing phrase: {phrase}")

    templates = {
        "spec": "specs/SPEC-001-template.md",
        "task": "tasks/TASK-001-template.md",
        "decision": "decisions/ADR-template.md",
        "learning": "learnings/LEARNING-template.md",
        "skill": "skills/SKILL-template.md",
    }
    for label, relpath in templates.items():
        if relpath not in skill_md:
            return fail(f"SKILL.md does not reference {label} template: {relpath}")

    openai_yaml = (ROOT / "agents" / "openai.yaml").read_text()
    for phrase in [
        'display_name: "Project System"',
        'short_description: "Bootstrap and run AI-native project memory repos"',
    ]:
        if phrase not in openai_yaml:
            return fail(f"openai.yaml missing phrase: {phrase}")

    print("PASS: project-system structure and references look consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
