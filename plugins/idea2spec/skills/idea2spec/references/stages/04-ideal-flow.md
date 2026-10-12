# 04 · Ideal flow (storyboard)

**Goal:** show one user living the whole MVP from first open to recommending it, as a sequence of moments. Each moment has one low-fi screen.
**Done when:**
- The person recognizes the story ("yes, that's how it would go").
- Every in-scope feature appears in a moment.
- The app only asks what it can't infer.

## What to ask the person (minimum)
Example questions are in English; translate them into the person's language.
- Before building, only if the stage 1 real example doesn't cover it: "How long does a typical use last: one evening, a week, a 3-day trip?" Default: the person's real example, covering at least 3 sessions or days.
- After they see it: "Does this look like how you lived it, or how you'd live it? Mark any moment that doesn't fit." (annotations)
- If the app needs to ask the user something, propose the questions yourself. Never ask the person "what should the app ask?". Travel: Franco replied "Are you asking me for suggestions?"

## What the agent does
One builder (the coordinator or one sub-agent that reads `canon.md`) writes `docs/04-flow.html`:
- **Story:** one user, the real example with real places and times, told in second person ("you"), never "he/she".
- **Arc:** first open with the app freshly installed → setup (the guided basic flow) → repeated use → the key moment → at least 2 unexpected events → ending → sharing or recommending.
- **Moments:** 15–25. Each one has a time label, one phone screen and 1–2 lines on what happens and which feature it shows.
- **Screens:** use **iOS native chrome from the start**, via the plugin's iOS kit in `templates/`. Never invent navigation bars or buttons. Low-fi: greyscale, real copy, no brand.
- **Close:** the document ends with the list of new assumptions the storyboard introduced. Travel examples: "hotel and flight as fixed anchors", "plan B applied automatically".

Before showing it, the builder or a reviewer checks:
- **Questions the app asks:** only what it can't infer *and* what changes over time, in human words.
- **Timing:** information arrives at the right moment. Bad news comes before you act, never on the way.
- **Data:** example data is consistent across moments (times, bookings, counts).
- **Effort:** nothing forces the user to do work the app could do (tick things off, recalculate, reorder).

## What gets produced
- `docs/04-flow.html` with `annotate.js`.
- **Canon:** behaviour rules (what is asked, what is inferred, what happens automatically, what is proposed for approval). Also the person's corrections as antipatterns.

## Checkpoint
- Send the link plus a 6-bullet summary of the arc and of the assumptions it added. Ask them to annotate.
- Expect 1–2 quick rounds. Apply annotations directly (coordinator, no new agents) and list what changed in ≤5 bullets.
- **If they say "I feel lost" or "too many different screens":** that is not a storyboard problem. It is the signal for stage 5, so move on and say why.

## Lessons from the thread (avoid from the start)
- **Silly questions.** "Walk a lot?" and "Eat well?" got: "Nobody wants to walk a lot; we shouldn't ask like that, it's a matter of intelligence." Ask only what can't be inferred.
- **Phrase answers the way a human talks.** "Intense" became "I want to make the most of it".
- **Don't ask what can be planned and adapted.** For "What time do you start?": "It should be planned and ready to change if that's not how it went." The same goes for meals: suggest top-rated options that fit, and let the user pick.
- **Bad news too late.** "The bookstore closed today, the app finds out before you arrive." Franco: "That makes no sense, you should have known earlier." Check closures and conflicts the night or morning before.
- **The app keeps track.** "We have to tick off what they do, and they can untick if it didn't happen", so the app doesn't suggest coffee to someone who just ate.
- **Concepts that don't explain themselves get cut or reworked.** Example: "single-gap mode". The rule: changing the plan on the go must exist, shown in a way people understand.
- **Uncomfortable fallbacks.** An "I don't know" option is fine, but don't make users turn on the camera.
- **Loose entry points.** "Add to day" was liked, but "I don't know what I tap; normally it'd be planned." Every action needs an obvious place it starts from.
- **Inconsistent example data.** A dinner booking clashed with a "choose between two dinners" moment. Check cross-moment data before showing.
- **Bookings and purchases.** Ask for all bookings during planning, and always offer a place to add an improvised purchase. The plan adapts.
- **Real example plus "you" voice** made the story readable. Keep both.
