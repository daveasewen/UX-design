# LANE RIV — VERIFY — Fable check of lane RI's icons/logos proposal (5520d43)

#277 · 2026-09-16 · verifier of `notes/_lanes/277/icons-propose/` · READ-ONLY outside this folder.
Everything below was RE-DRIVEN, not re-read. RI's scripts were run; RI's figures were re-derived by my own code where the brief asked for it.

## Counts

**GREEN 19 · AMBER 4 · RED 1**

**Verdict: PRESENT WITH THESE 3 FIXES** — R1 (RI-3 card), A1 (RI-1 sentence), A2 (re-drive the screenshots). A3 and A4 are pre-land conditions on the generator and the schema diff, not on the page.

---

## RED

### R1 — RI-3: the card's evidence sentence is a tautology of the exporter, the origin of `-active-2/-3` is missing, and the option the facts point at was dropped

What the card says: lead figure "15 bases with more than one 'active' glyph — and all 15 of them have a bare `-active`"; recommendation "(a) the bare `-active` is the default, by rule … and it works here: **all 15 of the multi-variant bases have a bare `-active`**, so (a) resolves every one of them".

What the file says:

```
knowledge/assets/icons/_export-icons.py:113-118
    s, i = base, 2
    while s in seen[gslug]:
        s = f"{base}-{i}"; i += 1
```

`-active-2` / `-active-3` is the exporter's **slug-collision counter**. The three dentist records are all named `Dentist Active` in the manifest (`name` identical on all 31 records across the 15 bases — re-read live), and the bare slug went to whichever Figma node the API enumerated first. "All 15 have a bare `-active`" is therefore guaranteed by construction — the first collision always keeps the bare slug — and carries no information about which drawing is the active state. The 31 glyphs are **genuinely different drawings** (path geometry compared per base: 0 of the 16 extras is identical to its bare sibling), so the question "which is *the* twin" is a look-at-the-sheet question, and nothing on the page shows the glyphs.

Two further facts that belong on the card:
* The gate does enforce (a) today — `active_names()` returns `{slug + "-active"}` and `twin_check()` would flag a snippet that twins `dentist` with `dentist-active-2` as MIS-TWINNED. So (a) is the status quo, and that is a fair reason to recommend it. But none of the 15 bases or their 31 actives is used by any snippet (byte-match: 0 of the 81 used icons is one of them), so the gate's assumption has never been exercised on these fifteen.
* IX §5 posed this as three options — (a) stays open · (b) **I'll pick the defaults** · (c) bare is default by rule. RI shipped two and dropped "I'll pick", without saying so. Given the glyphs differ and the names collide, "I'll pick" is the option that matches the facts.

This is the s274-D12 shape: an exporter artefact presented as structural evidence for a design default.

**Correction (three edits on one card, recommendation may stand):**
1. Replace the lead-figure sentence with: "15 bases with two or three 'active' drawings that share ONE Figma name — the `-2`/`-3` suffix is `_export-icons.py`'s collision counter, so the bare slug is Figma's enumeration order, not a design choice."
2. Rewrite the recommendation's evidence: "(a) ratifies what `_validate_icons.py` already enforces (`active_names()` → `slug + '-active'`), and none of these 31 glyphs is used by any snippet today, so nothing breaks either way. It does NOT say the bare drawing is the better one — nobody has looked."
3. Restore the option: "(c) I'll pick — put the 31 glyphs on a sheet and I choose 15." Keep (a) Recommended if RI still wants to; the honest recommendation is "(a) now, (c) when you have ten minutes with the sheet."

---

## AMBER

### A1 — RI-1's recommendation points at screenshots that are not on the page
The card says "That last number is a look, not an argument — judge it on the screenshots below". There is no `<img>` on the page (grep: 0), and the lane's eight PNGs are renders of the review page itself, not of the explorer with the `assets` family placed. The cost section ends "the layout is a look, and it is yours" with nothing to look at. IX §5 step 5 asked for a chip-on and a chip-off explorer render for exactly this.
**Fix:** either delete "judge it on the screenshots below" and say plainly "no chip-on render was made; +17.7% is arithmetic until one is", or build the explorer in a scratch copy with the family placed (RI already imports `extract()`/`extract_extra()` in memory) and embed two renders.

### A2 — the shipped screenshots carry the driver's residue
`_drive_page.py:283` clicks `#RI-1-a` and the reload test types "a note that must survive a reload" into RI-3's notes box; both persist through localStorage into every later screenshot. `ri-decisions-light/dark.png` show (a) ticked on RI-1; `ri-RI3-light/dark.png` show the test string in the notes box. The page itself does not pre-select anything (`load()` only re-checks what storage holds) — but the screenshots RI "looked at" and shipped show a decision already taken and a note already written. The #268 art-director rule was applied and still passed this.
**Fix:** clear localStorage (or open a fresh context) before the screenshot pass; re-drive; re-look.

### A3 — the `s230-D2` residue null is found by a substring-over-English test
`gen_kg_icons.py` (the `defaultFor` block): `for slug in sorted(metas): if slug.lower() in low and slug not in bound:` — every component slug is tested as a substring of the ruling's `ruled+says` text, and any hit not already bound gets a null whose `why` hardcodes "56px rail head, no lockup fits". Re-run live: three slugs are substrings (`app-shell-nav-rail`, `app-shell-top-nav`, `navigations`); two are bound, so the output is the right one (1 null). But the mechanism is a prose join producing a declared null, and a fourth substring slug would inherit the rail's reason verbatim. Bite 10 tests the happy path only.
**Fix (before land):** anchor on the ruling's own clause — the `says` field literally reads "App-shell-nav-rail deliberately NOT rebound" — or declare the residue by name against `s230-D2` and let the bite assert that a second substring slug does NOT produce a null.

### A4 — `meta.schema.diff` bakes live integers into landed schema text
The `usesIcon` and `usesLogo` descriptions in the diff carry 758, 371, 105, 81, 102, 835, 18 and the sentence "Measured live". The REPORT's "no integer typed into the HTML" is true of the HTML; the schema description is the thing that would land under `knowledge/` and go stale on the first regeneration. Minor, and the #276 descriptions may set the precedent.
**Fix (before land):** keep the four limits, drop the counts, or mark them "at 5520d43".

---

## GREEN — what re-drove clean

1. `--dry-run` into a scratch dir: `_icon_nodes.json` and `_logo_nodes.json` **byte-identical** to the committed ones; `dry-run.json` differs only in `wrote` (paths). 688 nodes (666/10/12), 1,299 edges (666/234/371/18/2/8).
2. `--selftest`: 17 bites, 17 ok, rc 0.
3. `_mutate.py` into scratch: BASELINE PASS, 25 mutants, **25 caught, 0 survivors**.
4. **The door is shut.** `land()` called against all **593** live ruling ids + `None`, `nope`, `s999-D99`: 0 landed — 558 refused at the allowlist ("does not ratify THIS proposal"), 36 refused at the shape gate (live ids like `ds-021`, `gauge-band`, `d0802-P3` are not `sNNN-DN`), 1 no-id, 1 unrecorded. `knowledge/_icon_nodes.json` / `_logo_nodes.json` do not exist afterwards; `git status` unchanged. `RATIFIES == ()`.
5. **Independent byte-match** (own 30-line derivation from `_validate_icons.py`'s `norm()`/`DRE`/`SVGRE`/`setdefault`-first and the metas' own `"snippet:<file>"` refs, no RI code imported): **371 pairs / 105 components / 81 icons**; symmetric difference against RI's 371 `usesIcon` edges = **0**. 758 library keys, 137 snippet→component refs, 0 glyph-bearing snippets without a component.
6. **20-sample: 20/20.** Each pair: the icon's SVG file exists, its normalised `d` is present in the mapped snippet outside HTML comments, and the enclosing `<svg>` is not `data-bespoke`. 17 via a `<symbol>` in the same file, 3 inline. (Note: `template-dashboard → view-grid` sits in `symbol#kpi-table` — the byte-match is honest where the symbol name is not.)
7. **Ambiguity check RI did not run:** 43 library geometries are owned by more than one `.svg`; **0** of the 81 used icons has a shared geometry, so no `usesIcon` target is a first-owner accident.
8. **32 declared nulls, each a real absence:** `menu-search` is the only on-disk/not-in-manifest slug (manifest `$generated` 2026-06-17); `circle` and `menu-more-verticle` are absent from the manifest; 15 bases with >1 active, 31 actives, 16 extras; `_rules-index.json` has 0 `logos.md` rules (17 `icons.md`); 0 rulings govern a logo `.svg`; `App-shell-nav-rail.reference.html` has 0 `assets/logos/` refs and 0 text wordmarks; `theme:` occurs 0 times as a node id in `_KG-EXPLORER.html`; `ruledBy` 8 drawn (`s264-D3` ×8) + 1 declared (`s212-D9` → `menu-search`).
9. **`defaultFor` vs `s230-D2`'s exact words:** exactly two stems are contained in `ruled+says` — `masterbrand-light-colour`, `masterbrand-dark-colour`. Dave's verbatim is `'use this as teh default logo "masterbrand-light-colour"'` and `'use this for dark mode masterbrand-dark-colour'`. The page quotes both from `says` and names the field. The *light* theme on the first edge comes from the filename stem and the inscribed `ruled` line ("on light chrome"), not from Dave's sentence, which says "default"; the edge note says `theme=light` from the stem, which is the honest source.
10. `usesLogo` reproduced independently: 18 pairs / 9 components / 4 logos; `template-auth` is the only mono consumer; 0 unmapped.
11. `_simulate_validator.py` re-run: baseline rc 0, simulated rc 0, N1–N4 all CAUGHT, live tree untouched.
12. Live graph reproduced in memory: **3,897 nodes / 6,721 edges**, of which 105 have `t: None`. Lane A1's 6,616 is the same graph minus those 105; RI's 1,299 likewise carries its 4 null-target edges (2 `defaultFor`, 2 orphan `activeVariantOf`). Same convention both sides; the page's "1299 new edges" is consistent with how the explorer counts.
13. Hero arithmetic: 688/3,897 = 17.7%, 1,299/6,721 = 19.3%, 356,431/2,893,289 = 12.32%, 348 KB / 2,825 KB, logo payload 6.3 KB — all reproduce.
14. RI-1's 170 "icons that carry no edge": 172 if null-target edges do not count as edges, 170 if they do (the 2 orphans carry a `t:null`). The page uses 170; the explorer convention supports it. Options (a)/(b)/(c)/(d) are exclusive.
15. RI-2 is posed honestly: (a)/(b) exclusive; 371 vs 1,947 (137/137 metas) reproduced by `--prose-count`; STRUCT-ONLY 32 is measured as "the substring `icon` appears nowhere in the meta JSON", which is the conservative direction (a lower bound). The four limits are on the card and in the schema diff. No prose join anywhere in the generator's code paths.
16. RI-4 is posed honestly: (a)/(b)/(c) exclusive; 10 unbound, 8 referenced by nothing (4 identifier + 4 hexagon), 2 mono used only by `template-auth`; "the condition `s230-D2` was written to fix" is a fair reading of the ruling's own `says` ("twelve masterbrand SVGs ship unbound").
17. `--numstat` re-read from **5520d43**: 21 files, **+22,382 −0**, every path under `notes/_lanes/277/icons-propose/`, 8 PNGs binary. INSERT-ONLY as claimed.
18. The page at 1280 and 390, both themes: decisions above evidence, one lead figure per card, one Recommended per card, attribution in every card, no horizontal scroll at 390, the two defects RI named (backticks, italicised `_validate_icons.py`) are fixed in the shipped render.
19. Nothing on the page is a prose-derived edge dressed as structure — with the one exception filed as R1, which is an exporter artefact dressed as evidence rather than an edge.

---

## Independent figures, in one place

```
usesIcon         371 pairs / 105 components / 81 icons     (RIV own derivation; Δ vs RI = 0)
20-sample        20/20 glyphs present in the mapped snippet, none bespoke, none in a comment
shared geometry  43 library duplicates; 0 touch the 81 used icons
usesLogo         18 / 9 / 4
door             593 live ids + 3 controls → 0 landed
selftest         17/17 · mutants 25/25 caught · validator sim rc 0, 4 negatives caught
nulls            32, all real absences in the file
live graph       3,897 / 6,721 (105 null-target) — matches A1's 6,616 + 105
numstat          21 files +22,382 −0 at 5520d43, all under the lane dir
```

## Not run, and why
`gen_kg_edges.py` · `_build_all.py` · `git stash` · `_build_kg_explorer.main()` · any write outside this folder. The dry run, the mutants and the validator simulation were pointed at scratch directories, never at the lane dir, so RI's committed outputs were compared against, not overwritten.
