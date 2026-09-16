# LANE RI — BRIEF — icons (666) then logos (12) into the graph: PROPOSE, nothing landed
#277 · 2026-09-16 · `s269-D1` STEP 4 · written by the conductor · **model: opus** · RK/RP shape

## The spec you are building from
`notes/_lanes/277/icons/FINDINGS.md` (lane IX, `ca294b4`) — read it whole. Its §2 node kinds, §3 ranked edges, §4 blockers and §5 four-decision plan are the design. **Do not re-derive what IX measured; re-run its commands to confirm, then build.**

## What to build (dry-run, into `notes/_lanes/277/icons-propose/`)
- `gen_kg_icons.py` — mirrors `gen_kg_principles.py` (#275, `notes/_lanes/275/principles-kg/`) and the roles/rules generators: `--dry-run` writes `_icon_nodes.json` + `_logo_nodes.json` + edges to THIS lane dir; `--land --ratified <ruling-id>` is the door and is NOT usable until a `s277-D*` id exists for it. Selftest ≥ 12 bites; `_mutate.py` mutants ≥ 12; a surviving mutant is a finding.
- Nodes: `icon:<slug>` (666, fields per IX §2 — name, slug, file, group, active, fillMode) + `iconGroup:<slug>` (10) + `logo:<slug>` (12: lockup × theme × colourMode).
- Edges, STRUCTURAL joins only (IX §3 ranks 1–6): `inGroup` (666) · `activeVariantOf` (232) · `usesIcon` component→icon from the **`_validate_icons.py` byte-match** (371) · `usesLogo` from `src=` (18) · `defaultFor` logo→theme from `s230-D2` (2) · `ruledBy` (9). ⛔ `themedBy` declined (IX measured it contentless). ⛔ NO prose/regex join — the slug-as-word route fires on 138/138 metas and is REFUSED (`s274-D12`, `s276-D5`).
- Declared nulls, in the #274 shape: `menu-search.svg` not in the manifest (`s212-D9` ruled it in — B1); the 2 active orphans; the 15 bases with `-active-2/-3` (B4, Dave's); the 10 logos with no rule source (B3); `app-shell-nav-rail` residue in `s230-D2`.
- `_validate_kg.py` grammar: propose the ADDITION (three kinds, six edge types, per-edge props) as a diff file, the way #276 did (`meta.schema.diff`); do not apply it. Run the validator against the simulated tree with the diff applied in a scratch copy and report.
- Explorer: simulate the payload the way IX did (+9.4% bytes); propose the chip name and its default (OFF, like `ux`).

## Review page — `REVIEW-icons-2026-09-16-v1.html` (copy `notes/_lanes/277/page/_build_page.py`, adapt; decisions ABOVE evidence; export JSON in the same shape)
≤ 4 decisions, from IX §5: **RI-1** node kinds (icon+iconGroup+logo = 688 / icon only 666 / not yet) · **RI-2** draw `usesIcon` from the byte-match (a) or wait (b) · **RI-3** the `-active-2/-3` default (a: first variant is the default, others declared) or leave open · **RI-4** the 10 unbound logos enter as nodes with declared-null governance (a) or wait for `logos.md` rules (b). Recommendation first on each, ONE figure per card, attribution in the card. Screenshot both themes at 1280 and 390 and LOOK at it.

## Gates, report, cautions
`_validate_kg.py` OK on the live tree (you landed nothing) · schema/selftest/mutants lines · `git status` only `notes/_lanes/277/icons-propose/` · REPORT.md measured not narrated, FILL at close, `--numstat` re-read from the shipped sha · one commit `#277 2026-09-16 — lane RI: …` · never `git stash` / `gen_kg_edges.py` / `_build_all.py` · stale lock → `.git/_orphan-locks/` · the KG audit lanes run in parallel under `notes/_lanes/277/kg-audit/` — commit serially.
