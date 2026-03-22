import {
  DEFAULT_DIFFICULTY,
  DEFAULT_SIZE,
  getFirstPuzzleForCategory,
  getNextPuzzleInCategory,
  getPuzzleById,
} from "./collection.js";
import { initGame } from "./game.js";
import { updatePuzzleMeta } from "./page-meta.js";
import { loadPreferences } from "./persistence.js";
import { parseRoute } from "./routing.js";

async function resolveHomePuzzle() {
  const preferences = loadPreferences();
  const fallbackSize = Number(document.body.dataset.defaultSize || DEFAULT_SIZE);
  const fallbackDifficulty = document.body.dataset.defaultDifficulty || DEFAULT_DIFFICULTY;
  const hasPinnedCategory = Boolean(document.body.dataset.defaultSize);
  const logicalSize = hasPinnedCategory
    ? fallbackSize
    : Number(preferences.logicalSize || fallbackSize);
  const difficulty = hasPinnedCategory
    ? fallbackDifficulty
    : preferences.difficulty || fallbackDifficulty;
  const preferred = await getNextPuzzleInCategory({
    logicalSize,
    difficulty,
  });

  if (preferred) {
    return preferred;
  }

  return getFirstPuzzleForCategory(DEFAULT_SIZE, DEFAULT_DIFFICULTY);
}

async function bootstrap() {
  const parsedRoute = parseRoute();
  const route =
    document.body.dataset.pageMode === "home" && parsedRoute.kind === "unknown"
      ? { kind: "home", puzzleId: null }
      : parsedRoute;

  if (route.kind === "puzzle" && route.puzzleId) {
    const puzzle = await getPuzzleById(route.puzzleId);

    if (puzzle) {
      updatePuzzleMeta(puzzle);
      await initGame({
        routeKind: "puzzle",
        initialPuzzle: puzzle,
      });
      return;
    }
  }

  const homePuzzle = await resolveHomePuzzle();
  await initGame({
    routeKind: "home",
    initialPuzzle: homePuzzle,
    initialStatusText:
      route.kind === "unknown"
        ? "Requested puzzle was not found. Loaded another puzzle from the collection."
        : undefined,
  });
}

bootstrap().catch((error) => {
  console.error(error);
});
