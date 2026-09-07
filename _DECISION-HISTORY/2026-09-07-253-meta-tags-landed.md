# 2026-09-07 · #253 — the six fields land on 24 metas, nine words are ruled in, and eighteen calls are left standing

provenance: 253 · 2026-09-07
status: observed

*The WHY and HOW. The WHAT lives in `_LIVE-STATE.md`'s ⏱ LATEST DELTA #253, `GOOD-MORNING.md`'s
★ LATEST banner, `knowledge/_rulings.json` § `s253-D1` / `s253-D2` / `s253-D3`, the five filed lane
reports under `notes/_subreports/2026-09-07-253-*`, and the two review pages
`reviews/META-TAGS-A-2026-09-07-v1.html` and `-B-`. Both-way links: spine → this file (the ⏱
delta's WHY/HOW line); this file → the ledger entries named above. Predecessor:
`_DECISION-HISTORY/2026-09-07-252-roles-list-adopted-extensions-owed.md`, which briefed this wave
cold and named the premise probe this session did not have to redo.*

---

## 1. Why the wave ran exactly as written, and what that is evidence of

#252 ended at the advisory line with **zero lanes fired**, and spent its last clean tokens writing
`_HANDOFF-252-lanes-cold.md`: the premise-probe result, three lane bodies, the verifier pairing and
the wave order. #253 opened, planted the recall probe, and fired that document without re-thinking
it. The measurable consequence is the fill: **134,053 real over ~60 turns**, 16,876 under the stop
line, with three build lanes, two verifiers, a three-file research side-lane and two review pages
inside it — where #252 spent nearly the same room on none of that.

The mechanism is not discipline, it is **routing**. #252's carry ⑤ named the class — *an artefact
authored for a human is priced as a deliverable and paid for as context* — after the harness
re-echoed a 26 KB review page into the conductor three times. At #253 the two new review pages,
each ~50 KB, were authored **inside lanes** and never entered the conductor's window at all. Same
work, two pages larger, 16,000 tokens cheaper.

## 2. Why the schema lane fired first and alone

The premise probe had established that `meta.schema.json` is `additionalProperties: false` with
nine enforcers. So the eight terms had to exist in the schema **before** any meta carried one, or
every gate would go red on arrival. Lane C therefore ran alone, and its report is careful about
something a builder is usually careless with: it proved the corpus still validated as a
**BEFORE/AFTER pair** — validating 137 metas against `git show HEAD:knowledge/components/meta.schema.json`
and then against the new one — rather than asserting an after-only green. The single failing file
(`EXAMPLE-button.meta.json`) failed identically on both sides. Delta introduced: zero.

The same lane did the thing #244 taught: it **probed `derived` before claiming its mutation arm
bites**. On the live corpus at that moment, zero metas carried any of the new terms, so a mutation
touching only `shape` would have changed nothing the checks read and "passed" as a false negative.
Every arm therefore mutates a field a NAMED check reads, and every arm prints its own baseline
beside its verdict.

## 3. Why a resolver that goes RED on ten metas is the design

Lane A authored nine `answers` words that do not exist in `chart-intents.json`, and
`_validate_roles_resolve.py` duly returned `RESULT: FAIL (10)`. That red is `s251-D11` working:
**the store grows only by Dave's ruling, never by a lane.** The page proposed the words by number;
the metas carried them; the gate refused them; Dave ruled — *"confirm"*, then *"this sound good to
me"* — and `6a41915` added the nine words. The resolver then read **GREEN 24/24 with no edit to any
meta**.

That is worth writing down because the alternative shape is so much easier to reach for: have the
lane add the word it needs. It would have been green all day and nobody would ever have decided
anything.

## 4. The part that is NOT a ruling, and why it is recorded as such

The two pages carry **eighteen numbered calls** — eight on page A's §14, ten on page B. Dave's
answer, at the end of a long day, was *"Im tired today play this back to me please"* and then *"all
your pal"*.

Under `s251-D15` (Claude authors, Dave vetoes) that is **neither a strike nor an adoption**. The
honest record is that the calls stand **CLAUDE-AUTHORED and UNVETOED**, and this file is where that
is written, because it is exactly the kind of thing a later session would otherwise read back off a
banner as "adopted". The same applies to **chart-bar's priority 84 → 92** (page B call 2), which
the conductor enacted at `6a41915` on his own authority: unvetoed Claude call, not a ruling, no
`s253-D*` id. **The veto is open at #254**, which is what the next session's title names.

The three that most want his eye:

- **chart-bar's rung.** Lane A wrote 84 (below chart-line's 88), lane B's page proposes 92 (top of
  the role) and the conductor enacted 92. Both are unique, so the gate is silent either way — the
  ordering is not a gate question.
- **the two `shape` grammars.** Lane A wrote `categories-by-series`; lane B wrote
  `<x-dimension> × <mark>` throughout. The derived `instead-of` grade compares `shape` strings for
  **equality**, so the grammar is load-bearing, not stylistic: two grammars means chart-bar can
  never grade `equivalent` to a lane-B twin.
- **`runway-bar`.** The fifteenth `intent` carrier, in `headline-metric` in `roles.json`, not
  chart-named, so neither lane's brief reached it. It is the only `intent` carrier left bare.

## 5. What the verifiers were for, and the one they earned

Both verifiers re-derived every claim by script rather than reading the reports. V-A came back
`claims 18 · green 18 · red 0 · mismatches 0`; V-B `claims 221 · green 219 · red 0 · mismatches 2`.

**M1** was cosmetic and fixed the same day (35 double-escaped `&amp;middot;`, confined to page B
§14, `2962a4c`). **M2** is the one that earned the seat: the `when` field table's counts are a
**human reading** of the predicates, not the script-computed figure lane B's report presents them
as. An operator-token sweep yields 11 fields where the page says 12, because two predicates express
their condition as prose (`the category axis is ordered left-to-right`) rather than as a token. It
is a superset, not a contradiction — nothing missing, nothing invented — but it means **no parser
can reproduce the page's own table**, which is precisely the thing you would rely on if you were
about to close the `when` vocabulary. A verifier that only re-ran the greens would have missed it.

## 6. The near-loss, and why it is a brief defect

Lane A ran `git checkout -- knowledge/components/` to undo its own reformat. Lane B ran the same
command over the same directory shortly after. Each found its authored metas back at HEAD.

Nothing was permanently lost, and the reason is worth naming exactly: **both lanes authored from a
script**, so both could re-run. One hand-authored edit anywhere in that wave and the work would
have been gone with no receipt that it had ever existed.

The rule this buys is not "be careful": it is that **a brief which gives two concurrent lanes the
same directory must say so, and must forbid a directory-wide revert.** Nothing in the repo enforces
that today — it belongs in the parallel-conductor brief template, and it is carried as such.

## 7. Where the runner's red went

`s253-D2` (*"1. Step 8 fix. (a)"*) chose the harder of two options: help-gate the eighteen scratch
scripts rather than exclude `knowledge/_tmp/` from the help-gate check. The gate's scope was not
narrowed to make a red go away — the general form being that a gate you shrink to fit today's tree
is a gate that measures the tree instead of the rule.

Step 8 is now green and `_build_all.py` aborts at **step 18** instead, where `_gm_usage.py
--selftest` refuses: *"session #218 testifies DIFFERENTLY in notes/_GAUGE-LOG.md and
notes/_GAUGE-LOG.md"*. Re-measured at the wrap seat, the two testimonies are at
`notes/_GAUGE-LOG.md:2276` and `:2294`, and the second is labelled *(second wrap; …)*. So the
reader is not catching a falsification — it is refusing **a session that wrapped twice**, a state
its schema has no term for, and refusing is the right behaviour for a reader that cannot adjudicate.
The repair is a term, not a patch.

There is a hazard behind the red that matters more than the red: `_build_all.py` step 1 rewrites
`compliance/graph-index.json` wholesale and steps 8/9 rebuild the blocks it discards, so **any abort
after step 1 strips them** — 41 files, 75 insertions / 1,707 deletions, measured by lane C and
repaired with `git show HEAD:<path>` (never `git checkout`, which needs the index).

## 8. What is still open

The eighteen calls · R1, the masked-recovery calibration test `s253-D1` deferred · lane C's Q1
(`priority-unique` binds the metas, while `roles.json` keeps five `chart-panel` providers at 60 and
26 of 27 `input` providers with no priority at all) and Q3 (`intent` and `answers` are now two homes
for one fact, which ADR-0017 exists to prevent) · `shape` resolving against nothing · `when` parsed
by nothing · step 18 · and the observation that **no consumer reads any of the six fields yet**. The
validator is still the first and only reader — declared at birth rather than discovered later
[[instrument-without-a-consumer]].
