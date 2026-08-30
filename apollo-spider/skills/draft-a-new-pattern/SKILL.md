---
name: draft-a-new-pattern
description: Help create a NEW component or pattern that fits the Apollo design system — built from its existing tokens, type composites, states, layout rails, accessibility rules and naming — and package it as a candidate ready to propose for the library. Use when the system is missing something you need. Produces a reviewable draft, not adopted canon. Use this when the output is UI and nothing in the library fits — “we need a component the system doesn’t have”, “design a new pattern for this”, “there’s no widget for this, invent one”, “add something to the library”, “the closest component is wrong, make a proper one”.
---

# Draft a new pattern

The **creative** mode. Use it when `generate-from-canon` flagged a Gap, or when you want
something the system doesn't have yet. The point isn't to freestyle — it's to grow the
system *on-brand and accessible by construction*, so your idea can become part of the
shared library rather than a one-off on one screen.

## Before you draft: make sure it's really missing

The library is 135 components and 8 foundations. Things hide under names you wouldn't
guess.

1. Search `showroom/index.json` by **alias and blurb**, not by the name in your head.
2. Look at the neighbours: `related` on each index entry, and
   `relationships.commonPatterns` in `knowledge/components/<slug>.meta.json`.
3. Check whether what you want is a **variant or a prop** of something that exists, not a
   new component. That's a much smaller ask and a much better outcome.
4. Check whether it's a **layout question** rather than a component one —
   `knowledge/_render/_bento_edit_rails.json` carries every layout dial and its options,
   and the answer may already be a legal setting.

If it survives all four, draft it.

## Rules

1. **Build from the system's primitives.**
   - Tokens by intent for every visual value — colour, spacing, radius, border width.
     Never a raw hex or px. Names live in `knowledge/tokens/*.json`, resolved in
     `knowledge/canon/canon.css`.
   - Type from the composites in `knowledge/canon/type.css` — `.t-cm-*` for component
     text, `.t-ed-*` for editorial. Never a raw font value.
   - Icons from `knowledge/assets/icons/` only. A genuinely custom shape is marked
     `<svg data-bespoke="why">`, so it reads as a decision.
   - Motion in CSS, on the motion tokens — not computed in JS. The library has to be
     portable, and JS logic doesn't travel to Figma.
   - The accessibility floor: AA contrast, a visible focus ring, a 24px minimum target,
     a `prefers-reduced-motion` block if it animates, and the right ARIA.
2. **Work in all four themes, and start in mono.** Mono is the baseline; legacy, console
   and supercharge are override sets over it. If you bind to tokens rather than values,
   the other three come for free — and that is the test of whether you did.
3. **Colour is meaning.** Coloured red or green text belongs to monetary values only,
   always with a symbol. The two reds are keyed to the background behind them — dark red
   `#DA1A00` on white, light red `#F6604C` everywhere else. Error checkboxes and radios
   take the red on the mark, never the label. Ink is a token that resolves per theme,
   never a literal, never pure black.
4. **Give it all the states** the thing genuinely has: default / hover / pressed / focus /
   disabled / loading / error / empty.
5. **Name it like its neighbours.** Look at the `level` and `usage` groups in
   `showroom/index.json` and pick a name that would sit naturally in that list. Sentence
   case in the UI, always.
6. **Document it in the library's own shape**, so it can slot in. Mirror
   `knowledge/components/<slug>.meta.json`: `purpose`, `props` (with the token each
   `binds` to), `variants`, `tokens`, `relationships` (`livesInside`,
   `mustNotNeighbour`, `commonPatterns`), `accessibility` (role, keyboard, focus, screen
   reader), `antiPatterns`, `provenance`.
   `knowledge/components/meta.schema.json` is the schema, and any existing meta is a
   worked example. Metas are named by the index `slug`; snippets by the same slug
   capitalised — but the case isn't consistent across the set, so match
   case-insensitively rather than guessing.

## Procedure

1. Clarify what the pattern is for, where it'll live and what it must not sit next to.
2. Compose it from canon primitives — bind tokens, apply composites, add the states.
3. Write the draft: a **snippet** (HTML/CSS or React) plus its **meta**.
4. **Gate it.** Use the `check-with-gates` skill. The quick loop is
   `python3 knowledge/_validate_screen.py <your-file>`; the full contribution contract is
   Route C in that skill — a `#token-manifest` block declaring every var and its token,
   plus light and dark blocks, which is what makes `_validate_snippets.py` and
   `_validate_coverage.py` able to accept it. Signing that contract is what turns a
   sketch into a candidate.
5. Note what's still **open** for a reviewer to decide, and say so plainly.

## Output

A **candidate**: the draft snippet + its meta + a short "what it's for / what's open"
note + the gate verdicts as they actually printed.

> Important: this produces a **candidate for review, not adopted canon.** A human reviews
> and promotes new patterns before they enter the library — that's what keeps the system
> trustworthy. Growing the system this way is exactly the input we want back from you.

*Experimental.*
