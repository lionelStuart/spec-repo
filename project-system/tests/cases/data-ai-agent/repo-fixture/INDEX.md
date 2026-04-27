# Index

## Specs

| ID | File | Status | Tags | Depends On |
| --- | --- | --- | --- | --- |
| SPEC-001 | `specs/SPEC-001-dataset-ingestion.md` | active | data,ingestion,schema | `ARCHITECTURE.md`, `decisions/ADR-001-metadata-first.md` |

## Tasks

| ID | File | Status | Spec | Depends On |
| --- | --- | --- | --- | --- |
| TASK-001 | `tasks/TASK-001-bootstrap-ingestion.md` | done | SPEC-001 | - |
| TASK-002 | `tasks/TASK-002-schema-normalization.md` | doing | SPEC-001 | TASK-001 |

## Decisions

| ID | File | Status | Scope |
| --- | --- | --- | --- |
| ADR-001 | `decisions/ADR-001-metadata-first.md` | accepted | ingestion,planning |

## Learnings

| ID | File | Topic | Trigger |
| --- | --- | --- | --- |
| LEARN-001 | `learnings/LEARN-001-date-column-normalization.md` | schema normalization | CSV import bug |

## Skills

| ID | File | Applies To |
| --- | --- | --- |
| SKILL-001 | `skills/SKILL-001-tabular-schema-checklist.md` | csv,xlsx,schema,profiling |
