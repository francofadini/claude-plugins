# 07 · Copy

<!--
HOW TO FILL: from canon §9 (language, register, voice) and §10 (glossary). Exact strings per screen live in
03-screens/*.md; this file holds the rules and the shared vocabulary. Delete this block when done.
-->

## Language and voice
- **Language:** [e.g. Spanish, neutral, "tú"]. All UI copy in this language; code, IDs and this spec in English.
- **Voice:** [one line, e.g. "a friend who knows the place: short, warm, never cute"].
- **Rules:**
  - Say what happens, not what the system does ("Booked for 17:30", not "Your request was processed").
  - Sentence case everywhere; the only uppercase is the small section label (`type.caption`).
  - No exclamation marks, no emoji in the UI.
  - Buttons are verbs ("Book", "Cancel cut"); never "OK", "Accept", "Submit".
  - Errors say what happened and what to do, never blame ("No connection. Your booking is saved and will be sent.").
  - Times, dates and numbers: [formats, e.g. 24 h "17:30", "Tue 6", currency "$15"].

## Glossary
<!-- One concept, one name, everywhere (UI, notifications, docs). Status: working (not decided yet) or decided (date). -->
| Concept | In the app | Status | Notes |
|---|---|---|---|
| [Concept] | "[Word]" | working | [Where it appears] |

## Forbidden terms
<!-- Each with its replacement. Keep the machine-readable list in spec/forbidden-copy.txt (one regex per line,
     used by scripts/audit.py) in sync with this table. -->
| Never say | Say instead | Why |
|---|---|---|
| "[Term]" | "[Replacement]" | [Reason or the person's words] |

---

> **Example (replace):**
> Glossary: appointment → "cut" (decided 2026-10-12) · free slot → "free chair" (working).
> Forbidden: "Reservation successful!" → "Booked for 17:30" (no exclamation, say the fact) · "Oops" → say what happened.
