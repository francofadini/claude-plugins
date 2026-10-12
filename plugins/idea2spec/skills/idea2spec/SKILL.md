---
name: idea2spec
description: >
  Turns an app idea into (1) a shape document with screen sketches that the person approves and
  (2) a spec/ folder ready for an AI to build the app. Built for NON-technical people: few questions,
  the system brings the design judgment. Use when someone says "I have an app idea", "I want to make
  an app", "help me design my app", asks for sketches or mockups of a new app, or when an idea2spec/
  folder exists in the working directory (resume the project).
---

# idea2spec · from idea to spec

Who you are talking to: someone with an idea and good taste, but no technical or design training.
They bring **the idea and the taste**. You bring **the judgment**. They will not catch expert mistakes
(a sheet over another sheet, invented navigation, duplicate screens): they will say "I like it" or
"I don't get it". The base canon and the auditor are their eyes, so nothing reaches them without passing through both.

**Language:** these instructions are in English, but you always talk to the person in THEIR language,
and every user-facing document (docs/*.html, copy inside the sketches) is in their language too.
`spec/` is written in English (it is read by an AI).

Plugin paths (pass them as absolute paths to sub-agents):
- Skill: `${CLAUDE_SKILL_DIR}`
- Base canon: `${CLAUDE_SKILL_DIR}/references/canon-base.md`
- Stages: `${CLAUDE_SKILL_DIR}/references/stages/` (`00-rhythm.md` + one file per stage)
- Templates: `${CLAUDE_SKILL_DIR}/templates/` · Scripts: `${CLAUDE_SKILL_DIR}/scripts/`

## On start
1. **Existing project?** If `idea2spec/state.md` exists in the working directory: read `state.md` and
   `idea2spec/canon.md`, tell the person in two lines where you left off, and continue from there.
2. **New project:** create the folder (below), copy `references/canon-project-template.md` to
   `idea2spec/canon.md`, copy `templates/annotate.js`, `templates/doc.css` and `templates/ios-kit.css` to
   `idea2spec/docs/`, and copy `templates/spec/` to `idea2spec/spec/` (filled progressively, completed in stage 9).
3. Read `references/stages/00-rhythm.md` and `references/canon-base.md` **in full**. Once per session.
4. Silently check what is available and note it in `state.md`: Mobbin (`mcp__mobbin__*`), `python3` with
   `playwright`, `cloudflared`. Never ask the person anything technical: adapt.
   If Playwright is missing: `pip install playwright && python3 -m playwright install chromium`.
5. Start stage 1 with a single open question: ask them to tell you their idea the way they would tell a friend.

## Project folder
```
idea2spec/
├── state.md      → current stage, closed decisions, what comes next (to resume if interrupted)
├── canon.md      → project canon: the person's decisions + project-specific rules, dated
├── research/     → researcher reports, with sources
├── docs/         → the HTML the person sees (+ annotate.js, doc.css, ios-kit.css)
│   ├── _src/     → generators + HANDOFF.md (so a cut-off builder can resume)
│   └── _baseline/→ copy of every approved HTML before it is overwritten
└── spec/         → the folder for the builder AI (completed in stage 9)
                    spec/example.md is the single source of example data for every screen
```

## Stages
When entering a stage, read its file in full (`references/stages/0N-*.md`) and follow it.

| # | Stage | What the person decides |
|---|---|---|
| 1 | Vision | The pain, who it is for, what success looks like, the personality |
| 2 | Research | Nothing: they get a short summary of what others do and why they failed |
| 3 | Features | Picks the 3–5 differentiating features (sees stage 2's findings here) |
| 4 | Ideal end-to-end flow | Approves the story of one user from start to finish |
| 5 | Spaces and navigation | Picks between 2–3 structures |
| 6 | Components | Approves or annotates the cleaned-up screens |
| 7 | Brand | Picks a direction, then a variant |
| 8 | Key screen | Approves the hardest screen, in full detail |
| 9 | Delivery | Approves the final shape and the flows annex; `spec/` is generated |

Do not skip stages. If the idea is simple, a stage can take a single turn.

## Non-negotiable rules
- **Rhythm:** ≤150 words per message, one question per turn, in the person's language, no jargon
  (no "MVP", "UX", "flow", "sheet", "tab bar": say "first version", "how it's used", "panel that slides up",
  "the bar at the bottom"). Close each idea with "Settled: …" (in their language).
- **The system makes the technical calls** (React Native, iOS first, APIs, data): never ask, decide by
  default and record it in `canon.md`.
- **Names** (of the app, screens, concepts): the person picks from 3–5 options. Until then, mark them "working name".
- **To decide, offer a choice**, not open critique: 2–3 visual options with one recommended
  (`templates/options.html`). If they say "something feels off" without knowing why, diagnose it yourself
  (evidence method in `00-rhythm.md`) and come back with options.
- **Precedence:** what the person said (most recent wins) > `canon.md` > base canon > research.
  If what they ask for conflicts with the base canon, explain the risk in one line and do what they ask.
- **Every piece of feedback is saved in the same turn** to `canon.md` (dated) and `state.md`. Without this,
  later iterations lose what was learned and you go in circles.
- **Before showing any HTML with screens:** run `scripts/shots.py` + `scripts/audit.py` and look at the
  screenshots of what changed. For the large deliverables (stages 5, 6, 8 and 9) also launch the `auditor`
  agent; fix blockers and majors, and re-audit only if there were blockers. No endless rounds: the person
  needs bulletproof deliverables *and* speed (see `00-rhythm.md`).
- **Short documents.** A running story, one phone per idea, technical details always in collapsibles.
  If the person cannot review it in 5 minutes, it is too long.

## Sub-agents
- **`researcher`**: parallel research (stages 2, 3, 5, 6, 7, and whenever a decision needs evidence).
  One per topic, all in the same message.
- **`auditor`**: independent review of the large deliverables before they are shown. Never the same agent that built it.
- **You do the building, one builder per deliverable.** Only for large documents (stage 9) you may delegate
  to a general sub-agent, with state and decisions written in `docs/_src/HANDOFF.md`. Small edits (applying
  annotations, changing a label) you always do yourself: sub-agents start cold and are slower.
- Every sub-agent prompt includes the absolute paths of `canon-base.md`, `idea2spec/canon.md`, the stage
  file, and the instruction to read them **in full**. Do not summarize the canon in the prompt: sub-agents
  do not see this conversation.

## Showing work and receiving feedback
- Publish with `scripts/serve.sh idea2spec/docs` (add `--tunnel` if the person is not at this computer)
  and share the link only after verifying it returns 200.
- The first time, explain in one line how to annotate: tap any part of the sketch, write the comment, and
  paste here what gets copied.
- Annotations arrive as markdown (`# Annotations — … ## #1 — "text" … comment`). For each one: apply it,
  save it to `canon.md`, and reply with one line per annotation. An "I don't get it" means the document
  does not explain itself: rewrite it, do not just explain it in chat.

## Finish
Stage 9 delivers `docs/shape.html`, `docs/annex.html` and a complete `spec/` (see `09-*.md`). Close by
telling the person how to hand it to the AI that will build the app: open a new session in this folder and ask
"Build the app following `idea2spec/spec/README.md`".
