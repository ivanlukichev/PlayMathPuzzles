import {
  DEFAULT_DIFFICULTY,
  getNextPuzzleInCategory,
} from "./collection.js";
import {
  loadRecentPuzzleIds,
  rememberRecentPuzzleId,
  savePreferences,
} from "./persistence.js";
import {
  getPuzzleUrl,
  navigateToPrint,
  visitPuzzle,
} from "./routing.js";
import {
  createEmptyBoardValues,
  formatElapsed,
  getFilledCount,
  getHintCellId,
  getMismatchedCellIds,
  getRemainingCounts,
  isSolved,
} from "./state.js";
import { createUI } from "./ui.js";

const INITIAL_STATUS = "Select a value from the tray and fill the white cells.";

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return true;
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "readonly");
  textarea.style.position = "absolute";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();

  try {
    document.execCommand("copy");
    return true;
  } catch (error) {
    return false;
  } finally {
    textarea.remove();
  }
}

export async function initGame(options = {}) {
  const initialPuzzle = options.initialPuzzle;
  const routeKind = options.routeKind || "home";
  const state = {
    routeKind,
    logicalSize: initialPuzzle.logicalSize,
    difficulty: initialPuzzle.difficulty,
    puzzle: initialPuzzle,
    boardValues: createEmptyBoardValues(initialPuzzle),
    selectedValue: null,
    selectedCellId: null,
    hintedCellIds: [],
    errorCellIds: [],
    placedCellIds: [],
    shakeCellIds: [],
    statusText: options.initialStatusText || INITIAL_STATUS,
    statusTone: "info",
    recentPuzzleIds: loadRecentPuzzleIds(),
    startTimestamp: Date.now(),
    completion: null,
    isPopupOpen: false,
  };

  rememberRecentPuzzleId(
    state.recentPuzzleIds,
    state.logicalSize,
    state.difficulty,
    state.puzzle.id,
  );
  savePreferences({
    logicalSize: state.logicalSize,
    difficulty: state.difficulty,
  });

  const ui = createUI({
    onSizeChange: handleSizeChange,
    onDifficultyChange: handleDifficultyChange,
    onTrayValueSelect: handleTrayValueSelect,
    onCellClick: handleCellClick,
    onCellLongPress: handleCellLongPress,
    onReset: handleReset,
    onHint: handleHint,
    onCheck: handleCheck,
    onNewPuzzle: handleNewPuzzle,
    onPrint: handlePrint,
    onCopyLink: handleCopyLink,
    onPopupNextPuzzle: handlePopupNextPuzzle,
    onPopupPrint: handlePopupPrint,
    onPopupCopyLink: handlePopupCopyLink,
  });

  render();
  window.setInterval(renderTimerOnly, 1000);

  function render() {
    ui.render(state, getRemainingCounts(state.puzzle, state.boardValues), {
      easy: "Easy",
      medium: "Medium",
      hard: "Hard",
    });
  }

  function renderTimerOnly() {
    ui.renderTimer(state);
  }

  function resetBoardForPuzzle() {
    state.boardValues = createEmptyBoardValues(state.puzzle);
    state.selectedValue = null;
    state.selectedCellId = null;
    state.hintedCellIds = [];
    state.errorCellIds = [];
    state.placedCellIds = [];
    state.shakeCellIds = [];
    state.startTimestamp = Date.now();
    state.completion = null;
    state.isPopupOpen = false;
  }

  function completePuzzle() {
    if (state.completion) {
      return;
    }

    state.completion = {
      elapsedMs: Date.now() - state.startTimestamp,
      difficulty: state.difficulty,
      logicalSize: state.logicalSize,
    };
    state.isPopupOpen = true;
    state.errorCellIds = [];
    state.statusText = `Puzzle solved in ${formatElapsed(state.completion.elapsedMs)}.`;
    state.statusTone = "success";
  }

  function clearTransientMarks() {
    state.errorCellIds = [];
  }

  function pulseCells(cellIds) {
    state.placedCellIds = [...cellIds];
    render();

    window.setTimeout(() => {
      state.placedCellIds = [];
      render();
    }, 220);
  }

  function shakeCells(cellIds) {
    state.shakeCellIds = [...cellIds];
    render();

    window.setTimeout(() => {
      state.shakeCellIds = [];
      render();
    }, 360);
  }

  function clearCell(cellId, { preserveSelection = false } = {}) {
    const cell = state.puzzle.cellLookup[cellId];

    if (!cell || cell.type !== "empty" || state.boardValues[cell.slotId] === null) {
      return false;
    }

    state.boardValues[cell.slotId] = null;
    state.hintedCellIds = state.hintedCellIds.filter((id) => id !== cellId);
    state.errorCellIds = state.errorCellIds.filter((id) => id !== cellId);
    state.shakeCellIds = state.shakeCellIds.filter((id) => id !== cellId);
    state.placedCellIds = state.placedCellIds.filter((id) => id !== cellId);
    state.selectedCellId = preserveSelection ? cellId : null;
    state.statusText = "Cell cleared.";
    state.statusTone = "info";
    render();
    return true;
  }

  function applyValueToCell(cellId, value) {
    const cell = state.puzzle.cellLookup[cellId];

    if (!cell || cell.type !== "empty" || value === null || state.completion) {
      return false;
    }

    const remainingCounts = getRemainingCounts(state.puzzle, state.boardValues);
    const currentValue = state.boardValues[cell.slotId];
    const available =
      (remainingCounts[value] || 0) + (currentValue === value ? 1 : 0);

    state.selectedCellId = cellId;

    if (available <= 0) {
      state.statusText = `No ${value} values remain in the tray.`;
      state.statusTone = "warning";
      shakeCells([cellId]);
      render();
      return false;
    }

    state.boardValues[cell.slotId] = value;
    state.hintedCellIds = state.hintedCellIds.filter((id) => id !== cellId);
    state.selectedCellId = null;
    state.shakeCellIds = state.shakeCellIds.filter((id) => id !== cellId);
    clearTransientMarks();

    if (isSolved(state.puzzle, state.boardValues)) {
      completePuzzle();
    } else {
      state.statusText = `${getFilledCount(state.boardValues)} of ${state.puzzle.emptySlotIds.length} cells filled.`;
      state.statusTone = "info";
    }

    render();
    pulseCells([cellId]);
    return true;
  }

  async function visitCategoryPuzzle(nextSize, nextDifficulty, excludeCurrent = true) {
    const currentId =
      excludeCurrent &&
      state.puzzle &&
      state.logicalSize === nextSize &&
      state.difficulty === nextDifficulty
        ? state.puzzle.id
        : null;
    const recentIds = state.recentPuzzleIds[`${nextSize}-${nextDifficulty}`] || [];
    const nextPuzzle = await getNextPuzzleInCategory({
      logicalSize: nextSize,
      difficulty: nextDifficulty,
      recentIds,
      currentId,
    });

    savePreferences({
      logicalSize: nextSize,
      difficulty: nextDifficulty,
    });
    visitPuzzle(nextPuzzle.id);
  }

  function handleSizeChange(nextSize) {
    if (!nextSize || nextSize === state.logicalSize) {
      return;
    }

    visitCategoryPuzzle(nextSize, state.difficulty, false);
  }

  function handleDifficultyChange(nextDifficulty) {
    if (!nextDifficulty) {
      return;
    }

    if (nextDifficulty === state.difficulty && !state.completion) {
      return;
    }

    visitCategoryPuzzle(state.logicalSize, nextDifficulty, true);
  }

  function handleTrayValueSelect(value) {
    if (state.completion) {
      return;
    }

    state.selectedValue = state.selectedValue === value ? null : value;

    if (state.selectedValue === null) {
      state.statusText = "Value selection cleared.";
      state.statusTone = "info";
      render();
      return;
    }

    if (state.selectedCellId) {
      const inserted = applyValueToCell(state.selectedCellId, state.selectedValue);

      if (inserted) {
        state.statusText = `${value} placed. Value stays selected for the next move.`;
        state.statusTone = "info";
        render();
        return;
      }
    }

    state.statusText = `Selected ${value}. Click a white cell to place it.`;
    state.statusTone = "info";
    render();
  }

  function handleCellClick(cellId) {
    if (state.completion) {
      return;
    }

    const cell = state.puzzle.cellLookup[cellId];

    if (!cell || cell.type !== "empty") {
      return;
    }

    if (state.selectedValue !== null) {
      if (state.boardValues[cell.slotId] === state.selectedValue) {
        clearCell(cellId);
        return;
      }

      applyValueToCell(cellId, state.selectedValue);
      return;
    }

    if (state.selectedCellId === cellId) {
      if (!clearCell(cellId)) {
        state.selectedCellId = null;
        state.statusText = "Cell selection cleared.";
        state.statusTone = "info";
        render();
      }
      return;
    }

    state.selectedCellId = cellId;
    state.statusText =
      state.boardValues[cell.slotId] === null
        ? "Cell selected. Choose a value from the tray."
        : "Cell selected. Choose a value or click again to clear it.";
    state.statusTone = "info";
    render();
  }

  function handleCellLongPress(cellId) {
    if (state.completion) {
      return;
    }

    clearCell(cellId);
  }

  function handleReset() {
    resetBoardForPuzzle();
    state.statusText = "Board reset.";
    state.statusTone = "info";
    render();
  }

  function handleHint() {
    if (state.completion) {
      return;
    }

    const hintCellId = getHintCellId(state.puzzle, state.boardValues);

    if (!hintCellId) {
      completePuzzle();
      render();
      return;
    }

    const cell = state.puzzle.cellLookup[hintCellId];
    state.boardValues[cell.slotId] = state.puzzle.solution[cell.slotId];
    state.selectedCellId = hintCellId;
    state.hintedCellIds = [hintCellId];
    state.placedCellIds = [];
    state.shakeCellIds = [];
    clearTransientMarks();

    if (isSolved(state.puzzle, state.boardValues)) {
      completePuzzle();
    } else {
      state.statusText = "Hint revealed one correct value.";
      state.statusTone = "warning";
    }

    render();
  }

  function handleCheck() {
    if (state.completion) {
      return;
    }

    const mismatchedCellIds = getMismatchedCellIds(state.puzzle, state.boardValues, true);

    if (mismatchedCellIds.length === 0) {
      completePuzzle();
      render();
      return;
    }

    state.errorCellIds = mismatchedCellIds;
    state.statusText = `${mismatchedCellIds.length} cells are incomplete or incorrect.`;
    state.statusTone = "error";
    shakeCells(mismatchedCellIds);
    render();
  }

  function handleNewPuzzle() {
    visitCategoryPuzzle(state.logicalSize, state.difficulty, true);
  }

  function handlePrint() {
    navigateToPrint(state.puzzle.id);
  }

  async function handleCopyLink() {
    const copied = await copyText(getPuzzleUrl(state.puzzle.id));
    state.statusText = copied ? "Puzzle link copied." : "Could not copy the puzzle link.";
    state.statusTone = copied ? "success" : "warning";
    render();
  }

  function handlePopupNextPuzzle() {
    visitCategoryPuzzle(state.logicalSize, state.difficulty, true);
  }

  function handlePopupPrint() {
    navigateToPrint(state.puzzle.id);
  }

  async function handlePopupCopyLink() {
    const copied = await copyText(getPuzzleUrl(state.puzzle.id));
    state.statusText = copied ? "Puzzle link copied." : "Could not copy the puzzle link.";
    state.statusTone = copied ? "success" : "warning";
    render();
  }
}
