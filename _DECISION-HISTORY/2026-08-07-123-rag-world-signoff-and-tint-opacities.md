# #123 — the RAG world signed off, the six parked consequences closed, and the atoms taught to survive

```
provenance: 123 · 2026-08-07
status: ruled — knowledge/_rulings.json entries 58–61 (`s123-D1`…`s123-D4`)
```

Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#123) · Banner: `GOOD-MORNING.md` ★ LATEST #123 ·
Ledger: `knowledge/_rulings.json` (`s123-D1`…`s123-D4`) · Predecessor arc:
`_DECISION-HISTORY/2026-08-07-mark-map-pass-and-the-half-dead-canon.md` (#122).

---

## Why this session existed

#122 ruled the mark map five times and enacted all five, and then stopped — because the five
rulings had **six mechanical consequences** nobody had decided, and because **nobody had looked at
the result**. #122's own finding was that `canon.css` had been half dead for twenty-three sessions
and that **Dave's eye**, not nineteen green gates, is what caught it. So the residual it wrote for
#123 was not a build task. It was: *look at it.*

That ordering turned out to matter. Every one of this session's four rulings was taken with the
rendered artefact in front of Dave.

---

## Finding 1 — the visual confirm passed, and it was the licence for everything after

Dave drove `reviews/outputs/mark-map-controller-v6.html` — three lanes, mono editable,
console+supercharge with a live `console == supercharge` assert, legacy display-only asserting
fills against {#col25-017} and marks against `s122-D5` — and the verdict was **"mega"**.

That closes #122's residual ① and the sixth parked consequence (*NOT DRIVEN VISUALLY*) in one act,
and it is registered as SIGNED OFF #123 in `knowledge/_REVIEW-SIGNOFF.md`.

**Why it is written down as a finding and not a formality:** the parked list included a 4.56
white-on-teal contrast leg and a supercharge badge shift that arrived through alias edges rather
than through anybody's decision. Both were *numbers* until Dave saw them rendered; only then could
they be accepted (they were, see below). A number over the bar and a number Dave has looked at are
different states of the record.

## Finding 2 — the fall-through class recurred TWICE inside its own remedy

This is the session's real lesson, and it belongs in the banner rather than in a footnote.

Parked consequence 1 was: legacy's warning/information **backgrounds** silently became the new mono
values (`#E0A61F` / `#78A7E8`) because legacy never *declared* its own — it had been inheriting
values that happened to be right, and when the base moved, legacy moved with it. Nobody ruled that.
Dave restored the old values (`#F0B13A` / `#7DABCD`) and had legacy declare them (`s123-D1`).

Then, enacting the tint ruling, **the same shape appeared twice more in the same afternoon**:

- **legacy `rag/error-tint` was undeclared** — the one legacy tint with no override. Dave's words:
  *"legacy should declare its own."* Declared `#F9F2F3` / `#260005`.
- **supercharge's tints were undeclared** — so the moment the base `rag/*-tint` values became mono's
  tuned composites, supercharge would have silently inherited opacity composites for surfaces it had
  just been ruled to keep solid. Pinned to its pre-`s123` solid pairs; the fall-through is closed.

**The pattern, stated so it can be checked next time:** *when a base value moves, every theme that
MEANT the old value must declare it.* Inheritance is indistinguishable from agreement until the base
changes — at which point the theme that was merely quiet gets silently re-ruled by someone else's
decision. This is `ds-039`'s cousin: not a gate that failed, but a state no gate is looking at.

Three instances in two sessions is the gate-don't-patch trigger. **No gate was built for it this
session** — it is recorded here and in the banner as the finding, and the remedy is unruled.

## Finding 3 — the tint decision arc, and an amendment to ds-026

The question parked at #122 was thin: *are `*-tint` pairs mode-invariant?* What Dave actually ruled
was wider, and he ruled it off a live controller (`reviews/outputs/tint-opacity-tuner-v1.html`, then
`-v2.html` with five lanes) rather than off a table.

His words, in order, and the arc they describe:

1. *"I think we use the solid tints for legacy only, all the rest can be tuned opacities"* — the
   first cut: solids are the legacy idiom, everything else is opacity over the surface.
2. On supercharge's warm ramp: *"the warm ramp can stay solids, they are for large surfaces"* — a
   correction to his own first cut, and the reason is physical, not aesthetic. Large surfaces are
   where a composited alpha is most likely to disagree with itself across stacking contexts.

⇒ **`s123-D3`: LEGACY + SUPERCHARGE solid · MONO + CONSOLE tuned opacities**, snapped to the
`--alpha-04..96` primitives.

**And this AMENDS ds-026.** The alpha primitives were minted at #99 under an explicit fence —
*state changes only*, Dave's own scope. Tints are a second permitted use. That is not a
reinterpretation smuggled through an enactment: it was named as an amendment and Dave ratified it
in terms — *"this is fine"*. The fence now reads: **alpha for state changes, and for tints in mono
and console.** Legacy and supercharge remain solid, which is what keeps the amendment narrow.

**Enacted in full**, and the enactment is where findings 2's two extra fall-throughs surfaced: base
`rag/*-tint` became the mono composites (alphas recorded per value in `$note`, priors retired to the
note), console's overrides carry its four tuned composites, supercharge pins its solids, legacy
declares its error tint.

## Finding 4 — `ownsHexes` was stale, and the honest answer was "nothing changed"

`_themes.json`'s `ownsHexes` still claimed `#B92F1E` was Mono's alone, which `s122-D3` had made
false. The stale map mattered because the **theme-provenance advisory's 37** was measured against
it — so the figure was not comparable across the `s122-D3` boundary.

Refreshed (`s123-D2`), re-run, and the result is **37 — unchanged**. That is worth recording
precisely because it is a null: all 37 remain pre-existing attributed items, and **none of them was
an artefact of the stale map**. A refresh that moves no number is evidence, not a wasted step; the
alternative was carrying an un-comparable figure forward indefinitely.

## Finding 5 — the SC badge shift, ratified rather than reverted

`s122-D3`'s alias edges had dragged supercharge's `badge/background` and `tabs/badge` dark leg from
`#CC4333` to `#B92F1E` — a side effect, not a decision. Seen rendered in tuner-v2 lane A (white
label contrast `4.51 → 5.94`), Dave's verdict was *"SC badge is fine"* (`s123-D4`).

Nothing to enact — the values were already live. **The ruling converts a side effect into a
decision**, which is the only thing that was actually missing, and it closes the last of #122's six.

## Finding 6 — the atom-destruction defect, and the fix that nearly bit itself

`s121-D1` left a live landmine: `gen_canon_tokens.py` rewrites the AUTO span in `canon.css`, and the
hand-authored `TOKENS alpha` / `marks` / `mark-carriers` atoms live *inside* that span with **no
store origin** — so a run would delete them. It had stayed survivable only because nothing in the
build ran it, which is a coincidence, not a guard.

Fixed this session: the generator now **harvests the hand-authored atoms before the rewrite and
re-injects them after**, and refuses — `AtomPreserveError`, named and loud — if one would be
dropped. Three-bite selftest; driven **twice on the real file**, idempotent, atoms 3/3.

**⛔ And what we got wrong, in the same hour.** The first version's own header comment contained the
string it used as a marker, so its marker-count regex matched the comment and the *next* regen would
have raised a **spurious `AtomPreserveError`** — a refusal that would have looked exactly like the
defect it was built to prevent. Caught and tightened to the `===== TOKENS` form in the same session.
The general shape: *an instrument whose own documentation is inside its own search space will
eventually measure itself.*

---

## Where it landed

- Rulings: `knowledge/_rulings.json` entries 58–61 (`s123-D1`…`s123-D4`); `_README` untouched at 20.
- Enactment: `apollo-legacy.overrides.json` · `apollo-console.overrides.json` ·
  `apollo-supercharge.overrides.json` · `semantic-colour.json` · `_themes.json` · `canon.css`
  (regenerated cascade) · `knowledge/canon/gen_canon_tokens.py`.
- Gate tails, all green post-enactment and **re-run at the wrap** (`_DECISION-HISTORY` receipt):
  `gen_theme_cascade --selftest` **OK** + generator reports **in sync** · `gen_token_ramp` **87
  already in sync** · property-resolves C2 `--strict` **87 files, 0 failures** · theme-provenance
  **37** (advisory) · `gen_canon_tokens --selftest` **OK (3 bites: harvest · preserve · refusal)** ·
  `tinycss2` **3,324 rules, 0 errors**. *(The `198 paths / 206 projections` figure lives in
  `s123-D1`'s own enacted receipt, taken at enactment time; the wrap re-run reports in-sync rather
  than re-emitting the count, so it is cited, not re-measured.)*
- Deliverables: `reviews/outputs/tint-opacity-tuner-v1.html`, `-v2.html` (v2 = five lanes),
  both registered in `knowledge/_REVIEW-SIGNOFF.md`.
- **DECLARED GAP:** no pixel render was possible in-sandbox (chromium TLS-blocked — environmental,
  the same fence as `_validate_state_contrast.py`). The tuners were **runtime-asserted in node**:
  36 elements, all lanes populated. That is a weaker proof than a render and is named as such.
  *(annotation added #130, 2026-08-08, BY ADDITION - the line above stands as written: the
  chromium TLS-block was adjudicated NOT REPRODUCING at #129, first-hand - see
  `knowledge/_RUNBOOK-render-verify.md`. The gap as declared at #123 is the record of that moment.)*

## What is still open

- The fall-through class (finding 2) has **no gate**. Three instances, two sessions, remedy unruled.
- `4.56` white-on-teal legacy success mark leg — accepted with the v6 pass, still the weakest leg.
- Everything on the carried list, unchanged by this session, is in `_LIVE-STATE.md` § OPEN and the
  #123 banner's residual line. This session ruled nothing outside `s123-D1`…`s123-D4`.
