# GM2 Developer Accessibility Triage

## Summary
- Total raw detections reviewed: 20
- Grouped developer issues: 4
- P0: 0
- P1: 2
- P2: 1
- P3: 1
- Simple-checker unlikely: 1
- Main repair themes: message body editor accessible naming, WebView focus behavior, persistent field labels, sender account announcement.

## Scope And Method
- Source analysis files: `results/GM2_analysis.md`, `results/GM2_results.csv`
- Trace files consulted: no additional raw trace reads beyond evidence already cited in the trace analysis.
- Grouping rule: detections were grouped when they described the same UI element or interaction, the same user impact, and a likely shared implementation fix.
- Priority rule: priority reflects developer repair urgency, not raw WCAG severity alone. Primary compose-path issues with strong event/user-action/tree evidence are P1; lower-impact or verification-needed issues are P2/P3.
- What this report does not do: it does not create new findings, judge true population-level prevalence, or replace real-device verification.

## Raw Detection Grouping

| Developer Issue ID | Priority | Grouped Title | Raw Detection Count | Source Issue Numbers | Why These Were Grouped |
|---|---|---:|---:|---|---|
| GM2-DEV-1 | P1 | Message body editor exposes unlabeled WebView and unnamed edit field | 8 | Events #1 #2; Trees #1 #2; Events+Actions #1 #2; All Inputs #1 #2 | All eight detections describe the WebView-based compose body failing to expose a clear accessible name/role for the body editing target. |
| GM2-DEV-2 | P1 | WebView wrapper disrupts compose focus order before the body field | 4 | Events #4; Trees #4; Events+Actions #4; All Inputs #4 | These detections describe the same navigation failure: TalkBack lands on an intermediate unlabeled WebView before the editable body. |
| GM2-DEV-3 | P2 | Subject field loses its accessible label after text entry | 4 | Events #3; Trees #3; Events+Actions #3; All Inputs #3 | These detections all describe the Subject field relying on hint text that disappears once the field has content. |
| GM2-DEV-4 | P3 | Sender account value is not announced with the From field | 4 | Events #5; Trees #5; Events+Actions #5; All Inputs #5 | These detections describe the From control omitting the selected sender account from the TalkBack announcement. |

## Priority Issues

### P1 Message body editor exposes unlabeled WebView and unnamed edit field
- Fix Category: Accessible Name
- WCAG: 4.1.2
- Raw Detection Count: 8
- Input Combos: Events only; Trees only; Events + User Actions; Events + User Actions + Trees
- User Impact: A TalkBack user reaches the Gmail compose body area but hears generic announcements such as "Webview, Window Gmail" and "Editing, Edit box" instead of a clear message-body label. This makes it hard to confirm where text will be entered.
- Evidence Strength: Strong
- Evidence Sources: events, user actions, trees
- Simple Checker Detectability: Partial
- Why This Priority: This affects the primary compose workflow and is confirmed across all input types, including user actions that reach the body editor.
- Evidence: Event 72 announces `["Webview, Window Gmail"]`; event 82 announces `["Editing, Edit box"]`; tree `tree_2026-05-26T08-45-35-206` shows the body EditText with empty `contentDescription` and `hint`, plus `isImportantForAccessibility: false`.
- Raw Detections Grouped: Events #1 #2; Trees #1 #2; Events + User Actions #1 #2; Events + User Actions + Trees #1 #2.
- Implementation Notes: The likely implementation issue is split exposure between a WebView wrapper and the actual editable node. A fix should avoid creating two confusing TalkBack targets: one generic wrapper and one unnamed edit field.
- Recommended Fix: Expose one accessible message body editing control with a persistent name such as "Message body" or "Email body". Avoid exposing an unlabeled WebView wrapper as the primary TalkBack target. Ensure the editable node reports the correct role and remains important for accessibility.
- Verification Step: With TalkBack, compose an email and navigate from Subject into the body. The focus announcement should identify the field as the message body and indicate it is editable.
- Residual Risk / Open Question: Real-device behavior should be checked because some WebView/editor focus behavior can differ between emulator and device.

### P1 WebView wrapper disrupts compose focus order before the body field
- Fix Category: Focus Order
- WCAG: 2.4.3
- Raw Detection Count: 4
- Input Combos: Events only; Trees only; Events + User Actions; Events + User Actions + Trees
- User Impact: Standard swipe navigation after the Subject field lands on an unlabeled WebView wrapper instead of the body editor. The user needed repeated navigation and then a direct tap to reach the body field.
- Evidence Strength: Strong
- Evidence Sources: events, user actions, trees
- Simple Checker Detectability: Unlikely
- Why This Priority: The issue appears during the primary compose path and requires trace/user-action evidence to see the disrupted navigation sequence.
- Evidence: User action seq 59 `swipe_right` leads to event 72 `["Webview, Window Gmail"]`; seq 62 `swipe_right` leads to event 81 with the same announcement; the tree shows an inner WebView with `isFocusable: true`, empty `contentDescription`, and `isImportantForAccessibility: false`.
- Raw Detections Grouped: Events #4; Trees #4; Events + User Actions #4; Events + User Actions + Trees #4.
- Implementation Notes: This is related to GM2-DEV-1 but kept separate because the developer fix may require focus-order/focusability changes in addition to naming the editor. If one implementation change fixes both, they can be merged in an engineering tracker.
- Recommended Fix: Remove the unlabeled WebView wrapper from TalkBack focus order or make it route directly to the named body editor. The next swipe after Subject should move to the body edit field, not to a generic intermediate WebView.
- Verification Step: With TalkBack, enter a subject, swipe right once, and confirm focus moves directly to the message body field.
- Residual Risk / Open Question: The trace notes a possible emulator-related typo after the focus disruption. The focus-order issue itself is still supported by repeated TalkBack focus events.

### P2 Subject field loses its accessible label after text entry
- Fix Category: Accessible Name
- WCAG: 3.3.2
- Raw Detection Count: 4
- Input Combos: Events only; Trees only; Events + User Actions; Events + User Actions + Trees
- User Impact: The Subject field is identified as "Subject" before typing, but after text is entered the hint disappears and the programmatic label is no longer present in events/tree evidence.
- Evidence Strength: Strong
- Evidence Sources: events, user actions, trees
- Simple Checker Detectability: Partial
- Why This Priority: The field remains usable but loses persistent labeling after input, which can make review/editing ambiguous.
- Evidence: Event 57 announces `["Subject, Edit box"]`; type events 59-70 show `label: ""`; tree `tree_2026-05-26T08-45-20-847` shows `text: "Hello"`, `isShowingHintText: false`, and empty `contentDescription`.
- Raw Detections Grouped: Events #3; Trees #3; Events + User Actions #3; Events + User Actions + Trees #3.
- Implementation Notes: This is a classic hint-as-label problem. The visible/hint label and the programmatic accessible name should not disappear once the user enters text.
- Recommended Fix: Provide a persistent programmatic label for the Subject EditText that remains available after text entry, instead of relying only on hint text.
- Verification Step: With TalkBack, type a subject, move focus away, then return to the field. The announcement should still identify it as Subject.
- Residual Risk / Open Question: Confirm whether Gmail uses platform text-input semantics that could expose labels differently on a physical device.

### P3 Sender account value is not announced with the From field
- Fix Category: Accessible Name
- WCAG: 4.1.2
- Raw Detection Count: 4
- Input Combos: Events only; Trees only; Events + User Actions; Events + User Actions + Trees
- User Impact: The From control announces only "From" and does not include the active sender email address, so a screen reader user may need to open the dropdown to confirm the sending account.
- Evidence Strength: Medium
- Evidence Sources: events, user actions, trees
- Simple Checker Detectability: Likely
- Why This Priority: The issue is lower severity and manually observed status is unconfirmed, but the tree and event evidence are consistent.
- Evidence: Event 56 announces `["From", "Double-tap to activate"]`; tree `tree_2026-05-26T08-43-42-766` shows `from_account_name` text `manyapbhat@gmail.com` with empty `contentDescription` and `isFocusable: false`.
- Raw Detections Grouped: Events #5; Trees #5; Events + User Actions #5; Events + User Actions + Trees #5.
- Implementation Notes: This may be a design decision if the account is only revealed inside the From dropdown, but a better accessible summary would include the selected account in the collapsed control.
- Recommended Fix: Include the selected sender account in the accessible name or state of the From control, for example "From, manyapbhat@gmail.com".
- Verification Step: Focus the From control with TalkBack and confirm the current sender account is announced without requiring activation.
- Residual Risk / Open Question: Verify whether account disclosure on collapsed From controls is required by product design and whether other mail apps expose this value.

## Lower Priority / Verification Needed
- GM2-DEV-4 should be verified on a real device before escalation because it is low severity and manually observed status is unconfirmed.
- GM2-DEV-3 should be checked after any broader compose-field accessibility fix, because a native text-input labeling change may resolve it alongside other form-field fixes.

## Likely Simple-Checker Findings
- GM2-DEV-4 Sender account value is not announced with the From field: likely detectable if a checker compares visible text/value with the accessible name of the collapsed From control.

## Dynamic Issues Simple Checkers May Miss
- GM2-DEV-2 WebView wrapper disrupts compose focus order before the body field: requires TalkBack navigation sequence evidence.
- GM2-DEV-1 Message body editor exposes unlabeled WebView and unnamed edit field: partially tree-detectable, but the severity depends on actual TalkBack announcements and user navigation.

## Verification Plan
1. Compose a new email with TalkBack enabled.
2. Navigate through From, To, Subject, and body using swipe gestures only.
3. Confirm the message body is announced with a clear name and editable role.
4. Confirm one swipe after Subject lands directly on the body editor, not a generic WebView.
5. Type a subject, move away, return to Subject, and confirm the field is still announced as Subject.
6. Focus the From control and confirm whether the selected sender account is announced.

## Triage Limitations
- The source trace was collected on an emulator, and the original analysis notes emulator input lag.
- The "Hellot" typo is not treated as an accessibility issue in this triage.
- The triage groups detections from an existing analysis; it does not search for new missed issues.
- Real-device verification is still needed before treating P2/P3 items as engineering commitments.

## Needs Layer 1 Review
- None. This triage did not add new raw findings.
