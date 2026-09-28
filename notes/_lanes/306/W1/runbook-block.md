### ★ PHASE 1 — THE WRAP RUNS TOOLS, NOT SCRIPTS (`s306-D4`, #306, 2026-09-28; added by addition — no step below is rewritten)

Dave, 16:58 BST, *"go on both"*, to *"Build phases 1 and 2 now: turn the wrap's throwaway scripts into permanent tools"*
(`notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md`). Built by #306 lane W1 (`notes/_subreports/2026-09-28-306-W1-phase1-tools.md`).
Each step below still says WHAT to write; this says HOW. **Write no script in `_work/`: every command takes files and arguments.**
Each tool: `--help`, `--selftest`, dry run unless `--write` / `--run`. `s306-D4` stays `ruled` until one real wrap proves
scripts 11 → 0, move files 9 → 1, rebuilds 5 → 1 (#305's counts).

| step | command |
|---|---|
| every figure (fill, subs, rulings, store, carries, sizes, shas) | `_wrap_facts.py --out <n>/W/FACTS.json --session N --rulings-base <opener sha> --since <last wrap sha> --transcript <conductor jsonl> --until <launch ISO> --subagents-dir <dir> --exclude <own jsonl>` |
| 2, 2c, 2d, 2f (banner, rolls, stratum, delta, stamp, title) | prose in files (a line `{{SECTION_SIZES}}` / `{{ROLL_STATE}}` is measured for you) → `_wrap_ops.py --session N --date D --banner --stratum --delta --stamp [--title] [--date-split] --out <n>/W/_ops-NW.json` → `_gm_move.py --ops … --dry-run`, then without |
| carries | `_wrap_carries.py roll --from N --to N+1 --new new.txt` · `strike --section N+1 --title '**…**' --note-file f` · `count`; `--write` to write |
| state rows | `_wrap_rows.py --spec rows.json`, then `--write` (mint born closed, close/reopen by addition) |
| 2g, 4b titles, 4d, the chain | `_wrap_regen.py --run --log <n>/W/_regen.log --paths-out <n>/W/paths.txt` — ONCE, after the last edit |
| 5 | `_wrap_commit.py msg --out … --line1 …` · `paths --out … --dir notes/_lanes/<n>/W …` · `commit --session N --msg … --paths … --log …`; a stranded lock: `unlock --tag <n>-W` |
| 5 CI, 5b | `_ci_readback.py` (block below, `s306-D7`) · the 5b line: `_wrap_ops.py --fill-token … --fill-file _LIVE-STATE.md --fill-text 5b.md --out …` |

(`<n>/W` = `notes/_lanes/<n>/W`; every tool is `python3 knowledge/<tool>`.) Unchanged: `_gm_move.py`, `_roll_state.py`,
`_gen_size_stamp.py --write`, `_state.py`, `_capture_gate.py`, `_git_commit.sh`. Still hand-written until phase 3: the prose (handoff, dossier,
W report, memory payload, summary).

