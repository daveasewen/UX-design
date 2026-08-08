# #134 — the mono alert nailed, and Dave's eye catches a stale snippet

```
provenance: local_366080a7 #134 · 2026-08-08
status: ruled (pointer: knowledge/_rulings.json § s134-D1..D4)
```

Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#134) · Banner: `GOOD-MORNING.md` ★ LATEST #134 ·
Ledger: `knowledge/_rulings.json` (`s134-D1`…`s134-D4`) · Predecessor arc:
`_DECISION-HISTORY/2026-08-08-133-the-kg-joins-the-memento-standard.md` (#133).

---

## Why this session existed

A quota-bound session (Dave: 31% Fable remaining, delegate everything) opened with three
reconnaissance lanes run in parallel: **A** — is the remainder of `s130-D4`/`D5`/`D6` + tabs
actually mechanical, or does it need Dave's word first? **B** — is the #130 error-mark image
confirm premise still live, or has it gone stale? **C** — why does
`_validate_state_contrast.py --selftest` fail differently across environments?

## Findings, and how the thinking moved

**Lane A: NOT mechanical.** Pressed tokens need fresh mints, mono error-red has four
flip-flopped occurrences in the corpus, and the tabs meta carries zero badge references to bind
against. Nothing was guessed or enacted; the blockers are named in
`notes/_briefs/2026-08-08-134-laneA-s130-remainder.md` and the set stays Dave's.

**Lane B: the premise was stale, not the finding.** The lost error-mark image that #130 was
waiting on never arrived and, on inspection, its proposed white-shape/red-glyph treatment never
existed anywhere in the built corpus — it can be retired as UNBUILT rather than left open.
Closed by `s134-D2` below.

**Lane C: an environment-dependence bug, not an environment fact.** The selftest crashed with a
bare `rc=1` when Playwright's browser path wasn't set, which read as an ordinary failure rather
than an environment refusal. Fixed with a named exception, `StateContrastSelftestError`, rc=2,
mutation-tested. The 7 arms that need a real browser stay UNPROVEN in-sandbox — declared, not
silenced.

**The matrix, and the find that mattered.** Building the RAG-roundel matrix across all four
themes exposed drift in **both directions** at once: the Alert snippet's amber
(`#C58900`) contradicted its own cited ruling (`s122-D2`'s `#E0A61F`) — caught by Dave's eye off
the rendered matrix, not by any gate. Separately, a sub measuring the snippet's dark-mode legs
reported "fails" at 3.68/3.63 — numbers that were correct readings of **stale bytes**.
`Alert.reference.html` predated `s122-D2` and still carried the retired dark-mode values in both
theme blocks. Dave's screenshot of the spine-sourced matrix contradicted the sub's numbers, which
is the tell: **when a measurement contradicts what Dave saw, suspect the measurement's subject,
not Dave's eye.** The snippet was re-based to the spine and every leg re-verified on the new
bytes. This is the same class the #133 token-claim KG edges exist to catch mechanically —
spine right, consumption stale — and it recurred here because the Alert snippet sits outside
that edge set.

**The rulings, each taken off a live artefact:**
- `s134-D1` — RAG roundel gating narrowed to the mark-on-shape leg only, on Dave's own
  contrast rationale ("we only care about the glyph having enough contrast … always accompanied
  by a label"). Shape-on-surface is still reported, never gated. `_validate_state_contrast.py`
  mutation-tested both directions.
- `s134-D2` — the white-shape/black-mark dark-mode flip is legacy-only; mono/console/SC use the
  same marks in both themes. This is what closes the #130 error-mark image confirm: the lost
  image's proposed treatment is retired unbuilt.
- `s134-D3` — amber fixed to `#E0A61F` in both themes, matching its own `s122-D2` citation.
- `s134-D4` — the mono alert, ruled off a live options controller with a JSON export: tint-only
  shell (no border, no accent), glyph `#1A1A1A` in both themes, `s122-D2`'s mode-invariant
  pastel shapes underneath. Dave was firm ("nailed to the mast") and confirmed the ink glyph on
  readback. Glyph legs measured 5.55/7.99/8.77/7.04; white-in-dark was tried and rejected by
  arithmetic (1.98–3.14). Symbols verified canon — the error glyph is byte-identical to
  `assets/icons/status-icons/error.svg`.

## Dead ends

- White-in-dark for the mono alert glyph — rejected by measurement, not by preference.
- Treating the error-mark image confirm as still-open — it resolved to a premise that had
  already evaporated (lane B).

## What's still open

- **Floated, Dave's own words, unresolved:** *"extend the no border ruling to mono too
  please."* `s134-D4` already **is** mono, so the referent is ambiguous — other themes' alerts,
  or other mono components? A readback question was put and he answered a different point
  (heat) instead. This is the first beat of #135.
- The KG review batch (`reviews/KG-EDGES-REVIEW-2026-08-08-s133-v1.html`) — untouched this
  session, carried forward.
- A render-proof eye pass on the tint-only alert's committed bytes — owed, not yet given.

## Method note

Every ruling this session followed the same shape: Dave's-eye-on-a-live-artefact → readback →
inscribe → delegate-enact → replay. The matrix and the options controller did the same job the
mark-map controller did at #122/#123 — put the render in front of him rather than a description
of it — and it is what caught both the amber drift and the stale snippet that no gate flagged.
