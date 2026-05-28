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
    ROOT / "scripts" / "project_doctor.py",
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


def has_project_system_governance(text: str) -> bool:
    return (
        "## Project-System Governance" in text
        and "Do not remove this section" in text
        and "external `project-system` skill" in text
        and "file contracts, task execution, write-back, archive control, and completion checks" in text
        and "Never leave root `AGENTS.md` without a project-system governance section." in text
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
        if not has_project_system_governance(root_agents):
            return "AGENTS.md does not protect project-system governance"
        if "project-system-meta" in target_index:
            return "INDEX.md still registers removed project-system-meta skill"
        if "tasks/TASK-001-template.md" in target_index or "specs/SPEC-001-template.md" in target_index:
            return "INDEX.md lists template files as active work"

        doctor = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "project_doctor.py"), str(target)],
            capture_output=True,
            text=True,
        )
        if doctor.returncode != 0:
            return f"project_doctor.py failed on initialized project: {doctor.stderr or doctor.stdout}"

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
        if archive.returncode == 0:
            return "archive_item.py archived a recently completed task without --force"
        if "most recent" not in (archive.stderr or archive.stdout):
            return f"archive_item.py did not explain recent-retention block: {archive.stderr or archive.stdout}"

        archive = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "archive_item.py"),
                str(target / "repo"),
                "tasks",
                "TASK-002",
                "--reason",
                "validation test",
                "--force",
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


def validate_web_minesweeper_case() -> str | None:
    case_root = ROOT / "tests" / "cases" / "web-minesweeper"
    if not case_root.exists():
        return "web-minesweeper case is missing"

    doctor = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "project_doctor.py"), str(case_root)],
        capture_output=True,
        text=True,
    )
    if doctor.returncode != 0:
        return f"project_doctor.py failed on web-minesweeper case: {doctor.stderr or doctor.stdout}"

    required = [
        case_root / "index.html",
        case_root / "styles.css",
        case_root / "script.js",
        case_root / "repo" / "tasks" / "TASK-001-build-web-minesweeper.md",
        case_root / "repo" / "specs" / "SPEC-001-web-minesweeper.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        return f"web-minesweeper case missing files: {', '.join(missing)}"

    html = (case_root / "index.html").read_text()
    css = (case_root / "styles.css").read_text()
    js = (case_root / "script.js").read_text()
    checks = {
        "HTML loads styles.css": 'href="styles.css"' in html,
        "HTML loads script.js": 'src="script.js"' in html,
        "HTML has board element": 'id="board"' in html,
        "game uses 9x9 board": "const size = 9;" in js,
        "game uses 10 mines": "const mineTotal = 10;" in js,
        "first click blocks neighbors": "const blocked = new Set([safeId, ...neighbors" in js,
        "CSS renders 9 columns": "repeat(9, 1fr)" in css,
        "keyboard flag support": 'event.key.toLowerCase() === "f"' in js,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        return f"web-minesweeper static checks failed: {', '.join(failed)}"

    script_check = subprocess.run(
        ["node", "--check", str(case_root / "script.js")],
        capture_output=True,
        text=True,
    )
    if script_check.returncode != 0:
        return f"web-minesweeper script syntax check failed: {script_check.stderr or script_check.stdout}"

    archive = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "archive_item.py"),
            str(case_root / "repo"),
            "tasks",
            "TASK-001",
            "--reason",
            "recent retention validation",
        ],
        capture_output=True,
        text=True,
    )
    if archive.returncode == 0:
        return "web-minesweeper recent task archived before retention window elapsed"
    if "most recent" not in (archive.stderr or archive.stdout):
        return f"web-minesweeper archive retention block was unclear: {archive.stderr or archive.stdout}"

    return None


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        return fail(f"missing required files: {', '.join(missing)}")

    skill_md = (ROOT / "SKILL.md").read_text()
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill_md:
            return fail(f"SKILL.md missing phrase: {phrase}")

    template_checks = {
        "assets/templates/AGENTS.md": [
            "## Project-System Governance",
            "Do not remove this section",
            "external `project-system` skill",
            "file contracts, task execution, write-back, archive control, and completion checks",
            "Start A Coding Round",
            "## Project Skills Routing",
            "Read a project skill when the active task, spec, ADR, or learning references it.",
            "description` frontmatter",
            "OpenAI/Codex-style directories with `SKILL.md` frontmatter",
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
            "## Done Means",
            "## Validation",
        ],
        "SKILL.md": [
            "## Project-System Tooling",
            "scripts/project_doctor.py",
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
            "Do not archive an item immediately just because it is done.",
            "Keep the most recent 5 inactive tasks and 3 inactive specs",
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

    web_case_failure = validate_web_minesweeper_case()
    if web_case_failure:
        return fail(web_case_failure)

    print("PASS: project-system structure and references look consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
