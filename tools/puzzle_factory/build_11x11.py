from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from tools.puzzle_factory.build import main


if __name__ == "__main__":
    raise SystemExit(main(fixed_size=11))
