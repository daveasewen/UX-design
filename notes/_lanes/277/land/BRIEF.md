# LANE LA — BRIEF — assemble the four metas: 29 + 47 + 11 = 87 `obeys` edges, every one with an authored `$why`
#277 · 2026-09-16 · enacting `s277-D1..D3` (`407f20b`) · written by the conductor · **model: opus** · PROPOSE, nothing spliced yet

## Rulings (read them in `knowledge/_rulings.json`, ids `s277-D1`, `s277-D2`, `s277-D3`)
- **D1**: the 29 filename-join citations land, with TWO sentences replaced (`chart-bar→dv-bar-001`, `chart-line→dv-line-005`) — replacement wording in `notes/_lanes/277/fable-check/CHECK.md`. For `dv-line-005` the ruling allows drop-and-declare; **prefer the reworded sentence only if you can point at a real mechanism; otherwise DROP it and declare the drop** (line goes 9 → 8).
- **D2**: `chart-donut` takes ALL 11 pie rules; `dv-pie-003` binds the donut alone.
- **D3**: the 47 family cells — bar 17 · line 15 · pie 15 — from the reconciled matrix in `notes/_lanes/277/page/_build_page.py` (`REC`). `dv-013` OFF bar. ⚠ D3 does NOT put family rules on the donut — the donut gets pie-file rules only (11). Do not widen.

## Inputs
- Start from `notes/_lanes/277/page/proposed-metas/chart-{line,pie,bar}.meta.json` (they carry the 29 with CP's two corrections). Apply the D1 replacements/drop.
- `knowledge/components/chart-donut.meta.json` — the LIVE donut meta; author against it.
- `knowledge/guidelines/data-visualisation.md` (19 family rules) + `-pie-charts.md` — read the PROSE.
- House style for a `$why`: `notes/_lanes/276/tie-off/REPORT.md` and the 27 sentences the Fable check passed. **A `$why` is a reason that names a mechanism THAT IS IN THE FILE** — a prop, a token role, an antiPattern, a `when` clause, a motion block. ⛔ The two that failed this morning named a prop that does not exist and borrowed an unrelated mechanism. Before you write a sentence, grep the live meta for the thing you are about to name. Every sentence will be read against the live file by a Fable verifier before it lands.

## Output — `notes/_lanes/277/land/proposed-metas/`
Four metas: `chart-line` (8 or 9 + 15), `chart-pie` (10 + 15), `chart-bar` (10 + 17), `chart-donut` (11). Produce them as **the live meta plus ONE inserted `edges.obeys` span** — build a splice script (`_splice.py`) that takes the live file bytes and inserts/extends the `edges.obeys` array by textual span, with the reconstruction proof the way `_inscribe_ruling.py` does it (remove the span ⇒ original bytes, `==`). **The proposed metas are what that script produces**, so lane LL can re-run it. Do NOT `json.dump` a meta.
- Also write `notes/_lanes/277/land/WHYS.md` — every one of the 87 sentences in a table: component · rule · `$why` · **the exact string in the live meta it rests on** (grep hit, line number). This table is what the verifier grades.

## Gates
Schema-validate all four against `meta.schema.json` (`$why` required) · `_validate_kg.py` OK on the simulated tree (four proposals swapped in, then swapped out) · counts assert: 8/9+15, 10+15, 10+17, 11 = 86 or 87 · `git status` shows changes ONLY under `notes/_lanes/277/land/`.

## Report — `notes/_lanes/277/land/REPORT.md`
Counts, the drop decision on `dv-line-005` with its reason, every gate line, `--numstat` **re-read from the shipped sha**. One commit `#277 2026-09-16 — lane LA: …`. Never `git stash`, never `gen_kg_edges.py`, never `_build_all.py`, stale `.git/index.lock` → `.git/_orphan-locks/`.
