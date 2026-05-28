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
3. Ensure root `AGENTS.md` explicitly states that the project is governed by this `project-system` skill.
4. Replace placeholder values before starting real work.
5. Keep the file names stable unless the project already has stronger conventions.

When script execution is allowed, prefer:

- `scripts/init_project.py` to materialize the template repo
- `scripts/new_task.py` to create a new task file
- `scripts/update_index.py` to register or refresh task and spec entries in `INDEX.md`
- `scripts/project_doctor.py` to diagnose governance, repo structure, index, archive, and project-skill routing drift
- `scripts/archive_item.py` to move inactive tasks and specs out of the active working set after the recent-retention window
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
2. `repo/PROJECT.md`
3. `repo/STATUS.md`
4. `repo/INDEX.md`
5. The active task in `repo/tasks/`
6. The task-linked spec in `repo/specs/`
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
- Read `repo/ROADMAP.md` only for planning, milestone, priority, release-scope, or backlog changes.
- Read or update `repo/ARCHITECTURE.md` when module boundaries, invariants, interfaces, or cross-module behavior change.
- Add or update `repo/decisions/`, `repo/learnings/`, and `repo/skills/` only when their trigger conditions are met, but do not leave those triggers only in chat context.
- Do not finish a task without writing back state.

## Project-System Tooling

When project-system scripts are available, prefer them over handwritten repetitive edits:

- Use `scripts/init_project.py` to initialize a target project root from `assets/templates/`.
- Use `scripts/new_task.py` to create tasks from `repo/_templates/TASK-template.md`.
- Use `scripts/update_index.py` to register or refresh active specs and tasks.
- Use `scripts/project_doctor.py` before or after meaningful project-memory edits to catch governance, repo layout, active index, archive entrypoint, and project-skill routing drift.
- Use `scripts/check_writeback.py` before ending a coding round.
- Use `scripts/archive_item.py` to move inactive specs and tasks into `repo/archive/` only after recent-retention rules allow it.

If scripts are not available in the target environment, follow the same file contracts manually. Keep generated specs and tasks in `repo/specs/` and `repo/tasks/`; keep reusable local templates in `repo/_templates/`; keep archived but preserved context in `repo/archive/`.

## File Contracts

Use each `repo/` file and directory according to this contract:

### `repo/PROJECT.md`

- Read at the start of a coding round to understand goals, non-goals, global constraints, default commands, repository layout, coding standards, and project done means.
- Update only when durable project facts change.
- Do not store task progress, transient blockers, or chat summaries here.

### `repo/STATUS.md`

- Read at the start of every coding round to find current focus, completion state, blockers, validation, and next steps.
- Update at the end of every coding round.
- Keep it short and current; do not turn it into a changelog or long narrative.

### `repo/INDEX.md`

- Use as the retrieval map for active specs, active tasks, decisions, learnings, skills, templates, and archive entrypoints.
- Update whenever active task/spec state or file path changes.
- Do not store detailed requirements, implementation notes, or execution logs here.

### `repo/ROADMAP.md`

- Read or update when milestones, priorities, release scope, backlog themes, or project completion signals change.
- Use it to decide whether a milestone or project can be called complete.
- Do not update for routine task progress unless it changes milestone state.

### `repo/ARCHITECTURE.md`

- Read or update when module boundaries, invariants, interfaces, or cross-module behavior change.
- Keep durable architecture facts here.
- Do not store temporary debugging notes or task checklists here.

### `repo/specs/`

- Store active capability definitions and acceptance boundaries.
- Specs describe what must be true; they do not track step-by-step execution.
- Keep recently completed, superseded, or deprecated specs in active memory for short-term continuity; archive older specs when no active task references them.

### `repo/tasks/`

- Store active executable work units.
- Tasks define scope, forbidden changes, acceptance, test plan, validation, progress, result, and follow-ups.
- Keep recently completed or canceled tasks in active memory for short-term continuity; archive older tasks after write-back when no active task depends on them.

### `repo/decisions/`

- Store durable technical decisions and tradeoffs.
- Add or update an ADR when a dependency, architecture, public contract, or long-lived approach changes.
- Do not use ADRs for minor implementation notes.

### `repo/learnings/`

- Store reusable debugging facts, failure modes, and delivery lessons.
- Add a learning when the same issue could recur or help a future agent.
- Promote repeatable learnings into `repo/skills/`.

### `repo/skills/`

- Store reusable project-specific procedures and checklists.
- Add or update a skill only when the procedure is reusable beyond the current task.
- Read a project skill when an active task, spec, ADR, or learning references it, or when the request matches its `description` frontmatter.
- Keep project skills in OpenAI/Codex skill format with `SKILL.md` frontmatter when they are meant to be discoverable.
- Do not store project-system operating rules here; those are governed by this external `project-system` skill and root `AGENTS.md`.

### `repo/_templates/`

- Store reusable local templates only.
- Use templates to create new specs, tasks, ADRs, learnings, and skills.
- Do not list templates as active specs/tasks in `repo/INDEX.md`.

### `repo/archive/`

- Store cold project memory that should not be read during normal startup.
- Read only when checking historical context, avoiding duplicate work, resolving an archived reference, or restoring old work.
- Do not delete archived content unless the project owner explicitly requests it.

## Archive Control

Keep `repo/tasks/` and `repo/specs/` small enough for an agent to scan safely.

Do not archive an item immediately just because it is done. Completed and canceled work should remain in the active working set while it is still recent context for the next agent.

Default recent-retention window:

- Keep the most recent 5 inactive tasks in `repo/tasks/`.
- Keep the most recent 3 inactive specs in `repo/specs/`.
- Use a different window only when the project owner or `repo/PROJECT.md` defines one.

Archive a task when all conditions are true:

1. Status is `done` or `canceled`.
2. It is outside the recent-retention window.
3. `repo/STATUS.md` no longer names it as current focus.
4. No active task in `repo/INDEX.md` depends on it.
5. Result, validation, and follow-ups are written back.

Archive a spec when all conditions are true:

1. Status is `done`, `superseded`, or `deprecated`.
2. It is outside the recent-retention window.
3. No active task in `repo/INDEX.md` references it.
4. Relevant decisions, learnings, and skills remain indexed.

Use `scripts/archive_item.py` when available. The script enforces recent retention by default. Archived files move to `repo/archive/tasks/` or `repo/archive/specs/`, and the archive event is recorded in `repo/archive/MANIFEST.md`.

## Completion Checks

Before claiming a task is complete:

1. Task acceptance criteria are satisfied.
2. Validation is recorded in the task and `repo/STATUS.md`.
3. `repo/INDEX.md` status matches the task status.
4. Triggered memory files are updated.
5. Follow-up work is captured in `repo/STATUS.md`, the task, or new tasks.

Before claiming a milestone or project is complete:

1. `repo/ROADMAP.md` exit criteria or project completion signals are satisfied.
2. `repo/STATUS.md` `Completion State` reflects the claim.
3. Blocking tasks in `repo/INDEX.md` are done or explicitly moved to follow-up.
4. Required validation from `repo/PROJECT.md` has passed or blockers are documented.

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

## Memory Update Triggers

Use these triggers to decide which durable memory files need edits:

- Update `repo/STATUS.md` at the end of every coding round.
- Update `repo/INDEX.md` when task status, spec status, document paths, dependencies, or archive state change.
- Update `repo/ROADMAP.md` when milestones, priorities, release scope, backlog themes, or project completion signals change.
- Update `repo/ARCHITECTURE.md` when module boundaries, invariants, interfaces, or cross-module behavior change.
- Add or update `repo/decisions/` when a dependency, architecture choice, public contract, irreversible migration, or long-lived implementation approach changes.
- Add or update `repo/learnings/` when a repeated failure mode, debugging fact, validation surprise, or reusable delivery lesson is discovered.
- Add or update `repo/skills/` only when a learning becomes a reusable project-specific procedure that future agents should execute.
- Update `repo/archive/MANIFEST.md` whenever tasks or specs are moved into archive.

Do not update every memory file by habit. Update the files whose trigger fired, and record explicitly when a required validation or write-back was blocked.

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
- `repo/PROJECT.md`: goals, non-goals, terminology, global constraints
- `repo/INDEX.md`: document IDs, state, tags, dependencies
- `repo/STATUS.md`: short-term memory for the next development round
- `repo/ROADMAP.md`: milestone and release view
- `repo/ARCHITECTURE.md`: system boundaries and invariants
- `repo/_templates/`: reusable local templates, not active work
- `repo/specs/`: capability definitions
- `repo/tasks/`: executable work units
- `repo/archive/`: older completed, canceled, superseded, or deprecated specs/tasks moved out of the active working set after recent retention
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
- `scripts/project_doctor.py`: diagnose governance, repo structure, index, archive, and project-skill routing drift
- `scripts/archive_item.py`: move inactive tasks/specs to `repo/archive/` after recent retention and record them in `repo/archive/MANIFEST.md`
- `scripts/check_writeback.py`: verify that core write-back artifacts still contain required sections

These scripts reduce drift in repetitive project-memory operations. They do not replace task judgment.

## Anti-Patterns

Never do the following:

- Start implementation without an active task when the work spans more than a trivial edit.
- Load every markdown file in the repo "just in case".
- Treat `STATUS.md` as a changelog.
- Store temporary chat transcripts in project memory files.
- Keep unresolved constraints only in model context instead of writing them to the repo.
