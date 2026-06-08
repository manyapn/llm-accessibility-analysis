# LLM Accessibility Analysis

This repository contains an exploratory research workflow for evaluating how AI tools identify accessibility issues in Android mobile app traces collected with TalkBack.

## Project Goal

The project compares manually observed accessibility issues against issues detected by LLM-based analysis. The current traces cover Gmail, Amazon, Google Maps, YouTube, and one Play Store setup trace.

## Repository Structure

- `data/recordings/` — raw TalkBack interaction traces.
- `results/` — per-task markdown analyses, per-task CSV outputs, and the canonical combined results table.
- `results/master_results.csv` — canonical master comparison table.
- `CLAUDE.md` — analysis instructions used with Claude Code.
- `PROMPT_TEMPLATE.md` — reusable prompts for running each trace analysis.
- `.claude/skills/wcag/` — local WCAG 2.2 reference skill used during analysis.

Each recording folder generally contains:

- `events.jsonl` — TalkBack focus events, announcements, and UI element metadata.
- `user_actions.jsonl` — recorded user actions during the task.
- `trees/` — Android view hierarchy snapshots.
- `screenshots/` — raw screenshots captured during the trace.

## External Tooling

The raw traces were collected using TalkBack-Portal, which is a separate tool and is not part of this repository:

https://github.com/jszh/TalkBack-Portal

## Data Notes

The recording data may include raw app UI text, screenshots, public comments or usernames from apps, coarse location strings, and participant/task identifiers. Treat these traces as research data rather than polished public-release artifacts.

## Current Limitations

- Some findings are preliminary and marked as unconfirmed.
- Emulator lag and repeated tap artifacts may affect interaction-based findings.
- Not all AI-detected issues have been verified on a real device.
- Screenshots are included as raw trace artifacts, but the current text analysis workflow primarily uses events, user actions, and view hierarchies.
