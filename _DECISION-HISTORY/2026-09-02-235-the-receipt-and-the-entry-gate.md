# 2026-09-02 · #235 — the receipt, and the entry gate that has to parse before it can judge

provenance: 235 · 2026-09-02
status: ruled — `knowledge/_rulings.json` § `s235-D1` · `s235-D2`

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #235 · `GOOD-MORNING.md` ★ LATEST #235.
Build half: `notes/_briefs/2026-09-02-235-L1-receipt-gate-brief.md` (`W-344`) and the filed report
`notes/_subreports/2026-09-02-235-L1-receipt-gate.md` (`W-345`), evidence at
`notes/_subreports/assets/2026-09-02-235-L1-receipt-gate/`. Lane parent:
`notes/_briefs/2026-09-02-234-v106-brief.md` (`W-343`), lane **L1**.
This file holds the WHY and HOW; the WHAT is in the ledger and the spine, and is not repeated here.*

---

## 1. The morning had exactly two questions in front of it, and both were about identity

#234 left the v1.0.6 brief with five ordered lanes and two things L1 could not start without: what a
provenance receipt is KEYED ON, and what the new gate is CALLED. Both read like bookkeeping. Neither
was.

**The key question — rC Q1 — was filename, slug, or content hash.** The recommendation put to Dave
was the hash, on one argument: *filenames and slugs can be renamed without the page changing*. A
receipt keyed on a name asserts provenance about a label, and labels are the part of this corpus that
moves most freely. He answered *"I'd go with your recommendation"* and it became `s235-D1`.

⚠ **The cost was priced BEFORE the answer, not discovered after it.** A content hash changes on every
regen serial, so a receipt is valid against the pack version it was minted from and **never across
cuts**. That is a real loss — it is exactly the case where the gate will shout `HASH-MISMATCH`, its
loudest verdict, for the most benign possible cause (a pack was re-cut). It was accepted with the
ruling rather than smuggled past it, and it is carried forward as an UNPROVEN with a price on it
(~2K tk for a pack-aware line) rather than as a surprise waiting at the v1.0.6 cut.

**The name question was smaller and had a hard constraint.** `_validate_behaviour.py` — the obvious
name — is TAKEN by ADR-0015 and means something else. Dave: *"`_validate_receipt.py` it is."* That is
`s235-D2`, and it is the reason the question existed at all: a name collision in this corpus is not
cosmetic, because the gate roster is read by humans deciding what a red means.

## 2. Why the gate had to PARSE before it could judge, and what that cost

`s234-D6` had already ruled the shape: `_validate_screen.py <path>` binds the rubric by parsing a
RECEIPT **first**. L1 built that literally — `knowledge/_validate_receipt.py` reads a
`#provenance-receipt` block, re-hashes every spliced region against it, checks the declared behaviour
address is loaded, and speaks ADR-0016 (`PASS` / `FAIL:<reason>` / `UNPROVEN:<what would prove it>`).

★ **The interesting part is what the sub had to build to make the test honest.** A receipt gate proved
against a hand-written page proves nothing, because a hand-written page has no source snippet to
diff against. So `knowledge/gen_provenance_receipt.py` composes a page by **splicing real bytes out of
five real snippets** and mints the receipt from what it actually spliced. Only then does a mutation
mean anything.

Three drives, all at the conductor's own seat:

1. `dashboards/international-banking-dashboard.regen-v1.html` → **`FAIL:NO-RECEIPT`, rc 1**.
2. the composed `…regen-v2-receipt.html` → **`PASS (+1 UNPROVEN)`, rc 0**.
3. one byte changed (`2,450.00` → `3,450.00`, page offset 65,526) → **`FAIL:HASH-MISMATCH` —
   `Stat-card#markup` does not match its receipt, *"first differing byte at offset 184 of the
   region"*, rc 1.**

⚠ **Drive 3 is the one that matters, and it is the [[mutation-tests-the-clause-not-the-feature]]
discipline paying out:** the arm does not test that the gate has a hash-mismatch branch, it tests that
a real one-byte edit to a real spliced region reaches that branch and names the region and the offset.
An offset the receipt alone could not have given.

## 3. The dead end that was not a dead end: the brief's premise did not survive its probe

The L1 brief was written against *"whichever module today injects `#token-manifest` into snippets"*.
⛔ **No module does.** 137 of 137 snippets carry it hand-authored. The premise died on contact.

★ **What survived was the SHAPE, not the mechanism** — a sibling JSON block beside the manifest, never
a key inside it. So the receipt became a NEW module rather than an extension of an existing one, and
the clause it honours is the one `s234-D5` actually cares about. This is
[[premise-ages-faster-than-rule]] with a happy ending: the probe ran before the build committed to the
wrong parent, and the correction is in the report rather than in a week of rework.

## 4. The ratchet, and why it is deliberately NOT a ruling

The chained step-0 ships as a **ratchet**: a page carrying a receipt is held hard to it; a page
carrying none reports `UNPROVEN:NO-RECEIPT` and does **not** block.

The number behind that choice is the whole argument: **7 of 7** screens in `_validate_screen.py`'s
default population would go red the day a blocking version lands. A gate that fails on correct
behaviour teaches sessions to route around it — the same reasoning that gave `ds-022` its `HOLE`
hatch. `--receipt-strict` flips it today for anyone who wants the hard form.

⛔ **The sub declared the posture as a BUILD JUDGMENT and refused to dress it as a ruling**, and it is
carried to Dave as ruling-shaped question 1: *when does `NO-RECEIPT` start blocking?* That refusal is
the point. A gate's strictness schedule is a policy about how much red the project will tolerate, and
that is not a thing a build sub gets to decide by shipping a default.

## 5. The contradiction L1 surfaced and could not resolve

⚠ **The two routes to a receiptable page disagree with each other, and neither side is obviously
wrong.** The verbatim `<style>` splice that makes a page receiptable carries **191 hex** literals and
therefore REDS `_validate_compose`. The route that PASSES compose is the hand-written one — which
cannot carry a receipt at all, because there is nothing to hash against.

So today a page can be *composable* or *provable*, not both. That is ruling-shaped question 2, and it
is a precondition to receipts on real screens rather than on a purpose-built fixture. Naming it as a
contradiction — rather than picking a side inside a build lane — is what keeps it visible.

## 6. What running the gate did to the record, declared rather than tidied

Driving `_validate_screen.py` rewrote `knowledge/_SCREEN-GATE.md` and **7** `*.canon.md` files, and
MINTED two new rows for the regen-v1 and regen-v2-receipt dashboards. ⛔ **Those files are committed
exactly as the gate wrote them.** Curating a generator's output at wrap time is how a generated
surface quietly becomes a hand-maintained one; whether the two dashboards STAY in the screen-gate
index is ruling-shaped question 3 and is Dave's.

## 7. Where this leaves the programme

L1 is the first v1.0.6 lane with running code and a bite-test on a real artefact. It also proves the
half of `s234-D5` that L2 has to supply: the gate already checks that a declared behaviour address is
**loaded**, so L2's job is to make the address exist as a typed declaration rather than as prose.

⛔ **Three rows did NOT close** — `W-344`, `W-340` and `W-342` each close on the **conductor** reading
a REPLAY-THESE line, and only the sub has read one. A sub reading the line is not the condition the
row states, and closing on the near-miss would be the cheapest possible false inscription.

**Open and Dave's, in order:** the `NO-RECEIPT` blocking date · the composed-page CSS route · the
screen-gate index membership · the role-name words (untouched by `s235-D2`) · rC Q3/Q4 · L2–L5.
**UNPROVEN and priced:** the receipt across a pack cut (~2K tk) · `retrievalSet` null · the page was
never rendered (~3K tk) · `_tests/test_gates.py` refused with `ENOSPC` and is a COULD-NOT-ASK, with CI
as the only verdict.
