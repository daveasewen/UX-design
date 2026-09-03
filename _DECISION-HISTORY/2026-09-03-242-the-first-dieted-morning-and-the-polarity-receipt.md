# #242 — the first dieted morning: the boot read 70,710, the polarity receipt got built, and the boot turned out to be 89% not ours

```
provenance: 242 · 2026-09-03
status: observed
```

*Spine entry: `_LIVE-STATE.md` § `## ⏱ LATEST DELTA — 2026-09-03 … #242`. Ledger: `knowledge/_rulings.json`
§ `s242-D1` · `s242-D2`. Banner: `GOOD-MORNING.md` § ★ LATEST #242. Reports:
`notes/_subreports/2026-09-03-242-lane-P-polarity-receipt.md` (+ its P2 addendum) ·
`notes/_subreports/2026-09-03-242-V2-polarity-verifier.md` · `notes/_subreports/2026-09-03-242-lane-F-boot-offload.md` ·
`notes/_subreports/2026-09-03-242-wrap.md`. Both-way: each of those files names this dossier's session.*

*This is the WHY and the HOW. The WHAT — the ruling texts, the pins, the counts — lives in the ledger, the
spine and the reports, and is not restated here except where the narrative needs the number to make sense.*

---

## 1. The session was opened on a stale premise, and the premise was the conductor's own

The opener recommended "charts wave 3" as the product strand to pick up. It was wrong, and it was wrong in a
way nothing in the repo could catch: `knowledge/_lanes.json` still carries lane 2's `§C·1 strands (a)–(d)`
at `queued`, while waves 3–6 all LANDED at #209 / #210 / #218 and
`ITINERARY-STATUS-2026-08-25-v4.json` reads **121 GATED · 1 GAP**.

This is the **assertion-propagation class**, fourth recurrence. The shape is always the same: a queue line
asserts a state, the work that would falsify it lands somewhere else, and nothing joins the two. The
correction was made in chat before any lane launched, so the cost was one exchange rather than a wasted
window — but the general lesson is the one worth keeping: **a queue line must carry its landed receipt, or
no gate can see that it is finished.** That is now carry ⑨ to #243.

⛔ The step state itself was deliberately NOT edited at this wrap. `_lanes.json` is the conductor's surface
and a wrap sub correcting it would be a wrap ruling on someone else's document. It is carried instead.

## 2. `W-387` — the build that had been ruled and not built for two sessions

`s240-D3` was ruled at #240 and carried, unbuilt, through #241 (which built the *other* ruled-not-built lane).
At #242 it was launched as lane P with an adversarial verifier behind it, and the arc is worth recording
because the verifier earned its cost twice over.

**Lane P built the receipt.** One pointer per node: `sources` (a frozen R1 register row) **or** `$seed` (the
`knowledge/_rulings.json` id that created a node born after R1). A retired node keeps its row, carries
`retiredBy`, and drops out of everything derived. Three refusals were driven both ways — `R1-DANGLING`,
`S-SOURCE` (both receipts, or neither) and a new `R4-RETIRED-GENERATED`. The `SCHEMA_SHA256` pin moved in the
same change as the schema, which is the whole point of the two-file seam.

**The interesting half is what happened to the six false-red controls.** #239's lane F had found seven green
controls of which six flipped red, because their sources were fictional paths or unverifiable phrases. Under
`s240-D3` all seven now *have* a green form: two were already green, four go green the moment the node's
receipt is the ruling id instead of an oracle it invented, and one goes green once the thirty R1 rows are
RETIRED rather than DELETED. ⚠ **But the six literal shapes stay red on #239's Q3, on purpose: a node may not
name its own oracle.** That is RULING-SHAPED, it was put to Dave, and it is UNANSWERED — carry ① to #243.
The honest reading is not "six controls are fixed"; it is "six controls have a legal form, and whether the
literal shape should also pass is Dave's".

**V2 was the clause, and it found two real gaps.** `s240-D3`'s close condition included "V2 has run", so V2
was launched adversarially: 43 attacks, expect-red 29, caught 29, ESCAPED 4, crash 0. The four escapes are
the pre-existing UNRULED 241 · 243 · 245 · 301 — not one more, which is the finding that matters. Its two
gaps were:

1. a retired node still named in `polarity-status.json`, reachable through a **hardcoded literal at `:1208`**
   that the structural drop-out never saw;
2. the widening left **unfloored** — putting `sources` back in the schema's `required` would have silently
   killed `$seed` with no refusal anywhere.

Both were fixed by lane P2 in the same session, selftest **137 arms / 0 failures**. ★ The lesson is the one
`s238` already taught and this session paid for again: **brief the verifier in the same wave as the builder.**
A verifier launched a session later would have reported the six false-reds as regressions and found neither
gap while there was still budget to fix them.

**And a stale artefact was caught in passing.** #239's filed `_seam_block.sh` is a **pre-fix #238 block** —
V2 confirmed it. It is dated history and was not edited; lane P's re-extracted copy in its own assets is the
one to use, and the pointer is carry ⑤.

⚠ One word is doing the wrong job: P2's floor reuses **`SCHEMA-LOOSENED`** for what is actually a
*tightening*. Renaming a refusal is a vocabulary change and vocabulary is Dave's — carry ⑦.

## 3. The boot was decomposed, and the answer was unwelcome

Lane F built `knowledge/_boot_decompose.py` and drove it against the session's own transcript. The result:

| component | tape |
|---|---|
| `MEMORY.md` | 3,569 |
| skills block | 1,626 |
| MCP blocks | 1,398 |
| deferred tool names | 800 |
| agent list | 557 |
| **Σ ours** | **7,964 ≈ 11%** |
| harness remainder | **≈62,746 — ESTIMATED BY SUBTRACTION** |

⛔ **The remainder is not a measurement and is written as one nowhere.** It is a subtraction of a cl100k tape
figure from a real-token figure: the units are mixed by construction. It is corroborated independently in
REAL units — a lane seat carrying the identical roster boots at 39,819 / 40,118 real, n=2 — but that
corroboration is a floor, not a decomposition.

**Why this matters for the diet.** Everything Dave owns is about a ninth of his boot. JIT loading,
progressive disclosure and componentisation of our own files have a hard ceiling of roughly 4,600 tape of
realistic saving against a 70,710 boot. **The only lever with real leverage is not in the repo at all** — it
is Dave's plugin/MCP panel. That reframing is what made the two rulings below worth putting to him at all.

**⛔ And one of lane F's findings was FALSIFIED by Dave, in the same session.** The lane reported that
computer-use "came back on". Dave's own panel screenshot shows the toggle has been **OFF since #241**. The
block ships regardless, so it is **HARNESS**, and the +1,618 against #241 is harness drift, not a roster
regression. The lane report is dated history and was NOT edited; the correction lives here and in the #242
delta. ★ The class is worth naming: **a decomposition that reads the payload cannot tell you why the payload
is there.** Presence in the transcript proves shipping, not enablement.

## 4. Dave's three lines, and what was ruled from them

The conductor put three numbered questions. The answer, verbatim:

> *"1. computer use has been off since the last session, if you need to do something do it. 2. yes 3. yes"*

**Line 1 is a correction, not a ruling**, and it is what falsified lane F above.

**Line 3 became `s242-D1`.** `MEMORY.md` is a **progressive-disclosure stub**: the boot index carries the
⛔/★★★ tier plus one retrieval line; every other hook lives verbatim in a dated overflow file, looked up BY
NAME, never deleted. The `MEMORY-ARCHIVE` #49 line already said the rule for *moves*; this ruling says it for
the *index itself*. Enacted at the conductor's seat in the same session: **3,569 → 1,417 tape** (12,656 →
4,636 bytes, 31 lines), with the whole prior index verbatim at `hook-overflow-2026-09-03-242.md`.

**Line 2 became `s242-D2`.** The plugin-roster skills are pruned from the boot: `docx` · `pptx` · `xlsx` ·
`pdf` · `schedule` · `setup-cowork` · `import-memory` · `explain-usage` · the two `cowork-plugin-management`
skills are the candidates; `dave-voice` · `swiss-design-system` · `dream-pass` stay. Lane F measured the
block at 1,626 tape with ~900 movable.

⚠ **The sequencing is NOT ruled and is written as a recommendation inside the ruling body.** The conductor
recommends running the prune *after* #243's first reading, so that one variable moves per session and the
stub's effect on the boot is measurable alone. Folding a recommendation into a ruling's `ruled` text is
exactly how #241's `s241-D2` came to carry lane D's inflated headline — a ruling is write-once, so the
distinction has to be made *before* the write, not corrected afterwards.

## 5. The boot reading, and why it is stated once

**70,710 real** at the first turn — **710 OVER** the `s241-D1` ceiling of 70,000, on its very first morning.

Three things are true about that number and they are easy to conflate:

1. Against the **derived band** (`s240-D1`) it is **GREEN at 1.15σ**. The band is what grades drift.
2. Against the **ceiling** (`s241-D1`) it is **over by 710** — and the ceiling arm grades it only from
   **#243's** wrap, because both boot checks parse `notes/_GAUGE-LOG.md` and this session's reading does not
   reach that file until #243's own 2f roll.
3. The +1,618 against #241's 69,092 is **harness drift** (finding 3 above), not anything the diet did or
   failed to do.

⛔ Per `s241-D2` S5 the figure is stated **once**, in the 2f stratum. Repeating it in the banner and the delta
and the stamp is how a single reading becomes three apparent measurements.

**And #241's own reading finally graded.** The #241 wrap predicted `boot-drift` would go RED on 69,092 and
correctly refused to write a DECLARED line when the gate returned 0 fails — the reading was still in the GM
stratum. This wrap's 2f roll is what puts it in the log, and this is the wrap that writes the line.

## 6. What is still open, and why none of it was closed here

`s203-D1`'s CI read-back is now owed for **three** pushes (`a09a3ea`, `7f8801f`, and this one) and the route
must be capped at the run page plus one JS grep — the uncapped route cost ≈55K of conductor FILL at #239.
The four UNRULED escapes are untouched and `W-374` stays at ESCAPED 4. `BOOT_BAND_SIGMA` is Dave's. Diet
S2/S3/S4/S6 are Dave's. The 119-sweep re-run is owed. `_validate_wiring.py` is still red on #235's orphan.
Lane F's proposed mechanised `MEMORY.md` cap was **NOT built** — its consumer is unnamed, and an instrument
without a consumer is a zombie. The surface experiment (a Claude Code CLI boot floor) is floated and Dave's.

## Resolved state

`W-387` CLOSED with a receipt. `s242-D1` and `s242-D2` inscribed, store 333 → 335. The polarity receipt is
live, V2 has run, and the two gaps it found are fixed. The boot is decomposed and the honest conclusion is
that the repo-side levers are nearly exhausted. What is open is what Dave owns: the six-controls reading, the
sigma multiplier, the second diet wave, the vocabulary word, and when to pull the panel lever.
