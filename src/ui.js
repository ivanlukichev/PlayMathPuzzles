import { createBoardCells, getCellId } from "./layout.js";
import { formatElapsed } from "./state.js";

export function createUI(handlers) {
  const elements = {
    board: document.getElementById("board"),
    tray: document.getElementById("tray"),
    timer: document.getElementById("timer"),
    status: document.getElementById("status"),
    sizeTabs: Array.from(document.querySelectorAll("[data-size]")),
    difficultyButtons: Array.from(
      document.querySelectorAll("[data-difficulty]"),
    ),
    resetButton: document.getElementById("reset-button"),
    hintButton: document.getElementById("hint-button"),
    checkButton: document.getElementById("check-button"),
    newPuzzleButton: document.getElementById("new-puzzle-button"),
    printButton: document.getElementById("print-button"),
    copyLinkButton: document.getElementById("copy-link-button"),
    popup: document.getElementById("completion-popup"),
    completionSummary: document.getElementById("completion-summary"),
    popupNextButton: document.getElementById("popup-next-button"),
    popupPrintButton: document.getElementById("popup-print-button"),
    popupCopyLinkButton: document.getElementById("popup-copy-link-button"),
  };

  const boardCellNodes = new Map();
  const longPressTimers = new Map();
  let cachedPuzzleId = null;
  let cachedBoardCells = [];

  function clearLongPress(cellId) {
    const timerId = longPressTimers.get(cellId);

    if (timerId) {
      window.clearTimeout(timerId);
      longPressTimers.delete(cellId);
    }
  }

  for (let row = 0; row < 11; row += 1) {
    for (let col = 0; col < 11; col += 1) {
      const cellId = getCellId(row, col);
      const button = document.createElement("button");
      button.type = "button";
      button.className = "board-cell";
      button.dataset.cellId = cellId;
      button.dataset.type = "inactive";
      button.disabled = true;
      button.addEventListener("click", () => handlers.onCellClick(cellId));
      button.addEventListener("pointerdown", () => {
        clearLongPress(cellId);
        const timerId = window.setTimeout(() => {
          handlers.onCellLongPress(cellId);
          clearLongPress(cellId);
        }, 420);
        longPressTimers.set(cellId, timerId);
      });
      button.addEventListener("pointerup", () => clearLongPress(cellId));
      button.addEventListener("pointerleave", () => clearLongPress(cellId));
      button.addEventListener("pointercancel", () => clearLongPress(cellId));
      elements.board.appendChild(button);
      boardCellNodes.set(cellId, button);
    }
  }

  for (const button of elements.difficultyButtons) {
    button.addEventListener("click", () => {
      handlers.onDifficultyChange(button.dataset.difficulty);
    });
  }

  for (const tab of elements.sizeTabs) {
    tab.addEventListener("click", (event) => {
      event.preventDefault();
      handlers.onSizeChange(Number(tab.dataset.size));
    });
  }

  elements.resetButton.addEventListener("click", handlers.onReset);
  elements.hintButton.addEventListener("click", handlers.onHint);
  elements.checkButton.addEventListener("click", handlers.onCheck);
  elements.newPuzzleButton.addEventListener("click", handlers.onNewPuzzle);
  if (elements.printButton) {
    elements.printButton.addEventListener("click", handlers.onPrint);
  }
  if (elements.copyLinkButton) {
    elements.copyLinkButton.addEventListener("click", handlers.onCopyLink);
  }
  elements.popupNextButton.addEventListener("click", handlers.onPopupNextPuzzle);

  if (elements.popupPrintButton) {
    elements.popupPrintButton.addEventListener("click", handlers.onPopupPrint);
  }

  if (elements.popupCopyLinkButton) {
    elements.popupCopyLinkButton.addEventListener("click", handlers.onPopupCopyLink);
  }

  function render(state, remainingCounts, labels) {
    renderSizeTabs(state.logicalSize);
    renderDifficultyButtons(state.difficulty);
    renderBoard(state);
    renderTray(state, remainingCounts);
    renderStatus(state.statusText, state.statusTone);
    renderTimer(state);
    renderPopup(state, labels);
  }

  function renderSizeTabs(currentSize) {
    for (const tab of elements.sizeTabs) {
      const isCurrent = Number(tab.dataset.size) === currentSize;
      tab.classList.toggle("is-current", isCurrent);
      tab.setAttribute("aria-current", isCurrent ? "page" : "false");
    }
  }

  function renderDifficultyButtons(currentDifficulty) {
    for (const button of elements.difficultyButtons) {
      button.setAttribute(
        "aria-pressed",
        button.dataset.difficulty === currentDifficulty ? "true" : "false",
      );
    }
  }

  function renderBoard(state) {
    if (cachedPuzzleId !== state.puzzle.id) {
      cachedPuzzleId = state.puzzle.id;
      cachedBoardCells = createBoardCells(state.puzzle.logicalSize, state.puzzle.puzzle);
    }

    const errorIds = new Set(state.errorCellIds);
    const hintedIds = new Set(state.hintedCellIds);
    const placedIds = new Set(state.placedCellIds);
    const shakingIds = new Set(state.shakeCellIds);
    const solved = Boolean(state.completion);

    for (const cell of cachedBoardCells) {
      const node = boardCellNodes.get(cell.id);
      node.className = "board-cell";
      node.dataset.type = cell.type;

      if (cell.type === "empty") {
        const currentValue = state.boardValues[cell.slotId];
        node.textContent = currentValue === null ? "?" : String(currentValue);
        node.disabled = solved;
        node.setAttribute("aria-label", `Cell ${cell.slotId}`);

        if (currentValue === null) {
          node.classList.add("is-placeholder");
        }

        if (state.selectedCellId === cell.id) {
          node.classList.add("is-selected");
        }

        if (currentValue !== null) {
          node.classList.add("is-filled");
        }

        if (state.selectedValue !== null && currentValue === state.selectedValue) {
          node.classList.add("is-value-match");
        }

        if (hintedIds.has(cell.id)) {
          node.classList.add("is-hinted");
        }

        if (errorIds.has(cell.id)) {
          node.classList.add("is-error");
        }

        if (placedIds.has(cell.id)) {
          node.classList.add("is-placed");
        }

        if (shakingIds.has(cell.id)) {
          node.classList.add("is-shaking");
        }

        if (solved) {
          node.classList.add("is-solved");
        }

        continue;
      }

      node.textContent = cell.value || "";
      node.disabled = true;
      if (state.selectedValue !== null && cell.value === state.selectedValue) {
        node.classList.add("is-value-match");
      }
      node.setAttribute("aria-label", cell.type === "number" ? `Given ${cell.value}` : cell.value || "");
    }
  }

  function renderTray(state, remainingCounts) {
    const totals = Object.create(null);
    const uniqueValues = [];

    for (const value of state.puzzle.trayValues) {
      if (!(value in totals)) {
        totals[value] = 0;
        uniqueValues.push(value);
      }

      totals[value] += 1;
    }

    elements.tray.innerHTML = "";

    for (const value of uniqueValues) {
      const remaining = remainingCounts[value] || 0;
      const button = document.createElement("button");
      button.type = "button";
      button.className = "tray-button";
      button.textContent = String(value);
      button.disabled = state.completion ? true : remaining === 0;

      if (state.selectedValue === value) {
        button.classList.add("is-selected");
      }

      if (state.selectedValue !== null && value === state.selectedValue) {
        button.classList.add("is-value-match");
      }

      button.addEventListener("click", () => handlers.onTrayValueSelect(value));

      const count = document.createElement("span");
      count.className = "tray-count";
      count.textContent = `${remaining}/${totals[value]}`;
      button.appendChild(count);

      elements.tray.appendChild(button);
    }
  }

  function renderStatus(text, tone) {
    elements.status.textContent = text;
    elements.status.dataset.tone = tone;
  }

  function renderTimer(state) {
    const elapsed = state.completion
      ? state.completion.elapsedMs
      : Date.now() - state.startTimestamp;
    elements.timer.textContent = formatElapsed(elapsed);
  }

  function renderPopup(state, labels) {
    elements.popup.hidden = !state.isPopupOpen;

    if (!state.completion) {
      return;
    }

    elements.completionSummary.textContent = `Time: ${formatElapsed(state.completion.elapsedMs)}. Size: ${state.logicalSize}x${state.logicalSize}. Difficulty: ${labels[state.completion.difficulty]}.`;
  }

  function focusCurrentDifficulty(currentDifficulty) {
    const button = elements.difficultyButtons.find(
      (item) => item.dataset.difficulty === currentDifficulty,
    );

    if (button) {
      button.focus();
    }
  }

  return {
    render,
    renderTimer,
    focusCurrentDifficulty,
  };
}
