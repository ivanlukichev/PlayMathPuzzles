import { getPuzzleById } from "./collection.js";
import { initPrintView } from "./print.js";

async function bootstrapPrint() {
  const puzzleId = document.body.dataset.puzzleId;

  if (!puzzleId) {
    window.location.replace("/");
    return;
  }

  const puzzle = await getPuzzleById(puzzleId);

  if (!puzzle) {
    window.location.replace("/");
    return;
  }

  initPrintView(puzzle);
}

bootstrapPrint().catch((error) => {
  console.error(error);
});
