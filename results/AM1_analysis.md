# AM1 — Amazon Core

**Task:** Search "wireless headphones" and open the first product detail page.

---

## AM1 — Events Only

### Emulator Note
Emulator lag observed: multiple browser taps before phone-side actions register throughout the session (e.g., user_actions seq 1–5: 5 browser taps before phone tap registers; seq 55–68: 14 rapid browser taps at the same coordinates). Focus cycling in the filter area also produced many repeated swipe-right gestures. These patterns are documented as emulator artifacts and are not flagged as accessibility issues.

### Issues Found

1. **Back button announces `<no_feedback>` on product page**
   - Description: The Back ImageButton (`chrome_action_bar_back_icon`) has an empty label and emits `<no_feedback>`, giving a blind user no information that a Back control is available.
   - WCAG: 1.1.1 Non-text Content (Level A); 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 21 — `resource_id: com.amazon.mShop.android.shopping:id/chrome_action_bar_back_icon`, `label: ""`, `announcement: ["<no_feedback>"]`
   - Manually Observed: N

2. **Back button announces full product page content instead of its own label**
   - Description: On the same element as Issue 1, TalkBack immediately announces a massive block of product highlights content ("Top highlights--content, Bullet, Bullet … About this item … Back, Button"). The Back button's accessible name is polluted with the WebView page content, making it impossible to determine the button's purpose without listening through a long announcement.
   - WCAG: 4.1.2 Name, Role, Value (Level A); 2.4.4 Link Purpose (Level A)
   - Severity: High
   - Evidence: event_seq 22 — `label: "Top highlights--content"`, announcement: `["Top highlights--content","Bullet","Bullet","Bullet","Bullet","Bullet","Top highlights"..."Back, Button","Double-tap to activate"]`
   - Manually Observed: N

3. **Search box announces only "Double-tap to activate" — no accessible name**
   - Description: The Amazon search box (`chrome_search_box`, ImageButton) announces only the activation instruction with no accessible name, leaving a blind user unable to identify the purpose of the control.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Medium
   - Evidence: event_seq 23 — `resource_id: com.amazon.mShop.android.shopping:id/chrome_search_box`, `label: "Double-tap to activate"`, `announcement: ["Double-tap to activate"]`
   - Manually Observed: N

4. **Multiple filter chips announce "Double-tap to activate" with no accessible name**
   - Description: Many filter chip elements in the horizontal filter strip (e.g., "Get It Fast", "Get It by Tomorrow", "All Discounts", "$20 to $35") announce only "Double-tap to activate" when focused. The accessible name is absent at focus time; in several cases a deferred announcement then provides the name, but a blind user who acts before the second announcement has no context for what they are activating.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 78 — `resource_id: gif`, `label: "Double-tap to activate"`, `announcement: ["Double-tap to activate"]`; event_seq 80 — `resource_id: 8308921011`, same pattern; event_seq 82 — `resource_id: 23566065011`, same; event_seq 84 — `resource_id: 23566064011`, same; event_seq 88 — `resource_id: 1253505011`, same.
   - Manually Observed: N

5. **All Filters button emits `<no_feedback>`**
   - Description: The "All Filters Icon" button (`s-all-filters-announce`) transitions to an empty label and emits `<no_feedback>` during navigation. The same button alternates between announcing "All Filters Icon", "close", empty, and "Double-tap to activate" within seconds, making it unreliable for blind users.
   - WCAG: 1.1.1 Non-text Content (Level A); 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 106 — `resource_id: s-all-filters-announce`, `label: ""`, `announcement: ["<no_feedback>"]`. Surrounding events: seq 105 announces "All Filters Icon, button"; seq 108 announces "close, button"; seq 109 announces "All Filters Icon, button" — all on the same element within 4 seconds.
   - Manually Observed: N

6. **TalkBack focus cycling between All Filters and close button — possible focus trap**
   - Description: After activating a filter in the horizontal filter strip, TalkBack focus cycles between the "All Filters Icon" button and an unnamed close button repeatedly. The session ends with the user unable to navigate to any product. This matches the manually observed issue: focus stuck on filter chips with no path to products.
   - WCAG: 2.1.2 No Keyboard Trap (Level A)
   - Severity: High
   - Evidence: events 101–109 (spanning ~65 seconds): `s-all-filters-announce` ("All Filters Icon") → close button → "All Filters Icon" → close → "All Filters Icon" → `<no_feedback>` → "Double-tap to activate" → "close, button" → "All Filters Icon". Task was never completed (no product detail page reached).
   - Manually Observed: Y

7. **Zero-height close button receives TalkBack focus**
   - Description: A button labeled "close" with bounds `{w:118, h:0}` — zero height, visually hidden — nonetheless receives TalkBack accessibility focus. This creates an unexpected element in the focus order that a sighted user cannot see.
   - WCAG: 2.4.3 Focus Order (Level A)
   - Severity: Medium
   - Evidence: event_seq 102 — `class: android.widget.Button`, `label: "close"`, `bounds: {x:945, y:294, w:118, h:0}`, `announcement: ["close, button","Double-tap to activate"]`; also event_seq 104.
   - Manually Observed: N

8. **Search suggestion row announces its full accessible name twice in sequence**
   - Description: When a search suggestion row receives focus, TalkBack announces the full label text repeated verbatim twice (e.g., "wireless keyboard and mouse append suggestion wireless keyboard and mouse, wireless keyboard and mouse append suggestion wireless keyboard and mouse"). This is unnecessarily verbose and disorienting.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Low
   - Evidence: event_seq 58 — `resource_id: sac-suggestion-row-2`, `label: "wireless keyboard and mouse append suggestion wireless keyboard and mouse"`, announcement: `["wireless keyboard and mouse append suggestion wireless keyboard and mouse, wireless keyboard and mouse append suggestion wireless keyboard and mouse","Double-tap to activate"]`
   - Manually Observed: N

---

## AM1 — Trees Only

### Emulator Note
Emulator lag noted (see Events Only section). Trees reflect UI state at discrete snapshots.

### Issues Found

9. **Close button in full filter panel uses URL query string as contentDescription**
   - Description: The close/dismiss button at the top of the full-screen "All Filters" panel has `contentDescription: "s?k=wireless+headphones&rh=p_36%3A1500-2000&dc&crid=2T85DA9I"` — a raw URL query string — instead of a meaningful label such as "Close filters". A blind user navigating to this button would hear an unintelligible query string.
   - WCAG: 1.1.1 Non-text Content (Level A); 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: tree_2026-05-26T17-16-48-445.json — `android.view.View` at bounds `{left:1018, top:322, right:1052, bottom:391}`, `text: ""`, `contentDescription: "s?k=wireless+headphones&rh=p_36%3A1500-2000&dc&crid=2T85DA9I"`
   - Manually Observed: N

10. **All interactive elements in full filter panel have `isImportantForAccessibility: false`**
    - Description: Every clickable/focusable element inside the full-screen filters panel (filter option chips, Clear Filters button, Show Results button) has `isImportantForAccessibility: false` and `isScreenReaderFocusable: false`. Despite these flags, TalkBack does navigate to them via WebView accessibility mode. This inconsistency means standard accessibility auditing tools would report the panel as inaccessible, while TalkBack behavior differs unpredictably.
    - WCAG: 4.1.2 Name, Role, Value (Level A); 1.3.1 Info and Relationships (Level A)
    - Severity: Medium
    - Evidence: tree_2026-05-26T17-16-48-445.json — all filter chip `android.view.View` elements: `isImportantForAccessibility: false`, `isScreenReaderFocusable: false`; examples: `rid: "p_72/1248879011"` ("Apply 4 Stars & Up"), `rid: "preference_pill/mps"` ("Apply Most Purchased"), `rid: "preference_pill/gif"` ("Apply Get It Fast")
    - Manually Observed: N

11. **Filter chips in horizontal strip have no explicit `contentDescription` — rely solely on `text` field**
    - Description: Filter chip elements in the search results filter strip (both the "Global refinements" and "Query specific refinements" ListViews) have `contentDescription: ""` and rely on the `text` field alone for their accessible name. While TalkBack does read the text field as a fallback, the absence of an explicit `contentDescription` creates fragility — as demonstrated in events where the same elements announce `<no_feedback>` or "Double-tap to activate" when their text is dynamically unavailable.
    - WCAG: 4.1.2 Name, Role, Value (Level A)
    - Severity: Low
    - Evidence: tree_2026-05-26T17-15-10-511.json — ListView "Global refinements" items: `android.view.View` with `contentDescription: ""`, `text: "Apply Most Purchased filter to narrow results"` / `"Apply 4 Stars & Up filter to narrow results"` / `"Apply Get It Fast filter to narrow results"`. Prime Filter button: `contentDescription: ""`, `text: "Prime Filter, unselected"`.
    - Manually Observed: N

---

## AM1 — Events + User Actions

### Emulator Note
Emulator lag confirmed by user_actions: repeated browser taps before phone-side actions register throughout the session. Notable: user_actions seq 55–68 contains 14 rapid browser taps at coordinates (1024, 2039) — all part of emulator lag while typing. Additionally, seq 133–145 shows 11 repeated taps at (292, 2011). These are emulator artifacts. The filter area interactions (seq 146–205) reflect genuine interaction attempts and are not emulator lag.

### Issues Found

1. **Back button announces `<no_feedback>` on product page** *(see Events Only Issue 1)*
   - Severity: High | WCAG: 1.1.1, 4.1.2 | Manually Observed: N
   - User actions context: No corresponding explicit user action for this — focus arrived here via TalkBack swipe navigation.

2. **Back button announces full product page content instead of its own label** *(see Events Only Issue 2)*
   - Severity: High | WCAG: 4.1.2, 2.4.4 | Manually Observed: N
   - User actions context: event linked to action_index 28 (swipe_left in user_actions seq 42).

3. **Search box announces only "Double-tap to activate"** *(see Events Only Issue 3)*
   - Severity: Medium | WCAG: 4.1.2 | Manually Observed: N

4. **Multiple filter chips announce "Double-tap to activate" with no accessible name** *(see Events Only Issue 4)*
   - Severity: High | WCAG: 4.1.2 | Manually Observed: N
   - User actions context: User_actions seq 121–131 show the user performing swipe-right through filter chips (action_index 63–76), confirming these focus events match intentional forward navigation through the filter strip.

5. **All Filters button emits `<no_feedback>`** *(see Events Only Issue 5)*
   - Severity: High | WCAG: 1.1.1, 4.1.2 | Manually Observed: N

6. **TalkBack focus cycling between All Filters and close button — confirmed focus trap**
   - Description: User_actions confirm the focus trap: after the user clicks filter `1253505011` (Apply $15–$20, user_actions seq 172), the subsequent events (101–109) show focus cycling between All Filters and close. The user then attempts 20+ repeated taps and swipe gestures (seq 173–205) in the filter area without success. Session ends without reaching a product — task not completed.
   - WCAG: 2.1.2 No Keyboard Trap (Level A)
   - Severity: High
   - Evidence: user_actions seq 172: `click resource_id: 1253505011 (Apply $15 to $20 filter)` → events 101–109: focus loops between All Filters and close button for the remainder of the session.
   - Manually Observed: Y

7. **Zero-height close button receives TalkBack focus** *(see Events Only Issue 7)*
   - Severity: Medium | WCAG: 2.4.3 | Manually Observed: N
   - User actions context: user_actions seq 178–179 show user clicking the close button (action_index 98, 99), which matches event 102.

8. **Search suggestion row announces full label text twice** *(see Events Only Issue 8)*
   - Severity: Low | WCAG: 4.1.2 | Manually Observed: N
   - User actions context: user_actions seq 89–101 show the user performing swipe-right to navigate forward through suggestion rows, confirming these are intentional focus events.

---

## AM1 — Events + User Actions + Trees

### Emulator Note
Same as Events + User Actions section above.

### Issues Found

1. **Back button announces `<no_feedback>` on product page**
   - Description: Same as Events Only Issue 1. Confirmed by tree: tree_2026-05-26T17-12-54-889.json shows `chrome_action_bar_back_icon` with `contentDescription: "Back"` — yet TalkBack announces `<no_feedback>` in the corresponding event (seq 21). The discrepancy between tree (has "Back") and event (`<no_feedback>`) indicates a transient state where the accessible name is dropped, possibly during page load.
   - WCAG: 1.1.1 Non-text Content (Level A); 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 21 — `announcement: ["<no_feedback>"]`; tree_2026-05-26T17-12-54-889.json: same element has `contentDescription: "Back"`.
   - Manually Observed: N

2. **Back button announces full product page content instead of its own label**
   - Description: Same as Events Only Issue 2. Tree context: the product detail page (tree_2026-05-26T17-12-54-889.json, resource id `dp`) contains the product highlights section. The Back button's accessible name was overridden by the WebView page content.
   - WCAG: 4.1.2 Name, Role, Value (Level A); 2.4.4 Link Purpose (Level A)
   - Severity: High
   - Evidence: event_seq 22 — `label: "Top highlights--content"`, full product page announcement; tree confirms the product highlights content is in the same WebView window.
   - Manually Observed: N

3. **Search box announces only "Double-tap to activate"**
   - Description: Same as Events Only Issue 3. Tree confirms `chrome_search_box` has `contentDescription: "Search"` in tree_2026-05-26T17-12-57-006.json, yet the event shows only "Double-tap to activate". Same transient name-drop pattern as Issue 1.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Medium
   - Evidence: event_seq 23 — `announcement: ["Double-tap to activate"]`; tree: `contentDescription: "Search"`.
   - Manually Observed: N

4. **Multiple filter chips announce "Double-tap to activate" with no accessible name**
   - Description: Same as Events Only Issue 4. Tree context: tree_2026-05-26T17-15-10-511.json shows these chips as `android.view.View` list items with `text` fields set but `contentDescription: ""`. The transient `<no label>` state in events occurs when `text` field is not yet rendered.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 78, 80, 82, 84, 88 — `announcement: ["Double-tap to activate"]`; tree: same elements have text "Apply Get It Fast filter to narrow results" etc.
   - Manually Observed: N

5. **All Filters button emits `<no_feedback>`**
   - Description: Same as Events Only Issue 5. Tree context: tree_2026-05-26T17-15-10-511.json shows `s-all-filters-announce` with `text: "All Filters Icon"` and `contentDescription: ""`. The `<no_feedback>` in event_seq 106 occurs when even the text field becomes empty during a UI transition.
   - WCAG: 1.1.1 Non-text Content (Level A); 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 106 — `label: ""`, `announcement: ["<no_feedback>"]`; tree: `contentDescription: ""`, `text: "All Filters Icon"`.
   - Manually Observed: N

6. **TalkBack focus cycling between All Filters and close button — confirmed focus trap**
   - Description: Same as Events + User Actions Issue 6. Tree context: the close button in the full filter panel (tree_2026-05-26T17-16-48-445.json) has a URL query string as its contentDescription, contributing to the confusing cycling experience.
   - WCAG: 2.1.2 No Keyboard Trap (Level A)
   - Severity: High
   - Evidence: events 101–109 + user_actions seq 172–205 confirm cycling; tree: close button has `contentDescription: "s?k=wireless+headphones&rh=..."`.
   - Manually Observed: Y

7. **Zero-height close button receives TalkBack focus**
   - Description: Same as Events Only Issue 7.
   - WCAG: 2.4.3 Focus Order (Level A)
   - Severity: Medium
   - Evidence: event_seq 102 — `bounds: {x:945, y:294, w:118, h:0}`, `label: "close"`.
   - Manually Observed: N

8. **Search suggestion row announces full label text twice**
   - Description: Same as Events Only Issue 8.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Low
   - Evidence: event_seq 58 — label repeated twice in announcement.
   - Manually Observed: N

9. **Close button in full filter panel uses URL query string as contentDescription**
   - Description: Same as Trees Only Issue 9.
   - WCAG: 1.1.1 Non-text Content (Level A); 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: tree_2026-05-26T17-16-48-445.json — close button `contentDescription: "s?k=wireless+headphones&rh=p_36%3A1500-2000&dc&crid=2T85DA9I"`.
   - Manually Observed: N

10. **All interactive elements in full filter panel have `isImportantForAccessibility: false`**
    - Description: Same as Trees Only Issue 10.
    - WCAG: 4.1.2 Name, Role, Value (Level A); 1.3.1 Info and Relationships (Level A)
    - Severity: Medium
    - Evidence: tree_2026-05-26T17-16-48-445.json — all filter panel elements: `isImportantForAccessibility: false`, `isScreenReaderFocusable: false`.
    - Manually Observed: N

11. **Filter chips in horizontal strip have no explicit `contentDescription`**
    - Description: Same as Trees Only Issue 11. Events confirm the consequence: when `text` is transiently unavailable, these chips have no fallback label.
    - WCAG: 4.1.2 Name, Role, Value (Level A)
    - Severity: Low
    - Evidence: tree_2026-05-26T17-15-10-511.json — filter chips `contentDescription: ""`; events confirm `<no_feedback>` / "Double-tap to activate" on same elements.
    - Manually Observed: N
