# 07 · Brand and personality

**Goal:** give the app a personality the person wants (concept, voice, type, color, motion) without touching the structure that is already approved.
**Done when:**
- The person chose a concept.
- A visual system exists, ready for production:
  - type scale;
  - palette (light and dark, contrast checked);
  - texture rules;
  - two brand intensities;
  - motion and haptics;
  - tokens.

## What to ask the person (minimum)
Example questions are in English; translate them into the person's language.
- Reuse the stage 1 personality answer. Ask again only if it is missing: "If the app were a person who comes along with you, what would they be like?"
- Checkpoint 1: "Which of these makes you want to use it? You can take parts from several."
- Checkpoint 2: "Which of these four would you show a friend?"
- Optional: "Is there an app you find beautiful?" Use the answer as a reference, not to copy.
- The app name: offer candidates once the concept is chosen, never force it. It can stay "[name]" until delivery.

## What the agent does
**0. Freeze the UX first.** Copy the approved stage 6 HTML and its generator to `docs/_baseline/`. From here on, brand never changes the structure or the copy of that baseline.

**1. In parallel:**
- **Reference brands:** the competition plus apps with strong personality (e.g. Things, Flighty, Partiful, Beli, Citymapper). For each: how they express brand without breaking iOS native (personality, voice with real microcopy, color, type, imagery, motion and haptics, icon), what is worn out, and 2025–26 trends.
- **Brand platform:**
  - a promise;
  - positioning against the competition;
  - personality traits, as "X, not Y";
  - voice rules plus tone per moment, with before → after rewrites of real app copy;
  - **3 territories**;
  - a long list of name candidates with a quick conflict check (web, not legal).

**2. Directions.** One builder applies 3–4 territories to the **same 5 key screens** of the baseline. Include the person's own words as a territory if they gave one. For each direction:
- palette, type, shape, imagery treatment;
- voice samples, motion, haptics, an icon sketch;
- the 5 screens.

End with a comparison table that includes "does it feel like [personality]?" → **Checkpoint 1.**

**3. Variants.** A quick "aesthetic" research (what makes apps desirable: extreme scale, absence of cells and borders, one accent, color as light, rituals that close) and then 4 variants of the chosen direction. Each variant has its "desire moment", the screen you'd want to show someone → **Checkpoint 2.**

**4. In parallel, the visual system:**
- typography, checked on real font files: weights, tabular figures, language coverage;
- palette with computed contrast;
- texture rules;
- tokens in TS/JSON.

Also a **motion and interaction language**: a few springs with their uses, haptics with Apple's meanings, sound off by default if used outdoors, and one novelty per screen, always with a visible button that does the same.

## What gets produced
- `docs/07-directions.html`, `docs/07-variants.html` and `docs/07-system.html` (the system sheet), all with `annotate.js`.
- `research/07-*.md`.
- **Canon:** the concept, voice rules, forbidden terms, two intensities, tokens and motion rules.

## Checkpoint
Two checkpoints: the direction, then the variant or concept. Show them side by side, the same screen in each option, with one recommendation. Accept mixes ("the color of A, the voice of B").

## Lessons from the thread (avoid from the start)
- **Separate concept from execution.** Franco: "I loved the Tiza concept, but none of the mockup design." He approved a *concept*, not screens. Ask about feeling and concept; screen design comes in stage 8.
- **Brand goes in the content, not on the system glass.** Use high intensity where the user plans or browses, and low intensity where they act under attention pressure (navigation, lock screen). There, only the image, a status color and big system type.
- **"Aesthetic, minimal, details that are often the absence of things."** Honor it, but absence must remove decoration, never grouping. It caused the "no structure" failure in stage 8.
- **Avoid:**
  - the ✦ sparkle and violet "AI" gradient;
  - mascots;
  - commercial urgency ("selling out");
  - generic 3D;
  - tinting system glass;
  - literal skeuomorphism.
- **Decorative details get noticed and disliked.** A double underline under titles: "the only thing that bothers me".
- **Never pick the name.** Present options with criteria. Franco never chose one, and that's fine: it stays pending without blocking.
- **Keep the UX frozen.** Franco: "the UX is almost done, we must not lose it". Re-check that brand passes didn't drop a rule from the canon.
