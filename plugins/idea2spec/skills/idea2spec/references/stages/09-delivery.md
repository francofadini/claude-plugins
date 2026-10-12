# 09 · Delivery: final shape, flows annex, spec folder

**Goal:** produce three things:
- the final shape the person approves;
- a step-by-step annex of every flow;
- a `spec/` folder another AI can build the React Native app from (iOS first) without asking anything.

**Done when:**
- The person approves the shape and the annex.
- The independent reviewer reports 0 blockers and 0 importants.
- `spec/` is complete and consistent with the canon.

## What to ask the person (minimum)
Example questions are in English; translate them into the person's language.
- Before building: nothing.
- After: "Read it like a story and annotate anything that doesn't make sense to you."
- At the end, once: the app name (3–5 candidates with criteria, plus "keep it pending"). Also ask for any open decision the canon marks as theirs, one per turn and in plain words. Everything else gets a stated default.

## What the agent does
1. **Consolidate before building.**
   - Compile the canon from `state.md`, research and approved docs: rules with sources, antipatterns, glossary, open items, "To test".
   - Make a list of objects and states, and check: **one screen per object, all its states inside it**. No separate "summary", "read-only", "today" or "last day" duplicates.
   - Write one source of example data, `spec/example.md` (places, times, bookings, counts), and generate every screen from it.
   - Check what a person would notice at a glance: the place exists and is open that day, the flight exists. No more than that.
2. **Final shape:** one builder writes `docs/shape.html` as a story that reads in about 10 minutes.
   - **Order:** problem (2 lines) → the idea and principles → how the app is lived, following one continuous example (each moment = 2–3 lines + a carousel of hi-fi screens) → how it's organized → the brand → what's still open.
   - **Technical and design detail always sits in collapsibles.** You can read it top to bottom without opening any.
   - **Don't** start with a decorative cover, compare with earlier versions, repeat a screen, or list questions inside it.
3. **Flows annex** (`docs/annex.html`), built by the same builder from the same data:
   - **Entry points:** every flow states its explicit starting point. **Flow 1 starts on the iOS home screen with the app freshly installed.**
   - **Steps:** each step is one screen, with arrows and the action that leads to the next; each flow ends where it ends.
   - **Map:** a small flow map shows how flows connect.
   - **Variants:** permission denied, offline, empty, nothing planned, error.
   - **Continuity:** all flows tell one continuous story. What changes in one flow carries into the next, and counts come from what actually happened.
4. **Review:**
   - The builder runs its checks plus screenshots.
   - **One fresh reviewer** reads the canon and walks each flow as a new user (see 00-rhythm).
   - Fix blockers and importants, and re-review only if there were blockers.
5. **Spec folder:** written from the canon, the example and the approved HTML, with no new decisions:
   - `README.md`: what the app is, reading order, stack (React Native/Expo, iOS first).
   - `01-product.md`: vision, principles, MVP in/out, metrics.
   - `02-navigation.md`: spaces, tabs, screen map, modality (new screen / panel / full screen), notifications and where they land.
   - `03-screens/<screen>.md`: one per screen, covering:
     - purpose and moment;
     - template;
     - content budget;
     - every state, with exact copy;
     - actions;
     - where you arrive from and where you go;
     - a PNG of each state.
   - `04-flows.md`: every flow step by step, matching the annex.
   - `05-components.md`: one shape per object, state system, action rules.
   - `06-design-tokens.md` plus `tokens.json`: type, color, spacing, radii, motion, haptics.
   - `07-copy.md`: voice, glossary, forbidden terms.
   - `08-data.md`: objects, attributes, relations; `example.md` as seed data.
   - `09-rules.md`: the canon rules and antipatterns the builder AI must respect.
   - `10-open.md`: pending decisions, "To test", technical validations to do first.

## What gets produced
- `docs/shape.html` and `docs/annex.html` (with `annotate.js`), backed up in `docs/_baseline/`.
- `spec/` as listed above.
- `canon.md` and `state.md` up to date.

## Checkpoint
- Send both links, verified with curl, plus three things: what was reviewed, what remains minor or open, and the one decision you need from them.
- Apply annotations directly. Give each annotation that says only "badly designed" a one-line diagnosis, so that it can't come back.
- **If they say "too long to review":** the document failed. Shorten it, moving detail into collapsibles.

## Lessons from the thread (avoid from the start)
- **"It makes no sense to start here."** The doc opened with a decorative cover. Start with the problem.
- **"Several screens for the same thing!"** Parallel documents each drew the day their own way, and there was a view-only mode that couldn't edit ("useless to me"). Fix: one screen per object with states, and one builder.
- **"How do I get to this screen?"** Every screen needs its entry point. The annex's first flow must make clear where it starts.
- **"You lose the feedback from past analyses."** Fix: the canon, read in full by every builder and reviewer, and updated with each piece of feedback the same turn.
- **Reviews found what the builder's self-check missed:**
  - a forbidden ✦ icon;
  - images of the wrong place;
  - sums that didn't add up;
  - closed venues on the example day;
  - a hotel and a flight that didn't exist.

  For an app promising "always true", the example must be true. But don't over-verify ("relax with the maps").
- **Agility.** After 8 audit rounds: "I don't want so much auditing; we need to be more agile." One independent review per deliverable, focused on judgment.
- **Silent suggestions confuse.** Use an explicit button that opens the right place with context ("Explore things nearby").
- **Show what is planned and what isn't.** A timeline below the next step, with done items folded and free time marked.
- **Too long to review = approved without reading.** That is a failure, not a success. Keep it at about 10 minutes.
