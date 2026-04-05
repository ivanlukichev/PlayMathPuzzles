from __future__ import annotations

from dataclasses import dataclass

from .utils import BOARD_SIZE, get_active_bounds, get_cell_id

TEMPLATES = {
    5: [
        {
            "id": "5x5-classic",
            "size": 5,
            "placements": [
                {"orientation": "h", "startX": 0, "startY": 0},
                {"orientation": "h", "startX": 0, "startY": 2},
                {"orientation": "h", "startX": 0, "startY": 4},
                {"orientation": "v", "startX": 0, "startY": 0},
                {"orientation": "v", "startX": 2, "startY": 0},
                {"orientation": "v", "startX": 4, "startY": 0},
            ],
        }
    ],
    7: [
        {
            "id": "7x7-stagger-a",
            "size": 7,
            "placements": [
                {"orientation": "h", "startX": 0, "startY": 0},
                {"orientation": "h", "startX": 0, "startY": 2},
                {"orientation": "h", "startX": 2, "startY": 4},
                {"orientation": "h", "startX": 2, "startY": 6},
                {"orientation": "v", "startX": 0, "startY": 0},
                {"orientation": "v", "startX": 2, "startY": 0},
                {"orientation": "v", "startX": 4, "startY": 2},
                {"orientation": "v", "startX": 6, "startY": 2},
            ],
        },
        {
            "id": "7x7-stagger-b",
            "size": 7,
            "placements": [
                {"orientation": "h", "startX": 2, "startY": 0},
                {"orientation": "h", "startX": 0, "startY": 2},
                {"orientation": "h", "startX": 2, "startY": 4},
                {"orientation": "h", "startX": 0, "startY": 6},
                {"orientation": "v", "startX": 0, "startY": 2},
                {"orientation": "v", "startX": 2, "startY": 0},
                {"orientation": "v", "startX": 4, "startY": 0},
                {"orientation": "v", "startX": 6, "startY": 2},
            ],
        },
    ],
    9: [
        {
            "id": "9x9-stagger-a",
            "size": 9,
            "placements": [
                {"orientation": "h", "startX": 0, "startY": 0},
                {"orientation": "h", "startX": 2, "startY": 2},
                {"orientation": "h", "startX": 0, "startY": 4},
                {"orientation": "h", "startX": 2, "startY": 6},
                {"orientation": "h", "startX": 4, "startY": 8},
                {"orientation": "v", "startX": 0, "startY": 0},
                {"orientation": "v", "startX": 2, "startY": 0},
                {"orientation": "v", "startX": 4, "startY": 2},
                {"orientation": "v", "startX": 6, "startY": 4},
                {"orientation": "v", "startX": 8, "startY": 4},
            ],
        },
        {
            "id": "9x9-stagger-b",
            "size": 9,
            "placements": [
                {"orientation": "h", "startX": 4, "startY": 0},
                {"orientation": "h", "startX": 2, "startY": 2},
                {"orientation": "h", "startX": 0, "startY": 4},
                {"orientation": "h", "startX": 2, "startY": 6},
                {"orientation": "h", "startX": 0, "startY": 8},
                {"orientation": "v", "startX": 0, "startY": 4},
                {"orientation": "v", "startX": 2, "startY": 2},
                {"orientation": "v", "startX": 4, "startY": 0},
                {"orientation": "v", "startX": 6, "startY": 2},
                {"orientation": "v", "startX": 8, "startY": 4},
            ],
        },
    ],
    11: [
        {
            "id": "11x11-weave-a",
            "size": 11,
            "placements": [
                {"orientation": "h", "startX": 0, "startY": 0},
                {"orientation": "h", "startX": 2, "startY": 2},
                {"orientation": "h", "startX": 0, "startY": 4},
                {"orientation": "h", "startX": 2, "startY": 6},
                {"orientation": "h", "startX": 4, "startY": 8},
                {"orientation": "h", "startX": 6, "startY": 10},
                {"orientation": "v", "startX": 0, "startY": 0},
                {"orientation": "v", "startX": 2, "startY": 0},
                {"orientation": "v", "startX": 4, "startY": 2},
                {"orientation": "v", "startX": 6, "startY": 4},
                {"orientation": "v", "startX": 8, "startY": 6},
                {"orientation": "v", "startX": 10, "startY": 6},
            ],
        },
        {
            "id": "11x11-weave-b",
            "size": 11,
            "placements": [
                {"orientation": "h", "startX": 6, "startY": 0},
                {"orientation": "h", "startX": 4, "startY": 2},
                {"orientation": "h", "startX": 2, "startY": 4},
                {"orientation": "h", "startX": 0, "startY": 6},
                {"orientation": "h", "startX": 2, "startY": 8},
                {"orientation": "h", "startX": 4, "startY": 10},
                {"orientation": "v", "startX": 0, "startY": 6},
                {"orientation": "v", "startX": 2, "startY": 4},
                {"orientation": "v", "startX": 4, "startY": 2},
                {"orientation": "v", "startX": 6, "startY": 0},
                {"orientation": "v", "startX": 8, "startY": 2},
                {"orientation": "v", "startX": 10, "startY": 4},
            ],
        },
    ],
}


@dataclass(frozen=True)
class Template:
    id: str
    logical_size: int
    placements: tuple[dict, ...]
    cells: tuple[dict, ...]
    lines: tuple[dict, ...]
    slot_count: int
    line_count: int
    slot_usage: dict[int, int]
    result_slot_indices: tuple[int, ...]
    intersection_slot_indices: tuple[int, ...]
    key_slot_indices: tuple[int, ...]


def _line_cells(orientation: str, start_x: int, start_y: int) -> list[dict]:
    if orientation == "h":
        return [
            {"x": start_x, "y": start_y, "role": "a", "type": "empty"},
            {"x": start_x + 1, "y": start_y, "role": "operator", "type": "operator"},
            {"x": start_x + 2, "y": start_y, "role": "b", "type": "empty"},
            {"x": start_x + 3, "y": start_y, "role": "equals", "type": "equals"},
            {"x": start_x + 4, "y": start_y, "role": "c", "type": "empty"},
        ]
    if orientation == "v":
        return [
            {"x": start_x, "y": start_y, "role": "a", "type": "empty"},
            {"x": start_x, "y": start_y + 1, "role": "operator", "type": "operator"},
            {"x": start_x, "y": start_y + 2, "role": "b", "type": "empty"},
            {"x": start_x, "y": start_y + 3, "role": "equals", "type": "equals"},
            {"x": start_x, "y": start_y + 4, "role": "c", "type": "empty"},
        ]
    raise ValueError(f"Unsupported orientation: {orientation}")


def _build_template(definition: dict) -> Template:
    size = definition["size"]
    bounds = get_active_bounds(size)
    cell_map: dict[str, dict] = {}
    slot_index_by_cell: dict[str, int] = {}
    slot_usage: dict[int, int] = {}
    lines: list[dict] = []
    next_slot_index = 0
    next_operator_index = 0

    for line_index, placement in enumerate(definition["placements"]):
        orientation = placement["orientation"]
        start_x = placement["startX"]
        start_y = placement["startY"]
        if orientation == "h" and start_x + 5 > size:
            raise ValueError(f"Template {definition['id']} has a horizontal line outside bounds.")
        if orientation == "v" and start_y + 5 > size:
            raise ValueError(f"Template {definition['id']} has a vertical line outside bounds.")

        slot_indices: list[int] = []
        operator_index = None
        for cell in _line_cells(orientation, start_x, start_y):
            row = bounds["rowStart"] + cell["y"]
            col = bounds["colStart"] + cell["x"]
            if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
                raise ValueError(f"Template {definition['id']} contains a cell outside the 11x11 board.")

            cell_id = get_cell_id(row, col)
            existing = cell_map.get(cell_id)
            if cell["type"] == "empty":
                if cell_id not in slot_index_by_cell:
                    slot_index_by_cell[cell_id] = next_slot_index
                    slot_usage[next_slot_index] = 0
                    next_slot_index += 1
                slot_index = slot_index_by_cell[cell_id]
                slot_usage[slot_index] += 1
                slot_indices.append(slot_index)
                cell_map[cell_id] = {
                    "id": cell_id,
                    "row": row,
                    "col": col,
                    "type": "empty",
                    "slotId": f"slot-{slot_index}",
                    "solutionIndex": slot_index,
                }
                continue

            if existing and existing["type"] != cell["type"]:
                raise ValueError(f"Template {definition['id']} has a conflicting overlap at {cell_id}.")

            if cell["type"] == "operator":
                operator_index = next_operator_index
                cell_map[cell_id] = {
                    "id": cell_id,
                    "row": row,
                    "col": col,
                    "type": "operator",
                    "operatorIndex": next_operator_index,
                }
                next_operator_index += 1
                continue

            cell_map[cell_id] = {
                "id": cell_id,
                "row": row,
                "col": col,
                "type": "equals",
                "value": "=",
            }

        if len(slot_indices) != 3 or operator_index is None:
            raise ValueError(f"Template {definition['id']} line {line_index} is malformed.")

        lines.append(
            {
                "id": f"{orientation}-{line_index}",
                "orientation": orientation,
                "slotIndices": tuple(slot_indices),
                "operatorIndex": operator_index,
            }
        )

    result_slot_indices = tuple(line["slotIndices"][2] for line in lines)
    intersection_slot_indices = tuple(
        slot_index
        for slot_index, usage_count in sorted(slot_usage.items())
        if usage_count > 1
    )
    key_slot_indices = tuple(sorted(set(result_slot_indices) | set(intersection_slot_indices)))
    return Template(
        id=definition["id"],
        logical_size=size,
        placements=tuple(definition["placements"]),
        cells=tuple(sorted(cell_map.values(), key=lambda cell: (cell["row"], cell["col"]))),
        lines=tuple(lines),
        slot_count=len(slot_usage),
        line_count=len(lines),
        slot_usage=dict(sorted(slot_usage.items())),
        result_slot_indices=result_slot_indices,
        intersection_slot_indices=intersection_slot_indices,
        key_slot_indices=key_slot_indices,
    )


BUILT_TEMPLATES = {
    size: tuple(_build_template(definition) for definition in definitions)
    for size, definitions in TEMPLATES.items()
}
TEMPLATES_BY_ID = {
    template.id: template
    for templates in BUILT_TEMPLATES.values()
    for template in templates
}


def get_templates_for_size(size: int) -> tuple[Template, ...]:
    templates = BUILT_TEMPLATES.get(size)
    if templates is None:
        raise ValueError(f"No templates configured for size {size}.")
    return templates


def get_template_by_id(template_id: str) -> Template:
    template = TEMPLATES_BY_ID.get(template_id)
    if template is None:
        raise ValueError(f"Unknown template id: {template_id}")
    return template

