#!/usr/bin/env python3
"""View hierarchy compaction for TalkBack accessibility analysis.

Schema note: tree files use nested children objects (not id references).
There is no built-in node id; this module assigns sequential DFS integers
(field 'id') so expand_node() can locate any node in the original tree.

Functions
---------
compact_tree(tree)          -> slim nested tree, accessibility-relevant nodes only
expand_node(tree, node_id)  -> full original detail for one node by id

CLI
---
    python view_hierarchy.py <tree_json> [--node <id>]
"""

import argparse
import copy
import json
import sys
from pathlib import Path

# Fields that carry human-readable content
_LABEL_FIELDS = (
    "text",
    "contentDescription",
    "hint",
    "stateDescription",
    "paneTitle",
    "tooltipText",
)

# Boolean flags that make a node interactive
_INTERACTIVE_FLAGS = (
    "isClickable",
    "isLongClickable",
    "isFocusable",
    "isScrollable",
    "isEditable",
    "isCheckable",
)

# Boolean flags that make a node accessibility-relevant independent of interactivity
_A11Y_FLAGS = (
    "isImportantForAccessibility",
    "isScreenReaderFocusable",
    "isHeading",
)

# Complete set of fields written to compact output (booleans only if True)
_COMPACT_SCALAR_FIELDS = ("resourceId", "className") + _LABEL_FIELDS + _INTERACTIVE_FLAGS + _A11Y_FLAGS


# Internal helpers

def _bounds_nonzero(node: dict) -> bool:
    b = node.get("boundsInScreen", {})
    w = b.get("right", 0) - b.get("left", 0)
    h = b.get("bottom", 0) - b.get("top", 0)
    return w > 0 and h > 0


def _has_label(node: dict) -> bool:
    return any(node.get(f) for f in _LABEL_FIELDS)


def _is_interactive(node: dict) -> bool:
    return any(node.get(f) for f in _INTERACTIVE_FLAGS)


def _is_a11y_relevant(node: dict) -> bool:
    return any(node.get(f) for f in _A11Y_FLAGS) or node.get("liveRegion", 0) != 0


def _should_keep_own(node: dict) -> bool:
    """Node has its own accessibility value (ignoring descendants)."""
    return (
        (_has_label(node) or _is_interactive(node) or _is_a11y_relevant(node))
        and _bounds_nonzero(node)
    )


def _has_surviving_descendants(node: dict) -> bool:
    """True if any descendant passes _should_keep_own."""
    for child in node.get("children", []):
        if _should_keep_own(child) or _has_surviving_descendants(child):
            return True
    return False


def _assign_ids(node: dict, counter: list) -> None:
    """DFS-order integer assignment into '_id'. Mutates the copy in place."""
    node["_id"] = counter[0]
    counter[0] += 1
    for child in node.get("children", []):
        _assign_ids(child, counter)


def _compact_node(node: dict) -> dict:
    slim: dict = {"id": node["_id"]}
    for field in _COMPACT_SCALAR_FIELDS:
        v = node.get(field)
        if v is None:
            continue
        if isinstance(v, bool):
            if v:
                slim[field] = True
        elif isinstance(v, str):
            if v:
                slim[field] = v
        else:
            slim[field] = v
    slim["boundsInScreen"] = node.get("boundsInScreen", {})
    kids = _compact_children(node.get("children", []))
    if kids:
        slim["children"] = kids
    return slim


def _compact_children(children: list) -> list:
    result = []
    for child in children:
        if _should_keep_own(child) or _has_surviving_descendants(child):
            # Keep as full compact node (structural wrappers preserved so
            # hierarchy remains navigable and ids stay unambiguous)
            result.append(_compact_node(child))
        # else: no label, not interactive, no useful descendants — drop entirely
    return result


def _count_nodes(node: dict) -> int:
    return 1 + sum(_count_nodes(c) for c in node.get("children", []))


def _find_by_id(node: dict, node_id: int):
    if node.get("_id") == node_id:
        return {k: v for k, v in node.items() if k != "_id"}
    for child in node.get("children", []):
        found = _find_by_id(child, node_id)
        if found is not None:
            return found
    return None


# Public API

def compact_tree(tree: dict) -> dict:
    """Return a slim accessibility tree.

    Keeps nodes that are interactive, focusable, accessibility-important, or
    carry a label/contentDescription/text. Structural containers are kept when
    they have surviving descendants (so hierarchy stays intact). Zero-size nodes
    and purely decorative leaf nodes with no useful descendants are dropped.

    Each kept node carries an 'id' field (DFS integer) usable with expand_node().
    Only these fields are kept per node: id, className, resourceId, text,
    contentDescription, hint, stateDescription, paneTitle, tooltipText,
    isFocusable, isClickable, isLongClickable, isScrollable, isEditable,
    isCheckable, isImportantForAccessibility, isScreenReaderFocusable,
    isHeading, boundsInScreen, children.
    Boolean flags are omitted when False.
    """
    root = copy.deepcopy(tree)
    _assign_ids(root, [0])
    if _should_keep_own(root) or _has_surviving_descendants(root):
        return _compact_node(root)
    return {}


def expand_node(tree: dict, node_id: int) -> dict:
    """Return the full original fields for the node with the given DFS id.

    Pass the same original tree dict that was passed to compact_tree().
    The id values come from the 'id' field in the compact_tree() output.
    Returns an empty dict if the id is not found.
    """
    root = copy.deepcopy(tree)
    _assign_ids(root, [0])
    return _find_by_id(root, node_id) or {}


# CLI

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("tree_file", help="Path to a tree JSON file (data/recordings/*/trees/*.json)")
    parser.add_argument("--node", type=int, metavar="ID", help="Print full detail for this node id")
    args = parser.parse_args()

    tree = json.loads(Path(args.tree_file).read_text())

    if args.node is not None:
        result = expand_node(tree, args.node)
        if not result:
            print(f"Node {args.node} not found.", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(result, indent=2))
        return

    compact = compact_tree(tree)

    before_nodes = _count_nodes(tree)
    after_nodes = _count_nodes(compact) if compact else 0
    before_chars = len(json.dumps(tree))
    after_chars = len(json.dumps(compact))

    pct_nodes = 100 * (1 - after_nodes / before_nodes) if before_nodes else 0
    pct_chars = 100 * (1 - after_chars / before_chars) if before_chars else 0

    print(f"Nodes : {before_nodes} -> {after_nodes}  ({before_nodes - after_nodes} dropped, {pct_nodes:.0f}% reduction)")
    print(f"Chars : {before_chars:,} -> {after_chars:,}  ({before_chars - after_chars:,} saved, {pct_chars:.0f}% reduction)")
    print()
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
