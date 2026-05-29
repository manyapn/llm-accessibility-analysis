# Claude Code Prompt Template
# Use at the start of a fresh session per trace.
# Replace [TASK_ID], [FOLDER], [APP], [TYPE], [MANUAL_OBSERVATIONS].

---

/wcag

Analyze the trace at [FOLDER] for accessibility issues.

Task ID: [TASK_ID]
App: [APP]
Type: [TYPE]

Run all 4 input combos in order:
1. Events only (events.jsonl)
2. Trees only (all files in trees/)
3. Events + User Actions (events.jsonl + user_actions.jsonl)
4. Events + User Actions + Trees (all three)

For each issue found in each combo:
- Write the full finding to [TASK_ID]_analysis.md (markdown format)
- Simultaneously append the same issue as a CSV row to [TASK_ID]_results.csv
- Do this for every issue before moving to the next combo

Do not batch — write markdown and CSV row together per issue as you go.
Do not flag emulator artifacts (zero-size bounds, repeated taps, multiple commas).
Note any emulator lag at the top of the markdown file.

Manually observed issues during recording:
[MANUAL_OBSERVATIONS]

---

# Ready-to-Use Prompts Per Task

## GM1 — Gmail Core
 
/wcag
 
Analyze the trace at /Users/manyapn/Documents/accessibility-research/recording_manyapn_gm1_gm1 for accessibility issues.
 
Task ID: GM1, App: Gmail, Type: Core
Model: claude-sonnet-4-6, Prompt Version: v1.0
 
Run all 4 input combos in order:
1. Events only (events.jsonl)
2. Trees only (all files in trees/)
3. Events + User Actions (events.jsonl + user_actions.jsonl)
4. Events + User Actions + Trees (all three)
For each issue: write to results/GM1_analysis.md and append CSV row to results/GM1_results.csv simultaneously. Include Model, Prompt Version, Date in every output. Do not batch. Do not flag emulator artifacts. Note emulator lag at top of markdown if observed.

Manually observed issues during recording:
[MANUAL_OBSERVATIONS]

---
 
## GM2 — Gmail Stressful
 
/wcag
 
Analyze the trace at /Users/manyapn/Documents/accessibility-research/recording_manyapn_gm2_gm2 for accessibility issues.
 
Task ID: GM2, App: Gmail, Type: Stressful
Model: claude-sonnet-4-6, Prompt Version: v1.0
 
Run all 4 input combos in order:
1. Events only (events.jsonl)
2. Trees only (all files in trees/)
3. Events + User Actions (events.jsonl + user_actions.jsonl)
4. Events + User Actions + Trees (all three)
For each issue: write to results/GM2_analysis.md and append CSV row to results/GM2_results.csv simultaneously. Include Model, Prompt Version, Date in every output. Do not batch. Do not flag emulator artifacts. Note emulator lag at top of markdown if observed.
 
Manually observed issues during recording:
[MANUAL_OBSERVATIONS]

---

## AM1 — Amazon Core
/wcag

Analyze the trace at /Users/manyapn/Documents/accessibility-research/recording_manyapn_AM_1 for accessibility issues.

Task ID: AM1, App: Amazon, Type: Core

Run all 4 input combos in order:
1. Events only
2. Trees only
3. Events + User Actions
4. Events + User Actions + Trees

For each issue: write to AM1_analysis.md and append CSV row to AM1_results.csv simultaneously. Do not batch. Do not flag emulator artifacts. Note emulator lag at top of markdown if observed.

Manually observed issues:
- TalkBack focus possibly stuck cycling through filter chips — could not navigate to product. Possible focus trap, needs verification on real device.

---

## AM2 — Amazon Stressful
/wcag

Analyze the trace at /Users/manyapn/Documents/accessibility-research/recording_manyapn_AM_2 for accessibility issues.

Task ID: AM2, App: Amazon, Type: Stressful

Run all 4 input combos in order:
1. Events only
2. Trees only
3. Events + User Actions
4. Events + User Actions + Trees

For each issue: write to AM2_analysis.md and append CSV row to AM2_results.csv simultaneously. Do not batch. Do not flag emulator artifacts. Note emulator lag at top of markdown if observed.

Manually observed issues:
[fill in before running]

---

## MP1 — Google Maps Core
/wcag

Analyze the trace at /Users/manyapn/Documents/accessibility-research/recording_MANYAPN_MP_1 for accessibility issues.

Task ID: MP1, App: Google Maps, Type: Core

Run all 4 input combos in order:
1. Events only
2. Trees only
3. Events + User Actions
4. Events + User Actions + Trees

For each issue: write to MP1_analysis.md and append CSV row to MP1_results.csv simultaneously. Do not batch. Do not flag emulator artifacts. Note emulator lag at top of markdown if observed.

Manually observed issues:
[fill in before running]

---

## MP2 — Google Maps Stressful
/wcag

Analyze the trace at /Users/manyapn/Documents/accessibility-research/recording_MANYAPN_MP_2 for accessibility issues.

Task ID: MP2, App: Google Maps, Type: Stressful

Run all 4 input combos in order:
1. Events only
2. Trees only
3. Events + User Actions
4. Events + User Actions + Trees

For each issue: write to MP2_analysis.md and append CSV row to MP2_results.csv simultaneously. Do not batch. Do not flag emulator artifacts. Note emulator lag at top of markdown if observed.

Manually observed issues:
[fill in before running]

---

## YT1 — YouTube Core
/wcag

Analyze the trace at /Users/manyapn/Documents/accessibility-research/recording_MANYAPN_YT_1 for accessibility issues.

Task ID: YT1, App: YouTube, Type: Core

Run all 4 input combos in order:
1. Events only
2. Trees only
3. Events + User Actions
4. Events + User Actions + Trees

For each issue: write to YT1_analysis.md and append CSV row to YT1_results.csv simultaneously. Do not batch. Do not flag emulator artifacts. Note emulator lag at top of markdown if observed.

Manually observed issues:
[fill in before running]

---

## YT2 — YouTube Stressful
/wcag

Analyze the trace at /Users/manyapn/Documents/accessibility-research/recording_MANYAPN_YT_2 for accessibility issues.

Task ID: YT2, App: YouTube, Type: Stressful

Run all 4 input combos in order:
1. Events only
2. Trees only
3. Events + User Actions
4. Events + User Actions + Trees

For each issue: write to YT2_analysis.md and append CSV row to YT2_results.csv simultaneously. Do not batch. Do not flag emulator artifacts. Note emulator lag at top of markdown if observed.

Manually observed issues:
[fill in before running]
