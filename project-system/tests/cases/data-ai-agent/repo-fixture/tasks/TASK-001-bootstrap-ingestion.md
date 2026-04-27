# TASK-001: Bootstrap Dataset Registry

## Status

done

## Source

`SPEC-001`

## Goal

Create the first ingestion path that accepts an uploaded file and stores baseline dataset metadata.

## Required Context

- `PROJECT.md`
- `STATUS.md`
- `specs/SPEC-001-dataset-ingestion.md`
- `ARCHITECTURE.md`

## Modify Scope

- `ingestion/*`
- `registry/*`

## Forbidden

- do not add planner behavior
- do not change chat-facing response shape

## Acceptance

- uploaded file receives a dataset ID
- baseline column list is stored in the registry

## Test Plan

- upload a valid CSV and confirm dataset ID creation
- upload an unsupported file and confirm a clear error

## Progress

- [x] Planned
- [x] Implemented
- [x] Validated
- [x] Written back

## Result

Dataset registration now persists file metadata and baseline column information for later schema normalization.

## Follow-Ups

- `TASK-002` semantic normalization
