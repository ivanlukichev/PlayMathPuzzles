from __future__ import annotations

from dataclasses import dataclass

from .difficulty import DIFFICULTY_RULES, count_immediate_lines, target_given_range
from .templates import Template


@dataclass(frozen=True)
class ScoreResult:
    score: float
    accepted: bool
    reason: str | None
    metrics: dict[str, float | int]


def score_puzzle(
    template: Template,
    difficulty: str,
    operators: list[str],
    tray: list[int],
    given_indices: list[int],
) -> ScoreResult:
    minimum_givens, maximum_givens = target_given_range(template, difficulty)
    given_count = len(given_indices)
    immediate_lines = count_immediate_lines(template, given_indices)
    duplicate_penalty = max((tray.count(value) for value in set(tray)), default=0)
    operator_diversity = len(set(operators))

    score = 100.0
    reason = None

    if given_count < minimum_givens:
        score -= 35
        reason = "too chaotic"
    if given_count > maximum_givens:
        score -= 35
        reason = "too easy"

    limit = DIFFICULTY_RULES[difficulty]["max_line_completions"]
    if limit is not None and immediate_lines > limit:
        score -= 25
        reason = "too easy"

    if difficulty == "easy" and immediate_lines == 0:
        score -= 20
        reason = reason or "too chaotic"

    if difficulty != "easy" and operator_diversity < 2:
        score -= 15

    if difficulty == "easy" and duplicate_penalty > max(3, len(tray) // 2):
        score -= 20
        reason = reason or "too chaotic"
    if difficulty == "hard" and duplicate_penalty < 2 and len(tray) >= 4:
        score -= 10

    if score < 60:
        reason = reason or "low quality score"

    return ScoreResult(
        score=score,
        accepted=score >= 60 and reason not in {"too easy", "too chaotic"} or score >= 70 and reason is None,
        reason=reason,
        metrics={
            "givenCount": given_count,
            "immediateLines": immediate_lines,
            "duplicatePenalty": duplicate_penalty,
            "operatorDiversity": operator_diversity,
        },
    )

