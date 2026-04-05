from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = ROOT / "public"

FILES = [
    "404.html",
    "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    "apple-touch-icon.png",
    "favicon-16x16.png",
    "favicon-32x32.png",
    "index.html",
    "robots.txt",
    "site.webmanifest",
    "sitemap.xml",
]

DIRECTORIES = [
    "11x11",
    "11x11-math-crossword",
    "5x5",
    "5x5-math-crossword",
    "7x7",
    "7x7-math-crossword",
    "9x9",
    "9x9-math-crossword",
    "articles",
    "assets",
    "data",
    "how-to-play-math-crossword",
    "math-crossword-easy",
    "math-crossword-hard",
    "math-crossword-medium",
    "print",
    "printable-math-crossword",
    "puzzle",
    "src",
]


def copy_entry(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def main() -> None:
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    for relative_path in FILES:
        copy_entry(ROOT / relative_path, PUBLIC_DIR / relative_path)

    for relative_path in DIRECTORIES:
        copy_entry(ROOT / relative_path, PUBLIC_DIR / relative_path)


if __name__ == "__main__":
    main()
