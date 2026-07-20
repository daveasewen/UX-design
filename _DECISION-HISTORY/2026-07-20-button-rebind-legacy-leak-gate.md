# 2026-07-20 — Button rebind → the teal leak → a gate, a green ruling, and Icon button

*Narrative dossier (the why/how; the WHAT lives in B-D6, R-D17, R-D18, ADR-0010, `_LIVE-STATE`). Dated from
`date`. Session opened to clear the `button/*` snippet-rebind blocker so we could build components; it became a
hunt for a whole class of Legacy-colour leakage, a new gate, a RAG ruling, an ADR, and the first built component.*

## The arc

**1. The rebind (the blocker).** The Mono `button/primary/*` tokens were minted last session but nothing rendered
them — the snippet still showed Legacy red and a colour-swap hover. Rebound `Button.reference.html` onto the
`button/{primary,secondary,tertiary,quaternary}/*` ladder: primary monochrome (no red, B-D1), hover as operational
0.70 opacity over the page (color-mix; the stored `#626262`/`#B7B7B7` kept as the colour-equivalent for
portable/chromatic consumers, ADR-0009/B-D3). Folded the B-D4 disabled-label fix across all four tiers — the
siblings' `label/disabled` had been re-pointed onto `text/disabled` `#E1E1E1`, which *equals* the disabled ground,
so the labels were invisible; rebound onto `text/on-disabled` (`#9D9D9D`/`#808080`, a visible ghost).

**2. Dave's catch → the leak.** With the button de-redded, Dave noticed the "Done" success state still teal. The
root cause was not the button: `color/green/600` literally holds `#00847F` (a "green" primitive storing the Legacy
teal), and `rag/success` aliases it — so **every** component binding the bare role rendered teal. Widening the
lens: **all four** bare `rag/*` roles are Legacy-drifted (error HSBC-red, warning `#FFBB33`, info navy); the R-D14
palette lives only in the `-background`/`-glyph` tokens. The bug was a mislabelled primitive poisoning a role.

**3. Gate, don't patch.** Dave: *"how do we stop this leakage so we don't have to keep fixing such errors."* Built
`_validate_legacy_leak.py` — every reference-snippet binding resolved in both modes; any hit on a registered
Legacy-only hex (seeded with the ruled teal) fails the build. It immediately caught **7** leaking surfaces, two we
hadn't enumerated (Reorder, Status-indicator) — the gate paying for itself on day one. This is the R-D17 finding.

**4. The green set was half-built — so we couldn't just fix it.** Ruling success = R-D14 green (B-D6), the Button
(a fill) rebound cleanly onto `rag/success-background` (complete both modes) + black label via a new per-mode
`text/on-success`. But the other seven are on-page *indicators* needing the glyph-strength green, and
`rag/success-glyph` had **no dark value**. Rather than invent a RAG colour (Dave's domain), the seven were
**waived with provenance** — honest debt, gate green, no silent gap.

**5. ADR-0010 — the schema lesson.** The leak was a *silently missing* dark green. Dave: save all values as
placeholders, value-or-null. Refined to "the ones we flex, with a style-builder in view." Written up: explicit
nullable slots for anticipated flex dimensions; `null` = declared-but-unset (distinct from absent / inherit); a
"no null under a live binding" gate as the companion to the leak gate — one stops the *wrong* colour, the other a
*missing* one.

**6. The ruling, on a live tuner.** Dave wanted to rule the green set the way he rules colour — a tweakable review
screen. Built `reviews/RAG-SUCCESS-GREEN-2026-07-20-v1.html`: OKLCh sliders, live contrast, a **salience guard**
(it surfaced that light green `#2B7E4F` sits a hair *behind* info-blue 5.03 — Dave saw it and held). He ruled
(R-D18): glyph dark `#4A9568`, tints `#DCEDE3`/`#12291D`, bare role rebased to track the glyph. Applied, swept all
seven components, **gate now 0 waived / 0 leaks** — teal fully evicted from Mono.

**7. Then we finally built.** Icon button (P1, "used everywhere") promoted from its proforma draft to gated canon
on the same Mono `button/*` ladder — real HSBC sprite glyphs, glyphs held to 4.5:1 (icon-015), 44px target,
mandatory aria-label, visible disabled glyph. First component of the build-out shipped. Build green 36/36.

## Corrections / things I got wrong

- I initially framed the motion tokenisation as a **shared** scale ramp; Dave corrected — it's **per-component**
  (the decided rule is +2px/−2px on the component's target size, factor derived so each reads ~2px; already gated
  by DEF-003). My "shared ramp" AskUserQuestion option was wrong.
- I **waited to be asked** about context instead of self-triggering the gauge at Red — the rule to proactively
  suggest session-end exists (`feedback-context-gauge`) and I didn't apply it. Sharpened in memory this session.

## Resolved state / still open

- **Landed:** B-D6, R-D17, R-D18, ADR-0010, `text/on-success`, the leakage gate, Icon button. Commits `528e205`
  (button + gate + RAG green) and `8f3f07c` (Icon button). Build green 36/36.
- **Open:** the bare `rag/error`/`warning`/`information` roles are identically Legacy-drifted — same fix pattern
  (rule the R-D14 set → rebind → seed the gate) when Dave wants them. ADR-0010's null-gate + slot rollout are
  staged, not built. Primary-hover ≈ secondary grey collision parked (`_FUTURE-STATE`). 39 P1 component gaps remain.
