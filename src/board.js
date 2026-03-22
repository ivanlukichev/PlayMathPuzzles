export const BOARD_SIZE = 11;

export const ACTIVE_BOUNDS_BY_SIZE = Object.freeze({
  5: Object.freeze({ rowStart: 3, colStart: 3, size: 5 }),
  7: Object.freeze({ rowStart: 2, colStart: 2, size: 7 }),
  9: Object.freeze({ rowStart: 1, colStart: 1, size: 9 }),
  11: Object.freeze({ rowStart: 0, colStart: 0, size: 11 }),
});

export function getActiveBounds(logicalSize) {
  const bounds = ACTIVE_BOUNDS_BY_SIZE[logicalSize];

  if (!bounds) {
    throw new Error(`Unsupported logical size: ${logicalSize}`);
  }

  return bounds;
}

export function getCellId(row, col) {
  return `r${row}c${col}`;
}
