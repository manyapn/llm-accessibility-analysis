#!/usr/bin/env python3
"""Compact all view hierarchy JSON files for one recording task.

This is a task-level wrapper around view_hierarchy.compact_tree(). It keeps the
single-tree experiment isolated while making it easier to produce compact trees
for an entire trace folder.

Usage:
    python3 compact_task_trees.py data/recordings/recording_manyapn_GM_2
    python3 compact_task_trees.py data/recordings/recording_manyapn_GM_2 --out /tmp/gm2_compact
"""

import argparse
import json
import sys
from pathlib import Path

from view_hierarchy import compact_tree


def _count_nodes(node: dict) -> int:
    if not node:
        return 0
    return 1 + sum(_count_nodes(child) for child in node.get("children", []))


def _json_size(value: dict) -> int:
    return len(json.dumps(value, separators=(",", ":")))


def _default_output_dir(task_dir: Path) -> Path:
    return Path("experiments") / "compact_trees" / task_dir.name


def compact_task_trees(task_dir: Path, out_dir: Path, pretty: bool) -> dict:
    trees_dir = task_dir / "trees"
    if not task_dir.is_dir():
        raise FileNotFoundError(f"Task folder not found: {task_dir}")
    if not trees_dir.is_dir():
        raise FileNotFoundError(f"Task folder has no trees/ directory: {task_dir}")

    tree_files = sorted(trees_dir.glob("*.json"))
    if not tree_files:
        raise FileNotFoundError(f"No JSON tree files found in: {trees_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    indent = 2 if pretty else None
    files = []
    totals = {
        "before_nodes": 0,
        "after_nodes": 0,
        "before_chars": 0,
        "after_chars": 0,
    }

    for tree_file in tree_files:
        tree = json.loads(tree_file.read_text())
        compact = compact_tree(tree)

        out_file = out_dir / f"{tree_file.stem}.compact.json"
        out_file.write_text(json.dumps(compact, indent=indent) + "\n")

        before_nodes = _count_nodes(tree)
        after_nodes = _count_nodes(compact)
        before_chars = _json_size(tree)
        after_chars = _json_size(compact)

        totals["before_nodes"] += before_nodes
        totals["after_nodes"] += after_nodes
        totals["before_chars"] += before_chars
        totals["after_chars"] += after_chars

        files.append(
            {
                "source": str(tree_file),
                "compact": str(out_file),
                "before_nodes": before_nodes,
                "after_nodes": after_nodes,
                "before_chars": before_chars,
                "after_chars": after_chars,
            }
        )

    manifest = {
        "task_dir": str(task_dir),
        "trees_dir": str(trees_dir),
        "out_dir": str(out_dir),
        "file_count": len(files),
        "totals": totals,
        "files": files,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def _reduction(before: int, after: int) -> float:
    if before == 0:
        return 0.0
    return 100 * (1 - after / before)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate compact view hierarchy JSON files for a recording task."
    )
    parser.add_argument("task_dir", help="Recording folder containing trees/")
    parser.add_argument(
        "--out",
        type=Path,
        help="Output directory. Defaults to experiments/compact_trees/<task-folder>/",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Write indented compact JSON instead of minified JSON.",
    )
    args = parser.parse_args()

    task_dir = Path(args.task_dir)
    out_dir = args.out or _default_output_dir(task_dir)

    try:
        manifest = compact_task_trees(task_dir, out_dir, args.pretty)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    totals = manifest["totals"]
    print(f"Compacted {manifest['file_count']} tree files")
    print(f"Output: {manifest['out_dir']}")
    print(
        "Nodes : "
        f"{totals['before_nodes']} -> {totals['after_nodes']} "
        f"({_reduction(totals['before_nodes'], totals['after_nodes']):.0f}% reduction)"
    )
    print(
        "Chars : "
        f"{totals['before_chars']:,} -> {totals['after_chars']:,} "
        f"({_reduction(totals['before_chars'], totals['after_chars']):.0f}% reduction)"
    )
    print(f"Manifest: {manifest['out_dir']}/manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
