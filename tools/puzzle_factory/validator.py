from __future__ import annotations

import re

from .solver import apply_operator
from .templates import Template, get_template_by_id
from .utils import REJECT_REASONS, build_tray, multiset

ID_PATTERN = re.compile(r"^(5|7|9|11)x\1-(easy|medium|hard)-\d{3}$")


def validate_solution_board(template: Template, operators: list[str], solution_values: list[int]) -> bool:
    if len(operators) != template.line_count:
        return False
    if len(solution_values) != template.slot_count:
        return False
    for line in template.lines:
        a_index, b_index, c_index = line["slotIndices"]
        if (
            apply_operator(
                operators[line["operatorIndex"]],
                solution_values[a_index],
                solution_values[b_index],
            )
            != solution_values[c_index]
        ):
            return False
    return True


def validate_tray(solution_values: list[int], given_indices: list[int], tray_values: list[int]) -> bool:
    return multiset(build_tray(solution_values, given_indices)) == multiset(tray_values)


def validate_export_entry(entry: dict) -> list[str]:
    issues: list[str] = []
    if not ID_PATTERN.match(entry["id"]):
        issues.append("low quality score")
    template = get_template_by_id(entry["templateId"])
    if not validate_solution_board(template, _extract_operators(entry["puzzle"]), entry["solution"]):
        issues.append("invalid line")
    if not validate_tray(entry["solution"], entry["givenIndices"], entry["tray"]):
        issues.append("tray mismatch")
    given_set = set(entry["givenIndices"])
    for cell in entry["puzzle"]:
        if cell["type"] == "number" and cell["solutionIndex"] not in given_set:
            issues.append("tray mismatch")
            break
        if cell["type"] == "empty" and cell["solutionIndex"] in given_set:
            issues.append("tray mismatch")
            break
    for reason in issues:
        if reason not in REJECT_REASONS:
            raise ValueError(f"Unexpected reject reason: {reason}")
    return issues


def _extract_operators(cells: list[dict]) -> list[str]:
    operators: list[str | None] = []
    for cell in cells:
        if cell["type"] != "operator":
            continue
        operator_index = cell["operatorIndex"]
        while len(operators) <= operator_index:
            operators.append(None)
        operators[operator_index] = cell["value"]
    return [value for value in operators if value is not None]

