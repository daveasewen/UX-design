# #305 B6: the four names, the accepted when-rules, the ring, the two wordings

provenance: 305 · 2026-09-28 · lane B6 (Opus 5.5, build seat, on the mount through device_bash). No git writes, no `git status`, no `_build_all.py`, no Project memory. `_rulings.json`, `_state.json` and `_CARRIES.md` were not touched (lane A2's).
status: observed
CITES: notes/_lanes/305/DAVE-RULINGS-2026-09-28-loose-ends.md (his words) · notes/_DECIDE-305-loose-ends-2026-09-27-v1.html · notes/_subreports/2026-09-27-305-B5-loose-ends.md · notes/_subreports/2026-09-27-305-B2-brain.md (the method) · notes/_lanes/304/R4a/drafts/when-rules.proposed.json (the wording) · A2's inscriptions s305-D58, D59, D60, D61 (read only)
machinery: 0 instrument / 1 feature (four `when` rules and one when-field)

## The answer

1. **The four names: held.** Nothing in the metas expresses how the 23 settled clashes were settled, so there is no form to copy. All 27 clashes still carry a setting and a slot under the same name, as they did before the sitting. `s305-D19` is `ruled`, and B2 said it "builds with the PoC". R5's catalogue generator still lets the slot win on all 27 (`G-SLOT-PROP-SAME-NAME` 27). Writing the four now would invent a form the other 23 do not have. It would also force two new names that are Dave's: a new name for the grid's applied search terms, and the shape of the tab bar's per-destination setting (both are costs `s305-D58` names). His four verdicts are in the record as `s305-D58` (A2). They build with the 23 in October.
2. **The accepted when-rules: built.** Four rules moved, all four worded exactly as R4a drafted them, gate plus prose, which is the machine form: filter bar, footer, the dashboard bento template and button (`AND actions <= 1`). `layout.grammar` joined `when-fields.json` by addition (s273-D4). The other 11 accepted rows already matched their metas byte for byte, so none of them changed. The list and top-nav metas are byte-identical to HEAD (cmp against this lane's backups). The chooser gives the same result as before on every case: R5's 20 are still 19/20 (the one miss is still W18) and B2's 6 are still 6/6. No case flips.
3. **The ring: confirmed, nothing changed.** Nothing built contradicts his rule. One wording tension is left open because `s305-D59` leaves it open.
4. **The modal and own-size wordings: confirmed in the tree as he saw them.**

## Per item

### 1 · data grid, lightbox, stepper, tab bar: held
- Measured on the live metas: 27 metas give a setting and a slot the same name. Each clash has a plain `props` entry (`$note` only) and a `slots` entry (`$status` "ruled s140-D2"). None of them has a marker saying which one won. The four in question look the same as the 23 (data grid `columns`/`filters`, modal-lightbox `items`, stepper `steps`, tab-bar `items`).
- The #304 schema page's sort (16 settings, 7 slots) was "this seat's reading of each name, not a measurement". It never went into a meta. B2 recorded calls 16–19 as "ruled, builds with the PoC; nothing built".
- What the build is when it comes: the four join the 23 under one expression (drop or demote the loser in each pair). The data grid's `filters` setting gets a new name, and the tab bar's `items` setting grows from a count to icon plus label. The last two are naming and shape calls, so Dave should see them.

### 2 · the 15 accepted when-rules: 4 built, 11 already in the tree
- Written by `notes/_lanes/305/B6/work/apply_rules.py`. It is idempotent and asserts the meta still holds the draft's `current` before replacing it. It writes through B2's `jspan.py`. A second run changed 0 files.
  - `button.meta.json`: line 15 only. Gate gains `AND actions <= 1`; the prose is byte-identical.
  - `filter-toolbar-bar.meta.json`, `footer.meta.json`, `template-dashboard-bento.meta.json`: one new `"when"` line, placed after `name`. These metas have no `provides`, and after `name` is where template-wizard, template-error and template-confirmation already put theirs.
  - `when-fields.json`: line 55 gains a comma, and line 56 adds `layout.grammar` with R4a's definition and example.
- The four strings equal R4a's `proposed` byte for byte (the script's equality check). The 11 unchanged accepted rows (breadcrumbs, bar chart, page title, KPI tile, layout, legend, main navigation, stat card, status dot, summary, view options) equal the draft and the metas, as B5 measured.
- Not touched: `list-items.meta.json` and `app-shell-top-nav.meta.json` (his "Change" on both). Both are cmp-identical to HEAD.
- Chooser (R5's `when_eval.py`, B2's test copied to this lane): before and after runs produce the same output byte for byte. R5's 20: A 19, B (default) 19. The miss is W18 (list-items for a grid question whose need is unstated, as before). B2's 6: 6/6. No flips.
- This lane's own probes (`work/probe_new_rules.py`, before = backups swapped in memory):
  - The button now refuses at `actions: 2` (unknown before, False after). Role `action` picks are unchanged in all four probes: with `actions: 3` it was split-button before and still is.
  - Filter bar: fires at records 10 / needs filter, and refuses at needs none.
  - Footer: fires at platform app, and refuses at marketing.
  - Bento: refuses at grid. At bento it returns unknown rather than true, because its first clause is prose inside the gate, as R4a's draft says.
  - Filter bar, footer and bento have no `provides`, so the role-based chooser cannot reach them yet. Their gates parse and evaluate.
- Graph: `gen_kg_roles_desk.py --land --ratified s270-D1` (B2's precedent) was rehearsed first on a scratch copy of `components/`. There, 1 meta changed. Landed live, it added exactly one edge: `template-dashboard-bento —yieldsTo→ template-dashboard`, from the new prose. A re-run wrote 0 metas.

### 3 · the ring: confirmed, nothing changed
His rule, verbatim: "The chart pattern should be set to fill but its container should constrain it by being smaller of having more than one element in it".
- Donut and pie `when`: `AND span.cols ≤ 6` hands a ring a half-width column. That is the container "being smaller", and `s305-D59` confirms this half. A 12-wide tile holding a ring and another element still gives the ring a band of 6 or less, so the gate does not contradict "more than one element in it".
- B1's tile hug (`Template-dashboard-bento.reference.html` :722–723, `align-self:start; height:auto` on a leaf tile holding a donut or pie) acts on the tile's height only. The tile keeps its column span, so the container still constrains the chart's width. It does not contradict the rule.
- The open tension (not changed): the ring is drawn at its own diameter (`figure.dv-fit-on[data-dv-type=donut|pie] .dv-svg{width:auto;height:auto}` :716), and the meta prose says "A ring does not stretch with its tile (ds-030)". "Set to fill" reads against both. `s305-D59` says in its own words that how fill "squares with ds-030 ... is open thread W-305n2, which this ruling feeds and does not close". Changing either would decide that thread. Held for Dave.

### 4 · modal and own-size wordings: confirmed
- The `when` strings in modals, split-button and dropdown each appear verbatim in the page's text (whitespace-normalised). No meta was changed.
- The own-size sentence "A part keeps its own size on any page. The page arranges parts; it never shrinks them." is in `knowledge/guidelines/web-foundations.md` (rule `{#webf-036}`) and on the page, verbatim. A2 recorded it as `s305-D61`.

## Gates run (at the seat, after the last edit)
- Schema (B2's write-free copy of the integrity check): **137/137, 0 errors** before and after.
- `_build_integrity.py`: **PASS 0 errors / 25 warnings**. Its report matches HEAD except for dates, and the tracked `_INTEGRITY-REPORT.md` was restored byte-identical (diff empty).
- `_validate_roles_resolve.py`: **PASS**. Every when field is legal, and `layout.grammar` is counted once (template-dashboard-bento).
- `_validate_intent_resolve.py`: PASS. `_validate_kg.py`: OK. `gen_kg_roles_desk.py --selftest`: PASS. `gen_kg_sources --check`, `gen_kg_titles --check` and `gen_kg_tokens --check`: all OK, in sync.
- Reader `_compose_slice.py --selftest`: 73/79. The six reds (46, 57, 60, 62, 71, 73) were already red before this lane.
- Catalogue (R5's generator, copied into this lane so R5's tracked outputs were not written): before and after on the same tree. **Only the four parts moved, and only in `when` / `description`**: all-catalogue 8 paths (Button when.gate; FilterToolbarBar, Footer and TemplateDashboardBento gain `when`), dashboard catalogue 6. G-WHEN went from 94 to 91 overall and from 2 to 0 on the dashboard. Schema errors published: 0. G-SLOT-PROP-SAME-NAME is still 27 (item 1 held). See `work/catalogue/catalogue-diff.json`.
- Explorer: built into a scratch path outside the repo (2m43s) and compared with the page on the mount. The only component edge added is the one bento `yieldsTo`. The other additions (s305-D58, D59, … nodes and edges) come from lane A2's in-flight inscriptions. **So the live `notes/_KG-EXPLORER.html` was NOT rewritten**, because rebuilding it now would bake a half-inscribed ruling store. That rebuild belongs to the commit seat's regen serial, after the last inscription.

## For the commit seat
- `s305-D60` (the 15 accepted rules) is enacted by this lane's four meta edits plus `when-fields.json`. The other 11 were already in the tree. Stamp it after the commit, if the brief allows.
- Regen serial: `gen_kg_roles_desk --land` is already done. Rebuild the explorer after A2's last inscription.
- Replay: `python3 notes/_lanes/305/B6/work/apply_rules.py`, then `python3 knowledge/gen_kg_roles_desk.py --land --ratified s270-D1`. Both are idempotent.
- `notes/_lanes/305/B6/work/__pycache__/` is gitignored bytecode and not for the commit.

## What is Dave's
- The four names' build and its two naming costs, with the 23, in October.
- W-305n2: ring "set to fill" against ds-030 and the ring's own-diameter drawing.
- The list rule and the top-nav rule, each "on its own".

## Changed paths (exact)
Modified, tracked:
knowledge/components/button.meta.json · knowledge/components/filter-toolbar-bar.meta.json · knowledge/components/footer.meta.json · knowledge/components/template-dashboard-bento.meta.json (the `when` line, plus the landed `yieldsTo` edge) · knowledge/when-fields.json

New:
notes/_subreports/2026-09-28-305-B6-names-and-rules.md · notes/_lanes/305/B6/OWNS.txt · notes/_lanes/305/B6/backup/** (7 pre-edit copies: the five above, plus list-items and app-shell-top-nav as proofs of no change) · notes/_lanes/305/B6/work/ (apply_rules.py, probe_new_rules.py, probe-new-rules.json, chooser_test.py, chooser-results.json, schema_check.py, jspan.py, gen_catalogue.py, roles-desk-dry-after.json, before/, after/, catalogue/)
