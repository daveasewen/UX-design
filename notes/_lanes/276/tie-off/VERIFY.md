# Lane TV — READ-ONLY verification of lane TO (#276, 2026-09-15)

Verifier: lane TV. I wrote exactly one file, this one. No commit, no stash, no checkout,
no `--land`, no edit to any lane TO artefact.

**One declared exception, same class as lane RV's at #275:** re-running `_drive_page.py` as
instructed **rewrote the committed `notes/_lanes/276/tie-off/screenshot.png`** (md5
`8b889dcd…` → `10a5b35c…`, 1,157,577 → 1,157,542 bytes). The page was re-rendered, not
re-authored. `git status` now shows that file modified; it is mine, declared here, and
left uncommitted.

Verdict in one line: **the lane's work is sound and nothing landed — but the report's own
headline table contradicts the report's body and the review page on two figures.** 26 of 29
claims reproduce GREEN. **2 RED** (both arithmetic in REPORT.md §1, both correct on the
page and in the artefacts). 1 amber (a meta count stated three different ways).

Corrections are **by addition**: the report's figure and the measured one, side by side.

---

## The table — one row per claim

| # | claim (REPORT.md) | how I drove it | measured | verdict |
|---|---|---|---|---|
| 1 | 17 files in `proposed-rules/` | `ls \| wc -l` | 17 | **GREEN** |
| 2 | schema-valid, 0 failures vs `knowledge/compliance/rule.schema.json` | `jsonschema.validate` on all 17 myself | 17 OK, **0 failures** | **GREEN** |
| 3 | every `title`/`level` off the W3C page, none from memory | `curl`+`urllib` fetched **all 17** `https://www.w3.org/WAI/WCAG22/Understanding/<slug>.html`, parsed the `<h1>` myself | **17/17 HTTP 200**, **17/17 title exact match**, **17/17 level exact match** | **GREEN** |
| 4 | exactly three AAA: 1.4.8, 2.4.13, 3.1.4 | W3C `<h1>` of every one of the 17 | `Counter{A:9, AA:5, AAA:3}`; AAA = **1.4.8, 2.4.13, 3.1.4** exactly | **GREEN** |
| 5 | the brief was wrong to name only 2.4.13 as AAA | W3C pages for 1.4.8 and 3.1.4 | `Understanding SC 1.4.8 Visual Presentation (Level AAA)`, `Understanding SC 3.1.4 Abbreviations (Level AAA)` | **GREEN** — the correction is real |
| 6 | severities 12 serious / 5 minor / 0 critical | counted over the 17 files | 12 / 5 / 0 | **GREEN** |
| 7 | **check types 11 manual · 6 semi-automated** | counted `check.type` over the 17 files | **12 manual · 5 semi-automated** | **RED** |
| 8 | 19 `cites` nulls today | `knowledge/_rule_nodes.json`, `type=='cites'`, `t` falsy | 51 cites · 32 resolved · **19 null** | **GREEN** |
| 9 | 19 nulls across 17 distinct criteria, 1.3.3 ×2 and 1.4.8 ×2 | regex the null `note` for `cites SC n.n.n`, `Counter` | 17 distinct; **1.3.3:2, 1.4.8:2**, all others ×1 | **GREEN** |
| 10 | nulls **19 → 0** with the 17 present | re-derived the lookup independently: set of proposed `sc` vs the null SC list | **resolve 19, remain 0, `remaining_sc []`** | **GREEN** |
| 11 | `sc:` nodes 38 → 55 | globbed `knowledge/compliance/rules/*.json` | 38 today; 38 ∪ 17 = **55**; **0 overlap** between proposed and existing | **GREEN** |
| 12 | the three 2.2 additions and only those carry the pending-EN clause | read `sources.en301549_clause` + `wcag_versions` on all 17 | 2.4.13 / 3.3.7 / 3.3.8 only | **GREEN** |
| 13 | `applies_to` `[]` on all 17, `external_automatable_refs` `[]` on all 17 | read all 17 | both `[]` on all 17 | **GREEN** |
| 14 | axe would attach **6 refs across 4 of the 17** | re-ran `_import_axe_rules.py:tag_to_sc` myself over `axe-core-rules-snapshot.json` (v4.12.1) | `1.4.2: no-autoplay-audio · 2.5.3: label-content-name-mismatch · 3.1.1: html-has-lang, html-lang-valid, html-xml-lang-mismatch · 3.1.2: valid-lang` = **6 refs / 4 criteria** | **GREEN** |
| 15 | **67 authored citations — 55 `rule:` + 12 `ux:`** (§1 and §3) | counted `edges.obeys` over the 6 proposed metas | **81 entries — 67 `rule:` + 14 `ux:`** | **RED** |
| 16 | per-component table: tags 9/2 · tags-input 5/2 · notifications 17/2 · links 16/3 · button 14/3 · icon-button 6/2 | counted each proposed meta | every row exact (9,5,17,16,14,6 rules = 67; 2,2,2,3,3,2 laws = 14) | **GREEN** |
| 17 | every citation carries a `$why` | scanned all 81 entries | **0 missing**; **81 `$why` strings, 81 unique** (no reuse) | **GREEN** |
| 18 | every `rule:` id exists in `_rules-index.json` | membership test against the index's 470 ids | **0 unresolved** | **GREEN** |
| 19 | every `ux:` id exists and is one of the six grade-A laws | `knowledge/_ux_principle_nodes.json` (175 nodes) + `knowledge/brain/principles.json` `grade=="A"` | **0 unresolved**; used = `pr-fitts, pr-graphical-perception, pr-hick, pr-speed-accuracy` ⊂ the six (`pr-klm`, `pr-steering` correctly unused) | **GREEN** |
| 20 | filename join, not regex — every rule id comes from its component's spec file | joined every cited id back to `_rules-index.json` `file` | **1 off-file citation in 67**: `links` → `ctkb-004` (`common-toolkit-buttons.md`) — exactly the one the report declares, with its own `$why` | **GREEN** |
| 21 | `icon-button`'s set is a strict subset of `button`'s; tags/tags-input do not overlap | set algebra on the cited ids | subset **True**; overlap **∅**, union 14 of the 23 in the shared file | **GREEN** |
| 22 | 7 component-named guideline files; chart-line/pie/bar the only obvious extras | listed every distinct `file` in `_rules-index.json` | **34 distinct files**; component-named = `common-toolkit-{buttons,links,notifications,tags-chips}` + `data-visualisation-{bar,line,pie}-charts` = **exactly 7**; no eighth | **GREEN** |
| 23 | chart-line 11 · chart-pie 11 · chart-bar 10 · `data-visualisation.md` 19 | counted rules per file | 11 · 11 · 10 · 19 | **GREEN** |
| 24 | `_validate_kg.py` stays OK | ran it | `_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean…` (139 metas checked) | **GREEN** |
| 25 | `_build_rules.py --selftest` 15/15 · `_author_metas.py --selftest` 17/17 | ran both | `selftest: 15/15 bites green` · `selftest: 17/17 bites green` | **GREEN** |
| 26 | `_validate_lane_ownership.py --selftest` 3/3, advisory exit 0 | ran both modes | `selftest: 3/3`; `LANE OWNERSHIP: OK — no staged path under another session's lane (this is #276).` **exit=0** | **GREEN** |
| 27 | `_mutate.py` — 18 mutants, all caught, 0 survivors | ran it | `BASELINE rules … PASS` / `BASELINE metas … PASS` / 18 mutants each `-> RED …` / **`ALL 18 MUTANTS CAUGHT`** | **GREEN** |
| 28 | `_drive_page.py` DRIVE PASS, 11/11, both themes | `source knowledge/_render/seat_env.sh` then ran it | 11 `ok` lines, **`DRIVE PASS`**; light `rgb(218,26,0)`, dark `rgb(246,96,76)` (s151-D1); worst clip 0.00px; 390px no h-scroll; 0 console errors | **GREEN** (see the declared screenshot rewrite above) |
| 29 | `git show --stat 8053591` touches only the lane + the guard | ran it | **36 files, 4,699 insertions — every path under `notes/_lanes/276/tie-off/` except `knowledge/_validate_lane_ownership.py` (78 lines). No other path.** | **GREEN** |
| 30 | nothing landed | counted the live corpus | `knowledge/compliance/rules/` **38**; live metas with an `obeys` block **0**; `meta.schema.json` `properties` **34 keys**, `obeysEdge` **absent**, `git diff` on it **empty**; `_rule_nodes.json` still **19 nulls** | **GREEN** |
| 31 | review page: 6 decisions, (a)/(b), export control | read the HTML | **6 decisions D-1…D-6**, `value="a"` ×6, `value="b"` ×6 — **and `value="c"` ×6** plus a clear option (a third option per decision, beyond what the brief specified; declared, not a defect) — `Export JSON` (download to `tie-off-decisions-2026-09-15.json`) + `Copy to clipboard` + `Clear all` | **GREEN** |
| 32 | metas in the corpus (138 in the report, 137 on the page, 139 in the gate) | `ls knowledge/components/*.meta.json` | **138 files**, of which one is `EXAMPLE-button.meta.json` ⇒ **137 real components**; `_validate_kg.py` counts **139** | **AMBER** |

---

## The two REDs, in full — by addition

### RED 1 — check types (REPORT.md §1 headline table)

| | figure |
|---|---|
| report says | **11 manual · 6 semi-automated** · 0 automated |
| I measure | **12 manual · 5 semi-automated** · 0 automated |

Driven: `Counter(json.load(open(f))['check']['type'] for f in proposed-rules/*.json)`
→ `{'manual': 12, 'semi-automated': 5}`.

The **report's own §2 row-by-row table is correct** — semi-automated on 1.4.2, 2.4.13, 2.5.3,
3.1.1, 3.1.2 and manual on the other twelve, which is 12/5. **The review page is also correct**:
it prints "manual 12 · semi-automated 5 · automated 0", built from the builder's table. Only the
headline sentence in §1 is wrong. **No artefact is affected — this is a typo in prose, not a
defect in the 17 files.**

### RED 2 — the citation count (REPORT.md §1 and §3)

| | figure |
|---|---|
| report says | **67 authored citations — 55 `rule:` + 12 `ux:`** ("**55 rule citations + 12 law citations = 67 entries**") |
| I measure | **81 entries — 67 `rule:` + 14 `ux:`** |

Driven: summed `len(edges.obeys)` over the six files in `proposed-metas/` —
`button 17 (14+3) · icon-button 8 (6+2) · links 19 (16+3) · notifications 19 (17+2) ·
tags-input 7 (5+2) · tags 11 (9+2)` = **81**.

The **report's own §3 component table sums to 67 rules and 14 laws** — so the report contradicts
itself twice in the same section: it calls 67 the *total* when 67 is the *rule* count, and it
states 55/12 where the table says 67/14. **The review page is correct throughout**: "81 authored
citations", "67 rule citations and 14 law citations", and D-3(a) "81 entries across 6 metas".
**Nothing in the metas is wrong — the figure Dave will read on the page is the right one.**

### AMBER — the metas denominator, stated three ways

Report §1/§2 say **138**; the review page says **137**; `_validate_kg.py` reports **139 metas
checked**. Measured: **138 `*.meta.json` files**, one of which is `EXAMPLE-button.meta.json`,
so **137 real components** — the page's figure is the defensible one and the report's is the raw
file count. The claim the number carries ("**0** of them names any of the 17 SCs / has an `obeys`
block") is **GREEN at every denominator**: I measured 0 both ways.

---

## What I could not drive

- **The fetch receipts as lane TO obtained them.** I could not replay lane TO's WebFetch calls;
  I fetched all 17 pages myself, fresh, on 2026-09-15 by `curl`/`urllib` and compared to the files.
  Every title and level matches W3C exactly, so the claim "none from memory" is corroborated by
  outcome, not by re-running the lane's own tool.
- **"reviewed by eye"** on the six authored `$why` sentences and on the screenshot — I checked
  that 81 sentences exist, are unique, and that every ref resolves, but I did not re-adjudicate
  each sentence's judgement. That is an art-director read, and it is Dave's or the conductor's.
- **The `$why` of the one cross-file citation** (`links` → `ctkb-004`) I read and accept; whether
  the buttons-vs-links boundary belongs on `links` is a judgement, not a measurement.

## What I checked for and did not find

- No ruling inscribed: `knowledge/_rulings.json` is untouched and still holds **584** rulings.
- No false attribution to Dave anywhere in REPORT.md or the page — his four quoted sentences in
  the BRIEF are the only words attributed to him, and the page attributes none.
- No invented node, edge or ref: **0 unresolved** `rule:` ids and **0 unresolved** `ux:` ids.
- `s274-D12`'s named false positive (`va25-013`, "Avatar"/"Badge") appears **nowhere** in the
  proposed metas — it appears only in the page's declared weak tier, labelled as the refused case.

---

**Tally: 29 GREEN · 2 RED · 1 AMBER.** Both REDs are prose arithmetic in REPORT.md §1/§3 that the
review page and the artefacts themselves get right. Every proposed file, every gate, every fetch
and the commit's scope reproduce exactly. Nothing landed.
