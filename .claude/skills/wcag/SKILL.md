---
name: wcag
description: WCAG 2.2 accessibility guidelines reference for mobile app analysis. Use when identifying, categorizing, or explaining accessibility issues found in TalkBack screen reader traces.
---

# WCAG 2.2 Mobile Accessibility Reference

## Full WCAG 2.2 Understanding Documents
The complete WCAG 2.2 understanding docs are in the `understanding/` folder in this skill directory, one file per success criterion. Consult relevant files to accurately cite criterion number, level (A/AA/AAA), and intent.

Full index: https://www.w3.org/WAI/WCAG22/Understanding/

---

## Do NOT Flag These (Emulator Artifacts)
- EditText zero-size bounds `{w:0, h:0}` during typing
- Multiple browser taps / triple-tap patterns before action registers
- Repeated punctuation or comma sequences in announcements
- Accidental speech rate or TalkBack setting changes

---

## Quick Reference: What to Flag in TalkBack Traces

| Signal in Trace | Likely WCAG Violation |
|---|---|
| `label: ""` on interactive element | 1.1.1, 4.1.2 |
| `announcement: ["<no_feedback>"]` | 1.1.1, 4.1.2 |
| `role: ""` on interactive element | 4.1.2 |
| Generic class (LinearLayout, View) used as button | 4.1.2, 1.3.1 |
| `isFocusable=false` on interactive element | 2.1.1 |
| `contentDescription=""` on meaningful element | 4.1.2 |
| Repeated identical announcements for different elements | 2.4.4 |
| Focus jumps unexpectedly | 2.4.3 |
| State (checked, selected, expanded) not in announcement | 4.1.2 |
| Status change with no announcement event | 4.1.3 |
| Context change on focus without activation | 3.2.1 |
| EditText with no label | 3.3.2, 1.3.5 |
| Focus trapped on same element repeatedly | 2.1.2 |
| Interactive element never receives focus in full session | 2.1.1 |
| Error state with no TalkBack announcement | 3.3.1 |
| Button visible label doesn't match announced label | 2.5.3 |
| Interactive target smaller than 24x24dp | 2.5.8 |

---

## Output Format Per Issue
1. Short descriptive title
2. WCAG 2.2 criterion (number + name + level)
3. Severity: Low / Medium / High
4. Evidence quoted directly from trace
5. Manually Observed: Y / N / Unconfirmed

Keep output concise. Do not overcomplicate. Do not flag emulator artifacts.
