# #152 — the star that was never dark, and the gate that measured a phantom

provenance: #152 · 2026-08-11
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta #152 · ledger: `knowledge/_rulings.json` §
`s152-D1` (and the `s151-D3` status amendment) · banner: `GOOD-MORNING.md` ★ LATEST #152. This
dossier holds the WHY and HOW; the terse records hold the WHAT. Authored by the delegated OPUS wrap
sub. Claims are either verified first-hand by this sub against the artefact (and say so) or are
attributed to the conductor and marked **relayed**. **This wrap ruled nothing** — `s152-D1` is
Dave's, made in-window, and is inscribed here and in the ledger by this wrap.*

## The arc

#152 opened on #151's residual ① — enact `s151-D3`: atom reach, and the star glyph (option C). The
ruling carried a condition nailed to it: the 1.66 diagnosis was **declared UNPROVEN**, and Dave had
ruled *knowing* it was unproven, so verification was owed **before** enactment, not after. That
condition is the reason this session has a finding at all.

## ① The verification that killed its own premise — twice

The carried story was that a selected chip on dark, under hover, put a dark star on a dark fill:
1.66:1. Two independent checks say it never happened.

**(a) Driven, not reasoned.** A real hover with transitions killed shows the selected chip **keeps
its white `--checked` fill** under hover and pressed: the `aria-pressed` rule sits *after*
`:hover`/`:active` at equal specificity and therefore wins the cascade. Ink `#333` on white =
**12.63:1**. There was never a dark-on-dark state to fix.

**(b) The 1.66 is an instrument misfire.** The MARK leg of
`knowledge/_validate_state_contrast.py` (the inner-node loop, read first-hand at `:327`–`:331`)
computes `ratio(inner-fill, the SHAPE's own computed fill)`. The chip star `<svg>` carries **no
`fill` attribute**, so the shape's computed fill is the **UA-default black** — a colour nothing
ever paints. `#333` against `#000` is **1.662**, exactly the number on the board. Light "passes"
at 21:1 for the same reason: it is measuring against a phantom, and the phantom happens to be
convenient in one mode.

★ **The lesson is the general one and it is not about stars:** a red whose *value* reproduces
exactly is still not a red about the thing it names. The gate was honest, the arithmetic was
right, and the subject was wrong. Cf. [[attribute-the-diff]] and
[[a-new-tier-silently-bypasses-its-tests]] — and the defect is a **class**, not an instance: any
`<svg>` with no explicit fill whose inner path paints with `currentColor`.

## ② Dave confirmed option C anyway, off the specimen

Shown the measured hover/pressed pair on the specimen — hover `#FFF` on `#232323` = **15.72**,
pressed `#FFF` on `#484848` = **9.15**, both PASS — Dave's reply was *"I thought I'd said to enact
c"*. The ruling stood; what was owed was the verification, and the verification is what was
delivered. ★ A ruling made on a declared-unproven premise does **not** become unruled when the
premise falls — it becomes a ruling whose receipt finally exists.

## ③ The enactment

**Leg 1 — atom reach** (`knowledge/canon/canon.css`, error block after `.field.is-error .box`;
mirrored in `knowledge/snippets/Selection-controls.reference.html`): the error red now reaches the
checkbox **mark (tick)**, the **indeterminate dash**, the **radio ring + dot** and the **switch
ring + thumb**. Checked/indeterminate **fills drop to transparent in error**, so the red mark sits
on the page — this is the RED option off the ruled-from specimen
`_review/atoms-reach-and-star-v1.html`, not a fresh invention. Labels stay **default ink**
(`s151-D1` rider). All of it via `var(--error-atom)`, which is background-keyed per `s151-D1`; the
six fork no-op guards are untouched, so legacy/console/supercharge do not move
[[four-themes-flexibility-is-the-requirement]].

**Three new error specimens** were added to the snippet — radio `r4`, switch `s4`, indeterminate
`c6` (with the JS that actually sets `indeterminate`) — *so that the gate can measure them*.
★ An enactment with no specimen is an enactment no gate can see; adding the specimens is part of
the enactment, not decoration.

**Leg 2 — the star, option C**: `.chip[aria-pressed="true"]:hover` / `:active` now take the washes
(`--chip-hover` / `--chip-pressed`) with `color: var(--label)`, border following the wash. Verified
by driven render: dark hover **15.72:1**, pressed **9.15:1**.

Verified first-hand by this wrap sub: `--error-atom` appears **16×** in `canon.css`; both
`aria-pressed` state rules present in `canon.css:2664`–`2665` and the snippet at `:170`–`:171`; the
three error specimens present at snippet `:220`/`:230`/`:239`.

## ④ What Dave ruled and this session did NOT do

`s152-D1`: **fix the gate's MARK leg now, and mutation-test it.** It is **RULED, NOT ENACTED** —
the window hit the stop line first. It carries to #153 as the new top item with the full receipt
above.

⚠ The consequence must be written plainly, because the alternative is a silent lie in a green
column: **the two remaining Selection-controls star reds are KNOWN-FALSE reds and are DECLARED, not
resolved.** They clear when the MARK-leg fix lands and not before. Marking them green now would be
exactly the false inscription the measurement above exists to prevent.

## Resolved state, and what is still open

**Resolved:** `s151-D3` legs 1 and 2 are enacted and its UNPROVEN caveat is discharged by
measurement · the 1.66 diagnosis is disproved twice over · `s152-D1` is recorded.

**Open:** ① the MARK-leg fix (`s152-D1`, ruled, unenacted) · ② the **green/success-ink
background-keyed scope** — still **Dave's and unanswered**, and it must not be inferred from
`s151-D1` · plus the carried set: Banner-8 hover-wash architecture gap, box border rung-or-`#F6604C`,
the Chart-bar/Reorder carrier gap, the ~12 `err-msg` classes, hover-wash symmetry, gate reds
30 · 45-residual · 82, and the snippet gate's 13 fails.
