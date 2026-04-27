#!/usr/bin/env python3

from pathlib import Path
import argparse
import shutil
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a project-memory repo from project-system templates.")
    parser.add_argument("target", help="Target repository path")
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
    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    copy_templates(templates, target, args.force)
    print(f"Initialized project-memory repo at {target}")
    if not args.force:
        print("Existing files were preserved. Use --force to overwrite template-managed files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
