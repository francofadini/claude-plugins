# Example data (seed)

<!--
HOW TO FILL: written FIRST in stage 9, before building the docs: every screen in docs/shape.html and
docs/annex.html is generated from this file, and the builder AI seeds the app with it.
- One continuous, TRUE example: real places exist and are open on the example day, times and counts add up.
  Check what a person would notice at a glance; no more than that.
- Every count shown on any screen must be derivable from this data.
- Keep it in the shape of 08-data.md (same object and attribute names), so it can be turned into a seed file.
Delete this block when done.
-->

## The story
[3–5 lines: who, when, what happens across the flows, in order. The annex follows exactly this.]

## Now
- **Today in the example:** [weekday, date, time when F1 starts]
- **Device:** iPhone, [language], [time zone]

## Records
<!-- One table per object from 08-data.md. IDs are referenced across tables and across screens. -->
### [Object]
| id | [attribute] | [attribute] | status |
|---|---|---|---|
| [a1] | […] | […] | […] |

## What changes along the flows
<!-- So later flows show the consequences of earlier ones (continuity). -->
| After flow | What changed | Seen in |
|---|---|---|
| F2 | [record] created | S01 (slot gone), S06 (new row) |

---

> **Example (replace):**
> **Story:** Tuesday Oct 6, 10:12. Ana installs the app (F1), books the 17:30 classic cut with Marco (F2), gets the reminder at 16:30 (F3) and moves it to 18:00 (F4).
> **Service:** `s1` · Classic cut · 30 min · $15. **Slot:** `t1730` · 17:30 · Marco · free → taken after F2.
> **After F2:** appointment `ap1` created · S01 no longer shows 17:30 · S06 shows "Today, 17:30 · Classic cut".
