# Developer Triage Experiment

This folder contains an experimental downstream workflow for converting raw
TalkBack accessibility detections into developer-facing repair priorities.

It is intentionally separate from the main WCAG detection pipeline.

Core pipeline files remain:
- `.claude/skills/wcag/SKILL.md`
- `PROMPT_TEMPLATE.md`
- `CLAUDE.md`
- `results/*_analysis.md`
- `results/*_results.csv`

Experimental files here:
- `ANALYSIS_LAYERS.md` — proposed separation between trace analysis,
  developer triage, and aggregate reporting.
- `DEVELOPER_TRIAGE_PROMPT.md` — optional grouping of raw detections into
  developer-prioritized issues.

Do not treat these prompts as part of the canonical study pipeline unless they
are explicitly promoted later.
