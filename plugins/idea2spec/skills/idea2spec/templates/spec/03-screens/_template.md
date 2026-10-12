# S[NN] · [Screen name]

<!--
HOW TO FILL: copy this file once per screen as `03-screens/S[NN]-[short-name].md` (e.g. S02-slot-detail.md).
One screen per OBJECT, with all its states inside it: no separate "summary", "read-only" or "today" screens.
Source: the approved docs (shape + annex), canon §6, example.md. Exact copy, exact values. Delete this block when done.

PNGs: one per state, captured from docs/ with scripts/shots.py (the phone's data-screen says "S[NN] … · <state>"):
  python3 scripts/shots.py idea2spec/docs/annex.html --only S[NN] --out idea2spec/spec/03-screens/png/tmp
then rename to `png/S[NN]-[state].png`.
-->

## Purpose and moment
- **Question it answers:** [The one question the person has on this screen.]
- **Moment:** [When it is used, e.g. "on the move, a glance of 4–8 s" or "at home, planning".]

## Template
[P1 Hub · P2 Index · P3 Detail · P4 Map + panel · P5 Moment] · **Anchor:** [the block that answers the question; ~25–45 % of the first view].

## Content budget
<!-- From the moment's budget in the canon. Count what is on screen in the busiest state. -->
| Images | Words (max) | Data points | Decisions | Primary actions |
|---|---|---|---|---|
| [n] | [n] | [n] | [n] | 0 or 1 |

## States
<!-- State changes content, never structure. Exact copy, in quotes, as it appears. One PNG per state. -->
### [State name, e.g. Default]
- **When:** [condition, in data terms: "appointment.status = booked and starts in > 1 h"].
- **Shows:** [what is on screen, top to bottom, naming components from 05-components.md].
- **Copy:**
  | Element | Text |
  |---|---|
  | Title | "[…]" |
  | Primary button | "[…]" |
- **PNG:** `png/S[NN]-[state].png`

### Empty
- **When:** […] · **Copy:** title "[…]", line "[…]", one action "[…]" · **PNG:** `png/S[NN]-empty.png`

### Loading · Error · Offline
- **Loading:** [skeleton of the layout, never a spinner over the whole screen] · **Error:** "[exact copy]" + [recovery action] · **Offline:** [what still works] "[copy]".

## Actions
| Action | Where | Kind | Result | Haptic |
|---|---|---|---|---|
| "[Label]" | [Footer, full width] | Primary | [What happens; where it goes] | [rigid / soft / success / none] |
| Swipe left on a row | List | Destructive | Removes it, shows "Undo" | [none] |

## Where you come from and where you go
| From | How |
|---|---|
| S01 [Name] | Tap a row (push) |
| Notification "[…]" | Deep link, back stack S01 › S[NN] |

| To | How |
|---|---|
| S03 [Name] | Primary action (sheet, medium) |
| Back | ‹ to S01 |

---

> **Example (replace), S02 · Slot detail:**
> **Question:** "Can I take this slot?" · **Moment:** at home or at work, 30 s · **Template:** P3 Detail, anchor = the time and the barber.
> **Budget:** 1 image · ≤ 30 words · 3 data points (time, service, price) · 1 decision · 1 primary.
> **Default state:** when `slot.free = true` · title "Today, 17:30" · line "Classic cut · 30 min · $15" · primary "Book".
> **Taken state:** when another client books it while open · line "Someone just took it" · primary "See next free slot".
> **Actions:** "Book" · footer, full width · creates the appointment, goes to S07 · haptic rigid.
> **From:** S01 slot row (push). **To:** S07 Appointment (replaces the stack top) · ‹ to S01.
