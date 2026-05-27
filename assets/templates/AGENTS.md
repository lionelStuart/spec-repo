# Project Agent Protocol

## Purpose

Use root `AGENTS.md` plus `repo/` as the source of truth for project context, active work, and durable decisions.
Keep normal project files such as source code, app configuration, tests, docs, and build files in their existing project-root locations, not inside `repo/`.

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
5. The active task in `repo/tasks/`
6. The task-linked spec in `repo/specs/`
7. Only the architecture, decision, or skill files referenced by that task or spec

Do not read the whole repository by default.

## Start A Coding Round

1. Read and follow `repo/skills/project-system-meta/SKILL.md`.
2. Apply its `File Contracts` when reading or editing any file under `repo/`.
3. Use `repo/STATUS.md` to identify the current focus.
4. Use `repo/INDEX.md` to locate the matching task file and linked spec.
5. Read the task's `Required Context` before editing implementation files.
6. Confirm the task's `Modify Scope`, `Forbidden`, `Acceptance`, and `Test Plan`.
7. If no active task exists, create or request a task before making nontrivial code changes.

## Execution Rules

Follow this loop:

1. Read the active task and required context.
2. Produce a small plan.
3. Modify only files allowed by the task's `Modify Scope`.
4. Run the task's `Test Plan` or record why a listed check could not run.
5. Write back project state before ending the task.

## Context Triggers

- Read `repo/ROADMAP.md` when work changes milestones, priorities, release scope, or backlog themes.
- Read `repo/ARCHITECTURE.md` when work changes module boundaries, invariants, interfaces, or cross-module behavior.
- Read `repo/decisions/` entries only when the active task or spec references them, or when a durable technical choice is being made.
- Read `repo/learnings/` when debugging repeats a known failure mode or when a new failure mode should be captured.
- Read `repo/skills/` when the active task or spec references a reusable procedure, or when a learning should become repeatable guidance.
- Read `repo/archive/MANIFEST.md` only when checking historical work, avoiding duplicate tasks/specs, or archiving completed work.

## Constraints

- Do not work without a task unless the repository is being bootstrapped.
- Do not modify unrelated files.
- Do not put implementation source, application tests, configs, docs, or build files inside `repo/`.
- Do not change public contracts unless the task or spec explicitly allows it.
- Do not introduce dependencies or frameworks without recording the decision.
- Do not end implementation with unwritten context in model memory.
- Do not let `repo/tasks/` or `repo/specs/` become a permanent backlog; archive completed, canceled, superseded, or deprecated items when safe.

## Completion Gate

Do not claim a coding task is complete until all applicable items are true:

1. Implementation changes satisfy the task's `Acceptance` section.
2. The task's `Test Plan` has passed, or blocked checks are recorded in the task result.
3. The task `Progress` checklist reflects planned, implemented, validated, and written-back state.
4. `repo/STATUS.md` and `repo/INDEX.md` reflect the latest task state.
5. Durable decisions, reusable learnings, and reusable skills have been recorded when triggered.
6. A follow-up agent can continue from files alone without hidden chat context.

Do not claim the project or a milestone is complete until all applicable items are true:

1. `repo/ROADMAP.md` completion signals or milestone exit criteria are satisfied.
2. `repo/INDEX.md` has no active task that blocks the claimed milestone or project completion.
3. `repo/STATUS.md` `Completion State` says `complete` or clearly lists only non-blocking follow-ups.
4. Required validation commands from `repo/PROJECT.md` have passed, or release-blocking failures are recorded.
5. Remaining open issues are explicitly classified as non-blocking or moved into follow-up tasks.

## Mandatory End-Of-Task Update

After implementation, update all applicable files:

1. The active task's progress and result
2. `repo/STATUS.md`
3. `repo/INDEX.md` task status
4. The linked spec if behavior changed
5. `repo/ROADMAP.md` if milestones, priorities, or release scope changed
6. `repo/ARCHITECTURE.md` if boundaries, invariants, or interfaces changed
7. `repo/decisions/` if a durable technical choice was made
8. `repo/learnings/` if a new problem or debugging fact was discovered
9. `repo/skills/` if the learning became a reusable procedure
