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

1. Create root `AGENTS.md` from `assets/templates/AGENTS.md`.
2. Create `repo/` from the remaining `assets/templates/` files and directories.
3. Ensure `repo/skills/project-system-meta/SKILL.md` exists and is referenced by root `AGENTS.md`.
4. Replace placeholder values before starting real work.
5. Keep the file names stable unless the project already has stronger conventions.

When script execution is allowed, prefer:

- `scripts/init_project.py` to materialize the template repo
- `scripts/new_task.py` to create a new task file
- `scripts/update_index.py` to register or refresh task and spec entries in `INDEX.md`
- `scripts/archive_item.py` to move inactive tasks and specs out of the active working set
- `scripts/check_writeback.py` before ending a development round

Use this default root layout (keep the project-level agent protocol at the project root and project memory inside `repo/`):

```text
root/
├── AGENTS.md
├── src/ or app files
├── package/config/build files
├── docs/ or other normal project files
└── repo/
    ├── PROJECT.md
    ├── INDEX.md
    ├── STATUS.md
    ├── ROADMAP.md
    ├── ARCHITECTURE.md
    ├── _templates/
    ├── specs/
    ├── tasks/
    ├── archive/
    ├── decisions/
    ├── learnings/
    └── skills/
```

Only `AGENTS.md` from this skill belongs directly in `root/`. All other memory system files belong inside `root/repo/`.
Do not move normal project files into `repo/`; source code, app configuration, tests, docs, and build files stay in their existing project-root locations.

## Load Context Progressively

Never read the whole repo by default.

Read in this order:

1. `AGENTS.md`
2. `repo/skills/project-system-meta/SKILL.md`
3. `repo/PROJECT.md`
4. `repo/STATUS.md`
5. `repo/INDEX.md`
6. The active task in `repo/tasks/`
7. The task-linked spec in `repo/specs/`
8. Only the architecture, decision, or skill files referenced by that task or spec

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
- Read `repo/ROADMAP.md` only for planning, milestone, priority, release-scope, or backlog changes.
- Read or update `repo/ARCHITECTURE.md` when module boundaries, invariants, interfaces, or cross-module behavior change.
- Add or update `repo/decisions/`, `repo/learnings/`, and `repo/skills/` only when their trigger conditions are met, but do not leave those triggers only in chat context.
- Do not finish a task without writing back state.

## Write Back State

At the end of every implementation task, update all applicable files:

1. Update the active task's progress, result, and follow-ups.
2. Update `STATUS.md` with current focus, completed work, open issues, and next steps.
3. Update `INDEX.md` task status when state changed.
4. Update the linked spec if acceptance criteria or constraints changed.
5. Update `ROADMAP.md` if milestones, priorities, release scope, or backlog themes changed.
6. Update `ARCHITECTURE.md` if boundaries, invariants, interfaces, or cross-module behavior changed.
7. Add or update an ADR in `decisions/` if a durable technical choice was made.
8. Add a learning in `learnings/` if a new failure mode or debugging fact was discovered.
9. Add or update a reusable procedure in `skills/` if the learning can be executed again.
10. Record the round's `LLM judge` result in a report or status artifact so the next round can optimize against it.

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

- root `AGENTS.md`: project-level agent entrypoint, loading order, write-back rules
- `repo/skills/project-system-meta/SKILL.md`: meta skill that defines how to operate project-system as a closed loop
- `repo/PROJECT.md`: goals, non-goals, terminology, global constraints
- `repo/INDEX.md`: document IDs, state, tags, dependencies
- `repo/STATUS.md`: short-term memory for the next development round
- `repo/ROADMAP.md`: milestone and release view
- `repo/ARCHITECTURE.md`: system boundaries and invariants
- `repo/_templates/`: reusable local templates, not active work
- `repo/specs/`: capability definitions
- `repo/tasks/`: executable work units
- `repo/archive/`: completed, canceled, superseded, or deprecated specs/tasks moved out of the active working set
- `repo/decisions/`: durable technical decisions
- `repo/learnings/`: incident-style findings and debugging notes
- `repo/skills/`: reusable procedures distilled from repeated work

## Use The Templates

Read template files from `assets/templates/` only when needed:

- Use `AGENTS.md` at the project root, then `PROJECT.md`, `INDEX.md`, `STATUS.md`, `ROADMAP.md`, and `ARCHITECTURE.md` inside `repo/` when bootstrapping.
- Use `_templates/SPEC-template.md` to define a new capability.
- Use `_templates/TASK-template.md` to define an execution unit.
- Use `_templates/ADR-template.md` for architecture decisions.
- Use `_templates/LEARNING-template.md` for postmortems or debugging findings.
- Use `_templates/SKILL-template.md` when promoting a learning into a reusable procedure.

## Use The Scripts

Prefer the provided scripts over handwritten repetitive setup:

- `scripts/init_project.py`: initialize a target repo from the template set
- `scripts/new_task.py`: create a task file with task ID, title, and source spec filled in
- `scripts/update_index.py`: add or refresh `spec` and `task` rows in `INDEX.md`
- `scripts/archive_item.py`: move inactive tasks/specs to `repo/archive/` and record them in `repo/archive/MANIFEST.md`
- `scripts/check_writeback.py`: verify that core write-back artifacts still contain required sections

These scripts reduce drift in repetitive project-memory operations. They do not replace task judgment.

## Anti-Patterns

Never do the following:

- Start implementation without an active task when the work spans more than a trivial edit.
- Load every markdown file in the repo "just in case".
- Treat `STATUS.md` as a changelog.
- Store temporary chat transcripts in project memory files.
- Keep unresolved constraints only in model context instead of writing them to the repo.
