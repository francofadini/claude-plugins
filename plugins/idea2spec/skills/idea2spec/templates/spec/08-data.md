# 08 · Data

<!--
HOW TO FILL: from canon §5 (objects) and §12 (data constraints). Plain language first, then types.
This is the domain model, not the database schema: the builder decides storage. Seed values live in example.md.
Delete this block when done.
-->

## Objects
<!-- One block per object. Attributes: name · type · required? · meaning in plain words. -->
### [Object]
[One line: what it is, in the person's words.]

| Attribute | Type | Required | Meaning |
|---|---|---|---|
| `id` | id | yes | |
| `[name]` | string | yes | [What it is] |
| `status` | enum: `[a]` · `[b]` | yes | [What each value means; which screen state it drives] |

**Rules:** [invariants, e.g. "an appointment never overlaps another one of the same barber"].

## Relations
```
[Object A] 1 ──< [Object B]       one A has many B
[Object B] >── 1 [Object C]
```

## Where data comes from
| Data | Source | Validated or inferred | Offline |
|---|---|---|---|
| [Opening hours] | [The barber enters them] | validated | cached |

## Derived values
<!-- Anything computed for display, with its formula, so screens and counts never contradict each other. -->
- `[nextFreeSlot]` = [formula].

---

> **Example (replace):**
> **Appointment** · "a cut booked by a client for a time" · `startsAt` datetime (yes) · `service` → Service (yes) · `status` enum `booked` · `cancelled` · `done` (drives S07 states).
> Relations: `Shop 1 ──< Service`, `Client 1 ──< Appointment >── 1 Service`.
> Rule: an appointment can be cancelled until 1 h before `startsAt`.
