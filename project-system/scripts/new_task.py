#!/usr/bin/env python3

from pathlib import Path
import argparse
import re
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a task file from the project-system task template.")
    parser.add_argument("repo", help="Target repository path")
    parser.add_argument("task_id", help="Task ID, for example TASK-003")
    parser.add_argument("title", help="Task title")
    parser.add_argument("--spec", default="SPEC-001", help="Linked spec ID")
    parser.add_argument("--status", default="draft", help="Initial task status")
    parser.add_argument("--depends-on", default="-", help="Depends On value for INDEX.md")
    parser.add_argument("--skip-index", action="store_true", help="Do not update INDEX.md automatically")
    return parser.parse_args()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "task"


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    repo_template = repo / "tasks" / "TASK-001-template.md"
    skill_template = Path(__file__).resolve().parents[1] / "assets" / "templates" / "tasks" / "TASK-001-template.md"
    template = repo_template if repo_template.exists() else skill_template
    if not template.exists():
        print("Task template not found.")
        return 1

    content = template.read_text()
    content = content.replace("TASK-001", args.task_id)
    content = content.replace("[Task Name]", args.title)
    content = content.replace("\ndraft\n", f"\n{args.status}\n", 1)
    content = content.replace("`SPEC-001`", f"`{args.spec}`", 1)
    content = content.replace("specs/SPEC-001-template.md", f"specs/{args.spec}.md")

    filename = f"{args.task_id}-{slugify(args.title)}.md"
    destination = repo / "tasks" / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content)

    if not args.skip_index:
        update_index = Path(__file__).resolve().parent / "update_index.py"
        relpath = destination.relative_to(repo).as_posix()
        result = subprocess.run(
            [
                sys.executable,
                str(update_index),
                str(repo),
                "tasks",
                args.task_id,
                relpath,
                "--status",
                args.status,
                "--spec",
                args.spec,
                "--depends-on",
                args.depends_on,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stderr or result.stdout)
            return result.returncode

    print(destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
