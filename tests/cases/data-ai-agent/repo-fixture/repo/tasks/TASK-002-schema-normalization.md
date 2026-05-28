# TASK-002: Normalize Schema Types

## Status

doing

## Source

`SPEC-001`

## Goal

Normalize date, currency, and percentage columns into planner-safe semantic types with warnings for ambiguous inputs.

## Done Means

- normalized schema includes planner-safe semantic hints for date, currency, and percentage columns
- ambiguous mixed-format columns emit explicit warnings instead of silent coercion

## Required Context

- `repo/PROJECT.md`
- `repo/STATUS.md`
- `repo/specs/SPEC-001-dataset-ingestion.md`
- `repo/decisions/ADR-001-metadata-first.md`
- `repo/skills/tabular-schema-checklist/SKILL.md`

## Modify Scope

- `ingestion/*`
- `registry/*`
- `tests/*`

## Forbidden

- do not alter the chat-facing API
- do not add chart planning code here

## Acceptance

- normalization produces semantic hints for common analytical columns
- ambiguous inputs produce explicit warnings
- planner-facing schema output remains stable

## Test Plan

- mixed date formats trigger warning output
- clean currency columns normalize consistently
- percentage columns remain numeric and traceable

## Implementation Notes

- preserve raw uploaded file references
- keep schema output stable for planner consumers

## Progress

- [x] Planned
- [ ] Implemented
- [ ] Validated
- [ ] Written back

## Validation

- not run yet; implementation is still in progress

## Result

In progress.

## Follow-Ups

- update chart planner once normalization stabilizes
