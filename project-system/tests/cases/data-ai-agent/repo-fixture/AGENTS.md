# Project Agent Protocol

## Purpose

Use this repository as the operational memory system for the Data AI Agent project.

## Mandatory Read Order

Read in this order before implementation:

1. `PROJECT.md`
2. `STATUS.md`
3. `INDEX.md`
4. the active task in `tasks/`
5. the linked spec in `specs/`
6. only linked architecture, decision, or reusable skill documents

Do not read the whole repository by default.

## Execution Rules

1. Work only from an active task.
2. Keep file modifications within the task scope.
3. Update project state before ending the round.

## Mandatory End-Of-Task Update

After implementation, update:

1. the current task result and progress
2. `STATUS.md`
3. `INDEX.md`
4. any changed acceptance or constraint in the linked spec
5. `decisions/` if a durable technical choice was made
6. `learnings/` for new debugging knowledge
7. `skills/` if a learning becomes reusable
