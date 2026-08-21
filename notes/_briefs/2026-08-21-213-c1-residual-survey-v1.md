# §C·1 RESIDUAL SURVEY — what of strands (a)–(d) is genuinely still open after waves 3–6

> ⛔ **DATED PERIOD RECORD, NOT A LIVE HOME.** Written 2026-08-21 by the #213 LANE S survey sub
> (Opus, READ-ONLY). The store stays the one live home (`knowledge/_state.json`, `knowledge/_rulings.json`).
> **Nothing here is a ruling.** Nothing here was built. Every LANDED verdict carries a probeable token;
> every unmatched grep is named as a probe, per [[unmatched-grep-is-not-an-absence]].

| governance | value |
|---|---|
| serves | `notes/_briefs/2026-08-21-213-mine-burn-fanout-brief-v1.md` § LANE S |
| lane record | `knowledge/_lanes.json` → `lane-2-apollo-charts` · state `active` · item `§C·1 strands (a)–(d)` = `queued` |
| strand text surveyed | `GOOD-MORNING.md:342–361` (a/b/c/d, with their `qprobe` declarations) |
| lane view | `_LIVE-STATE.md:33` (`⏳ §C·1 strands (a)–(d) … queued`) and `:34` (lane `until:` clause) |
| size bands | `s168-D2/D3` job-window tokens: **S** ≲40K · **M** ~40–100K · **L** ≳100K (sub spend excluded) |

---

## 0 · HEADLINE

**Three of the four strands' BUILD halves are done. What is left is almost entirely DAVE'S EYE and one
missing ADR.** Waves 3–6 put 43 new artefacts on disk and the conductor's serial set (canon projection,
KG, showroom) genuinely ran — that was the largest declared gap at #210 and it has since closed. The lane
cannot close because:

1. every wave's output ships **PROPOSED-not-ruled** and its store rows are **parked awaiting Dave** (W-63, W-71…W-74 open; W-75…W-84 parked);
2. **59 component metas sit outside `CATEGORIES`** (showroom "More" bucket) — deliberate, and unblocked only by Dave's promotion word;
3. strand (c)'s **ADR does not exist** (no `ADR-0018` in `docs/decisions/`) and is gated by the §C·2 ruling batch, which is Dave's;
4. the derived itinerary snapshot is **eleven waves stale** and would false-brief the next conductor.

---

## 1 · STRAND (a) — CHART-EXPANSION PROGRAMME

**Verdict: LANDED for both its ruled steps · two items FENCED/PARKED by earlier rulings · residual chart work lives OUTSIDE this strand.**

| claim | evidence pointer |
|---|---|
| STEP 1 done | `GOOD-MORNING.md:343` `<!-- qprobe: state=landed receipt=00abdf3 -->` — scatter exemplar end-to-end |
| STEP 2 (wave 2) landed | `GOOD-MORNING.md:348` `<!-- qprobe: state=landed receipt=df44e51 -->`; the divvy text below it is struck-through and marked "⛔ not a plan" since #196 |
| 8 wave-2 chart families on disk | `knowledge/components/Chart-{boxplot,bullet,butterfly-h,butterfly-v,candlestick,histogram,scatter}.meta.json` present (probe: `ls knowledge/components | grep Chart-`) |
| ds-020 still fenced | `knowledge/_DS-IMPROVEMENTS.md:1317` — "Chart-scatter is the only cartesian chart still drawing axis + grid the pre-DV-D07 way (2026-07-28, #27, measured)" |
| heatmaps parked | `_FUTURE-STATE.md:330–343` — heatmap tuner + deliberate deferral out of the chart build-out |
| DV-D07 mint candidate STRUCK | `GOOD-MORNING.md:360` — already enacted 2026-07-23, `semantic-colour.json:2035–2075` |

**OPEN under (a): nothing that belongs to this strand.** ⛔ Do not re-fire a chart wave off line 348 — that
line has now been mis-read as an open divvy plan **twice** (#26, #196; `_LIVE-STATE.md` records the second
recurrence explicitly). The live chart residual is carried by its own store rows, **not** by §C·1(a):
`W-02` (dv-legend/dv-behaviour ceiling) · `W-03` (ds-012(b) gutter) · `W-04` (DV-D16 floating growth) ·
`W-97` (bar-motion half) · `W-98` (dv-lockup wave, awaiting Dave's 3 titles).

**Size if Dave wants ds-020 unfenced:** M (axis/grid idiom rewrite on Chart-scatter + a four-theme render
proof + the copy-inheritance note every wave lane was warned about at `GOOD-MORNING.md:347`).

---

## 2 · STRAND (b) — WAVE 3 FAN-OUT (component library)

**Verdict: BUILD LANDED · BLOCKED-ON-DAVE for promotion.**

| claim | evidence pointer |
|---|---|
| all 9 wave-3 components exist | `knowledge/snippets/{Transaction-row,Standing-order-mandate-row,Limits-meter,Range-slider,Rating,Transfer-list,Split-button,Fab,Back-to-top}.reference.html` — probe: `ls knowledge/snippets/`, 9/9 present |
| receipts exist | `notes/_receipts/2026-08-20-209-wave3-lane{A,B,C}-*.md` |
| brief + receipts have a store row | `W-62` (open, claude) |
| the wave itself is Dave's | `W-63` (open, dave) — "wave-3 NINE components BUILT PROPOSED-NOT-RULED … TWO EXISTENCE QUESTIONS from Lane A" |
| heavy 7 (wave 4) also landed | `knowledge/snippets/{Calendar,Tree,Cascader,Carousel,Qr-code,Splitter,Image-block}.reference.html` — 7/7 present; rows `W-71`/`W-72`/`W-73`/`W-74` (open, dave) |

**OPEN under (b):**
- **(b1) Dave's eye on 16 components + the two existence questions** — **BLOCKED-ON-DAVE**, rows `W-63` (wave 3) and `W-74`/`W-71`/`W-72`/`W-73` (wave 4). Not agent work.
- **(b2) A review surface to make that eye possible.** ⚠ **Probe run:** `ls -t reviews/` — the newest wave-related review artefact is `REVIEW-210-existence-side-by-side-v1.html`; there is **no four-theme review page covering the 43 new components**, and the last four-theme review pages in the repo are `REVIEW-203-*-four-themes-v1.html`. Under [[review-live-variant-spread]] and [[feedback-live-controller]] Dave cannot rule 43 components from receipts. **Size: M** (one generated review page, live specimens, four themes × light/dark, per-component PROPOSED/RULE control).
- **(b3) Itinerary re-measure.** `reviews/ITINERARY-STATUS-2026-08-19-v1.json` still reads `$session "#203 Wave 3b Lane H"`, `$counts {GATED 94, NO-ARTEFACT-CLASS 28}`, `$true_gaps [86]` — measured **before** waves 3/4/5/6. Its generator `knowledge/gen_itinerary_status.py` exists and is re-runnable. [[premise-ages-faster-than-rule]] — this exact class false-briefed 6 lanes at #203. **Size: S.**

---

## 3 · STRAND (c) — TEMPLATES + SHELLS CLEAN-ROOM (Layer-2)

**Verdict: THE ARTEFACTS LANDED (waves 5+6) · THE STRAND ITSELF — an ADR — IS STILL OPEN and BLOCKED-ON-DAVE.**

The strand as written (`GOOD-MORNING.md:357–358`) is *"solo Fable ADR-style session … Best AFTER the ruling
batch: field-family, stepper-fold and delta-seam answers shape it."* Waves 5/6 built the **components** the
ADR would govern; they did not write the ADR.

| claim | evidence pointer |
|---|---|
| 7 app shells on disk | `knowledge/snippets/App-shell-{top-nav,side-nav,multi-column,split,focused,doormat,nav-rail}.reference.html` |
| 11 templates on disk | `knowledge/snippets/Template-{dashboard,list-index,detail,create-edit,wizard,auth,settings,empty,error,report,confirmation}.reference.html` |
| 9 lock-ups on disk | `knowledge/snippets/{Page-header-lockup,Filter-toolbar-bar,Footer-doormat-lockup,CTA-lockup,Feature-grid-lockup,Section-heading-lockup,Card-header-lockup,Hero-variants,Stats-band-lockup}.reference.html` |
| library now 135 snippets | probe: `ls knowledge/snippets/*.reference.html \| wc -l` → **135** |
| **the #210 "largest single gap" is CLOSED** | wave-5 lane B receipt §9 item 1 said *"no `.cn-template-*` block exists in `canon/canon.css`, so theme-cascade projection is silently OFF"*. Re-probed today: `grep -c` on `knowledge/canon/canon.css` → **cn-template 1528 · cn-app-shell 696 · cn-calendar 41 · cn-tree 57 · cn-transaction-row 45 · cn-carousel 44 · lockup 350**. The conductor projected them. |
| **KG residual CLOSED** | receipt §9 item 2 named 5 unseen contexts. Re-probed: `business-banking-overview`, `account-overview-screens`, `payments-screens`, `payment-detail-screens` each present in `knowledge/components/_nodes-context.json`; `statement-archive` present in `knowledge/components/_nodes-pattern.json` (it is a pattern, not a context — its absence from the context registry is correct, not a gap). |
| showroom regenerated | `showroom/{template-dashboard,app-shell-top-nav,calendar,tree,split-button,feature-grid-lockup,…}.html` all exist, mtime ≥ 2026-08-20 |
| rows are PARKED, not open | `W-75`…`W-84` all `state: parked`, `owner: dave` (the #212 desk triage) |
| **⛔ no ADR exists** | **probe: `find . -iname "ADR-00*" -not -path "./.git/*"`** → 17 ADRs, `ADR-0001`…`ADR-0017`, **no ADR-0018 and nothing named templates/shells**. `W-0b` independently says findings 3+4 *"merge with the templates/shells zero tier (one missing capability, three symptoms — ADR-shaped)"*. |

**OPEN under (c):**
- **(c1) The clean-room ADR itself — BLOCKED-ON-DAVE.** Row: `W-08` item (ii) — *"§C·2 RULING BATCH 15 + 17–22 — unmoved for days, **gates §C·1(c)**"* (`GOOD-MORNING.md:105`). The gating is explicit in Dave's own queue text. Model when unblocked: **Fable**, solo. **Size: L.**
- **(c2) `CATEGORIES` placement for 59 metas — BLOCKED-ON-DAVE (promotion), then S to enact.** **Probe:** parsed `CATEGORIES` out of `knowledge/gen_showroom.py:127` → 84 categorised slugs vs 136 metas in `knowledge/components/` → **59 metas fall to the "More" bucket**, including every wave-3/4/5/6 organism and the 7 chart families. Wave briefs made this deliberate ("CATEGORIES unregistered (More bucket) per the #204 precedent"), so it is **not a defect — it is the promotion step Dave's ruling unlocks.**
- **(c3) A Layer-2 artefact class has no gate of its own.** Wave-5 lane B receipt §9 item 8, verbatim: *"Nothing checks that a template composes rather than re-draws — the diff-proof in §6 is a script in a receipt, not a gate, and it dies with this session unless someone homes it."* Two receipts (`wave5-laneB`, `wave6-laneB`) each carry a re-runnable diff-proof script in prose. [[instrument-without-a-consumer]] + [[no-gate-parses-the-artefact]]. **Size: M** (home one script, drive it on a mutant, wire ADVISORY).
- **(c4) `MIGRATED_SNIPPETS` coverage — MEASURED, VERDICT HONESTLY UNPROVEN.** **Probe:** parsed the set literal at `knowledge/_validate_radius.py:46` → 81 entries; 135 snippets on disk ⇒ **54 absent**, including all wave-4/5/6 organisms. ⚠ **But** pre-wave atoms (`Accordion`, `Avatar`, `Divider`, `Tooltip`, `Pagination`) are also absent, so absence does **not** prove a defect — the set may be scoped to radius-rebound snippets only. **Do not act on this number without reading `_validate_radius.py:23` and `:228` first.** **Size to resolve: S.**
- **(c5) Cross-wave defect residuals still live at source.** Wave-5 lane B §9 item 9, verbatim: *"⛔ THE DEFECT IN `Layout-utilities` IS STILL THERE. So is the one in `Timeline` and `Document-row`."* Partially addressed by #211 lane R2 (`W-90` — `.l-split` container self-query repaired at cause), so **re-probe before scoping**: the R2 receipt claims 8 consumers repaired from one file. **Size: S–M after re-probe.**
- **(c6) Four-theme SEEN, not just projected.** Both wave-5/6 lane-B receipts declare console/legacy/supercharge **UNPROVEN by render** for all their pages. Projection now exists (c-table above), so this is now a *render-and-look* job, not a wiring job. Folds naturally into **(b2)**. **Size: folded into (b2).**

---

## 4 · STRAND (d) — ENACT WINDOW (cheap)

**Verdict: PART-CONSUMED · its headline input is BLOCKED-ON-DAVE · a real S-sized agent-owned tail survives.**

Strand text: *"absorb §C·2 rulings as token/registry edits + §C·4"* plus four named candidates.

| candidate (`GOOD-MORNING.md:359–361`) | verdict | evidence |
|---|---|---|
| mint `data/axis` + `data/grid` | **STRUCK — already enacted** | `GOOD-MORNING.md:360`, `semantic-colour.json:2035–2075` (third recurrence of the stale-queue class, found #199) |
| **R-D9 ramp promotion** | **OPEN, and it COLLIDES with this session's LANE E2** | R-D9 is the RAG salience ramp: `knowledge/_ENACTMENT-REGISTER.md:83` reads `R-D9 \| **UNPROVEN**`; bodies at `knowledge/_proforma/_RAG-DECISIONS.md:675,733`, `_DS-IMPROVEMENTS.md:237,251`. ⛔ Lane E2 (`W-99a`, s212-D2) is wiring RAG A+B+C into canon **right now** — do not fire an R-D9 lane in the same window. |
| **Stat-card `spark` slot** | **OPEN — genuinely absent** | **Probe:** `grep -ic spark knowledge/snippets/Stat-card.reference.html` → **0**; `grep spark knowledge/components/stat-card.meta.json` → no match. Note `s182-D2` ruled the sparkline "an atom alone" and moved the table CTA to a future trend-card — so **the slot's shape is arguably Dave's, not enactment.** |
| **live radius/corner tuner v2** | **PART-DONE** | v1–v4 exist: `reviews/RADIUS-CORNER-TUNER-2026-08-18-v{1,3,4}.html` + v4 render png; `s199-D3` console radii ENACTED. The **segmented-switch radius carve-out** is the v2 remainder and Dave tunes it — [[live-radius-corner-tuner]] is a NOTICE-UNPROMPTED refusal, not a lookup. **BLOCKED-ON-DAVE.** |

**§C·4 standing carries — re-probed today, and two have gone stale-green:**

| §C·4 item | verdict | probe |
|---|---|---|
| `s155-D1` mono green fork ENACTMENT (`GOOD-MORNING.md:418`, still reads "Ruled, NOT enacted") | **⚠ APPEARS ENACTED — the queue line is stale** | `grep -rl 137F3C` → `knowledge/canon/canon.css`, `knowledge/tokens/semantic-colour.json`, `knowledge/tokens/palettes/rag/mono.json`; `66CC8D` likewise + `knowledge/canon/gen_theme_cascade.py`, `knowledge/tokens/themes/_themes.json`. **Assertion-propagation class, 4th sighting.** Correcting the queue line is the conductor's. |
| CI survey/browser tidy-up, "known gap" prose (`:419`) | **half DONE** | `knowledge/_tests/test_gates.py:20–27` now reads *"Since #155 the CI `render` job … BLOCKING … no longer untested in CI"* — the FALSE prose is corrected. Whether the gates job still goes red browserless is UNPROVEN here (no CI read). |
| Actions runtime bump (`:420`) | **OPEN, trivially** | `grep -n "checkout@v\|setup-python@v" .github/workflows/*.yml` → `checkout@v4` ×2, `setup-python@v5` ×2. Not bumped. |
| `s114-D5` hit-area measurement redesign (`:421`) | **OPEN, agent-owned** | brief exists: `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md` (pending half); one build owns both the 6 phantom failures and the `axs-003` quirk |
| `s163-D1` cross-instrument claim check (`:407`) · `s142-D1` aesthetic leg 113 unseen rows (`:408`) | **BLOCKED-ON-DAVE** | both carry explicit `until: Dave rules…` clauses |

**Sized OPEN work under (d):** an **S** enact lane = Actions bump + Stat-card spark slot **scoped-not-built** +
the §C·4 stale-line corrections handed to the conductor. `s114-D5` is its own **M**.

---

## 5 · WHAT ACTUALLY BLOCKS `lane-2-apollo-charts` FROM CLOSING

The lane record's `until:` clause (`_LIVE-STATE.md:34`) is *"lands when DV-J1/DV-J2 + the §C·1 strands ship."*
DV-J2 is `landed`, DV-J1 is `landed`, DV-J2b is `superseded` (s182-D2) — **§C·1 is the sole remaining blocker,
and §C·1's own remaining mass is Dave's eye plus one ADR.** The honest statement for the next opener:

> **§C·1 is BUILD-COMPLETE for (a) and (b), BUILD-COMPLETE-BUT-UNGOVERNED for (c), and PART-CONSUMED for (d).
> Nothing large is agent-buildable inside §C·1 today without Dave first ruling the 43 proposed components
> and the §C·2 batch.**

---

## 6 · PROPOSED DIVVY PLAN — for the conductor to fire next

⛔ PROPOSED, not ruled. Every shared file is assigned to **exactly ONE** lane; the serial set is the
conductor's alone. Fire order matters only where noted.

| lane | model | job | OWNS these files (nobody else touches them) | size |
|---|---|---|---|---|
| **R — the review surface** ⭐ fire first | **Opus** | Generate ONE live review page over the 43 wave-3/4/5/6 components: four themes × light/dark, live specimens copied from the approved artefacts ([[specimen-starts-from-reference]] — ⛔ never re-draw), a per-component PROPOSED / RULE / DEFER control, and export. This is what unblocks W-63, W-71…W-84 in one sitting. | NEW `reviews/REVIEW-213-wave3-6-four-themes-v1.html` + NEW `notes/_receipts/2026-08-21-213-laneR-*.md` (+ a NEW generator under `knowledge/_render/` if it writes one) | **M** |
| **I — itinerary re-measure** | **Sonnet** | Re-run `knowledge/gen_itinerary_status.py` and emit a **v2-dated** status snapshot; report the delta vs the #203 v1 in the receipt. ⛔ do not overwrite the v1 files (version-don't-overwrite); ⛔ the `.xlsx` is FROZEN read-only. | NEW `reviews/ITINERARY-STATUS-2026-08-21-v2.{json,html}` + NEW receipt. READ-ONLY on `gen_itinerary_status.py` | **S** |
| **G — the Layer-2 gate** | **Opus** | Home the composes-vs-re-draws diff-proof that lives as prose in the wave-5/6 lane-B receipts (§6 of each) as a real script under `knowledge/`, drive it on a MUTANT so it can be seen to FAIL ([[mutation-tests-the-clause-not-the-feature]]), wire ADVISORY only. | NEW `knowledge/_validate_layer2_composition.py` + NEW receipt. ⛔ does NOT edit `_build_all.py` (conductor's) | **M** |
| **N — the small enact tail** | **Sonnet** | Bump `checkout@v4→v5`, `setup-python@v5→v6`; re-probe whether the gates job still reds browserless and report; scope (never build) the Stat-card `spark` slot against `s182-D2`; hand the conductor the exact stale-line corrections for `GOOD-MORNING.md:418` (s155-D1 appears enacted). | `.github/workflows/gates.yml` + NEW receipt. ⛔ **never edits `GOOD-MORNING.md`** — it reports the correction | **S** |

**STAYS SERIAL — conductor only, ONE commit:** `_validate_radius.py` `MIGRATED_SNIPPETS` · `gen_showroom.py`
`CATEGORIES` · the spine · `knowledge/_state.json` / `_rulings.json` / `_lanes.json` · `GOOD-MORNING.md` ·
`_LIVE-STATE.md` · `MEMORY.md` · `_CHAIN.md` · git. Per [[regen-serial-set-is-ordered]] run the **whole**
serial per wave, ramp first, index last.

**DO NOT FIRE THIS WINDOW (collisions with the live #213 lanes):**
- ⛔ any **R-D9 / RAG** lane — LANE E2 (`W-99a`) owns RAG canon right now;
- ⛔ any lane touching `--text-disabled` / `--border-disabled` or the disabled block generator — LANE E1 (`W-99`) owns it;
- ⛔ any local-var rename or `_TOKEN-FORK-LEDGER.json` edit — LANE E3 (`W-59`) owns it, and wave-5 lane B §7 proposes a **sixth** ledger member that E3 must be told about;
- ⛔ `CATEGORIES` promotion, ds-020 unfencing, the templates/shells ADR, the tuner v2 carve-out — **all four wait on Dave.**

**BLOCKED-ON-DAVE, one list for the chat read-back:** `W-63` · `W-71` · `W-72` · `W-73` · `W-74` (wave 3+4 eyes,
incl. 2 existence + 38 open questions) · `W-75`…`W-84` parked (wave 5+6 eyes) · `W-08`(ii) §C·2 batch 15 + 17–22
**gating strand (c)** · `W-98` dv-lockup titles · the tuner v2 segmented-switch carve-out · `s163-D1` successor ·
`s142-D1` aesthetic leg.

---

## 7 · RESIDUALS OF THIS SURVEY — declared, not smoothed

1. **No gate or validator was RUN.** Every verdict above is a file/grep/parse probe. `_validate_binds_resolve.py`
   check D, `_validate_kg.py` and `_validate_state_contrast.py` were **not executed** (they rewrite tracked audit
   files, outside a READ-ONLY lane's fence). "Projection exists in canon.css" is a **presence** claim, not a
   **resolves** claim — [[unmatched-grep-is-not-an-absence]] cuts both ways.
2. **Nothing was rendered.** The four-theme claim in §3 is that the *cascade blocks exist*, not that the pages
   have been *seen*. That is exactly why lane R is proposed first.
3. **No git history was read** (fence 1). Every "landed" verdict rests on the working tree as of 2026-08-21,
   not on commits.
4. **`MIGRATED_SNIPPETS` (c4) is measured but its meaning is UNPROVEN** — stated as such rather than resolved.
5. **§C·4 was surveyed, not exhausted.** `GOOD-MORNING.md:404–421` carries a restored ~35-item tail (#166) that
   this survey did not walk item-by-item; only the items strand (d) names were probed.
6. **Sizes are planning estimates, not measurements** [[planning-estimate-is-not-a-measurement]].
