#!/usr/bin/env python3

from pathlib import Path
import argparse
import shutil
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a project-memory repo from project-system templates.")
    parser.add_argument("target", help="Target root path that will contain sibling project and repo directories")
    parser.add_argument("--repo-dir", default="repo", help="Name of the project-memory repository directory")
    parser.add_argument("--project-dir", default="project", help="Name of the implementation project directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    return parser.parse_args()


def copy_templates(src: Path, dst: Path, force: bool) -> None:
    for item in sorted(src.rglob("*")):
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            continue
        shutil.copy2(item, target)


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    templates = root / "assets" / "templates"
    root_target = Path(args.target).resolve()
    root_target.mkdir(parents=True, exist_ok=True)

    project_dir = root_target / args.project_dir
    repo_dir = root_target / args.repo_dir
    project_dir.mkdir(parents=True, exist_ok=True)
    repo_dir.mkdir(parents=True, exist_ok=True)

    copy_templates(templates, repo_dir, args.force)
    print(f"Initialized project root at {root_target}")
    print(f"- project directory: {project_dir}")
    print(f"- memory repo directory: {repo_dir}")
    if not args.force:
        print("Existing files were preserved. Use --force to overwrite template-managed files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
