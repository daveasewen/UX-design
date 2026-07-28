# Worker receipt — §A subdivision (`gm:A` is no longer one atom) — 2026-07-28

**Lane:** `worker-a-subdivision` · **Role: WORKER.** No git — the conductor (#33) reconciles and commits.
**Brief:** `notes/_briefs/2026-07-28-a-subdivision-worker-brief.md` (session #33, Opus conducting).
**Model:** Sonnet, as the brief permitted.
**Stamp:** 2026-07-28 (sandbox `date`).
**Context gauge at authoring: 🟢 GREEN — ~30% fill / ~70% remaining (ESTIMATE, ±15%).**
Band quoted from `knowledge/_RUNBOOK-context-gauge.md` § *"THE FLOOR IS MEASURED, NEVER ASSUMED"*
(🟢 GREEN = **> 55% remaining**), not from memory. Scrutiny indicator, not a quality score — a green
band means the numbers below were not produced hot; it does not mean they are right. **Every token
number in this receipt is `cl100k`**, with the ds-021 charged figure alongside where it matters
(×1.55, provisional — the charged multiplier is RULED-but-UNENACTED, so treat the charged column as
directional).

---

## ⛔ FORK TO DAVE — the build does NOT exit 0, and this lane cannot make it

**`python3 knowledge/_build_all.py` aborts at step 8/72**, on `_capture_gate.py --selftest`:

```
❌ selftest: M10: a fat §A/§C warned the CHAIN — the re-point did not take. After the GM-D7-am cut
   (#33) §A and §C are retrieval, not chain; if they still charge the chain the budget measures the
   old contract.
❌ selftest: CHAIN_BUDGET_TK = (4500, 6000), ruled (24000, 28000) (2026-07-27 M-set) — re-dialling
   is Dave's, and updating this pin is part of doing it
```

**This is not this lane's red, and this lane must not clear it.** `knowledge/_capture_gate.py` is on
the brief's **MUST NOT EDIT** list — the conductor holds the write-lock. The failure is the
conductor's own in-flight GM-D7-am work: `CHAIN_BUDGET_TK` was re-dialled at line 218 to
`(4500, 6000)` while the selftest pin at line 1362 still expects the ruled `(24000, 28000)`, and the
M10 chain re-point has not landed. The gate is telling the truth and telling it loudly — **it is
working**, and per its own wording the re-dial is Dave's, not an agent's.

⇒ **Dave / conductor: the chain budget needs re-dialling and its pin updating in the same deliberate
edit pair (the M10 pattern).** Until that happens no session can produce a green `_build_all.py`.
The brief's constraint 5 warned against becoming the third wrap to commit over a red build — this
receipt is that warning discharged, not ignored.

**What IS proven green for this lane** (run individually, foreground, this window):

| step | result |
|---|---|
| `_build_all.py` steps 1–7 | pass (the run reached step 8 before aborting) |
| `_gm_usage.py --selftest` | **OK — 31 bites** (was 17) |
| `_build_memento_index.py` | **OK — 271 records** written |
| `_build_memento_index.py --check` | **OK — current** (determinism holds) |
| `_build_memento_index.py --selftest` | **OK — 21 bites**, closed contracts refuse |
| `_memento_search.py --selftest` | **OK** — all 4 known-answer pins + both fetch bites |

I did **not** run the remaining ~64 steps: doing so needs either an edit to `_build_all.py` or a
driver that skips the fenced step, and neither is worth the risk with a conductor live in the tree.
**The build's own exit code is the contract, and it is currently 1.**

---

## The measurement — before and after

**Before.** `--fetch gm:A` returned the whole of §A:

| | cl100k tk | charged~ (×1.55) | bytes |
|---|---|---|---|
| `gm:A` (whole section) | **4,208** | ~6,522 | **15,817** |

⚠ The brief quoted **15,869 B**; I measure **15,817 B**. A 52-byte drift, consistent with the
conductor editing §A prose in the same wall-clock window. The token count (4,208) matches exactly.
Flagged rather than reconciled — I did not read the conductor's working tree to chase it.

**After.** §A is 11 records plus a router. Per-subsection, all `cl100k`:

| id | tk cl100k | charged~ | bytes |
|---|---|---|---|
| `gm:A:PRE` (framing + STANDING note) | 617 | 956 | 2,372 |
| `gm:A:WHAT` | 202 | 313 | 813 |
| `gm:A:THEMES` | 494 | 766 | 1,828 |
| `gm:A:WHERE` | 754 | 1,169 | 3,011 |
| `gm:A:CMD` | 66 | 102 | 266 |
| `gm:A:RULES` | 733 | 1,136 | 2,698 |
| `gm:A:AGENT` | 403 | 625 | 1,569 |
| `gm:A:DOCS` | 540 | 837 | 1,723 |
| `gm:A:PARALLEL` | 120 | 186 | 482 |
| `gm:A:RENDERS` | 150 | 232 | 523 |
| `gm:A:HOW` | 129 | 200 | 522 |
| **children total** | **4,208** | ~6,522 | 15,817 |
| `gm:A` (ROUTER) | 382 | 592 | 1,311 |

Children sum exactly to the old whole — the split loses nothing and duplicates nothing.

**Cost of the §A-shaped questions the brief named** (the door's stage-1 refs already hand a session
the child id, so the ordinary path is a direct child fetch — the router is only paid by someone
holding the legacy id):

| question | fetch | tk cl100k | charged~ | vs 4,208 before |
|---|---|---|---|---|
| "what's the build command" | `gm:A:CMD` | **66** | ~102 | **−98%** |
| "what are the four themes" | `gm:A:THEMES` | **494** | ~766 | **−88%** |
| "where does X live" | `gm:A:WHERE` | **754** | ~1,169 | **−82%** |
| legacy id, then the child | `gm:A` → `gm:A:WHERE` | **1,136** | ~1,761 | **−73%** |

**The worst case is 1,136 tk — router plus the largest child.** There is no path back to 4,208.

---

## The backward-compatibility decision (the brief asked which, and why)

**Chosen: `gm:A` survives as a ROUTER — the section heading plus a generated index of its 11
children with heads and line counts. 382 tk. Not the payload, not a dangling id.**

Rejected alternative: keep `gm:A` as the full text alongside the children. It satisfies "the id still
answers", but it leaves **the expensive path as the one a searcher naturally takes** — `gm:A` is the
memorable id, it ranks on §A-shaped queries, and fetching it costs the full 4,208 tk. That re-opens
the exact hole this lane exists to close, while looking closed. Also rejected: deleting `gm:A`. A
dangling id that used to work is a retrieval regression, and the brief is explicit that retrieval
regressions cost #32 two sessions.

A router is the only shape that answers the one question a coarse id can honestly answer — *which
part?* — at ~9% of the payload's price.

**Router quotes LINE COUNTS, not token counts, deliberately.** Token measurement depends on whether
`tiktoken` is importable; this index is **byte-compared by `--check`**. An environment-dependent
number inside a determinism-gated artefact would make the gate flap — the `__dirlock`/fresh-sandbox
class of failure. Line counts are deterministic, and the router labels them as **counts, not
measurements** (a count is not a measurement — ds-021's sibling).

---

## What changed, and where

**`knowledge/_gm_usage.py`** (MAY EDIT)

1. **`GM_A_SUBVOCAB`** — new, 11 entries, document order, line-START anchored regexes. Same dv-004
   shape as its siblings: only copy, order is the contract, `_gm_a_unknown` **REFUSES** an
   unregistered `## ` inside §A. The `unknown_check` is untouched and unweakened.
2. **`split_gm_a(lines, span)`** — subdivides the §A span, re-basing line numbers onto the whole
   file so records keep honest `file:line` provenance.
3. **`split_sections`** — one-line generalisation: the implicit leading span is now named by the
   **vocabulary's first entry** (`HDR` for GM/LS, `PRE` for §A) instead of a hardcoded `"HDR"`.
   Behaviour for GM_VOCAB and LS_VOCAB is byte-identical — both name theirs `HDR`.
4. **Selftest 17 → 31 bites.** The hardcoded `{17}` in the pass message is now `len(run)`, so the
   count cannot rot (it already had — it was a literal).

**`knowledge/_build_memento_index.py`** (MAY EDIT)

5. **`_emit_gm_a()`** — new; `parse_gm_ls` dispatches to it for `gm:A` only. Emits 11 child records
   (`kind="gm-section"`, so they bucket and rank in the door normally) plus the router. Refuses
   through the same fail-loud path as everything else.
6. **Selftest +6 bites.**

**No file outside the fence was touched.** `GOOD-MORNING.md`, `_capture_gate.py`, `_LIVE-STATE.md`
and both archives are unmodified. **No heading was needed in `GOOD-MORNING.md`** — the 11
subsections the brief listed all already exist, so the collision the brief warned about never arose.

---

## ★ Why `GM_A_SUBVOCAB` is separate from `GM_VOCAB`, and must stay separate

This was the one real judgment call, and it went the way the brief's own constraint 2 points.

`GM_VOCAB` is the **section-usage** vocabulary. `validate_usage_line` demands testimony for **every**
id in it, and `SECTION_USAGE_BLOCKING` is `True`. Adding 11 ids to `GM_VOCAB` would therefore have
required editing the `> **section-usage #N:**` line **inside `GOOD-MORNING.md`** — a file this lane
is fenced out of — and would have **failed the conductor's wrap** until that edit landed.

Retrieval granularity and testimony granularity are different questions at different costs.
Conflating them makes the cheap change (a finer door) pay the expensive change's price (a wider
testimony contract). So: **§A's usage testimony is still a single `A:<code>`. Unchanged by design,
not by omission.**

**Per constraint 2, noted and NOT fixed:** the section-usage instrument now reports at a coarser
grain than the door does. `A:R` cannot distinguish "read the build command" from "read the whole
orientation", and the 82–98% saving above is invisible to the usage dataset. Whether testimony
should follow the door to per-subsection is **#34's call**. If it does, the ids are already minted
and `GM_A_SUBVOCAB` is the only copy to point at.

---

## The bites — paired, positive-first, and PROVEN load-bearing

Constraint 4 is the one I spent the most care on, because #32's lesson is that a failure-only suite
survives a revert that deletes the whole comparison.

**Positive (in `_gm_usage.selftest`):** the fixture yields **every** registered subsection **in
document order**; `PRE` owns the heading and framing while `WHAT` starts at its own heading; the
spans **TILE** the section with no gap, no overlap, no lost line; offsets **re-base** onto the whole
file. Then the same assertions **against the real shipping `GOOD-MORNING.md`** — every subsection
present, every one non-empty, and **none of them the whole of §A** (the hole itself, asserted as an
absence that only a real split can satisfy).

**Positive (in `_build_memento_index.selftest`):** every registered subsection is its own record;
`gm:A` still resolves; `gm:A` **is** a router (says `ROUTER`, names all 11 children, < 3,000 B); the
largest child is a fraction of the old whole (**2,945 B vs 15,817 B**); children carry ascending
`GOOD-MORNING.md:<line>` provenance.

**Negative:** an unregistered `## ` subsection **refuses**; a removed registered heading **refuses**
and names it (`not found: WHERE`); reordered headings **refuse**; and the refusal is proven through
the **real parse path** on a mutated copy of the real file, asserting **no records were emitted**.

**Revert proof (run this window, not committed).** I restored the pre-lane behaviour in-process —
`_emit_gm_a` replaced by the old single-record emit — and re-ran the suite:

```
exit: 1
[FAIL] §A: every registered subsection is its own record
[FAIL] §A: `gm:A` is a ROUTER, not the payload — it names its children and is small
[FAIL] §A: the LARGEST child is a fraction of the old whole (0 B vs 15,817 B)
[FAIL] §A: unregistered subsection REFUSES the build (never indexes around a hole)
```

Four bites go red on a revert. `gm:A still resolves` correctly stays **green** — it is a
compatibility guard, not a feature guard, and it should survive a revert. **The positive bites are
load-bearing, demonstrated rather than asserted.**

---

## Found and NOT fixed

1. **⛔ `_build_all.py` is RED at step 8 on a fenced file** — the chain-budget pin pair above.
   Blocks the brief's own definition of done. **Dave's / the conductor's, in one deliberate edit pair.**
2. **The section-usage instrument now reports coarser than the door** — #34's, per constraint 2.
   Detail in the section above.
3. **Brief's byte figure drifted** — 15,869 vs my measured 15,817. Conductor's concurrent prose edits
   are the likely cause; the token count is unaffected. Worth a glance, not a chase.
4. **The `_gm_usage` selftest pass-count was a hardcoded literal** (`{17}`) that had already rotted
   relative to its own suite. Fixed in passing, since I was adding to that count. **Flagging the
   class, not just the instance:** a selftest that reports a number it does not compute is an
   instrument without a consumer, and there may be siblings — I did not sweep for them.
5. **`_gm_a_unknown` is deliberately fence-UNAWARE**, exactly like `_ls_unknown`: a `## ` at line
   start inside a code fence inside §A would refuse rather than be silently normalised away. There
   is none today (checked — the two fences in `## Where things live` and `## The one command that
   matters` contain no `## ` lines). If one ever appears, the build refuses loudly, which is the
   correct dv-004 behaviour and not a bug to be "fixed" with a fence-skipper.
6. **The router is keyword-rich** (it names all 11 child heads), so it may outrank individual
   children on broad §A queries. This is acceptable — it is cheap and it routes — but if a session
   ever reports being sent to the router when it wanted a child, that is the reason.

---

## For the conductor's reconcile

**Exactly two files changed**, both inside the fence:

- `knowledge/_gm_usage.py`
- `knowledge/_build_memento_index.py`

Plus the regenerated `knowledge/_memento-index.json` (271 records — **generated, never hand-edited**;
the index is rebuilt LAST at ritual step 2g, and `index_freshness_check` compares CONTENT, so a
rebuild after any further GM/LS prose edit is required before the wrap).

**Reconcile every path — no blind `git add -A` with a worker live.** This receipt is the third path.
