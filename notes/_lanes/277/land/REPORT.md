# Lane LA — the four metas assembled: 29 + 47 + 11 = **87 `obeys` edges, every one with an authored `$why`**

#277 · 2026-09-16 · enacting `s277-D1` / `s277-D2` / `s277-D3` (`407f20b`) · **PROPOSED — nothing
under `knowledge/` is written.** The four proposals sit in `notes/_lanes/277/land/proposed-metas/`
and are produced by a script lane LL can re-run.

Deliverables: `_whys.py` (the 87 sentences + their anchors) · `_splice.py` (the textual-span builder
with its reconstruction proof) · `proposed-metas/` (4) · `WHYS.md` (the verifier's table) ·
`_gates.py` · `gates.txt` · this report.

---

## 1. The counts, per component

| component | rule-file citations | family citations | total | ruling |
|---|---:|---:|---:|---|
| `chart-line` | **9** (`dv-line-001…008`, `011`) | **15** | **24** | D1 + D3 |
| `chart-pie` | **10** (the 11 minus `dv-pie-003`) | **15** | **25** | D1/D2 + D3 |
| `chart-bar` | **10** (`dv-bar-001…010`) | **17** | **27** | D1 + D3 |
| `chart-donut` | **11** (the pie file entire, `dv-pie-003` included) | **0** | **11** | D2 |
| **all four** | **40** | **47** | **87** | |

**87, not 86** — `dv-line-005` is KEPT, reworded. The decision is §2.

The family split is `bar 17 · line 15 · pie 15 = 47`, re-derived from lane CP's
`notes/_lanes/277/page/_build_page.py` matrix (`REC` = CO's `FAMILY` + the two settled overrides +
`dv-013`/bar held OFF). `dv-013` and `dv-015` bind none of the three.

⛔ **The donut takes NO family rules.** `s277-D3` attaches the 19 family rules to bar / line / pie
only; `s277-D2` gives the donut the pie FILE. `_whys.EXPECTED` asserts `chart-donut = 11 + 0` and the
build refuses on any other shape, so the widening the brief warned against cannot happen by accident.

---

## 2. `dv-line-005` — **KEPT, reworded. The line goes 9, not 8.**

`s277-D1` allowed drop-and-declare; the brief's test was *prefer the reworded sentence only if you can
point at a real mechanism*. **I can, and it greps.** The reworded sentence (the conductor's wording
from `fable-check/CHECK.md`, taken as written) rests on two strings that are in the live
`chart-line.meta.json`:

- `series 1–5 on ONE continuous time axis` — **line 16**, the `when` clause
- `"name": "series"` — **line 19**, the prop that clause caps

The rule (`data-visualisation-line-charts.md` §Content display) asks for *comparable measurement
intervals, similar scale; single-axis grid for large intervals, double-axis for small; drop gridlines
if they confuse* — `[TASTE]`. The meta's structural commitment to **ONE continuous time axis** carrying
1–5 series IS the comparable-intervals / single-axis half of that, stated from the routing side. The
gridline-density half is genuinely the author's, and the sentence says so out loud, and says the edge
is the weakest of the nine. That is a thin binding honestly labelled, not a true-sounding sentence with
nothing behind it — which was the actual defect the Fable check named.

**What was wrong before, and is now gone:** CO's sentence claimed the rule was *"the reason `responsive`
pins the viewBox 1:1 rather than rescaling intervals"*. The 1:1 pin is DV-D02's text-never-scales
mechanism (`responsive.rule`, line 100) and says nothing about measurement intervals. That borrowing is
not in the file any more; `responsive.rule` is not named by this edge at all.

The other RED, `chart-bar → dv-bar-001`, is replaced with the CHECK's wording verbatim: the title is
**not a prop** on `chart-bar` (props are orientation · series · sort · data · empty) — it is a TYPE
ROLE, `title .t-cm-section-label` in `tokens.font-family`, **line 33**. Anchored there.

---

## 3. How the proposals were built — a span, not a `json.dump`

`_splice.py` takes the LIVE file's bytes and inserts **ONE** `edges.obeys` span as the first key inside
`edges`. None of the four live metas carries an `obeys` block today (R5 asserts it), so each proposal is
exactly one insertion. Five refusals, all loud and named, all rc-nonzero:

| | check | result |
|---|---|---|
| **R1** | RECONSTRUCT — removing the inserted span gives back the ORIGINAL BYTES, `==` on the raw string | OK ×4 |
| **R2** | PARSES — the new text `json.loads` and equals the live object plus exactly `edges.obeys` | OK ×4 |
| **R3** | GROUNDED — every anchor grepped in the LIVE bytes; a miss REFUSES the build by name | OK, 87/87 |
| **R4** | COUNTS — the per-component split equals `_whys.EXPECTED` | OK ×4 |
| **R5** | NO-OBEYS — the live meta must not already carry `edges.obeys` | OK ×4 |

Spans inserted: `chart-line` 6,828 chars at byte 10,250 · `chart-pie` 7,307 at 9,980 · `chart-bar`
7,818 at 11,725 · `chart-donut` 3,835 at 10,424. Re-running the script reproduces all four
byte-for-byte (verified by a second run leaving `git status` unmoved).

**This is the `_inscribe_ruling.py` discipline** (#179): a `json.load` → append → `json.dump` round trip
reformats every line the serializer's defaults disagree with, and buries 87 real additions inside
hundreds of spurious ones. No meta was `json.dump`ed.

---

## 4. R3 in full — the one rule that mattered

**Every `$why` names a mechanism that is in the live file, and `WHYS.md` records the grep hit and the
line number for all 87.** `_whys.py` carries 1–3 EXACT SUBSTRING anchors per sentence; `_splice.py`
greps each against the live raw bytes before it will write anything. All 87 held on the first build —
no sentence had to be retired for failing its anchor.

Two anchors are **NEGATIVE** (`!needle`, asserting an absence), because two sentences rest on one:

- `chart-line → dv-line-001` — the line/bar asymmetry. `data-domain-min` occurs **0 times** in
  `chart-line.meta.json` and **once** in `chart-bar.meta.json` (line 70). The absence is the binding.
- `chart-bar → dv-bar-008` — past-vs-projected. `projected` occurs **0 times** in `chart-bar.meta.json`;
  the meta declares no projected variant, and the rule is what a future one must satisfy.

An absence is checkable exactly as a presence is, and both are checked on every run.

`WHYS.md` is the table the Fable verifier grades: **`notes/_lanes/277/land/WHYS.md`** — 87 rows,
component · rule · `$why` · the exact live string with its line number, generated from the same
`_whys.py` the metas are built from, so the graded sentence and the shipped sentence cannot drift.

---

## 5. Gates — every line

Written by `_gates.py` to `notes/_lanes/277/land/gates.txt`:

```
PASS G1 schema chart-line.meta.json validates against meta.schema.json (24 obeys, $why required and present on every one)
PASS G1 schema chart-pie.meta.json validates against meta.schema.json (25 obeys, $why required and present on every one)
PASS G1 schema chart-bar.meta.json validates against meta.schema.json (27 obeys, $why required and present on every one)
PASS G1 schema chart-donut.meta.json validates against meta.schema.json (11 obeys, $why required and present on every one)
PASS G2 refs chart-line: every `rule:` id resolves in _rules-index.json
PASS G2 refs chart-pie: every `rule:` id resolves in _rules-index.json
PASS G2 refs chart-bar: every `rule:` id resolves in _rules-index.json
PASS G2 refs chart-donut: every `rule:` id resolves in _rules-index.json
PASS G3 counts: chart-line 9+15=24 · chart-pie 10+15=25 · chart-bar 10+17=27 · chart-donut 11+0=11 — TOTAL 87 (29 + 47 + 11)
PASS G4 _validate_kg.py on the simulated tree (4 proposals swapped in): rc=0 — _validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.
PASS G4 restore: the four live metas byte-compare EQUAL to the bytes held before the swap
```

`G1` is the gate the brief named: `meta.schema.json`'s `obeysEdge` REQUIRES `$why` at `minLength 40`
and forbids a null `ref`, and all 87 clear it.

`G4` swaps the four proposals into `knowledge/components/`, runs `knowledge/_validate_kg.py`, and swaps
the originals back in a `finally` — then proves the restoration by byte-comparing against the bytes held
before the swap. The gate reported **90** `ref:null`+`$note` entries and **82** ruled verdicts asserted
present (MERGE 5 / PROMOTE 52 / ATTACH 25), unchanged by the proposals. ⛔ `gen_kg_edges.py` was never
invoked by this lane; `_validate_kg.py`'s own freshness arm runs it against its own scratch copy, which
is that gate's behaviour, not a write of this lane's. `_build_all.py` was not run. No `git stash`. No
stale `.git/index.lock`.

**`git status` after the battery: changes ONLY under `notes/_lanes/277/land/`.** (Two files —
`notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl` — were already modified in the
working tree when this lane opened, are not this lane's, and are NOT in the commit.)

---

## 6. What a splicer needs to know next

- The four proposals are **complete files**, not patches: lane LL copies them over
  `knowledge/components/<stem>.meta.json`, or re-runs `_splice.py` to regenerate them. Re-running is the
  better move — it re-greps all 87 anchors against whatever the live metas say **that day**, so a meta
  that has moved under a citation refuses the build instead of landing a stale sentence.
- The `5-vs-6` conflict is **still open and still flagged**: `chart-pie.when` says `parts ≤ 5` (line 16)
  while `props.slices` says `Maximum 6 (dv-pie-009)` (line 25), and `chart-donut` carries the same 6.
  `s277-D3` explicitly does not resolve it. `dv-pie-009` is cited on pie and donut as the file states it,
  **6**, and this lane did not quietly pick a side.
- `dv-line-005` is the weakest of the 87 and says so in its own sentence. If the verifier refuses it, the
  drop is one line out of `_whys.LINE` and one number in `_whys.EXPECTED`, and the line becomes 8 + 15.
