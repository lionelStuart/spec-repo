# Architecture

## System Summary

The system accepts uploaded datasets, extracts schema metadata, stores normalized dataset descriptors, plans analysis steps from natural language, executes approved operations, and records execution traces.

## Boundaries

- Ingestion owns file registration and schema profiling.
- Planning owns question interpretation and tool selection.
- Execution owns running tabular operations and chart generation.

## Invariants

- Every answer must map back to a dataset ID and execution trace.
- Schema normalization must happen before planning uses dataset metadata.
- Raw uploaded files remain immutable.

## Modules

### ingestion

- Responsibility: register datasets and infer schema
- Inputs: uploaded CSV or Excel file
- Outputs: dataset metadata, normalized columns, storage reference
- Forbidden Changes: do not embed planning logic here

### planner

- Responsibility: convert user intent into an analysis plan
- Inputs: user question, dataset metadata
- Outputs: ordered tool-call plan
- Forbidden Changes: do not execute data operations directly

### execution

- Responsibility: run approved tabular operations and chart generation
- Inputs: analysis plan, dataset reference
- Outputs: result table, chart artifact, execution trace
- Forbidden Changes: do not mutate source files

## External Interfaces

- chat-facing agent API
- internal dataset registry
- object storage for uploaded files
