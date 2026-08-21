# #212 — the triage sitting: how "get this boot down" became half a desk

provenance: 212 · 2026-08-21
status: observed

*Both-way links: spine entry `_LIVE-STATE.md` § ⏱ LATEST DELTA #212 · ledger
`notes/_MEMENTO-DECISIONS.md` § ★ #212 · rulings `knowledge/_rulings.json` § `s212-D1`…`s212-D12`.
This dossier holds the WHY and HOW; the ledger holds the WHAT. Nothing here is a ruling.*

---

## The arc, in one paragraph

Dave opened with *"to start, Id like to get this boot down"* — a cost complaint about the cold-start
price, nothing more. The boot audit needed an inventory of what the boot was carrying, the inventory
needed the desk enumerated, and the enumerated desk turned out to be **forty-nine of his own rows**,
most of them small calls that had been waiting for a sitting that never came because no session ever
had a cheap enough way to put them all in front of him at once. The answer was three control pages,
and the day became a triage. Twelve rulings later, his open rows measured **twenty-eight**.

## Why three pages and not one

The first page (`REVIEW-212-boot-and-desk-triage-v1.html`) is an inventory with a strike-list grammar:
connectors, skills, then the desk in four bands — the eye-review pile, the unconditioned ancients, the
dials-and-leftovers, and what stays live. It exists to make the shape visible before any single call is
asked for.

The second (`-dials-v1.html`) exists because **a number you have not seen is not a number you can
ratify**. Six of the fourteen items were bare constants — `700`, `1.57`, `6`, four size caps — and
asking Dave to ratify a constant he has never watched behave is asking for a rubber stamp, not a
ruling. The page shows each dial with what it currently does.

The third (`-rule-now-v1.html`) exists because the remaining calls were **visual**, and a visual call
put in prose is a call answered on the wrong evidence. The disabled-grey pick, the RAG manifestation,
the donut pair — each got its live render, iframed, so the eye was judging the artefact and not a
description of it. This is also what quietly discharged the #86 caveat that the RAG live render had
never actually been verified.

## The finding that cost the most time, and why it is worth keeping

`s212-D11` restamped four advisory caps from the old tape unit into real tokens. The restamp is a
*restatement*, not a re-dial: for each cap, `REAL(artefact at its ruling) × (cap / cl100k at its
ruling)`, with every baseline reproduced exactly at the original ruling commit before a single number
was proposed. That discipline is why the numbers are defensible.

And then the gate went red — on **M8**, a check that had nothing to do with any of it.

The cause: M8's selftest fixtures hard-coded 17- and 30-line bodies, sized so they would land either
side of the *old* constant. Move the constant and the fixtures test nothing; worse, they fail, and the
failure looks like a product defect rather than a stale test. **A fixture that pins a derived number as
a literal converts every legitimate constant change into a fake failure.** The fix was to derive the
fixture sizes from the live constant, which is the class fix and not the instance one.

The general form is worth hunting: anywhere a selftest pins a size it does not own, the same trap is
already set.

## The ruling that had nothing left to enact

`s212-D4` strikes the stray `70%/95%` band from `GOOD-MORNING.md`. At the wrap the literal was probed
and **is not there** — `grep -c` returns 0, and the only surviving mentions are dated notes and one
generated block that clears itself when the row closes.

The temptation at that point is to make *some* edit so the enactment register has something to point
at. That would be a false inscription in the smallest possible package. The honest record is: probed,
already absent, the strike rides on the ruling and the row closure. This is `enactment-register-adr-0016`
doing its job in the direction people forget — **CLAIMED lies, UNPROVEN is honest**, and *"already
true"* is a third state that also has to be said out loud.

## The register that could not see its own store

Marking the closed rows in `knowledge/_GOVERNING-RECORDS.md` required joining the register to
`knowledge/_state.json`. The join found three rows — `G3`, `G7`, `G8` — reading **OPEN** in the
register while the store had carried them closed since #161/#163, and one row, `G18`, that lives in the
store and has never existed in the register at all.

Nobody was careless. The register's own contract says the closure is inscribed in the ledger first and
*then* the row is marked here — two acts, and the second one is the one a session under wrap heat drops.
Fifty-one sessions of a row reading OPEN is not a lapse in attention; it is a **missing gate**. The rows
were repaired by marking (never deleting — the register is also the record of what was once open), each
with its own pre-existing pointer rather than this session's, and the class was written up rather than
patched over.

## The by-reference carry tail, and the bill it just presented

#211 solved a real problem the right way. Its banner's deep carry tail had grown to fifty-four items and
the chain was missing its `<40%` demand; re-typing the tail every wrap was the cost, so #211 carried it
**by reference**: *read it on the ★ PRIOR (#210) banner, which is still live in this file.* The chain
came in at 26% and the selftest went green. It worked.

What it also did was write a pointer whose truth depended on the next wrap not doing its job. 2c keeps
LATEST plus one PRIOR; #212's banner pushes #211 into the PRIOR slot and rolls #210 out. The sentence
became stale-by-one the moment this wrap ran, exactly as designed and exactly as unavoidable.

So the trade is now visible with a price on it: **by-reference buys a lean chain and pays a redirect at
every wrap, compounding by one hop each time. Re-typing pays tokens and buys a machine check** —
`carry_wording_check` can only compare text that exists.

#212 took neither pole. The surviving carry set is five items, not fifty-four, because this session
*ruled* two of them out of existence. Five is cheap enough to re-type, so five were re-typed and are
MEASURED; two were struck with receipts; the deep #210 tail stays by reference, redirected to its
archive batch, and is DECLARED UNMEASURED beside the carries rather than inside them.

The point is not which form is right. It is that **the form should follow the size of the carry set**,
and the carry set shrinks when someone rules.

## The number Dave asked for, and the answer he did not order

He asked whether the advisory cutoff should change, and the wrap was asked to mine
`notes/_GAUGE-LOG.md` for the **conductor-side** cost of recent delegated wraps.

There isn't one. The log has three relevant fields and none of them is that: `pre-flight` reads
⛔ NOT CAPTURED on thirteen consecutive delegated wraps, because a sub cannot measure the conductor's
window; `post-mortem` records FILL at the wrap-brief cut, which is the whole session and not the wrap's
share of it; `subs` is QUOTA and explicitly excludes the wrap sub's own spend. **The cost of writing a
brief and handing off has never been a measured quantity in this project.**

That is a more useful answer than a fabricated series would have been, and it is the honest one. The
nearest available data — the brief-cut FILL for #204 through #212 — is in the ledger, reported and not
interpreted, because a wrap sub does not price a stop line.

## What is still open, and why none of it was closed here

The fence held. `P8` is the one routing amendment left unruled and it is a genuine three-way tension,
not an oversight — Anthropic's Opus 5 guidance says remove verification scaffolding, canon rule 5 says
verify, and `s204-D1` built an adversarial verifier on purpose. Three readings stand in the check and
the pick is his.

Beside it: the stop-line re-base (his, with a boot-reduction option priced alongside, per the `s208-D1`
rider — and today's boot ran 63,258, five thousand over its own band); `W-99d`'s two riders; the whole
#211 seven-receipt sitting, now aged [1]; and the `W-` id space, which ran out at 99 during this very
session and is currently held together with letter suffixes.

That last one is the small, funny, real consequence of a good day: **the desk got half as long and the
naming scheme ran out anyway.**
