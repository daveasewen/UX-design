# ADR-0016 — Enactment proof: rulings must be provably LIVE, not merely inscribed

**Date:** 2026-07-27 · **Status:** accepted (Dave, in-chat, 2026-07-27, promoting his own ds-014 complaint into the build: *"okay we are loosing decisions, this is getting frustrating"* → *"is this in the next session, we nee to fix it"* — the fix is the deliverable, not a proposal) · **Extends:** ADR-0007 (project memory / decision graph — this is the *enforcement* half of the record it keeps) · **Relates:** ADR-0004 (WCAG 2.2 AA floor — several UNPROVEN rows are accessibility rulings) · ADR-0013 (the `_validate_partials.py` ratchet, reused here as the rollout posture) · ds-013, ds-014 (the defects that forced it)

## Context

Apollo's governing principle is **verification = enforcement**: judgment is encoded as blocking
gates, and "done" is withheld until they pass. Fifty-six build steps enforce it.

That principle has a hole in it, and 2026-07-27 is the day the hole became measurable.

**Our gates prove the corpus is SELF-CONSISTENT. Nothing proved a RULING IS LIVE in the artefact
Dave looks at.** Those are different questions. A ruling can be debated, ruled, inscribed in its
ledger, referenced in a gate, shipped green — and be silently not in force for weeks. The gate is
green because the corpus agrees with itself. Nobody asked whether the pixel obeys.

Three OBSERVED instances, all inside eight days:

1. **DV-D08** was ruled, inscribed, gated-green and **not in force for weeks**.
2. **ds-013** — `gen_showroom.py` handed snippets to their pane iframes as `srcdoc`, which re-based
   every relative URL against the parent. `type.css` **404'd in all 49 showroom panes**; every
   `.t-cm-*` composite was inert. The whole library rendered uncomposed type and every gate stayed
   green. Found by Dave's eye.
3. **dv-004** (BLOCKING: *"minimum 2px separation between colour blocks"*) — implemented in
   `_validate_dataviz.py`, guarded by `if dtype in ("donut", "pie", "stacked")`. Chart-bar's stacked
   figure declares `data-dv-type="stacked-column"`. **Measured separation: 0.0px, `stroke: none`,
   at 1180 and 760, in the snippet and the showroom alike.** The gate did not fail; it never looked.

The common shape is not carelessness. It is that **every one of these was found by a human eye, and
none of them was reachable by any check we had.** Dave's ds-014 list is four items long because
that is how many he happened to notice.

The failure mode with teeth is the third one: **a check that cannot see its subject and passes
quietly.** `_sweep_type_enactment.py` reported a cheerful *"0 deviations"* when it could not read
the stylesheet at all. `_verify_dv_legend_members.js` would have passed any member whose series
happened to be named "Current". A green light from a blind check is worse than no check — it is
what let ds-013 live for weeks.

## Decision

**1 · A ruling's enactment status is a first-class, generated fact.**
`knowledge/_build_enactment_register.py` emits `knowledge/_ENACTMENT-REGISTER.md`: one row per
ruling harvested from every ledger (`_DATAVIZ-`, `_RAG-`, `_TYPE-`, `_BUTTON-DECISIONS.md`) and
every ADR. Regenerated every build, so it cannot rot.

**2 · Four verdicts, and the middle one is the point.**

| verdict | meaning |
|---|---|
| **PROVEN** | an executable check names the ruling **AND** a selftest case proves that check can FAIL on it. The only verdict that means *in force*. |
| **CLAIMED** | a check names the ruling, but nothing proves the check can fail on it. **ds-013 lived here.** |
| **UNPROVEN** | no executable check names it at all. |
| **NOT-GATEABLE** | the ledger says so **explicitly, with a reason**. Never inferred by the script. |

CLAIMED is not a soft PROVEN. It is the specific state in which our three worst defects hid, and
naming it is most of this ADR's value.

**3 · Scope blindness is audited, not assumed.**
A gate that branches on a corpus vocabulary silently skips values it does not enumerate. The
register cross-references the vocabulary **live in the corpus** against the branches the gate
actually tests. First run, first vocabulary (`data-dv-type`): **three blind values** —
`stacked-column`, `grouped-column`, `scatter` — appearing **zero** times in `_validate_dataviz.py`,
so dv-004, dv-bar-009 and dv-line-011 are all inert on those charts.

**4 · Every proof must carry a bite that proves the proof can fail.**
A P2 enactment check ships with a case that makes it fail, or it is not a proof — it is a CLAIMED
row wearing a badge. The register's own generator obeys this: it refuses to write a register that
harvested zero rulings rather than reporting a cheerful empty one.

**5 · Ruled-vs-RENDERED, never ruled-vs-ruled.**
An enactment proof reads the RULED value out of its source of truth and asserts the RENDERED value
in a real browser with the licensed face. Static agreement between two documents is what we already
have and is exactly what missed all three defects. `_sweep_type_enactment.py` is the pattern.

**6 · Rollout is a ratchet, advisory first (P3).**
Wired as an **advisory** build step on day one (step 56 of 57). It reports **53 UNPROVEN of 76**,
and a gate that fails 53 rows on day one gets switched off — and a switched-off gate is how we got
here. It goes
blocking once the register is green or each row is deliberately waived, per the posture that
worked for `_validate_partials.py`.

**7 · Promotion stays Dave's.** The register measures; it never derives a fix and never promotes
one. Every row it turns up is a candidate for Dave's ruling, not an agent's correction
(derivation governance, unchanged).

## Consequences

**The first honest measure of this debt: 3 of 76 rulings (4%) are PROVEN.** 20 CLAIMED, 53
UNPROVEN. That number is the finding, not a failure of the script — and it reframes Dave's ds-014
complaint. He is not noticing four regressions. He is noticing the visible edge of 73 rulings that
nothing checks, and he is doing it with his eyes because that is currently the only instrument we
have.

⚠ **These figures are MEASURED at 2026-07-27, from the register the build wrote — not predicted.**
The count includes this ADR (the register harvests ADRs, so ADR-0016 is itself an UNPROVEN row, as
it should be: nothing yet asserts that the register is in force). An earlier draft of this section
said 75/52; that was written before the generator ran and is corrected here rather than left
standing — the same class of error as Correction 2 of 2026-07-26.

- **Positive.** The debt is now a number that moves. Newly-authored rulings can be triaged at
  inscription time. "Gated" stops being a synonym for "enforced" in our own prose.
- **Cost.** P2 is real work: each proof needs a render harness, a source-of-truth read, and a
  failing bite. Advisory-first means the register can be ignored — mitigated only by the ratchet
  actually being walked.
- **Risk, named.** This register is itself a check, and therefore itself capable of being blind. It
  detects a ruling ID by textual reference, so a check that enforces a ruling **without naming it**
  reads as UNPROVEN (false debt), and a check that names a ruling in a comment reads as CLAIMED
  (false credit). Both are safe directions — they overstate the debt — but they must be corrected
  by hand as P2 lands, not silently tolerated.
- **Supersedes nothing.** It closes the gap ADR-0007 left: the record kept provenance and
  confidence about what was DECIDED, never about whether the decision still BITES.

## Provenance

OBSERVED this session, by render, in the licensed cut, at 1180 and 760, snippet and showroom:

- **Stacked segment separation: 0.0–0.1px** across all 4 columns × 3 boundaries, `stroke: none`
  (dv-004 requires ≥2px). Identical in snippet and showroom ⇒ a genuinely lost decision.
- **Stacked alpha-key contrast: 3.31 / 3.46 / 3.78:1** at 12px/700 against the three series fills.
  The keys render `#1A1A1A` (`--ink`), not the `var(--page)` their markup declares — CSS
  `text.dv-barkey{fill:var(--ink)}` overrides the SVG presentation attribute. White would measure
  ≈5:1 and pass. Identical in snippet and showroom ⇒ a genuinely lost decision.
- **Donut centring: does NOT reproduce.** Centre value dx **+0.00**, dy **−2.00** (optical), ring
  offset **0.00** inside its canvas — identical in snippet and showroom at both widths. Consistent
  with a ds-013 artefact, now fixed. *Separately and un-ruled:* `.dv-donut-row` is `flex-start`, so
  the ring+legend cluster pins left and whitespace grows with viewport (−114px at 600 → −534px at
  1440 from figure centre). No ruling covers it; flagged, not fixed.

*Inferred, not observed:* that the 20 CLAIMED rows contain further live defects. Plausible on this
evidence — dv-004 was a CLAIMED row — but unmeasured until P2.
