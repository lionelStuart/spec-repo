# SPEC-001: Web Minesweeper

## Status

done

## Goal

Provide a static browser Minesweeper game that can be opened directly from `index.html` and played without a build step.

## Non-Goals

- No backend persistence, accounts, leaderboard, or multiplayer.
- No configurable board sizes for this fixture.

## Inputs

- Left click or keyboard activation to reveal a cell.
- Right click or `F` key to toggle a flag.
- Reset button to start a new game.

## Outputs

- A 9x9 Minesweeper board with 10 mines.
- Mine counter, timer, status text, win state, and loss state.

## Constraints

- Implementation files stay in the project root.
- Project memory and coordination files stay under `repo/`.
- The first revealed cell and its neighbors must be safe.

## Error Cases

- Revealing a mine ends the game and exposes all mines.
- Revealing all non-mine cells wins the game and flags remaining mines.

## Acceptance

- Opening `index.html` renders a playable 9x9 board.
- First reveal never hits a mine.
- Empty cells flood reveal adjacent empty areas.
- Right click and `F` toggle flags without revealing cells.
- Reset starts a fresh game and clears timer, flags, and status.

## Related Context

- `repo/ARCHITECTURE.md`
- `repo/tasks/TASK-001-build-web-minesweeper.md`
