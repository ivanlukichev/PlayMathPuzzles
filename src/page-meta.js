import {
  buildPuzzleDescription,
  buildPuzzleHeading,
  buildPuzzleTitle,
} from "./collection.js";

function titleCase(value) {
  return value ? value[0].toUpperCase() + value.slice(1) : "";
}

export function updatePuzzleMeta(puzzle, mode = "game") {
  const headingNode = document.getElementById("page-heading");
  const subtitleNode = document.getElementById("page-subtitle");
  const titleNode = document.querySelector("title");
  const metaDescription = document.querySelector('meta[name="description"]');
  const collectionValue = document.getElementById("collection-value");
  const sizeValue = document.getElementById("size-value");

  if (titleNode) {
    titleNode.textContent =
      mode === "print"
        ? `${buildPuzzleTitle(puzzle)} Print View`
        : buildPuzzleTitle(puzzle);
  }

  if (metaDescription) {
    metaDescription.setAttribute("content", buildPuzzleDescription(puzzle));
  }

  if (headingNode) {
    headingNode.textContent = buildPuzzleHeading(puzzle);
  }

  if (subtitleNode) {
    subtitleNode.textContent =
      mode === "print"
        ? "Print-friendly view with QR back to the online puzzle."
        : `Puzzle #${puzzle.index}. Fixed library entry with a stable URL, printable view, and shareable link.`;
  }

  if (collectionValue) {
    collectionValue.textContent = titleCase(puzzle.difficulty);
  }

  if (sizeValue) {
    sizeValue.textContent = `${puzzle.logicalSize}x${puzzle.logicalSize}`;
  }
}
