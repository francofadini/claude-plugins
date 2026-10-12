# [App name] · Build spec

<!--
HOW TO FILL THIS FOLDER (delete every instruction comment like this one once filled)
- Written in stage 9 from the project canon (idea2spec/canon.md), spec/example.md and the APPROVED
  docs/shape.html and docs/annex.html. No new decisions here: if something is missing, it goes to 10-open.md.
- Audience: an AI (or developer) that builds the app without being able to ask the person anything.
  Be explicit, use IDs, give exact copy and exact values. No marketing, no history of how decisions were made.
- IDs are shared across files and documents: screens S01…, flows F1…, components C01…, rules (canon codes).
- Every "Example" block is there to show the format: replace it with the project's content.
-->

## What this app is
[One paragraph: who it is for, the problem, what the app does about it. Copy the promise from 01-product.md.]

> **Example:** A booking app for one neighborhood barbershop. Clients see the free slots of the day, book a cut in two taps and get a reminder an hour before. The barber sees the day's agenda.

## Stack and platform
- **React Native with Expo** (dev client, Continuous Native Generation), **iOS first**. Android is out of scope until stated otherwise.
- Native iOS 26 chrome through native components: native stack headers, native tabs, native sheets with detents. Never draw custom navigation bars, tab bars or sheets.
- [Backend / storage / auth decisions from canon §12, or "local only" if there is no backend.]
- Design tokens come from `tokens.json` (generate a typed `tokens.ts` from it; never hardcode a color or a size).

## Reading order
Read all of it once before writing code, in this order:

| # | File | What it gives you |
|---|---|---|
| 1 | `01-product.md` | Why the app exists, principles, MVP in/out, metrics |
| 2 | `09-rules.md` | The rules and anti-patterns you must not break. A violation is a bug |
| 3 | `02-navigation.md` | Spaces, tabs, screen map, modality, notifications and where they land |
| 4 | `03-screens/*.md` | One file per screen: states with exact copy, actions, entrances and exits, PNGs |
| 5 | `04-flows.md` | Every flow step by step (mirrors `docs/annex.html`) |
| 6 | `05-components.md` | The ONE shape of each component, states, action rules |
| 7 | `06-design-tokens.md` + `tokens.json` | Type, color, spacing, radii, motion, haptics |
| 8 | `07-copy.md` | Voice, glossary, forbidden terms |
| 9 | `08-data.md` + `example.md` | Objects, attributes, relations; seed data for development and screenshots |
| 10 | `10-open.md` | What is still pending, the default to build meanwhile, technical validations to do first |

Visual reference: `../docs/shape.html` (the story) and `../docs/annex.html` (every flow). PNGs in `03-screens/png/` are the per-state source of truth for layout.

## Precedence when two sources disagree
1. `09-rules.md` and the person's decisions logged in the canon (most recent wins).
2. `03-screens/*.md` (exact copy and states) over the PNGs; PNGs over the HTML docs.
3. If it is still ambiguous: build the default listed in `10-open.md`, never invent a new behavior, and list the question in your report.

## How to build with it
- Build screen by screen following `04-flows.md` in order (F1 first: it starts on the iOS home screen with the app just installed).
- Seed the app with `example.md`, so the running app can be compared side by side with the PNGs.
- A screen is **done** when: every state in its file exists and is reachable, the copy matches exactly, it arrives from and goes to the screens listed, it uses only components from `05-components.md` and tokens from `tokens.json`, and nothing in `09-rules.md` is broken.
