# Pure-inference diagnostic — where the governed version's gaps are, 2026-07-05

*Two cold Opus passes on the same SME Payments data, zero brand governance (no canon, no curbs, no
a11y mandate, no component library) — a ceiling probe, not a production build. Goal: find where the
governed `expressive-v2` falls short by seeing what the model does with nothing holding it back.
Variant A: named influences (Linear/Stripe/Mercury/Ramp/fintech awards), full recall permitted.
Variant B: no named influences, "your own idea of award-winning" only.*

## What both diagnostic runs did that the governed version didn't

- **Full colour systems, not a single retrieved accent.** Both built multi-hue palettes (indigo/
  emerald glows + Stripe-green in A; lime/ice-blue/amber in B) used *semantically* — colour carries
  meaning across the whole screen (live money / future / decision-needed), not one red accent doing
  one job. The governed version is deliberately restricted to canon colours plus one disciplined
  accent — this is the single biggest visual gap, and it's a direct, expected consequence of the
  cardinal curb (brand colour retrieved, never invented), not a craft failure.
- **Custom display typefaces.** Geist Mono / Inter (A) and Fraunces / Space Grotesk (B) — both reach
  for typographic personality the Univers-only cardinal curb forecloses entirely.
- **Rounded geometry, glows, pulse/spin decoration.** Both used soft radii, glow blur, and pure
  decorative motion (a conic-spinning mark, ambient pulses) — the square-corner + "motion only
  where it earns its keep" curbs rule these out by design.
- **A genuine point of view on structure, not just decoration.** Variant B in particular organised
  the whole screen around an idea ("time as the spine" — a vertical arc for today, a horizontal
  timeline for the future) rather than a component checklist. This is the more interesting finding:
  it's a *compositional* idea, not a colour/type one, and nothing about the cardinal curbs would
  have blocked it — the governed expressive-v2 runs didn't reach for an organising idea this strong,
  which suggests the gap isn't only the curbs, it's also that the gravity-fix prompt still leaned on
  "extract a pattern from named products" rather than "have a point of view about this data."

## What this suggests about the real gap

The colour/type/radius gaps are **expected and by design** — that's what the cardinal floor is for,
and no amount of prompt tuning should reopen them. The more useful finding is the **structural
one**: pure inference reached for an organising *idea* (time-as-spine, decide-now vs watch-later)
that felt more like a real product concept than the governed version's "apply five named patterns to
existing sections." Worth carrying into the next gravity-instruction iteration: ask for a point of
view on the *data's structure*, not just borrowed craft techniques layered onto the existing section
order.

## Caveat

This is two runs, one model, one screen, no rendered visual check (same limitation as every other
artifact this session) — a diagnostic signal, not a verdict. Compare directly via
`register-spread-2026-07-05-compare.html` ("Diagnostic — zero curbs" buttons) against
`expressive-v2.html` in both spread folders and the old portfolio reference.

## Entry points

`register-spread-2026-07-05-compare.html` · `with-influences.html` / `without-influences.html` ·
`_LIVE-STATE.md` (inference-gravity target-state entry) · memory `spread-review-gaps-2026-07-05`.
