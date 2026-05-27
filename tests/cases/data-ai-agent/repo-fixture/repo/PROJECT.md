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

## Repository Layout

- Implementation files live in the project root using the product's normal source tree.
- Project memory and agent coordination files live in `repo/`.
- Do not move ingestion, registry, planner, tests, configs, or build files into `repo/`.

## Coding Standards

- Keep ingestion, planning, and execution boundaries separate.
- Add tests for schema inference behavior before marking ingestion tasks validated.

## Project Done Means

- analysts can upload CSV and Excel files and inspect normalized schema quality
- planner-facing schema metadata is stable enough for natural-language analysis planning

## Terminology

- `dataset registry`: metadata store for uploaded datasets and normalized schema
- `analysis plan`: structured tool-call sequence generated before execution
- `execution trace`: stored record of tool calls, outputs, and errors

## Default Commands

- `dev`: `make dev`
- `test`: `make test`
- `build`: `make build`
