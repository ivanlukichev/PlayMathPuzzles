from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import logging
import random

from .difficulty import generate_given_index_candidates
from .scorer import ScoreResult, score_puzzle
from .solver import apply_operator, count_solutions
from .templates import Template, get_templates_for_size
from .utils import BuildStats, build_tray, get_cell_id
from .validator import validate_export_entry, validate_solution_board

DIFFICULTY_PROFILES = {
    "easy": {
        "ops": ("+", "-"),
        "operand_max": 9,
        "result_max": 12,
    },
    "medium": {
        "ops": ("+", "-", "×", "÷"),
        "operand_max": 12,
        "result_max": 24,
    },
    "hard": {
        "ops": ("+", "-", "×", "÷"),
        "operand_max": 20,
        "result_max": 40,
    },
}


@dataclass(frozen=True)
class EquationCandidate:
    op: str
    values: tuple[int, int, int]


@dataclass(frozen=True)
class GeneratedPuzzle:
    template_id: str
    operators: tuple[str, ...]
    solution_values: tuple[int, ...]
    given_indices: tuple[int, ...]
    tray: tuple[int, ...]
    puzzle: tuple[dict, ...]
    solution_count: int
    score: float
    metrics: dict[str, int | float]


def build_equation_pool(difficulty: str) -> tuple[EquationCandidate, ...]:
    profile = DIFFICULTY_PROFILES[difficulty]
    pool: list[EquationCandidate] = []
    for op in profile["ops"]:
        for a in range(1, profile["operand_max"] + 1):
            for b in range(1, profile["operand_max"] + 1):
                c = apply_operator(op, a, b)
                if c is None or c > profile["result_max"]:
                    continue
                pool.append(EquationCandidate(op=op, values=(a, b, c)))
    return tuple(pool)


def _line_density(template: Template, line: dict) -> int:
    return sum(template.slot_usage[index] for index in line["slotIndices"])


def _line_has_candidate(line: dict, slot_values: list[int | None], pool: tuple[EquationCandidate, ...]) -> bool:
    for candidate in pool:
        if all(
            slot_values[slot_index] in (None, candidate.values[position])
            for position, slot_index in enumerate(line["slotIndices"])
        ):
            return True
    return False


def generate_solved_board(
    template: Template,
    difficulty: str,
    rng: random.Random,
    pool: tuple[EquationCandidate, ...],
) -> tuple[list[str], list[int]] | None:
    ordered_lines = sorted(template.lines, key=lambda line: _line_density(template, line), reverse=True)
    slot_values: list[int | None] = [None] * template.slot_count
    operators: list[str | None] = [None] * template.line_count

    def search(line_position: int) -> bool:
        if line_position == len(ordered_lines):
            return True

        line = ordered_lines[line_position]
        candidates = [
            candidate
            for candidate in pool
            if all(
                slot_values[slot_index] in (None, candidate.values[position])
                for position, slot_index in enumerate(line["slotIndices"])
            )
        ]
        rng.shuffle(candidates)

        for candidate in candidates:
            changed_slots: list[int] = []
            for position, slot_index in enumerate(line["slotIndices"]):
                if slot_values[slot_index] is None:
                    slot_values[slot_index] = candidate.values[position]
                    changed_slots.append(slot_index)
            operators[line["operatorIndex"]] = candidate.op

            valid = True
            for future_line in ordered_lines[line_position + 1 :]:
                if not _line_has_candidate(future_line, slot_values, pool):
                    valid = False
                    break

            if valid and search(line_position + 1):
                return True

            for slot_index in changed_slots:
                slot_values[slot_index] = None
            operators[line["operatorIndex"]] = None

        return False

    if not search(0):
        return None

    final_operators = [value for value in operators if value is not None]
    final_values = [value for value in slot_values if value is not None]
    return final_operators, final_values


def render_puzzle_cells(
    template: Template,
    operators: list[str],
    solution_values: list[int],
    given_indices: list[int],
) -> list[dict]:
    given_set = set(given_indices)
    cells: list[dict] = []
    for cell in template.cells:
        if cell["type"] == "operator":
            cells.append({**cell, "value": operators[cell["operatorIndex"]]})
            continue
        if cell["type"] == "equals":
            cells.append(dict(cell))
            continue
        value = solution_values[cell["solutionIndex"]]
        if cell["solutionIndex"] in given_set:
            cells.append({**cell, "type": "number", "value": value})
        else:
            cells.append(dict(cell))
    return cells


def try_mask_solution(
    template: Template,
    difficulty: str,
    operators: list[str],
    solution_values: list[int],
    rng: random.Random,
) -> tuple[GeneratedPuzzle | None, str | None]:
    last_reason = None
    for given_indices in generate_given_index_candidates(template, difficulty, rng):
        tray = build_tray(solution_values, given_indices)
        givens_by_index = {index: solution_values[index] for index in given_indices}
        solution_count = count_solutions(template, operators, tray, givens_by_index, max_solutions=2)
        if solution_count == 0:
            last_reason = "no solution"
            continue
        if solution_count > 1:
            last_reason = "multiple solutions"
            continue
        score: ScoreResult = score_puzzle(template, difficulty, operators, tray, given_indices)
        if not score.accepted:
            last_reason = score.reason or "low quality score"
            continue
        puzzle = render_puzzle_cells(template, operators, solution_values, given_indices)
        candidate = GeneratedPuzzle(
            template_id=template.id,
            operators=tuple(operators),
            solution_values=tuple(solution_values),
            given_indices=tuple(given_indices),
            tray=tuple(tray),
            puzzle=tuple(puzzle),
            solution_count=solution_count,
            score=score.score,
            metrics=score.metrics,
        )
        return candidate, None
    return None, last_reason or "low quality score"


def generate_single_puzzle(
    size: int,
    difficulty: str,
    rng: random.Random,
    logger: logging.Logger,
    pool: tuple[EquationCandidate, ...] | None = None,
) -> tuple[GeneratedPuzzle | None, str | None]:
    templates = get_templates_for_size(size)
    template = rng.choice(templates)
    logger.debug("template chosen size=%s difficulty=%s template=%s", size, difficulty, template.id)
    pool = pool or build_equation_pool(difficulty)
    solved = generate_solved_board(template, difficulty, rng, pool)
    if solved is None:
        return None, "conflicting intersection"
    operators, solution_values = solved
    if not validate_solution_board(template, operators, solution_values):
        return None, "invalid line"
    candidate, reject_reason = try_mask_solution(template, difficulty, operators, solution_values, rng)
    return candidate, reject_reason


def build_category(
    size: int,
    difficulty: str,
    count: int,
    rng: random.Random,
    logger: logging.Logger,
    max_attempts: int | None = None,
) -> tuple[list[GeneratedPuzzle], BuildStats]:
    pool = build_equation_pool(difficulty)
    stats = BuildStats()
    accepted: list[GeneratedPuzzle] = []
    seen_fingerprints: set[tuple] = set()
    attempt_limit = max_attempts or max(count * 250, 1000)

    while len(accepted) < count and stats.generated < attempt_limit:
        candidate, reject_reason = generate_single_puzzle(size, difficulty, rng, logger, pool=pool)
        if candidate is None:
            reason = reject_reason or "low quality score"
            stats.reject(reason)
            logger.debug("candidate rejected size=%s difficulty=%s reason=%s", size, difficulty, reason)
            continue

        fingerprint = (
            candidate.template_id,
            candidate.operators,
            candidate.solution_values,
            candidate.given_indices,
        )
        if fingerprint in seen_fingerprints:
            stats.reject("low quality score")
            logger.debug("candidate rejected size=%s difficulty=%s reason=duplicate", size, difficulty)
            continue

        seen_fingerprints.add(fingerprint)
        accepted.append(candidate)
        stats.accept()
        logger.info(
            "accepted size=%s difficulty=%s progress=%s/%s template=%s score=%.1f solutions=%s",
            size,
            difficulty,
            len(accepted),
            count,
            candidate.template_id,
            candidate.score,
            candidate.solution_count,
        )

    return accepted, stats

