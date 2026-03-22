const HOME_PATH = "/";

export function getPuzzlePath(id) {
  return `/puzzle/${encodeURIComponent(id)}/`;
}

export function getPrintPath(id) {
  return `/print/${encodeURIComponent(id)}/`;
}

export function getPuzzleUrl(id) {
  return new URL(getPuzzlePath(id), window.location.origin).toString();
}

export function parseRoute(pathname = window.location.pathname) {
  const normalized = pathname.endsWith("/") ? pathname : `${pathname}/`;
  const printMatch = normalized.match(/^\/print\/([^/]+)\/$/);

  if (printMatch) {
    return {
      kind: "print",
      puzzleId: decodeURIComponent(printMatch[1]),
    };
  }

  const puzzleMatch = normalized.match(/^\/puzzle\/([^/]+)\/$/);

  if (puzzleMatch) {
    return {
      kind: "puzzle",
      puzzleId: decodeURIComponent(puzzleMatch[1]),
    };
  }

  return {
    kind: normalized === HOME_PATH ? "home" : "unknown",
    puzzleId: null,
  };
}

export function visitPuzzle(id) {
  window.location.assign(getPuzzlePath(id));
}

export function navigateToPrint(id) {
  window.open(getPrintPath(id), "_blank", "noopener,noreferrer");
}
