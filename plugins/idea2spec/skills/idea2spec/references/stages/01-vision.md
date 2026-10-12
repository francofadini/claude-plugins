# 01 · Vision

**Goal:** understand the pain, who it is for and what MVP success means. Turn it into a one-page product vision and a shared brief for the research.
**Done when:**
- The person approves the vision ("I like it" is enough).
- `research/00-brief.md` exists, with the pains in the order the user lives them.

## What to ask the person (minimum, one question per turn)
Example questions are in English. Translate them into the person's language and register.

First let them talk. People give the vision in pieces, often in one long voice message, so absorb all of it before proposing anything.

1. **Concrete pain.** "Tell me about the last time this happened to you. What were you trying to do, and what was the most annoying part?" If the answer is abstract, follow up once: "And then what did you do?"
2. **Who.** "Picture one real person who would use this. Who are they and when would they open the app?"
3. **MVP success.** "Imagine it's three months from now and it works. What changed for that person, and how would you notice?" If they don't know, set the default: *useful enough that people use it and recommend it*.
4. **Personality.** "If the app were a person who comes along with you, what would they be like?" In the travel case this came up late (in branding) and was gold: "one more person on the trip, a friend who sometimes gives an opinion, sometimes joins in, sometimes throws out ideas". Ask it here.
5. **Real example.** "Do you have a real example we can use as the thread of the whole story: a plan, a screenshot, a case you lived?" In the travel case, Franco's actual "Tuesday 6" New York plan was the example in every sketch until the end. A real case keeps everything concrete.

Decided by default (say it, don't ask):
- React Native, iOS first.
- No technical-feasibility research.
- Business model out of scope.
- The app name stays pending until stage 7/9.
- App copy in the audience's language.

## What the agent does
- **Vision doc.** If the person mentioned a reference (a blog post or a vision they like), read it and use its format. Otherwise use the default product-vision format (Franco's "The product vision", made2-stories on Medium):
  - **Mission:** the problem in 2 lines.
  - **Vision statement:** 1 line, plus 2 alternatives.
  - **3 principles:** each a short, memorable sentence. Travel: "Look at the city, not the phone", "The app proposes, you choose", "Always true".
  - **3 metrics:** each tied to the MVP goal and with a target. Travel: "minutes to plan tomorrow < 3", "stops that were closed when you arrived = 0".
  - **3 strategies:** for example "build first what happens during the day" and "an AI that edits the plan, not one that chats".
  - **What it is NOT**, in 3 bullets.
- **Shared brief** (`research/00-brief.md`, ≤30 lines). Every research agent reads this:
  - the concept;
  - the user's moments in order (travel: plan → prepare the next day at night → live the day);
  - pains per moment;
  - which moment matters most;
  - what is explicitly later (travel: community);
  - research rules (see stage 2).
- **Launch stage 2 research in parallel** as soon as the brief exists. Draft the vision while the agents run.
- No sub-agents are needed for this stage itself.

## What gets produced
- `docs/01-vision.html`: one page that reads in 2 minutes, mobile-first, with `annotate.js`.
- `research/00-brief.md`.
- **Canon:** mission, principles, MVP goal and what it is NOT. **State:** the person's literal phrases (they are the best copy later).

## Checkpoint
- Send the link plus a 5-line summary (mission, statement, the 3 principles).
- Ask one thing: "What resonates, and what would you change?"
- **If they answer "I don't know":** offer the 2 alternative statements side by side, recommend one and mark it as the default.
- **If something feels off but they can't say why:** ask "Which sentence would you remove?" Removing is easier than writing.

## Lessons from the thread (avoid from the start)
- **Don't ask about business model, pricing or monetization.** In the travel case, after the research of failed apps, the agent asked "how would this get paid for?". Franco: "I don't care about the business model; the MVP goal is to be useful enough to be used and recommended."
- **Don't plan technical research the person didn't ask for.** Franco cut it immediately: "React Native for sure, you can skip all that".
- **Don't ask meta questions before showing value.** "Is this just for you or a product for others?" was asked twice before anything existed, and Franco ignored it. If you need it, infer it from question 2.
- **Write the pains in the order the user lives them, and mark the most important moment.** That ordering split the research cleanly into fronts. The six travel agents all started from the same brief and their outputs fitted together.
- **Keep the person's words verbatim.** "If you travel, enjoy it; don't spend it planning" became the north star. A paraphrase would have lost it.
- **Mark hypotheses that are the person's experience, not data.** Travel examples: "people plan at night, tired", "it's full, change it". Research has to confirm them or flag them as "validate with users".
