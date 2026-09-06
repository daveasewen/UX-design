# `#250`-`PROBE` — the ADR-0015 byte gate: anatomy, minified floor, and the price of each of Dave's four options

session: `#250` · 2026-09-06
window: premise probe (byte gate)
sub index: `PROBE`
brief: chat brief (no file) — "PREMISE PROBE for the byte gate", 6 numbered premises
tokens: `UNMEASURED — sub could not read `message.usage` from inside the lane`

## VERDICT

All six premises were probed and every number below is pasted from a command run in this window.
The lane's headline premise — *"(c) a comments-only shave of ≥3.7 KB clears the red"* — is **half
true and the half that fails is the page budget**. Shaving 3.7 KB from `dv-behaviour.js` alone
clears `MAX_BYTES` (19,768 → 16,068) but leaves the group at **36,710 > 34,816 — still red by
1,894 B**. A full comment strip of all three sources clears BOTH caps with room (13,119 per-source,
24,837 page), so (c) is *feasible* but is a **15,573-byte provenance amputation**, not a 3.7 KB
trim. Two structural findings change the shape of the fork: (1) `terser` takes the three sources to
**16,124 B total** (2,793 + 1,846 + 961 = 5,600 B gzipped), and ADR-0015 **explicitly rejected
minification when Dave asked for it on 2026-07-26** — the cap is a complexity forcing function, not
a wire-weight proxy, so a minified figure is not a legal answer to this gate; and (2) the gate's
"page budget" sums **every** source in the group regardless of the `consumes` opt-out that
Amendment 2 added, so it is measuring a registry sum, not a page: **only `Chart-donut` actually
loads 40,410 B**; every other member loads 34,899 or 19,768. Nothing here is ruled or recommended —
priced only.

COUNTS: findings `11` · ruling-shaped `1` · UNPROVEN `3`

CITES: `#96-D5` (`notes/_MEMENTO-DECISIONS.md:3874`) · `ADR-0015` §4 + Amendment 1 (node
`ADR-0015-A1`) + Amendment 2 · `s235-D2` (`knowledge/_rulings.json:5337`) · `s234-D6`
(`knowledge/_rulings.json:5304`)

## What was done

Read-only probes against `/Users/daviewen/Documents/Claude/Projects/UX-design`. No repo file was
modified. `_build_all.py` was NOT run. One file written: this report.

## Findings

**1 · Byte anatomy of the three sources (premise 1).**
`python3` walk over `knowledge/component-types.json` → `component-type/dataviz/$behaviour`:

```
dataviz/dv-behaviour: canon/dv-behaviour.js = 19768
dataviz/dv-legend:    canon/dv-legend.js    = 15131
dataviz/dv-donut-sweep: canon/dv-donut-sweep.js = 5511
  GROUP dataviz total = 40410
```

Those three files are exactly what sums to 40,410. Comment/blank/code split (block comments matched
`/\*…\*/`, line comments `^\s*//`, blanks whole-line):

| file | total | block comment | line comment | blank | code-only |
|---|---|---|---|---|---|
| `dv-behaviour.js` | 19,768 | 6,649 | 0 | 7 | **13,112** |
| `dv-legend.js` | 15,131 | 7,317 | 0 | 12 | **7,802** |
| `dv-donut-sweep.js` | 5,511 | 1,607 | 0 | 4 | **3,900** |
| **sum** | **40,410** | **15,573** | 0 | 23 | **24,814** |

Every comment byte in the kit is a **block** comment; there are no `//` comments and effectively no
blank-line slack (23 B across three files). The provenance trail IS the block comments.

**2 · A comments-only shave: what it yields, and where (c) misses (premise 1).**
Full comment strip, blanks kept: `dv-behaviour` **13,119** · `dv-legend` **7,814** ·
`dv-donut-sweep` **3,904** · page **24,837**. Both caps clear, with 3,265 B of per-source headroom
and 9,979 B of page headroom.

But the shortfalls are unequal and the brief's "≥3.7 KB" figure only sizes the smaller one:

```
per-source shortfall dv-behaviour: 3384   page shortfall: 5594
shave 3700 from dv-behaviour only -> src 16068  page 36710  page still over by 1894
```

**So (c)-as-briefed does NOT get under both caps.** The minimum comment shave that clears both is
**5,594 B page-wide, of which ≥3,384 B must come out of `dv-behaviour.js` specifically** — i.e.
36% of the kit's total comment mass, or 51% of `dv-behaviour`'s own.

**3 · Minified floor (premise 2).** `npx terser <file> --compress --mangle` (terser 5.51.2, present
in the image):

```
dv-behaviour.js   raw=19768  terser=8552  terser+gzip=2793
dv-legend.js      raw=15131  terser=5071  terser+gzip=1846
dv-donut-sweep.js raw=5511   terser=2501  terser+gzip=961
```

Shipped-minified group = **16,124 B**; minified+gzip = **5,600 B**. Against the 34,816 page budget
a shipped artefact is at 46% minified, 16% on the wire.

**4 · The gate measures SOURCE, and ADR-0015 says so on purpose (premise 2).** The gate's docstring
reads: *"size ≤ 16 KB raw (ADR-0015 §4; observed proforma baseline 9.9 KB for the whole kit — the
cap is headroom, not a target)"* (`knowledge/_validate_behaviour.py:10-11`). ADR-0015 §4: *"Size
gate (blocking): source ≤ 16 KB raw."* And Amendment 1 records that minification was **already put
to Dave and declined**:

> *"Minify the source (Dave asked, 2026-07-26) — declined: the cap is a complexity forcing
> function, and minifying shrinks the number without simplifying the thing… Transport compression
> already takes the group from 28,332 B to 9,622 B gzipped, free. A true wire-weight answer belongs
> in the ADR-0008 adapter layer."*
> — `docs/decisions/ADR-0015-behaviour-partials-dataviz.md:78-88`

Amendment 1 also renames the 16 KB cap's job: *"The 16 KB cap stays per-source, and its job is
renamed: LEGIBILITY. A behaviour source must stay small enough for one person to hold in their
head."* (line 65). The page budget's job is stated at line 67-73: *"Splitting a source must not buy
headroom."*

**5 · Everything that hard-codes the constants (premise 3).** `grep -rn` for
`16384|34816|32768|16 KB|34 KB|16KB|34KB|32KB|32 KB|MAX_BYTES|PAGE_BYTES`, excluding `.git/`,
`_to_delete/`, `outputs/`. **Live code + docs + registry (a re-dial must touch or contradict
these):**

| file:line | text | class |
|---|---|---|
| `knowledge/_validate_behaviour.py:38` | `MAX_BYTES = 16 * 1024` | **THE CONSTANT** |
| `knowledge/_validate_behaviour.py:43` | `PAGE_BYTES = 34 * 1024  # ⚠ RE-DIALLED 32→34KB by DAVE, #96` | **THE CONSTANT** |
| `knowledge/_validate_behaviour.py:10` | docstring `size ≤ 16 KB raw` | prose |
| `knowledge/_validate_behaviour.py:41, 81, 181-185` | `16KB`/`32KB`/`34KB` in comments + the selftest pad comment | prose + **fixture** |
| `knowledge/_validate_behaviour.py:137, 140, 144` | report prose `≤16KB`, `of 16 KB`, `of 32 KB` | **stale in print already** |
| `knowledge/_build_all.py:212` | `# ≤16KB raw · no polling/network…` | prose |
| `knowledge/gen_component_partials.py:43` | `The performance contract on the SOURCE (≤16KB, banned patterns) is _validate_behaviour.py's.` | prose |
| `docs/decisions/ADR-0015-…md:29, 47, 65, 67, 68, 73, 78, 126` | `16 KB` ×5, `32 KB` ×3 | **THE ADR — still says 32 KB** |
| `knowledge/component-types.json:103, 464, 476, 488` | `$description` prose on the cap fork | registry prose |
| `knowledge/_decision-graph.json:366` · `_decision-graph-seed-2026-07-21.json:380` · `knowledge/_DECISION-GRAPH.md:39` | node title *"the 16KB cap becomes per-source legibility plus a 32KB per-group page budget"* | **graph node title** |
| `knowledge/canon/dv-behaviour.js:8` · `dv-legend.js:8, 15` · `dv-donut-sweep.js:3, 6` | in-source contract banners (`16KB`, `32 KB`) | **inside the gated bytes** |
| `knowledge/_BEHAVIOUR-GATE.md:3, 5-9, 12-13` | generated report | regenerates |

**Generated / historical (a re-dial does NOT touch, but they will disagree):** 14
`knowledge/snippets/*.reference.html` carry the `≤16KB raw` contract banner **inside the injected
AUTO-BEHAVIOUR block** (Chart-{line,bar,donut,combo,scatter,pie,boxplot,bullet,candlestick,
histogram,butterfly-h,butterfly-v,stacked-area,sparkline} + `Template-dashboard-bento`), plus 9 of
them the `15.5KB of the 16KB per-source cap` split note; `dashboards/international-banking-
dashboard.regen-v2-receipt.html:1262,1522,1529`; `reviews/_specimen-chart-scatter-69.html:440,664`;
`knowledge/snippets/_REVIEW-66-scatter-title-before.html:330`. Plus ~40 hits across `notes/`,
`_GM-ARCHIVE.md`, `_LIVE-STATE-ARCHIVE.md`, `_DECISION-HISTORY/` — dated history, correctly frozen.

**6 · The gate's own printed prose is ALREADY stale, and was flagged twice (premise 3).**
`_validate_behaviour.py:137,144` still print *"per group ≤32KB"* and *"of 32 KB"* while `PAGE_BYTES`
is 34,816 — so `_BEHAVIOUR-GATE.md:9` currently reads `40410 bytes (39.5 KB of 32 KB, 116%)`, where
39.5/32 is not 116%. Named at `notes/_subreports/2026-08-27-220-audit-L1.md:244-248` and again at
`notes/_receipts/2026-08-24-crank-charts.md:28`. **Precedent: the #96 re-dial left three prose
strings behind for 32 days and counting.**

**7 · No waiver mechanism exists (premise 4).** `grep -n "waiver|WAIVER|noqa|allowlist|exempt|
EXEMPT|override" knowledge/_validate_behaviour.py knowledge/_build_all.py`. In
`_validate_behaviour.py` the only two hits are `# noqa: E402` on the help-gate import (line 27) and
the word "waiver" **inside the #96 comment describing Dave's three options** (line 45). There is
**NO** per-file, per-source, in-band or sidecar waiver form in this gate. **NONE.**

The *neighbouring* precedent is `_build_all.py`'s named-exemption list (lines 275-296, 829): a
`_validate_*.py` may be *exempt BY NAME with a reason* from being wired as a build step, bitten
four ways, with the exemption's own rot history in comments (`# RE-WIRED #120: exempt as ROTTED
since #118…`). That is an exemption from *running a gate*, not from *a gate's finding* — building
option (b) means importing that pattern into a layer that has never had it.

**8 · History of the constant (premise 5).**

```
$ git log --oneline -S "PAGE_BYTES" -- knowledge/_validate_behaviour.py
e3174d1 #120 2026-08-07 — ✅ COMMIT-SEAM HARNESS FIXED, BUILD GREEN TO STEP 73 …
7401daf Behaviour cap fork RULED (ADR-0015 amendment) + Chart-donut migrated to the DV-D11/12/13 legend model

$ git log --oneline -S "34 * 1024" -- knowledge/_validate_behaviour.py
df1765a after #96 2026-08-05 — ★★ WAVE 2 PROVEN: ALL 8 RENDER-VERIFIED, DAVE RULED ALL 7 FLAGS + 4 MORE …
```

`-S "PAGE_BYTES"` does not surface the #96 re-dial (occurrence count unchanged); `-G` and
`-S "34 * 1024"` both find it at **`df1765a`**. The rationale, verbatim from the file
(`knowledge/_validate_behaviour.py:43-46`):

> `PAGE_BYTES = 34 * 1024  # ⚠ RE-DIALLED 32→34KB by DAVE, #96 2026-08-05: the 32KB cap predates the`
> `# 8 wave-2 members; his "extend fitOne() now" (#96-D1 ⑥) collided with it at 32,871 after the`
> `# addition was shaved twice. His pick from three options (re-dial / marked waiver / park), receipted`
> `# notes/_MEMENTO-DECISIONS.md § ★ #96. The PAGE-not-per-file scope is UNCHANGED (his 07-26 ruling).`

**The three options at #96 are the same three now, minus the shave.** And the shave was not
optional then: *"the addition was shaved twice"* BEFORE the fork was put to him — the fork was for
the **remainder** (103 B over; `_DECISION-HISTORY/2026-08-05-the-96-rulings.md:23-26`).

**9 · The ruling receipt (premises 5-6).** `notes/_MEMENTO-DECISIONS.md:3874`:

> **#96-D5 (Dave):** ADR-0015 dataviz behaviour PAGE budget **re-dialled 32→34KB** — his pick
> (options: re-dial / marked waiver / park) after #96-D1 ⑥ collided with the cap at 32,871
> (addition shaved twice first, per gate-inside-the-growth-loop). Page-not-per-file scope
> unchanged. Enacted `_validate_behaviour.py:37`; gate re-run GREEN.

**10 · `knowledge/_rulings.json` carries NO byte-cap ruling (premise 6).**
`grep -n "ADR-0015\|PAGE_BYTES\|MAX_BYTES\|16 KB\|34 KB\|16KB\|34KB\|page budget"
knowledge/_rulings.json` returns exactly two hits, and neither rules a byte:

- **`s235-D2`** (line 5337) — *"THE NEW L1 GATE IS NAMED `_validate_receipt.py` … `_validate_
  behaviour.py` **stays what ADR-0015 made it**"* — a fence around this gate's scope, not its caps.
- **`s234-D6`** (line 5304-5308) — Dave: *"You recommend, I always lean to **real solutions not
  patches**, and mechanical over inference."* Not about bytes; it is the standing posture any
  waiver or re-dial argument runs into.

So `#96-D5` lives only in `notes/_MEMENTO-DECISIONS.md` and the file comment — **the ADR-0015 text
itself was never amended and still says 32 KB in all three places** (lines 67, 73, 126). A re-dial
inherits an already-unreconciled document.

**11 · The gate is not measuring a page (premise 2, structural).** `check_group` sums **every**
`$behaviour` source in the group. But ADR-0015 Amendment 2 (2026-07-28) added per-member
`consumes`, and 15 of 15 members declare it. Actual per-member load:

```
Chart-donut:        dv-behaviour+dv-legend+dv-donut-sweep = 40410
Chart-{line,bar,combo,scatter,pie,stacked-area,butterfly-h,butterfly-v}: = 34899
Chart-{sparkline,histogram,boxplot,bullet,candlestick}, Template-dashboard-bento: = 19768
```

**Only `Chart-donut` loads 40,410 B.** The second-heaviest real page is **34,899 — over 34,816 by
83 B**, so the group would be red on a `consumes`-aware measure too, but by 83 B on 8 members and
5,594 B on one. Amendment 2 asserted *"Budgets untouched… `_validate_behaviour.py` unmodified"*
(ADR line 126) — that is the seam: the budget's own ADR calls it a PAGE budget while the code sums
a REGISTRY.

## Pricing Dave's four options

| option | costs (bytes / edits) | breaks | leaves red |
|---|---|---|---|
| **(a) re-dial both caps** | 0 source bytes. **2 constant edits** (`MAX_BYTES` 16→20 KB ≥19,768; `PAGE_BYTES` 34→40 KB ≥40,410). Plus: 3 stale report strings (`:137,140,144`), the docstring (`:10`), the selftest pad comment (`:181-185`) — the 3-pad fixture at 3×16,364 = 49,092 still exceeds a 40 KB `PAGE_BYTES`, so the bite survives *by luck*, un-re-derived. Plus ADR-0015 amendment 3 (8 typed figures, still saying "32 KB" from the LAST re-dial), the decision-graph node title in 3 files, the registry `$description`s, and 14 snippet banners that re-inject on next `gen_component_partials.py` run. **~10 live files + 14 regenerated.** | Nothing executable. It breaks the ADR's own stated reason for the cap — *"a cap that moves once moves again"* (ADR line 78, written to REJECT exactly this) — for the **second** time in 32 days, and it retires the forcing function the ADR calls *"the forcing function working, not a defect"* (line 90). | **Nothing red.** Gate goes green on the next run. |
| **(b) marked waiver** | 0 source bytes. **New mechanism**: a waiver form does not exist in this gate (finding 7) — a marker syntax, a reason field, an expiry or session stamp, report rendering, and ≥2 selftest bites (waiver honoured / malformed waiver refused), on the `_build_all.py` named-exemption pattern. **~150-250 new lines in `_validate_behaviour.py` + selftest + ADR amendment.** Dearest in build, cheapest in canon bytes. | Nothing today. It opens a *class*: a gate whose finding can be marked away is a gate whose red is negotiable, and this repo's own record (`_build_all.py:288` `exempt as ROTTED since #118`) shows exemptions rot silently for sessions. Collides with `s234-D6` (*"real solutions not patches"*). | **Nothing red** once written — but the gate is then green *while over budget*, which is the state ADR-0015 §4 exists to make impossible. |
| **(c) shave ≥3.7 KB of comments** | **The brief's figure is short.** Needs **5,594 B page-wide with ≥3,384 B from `dv-behaviour.js`** — 36% of all 15,573 comment bytes in the kit, 51% of `dv-behaviour`'s. All of it block comments; there is no blank-line or line-comment slack (23 B total). Then `gen_component_partials.py --check` forces a **byte-exact re-injection into 14 snippet files** + `_BEHAVIOUR-GATE.md` regen. **3 canon files + 14 regenerated + a full build.** | The provenance trail. The comments in these files ARE the ADR/DV-D record (`dv-legend.js:8-15` carries the whole split rationale). ADR-0015 Amendment 1 already measured a comment strip once (26,615 → 22,364) and still had to split — comments were spent then, and this spends the rest. Also self-erasing: the stripped banners are the `≤16KB` contract text a reader of a portable snippet sees. | **Nothing red** if the full 5,594 is taken. **Red by 1,894 B** if only the briefed 3.7 KB from `dv-behaviour` is taken. |
| **(d) park the lane** | 0 bytes, 0 edits — but the #249 VFIT work (≈4,588 B added, 3,697 code-only) is already committed at `c05ff59`. Parking means **reverting** those bytes or leaving the gate red. | Nothing built. The FIT proposal (a), built 19/19 at #249, does not ship. | **`_validate_behaviour.py` stays RED — two fails, blocking** (`19768 > 16384` and `40410 > 34816`), which means `_build_all.py` cannot go green, which is the ceiling arm already named RED by name at the #249 wrap (`GOOD-MORNING.md:477`). Parking is the only option that leaves the build red. |

### The strongest case AGAINST the easiest option

**(a) re-dial looks easiest — two integers — and it is the option ADR-0015 explicitly wrote down as
rejected.** Three things stand against it, in ascending weight:

1. **It is not two integers.** Finding 5 lists 10 live files and finding 6 proves the #96 re-dial
   *did not finish*: three printed strings still say "32 KB" 32 days later, and the gate's own
   published report currently prints an arithmetic contradiction (`39.5 KB of 32 KB, 116%`). A
   second re-dial done to the same standard leaves a report that lies about two different numbers.
2. **It converts a legibility cap into a size observation.** Amendment 1 renamed the 16 KB cap's
   job to LEGIBILITY — *"small enough for one person to hold in their head"*. `dv-behaviour.js` at
   19,768 B is 27% over a threshold that was set for a human, not a browser. Re-dialling
   `MAX_BYTES` to 20 KB does not make the file more legible; it records that it stopped being.
3. **It is the second pull of a lever the ADR predicted would be pulled repeatedly.** ADR line 78,
   rejecting the 32 KB raise: *"a cap that moves once moves again."* It has now moved once (32→34).
   A 34→40 move is an 18% jump against #96's 6%, taken for a lane's addition rather than for a
   measured re-baselining of what the kit should weigh. And it is the option that **spends the
   forcing function to avoid the conversation the forcing function exists to force** — the ADR's
   own words at line 90: *"⚠ The next behaviour addition therefore faces this same conversation —
   that is the forcing function working, not a defect."*

The counter-case, stated for completeness because pricing is not advocacy: the wire numbers
(finding 3 — 5,600 B gzipped, 16% of budget) say the *user-facing* premise of the cap is not in
danger, and the `consumes` finding (11) says the gate is over-measuring 14 of 15 members. Both are
arguments that the **cap's shape**, not its value, is the thing to revisit — which is neither (a)
nor (b) nor (c) nor (d).

## RULING-SHAPED QUESTIONS

1. **The byte fork itself is Dave's and is NOT ruled here.** Options (a) re-dial `MAX_BYTES`
   ≥19,768 and `PAGE_BYTES` ≥40,410 · (b) build a marked-waiver mechanism that does not yet exist ·
   (c) shave **5,594 B** of comments (not 3.7 KB — see finding 2), ≥3,384 of them from
   `dv-behaviour.js` · (d) park and leave the build red. Priced in the table above. **No
   recommendation is offered — the brief said price, not recommend.**

   *A fifth shape surfaced by finding 11 that is not on Dave's list and is therefore also his:*
   make `check_group` `consumes`-aware so the page budget measures what a member page actually
   loads. It does not clear the red on its own (`Chart-donut` still loads 40,410; the 8 two-source
   members still sit 83 B over), so it is a **re-shaping**, not a remedy — but it changes what a
   re-dial would be re-dialling.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** that a 5,594-byte comment shave is *achievable without cutting load-bearing
  provenance* — the anatomy proves the bytes exist, not that they are spendable. Price to prove:
  one read of all 15,573 comment bytes and a line-by-line keep/cut pass, ~12-15K tokens.
- **UNPROVEN:** that option (a) leaves the build green end to end. Only `_validate_behaviour.py`
  was reasoned about; `_build_all.py` was **not run** (brief forbade it). Price to prove: one full
  build, ~1 command + its output.
- **UNPROVEN:** the exact selftest consequence of each re-dial value. The 3-pad page-budget bite
  (`_validate_behaviour.py:185-188`) is derived from `MAX_BYTES`, so moving `MAX_BYTES` moves the
  pads; the arithmetic was checked for one candidate pair (20 KB / 40 KB) only, by hand, not by
  running `--selftest`. Price to prove: `python3 knowledge/_validate_behaviour.py --selftest` per
  candidate pair, ~200 tokens each.
- **CLAIMED (from the brief, and corrected here):** *"shave ≥3.7 KB of comments"* — re-measured
  from the artefact as **5,594 B page-wide**; the 3.7 KB figure clears only the per-source cap.
- **CLAIMED (from `_MEMENTO-DECISIONS.md:3874`, not re-read from the #96 gate run):** that the #96
  re-dial left the gate GREEN. Re-read costs one `git show df1765a` + a gate run at that tree.

## Evidence

No evidence files: every claim above quotes its probe inline (the command and its pasted output).

REPLAY-THESE: `knowledge/_validate_behaviour.py` lines 36-46 + 135-146 (the two constants and the
three stale prose strings) (~900 tk) · `docs/decisions/ADR-0015-behaviour-partials-dataviz.md`
lines 60-95 (Amendment 1: the renamed cap job + the rejected-minify paragraph) (~1,100 tk)
