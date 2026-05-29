# Accessibility Research Project

## Goal
Analyze Android screen reader (TalkBack) traces to identify accessibility issues in mobile apps, assessed against WCAG 2.2 guidelines.

## Apps & Tasks
- Gmail: GM1 (Core), GM2 (Stressful)
- Amazon: AM1 (Core), AM2 (Stressful)
- Google Maps: MP1 (Core), MP2 (Stressful)
- YouTube: YT1 (Core), YT2 (Stressful)

## Input Files
Each trace folder contains:
- `events.jsonl` — TalkBack focus events, announcements, UI element metadata
- `user_actions.jsonl` — actions performed during the task
- `trees/` — view hierarchy JSONs per screen
- `screenshots/` — ignore entirely

## Input Combos (run all 4 per trace)
1. **Events only** — `events.jsonl` only
2. **Trees only** — all files in `trees/` only
3. **Events + User Actions** — `events.jsonl` + `user_actions.jsonl`
4. **Events + User Actions + Trees** — all three

## Analysis Pipeline (per trace, fresh session)
For each combo, do both steps simultaneously before moving to the next combo:

**Step A — Write to `[TASK_ID]_analysis.md`:**
```
## [TASK_ID] — [Combo Name]

### Emulator Note (if applicable)
[note any lag or artifacts]

### Issues Found
1. **[Short title]**
   - Description: [clear, concise]
   - WCAG: [criterion number + name + level]
   - Severity: High / Medium / Low
   - Evidence: [specific quote or reference from trace]
   - Manually Observed: Y / N / Unconfirmed
```

**Step B — Simultaneously append each issue as a CSV row to `[TASK_ID]_results.csv`:**

Column order:
Task ID, App, Type, Issue #, Input Combo, Issue Description, WCAG Criterion, Severity, Manually Observed, Emulator Artifact, Verified on Real Device, Claude (Events), Claude (Trees), Claude (Events + User Actions), Claude (Events + User Actions + Trees), Codex (Events), Codex (Trees), Codex (Events + User Actions), Codex (Events + User Actions + Trees), Notes

Rules:
- Write markdown and CSV row for each issue at the same time — do not batch
- Mark Y only in the Claude column matching the current input combo
- Leave all Codex columns blank
- Emulator Artifact: Y if flagged, N if confirmed real, ? if uncertain
- Verified on Real Device: leave blank
- Notes: include the evidence quote from the markdown
- Create header row if file does not exist

## What to Flag
Only flag issues that would affect a real blind user on a real device:
- Missing or empty labels (`label: ""` or `<no_feedback>`)
- Uninformative announcements (e.g. "Button, double-tap to activate" with no context)
- Incorrect or missing roles on interactive elements
- Elements with `isFocusable=false` that should be interactive
- `contentDescription=""` on meaningful UI elements
- Focus order issues (unexpected jumps, traps)
- Dynamic content changes not announced
- State not communicated (checked, selected, expanded)
- Status messages not announced
- Label mismatch between visible text and announced name

## Do NOT Flag (false positives / emulator artifacts)
- EditText zero-size bounds `{w:0, h:0}` during typing — emulator artifact
- Multiple browser taps before action registers — emulator lag
- Triple-tap or repeated tap patterns — emulator lag
- Repeated punctuation or multiple commas in announcements — data artifact
- Accidental speech rate changes — emulator navigation artifact

## Emulator Lag Documentation
If the session shows emulator lag, note it at the top of the markdown file:
> **Emulator Note:** [description]. This may affect reliability of interaction-based findings.

Do not flag emulator lag as accessibility issues — document it separately.

## WCAG 2.2 Reference
Use the `/wcag` skill when identifying and categorizing issues.
