# Agent Run Harness

Use this harness to evaluate the real effect of `project-system` on a coding agent.

The evaluation has two stages:

1. `agent run`: ask an agent to use the skill and operate on a project case
2. `judge review`: ask an independent model to score the resulting artifacts

## Goal

Measure actual agent behavior, not only template quality.

The key question is:

`When an agent uses this skill on a realistic project task, does it stay grounded, load context progressively, preserve state, and improve continuity across rounds?`

## Evaluation Flow

### Stage 1: Agent Run

Give the agent:

- the skill path
- the case description
- the fixture repo
- a concrete task to advance

The agent must:

1. use the `project-system` skill
2. read context through the repo protocol
3. advance the active task
4. write back task, status, index, and any new learnings or skills
5. leave all outputs in the repo fixture

### Stage 2: Judge Review

Give a separate judge model:

- the rubric
- the case description
- the original fixture
- the post-run fixture
- the agent transcript or summarized action log

The judge scores:

- how well the skill shaped the agent's behavior
- how much the repo artifacts improved after the run
- whether the write-back protocol actually preserved useful state

## Required Inputs

- [SKILL.md](/Users/a1021500406/private/spec-repo/project-system/SKILL.md)
- [llm-judge-rubric.md](/Users/a1021500406/private/spec-repo/project-system/tests/llm-judge-rubric.md)
- [CASE.md](/Users/a1021500406/private/spec-repo/project-system/tests/cases/data-ai-agent/CASE.md)
- the repo fixture directory

## Output Expectations

The evaluation should produce:

1. agent run prompt
2. judge prompt
3. post-run repo artifact snapshot
4. judge report with scores and failure analysis

## Success Standard

This harness is working if:

- the agent meaningfully updates the repo instead of just chatting about it
- the judge can distinguish strong versus weak runs
- the resulting report helps improve the skill, not just praise it
