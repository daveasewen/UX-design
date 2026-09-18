# #284 — WRAP BRIEF (delegated wrap, Opus 5; conductor Fable 5.1)

**Session #284 · 2026-09-18 · ONE DAY, no date split · title `Apollo - #284: the logo masters, at last`**

## THE JOB
Run the capture ritual for #284 exactly as the runbook says. Read, in this order, before doing anything:
1. `knowledge/_RUNBOOK-capture-ritual.md` (or whichever file `ls knowledge/_RUNBOOK-*.md` shows is the wrap ritual — if the name differs, say which you used) — every step, in order, including 2c/2d/2f rolls through `_gm_move.py`, 2g index rebuild LAST, step 3 cloud memory, 4b rename line, 4c scratch hygiene, step 5 commit + push + CI read-back.
2. `notes/_lanes/283/W/WRAP-REPORT.md` and `notes/_subreports/2026-09-18-283-W-wrap.md` — the previous wrap's shape; match it.
3. `_HANDOFF-134-the-seam-check-is-born-and-the-disk-is-diagnosed.md` — write `_HANDOFF-135-…` in the same form.
4. `notes/_lanes/284/DAVE-RULINGS-2026-09-18.md` — his words verbatim. Do not paraphrase them anywhere.

## WHAT HAPPENED IN #284 — every figure below is DECLARED by the conductor; MEASURE each at your seat and publish both where they disagree

- **The disk lever.** #283 said the full disk was "not fixable from his Mac". Dave pasted a how-to; the conductor instructed him; he quit the app and trashed `claudevm.bundle` in `~/Library/Application Support/Claude/`, leaving the `warm` folder. `/sessions` went 98.7% (127,716 KB free) → 0.1% (9,665,792 KB free), `uptime` 1 min, the 127 dead homes gone. **This session survived the rebuild** (same chat continued). Filed at `notes/_lanes/284/DISK-LEVER-2026-09-18.md` (committed in `ade8a403`). Dave's words: *"we've done all this i guess"*. NOT a ruling; a finding + an act.
- **The seam ritual was obeyed:** `_seam.py` before the lane read `FILL 147,056 real / 11 turns · boot 80,882 · ✅ 32,944 under the 180,000 stop line`; after the lane `172,494 / 17`; after the commit `195,366 / 36 · ⚠ STOP LINE 180,000 PASSED — tolerated to 220,000`.
- **ONE LANE, Opus 5, lane LM — the 40 per-size logo masters.** Brief `notes/_lanes/284/logo-masters/BRIEF.md`. Report `notes/_subreports/2026-09-18-284-LM-logo-masters.md`. Output: `knowledge/assets/logos/_gen_masters.py` (generator, `--check` rc 0) + `knowledge/assets/logos/masters/` 40 SVGs, raw px width/height, NO viewBox, hexagon exact on the h/4 grid, wordmark stems snapped; masterbrand widths 89/104/119/133/148 (rounded; floor alternative named in the report). Contact sheet `notes/_lanes/284/logo-masters/MASTERS-2026-09-18.html` + shots. Sub tokens **159,965 (n=1)**, 57 tool uses, 797 s. Fable reviewed the 1:1 and 4× shots by eye. One flaw the lane named: the B's horizontals a pixel off the H's crossbar at 24 and 40. **Dave: *"the sheet is good BTW"* — ACCEPTED BY EYE.** `s282-D3` is thereby ENACTED. Not registered in `_logo_nodes.json` (generator fence) — follow-on, owed.
- **Store row `W-284lm`** added (owner dave; close = sheet accepted [DONE by his word] + registration in `_logo_nodes.json` [OWED]). Update the row's state/wording only as the runbook licenses.
- **ONE COMMIT: `ade8a403`**, UNPUSHED at this brief's cut. Path: `SESSION_N=284 SHOWROOM_ACK=… bash knowledge/_git_commit.sh --reconciled <msgfile> <named paths>` — the `#243` declared not-a-wrap form, showroom drift inherited (138 vs inscribed 108), doc-row gate satisfied by the store row, `_CHAIN.md` regenerated and staged. **The commit took SIX runs**: showroom refusal (ack'd), doc-row refusal (row added), chain-stale refusal (regenerated), then a stranded `.git/index.lock` twice because runbook step 0 (`allow_cowork_file_delete`) had been SKIPPED — once granted, `rm -f .git/index.lock` worked and the commit landed. **The grant is ACTIVE for this session** — you may `rm` locks; the shim is gone (rebuild) and not needed.
- **NO RULING INSCRIBED this session** — `_rulings.json` stays 620. Verify by `json.load` count. Two ruling-shaped things are on the table (below), neither inscribed; inscribing is Dave's. Do NOT inscribe them.
- **THE WINDOW FINDING and Dave's CORRECTION.** Research (Anthropic help centre, "How large is the context window on paid Claude plans?", updated ~2 weeks ago): Fable 5.1 / Opus 5 in Cowork on a paid plan have a **1M** window; auto-compaction near the limit; "tools and connectors are token-intensive". The conductor proposed re-basing the stop line; **Dave corrected: the 180,000 line was gauged against the MESSY-MIDDLE (quality) problem, not the window — it STANDS.** What the finding still changes: the 256,000 "hard" figure is not a wall for this model, so #277/#281/#282's "hard-line breaches" were quality breaches — a WORDING fix in `_gauge_tokens.py`, Dave's to order, NOT done. Verbatim in the rulings file.
- **THE DELEGATION LAPSE — Dave's words, ruling-shaped, restating #57/`s204-D1`:** everything delegated, the conductor is orchestrator + judgment layer. The conductor did lane work in-seat four times (disk/spec ~15K · six commit runs ~30K · two screenshots read in-seat · research in-seat). Only the drawing was a lane. The conductor's proposed mechanical fix, NOT built: `_seam.py` gains a conductor in-seat tool-output arm since the last seam, warning above a threshold; the opener states routing before the first beat; the commit is a lane by default. These are #285's first moves (below).
- **Fill drivers, named:** tool output ~107K at the opener (handoff + chain + check-in + memory index), the six commit runs, two images. The lane cost the window ~300 tokens.

## GAUGE — measure, do not copy
- FILL: measure first-hand from the conductor's transcript (`python3 knowledge/_checkin.py --window 200000 --no-block` and `_seam.py`); the conductor's last reading was **195,366 real / 36 turns** before the research and this brief; expect ~205–215K at cut. Publish the DECLARED and the MEASURED figure and the delta. The stop line 180,000 was PASSED; ≤220,000 tolerated; 256,000 not breached — and say, in the gauge line, that per Dave's correction the 180,000 line is the quality line and the 256,000 figure is not a wall for this model (finding, not re-base).
- BOOT: **80,882 real, n=1**, NINTH post-diet reading over the 70,000 ceiling; NOT a re-base; the ceiling literal is not moved.
- subs: **159,965, n=1** (lane LM). One lane only. No pace panel asked for; invent none.
- Disk: measure `df /sessions` at your seat.
- Sizes: measure GM / LS / corpus / `_CHAIN.md` as the runbook says.

## #285 — FIRST MOVES, IN ORDER (write these into the handoff)
1. **Routing line at the opener, then a boot experiment:** Dave names which connectors Apollo needs (his; asked, unanswered — *"which connectors Apollo needs"*); connectors detached in Project settings; boot measured cold at the next opener, one variable.
2. **The seam's in-seat arm** (`_seam.py`: conductor tool-output tokens since the last seam, warn above a threshold) — one Opus lane.
3. **`--quiet` on `_git_commit.sh`** (verdict lines only) and the commit run as a lane by default — one Opus lane.
4. Register the 40 masters in `_logo_nodes.json` by a sanctioned run of `gen_kg_icons.py` (the generator that undoes hand-authored state — needs Dave's word on how).
5. The 256,000 wording fix in `_gauge_tokens.py` — Dave's to order.
6. Everything still open on `_HANDOFF-130`…`-134` — nothing there was closed today except that the 40 masters are DRAWN and ACCEPTED; strike nothing without a receipt.

## FENCES
- ⛔ Do NOT inscribe a ruling. Do NOT edit `_gauge_tokens.py` constants. Do NOT run `_build_all.py`, `gen_kg_icons.py`, `land_rests_on.py`, `gen_kg_rules.py`.
- ⛔ Do NOT paraphrase Dave's words; quote the rulings file.
- Instrumentation appends (`notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`): commit them with the wrap as #282/#283 did to clear the push gate; the policy is Dave's.
- Cloud memory (step 3): write `WRAP-MEMORY-HOOK.md` FIRST, then attempt the store write from your seat as #279–#283 did (n=5 measured the runbook's "structural" limit false); record the result at the hook's foot. Memory path prefix `/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/`; index at `index.md` — read it (version token) before editing; new line newest-first above the #283 line. If the memory tools are not available at your seat, say so and leave the hook for the conductor.
- Push is at the conductor's judgment: PUSH, then read CI over the public GitHub API (`GET /repos/daveasewen/UX-design/actions/runs?per_page=1`) and quote status/conclusion literally; claim no colour a queued run doesn't have.
- Title for the next chat: generate with `python3 knowledge/_gen_titles.py --session 284`; the declared title is `Apollo - #285: the routing line and the boot experiment`.

## RETURN CONTRACT
File the full wrap report at `notes/_subreports/2026-09-18-284-W-wrap.md` and `notes/_lanes/284/W/WRAP-REPORT.md`. Return to the conductor ONLY: the handoff path, the commit sha + push verdict line quoted, the CI status line quoted, measured FILL/boot/subs, the memory write result (version or "not reachable"), the rename line for chat, and any measurement that disagreed with this brief.
