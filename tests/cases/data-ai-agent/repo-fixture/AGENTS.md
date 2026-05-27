# Project Agent Protocol

## Purpose

Use root `AGENTS.md` plus `repo/` as the operational memory system for the Data AI Agent project.
Keep implementation files in the project root. Use `repo/` only for project memory and agent coordination artifacts.

## Protected Meta Skill Link

Do not remove this section or the link below. This root `AGENTS.md` must always bind the project to the project-system meta skill:

- Required meta skill: `repo/skills/project-system-meta/SKILL.md`
- Discoverable skill directory: `repo/skills/project-system-meta/`

`repo/skills/project-system-meta/` is an OpenAI/Codex-style meta skill directory. Its `SKILL.md` defines how agents must use `repo/` to build, maintain, validate, archive, and complete this project. Agents must treat it as the operating skill for this project, not as optional documentation.

If the path changes, update the path here, in `repo/INDEX.md`, and in every active task's `Required Context` in the same change. Never leave root `AGENTS.md` without a required meta skill link.

## Mandatory Read Order

Read in this order before implementation:

1. `repo/skills/project-system-meta/SKILL.md`
2. `repo/PROJECT.md`
3. `repo/STATUS.md`
4. `repo/INDEX.md`
5. the active task in `repo/tasks/`
6. the linked spec in `repo/specs/`
7. only linked architecture, decision, or reusable skill documents

Do not read the whole repository by default.

## Start A Coding Round

1. Read and follow `repo/skills/project-system-meta/SKILL.md`.
2. Apply its `File Contracts` when reading or editing any file under `repo/`.
3. Use `repo/STATUS.md` to identify the current focus.
4. Use `repo/INDEX.md` to locate the matching task file and linked spec.
5. Read the task's `Required Context` before editing implementation files.
6. Confirm the task's `Modify Scope`, `Forbidden`, `Acceptance`, and `Test Plan`.

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

Keep `repo/tasks/` and `repo/specs/` focused on active work; archive completed, canceled, superseded, or deprecated items into `repo/archive/` when safe.
