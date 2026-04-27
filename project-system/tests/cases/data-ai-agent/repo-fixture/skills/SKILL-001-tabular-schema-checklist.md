# SKILL-001: Tabular Schema Checklist

## Applies To

- csv ingestion
- excel ingestion
- schema profiling

## Preconditions

- a dataset file has been registered
- raw columns are available for inspection

## Checklist

1. confirm header extraction succeeded
2. test date, currency, and percentage inference on representative samples
3. preserve both original column names and normalized semantic types
4. emit explicit warnings for ambiguous mixed-format columns
5. verify planner-facing schema shape remains stable

## Common Failure Modes

- mixed date formats collapse into string columns
- currency symbols produce non-numeric inference
- percentage strings lose numeric comparability

## Verification

- run ingestion tests against mixed-format fixtures
- inspect normalized schema output before planner integration
