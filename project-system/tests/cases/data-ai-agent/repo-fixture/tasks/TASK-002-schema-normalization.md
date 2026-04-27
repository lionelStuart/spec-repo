# TASK-002: Normalize Schema Types

## Status

doing

## Source

`SPEC-001`

## Goal

Normalize date, currency, and percentage columns into planner-safe semantic types with warnings for ambiguous inputs.

## Required Context

- `PROJECT.md`
- `STATUS.md`
- `specs/SPEC-001-dataset-ingestion.md`
- `decisions/ADR-001-metadata-first.md`
- `skills/SKILL-001-tabular-schema-checklist.md`

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

## Progress

- [x] Planned
- [ ] Implemented
- [ ] Validated
- [ ] Written back

## Result

In progress.

## Follow-Ups

- update chart planner once normalization stabilizes
