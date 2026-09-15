# LANE RL2 — BRIEF — land the 145 principles + 30 polarities into the graph
#275 · 2026-09-15 · s269-D1 STEP 3, ENACT · written by the conductor · model: opus

## The word
Dave ruled `s275-D1..D6` (knowledge/_rulings.json, 584 entries; his export + 'go' verbatim at `notes/_lanes/275/DAVE-RULINGS-2026-09-15.md`). Read the six `ruled` texts first. `s275-D2` is the id `--land --ratified` takes. `s275-D6`: the file and its explorer reader land in the SAME commit.

## The precedent to mirror exactly
Lane RL, #274, commit `00f3a87` — `git show 00f3a87 --stat` and read its diff of `knowledge/_build_kg_explorer.py` (the `_rule_nodes.json` reader + "Guideline rules" chip, explorer v1.11). Do for `knowledge/_ux_principle_nodes.json` what that commit did for `_rule_nodes.json`: same reader shape, its own chip(s), node families `ux` and `polarity`, the six edge types drawn. Do not restyle anything else in the explorer.

## Steps
1. `python3 knowledge/gen_kg_principles.py --land --ratified s275-D2` → `knowledge/_ux_principle_nodes.json`. Confirm 175 nodes / 111 edges / 27 declared nulls (lane RP's measured counts, verified by lane RV in `notes/_lanes/275/principles-kg/VERIFY.md`), and that `$description` names `s275-D2` — not the dry-run's "PROPOSED … NOT RATIFIED" text (the #275 fence, `ef1213b`). If the generator's landed `$description` still says PROPOSED, fix the generator by textual span the way `gen_kg_rules.py:land()` was fixed, re-land, and say so.
2. Teach `knowledge/_build_kg_explorer.py` to read the file (textual-span edit; bump the explorer version by one minor, e.g. v1.11 → v1.12, wherever the version string lives). Regenerate the explorer the way #274 did (find the regen command in `00f3a87`'s message or `_build_kg_explorer.py`'s docstring). Count the `ux:` and `polarity:` nodes and the six edge types in the regenerated `notes/_KG-EXPLORER.html` and print the counts.
3. Gates, exact tails in the report: `python3 knowledge/_validate_kg.py` · `python3 knowledge/gen_kg_principles.py --selftest` · `python3 knowledge/_validate_compose.py` (if it exists and is what #274 ran) · `python3 knowledge/_parked.py --check` (P-274-3 / P-269-* hooks may fire — print, don't act) · the roles resolver if #274's RL ran one (`grep -n resolver notes/_lanes/274/rules-land/REPORT.md` or the wrap commit `c2c7890` for the command; FAIL(6) is INHERITED from #261 — report the number, do not heal it).
4. Drive the explorer in chromium (`cd` to the repo, `source knowledge/_render/seat_env.sh`, reuse whatever driver #274's RL used — grep `notes/_lanes/274/` and `knowledge/_render/` before writing one): open `notes/_KG-EXPLORER.html`, turn on the new chip(s), screenshot to `notes/_lanes/275/principles-land/screenshot.png`, 0 console errors. Also screenshot with the chip OFF to prove nothing else moved.
5. `REPORT.md` in this folder: what landed (counts), the reader diff summary (lines added, nothing else touched), gates with exact tails, screenshots, anything you could not do and the first obstacle.
6. ONE commit of exactly: `knowledge/_ux_principle_nodes.json`, `knowledge/_build_kg_explorer.py`, `notes/_KG-EXPLORER.html`, this folder's files, and `knowledge/gen_kg_principles.py` only if step 1 required the fence fix. Message begins `#275 2026-09-15 — s275-D1..D6 ENACTED (lane RL2):`. If `.git/index.lock` exists, STOP and report — do not delete or move it.

## Fences (⛔)
- Never edit `_rulings.json`, any `*.meta.json`, `principles.json`, `polarities.json`, `meta.schema.json`, `_rule_nodes.json`, `_rules-index.json`.
- Never run `gen_kg_edges.py`. Never `git stash`. Never `git checkout`/`restore` a path.
- Textual span edits only; never re-dump a JSON or re-serialise a file you did not generate (a re-dump of `_rulings.json` produced a 3,672-line diff today — reverted).
- Any sentence you present as Dave's must pass `python3 knowledge/_quote_gate.py "<words>"`; on 0, verify against `notes/_lanes/275/DAVE-RULINGS-2026-09-15.md` and say so.
- Land NOTHING else: `inFamily` and `evidencedBy` stay off (s275-D2). No rule → component, no meta citations (s275-D5 is a later authored lane).

## Report back to the conductor (≤ 300 words)
Counts landed · explorer version + chip names · gates with exact result tails · screenshots' paths · commit hash · anything not done and why.
