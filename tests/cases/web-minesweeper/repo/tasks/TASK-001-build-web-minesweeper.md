# TASK-001: Build Web Minesweeper

## Status

done

## Source

`SPEC-001`

## Goal

Create the smallest useful static Web Minesweeper game and prove that implementation files can live at the project root while project memory remains under `repo/`.

## Done Means

- `index.html`, `styles.css`, and `script.js` implement a playable 9x9 Minesweeper game.
- Project-system memory files describe the task, spec, status, and validation.

## Required Context

- `repo/PROJECT.md`
- `repo/STATUS.md`
- `repo/specs/SPEC-001-web-minesweeper.md`

## Modify Scope

- `index.html`
- `styles.css`
- `script.js`
- `repo/PROJECT.md`
- `repo/STATUS.md`
- `repo/INDEX.md`
- `repo/specs/SPEC-001-web-minesweeper.md`
- `repo/tasks/TASK-001-build-web-minesweeper.md`

## Forbidden

- Do not move implementation files into `repo/`.
- Do not add a frontend framework or build step.

## Acceptance

- Opening `index.html` renders the game board and controls.
- First reveal is safe.
- Left click reveals cells and zero cells expand to neighbors.
- Right click and `F` flag cells.
- Reset starts a fresh game.
- Status text reports progress, win, and loss.

## Test Plan

- Run `python3 scripts/project_doctor.py tests/cases/web-minesweeper`.
- Run `python3 scripts/check_writeback.py tests/cases/web-minesweeper/repo --task tasks/TASK-001-build-web-minesweeper.md`.
- Inspect `index.html` in a browser for basic playability when interactive browser validation is available.

## Implementation Notes

- Mine placement happens after the first reveal so the first cell and neighbors can be excluded.
- The game uses plain DOM APIs and no external assets.

## Progress

- [x] Planned
- [x] Implemented
- [x] Validated
- [x] Written back

## Validation

- `python3 scripts/project_doctor.py tests/cases/web-minesweeper`: passed.
- `python3 scripts/check_writeback.py tests/cases/web-minesweeper/repo --task tasks/TASK-001-build-web-minesweeper.md`: passed.
- `node --check tests/cases/web-minesweeper/script.js`: passed.
- Static fixture checks for HTML/CSS/JS wiring and Minesweeper constants: passed.

## Result

Created a static Web Minesweeper fixture with root implementation files and complete project-system memory.

## Follow-Ups

- Add Playwright browser assertions if this fixture becomes part of UI automation.
