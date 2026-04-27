# Status

## Current Focus

- `TASK-002` schema normalization for uploaded datasets

## Last Completed

- `TASK-001` created the dataset registry bootstrap flow
- added initial upload metadata validation

## Current Constraints

- do not change external chat-facing API contracts
- keep ingestion and query planning loosely coupled
- preserve raw uploaded file references for auditing

## Open Issues

- date-like columns are inconsistently inferred across CSV sources
- chart suggestions do not yet use normalized semantic types

## Next Steps

1. finish schema normalization rules for date, currency, and percentage columns
2. add failure-path tests for ambiguous column inference
3. update the chart planner to consume normalized schema metadata
