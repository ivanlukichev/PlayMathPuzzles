from __future__ import annotations

import json
from pathlib import Path


def load_existing_entries(output_path: Path) -> list[dict]:
    if not output_path.exists():
        return []
    return json.loads(output_path.read_text(encoding="utf-8"))


def merge_entries(existing_entries: list[dict], new_entries: list[dict], categories: set[tuple[int, str]]) -> list[dict]:
    kept_entries = [
        entry
        for entry in existing_entries
        if (entry["size"], entry["difficulty"]) not in categories
    ]
    merged = kept_entries + new_entries
    return sorted(merged, key=lambda entry: (entry["size"], entry["difficulty"], entry["index"]))


def write_entries(output_path: Path, entries: list[dict]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

