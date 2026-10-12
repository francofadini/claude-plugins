# Project canon · [app name or working name]

Version [N] · [YYYY-MM-DD] · Sources: [interview, user notes, approved documents, research].

The project's memory: every rule that is specific to this app, one line each, with its source and date. It complements `canon-base.md`; when they collide, this file wins, and the user's most recent word wins over both. Every name here is a working name unless marked "decided" (the user decides names). Codes per section (`PJ1`, `ST3`…) are for citing in audits. Remove the instruction lines (in italics) as sections get filled; leave a section with "—" if it does not apply yet.

---

## 1. Mission and promise
*One line for the mission (who it helps, to do what, without what pain), one line for the promise as the person would say it, and the MVP goal (default: useful enough to be used and recommended).*

## 2. Product principles
*3–5 principles that decide trade-offs in this app, each with a short sentence of what it implies on screen (e.g. "The app proposes, you choose: it arrives with an option already chosen"). Mark which come from canon-base and which are the project's own.*

## 3. What the app is NOT
*Explicit non-goals and out-of-scope features (and "after the MVP" items), each with the reason or the user quote. Include adjacent jobs it reminds about but doesn't manage.*

## 4. Users and core moment
*Who it is for (one line per segment), the core moment the app is designed for, and the list of usage moments mapped to the CO1 budget rows (which moments exist in this app and which budget each uses).*

## 5. Objects and structure
*The object map (object · key attributes · relations · main actions), the root object and the fixed hierarchy, the spaces/tabs (or "no tab bar" and why), and what is a state rather than a section.*

## 6. Key screens and their states
*One entry per object screen: template (P1–P5), the question it answers, its anchor, its states (state changes content, never structure), its primary action, and how one gets there (entrances) and leaves.*

## 7. Flows
*Numbered in the order of real use. Each: where it starts (what is tapped, on which screen), the steps as screens, where it ends, and its variants (each with its own start and end).*

## 8. Modality and navigation decisions
*Project-specific applications of MO rules: which tasks are push, sheet, large sheet or full screen; allowed exceptions (e.g. one modal sheet over a full-screen view); the persistent accessory or Live Activity if any; notifications and the screen each one opens.*

## 9. Content budget and copy
*The language and register chosen (default: the person's language, neutral variant; Spanish with "tú"), the voice and persona if any, where the "why" is allowed, time and date formats, and any project budget that differs from CO1. Forbidden terms do not go here: they go in `spec/forbidden-copy.txt` with their replacement.*

## 10. Working glossary
*Table: concept · how the app says it · status (working / decided, with date) · source. One concept, one name. Include tabs, sections, states, buttons and the app name.*

| Concept | In the app | Status | Source |
|---|---|---|---|
| | | | |

## 11. Brand and visual system
*The chosen direction and its concept in one line; typefaces (role of each), color tokens with hex and the single accent, imagery treatment, textures, radii, intensities (calm vs on the move), and the project's components inventory (each object's ONE shape). Only what the user approved; options under review go to §14.*

## 12. Data, content and technical constraints that shape the design
*Data sources and what must be true (validated vs inferred), licenses that limit what can be shown or stored, offline behavior, platform/stack decisions (default: React Native with Expo, iOS first) and native modules needed. Technical detail folds into collapsibles in documents.*

## 13. User decisions (log)
*Dated, most recent last, with the user's words when possible: "YYYY-MM-DD · decision · quote/source". Includes reversible defaults the coordinator applied ("default, reversible") until the user confirms.*

## 14. Project anti-patterns
*Errors already seen in this project, each as "the error → the rule that prevents it", with date and source. If one reappears, the audit fails.*

## 15. Open and pending
*Split in: pending user decisions (names first) · conflicts between sources (state both sides, the applied default, and that it awaits the user) · to test (evidence questions a user decision; not changed without their OK) · technical validations before drawing more.*
