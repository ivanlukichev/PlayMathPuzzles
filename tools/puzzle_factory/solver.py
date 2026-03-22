from __future__ import annotations

from collections import Counter

from .templates import Template


def apply_operator(op: str, a: int, b: int) -> int | None:
    if op == "+":
        return a + b
    if op == "-":
        value = a - b
        return value if value > 0 else None
    if op == "×":
        return a * b
    if op == "÷":
        if b == 0 or a % b != 0:
            return None
        value = a // b
        return value if value > 0 else None
    return None


def derive_missing_value(op: str, values: list[int | None], missing_position: int) -> int | None:
    a, b, c = values
    if missing_position == 2:
        if a is None or b is None:
            return None
        return apply_operator(op, a, b)
    if missing_position == 0:
        if b is None or c is None:
            return None
        if op == "+":
            value = c - b
            return value if value > 0 else None
        if op == "-":
            return c + b
        if op == "×":
            if b == 0 or c % b != 0:
                return None
            value = c // b
            return value if value > 0 else None
        if op == "÷":
            return c * b
    if missing_position == 1:
        if a is None or c is None:
            return None
        if op == "+":
            value = c - a
            return value if value > 0 else None
        if op == "-":
            value = a - c
            return value if value > 0 else None
        if op == "×":
            if a == 0 or c % a != 0:
                return None
            value = c // a
            return value if value > 0 else None
        if op == "÷":
            if c == 0 or a % c != 0:
                return None
            value = a // c
            return value if value > 0 else None
    return None


def count_solutions(
    template: Template,
    operators: list[str] | tuple[str, ...],
    tray_values: list[int] | tuple[int, ...],
    givens_by_index: dict[int, int],
    max_solutions: int = 2,
) -> int:
    lines_by_slot: list[list[dict]] = [[] for _ in range(template.slot_count)]
    for line in template.lines:
        for slot_index in line["slotIndices"]:
            lines_by_slot[slot_index].append(line)

    base_assignments: list[int | None] = [None] * template.slot_count
    for slot_index, value in givens_by_index.items():
        base_assignments[int(slot_index)] = value

    solution_count = 0

    def propagate(assignments: list[int | None], counts: Counter[int]) -> tuple[list[int | None], Counter[int]] | None:
        changed = True
        while changed:
            changed = False
            for line in template.lines:
                values = [assignments[index] for index in line["slotIndices"]]
                missing_positions = [index for index, value in enumerate(values) if value is None]
                if not missing_positions:
                    if apply_operator(operators[line["operatorIndex"]], values[0], values[1]) != values[2]:
                        return None
                    continue
                if len(missing_positions) != 1:
                    continue
                missing_position = missing_positions[0]
                derived_value = derive_missing_value(
                    operators[line["operatorIndex"]],
                    values,
                    missing_position,
                )
                if derived_value is None:
                    return None
                slot_index = line["slotIndices"][missing_position]
                if assignments[slot_index] is not None:
                    if assignments[slot_index] != derived_value:
                        return None
                    continue
                if counts[derived_value] <= 0:
                    return None
                assignments[slot_index] = derived_value
                counts[derived_value] -= 1
                if counts[derived_value] == 0:
                    del counts[derived_value]
                changed = True
        return assignments, counts

    def get_candidates(slot_index: int, assignments: list[int | None], counts: Counter[int]) -> list[int]:
        forced_values = set()
        for line in lines_by_slot[slot_index]:
            values = [assignments[index] for index in line["slotIndices"]]
            missing_positions = [index for index, value in enumerate(values) if value is None]
            if len(missing_positions) != 1:
                continue
            derived_value = derive_missing_value(
                operators[line["operatorIndex"]],
                values,
                missing_positions[0],
            )
            if derived_value is None:
                return []
            forced_values.add(derived_value)
        if len(forced_values) > 1:
            return []
        if len(forced_values) == 1:
            value = next(iter(forced_values))
            return [value] if counts[value] > 0 else []
        return sorted(counts.keys())

    def search(assignments: list[int | None], counts: Counter[int]) -> None:
        nonlocal solution_count
        propagated = propagate(assignments[:], Counter(counts))
        if propagated is None:
            return
        next_assignments, next_counts = propagated
        if all(value is not None for value in next_assignments):
            if not next_counts:
                solution_count += 1
            return

        best_slot_index = None
        best_candidates = None
        for slot_index, value in enumerate(next_assignments):
            if value is not None:
                continue
            candidates = get_candidates(slot_index, next_assignments, next_counts)
            if not candidates:
                return
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_slot_index = slot_index
                best_candidates = candidates

        for candidate in best_candidates or []:
            branch_assignments = next_assignments[:]
            branch_counts = Counter(next_counts)
            branch_assignments[best_slot_index] = candidate
            branch_counts[candidate] -= 1
            if branch_counts[candidate] == 0:
                del branch_counts[candidate]
            search(branch_assignments, branch_counts)
            if solution_count >= max_solutions:
                return

    search(base_assignments, Counter(tray_values))
    return solution_count

