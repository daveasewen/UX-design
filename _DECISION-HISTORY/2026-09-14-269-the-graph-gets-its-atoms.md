# #269 — the graph gets its atoms

provenance: 269 · 2026-09-14
status: observed

*The session NARRATIVE DOSSIER (capture ritual step 1b) — the WHY and the HOW. The WHAT lives in
the terse records: `knowledge/_rulings.json` `s269-D1`…`s269-D10`, `GOOD-MORNING.md`'s ★ LATEST
#269 banner, `_LIVE-STATE.md`'s ⏱ LATEST DELTA #269, and `_HANDOFF-120-the-graph-gets-its-atoms.md`,
which the conductor wrote at FILL 374,074 real BEFORE this ritual ran. Both-way links: the spine
entry is the ⏱ LATEST DELTA #269; the ledger entries are the ten `s269-D*` rows.*

⚠ **Written by the DELEGATED WRAP SUB, not by the conductor.** This seat did not see the session's
reasoning happen; it reconstructed the arc from the handoff, the ten commits `f02fe4c..41dbdeb`,
the four lane JSONs under `notes/_lanes/269/kg-gaps/` and `DAVE-RULINGS-2026-09-14.md`. Where the
arc is inferred rather than witnessed, it says so. That is an ADR-0016 `CLAIMED`, not a lie of
omission.

---

## 1. The problem nobody had named: the record could not tell his words from a paraphrase

The session opened on an n-gram research question and found a defect underneath it. Apollo's whole
discipline is *quote Dave verbatim, never re-word* — it is written into the capture ritual, into
`s183-D1`, into `s188-D2`, into the carry contract. **Nothing checked it.** A sentence presented as
Dave's had exactly one gate: whoever typed it remembering correctly.

The instrument built in answer is small and read-only. `knowledge/_quote_gate.py` takes a phrase,
looks it up verbatim over the Memento index, and answers either FOUND with `id·file:line` or a
miss with the nearest real phrase, the longest common run, and a did-you-mean. `_near_dupes.py`
scores 8-word shingle Jaccard across the corpus. `_ngram.py` is the shared library under both.
Fourteen bites, eleven bites, and a runbook section in `_RUNBOOK-consult.md`.

**The reason it earns its place is that it bit on day one, twice.** The run-of-show page said
*"research"* where Dave had written *"resaech"*, and it said *"designer"* where his phrase was
*"an operator not a platform owner"*. Neither would ever have been caught by reading — the first
looks like a typo fixed, the second like a synonym. One is; one is not.

That distinction became a ruling in its own right. `s269-D7`, on his sentence *"obviously this
should be corrected, I have very dyslexic fingers as well as my very bad spelling brain"*: a
corrected spelling is still his words; a changed word or a changed digit is not. The gate
implements exactly that line — `"six"` ≠ `"6"` — and punctuation and markdown marks count as
transcription rather than a miss.

**The dead end that was refused rather than taken:** the obvious way to make quote lookup better
is to change the ranking in `_search_core.py`. That file and `_memento_search.py` are pinned
byte-identical to the memento package by `_validate_package_delta.py`, so any ranking change is a
RELEASE, not an edit. The session left the pack untouched and parked the idea (`P-269-1`,
`P-269-2`) instead of paying a release price it had not been given.

## 2. "Parked" stopped being a figure of speech

Dave asked for it directly: *"store them for future sake, can they be triggered, or can we have a
hook so they don't get missed at the appropriate time"*, and the next day *"okay we need this
recorded with tripwires"*.

The failure mode being closed is the one this repo has measured repeatedly: a deferred item
written into a banner or a residual is **carried**, not **scheduled**, and a carry is read by
whoever happens to look. `knowledge/_parked.json` holds nine rows; `knowledge/_parked.py` is the
door; six events can fire a row — release-cut, kg-edge-gen, dream-pass, memento-cut, token-report,
guidelines-ingest — through five hooks that **print only**, sit inside `try/except`, and never
return a verdict.

**The care that makes it honest rather than clever, and it is worth naming:** the hooks cannot
fail a build. A tripwire that can turn a gate red is a gate, and gates are ruled, not invented at a
wrap. And `P-269-8`'s `at_commit` is pinned to `45a62c3` so that its own fix cannot trip it — the
self-reference bug caught before it shipped rather than after.

It was **driven**, not asserted: a v1.0.14 manifest fires three of the nine.

## 3. Turning the same habit on the graph, and finding thirteen families at zero

The third act is the one Dave acted on. Four Opus lanes — A-inventory, B-component-edges,
C-external, V-verify — read the knowledge graph and asked what is *not* in it. **All four were
read-only by construction**, and `gen_kg_edges.py` was fenced out on the #265 ruling.

The graph today is 890 nodes and 1,267 edges across 16 types, plus the governance and WCAG
families at 1,941 / 3,605. **Thirteen entity families sit at zero**: tokens 932 · icons 666 ·
tagged rules 470 · untagged docs 25 of 381 headings · principles 145 · polarities 30 · logos 12 ·
photos 251 · fonts 111 · roles 12 · DESK fields · synonyms 69 · personas 0.

Three findings inside that inventory are worth more than the count:

1. **`knowledge/_rules-index.json` is NOT orphaned.** It looked like a dead artefact. It is
   consumed by `_build_consult_index.py:53` and `_build_instrument_fit.py:60`. The lane checked
   before it wrote "unused" — which is the only reason the proposal does not carry a false claim
   about a live file.
2. **`conformsTo` is a near-duplicate of `appliesTo`** — 826 of 834 overlap. That is a vocabulary
   problem, not a data problem, and the proposal says so without acting on it.
3. **The photography KG-NOTE is stale**: it says 12 derivatives, the folder holds 251. Named, not
   fixed, because repairing canon was outside a proposal lane's fence.

**The verifier lane is why the page is trustworthy.** V re-took 65 counts: 53 came back exact and
**12 were corrected on the page before Dave ever saw it**. Of 133 evidence lines, none was
fabricated. A lane had said `usesIcon` had 4; it has 19. The correction is visible in the record
rather than smoothed out of it — which is the whole argument for running a verifier in the same
wave as the lanes it checks.

## 4. What Dave ruled, and the line the wrap had to hold

He accepted the six recommendations in a single sentence:

> *"I think your recommendations for the 6 look good, personas and JTBD is interesting but we
> don't have any we can rely on, could we create placeholders, or create our own on the back of
> some research? I don't want to loose the idea. We will be adding more, for example I'm trying
> to get hold of our CX principles."*

**That sentence is `says` in all six of `s269-D1`…`s269-D6`, uncorrected**, because he accepted
the six in one breath and splitting it into six different quotes would invent six sentences he
never wrote. The six *readings* — the order 1–5, the `ux:` prefix, tokens at TIER grain, the
photography node as the manifest row, metas citing the six A-grade laws first, content-standard
and lifecycle-status as new kinds — are the **conductor's reading**, and every one of those `ruled`
fields opens by saying so.

★ **This is the session's own instrument turned on the session's own record.** The whole point of
`_quote_gate.py` is that a paraphrase presented as his words is a defect; a wrap that inscribed the
numbered readings as if he had typed them would have committed exactly that defect in the ledger,
hours after building the door designed to catch it.

He did not drop persona and JTBD, and the ruling records that too: `P-269-9`, firing when
`knowledge/guidelines` moves — which is when the CX principles he is chasing arrive.

Four more rulings inscribe the other words he gave this session: `s269-D7` the spelling rule,
`s269-D8` the audience phrase, `s269-D9` the n-gram go-ahead (*"as long as it's safe and you test
the usual dependancies and externalities lets go for it"*), `s269-D10` the tripwire word.

## 5. The thing that is open, and the reason it is written as ASKED

The conductor proposed a **compose-time door**: a third door on the retrieval spine that takes a
task in and returns a closed context slice — the components providing the roles, the BLOCKING
rules first, the type composites, the icons, the tokens, the anti-neighbours, and the ruling behind
each — so the generate skill's step 1 becomes *"ask the graph"* instead of *"read the metas"*, and
the gates check the page against the same slice.

**His last words on it were the heat question, not a yes.**

It is carried as ASKED, in the handoff, in the banner, in the delta and in `_CARRIES.md` § residual
→ #270 item ②, and #270 is instructed to get the one word before drafting a line of it. The reason
for the repetition is not emphasis: a proposal that appears once, in a rolling home, is how a
proposal becomes a ruling by accident.

## 6. Resolved state, and what is still open

**Resolved:** three read-only n-gram doors exist and are bitten. The parked register exists and is
driven. The graph-engineering table from 2026-08-05 is audited row by row and is no longer an open
list. The proposal exists, verified. Ten rulings are inscribed, 453 → 463.

**Open, and all of it Dave's:** the compose-time door (one word). The twelve candidate edge types —
a new type is a vocabulary change under #75. The `conformsTo`/`appliesTo` near-duplicate. The stale
photo KG-NOTE and the missing font manifest. Every #119 open, untouched: the ask, the title edges,
the v1.0.6 hand-over date, dream pass 12's four proposals, the pre-bake real-page drive as a step,
the fly-through direction, the v1.0.13 hand-over date, the six-month comparator. And three blocking
gate refusals carried in the `#243` form — the boot-drift ceiling breach, and the #243 and #264
boot double-counts, left unrepaired because `notes/_GAUGE-LOG.md` is append-only and both blocks
are another session's testimony.

**The gauge is the session's own warning, and he wrote it himself:** FILL 397,011 real at the wrap
seat, boot 78,777, the largest breach on the board. *"374,074 is quite a bust, this makes me
nervous, typically this is where things get squirrely."* The handoff was written before the ritual
ran because of that sentence — which is, in the end, the most transferable thing in this session:
**at a bad gauge reading, write the record FIRST and delegate the ritual, rather than trusting a
ritual run at the far edge of a window.**
