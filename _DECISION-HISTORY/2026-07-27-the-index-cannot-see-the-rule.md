# The index cannot see the rule — instrument fit at corpus scale (2026-07-27, later morning #4)

```
provenance: local_cbfd919e · 2026-07-27
status: observed
```

*Session: Opus 5 solo self-conducting, effort MAX. Dave ruled four of the five open calls at the
top of the window and set the order: **finish #3, then #2**. Spine entry: `_LIVE-STATE.md` ⏱ LATEST
delta, same date. Defect record: `knowledge/_DS-IMPROVEMENTS.md` **ds-016**. Ideas:
`_FUTURE-STATE.md` § KG forcing-function → **Exploration beat 2**. Sibling dossier (the session
that produced the five calls): `2026-07-27-the-instrument-cannot-see-the-property.md`.*

---

## What was asked

Dave's rulings, verbatim in substance: **(1)** instrument fit — "go with your ideas" ⇒ third axis;
**(2)** "I lean adoption, seams less likely to carry mistakes, you can correct me if I'm wrong,
maybe sweep if more efficient, I need to understand the implications of both"; **(3)** run the
465-rule pass — "cool"; **(4)** "I lean fix, but this probably needs a discussion" ⇒ **DEFERRED, not
ruled**; **(5)** `CTRL` sweep — "yes". Plus a standing steer that shaped every design decision below:
***"I just want the most robust methods."***

## Finding 1 — the tool had to be built so it could not guess

The whole point of the pass is to expose checks that measure a proxy. A tagger that assigns
instruments by keyword overlap would have BEEN that defect — it is precisely what call (4) exists
to fix in `_consult.py`'s `enforcement_for_rule()`. So three constraints were fixed before any code:

1. **The gate side is OBSERVED, never inferred.** Instrument detection keys on imports and API calls
   (`sync_playwright`, `.chromium.launch`, `page.evaluate`, DOM-parser imports) — never on words.
2. **The rule side is tagged from the rule's own TEXT, and every tag carries the phrase that
   produced it.** A reader can overrule any row without reverse-engineering the pattern table.
3. **UNKNOWN is a first-class bucket.** An unclassified rule silently filed as I0 would be recorded
   as "static is adequate" — the exact lie the register exists to expose.

Constraint 1 earned itself within minutes. A first, deliberately crude probe reported **three gates
as RENDER** — `_validate_proforma.py`, `_validate_token_tiers.py`, `_validate_type_composites.py`.
None drives a browser. All three matched the bare word **chrome**, as in *monochrome* and
*demo-chrome*. ⚠ **The error direction is the point: it made gates look STRONGER than they are**,
which in a fitness audit produces silence, not noise. Pinned as bite 2.

## Finding 2 — the bite failed on its first run, and that is how the real finding surfaced

Bite 1 asserted the ds-015 ground truth: `aid-009` requires RENDER and lands UNDER-INSTRUMENTED.
It returned `None`. **`aid-009` is not in `_rules-index.json` at all.**

Chasing that, measured:

- `guidelines/*.md` declares **698** rule anchors (`{#id}`).
- `_rules-index.json` holds **465** — the ones carrying an enforcement-destiny tag. This is
  BY DESIGN; the generator's docstring says so plainly.
- The remaining **265 anchors carry an ID but no destiny tag**, and are therefore invisible to the
  index, to `_consult.py`, to the enactment register, and to this new pass.
- **7 of those 265 are cited by a live gate as its authority**: `aca-003` · `aca-004` · **`aid-009`**
  · `aid-020` · `avd-006` · `axs-003` · `nam-001`.

`aid-009` is Dave's hit-area ruling of 2026-07-03 and the founding case of ds-015.
`_validate_a11y.py` names it five times as the ruling it enforces. Its anchor line ends
`Bite-tested (test_gates target24)] {#aid-009}` — the destiny tag was never written. So the rule a
BLOCKING gate enforces **cannot be retrieved by any tool that reads the index.**

And the mirror image, in the same family: `icon-005` — **BLOCKING**, *"Functional icons need a
minimum 44×44px target area"* — IS indexed, and **no gate names it at all.** The 44×44 rule that
exists has no check; the check that exists cites a rule that cannot be looked up.

⇒ **This is ds-015 inverted.** There, the gate could not see the component. Here, the index cannot
see the rule. The signature is identical to the silent-lookup class recorded three times already
(ds-010 · ds-013 · the DV-D15 local mirror): **the markup is correct, the lookup fails, and nothing
reports it.**

⚠ **Fairness, recorded at the time:** the 265 are excluded *by design*, not by bug. The defect is
not the exclusion — it is that **nothing anywhere reported that seven live gates depend on rules
inside the excluded set.** Deciding what to do about it is call (4)'s discussion, not this session's.

## Finding 3 — the tool counted itself as a gate

After the fix, `icon-005` came out **FIT**. Its evidence column named exactly one file:
`_build_instrument_fit.py` — because the bite comment mentions `icon-005`. **A register that NAMES a
rule was being counted as a check that ENFORCES it**, and the self-reference read as green.

Third instance this week of the standing lesson: *assume your probe is wrong in the direction that
reads as green.* Fixed with a `NOT_A_GATE` exclusion (this file + `_build_enactment_register.py`,
which has the same exposure) and pinned as bite 8.

## The measured result — and its honest limit

**465 rules · UNDER-INSTRUMENTED 12 · UNGATED 165 · UNTAGGED 279 · EYE-ONLY 4 · FIT 5.**

**Two of the 12 are BLOCKING, and both are contrast rules with static gates:** `dv-016` (chart
titles/axis/gridlines, black-or-grey by ground) and `icon-011` (*"icons require 4.5:1 contrast in
all instances"*). Contrast is a **composited** property; a static parse reads the declared hex, not
what lands on screen. That is the same class as ds-010, ds-013 and DV-D15 — three proven instances
already.

⚠ **The limit is stated first, not buried: 279 of 465 (60%) are UNTAGGED.** The pattern table
classifies 40% of the corpus, so **12 is a floor, not an answer.** Deliberately NOT fixed by
widening patterns until the report went quiet — that is anti-false-fix #2 in the tool's own header,
and it would have converted a measured finding into a tuned one.

**11 bites, all passing.** Three of them (2, 8, and 1c) exist only because they caught a live defect
in this tool during this session.

## Finding 4 — Dave's call (2): adoption vs sweep are complementary, and he ruled it so

He asked to be corrected if wrong. He wasn't wrong — the framing was.

- **Adoption-time** captures intent at the moment it exists, from whoever knows *why*; it yields
  **counted** data rather than inferred data. But it can only see adoptions made *after* it exists —
  **64 of 67 snippets already use the `::before` expander, and it would find zero of them** — and a
  *missing* declaration is silence, the same failure mode being hunted.
- **Sweep-time** is retroactive and needs no cooperation. Proven the same day: this pass surfaced 7
  dangling citations laid down months apart, which no adoption-time trigger could ever reach. But it
  reports late, and **its own coverage is unmeasured** — this sweep is blind to 265 rules and cannot
  classify 279 more, and nothing revealed that until a second check was built.

⇒ **Neither is sufficient. Each one's blind spot is the other's coverage, and the only way to detect
a MISSING declaration is to sweep for it** — so the sweep is not optional, it is what makes the
adoption-time rule enforceable. **Dave ruled: *"You're right about 2 they are complimentary."***
Shape recommended and now held for design: adoption-time as the forcing function, plus a sweep
**narrowed to one job — find undeclared adoptions** (far smaller than a general sweep, therefore
cheaper and less blind).

## Resolved state

- `knowledge/_build_instrument_fit.py` — NEW, 11 bites, wired **advisory** into `_build_all.py` as
  steps 58 (selftest) + 59 (report), per the ADR-0016 P3 posture. Build **60/60 GREEN**.
- `knowledge/_INSTRUMENT-FIT.md` + `_instrument-fit.json` — generated, regenerate every build.
- ds-016 logged. Call (2) RULED complementary. Calls (1)(3)(5) ruled and (3) delivered.

## Still open

- **Call (4) — the consult's enforcement column.** Dave: *"I lean fix, but this probably needs a
  discussion."* NOT ruled. The `5/5 shown` denominator remains separable and trivial; **it was NOT
  done this session** (Red budget) and stays in GM §C·4.
- **Call (5) — the `CTRL` vocabulary sweep** in `_validate_a11y.py`: ruled YES, **not started.**
- **ds-016's own question:** what happens to the 265 untagged anchors — tag them, or make a gate
  citing an unindexed rule fail loud? That is the adoption-time/sweep pair applied to itself.
- **The 279 UNTAGGED rules** — whether to invest in the pattern table is Dave's call; the count is
  published so the decision is made on a number, not a feeling.
