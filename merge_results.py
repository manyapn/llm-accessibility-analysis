#!/usr/bin/env python3
"""Regenerate results/master_results.csv from the per-task results/*_results.csv files.

Concatenates all per-task rows as-is (no deduplication) into the canonical
20-column schema defined in CLAUDE.md. Per-task files with extra columns
(e.g. PS1's Model/Prompt Version/Date) are normalized down to the canonical
columns for the master; their source CSVs are left untouched.
"""

import csv
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
MASTER_PATH = RESULTS_DIR / "master_results.csv"

TASK_IDS = ["GM1", "GM2", "AM1", "AM2", "MP1", "MP2", "YT1", "YT2", "PS1"]

CANONICAL_COLUMNS = [
    "Task ID",
    "App",
    "Type",
    "Issue #",
    "Input Combo",
    "Issue Description",
    "WCAG Criterion",
    "Severity",
    "Manually Observed",
    "Emulator Artifact",
    "Verified on Real Device",
    "Claude (Events)",
    "Claude (Trees)",
    "Claude (Events + User Actions)",
    "Claude (Events + User Actions + Trees)",
    "Codex (Events)",
    "Codex (Trees)",
    "Codex (Events + User Actions)",
    "Codex (Events + User Actions + Trees)",
    "Notes",
]


def main():
    rows = []
    for task_id in TASK_IDS:
        path = RESULTS_DIR / f"{task_id}_results.csv"
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                rows.append({col: row.get(col, "") for col in CANONICAL_COLUMNS})

    with open(MASTER_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows, {len(CANONICAL_COLUMNS)} columns to {MASTER_PATH}")
    print("Task IDs:", sorted({r['Task ID'] for r in rows}))


if __name__ == "__main__":
    main()
