# 02 · Navigation

<!--
HOW TO FILL: from canon §5 and §8, and the "How it is organized" section of the shape.
Every screen of 03-screens/ appears in the screen map with its presentation. Delete this block when done.
Modality vocabulary (use exactly these words):
- push: new screen in the stack, back with ‹ (chevron only).
- sheet: panel over the current screen, with detents (small / medium / large), closed with ✕ or by swiping down.
- large sheet: multi-step task; ✕ in step 1, ‹ from step 2.
- persistent sheet: non-modal panel over a map; it does not close.
- full screen: immersive content (stories, camera, a loading moment).
Never a sheet on top of another sheet.
-->

## Spaces and tabs
| Tab | Root screen | What lives here | Symbol (SF Symbol) |
|---|---|---|---|
| [Tab] | S01 | [One line] | `[symbol.name]` |

<!-- If there is no tab bar, say so and why. Tabs never appear, disappear or empty depending on the moment. Each tab keeps its own stack. -->

## Screen map
```
[Tab 1]
└─ S01 [Root]                       (tab root)
   ├─ S02 [Detail]                  push
   │  └─ S03 [Edit]                 sheet · medium
   └─ S04–S05 [Create]              large sheet · 2 steps
[Tab 2]
└─ S06 [Root]                       (tab root)
```

## Modality per screen
| Screen | Presentation | Opened from | Exit | Notes |
|---|---|---|---|---|
| S02 [Detail] | push | S01 row | ‹ | |
| S03 [Edit] | sheet, medium + large | S02 primary action | ✕ / swipe down | Saves on ✓ |

## Notifications and deep links
<!-- Every notification opens its object INSIDE its hierarchy, with the back stack built. Never an orphan screen. -->
| Notification | When | Text (exact) | Opens | Back stack |
|---|---|---|---|---|
| [Name] | [Trigger] | "[Copy]" | S02 | S01 › S02 |

## Permissions
| Permission | Asked when (never on first launch without reason) | Why, as shown to the person | If denied |
|---|---|---|---|
| Notifications | [Moment] | "[Copy]" | [Fallback] |

---

> **Example (replace):**
> Tabs: **Book** (S01, `scissors`) · **My cuts** (S06, `calendar`).
> S02 Slot detail · push from S01 · exit ‹.
> Notification "Your cut is in 1 hour" · 60 min before · opens S07 Appointment · back stack S06 › S07.
