# Project Agent Protocol

## Purpose

Use root `AGENTS.md` plus `repo/` as the source of truth for project context, active work, and durable decisions.
Keep normal project files such as source code, app configuration, tests, docs, and build files in their existing project-root locations, not inside `repo/`.

## Project-System Governance

Do not remove this section. This project is governed by the external `project-system` skill. Agents must follow `project-system` rules when reading or editing `repo/`, including file contracts, task execution, write-back, archive control, and completion checks.

If this project is moved to an environment where `project-system` is not installed, keep this `AGENTS.md` as the local operating contract and preserve the `repo/` file contracts. Never leave root `AGENTS.md` without a project-system governance section.

## Mandatory Read Order

Read in this order before implementation:

1. `repo/PROJECT.md`
2. `repo/STATUS.md`
3. `repo/INDEX.md`
4. The active task in `repo/tasks/`
5. The task-linked spec in `repo/specs/`
6. Only the architecture, decision, or skill files referenced by that task or spec

Do not read the whole repository by default.

## Start A Coding Round

1. Follow the `project-system` file contracts when reading or editing any file under `repo/`.
2. Use `repo/STATUS.md` to identify the current focus.
3. Use `repo/INDEX.md` to locate the matching task file and linked spec.
4. Read the task's `Required Context` before editing implementation files.
5. Confirm the task's `Modify Scope`, `Forbidden`, `Acceptance`, and `Test Plan`.
6. If no active task exists, create or request a task before making nontrivial code changes.

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

## Project Skills Routing

Use `repo/skills/` for project-specific reusable procedures only.

- Read a project skill when the active task, spec, ADR, or learning references it.
- Read a project skill when the user request or current failure mode matches its `description` frontmatter.
- Add or update a project skill only after a learning becomes a repeatable procedure.
- Keep discoverable project skills as OpenAI/Codex-style directories with `SKILL.md` frontmatter.
- Do not place project-system governance rules in `repo/skills/`; governance stays in this root `AGENTS.md` and the external `project-system` skill.

## Constraints

- Do not work without a task unless the repository is being bootstrapped.
- Do not modify unrelated files.
- Do not put implementation source, application tests, configs, docs, or build files inside `repo/`.
- Do not change public contracts unless the task or spec explicitly allows it.
- Do not introduce dependencies or frameworks without recording the decision.
- Do not end implementation with unwritten context in model memory.
- Do not archive tasks or specs immediately on completion; keep recent inactive records for continuity.
- Do not let `repo/tasks/` or `repo/specs/` become a permanent backlog; archive older completed, canceled, superseded, or deprecated items when safe.

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
