# Developer Triage Prompt

Use this prompt after trace analysis. It converts raw detection-level findings
into a smaller developer-facing repair list.

Replace bracketed values before running.

---

## Repeatable Prompt

```text
You are creating a developer-facing accessibility triage report from an existing
TalkBack trace analysis. This is one step above trace analysis.

Task ID: [TASK_ID]
App: [APP]
Type: [Core or Stressful]
Recording folder: [data/recordings/...]
Analysis markdown: results/[TASK_ID]_analysis.md
Detection CSV: results/[TASK_ID]_results.csv

Goal:
Convert detection-level WCAG findings into a smaller set of prioritized
developer issues. One row in the CSV is one detection; the same underlying issue
may recur across input combos. Group duplicate detections when they share the
same UI element, user impact, and likely fix.

Important interpretation rule:
Manually Observed = N means the issue was not perceptible to a sighted reviewer
watching the recording. It is not the same as a false positive. Screen-reader
name, role, value, and status-message failures may be real even when sighted
review cannot confirm them.

Inputs to inspect:
1. results/[TASK_ID]_analysis.md
2. results/[TASK_ID]_results.csv
3. events.jsonl, user_actions.jsonl, and trees/ only when needed to verify
   evidence or merge duplicate detections
4. visual_summary.md or screenshot_descriptions.json only if present and useful

Do the work in this order:
1. Read the task analysis and detection CSV.
2. Normalize WCAG criterion names to criterion IDs, e.g. 4.1.2, 4.1.3, 2.4.3.
3. Group duplicate detections across input combos into one underlying issue.
4. For each grouped issue, assign:
   - Developer Priority: P0 / P1 / P2 / P3
   - Fix Category: Accessible Name / Role / State / Focus Order / Status Message
     / Keyboard Reachability / Target Size / Other
   - Evidence Strength: Strong / Medium / Weak
   - Simple Checker Detectability: Likely / Partial / Unlikely
5. Apply these priority rules:
   - P0: task completion blocked, focus trap, unrecoverable focus jump, or
     primary workflow element receives <no_feedback>.
   - P1: primary workflow issue with strong evidence, repeated user retry, or
     missing critical status/state announcement.
   - P2: real issue with limited observed workflow impact, or strong tree/static
     evidence without user-action confirmation.
   - P3: weak, tree-only, measurement-needed, or likely simple-checker issue
     needing verification.
6. Do not escalate tree-only 4.1.2 findings unless the TalkBack announcement or
   user actions show user impact.
7. Do not treat emulator lag, repeated browser taps, zero-size EditText during
   typing, or accidental TalkBack setting changes as accessibility issues.
8. Do not create new raw findings. If a new possible issue appears while reading
   the trace, mention it under "Needs Layer 1 Review" instead of adding it to
   the developer issue list.

Write:
1. A markdown report to results/[TASK_ID]_developer_triage.md
2. A CSV report to results/[TASK_ID]_developer_triage.csv

Markdown format:

# [TASK_ID] Developer Accessibility Triage

## Summary
- Total raw detections reviewed:
- Grouped developer issues:
- P0:
- P1:
- P2:
- P3:
- Simple-checker unlikely:
- Main repair themes:

## Scope And Method
- Source analysis files:
- Trace files consulted:
- Grouping rule:
- Priority rule:
- What this report does not do:

## Raw Detection Grouping
Table columns:
Developer Issue ID | Priority | Grouped Title | Raw Detection Count | Source Issue Numbers | Why These Were Grouped

## Priority Issues

For each grouped issue:

### [P0/P1/P2/P3] [Short developer-facing title]
- Fix Category:
- WCAG:
- Raw Detection Count:
- Input Combos:
- User Impact:
- Evidence Strength:
- Evidence Sources:
- Simple Checker Detectability:
- Why This Priority:
- Evidence:
- Raw Detections Grouped:
- Implementation Notes:
- Recommended Fix:
- Verification Step:
- Residual Risk / Open Question:

## Lower Priority / Verification Needed
List P3 or weak-evidence findings briefly.

## Likely Simple-Checker Findings
List issues a static accessibility checker would probably catch.

## Dynamic Issues Simple Checkers May Miss
List focus, status-message, user-action, and task-outcome issues that require
trace analysis.

## Verification Plan
List the concrete TalkBack checks a developer or QA person should run after
fixing the grouped issues.

## Triage Limitations
List emulator artifacts, real-device verification gaps, and any places where
the triage depends on inference from the trace-analysis outputs.

CSV columns:
Task ID,App,Type,Developer Issue ID,Priority,Fix Category,WCAG,Title,Raw Detection Count,Input Combos,User Impact,Evidence Strength,Evidence Sources,Simple Checker Detectability,Recommended Fix,Verification Step,Source Issue Numbers,Notes

Keep the output developer-facing. Use WCAG as supporting context, but lead with
user impact and recommended fix.
```

---

## Notes For Interpreting Output

- The CSV should be smaller than `[TASK_ID]_results.csv` because duplicate
  detections across input combos are grouped.
- `Simple Checker Detectability = Unlikely` is the most research-relevant bucket:
  it identifies issues that need trace analysis rather than static scanning.
- `P0` and `P1` are the engineering repair queue. `P2` is backlog/verify. `P3`
  should not be escalated without more evidence.
- For aggregate study reporting, compute metrics on both raw detections and
  grouped developer issues. Raw detections answer "what did the model flag";
  grouped issues answer "what should a developer fix."
