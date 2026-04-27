# Agent Run Prompt: Data AI Agent

Use `project-system` at:

`/Users/a1021500406/private/spec-repo/project-system`

Operate on this case:

`/Users/a1021500406/private/spec-repo/project-system/tests/cases/data-ai-agent/CASE.md`

Operate on this project repo fixture:

`/Users/a1021500406/private/spec-repo/project-system/tests/cases/data-ai-agent/repo-fixture`

## Task

Advance the project from the current state by completing the active work around schema normalization for the Data AI Agent project.

## Required Behavior

1. Follow the repo loading protocol rather than reading everything at once.
2. Work from the active task and its linked spec.
3. Improve the project state as if you were the coding agent assigned to the next development round.
4. Write back all relevant state into the repo fixture.

## Minimum Expected Outputs

- update the active task progress and result
- update `STATUS.md`
- update `INDEX.md` if task state changes
- add or update a learning if new reusable debugging knowledge emerges
- add or update a reusable skill if the learning should become repeatable guidance

## Constraints

- stay within the project-system workflow
- do not rewrite the whole repo
- do not remove existing project memory structure
- prefer narrow, high-signal updates over large generic rewrites

## Deliverable

Modify the fixture repo in place so a follow-up agent can continue from your written artifacts without relying on hidden chat context.
