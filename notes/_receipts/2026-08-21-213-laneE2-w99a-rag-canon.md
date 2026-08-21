# Receipt — #213 LANE E2 · `W-99a`: G17 RAG manifestation A+B+C into canon (`s212-D2`)

> ⛔ **DATED RECORD, NOT A LIVE HOME.** Nothing here is a ruling. The store
> (`knowledge/_state.json`, `knowledge/_rulings.json`) stays the one live home; only
> `knowledge/_inscribe_ruling.py` writes rulings, and only on Dave's word.
> Lane: Opus sub, #213 mine-side burn-down fan-out. Conductor owns git + the serial set.

---

## 1 · Premise table (probe · result · when)

| # | premise to re-probe | probe run | result | when |
|---|---|---|---|---|
| P1 | `s212-D2` exists and says A+B+C | read `knowledge/_rulings.json`, id `s212-D2` | **CONFIRMED, quoted:** *"The RAG status canon pick, open since 2026-07-19, is A+B+C - all three manifestations are canon. … Enactment (wiring the pick into canon) is queued as its own store row."* `governs: [knowledge/_GOVERNING-RECORDS.md]` | 2026-08-21 |
| P2 | the G17 row is closed and points at `W-99a` | `grep -n "G17" knowledge/_GOVERNING-RECORDS.md` → line 33 | **CONFIRMED:** *"✅ **CLOSED #212** — `s212-D2` (canon pick **A+B+C** …). Enactment rowed `W-99a`."* | 2026-08-21 |
| P3 | what A, B and C actually ARE | read `reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1.REVIEW.html` (+ the non-REVIEW source for the markup) | **QUOTED, not re-derived** — see §2 | 2026-08-21 |
| P4 | where RAG status manifests in canon today | `grep -rn "rag-error-background\|rag-success-background\|…" knowledge/snippets/*.html` → **no output**; `grep -rn "rag-text-on\|rag/text-on" knowledge/ --include=*.html --include=*.py --include=*.json` → only `canon/canon.css` | **B and C did not exist.** Only the dot (`rag/*` bare roles) and the tint chip (`rag/*-tint`) manifested. The fill rung (`rag/*-background`) had **no snippet consumer at all** outside Banner/Alert-class message surfaces | 2026-08-21 |
| P5 | Status-indicator is the right home | read `knowledge/components/status-indicator.meta.json` + `knowledge/snippets/Status-indicator.reference.html` | **CONFIRMED** it is the existing RAG-coded atom (G17-A). ⚠ **Vocabulary collision found** — the snippet already had "form A/B/C" meaning *inline / tint chip / live-announced*, a 2026-06-22 taxonomy that is **not** G17's A/B/C. Handled by prefixing every G17 letter `G17-` and saying so in both files | 2026-08-21 |
| P6 | the ink-on-fill binding precedent | read `knowledge/snippets/Banner.reference.html` lines 106–109 + manifest | **CONFIRMED and COPIED VERBATIM** (never re-drawn): `err/warn → --on-light`, `success → --on-ok` (`text/on-success`), `info → --on-info` (`rag/text/on-information`, `s131-D1`) | 2026-08-21 |
| P7 | non-mono themes need the white error ink restated | read `knowledge/tokens/themes/apollo-*.overrides.json § guards.banner` | **CONFIRMED:** `s149-D1` is MONO ONLY and each theme restates white as a per-component **guard rule**, not a token override. A new fill component inherits mono's dark ink unless it carries its own guard | 2026-08-21 |

---

## 2 · What A, B and C are — quoted from the artefact, never re-derived

Source: `reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1.REVIEW.html` (the file `s212-D2` names as evidence).

- **Form A · Status-indicator — dot + label** — *"EXISTING CANON … The component that already exists and is RAG-coded … Label carries the meaning, so per R-D6 the dot's contrast relaxes … Lightest touch; best for inline / lists / accessibility."*
- **Form B · Filled cell / badge** — *"The salience-ramp fills (R-D8/R-D10): the whole cell carries the status. For dense tables / dashboards where a column IS the status and scan speed matters. This is where the fill colours, black/white text and the ramp live."*
- **Form C · Bar / edge accent** — *"Left-edge accent for **cards** and grouped rows where the whole object has a status. Colour + label (icon-013)."*
- **Excluded, do not re-litigate** — *"Tags surface KEYWORD DESCRIPTORS, not status"* · *"Pills/Chips are FUNCTIONAL (selection/filter)"* (ctkt / ctkt-018). Not drawn.
- Surface map, the artefact's own steer, adopted: *"A for inline / lists / anywhere a single status sits in text; B for status columns in dense tables (scan speed); C for cards."*

⚠ **The artefact's literal colours were NOT copied.** Its swatches are the July R-D10 hexes (`#B92F1E` etc.) and its breach cell carries `color:#fff`. Both are superseded by the ruled token layer (`s122-D2` re-base; `s149-D1`/`s194-D1` white-on-error abolished for mono). The enactment binds **tokens**, so each theme renders its own ruled values. Recorded in the meta `$g17.$note`.

---

## 3 · What landed (every claim carries its probeable token)

All edits are **UNCOMMITTED**. Files touched by this lane:

| file | change | evidence |
|---|---|---|
| `knowledge/snippets/Status-indicator.reference.html` | G17-B `.cell` + `.statustable` and G17-C `.sbar` blocks; 9 new manifest vars; 5 new `contrastPairs`; 4 new `knownFindings`; header note | `python3 knowledge/_validate_snippets.py` → `snippet gate: 135 snippet(s), 0 failure(s)` |
| `knowledge/components/status-indicator.meta.json` | `build.forms` gains `G17_A/B/C` + a `$note` naming the two taxonomies; new `build.$g17` block with `$status`, `excluded`, `$note`, `$proposed` | `python3 -c "import json;json.load(...)"` → `meta JSON ok`; `_validate_binds_resolve.py` exit 0 |
| `knowledge/tokens/themes/apollo-legacy.overrides.json` | guard `status-indicator` → `.cn-status-indicator .cell.err {--ink:var(--on-dark);}` | emitted at `canon.css:20944` |
| `knowledge/tokens/themes/apollo-console.overrides.json` | same err guard **+ a PROPOSED `.cell.inf` guard** (§6) | `canon.css:22630`, `canon.css:22638` |
| `knowledge/tokens/themes/apollo-supercharge.overrides.json` | same err guard **+ a PROPOSED `.cell.inf` guard** (§6) | `canon.css:25899`, `canon.css:25905` |
| `knowledge/canon/canon.css` | regenerated (components + theme cascade) — **never hand-edited** | `canon/gen_canon_components.py --check` OK · `canon/gen_theme_cascade.py --check` OK · `--selftest` OK |
| `knowledge/canon/gen_canon_components.py` | **out-of-lane class fix**, see §5 | driven, §5 |
| `reviews/RAG-STATUS-MANIFESTATION-ENACTED-2026-08-21-s213-v1.html` | NEW dated live specimen: 4 themes × light+dark, canon markup **copied out of the gated snippet by script**, never re-drawn (`specimen-starts-from-reference`) | rendered, §4 |

⚠ **The three theme-override JSON files were rewritten by a `json.dump(indent=2)` round-trip.** Key order is preserved (`object_pairs_hook=OrderedDict`); `guards` is re-sorted by key, matching the file's existing convention. The conductor should eyeball the diff before committing — this lane cannot run `git diff` (fence 1).

### Gate run, after the change

```
_validate_snippets.py                 exit=0  135 snippet(s), 0 failure(s)
canon/gen_canon_components.py --check exit=0  135 components in sync
canon/gen_theme_cascade.py --check    exit=0  228 override path(s), 386 component projection(s) in sync
canon/gen_theme_cascade.py --selftest exit=0  selftest OK
gen_token_ramp.py --check             exit=0  0 file(s) DRIFTED
gen_component_partials.py --check     exit=0  all AUTO-PARTIAL blocks in sync
_validate_no_hardcode.py              exit=0  11 tranche file(s)
_validate_dtcg.py                     exit=0  0 failure(s), 61 declared deferral(s)
_validate_palette_tier.py             exit=0
_validate_binds_resolve.py            exit=0  135 snippets / 2121 vars
_validate_radius.py                   exit=1  4 strict fail(s) — PRE-EXISTING, see §7
```

### The gate can FAIL on the clauses I changed (bites shown failing on mutants)

Two mutants, driven, then reverted:

1. drifted `--err-bg` `#F6604C → #F66040` ⇒ `❌ Status-indicator.reference.html: DRIFT --err-bg (light) = #F66040 but rag/error-background = #F6604C` (+ dark leg).
2. swapped the declared info pair to `rag/text/on-dark` ⇒ `❌ CONTRAST rag/text/on-dark on rag/information-background (light) = 2.47:1 < 4.5:1` (+ dark leg).

Green is therefore meaningful, not self-comparing (#171).

---

## 4 · Driven render proof — four themes, light + dark

Runbook followed: `knowledge/_RUNBOOK-render-verify.md` (symlink farm, `<include>` present — `fc-list` 404 faces / 10 HSBC, so the fallback stack is real and not the 10-face illusion). Renderer: `knowledge/_render/render.py` (its `document.fonts.check` assert passed; page rendered in the licensed HSBC cut).

**Not a screenshot claim — the page was DRIVEN.** 80 computed-style rows read out of the live DOM (`getComputedStyle`), every fill/ink pair scored with `knowledge/_contrast_utils.contrast_ratio`:

| theme | leg | fill | ink | ratio |
|---|---|---|---|---|
| mono | ok / warn / err / inf | `#66CC8D` / `#E0A61F` / `#F6604C` / `#78A7E8` | `#000000` / `#1A1A1A` / `#1A1A1A` / `#1A1A1A` | 10.59 · 7.99 · **5.55** · 7.04 |
| legacy | ok / warn / err / inf | `#00847F` / `#FFBB33` / `#A8000B` / `#305A85` | `#FFFFFF` / `#1A1A1A` / `#FFFFFF` / `#FFFFFF` | 4.56 · 10.28 · **7.87** · 7.17 |
| console | ok / warn / err / inf | `#5DAC7B` / `#D5990B` / `#B92F1E` / `#5A85C1` | `#000000` / `#1A1A1A` / `#FFFFFF` / `#1A1A1A` | 7.65 · 6.95 · **6.02** · **4.61** |
| supercharge | ok / warn / err / inf | `#5DAC7B` / `#D5990B` / `#B92F1E` / `#5A85C1` | `#000000` / `#13110E` / `#FFFFFF` / `#13110E` | 7.65 · 7.53 · **6.02** · **4.99** |

- **Light and dark measured separately for all four themes** (the fills are mode-invariant by `R-D7`/`s122-D2`; the G17-C bar ground and label do flip, e.g. mono `#F0F0F0`/`#1A1A1A` → `#1F1F1F`/`#FFFFFF`, supercharge `#DFDEDC`/`#13110E` → `#2A2621`/`#F7F6F4`).
- **`TEXT-PAIR FAILS: 0`** across all 80 rows.
- **`DANGLING: 0`** — no element resolved to `rgba(0,0,0,0)` where a fill was expected (#184 SILENT BLACK class, checked explicitly).
- G17-C edge width read as `4px` in every theme/mode; edge colours track each theme's bare rag role.
- PNGs at 1180 and 480 rendered and **looked at** (legacy light+dark crop read directly): layout sane, tables and bars correct, dark panels correct.

⚠ **THE FIRST HARNESS WAS WRONG AND ITS GREEN WAS A LIE.** Attempt 1 put `data-apollo-theme` and `class="cn-status-indicator"` on the SAME element; the cascade selector is a **descendant** combinator, so no theme applied and all four themes reported identical mono values — a fully plausible all-PASS table. Caught only by reading legacy's fill and asking why it was `#F6604C`. Recorded because it is the `green-tests-cannot-see-scope` class in a new dress.

**Repro:**
```bash
python3 knowledge/_render/render.py \
  reviews/RAG-STATUS-MANIFESTATION-ENACTED-2026-08-21-s213-v1.html out.png 1180 1200
```
(PNGs live in the sandbox `/var/tmp/out-s213e2/` — **NON-REPO**, `s191-D2`. One crop was staged at `_to_delete/s213e2-render-proof/crop-legacy.png` for the read and can be dropped.)

---

## 5 · ⛔ BLOCKING LIVE FINDING (pre-existing, out of lane, FIXED because it blocked the proof)

**Every `[data-apollo-theme]` rule in `canon.css` was dead in the browser. The whole four-theme cascade was inert.**

Discovered while the per-theme proof refused to differ by theme. Measured, first-hand, in Chromium against the live file:

| state | rules parsed from `canon.css` | `[data-apollo-theme]` rules reaching the browser |
|---|---|---|
| **before** (live repo, unmodified) | **4,094** | **0** |
| after removing one bad sequence | 4,524 | 0 |
| after removing the second | 7,229 | **792** |
| **after the generator fix, live file** | **7,243** | **792** |

**Cause.** Component `knownFindings` prose is emitted verbatim into the generated CSS header comment. CSS comments do not nest, so the **first `*/` in that prose closes the comment early** and everything after it parses as garbage — Chromium then drops every rule below. Two authored findings quoted shell globs ending in `*/`:

- `Payment-card-visual` (#204): `` `ls knowledge/assets/icons/**/ | grep -iE "chip|visa|…"` `` — `canon.css:12859`
- `Standing-order-mandate-row` (#209): `` `ls knowledge/assets/icons/*/ | grep -iE "recur|repeat|…"` `` — `canon.css:14254`

**This is ds-039 recurring.** The generator's own comment says the #122 fix stopped a harvest that was *"killing the CSS parser at that line and silently dropping EVERY rule after it (the whole AUTO-THEMES block included)"* — but that guard only refuses a literal `<`. A glob ending `*/` walks straight past it. **No gate parses `canon.css` as CSS** ([[no-gate-parses-the-artefact]]), so this survived two sessions and every green build.

**Fix applied — in the GENERATOR, not the artefact** (`ds-018` lesson): `knowledge/canon/gen_canon_components.py` gains `cmt(text)`, applied to Aria / Reuses / Finding / Drift header lines, which rewrites `*/ → * /`. Plain ASCII and visible on purpose — an invisible (zero-width) fix is how this class survives the next audit.

**Mutation-proven by DRIVING it:** a `*/`-bearing finding injected into the Status-indicator manifest, regenerated, then measured in the browser — raw sequence count `0`, neutralised form present, and the sheet still parses **7,243 rules / 792 themed**. The fail arm is the two real historical cases above (4,094 / 0), not a fixture.

⚠ **This repair is OUT OF LANE E2's SCOPE and the conductor may back it out** — it is one added function plus four call sites in `gen_canon_components.py`, and the canon.css delta that follows from re-running the generator. It is reported rather than quietly folded in because it changes ~3,100 CSS rules' visibility across the whole system. **It was not optional for this lane:** without it, "driven render proof per theme" is unachievable, and any G17 theme guard would be dead on arrival.

⬛ **PROPOSED, NOT BUILT:** a gate that parses `canon.css` with a real CSS parser and asserts (a) rule count within a band, (b) `[data-apollo-theme]` rules > 0. That is the instrument this class has now evaded twice. `_DS-IMPROVEMENTS.md` candidature is fenced from this lane — Dave's.

---

## 6 · Open choices — PROPOSED, NOT RULED

**P-E2-1 · One atom or three components?**
The artefact's closing steer was *"spec the cell/bar as gated components"* — i.e. **two new components**. This enactment instead extends the existing gated Status-indicator snippet. Reasons: no new registry / `CATEGORIES` / `MIGRATED_SNIPPETS` / doc rows are needed (all conductor-owned shared files), one atom keeps one job, and List-items already reuses this atom's chip. Splitting later is a pure move of the CSS blocks. **Dave's call.**

**P-E2-2 · The console + supercharge information ink (a live sub-AA leg this work exposed).**
`rag/text/on-information` is overridden to `#FFFFFF` in console and supercharge, while the shared-map information **fill** is `#5A85C1`. **White on `#5A85C1` measures 3.78:1** — under the 4.5:1 text floor, and neither theme carries a Legacy-style exemption (`R-D24` is legacy-only). I did **not** ship that: the G17-B info cell carries a guard seating its ink on `rag/text/on-light` instead — **console 4.61:1, supercharge 4.99:1, both measured on the live render**. The guard's `$note` in each override file says PROPOSED, NOT RULED, in full.
⚠ **The same 3.78:1 leg already exists on `.cn-banner .banner.info` in both themes and was NOT touched.** The question for Dave, in his terms: *is the fix per-component (as shipped here), or upstream — either re-seating `rag/text/on-information` for console/supercharge, or re-hueing the information fill?* Until he rules, canon carries two different answers for the same pair, which is exactly the sort of split that should not sit unattended.

**P-E2-3 · Neutral / cancelled has no fill.**
`rag/neutral` has no `-background` sibling, so G17-B's cancelled row falls back to the dot+label rather than invent a token. This is the same shape as the long-standing `rag/neutral-tint` gap already logged in the meta. **Not invented around.** Whether to mint `rag/neutral-background` (+ `-tint`) and complete the set is Dave's.

**P-E2-4 · Row edits I am NOT making (fence: `_GOVERNING-RECORDS.md` row-state is the conductor's).**
Exact edit proposed for the **G17** row (line 33), appended to the existing status cell, nothing trimmed:

> `✅ **CLOSED #212** — s212-D2 … Enactment rowed W-99a.` **→ append:** `⚙ **ENACTED #213** (lane E2, uncommitted): G17-A/B/C wired in `snippets/Status-indicator.reference.html` + regenerated canon; per-theme guards in the three override sets; driven render proof 4 themes × light+dark, 80 computed rows, 0 fails — `notes/_receipts/2026-08-21-213-laneE2-w99a-rag-canon.md`. Two items PROPOSED-not-ruled: the one-atom-vs-two-components split, and the console/supercharge information ink (3.78:1 upstream leg).`

Also proposed, for the conductor's store pass: a `_state.json` row (or `home` pointer on `W-99a`) naming the new artefact `reviews/RAG-STATUS-MANIFESTATION-ENACTED-2026-08-21-s213-v1.html`, so it cannot join the forgotten-document class (#185). The doc-row gate's population is `notes/_briefs/*` + `_BRIEF-*` only, so this file is **outside** the gate — which is precisely why it needs the row by hand.

---

## 7 · Residuals declared

1. **`_validate_radius.py` is RED with 4 strict fails — PRE-EXISTING, NOT MINE.** `grep -c "border-radius:0" ` returns **4 in the pre-change snapshot and 4 after**; offenders are `.cn-hero-variants` (×2) and `.cn-stats-band-lockup` (×2). Untouched.
2. **`_build_all.py` was NOT run to completion** — it exceeded the sandbox call budget (timed out at ~178 s). Bounded verification (`s172-D3`) was used instead: the ten gates in §3 that this change can actually break, plus two mutants. **The full build is UNPROVEN by this lane and the conductor must run it before committing.**
3. **`canon.css` now contains OTHER LANES' OUTPUT.** Regenerating from the snippets picked up work that landed in the same working tree while E2 ran — `--ring → --avg-ring`, `--scrim → --cp-scrim`, `--rule → --cp-rule` (lane E3's collision renames) and `--data-control-label-disabled` changes (lane E1's shape). **No lane's `canon.css` is its own.** Regeneration is deterministic, so the conductor should re-run `gen_canon_components.py` → `gen_theme_cascade.py` → `gen_token_ramp.py` **once, after all lanes have landed**, rather than trust any lane's copy.
4. **Theme-override JSON round-trip** — see the ⚠ in §3.
5. **`_to_delete/s213e2-render-proof/crop-legacy.png`** staged for the visual read; the sandbox cannot `rm`. Droppable.
6. **UNPROVEN BY SCOPE:** the G17 forms were driven in Chromium only, at 1180 and 480, in the specimen page. They have not been exercised inside a real composed template, and no gate reads them there.

---

## 8 · Serial-set steps this work obligates (conductor's; NOT run here)

| serial step | needed? | why |
|---|---|---|
| **registry** (`component-types.json`) | **NO** | no new component minted; Status-indicator is `interactive:false` and injects no partial |
| **`MIGRATED_SNIPPETS`** (`_validate_radius.py`) | **NO** | Status-indicator's new radius binds `var(--border-radius-indicator)`; the radius gate's 4 fails are elsewhere and pre-existing |
| **`CATEGORIES`** (`gen_showroom.py`) | **NO** | no new snippet file |
| **spine / store** | **YES** | (a) `W-99a` → enacted-pending-Dave; (b) the G17 row edit in §6 P-E2-4; (c) a row/home for the new review artefact |
| **git** | **YES** | one commit, conductor's, after a full `_build_all.py` |
| **⚠ extra, because of §5** | **YES** | the `gen_canon_components.py` fix + its ~3,100-rule canon delta should be called out in the commit message as its own thing, not buried in a G17 enactment |

---

## 9 · Pitfalls replayed (Dave #165) — and what actually bit

- **#202 (argued about a component that didn't exist)** — every premise re-probed first; P4/P5 changed the plan (B and C did not exist; the A/B/C letters collided).
- **#184 (dangling `var()` renders silent black)** — checked explicitly in the drive: `DANGLING: 0`.
- **#171 (self-comparing asserts pass on their own mutants)** — two snippet mutants shown FAILING before green was accepted.
- **#104 / #209 (a mutation test proves the CLAUSE, not the FEATURE — DRIVE THE THING)** — **this one bit twice.** The first harness produced an all-PASS table with the theme layer inert, and the first diagnosis of §5 (the orphan `display:inline-flex` lines in three snippets) was **wrong** — removing them changed nothing. Only driving the browser found the real cause. Both are recorded rather than tidied away.
- **ds-018 / generator hand-patching** — the §5 fix went into the generator; `canon.css` was never hand-edited.
- **#210 (ordered serial set)** — not run here; obligations named in §8.
