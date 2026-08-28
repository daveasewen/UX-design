# #222 — the release becomes the only lane, and a designer's broken machine ruled it

provenance: 854d1675-bd4d-4907-a839-58a59b17ef2b · 2026-08-28
status: observed

*Spine entry: `GOOD-MORNING.md` ★ LATEST #222 · `_LIVE-STATE.md` ⏱ LATEST delta #222.
Ledger: `knowledge/_rulings.json` § `s222-D1` · `s222-D2` · `s222-D3` — every id READ from the
store at this wrap, never retyped from a brief. Commits: `d4e69d0` · `36754e2` · `ba2c9f5` ·
`789f433`, all four pushed, subjects read back from `git log`. Filed reports:
`notes/_subreports/2026-08-28-222-mono-default-switch.md` ·
`notes/_subreports/2026-08-28-222-encoder-vendoring.md` ·
`notes/_subreports/2026-08-28-222-fallback-encoder.md` ·
`notes/_subreports/2026-08-28-222-route-a-report.md`. Deliverable:
`notes/_briefs/2026-08-28-222-release-plan-v1.md` (row `W-249`).*

---

## Why this session turned, and when

#222 opened as a design session. The first thing it owed Dave was one word about mono's gallery
default — a carry that had survived two wraps — and it got that word inside the opening
exchange. `s222-D1` closed `s220-D2`(3)'s expressly-open mono clause: square image, transparent
caption, console's colours, both modes, the grey caption ground kept as an edit-pass option.
That could have been the whole day.

It was not, because of something that happened on **Dave's own machine**, not ours. He opened
the pack we shipped at #220 in VS Code with Copilot — the first live session of the bridge the
record had been carrying as UNPROVEN for four wraps — and the chain inscription **refused**:
tiktoken's encoder data could not be fetched. This is the exact failure L4 predicted at #220 and
that `apollo-spider/FIRST-SESSION.md` itself warns about. The prediction had been on the record
as a priced risk; now it was a receipt, filed as his own row `W-244`.

The important thing about that moment is what it did to the ordering. A design lane and a
release lane had been running as peers. One designer's first hour, failing on the first
instrument he touched, is what made them not peers any more. His words were
*“I need this to work out of the box for the designers.”*

---

## Finding 1 — an out-of-the-box ruling grew a second ruling the same afternoon

`s222-D2` is the small version: **vendor the cl100k_base encoder data inside the pack**, resolve
it from the vendored location automatically, keep the honest measurement refusal for genuinely
broken installs. No download, no env var, no reachable blob host.

The lane that enacted it did the thing the record keeps asking for and the thing a brief cannot
do for itself: it **replayed its own premises first, and two of them died**. The brief scoped the
work to `apollo-spider/`; grepped twice, the stage contains no code that measures tokens at all.
The instrument that actually refused on Dave's machine is `memento-package/machinery/_capture_gate.py`'s
`measure_tokens` — the **frozen** package surface, behind Dave's `#64` boundary. The brief had put
the measurer in the wrong tree. That is the conductor's miss, named here rather than smoothed:
[[premise-ages-faster-than-rule]], again, and this time in a brief he wrote that morning.

Vendoring the data closes the *fetch* failure. It does not close the case where `import tiktoken`
fails outright — a pip-less machine, a locked-down laptop, a broken venv. That case is exactly
what a designer's first hour looks like when it goes badly. So the question came back to Dave as a
priced A/B, and he took **option B**: a pure-Python exact fallback encoder over the same vendored
data, live only when the import fails, with the engine named in every output — and, in the same
breath, the sequencing ruling that mattered more than either half:

> *“need to get this release fixed before we do any thing else, how about we do B, and you can
> just hand me a plan to get all the loose ends fixed in priority and dependancy order”*

That is `s222-D3`, and its clause **(2)** is the one that reorganised the board: the release
outranks every other lane until it is baked. The bento sitting, the mono dark chord, `W-217`'s
close and the mutation-arm call all parked behind it — by his word, not by ours.

---

## Finding 2 — why "exact" had to be measured, and what measuring it cost

A fallback encoder that is *nearly* right is worse than no fallback: every token figure in the
record silently forks by engine, and no gate could see it. So the claim to prove was not "it
works" but **"it is byte-identical to real tiktoken"**.

The equality gate drove **1,910 files · 69,483,685 chars · 21,813,749 tokens** through both
engines and found **zero divergent tokens**, then generated `_CHAIN.md` with each engine and
compared the artefacts: byte-identical, sha256 `fe70784b…` both ways. Mutation-driven in both
directions, so a gate that could not fail was not mistaken for a gate that passed.

Then the lane **stopped**. Wiring the fallback so that `_gen_chain.py` actually reaches it means
editing the frozen shim, and the frozen shim is Dave's `#64` boundary. It priced route (a) in its
own ⑤ Q1 and left it. This is the behaviour the record wants and rarely gets: a lane that finishes
its proof and refuses its last step, rather than one that reasons its way across a fence because
the fence was inconvenient at 90% done.

Route (a) then ran as its own lane, re-porting `measure_tokens` in the source and **both** frozen
shim copies — 33 lines each, byte-identical. It landed as **two commits on purpose**: `ba2c9f5`
carries the wire with the delta gate **red by construction** (the gate's own documented remedy
requires naming the commit that carries the change, and that sha does not exist until the commit
does), and `789f433` bumps `PORT_COMMIT_A` and both shim provenance lines to `ba2c9f5`, turning
the gate green. A red that is *predicted, explained and closed in the next commit* is a different
object from a red that is discovered; recording which one it was is the whole point.

---

## Finding 3 — four things nobody went looking for, and why they made the deliverable a plan

The release lanes kept turning up defects that were not on anyone's list:

- **The ship roster has silently drifted 55 → 56** against `s219-D9`'s ruled *"the pack ships 55
  gates"*. Two browser gates die with a raw traceback in a **third state** nobody had covered —
  playwright *imports* fine but its browser binaries are absent. #221's lane C fixed the
  can't-import case; this is its neighbour. The consequence is worse than the count: the release
  generator's probe classifies gates by what happens when it runs them, so **which gates ship
  depends on what happens to be installed on the machine that runs the probe.** A release should
  not have that property.
- **`RATIFY_ID` is pinned to `s219-D10`**, so `--release` ratification is a **no-op for v-next**:
  the machine would never ask Dave for his word, and would report itself ratified anyway.
- **The version number lives in FOUR homes, not two** — the build script, the manifest generator,
  the ledger row, and the ledger re-seed. #220 had already flagged two of them as an ADR-0017
  one-home violation; the other two were found here.
- **`_validate_package_delta.py`'s arm 2 has never audited the shim**, and a real re-port passed
  straight through it this session. A gate arm with no reachable bite is
  [[instrument-without-a-consumer]] in its most expensive form: it is *believed*.

Any one of these would have made a bake dishonest. Together they answer the question the day was
actually asking — not "can we bake?" but "what is between us and a bake we could defend?" So the
deliverable Dave asked for is what he got: `notes/_briefs/2026-08-28-222-release-plan-v1.md`, every
loose end in priority and dependency order, **with nothing in it decided.** It names five decisions
that are his, plus the roster count if it still moves after the gates are fixed, plus his fifteen
minutes in Copilot afterwards — the only real proof, and the one no gate can substitute for.

---

## What went wrong in the conductor's own seat

Recorded because the honesty clause is his own, and because a wrap that only reports the wins is
the wrap that stops being useful.

- **The ~190,000 armed advisory and the 200,000 working line were crossed INSIDE the sub waves and
  declared LATE, at the seam.** #221 had enacted the remedy for exactly this and got it right; #222
  regressed. A silent crossing is a failed declaration even when the platform window makes it safe.
- **The `s214-D6` recall probe was never planted at the opener.** Without it the conditional band
  cannot be green, so the band ran **degraded-declared** and mechanical-only after the seam. The
  probe's absence was noticed at the seam, not at the opener, which is the wrong end of the lane
  [[checkin-at-the-ends-cannot-catch-the-lane]].
- **Three stale premises of his own were named as they were found:** `W-206`'s licence Q1 had
  already been ruled at `s220-D3` (*"images are in licence, all good"*); the memory hook naming an
  "import-smoke gate" names no repo instrument; and the encoder brief put the measurer in the
  wrong tree (Finding 1).

FILL then crossed the **256,000 unqualified wall** — 266,423 at the declaring check-in — and the
session wrapped at the wall. The ~15M platform window made the whole day safe, and that is
**evidence for the pending `s208-D1` re-base, never a licence for it**; his boot-REDUCTION rider
still binds. boot read **75,422 real**, out of band by 17,519, the **twelfth consecutive**
out-of-band reading. Twelve is not drift.

---

## Resolved state, and what is still open

**Resolved:** mono's gallery default (`s222-D1`, enacted). The pack measures tokens out of the box
(`s222-D2`, enacted). The exact fallback engine exists, is proven equal, and is wired end to end
through both frozen shim copies (`s222-D3`(1) + route (a), enacted, delta gate green at `789f433`).

**Open, and his:** the five release-plan decisions · item 5's roster count under `s219-D9` · his
fifteen minutes in Copilot · the mono **dark chord**, still expressly open · `W-217`, expressly
still open and parked · the 97 open sitting calls and 25 candidates, untouched · the `s208-D1`
re-base · his end-of-day quota reading, owed in chat and not invented here.
