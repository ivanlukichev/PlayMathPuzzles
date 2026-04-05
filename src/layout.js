import { BOARD_SIZE, getActiveBounds, getCellId } from "./board.js";
import { getTemplateById } from "./templates.js";

export { BOARD_SIZE, getActiveBounds, getCellId } from "./board.js";

export function createPuzzleLayout(templateId, operators, givensByIndex = {}) {
  const template = getTemplateById(templateId);

  if (!Array.isArray(operators) || operators.length !== template.lineCount) {
    throw new Error(
      `Template ${templateId} needs exactly ${template.lineCount} operators.`,
    );
  }

  return template.cells.map((cell) => {
    if (cell.type === "empty") {
      const givenValue = givensByIndex[cell.solutionIndex];

      if (givenValue !== undefined) {
        return {
          ...cell,
          type: "number",
          value: givenValue,
        };
      }

      return cell;
    }

    if (cell.type === "operator") {
      return {
        ...cell,
        value: operators[cell.operatorIndex],
      };
    }

    return cell;
  });
}

export function createBoardCells(logicalSize, puzzleCells) {
  const bounds = getActiveBounds(logicalSize);
  const cellMap = new Map(puzzleCells.map((cell) => [cell.id, cell]));
  const cells = [];

  for (let row = 0; row < BOARD_SIZE; row += 1) {
    for (let col = 0; col < BOARD_SIZE; col += 1) {
      const id = getCellId(row, col);
      const puzzleCell = cellMap.get(id);

      if (puzzleCell) {
        cells.push(puzzleCell);
        continue;
      }

      const isInsideActiveBounds =
        row >= bounds.rowStart &&
        row < bounds.rowStart + bounds.size &&
        col >= bounds.colStart &&
        col < bounds.colStart + bounds.size;

      cells.push({
        id,
        row,
        col,
        type: isInsideActiveBounds ? "inactive" : "inactive",
      });
    }
  }

  return cells;
}
