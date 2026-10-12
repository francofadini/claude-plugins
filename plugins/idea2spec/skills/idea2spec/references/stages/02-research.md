# 02 · Research: competition, failed apps, user voice

**Goal:** learn what others do, what users complain about and why earlier attempts died. Find the gap the MVP should own.
**Done when:**
- Every front has its `.md` with cited sources and downloaded references.
- The synthesis lists:
  - 3–5 findings with data;
  - the gap;
  - the person's hypotheses that research did NOT confirm;
  - a failed-apps gallery with real screenshots.

## What to ask the person
Nothing. This stage is informative. Its results are shown together with stage 3, so the person makes one decision with everything in view.

## What the agent does
Launch all fronts in parallel in a single message (they take 5–20 min). Every agent reads `research/00-brief.md` and `canon.md` first.

**A. Competition, one front per moment of the user journey** (3–4 agents). Travel example: planning/inspiration, tomorrow's plan, during the day, changes on the go.
- Use Mobbin when available (`mcp__mobbin__search_screens` / `mcp__mobbin__search_flows`, platform iOS). Otherwise use web search plus App Store pages.
- Per app: tabs, how it solves this moment, what it does with AI, and what to copy or avoid, and why.
- Look at the images for real; don't describe from metadata.

**B. Failed apps with post-mortems** (2–3 agents, split by era). Travel example: giants that shut down, pre-AI startups, AI-era wrappers.
- Get real screenshots from archived App Store pages (Wayback Machine → `mzstatic`), press or Mobbin.
- Why it failed, with sources: official statements, founder post-mortems, press.
- Does our idea differ? Mark it green (we differ), yellow (partly) or red (direct risk).
- Then the general lesson. Travel: "planning doesn't retain, executing the day does"; "if it sends you to another app to move, you are Google Trips".

**C. User voice** (1 agent).
- Sources: App Store reviews (`apps.apple.com/...?see-all=reviews`), Trustpilot, recent surveys and press.
- Reddit blocks agents (400/403). Don't waste time; say it in the report.
- Quote literally, with stars and date.
- Mark competitor blogs as `[vendor]`.
- Verdict per pain from the brief: CONFIRMED / WEAK / NOT FOUND.
- Also report new pains the person didn't mention.

**Optional D.** One front for anything the brief flags as "later but key" (travel: community and place cards), only to keep the MVP from blocking it.

**Never:** technical feasibility (the stack is fixed), pricing research, or naming.

### Rules for every research agent (paste them in the brief)
- Cite every screen with its `mobbin_url` or link.
- Mobbin `image_url` links expire after about 30 days: download the strongest ones (max ~12 per front) to `research/img/<front>-<app>-<desc>.webp`, then open and check them.
- Mark evidence vs inference. For studies: `[V]` full text read, `[A]` abstract only, `[S]` secondary citation. Mark your own reasoning `(inference)`.
- If an app is not in Mobbin, say so and use web sources, marked as such.
- Write in the person's language, concise, ≤1,200 words, with an explicit opinion.
- Never invent product or feature names. Use working names, marked as such.
- Final report to the coordinator: the file path plus 8 lines.

### Output format per file (`research/0N-<front>.md`)
1. Table of apps × what matters for this moment.
2. N patterns, each with its reference link and an image if downloaded.
3. What we would copy, what we would avoid, and why.
4. Open questions (for the coordinator, not for the person).
5. Sources.

## What gets produced
- `research/01..0N-*.md`, `research/failed/*.md` and `research/img/`.
- `docs/02-research.html`:
  - findings, each with one number and its source;
  - "what research did not confirm (to validate with users)";
  - the failed-apps gallery with screenshots and the green/yellow/red marks, mobile-first.
- **Canon:** the gap (the "why us") and the failure modes to avoid, as rules. Travel: "navigation lives inside the app, never a link to Maps as the main path".

## Checkpoint
There is no separate checkpoint. Send the link and 3–4 bullets in the stage 3 message. If the person reacts ("that's not how I lived it"), log their words in `state.md` and the canon.

## Lessons from the thread
- **One shared brief made 6 parallel agents coherent.** Splitting fronts by user moment, not by app, produced outputs that slotted straight into features later.
- **Real screenshots of failed products were what Franco valued most.** He asked for them explicitly ("I want to see what the experience was like, even if they're dead"). Text alone doesn't do it.
- **Don't propose a structure (tabs) in the synthesis.** The agent offered "A/B/C tab structures" here. It was premature: Franco ignored it, and the real structure came out of dedicated research in stage 5.
- **Don't wait on an agent that says "waiting for a sub-agent".** Read its output file. In the travel case the document was already written while the agent claimed it was still waiting.
- **Say what research could not confirm.** Three of Franco's core hypotheses had no external evidence because Reddit was blocked. Saying so kept the team honest, and they went to "validate with users".
- **The strongest findings were behavioural, not feature lists.** Travel examples:
  - "Apps serve planning, not the day of the trip."
  - "No AI travel app edits the plan; they all chat."
  - "52% of ChatGPT itineraries send you somewhere outside its opening hours."

  Look for that kind of gap.
