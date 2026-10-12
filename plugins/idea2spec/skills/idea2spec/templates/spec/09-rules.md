# 09 · Rules

<!--
HOW TO FILL: generated from the canon: the project canon (idea2spec/canon.md) plus the base canon rules that
apply to this app. Copy rules as one line each, keep their codes (to cite in reviews), and drop the ones that
only concern documents or the design process. Do not paraphrase into vaguer words. Delete this block when done.
Precedence: the person's decisions > project canon > base canon.
-->

The builder must respect every rule below. Breaking one is a bug, even if the code works.
If a rule seems to block something the screens require, do not choose: follow the screen file, and report the conflict.

## Structure and navigation
- **[CODE]** · [Rule, one line.] · [source]

## Modality (iOS)
- Never a sheet on top of another sheet. Inside a sheet, navigate by replacing its content.
- One exit per thing: ‹ if you went down, ✕ if it opened on top; never both.
- Native iOS 26 chrome only (native stack, native tabs, native sheets). No custom bars.
- [Project rules with codes.]

## Content and copy
- 0 or 1 primary action per screen.
- [Content budgets per moment, e.g. "on the move: 1 image, ≤ 12 words, 1 data point, 0 decisions".]

## Visual
- Tokens only (`tokens.json`); no raw values.
- Each object has one shape (`05-components.md`).

## Data and behavior
- [e.g. "Undo instead of confirmation dialogs", "what the app does by itself never vibrates".]

## Anti-patterns already seen (each → the rule that prevents it)
<!-- From canon §14 and base canon §10. If one appears in the app, it is a blocker. -->
- **[What went wrong]** → [rule that prevents it] ([code]).

---

> **Example (replace):**
> - **ST2** · One screen per object, all states inside it: no separate "today" screen for an appointment. · canon 2026-10-10
> - **Duplicate screens for the same thing** → one screen per object with states (ST2).
