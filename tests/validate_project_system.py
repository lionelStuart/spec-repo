#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import tempfile


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
    ROOT / "assets" / "templates" / "archive" / "MANIFEST.md",
    ROOT / "assets" / "templates" / "_templates" / "SPEC-template.md",
    ROOT / "assets" / "templates" / "_templates" / "TASK-template.md",
    ROOT / "assets" / "templates" / "_templates" / "ADR-template.md",
    ROOT / "assets" / "templates" / "_templates" / "LEARNING-template.md",
    ROOT / "assets" / "templates" / "_templates" / "SKILL-template.md",
    ROOT / "assets" / "templates" / "skills" / "project-system-meta/SKILL.md",
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


def has_skill_frontmatter(path: Path, expected_name: str) -> bool:
    text = path.read_text()
    return (
        text.startswith("---\n")
        and f"name: {expected_name}" in text
        and "description:" in text
        and "\n---\n" in text[4:]
    )


def has_protected_meta_skill_link(text: str) -> bool:
    return (
        "## Protected Meta Skill Link" in text
        and "Do not remove this section" in text
        and "Required meta skill: `repo/skills/project-system-meta/SKILL.md`" in text
        and "Discoverable skill directory: `repo/skills/project-system-meta/`" in text
        and "OpenAI/Codex-style meta skill directory" in text
        and "operating skill for this project" in text
        and "Never leave root `AGENTS.md` without a required meta skill link." in text
    )


def validate_init_project_layout() -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "target"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "init_project.py"), str(target)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return f"init_project.py failed: {result.stderr or result.stdout}"

        expected = [
            target / "AGENTS.md",
            target / "repo" / "PROJECT.md",
            target / "repo" / "INDEX.md",
            target / "repo" / "STATUS.md",
            target / "repo" / "archive",
            target / "repo" / "archive" / "MANIFEST.md",
            target / "repo" / "archive" / "tasks",
            target / "repo" / "archive" / "specs",
            target / "repo" / "_templates",
            target / "repo" / "_templates" / "TASK-template.md",
            target / "repo" / "_templates" / "SPEC-template.md",
            target / "repo" / "specs",
            target / "repo" / "tasks",
            target / "repo" / "decisions",
            target / "repo" / "learnings",
            target / "repo" / "skills",
            target / "repo" / "skills" / "project-system-meta/SKILL.md",
        ]
        missing = [str(path.relative_to(target)) for path in expected if not path.exists()]
        if missing:
            return f"init_project.py missing expected output: {', '.join(missing)}"
        if (target / "repo" / "AGENTS.md").exists():
            return "init_project.py placed AGENTS.md inside repo/"
        if (target / "project").exists():
            return "init_project.py created deprecated project/ directory"
        root_agents = (target / "AGENTS.md").read_text()
        target_index = (target / "repo" / "INDEX.md").read_text()
        if not has_protected_meta_skill_link(root_agents):
            return "AGENTS.md does not protect the project-system meta skill link"
        if "skills/project-system-meta/SKILL.md" not in target_index:
            return "INDEX.md does not register project-system-meta/SKILL.md"
        if not has_skill_frontmatter(target / "repo" / "skills" / "project-system-meta" / "SKILL.md", "project-system-meta"):
            return "project-system-meta/SKILL.md is missing OpenAI skill frontmatter"
        if "tasks/TASK-001-template.md" in target_index or "specs/SPEC-001-template.md" in target_index:
            return "INDEX.md lists template files as active work"

        new_task = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "new_task.py"),
                str(target / "repo"),
                "TASK-002",
                "Schema Work",
                "--spec",
                "SPEC-001",
            ],
            capture_output=True,
            text=True,
        )
        if new_task.returncode != 0:
            return f"new_task.py failed: {new_task.stderr or new_task.stdout}"
        task_text = (target / "repo" / "tasks" / "TASK-002-schema-work.md").read_text()
        if "`repo/specs/SPEC-001.md`" not in task_text:
            return "new_task.py did not generate the default SPEC-001 path"
        if "repo/repo/" in task_text:
            return "new_task.py generated a duplicated repo/repo path"

        task_path = target / "repo" / "tasks" / "TASK-002-schema-work.md"
        task_path.write_text(task_text.replace("\ndraft\n", "\ndone\n", 1))
        update_done = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "update_index.py"),
                str(target / "repo"),
                "tasks",
                "TASK-002",
                "tasks/TASK-002-schema-work.md",
                "--status",
                "done",
                "--spec",
                "SPEC-001",
            ],
            capture_output=True,
            text=True,
        )
        if update_done.returncode != 0:
            return f"update_index.py failed while preparing archive test: {update_done.stderr or update_done.stdout}"
        archive = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "archive_item.py"),
                str(target / "repo"),
                "tasks",
                "TASK-002",
                "--reason",
                "validation test",
            ],
            capture_output=True,
            text=True,
        )
        if archive.returncode != 0:
            return f"archive_item.py failed: {archive.stderr or archive.stdout}"
        if not (target / "repo" / "archive" / "tasks" / "TASK-002-schema-work.md").exists():
            return "archive_item.py did not move the task into archive/tasks"
        archived_index = (target / "repo" / "INDEX.md").read_text()
        archived_manifest = (target / "repo" / "archive" / "MANIFEST.md").read_text()
        if "| TASK-002 |" in archived_index:
            return "archive_item.py did not remove archived task from active INDEX.md"
        if "TASK-002" not in archived_manifest:
            return "archive_item.py did not record archived task in archive/MANIFEST.md"

        bad = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "init_project.py"), str(target), "--repo-dir", "../outside"],
            capture_output=True,
            text=True,
        )
        if bad.returncode == 0:
            return "init_project.py accepted a repo directory outside the target root"

    return None


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        return fail(f"missing required files: {', '.join(missing)}")

    if not has_skill_frontmatter(ROOT / "assets" / "templates" / "skills" / "project-system-meta" / "SKILL.md", "project-system-meta"):
        return fail("project-system-meta/SKILL.md is missing OpenAI skill frontmatter")

    skill_md = (ROOT / "SKILL.md").read_text()
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill_md:
            return fail(f"SKILL.md missing phrase: {phrase}")

    template_checks = {
        "assets/templates/AGENTS.md": [
            "## Protected Meta Skill Link",
            "Do not remove this section",
            "Required meta skill: `repo/skills/project-system-meta/SKILL.md`",
            "Discoverable skill directory: `repo/skills/project-system-meta/`",
            "OpenAI/Codex-style meta skill directory",
            "operating skill for this project",
            "repo/skills/project-system-meta/SKILL.md",
            "File Contracts",
            "Start A Coding Round",
            "Completion Gate",
            "Do not claim the project or a milestone is complete",
        ],
        "assets/templates/PROJECT.md": [
            "## Repository Layout",
            "## Coding Standards",
            "## Project Done Means",
        ],
        "assets/templates/STATUS.md": [
            "## Completion State",
            "## Last Validation",
        ],
        "assets/templates/ROADMAP.md": [
            "## Current Milestone",
            "## Project Completion Signals",
        ],
        "assets/templates/_templates/TASK-template.md": [
            "repo/skills/project-system-meta/SKILL.md",
            "## Done Means",
            "## Validation",
        ],
        "assets/templates/skills/project-system-meta/SKILL.md": [
            "## Required Loop",
            "## Project-System Tooling",
            "## File Contracts",
            "### `repo/PROJECT.md`",
            "### `repo/STATUS.md`",
            "### `repo/INDEX.md`",
            "### `repo/ROADMAP.md`",
            "### `repo/ARCHITECTURE.md`",
            "### `repo/specs/`",
            "### `repo/tasks/`",
            "### `repo/decisions/`",
            "### `repo/learnings/`",
            "### `repo/skills/`",
            "### `repo/_templates/`",
            "### `repo/archive/`",
            "## Memory Update Triggers",
            "## Archive Control",
            "## Completion Checks",
        ],
        "assets/templates/archive/MANIFEST.md": [
            "## Archived Specs",
            "## Archived Tasks",
            "## Archive Rules",
        ],
    }
    for relpath, phrases in template_checks.items():
        text = (ROOT / relpath).read_text()
        for phrase in phrases:
            if phrase not in text:
                return fail(f"{relpath} missing phrase: {phrase}")

    templates = {
        "spec": "_templates/SPEC-template.md",
        "task": "_templates/TASK-template.md",
        "decision": "_templates/ADR-template.md",
        "learning": "_templates/LEARNING-template.md",
        "meta skill": "skills/project-system-meta/SKILL.md",
        "skill": "_templates/SKILL-template.md",
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

    init_failure = validate_init_project_layout()
    if init_failure:
        return fail(init_failure)

    print("PASS: project-system structure and references look consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
