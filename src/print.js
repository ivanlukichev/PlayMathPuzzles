import { createBoardCells } from "./layout.js";
import {
  buildPuzzleHeading,
} from "./collection.js";
import { getPuzzleUrl } from "./routing.js";
import { updatePuzzleMeta } from "./page-meta.js";

function buildQrImageUrl(targetUrl) {
  const encoded = encodeURIComponent(targetUrl);
  return `https://api.qrserver.com/v1/create-qr-code/?size=180x180&format=svg&data=${encoded}`;
}

export function initPrintView(puzzle) {
  updatePuzzleMeta(puzzle, "print");

  const titleNode = document.getElementById("print-title");
  const boardNode = document.getElementById("print-board");
  const linkNode = document.getElementById("print-link");
  const qrNode = document.getElementById("print-qr");
  const printButton = document.getElementById("print-page-button");
  const openButton = document.getElementById("open-online-button");
  const onlineUrl = getPuzzleUrl(puzzle.id);

  if (titleNode) {
    titleNode.textContent = buildPuzzleHeading(puzzle);
  }

  if (boardNode) {
    const cells = createBoardCells(puzzle.logicalSize, puzzle.puzzle);
    boardNode.innerHTML = "";

    for (const cell of cells) {
      const node = document.createElement("div");
      node.className = "board-cell";
      node.dataset.type = cell.type === "empty" ? "empty-print" : cell.type;

      if (cell.type === "number" || cell.type === "operator" || cell.type === "equals") {
        node.textContent = cell.value || "";
      } else {
        node.textContent = "";
      }

      boardNode.appendChild(node);
    }
  }

  if (linkNode) {
    linkNode.textContent = onlineUrl.replace(/^https?:\/\//, "");
    linkNode.href = onlineUrl;
  }

  if (qrNode) {
    qrNode.src = buildQrImageUrl(onlineUrl);
    qrNode.alt = `QR code for ${puzzle.id}`;
  }

  if (printButton) {
    printButton.addEventListener("click", () => window.print());
  }

  if (openButton) {
    openButton.href = onlineUrl;
  }
}
