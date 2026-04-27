# ADR-001: Use Metadata-First Ingestion Before Planning

## Status

accepted

## Context

Natural-language planning quality depends on trustworthy dataset metadata. If planning runs against raw, inconsistent column inference, downstream execution becomes brittle and explanations lose traceability.

## Decision

Require every uploaded dataset to pass through metadata extraction and schema normalization before it is exposed to the planning layer.

## Consequences

- planning receives stable semantic schema
- ingestion becomes a hard dependency for analysis
- debugging can target ingestion and planning separately

## Related Work

- `specs/SPEC-001-dataset-ingestion.md`
- `tasks/TASK-002-schema-normalization.md`
