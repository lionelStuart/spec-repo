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
| PROJECT-SYSTEM-META | `skills/project-system-meta/SKILL.md` | all project-system agent rounds |
| SKILL-001 | `skills/tabular-schema-checklist/SKILL.md` | csv,xlsx,schema,profiling |

## Templates

- Spec template: `_templates/SPEC-template.md`
- Task template: `_templates/TASK-template.md`
- ADR template: `_templates/ADR-template.md`
- Learning template: `_templates/LEARNING-template.md`
- Skill template: `_templates/SKILL-template.md`
