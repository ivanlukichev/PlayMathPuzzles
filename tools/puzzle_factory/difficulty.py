from __future__ import annotations

import random

from .templates import Template

DIFFICULTY_RULES = {
    "easy": {
        "ratio": (0.40, 0.50),
        "preferred_key_share": 0.75,
        "max_line_completions": None,
    },
    "medium": {
        "ratio": (0.20, 0.30),
        "preferred_key_share": 0.6,
        "max_line_completions": 2,
    },
    "hard": {
        "ratio": (0.0, 0.10),
        "preferred_key_share": 0.5,
        "max_line_completions": 0,
    },
}


def target_given_range(template: Template, difficulty: str) -> tuple[int, int]:
    rule = DIFFICULTY_RULES[difficulty]
    slot_count = template.slot_count
    minimum = max(0, round(slot_count * rule["ratio"][0]))
    maximum = round(slot_count * rule["ratio"][1])
    if difficulty == "hard":
        maximum = max(minimum, min(maximum, 1 if slot_count <= 9 else 2))
    return minimum, min(slot_count, maximum)


def generate_given_index_candidates(
    template: Template,
    difficulty: str,
    rng: random.Random,
    samples: int = 48,
) -> list[list[int]]:
    minimum, maximum = target_given_range(template, difficulty)
    key_slots = list(template.key_slot_indices)
    result_slots = list(dict.fromkeys(template.result_slot_indices))
    other_slots = [index for index in range(template.slot_count) if index not in key_slots]
    candidates: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()

    for _ in range(samples):
        target_count = rng.randint(minimum, maximum) if maximum >= minimum else minimum
        chosen: list[int] = []
        key_pool = key_slots[:]
        result_pool = result_slots[:]
        other_pool = other_slots[:]
        rng.shuffle(key_pool)
        rng.shuffle(result_pool)
        rng.shuffle(other_pool)

        if difficulty == "easy":
            while result_pool and len(chosen) < min(target_count, max(1, len(result_slots))):
                chosen.append(result_pool.pop())
            while key_pool and len(chosen) < target_count:
                value = key_pool.pop()
                if value not in chosen:
                    chosen.append(value)
        elif difficulty == "medium":
            if key_pool and target_count > 0:
                chosen.append(key_pool.pop())
            if result_pool and len(chosen) < target_count and rng.random() < 0.5:
                value = result_pool.pop()
                if value not in chosen:
                    chosen.append(value)
        elif difficulty == "hard" and target_count > 0 and key_pool and rng.random() < 0.7:
            chosen.append(key_pool.pop())

        combined_pool = key_pool + other_pool
        rng.shuffle(combined_pool)
        for slot_index in combined_pool:
            if len(chosen) >= target_count:
                break
            if slot_index not in chosen:
                chosen.append(slot_index)

        normalized = tuple(sorted(chosen))
        if normalized not in seen:
            seen.add(normalized)
            candidates.append(list(normalized))

    if [] not in candidates and minimum == 0:
        candidates.append([])
    return sorted(candidates, key=lambda values: (len(values), values))


def count_immediate_lines(template: Template, given_indices: list[int]) -> int:
    given_set = set(given_indices)
    count = 0
    for line in template.lines:
        visible = sum(1 for slot_index in line["slotIndices"] if slot_index in given_set)
        if visible >= 2:
            count += 1
    return count

