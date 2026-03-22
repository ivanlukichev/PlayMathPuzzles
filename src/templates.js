import { BOARD_SIZE, getActiveBounds, getCellId } from "./board.js";

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function lineToCells(line) {
  if (line.direction === "across") {
    return [
      { row: line.row, col: line.col, role: "a", type: "empty" },
      { row: line.row, col: line.col + 1, role: "operator", type: "operator" },
      { row: line.row, col: line.col + 2, role: "b", type: "empty" },
      { row: line.row, col: line.col + 3, role: "equals", type: "equals" },
      { row: line.row, col: line.col + 4, role: "c", type: "empty" },
    ];
  }

  if (line.direction === "down") {
    return [
      { row: line.row, col: line.col, role: "a", type: "empty" },
      { row: line.row + 1, col: line.col, role: "operator", type: "operator" },
      { row: line.row + 2, col: line.col, role: "b", type: "empty" },
      { row: line.row + 3, col: line.col, role: "equals", type: "equals" },
      { row: line.row + 4, col: line.col, role: "c", type: "empty" },
    ];
  }

  throw new Error(`Unsupported line direction: ${line.direction}`);
}

function buildTemplate(definition) {
  const bounds = getActiveBounds(definition.logicalSize);
  const cellMap = new Map();
  const slotIndexByCellId = new Map();
  const slotUsage = new Map();
  const lineEntries = [];
  let nextSlotIndex = 0;
  let nextOperatorIndex = 0;

  for (const line of definition.lines) {
    const lineCells = lineToCells(line);
    const slotIndices = [];
    const operatorIndices = [];

    for (const cell of lineCells) {
      assert(
        cell.row >= bounds.rowStart &&
          cell.row < bounds.rowStart + bounds.size &&
          cell.col >= bounds.colStart &&
          cell.col < bounds.colStart + bounds.size,
        `Template ${definition.id} has a cell outside its active bounds.`,
      );
      assert(
        cell.row >= 0 &&
          cell.row < BOARD_SIZE &&
          cell.col >= 0 &&
          cell.col < BOARD_SIZE,
        `Template ${definition.id} has a cell outside the 11x11 board.`,
      );

      const cellId = getCellId(cell.row, cell.col);
      const existing = cellMap.get(cellId);

      if (cell.type === "empty") {
        if (!slotIndexByCellId.has(cellId)) {
          slotIndexByCellId.set(cellId, nextSlotIndex);
          slotUsage.set(nextSlotIndex, 0);
          nextSlotIndex += 1;
        }

        const slotIndex = slotIndexByCellId.get(cellId);
        slotUsage.set(slotIndex, slotUsage.get(slotIndex) + 1);
        slotIndices.push(slotIndex);
        cellMap.set(cellId, {
          id: cellId,
          row: cell.row,
          col: cell.col,
          type: "empty",
          slotId: `slot-${slotIndex}`,
          solutionIndex: slotIndex,
        });
        continue;
      }

      if (existing) {
        assert(
          existing.type === cell.type,
          `Template ${definition.id} has a conflicting cell overlap at ${cellId}.`,
        );
      }

      if (cell.type === "operator") {
        operatorIndices.push(nextOperatorIndex);
        cellMap.set(cellId, {
          id: cellId,
          row: cell.row,
          col: cell.col,
          type: "operator",
          operatorIndex: nextOperatorIndex,
        });
        nextOperatorIndex += 1;
        continue;
      }

      cellMap.set(cellId, {
        id: cellId,
        row: cell.row,
        col: cell.col,
        type: "equals",
        value: "=",
      });
    }

    assert(
      slotIndices.length === 3,
      `Template ${definition.id} line ${line.id} must contain 3 numeric cells.`,
    );
    assert(
      operatorIndices.length === 1,
      `Template ${definition.id} line ${line.id} must contain 1 operator cell.`,
    );

    lineEntries.push({
      id: line.id,
      direction: line.direction,
      slotIndices: Object.freeze(slotIndices),
      operatorIndex: operatorIndices[0],
    });
  }

  const slotEntries = Array.from(slotUsage.entries()).sort((left, right) => left[0] - right[0]);
  const slotCount = slotEntries.length;
  const resultSlotIndices = lineEntries.map((line) => line.slotIndices[2]);
  const intersectionSlotIndices = slotEntries
    .filter(([, usageCount]) => usageCount > 1)
    .map(([slotIndex]) => slotIndex);

  return Object.freeze({
    id: definition.id,
    logicalSize: definition.logicalSize,
    activeBounds: bounds,
    lineCount: lineEntries.length,
    slotCount,
    cells: Object.freeze(
      Array.from(cellMap.values()).sort((left, right) => {
        if (left.row !== right.row) {
          return left.row - right.row;
        }

        return left.col - right.col;
      }),
    ),
    lines: Object.freeze(lineEntries),
    slotUsage: Object.freeze(Object.fromEntries(slotEntries)),
    resultSlotIndices: Object.freeze(resultSlotIndices),
    intersectionSlotIndices: Object.freeze(intersectionSlotIndices),
    keySlotIndices: Object.freeze(
      Array.from(new Set([...resultSlotIndices, ...intersectionSlotIndices])).sort(
        (left, right) => left - right,
      ),
    ),
  });
}

const TEMPLATE_DEFINITIONS = Object.freeze([
  {
    id: "5x5-classic",
    logicalSize: 5,
    lines: [
      { id: "h-0", direction: "across", row: 3, col: 3 },
      { id: "h-1", direction: "across", row: 5, col: 3 },
      { id: "h-2", direction: "across", row: 7, col: 3 },
      { id: "v-0", direction: "down", row: 3, col: 3 },
      { id: "v-1", direction: "down", row: 3, col: 5 },
      { id: "v-2", direction: "down", row: 3, col: 7 },
    ],
  },
  {
    id: "7x7-stagger-a",
    logicalSize: 7,
    lines: [
      { id: "h-0", direction: "across", row: 2, col: 2 },
      { id: "h-1", direction: "across", row: 4, col: 2 },
      { id: "h-2", direction: "across", row: 6, col: 4 },
      { id: "h-3", direction: "across", row: 8, col: 4 },
      { id: "v-0", direction: "down", row: 2, col: 2 },
      { id: "v-1", direction: "down", row: 2, col: 4 },
      { id: "v-2", direction: "down", row: 4, col: 6 },
      { id: "v-3", direction: "down", row: 4, col: 8 },
    ],
  },
  {
    id: "7x7-stagger-b",
    logicalSize: 7,
    lines: [
      { id: "h-0", direction: "across", row: 2, col: 4 },
      { id: "h-1", direction: "across", row: 4, col: 2 },
      { id: "h-2", direction: "across", row: 6, col: 4 },
      { id: "h-3", direction: "across", row: 8, col: 2 },
      { id: "v-0", direction: "down", row: 4, col: 2 },
      { id: "v-1", direction: "down", row: 2, col: 4 },
      { id: "v-2", direction: "down", row: 2, col: 6 },
      { id: "v-3", direction: "down", row: 4, col: 8 },
    ],
  },
  {
    id: "9x9-stagger-a",
    logicalSize: 9,
    lines: [
      { id: "h-0", direction: "across", row: 1, col: 1 },
      { id: "h-1", direction: "across", row: 3, col: 3 },
      { id: "h-2", direction: "across", row: 5, col: 1 },
      { id: "h-3", direction: "across", row: 7, col: 3 },
      { id: "h-4", direction: "across", row: 9, col: 5 },
      { id: "v-0", direction: "down", row: 1, col: 1 },
      { id: "v-1", direction: "down", row: 1, col: 3 },
      { id: "v-2", direction: "down", row: 3, col: 5 },
      { id: "v-3", direction: "down", row: 5, col: 7 },
      { id: "v-4", direction: "down", row: 5, col: 9 },
    ],
  },
  {
    id: "9x9-stagger-b",
    logicalSize: 9,
    lines: [
      { id: "h-0", direction: "across", row: 1, col: 5 },
      { id: "h-1", direction: "across", row: 3, col: 3 },
      { id: "h-2", direction: "across", row: 5, col: 1 },
      { id: "h-3", direction: "across", row: 7, col: 3 },
      { id: "h-4", direction: "across", row: 9, col: 1 },
      { id: "v-0", direction: "down", row: 5, col: 1 },
      { id: "v-1", direction: "down", row: 3, col: 3 },
      { id: "v-2", direction: "down", row: 1, col: 5 },
      { id: "v-3", direction: "down", row: 3, col: 7 },
      { id: "v-4", direction: "down", row: 5, col: 9 },
    ],
  },
  {
    id: "11x11-weave-a",
    logicalSize: 11,
    lines: [
      { id: "h-0", direction: "across", row: 0, col: 0 },
      { id: "h-1", direction: "across", row: 2, col: 2 },
      { id: "h-2", direction: "across", row: 4, col: 0 },
      { id: "h-3", direction: "across", row: 6, col: 2 },
      { id: "h-4", direction: "across", row: 8, col: 4 },
      { id: "h-5", direction: "across", row: 10, col: 6 },
      { id: "v-0", direction: "down", row: 0, col: 0 },
      { id: "v-1", direction: "down", row: 0, col: 2 },
      { id: "v-2", direction: "down", row: 2, col: 4 },
      { id: "v-3", direction: "down", row: 4, col: 6 },
      { id: "v-4", direction: "down", row: 6, col: 8 },
      { id: "v-5", direction: "down", row: 6, col: 10 },
    ],
  },
  {
    id: "11x11-weave-b",
    logicalSize: 11,
    lines: [
      { id: "h-0", direction: "across", row: 0, col: 6 },
      { id: "h-1", direction: "across", row: 2, col: 4 },
      { id: "h-2", direction: "across", row: 4, col: 2 },
      { id: "h-3", direction: "across", row: 6, col: 0 },
      { id: "h-4", direction: "across", row: 8, col: 2 },
      { id: "h-5", direction: "across", row: 10, col: 4 },
      { id: "v-0", direction: "down", row: 6, col: 0 },
      { id: "v-1", direction: "down", row: 4, col: 2 },
      { id: "v-2", direction: "down", row: 2, col: 4 },
      { id: "v-3", direction: "down", row: 0, col: 6 },
      { id: "v-4", direction: "down", row: 2, col: 8 },
      { id: "v-5", direction: "down", row: 4, col: 10 },
    ],
  },
]);

export const PUZZLE_TEMPLATES = Object.freeze(TEMPLATE_DEFINITIONS.map(buildTemplate));

export const PUZZLE_TEMPLATES_BY_ID = Object.freeze(
  Object.fromEntries(PUZZLE_TEMPLATES.map((template) => [template.id, template])),
);

export const PUZZLE_TEMPLATES_BY_SIZE = Object.freeze({
  5: Object.freeze(PUZZLE_TEMPLATES.filter((template) => template.logicalSize === 5)),
  7: Object.freeze(PUZZLE_TEMPLATES.filter((template) => template.logicalSize === 7)),
  9: Object.freeze(PUZZLE_TEMPLATES.filter((template) => template.logicalSize === 9)),
  11: Object.freeze(PUZZLE_TEMPLATES.filter((template) => template.logicalSize === 11)),
});

export function getTemplateById(templateId) {
  const template = PUZZLE_TEMPLATES_BY_ID[templateId];

  if (!template) {
    throw new Error(`Unknown puzzle template: ${templateId}`);
  }

  return template;
}

export function getTemplatesForSize(logicalSize) {
  const templates = PUZZLE_TEMPLATES_BY_SIZE[logicalSize];

  if (!templates) {
    throw new Error(`No template set found for size ${logicalSize}.`);
  }

  return templates;
}
