from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import hashlib
import logging
from pathlib import Path
from typing import Any

BOARD_SIZE = 11
DIFFICULTIES = ("easy", "medium", "hard")
ACTIVE_BOUNDS_BY_SIZE = {
    5: {"rowStart": 3, "colStart": 3, "size": 5},
    7: {"rowStart": 2, "colStart": 2, "size": 7},
    9: {"rowStart": 1, "colStart": 1, "size": 9},
    11: {"rowStart": 0, "colStart": 0, "size": 11},
}
DEFAULT_TARGETS = {
    5: {"easy": 100, "medium": 100, "hard": 100},
    7: {"easy": 10, "medium": 10, "hard": 10},
    9: {"easy": 10, "medium": 10, "hard": 10},
    11: {"easy": 10, "medium": 10, "hard": 10},
}
REJECT_REASONS = (
    "invalid line",
    "conflicting intersection",
    "no solution",
    "multiple solutions",
    "tray mismatch",
    "too easy",
    "too chaotic",
    "low quality score",
)


@dataclass
class BuildStats:
    generated: int = 0
    accepted: int = 0
    rejected: int = 0
    reject_reasons: Counter[str] = field(default_factory=Counter)

    def reject(self, reason: str) -> None:
        self.generated += 1
        self.rejected += 1
        self.reject_reasons[reason] += 1

    def accept(self) -> None:
        self.generated += 1
        self.accepted += 1

    def summary(self) -> dict[str, Any]:
        return {
            "generated": self.generated,
            "accepted": self.accepted,
            "rejected": self.rejected,
            "rejectReasons": dict(self.reject_reasons),
        }


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_active_bounds(size: int) -> dict[str, int]:
    bounds = ACTIVE_BOUNDS_BY_SIZE.get(size)
    if bounds is None:
        raise ValueError(f"Unsupported logical size: {size}")
    return bounds


def get_cell_id(row: int, col: int) -> str:
    return f"r{row}c{col}"


def stable_seed(*parts: object) -> int:
    payload = "|".join(str(part) for part in parts)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def build_puzzle_id(size: int, difficulty: str, index: int) -> str:
    return f"{size}x{size}-{difficulty}-{index:03d}"


def build_legacy_id(size: int, difficulty: str, index: int) -> str:
    if size == 5:
        return f"{difficulty}-{index:03d}"
    return f"{size}{difficulty[0]}-{index:03d}"


def multiset(values: list[int] | tuple[int, ...]) -> Counter[int]:
    return Counter(values)


def build_tray(solution_values: list[int] | tuple[int, ...], given_indices: list[int] | tuple[int, ...]) -> list[int]:
    given_set = set(given_indices)
    return sorted(
        value for index, value in enumerate(solution_values) if index not in given_set
    )


def configure_logging(level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(levelname)s %(message)s",
    )
    return logging.getLogger("puzzle_factory")

