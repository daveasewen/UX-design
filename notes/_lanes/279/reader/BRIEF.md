# LANE RD — BRIEF — the reader: `_compose_slice.py` wired as step 1 of generate, the thin-slice contract, and the ASK door
#279 · 2026-09-16 · enacting `s277-D10` + `s277-D13` under `s278-D1` · `s274-D11` applies · written by the conductor (Fable 5.1) · **model: fable** — this is the judgement lane the other four Constitution lanes wait on

## Rulings — read them WHOLE in `knowledge/_rulings.json`, do not work from this summary
- **s277-D10**: `_compose_slice.py` — the only door that walks edges and which nothing calls — becomes **step 1 of generate-from-canon** under the thin-slice contract. In: intent + shape + roles + optional component set + budget. Out: components · governs · obeys (authored / derived / routed) · must-not incl. nulls · tokens at group+tier · assets · unresolved · sized. The measured claim to re-measure: 19,117 vs 111,468 tokens (5.8×) for the same dashboard.
- **s277-D13**: ASK — a typed-question door returning the ≤1K-token answering slice for any of the 12 canonical designer questions (`notes/_lanes/277/kg-audit/` names them; A3-AUGMENT.md is the design), built as the SAME lane as the reader.
- **s278-D1**: the slice is a SEED composed once at step 1; ASK is the ON-DEMAND door and READS THE CONSTITUTION LIVE (`knowledge/_rulings.json` + the graph) so a ruling inscribed after the seed was composed is answerable without recomposing. One contract, two halves.
- **s274-D11**: an instrument without a consumer is refused — the reader lands in the SAME commit as its consumer. Here the consumer is the generate step in `designer-skills-v2/` (find the step-1 code that today reads the 138 metas + canon.css; it is what D10 says gets replaced/prefaced).
- **s277-D4..D7** landed this morning (`f641242`): `knowledge/_icon_nodes.json` / `_logo_nodes.json`, 688 nodes, family `assets`. The slice's `assets` field reads those.

## What you build
1. **The contract, as code and as a spec** — `knowledge/_compose_slice.py` gains the typed in/out above. Write the spec in the module docstring AND in `knowledge/_RUNBOOK-compose-from-canon.md` by ADDITION (a new section; no existing line rewritten). Every output field either carries content or a declared null with a note — the house rule (`s274-D7..D12` shape).
2. **Step 1 wiring** — generate-from-canon calls `_compose_slice.py` first and works from the slice; the metas/canon.css read is no longer step 1's default. Keep the old path reachable behind a flag if removing it would break a gate; say which.
3. **ASK** — `python3 knowledge/_compose_slice.py --ask "<question>"` (or a function `ask(question, seed=None)`) for the 12 canonical questions: maps the question to its typed shape, walks the LIVE graph + rulings, returns ≤1K tokens (measure with tiktoken cl100k; refuse loudly over budget, never truncate silently). Unmappable question ⇒ a legal refusal that names the first obstacle.
4. **Measure, don't assert** — re-run the 19,117 vs 111,468 claim on the real generate step for the same dashboard, publish the two numbers you get with the command that produced them. If the ratio moved, say so; do not re-type the ruling's figure.
5. **Tests** — a `--selftest` with named bites for: every out field present; nulls carry notes; ASK ≤1K on all 12 questions; ASK sees a ruling inscribed AFTER the seed (plant one in a scratch copy of `_rulings.json`, never the live file); seed is unchanged by ASK; budget refusal. Then `_validate_kg.py` and any generate gate the runbook names — all green on the live tree.

## Cautions (all from #277's lessons, every one paid for)
- Verify against the LIVE file: before you name a field, an edge type, a prop or a node id in code or prose, grep it in the tree. Two of twenty-nine `$why` sentences last session named things that did not exist and three Opus seats passed them.
- Never `git stash` · never `gen_kg_edges.py` · never `_build_all.py` · never `_build_kg_explorer.main()` · builders that write on import exist (`_build_page.py`, `_dry_run.py` class) — check before importing.
- `.git/index.lock` stale ⇒ `mv` to `.git/_orphan-locks/`, never `rm`. The mount cannot unlink locks; lane IL used a `git` wrapper on PATH that `mv`s them — `/tmp/gitshim/git` may still exist, or recreate it.
- `git status` clean except your paths; `notes/_dream/_GRADE-DECISIONS.jsonl` is already dirty — leave it.
- Do NOT touch `_build_kg_explorer.py` (the explorer relabel is lane (ii), after you).

## Report — `notes/_lanes/279/reader/REPORT.md` + copy at `notes/_subreports/2026-09-16-279-RD-reader.md`
Contract as landed · the wiring diff · ASK's 12 answers with their token counts · the measured claim with commands · every gate line · `git diff --numstat` re-read from the SHIPPED sha · what lanes (ii)–(v) can now consume. The subreport needs a `_state.json` row (`_state.add()` — read `knowledge/_state.py` for the shape; lane IL owed one for `notes/_subreports/2026-09-16-279-IL-icons-land.md` — add that row too, it is the same seat).
One commit via `SESSION_N=279 SHOWROOM_ACK=1 bash knowledge/_git_commit.sh --reconciled <fresh msgfile> <paths…>` — FRESH msgfile per attempt (`/tmp/_msg-279-RD-$(date +%s).txt`), bare subject, no "after #279" prefix. Subject: `#279 lane RD: the reader — _compose_slice.py is step 1, thin-slice contract + ASK door, s277-D10/D13 under s278-D1`.
Paths in bash: `/sessions/laughing-elegant-feynman/mnt/UX-design/`. `pip install tiktoken --break-system-packages` first.
