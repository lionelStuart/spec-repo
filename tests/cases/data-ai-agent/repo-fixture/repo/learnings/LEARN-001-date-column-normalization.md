# LEARN-001: Mixed Date Columns Collapse Into Strings

## Date

2026-04-27

## Context

While testing schema normalization for uploaded CSV files, columns containing both `YYYY-MM-DD` and `MM/DD/YYYY` values were inferred as plain strings.

## Symptom

The planner lost confidence in date-aware aggregations and stopped recommending time-series charts.

## Cause

The inference step used one-pass sampling without a normalization fallback for mixed date formats.

## Fix

- add a second-pass date parser for mixed common formats
- record a warning when normalization succeeds with fallback logic

## Reuse Value

This should remain reusable because mixed date columns are likely to recur across business-uploaded spreadsheets. Promote it into a schema-checklist skill.
