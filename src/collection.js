import { getActiveBounds } from "./board.js";

export const DEFAULT_SIZE = 5;
export const DEFAULT_DIFFICULTY = "medium";

export const COLLECTION_TARGETS = Object.freeze({
  5: Object.freeze({ easy: 100, medium: 100, hard: 100 }),
  7: Object.freeze({ easy: 10, medium: 10, hard: 10 }),
  9: Object.freeze({ easy: 10, medium: 10, hard: 10 }),
  11: Object.freeze({ easy: 10, medium: 10, hard: 10 }),
});

const COLLECTION_URL = "/data/puzzles.json";
let collectionPromise = null;

function createPuzzleRuntime(entry) {
  const solution = Object.create(null);
  const slotToCellId = Object.create(null);
  const cellLookup = Object.create(null);
  const givenValues = Object.create(null);
  const givensByIndex = Object.create(null);
  const ops = [];
  const emptySlotIds = [];
  const givenSlotIds = [];

  for (const index of entry.givenIndices) {
    givensByIndex[index] = entry.solution[index];
  }

  for (const cell of entry.puzzle) {
    cellLookup[cell.id] = cell;

    if (cell.type === "operator") {
      ops[cell.operatorIndex] = cell.value;
      continue;
    }

    if (cell.slotId) {
      slotToCellId[cell.slotId] = cell.id;
      solution[cell.slotId] = entry.solution[cell.solutionIndex];
    }

    if (cell.type === "empty") {
      emptySlotIds.push(cell.slotId);
      continue;
    }

    if (cell.type === "number") {
      givenSlotIds.push(cell.slotId);
      givenValues[cell.slotId] = cell.value;
    }
  }

  return Object.freeze({
    id: entry.id,
    legacyId: entry.legacyId,
    logicalSize: entry.size,
    size: entry.size,
    difficulty: entry.difficulty,
    index: entry.index,
    activeBounds: getActiveBounds(entry.size),
    puzzle: Object.freeze(entry.puzzle.map((cell) => Object.freeze({ ...cell }))),
    solutionOrder: Object.freeze([...entry.solution]),
    solution: Object.freeze({ ...solution }),
    trayValues: Object.freeze([...entry.tray]),
    tray: Object.freeze([...entry.tray]),
    templateId: entry.templateId,
    givenIndices: Object.freeze([...entry.givenIndices]),
    givensByIndex: Object.freeze({ ...givensByIndex }),
    givenValues: Object.freeze({ ...givenValues }),
    emptySlotIds: Object.freeze([...emptySlotIds]),
    givenSlotIds: Object.freeze([...givenSlotIds]),
    slotToCellId: Object.freeze({ ...slotToCellId }),
    cellLookup: Object.freeze({ ...cellLookup }),
    ops: Object.freeze([...ops]),
    categoryKey: `${entry.size}-${entry.difficulty}`,
  });
}

function buildCollectionIndex(entries) {
  const puzzles = entries.map(createPuzzleRuntime);
  const byId = Object.create(null);
  const bySizeAndDifficulty = {
    5: { easy: [], medium: [], hard: [] },
    7: { easy: [], medium: [], hard: [] },
    9: { easy: [], medium: [], hard: [] },
    11: { easy: [], medium: [], hard: [] },
  };

  for (const puzzle of puzzles) {
    byId[puzzle.id] = puzzle;
    bySizeAndDifficulty[puzzle.logicalSize][puzzle.difficulty].push(puzzle);
  }

  for (const size of Object.keys(bySizeAndDifficulty)) {
    for (const difficulty of Object.keys(bySizeAndDifficulty[size])) {
      bySizeAndDifficulty[size][difficulty].sort((left, right) => left.index - right.index);
      bySizeAndDifficulty[size][difficulty] = Object.freeze(bySizeAndDifficulty[size][difficulty]);
    }

    bySizeAndDifficulty[size] = Object.freeze(bySizeAndDifficulty[size]);
  }

  return Object.freeze({
    puzzles: Object.freeze(puzzles),
    byId: Object.freeze(byId),
    bySizeAndDifficulty: Object.freeze(bySizeAndDifficulty),
  });
}

export async function loadCollection() {
  if (!collectionPromise) {
    collectionPromise = fetch(COLLECTION_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to load puzzle collection: ${response.status}`);
        }

        return response.json();
      })
      .then(buildCollectionIndex);
  }

  return collectionPromise;
}

export async function getPuzzleById(id) {
  const collection = await loadCollection();
  return collection.byId[id] || null;
}

export async function getPuzzlesByCategory(logicalSize, difficulty) {
  const collection = await loadCollection();
  return collection.bySizeAndDifficulty[logicalSize]?.[difficulty] || [];
}

export async function getCollectionCounts() {
  const collection = await loadCollection();
  const counts = {
    5: { easy: 0, medium: 0, hard: 0 },
    7: { easy: 0, medium: 0, hard: 0 },
    9: { easy: 0, medium: 0, hard: 0 },
    11: { easy: 0, medium: 0, hard: 0 },
  };

  for (const puzzle of collection.puzzles) {
    counts[puzzle.logicalSize][puzzle.difficulty] += 1;
  }

  return counts;
}

export async function getFirstPuzzleForCategory(logicalSize, difficulty) {
  const puzzles = await getPuzzlesByCategory(logicalSize, difficulty);
  return puzzles[0] || null;
}

export async function getNextPuzzleInCategory({
  logicalSize,
  difficulty,
  recentIds = [],
  currentId = null,
}) {
  const pool = await getPuzzlesByCategory(logicalSize, difficulty);

  if (!pool.length) {
    throw new Error(
      `No puzzles found for size ${logicalSize} and difficulty ${difficulty}.`,
    );
  }

  const recentSet = new Set(recentIds);
  let candidates = pool.filter(
    (puzzle) => puzzle.id !== currentId && !recentSet.has(puzzle.id),
  );

  if (!candidates.length) {
    candidates = pool.filter((puzzle) => puzzle.id !== currentId);
  }

  if (!candidates.length) {
    candidates = pool;
  }

  const index = Math.floor(Math.random() * candidates.length);
  return candidates[index];
}

export function buildPuzzleHeading(puzzle) {
  const label = puzzle.difficulty[0].toUpperCase() + puzzle.difficulty.slice(1);
  return `${puzzle.logicalSize}x${puzzle.logicalSize} ${label} Math Crossword`;
}

export function buildPuzzleTitle(puzzle) {
  const label = puzzle.difficulty[0].toUpperCase() + puzzle.difficulty.slice(1);
  return `Math Crossword ${puzzle.logicalSize}x${puzzle.logicalSize} ${label} Puzzle #${puzzle.index}`;
}

export function buildPuzzleDescription(puzzle) {
  return `Play a ${puzzle.logicalSize}x${puzzle.logicalSize} ${puzzle.difficulty} math crossword puzzle online.`;
}
