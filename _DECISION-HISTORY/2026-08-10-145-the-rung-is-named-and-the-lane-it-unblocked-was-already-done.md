# #145 — the rung is named, and the lane it was supposed to unblock turned out to be already done

provenance: 145 · 2026-08-10
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA (#145) · `GOOD-MORNING.md` ★ LATEST (#145).
Ledger: `knowledge/_rulings.json` § `s145-D1`. Value provenance (unchanged from `s144-D1`):
`reviews/PLUSMINUS-TUNER-2026-08-10-s144-v2.html`. Both-way links per
`_DECISION-HISTORY/README.md`.*

---

## Why this session existed

#144 closed with the plus/minus coloured-text rung RULED but NOT ENACTED: four values (light/dark
for error and success), scope collapsed twice down to red/green signed numerals only, but no name
for the rung and therefore nothing minted in `knowledge/tokens/semantic-colour.json`. #144's own
residual ① named the gap plainly: *"RUNG NAME UNRULED — `rag.<hue>-text` vs `rag.<hue>-ink`."*
#145 opened, forward-titled `Apollo - #145: mint the rung [0]`, to close exactly that — OPUS
conductor, Dave live, one arc.

A second, parked item rode alongside it: residual ② of #143/#144, "colour-spine DTCG migration —
7 address-intent rows," carried twice without opening. This session's second half turned out to be
about that parked item, not about new work on it.

## The naming ruling, and the two reasons behind it

Dave was given a measured three-option set with the cost of each named, and picked `-ink`. The
ledger (`s145-D1`) records his reasoning in full; the two load-bearing points are worth restating
here because neither is obvious from the address alone.

**Why not `-text`.** `rag/text/*` already exists in the spine, minted at `s131-D1`, and it is
GROUND-keyed: `on-light`, `on-dark`, `on-information` — the axis is *what surface the text sits
on*. The new rung is MODE-keyed, and the thing that varies across its two values is *hue*, not
ground. Using `-text` for both would have put the same word on two different axes one level apart
in the same token family — a name collision that reads fine in isolation and confuses on the first
cross-reference.

**Why it stays under `rag/` rather than moving to a general text-colour family.** `s144-D1` locked
the hue of both new values to the `s122-D2` fills (red 7.0588°/30.2375°, green
142.9412°/154.5908°, HSB/OKLCH) — the ink colours are not independent choices, they are the family
fill's hue carried into a legibility-safe lightness. Keeping the address under `rag/` keeps that
derivation visible; moving it out would have hidden the fact that these two values are *derived
from*, not merely *similar to*, the fills.

One more thing was checked rather than assumed: whether "ink" was already a word this system uses.
It is, but only on the consumption side — `--ink` as a CSS custom property bound to `text/default`
in `tokens/_manifests/sutherland-fixtures.json`, and prose usage at `s134-D4` ("ink on the SHAPE").
It had never been a *path segment* in the semantic spine itself. So `-ink` is new to the spine's
address grammar, but not a word invented for this ruling — a small distinction, checked rather than
assumed, in the spirit of the *"ink was already the system's word"* framing Dave would otherwise
have had to take on faith.

## The mode-fork is forced, not designed

`rag/error-ink` and `rag/success-ink` are the first rungs in the rag hue family to carry two
different hex values across light and dark. All twelve prior hue rungs — the four `-background`
values, the four `-glyph` values, the bare family roles — are mode-invariant by `s122-D2`'s own
ruling; only `-tint` had forked before this. The temptation, on seeing the file, is to read the
fork as an inconsistency. It isn't: `s144-D1`'s own arithmetic makes a single mode-invariant value
impossible here (the luminance window against `#FFFFFF` and against `#1A1A1A` do not overlap), so
the fork is a *receipt* of that finding, not a fresh design decision made at #145. The asymmetry
between error/success (which now have ink rungs) and warning/information (which don't) is likewise
a receipt of Dave's #144 scoping, not a gap to fill later.

## The enactment, and the one gap it cannot close

Enactment was mechanical once the name existed: two keys added to `semantic-colour.json` by textual
insertion (rest of the file asserted parse-equal), the token generators re-run and re-verified
idempotent, the four downstream gates re-driven. The one thing enactment cannot do is prove the new
rungs pass AA by instrument, because nothing in the component layer consumes them yet —
`amount-display.sign`'s enum is `["none","negative"]`, with no `positive` value to bind
`rag/success-ink` to. That gap was named at #143 (finding ⑤) and is still open; this session did
not close it, and the ledger says so plainly rather than implying the ruling proves more than it
does. The AA numbers Dave saw are real — they come from his own #144 tuner — but a tuner reading is
not a gate, and the record now distinguishes the two explicitly: PROVEN-by-tuner is not the same
claim as PROVEN-by-gate.

## The bigger finding: a parked lane whose premise had already resolved

The session's second half was not "work on the colour-spine migration." It was checking whether
that work still needed doing, before spending a sub on it — and it didn't.

Lane ② had been carried since #142 as "the colour-spine DTCG migration, which the 7 address-intent
rows (`rag.*` binds on four components, `background.default`/`surface.*` binds on three more) are
waiting on." Probed directly this session: all seven addresses already resolve in
`semantic-colour.json` to proper `$value`/`$type` leaves. `_validate_dtcg.py` reports zero failures
on the spine; its eight deferrals on that file are all `DEF-COLOR-MISTYPE`, all on blur/image
opacity tokens typed `color` while holding plain numbers — none of them touch `rag` or `surface`.
The migration those seven rows were waiting on had already landed at #141 (`s141-D1`, DTCG axis A).
Lane ② was a job already done, parked twice by two different sessions that never checked.

That in itself would be a tidy correction — cross out a stale line, move on. What makes it worth a
dossier entry is what the probe found underneath: **nothing re-checks that a meta's `binds` address
actually resolves against the colour spine.** Four validators mention `binds` by name
(`_validate_binds_ratchet.py`, `_validate_partials.py`, `_validate_radius.py`,
`_validate_type_blast_radius.py`); none of them opens `semantic-colour.json`. The seven addresses
this session verified by hand-probing the JSON would be exactly as invisible to every gate if they
were wrong — rename a rung, and seven metas point at nothing while the whole build stays green. The
finding recorded as lane ② was never really about the migration; the migration was a red herring
that happened to be sitting on top of the actual gap. This is named as a residual for #146 to build
(the binds-resolve gate), not designed or scoped here — that decision, and its shape, are the next
conductor's and Dave's.

The seven `$status` strings that had asserted "colour spine NOT yet DTCG-migrated" were corrected
in place, by addition: the stale clause is kept, struck through in effect by a dated correction
appended after it, not deleted — this repo's standing discipline for a wrong claim once written.

## This wrap's own finding, made while verifying receipts

Re-running the token generators to confirm the ink-rung enactment (a routine verification step,
not new work) surfaced a second, unrelated regression: `canon.css`'s
`--typography-font-family-default` lost its web-safe fallback stack. Where the committed file
carried `"Univers Next for HSBC", "Helvetica Neue", Arial, Helvetica, sans-serif` in both theme
blocks, the regenerated file carries the bare, unquoted `Univers Next for HSBC` — nothing to fall
back to if that face is unavailable.

The cause is a latent mismatch, not new damage: `gen_canon_tokens.py`'s fallback substitution only
fires `if ttype == "string"`, but the font-family token in `typography.json` carries DTCG's proper
type, `"fontFamily"` — the condition has never matched this token, and the `$webStack` field built
specifically to carry the fallback chain (`knowledge/guidelines/typography-standards-2026.md`) is
never read by the generator at all. `canon.css` had not been regenerated since #132 — eleven
sessions of drift between rulings and the generated file sat unexercised because nothing ran the
generator in between. This session's regen, run to enact two new CSS variables, exercised the
mismatched path for the first time and the fallback silently disappeared.

This wrap sub found it, confirmed it reproduces on a second `--check` run, and left it exactly as
found: a wrap sub's remit is capture, not generator-code repair, and deciding how to fix a
substitution condition is a design call that belongs to whoever builds the fix. Named plainly in
the residual rather than folded into "housekeeping."

## Resolved state

`s145-D1` is RULED AND ENACTED — the name, the two token keys, the four downstream gates, all
verified on the artefact at HEAD. What is still open, all Dave's: the `success-ink` binding site
(`amount-display.sign` needs a `positive` value, or the rung stays ahead of its consumer); the dark
selected-row token (`#272727`); the `#1A1A1A`-on-dark-rag-tints question (still explicitly
UNVERIFIED, not resolved by proximity to this session's other rag work); and, newly, whether and
how to build the binds-resolve gate this session's probe found missing, and how to fix the
font-family fallback this wrap sub found broken.
