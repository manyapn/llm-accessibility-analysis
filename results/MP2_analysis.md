# MP2 — Google Maps, Stressful Task: Start directions from current location to Space Needle, inspect route options, stop before tapping Start

**Model:** claude-sonnet-4-6 | **Prompt Version:** v1.0 | **Date:** 2026-05-28

---

> **Emulator Note:** Multiple browser taps observed before phone action registrations throughout the session (e.g., user_action seqs 1–3: 3 browser taps before phone tap; seqs 6–8, 11–14, 16–18, 22–24, 27–29, 35–36, 40–42: repeated browser taps before each phone action). This is consistent with emulator input lag and is not flagged as an accessibility issue. Individual findings are assessed for real-device relevance.

---

## MP2 — Events Only

### Issues Found

1. **Unlabeled search omnibox container announces "Unlabelled" to TalkBack**
   - Description: When the routes screen loads after the user taps "Directions to Space Needle," TalkBack focuses on `com.google.android.apps.maps:id/search_omnibox_container` — a FrameLayout with zero height — and announces "Unlabelled, Out of list." This provides no useful information to a blind user. The element immediately receives focus before the routes UI is fully rendered, and TalkBack reads its missing label rather than skipping it.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Medium
   - Evidence: Event seq 4: `resource_id: "com.google.android.apps.maps:id/search_omnibox_container"`, `class: "android.widget.FrameLayout"`, `label: "Unlabelled"`, `bounds: {w:1080, h:0}`, `announcement: ["Unlabelled, Out of list", "Start location, Choose start location, Destination, Space Needle"]`
   - Manually Observed: Unconfirmed

2. **TalkBack focus unexpectedly jumps to Android home screen launcher mid-task**
   - Description: While the user is on the route options screen browsing transport mode tabs in Maps, TalkBack focus abruptly jumps to `com.google.android.apps.nexuslauncher:id/date` — the system clock/date widget on the Android home screen launcher. The announcement mixes Maps route context ("Ride service: 36 min, 35 min, selected, Showing item 4 of 5.") with home screen content ("Home, Tue, May 26"). This completely disorients a blind user who is mid-task comparing transport modes. A second focus jump to the launcher occurs at event seqs 32–33 (~47 seconds later).
   - WCAG: 2.4.3 Focus Order — Level A
   - Severity: High
   - Evidence: Event seq 19: `resource_id: "com.google.android.apps.nexuslauncher:id/date"`, `class: "android.widget.TextView"`, `label: "Ride service: 36 min"`, `announcement: ["Ride service: 36 min", "35 min", "selected", "Showing item 4 of 5.", "Home", "Tue, May 26", "Double-tap to activate"]`. Event seqs 32–33 show second launcher focus jump: announcement `["Home", "Predicted app: Maps, Out of list", ...]`.
   - Manually Observed: Unconfirmed

3. **Mode tab selection triggers redundant, fragmented announcements**
   - Description: When the user selects a transport mode tab (Transit, Walking), TalkBack fires three separate announcement events in quick succession: (1) a focus announcement with the mode name and duration, (2) a duration-only announcement without mode context, then (3) a "selected" state confirmation. The standalone duration fragments — "1 hr 31" (seq 11) and "8 hr" (seq 15) — have no mode context and would confuse a user navigating quickly. This appears to be a live region firing separately from the focus announcement.
   - WCAG: 4.1.3 Status Messages — Level AA
   - Severity: Low
   - Evidence: Seq 10 (focus): `announcement: ["Transit mode: 1 hr 31", "Double-tap to activate"]`. Seq 11 (announcement): `["1 hr 31", "Transit mode: 1 hr 31"]`. Seq 12 (announcement): `["Transit mode: 1 hr 31", "Page 2 of 5", "selected"]`. Same three-event pattern at seqs 14–16 for Walking mode: "8 hr," "Walking mode: 8 hr," "Walking mode: 8 hr, Page 3 of 5, selected."
   - Manually Observed: Unconfirmed

4. **Unlabeled full-screen interactive View announces "Unlabelled"**
   - Description: After the user selects Space Needle from autocomplete and is returned to the route start screen, TalkBack focuses on a full-screen `android.view.View` (covering 1080×2337 pixels) with `label: "Unlabelled"` and announces "Unlabelled, Double-tap to activate." A blind user is presented with a large interactive element offering no description of its purpose or what activating it would do.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Medium
   - Evidence: Event seq 26: `class: "android.view.View"`, `label: "Unlabelled"`, `bounds: {x:0, y:0, w:1080, h:2337}`, `announcement: ["Unlabelled", "Double-tap to activate"]`
   - Manually Observed: Unconfirmed

---

## MP2 — Trees Only

### Issues Found

1. **"Steps" navigation button has empty contentDescription**
   - Description: The "Steps" button in the route options footer (`com.google.android.apps.maps:id/persistent_footer_secondary_button`) is a clickable, focusable `android.widget.Button` with `contentDescription: ""` and no text at the Button level. Its child `android.view.View` has `text: "Steps"` but also `contentDescription: ""`. TalkBack cannot derive any accessible name for this button. When focused, the button would announce only the generic role and gesture instruction ("Button, double-tap to activate") with no indication of its purpose. The "Steps" button provides access to turn-by-turn directions — a critical navigation function.
   - WCAG: 4.1.2 Name, Role, Value — Level A / 1.1.1 Non-text Content — Level A
   - Severity: High
   - Evidence: `tree_2026-05-26T17-24-06-015.json`: `android.widget.Button` `(persistent_footer_secondary_button)`, `contentDescription: ""`, `text: ""`, `isClickable: true`, `isFocusable: true`. Child `android.view.View`: `text: "Steps"`, `contentDescription: ""`.
   - Manually Observed: Unconfirmed

2. **Alternate route map overlays are unreachable via TalkBack**
   - Description: Two `android.view.View` elements on the driving directions map represent selectable alternate routes: "Alternate route 36 min via E Lake Sammamish Pkwy NE and WA-520 W, has $3.95 tolls" and "Alternate route 41 min via I-90 W, no tolls." Both have `isImportantForAccessibility: false`, which excludes them from TalkBack's linear navigation. Despite having descriptive `contentDescription` values and `isFocusable: true`, a blind user cannot reach or select these alternate routes using swipe navigation. Only the primary route is accessible, silently limiting route comparison for TalkBack users.
   - WCAG: 2.1.1 Keyboard — Level A
   - Severity: High
   - Evidence: `tree_2026-05-26T17-24-06-015.json`: `android.view.View`, `contentDescription: "Alternate route 36 min via E Lake Sammamish Pkwy NE and WA-520 W, has $3.95 tolls"`, `isImportantForAccessibility: false`, `isFocusable: true`, `isClickable: false`. Same for `"Alternate route 41 min via I-90 W, no tolls"`.
   - Manually Observed: Unconfirmed

---

## MP2 — Events + User Actions

### Issues Found

No new unique issues identified beyond those found in Combo 1 (Events only). All four issues (unlabeled container, launcher focus jump, fragmented mode announcements, unlabeled full-screen View) are confirmed with additional context from user actions:

- **Issue 2 (launcher focus jump) — trigger clarified:** User action data shows that the launcher focus jump (event seq 19) follows browser taps at coordinates (936, 480) and (949, 471) (user_action seqs 32–33). The Bicycling mode tab occupies bounds x:941–1080 in the tree. These taps land at or just past the right edge of the visible transport mode tab row. The sequence suggests that pressing near the off-screen or partially clipped Bicycling mode tab edge causes TalkBack focus to exit Maps and land on the launcher. This is not emulator lag — the phone then re-opens Maps (user_action seq 37–38) confirming the focus left the app entirely.

- **Issue 1 (unlabeled container) — confirmed:** User action seq 9 (phone tap action_index 7) triggers the routes screen where event seq 4 shows the unlabeled FrameLayout. The user actively navigated to the routes screen; this is not a transient artifact.

---

## MP2 — Events + User Actions + Trees

### Issues Found

1. **Transit route trip cards have empty contentDescription, producing verbose duplicate announcements**
   - Description: All `com.google.android.apps.maps:id/directions_trip_card` elements — clickable, focusable FrameLayouts representing individual transit route options — have `contentDescription: ""`. TalkBack must construct the accessible name by compositing child element text. The result is an extremely verbose announcement sequence (event seq 13 spans the full route card including "transit directions, Page, 2 of 23, In list, 23 items," route details, and then "2 of 23, In list, 23 items" and "Double-tap to activate, Double-tap to activate" repeated twice each). The duplicated position information and gesture instruction indicate an incomplete accessible name construction that would confuse a blind user navigating a list of 23 route options.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Medium
   - Evidence: `tree_2026-05-26T17-24-22-806.json`: `directions_trip_card` (android.widget.FrameLayout), `contentDescription: ""`, `isClickable: true`, `isFocusable: true`, `collectionItemInfo: {rowIndex:1}`. Cross-ref: Event seq 13: `announcement: ["transit directions, Page, 2 of 23, In list, 23 items", "Drive for 17 min, then Bus, ​545, then Monorail, ​Monorail, 1 hour 2 minutes, Leave by 10:27 AM · Light traffic, in 25 min (scheduled), 40 min (on time) from SR-520 at NE 40th St, 2 of 23, In list, 23 items", "Double-tap to activate", "Double-tap to activate"]`
   - Manually Observed: Unconfirmed

**Cross-combo confirmations (no new issues added):**
- **Issue 5 (Steps button empty label) confirmed:** Events show no TalkBack announcement for the Steps button throughout the session. Tree confirms `persistent_footer_secondary_button contentDescription: ""`. Combined evidence is conclusive.
- **Issue 6 (alternate routes inaccessible) confirmed:** Tree confirms `isImportantForAccessibility: false` on both alternate route views. Events never show TalkBack focusing on any alternate route map label. User never hears "Alternate route 41 min via I-90 W" — consistent with exclusion from the accessibility tree.
- **Issues 1, 2, 3, 4 (Events only issues) confirmed:** All visible across events, cross-referenced to relevant tree states.
