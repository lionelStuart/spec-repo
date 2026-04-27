# Judge Prompt: Data AI Agent Agent-Run Evaluation

You are evaluating the real effect of a project-memory skill on a coding agent.

Use this rubric:

`/Users/a1021500406/private/spec-repo/tests/llm-judge-rubric.md`

Use this case:

`/Users/a1021500406/private/spec-repo/tests/cases/data-ai-agent/CASE.md`

Use this skill:

`/Users/a1021500406/private/spec-repo/SKILL.md`

You will compare:

1. the pre-run repo fixture
2. the post-run repo fixture
3. the agent's action log or transcript summary

## What To Judge

Judge whether the skill improved actual agent execution quality.

Focus on:

- whether the agent stayed grounded in task and spec
- whether it loaded context progressively
- whether it wrote back enough state for the next round
- whether the resulting repo is more operationally useful after the run
- whether learnings and reusable skills were updated in a meaningful way

## Output Format

1. score each rubric dimension from `1` to `10`
2. provide one concise paragraph of reasoning per dimension
3. provide an overall score out of `100`
4. provide one verdict:
   - `Not Ready`
   - `Useful But Fragile`
   - `Strong`
   - `Production-Worthy`
5. list the top three reasons the run succeeded or failed

## Constraint

Do not reward the run merely because files changed.

Reward the run only if the resulting repo state would genuinely help a new agent continue the project with less context loss and better task control.
