# LANE SC2 — REPORT — per-rule facet override + `hexagons` facet (RV F4 / F5), RD F2 / F3 by addition, RV + EV verifies filed
#279 · 2026-09-16 · lane SC2 (Fable 5.1) · enacting the two SC fixes and the two RD fixes the verify seat (RV, `notes/_lanes/279/reader-verify/VERIFY.md`) named · `s277-D9` (the scope store), `s274-D11` (consumer same commit), `s218-D7` (verify reports filed as rows)

**The one line.** A facet row in `knowledge/guidelines/_scope.json` may now carry `ruleFacets` — a rule's OWN facets, a subset of its file's, each resting on a quoted span of the rule's text — and the reader honours it on every path (`obeys_for`, `rule_reach`, ASK Q2, `--measure-scope`). 27 overrides on 5 rows; `photo26-002` reaches 2 image-bearing components instead of 11 (no nav through `logos`); `va25-014` / `va25-020` reach 9 / 2 instead of 111. `hexagons` joins the closed facet set (19), binding nothing, declared. Reach 410 → **408** of 470 (the two rules moved to `illustration` / `media` honestly reach 0); BLOCKING **52** unchanged. Selftest 54 → **62**, 0 failed; `_validate_kg.py` rc 0. RD's 31.8× and the missing numstat are corrected BY ADDITION, both copies. RV and EV verifies filed as `W-279rv` / `W-279ev`.

## 1. F4 — the per-rule facet override

**Store** (`_scope.json`): a new top-level `$overrideRule` says the contract; a facet row may carry `ruleFacets: [{rule, facets, $source, $why}]`. `facets` must be a SUBSET of the row's facets (narrower, never wider). `$source` is a verbatim span of the rule's own text in the guideline file, graded like the row `$source` (whitespace-collapsed substring). Exceptions still win over an override. A row's `facets` / `tokenGroups` / `components` / `exceptions` are untouched — the override is by addition.

**Reader** (`_compose_slice.py`, 10 lines in `scope_reach` + a 4-line helper `_rule_components(d, rid)`): `scope_reach` computes per-override reach = the components in the FILE's reach that bind one of the rule's facets, and records it under `ruleFacets[rid]`; an override whose facets are not a subset of the row's, or that sits on a null / component row, is REFUSED — recorded in `refusedOverrides`, never applied, the rule keeps the file's reach. `_rule_components` returns the override's components when present, else the file's; it is what `rule_reach` (the measure), `obeys_for` (routed-by-scope, BLOCKING only) and ASK Q2 (`routedByScope.ruleFacets` + a `declared[]` line quoting the `$source`) now read. `--measure-scope` prints `ruleFacets` (per rule: facets, components, file_components) and `refusedOverrides` (`{}` on the live store).

**The override rows — rule → facets → reach (file → rule) → `$source`.** Every `$source` was checked as a live substring by me before writing and is bite 55's job from now on.

| file | rule | facets | reach | `$source` |
|---|---|---|---|---|
| `accessibility-visual-design` | `avd-001` | colour | 135 → **132** | "colour is never the only carrier of meaning" |
| `accessibility-visual-design` | `avd-002` | colour/type | 135 → **132** | "text contrast 4.5:1, large text 3:1" |
| `accessibility-visual-design` | `avd-004` | type/imagery | 135 → **116** | "no images of text" |
| `accessibility-visual-design` | `avd-009` | interaction | 135 → **60** | "focus indicator thickness + change-contrast" |
| `brand-refresh-assets` | `logo26-001` | logos | 11 → **9** | "An HSBC logo appears at least once on every piece of communication or customer journey." |
| `brand-refresh-assets` | `photo26-001` | imagery | 11 → **2** | "lead with photography as the principal creative medium" |
| `brand-refresh-assets` | `photo26-002` | imagery | 11 → **2** | "a generation engine must never fabricate photographic imagery" |
| `brand-refresh-assets` | `photo26-003` | imagery | 11 → **2** | "briefing vocabulary for image selection at composition time" |
| `colour-usage` | `col25-013` | dark-mode | 132 → **132** | "Exclusively dark-mode, digital only" |
| `colour-usage` | `col25-014` | illustration | 132 → **0** | "the illustration palette must never dominate" |
| `colour-usage` | `col25-017` | status | 132 → **54** | "Digital-UX context ONLY" |
| `neurodiversity` | `neuro-014` | colour | 135 → **132** | "bright colours ≤20% of screen content" |
| `neurodiversity` | `neuro-028` | imagery | 135 → **2** | "Simple images, understood within ~2 seconds; single object in focus." |
| `neurodiversity` | `neuro-029` | imagery | 135 → **2** | "Meaningful images only" |
| `neurodiversity` | `neuro-030` | imagery | 135 → **2** | "Background images sparingly; no content/form inputs overlaid on decorative images" |
| `neurodiversity` | `neuro-034` | media | 135 → **0** | "Text intro above every video" |
| `neurodiversity` | `neuro-036` | motion | 135 → **46** | "Attention-attracting movement is a LAST resort" |
| `visual-assets` | `va25-003` | imagery | 111 → **2** | "a page-type parameter that caps complementary imagery" |
| `visual-assets` | `va25-004` | imagery | 111 → **2** | "new-to-HSBC users may get more complementary assets" |
| `visual-assets` | `va25-014` | logos | 111 → **9** | "clear space = 1× hexagon height on all sides" |
| `visual-assets` | `va25-015` | logos | 111 → **9** | "the Masterbrand logo appears in ALL digital mastheads" |
| `visual-assets` | `va25-016` | logos | 111 → **9** | "never distort, recolour, reorient or recreate" |
| `visual-assets` | `va25-017` | logos | 111 → **9** | "Variant selection on photographic backgrounds" |
| `visual-assets` | `va25-018` | imagery | 111 → **2** | "No Generative AI, mixed media or CGI-rendered elements in imagery" |
| `visual-assets` | `va25-019` | imagery | 111 → **2** | "governs fixture-image selection if the engine ever picks photos" |
| `visual-assets` | `va25-020` | imagery/hexagons | 111 → **2** | "hexagon- geometry angles, never a forced 45°; wide 'opening up' frames + intimate close crops" |
| `visual-assets` | `va25-022` | imagery | 111 → **2** | "Photography textures always use the red/white/grey palette." |

Why these and not more: RV named `photo26-002` (F4's example) and visual-assets' video/hexagon rules; SC § 7.2 named neurodiversity's flashing-rule-via-`type` class. I applied the override where a rule's own text names ONE asset class or section that the file's union blurs — logos vs photography (brand-refresh, visual-assets), the Images / Video / Movement / Colours sections of neurodiversity, the Colour / Motion sections of accessibility-visual-design, and the three palette-scoped rules of colour-usage. Left at file grain, on purpose: `va25-013` (aspect ratios) — its own text says "icons/avatars 1:1 square", so it DOES bind icon-bearing components and an override that removed `icons` would contradict the quoted rule (RV's "video-aspect-ratio" case is this rule; it stays at 111 by its own words); `va25-001/002/005/006/007/012` (every asset class); `avd-006` (alt text on every non-text element, a BLOCKING gate that must keep icon-bearing components); `neuro-026` (icons support text — `icons` is not in the neurodiversity row's set, and an override cannot widen). `col25-013` (dark-mode) narrows by facet but not by count — the dark-mode and colour groups bind the same 132 components today; kept because the facet is the honest one.

Two row-level facet additions rode along, each named by a section header and each binding nothing today (reach unchanged): `hexagons` on three rows (F5, below) and `media` on `neurodiversity.md` (its "## Video content" section — `media.covers` 2 → 3) so that `neuro-034` could declare it.

## 2. F5 — the `hexagons` facet

Added to the closed set: `hexagons` — `binds: {tokenGroups: [], metaFields: [], edges: []}`, `$why` DECLARED "no token group, meta field or edge carries a Creative Hexagon today — the shape lives in the composition/journey strand" — exactly the shape `pictograms` / `illustration` / `media` have. Named by the three rows whose section headers name it: `brand-refresh-assets.md` ("## Creative Hexagons (2026)"), `visual-assets.md` ("## Creative Hexagons (2025)"), `typography-usage.md` ("## Hexagon placement (composition — fenced)"). `covers` 3, components binding 0. The hexagon rules themselves: `hex26-002/005` stay exception rows (REVIEW); `va25-020` declares `imagery/hexagons`; `type25-017` and `va25-026/027` are not in `_rules-index.json` (RECORDED / fenced), so nothing routes through the facet today — as declared. Facet set now 19.

## 3. Measured — before / after, with the command

Command: `python3 knowledge/_compose_slice.py --measure-scope` → `notes/_lanes/279/scope-fix/measure-scope.json` (SC's file in `notes/_lanes/279/scope/` is the before).

| figure | SC (`a39d4cd`) | SC2 (this commit) |
|---|---|---|
| of 470 rules, reach ≥1 component | 410 (60 none) | **408** (62 none) |
| of 59 BLOCKING, reach ≥1 component | 52 (7 none) | **52** (7 none) |
| by scope alone / obeys alone / both — all | 303 / 1 / 106 | **301 / 1 / 106** |
| by scope alone / obeys alone / both — BLOCKING | 43 / 0 / 9 | **43 / 0 / 9** |
| overrides (rows / rules / refused) | — | **5 / 27 / 0** |

The two rules that left the reached set: `col25-014` (illustration palette → `illustration`, binds nothing) and `neuro-034` (text intro above every video → `media`, binds nothing). Both reached 132–135 colour/type-bearing components before by the file's union; 0 is the honest number and the same class as the 24 pictogram/illustration rules SC already declared. The 7 BLOCKING unreached are unchanged (`pict-001/007/008/009/010/011`, `ill-010`).

Dashboard seed (`python3 knowledge/_compose_slice.py "<dashboard task>" --explain` → `notes/_lanes/279/scope-fix/seed-dashboard-explain.txt`): OBEYS 77 → **76**, routed-by-scope 15 → **14** — `photo26-002` left (it reached the seed only through `app-shell-top-nav`'s `usesLogo` edge; the seed's one image-bearing component, `list-items`, is an alternate, and `obeys_for` reads primaries). `--measure`: seed 31,536 → **31,372** cl100k; vs the 31 metas 3.53× → **3.55×**; vs step 1 before the wiring (1,005,758) **32.06×**.

## 4. RD's F2 / F3 — by addition

- **F2** — `notes/_lanes/279/reader/REPORT.md` § 4 (after the "ratio vs that | 31.83×" row) and `knowledge/_RUNBOOK-compose-from-canon.md` (after line 198): a correction paragraph citing `measure.json:22`'s **35.14** (1,005,758 / 28,621) and today's live 32.06× (1,005,758 / 31,372). The original lines stand as written. Both report copies identical (`diff` empty).
- **F3** — RD § 8, both copies: the numstat from `git diff --numstat d6bd57b~1 d6bd57b` (12 lines) appended under the "(appended below…)" line, with RV's note on the 40 `_state.json` deletions, and a line saying F1 (the frozen-release gate) is NOT addressed here — `designer-skills-v2/` and `knowledge/_release/` are lane PK's.

## 5. Verifies filed

- `notes/_lanes/279/reader-verify/VERIFY.md` + `notes/_subreports/2026-09-16-279-RV-reader-scope-verify.md` (identical) → `W-279rv`, state **done**, closed by this commit (F4/F5 landed here; F2/F3 landed here by addition; F1 named for PK).
- `notes/_lanes/279/explorer-verify/VERIFY.md` + `notes/_subreports/2026-09-16-279-EV-explorer-verify.md` (identical) → `W-279ev`, state **open**, closes when Dave answers the `designrulings` chip question (EV § 9: citation-edge chip as built, or a ruling-node set waiting on a ratified per-ruling scope).
- Both rows via `_state.add()` (W-279rd shape). This lane's own row is **`W-279sf`**, not `W-279sc2`: the store's id pattern (`W-[0-9]{1,3}[a-z]{0,2}`) refuses a digit after the letters — declared in the row's title.

## 6. Gates — every line

```
$ python3 knowledge/_compose_slice.py --selftest
  62 bites, 0 failed   (1–54 as at a39d4cd, untouched;
                        55 OVERRIDE: every override names a rule OF ITS FILE, facets ⊆ the row's, live $source, reach ⊆ the file's — 26 strictly narrower, 0 refused
                        · 56 MUTATION: an override that would WIDEN (naming.md nam-001 → copy+icons, scratch) is REFUSED, reach stays 116
                        · 57 MUTATION: an override on a NULL-scope row (accessibility-framework.md axf-002, scratch) is REFUSED, routes nothing, live file untouched
                        · 58 RV F4: photo26-002 no longer reaches app-shell-top-nav; every component it reaches binds imagery (2); logo26-001 == the usesLogo set (9)
                        · 59 RV F4: va25-014 (logos) / va25-020 (imagery/hexagons) reach 9 / 2, none through icons, vs the file's 111
                        · 60 obeys_for honours it: a slice on app-shell-top-nav carries logo26-001 routed-by-scope and NOT photo26-002
                        · 61 ASK Q2 on photo26-002 reports ruleFacets=imagery, 2 components, declares the override with its $source
                        · 62 RV F5: hexagons in the closed set, binds nothing, named by exactly the three rows)
$ python3 knowledge/_validate_kg.py            → OK, rc 0
$ python3 knowledge/_compose_slice.py --measure-scope → § 3
$ python3 knowledge/_compose_slice.py --measure       → seed 31,372 / 111,468 (3.55×) / 1,005,758 (32.06×)
```

## 7. Not done, with size

1. **RV F1 — the frozen-release gate (s114-D4) is still RED** on `designer-skills-v2/generate-from-canon/SKILL.md`. Not mine: `designer-skills-v2/` and `knowledge/_release/` are lane PK's this session. Size: the version bump in `_gate_frozen_release.py`'s table + `--seed`, one commit (RV § 4).
2. **The explorer's 'inference by declared scope' chip** — still EX's file (lane EX2 live). `scope_reach(g)[file]["ruleFacets"]` is what the chip should read per rule; `_rule_components(d, rid)` is the one call. Size unchanged from SC § 7.1 (~25 lines).
3. **`va25-013`** stays at 111 by its own words (§ 1). If Dave wants the aspect-ratio rule split (video/photo vs icon/avatar vs third-party logo), that is a rule split in `visual-assets.md`, not an override. Size: one guideline edit + regen of `_rules-index.json`.
4. **RV's (1) note** — a one-line bite on the BUILT seed for a field emitted `[]` with no note — not in my brief; size 3 lines.
5. **Overrides on the remaining wide rows** (`accessibility-client-side-dev.md` at 137 via `markup`, `web-foundations.md`, `common-toolkit-foundations.md`) — I read them and left them: a dev/markup standard binds every rendered component by its own framing. Rows on demand, same mechanism.

## 8. Shipped sha and `git diff --numstat` from it

The brief is ONE commit, so the sha cannot sit inside the report it ships in (RD's F3 was this exact gap); the sha is in the reply and in `_CHAIN.md`'s row. The numstat below is `git diff --numstat HEAD` on the staged paths immediately before the commit — the commit's own numstat differs only by `notes/_REHEARSAL-LOG.jsonl` 1/0 (the script's session witness) and `_CHAIN.md` if the chain gate regenerates it; the two report copies are new files of this length (`wc -l`), which a report cannot state about itself exactly.

```
7	0	knowledge/_RUNBOOK-compose-from-canon.md
110	7	knowledge/_compose_slice.py        (reader: scope_reach override leg + _rule_components + obeys_for/rule_reach/ask/measure reads ≈ 30; bites 55–62 ≈ 70; docstring 5)
66	0	knowledge/_state.json               (W-279rv, W-279ev, W-279sf; 0 existing rows changed)
266	12	knowledge/guidelines/_scope.json    (the 12 deletions are closing brackets / $why / covers lines re-emitted where a facet or override was appended; no row lost a key)
21	0	notes/_lanes/279/reader/REPORT.md
21	0	notes/_subreports/2026-09-16-279-RD-reader.md
108	0	notes/_lanes/279/reader-verify/VERIFY.md              (new)
108	0	notes/_subreports/2026-09-16-279-RV-reader-scope-verify.md   (new, identical)
87	0	notes/_lanes/279/explorer-verify/VERIFY.md            (new)
87	0	notes/_subreports/2026-09-16-279-EV-explorer-verify.md       (new, identical)
521	0	notes/_lanes/279/scope-fix/measure-scope.json         (new)
87	0	notes/_lanes/279/scope-fix/seed-dashboard-explain.txt (new)
125	0	notes/_lanes/279/scope-fix/REPORT.md + notes/_subreports/2026-09-16-279-SC2-scope-fix.md (new, identical)
```

NOT staged, deliberately: `knowledge/_build_kg_explorer.py`, `knowledge/_kg_explorer.template.html`, `notes/_KG-EXPLORER.html`, `notes/_lanes/279/explorer-fix/` (lane EX2 live); `knowledge/_graph-mark-observations.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` (instrument appends, per brief); `notes/_lanes/279/DAVE-RULINGS-2026-09-16.md` (the conductor's). `_state.check()` reports the one PRE-EXISTING failure `W-278wr: missing required field(s) links` (SC saw the same); the three new rows passed on add. A 0-byte `.git/index.lock` 15 min old with no git process was moved to `.git/_orphan-locks/` before staging.
