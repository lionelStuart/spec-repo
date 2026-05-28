# Project Agent Protocol

## Purpose

Use root `AGENTS.md` plus `repo/` as the operational memory system for the Data AI Agent project.
Keep implementation files in the project root. Use `repo/` only for project memory and agent coordination artifacts.

## Project-System Governance

Do not remove this section. This project is governed by the external `project-system` skill. Agents must follow `project-system` rules when reading or editing `repo/`, including file contracts, task execution, write-back, archive control, and completion checks.

If this project is moved to an environment where `project-system` is not installed, keep this `AGENTS.md` as the local operating contract and preserve the `repo/` file contracts. Never leave root `AGENTS.md` without a project-system governance section.

## Mandatory Read Order

Read in this order before implementation:

1. `repo/PROJECT.md`
2. `repo/STATUS.md`
3. `repo/INDEX.md`
4. the active task in `repo/tasks/`
5. the linked spec in `repo/specs/`
6. only linked architecture, decision, or reusable skill documents

Do not read the whole repository by default.

## Start A Coding Round

1. Follow the `project-system` file contracts when reading or editing any file under `repo/`.
2. Use `repo/STATUS.md` to identify the current focus.
3. Use `repo/INDEX.md` to locate the matching task file and linked spec.
4. Read the task's `Required Context` before editing implementation files.
5. Confirm the task's `Modify Scope`, `Forbidden`, `Acceptance`, and `Test Plan`.

## Execution Rules

1. Work only from an active task.
2. Keep file modifications within the task scope.
3. Update project state before ending the round.

## Context Triggers

- Read `repo/ROADMAP.md` when work changes milestones, priorities, release scope, or backlog themes.
- Read `repo/ARCHITECTURE.md` when work changes module boundaries, invariants, interfaces, or cross-module behavior.
- Read `repo/decisions/` when a referenced decision applies or when a durable technical choice is being made.
- Read `repo/learnings/` when debugging may repeat a known failure mode.
- Read `repo/skills/` when a referenced reusable checklist applies.
- Read `repo/archive/MANIFEST.md` only when checking historical work, avoiding duplicate tasks/specs, or archiving completed work.

## Project Skills Routing

Use `repo/skills/` for project-specific reusable procedures only.

- Read a project skill when the active task, spec, ADR, or learning references it.
- Read a project skill when the user request or current failure mode matches its `description` frontmatter.
- Add or update a project skill only after a learning becomes a repeatable procedure.
- Keep discoverable project skills as OpenAI/Codex-style directories with `SKILL.md` frontmatter.
- Do not place project-system governance rules in `repo/skills/`; governance stays in this root `AGENTS.md` and the external `project-system` skill.

## Mandatory End-Of-Task Update

After implementation, update:

1. the current task result and progress
2. `repo/STATUS.md`
3. `repo/INDEX.md`
4. any changed acceptance or constraint in the linked spec
5. `repo/ROADMAP.md` if milestones, priorities, or release scope changed
6. `repo/ARCHITECTURE.md` if boundaries, invariants, or interfaces changed
7. `repo/decisions/` if a durable technical choice was made
8. `repo/learnings/` for new debugging knowledge
9. `repo/skills/` if a learning becomes reusable

## Completion Gate

Do not claim a coding task is complete until acceptance criteria pass, validation is recorded, progress is written back, and a follow-up agent can continue from files alone.

Do not claim the project or current milestone is complete until `repo/ROADMAP.md` exit criteria are satisfied, `repo/STATUS.md` completion state is updated, blocking tasks are closed or moved to follow-up, and validation has passed or is explicitly blocked.

Do not archive tasks or specs immediately on completion; keep recent inactive records for continuity.
Keep `repo/tasks/` and `repo/specs/` focused on active work; archive older completed, canceled, superseded, or deprecated items into `repo/archive/` when safe.
