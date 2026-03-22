const PREFERENCES_KEY = "math-crossword.preferences.v1";
const RECENT_PUZZLES_KEY = "math-crossword.recent-puzzles.v1";

function getStorage() {
  try {
    return window.localStorage;
  } catch (error) {
    return null;
  }
}

function readJson(key, fallback) {
  const storage = getStorage();

  if (!storage) {
    return fallback;
  }

  try {
    const raw = storage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch (error) {
    return fallback;
  }
}

function writeJson(key, value) {
  const storage = getStorage();

  if (!storage) {
    return;
  }

  try {
    storage.setItem(key, JSON.stringify(value));
  } catch (error) {
    // Ignore storage failures to keep gameplay stable.
  }
}

export function loadPreferences() {
  return readJson(PREFERENCES_KEY, {});
}

export function savePreferences({ logicalSize, difficulty }) {
  writeJson(PREFERENCES_KEY, {
    logicalSize,
    difficulty,
  });
}

function createRecentShape() {
  return {
    "5-easy": [],
    "5-medium": [],
    "5-hard": [],
    "7-easy": [],
    "7-medium": [],
    "7-hard": [],
    "9-easy": [],
    "9-medium": [],
    "9-hard": [],
    "11-easy": [],
    "11-medium": [],
    "11-hard": [],
  };
}

export function loadRecentPuzzleIds() {
  const recent = readJson(RECENT_PUZZLES_KEY, createRecentShape());
  return {
    ...createRecentShape(),
    ...recent,
  };
}

export function rememberRecentPuzzleId(recentPuzzleIds, logicalSize, difficulty, puzzleId, limit = 6) {
  const key = `${logicalSize}-${difficulty}`;
  const next = (recentPuzzleIds[key] || []).filter((id) => id !== puzzleId);
  next.unshift(puzzleId);
  recentPuzzleIds[key] = next.slice(0, limit);
  writeJson(RECENT_PUZZLES_KEY, recentPuzzleIds);
  return recentPuzzleIds;
}
