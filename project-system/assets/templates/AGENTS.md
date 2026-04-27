# Project Agent Protocol

## Purpose

Use this repository as the source of truth for project context, active work, and durable decisions.

## Mandatory Read Order

Read in this order before implementation:

1. `PROJECT.md`
2. `STATUS.md`
3. `INDEX.md`
4. The active task in `tasks/`
5. The task-linked spec in `specs/`
6. Only the architecture, decision, or skill files referenced by that task or spec

Do not read the whole repository by default.

## Execution Rules

Follow this loop:

1. Read the active task and required context.
2. Produce a small plan.
3. Modify only scoped files.
4. Write back project state before ending the task.

## Constraints

- Do not work without a task unless the repository is being bootstrapped.
- Do not modify unrelated files.
- Do not change public contracts unless the task or spec explicitly allows it.
- Do not introduce dependencies or frameworks without recording the decision.
- Do not end implementation with unwritten context in model memory.

## Mandatory End-Of-Task Update

After implementation, update all applicable files:

1. The active task's progress and result
2. `STATUS.md`
3. `INDEX.md` task status
4. The linked spec if behavior changed
5. `decisions/` if a durable technical choice was made
6. `learnings/` if a new problem or debugging fact was discovered
7. `skills/` if the learning became a reusable procedure
