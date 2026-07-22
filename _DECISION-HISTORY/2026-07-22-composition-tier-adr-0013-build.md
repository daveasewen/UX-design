# 2026-07-22 — The composition tier built: ADR-0013's clean-room, and the press-physics reversal (B-D7)

*Session: "Apollo ADR-0013 clean-room" (FABLE solo, serial, afternoon — same day as the ADR-0014
theming clean-room). Spine entry: `_LIVE-STATE.md` 2026-07-22 afternoon delta. Ledger: 
`knowledge/_proforma/_BUTTON-DECISIONS.md` B-D7. Record: `docs/decisions/ADR-0013` Consequences
(build ✅). Lands whole, dated from `date`, never silently edited after.*

---

## Why this session existed

ADR-0013 (ruled 2026-07-21) diagnosed that atom retrieval was VALUE-level only: organisms bound the
same tokens as the atoms but re-typed the atoms' RULES locally — 13/40 snippets carried a local
button recipe, 7 carried Button's scale-press by copy, 4 pressed with `translateY(1px)`. Fanning ~50
Phase-2 components onto that pattern would have duplicated sub-atoms ~50×. The mechanism (generated
partials + a component-type tier) was ruled to land BEFORE Phase-2. This session was that build.

## Finding 1 — the reviewed refinement that turned out to be the canon (the B-D7 arc)

The survey turned up something the ADR's language ("Icon-button — lock-step atom") didn't anticipate:
Icon-button's physics was **not drift but a documented refinement** — `scale(calc(1 + 2/44))`,
"size-scoped scale-physics: hover +2px / press −2px on the 44px target", darken .94 — and Tranche-1
corroborated the same philosophy corpus-wide (its whole factor zoo is size-scoped: btn 1.02 ≈ 1px/side
at ~120px, ib 1.045 at 44px). Injecting Button's flat 1.04/0.95 would have erased a reviewed choice.

Asked plainly ("percent vs exactly-2-pixels"), Dave first ruled **flatten to the shared 4%**. Within
the hour he reversed: *"the movement in the icon button (its more subtle) is the one that should
propagate to everything in console and Mono"* — and extended the ruling in the same breath: *"the
movement should be absent from Legacy and Supercharge, just colour change. But of course this should
be changeable in the future if finessing is needed"*, then the constraint *"as long as we don't use
any js we may tune later."*

**Both beats are inscribed in B-D7 deliberately** — the reversal IS the ruling, and recording only
the second beat would have made the first look like agent drift when the transcript evaporates.

### How the reversal reshaped the design (cheaper than it looked)

The mechanism barely moved; only the parameter set changed:

- Factors became **`motion/press/travel` = 2** (px of total size change — pixel-true, so big buttons
  stop lunging) and **`motion/press/darken` = 0.94**, expressed as
  `scale(calc(1 ± var(--press-travel)/var(--phys-size)))`.
- **`--phys-size` is deliberately LOCAL geometry, not a token** (like `--h`): buttons 120 (Tranche-1's
  width-scoping), icon button 44. Uniform scale cannot give equal px growth on both axes of a
  non-square control, so the characteristic-size divisor is an honest approximation, not physics —
  the Tranche-1 precedent was followed rather than inventing a third model.
- **The theme dial fell out for free:** `travel→0` makes the transform the identity and `darken→1`
  makes the filter a no-op — so "movement absent from Legacy/Supercharge" is two one-line overrides
  in the existing override sets, no rule changes, no fencing of the partial per theme. Components
  stay theme-blind; finessing later = editing a number. Verified in the generated cascade at every
  tier: root var + group cache (via alias expansion) + all four member component re-projections,
  both themes.
- Console **inherits** Mono's motion (no override) rather than joining the ADR-0014 locked fence —
  the fence was ruled for colour; extending a LOCKED ruling uninvited felt wrong. Flagged to Dave
  instead.

Icon-button ends the session visually **byte-identical** to its reviewed self; Button and Modals
calm down (4% → ~1.7% at 120px, darken .85 → .94); Progress-tracker's translateY press becomes the
family scale; Legacy/SC lose movement entirely. All four are on Dave's eyeball list.

## Finding 2 — the registry as a token store with $-structural keys

ADR-0013 ruled "ONE registry, both halves." The shape that made both halves work in one file:
`component-type/<group>/<param>` is **path-addressable** (so every existing walker — projector,
cascade, tier logic — resolves it with one prefix route), while the rule halves live under
**$-prefixed keys** (`$members`, `$partials`) which every token walker already skips. The alias hop
(component var → type-group → semantic role) needed zero generator re-architecture: adding the
registry to `gen_theme_cascade.alias_map()` made `_expand_aliases` propagate a theme's
`motion/press/travel` override to the group cache automatically — the same fixed-point that carried
the warm ramp yesterday.

One deliberate niggle: unitless formatting. Three formatters (`gen_canon_tokens`, `gen_snippet_tokens`,
`gen_theme_cascade`) render numbers as px; the press factors must stay bare. Each gained the same
path-predicate rather than a shared helper — three small local predicates were judged less risky than
threading a new import through generators mid-session. If a fourth consumer appears, consolidate.

## Finding 3 — contracts, not conventions, at the membership boundary

The generator enforces four contract classes per member, and the live run proved each earns its keep:
required vars (`--press-travel`/`--press-darken`/`--phys-size`/`--spring`/`--press` — the injected
rules' free variables), **matchValues** (`--spring`/`--press` must EQUAL the source atom's declared
composites — duration/easing are already tokens but composites can't manifest-bind yet, so value-match
pins them against drift), required declarations (`transform var(--spring)` — the base-rule transition
the partial's hover depends on), and **manifest binds** (the factor vars must bind the GROUP tokens,
which is what makes the exit gate's one-dial-moves-everyone true). Membership without markers is a
loud failure, not a silent skip — accretion stays deliberate (ruling 3).

## Finding 4 — what bit, and why that's the system working

- **The empty-marker bug.** The first AUTO-PARTIAL regex demanded a newline BETWEEN the marker pair,
  so a freshly-migrated file's adjacent markers (the exact shape every future migration starts with)
  read as "no markers". The live run caught it on Modals in minutes; the fix normalises padding in
  the replacement, and selftest bite 5b now holds the door open (`ADR-0005 §5`: a gate earns trust by
  biting on the true-positive).
- **The grid gate bit the resurrection.** The 273d18c~1 dots stepper carried `top:13px`/`height:3px`
  from the pre-gate era; DEF-005 failed the build. Corrected to 12px/4px (the 4px connector now
  matches the track's height — arguably better than the original). Lesson worth keeping: 
  **resurrect-verbatim is not exempt from current gates** — a reviewed artefact from an earlier
  regime re-enters through the same door as new work.
- **Ratchet census = 32 rules**, exactly the accretion worklist ruling 3 wants (Selection-controls'
  translateY, Input-fields' tail-btn, Quick-actions' `--qa-*` zoo, Modals' `.close` press…). None
  were forced into the family — observed duplication, queued.

## Also closed in this session

**ds-008** (radius census counted HTML-comment prose; now strips `<!-- -->` + bite case) and
**ds-009**, fixed stronger than specced: the consult corpus is **discovered** (glob over
`_proforma/_*-DECISIONS.md`), the ruling-ID regex is generic, and a ledger yielding zero records
fails the BUILD — the completeness assertion runs every build rather than living in a hand-run
selftest. B-D1…B-D7 are now retrievable (verified live mid-session).

## Resolved state

Build **51/51 green** (45→51: partials sync + partials selftest + canon-components regenerate +
determinism check + ratchet + ratchet selftest). Exit gate passed both halves — value dial 2→6 moved
all four consumers in both modes; a source rule-text probe moved all three injected copies; both
reverted clean. Seed 124 = inscribed 124, zero mismatch. Showroom regenerated. Render-verify still
OWED (sandbox headless-shell refusal, unchanged from the morning session).

## Open

Dave's eyeball pass (B-D7 deltas + the morning's SC dark sheet + 4 held whites + Console radius +
bigplay) · Phase-2 fan-out now unblocked · census-driven accretion (icon-press group?) · composite
motion tokens (would retire the matchValues pin) · consider motion prefixes joining the Console fence
if Dave wants it locked rather than inherited.
