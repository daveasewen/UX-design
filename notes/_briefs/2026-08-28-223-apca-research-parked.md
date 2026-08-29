# PARKED — APCA desk research (Dave's word, #223 post-wrap, 2026-08-28)

Dave, in chat, after the #223 wrap: *"Park this for some research, 'the Accessible Perceptual
Contrast Algorithm' this seems better than WCAG, do some desk research on this when we get a moment."*

**What this is.** APCA (the Accessible Perceptual Contrast Algorithm) — the perceptually-uniform
contrast model developed for the WCAG 3 drafts, replacing WCAG 2.x's luminance-ratio arithmetic.
Dave's instinct: it may be better than the WCAG ratios this repo currently enforces.

**Why it touches this repo.** The contrast surface here is ratio-based today: the dataviz series-3
floor is held at 4.61:1 (with a ruled don't-lighten), `_validate_state_contrast.py` runs BLOCKING
in CI's render job, and the two-red law / mono error-ink camp were all ruled with ratio arithmetic
in the room. If APCA is adopted or trialled, every one of those figures changes meaning — polarity
(light-on-dark vs dark-on-light) and font weight/size enter the measurement, which the current
gates cannot see.

**Scope of the desk research when it opens** (a browsing/research lane, NOT a build lane):
- The perceptual model itself, and where WCAG 2.x ratios mis-rank real pairs (the classic false
  passes/false fails).
- Standards status: WCAG 3 draft maturity, likelihood and timeline of it becoming normative;
  what conformance means meanwhile (WCAG 2.x remains the legal bar in most jurisdictions).
- Licensing/IP status of the algorithm and reference implementations.
- What adopting it would move HERE: which ruled figures, which gates, which theme-pair verdicts —
  priced, not enacted. Dave's astigmatism note (red/yellow problem hues, blue/green stable) may
  interact with the polarity sensitivity — flag for his eye, never assume.
- The honest counter-case: critiques of APCA, and what WCAG 2.x still does better.

**Closes when** (mirrors the W-row): the brief above exists with those five sections, Dave has
read it, and he rules adopt / trial / drop.

**DO-NOT-RULE.** Nothing here is a ruling. No gate, figure, or theme value moves until Dave's
word, and the ruled contrast canon (two-red law s151-D1, mono error camp s149-D1, the 4.61:1
floor) stands untouched throughout.
