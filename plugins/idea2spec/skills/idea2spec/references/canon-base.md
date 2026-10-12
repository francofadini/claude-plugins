# Base canon · consumer mobile apps (iOS first)

Generic product and design criteria that apply to any consumer mobile app. The project canon (`canon-project-template.md`, filled per project) adds what is specific. Read both entirely before designing, building, iterating or auditing any screen, flow or spec, and pass both to every subagent.

- Each rule has a code (`NA3`) to cite in audits. Format: rule — why.
- **(default)** = applied unless the user decides otherwise; if they do, record it in the project canon with its date.
- Precedence: (1) what the user said, most recent wins; (2) project canon; (3) this base; (4) research. A conflict that this order does not resolve is asked, never resolved silently.
- Examples in parentheses come from a travel app and only illustrate; the rule is generic.

---

## 1. Method (how decisions are made)

- ME1 · Evidence over opinion: when there is a hypothesis or a screen "doesn't feel right", decide with studies + real apps (Mobbin, HIG, NN/g), not taste — it was the method that worked best (e.g. "one reference image at a time" was confirmed by research before changing the flow).
- ME2 · What the user said wins, and the most recent statement wins. Never change a user decision because evidence questions it: list it under "To test" in the project canon and ask.
- ME3 · Names are the user's call: every feature, section, state, button and app name is a working name until the user picks one. Offer 2–4 options; never settle one alone. Mark working names in documents (dotted underline).
- ME4 · Don't invent what isn't decided: open questions go to "Open"; if work cannot stop, apply a reversible default, say it is a default, and record it.
- ME5 · Read the canon before every iteration: improvements that ignore past feedback make the project go in circles. Every new rule from the user goes into the project canon the same day, with date and source.
- ME6 · Model objects before screens (objects, relations, actions, attributes): screens come from objects, so "Today" ends up a state of a Day, not a section.
- ME7 · Walk every proposal through every state: empty, first use, one item, many items, in progress, finished, after — structures that only work in one state get rejected.
- ME8 · Ask the user the minimum: one question per turn, with the options visible; a non-technical person approves outcomes, not internals.
- ME9 · The example data is one table: names, times, sums and counts on every phone come from a single source, so phones never contradict each other.
- ME10 · The example is plausible and true where the user would notice (a place closed that day, a flight that doesn't exist); exactness beyond that is not audited (sketches are sketches — criterion over precision).
- ME11 · If a fix turns into a fragile workaround (manual offsets, per-platform math), stop and look for the idiomatic API or community standard first.
- ME12 · Audit before showing: run `scripts/audit.py` + a visual pass (`checklist-qa.md`); deliver with 0 B and 0 I. Keep it proportional: no mutation suites or re-audits unless asked.
- ME13 · Documents for the user: short (≤10 min of reading outside phones and collapsibles), technical detail folded in collapsibles, no rule repeated, nothing shown as "open" that is already applied, the final deliverable never compares with older versions, every technical term explained in one line the first time.
- ME14 · Flows are documented in the order of real use; each flow says where it starts (what the person taps, on which screen) and where it ends; every action on a phone has its destination drawn or stated.

## 2. Product

- PR1 · MVP goal: useful enough to be used and recommended. Business model, pricing and monetization are out of scope **(default)** — they distort the shape before the core is proven.
- PR2 · State the mission in one line, the promise in one line, and 3–5 principles that decide trade-offs — principles that don't decide anything are decoration.
- PR3 · Find the core moment (the job the app does better than anyone) and design for it; everything else is the entrance door (e.g. the day on the street, not trip planning).
- PR4 · Write what the app is NOT. Out of scope **(default)**: social features (feed, profiles, followers), community, imports from other apps, payments, admin tools, multi-account, gamification — added only if they serve the core moment.
- PR5 · Don't manage what isn't your core: remind and link out instead of rebuilding a third-party job (e.g. "buy tickets in advance" as a task with an external link, not ticket storage).
- PR6 · The app proposes, the person chooses: arrive with one option already chosen; change or undo is one tap.
- PR7 · Don't ask what the app can propose (start time, meals); do ask what only the person can decide (preferences, intensity) — and never pre-select it for them ("we marked you as relaxed").
- PR8 · Always true: facts come from sources and are checked against the moment they matter; "I don't know" beats a confident wrong answer.
- PR9 · Always a next step: no dead ends; whatever the person does, everything keeps working and adapts without friction.
- PR10 · Stable structure, contextual content: what changes with time is content and priority, never structure (adaptive menus measure slower and are rejected).
- PR11 · If there is AI: it is invisible in the brand (show what it does, never "AI-powered", no sparkles), it edits the object instead of chatting, and chat is never the only way to do something.
- PR12 · Desirable by beauty: minimalism, good type, detail — often the absence of things. Pleasure, never manipulation: no dark patterns, streaks, badges, counters or "come back" notifications; rewards are aesthetic and have an end.
- PR13 · Innovate in content and timing, not in navigation or chrome: an amazing experience without breaking flows and patterns people already know.

## 3. Structure and navigation

- NA1 · One root object and a fixed hierarchy (list → object → detail), at most ~3 pushes deep; everything else in sheets.
- NA2 · Tab bar only for same-level sections people visit often: 2–5 tabs (a search tab counts), never "More". With a single main object, no tab bar (the Apple Maps model).
- NA3 · Tabs are for navigating, never for actions ("Create", "Need something now"), profile or a moment ("Today"): a moment is a state of an object.
- NA4 · No tab appears, disappears or stays empty depending on the moment — a tab that is "weird" 90% of the time is not a section.
- NA5 · Profile and settings via the avatar on the root screen → sheet.
- NA6 · Each tab keeps its own stack; the tab bar is visible except under a modal.
- NA7 · Always know where you are: every screen says which object (and which part of it); one visible way back; returning to the hub is one tap.
- NA8 · One screen per thing: each object has ONE screen for all its states (empty, ready, in progress, past); states change content, never structure. No "view-only" duplicate — users edit where they look.
- NA9 · Don't duplicate views or entrances: needs that are the same interaction (something closed, plans changed, I need X now) are ONE interaction, not five screens.
- NA10 · No orphan screens: every screen has a known entrance (tab, push, notification, accessory) and exit; a notification opens its object inside its hierarchy with a coherent back stack.
- NA11 · Nothing variable above fixed controls: a row whose presence depends on data (alerts, pending tasks) has a fixed height and only changes its text, so the screen doesn't seem to change.
- NA12 · An ongoing activity lives in a persistent accessory (Music mini-player pattern) and a Live Activity, not as a screen that replaces others. If there is a mode, show it with ≥2 signals.
- NA13 · Saving something doesn't force a second decision: it goes to the collection, organizing comes later (e.g. "Add" → the list, never directly to a day).
- NA14 · Empty states: one action, inside an anchor block that previews what the person will get — never half a phone of nothing.
- NA15 · Permissions are asked at the moment of value with the why in one line, never at first launch; without the permission the app still works in a reduced way.

## 4. Modality and iOS (HIG)

- MO1 · Push to go down the hierarchy (‹). Sheet for a short task. Large sheet for a multi-step task (create X). Full screen only for immersive content (stories, camera, loading moment).
- MO2 · **Never a sheet over another sheet** ("Display only one sheet at a time", HIG). Inside a sheet, replace its content or push inside it (Apple Maps: place → directions); choosing closes it and returns with Undo.
- MO3 · Allowed: one modal sheet over a full-screen base that is not a sheet; nothing inside it may open another sheet. System pickers opened from a sheet go full screen.
- MO4 · No "app inside the app" in a modal: one linear hierarchy inside it.
- MO5 · A bottom sheet is not a place to stay: if the person will read for a while, it is a screen.
- MO6 · One exit per screen: ‹ if you went down, ✕ if it opened on top; never both. Data sheets: ✕ leading (cancel), ✓/prominent action trailing; never Cancel + Done + Back together.
- MO7 · Multi-step flow: step 1 has ✕, later steps ‹; the action trailing/bottom; the last step ends in the final action; one datum per step.
- MO8 · Sheet over a map: non-modal, detents, grabber, the map behind stays interactive, not dismissed by swiping.
- MO9 · Rare actions go in ···; actions that fix a row go to context menu/swipe (always with a visible alternative); destructive in red and separated.
- MO10 · **Native chrome by default in sketches** (current iOS, Liquid Glass): large title, bars without background, symbols (not text) in glass circles/capsules, back = chevron only, floating tab bar, sheets with grabber and detents, system values. Never invent chrome or navigation patterns.
- MO11 · Two layers: content below (solid), glass only in the navigation layer; glass is not tinted for branding (only the prominent action and the selected tab carry the tint); never glass on glass (a button inside a sheet is a fill).
- MO12 · Touchable things are capsules or concentric shapes; targets ≥44 pt.
- MO13 · Undo instead of "Are you sure?"; undo stays until the next action, never a toast that vanishes in 4 s.
- MO14 · If the system can detect a state change, it happens by itself: no "Start the day"/"Finish" buttons as main actions.
- MO15 · Notifications: one per thing, only with a task behind, at transitions (leaving, arriving), never mid-task; no "look how interesting" pings. While an activity is live, progress goes through the Live Activity, not notifications.
- MO16 · Live Activity / lock screen (~2 s glance): 1 image or symbol + 1 phrase ≤6 words + 1 datum, 0 buttons; alert only at critical points.

## 5. Content

- CO1 · Budget per moment, as a hard limit — if something goes in, something goes out:

| Moment | Attention | Content | Decisions | Own actions |
|---|---|---|---|---|
| Browsing/planning, seated | minutes, willing | ≤3 data per row · ≤5 suggestions per batch, each with its why | 1 per screen | 0–1 primary |
| Tired / end of day | ~3 min | the delta (what changed) first, ≤7 items above the fold | ≤3 total, all with default | 1 primary |
| Interrupted (before leaving) | 1–2 min | 3 data | 0 (1 if something changed) | 1 primary |
| In motion | 4–6 s glances | 1 image + ≤12 words + 1 hint only if it helps act | 0 | ≤2 equal secondaries |
| Problem / hurry | stressed | ≤3 options, one chosen · ≤2 data each · no whys | 1 | 1 primary + Undo |
| Lock screen | ~2 s | 1 image + 1 phrase ≤6 words + 1 datum | 0 | 0 |
| After / closure | relaxed | 1 headline + ≤3 numbers | 0–1 | 1 |

- CO2 · One moment, one task: the screen is ordered by its moment's task; the rest is one tap away behind a label that predicts what opens; at most 2 levels hidden; ··· only for rare things.
- CO3 · **Only the indispensable on screen**: no explanations, justifications, system mechanics ("goes back to unassigned", "downloaded offline") or instructions inside screens ("Tap the sides to advance") — if the screen needs them, the design failed.
- CO4 · The "why" appears only where it helps decide (a suggestion, a change the app made) and fits in one line; never in rows, live views or quick fixes.
- CO5 · The normal state is not shown (a ready thing doesn't say "Ready"); a state appears once per row, as a word + symbol.
- CO6 · Each datum in one surface at a time: if the banner/Live Activity says it, the sheet doesn't repeat it.
- CO7 · Few options, one already chosen and marked (border), with Undo; ≤5 per batch when browsing, ≤3 under pressure.
- CO8 · Done things collapse into one row ("6 done ›"); what's next goes on top; importance is size (next big, later a row, past a small shelf).
- CO9 · What decides behavior goes in the title or the status line, never buried in a subtitle.
- CO10 · Situational info appears only when it applies, one at a time.
- CO11 · Bad news early, at a calm moment (the night before, before leaving), never when the person is on the way.
- CO12 · Exact clock times only for anchors (bookings, departures); the rest relative ("in 25 min", "in the morning"). One date format and one relative scale in the whole app; no abbreviations (**default**; system pickers use the system format).
- CO13 · No visible numeric thresholds or rigid rules where the AI can decide with context (radius, minutes, load limits); no fixed counters.
- CO14 · Rows: ≤3 data, at most two "·"; titles and sentences, none.
- CO15 · When an image is the instruction, one reference image at a time; what comes next is text or paged one by one.
- CO16 · Color never alone (always with a word); the accent only on what is tappable and "now"; red only for destructive/closed; semantic colors as text or symbol, never as backgrounds.
- CO17 · Closed or unavailable items are shown marked, not hidden; data without a confirmed source is not shown.

## 6. Copy

- CP1 · The app's copy is in the person's language, in its neutral variant: no regionalisms, slang or informal terms **(default)**. Spanish → "tú" **(default)**; voseo or "usted" only if the user chooses it.
- CP2 · Voice as Apple suggests: plain, concise, no "we" and no first person for the app; impersonal or object-centered sentences ("Your Tuesday changed: rain in the morning"). If the project canon defines a persona, it shapes word choice, never this rule.
- CP3 · Never blame the person; the subject is the plan, the route or the system ("You went a different way", "Te desviaste" — never "You got lost", "Te perdiste"). Never ask whether they made a mistake.
- CP4 · No hype: no "perfect", "magic", "amazing", "smart", "AI-powered", no sparkles icon or violet "AI" gradient; if we don't know, say so.
- CP5 · No exclamation marks and no emoji (SF Symbols instead, also for weather).
- CP6 · No invented urgency and no guilt ("tends to sell out", never "Last tickets!").
- CP7 · Buttons say what happens: verb + object for tasks ("Create trip"), first person to report ("I'm here"); never "OK" or "Accept".
- CP8 · The first two words say what it is about; one idea per sentence.
- CP9 · Sentence case; no sustained capitals except one small label per screen.
- CP10 · One concept, one name, one component across all screens; same datum, same text everywhere.
- CP11 · The options of a choice sound equally good: none phrased as "less".
- CP12 · Read-aloud test: would a knowledgeable person say it like that, quietly, next to you? If it sounds like a system, a salesperson or a manual, rewrite.
- CP13 · Every word the user rejects goes to `spec/forbidden-copy.txt` with its replacement (format in `scripts/audit.py`), so it is checked automatically from then on.
- CP14 · Document text addressed to the user may be conversational; screen copy may not.

## 7. Visual composition

- CM1 · Template first, then the screen: every screen declares one of five templates and respects its zones (working names):
  - **P1 Hub** — compact masthead (≤18% of height) → anchor block (the next or main thing, with image) → 1–3 shelves, each with its own shape.
  - **P2 Index** — header with the object's state as anchor → fixed status/tasks row → segmented control → list (the next item in a block, the rest loose).
  - **P3 Detail** — full-bleed image (~40%) → title + one line → data row in 2–3 columns → sections (spacing or band) → fixed primary at the bottom.
  - **P4 Map + sheet** — map 55–62% → sheet whose title is the state → the next-step block → band → what follows.
  - **P5 Moment** — label → display → figure → 2-column table → foot on the margin (cover, closure, empty states).
- CM2 · One question per screen and one anchor of content that answers it: 25–45% of the first view in hubs and details, 20–25% in indexes. The large title is not the anchor; if nothing under it weighs more than a row, the screen is unfinished.
- CM3 · Three spacing levels in ~1:3:6 (≈12 inside a group · 44 between groups · 64 or an 8 pt band between zones); never less than 3:1 between groups and rows — uniform air groups nothing.
- CM4 · Margins 16–20; one text column for every row (a fixed leading column for thumbnail/icon/number, text always starting at the same x); states and times always in the trailing column.
- CM5 · Surfaces belong to content, not chrome: the protagonist and anything of a different nature go in a block; homogeneous lists stay loose. Never a card inside a sheet or inside another card.
- CM6 · Weight, not only size: every screen has at least one text at 500+; ≤2 prominent elements and ~3 text sizes per screen; a scale of ≤6 sizes app-wide.
- CM7 · **One primary action per screen (0 or 1)**, the only full-width filled button, fixed at the bottom in details and sheets. A secondary is never half-width beside it; never a full-width gray button (reads as disabled); the row "+" is neutral, the accent stays for the screen's action.
- CM8 · Each shelf in a hub has its own shape (capsules, large card, tiles, rows); importance is said with block size.
- CM9 · Empty space is anchored between things with weight; if the screen is short, the anchor grows instead of leaving half a phone empty.
- CM10 · Squint test: blurred, the screen shows 3–5 blobs, not an even gray.
- CM11 · Selected = border + size, not color.
- CM12 · No decorative rules under titles, no ornaments; separators only if spacing can't do it.
- CM13 · Accessibility: AA contrast on every background (including over photos), Dynamic Type, Reduce Motion, 44 pt targets.
- CM14 · The brand lives in content (type, color, imagery, tone); the chrome stays native. Brand exploration mockups define direction and material, never the layout to copy.
- CM15 · Two intensities when the app is used both calmly and on the move: brand at full volume while calm, quiet and system-like on the move (lock screen, glanceable views). Tone changes, structure doesn't.

## 8. Components

- CT1 · Each object has ONE shape everywhere; build an inventory and reuse it (a stop looks the same in the list, the map and the stories).
- CT2 · Object row: leading thumbnail/symbol · title = the name (never a state or a route) · subtitle = what or when · state trailing · chevron if it opens.
- CT3 · Row affordance: navigates → chevron; does something → small button; only informs → nothing.
- CT4 · An action lives in its object's row or detail, never loose far from it.
- CT5 · Filters are capsules: on = filled + ✓, off = outline, menu filters show ⌄ and the chosen value; never an × inside a chip (web pattern). Actions never look like filters.
- CT6 · Badges never carry verbs and never look like disabled buttons; badge and chevron don't compete.
- CT7 · System suggestions never hide inside the person's own content (a silent suggestion inside their list is not read as a suggestion); offer a clear entry ("Explore nearby").
- CT8 · Alerts about the screen go on top (above the sheet), not between items; an automatic-change banner says what changed and why in one line, closes with ×, and doesn't come back.
- CT9 · One thumbnail size per list; images full-bleed with text on the floor of the image, never over its focus.
- CT10 · Waiting has a shape (skeleton, the work being done in one line), never a lone spinner or an infinite loop.

## 9. Motion and haptics

- MH1 · Motion is physics, not choreography: springs without bounce, interruptible, inheriting the finger's velocity; bounce only when the finger flicked.
- MH2 · The system moves the chrome (sheets, tabs, glass, zoom); never imitate or animate it.
- MH3 · Two or three spring presets for the whole app; frequent interactions ≤300 ms; nothing makes you wait; no double tap (it delays every single tap).
- MH4 · No infinite loops (pulses, shimmer, breathing); live things move because data changed.
- MH5 · Haptics answer what the person did, with the system patterns' documented meaning (selection, impact, success, error); what the app does by itself doesn't vibrate; small vocabulary.
- MH6 · No interface sounds **(default)**.
- MH7 · Reduce Motion is mandatory: displacements become fades.
- MH8 · At most one interaction novelty per screen, always redundant with a visible path, taught by motion — never by tutorials or coachmarks.
- MH9 · The map camera never moves while a finger is on the map; it frames the free area above the sheet.

## 10. Anti-patterns already seen (each → the rule that prevents it; if it reappears, the audit fails)

### Structure
- AP1 · A tab for a moment ("Today") that looks wrong before the moment exists; structure designed for one item only → NA3, NA4, ME7.
- AP2 · Invented chrome or navigation → MO10.
- AP3 · Several screens for the same object (summary, view-only, live view, last-day view) → NA8.
- AP4 · Two entrances to the same thing ("Start the day" + a mode) → NA9, MO14.
- AP5 · Screens nobody knows how to reach; flows that don't say where they start → NA10, ME14.
- AP6 · **Sheet over sheet**, or stacked panels inside a mode → MO2.
- AP7 · Variable card above the segmented control, making the screen seem to change → NA11.
- AP8 · A feature hidden as a sheet inside an object ("app inside a modal") → MO4.
- AP9 · Five screens for what is one interaction (closed, full, detour, need X now, plan finished) → NA9.
- AP10 · Saving that forces a decision (add straight into a day) → NA13.
- AP11 · Deep links without a defined destination → NA10.

### Interaction
- AP12 · Two or three actions of the same weight; full-width gray buttons that look disabled → CM7.
- AP13 · Chips that look like filters but are actions; chip with × inside; filters that aren't capsules → CT5.
- AP14 · Badges with verbs or dates that look like disabled buttons → CT6.
- AP15 · Actions far from their object → CT4.
- AP16 · Obvious questions ("do you like eating well?"), questions the app can answer, a third option that says nothing → PR7, CP11.
- AP17 · Inferring a personal choice and pre-marking it → PR7.
- AP18 · Gestures as the only path; tutorials to teach them → MH8.
- AP19 · Notifications mid-task or "look at this" without a task; a disappearing undo toast → MO15, MO13.
- AP20 · Automatic changes without saying why, that come back after closing, or that always replace what they removed → CT8.
- AP21 · The app silently applies changes that touch something the person committed to (a booking) → propose instead.
- AP22 · Fixed numeric rules where context should decide → CO13.

### Content and copy
- AP23 · "Potpourri" screens: everything with the same weight, the sheet repeating the banner → CO1, CO6.
- AP24 · **Text that explains or justifies** ("You walked 14 km so we marked it relaxed") → CO3.
- AP25 · Whys everywhere instead of only where they decide → CO4.
- AP26 · Blame ("Did you get lost?") → CP3.
- AP27 · Regionalisms, slang and an unchosen register in the copy → CP1.
- AP28 · Subtitles with 3+ data chained by "·" burying the key one → CO14, CO9.
- AP29 · One concept with several names; several date formats → CP10, CO12.
- AP30 · Accent color on text that isn't tappable; red as decoration → CO16.
- AP31 · Example data inconsistent between phones (times, sums, names, a place that disappears) → ME9.
- AP32 · Live/real-time data where the screen isn't live (minutes from "you" in a browsing view) → CO1.
- AP33 · Two reference images at once when the image is the instruction → CO15.
- AP34 · Commercial urgency, mascots, hype → CP4, CP6.

### Visual
- AP35 · Composition without structure: no anchor, uniform air (1.9:1), surfaces only on controls, no templates, everything Light/Regular → CM1–CM6.
- AP36 · Decorative rule under titles → CM12.
- AP37 · Copying brand-exploration mockups as layouts → CM14.
- AP38 · Brand tint on glass, glass on glass, homemade glassmorphism → MO11.
- AP39 · Cards inside sheets or cards → CM5.
- AP40 · Empty root screen with half a phone of nothing → NA14, CM9.
- AP41 · Literal skeuomorphism (curled paper, tape, handwriting) and brand texture in glanceable views → CM15.

### Method
- AP42 · Iterating without reading the canon: improvements that lose past feedback → ME5.
- AP43 · Delivering without the audit → ME12.
- AP44 · Inventing feature names; resolving a user decision because evidence disagrees → ME3, ME2.
- AP45 · Technical detail in the body of the document; documents too long to review; comparing with old versions → ME13.
