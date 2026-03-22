export function createRecentPuzzleMemory() {
  return {
    easy: [],
    medium: [],
    hard: [],
  };
}

export function rememberPuzzleId(recentPuzzleIds, difficulty, puzzleId, limit = 5) {
  const next = recentPuzzleIds[difficulty].filter((id) => id !== puzzleId);
  next.unshift(puzzleId);
  recentPuzzleIds[difficulty] = next.slice(0, limit);
  return recentPuzzleIds;
}

export function createEmptyBoardValues(puzzle) {
  return Object.fromEntries(puzzle.emptySlotIds.map((slotId) => [slotId, null]));
}

export function getRemainingCounts(puzzle, boardValues) {
  const remaining = Object.create(null);

  for (const value of puzzle.trayValues) {
    remaining[value] = (remaining[value] || 0) + 1;
  }

  for (const value of Object.values(boardValues)) {
    if (value === null) {
      continue;
    }

    remaining[value] -= 1;
  }

  return remaining;
}

export function getFilledCount(boardValues) {
  return Object.values(boardValues).filter((value) => value !== null).length;
}

export function isSolved(puzzle, boardValues) {
  return puzzle.emptySlotIds.every(
    (slotId) => boardValues[slotId] === puzzle.solution[slotId],
  );
}

export function getMismatchedCellIds(puzzle, boardValues, includeEmpty = true) {
  return puzzle.emptySlotIds
    .filter((slotId) => {
      const current = boardValues[slotId];

      if (current === null) {
        return includeEmpty;
      }

      return current !== puzzle.solution[slotId];
    })
    .map((slotId) => puzzle.slotToCellId[slotId]);
}

export function getHintCellId(puzzle, boardValues, randomFn = Math.random) {
  const mismatchedSlotIds = puzzle.emptySlotIds.filter(
    (slotId) => boardValues[slotId] !== puzzle.solution[slotId],
  );

  if (mismatchedSlotIds.length === 0) {
    return null;
  }

  const index = Math.floor(randomFn() * mismatchedSlotIds.length);
  const slotId = mismatchedSlotIds[index];
  return puzzle.slotToCellId[slotId];
}

export function formatElapsed(milliseconds) {
  const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  if (hours > 0) {
    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
  }

  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}
