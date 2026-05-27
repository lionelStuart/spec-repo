#!/usr/bin/env python3

from pathlib import Path, PurePath
import argparse
import shutil
import sys


REPO_DIRECTORIES = [
    "specs",
    "tasks",
    "decisions",
    "learnings",
    "skills",
    "archive/tasks",
    "archive/specs",
    "_templates",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a project-memory repo from project-system templates.")
    parser.add_argument("target", help="Target project root path that will contain AGENTS.md and the repo directory")
    parser.add_argument("--repo-dir", default="repo", help="Name of the project-memory repository directory")
    parser.add_argument("--project-dir", help=argparse.SUPPRESS)
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    return parser.parse_args()


def copy_repo_templates(src: Path, dst: Path, force: bool) -> None:
    for item in sorted(src.rglob("*")):
        rel = item.relative_to(src)
        if rel == Path("AGENTS.md"):
            continue
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            continue
        shutil.copy2(item, target)


def copy_root_file(src: Path, dst: Path, force: bool) -> None:
    if dst.exists() and not force:
        return
    shutil.copy2(src, dst)


def validate_dir_name(value: str, label: str) -> str | None:
    name = value.strip()
    path = PurePath(name)

    if not name or path.is_absolute() or len(path.parts) != 1 or name in {".", ".."}:
        print(f"Error: {label} must be a single directory name inside the target root.", file=sys.stderr)
        return None
    return name


def main() -> int:
    args = parse_args()
    repo_name = validate_dir_name(args.repo_dir, "--repo-dir")
    if repo_name is None:
        return 2
    if args.project_dir:
        print("Warning: --project-dir is deprecated and ignored; project files live in the target root.", file=sys.stderr)

    root = Path(__file__).resolve().parents[1]
    templates = root / "assets" / "templates"
    root_target = Path(args.target).resolve()
    root_target.mkdir(parents=True, exist_ok=True)

    repo_dir = root_target / repo_name
    repo_dir.mkdir(parents=True, exist_ok=True)
    for relpath in REPO_DIRECTORIES:
        (repo_dir / relpath).mkdir(parents=True, exist_ok=True)

    copy_root_file(templates / "AGENTS.md", root_target / "AGENTS.md", args.force)
    copy_repo_templates(templates, repo_dir, args.force)
    print(f"Initialized project root at {root_target}")
    print(f"- agent protocol: {root_target / 'AGENTS.md'}")
    print(f"- memory repo directory: {repo_dir}")
    if not args.force:
        print("Existing files were preserved. Use --force to overwrite template-managed files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
