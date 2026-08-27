# #220 sub-report — charts lane: DV-J2b sparkline — **DISCHARGED BY MEASUREMENT**

**Outcome: NOTHING WAS BUILT, DELIBERATELY.** STEP 0 falsified the brief's premise. The sparkline
strand is `superseded` and the table-idiom strand is `landed` in the records; and the build the brief
specified would have **reversed a Dave ruling** (`s182-D2`). This is the **FOURTH recorded recurrence**
of the stale-queue class (#26, #196, #199, now #220) — and this time the surface that misled is
identified, with the reason the BLOCKING gate cannot see it.

`COUNTS:` probes 12 · findings 9 · ruling-shaped questions 4 · UNPROVEN 2 · files created 1 (this report) ·
files modified 0 · components built 0 · review pages built 0 · gates driven 5 (all green) · rulings read from store 3

---

## 1. Premise verification — the receipts

**The authority is `knowledge/_lanes.json`** (its own `$description`: *"Data carries STATE, prose carries
WHY"*). Read at source, this session:

| strand | brief said | **RECORD says** | receipt |
|---|---|---|---|
| DV-J2 scatter | (landed) | `landed` | #27 |
| **DV-J2b sparkline** | *"queued"* | **`superseded`** | `s182-D2` (#182); state word aligned #190 under `s190-D1` |
| **DV-J1 table-idiom** | *"queued"* | **`landed`** | Dave's word #191 — *"call it landed, with a receipt naming both halves"* |

**Where the false premise came from — named exactly:** `GOOD-MORNING.md:343`, the §C·1 eager ROUTING
line, carries the verbatim string:

```
DV-J2b sparkline queued · DV-J1 table-idiom queued
```

That prose disagrees with the records it is supposed to mirror. `notes/_briefs/2026-08-21-213-c1-residual-survey-v1.md:136`
already said so five sessions ago: *"DV-J2 is `landed`, DV-J1 is `landed`, DV-J2b is `superseded` (s182-D2)"*.

### 1a. ⛔ THE BLOCKING GATE FOR THIS EXACT DRIFT READS **GREEN** — DRIVEN, NOT ASSUMED

`_capture_gate.py::lane_routing_check` exists precisely to stop *"drift between the eager line and the
records… the confident-false-inscription class"*, and is **BLOCKING by ruling (O1′ #24, pick 3)**. I drove it:

```python
lanes, errs = _gen_lanes.load_lanes()          # errs: []
_gen_lanes.check_routing_line(gm_text, lanes)  # -> []   ← GREEN, right now
```

**Why it is blind, from its own source:** `routing_expectations()` returns
`[(lane["id"], STATE_WORD[lane["state"]]) for lane in lanes]` — **lane-level pairs only**. The check
asserts three things: each lane's state word beside its lane id, no unregistered lane ids, and that the
records file is named. **It never parses the per-STEP words inside the parenthetical.** So
`DV-J2b sparkline queued` is structurally ungated prose sitting on the most eager cold-start surface
in the repo. [[no-gate-parses-the-artefact]] · [[premise-ages-faster-than-rule]].

---

## 2. The specified build could not have been built as written — and should not be

**(a) Both artefacts the brief told me to copy from the scatter exemplar do not exist.**

| named in brief | measured |
|---|---|
| scatter's **toolbar** | `dv-toolbar` = **0 occurrences repo-wide**. The only `toolbar` strings in `Chart-scatter`/`Chart-sparkline` are inside **JS comments**. |
| scatter's **mark contract** | `data-dv-mark` = **0** in all 14 chart snippets. |

**(b) Adding a toolbar would REVERSE `s182-D2`.** The ruling's own words: *"the sparkline is an atom
alone… a sparkline shows the trend beside a headline figure and supporting quantities, **it is not an
analysis tool**"*. The snippet declares the same at `Chart-sparkline.reference.html:25`:

```
NO legend machinery (single series) · NO table popover / CSV toolbar ·
NO title slot (axis-free ambient idiom; the sr-only figcaption names it).
```

The "compact Layer-2" is **deliberate, by ruling** — not a gap awaiting catch-up.

**(c) `s182-D2` is already fully enacted in the file.** 4 × `<details>` and 4 × `"View as table"` hits
are **all comment prose documenting the removal**; the single `<summary>` is inside a `/* */` JS comment.
**Zero live table markup in the atom.**

---

## 3. Strand health — the sparkline is not merely done, it is GREEN (measured this session)

| instrument | verdict |
|---|---|
| `knowledge/_gate_dataviz_vars.py` (BLOCKING, `s191-D3`) | ✅ 18 files, **767 colour refs, 4 themes** — every attribute resolves in ≥1 theme. **No silent black.** |
| `knowledge/_validate_snippets.py` | ✅ 135 snippets, 0 failures |
| `knowledge/_validate_dataviz.py` | ✅ 15 chart surfaces; sparkline **PASS** (3 charts, 0 blocking, 3 advisory) |
| `knowledge/_render/verify_sparkline_responsive.py` | ✅ **PROOF PASS** — driven first-hand |

Render proof output (JS-on **and** JS-off × 3 viewports):

```
js=on  vw= 420  spark= 348.0/ 348.0  h=64   js=off vw= 420  spark= 348.0/ 348.0  h=64
js=on  vw= 900  spark= 828.0/ 828.0  h=64   js=off vw= 900  spark= 828.0/ 828.0  h=64
js=on  vw=1440  spark=1368.0/1368.0  h=64   js=off vw=1440  spark=1368.0/1368.0  h=64
PROOF PASS: enclosure-responsive at every width, JS-on and JS-off; heights unchanged (64/44)
```

*(Sandbox note: `chromelibs-220` + `pw-browsers-220` were already staged by a sibling #220 lane. First
launch died on `libXdamage.so.1` — **a crash, not a fail**; `ldd` with `LD_LIBRARY_PATH` set showed zero
missing libs, and passing the env **inline via `env`** rather than `export &&` ran it green. Worth the
runbook's sixth stratum if it recurs.)*

---

## 4. ⛔ THE REAL DEFECT FOUND: `chart-sparkline.meta.json` IS STALE, AND A BROWSER JUST DISPROVED IT

`knowledge/components/chart-sparkline.meta.json` still describes the **pre-`s182-D2`, pre-`s184-D1`**
component. The snippet is correct; **the meta is not**. Seven stale passages:

1. `purpose` — *"two reviewed scales: standalone (**with its data table**)"*
2. `purpose` / `tokenValidation.$note` — *"COMPACT Layer-2 … popover + **fit (CSS width release under `.dv-fit-on`)**"*
3. `props.data.$note` — *"Standalone carries a **real `<table>`** (dv-005)"*
4. `variants.standalone` — *"**table** = the data surface"*
5. `accessibility.keyboard` — *"the **`<details>` summary** is focusable"* (the element is gone)
6. `accessibility.name` — *"the **table** is the full data surface"*
7. `antiPatterns` — *"**A standalone spark without its table** (dv-005 — the shape alone is not data)"*
   ⚠ This makes the **ruled** shape an anti-pattern in its own contract.

**And one claim is now MEASURABLY FALSE, not merely aged** — `responsive.rule` says:

> *"JS-on, `.dv-fit-on` … releases the standalone's fixed 340px to width:100% … **JS-off = fixed 340 baked**"*

The render proof measured **JS-off = 348 / 828 / 1368**, varying with the enclosure. `s184-D1` superseded
that behaviour at #184; the snippet's own `$note` records the supersession, **the meta never got it**.

**⛔ And two gates ran GREEN straight over it** (`_validate_snippets` 135/0, `_validate_dataviz` PASS) —
**no gate compares meta prose to rendered behaviour.** Same class as §1a.

**I did not fix it.** The brief grants me the components tree **NEW files only**, and this is an existing
gated artefact. Handed over below.

---

## 5. Two more stale surfaces, both partial

**5a. `knowledge/_REVIEW-SIGNOFF.md:282`** — the tuner-v2 row still reads *"SCALING IS THE ONLY OPEN
DECISION ON THE PAGE [0 — DAVE'S, #183's natural opener]"*. **Half of that closed at #184.** `s184-D1`
took the width call (*"the line should be responsive to its enclosure by default"*, readback *"this is
all correct"*). What genuinely survives is **only the 4px-grid height-snap**, which `s184-D1` expressly
left *"open direction, not ruled"*.

**5b. `knowledge/_lanes.json`, DV-J2b successor list** — reads *"trend-card composition (needs Dave's
word) or sparkline **colour**/height-snap at the tuner"*. The **colour half was closed by `s182-D3`**
(#182, same session) — *"the tuner's 37-candidate colour picker is MOOT"*. Only trend-card + height-snap survive.

---

## 6. Not a defect — declared so nobody re-finds it

The sparkline carries the **shared `dv-behaviour` core** (table popover, `clampPanel`, CSV copy, view
toggles) with no markup to bind to. It is **inert and guarded** — `if (!sum || !panel) return;` and
`det.classList.contains('dv-tbl')`, and the atom has no `dv-tbl`. This is the known
self-contained-snippet-vs-shared-core carry (GOOD-MORNING ⑧, age 4), **not** new dead code from `s182-D2`.

---

## 7. CONDUCTOR SERIAL-SET EDITS NEEDED (I made none — [[regen-serial-set-is-ordered]])

Ordered. **1 is the one that stops the recurrence.**

1. **`GOOD-MORNING.md:343`** (spine, §C·1 ROUTING). Replace the exact substring
   `DV-J2b sparkline queued · DV-J1 table-idiom queued`
   with the record words, e.g. `DV-J2b sparkline SUPERSEDED (s182-D2) · DV-J1 table-idiom LANDED (#191)`.
   ⚠ The line is regenerated/checked — make the edit where the generator will keep it.
2. **`knowledge/components/chart-sparkline.meta.json`** — the 7 passages in §4. Item 7 (the anti-pattern)
   and `responsive.rule` are the load-bearing two.
3. **`knowledge/_REVIEW-SIGNOFF.md:282`** — annotate (never rewrite): width closed by `s184-D1`,
   **height-snap alone** still open. Header-wins/add-never-trim.
4. **`knowledge/_lanes.json`** DV-J2b successor list — strike the colour half, receipt `s182-D3`.
5. **PRICED, NOT BUILT — the gate fix.** Extend `_gen_lanes.check_routing_line` to parse the per-step
   words in each lane's parenthetical and assert them against `sequence[*].state`. ~15 lines beside
   `routing_expectations`; it is imported by the wrap gate, so one implementation covers both. **This is
   the only edit that prevents recurrence #5** — [[gate-dont-patch]], Dave #215: *"always real fixes never
   patches, they just get lost"*.

---

## RULING-SHAPED QUESTIONS (Dave's — none of these was ruled here)

1. **The 4px-grid height-snap.** `s184-D1` left it *"open direction, not ruled"*; heights stand at
   64px/44px and the render proof **pins them so nobody enacts a height ruling that was never made**.
   Rule it at the tuner, or park it?
2. **The trend-card composition.** `s182-D2` is explicit: *"might be a partially built trend card with
   option, I haven't decided yet"* — **FLOATED, NOT RULED**, and the table CTA's icon-button form waits
   on it. Build, or keep parked? ⛔ Never launder into a ruling.
3. **A live contradiction in the record, still unreconciled** (already flagged at `_REVIEW-SIGNOFF.md:282`,
   carried, not fixed): **`s151-D1` and `s149-D1` are inscribed MONO ONLY, while `s182-D3` keys the same
   red/green inks across ALL FOUR THEMES.** Which governs? ⛔ I touched nothing — the two-red law and the
   mono error ink camp are untouchable without his word.
4. **Should a component meta be allowed to restate live facts at all?** §4 is a second home for facts
   whose one home is the ruling store + the snippet — the **ADR-0017 WRITE-ONCE** shape. Correct-in-place,
   or thin the meta to addresses?

---

## UNPROVEN (honest, and therefore priced TODOs)

1. **I did not re-drive the corrected markup-anchored DV-J1 probe.** The #191 receipt claims *21 markup
   `<summary>` across 13 chart snippets, 0 off-idiom*. My crude comment-stripped count returned **47
   across 13** — it does **not** exclude `<script>`/JSON blocks, so **my number is the wrong instrument,
   not a contradiction**. DV-J1's `landed` state rests on Dave's #191 ruling and its receipt, not on any
   re-measurement by me. [[measure-dont-convert-units]]
2. **No per-theme visual specimen was captured.** The var gate proves no dangling var across all four
   themes and the render proof covers geometry; **neither is an eye on light+dark × 4 themes**. Not
   required for a discharge — declared because absence is never defaulted.

---

## REPLAY-THESE (verbatim, for the conductor's chat)

- **The sparkline lane is CLOSED and was closed five sessions ago — nothing was built today, on purpose.**
  DV-J2b is `superseded` (`s182-D2`), DV-J1 is `landed` (Dave's word #191). The word "queued" survives
  only in one line of prose at `GOOD-MORNING.md:343`.
- **The BLOCKING gate that exists for exactly this drift reads GREEN**, because it checks lane state
  words and never the step words. That is the recurrence engine, and it is a ~15-line fix.
- **The brief's build would have reversed a Dave ruling.** It asked for a toolbar on an atom whose ruling
  says *"it is not an analysis tool"* — and the toolbar it said to copy from scatter **does not exist**
  (`dv-toolbar` = 0 repo-wide).
- **One real defect found:** `chart-sparkline.meta.json` still documents the deleted table and a fixed
  340px width. **The browser measured 348/828/1368 against the meta's "fixed 340 baked"** — and two gates
  ran green over it.
- **The strand is green:** var gate 767 refs / 4 themes, snippet gate 135/0, dataviz gate PASS, render
  proof PASS.
