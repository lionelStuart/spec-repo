# Project

## Summary

Data AI Agent is a workspace assistant for analysts that ingests tabular datasets, explains schema quality, answers natural-language questions, and generates charts with transparent execution traces.

## Goals

- Let users upload CSV and Excel datasets and inspect schema quality.
- Answer natural-language analytical questions against registered datasets.
- Generate chart recommendations and executable query plans.

## Non-Goals

- Do not support arbitrary external database connections in phase one.
- Do not build autonomous background agents that mutate source data.

## Users

- Business analysts
- Data operations staff

## Global Constraints

- Keep all user-facing APIs OpenAI-agent friendly.
- Preserve traceability from natural-language question to executed data operation.
- Do not modify original uploaded files.

## Terminology

- `dataset registry`: metadata store for uploaded datasets and normalized schema
- `analysis plan`: structured tool-call sequence generated before execution
- `execution trace`: stored record of tool calls, outputs, and errors

## Default Commands

- `dev`: `make dev`
- `test`: `make test`
- `build`: `make build`
