# 00 · Rhythm: how to run the whole process with a non-technical person

The person brings the idea and says "I like it" or "I don't get it". The system supplies the design judgment. If the person finds an expert-level mistake, the process failed.

Talk to the person in THEIR language. Every example question in these files is in English: translate it into the person's language and register.

## Messages
- **≤150 words and one question per turn.** If you have three doubts, ask the most important one. The others wait.
- **No jargon in the chat.** Never say "sheet", "push", "HIG", "segmented control", "tab bar" or "deep link". Say "panel that slides up", "new screen" or "tabs at the bottom". If a technical concept matters, explain it in one line or let the system decide it.
- **Close every idea with "Settled: X"** before moving on. Only then write it to the state file and the canon.
- **A one-off question is just a question.** Answer it in the chat and do not touch any document. Travel case: Franco asked whether Citymapper was born for travelers and the agent edited the gallery. His reply: "I didn't care about the doc, I just wanted the answer".
- **What the system decides is announced, not asked:** "I set X by default. If you prefer something else, we change it." Every default is reversible.
- **Open questions live in the chat, one at a time.** Never put a "questions for you" list at the end of an HTML. In the travel case, almost every such question came back as "I didn't understand".
- **Language of the app:** the app copy uses the audience's language, neutral, with no regionalisms from either the agent or the person. Avoid "we": write sentences centred on what happens ("Your Tuesday changed: rain in the morning").
- **While something runs, say what is running and how long it will take.** If the person asks "still going?", tell them what is left, without promises.

## State and memory (to resume, and to avoid going in circles)
Everything lives in the user's project folder, `idea2spec/`:
- **`state.md`:** current stage, last checkpoint and next pending question. It also logs each "Settled: X" with its date and **the person's literal words**. Update it every turn, not at the end.
- **`canon.md`:** the current product rules (one line each, with source), antipatterns (each mistake already flagged, with the rule that prevents it), a working glossary and open items.
  - **Every piece of feedback goes into the canon in the same turn.**
  - Precedence: what the person said (most recent wins) > decisions from approved stages > research.
- **Other folders:** `research/`, `docs/` (the HTML the person sees), `docs/_src/` (generators plus a `HANDOFF.md`) and `spec/` (stage 9).
- **Where files go:**
  - Generators and outputs always live inside `idea2spec/`, never only in `/tmp`.
  - Before overwriting an approved HTML, copy it to `docs/_baseline/`.

Travel case: after 4 days the rules were spread across 20+ documents, and "never a panel on top of a panel" came back. Franco: "We are going in circles; you lose the feedback from past analyses". A single canon fixed it.

## Sub-agents: when and when not
- **Yes, in parallel, in a single message:**
  - research (3–6 independent fronts);
  - audits from different angles;
  - the independent review of a large deliverable.
- **No:** small edits, applying three annotations or changing a label. The coordinator does those directly, because a sub-agent starts cold and is slower.
- **One builder per deliverable.** In the travel case, four documents were built in parallel on the same object (the day). The result was "several screens for the same thing", and they had to be unified.
- **Every sub-agent that designs or builds reads `canon.md` in full.** Give it the path; do not summarize the canon in the prompt. Sub-agents do not see the conversation or the memory.
- **Spawn fresh, with explicit context, for new tasks.** A resumed agent may believe it is "waiting" without doing anything. Check the output file instead of waiting.
- **Research brief:** the concept, the pains in the order the user lives them, citation rules and the output format (see stage 2). The agent's final report is 8 lines.

## Publishing the HTML
- **Serve it:**
  - Serve `idea2spec/docs/` locally (`python3 -m http.server` on a free port).
  - If the person is not at the computer, open a tunnel (`cloudflared tunnel --url http://localhost:PORT`) that exposes **only** `docs/`.
- **Check it:** confirm with `curl` that it returns 200, and look at a 390 px screenshot before sharing the link. Never share an untested link.
- **Every HTML** is responsive (it gets reviewed on a phone) and includes `annotate.js` before `</body>`.
- **The first time,** explain in two lines: "Tap **Annotate**, tap anything and write what you think. When you're done, tap **Finish** and paste what was copied here."

## What gets reviewed before showing anything
The reviewer is the expert eye the person does not have.
1. **Builder checks.** The builder runs its own checks: Playwright at 1000 and 390 px for console errors, horizontal scroll, collapsibles that open and the canon's forbidden terms. Then it looks at a screenshot of every screen that changed.
2. **Independent review of large deliverables.** For stages 5, 6, 8 and 9, a **fresh reviewer** who did not build it reads the canon and reviews with judgment. It checks:
   - where you arrive at each screen from and where you go next;
   - panels stacked on panels;
   - duplicate screens for the same thing;
   - more than one primary action;
   - text that explains the system;
   - example data that contradicts itself;
   - anything the person already flagged.

   Severity: blocker / important / minor.
3. **Fixes.** Fix blockers and importants. Re-review only if there were blockers. No endless rounds, no mutation testing and no measuring map coordinates: sketches are sketches.

Travel case: without a reviewer, Franco kept catching basic errors ("I need bulletproof deliverables"). After 8 audit rounds he complained about speed: "I don't want so much auditing; if the agents have the context they need, that's enough for me". The middle ground is the procedure above.

## Checkpoints and duration
| Stage | Checkpoints with the person | Agent time |
|---|---|---|
| 1 Vision | 1 | 15–25 min |
| 2 Research | 0 (informative, shown with stage 3) | 20–40 min in parallel |
| 3 Features | 1 | 10 min |
| 4 Ideal flow | 1–2 | 30–45 min |
| 5 Spaces | 1–2 | 45–75 min |
| 6 Components | 1 | 45–75 min |
| 7 Brand | 2 | 60–90 min |
| 8 Key screen | 1–2 | 45–75 min |
| 9 Delivery | 1–2 | 90–150 min |

- **Total:** **10 to 14 checkpoints**, about 6–9 h of agent work and 2–3 h of the person's time.
- **Calendar:** 2 to 4 days if the person replies the same day.
- **Benchmark:** the travel thread took 6 days with an expert, and more than half of that was avoidable rounds.

## Always
- When starting a stage, say what will happen and when you will be back with something to look at.
- When closing a stage, update `state.md` and `canon.md` and say in one line what comes next.
- If Mobbin shows its usage notice, show it to the person verbatim.
