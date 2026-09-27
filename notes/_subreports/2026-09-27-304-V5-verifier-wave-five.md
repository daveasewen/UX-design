# #304 V5 — verifier, wave five: W5a PASS WITH FIXES (disclosures, one optional narrowing) · W5c PASS WITH FIXES (one title bug, wiring order) · W5b PASS WITH FIXES (four corrections, the slot's contents)

provenance: 304 · Sunday 2026-09-27 · seat V5 (Fable 5.1, verifier; built none of wave five) · mount HEAD `ff382c0b` (NOT `3100da99`: the scheduled dream pass 14 committed on top at 07:29 BST — 3 files, `notes/_dream/2026-09-27-proposals.md`, the rehearsal log, the schematic) · fresh throwaway clone `$HOME/v5` (`git clone --shared`, full history, at `ff382c0b`) with W5a's 41 files + W5c's 5 + the three lane dirs + the sitting page overlaid, W5c's wiring applied, the C1 serial regenerated, three clone commits (`5939be6d` overlay, `6e3c8429` wiring, `a4a851d4` serial) · a sparse worktree `$HOME/v5head` at `ff382c0b` for HEAD-side controls · writes on the mount: this report and `notes/_lanes/304/V5/` only · no git writes, no `_build_all.py`/survey/`--wrap` on the mount, no Project memory
status: observed — every figure below was printed by a gate, a selftest, the survey, the harness or a browser probe at the seat, receipts under `notes/_lanes/304/V5/`
DECLARED SLIP: one `git status --porcelain | head -0` ran on the mount in my first minute (a reflex in a compound command). It wrote nothing visible: no `.git/index.lock` exists after it, and every mount file I later compared still equals HEAD or the lane's clone commit. Named here so nobody else has to find it.

## THE VERDICTS

| seat | verdict | what the commit seat does |
|---|---|---|
| W5a | **PASS WITH FIXES** | commit all 41 as they are (bytes == its clone commit `2a8d2b59`, 41/41). The fixes are DISCLOSURES on Tuesday's page (§2), plus one optional narrowing if Dave's eye refuses the root change. |
| W5c | **PASS WITH FIXES** | commit the 5 files + lane dir; then run `python3 notes/_lanes/304/W5c/tools/wire_kg_generators.py .` (W5a did NOT touch `_build_all.py`, mount == HEAD, so the order constraint is moot — wire in the same commit). One title bug to fix before or after (§3). |
| W5b | **PASS WITH FIXES** | the page ships, with four corrections and the slot filled (§4). |

Survey (§1): 152 steps in the clone, **0 green→red against V4's set by step name**, the 4 new wired steps pass. `.git/index.lock` (§5): gone; made by the dream pass's own `git status` at 07:14 BST, cleared by its commit at 07:29.

## 1 · THE SURVEY — fresh clone, W5a + W5c + wiring + serial, all 152

Chunks 1:30 · 31:70 · 71:100 · 101:128 · 129:141 · 142:152 (`survey/after_*.log`), `--include-mutating --resume --timeout 60`, HSBC face at the seat.

- FAIL: `[81]` 4px-grid · `[90]` token fork-ban · `[98]` roles/answers · `[131]` `[132]` delta-audit ×2 · `[136]` integrity lint · `[138]` probe registry · `[139]` claim-table linter · `[148]` pack ship-list = the same nine as V4/W5a/W5c (numbers shifted +4 after `[85]`). Could-not-ask `[10] [13] [61] [68] [140]`; timeout `[73]`. Every red detail block identical to V4's (`survey/compare-v4-v5.txt`) except two, both explained:
  - `[129]` schematic determinism went red in my run ONLY because my chunk boundary fell between `[128]` (writes the schematic) and `[129]` (checks it) and the verdict ledger moved at the chunk end; re-run `--range 128:130` in one chunk: **3/3 pass** (`survey/after_128_130.log`). A chunking artefact, not the diff. Note for anyone chunking: keep 128 and 129 together.
  - `[139]` claim-table linter read "3 rc/observation mismatch" v V4's 4. The linter SAMPLES 20 rows ("8 of 20 sampled rows were NOT run"); run directly it printed 4 again. Sampling noise, not the diff.
- The four wired steps: `[86]` token drift check · `[87]` token selftest (8 bites) · `[88]` title drift check · `[89]` title selftest (12 bites) — **all ✅**. `_build_all.py --selftest`: "exact-ID failure routing over 152 steps" PASS. `wire_kg_generators.py --check` after wiring: already wired; idempotent.
- Serial regen in the clone rc 0 ×6; `_CHAIN.md` 7,800 tk (dream pass's 14th record adds 3 tk), schematic FRESH.

## 2 · W5a — five fixes verified; two of them change rendered pages and neither is ruled

**Reproduced, one run (cand2-r1 restaged twice, HEAD canon+engine v W5a canon+engine, everything else identical):**
- harness ink per view **4.7 → 1.8** (affected dead 8 · cut 5 · collision 7→1 · size 23→0 · markers 4; `measure/views-*.json`). W5a's table row for r1 is exact; the 5.10 → 2.10 mean is three runs and I ran one.
- own-size **82 → 0** findings on 10 pages, 980 parts matched both sides (`measure/os-*.txt`).
- receipt gate **6/10 → 0/10** pages red (BEHAVIOUR-NOT-LOADED on accounts/fx/liquidity/payments/risk/trade at HEAD, none with W5a).
- `_validate_receipt --selftest` PASS · `test_icons_markup.py` PASS (M1 mutation reds at HEAD) · `_validate_geometry --selftest` OK · `score.py selftest-views` PASS · on the mount `gen_canon_components --check` OK (137) · `gen_showroom --check` OK · `_drive_chart_engine --check` 27/27 FRESH · `_validate_behaviour` OK (and `_BEHAVIOUR-GATE.md` byte-unchanged after my check run).

**The licence questions, answered:**

(a) **The root text-box-trim default.** The pattern's source is the 2026-06-29 design decision in canon.css's own header ("flush UI labels … dot+label rows, key/value pairs, eyebrows, list/table text"; headings and body excluded) — not a numbered ruling. s261-D4 (5) "as tight as the original" is about the Kpi-tile only, and W5a left `p.kpi-lbl` alone (measured: no Kpi lock-up moves). s268-D3 records the per-component copies. So NO ruling licenses the root change; W5a argues it from the generator's #215 scope note and from the own-size premise — which is Dave's 24 Sept sentence and Tuesday's **call 23** ("a part is always drawn at its own reference size"), NOT YET RULED. W5a has enacted call 23's consequence at the root ahead of the call.

**What it changes, measured (the K3 test, `tools/k3.py`, `k3b.py`).** On cand2-r1's overview and payments, 4 apollo themes × light/dark, 6,136 text elements: every element whose box moved >1px sits in a `cn-chart-*` scope (legend spans 8.7→12, buttons 16.7→20, Reset 18.7→22, data-table td 17.7→21 / 29.7→33, th 41.7→45, captions +3.3) — W5a's attribution holds there, and no Kpi/label/value lock-up outside charts moved. **But on canon pages that carry the other untrimmed components the change reaches further than the report names:** `_fitness-test/canon-gallery.canon.html` 49 non-chart elements move — **Stat-card** figure/period spans 11.6→21, Icon-button captions, Account-selector labels, File-upload size, Popover trigger 15.2→21; `nio-dash-console-v1.canon.html` Account-selector 10.1→14, 11.6→16, 8.7→12 (`measure/k3b.txt`). Stat-card is a key/value lock-up, which the June decision named as a trim target. Each of those now renders at its reviewed snippet's (untrimmed) size, which is what the own-size gate wants — but it is a visible change on 26 components on every canon page, shown to nobody. **Fix: Tuesday's page must carry it** (call 23 gains "already enacted at the root by W5a — 26 components untrimmed on canon pages; ratify or reverse", with a Stat-card and an Account-selector before/after crop). **Optional narrowing** if Dave refuses: keep the 111 bounded copies, revert the root line, and add a chart-only `text-box-trim:none` restore in the 14 chart scopes — that alone clears the legend clip (the defect that started this) without touching Stat-card and friends. Not built; one line per scope in the generator.

(b) **The right gutter (`gutterPR`).** ds-012(b) is Dave's 2026-07-27 ruling that "the plot area is computed from the widest label, not a fixed number", ruled on the LEFT gutter of the h-bar; his reason ("fixes the class": label length and face looseness) covers the right edge by the same words, and the code reuses the same provisional `PL_MAX_FRAC`/`PL_EDGE_PAD` (point 3, his eye). The maths is right (I re-derived it: PR ≥ W−PL−(W−PL−pad−dx−overhang)/f). Reading: within the licence as an extension, and W5a declared it. Put it on the page as one line under call 6 ("the right-hand twin now built, same rule — ratify"), since call 6's text says it "runs next without a ruling".

(c) **The receipt-gate fence.** Cannot be abused from the page: `inline_scripts()` skips fenced scripts on the PAGE side too (`exclude_demo` defaults True in `behaviour_loaded`), so a page that fences its real script loses it from the carried set (NOT-LOADED, stricter) and 3b DEMO-CHROME-COPIED fires on any APOLLO-DEMO marker in a page. The only way to dodge is to fence a load-bearing script in a repo SNIPPET, and **no gate validates that a fenced span is genuinely deletable** — that is pre-existing (own-size walks the same fence) and s258-D3's "every APOLLO-DEMO span deletes and the component still renders" is a claim no instrument checks. Not a wave-five defect; a follow-on for a lane (render each snippet with its fences deleted, compare).

(d) **Q3 reduced-motion fit flake is real and pre-existing:** payments.html unfit loads 6/10 at HEAD, 2/10 with W5a (`tools/fitflake2.py`; the 1.7× glyphs are this). Noise in both directions; it is in the ink rows of every run. Carry Q3 to the page as W5a asks.

## 3 · W5c — titles hold; one class of session title is a misstatement

- Same tree, HEAD builder (1.28) v W5c builder (1.29): **5,114 node ids identical, 9,774 edges identical (multiset), every coordinate identical; the only node fields that differ are `label` (1,203) and `titleFrom` (1,203)**; every new label starts with the old bare code + space (0 exceptions); by type ruling 638 · rule 473 · session 92. The mount's `_KG-EXPLORER.html` equals my 1.29 rebuild at the same tree except the commit stamp (`3100da99` v `ff382c0b`) — fine, declared build-time note. (My first comparison against the COMMITTED html showed coordinates moving — that is the tree having grown since the 1.28 bake, the 1.27 class, not W5c.)
- `_rulings.json`, `_rule_nodes.json`, `_state.json`, `_build_all.py`: mount == HEAD byte for byte. `gen_kg_titles.py --check` OK, in sync; `--selftest` 12/12.
- **15 titles sampled by hand** (seed 5: 8 rulings, 5 rules, 2 sessions) against their records: **0 misstated** — e.g. `s222-D2 The designer pack must measure tokens out of the box`, `snippets-pure-canon The purge lands in the sources` (from `says`, since `ruled` is `#98`), `nam-004 Labels over invented names for standard services`, `#96 session of 2026-08-05, 3 rulings`.
- **The bug.** Six session nodes are titled "`#n session, 0 rulings`" (#31, #57, #76, #79, #81, #82). For three of them that is false: `gauge-refusal` is ruled `#79-D1`, `ds-021-C` is `#81-D1`, `ds-021-D1-82` is `#82-D1` — the counter matches `ruled == "#n"` or `id ~ ^s<n>-` and misses the `#n-Dk` form (the page's own tab has the same blind spot, so W5c's "matches the page" claim is true and the title is still wrong as a sentence). **Fix (either):** match `^#n(-D\d+)?$` in `gen_kg_titles.py` session counting AND in the template's `sessionTab` filter (one regex each), then `--write`; or drop the count when it is 0 ("`#79 session`"). Small; can land in the same commit or the next.
- Declared and agreed: 43 question-form titles from #272 (accurate, not the verdict); the canvas cut at 34 chars is busier when dug — Dave's call (add to the page, §4).

## 4 · W5b — 10 calls checked; four corrections and what fills the slot

Checked against their sources: call 2 (17 true findings at 390, fixtures do not ship, roster 58 — R4b ✓) · call 5 (22/26 px, 155.14/159.14 — V3 ✓) · call 6 (29 → 0 collisions — V4 ✓) · call 10 (3.71:1, 3.75:1 — R4s ✓) · call 12 (badge 7→8, [81] — R6b/CI page ✓) · call 28 (256,000/300,000, 236,000/276,000 — housekeeping page ✓) · call 29 (72,768, ~128,000 — A2 ✓) · call 30 (6 November — housekeeping page ✓) · call 4 (mint v meta: the mint takes the FIRST AUTO-BEHAVIOUR name in document order that `component-types.json`'s `$behaviour` registry knows — "one row of a type table" is fair; W5a's wording is sharper, use it) · call 1 — **misstated twice, below**.

**Corrections for `page.src.html`, then `render.py`:**
1. **Call 1.** "after the two gate-code fixes from seat W5a that change no rendered page, and with no new cold run" is no longer true: W5a's wave changes canon.css (root trim + 111 copies), the engine (right gutter) and 30 regenerated snippet/showroom pages — every chart legend, chart data table and 26 components render differently on canon pages. Say so, and say what stands in for the cold run: the three cand2 runs restaged on the W5a canon+engine (own-size 82/104/146 → 0, ink 5.10 → 2.10, receipt reds 6/6/10 → 0/0/10). Also: "trace 0.38 to 0.18, canon parts 6.3 to 14.7" are **candidate 1's** figures against v1.0.13 (W3b); candidate 2's trace index was not measured (R4s2 re-drew, did not re-build). Attribute or drop.
2. **Call 5, last sentence** ("inside the bento the KPI tile is already 4px taller … a generator scope leak, not a ruling"): W5a says the opposite — it is NOT a generator fix because the general cure would cut the bento's deliberate child rules; it is **Q2, Dave's word: 40px (the tile's own snippet) or 44px (the bento's tiles)**. Move it to the slot as a call.
3. **Call 6** "the right-hand end … runs next without a ruling" → built in W5a (gutterPR, ds-012(b)'s twin, same provisional constants); one line: ratify with this call.
4. **Call 53** (the 1,135 code-only titles) → done in W5c for ruling/rule/session (1,203 → 0; 49 left: 30 polarities, 13 guidelines, 6 artefacts), committed unruled: ratify or reverse, plus the canvas question below. **Call 11** (640px shell): "eight of nine cold runs" — R4s/R4s2 give 640px on v1013-r2, cand-r1/r2/r3, cand2-r1/r2 = **six of nine** (cand2-r3's pane stops ~730px; v1013-r1 1000px; v1013-r3 none).

**Slot "41a onward" should carry:**
- 41a · **Q1** is already call 4 — point the slot at it.
- 41b · **Q2** Kpi-tile spark in the bento: 40 or 44px (from call 5).
- 41c · **The root trim default**: 26 components now untrimmed on canon pages (Stat-card, Account-selector, Icon-button, File-upload, Popover, Alert, Banner, Toast, Drawer, Modal, Empty-state, Skeleton, the 14 charts) — ratify (it is call 23's rule enacted at the root) or reverse to the chart-only narrowing (§2a). Crops: `notes/_lanes/304/W5a/renders/legend-c2r1-payments-{before,after}-*.png` plus a Stat-card pair the conductor renders from `canon-gallery.canon.html`.
- 41d · **Q3** reduced-motion fit flake: seen, not fixed, next engine lane (no call, a note).
- 41e · **W5c canvas**: code alone on the canvas with the title kept for search/panel/INSPECT, or code + title cut at 34 — one template line either way. And the 49 remaining bare labels: extend or leave.
- Context box: HEAD is `ff382c0b` — dream pass 14 fired at 07:12 BST and floated 8 proposals (P1–P8), 0 ruled; they wait for the dream ritual, not this sitting.

## 5 · `.git/index.lock`

Not on the mount now (`ls .git/index.lock`: no such file; nothing under `.git/` newer than 06:00 UTC named lock). Who made it: the scheduled dream pass ("fire landed 07:12 BST" = 06:12 UTC); its own proposals file says its read-only `git status` hit "unable to unlink … Operation not permitted" on `.git/index.lock` and left it ([[git-lock-mv-not-rm]]) — that is the 06:14:11 UTC stamp W5c saw. Its conductor's commit `ff382c0b` at 06:29 UTC went through `_git_commit.sh`, which clears stale locks, and the lock is gone. Nothing for the commit seat to move.

## 6 · Order for the commit seat

1. Regenerate nothing: W5a's 41 mount files == its surveyed clone commit (41/41 cmp), W5c's 5 == its clone commit per its report and my rebuild.
2. `python3 notes/_lanes/304/W5c/tools/wire_kg_generators.py .` (mount `_build_all.py` == HEAD; anchors 1/1). Then the C1 serial as `--check`; `_gen_chain` will read 152 steps.
3. Optionally the session-title regex fix (§3) + `gen_kg_titles.py --write` + `--check` before the commit; otherwise file it as W5c's first fast-follower.
4. Sitting page: the four corrections and the slot (§4), `render.py`, then commit the page with the wave.
5. Commit on `ff382c0b`. Include the cand2 outputs/RUN-REPORTs, `_REVIEW-304-candidate-2-*`, R4s2 scores, C4's report and brief as W5b's page cites them.
6. CI read-back: the four new steps by name; `[129]` must not be chunk-split in any local re-run.

## Limits

One run reproduced (r1), not three; K3 at 1440 only; the survey baseline is V4's after logs, as W5a's was; the 26-component reach was measured on two `_fitness-test` pages, not all 58; nothing pushed. Clone `$HOME/v5`, worktree `$HOME/v5head`, stages `$HOME/v5st` and runs `$HOME/v5runs-*` die with the VM; `$HOME/v4` (V4's finished clone, 1.9 GB) was removed to make room — its receipts are already under `notes/_lanes/304/V4/`.

## `_state` row spec

```json
{"id":"W-304fv5","title":"#304 V5 verifier wave five - W5a PASS WITH FIXES (root trim default reaches 26 components on canon pages, unruled; right gutter within ds-012(b) by reading), W5c PASS WITH FIXES (three '0 rulings' session titles false: #79/#81/#82 use the #n-Dk form), W5b PASS WITH FIXES (call 1 premise stale, call 5 contradicts Q2, call 11 six not eight, slot 41a filled); fresh-clone survey 152 steps 0 green-to-red, four wired steps pass","home":"notes/_subreports/2026-09-27-304-V5-verifier-wave-five.md","links":["notes/_lanes/304/V5/survey/compare-v4-v5.txt","notes/_lanes/304/V5/measure/k3b.txt","notes/_lanes/304/V5/measure/views-after.json","notes/_lanes/304/V5/tools/k3.py"],"project":"apollo","opened":304,"state":"open","owner":"claude","condition":"stated","body":"s218-D7 filed report, wave five verifier. Reproduced on cand2-r1: ink 4.7->1.8, own-size 82->0, receipt reds 6->0. K3: outside charts no lock-up moves on the cand2 pages, but canon-gallery/nio-dash show Stat-card, Account-selector, Icon-button, File-upload, Popover growing to snippet size (root default no longer reaches them). index.lock was the dream pass's git status at 06:14 UTC, cleared by its commit.","closes_when":"the wave-five commit lands with the wiring applied and the sitting page corrected (calls 1, 5, 6, 11, 53; slot 41a-41e), and the session-title regex fix is either in it or filed as W5c's fast-follower"}
```
