# 04 · Flows

<!--
HOW TO FILL: one section per flow, mirroring docs/annex.html one to one (same numbers, same steps, same copy).
Flows are numbered in the order of real use. F1 starts on the iOS home screen with the app just installed.
All flows tell one continuous story (spec/example.md): what changes in one carries into the next.
Variants (permission denied, offline, empty, nothing yet, error) each have their own start and end.
Delete this block when done.
-->

## Flow map
| Flow | Starts at | Ends at | Leads to |
|---|---|---|---|
| F1 [Name] | iOS home screen, app just installed | S01 with [state] | F2 |

---

## F1 · [Name]
**Starts at:** [moment in the example] · [exact screen and state] · [what the person taps to begin].

| # | Screen · state | The person… | The app… | Next |
|---|---|---|---|---|
| 1 | iOS home screen | taps the app icon | opens S01 · first launch | 2 |
| 2 | S01 · empty | taps "[Copy]" | opens S04 as a large sheet | 3 |

**Ends at:** [screen · state], [what back does from there].

**Variants**
- **[Offline at step 2]** · starts at: step 2 with no connection · S01 · offline shows "[copy]" · ends at: back to step 2 when the connection returns.
- **[Notifications denied]** · starts at: […] · […] · ends at: […].

---

> **Example (replace), F2 · Book a cut:**
> **Starts at:** Tuesday 10:12, Ana opens the app from the home screen; S01 · default shows today's free slots.
> | 1 | S01 · default | taps "17:30" | pushes S02 | 2 |
> | 2 | S02 · default | taps "Book" | creates the appointment (haptic rigid), shows S07 | 3 |
> | 3 | S07 · booked | taps ‹ | back to S01, the 17:30 slot is gone | end |
> **Ends at:** S01 · default, without 17:30. **Variant "Taken while deciding":** starts at step 2 when the slot is booked by someone else · S02 · taken · "See next free slot" → S02 for 18:00.
