# LANE RV — VERIFY — the reader (RD, `d6bd57b`) and scope (SC, `9e7a158` + `3263dd7` + `a39d4cd`)

#279 · 2026-09-16 · verify seat (Fable 5.1), read-only on the tree except this file and its `_subreports/` copy · everything below was RUN against the LIVE tree at `e7ff7b9` (+ the three uncommitted paths other lanes hold), never against the reports · scratch copies in `/tmp/rv279-*` and `/tmp/rvold/` (root disk, not `/sessions`), deleted after; `knowledge/_rulings.json` sha `0f5bf047…` before and after.

## VERDICTS

- **RD — GREEN WITH FIXES.** The contract, ASK, the live read and the selftest all hold as claimed. Three fixes: (F1) the edit to `designer-skills-v2/generate-from-canon/SKILL.md` turns the BLOCKING **frozen-release gate RED** (`s114-D4`) — RD's report says "no gate reads the SKILL.md … nothing broke", which is wrong (RD grep'd `knowledge/*.py` and missed `knowledge/_release/`); (F2) the ratio "31.8×" in the report § 4 and the runbook line 196 is not what RD's own `measure.json` says (35.14×) — a re-typed figure; (F3) report § 8 still reads "(appended below after the commit landed)" — the numstat was never appended, in either copy.
- **SC — GREEN WITH FIXES.** All 34 `$source` spans are live substrings; the reach figures reproduce exactly from an independent join; the bites bite. Two fixes: (F4) the row-level facet union already misroutes in the dashboard seed — `photo26-002` (a photography ban) reaches `app-shell-top-nav` through facet `logos` because `brand-refresh-assets.md` carries `[logos, imagery]` as one row; the per-rule facet override SC priced (~10 lines) is the fix and should land before the explorer draws the chip; (F5) a `hexagons` facet is named by three files' section headers and absent from the set (harmless today — every indexed `hex26-*` rule is REVIEW and excepted — but `va25-014`/`va25-020` are hexagon rules riding on `imagery`/`icons`).

Neither lane touched a path outside its brief. Nothing here is a hold.

---

## The checks

### (1) Contract — own code, not `--selftest`
```
python3 -c "import _compose_slice as cs; s=cs.build_slice(cs.TASK_A) …"   (knowledge/ on sys.path)
```
- 8/8 `CONTRACT_FIELDS` present on the dashboard seed: components 31 · governs 38 · obeys 77 (authored 28 / derived 4 / routed 30 / routed-by-scope 15) · mustNot 8 (6 `ref:null`) · tokens 25 · assets 31 · unresolved 22 · sized dict(12).
- `$nulls` = `{}` on the dashboard (nothing null); `ref:null` rows without a `$note` anywhere in the seed: **0**.
- Forced a null-yielding call (`components=["zz-none-component"]`): 5 fields null, **5/5 carry a `$nulls` note**; `obeys` still 7 (the always-on routed screen set — declared in the docstring), `unresolved` 2.
- Note, not a fix: the house-rule bite (2) tests `_finish_fields` by mutation, not the emitted seed — a field emitted as `[]` with no note passes bites 1–3 (my hand-break variant 2 below was caught only by bite 16). A one-line bite on the built seed would close that.

### (2) ASK — 12 questions, own tiktoken count (cl100k_base 0.14.0)
Counted `json.dumps(answer minus sized)` myself; the door's own `sized.tokens` is the same number on all 12.

| Q | RD | RV (mine) | RV incl. `sized` block |
|---|---|---|---|
| Q1 governs button | 615 | **615** | 666 |
| Q2 binds ctkb-003 | 162 | **205** | 256 |
| Q3 principle ctkb-002 | 256 | **256** | 307 |
| Q4 conflicts button | 290 | **290** | 341 |
| Q5 ruled table | 196 | **196** | 247 |
| Q6 evidence s277-D10 | 309 | **309** | 360 |
| Q7 answers comparison | 212 | **212** | 263 |
| Q8 avoid toast | 244 | **244** | 295 |
| Q9 tokens button | 750 | **750** | 801 |
| Q10 usedIn button | 291 | **291** | 342 |
| Q11 wcag button | 578 | **578** | 629 |
| Q12 assets app-shell-doormat | 624 | **624** | 675 |
| total | 4,527 | **4,570** | |

Q2 moved 162 → 205 because SC added `routedByScope` to Q2 after RD's run — the only delta; the rest match to the token. All 12 ≤ 1,000 either way (max 801 with the `sized` block).
- **Planted ruling, scratch copy:** copied `knowledge/{components,guidelines,tokens,compliance,*.json}` to `/tmp/rv279-scratch/knowledge`, composed the seed from the scratch copy, THEN appended `s998-D7` governing `table.meta.json` to the scratch `_rulings.json`, then `ask("what governs component:table?", seed=old_seed, live=load_live(scratch))` → **`ruling:s998-D7` returned** (`via: governs[] meta path`), not in `seed.governs`, seed sha256 unchanged, Q5 sees it too, `ask()` against the live root does NOT see it. Live `_rulings.json` sha unchanged, `git status` clean on it.
- `load_live()` has no cache (`_mtime` is only stamped into the answer); `--ask` rebuilds `live` from `HERE` on every CLI call — the live read is real.

### (3) The measured claim
```
python3 knowledge/_compose_slice.py --measure                                  → seed 31,536 / 111,468 (3.53×) / 1,005,758 (31.89×)
git show f641242:knowledge/_compose_slice.py > /tmp/rvold/knowledge/_compose_slice_old.py ; --explain   → slice 19,117 vs 111,468 = 5.83×
git show d6bd57b:knowledge/_compose_slice.py … --measure                       → 28,621 / 111,468 (3.89×) / 1,005,758 (35.14×)
```
Old code reproduces the ruling's 19,117 (5.83×); RD's 28,621 (3.89×) reproduces at its sha; live (after SC) is 31,536 (3.53×). Per-field live: components 7,639 · governs 5,225 · obeys 10,909 · mustNot 575 · tokens 1,772 · assets 2,597 · unresolved 1,597. **F2:** RD's report § 4 and `_RUNBOOK-compose-from-canon.md:196` say 31.8× against the pre-wiring 1,005,758; RD's own `measure.json:22` says **35.14** (1,005,758 / 28,621). 31.8× is the post-SC figure, which RD could not have had. Re-typed, not measured.

### (4) Wiring
- `git diff f641242 d6bd57b -- designer-skills-v2/generate-from-canon/SKILL.md` → 27/4; step 1 says exactly what RD claims (reader first, `--out seed.json --explain`, open a meta only when the seed names it, LINK canon.css/type.css, `--ask` mid-session, fallback declared "not default" with the required used/missing note). `components[].meta` and `components[].snippet` exist on live rows; `--help` prints the 12 verbs.
- **F1 — a gate reads it and is now RED:** `python3 knowledge/_release/_gate_frozen_release.py --check` → rc 1: `FROZEN RELEASE MOVED: designer-skills-v2 (version v2) … 1 CHANGED: designer-skills-v2/generate-from-canon/SKILL.md`. This is BLOCKING in `_build_all.py:595` (s114-D4, built #219). `git diff --stat 117b33cb f641242 -- designer-skills-v2/` is empty — v2 was untouched from the ledger seed until RD; RD caused it alone. `_gen_pack_manifest.py:537` also records v2 as "FROZEN release, s114-D4" and bite `groups/excludes` insists nobody claims that SKILL.md. The commit script does not run this gate, which is why the commit landed. **Fix (the gate's own instruction):** bump the v2 row's `version` in `_gate_frozen_release.py`'s declaration table and `--seed` in the same commit — `s277-D10` names `designer-skills-v2/` in `governs[]`, so Dave's word for the move exists; the version bump is mechanical. Alternative if the conductor reads s114-D4 stricter: revert the SKILL.md hunk and cut it as v2.1. Either is one commit.

### (5) Scope — 12 rows by eye (`random.seed(279); random.sample(sorted(files), 12)`)

| # | file | kind | `$source` | grade | why |
|---|---|---|---|---|---|
| 1 | accessibility-framework.md | null | "applies to all external-facing HSBC digital products worldwide" | **honest** | axf-005 "Global scope" — the file's scope IS product-level; null is right |
| 2 | accessibility-information-architecture.md | facet copy | "binds heading/label microcopy" | **honest** | the ingester's bracket on aia-002, "the one substantive rule on the page"; it is the file's own statement of what it binds |
| 3 | accessibility-interaction-design.md | facet ×4 | "actionable elements large enough to tap" | **stretched** | a single rule title (ID-15); the file's scope is its role + four section headers (Navigation / Touch targets / Layout / Forms) — the facets are right, the sentence is convenient |
| 4 | accessibility-qa-cx-testing.md | null | "this is the METHOD page (BS 8878 lineage)" | **honest** | the file's own framing |
| 5 | accessibility-standards-hub.md | facet interaction | "a visible focus indicator must have" | **stretched** | a fragment of axs-004, the file's one indexed rule; the file is "the WCAG 2.2 adoption map" (product-level, like #1). Routes 1 rule correctly, but by rule content, not by scope |
| 6 | brand-refresh-assets.md | facet logos, imagery | "Marketing-weighted content — … component relevance flagged where real." | **stretched** | genuinely the file's self-description, but it says relevance is *flagged where real* — the opposite of a blanket facet route; and the row's union of logos+imagery is what misroutes photo26-002 (F4) |
| 7 | colour-standards-2026.md | facet colour, data-vis, status | "Don't introduce colours outside the palettes." | **stretched** | col26-015, a RULE, quoted as scope; the file's applicability sentence is col26-002 "in all communications" |
| 8 | common-toolkit-notifications.md | component notifications | "canon meta (notifications.meta.json) was rebuilt from THIS node set 2026-06-24" | **honest** | the file names its canon counterpart |
| 9 | data-visualisation-bar-charts.md | component ×4 | "Rectangular bars, heights/lengths proportional to values; vertical or horizontal." | **honest** | the Usage definition; the histogram/butterfly extension is declared in `$why` and leans on data-visualisation.md |
| 10 | generative-ai-brand.md | null | "This is GOVERNANCE, not visual rules" | **honest** | the file's own framing |
| 11 | naming.md | facet copy | "the TEXT RULES bind any UI copy that carries product/service names" | **honest** | the file's header; narrower than "all copy" — file-grain coarseness, not a wrong quote |
| 12 | tone-of-voice.md | facet copy | "all generated copy inherits" | **honest** | tov-001's bracket + tov-003 "all generated copy is brand-signed"; the file even has a "## Scope note" section that would have been the cleaner quote |

**8 honest · 4 stretched · 0 wrong.** The three nulls (#1, #4, #10) are real scope-less files — product, method, governance. Facet set vs files: `hexagons` is named as a section by `brand-refresh-assets.md`, `visual-assets.md` ("Creative Hexagons") and `typography-usage.md` ("Hexagon placement — fenced") and is not a facet (F5); `sound/mnemonic` (visual-assets § "Video, mnemonic, sound") folds into `media` acceptably.

### (6) Reach — own join (`_scope.json` rows + facets[].binds · metas' `tokens` blocks via the same `TOKEN_PATH_RX` · `_rules-index.json` · icon/logo node edges)
- ALL 470: obeys-only **107 → either 410** · scope-alone **303** / obeys-alone **1** / both **106** · unreached 60.
- BLOCKING 59: **9 → 52** · scope-alone 43 / obeys-alone 0 / both 9 · unreached `ill-010, pict-001/007/008/009/010/011`.
- Facet coverage (components binding): copy 116 · type 116 · colour 132 · dark-mode 132 · icons 111 · pictograms 0 · illustration 0 · imagery 2 · logos 9 · motion 46 · elevation 36 · layout 85 · interaction 60 · markup 137 · forms 49 · data-vis 19 · status 54 · media 0.
Every figure equals SC's § 2 / § 5 tables.

### (7) Gates and bites
```
python3 knowledge/_compose_slice.py --selftest   → 54 bites, 0 failed, rc 0   (8.7 s)
python3 knowledge/_validate_kg.py               → OK, rc 0
```
Hand-breaks in `/tmp/rvold/knowledge/` (symlink farm over the live tree; only the two edited files copied):
- `$source` on the naming.md row "bind any" → "bind every": **bite 45 FAIL 33/34 ['naming.md'], rc 1**.
- `s.pop("assets")` after `_finish_fields` in a copy of `_compose_slice.py`: **bite 1 FAIL ['assets'], bite 3 FAIL**, then a `KeyError` in bite 16 aborts the run — rc 1 (red, but the runner does not survive a missing field to report the rest; cosmetic).
- `s["assets"] = []` (silently empty, no note): only **bite 16 FAIL**, rc 1 — see the (1) note.

### (8) numstat from the shipped shas
- `git diff --numstat 9e7a158~1 9e7a158` → 11 lines, **identical** to SC § 8 (261/7 `_compose_slice.py`, 1247/0 `_scope.json`, 19/0 `_state.json`, 2/2 `_CHAIN.md`, …). `3263dd7` = 4/1 report + copy; `a39d4cd` = 15/3 report + copy — report-only, as declared.
- `git diff --numstat d6bd57b~1 d6bd57b` → 12 lines (27/4 SKILL.md, 64/0 runbook, 1299/469 `_compose_slice.py`, 75/40 `_state.json`, 2/2 `_CHAIN.md`, 1/0 rehearsal log, the seven lane files). **F3:** RD § 8 in both copies still reads "(appended below after the commit landed)". The in-prose figures that exist (SKILL 27/4, runbook 64/0) match. `_state.json`'s 40 deletions are diff alignment: ids before 647 → after 649, added `W-279il, W-279rd`, removed 0, existing rows changed 0 (same check on SC: 650 → 651, `W-279sc`, 0 changed).

### (9) Outside the brief
RD: none — `_CHAIN.md` (counts) and `notes/_REHEARSAL-LOG.jsonl` are the commit script's own writes; the runbook is 64/0 (addition only); `_build_kg_explorer.py` untouched. SC: none — the same two script writes; explorer files left unstaged as briefed. Neither lane touched `_rulings.json`, `gen_kg_edges.py` outputs or the explorer.

---

## Judgement

**Does the reader as landed satisfy s278-D1's "reads the Constitution live" inside the repo?** Yes: `load_live()` re-reads `_rulings.json`, the 137 metas, the rule/ux/icon/logo node files and `_scope.json` on every `ask()` call with no cache, and `--ask` builds that view from `HERE` on each CLI invocation, so a ruling appended after the seed is answered (my `s998-D7` plant was returned by Q1 and Q5 against a seed composed before it, with the seed byte-identical and the live file untouched). The seed is composed once, carries `$contract` naming itself a seed, and nothing in `ask()` writes to it — the two halves are separate as the ruling draws them. Inside the repo the ruling is met; whether a designer holding the pack can ever call the door is the open pack question RD declared (neither `_compose_slice.py` nor `_rulings.json` ships), and that stays Dave's.

**Does routed-by-scope at file grain risk what SC flagged badly enough to hold the lane?** The risk is not hypothetical: on the dashboard seed itself `photo26-002` (no generative-AI imagery) reaches `app-shell-top-nav` because the `brand-refresh-assets.md` row unions `logos` and `imagery`, and `visual-assets.md`'s video-aspect-ratio and hexagon-clear-space rules reach all 111 icon-bearing components. But the class is labelled on every row, BLOCKING-only in the seed, dropped first under budget, kept out of `authored`/`routed`, and the whole non-BLOCKING reach lives only behind ASK Q2 — the cost on the dashboard was 15 rows and 2,915 tokens of over-inclusion, never a wrong prohibition presented as authored. The exception row plus the class label is enough to land on; the per-rule `facet` override SC priced (~10 lines, rows on demand) should be the next touch on `_scope.json` — before the explorer draws the "inference by declared scope" chip, so the page never shows the photo-ban-on-a-nav case as the ruling's intent.
