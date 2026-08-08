# #132 — the console/SC info blue, the tint that must not follow, and the gloss that had no record

```
provenance: local_5aca6a78-d665-4e3e-af97-fae41eaee2ae · 2026-08-08
status: ruled — knowledge/_rulings.json § s132-D1 · notes/_MEMENTO-DECISIONS.md § ★ #132
```
Ruling: `knowledge/_rulings.json` § `s132-D1` · spine delta: `_LIVE-STATE.md` ⏱ LATEST #132 · ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #132.

## Finding 1 — the controller worked exactly as the memory said it would

`s131-D1.watch` left console/SC info as DIRECTION ONLY. A fresh, focused controller
(`reviews/INFO-BLUE-CONTROLLER-2026-08-08-s132-v1.html`) was built with the flip point made explicit:
on this hue, white dies below 4.5 around L≈52%, so "lighter" *implies* the ink mark. Dave picked
`#5A85C1` and pasted the controller's own export back — ruling in one message, ink mark 4.61:1
accepted with the flip read back to him and confirmed firm. WHY the readback mattered: the mark flip
changes the family grammar (error becomes the sole white mark on console/SC), which is bigger than
the hex and easy to ratify by accident from an export blob.

## Finding 2 — the SC tint pin nearly fell through, and the note caught it

The enactment's first patch re-composited BOTH themes' information tints at console's ruled alphas
(28/44). Console's tint note licenses exactly that. Supercharge's does the opposite: **SOLID pins**
(s123-D3, Dave: "the warm ramp can stay solids"), with re-hue off the solids named *a separate,
unruled call*. The wrong values (`#D1DDEE`/`#364963` over SC's `#D6E3EC`/`#092131`) were live in the
working tree for one tool-call before the note's own text flagged it; reverted in-window, the clause
quoted in the amended note. The general lesson is already inscribed as the fall-through class — the
new datapoint is that the *defence that worked* was supersession-by-addition keeping the licence text
adjacent to the value it governs. A parse-gate on tint provenance (console=derived, SC=pinned) would
make this structural; not ruled, raised in the ledger.

## Finding 3 — "the two console/SC information-REST items" resolves to no record

The #131 chain carried the phrase as if it named audit records. It does not: `_STATE-CONTRAST-AUDIT.md`
contains no line naming information, any theme. Archaeology traces the phrase to #130's prose ("#4F77B0
… also fixes the console/SC information REST failure") — a *worry*, inherited forward as a *record*.
A Banner-scoped re-run of `_validate_state_contrast.py` on the enacted bytes reproduced only the four
known 4.09 pressed fails (s130-D4 territory, untouched by this ruling). The white-on-info worry is
dissolved arithmetically by the mark flip (ink 4.61 at REST). Nothing was closed by name because
nothing existed by name — the mismatch is declared in `_REVIEW-SIGNOFF.md` and the delta rather than
smoothed into a claimed closure. Class: a gloss in a generated wrapper is still prose; only the store
counts.

## Finding 4 — s131-D2 existed and the session's own agenda was stale

The #132 agenda (from the #131 chain) listed the KG remedy as "Dave's, three options". The store said
otherwise: `s131-D2` was ruled post-wrap (commit e4d2796) — the KG must be as robust as the Memento
graphs — but was inscribed with no `evidence` field and no ledger section, leaving `_governs` RED on
committed bytes. Repaired by addition at #132 (ledger section written late and saying so; evidence
pointed at it). The chain-outranked-by-later-commit case is exactly the standing `_HANDOFF-newer-
than-chain` rule, generalised: **a commit newer than the chain outranks the chain too.** Enactment of
s131-D2 is untouched and is #133's headline.

## Environment (datapoints, not rules)

`$HOME` volume 100% full — even `mkdir ~/.fonts` failed; full `/var/tmp` rehome worked: `HOME=`,
`pip --target`, browsers reused from `/var/tmp/pw-browsers-s131`. A partial ENOSPC pip install left a
`playwright` package that imported but lacked `sync_api` — force-reinstall to a clean `--target` fixed
it. Third sibling of the #129/#131 ENOSPC family; still n<threshold for a runbook rule.

## Resolved state

s132-D1 ruled + enacted end-to-end (spine → regen → render-proof, 24/24 exact, conductor viewed).
Open: s131-D2 enactment [#133 ①] · s130-D4/D5/D6 + tabs · error-mark image · mark-vs-fill 3.0 gate ·
state-contrast selftest env refusal · the #130 carried set.
