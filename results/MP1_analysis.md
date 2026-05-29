# MP1 — Google Maps, Core Task: Search "Space Needle" and open its details page

---

## MP1 — Events Only

### Emulator Note
Events show repeated focus events on the same keyboard key during typing (e.g., event seqs 20–21 both focus on the 'p' key at identical timestamps 57567ms). These duplicates are emulator artifacts and are not flagged as issues.

### Issues Found

1. **Action button announces "Double-tap to activate" without context during page load**
   - Description: When the Space Needle details page initially renders, a Button at position (42, 1526) announces ["Double-tap to activate"] with no descriptive accessible name. A fraction of a second later (event 31), TalkBack announces "Directions to Space Needle, 400 Broad St, Button, 1 of 8, In list, 8 items" — indicating the name was populated asynchronously after initial render. A blind user who receives focus before content loads hears only the gesture instruction with no indication of purpose.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Medium
   - Evidence: Event seq 30: `android.widget.Button`, `label: "Double-tap to activate"`, `bounds: {x:42, y:1526, w:321, h:126}`, `announcement: ["Double-tap to activate"]`. Event seq 31 (740ms later): announcement `["Directions to Space Needle, 400 Broad St, Button, 1 of 8, In list, 8 items"]` — name appeared after page settled.
   - Manually Observed: Unconfirmed

2. **Search suggestion rows announced without semantic role**
   - Description: Search suggestion rows are implemented as `android.widget.LinearLayout` elements. When TalkBack focuses on a suggestion, no semantic role (Button, List item) is announced — only the name and gesture instruction. Users cannot tell whether they are activating a navigation action or entering text into the search field, and cannot distinguish the item type from the announcement alone.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Low
   - Evidence: Event seq 27: `android.widget.LinearLayout`, `role: ""`, `label: "Space Needle"`, announcement: `["Space Needle, Broad Street, Seattle, WA, Window Maps", "Double-tap to activate"]`. No role token (e.g., "Button") is present in the announcement.
   - Manually Observed: Unconfirmed

---

## MP1 — Trees Only

### Issues Found

3. **"Tickets" action button implemented as unlabeled CompoundButton with wrong role**
   - Description: The "Tickets" quick-action button on the Space Needle details page is implemented as a `CompoundButton` (a toggle/checkbox widget) with no `contentDescription` and no `text` on the interactive element itself. The inner non-clickable `Button` child holds the text "Tickets." A CompoundButton implies a checkable state ("on/off"), which is semantically incorrect for a booking CTA. TalkBack would derive the name "Tickets" from child traversal, but announce it as a "Toggle button" — misleading to users who expect a simple action button.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Medium
   - Evidence: `tree_2026-05-26T17-21-54-781.json`: `android.widget.CompoundButton` at pos=(386,1526) size=267×126 — `contentDescription: ""`, `text: ""`. Child `android.widget.Button` — `text: "Tickets"`, `isClickable: false`. Sibling action buttons (Directions, Call, Directory) each have explicit `contentDescription` set on their `CompoundButton`; this one does not.
   - Manually Observed: Unconfirmed

4. **"Clear" search button has no contentDescription on the interactive Button element**
   - Description: The "Clear" button that clears the search field is implemented as a `Button` with no `contentDescription`. Its child `ImageView` carries `contentDescription: "Clear"`. TalkBack may derive the accessible name via child traversal, but the interactive element itself lacks an explicit label — a fragile pattern that can fail depending on TalkBack version or `isImportantForAccessibility` settings.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Low
   - Evidence: `tree_2026-05-26T17-21-37-222.json` (and earlier search trees): `android.widget.Button`, `resourceId: "com.google.android.apps.maps:id/search_omnibox_text_clear"`, `contentDescription: ""`, `text: ""`, size=126×126. Child `android.widget.ImageView` — `contentDescription: "Clear"`.
   - Manually Observed: Unconfirmed

5. **"See nearby attractions" button has no contentDescription**
   - Description: An action button on the Space Needle details page is rendered with no `contentDescription` on the interactive `Button` element. Its child `View` holds `text: "See nearby attractions"` but no `contentDescription`. This means the button's accessible name depends entirely on child text traversal, which is not guaranteed to be exposed by all TalkBack configurations.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Low
   - Evidence: `tree_2026-05-26T17-21-54-781.json`: `android.widget.Button` at pos=(309,299), size=462×126 — `contentDescription: ""`, `text: ""`. Child `android.view.View` — `text: "See nearby attractions"`, `contentDescription: ""`.
   - Manually Observed: Unconfirmed

---

## MP1 — Events + User Actions

### Emulator Note
Multiple browser-side taps were required before the phone registered actions throughout the session (e.g., `user_actions` seq 1–3 tapping (508,2213) three times before phone registered; seq 7–9 tapping (232,437) three times to open Maps; seq 23–25 tapping (374,391) three times to select Space Needle suggestion). This is consistent with emulator lag and does not reflect real-device behavior. Zero-size EditText bounds during typing (event seqs 4, 7, 16, 18, 23) are also emulator artifacts and are not flagged.

### Issues Found

1. **Action button announces "Double-tap to activate" without context during page load** *(re-confirmed)*
   - Description: Same as Combo 1 Issue 1. User_actions confirm the sequence: seq 28 shows a browser tap at (259,1558) navigating toward the Directions button area after the Space Needle details page loaded. Event seq 30 (just before the page fully loaded) shows the Directions button announced as "Double-tap to activate." This is consistent with asynchronous accessible name population during page load.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Medium
   - Evidence: Event seq 30: `announcement: ["Double-tap to activate"]` for Button at (42,1526). User_actions seq 28: `browser tap at (259, 1558)` — navigating to details action area.
   - Manually Observed: Unconfirmed

2. **Search suggestion rows announced without semantic role** *(re-confirmed)*
   - Description: Same as Combo 1 Issue 2. User_actions seq 27 confirms `action: "click"` on `android.widget.LinearLayout` with `text: "Space Needle Broad Street, Seattle, WA"` — the LinearLayout IS the interactive suggestion element. The lack of semantic role on this clickable container is confirmed.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Low
   - Evidence: `user_actions` seq 27: `action: "click"`, `class: "android.widget.LinearLayout"`, `text: "Space Needle Broad Street, Seattle, WA"`. Event seq 27 announcement contains no role token.
   - Manually Observed: Unconfirmed

---

## MP1 — Events + User Actions + Trees

### Emulator Note
Same as Events + User Actions combo: emulator lag confirmed via repeated browser taps; zero-size EditText bounds during typing are artifacts.

### Issues Found

1. **Action button announces "Double-tap to activate" without context during page load** *(confirmed across all inputs)*
   - Description: Confirmed by events (seq 30 announcement), user_actions (seq 28 navigation to details page), and tree structure (tree shows Directions button at identical position (42,1526) size=321×126 with `contentDescription: "Directions to Space Needle, 400 Broad St"` — indicating the name was set AFTER the tree was captured, ~529ms after the focus event).
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Medium
   - Evidence: Event seq 30 announcement `["Double-tap to activate"]`; tree `tree_2026-05-26T17-21-54-781.json` same button with `contentDescription: "Directions to Space Needle, 400 Broad St"` — name populated asynchronously.
   - Manually Observed: Unconfirmed

2. **Search suggestion rows announced without semantic role** *(confirmed across all inputs)*
   - Description: Confirmed by events (seq 27 announcement lacks role), user_actions (seq 27 click on LinearLayout), and trees (multiple search result trees show LinearLayout containers with `contentDescription: ""` used as interactive suggestion rows, while child TextViews carry the visible text).
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Low
   - Evidence: Trees (e.g., `tree_2026-05-26T17-21-37-222.json`): multiple `android.widget.LinearLayout` with `contentDescription: ""`, `isClickable: true`; children `TextView` hold suggestion names and addresses. Event seq 27: no role in announcement.
   - Manually Observed: Unconfirmed

3. **"Tickets" action button implemented as unlabeled CompoundButton with wrong role** *(confirmed from trees)*
   - Description: Same as Trees-only Issue 3. Confirmed by tree structure on final details page state.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Medium
   - Evidence: `tree_2026-05-26T17-21-54-781.json`: `android.widget.CompoundButton` at (386,1526), `contentDescription: ""`, `text: ""`. Child `android.widget.Button` `text: "Tickets"`, not clickable.
   - Manually Observed: Unconfirmed

4. **"Clear" search button has no contentDescription on the interactive Button element** *(confirmed from trees)*
   - Description: Same as Trees-only Issue 4.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Low
   - Evidence: Multiple trees: `android.widget.Button` `rid: search_omnibox_text_clear`, `contentDescription: ""`. Child ImageView: `contentDescription: "Clear"`.
   - Manually Observed: Unconfirmed

5. **"See nearby attractions" button has no contentDescription** *(confirmed from trees)*
   - Description: Same as Trees-only Issue 5.
   - WCAG: 4.1.2 Name, Role, Value — Level A
   - Severity: Low
   - Evidence: `tree_2026-05-26T17-21-54-781.json`: `android.widget.Button` at (309,299), `contentDescription: ""`. Child View: `text: "See nearby attractions"`.
   - Manually Observed: Unconfirmed
