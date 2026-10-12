# 06 · Design tokens

<!--
HOW TO FILL: values come from the approved brand (canon §11, stage 7 system sheet) and composition (stage 6/8).
tokens.json is the machine source of truth; this file explains how to use each group and why.
If a value here and in tokens.json differ, tokens.json wins: fix this file. Delete this block when done.
-->

**Source of truth:** `tokens.json` (W3C Design Tokens format). Generate `src/theme/tokens.ts` from it; components read tokens only, never raw hex or numbers. Light and dark live under `color.light` and `color.dark` with the same keys.

## Color
- One accent: `color.*.accent`. It marks the single primary action, the selected tab and links. Nothing else is tinted.
- Glass (navigation chrome) is never tinted for branding; content surfaces are solid.
- Every text passes WCAG AA on every background it can sit on. `ink3` only for placeholders and disabled.
- States always pair the color with a word and a symbol (see `05-components.md` · State system).

| Token | Light | Dark | Use |
|---|---|---|---|
| `accent` | [#hex] | [#hex] | [Primary action, selected tab] |

## Type
- Families: `font.family.text` for data and controls (system SF Pro), `font.family.display` for large titles [and the brand voice].
- [Rule for the display face: minimum size, never in rows or buttons, at most one display per screen.]
- Support Dynamic Type; cap growth only on display sizes. Tabular figures for times, prices and counts.

| Style | Size / line | Weight | Use |
|---|---|---|---|
| `type.largeTitle` | 34 / 41 | 700 | Root screens |

## Spacing and layout
- Three-level rhythm: `space.inGroup` (12) inside a group · `space.betweenGroups` (44) between groups · `space.betweenZones` (64) between zones. Never less than 3:1 between groups and rows.
- Side margin `space.margin` (20); `space.marginTight` (16) in dense or on-the-move screens.
- Touch targets ≥ `space.touch` (44).

## Radii
`radius.thumb` 8 · `radius.field` 12 · `radius.card` 26 · `radius.capsule` for everything tappable that is not a row. System component radii are never changed.

## Motion
- Physics, not choreography: springs with no bounce, interruptible, inheriting the finger's velocity (`motion.spring.*` → Reanimated `withSpring({ duration, dampingRatio })`).
- No infinite loops (pulses, shimmer). For waiting, a skeleton of the layout.
- System chrome animations (sheets, tabs, navigation, glass) come from the system: never imitate them.
- Reduce Motion: movement becomes a fade (`motion.fade.reduceMotion`).

## Haptics
| Token | expo-haptics | When |
|---|---|---|
| `haptic.select` | `impactAsync(Rigid)` | The person marks, adds or chooses |
| `haptic.success` | `notificationAsync(Success)` | Something long finished |
No sounds. Nothing the app does on its own vibrates.

---

> **Example (replace):** accent `#1F6F5C` (light) / `#5FC3A8` (dark), used only on "Book" and the selected tab. Display family "Fraunces" for large titles at ≥ 28 pt, never in rows. `haptic.select` when "Book" is tapped.
