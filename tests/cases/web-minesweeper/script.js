const size = 9;
const mineTotal = 10;
const boardEl = document.querySelector("#board");
const mineCountEl = document.querySelector("#mine-count");
const timerEl = document.querySelector("#timer");
const statusEl = document.querySelector("#status");
const resetEl = document.querySelector("#reset");

let cells = [];
let started = false;
let gameOver = false;
let flags = 0;
let opened = 0;
let seconds = 0;
let timerId = null;

function pad(value) {
  return String(value).padStart(3, "0");
}

function indexOf(row, col) {
  return row * size + col;
}

function neighbors(row, col) {
  const result = [];
  for (let dr = -1; dr <= 1; dr += 1) {
    for (let dc = -1; dc <= 1; dc += 1) {
      if (dr === 0 && dc === 0) continue;
      const nr = row + dr;
      const nc = col + dc;
      if (nr >= 0 && nr < size && nc >= 0 && nc < size) {
        result.push(cells[indexOf(nr, nc)]);
      }
    }
  }
  return result;
}

function updateHud() {
  mineCountEl.textContent = pad(mineTotal - flags);
  timerEl.textContent = pad(seconds);
}

function startTimer() {
  if (timerId) return;
  timerId = window.setInterval(() => {
    seconds += 1;
    updateHud();
  }, 1000);
}

function stopTimer() {
  window.clearInterval(timerId);
  timerId = null;
}

function createCells() {
  cells = Array.from({ length: size * size }, (_, id) => ({
    id,
    row: Math.floor(id / size),
    col: id % size,
    mine: false,
    open: false,
    flagged: false,
    adjacent: 0,
  }));
}

function placeMines(safeId) {
  const safe = cells[safeId];
  const blocked = new Set([safeId, ...neighbors(safe.row, safe.col).map((cell) => cell.id)]);
  const candidates = cells.filter((cell) => !blocked.has(cell.id));

  for (let placed = 0; placed < mineTotal; placed += 1) {
    const pick = Math.floor(Math.random() * candidates.length);
    candidates.splice(pick, 1)[0].mine = true;
  }

  cells.forEach((cell) => {
    cell.adjacent = neighbors(cell.row, cell.col).filter((other) => other.mine).length;
  });
}

function render() {
  boardEl.innerHTML = "";
  cells.forEach((cell) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "cell";
    button.dataset.id = String(cell.id);
    button.setAttribute("aria-label", `Row ${cell.row + 1}, column ${cell.col + 1}`);
    button.addEventListener("click", () => reveal(cell.id));
    button.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      toggleFlag(cell.id);
    });
    button.addEventListener("keydown", (event) => {
      if (event.key.toLowerCase() === "f") {
        event.preventDefault();
        toggleFlag(cell.id);
      }
    });
    boardEl.appendChild(button);
  });
  paint();
}

function paint() {
  cells.forEach((cell) => {
    const button = boardEl.querySelector(`[data-id="${cell.id}"]`);
    button.className = "cell";
    button.textContent = "";
    button.disabled = gameOver || cell.open;

    if (cell.open) {
      button.classList.add("open");
      if (cell.mine) {
        button.classList.add("mine");
        button.textContent = "*";
      } else if (cell.adjacent > 0) {
        button.textContent = String(cell.adjacent);
      }
    } else if (cell.flagged) {
      button.classList.add("flagged");
      button.textContent = "F";
    }
  });
  updateHud();
}

function reveal(id) {
  const cell = cells[id];
  if (gameOver || cell.open || cell.flagged) return;

  if (!started) {
    placeMines(id);
    started = true;
    statusEl.textContent = "Game in progress.";
    startTimer();
  }

  cell.open = true;
  opened += 1;

  if (cell.mine) {
    lose();
    return;
  }

  if (cell.adjacent === 0) {
    neighbors(cell.row, cell.col).forEach((other) => reveal(other.id));
  }

  if (opened === size * size - mineTotal) {
    win();
    return;
  }

  paint();
}

function toggleFlag(id) {
  const cell = cells[id];
  if (gameOver || cell.open) return;
  cell.flagged = !cell.flagged;
  flags += cell.flagged ? 1 : -1;
  paint();
}

function lose() {
  gameOver = true;
  stopTimer();
  cells.forEach((cell) => {
    if (cell.mine) cell.open = true;
  });
  statusEl.textContent = "Mine hit. Reset to try again.";
  paint();
}

function win() {
  gameOver = true;
  stopTimer();
  statusEl.textContent = "Cleared. You win.";
  cells.forEach((cell) => {
    if (cell.mine) cell.flagged = true;
  });
  flags = mineTotal;
  paint();
}

function reset() {
  stopTimer();
  started = false;
  gameOver = false;
  flags = 0;
  opened = 0;
  seconds = 0;
  statusEl.textContent = "Reveal a cell to begin.";
  createCells();
  render();
}

resetEl.addEventListener("click", reset);
reset();
