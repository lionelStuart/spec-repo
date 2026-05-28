# Web Minesweeper Case

This fixture validates that `project-system` can initialize and guide a small browser game project without moving normal implementation files into `repo/`.

## Scenario

Create a static web Minesweeper game with:

- first-click-safe mine placement
- reveal and flag interactions
- mine counter, timer, reset, win, and loss states
- keyboard-accessible board cells

## Expected Project-System Behavior

- Root `AGENTS.md` governs the project.
- Project memory lives under `repo/`.
- Web implementation files remain at the project root.
- Recently completed work remains in `repo/specs/` and `repo/tasks/` for continuity after write-back.
- `repo/STATUS.md`, `repo/INDEX.md`, and `repo/archive/MANIFEST.md` reflect the completed but recently retained task.
