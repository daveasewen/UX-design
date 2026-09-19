# #287 lane W — the 256,000 "wall" wording swept from the ten live files

Lane W of Apollo #287. Job: on Dave's *"3. do it"* (`notes/_lanes/287/DAVE-RULINGS-2026-09-19.md`),
amend every live prose location that calls **256,000** a wall / hard stop / crash edge, using the
gauge's own corrected vocabulary: **256,000 is a tolerance line — a quality line, not a context wall
for this model (Fable 5.1 / Opus 5 in Cowork: 1M window + auto-compaction); 180,000 is the quality
line that binds.**

⛔ **NO NUMBER MOVED.** `BUDGET_HARD` is still `256_000`, `STOP_LINE_TK` still `180_000`. Only the
word next to each figure changed. **Nothing committed.**

---

## 1 · THE PROBE, RE-RUN FIRST — BEFORE / AFTER

Probe as lane G defined it: lines matching `256,000|256000|256_000|256K` that **also** carry
`hard` or `wall` (case-insensitive), over the ten live files.

| file | #286 lane G | **#287 measured at open** | **after the sweep** |
|---|---|---|---|
| `notes/_MEMENTO-DECISIONS.md` | 10 | **10** | **3** |
| `knowledge/_rulings.json` | 10 | **11** | **11** |
| `notes/_RULINGS.html` | 9 | **10** | **10** |
| `knowledge/_state.json` | 8 | **8** | **4** |
| `knowledge/_RUNBOOK-context-gauge.md` | 7 | **7** | **3** |
| `_LIVE-STATE.md` | 7 | **6** | **5** |
| `GOOD-MORNING.md` | 3 | **2** | **1** |
| `_CHAIN.md` | 2 | **2** | **1** |
| `dashboard/index.html` | 1 | **1** | **3** |
| `knowledge/_standing.md` | 1 (already correct) | **1** | **1** |
| **TOTAL** | **58** | **58** | **42** |

⚠ **THE TOTAL IS THE SAME 58 BUT THE DISTRIBUTION MOVED** since lane G counted it — lanes I and K
landed in between. `_rulings.json` +1 and `_RULINGS.html` +1 (lane I inscribed `s287-D1`, whose
`ruled` text names the 256,000 fix and is **already correct**); `_LIVE-STATE.md` −1 and
`GOOD-MORNING.md` −1 (the #286 wrap's own rewrite of those banners). So the starting set is 58, not
lane G's 58 line-for-line.

⚠ **`dashboard/index.html` went 1 → 3.** It is GENERATED from `knowledge/_state.json`; the three
hits are the *corrective clause itself* ("**not a context wall** for this model") now rendered in
three store rows. Every one is a negation. See §6.

---

## 2 · WHY 42 REMAIN, AND WHY THAT IS THE RIGHT NUMBER

The probe is a **word proximity** heuristic, not a claim detector. After the sweep **zero of the 42
asserts that 256,000 is a wall**. They fall in four classes:

**(a) THE CORRECTION'S OWN WORDS — 16.** The amended text says *"not a context wall"*, so it matches
the probe by construction. Removing the match would mean removing the fix.
`_RUNBOOK-context-gauge.md:89` · `_MEMENTO-DECISIONS.md:5239, 5385` · `_state.json:1802, 9792,
10620, 10706` · `dashboard/index.html:9255, 9256, 9295` · `_LIVE-STATE.md:121, 149, 151` ·
`_standing.md:19` (already correct at #286).

**(b) DAVE'S INSCRIBED RULING TEXT, ANNOTATED NOT REWRITTEN — 11**, all in `_rulings.json` and its
render. Per the job's rule 3 these are appended to, never re-worded. See §4.

**(c) THE CONSTANT'S OWN NAME — 2.** `BUDGET_HARD` contains the string `HARD` and **may not be
renamed** (it is the live constant in `knowledge/_gauge_tokens.py`). Any sentence naming the
constant beside its value matches the probe forever.
`_RUNBOOK-context-gauge.md:53` (the table row, relabelled **QUALITY-MAX** with the constant name in
parentheses) · `_MEMENTO-DECISIONS.md:5385`.

**(d) THE #286 RECORD OF THE OWED WORK, NOW MARKED SWEPT — 3.** These sentences *report* that 58
locations called it a wall; they do not themselves make the claim. Each now carries an appended
`⇒ ✅ SWEPT AT #287` clause rather than being deleted, because deleting them would erase what #286
declared. `_LIVE-STATE.md:14, 85` · `GOOD-MORNING.md:485` · `_CHAIN.md:83` (generated from
`_LIVE-STATE.md:85`).

**(e) ONE FALSE POSITIVE — 1.** `_MEMENTO-DECISIONS.md:3956` matches on `HARD_STOP`, the **retired
percentage-band constant** (`BAND_FLOOR/HARD_STOP/MARKED_MAX = 45/60/63` in `_capture_gate.py`) —
nothing to do with 256,000. It is `256K` and `HARD_STOP` sharing a long line. **No edit; it would be
a wrong one.**

⇒ **Genuine wall-assertions remaining in the ten files: 0**, other than the ruling texts of class
(b), which rule 3 forbids a lane from rewriting and which now carry the amendment clause.

---

## 3 · EVERY PATH TOUCHED, WITH `git diff --stat`

```
 GOOD-MORNING.md                     |    4 +-
 _CHAIN.md                           |   14 +-      (GENERATED — regenerated, not hand-edited)
 _LIVE-STATE.md                      |    9 +-
 dashboard/index.html                | 9590 +++++---  (GENERATED — regenerated, see §6)
 knowledge/_RUNBOOK-context-gauge.md |   24 +-
 knowledge/_memento-index.json       |   78 +-      (GENERATED — rebuilt, see §8)
 knowledge/_rulings.json             |   47 +-
 knowledge/_state.json               |   35 +-
 notes/_MEMENTO-DECISIONS.md         |   20 +-
 notes/_RULINGS.html                 |   67 +-      (GENERATED — re-rendered, not hand-edited)
 10 files changed, 6064 insertions(+), 3824 deletions(-)
```

Plus this subreport. ⛔ **Lanes I and K's uncommitted work is intact and untouched** —
`knowledge/_build_kg_explorer.py`, `knowledge/_kg_explorer.template.html`, `knowledge/_seam.py`,
`knowledge/_standing.md`, `notes/_KG-EXPLORER.html` still show only their modifications, and both
lane subreports are still present as untracked files.

### The substantive wording changes

| file | change |
|---|---|
| `_RUNBOOK-context-gauge.md:53` | table row **HARD → QUALITY-MAX** (constant name `BUDGET_HARD`, *historically labelled hard*), cell gains the #287 amendment sentence |
| `…:60` | *"Both HARD and WORKING are SOURCED"* → *"Both QUALITY-MAX (the row formerly labelled hard, constant `BUDGET_HARD`) and WORKING are SOURCED"* — **Dave's quote in that sentence is untouched** |
| `…:85` | *"256,000 stays the UNQUALIFIED **wall**"* → *"…UNQUALIFIED **tolerance line**"*; *"never widen past the wall"* → *"past that line"*; three-line amendment note added naming `s214-D2` as the inscriber |
| `…:372, 390` | *"256,000 hard"* → *"256,000 quality-max"* |
| `…:872` | seam verdict recap *"hard 256,000"* → *"quality-max 256,000"* |
| `…:926` | *"256,000 is the absolute hard stop"* → *"256,000 is the TOLERANCE LINE (a quality line, not a context wall for this model; 180,000 is the quality line that binds — wording amended #287)"*. ⚠ The formula term `wall − wrap` is **kept verbatim** and glossed — it is a named formula used elsewhere in the runbook, and renaming a formula term is not a wording fix |
| `_MEMENTO-DECISIONS.md` D24, D26, 2229, 3599, 3956-banner | *"hard 256,000"* / *"HARD 256,000"* / *"the HARD one"* → *"quality-max"* throughout |
| `…:5239` | *"256,000 is the hard stop"* → full tolerance-line clause |
| `…:5385` | `BUDGET_HARD` 256,000 gains *"(a quality/tolerance line, not a context wall for this model — wording amended #287)"* |
| `…:5568, 5748, 5835` | *"the 200,000 / 256,000 **walls**"* → *"…**lines**"* (3 occurrences, one phrase) |
| `GOOD-MORNING.md:17` | price banner *"hard 256,000 (SOURCED)"* → *"quality-max 256,000 (SOURCED)"* |
| `GOOD-MORNING.md:485` | #286 declared-skip entry gains the `⇒ ✅ SWEPT AT #287` clause (content preserved) |
| `_LIVE-STATE.md:14` | *"hard **256,000**"* → *"quality-max **256,000**"*; *"THE 256,000 HARD LINE WAS NOT BREACHED"* → *"THE 256,000 TOLERANCE LINE WAS NOT BREACHED"*; the 58-locations record gains the SWEPT clause |
| `_LIVE-STATE.md:85` | the 58-locations record gains the SWEPT clause |
| `_LIVE-STATE.md:961` | *"256,000 is the absolute hard stop"* → full tolerance-line clause |

---

## 4 · `knowledge/_rulings.json` — THE MECHANISM, EXACTLY

**There is no annotate/supersede/amend path to `ruled`.** `knowledge/_inscribe_ruling.py` offers
`--amend-evidence` only, and its own comment block (lines 280–295) states the fence:

> *"`says` is never reachable from here — a ruling's words are Dave's and an 'amend' that could
> reach them is a re-stamp wearing a tool's clothes."*

Its scope check (`amend_evidence`, ~line 360) **refuses any result that differs outside the target's
`evidence` array**, so the tool cannot be used for this at all.

⇒ **Fallback used, as the job specified:** a bracketed clause **appended** to each affected record's
text, applied as a **byte-level span swap carrying the same proof discipline as the tool**:

- the value is located by `json.dumps(old_value)` and must appear **exactly once** in the raw file;
- only that literal is replaced — **no `json.load → dump` reformat**, so every other byte is carried
  through by construction;
- after the swap the file is re-parsed and proven: same top-level keys, `_README` identical, same
  ruling count (**622**), and the **only** difference is the named field of the named record, whose
  new value is **exactly `old + CLAUSE`**.

The clause, verbatim:

```
 [wording amended #287 on Dave's 'do it': 256,000 is a tolerance/quality line, not a wall — s287 lane W]
```

**Six records annotated**, none re-worded:

| id | field | why it was in scope |
|---|---|---|
| `s214-D2` | `ruled` | *"256K STAYS THE UNQUALIFIED WALL"* |
| `s260-D2` | `ruled` | *"The 200,000 working wall and 256,000 hard wall are UNTOUCHED"* |
| `s271-D1` | `ruled` | *"200,000 working and 256,000 hard are NOT moved"* |
| `s272-D93` | `ruled` | *"256,000 stays the hard line"* |
| `s283-D1` | `ruled` | seam verdict recap *"hard 256,000"* |
| `s129-D1` | `watch` | *"the 200,000 / 256,000 walls did NOT move"* — a `watch` advisory, not Dave's inscribed words, but annotated the same way rather than rewritten |

⛔ **`says` WAS NOT TOUCHED — those are quotes.** Four `says` fields carry the wall wording and stay
exactly as inscribed: `gauge-band`, `s161-D1`, `s214-D2`, `s214-D4`. `s214-D2`'s `says` is the
sharpest (*"256,000 remains the hard wall, unqualified, band or no band"*) and is **Dave's own
sentence**; its `ruled` now carries the amendment beside it, which is the whole point of annotating
rather than editing.

⛔ **`s287-D1` was NOT amended** — lane I's ruling already states the correction (*"The 256,000
wording fix in `knowledge/_gauge_tokens.py` — that 256,000 is not a wall for this model in Cowork —
is HIS"*). It matches the probe as a negation.

**`notes/_RULINGS.html` was NOT hand-edited.** Re-rendered with `python3 knowledge/_render_rulings.py`:

```
wrote notes/_RULINGS.html  622 rulings  160 sessions  1112088 bytes  sha256 78acfda9…
--check: FRESH _RULINGS.html matches _rulings.json sha256 78acfda9…   exit 0
```

`s263-D10`'s wrap gate (stale-render) is therefore green.

---

## 5 · `knowledge/_state.json` — THE MECHANISM

**`knowledge/_state.py` has no row-text editing API.** It exposes `load/save/check/add/live/counts/
render_index/selftest` only; `add()` appends a new item and `save()` would re-serialize the whole
file. No CLI `main()` exists for editing.

⇒ Same discipline as §4: **raw span swap on the exact `json.dumps` of each field value**, proven by
re-parse — `_README` and `meta` byte-identical, item count unchanged at **706**, and exactly seven
rows differing in exactly the named fields.

| row | field | change |
|---|---|---|
| `items[126]` | `closes_when` | *"256K stays wall"* → *"256K stays the tolerance line"* |
| `items[126]` | `body` | *"with 256K the unqualified wall."* → *"…the unqualified tolerance line (wording amended #287: …not a context wall…)."* |
| `items[633]` | `closes_when` | *"at the 256,000 hard wall"* → *"at the 256,000 tolerance line (+note)"* |
| `items[666]` | `why` | *"published the 256,000 hard-line breach"* → *"…tolerance-line breach"* |
| `items[670]` | `why` | *"breach of the 256,000 hard line"* → *"…tolerance line"*; *"cut past the wall"* → *"cut past that line"* |
| `items[671]` | `why` | *"stay under the 256,000 hard line"* → *"…tolerance line"* |
| `items[673]`, `items[677]` | `closes_when` | *"what a session should do at the hard wall"* → *"…at the 256,000 tolerance line (+note)"* |

**Store gate:** `python3 knowledge/_state.py` → **exit 0**, no FAIL, counts unchanged
(`items 706 · live 599 · conditioned 692 · UNCONDITIONED 14`, frozen-set size 19). The four standing
⚠ advisories (declared debt, real-input coverage, project split, home pointers) read exactly as
before. ✅ **PASS.**

---

## 6 · `dashboard/index.html` — GENERATED, SO REGENERATED · ⚠ READ THIS ONE

The single location was **`items[126]`'s `closes_when` rendered verbatim** — the dashboard is built
by `knowledge/gen_dashboard.py` from `knowledge/_state.json`. So the source row was edited (§5) and
the dashboard **regenerated**, per rule 7. It was **not** hand-edited.

⚠ **THE DIFF IS 9,590 LINES AND MOST OF IT IS NOT MINE.** Measured, not assumed:

| what was compared | diff lines |
|---|---|
| committed `dashboard/index.html` **vs** a regen from the **UNCHANGED HEAD `_state.json`** | **11,617** |
| that HEAD-state regen **vs** my regen | **1,262** |

⇒ **The committed dashboard was ALREADY STALE against its own source before this lane touched it** —
regenerating from HEAD's store alone moves 11,617 lines. My seven row edits account for ~1,262 of
the delta, and even that is mostly **re-ranking cascade**: `gen_dashboard.py` scores rows by prose
scan / body length, so lengthening a `body` or `closes_when` shifts `score` and `rank` and reorders
the list. That is inherent to the generator, not a content change I chose.

⛔ **The committing lane should know the dashboard in the tree is now FRESH against the store for the
first time in some sessions, and that the bulk of its diff is inherited staleness, not #287 wording.**

---

## 7 · `_CHAIN.md` — GENERATED, SO REGENERATED · THE `--check` VERDICT

Never hand-edited. Sources `GOOD-MORNING.md` and `_LIVE-STATE.md` were edited (§3), then:

```
python3 knowledge/_gen_chain.py
  ✅ _CHAIN.md: 12,063 tiktoken cl100k_base · GM header+LATEST 4910 tk ·
     LS LATEST delta only (of 91 delta lines) 6299 tk ·
     FILE 12,063 = slice 11,209 + wrapper 854 · fixed point in 2 pass(es)     exit 0

python3 knowledge/_gen_chain.py --check
  ✅ _CHAIN.md is FRESH — byte-matches the live chain · (same figures)        exit 0
```

✅ **CHAIN `--check`: FRESH.** The old `_CHAIN.md:42` price-banner hit is gone (it rendered
`GOOD-MORNING.md:17`, now *quality-max*); `_CHAIN.md:83` remains as the SWEPT-annotated record of
`_LIVE-STATE.md:85`.

---

## 8 · GATE DELTAS — ONE NEW FAIL APPEARED AND WAS HEALED BY ITS OWN PRESCRIBED REMEDY

`python3 knowledge/_checkin.py --window 200000 --no-block`

| run | structural fails | note |
|---|---|---|
| inherited baseline (per the brief) | **6** | ceiling breach + 5 boot double-counts |
| after the sweep, **before** the index rebuild | **7** | ⚠ **+1 NEW** |
| after the index rebuild | **6** | ✅ **back to the inherited 6** |

**The new fail, verbatim:**

> ❌ FAIL retrieval index is STALE — it does not match GOOD-MORNING.md / _LIVE-STATE.md as they now
> stand, so `_memento_search.py` is serving a PREVIOUS session's record. Run
> `python3 knowledge/_build_memento_index.py` and stage the result (ritual step 2g). This is the #32
> defect — do not close over it.

**Caused by this lane** (editing the two chain sources), and healed by running exactly what the gate
named — `_build_memento_index.py`, **which is not on this lane's fenced list** (`gen_kg_rules.py`,
`land_rests_on.py`, `gen_kg_icons.py`, `_build_all.py`) and is the ritual's own step 2g:

```
memento index: 2245 records → knowledge/_memento-index.json
(brief:205, carries-section:64, component-meta:139, context-node:222, dream:12, gauge-block:268,
 gm-archive-section:256, gm-section:20, lane:4, ledger-section:86, ls-archive-section:521,
 ls-section:11, pattern-node:380, runbook-section:57)
```

**The 6 that remain are exactly the inherited set**, unchanged in body: boot-drift **CEILING BREACH**
(`BOOT_CEILING_TK` 70,000, 7 post-diet readings over it — `s240-D2`/`s241-D1` shrink-only, Dave's
alone) and the five `notes/_GAUGE-LOG.md` boot double-counts (#243 ×5, #264, #272, #273, #274 ×2
each). Plus the 2 standing **heals-at-wrap** items (the `_LIVE-STATE.md` / `GOOD-MORNING.md`
date-zone refreshes, ritual steps 1/2) — **pre-existing, not mine**.

### ⚠ NO CHAIN-FRESH OR SIZE-STAMP GATE COMPLAINED — AND NOTHING WAS RE-STAMPED

Per rule 9: the chain-fresh gate is **green** (§7) and **no size-stamp gate fired**. The only
size-shaped output is the standing **advisory** warn *"GOOD-MORNING.md compactable: 29,072 tape /
~45,643 bill … ADVISORY, never a trim order"*, which is not a fail. ⛔ **No size stamp was re-written
by this lane.**

### Two NEW warns, both attributable to this lane, both advisory

> ⚠ **REGEN SERIAL (advisory):** this wave regenerated `_gm_usage.py` (step 17) … `_gen_chain.py`
> (step 118), but 31 serial member(s) INSIDE …
>
> ⚠ **REGEN SERIAL (advisory):** the serial ran OUT OF ORDER — `_gm_usage.py` was regenerated AFTER
> `gen_dashboard.py`, which follows it in …

⇒ This lane ran `gen_dashboard.py`, `_render_rulings.py`, `_gen_chain.py` and
`_build_memento_index.py` **individually**, not through the serial. **The serial's own runner is
`_build_all.py`, which this lane is fenced from**, so the ordering warn cannot be cleared here.
**Named, not fixed — it is the committing lane's to note or a later wave's to clear.** The warn total
is 29, and the prior logged run at this seat also read 29.

---

## 9 · REFUSED / NOT DONE, EACH WITH ITS REASON

1. ⛔ **`_rulings.json` `says` fields — 4 locations NOT edited.** Dave's quotes; rule 3.
2. ⛔ **`_rulings.json` / `_RULINGS.html` `ruled` texts NOT re-worded** — annotated only, because
   `_inscribe_ruling.py` has no `ruled` path and the fallback the job specified is an appended
   clause. **The original sentences still read as Dave inscribed them.**
3. ⛔ **`_MEMENTO-DECISIONS.md:3956` NOT edited** — false positive on the retired `HARD_STOP` 45/60/63
   percentage constant (§2e). Editing it would have introduced an error.
4. ⛔ **The formula term `wall − wrap` kept verbatim** in `_RUNBOOK-context-gauge.md:926`,
   `_MEMENTO-DECISIONS.md:5239` and `_LIVE-STATE.md:961` — a named formula, glossed in place rather
   than renamed.
5. ⛔ **`BUDGET_HARD` NOT renamed.** It is the live constant; renaming it is a code change, not a
   wording fix, and would move far more than a word.
6. ⛔ **The append-only testimony NOT touched** — `notes/_GAUGE-LOG.md`, `_DECISION-HISTORY/`,
   `notes/_subreports/`, `_CARRIES.md`, `_GM-ARCHIVE.md`, `_LIVE-STATE-ARCHIVE.md`,
   `notes/_briefs/`, `notes/_lanes/2xx/`, `outputs/_wrap*`, `knowledge/_tmp/wrap*`. Rule 6.
   (`knowledge/_memento-index.json` is the **generated index** of those files, not testimony; it was
   rebuilt, not edited — §8.)
7. ⛔ **`knowledge/_seam.py`'s 4 printed "HARD LINE BREACHED" locations NOT touched** — lane G left
   them owed to whichever lane owns `_seam.py`, the file is modified in the tree by another lane
   this session, and it is outside the ten-file prose list. **Still the one remaining printed wall
   wording in live code.**
8. ⛔ **NOTHING COMMITTED.** No `git add`, no commit, no push.

---

## FILES TOUCHED

- `knowledge/_RUNBOOK-context-gauge.md` — wording (7 sites)
- `notes/_MEMENTO-DECISIONS.md` — wording (9 sites)
- `knowledge/_rulings.json` — 6 records annotated by appended clause (5 `ruled`, 1 `watch`)
- `notes/_RULINGS.html` — **regenerated** by `_render_rulings.py`
- `knowledge/_state.json` — 7 rows, 9 field edits
- `dashboard/index.html` — **regenerated** by `gen_dashboard.py` (see §6)
- `_LIVE-STATE.md` — wording (5 sites)
- `GOOD-MORNING.md` — wording (2 sites)
- `_CHAIN.md` — **regenerated** by `_gen_chain.py`, `--check` FRESH
- `knowledge/_memento-index.json` — **rebuilt** by `_build_memento_index.py` to heal the fail this
  lane caused
- `notes/_subreports/2026-09-19-287-W-wall-wording-swept.md` — this file
