---
name: project-system
description: Initialize or operate an AI-native project memory repo for long-running software work. Use when Codex needs to bootstrap a new project structure, load project context progressively from repo documents, execute work from specs and tasks, or write back status, decisions, learnings, and reusable skills after implementation.
---

# Project System

Use this skill to turn a repository into a durable project memory system instead of a loose set of markdown files.

Use the templates in [`assets/templates/`](./assets/templates/) as the default project skeleton.
Use the scripts in [`scripts/`](./scripts/) when available so repetitive setup and write-back checks are less dependent on manual document-following.

## Bootstrap A Repo

When the repository does not already contain a project memory system:

1. Create the root files from `assets/templates/`.
2. Create the directories from `assets/templates/specs`, `tasks`, `decisions`, `learnings`, and `skills`.
3. Replace placeholder values before starting real work.
4. Keep the file names stable unless the project already has stronger conventions.

When script execution is allowed, prefer:

- `scripts/init_project.py` to materialize the template repo
- `scripts/new_task.py` to create a new task file
- `scripts/update_index.py` to register or refresh task and spec entries in `INDEX.md`
- `scripts/check_writeback.py` before ending a development round

Use this default root layout (keep implementation project files and memory repo isolated as siblings):

```text
root/
├── project/
└── repo/
    ├── AGENTS.md
    ├── PROJECT.md
    ├── INDEX.md
    ├── STATUS.md
    ├── ROADMAP.md
    ├── ARCHITECTURE.md
    ├── specs/
    ├── tasks/
    ├── decisions/
    ├── learnings/
    └── skills/
```

Never flatten template files directly into `root/`. The memory system files belong inside `root/repo/` only.

## Load Context Progressively

Never read the whole repo by default.

Read in this order:

1. `AGENTS.md`
2. `PROJECT.md`
3. `STATUS.md`
4. `INDEX.md`
5. The active task in `tasks/`
6. The task-linked spec in `specs/`
7. Only the architecture, decision, or skill files referenced by that task or spec

Use `INDEX.md` as the retrieval map. Do not guess document names if the index already defines them.

If no task exists yet, create one before implementation unless the user explicitly wants repo bootstrap only.

## Operate The Development Loop

Use this fixed loop:

1. Read the active task and linked context.
2. Produce or confirm a small plan.
3. Modify only the scoped files.
4. Update project memory before ending the task.
5. Run an `LLM judge` evaluation for the round and write the score back to the repo when the environment supports it.

Treat `specs/` as capability definitions and `tasks/` as execution units.

Use these rules:

- Do not work from a spec alone when the change is nontrivial.
- Do not modify unrelated files.
- Do not read architecture or decisions unless the active task depends on them.
- Do not finish a task without writing back state.

## Write Back State

At the end of every implementation task, update all applicable files:

1. Update the active task's progress, result, and follow-ups.
2. Update `STATUS.md` with current focus, completed work, open issues, and next steps.
3. Update `INDEX.md` task status when state changed.
4. Update the linked spec if acceptance criteria or constraints changed.
5. Add or update an ADR in `decisions/` if a durable technical choice was made.
6. Add a learning in `learnings/` if a new failure mode or debugging fact was discovered.
7. Add or update a reusable procedure in `skills/` if the learning can be executed again.
8. Record the round's `LLM judge` result in a report or status artifact so the next round can optimize against it.

Prefer small, specific write-backs. Do not dump long narratives into `STATUS.md`.

## Evaluate Every Round

Treat `LLM judge` scoring as a required part of the development loop, not an optional review step.

For every meaningful round:

1. collect the updated repo artifacts for the round
2. evaluate the round with the judge rubric
3. record the score, reasoning, and top failures
4. use the weakest scored dimension to guide the next improvement round

If the environment cannot run a full independent judge, record that explicitly instead of silently skipping evaluation.

## File Semantics

Use the templates as the baseline contract:

- `AGENTS.md`: repo rules, loading order, write-back rules
- `PROJECT.md`: goals, non-goals, terminology, global constraints
- `INDEX.md`: document IDs, state, tags, dependencies
- `STATUS.md`: short-term memory for the next development round
- `ROADMAP.md`: milestone and release view
- `ARCHITECTURE.md`: system boundaries and invariants
- `specs/`: capability definitions
- `tasks/`: executable work units
- `decisions/`: durable technical decisions
- `learnings/`: incident-style findings and debugging notes
- `skills/`: reusable procedures distilled from repeated work

## Use The Templates

Read template files from `assets/templates/` only when needed:

- Use `AGENTS.md`, `PROJECT.md`, `INDEX.md`, `STATUS.md`, `ROADMAP.md`, and `ARCHITECTURE.md` when bootstrapping.
- Use `specs/SPEC-001-template.md` to define a new capability.
- Use `tasks/TASK-001-template.md` to define an execution unit.
- Use `decisions/ADR-template.md` for architecture decisions.
- Use `learnings/LEARNING-template.md` for postmortems or debugging findings.
- Use `skills/SKILL-template.md` when promoting a learning into a reusable procedure.

## Use The Scripts

Prefer the provided scripts over handwritten repetitive setup:

- `scripts/init_project.py`: initialize a target repo from the template set
- `scripts/new_task.py`: create a task file with task ID, title, and source spec filled in
- `scripts/update_index.py`: add or refresh `spec` and `task` rows in `INDEX.md`
- `scripts/check_writeback.py`: verify that core write-back artifacts still contain required sections

These scripts reduce drift in repetitive project-memory operations. They do not replace task judgment.

## Anti-Patterns

Never do the following:

- Start implementation without an active task when the work spans more than a trivial edit.
- Load every markdown file in the repo "just in case".
- Treat `STATUS.md` as a changelog.
- Store temporary chat transcripts in project memory files.
- Keep unresolved constraints only in model context instead of writing them to the repo.
