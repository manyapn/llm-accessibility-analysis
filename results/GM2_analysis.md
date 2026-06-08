# GM2 Accessibility Analysis — Gmail Stressful

**Model:** claude-sonnet-4-6
**Prompt Version:** v1.0
**Date:** 2026-05-29

> **Emulator Note:** Multiple browser-side taps were required before actions registered throughout the session (e.g., user_actions seq 10–12, 35–37, 38–40 show 2–3 browser taps before a phone-side action triggers). This pattern is consistent with emulator input lag and is not flagged as an accessibility issue. The "Hellot" subject typo (event 73) may be partially attributable to emulator lag in input/accessibility focus alignment — verify on real device.

---

## GM2 — Events Only

### Issues Found

1. **WebView body editor announced as generic "Webview"**
   - Description: When TalkBack navigates to the email body area, the announcement is "Webview, Window Gmail" with no label identifying this as the email composition field. A blind user cannot determine the purpose of this element.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: Event 72: `class: "android.webkit.WebView"`, `label: "Webview"`, `announcement: ["Webview, Window Gmail"]`
   - Manually Observed: Y

2. **Email body edit field announced without a name**
   - Description: After navigating into the email body, the edit field announces as "Editing, Edit box" with no label. A blind user has no programmatic confirmation they are in the message body field.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: Event 82: `class: "android.widget.EditText"`, `label: "Editing"`, `announcement: ["Editing, Edit box", "Actions available, use Tap with 3 fingers to view"]`
   - Manually Observed: Y

3. **Subject field loses accessible label after typing**
   - Description: The Subject EditText relies solely on hint text for its accessible label. Once text is typed, the hint disappears and the field label is lost — events during and after typing show `label: ""` rather than "Subject".
   - WCAG: 3.3.2 Labels or Instructions (Level A)
   - Severity: Medium
   - Evidence: Event 57: `announcement: ["Subject, Edit box"]`; type events 59–70 show `label: ""` on `resource_id: "com.google.android.gm:id/subject"`
   - Manually Observed: Y

4. **Unexpected focus jump to WebView interrupts compose navigation**
   - Description: After completing subject text ("Hello"), a standard TalkBack swipe-right navigation routes focus to the WebView container (announced as "Webview") instead of the body editor. This occurred twice (events 72 and 81), requiring the user to navigate to the body field twice. A stray "t" was also typed into the subject ("Hellot", event 73) — possibly emulator-related; verify on real device.
   - WCAG: 2.4.3 Focus Order (Level A)
   - Severity: High
   - Evidence: Event 72: focus jumps to `class: "android.webkit.WebView"`, `announcement: ["Webview, Window Gmail"]` after subject typing; event 81: same WebView intercept on second navigation attempt
   - Manually Observed: Y

5. **Sender account email address not announced**
   - Description: The From field announces "From, Double-tap to activate" but the actual account email is not read. A blind user cannot confirm the sending account without activating the From dropdown.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Low
   - Evidence: Event 56: `resource_id: "com.google.android.gm:id/from_label"`, `announcement: ["From", "Double-tap to activate"]` — account email not announced
   - Manually Observed: Unconfirmed

---

## GM2 — Trees Only

### Issues Found

1. **WebView body container has empty contentDescription and isImportantForAccessibility=false**
   - Description: The outer and inner WebView nodes wrapping the email body both have `contentDescription: ""` and `isImportantForAccessibility: false`. TalkBack cannot derive a meaningful label from the tree — the container appears as a generic, unlabeled region.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: tree_2026-05-26T08-45-20-847: body_wrapper > WebView (outer): `contentDescription: ""`, `isImportantForAccessibility: false`; inner WebView: `contentDescription: ""`, `isImportantForAccessibility: false`, `isScreenReaderFocusable: false`
   - Manually Observed: Y

2. **Body EditText is hidden from the screen reader**
   - Description: The editable body field inside the WebView has `isImportantForAccessibility: false`, `isScreenReaderFocusable: false`, and both `contentDescription` and `hint` are empty. TalkBack receives no name or role for this field.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: tree_2026-05-26T08-45-35-206: body EditText `contentDescription: ""`, `hint: ""`, `isImportantForAccessibility: false`, `isScreenReaderFocusable: false`
   - Manually Observed: Y

3. **Subject EditText has no contentDescription — label depends entirely on hint text**
   - Description: Subject EditText has `contentDescription: ""` and uses only `hint: "Subject"` for its accessible name. After text is entered, `isShowingHintText` becomes false and the field has no persistent programmatic label.
   - WCAG: 3.3.2 Labels or Instructions (Level A)
   - Severity: Medium
   - Evidence: tree_2026-05-26T08-44-48-094: subject `contentDescription: ""`, `hint: "Subject"`, `isShowingHintText: true`; tree_2026-05-26T08-45-20-847: `text: "Hello"`, `contentDescription: ""`, `isShowingHintText: false`
   - Manually Observed: Y

4. **Inner WebView intercepts TalkBack focus order despite carrying no accessible name**
   - Description: The inner WebView node is `isFocusable: true` but has `isImportantForAccessibility: false` and `contentDescription: ""`. This creates a navigable-but-silent waypoint in the compose focus order between the subject field and the body editor.
   - WCAG: 2.4.3 Focus Order (Level A)
   - Severity: High
   - Evidence: tree_2026-05-26T08-43-42-766: inner WebView `isFocusable: true`, `contentDescription: ""`, `isImportantForAccessibility: false`, `isScreenReaderFocusable: false` — positioned between subject and body in the view hierarchy
   - Manually Observed: Y

5. **From account email value is not focusable or labeled**
   - Description: The from_account_name TextView showing the sender email has `isFocusable: false` and `contentDescription: ""`. It is not reachable independently by TalkBack, so the sender email is invisible to screen reader users.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Low
   - Evidence: tree_2026-05-26T08-43-42-766: `from_account_name` `text: "manyapbhat@gmail.com"`, `contentDescription: ""`, `isFocusable: false`
   - Manually Observed: Unconfirmed

---

## GM2 — Events + User Actions

### Issues Found

1. **WebView body editor announced as "Webview" — confirmed triggered by standard swipe navigation**
   - Description: User action seq 59 (swipe_right, action_index 18 at t=129064ms) triggers a focus event to the WebView body container, which announces "Webview, Window Gmail" with no descriptive label. Standard TalkBack swipe navigation reliably produces this unlabeled announcement.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: user_actions seq 59: `action: "swipe_right"`, `action_index: 18`; event 72: `announcement: ["Webview, Window Gmail"]`
   - Manually Observed: Y

2. **Email body edit field has no accessible name — confirmed by direct tap**
   - Description: User actions seq 65 (tap, action_index 20) and seq 66 (click on EditText, action_index 21) explicitly target the body EditText. On gaining focus, it announces only "Editing, Edit box" — no name identifying it as the message body field.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: user_actions seq 65-66: click on android.widget.EditText (action_index 20-21); event 82: `announcement: ["Editing, Edit box", "Actions available, use Tap with 3 fingers to view"]`
   - Manually Observed: Y

3. **Subject field label lost during and after typing**
   - Description: User action seq 43 (tap H key at t=101182ms) begins subject entry. Type events 59–70 show the subject EditText with `label: ""` throughout typing — the "Subject" label from the initial focus (event 57) is not maintained while text is being entered.
   - WCAG: 3.3.2 Labels or Instructions (Level A)
   - Severity: Medium
   - Evidence: Event 57: `announcement: ["Subject, Edit box"]`; type events 59–70: `resource_id: "com.google.android.gm:id/subject"`, `label: ""`; user_actions seq 43: `action: "tap"` on keyboard key
   - Manually Observed: Y

4. **Two swipe-right actions required to reach body field — focus order disrupted by WebView**
   - Description: User_actions seq 59 and 62 (both swipe_right, action_indices 18 and 19) both route TalkBack to the WebView container instead of the body editor. A direct tap (seq 63-64, action_index 20) was then required to reach the body field, confirming the user had to navigate twice. The "Hellot" character error (event 73, user_action seq 60 tapping "t" at t=133166ms while body had not yet received input focus) may be emulator-related — verify on real device.
   - WCAG: 2.4.3 Focus Order (Level A)
   - Severity: High
   - Evidence: user_actions seq 59 (`swipe_right`, action_index 18) → event 72 `announcement: ["Webview, Window Gmail"]`; seq 62 (`swipe_right`, action_index 19) → event 81 `announcement: ["Webview, Window Gmail"]`; seq 65-66 (tap/click, action_index 20-21) → event 82 `announcement: ["Editing, Edit box"]`
   - Manually Observed: Y

5. **From account email not announced when From field receives focus**
   - Description: User action seq 41-42 (tap + click on from_label, action_index 14 at t=99171ms) focuses the From field. TalkBack announces "From, Double-tap to activate" — the current account email is not included in the announcement.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Low
   - Evidence: user_actions seq 41: `action_index: 14`, `class: "android.widget.TextView"`, `text: "From"`; event 56: `announcement: ["From", "Double-tap to activate"]`
   - Manually Observed: Unconfirmed

---

## GM2 — Events + User Actions + Trees

### Issues Found

1. **WebView body area: unlabeled container confirmed across all signals**
   - Description: The Gmail email body is implemented as a WebView-based editor. TalkBack announces it as "Webview, Window Gmail" with no role or purpose label. The tree confirms all WebView nodes have empty contentDescription and isImportantForAccessibility=false. Standard swipe navigation (user_action seq 59, swipe_right) reliably triggers this unlabeled focus event.
   - WCAG: 4.1.2 Name, Role, Value (Level A); 1.1.1 Non-text Content (Level A)
   - Severity: High
   - Evidence: event 72: `announcement: ["Webview, Window Gmail"]`; user_actions seq 59: `action: "swipe_right"`, action_index 18; tree_2026-05-26T08-45-20-847 body_wrapper WebView: `contentDescription: ""`, `isImportantForAccessibility: false`
   - Manually Observed: Y

2. **Email body EditText fully inaccessible to screen reader — confirmed by tree and events**
   - Description: The body edit field (inside WebView) has isImportantForAccessibility=false, isScreenReaderFocusable=false, and no contentDescription or hint. When finally reached via direct tap (user_action seq 65-66, action_index 20-21), TalkBack announces only "Editing, Edit box" — no name or role description. A blind user cannot confirm they are in the body field.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: tree_2026-05-26T08-45-35-206: body EditText `contentDescription: ""`, `hint: ""`, `isImportantForAccessibility: false`, `isScreenReaderFocusable: false`; event 82: `announcement: ["Editing, Edit box"]`; user_actions seq 65-66: action_index 20-21
   - Manually Observed: Y

3. **Subject field accessible label lost after typing — hint-only labeling confirmed by tree**
   - Description: Subject EditText has no contentDescription (confirmed in tree). Its only accessible name is hint text "Subject" (isShowingHintText=true pre-typing). After "Hello" is typed, isShowingHintText=false and contentDescription remains empty — the label is gone. Events confirm: label="" throughout typing vs. "Subject, Edit box" on initial focus.
   - WCAG: 3.3.2 Labels or Instructions (Level A)
   - Severity: Medium
   - Evidence: tree_2026-05-26T08-44-48-094: `contentDescription: ""`, `hint: "Subject"`, `isShowingHintText: true`; tree_2026-05-26T08-45-20-847: `text: "Hello"`, `isShowingHintText: false`; event 57: `announcement: ["Subject, Edit box"]`; type events 59–70: `label: ""`
   - Manually Observed: Y

4. **Compose focus order disrupted: WebView intercepts swipe navigation — two attempts required**
   - Description: Two standard TalkBack swipe-right actions (user_actions seq 59, 62; action_indices 18, 19) both land on the WebView container instead of the body editor. The tree confirms the inner WebView is isFocusable=true but isImportantForAccessibility=false with no accessible name, creating a navigable silent waypoint. A direct tap was required to reach the body field. A "Hellot" typo (event 73) resulted from input/accessibility focus misalignment — verify on real device.
   - WCAG: 2.4.3 Focus Order (Level A)
   - Severity: High
   - Evidence: user_actions seq 59 (`swipe_right`, action_index 18) → event 72 `announcement: ["Webview, Window Gmail"]`; seq 62 (`swipe_right`, action_index 19) → event 81 `announcement: ["Webview, Window Gmail"]`; tree: inner WebView `isFocusable: true`, `isImportantForAccessibility: false`, `contentDescription: ""`
   - Manually Observed: Y

5. **From sender email address not reachable by TalkBack — confirmed by tree**
   - Description: The from_account_name TextView (showing "manyapbhat@gmail.com") has contentDescription="" and isFocusable=false in the tree. When user action seq 41-42 focuses the From field (action_index 14), TalkBack announces only "From, Double-tap to activate" — the sender email is never read. A blind user must activate the From dropdown to discover the sending account.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Low
   - Evidence: tree_2026-05-26T08-43-42-766: `from_account_name` `contentDescription: ""`, `isFocusable: false`, `text: "manyapbhat@gmail.com"`; event 56: `announcement: ["From", "Double-tap to activate"]`
   - Manually Observed: Unconfirmed
