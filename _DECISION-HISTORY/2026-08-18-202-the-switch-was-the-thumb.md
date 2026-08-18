# #202 — the switch was the THUMB: a misreading enacted, caught by Dave's eye, corrected from the store

provenance: 202 · 2026-08-18
status: ruled — `knowledge/_rulings.json` § `s202-D1` · `s202-D2` · `s202-D3`

*Spine entry: `GOOD-MORNING.md` ★ LATEST #202 banner · `_LIVE-STATE.md` ⏱ LATEST DELTA #202.
Ledger: `knowledge/_rulings.json` (201 records at this wrap; `s202-D1`/`D2`/`D3` the newest three).
Both-way links per `_DECISION-HISTORY/README.md`.*

---

## Why this dossier exists

This session did not fail at a value. It failed at a **word**, and then spent seven work-sub cycles
enacting the failure. The final state is small — three rulings, one re-mint, one repaired generator,
one specimen — and it is the least interesting part of the record. What is worth keeping is the ARC:
how a single ambiguous noun in a ruling passed every gate, produced three artefacts Dave rejected on
sight, and was ended not by a better build but by **reading the store**.

## Finding 1 — the opening premise was right, and it was not the problem

The session opened on #201's residual ③: `s201-D5` had **ruled** square-theme floor precedence
(`thumb = max(container − padding, 0)`) but **minted nothing** for mono, legacy and supercharge. That
gap was real and it closed cleanly as **`s202-D1`**: the three square themes take Console's *tuned
dimensions* verbatim — sizes 24/36/44/48, paddings 2/2/4/4 — with radii 0 at every scale, and
`min-hit-area` 44 promoted to the base tier. Concrete numbers on disk, mint-time, no runtime
derivation (`s200-D1` clause a). Squares stay square.

Worth naming because of what came next: **the part of the session that was well-posed took a fraction
of the budget.** The overrun did not come from the hard problem. It came from the one nobody checked
was a problem at all.

## Finding 2 — the collision: "switch" had two readings and only one was in the store

`s199-D3` carved out a radius exception for the *switch*. This session read that word as a
**two-state variant of the segmented control** — a toggle. Under that reading the obvious work is to
mint a `segmented-switch` token family and show Dave what it looks like beside the segmented control.
So that is what happened: tokens minted, and **three** compare pages built to put the
beside-vs-replace question to him.

Dave rejected each one by eye. First *"the switch is still wrong"*. Then, at the third:
*"is your sub on drugs?"*

★ **Every gate was green across all three.** The tokens validated, the units validated, the tiers and
forks and provenance validated, the pages rendered. Nothing in the machinery can see that a correctly
minted token answers a question nobody asked — the defect was upstream of every instrument
[[green-tests-cannot-see-scope]].

## Finding 3 — what ended it was a store read, not a better build

The reflex after a rejection is another iteration. The thing that actually worked was reading
`s199-D3` **together with** `s200-D1`: the carve-out is the **sliding thumb** inside the segmented
control. Not a variant. One search, one minute, and the whole beside-vs-replace question **dissolved**
rather than being answered — it had never been a real question [[retrieval-default-hides-the-ruling]].

The corrected reading is inscribed as **`s202-D2`**, and it carries its enactment:

- console thumbs **RE-MINTED 4/6/6/8 → 0/2/4/6** — container (6/8/10/12) minus the **tuned dial 6**,
  floored at 0;
- the `segmented-switch` tokens **UN-MINTED — gone, not shadowed** (verified at the wrap:
  `grep -r segmented-switch` over `knowledge/tokens/` and `knowledge/canon/canon.css` returns nothing);
- `knowledge/gen_radius_derive.py` now derives `thumb = max(container − 6, 0)`, with **padding
  RETIRED as a radius input** — the selftest carries a dedicated dial proof that prints
  *"padding proven inert"*, so the retirement is tested rather than asserted;
- `--check` and `--selftest` both **rc=0**, which also consumes #201's residual ① (the stale sidecar).

## Finding 4 — the class-fix, and the fence it does not have

**`s202-D3`** generalises it: *no question framed as OPEN reaches Dave without the store search run and
its hits quoted alongside.* That is the cheapest possible fence for this class — it costs one search
and it would have refused this session's whole detour at the first beat
[[unrun-search-indistinguishable-from-absent-record]].

⚠ What it is **not**: a glossary. A glossary — one home where "switch", "thumb", "container", "track"
mean one thing each — was **floated and left floated**. It is Dave's, it is not queued, and until it
exists the next vocabulary collision has no fence except the provenance line. Recorded as floated,
never laundered into a ruling [[feedback-dont-launder-a-premise-into-a-ruling]].

## Finding 5 — a premise from the previous session was false, and the record said "expected"

#201's banner recorded that CI's complete `_build_all.py` pass was **EXPECTED** to clear the stale
baked artefacts after its push. This session found that premise is **false: CI surveys, it never
regenerates.** Nothing was ever going to clear on a push.

So the repair was done here instead — the four staleness fails (blast-radius, canon components, theme
cascade, mention map) fixed locally, and `knowledge/canon/canon.css`'s pre-rename
`--color-*-hover-1|2` var names cleared via `gen_canon_tokens.py` (`grep -c` → 0 at this wrap).

★ The general lesson, which is not new and arrived anyway: **an "EXPECTED" on a banner is a prediction
wearing the clothes of a receipt.** #201 wrote it honestly and labelled it as expected; one session
later the prediction's *premise* — not its outcome — turned out to be wrong
[[premise-ages-faster-than-rule]] [[enactment-register-adr-0016]].

## Finding 6 — a sub's `git checkout` destroyed work that no gate protected

Mid-session a work sub ran `git checkout` on a path to undo its own formatting slip. The tree carried
**uncommitted** work, and the command discarded the `s202-D1` `$note` prose along with the slip.

- The **values** were recovered and independently corroborated against
  `knowledge/_derive-radius-proposal.json`.
- The **prose** was reconstructed, and it is marked as reconstructed **in the artefact itself** —
  `$reconstructionNote` in `knowledge/tokens/layout.json`. A future reader must not cite it as the
  mint's own words. ⚠ A restatement that does not say it is a restatement is a confident false
  inscription; this one says so.
- Gated by addition: **worker-checklist step 0** in `knowledge/_RUNBOOK-parallel-conductor.md:126` —
  *"NEVER run `git checkout`/`git restore` on a path while the tree carries uncommitted work … undo
  your own mistake by re-editing, never by checkout"* [[feedback-gate-dont-patch]].

## Finding 7 — the specimen that survived, and the binding nobody ruled

`reviews/SEGMENTED-SCALE-SPECIMEN-2026-08-18-v3.html` is the **approved v1 grammar** carried forward
with the corrected thumbs and with the labels re-set on the **real type scale** — 12/14/16/16, i.e.
`font-7`/`font-6`/`font-5`. The 11px the earlier pages used was **off-scale**, which is a defect worth
recording separately from the switch story: it survived three builds because everyone was looking at
the corners.

⬛ **The binding itself is PROPOSED, not ruled.** Nothing says a segmented label takes those steps. It
is the natural opener for #203 and it is Dave's eye, not a gate's.

`-v2` and all three `SEGMENTED-SWITCH-COMPARE` pages are stamped SUPERSEDED / QUESTION-DISSOLVED and
kept — they are the record of the collision, and deleting them would delete the evidence that the
class exists.

## The cost, stated plainly

FILL at wrap-open **207,226 real** — past the ADVISORY stop line 150,929 by **56,297**, with the
200,000 working line crossed and the 256,000 wall binding (`s190-D2`). Seven work subs,
**666,600 tokens measured**. Effort band **L**.

★ The margin was not eaten by the ruled work. It was eaten by **building three times against a word
that a one-call search would have defined**. That sentence is the whole dossier.

## Resolved state, and what is still open

**Resolved:** `s202-D1` minted · `s202-D2` re-minted and its generator repaired and self-proving ·
`s202-D3` inscribed · the sidecar green · the local staleness repaired · the checkout ban in the
conductor runbook · the specimen rebuilt on the real scale.

**Open, and named:** the **type-scale label bindings** (proposed, Dave's) · the **glossary**
(floated, Dave's) · the **push and its CI read-back** (no push word was given — CI has not seen #202) ·
the **44 hit-area token still has no consumer gate**, now minted at the base tier as well, which
widens the number's reach without widening any fence · the **specimen asserts still have no
consumer**, and that absence now spans v3 too.
