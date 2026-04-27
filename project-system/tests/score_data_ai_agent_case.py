#!/usr/bin/env python3

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "cases" / "data-ai-agent" / "repo-fixture"


def read(relpath: str) -> str:
    return (FIXTURE / relpath).read_text()


def exists(relpath: str) -> bool:
    return (FIXTURE / relpath).exists()


def check(relpath: str, phrases: list[str]) -> bool:
    text = read(relpath)
    return all(phrase in text for phrase in phrases)


def score_structure() -> tuple[int, str]:
    required = [
        "AGENTS.md",
        "PROJECT.md",
        "INDEX.md",
        "STATUS.md",
        "ROADMAP.md",
        "ARCHITECTURE.md",
        "specs/SPEC-001-dataset-ingestion.md",
        "tasks/TASK-001-bootstrap-ingestion.md",
        "tasks/TASK-002-schema-normalization.md",
        "decisions/ADR-001-metadata-first.md",
        "learnings/LEARN-001-date-column-normalization.md",
        "skills/SKILL-001-tabular-schema-checklist.md",
    ]
    missing = [path for path in required if not exists(path)]
    if missing:
        return 0, f"missing files: {', '.join(missing)}"
    return 15, "all required repo-memory files exist"


def score_loading_protocol() -> tuple[int, str]:
    if check(
        "AGENTS.md",
        ["Mandatory Read Order", "`PROJECT.md`", "`STATUS.md`", "`INDEX.md`", "Do not read the whole repository by default."],
    ):
        return 20, "progressive loading protocol is explicit"
    return 0, "loading protocol is incomplete"


def score_spec_task_discipline() -> tuple[int, str]:
    spec_ok = check(
        "specs/SPEC-001-dataset-ingestion.md",
        ["## Goal", "## Non-Goals", "## Acceptance", "## Related Context"],
    )
    task_ok = check(
        "tasks/TASK-002-schema-normalization.md",
        ["## Source", "## Required Context", "## Modify Scope", "## Acceptance", "## Progress"],
    )
    if spec_ok and task_ok:
        return 15, "spec and task are separated cleanly"
    return 0, "spec-task separation is weak"


def score_write_back() -> tuple[int, str]:
    status_ok = check(
        "STATUS.md",
        ["## Current Focus", "## Last Completed", "## Open Issues", "## Next Steps"],
    )
    index_ok = "doing" in read("INDEX.md") and "done" in read("INDEX.md")
    task_ok = "[x] Planned" in read("tasks/TASK-001-bootstrap-ingestion.md")
    if status_ok and index_ok and task_ok:
        return 20, "status, index, and task progress capture write-back state"
    return 0, "write-back signals are incomplete"


def score_self_bootstrap() -> tuple[int, str]:
    learning_ok = check(
        "learnings/LEARN-001-date-column-normalization.md",
        ["## Cause", "## Fix", "## Reuse Value"],
    )
    skill_ok = check(
        "skills/SKILL-001-tabular-schema-checklist.md",
        ["## Checklist", "## Common Failure Modes", "## Verification"],
    )
    if learning_ok and skill_ok:
        return 15, "learning-to-skill loop is demonstrated"
    return 0, "self-bootstrapping loop is missing"


def score_domain_fidelity() -> tuple[int, str]:
    project = read("PROJECT.md")
    architecture = read("ARCHITECTURE.md")
    spec = read("specs/SPEC-001-dataset-ingestion.md")
    phrases = [
        "tabular",
        "schema",
        "natural-language",
        "chart",
        "execution trace",
    ]
    joined = "\n".join([project, architecture, spec]).lower()
    if all(phrase in joined for phrase in phrases):
        return 15, "fixture is specific to a data AI agent workflow"
    return 0, "fixture stays too generic for the target domain"


def main() -> int:
    dimensions = [
        ("structure_completeness", score_structure),
        ("progressive_loading", score_loading_protocol),
        ("spec_task_discipline", score_spec_task_discipline),
        ("write_back_quality", score_write_back),
        ("self_bootstrapping", score_self_bootstrap),
        ("domain_fidelity", score_domain_fidelity),
    ]

    total = 0
    print("Data AI Agent Demo Scorecard")
    print("=" * 30)
    for name, fn in dimensions:
        score, reason = fn()
        total += score
        print(f"{name}: {score}/{'20' if 'loading' in name or 'write_back' in name else '15'}")
        print(f"  {reason}")

    print("-" * 30)
    print(f"total: {total}/100")
    return 0 if total == 100 else 1


if __name__ == "__main__":
    sys.exit(main())
