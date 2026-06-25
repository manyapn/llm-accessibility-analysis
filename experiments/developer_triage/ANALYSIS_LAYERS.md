# Accessibility Analysis Layers

The working abstraction is intentionally shallow:

```text
raw data -> trace analysis -> developer triage
```

Developer triage is only one step above trace analysis. It should not require
an intermediate review file.

## Layer 1: Trace Analysis

Purpose: identify accessibility issues in a TalkBack trace and cite the closest
WCAG criterion.

Use:
- `.claude/skills/wcag/SKILL.md`
- `PROMPT_TEMPLATE.md`
- `CLAUDE.md`

Inputs:
- `events.jsonl`
- `user_actions.jsonl`
- `trees/`

Outputs:
- `results/[TASK_ID]_analysis.md`
- `results/[TASK_ID]_results.csv`

Claims this layer can make:
- A trace contains a possible issue.
- A likely WCAG criterion applies.
- The issue was or was not manually observed by the reviewer.

Claims this layer should not make:
- Developer priority.
- Grouped repair issue counts.
- Dataset-wide precision or recall.

## Layer 2: Developer Triage

Purpose: convert completed trace-analysis outputs into a smaller
developer-facing repair list.

Use:
- `DEVELOPER_TRIAGE_PROMPT.md`

Inputs:
- `results/[TASK_ID]_analysis.md`
- `results/[TASK_ID]_results.csv`
- trace files only when needed to verify evidence or merge duplicates

Outputs:
- `results/[TASK_ID]_developer_triage.md`
- `results/[TASK_ID]_developer_triage.csv`

Claims this layer can make:
- Multiple raw detections refer to one underlying developer issue.
- A grouped issue is P0 / P1 / P2 / P3.
- A likely fix category and verification step.
- Whether a grouped issue is likely, partially, or unlikely to be caught by a
  simple checker.

Claims this layer should not make:
- New raw findings not supported by trace analysis.
- Dataset-wide precision or recall.

## Aggregate Research Reporting

Aggregate reporting may use both raw detection outputs and developer-triage
outputs, but it should keep the counts separate:

- Raw detections answer: what did the analysis flag?
- Developer issues answer: what should a developer fix?
