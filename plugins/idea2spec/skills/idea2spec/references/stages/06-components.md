# 06 · Components, content budget and screen templates

**Goal:** order every screen with these rules:
- one shape per object;
- at most one primary action;
- a state said once;
- content limited to what that moment allows;
- screen templates that give each screen structure.

Still iOS-basic greyscale, no brand.

**Done when:**
- The inventory has one form per object, drawn large.
- Every phone carries its moment and budget line.
- Every screen follows one template and passes the squint test (blurred, you still see the anchor and the groups).

## What to ask the person (minimum)
Example questions are in English; translate them into the person's language.
- "Is there an app whose screens feel clear and well ordered to you, even about something else?" It is the best input for composition. Franco named Uber, and it fixed the "no body" problem.
- If the person states a hunch ("I'd rather see one at a time"), don't ask more. Run the evidence method below and come back with a verdict.

## What the agent does
**Round 1, in parallel:**
1. **Screen-by-screen heuristic audit.** Screenshot every phone. Check:
   - hierarchy: is the first thing you see the most important?
   - grouping;
   - whether the copy works without context;
   - whether buttons look tappable (grey full-width buttons look disabled);
   - density.

   Propose a top-to-bottom order per screen.
2. **Component inventory.** Count the variants of each object; travel had about 25 pieces in 70 variants. Then propose a small system:
   - one row per object, with fixed slots;
   - one state system (normal state not shown, each state said once, colors with one meaning);
   - action rules (0–1 primary per screen, the action sits next to its object, the rest goes in a menu).
3. **Composition references.** The best iOS apps on Mobbin for equivalent screens, plus the app the person named, analyzed as skeletons: zones, anchor, surfaces, weight, fixed CTA.

**Round 2, in parallel. Run it when screens still feel like a "potpourri"; it usually does:**
4. **What to show per moment** (evidence). Glance attention while moving (4–8 s bursts), choice overload under fatigue or time pressure, defaults, and interruption timing. The output is a **content budget per moment**. Travel example: walking = 1 image, ≤12 words, 1 datum, 0 decisions; lock screen = 1 sentence ≤6 words; tired evening = only what changed, ≤3 options with one preselected.
5. **Density audit.** Count data, competing primaries, decisions and repetitions per screen, and rank the screens worst to best. Run it on the document too: repeated rules, contradictions, "open" decisions that were already decided.
6. **Decision evidence audit.** For every decision: a study, a guideline or leading app, or just our assumption? Look for studies on the weak ones. If the evidence contradicts the *person's* decision, list it under "To test". Never change it without their OK.

**Screen templates (composition)**, written once and used everywhere:
- one anchor block per screen;
- space between groups ≥3× the space between rows;
- fixed text column and margins;
- content surfaces;
- weight for hierarchy;
- a fixed bottom CTA where needed;
- 4–6 templates (e.g. Hub, Index, Detail, Map+panel, Moment).

### Evidence method (when there is a hunch or "it doesn't feel right")
1. State the hypothesis in one line.
2. Research in parallel: studies with `[V]/[A]/[S]` marks and real apps on Mobbin, plus a measurement of ours if useful.
3. Verdict: confirmed / nuanced / refuted, with the gaps.
4. Concrete change per screen.
5. Rule into the canon.

Travel: "one visual reference at a time" was confirmed (Bauer 2016: 1 landmark beats 4) with a nuance: hint the next step in text.

## What gets produced
- `docs/06-components.html`:
  - the system drawn large;
  - screens rebuilt;
  - a budget line under each phone;
  - a short working glossary (one name per concept).
- `research/06-*.md`.
- **Canon:** component rules, budgets per moment, templates, glossary, and a "To test" list.

## Checkpoint
- Send the link plus ≤5 bullets: what was reordered, before → after numbers, and one open decision at most.
- **Comprehension test** on 2 screens: "Look at this for 5 seconds: what would you do first?"
- **If they say "it doesn't feel right" with no reason:**
  - offer two versions side by side ("Which one do you understand faster?");
  - run the evidence method on the best hypothesis;
  - never answer with more explanation.

## Lessons from the thread (avoid from the start)
- **One concept, one name, one shape.** "Day not planned yet" had 4 names, the trip 10 forms and the day 13 forms. There were also 7 button styles and 8 date formats.
- **No pills that look like filters but are actions.** No chip with an × inside. Use real filters (capsules) or icon buttons.
- **≤1 "·" per subtitle.** What drives behaviour goes in the title or state line, not buried in grey. Use blue only for tappable things.
- **No card or alert above tabs or segments that comes and goes.** It makes the screen look like it changed. Use one fixed row ("2 pending tasks").
- **Never blame the user.** "Are you lost?" became silent rerouting ("New route from here · 2 min more"). Principle: adapt to any change without friction.
- **Exact clock times on leisure make it feel like work** (Tonietto & Malkoc 2016). Use exact times only for anchors (bookings, departures), and order or time-of-day for the rest.
- **Automatic changes are proposals unless they're trivial.** Only 12% accept AI deciding alone. Undo stays fixed on the changed row, never as a 4-second toast.
- **No panel on a panel, no read-only duplicate screen, no lost feature.** Re-check the scope inventory every round.
- **Strip decoration, not grouping.** Removing borders and separators without adding space or surfaces left text "floating" (see stage 8).
