---
name: project-system-meta
description: Use inside a project-system managed repository to operate repo/ as a closed-loop project memory system. Read this before coding rounds, task execution, write-back, handoff, archive decisions, or project and milestone completion checks.
---

# PROJECT-SYSTEM-META: Operate Project Memory

## Applies To

- every coding round that uses this project-system repository
- every bootstrap, task execution, write-back, handoff, and completion check

## Purpose

Use this meta skill to operate `repo/` as a closed-loop project memory system. It tells the agent how to turn `AGENTS.md`, `PROJECT.md`, `STATUS.md`, `INDEX.md`, `ROADMAP.md`, specs, tasks, decisions, learnings, and skills into an execution loop instead of passive documentation.

## Required Loop

1. Start from root `AGENTS.md`.
2. Read this file before choosing implementation files.
3. Use `repo/STATUS.md` to identify the current focus and completion state.
4. Use `repo/INDEX.md` to locate the active task, linked spec, and referenced context.
5. Read only the task-required context before editing code.
6. Execute the task within its `Modify Scope` and `Forbidden` constraints.
7. Run or record the task's `Test Plan`.
8. Write back task progress, validation, result, status, and index state.
9. Apply memory update triggers for roadmap, architecture, decisions, learnings, and skills.
10. Stop only when the task or project completion gate is represented in files.

## Project-System Tooling

This repository was initialized by `project-system`.

When the project-system scripts are available, prefer them over handwritten repetitive edits:

- `scripts/new_task.py` for creating tasks from `repo/_templates/TASK-template.md`
- `scripts/update_index.py` for registering or updating active specs/tasks
- `scripts/check_writeback.py` before ending a coding round
- `scripts/archive_item.py` for moving inactive specs/tasks into `repo/archive/`

If the scripts are not available inside the target project, follow the same file contracts manually. Keep generated specs and tasks in `repo/specs/` and `repo/tasks/`; keep reusable templates in `repo/_templates/`.

## File Contracts

Use each `repo/` file and directory according to this contract:

### `repo/PROJECT.md`

- Read at the start of a coding round to understand goals, non-goals, global constraints, default commands, repository layout, coding standards, and project done means.
- Update only when durable project facts change.
- Do not store task progress, transient blockers, or chat summaries here.

### `repo/STATUS.md`

- Read at the start of every coding round to find current focus, completion state, blockers, validation, and next steps.
- Update at the end of every coding round.
- Keep it short and current; do not turn it into a changelog or long narrative.

### `repo/INDEX.md`

- Use as the retrieval map for active specs, active tasks, decisions, learnings, skills, templates, and archive entrypoints.
- Update whenever active task/spec state or file path changes.
- Do not store detailed requirements, implementation notes, or execution logs here.

### `repo/ROADMAP.md`

- Read or update when milestones, priorities, release scope, backlog themes, or project completion signals change.
- Use it to decide whether a milestone or project can be called complete.
- Do not update for routine task progress unless it changes milestone state.

### `repo/ARCHITECTURE.md`

- Read or update when module boundaries, invariants, interfaces, or cross-module behavior change.
- Keep durable architecture facts here.
- Do not store temporary debugging notes or task checklists here.

### `repo/specs/`

- Store active capability definitions and acceptance boundaries.
- Specs describe what must be true; they do not track step-by-step execution.
- Archive done, superseded, or deprecated specs when no active task references them.

### `repo/tasks/`

- Store active executable work units.
- Tasks define scope, forbidden changes, acceptance, test plan, validation, progress, result, and follow-ups.
- Archive done or canceled tasks after write-back when no active task depends on them.

### `repo/decisions/`

- Store durable technical decisions and tradeoffs.
- Add or update an ADR when a dependency, architecture, public contract, or long-lived approach changes.
- Do not use ADRs for minor implementation notes.

### `repo/learnings/`

- Store reusable debugging facts, failure modes, and delivery lessons.
- Add a learning when the same issue could recur or help a future agent.
- Promote repeatable learnings into `repo/skills/`.

### `repo/skills/`

- Store reusable procedures and checklists.
- Always keep `repo/skills/project-system-meta/SKILL.md`; it is the operating contract for this repo.
- Add or update a skill only when the procedure is reusable beyond the current task.

### `repo/_templates/`

- Store reusable local templates only.
- Use templates to create new specs, tasks, ADRs, learnings, and skills.
- Do not list templates as active specs/tasks in `repo/INDEX.md`.

### `repo/archive/`

- Store cold project memory that should not be read during normal startup.
- Read only when checking historical context, avoiding duplicate work, resolving an archived reference, or restoring old work.
- Do not delete archived content unless the project owner explicitly requests it.

## Memory Update Triggers

- Update `repo/ROADMAP.md` when milestones, priorities, release scope, backlog themes, or project completion signals change.
- Update `repo/ARCHITECTURE.md` when module boundaries, invariants, interfaces, or cross-module behavior change.
- Add or update `repo/decisions/` when a durable technical choice is made.
- Add or update `repo/learnings/` when a new failure mode, debugging fact, or reusable delivery lesson appears.
- Add or update `repo/skills/` when a learning becomes repeatable procedure.

## Archive Control

Keep `repo/tasks/` and `repo/specs/` small enough for an agent to scan safely.

Archive a task when all conditions are true:

1. Status is `done` or `canceled`.
2. `repo/STATUS.md` no longer names it as current focus.
3. No active task in `repo/INDEX.md` depends on it.
4. Result, validation, and follow-ups are written back.

Archive a spec when all conditions are true:

1. Status is `done`, `superseded`, or `deprecated`.
2. No active task in `repo/INDEX.md` references it.
3. Relevant decisions, learnings, and skills remain indexed.

Use `scripts/archive_item.py` when available. Archived files move to `repo/archive/tasks/` or `repo/archive/specs/`, and the archive event is recorded in `repo/archive/MANIFEST.md`.

## Completion Checks

Before claiming a task is complete:

1. Task acceptance criteria are satisfied.
2. Validation is recorded in the task and `repo/STATUS.md`.
3. `repo/INDEX.md` status matches the task status.
4. Triggered memory files are updated.
5. Follow-up work is captured in `repo/STATUS.md`, the task, or new tasks.

Before claiming a milestone or project is complete:

1. `repo/ROADMAP.md` exit criteria or project completion signals are satisfied.
2. `repo/STATUS.md` `Completion State` reflects the claim.
3. Blocking tasks in `repo/INDEX.md` are done or explicitly moved to follow-up.
4. Required validation from `repo/PROJECT.md` has passed or blockers are documented.

## Anti-Patterns

- Do not treat `repo/` as a place for source code, app tests, configs, or build files.
- Do not skip `repo/INDEX.md` and guess task/spec file names.
- Do not leave completion, blockers, or validation only in chat context.
- Do not create a learning without considering whether it should become a reusable skill.
