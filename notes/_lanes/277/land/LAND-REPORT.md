# Lane LL — LAND — #277, 2026-09-16 · s277-D1 / s277-D2 / s277-D3 ENACTED

Dave ratified on the review page (export `2026-09-16T07:20:00.078Z`, **a / a / b**, no notes) and said
**"go"** on the read-back; the rulings were inscribed at `407f20b`. Lane LA proposed at `e19fbce`;
lane FV graded at `7102f9d` — **63 GREEN / 18 AMBER / 6 RED, verdict LAND WITH 6 REPLACEMENTS**.
This lane applied the six, rebuilt, re-gated, and spliced the four metas into `knowledge/`.

**ONE commit.** Counts land unmoved: **24 / 25 / 27 / 11 = 87**.

---

## STEP 1 — the six replacements

Applied to `notes/_lanes/277/land/_whys.py` by exact-string replacement, each asserted to match
**exactly once** before it was made. No other sentence was touched.

| # | edge | what changed | new anchor(s) added |
|---:|---|---|---|
| **1** | `chart-line` → `dv-line-001` | "this meta **is** the line side of the asymmetry" → **records only the mandatory side's absence**; names the engine's zero clamp and `dv-render-line.js`'s CORE REQUEST against this very rule — a rule the line is built to honour and **does not yet enact** | `"script": "knowledge/canon/dv-render.js"` (chart-line **L249**) added to the existing `antiPatterns` + `!data-domain-min` |
| **10** | `chart-line` → `dv-001` | dropped the borrowed DV-D02 viewBox-pin mechanism (the same defect the conductor RED'd on `dv-line-005`) → **no author picks the y-range**: the engine derives the domain, widens to whole steps, floors at zero, and REWRITES the table rows from the same spec | anchor list **replaced**: `"script": "knowledge/canon/dv-render.js"` (**L249**) · `REWRITES those same rows from the spec` (**L256**) |
| **15** | `chart-line` → `dv-007` | "**refuses** to do the second" (the inverse of the rule, on its face) → "**keeps** the second by pinning the viewBox 1:1 — TEXT NEVER SCALES with the geometry" | `TEXT NEVER SCALES (viewBox pinned 1:1)` (**L100**) added |
| **18** | `chart-line` → `dv-010` | "edge-flips **rather than covering the plot**" (a real word given a meaning it does not have) → the popover is the **only** overlay and is **transient**; the edge-flip keeps it **inside the viewport** | anchor widened to the full `motion.hover` clause `pointer + keyboard focus, edge-flips, role=status; replaces native <title>. Values == table.` (**L95**) |
| **28** | `chart-pie` → `dv-pie-005` | false attribution of cause — the antiPattern's stated reason is **type26-013**, not readability → the meta answers by **never labelling inside at all**, with the on-fill ban credited to the file's own reason | unchanged (`never sit ON the fills` **L40** · `White letters on segment fills (type26-013` **L72**) |
| **63** | `chart-bar` → `dv-004` | named an **identity** channel (the in-segment letter key, which is dv-011's and #70's) for a **separation** rule → the 2px is **cut in geometry** by the partial the meta names (`dv-render-bar`: a gap between lanes and off the block below every stacked join, a gap and never a painted stroke). **Also removes the #63-vs-#76 contradiction** FV found on this meta | anchor list **replaced**: `"partial": ["dv-behaviour", "dv-render", "dv-render-bar"]` (**L90**) · `geometry is generation-time` (**L20**) · `"name": "stacked column"` (**L29**) |

All six new anchors were grepped in the LIVE metas **before** the edit; all present (the one negative
anchor `!data-domain-min` re-checked at **0 hits** in `chart-line.meta.json`).

`git diff --numstat notes/_lanes/277/land/_whys.py` → **`11  11`** — six `$why` lines + five anchor
lines (row #28's anchors did not change).

### rebuild

```
  chart-line    9 file + 15 family = 24  | span 7587 chars inserted at byte 10250 | R1 reconstruct OK · R2 parses OK · R3 anchors OK
  chart-pie    10 file + 15 family = 25  | span 7481 chars inserted at byte  9980 | R1 reconstruct OK · R2 parses OK · R3 anchors OK
  chart-bar    10 file + 17 family = 27  | span 8015 chars inserted at byte 11725 | R1 reconstruct OK · R2 parses OK · R3 anchors OK
  chart-donut  11 file +  0 family = 11  | span 3835 chars inserted at byte 10424 | R1 reconstruct OK · R2 parses OK · R3 anchors OK
  TOTAL 87 obeys edges, every one with an authored $why grounded in the live file.
```

`R3 GROUNDED` is the one that matters and it is what refuses a sentence naming a mechanism the file
does not carry. It passed on all four **after** the replacements, which is the whole point of the
replacements having been made in `_whys.py` and not in the built files.

---

## STEP 2 — the diff against lane LA's proposals · exactly six `$why` strings

```
git diff --numstat notes/_lanes/277/land/proposed-metas/
  1   1   proposed-metas/chart-bar.meta.json
  4   4   proposed-metas/chart-line.meta.json
  1   1   proposed-metas/chart-pie.meta.json
                    (chart-donut.meta.json — no diff at all)
```

Object-level, proposal-old vs proposal-new, `obeys` popped:

```
  chart-line   rest-identical: True · refs identical: True · $why changed: 4 ['rule:dv-line-001', 'rule:dv-001', 'rule:dv-007', 'rule:dv-010']
  chart-pie    rest-identical: True · refs identical: True · $why changed: 1 ['rule:dv-pie-005']
  chart-bar    rest-identical: True · refs identical: True · $why changed: 1 ['rule:dv-004']
  chart-donut  rest-identical: True · refs identical: True · $why changed: 0 []
```

**Six, and only six.** No `ref` moved, no entry was added or dropped, nothing outside `edges.obeys`
changed. `WHYS.md` regenerated from the same data (`6  6`), so the sentence graded and the sentence
that landed are still one string.

---

## STEP 3 — the splice into `knowledge/` · **INSERT-ONLY, per file**

Each proposal IS the live file plus one inserted `edges.obeys` span, so copying it over the live meta
must show **0 deletions**. It does:

```
git diff --numstat knowledge/components/
  110   0   knowledge/components/chart-bar.meta.json
   46   0   knowledge/components/chart-donut.meta.json
   98   0   knowledge/components/chart-line.meta.json
  102   0   knowledge/components/chart-pie.meta.json
```

**0 deletions on all four.** Not a re-dump: the file was never `json.dump`ed — `_splice.py` inserts a
span of text into the live bytes and proves it by reconstruction (R1), so every byte that was there
before is still there, in its original place, in its original escape style.

Corpus effect: `edges.obeys` **81 → 168** entries, **6 → 10** metas.

---

## STEP 4 — gates

| gate | exact output line |
|---|---|
| `_gates.py` G1 schema × 4 | `PASS G1 schema chart-line.meta.json validates against meta.schema.json (24 obeys, $why required and present on every one)` — and the same for `chart-pie` (25), `chart-bar` (27), `chart-donut` (11) |
| `_gates.py` G2 refs × 4 | `PASS G2 refs chart-{line,pie,bar,donut}: every `rule:` id resolves in _rules-index.json` |
| `_gates.py` G3 counts | `PASS G3 counts: chart-line 9+15=24 · chart-pie 10+15=25 · chart-bar 10+17=27 · chart-donut 11+0=11 — TOTAL 87 (29 + 47 + 11)` |
| `_gates.py` G4 simulated tree | `PASS G4 _validate_kg.py on the simulated tree (4 proposals swapped in): rc=0 — … _validate_kg.py: OK …` |
| `_gates.py` G4 restore | `PASS G4 restore: the four live metas byte-compare EQUAL to the bytes held before the swap` |
| `_gates.py` verdict | **`ALL GATES PASS`** |
| `python3 knowledge/_validate_kg.py` | `_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.` — `metas checked: 139` · `ref:null + $note: 90` · `82 ruled verdicts asserted present`, **rc 0** |
| `python3 knowledge/_validate_kg.py --selftest` | `[OK] selftest never touched the live corpus` / `selftest OK.` |
| `python3 knowledge/_validate_compose.py` | `- ✅ 7 screen(s), every <title> present + unique` / **`RESULT: PASS ✅`** |
| `python3 knowledge/_validate_roles_resolve.py` | **`RESULT: FAIL (6)`** — **INHERITED, unchanged**: all six are `data-grid: FAIL [with-resolves] — every `with` entry needs a `slug` string (s251-D6 …)`, exactly as #276's land recorded them. `data-grid.meta.json` is not in this commit. |
| `python3 knowledge/_validate_lane_ownership.py` (staged) | `LANE OWNERSHIP: OK — no staged path under another session's lane (this is #277).` exit 0 |
| `python3 knowledge/_validate_lane_ownership.py --selftest` | **`selftest: 2/3`** — **INHERITED, declared**: the failing bite is `FAIL — session parsed out of the _CHAIN.md line shape`; the other two pass. Neither `_validate_lane_ownership.py` nor `notes/_CHAIN.md` is in this commit, and nothing this lane wrote can reach that bite. #276 recorded `3/3`; the regression is **not this lane's** and is **left for the conductor** (it is the exact shape P-276-1 was parked to catch). |
| chromium drive of the explorer | **`DRIVE PASS`** — 14/14, **0 console errors / warnings / page errors** |

`_validate_kg.py` needed **no change** this time. #276's land taught it `rule:` / `ux:` refs and
per-edge-type schema properties, and the 87 new edges are the same shape (`{ref, $why}`, `rule:` only),
so all 168 resolve on the first run.

### the explorer

`VERSION = "1.13"` → **`"1.14"`** in `knowledge/_build_kg_explorer.py`, reason on the line
(`1  1`). Regenerated with the sanctioned generator only — **`python3 knowledge/_build_kg_explorer.py`**;
`gen_kg_edges.py` and `_build_all.py` were **never** invoked by this lane (`_validate_kg.py` runs
`gen_kg_edges.py` against its own scratch copy as its freshness arm — that is the gate's behaviour, not
this lane's write).

```
wrote notes/_KG-EXPLORER.html · v1.14 · snaps 54 · nodes 3909 · edges 6759 · islands 2 · orphans 0 · 2,893,289 B
  rules family (s274-D7..D12, ratified s274-D8): 634 edges + 0 declared nulls
  UX-principle family (s275-D1..D6, ratified s275-D2): 171 new nodes / 96 edges + 15 declared nulls
```
(v1.13 wrote `nodes 3905 · edges 6660`; the growth is the three #277 rulings and this session's lane
commits, not this land — the explorer still does **not read** `edges.obeys`.)

**DECLARED GAP, unchanged from #276:** the explorer does not draw `component → rule:` from
`edges.obeys`. `s277-D1..D3` did not ask for a reader and the edges are not unread — `_validate_kg.py`
resolves all **168** and the schema types them. A reader is still a named job for a later lane.

### the drive · `notes/_lanes/277/land/_drive_explorer.py` (new)

`source knowledge/_render/seat_env.sh` (`SEAT_ENV: OK seat=quirky-gracious-ptolemy · faces=10/404 · farm=10/10`),
then the driver. The chip is **clicked for real**, never `famOn` poked from the console. Because the
explorer has no `obeys` reader, the corpus count is read **off the metas on disk inside the drive** and
asserted next to the page bites, rather than pretended to be a page fact.

```
  ok    version string is v1.14 (v1.13 before the land)
  ok    the Guideline rules chip exists
  ok    the chip is OFF at first paint
  ok    clicking the REAL chip turns the rules family on
  ok    the guidelines chip turns on too
  ok    the rules family draws with the chip on          (drawn nodes 1050 -> 1592)
  ok    rule: nodes 470 (unmoved — this land mints no rule node)
  ok    sc: nodes 55 (unmoved — this land mints no criterion)
  ok    all four chart components are in the graph
  ok    corpus edges.obeys = 168 (81 before the land, +87)
  ok    edges.obeys now on 10 metas (6 before the land, +4 charts)
  ok    the four charts carry 24/25/27/11 = 87
  ok    every $why clears the schema's minLength 40
  ok    0 console errors / warnings / page errors
DRIVE PASS
```

**Screenshots, reviewed by eye** ([[art-director-reviews-lane-output-268]]):
- `notes/_lanes/277/land/screenshot-explorer-chip-off.png` — first paint, the Guideline-rules chip OFF.
- `notes/_lanes/277/land/screenshot-explorer-rules-on.png` — both chips on, fitted. Header reads
  **`as of v1.14 · 2026-09-16 · 7102f9d`**, **`593 rulings · 55 success criteria`**, legend
  **`SC 55 · RULE 470 · GUIDELINE RULES 634`**, `orphans none`, `islands 2` (Hero-variants 8,
  Template — auth 7 — both pre-existing).

---

## STEP 5 — `knowledge/compliance/README.md`

**LEFT UNTOUCHED.** #276's land lane explicitly did not touch it and said why: its
"Current graph (generated 2026-06-18)" block is a **generated** block that was already stale before that
lane, and re-stating part of it by hand makes it internally inconsistent. Nothing in s277-D1..D3
mints a rule file or a success criterion, so this land does not even move the figures that block
carries. Regenerating it remains a named job, not this lane's.

---

## The 18 AMBERs

Landed **as-is**, per the brief and FV's verdict. The tightenings FV offered (#26/#78 "precisely" →
"two of three", #76 drop the high-contrast clause, #81 "for the same reason" → "on type26-013") are
**not applied** — they change no count and were marked optional, and a land lane that edits sentences
nobody ruled on is a land lane writing its own copy. They are on the record in
`notes/_lanes/277/fable-verify/VERIFY.md` for whoever reopens these edges.

Two things FV left open and this land does **not** close:
- the **`parts ≤ 5` vs `Maximum 6 (dv-pie-009)`** conflict — s277-D3 flags it and does not resolve it;
  #31 and #32 each quote their own line and land side by side, still open, correctly.
- **`dv-013` on `chart-bar`** — offered to Dave, no note came, so it **stays off**, and the figure is
  **47**, not 48.

---

## Housekeeping

- Never stashed (`git stash list` empty before and after). No `.git/index.lock` was present; nothing
  went to `.git/_orphan-locks/`.
- `notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl` are dirty from tooling that
  ran before this lane opened. **Not staged — they are not this lane's**, exactly as #276 declared.
- A read-only KG-audit lane was running in parallel; it writes nothing, and `git status` confirms
  nothing of its appeared in the index.
- **NOT DONE, declared:** the `_validate_lane_ownership.py --selftest` 3/3 → 2/3 regression (above) is
  inherited and left for the conductor.

---

## The shipped commit

`git show --numstat`, re-read from the shipped sha:

```
1	1	knowledge/_build_kg_explorer.py
110	0	knowledge/components/chart-bar.meta.json
46	0	knowledge/components/chart-donut.meta.json
98	0	knowledge/components/chart-line.meta.json
102	0	knowledge/components/chart-pie.meta.json
2	2	notes/_KG-EXPLORER.html
240	0	notes/_lanes/277/land/LAND-REPORT.md
6	6	notes/_lanes/277/land/WHYS.md
93	0	notes/_lanes/277/land/_drive_explorer.py
11	11	notes/_lanes/277/land/_whys.py
1	1	notes/_lanes/277/land/proposed-metas/chart-bar.meta.json
4	4	notes/_lanes/277/land/proposed-metas/chart-line.meta.json
1	1	notes/_lanes/277/land/proposed-metas/chart-pie.meta.json
-	-	notes/_lanes/277/land/screenshot-explorer-chip-off.png
-	-	notes/_lanes/277/land/screenshot-explorer-rules-on.png
```

**Every file in the commit that this land AUTHORED is insertions-only**; the four `2 2` / `1 1` /
`6 6` / `11 11` / `4 4` rows are, in order, the regenerated explorer HTML, the `VERSION` line and the
three rebuilt proposals, the regenerated `WHYS.md`, and the six `$why` + five anchor lines in
`_whys.py` — every one of them a file this lane owns under `notes/`, or the two generated artefacts.
**Nothing under `knowledge/components/` shows a single deletion.**

This block was re-read with `git show --numstat` from the shipped sha AFTER the report was amended
into it; the `LAND-REPORT.md` row above is this file's own length and is self-consistent. The sha is
returned by the lane (a commit cannot carry its own hash).

