# HANDOFF #121 — #270 → #271 — THE DOOR AND THE CUT-OFF

> ⚠ **This file is NEWER than `_CHAIN.md` and OUTRANKS it.** Written by the #270 conductor (Fable) at
> FILL ≈180,000 real — AT the stop line, BEFORE the ritual, so nothing here depends on a delegated
> wrap remembering it. Every claim is a receipt you can probe.

## ⛔ READ FIRST, IN THIS ORDER
1. This file. 2. `_CHAIN.md`. 3. The three pages in `notes/` (below). 4. `python3 knowledge/_parked.py --check` (10 rows now).
★ Stale-mount check: `git log --oneline -3` vs `ls -la --time-style=full-iso _CHAIN.md`.

## ⛔⛔ DAVE'S — VERBATIM. THE WRAP INSCRIBES; NOBODY RE-WORDS. Source: `notes/_lanes/270/DAVE-RULINGS-2026-09-14.md`
- **A. Both lanes GO (opener):** *"cool, lets do both in teh oredr you prefer"* — conductor chose lane 1 (roles/DESK) then the door.
- **B. Dropdown cut-off, RULED FROM MEMORY:** *"If I remember correctly we use dropdowns for 5 and above"* → *"okay lets do it from my memory 5 is the cutoff"*. ⇒ inscribe as **`s270-D1`** (his sentence in `says`; conductor's reading, LABELLED: radio = single-select ∧ options ≤ 4; dropdown = single-select ∧ options ≥ 5, DEFAULT not last resort). **PROVISIONAL** — source is his recollection; the number is in NO ingested file (checked: `guidelines/`, `roles.json`, both metas, Memento, `_rulings.json`). Tripwire **`P-270-1`** on `guidelines-ingest` (already in `_parked.json`, driven, selftest OK).
- **C. Door shape (direction, NOT a build ruling):** *"three compositions that are all defensible under the same rules"* · *"maybe the logic is cast the net wider for the slice, the slice carries the scoring so if variations asked for there is scope to substitute"*. Reading: slice carries EVERY provider per role with score + `when` + `chosen`; rules/tokens fixed. Two dials named in chat: net width (temperature analogy, his) and rule-layer binding (foundation-only extreme, older conversation). Modes = presets, NOT built.
- **D. NOT RULED — DO NOT RULE:** the four edge types (`providesRole`/`answersIntent`/`hasDataShape`/`yieldsTo`) entering the closed vocabulary — page asks for one word "ratify" → would be `s270-D2`, lands via `gen_kg_roles_desk.py --land --ratified s270-D2` · door step-1 switch advisory/blocking · copy record-list `when`s from `roles.json` onto the metas · split `selection-controls` meta · multi-select boundary · combobox threshold · all #119 opens (deck ask, title edges, v1.0.6 date, dream pass 12, pre-bake step, fly-through, v1.0.13 hand-over, six-month comparator) · boot ceiling literal · #243/#264 double-counts.

## WHAT #270 DID — RECEIPTS (4 commits `5b99b0f` `21baa87` `4d1c849` + this; ALL LOCAL, push is his word)
1. **Lane 1 — `knowledge/gen_kg_roles_desk.py`** (8 bites; `--land` refuses without a RECORDED ruling id — mutation-proven by me). Dry run: 115 edges / 45 nodes on 26 metas; `_validate_kg.py` GREEN on scratch with schema diff, RED (100) without. Page `notes/_PROPOSAL-kg-roles-desk-2026-09-14-v1.html`. Lane folder `notes/_lanes/270/roles-desk/`. ★ Drift: `roles.json` 108 memberships vs 24 metas with `provides`; 4 roles zero providers in metas; `when` 81/108 reproduces. NOTHING LANDED.
2. **Lane 2 — `knowledge/_compose_slice.py`** (12 bites, 2 mutation). 3 driven slices ≈6× smaller than the metas they replace, 25× vs library. Page `notes/_PROPOSAL-compose-time-door-2026-09-14-v1.html`; `GATE-SHAPE.md` in `notes/_lanes/270/compose-door/`. ⚠ **My own drive (approvals-queue task): picks by word-match — chose `meter`/`summary` for "status badges", left `badge`/`table` as prose in `unresolved`.** ADVISORY only; v2 = C above.
3. **Research lane — `notes/_REVIEW-when-predicates-selection-and-lists-2026-09-14-v1.html`** (16 own + 49 external sources, `notes/_lanes/270/when-research/`). ★ **CORRECTION OF MINE:** record-list `when`s EXIST in `roles.json` (table "default, read-mostly" · data-grid "sort/filter/select/edit-in-place" · list-items "≤3 fields, tappable") — wrong home, no gate reads them. Selection controls: 27/27 `when: null`; HSBC sources silent BY CONSTRUCTION — the Common Toolkit component specs (Dropdown, Selection controls, Segmented, Input fields) + forms prose node `45226:149920` were NEVER ingested (`guidelines/forms.md:40`, `_INGESTION-QUEUE.md` § Queued). Switch vs checkbox = "effect is immediate", 5/5 systems.
4. **Art-director pass by me:** both proposal pages rendered 1280, no overflow, Univers Next stack, quote gate run — today's quotes NOT in the index (stale index, ritual 2g), pages say "today's chat".

## #271 — FIRST MOVES (when he says go)
1. Get the one word on D (edge types) → land lane 1 → `_build_kg_explorer.py` regen + 3 colour vars → `_kg_history.py`.
2. Door v2 per C (options per role, score + when + chosen) — cheap data-shape change in `_compose_slice.py`.
3. Add "Common Toolkit form-component specs" to `_INGESTION-QUEUE.md` as a NAMED source (needs Figma). Draft the 8 selection `when`s from B for his review.
**Cautions:** `model: opus`, verifier same wave, `_checkin.py` every ~10 turns, screenshot + text diff before presenting, `.git/index.lock` → `allow_cowork_file_delete`, never `git stash`, never `gen_kg_edges.py`, disk `/sessions` ~96%.

## STRUCTURAL REDS AT THE SEAM (for the wrap to heal or declare, not hide)
Memento index stale (today's lane files) → rebuild + stage (2g) · boot 79,592 = SIXTH breach, shrink-only, his · #243/#264 double-counts (append-only, his) · MEMORY.md over cap (advisory, stub rule governs) · uncommitted `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` · dream pass 12 unruled (31h+).
**Gauge:** boot 79,592 real · FILL ≈180,000 real at handoff (stop line 180,000 — AT it, not past) · subs: lane1 164,816 · lane2 195,301 · research 154,395 = 514,512.
