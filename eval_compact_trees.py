#!/usr/bin/env python3
"""Evaluate generated compact tree files for one recording task.

Checks:
- every raw trees/*.json file has one compact output
- every compact file is valid JSON and matches current compact_tree() output
- compact node schema contains only expected fields
- compact node ids are unique per tree and expand back to a source node
- total compact JSON size is meaningfully smaller than raw tree JSON size
"""

import argparse
import json
import sys
from pathlib import Path

from view_hierarchy import _COMPACT_SCALAR_FIELDS, compact_tree, expand_node


ALLOWED_COMPACT_FIELDS = {"id", "boundsInScreen", "children", *_COMPACT_SCALAR_FIELDS}
BOOL_COMPACT_FIELDS = {
    "isClickable",
    "isLongClickable",
    "isFocusable",
    "isScrollable",
    "isEditable",
    "isCheckable",
    "isImportantForAccessibility",
    "isScreenReaderFocusable",
    "isHeading",
}


def _default_compact_dir(task_dir: Path) -> Path:
    return Path("experiments") / "compact_trees" / task_dir.name


def _count_nodes(node: dict) -> int:
    if not node:
        return 0
    return 1 + sum(_count_nodes(child) for child in node.get("children", []))


def _json_size(value: dict) -> int:
    return len(json.dumps(value, separators=(",", ":")))


def _collect_ids(node: dict, ids: list[int]) -> None:
    if not node:
        return
    node_id = node.get("id")
    if isinstance(node_id, int):
        ids.append(node_id)
    for child in node.get("children", []):
        _collect_ids(child, ids)


def _validate_schema(node: dict, path: str, errors: list[str]) -> None:
    if not isinstance(node, dict):
        errors.append(f"{path}: compact node is not an object")
        return

    unknown = set(node) - ALLOWED_COMPACT_FIELDS
    if unknown:
        errors.append(f"{path}: unknown compact fields: {sorted(unknown)}")

    if "id" not in node or not isinstance(node["id"], int):
        errors.append(f"{path}: missing integer id")

    if "boundsInScreen" not in node or not isinstance(node["boundsInScreen"], dict):
        errors.append(f"{path}: missing boundsInScreen object")

    for field in BOOL_COMPACT_FIELDS:
        if field in node and node[field] is not True:
            errors.append(f"{path}: {field} should be omitted unless true")

    children = node.get("children", [])
    if "children" in node and not isinstance(children, list):
        errors.append(f"{path}: children must be a list")
        return

    for index, child in enumerate(children):
        _validate_schema(child, f"{path}.children[{index}]", errors)


def _evaluate_file(source_file: Path, compact_file: Path) -> tuple[dict, list[str]]:
    errors = []
    try:
        source = json.loads(source_file.read_text())
    except json.JSONDecodeError as exc:
        return {}, [f"{source_file}: source JSON parse failed: {exc}"]

    if not compact_file.exists():
        return {}, [f"{source_file}: missing compact output {compact_file}"]

    try:
        compact = json.loads(compact_file.read_text())
    except json.JSONDecodeError as exc:
        return {}, [f"{compact_file}: compact JSON parse failed: {exc}"]

    expected = compact_tree(source)
    if compact != expected:
        errors.append(f"{compact_file}: does not match compact_tree(source)")

    _validate_schema(compact, compact_file.name, errors)

    ids = []
    _collect_ids(compact, ids)
    duplicate_ids = sorted({node_id for node_id in ids if ids.count(node_id) > 1})
    if duplicate_ids:
        errors.append(f"{compact_file}: duplicate compact ids: {duplicate_ids[:10]}")

    for node_id in ids:
        if not expand_node(source, node_id):
            errors.append(f"{compact_file}: id {node_id} does not expand in source")
            break

    stats = {
        "before_nodes": _count_nodes(source),
        "after_nodes": _count_nodes(compact),
        "before_chars": _json_size(source),
        "after_chars": _json_size(compact),
    }
    return stats, errors


def _reduction(before: int, after: int) -> float:
    if before == 0:
        return 0.0
    return 100 * (1 - after / before)


def evaluate(task_dir: Path, compact_dir: Path, min_char_reduction: float) -> int:
    trees_dir = task_dir / "trees"
    errors = []

    if not trees_dir.is_dir():
        print(f"FAIL: missing trees directory: {trees_dir}", file=sys.stderr)
        return 1
    if not compact_dir.is_dir():
        print(f"FAIL: missing compact output directory: {compact_dir}", file=sys.stderr)
        return 1

    source_files = sorted(trees_dir.glob("*.json"))
    compact_files = sorted(compact_dir.glob("*.compact.json"))
    expected_compact_files = {
        compact_dir / f"{source_file.stem}.compact.json" for source_file in source_files
    }
    extra_compact_files = sorted(set(compact_files) - expected_compact_files)
    if extra_compact_files:
        errors.append(f"unexpected compact files: {[str(path) for path in extra_compact_files[:5]]}")

    totals = {
        "before_nodes": 0,
        "after_nodes": 0,
        "before_chars": 0,
        "after_chars": 0,
    }

    for source_file in source_files:
        compact_file = compact_dir / f"{source_file.stem}.compact.json"
        stats, file_errors = _evaluate_file(source_file, compact_file)
        errors.extend(file_errors)
        for key in totals:
            totals[key] += stats.get(key, 0)

    char_reduction = _reduction(totals["before_chars"], totals["after_chars"])
    if char_reduction < min_char_reduction:
        errors.append(
            f"character reduction {char_reduction:.0f}% is below minimum {min_char_reduction:.0f}%"
        )

    print(f"Source trees : {len(source_files)}")
    print(f"Compact files: {len(compact_files)}")
    print(f"Nodes        : {totals['before_nodes']} -> {totals['after_nodes']}")
    print(
        "Chars        : "
        f"{totals['before_chars']:,} -> {totals['after_chars']:,} "
        f"({char_reduction:.0f}% reduction)"
    )

    if errors:
        print("FAIL")
        for error in errors[:20]:
            print(f"- {error}")
        if len(errors) > 20:
            print(f"- ... {len(errors) - 20} more errors")
        return 1

    print("PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate compact tree outputs for a recording task."
    )
    parser.add_argument("task_dir", help="Recording folder containing trees/")
    parser.add_argument(
        "--compact-dir",
        type=Path,
        help="Compact tree directory. Defaults to experiments/compact_trees/<task-folder>/",
    )
    parser.add_argument(
        "--min-char-reduction",
        type=float,
        default=50.0,
        help="Minimum acceptable total character reduction percentage.",
    )
    args = parser.parse_args()

    task_dir = Path(args.task_dir)
    compact_dir = args.compact_dir or _default_compact_dir(task_dir)
    return evaluate(task_dir, compact_dir, args.min_char_reduction)


if __name__ == "__main__":
    raise SystemExit(main())
