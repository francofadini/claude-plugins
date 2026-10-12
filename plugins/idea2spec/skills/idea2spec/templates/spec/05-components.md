# 05 · Components

<!--
HOW TO FILL: from canon §11 (components inventory) and stage 6. Each object has ONE shape everywhere:
the same appointment row in the list, in search results and in a notification preview. If a screen needs
something new, it becomes a variant here, never a one-off. Components own their look: they are not
restyled from outside (no style overrides from screens). Delete this block when done.
-->

## State system
<!-- How every state is expressed, the same way across the app. Color is never the only signal. -->
| State | Word | Symbol | Color token | Where it goes |
|---|---|---|---|---|
| [Done] | "[Done]" | `checkmark` | `color.state.ok` | Right side of the row |

## Action rules
- 0 or 1 primary action per screen; only the primary is full width; it sits fixed at the bottom (footer) in details and sheets.
- If a row navigates it has a chevron; if it does something, a small button; if it only informs, nothing.
- The action lives on its object's row or in its detail, never loose far away.
- Undo instead of "Are you sure?". Destructive actions are red and separated (context menu or swipe).
- [Project-specific rules from the canon.]

## Components
<!-- One block per component. Name = the code name used in React Native (PascalCase). -->

### C01 · [ObjectRow]
- **What it is:** [one line].
- **Anatomy (left → right / top → bottom):** [leading image 56 pt] · [title = the object's name] · [subtitle = what or when] · [state, right] · [chevron if it opens].
- **Variants:** `default` · `compact` (52 pt, no image) · [ … ]. Nothing else.
- **States:** default · pressed · disabled · [selected = 1.5 pt border, not color].
- **Props (suggested):** `title: string`, `subtitle?: string`, `state?: StateKey`, `onPress?: () => void`.
- **Tokens:** `space.row`, `radius.thumb`, `type.rowTitle`, `type.rowSubtitle`.
- **Used in:** S01, S06, notification preview.
- **Never:** [the anti-pattern this shape avoids, e.g. "status as the title"].

### C02 · [PrimaryButton]
- **Variants:** `primary` (accent fill, full width, 50 pt) · `secondary` (fill, small) · `destructive`.
- **Rule:** only one `primary` per screen.

---

> **Example (replace), C01 · SlotRow:** leading = time in tabular figures · title = "Classic cut" · subtitle = "with Marco · 30 min" · right = "Free" or "Taken" (word + symbol) · chevron when free. Variants: `default`, `next` (the next free slot, slightly larger, preselected). Used in S01 and S06. Never: price as the title.
