# TASK-001: Bootstrap Dataset Registry

## Status

done

## Source

`SPEC-001`

## Goal

Create the first ingestion path that accepts an uploaded file and stores baseline dataset metadata.

## Done Means

- uploaded files receive stable dataset IDs
- baseline metadata is persisted for later schema normalization

## Required Context

- `repo/PROJECT.md`
- `repo/STATUS.md`
- `repo/specs/SPEC-001-dataset-ingestion.md`
- `repo/ARCHITECTURE.md`

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

## Implementation Notes

- keep ingestion separate from planner behavior
- preserve the chat-facing response shape

## Progress

- [x] Planned
- [x] Implemented
- [x] Validated
- [x] Written back

## Validation

- valid CSV upload test: passed
- unsupported file error test: passed

## Result

Dataset registration now persists file metadata and baseline column information for later schema normalization.

## Follow-Ups

- `TASK-002` semantic normalization
