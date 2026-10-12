# 10 · Open

<!--
HOW TO FILL: from canon §15. Nothing here blocks the build: every open item has a default to build now,
chosen so it is cheap to change later. Delete this block when done.
-->

## Pending decisions (the person decides)
| # | Question | Options | Build now (default) | Cost to change later |
|---|---|---|---|---|
| D1 | [App name] | [A · B · C] | Working name "[…]" in one constant | Low |

## To test
<!-- Decisions the evidence questions. They stay as decided until a test says otherwise; never changed without the person's OK. -->
| # | Decision as built | Why it is in doubt | How to test | What would change it |
|---|---|---|---|---|
| T1 | [Decision] | [Evidence, with source] | [Test with N users / metric] | [Result] |

## Technical validations to do FIRST
<!-- Risks that could change screens if they fail. Build a spike for each before the screens that depend on them. -->
| # | Validate | Why it matters | Screens affected | If it fails |
|---|---|---|---|---|
| V1 | [e.g. native sheet with detents over a map in Expo] | [The main screen depends on it] | S03 | [Fallback] |

---

> **Example (replace):**
> **D1** · Name of the free slot: "free chair" or "slot" · build "free chair" · low cost.
> **T1** · Next free slot preselected · some users may book by mistake · 5 users, count accidental bookings · > 1 in 5 → no preselection.
> **V1** · Push notification 60 min before, scheduled locally without a backend · F3 depends on it · S07 · fallback: server push.
