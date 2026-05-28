# Project

## Summary

Web Minesweeper is a static HTML/CSS/JavaScript game fixture used to validate that `project-system` can guide a normal coding project while keeping implementation files outside `repo/`.

## Goals

- Provide a playable 9x9 Minesweeper game with 10 mines.
- Demonstrate project-system bootstrap, task execution, write-back, and validation on a small web project.

## Non-Goals

- No backend, persistence, user accounts, or leaderboard.
- No bundler, framework, package manager, or generated build output.

## Users

- A player opening `index.html` in a browser.
- An agent validating project-system behavior on a concrete coding task.

## Global Constraints

- Keep `index.html`, `styles.css`, and `script.js` at the project root.
- Keep project memory, specs, tasks, and archive files under `repo/`.
- The game must work without network access or a build step.

## Repository Layout

- `index.html`: static entrypoint.
- `styles.css`: game layout and visual state.
- `script.js`: Minesweeper state, interactions, timer, and win/loss logic.
- `repo/`: project memory and agent coordination files.
- Do not move source code, application tests, configs, docs, or build files into `repo/`.

## Coding Standards

- Use plain browser APIs and readable state transitions.
- Keep board dimensions stable so cells do not shift during play.
- Preserve keyboard support for flagging with `F`.

## Project Done Means

- A user can open `index.html`, reveal cells, flag suspected mines, reset, win, and lose.
- `repo/STATUS.md`, `repo/INDEX.md`, and the active task record completion and validation.

## Terminology

- `cell`: one square on the 9x9 board.
- `flag`: a marker placed on a suspected mine.
- `first-click-safe`: the first revealed cell and adjacent cells are guaranteed not to contain mines.

## Default Commands

- `dev`: open `index.html` in a browser.
- `test`: run `python3 ../../scripts/project_doctor.py .` from this case root, or run the project-system tests from the parent repository.
- `build`: not required for this static fixture.
