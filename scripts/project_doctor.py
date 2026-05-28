#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys


REQUIRED_REPO_FILES = [
    "PROJECT.md",
    "INDEX.md",
    "STATUS.md",
    "ROADMAP.md",
    "ARCHITECTURE.md",
    "archive/MANIFEST.md",
    "_templates/SPEC-template.md",
    "_templates/TASK-template.md",
    "_templates/ADR-template.md",
    "_templates/LEARNING-template.md",
    "_templates/SKILL-template.md",
]

REQUIRED_REPO_DIRS = [
    "specs",
    "tasks",
    "decisions",
    "learnings",
    "skills",
    "archive",
    "archive/tasks",
    "archive/specs",
    "_templates",
]

REQUIRED_AGENTS_PHRASES = [
    "## Project-System Governance",
    "external `project-system` skill",
    "## Project Skills Routing",
    "repo/skills/",
    "Never leave root `AGENTS.md` without a project-system governance section.",
]

DEFAULT_RECENT_KEEP = {
    "tasks": 5,
    "specs": 3,
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose a project-system repo without modifying files.")
    parser.add_argument("target", help="Project root containing AGENTS.md and repo/, or the repo directory itself")
    parser.add_argument("--repo-dir", default="repo", help="Project-memory directory name when target is a project root")
    return parser.parse_args()


def resolve_paths(target: Path, repo_dir: str) -> tuple[Path, Path]:
    target = target.resolve()
    if (target / "PROJECT.md").exists() and (target / "INDEX.md").exists():
        return target.parent, target
    return target, target / repo_dir


def read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def parse_index_rows(index_text: str) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for line in index_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        item_id, file_path, status = cells[:3]
        if item_id in {"ID", "---"} or file_path in {"File", "---"}:
            continue
        rows.append((item_id, file_path, status, line))
    return rows


def has_skill_frontmatter(path: Path) -> bool:
    text = read_text(path)
    return text.startswith("---\n") and "\n---\n" in text[4:] and "name:" in text and "description:" in text


def main() -> int:
    args = parse_args()
    root, repo = resolve_paths(Path(args.target), args.repo_dir)
    failures: list[str] = []
    warnings: list[str] = []

    agents = root / "AGENTS.md"
    if not agents.exists():
        failures.append(f"missing root AGENTS.md at {agents}")
    else:
        agents_text = read_text(agents)
        for phrase in REQUIRED_AGENTS_PHRASES:
            if phrase not in agents_text:
                failures.append(f"AGENTS.md missing required phrase: {phrase}")
        if "project-system-meta" in agents_text:
            failures.append("AGENTS.md still references removed project-system-meta")

    if not repo.exists():
        failures.append(f"missing repo directory at {repo}")
    else:
        for relpath in REQUIRED_REPO_DIRS:
            if not (repo / relpath).is_dir():
                failures.append(f"missing repo directory: {relpath}")
        for relpath in REQUIRED_REPO_FILES:
            if not (repo / relpath).is_file():
                failures.append(f"missing repo file: {relpath}")

        index_text = read_text(repo / "INDEX.md")
        if "project-system-meta" in index_text:
            failures.append("INDEX.md still references removed project-system-meta")
        if "## Archive" not in index_text:
            failures.append("INDEX.md missing archive entrypoint section")
        if "archive/MANIFEST.md" not in index_text:
            failures.append("INDEX.md does not point to archive/MANIFEST.md")

        index_rows = parse_index_rows(index_text)
        referenced_ids = {
            item_id
            for item_id, _file_path, _status, _line in index_rows
            for other_id, _other_file, _other_status, other_line in index_rows
            if item_id != other_id and item_id in other_line
        }
        inactive_seen = {
            "tasks": [row for row in index_rows if row[1].startswith("tasks/") and row[2] in {"done", "canceled"}],
            "specs": [row for row in index_rows if row[1].startswith("specs/") and row[2] in {"done", "superseded", "deprecated"}],
        }
        recent_ids = {
            kind: {row[0] for row in rows[-DEFAULT_RECENT_KEEP[kind] :]}
            for kind, rows in inactive_seen.items()
        }

        for item_id, file_path, status, _line in index_rows:
            if file_path.startswith("archive/"):
                warnings.append(f"{item_id} is archived but still listed in active INDEX.md")
            kind = "tasks" if file_path.startswith("tasks/") else "specs" if file_path.startswith("specs/") else ""
            if (
                status in {"done", "canceled", "superseded", "deprecated"}
                and file_path.startswith(("tasks/", "specs/"))
                and item_id not in referenced_ids
                and item_id not in recent_ids.get(kind, set())
            ):
                warnings.append(f"{item_id} is inactive, outside recent retention, and still listed in active INDEX.md")

        for skill_file in sorted((repo / "skills").glob("*/SKILL.md")):
            if not has_skill_frontmatter(skill_file):
                warnings.append(f"project skill missing OpenAI skill frontmatter: {skill_file.relative_to(repo)}")

        status_text = read_text(repo / "STATUS.md")
        if "## Current Focus" not in status_text or "## Completion State" not in status_text:
            failures.append("STATUS.md missing current focus or completion state")

    for failure in failures:
        print(f"FAIL: {failure}")
    for warning in warnings:
        print(f"WARN: {warning}")

    if failures:
        return 1

    print("PASS: project-system doctor checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
