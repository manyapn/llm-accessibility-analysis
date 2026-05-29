# AM2 — Amazon Stressful Task
**Task:** Search "wireless headphones", apply "4 stars and up" filter, inspect updated results, end when filtered results are loaded.

> **Emulator Note:** Repeated browser taps observed before phone actions registered throughout the session (e.g., user_action seqs 18–22: 3 long_clicks + 2 browser taps before phone tap; seqs 29–33 and 38–44: 3+ browser taps per close/reopen cycle; seqs 99–108: 5 taps at same coordinates before phone registration). This is consistent with emulator input lag and does not reflect real-device screen reader behavior. It is documented here and excluded from accessibility findings.

---

## AM2 — Events Only

### Issues Found

1. **Filter chips with "Double-tap to activate" as sole accessible name**
   - Description: Multiple filter chips in the horizontal filter bar have their accessible name set to "Double-tap to activate" — the activation instruction — with no descriptive label. A blind user cannot determine what the filter does before activating it.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 8: `resource_id="1253506011"`, `label="Double-tap to activate"`, `announcement:["Double-tap to activate"]`. Same pattern at event_seq 10, 13, 30, 40, 42, 44, 48, 55, 56.
   - Manually Observed: Unconfirmed

2. **Filter chip announces `<no_feedback>` — completely empty accessible name**
   - Description: At least one filter chip (resource_id "gif", corresponding to a "Get It Fast"-type filter) has an empty contentDescription and announces `<no_feedback>`. The user receives no information about this element when TalkBack lands on it.
   - WCAG: 1.1.1 Non-text Content (Level A)
   - Severity: High
   - Evidence: event_seq 12: `resource_id="gif"`, `label=""`, `announcement:["<no_feedback>"]`. Also event_seq 47 in the All Filters panel: `resource_id="2266979011"`, `class="android.widget.Button"`, `label=""`, `announcement:["<no_feedback>"]`.
   - Manually Observed: Unconfirmed

3. **Two distinct filter categories merged into single focus point with duplicate position indices**
   - Description: In the All Filters panel, two separate filter category sections are merged into a single focusable element, causing them to be announced simultaneously with the same position index. A blind user cannot distinguish between the two categories, cannot navigate to them independently, and cannot know which one will be activated on double-tap.
   - WCAG: 1.3.1 Info and Relationships (Level A)
   - Severity: High
   - Evidence: event_seq 36: single focus event announces `"collapsed, Brands, button, 5 of 13"` AND `"collapsed, Noise Control, button, 5 of 13"` in the same announcement. event_seq 49: `"collapsed, Features, button, 10 of 13"` AND `"collapsed, Compatible Devices, button, 10 of 13"` — two distinct categories sharing the same index. Also event_seq 4: `"Apply Get It Fast filter, 7 of 10"` AND `"Apply Get It by Tomorrow filter, 8 of 10"` announced together.
   - Manually Observed: Unconfirmed

4. **Close button in All Filters modal has zero touch target height**
   - Description: The close button in the All Filters modal panel has a height of 0 pixels in its screen bounds. While TalkBack can still navigate to it via swipe (focus is placed and "close, button" is announced), the button's touch target is effectively invisible and untappable for any direct touch interaction.
   - WCAG: 2.5.8 Minimum Target Size (Level AA)
   - Severity: Medium
   - Evidence: event_seq 21: `class="android.widget.Button"`, `label="close"`, `bounds:{x:945, y:294, w:118, h:0}`. Same bounds at event_seq 23.
   - Manually Observed: Unconfirmed

5. **Raw URL announced as accessible name for browser tab element**
   - Description: A browser tab element (ActionBar$Tab) announces a full raw URL string (a product reference URL) as its primary accessible name before announcing its semantic label. The URL is verbose, meaningless, and confusing to a screen reader user.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Medium
   - Evidence: event_seq 65: `class="androidx.appcompat.app.ActionBar$Tab"`, `label="ref=sr_1_1_sspa?ie=UTF8&psc=1&spc=MTozMTY0..."`, `announcement:["ref=sr_1_1_sspa?ie=UTF8...", "Your Amazon.com Tab 2 of 4", "Double-tap to activate"]`. The URL dominates the announcement.
   - Manually Observed: Unconfirmed

---

## AM2 — Trees Only

### Issues Found

1. **Bottom navigation tab elements have no accessible name on parent container**
   - Description: All four bottom navigation bar tabs (ActionBar$Tab) have no contentDescription on the tab element itself. TalkBack may fall through to child labels as a fallback, but accessibility of these tabs depends on implementation details and is not guaranteed. The tabs are clickable and focusable.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Medium
   - Evidence: `start_2026-05-26T17-17-57-813.json`: 4 × `androidx.appcompat.app.ActionBar$Tab` with `contentDescription=""`, `isClickable=true`, `isFocusable=true`. Child ImageView/FrameLayout elements carry labels ("Home Tab 1 of 4", "Your Amazon.com Tab 2 of 4", "Cart 0 item Tab 3 of 4", "Browse menu Tab 4 of 4") but are not set on the interactive parent.
   - Manually Observed: Unconfirmed

2. **"View Sponsored information or leave ad feedback" button below minimum touch target height**
   - Description: A button for leaving ad feedback has a measured height of 40 pixels. At typical Android screen density (~2.75×), this is approximately 14.5dp — well below the WCAG 2.5.8 minimum of 24×24dp. The element is a real interactive button that provides user functionality.
   - WCAG: 2.5.8 Minimum Target Size (Level AA)
   - Severity: Medium
   - Evidence: `start_2026-05-26T17-17-57-813.json`: `class="android.widget.Button"`, `contentDescription="View Sponsored information or leave ad feedback"`, `boundsInScreen: right-left=142, bottom-top=40`. Same bounds in `tree_2026-05-26T17-18-04-864.json` and subsequent trees.
   - Manually Observed: Unconfirmed

3. **Large unlabeled interactive view in search results area**
   - Description: A large `android.view.View` element covering the entire search results area (1084×1667px) is marked as clickable with no contentDescription or text. TalkBack can navigate to this element and attempt activation, but the user receives no information about its purpose. This appears to be a full-page overlay or container that is inadvertently exposed as interactive.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: `start_2026-05-26T17-17-57-813.json`: `class="android.view.View"`, `contentDescription=""`, `text=""`, `isClickable=true`, `isFocusable=false`, `boundsInScreen: 0,0–1084,1667`. Consistent across all tree snapshots. A sibling `android.widget.TextView` with the same bounds is also clickable with no label.
   - Manually Observed: Unconfirmed

4. **Product title link elements have near-zero touch target height in search results**
   - Description: Individual product listing link elements (for product titles and small swatches) have heights of 18px in the tree, well below the minimum 24dp required. While the product card as a whole may offer a larger tap area, the individual link elements exposed to TalkBack have insufficient touch target sizes.
   - WCAG: 2.5.8 Minimum Target Size (Level AA)
   - Severity: Low
   - Evidence: `tree_2026-05-26T17-19-40-747.json`: `class="android.view.View"`, `label="DOQAUS Bluetooth Headphones Over Ear Wireless"`, `boundsInScreen: width=511, height=18`. `label="DOQAUS Over-Ear Bluetooth Headphones with..."`, `height=18`. `label="+1 other color/pattern"`, `height=42`.
   - Manually Observed: Unconfirmed

---

## AM2 — Events + User Actions

### Emulator Note
Same lag as noted at top. Multiple repeated browser taps before phone action confirms emulator input lag throughout this session.

### Issues Found

1. **Filter chips with "Double-tap to activate" as sole accessible name**
   - Description: Same as Events Only Issue 1. User action context shows the user navigated through the filter bar (seqs 1–17, multiple swipe_right actions) and encountered these uninformative chips throughout the task.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 8: `label="Double-tap to activate"`, `announcement:["Double-tap to activate"]`. User navigated past at least 8 filter chips announcing only this instruction during swipe_right actions (action_index 110–124).
   - Manually Observed: Unconfirmed

2. **Filter chip announces `<no_feedback>` — empty accessible name**
   - Description: Same as Events Only Issue 2. The "gif" (Get It Fast) filter chip and a button in the All Filters panel both yield `<no_feedback>` during the user's navigation.
   - WCAG: 1.1.1 Non-text Content (Level A)
   - Severity: High
   - Evidence: event_seq 12: `resource_id="gif"`, `announcement:["<no_feedback>"]` triggered during user swipe_right (action_index 121). event_seq 47: `resource_id="2266979011"`, `announcement:["<no_feedback>"]` during All Filters panel navigation (action_index 172).
   - Manually Observed: Unconfirmed

3. **Two distinct filter categories merged into single focus point**
   - Description: Same as Events Only Issue 3.
   - WCAG: 1.3.1 Info and Relationships (Level A)
   - Severity: High
   - Evidence: event_seq 36: "Brands, 5 of 13" AND "Noise Control, 5 of 13" during swipe_right (action_index 162). event_seq 49: "Features, 10 of 13" AND "Compatible Devices, 10 of 13" (action_index 174).
   - Manually Observed: Unconfirmed

4. **Close button in All Filters modal has zero touch target height**
   - Description: Same as Events Only Issue 4. User actions show the user attempted to close the All Filters modal multiple times (action_index 133, 135, 136) with repeated browser taps, consistent with difficulty activating the zero-height close button.
   - WCAG: 2.5.8 Minimum Target Size (Level AA)
   - Severity: Medium
   - Evidence: event_seq 21: `label="close"`, `bounds:{w:118, h:0}`. User_action seq 29–33: 3 browser taps at coords (1047,331) followed by phone taps to close panel — indicating tap-target difficulty.
   - Manually Observed: Unconfirmed

5. **Raw URL announced as accessible name for browser tab**
   - Description: Same as Events Only Issue 5.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Medium
   - Evidence: event_seq 65: URL-as-label announced, reached during user scrolling of results page (action_index 185+).
   - Manually Observed: Unconfirmed

6. **"4 Stars & Up" filter chip loses accessible name after filter is applied**
   - Description: The filter chip at resource_id "1248879011" is correctly labeled "Apply 4 Stars & Up filter to narrow results" before activation. After the user successfully applies this filter (user_action seq 24: click on resource_id "1248879011", action_index 131), the same resource_id element now announces `<no_feedback>`. The filter slot's accessible name is lost during the dynamic page update, leaving a focusable element with no label.
   - WCAG: 4.1.3 Status Messages (Level AA)
   - Severity: Medium
   - Evidence: event_seq 17 (action_index 127): `resource_id="1248879011"`, `label="Apply 4 Stars & Up filter to narrow results"`, correct announcement. user_action seq 24: phone click on "1248879011". event_seq 28 (action_index 143): same `resource_id="1248879011"`, `label=""`, `announcement:["<no_feedback>"]`.
   - Manually Observed: Unconfirmed

7. **No status message announced when filter is applied or results load**
   - Description: After the user applies the "4 Stars & Up" filter (user_action seq 24, click action_index 131), TalkBack does not announce a status message confirming that the filter was applied or stating the new result count. Focus moves to the All Filters button area with only a page-structure announcement. The user must navigate to find a "Remove 4 Stars & Up filter" chip to confirm the filter took effect.
   - WCAG: 4.1.3 Status Messages (Level AA)
   - Severity: Medium
   - Evidence: After user_action seq 24 (click 1248879011, action_index 131), events 18–20 (timestamp 39869ms) show focus on "All Filters Icon" with announcement: `["All Filters Icon, button", "Double-tap to activate"]` — no "filter applied", no result count. No live-region announcement of filtered result count observed in the entire event sequence.
   - Manually Observed: Unconfirmed

---

## AM2 — Events + User Actions + Trees

### Issues Found

1. **Filter chips with "Double-tap to activate" as sole accessible name**
   - Description: Filter chips in the horizontal filter strip use "Double-tap to activate" as their contentDescription (or have no contentDescription). This is confirmed in both the events trace and the tree structure. The tree shows elements with `contentDescription=""` at those positions, and the events confirm TalkBack reads only "Double-tap to activate".
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: High
   - Evidence: event_seq 8: `label="Double-tap to activate"`, `announcement:["Double-tap to activate"]`. Trees `start/tree_*`: multiple `android.view.View` elements in the filter bar with `contentDescription=""` and `isClickable=true`, confirming the empty/default label.
   - Manually Observed: Unconfirmed

2. **Filter chip announces `<no_feedback>` — empty accessible name (confirmed in trees)**
   - Description: The "gif" filter chip and certain All Filters panel buttons have no contentDescription in the tree and announce `<no_feedback>` in events. The tree confirms the structural absence of a label on these interactive elements.
   - WCAG: 1.1.1 Non-text Content (Level A)
   - Severity: High
   - Evidence: event_seq 12: `resource_id="gif"`, `announcement:["<no_feedback>"]`. Trees confirm: interactive `android.view.View` / `android.widget.Button` elements with `contentDescription=""` and `text=""` throughout the filter bar across all tree snapshots.
   - Manually Observed: Unconfirmed

3. **Two distinct filter categories merged into single focus point with duplicate indices**
   - Description: Tree analysis of the All Filters panel confirms filter category sections are grouped such that two categories share a single interactive container. Events confirm both are announced simultaneously with the same positional index. This is a structural 1.3.1 failure: distinct content relationships cannot be programmatically determined.
   - WCAG: 1.3.1 Info and Relationships (Level A)
   - Severity: High
   - Evidence: event_seq 36: "Brands, 5 of 13" AND "Noise Control, 5 of 13" in one focus event. event_seq 49: "Features, 10 of 13" AND "Compatible Devices, 10 of 13". Tree `tree_2026-05-26T17-19-12-589.json`: single `android.widget.Button` `resource_id="23746028011"` with `bounds=(380,536,318×84)` encapsulates two separate filter sections.
   - Manually Observed: Unconfirmed

4. **Close button in All Filters modal has zero touch target height (confirmed in tree)**
   - Description: The close button's zero height is confirmed in both the events bounds and the tree view hierarchy. The element is accessible to TalkBack via swipe navigation but is untappable by direct touch.
   - WCAG: 2.5.8 Minimum Target Size (Level AA)
   - Severity: Medium
   - Evidence: event_seq 21: `bounds:{w:118, h:0}`. Tree `tree_2026-05-26T17-18-42-161.json`: `class="android.widget.Button"`, `contentDescription="close"`, `boundsInScreen: right-left=118, bottom-top=0`. User_action repeated taps at close coords confirm activation difficulty.
   - Manually Observed: Unconfirmed

5. **Raw URL announced as accessible name for browser tab**
   - Description: An ActionBar$Tab element has its accessible name set to a full product URL string. Trees confirm ActionBar$Tab elements carry no contentDescription; the URL appears to be dynamically assigned from the loaded page. Events confirm this is what TalkBack reads aloud.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Medium
   - Evidence: event_seq 65: URL string announced first, then "Your Amazon.com Tab 2 of 4". Trees: all ActionBar$Tab elements have `contentDescription=""`, confirmed in `start` and all subsequent tree snapshots.
   - Manually Observed: Unconfirmed

6. **Applied "4 Stars & Up" filter chip loses accessible name post-activation**
   - Description: After the user applies the "4 Stars & Up" filter, the element at resource_id "1248879011" loses its accessible name. Tree snapshots after filter application (e.g., `tree_2026-05-26T17-19-05-538.json`) confirm that the filter bar reorganizes and this element becomes empty-labeled while remaining in the focus order.
   - WCAG: 4.1.3 Status Messages (Level AA)
   - Severity: Medium
   - Evidence: Pre-application event_seq 17: `announcement:["Apply 4 Stars & Up filter to narrow results, 6 of 10"]`. Post-application event_seq 28: `resource_id="1248879011"`, `label=""`, `announcement:["<no_feedback>"]`. Tree `tree_2026-05-26T17-19-05-538.json`: element at that filter position has empty contentDescription.
   - Manually Observed: Unconfirmed

7. **No status message announced when filter is applied or results load**
   - Description: Trees confirm there is no `liveRegion` attribute set on the search results container (`liveRegion=0` throughout all trees). Events and user actions confirm no status announcement fires after filter application. The results update silently, with no programmatic notification to TalkBack.
   - WCAG: 4.1.3 Status Messages (Level AA)
   - Severity: Medium
   - Evidence: After user_action seq 24 (filter click), no status announcement in subsequent events. All tree snapshots confirm: search results container has `liveRegion=0`. The result count ("11 items" in event_seq 26) is only discoverable by navigating to the filter chips, not announced proactively.
   - Manually Observed: Unconfirmed

8. **Bottom navigation tabs missing accessible name on interactive parent element**
   - Description: All four bottom navigation tabs have no contentDescription on the tab element itself. Events (event_seq 65) confirm TalkBack encounters these tabs and can read URL content as a spurious name; trees confirm all 4 tabs have empty contentDescription. The child ImageView/FrameLayout carries the correct label but is not the focusable element.
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Severity: Medium
   - Evidence: Trees (all snapshots): 4 × `androidx.appcompat.app.ActionBar$Tab` with `contentDescription=""`, `isClickable=true`. event_seq 65 shows TalkBack reading URL before child label "Your Amazon.com Tab 2 of 4" — name derivation from non-standard source confirmed.
   - Manually Observed: Unconfirmed
