# SPEC-001: Dataset Ingestion And Schema Normalization

## Status

active

## Goal

Register uploaded CSV and Excel files, infer schema, normalize semantic column types, and store metadata that downstream planners can consume safely.

## Non-Goals

- do not implement autonomous data cleaning
- do not support external SQL databases in this phase

## Inputs

- uploaded file
- file-level metadata
- ingestion configuration

## Outputs

- dataset ID
- normalized schema metadata
- storage reference to the raw file

## Constraints

- do not mutate the raw uploaded file
- preserve original column names alongside normalized semantic types
- schema output must remain planner-compatible

## Error Cases

- unsupported file format
- ambiguous type inference for mixed-format columns
- missing header rows

## Acceptance

- users can register a CSV or Excel file and receive a dataset ID
- normalized schema includes semantic hints for dates, currency, and percentages
- ambiguous columns produce explicit warnings instead of silent coercion

## Related Context

- `ARCHITECTURE.md`
- `decisions/ADR-001-metadata-first.md`
- `skills/SKILL-001-tabular-schema-checklist.md`
