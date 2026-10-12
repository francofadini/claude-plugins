# QA checklist · shape HTML and spec

Used by the auditor agent, which is never the agent that built the deliverable. Every check cites the rule it verifies: base canon codes (`MO2`) or project canon codes. Read `canon-base.md` and the project canon first.

**Severity:** **B** blocking (breaks a user decision, the HIG, or an anti-pattern of canon-base §10 / the project canon) · **I** important (breaks a canon rule without being an anti-pattern) · **M** minor. Deliver with 0 B and 0 I.

**Unit of audit:** each phone = `figure.shot` (as in `templates/shape.html`; also `figure.fig` or `[data-phone]`) with an `id`; its screen is the `.ios-phone` (or `.frame`) inside; the `figcaption` is document text. Document text may be conversational; screen copy may not (CP14). Report the phone `id` + the text that triggers.

---

## (a) Automatic checks — `scripts/audit.py`

```
python3 scripts/audit.py <shape.html> [--forbidden spec/forbidden-copy.txt] [--lang es] [--register tu] [--shots /tmp/shots] [--json]
```
Renders with Playwright at 390 and 1000 px. Exit code 1 if any B. Hits marked "confirm"/"review" (register, tech terms, contrast M) are candidates: a human confirms each one before counting it.

| Check id | What it detects | Rule | Sev. |
|---|---|---|---|
| `console-error` | Any console error or page exception at load | — | B |
| `horizontal-scroll` | `scrollWidth > innerWidth` at 390 and 1000 px | — | I |
| `collapsible` | A `details` (or `aria-expanded` toggle) that doesn't open or opens empty | ME13 | I |
| `broken-image` / `broken-icon` | Image that fails to load; `<use href="#x">` with no target | — | I / M |
| `reading-time` | Visible text outside phones and collapsibles > 10 min at 230 wpm (summaries count) | ME13 | I |
| `tech-outside-collapsible` | API, SDK, SwiftUI, React Native, JSON, px/pt… outside a collapsible | ME13 | I (review) |
| `repeated-sentence` | The same sentence (≥8 words) twice in the document | ME13 | M |
| `sheet-over-sheet` | More than one visible sheet in a phone | MO2 | B |
| `modal-sheet-review` | One sheet + scrim: allowed only over a non-sheet full-screen base; check nothing inside opens another sheet | MO3 | M (review) |
| `multiple-primaries` | More than one full-width filled (saturated) button in a phone | CM7 | B |
| `wide-gray-button` | Full-width gray button (reads primary-but-disabled) | CM7 | I |
| `primary-hidden` | The primary is clipped by the frame or covered by another element | CM7 | I |
| `tab-count` | Tab bar with more than 5 tabs | NA2 | I |
| `chip-with-x` | Capsule with a label and an × inside | CT5 | B |
| `back-and-close` | ‹ and ✕ in the same header | MO6 | I |
| `contrast` | Text below AA on a solid background (<3:1 → I, otherwise M) | CM13 | I / M |
| `all-caps` | More than one all-caps text per phone | CP9 | M |
| `too-many-dots` | A text node with more than two "·" | CO14 | I |
| `emoji` | Emoji in screen copy | CP5 | I |
| `base-copy` | Generic voice violations: "oops", blame, OK/Accept, hype, "!" | CP3–CP7 | I |
| `register` | Spanish with "tú": voseo forms and Rioplatense slang (confirm each) | CP1 | B |
| `forbidden-copy` | Any entry of `spec/forbidden-copy.txt` in screen copy (`!` entries also in document text) | CP13 + project | B |

Not automated, check by hand with the screenshots (`--shots`): card inside a sheet (CM5), tinted glass or glass on glass (MO11), decorative rule under a title (CM12), two reference images at once (CO15).

## (b) Screen by screen (look at each screenshot for real)

For each phone answer yes/no and note the `id`:

1. **Template:** which one is it (P1 Hub · P2 Index · P3 Detail · P4 Map + sheet · P5 Moment) and does it respect its zones? [CM1]
2. **One question, one anchor:** can you say in one line what question the screen answers and what answers it? Is the anchor content (not the large title) and the right size (25–45% hub/detail, 20–25% index)? [CM2]
3. **Squint:** blurred, 3–5 blobs, not an even gray? No half phone empty? [CM9, CM10, NA14]
4. **Rhythm and alignment:** groups clearly separated from rows (≥3:1)? Text of every row starts on the same column? States and times trailing? [CM3, CM4]
5. **Surfaces:** protagonist and different-nature content in a block, homogeneous content loose? No surfaces only on controls? No card inside a sheet or card? [CM5]
6. **Moment budget:** name the moment (browsing, tired, interrupted, in motion, problem, lock screen, after) and count data, decisions and actions against CO1. What exceeds — could it be one tap away behind a predictive label? [CO1, CO2]
7. **Only the indispensable:** any text that explains, justifies, describes system mechanics or gives instructions? Whys where they don't decide? [CO3, CO4]
8. **One primary:** zero or one filled full-width action, at the bottom in details and sheets; secondaries look secondary, not disabled. [CM7]
9. **Components in their ONE shape:** compare every piece against the project's component inventory; does any piece appear drawn differently on another phone? [CT1–CT10, CP10]
10. **States and color:** one state per row, only if not normal, word + symbol; accent only on tappable and "now"; red only destructive/closed. [CO5, CO16]
11. **Where am I:** is the object (and its part) clear? Exactly one visible way back? [NA7, MO6]
12. **Native chrome:** large title, bar-less buttons with symbols, back = chevron only, sheets with grabber and detents, untinted glass, native tab bar. Anything invented? [MO10, MO11]
13. **Modality:** what opens on top is a sheet and its base isn't a sheet; long tasks in a large sheet; immersive in full screen. [MO1–MO5]
14. **Copy aloud:** the person's language in its neutral variant, the chosen register, no blame, no hype, no exclamations, buttons with verb + object, first two words carry the meaning. [CP1–CP12]
15. **Example coherence:** names, times, days and sums match the other phones and the example table; sums add up. [ME9, ME10]
16. **Accessibility:** AA contrast including text over images; targets ≥44 pt; color never alone. [CM13, CO16]
17. **Motion described:** if the document describes motion, does it follow MH1–MH9 (no loops, no haptics for what the app does, one novelty with a visible path)?
18. **Project rules:** every screen-level rule and anti-pattern of the project canon that applies to this screen.

## (c) Flow by flow, as a first-time user

Follow each flow phone by phone, from end to end, as someone who has never seen the app. Note exactly where they would get lost.

1. **Clear starting point:** the first phone says where the flow starts (what the person taps, on which screen). [ME14]
2. **Entrance and exit:** every screen has its entrance (tab, push, notification, accessory) and exit (‹, ✕, swipe); no orphan screen; every action's destination is drawn or stated. [NA10, ME14]
3. **No duplicates:** no object has two different screens; its variants are states of the same screen. [NA8, NA9]
4. **No sheet over sheet along the way:** follow every action that opens something from inside a sheet; it replaces content or pushes, never a second sheet. [MO2, MO3]
5. **Always a next step:** in every state (with data, without data, after a problem, after finishing) there is a next step; no dead end. [PR9]
6. **Automatic states:** what the system can detect changes by itself; no "Start/Finish" as main actions. [MO14]
7. **Notifications and Live Activity:** each opens its object inside its hierarchy with the back stack built. [NA10, MO15]
8. **Saving and changing:** saving never forces a second decision; every change can be undone; automatic changes say why once and don't come back. [NA13, MO13, CT8]
9. **Creation flow:** can be finished with the minimum (with "later" for optional data); every value read or inferred can be corrected; one datum per step. [MO7, PR7]
10. **Empty, offline and permission-denied paths** have been drawn or stated, and the app still works in a reduced way. [NA14, NA15]
11. **One continuous story:** flows tell the same example in order; what changes in one flow carries into the next; counts derive from the real state. [ME9]

## (d) Against the canons

1. Does anything contradict a rule of either canon without the document asking about it? → B.
2. Does any anti-pattern (canon-base §10 or the project's list) appear? → B.
3. Was any open decision or conflict resolved without asking the user, or any "To test" item changed? → B.
4. Is there a new rule that neither canon has? → propose it to the coordinator with its source; it goes into the project canon.

## Report

Save `AUDIT-<date>.md` next to the deliverable (not in the plugin), one row per finding: phone `id` · check (`a:multiple-primaries`, `b6`, `c4`…) · rule · severity · what is seen · proposed fix. At the end: totals per severity and what remains minor or open.
