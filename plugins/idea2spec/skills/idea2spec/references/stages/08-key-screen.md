# 08 · Key screen (the hardest one first)

**Goal:** design one screen in high fidelity, with brand, composition, states, motion and detail, before extending to the rest. It must be the hardest one: the core of the value, with the most states.
**Done when:**
- The person approves the key screen ("much better" is enough).
- Its decisions have been generalized into the screen templates, so stage 9 can apply them everywhere.

## What to ask the person (minimum)
Example questions are in English; translate them into the person's language.
- Which screen: don't ask. Recommend it and say why ("the one you'll use most while [core moment]"), then let them confirm or swap.
- After showing it: "Does this make you want to use it? What would you tap first?"
- If it doesn't feel right: "Is there an app whose screens you like, even about something else?" Skip this if stage 6 already answered it.

## What the agent does
1. **Composition check first.** If stage 6 didn't produce templates, or they lost body with brand applied, run the composition layer now. A research agent validates the likely causes with evidence and measures our screens:
   - no anchor (the screen's title is the only weight);
   - group spacing <3× row spacing;
   - several text alignments;
   - surfaces only on controls, so the chrome has more body than the content;
   - no strong weight;
   - no screen templates.

   It also analyzes the reference app as skeletons and states "what we take from [app]": structure, not aesthetics. Then a builder adds tokens and templates to the system and redoes 2–3 screens **before/after**, with the squint test.
2. **Design the key screen in hi-fi:**
   - every state of the screen (empty, normal, in progress, done, error or offline);
   - the motion spec: entering, changing state, the interruptible gesture, transitions between screens;
   - haptics;
   - only the copy that is needed.
3. **Innovate carefully:** at most one novelty per screen, always backed by a familiar visible control. Don't break patterns people already know from the platform.
4. A fresh reviewer checks against the canon before showing (see 00-rhythm).

## What gets produced
- `docs/08-key-screen.html`: the screen in every state, a short motion description, and before/after if the composition changed.
- `research/08-*.md` when composition research ran.
- **Canon:** composition tokens, templates, the key screen's rules and motion rules.

## Checkpoint
- Send the link plus ≤5 bullets: what makes the screen work and the before/after.
- Ask: "Does this have the structure you were missing?" or "Does it make you want to use it?"
- If they approve, move straight to stage 9. Don't design the other screens one by one with checkpoints.

### When they say "I don't like it" but can't explain why
Treat it as a design diagnosis, not a taste issue:
1. Name what they describe in design terms (Franco: "it lacks structure, lacks body; I like every decision individually, but the composition doesn't come together").
2. Form 3–4 concrete hypotheses and say them in plain words ("nothing tells you what matters here", "everything weighs the same").
3. Ask one question that unlocks it: an app they like.
4. Run the evidence method (stage 6) and come back with before/after on the same content. The before/after convinces; explanations don't.

## Lessons from the thread (avoid from the start)
- **We skipped a layer.** The travel project defined pieces (type, color, components) and rules, then jumped straight to screens. The middle layer (how pieces combine: grid, rhythm, surfaces, templates) was missing, so the screens had no body. The research measured it:
  - group space was only 1.9× row space;
  - 46% of a screen was empty;
  - the anchor was the screen's name;
  - the only surfaces were controls.
- **The person's reference app unlocked it.** Franco said "Uber does a good job". Taking its *structure* fixed composition while keeping the brand's aesthetic:
  - the title is the state ("Leave in 25 min");
  - one hero block;
  - content surfaces;
  - thin bands;
  - weight for hierarchy;
  - one big fixed button.
- **Hardest screen first, then approve, then extend.** Franco: "this part is the hardest, so I'd make one screen to start; when I approve it we continue". It avoided redoing 40 screens.
- **Low brand intensity under attention pressure.** In navigation and on the lock screen: system type, no texture, no serif, nothing decorative.
- **The minimum on screen.** No text explaining or justifying system logic ("You walked 14 km yesterday, so we marked it relaxed"). Franco: "only what's essential on screen".
- **Don't treat sketch maps or images as real assets.** They are illustrative. The criterion matters, not geographic precision (Franco: "relax with the maps, they're sketches").
