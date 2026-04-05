from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from tools.puzzle_factory.export_json import load_existing_entries, merge_entries, write_entries
    from tools.puzzle_factory.generator import GeneratedPuzzle, build_category
    from tools.puzzle_factory.utils import (
        DEFAULT_TARGETS,
        DIFFICULTIES,
        build_legacy_id,
        build_puzzle_id,
        configure_logging,
        project_root,
        stable_seed,
    )
    from tools.puzzle_factory.validator import validate_export_entry
else:
    from .export_json import load_existing_entries, merge_entries, write_entries
    from .generator import GeneratedPuzzle, build_category
    from .utils import (
        DEFAULT_TARGETS,
        DIFFICULTIES,
        build_legacy_id,
        build_puzzle_id,
        configure_logging,
        project_root,
        stable_seed,
    )
    from .validator import validate_export_entry


def puzzle_to_entry(size: int, difficulty: str, index: int, candidate: GeneratedPuzzle) -> dict:
    entry = {
        "id": build_puzzle_id(size, difficulty, index),
        "legacyId": build_legacy_id(size, difficulty, index),
        "size": size,
        "difficulty": difficulty,
        "index": index,
        "templateId": candidate.template_id,
        "puzzle": list(candidate.puzzle),
        "solution": list(candidate.solution_values),
        "tray": list(candidate.tray),
        "givenIndices": list(candidate.given_indices),
    }
    issues = validate_export_entry(entry)
    if issues:
        raise ValueError(f"Entry {entry['id']} failed validation: {issues}")
    return entry


def parse_args(argv: list[str] | None = None, fixed_size: int | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build offline Math Crossword puzzle libraries.")
    if fixed_size is None:
        parser.add_argument("--size", type=int, choices=(5, 7, 9, 11), required=True)
    parser.add_argument("--difficulty", choices=DIFFICULTIES)
    parser.add_argument("--count", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    if fixed_size is not None:
        args.size = fixed_size
    return args


def build_categories_for_args(args: argparse.Namespace) -> dict[str, int]:
    size_targets = DEFAULT_TARGETS[args.size]
    if args.difficulty:
        target_count = args.count if args.count is not None else size_targets[args.difficulty]
        return {args.difficulty: target_count}
    if args.count is not None:
        return {difficulty: args.count for difficulty in DIFFICULTIES}
    return dict(size_targets)


def main(argv: list[str] | None = None, fixed_size: int | None = None) -> int:
    args = parse_args(argv, fixed_size=fixed_size)
    logger = configure_logging(args.log_level)
    output_path = args.output or project_root() / "data" / "puzzles.json"
    categories_to_build = build_categories_for_args(args)
    existing_entries = load_existing_entries(output_path)
    generated_entries: list[dict] = []

    for difficulty, count in categories_to_build.items():
        seed = args.seed if args.seed is not None else stable_seed("puzzle-factory", args.size, difficulty, count)
        rng = random.Random(seed)
        logger.info(
            "building size=%s difficulty=%s count=%s seed=%s output=%s",
            args.size,
            difficulty,
            count,
            seed,
            output_path,
        )
        accepted, stats = build_category(args.size, difficulty, count, rng, logger)
        if len(accepted) < count:
            logger.error(
                "build incomplete size=%s difficulty=%s accepted=%s target=%s summary=%s",
                args.size,
                difficulty,
                len(accepted),
                count,
                stats.summary(),
            )
            return 1
        category_entries = [
            puzzle_to_entry(args.size, difficulty, index, candidate)
            for index, candidate in enumerate(accepted, start=1)
        ]
        generated_entries.extend(category_entries)
        logger.info(
            "summary size=%s difficulty=%s generated=%s accepted=%s rejected=%s rejectReasons=%s",
            args.size,
            difficulty,
            stats.generated,
            stats.accepted,
            stats.rejected,
            dict(stats.reject_reasons),
        )

    merged = merge_entries(
        existing_entries,
        generated_entries,
        categories={(args.size, difficulty) for difficulty in categories_to_build},
    )
    write_entries(output_path, merged)
    logger.info("export count=%s path=%s", len(merged), output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
