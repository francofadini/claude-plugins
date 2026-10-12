# 05 · Spaces and navigation

**Goal:** define a fixed structure in which the user always knows where they are and where they can go. It covers:
- tabs and what lives in each;
- how you enter and go back;
- multiple instances of the main object;
- states over time;
- where each notification lands.

**Done when:**
- Every storyboard moment has a place in the structure.
- Every row of the states matrix has a screen.
- The chrome is native iOS.
- The person can answer "where are you, how do you go back?" for any screen.

## What to ask the person (minimum)
Example questions are in English; translate them into the person's language.
- "Besides [main object, e.g. trips], is there another big thing people will do often in the app?" This detects a second vertical early. In the travel case, Search/Explore showed up late ("this should be almost a vertical") and changed the tabs.
- "Can someone have several [trips] at once, or one after another?" Only if stage 4 didn't answer it.
- Everything else is decided by the system with evidence.

## What the agent does
**Never propose a structure before researching.** Launch 4 fronts in parallel:
1. **Same-domain apps.** How they show 0, 1 and N instances, upcoming vs past, and how the app changes before, on the day, during and after. Use Mobbin iOS and look at exact tab bars.
2. **Apps with a "live mode".** Delivery or rides in progress, flights, theme parks, events, "Today" apps. How the active thing coexists with the tabs.
3. **Apps of the dominant interaction** (map, feed, chat, editor…). What happens to the tabs during the main task.
4. **Principles:** Apple HIG, NN/g and object-oriented UX (an objects map with attributes, relations and actions), plus how to run a cheap tree test with 5–8 people.

Then the coordinator writes the proposal. Build it with one builder using the iOS kit. Then, in parallel:
- **Defect reviewer** (fresh agent). It walks every state and the key hours: first use, weeks before, the day it starts, morning, mid-task, night, the last day, after, two overlapping instances. It reports each defect with severity and a fix.
- **"How does the live mode start and end?"** Only if the app has one. Prefer automatic start when the time is known, with an optional manual "start now", and automatic end. Check what the OS allows.
- **Native chrome kit check.** iOS 26 Liquid Glass: back is a chevron only, icons instead of words, floating panels.

## What gets produced
`docs/05-spaces.html` (iOS-basic greyscale) with:
- the spaces map;
- 3–4 rules for never getting lost;
- a "screens over time" strip with one phone per state;
- an enter/exit table plus "where each notification lands";
- the storyboard moments placed in their space.

Also `research/05-*.md`. **Canon:** the structure rules and each defect as an antipattern.

## Checkpoint
- Send the link plus 5 bullets.
- **Comprehension test** instead of "do you like it?": show 2–3 phones from the strip and ask, one per turn, "Where are you here, and how would you go back?" or "Where would you tap to [usual task]?" Wrong answers are defects. Fix them, don't explain them away.
- **If they say "it's quite bad" without detail:** research more before proposing again. Don't defend the proposal.

## Lessons from the thread (avoid from the start)
- **The first proposal was made without research and was rejected:** "You missed the flow of having several trips, the 'Today' is weird when it isn't today yet; you need to learn and research a lot." The research reversed the core of that proposal.
- **Tabs never change, hide or depend on state.** A "Today" tab is empty or odd most of the time, because "today" is a *state*, not a place.
- **What changes over time is the content, not the structure.** Before the trip, show a countdown, not an empty day.
- **Multiple instances** go in one list ordered by state: in progress, then upcoming, then past.
- **The live mode is a persistent bar or a Live Activity, not a tab.** It starts on its own when the time is known. Franco asked, "Do I have to start it manually? That's unclear."
- **Invented chrome hurts.** Franco: "use iOS navigation and its guidelines by default (what's there is an invention)". Later: "I liked that the sketches are basic iOS; it helps us focus on functionality."
- **Don't over-solve edge cases the person scopes out.** On multi-city: "don't solve it for now; that's two trips".
- **Check the scope inventory.** "I feel we lost the search; we must have a great search." Each structure change must keep every in-scope feature.
- **Scope the second vertical.** "You should only explore where you have a trip; it's for planning a trip, not choosing a destination." Ask what it is *for* before designing it.
- **Never a panel on top of a panel.** One way to see each thing; no read-only duplicate of an editable screen.
