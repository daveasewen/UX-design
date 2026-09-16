#!/usr/bin/env python3
"""#278 wrap — build `_CARRIES.md` § `## residual → #279` from § `## residual → #278`.

ONE programmatic pass, the #261…#277 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ ONE SURGICAL EDIT, carrying its `s183-D1`/`s188-D2` receipt:
      · #278's ② (the `s277-D13` clause, one word at #278's opener) — DISCHARGED by `s278-D1`
        on Dave's *"Ill go with you, lets just move on to the other graph work"*. STRUCK.
  (c) the session's ONE NEW item written in front.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause 1.
"""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","..","..",".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #278:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -----------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the ONE surgical edit ------------------------------------------------------------
OLD = ("⬛ **② THE `s277-D13` CLAUSE IS ONE WORD AT #278'S OPENER, AND IT IS WRITTEN INTO THE "
       "RULING AS AN OPEN QUESTION** [1, DAVE'S]")
NEW = ("~~⬛ **② THE `s277-D13` CLAUSE IS ONE WORD AT #278'S OPENER, AND IT IS WRITTEN INTO THE "
       "RULING AS AN OPEN QUESTION** [1, DAVE'S]~~ ⛔ **STRUCK AT THE #278 WRAP — THE WORD CAME "
       "AND THE STRIKE CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt).** Dave, verbatim "
       "on the read-back: *\"Ill go with you, lets just move on to the other graph work\"* "
       "(`notes/_lanes/278/DAVE-RULINGS-2026-09-16.md`). Inscribed as **`s278-D1`** — the thin "
       "slice is a **SEED**, composed once at step 1 by `_compose_slice.py`, and **ASK is the "
       "ON-DEMAND DOOR** that reads the Constitution live for what the seed lacks; seed and door "
       "under one contract. Correction inscribed at: `knowledge/_rulings.json` § `s278-D1` "
       "(store 603 → 604, `git diff --numstat` `15  0`) · `_HANDOFF-129-the-cloud-move-and-the-seed.md`. "
       "⚠ The clause is DISCHARGED; the ENACTMENT of `s277-D8`…`s277-D13` is NOT, and rides on as "
       "item ① above.")
assert aged.count(OLD) == 1, ("strike anchor", aged.count(OLD))
aged = aged.replace(OLD, NEW, 1)

# ---- (c) the session's ONE new item -------------------------------------------------------
NEWITEM = (
 "⬛ **① THE CLOUD MEMORY STORE CARRIES THREE OBLIGATIONS AND NOT ONE OF THEM IS RULED** "
 "[NEW — 0, DAVE'S] — the Cowork memory directory became the claude.ai Project memory at "
 "#278 (import 2026-09-16 03:14–17Z, `sources: [cowork-import]`), and three things came with "
 "it that no ruling covers. **(a) COMPACTION** — the cloud index file caps at **49,152 B** and "
 "the pre-import index did not come across, so the file was restarted from the #277 line; "
 "periodic compaction is owed and the dream pass is its seat, not urgent at one line but "
 "un-scheduled. **(b) THE ONE-WAY RE-IMPORT RISK** — an Anthropic re-import could overwrite "
 "cloud-only lines, which is harmless **only for as long as the repo holds everything durable**; "
 "the accelerator/record split is therefore load-bearing rather than a preference, and nothing "
 "checks it. **(c) THE WRITE SCOPE** — the store is account-wide on READ (other Projects' "
 "subtrees are visible) and Apollo-only on WRITE, so keeping Apollo files Apollo-only is a "
 "discipline with no gate behind it. ⛔ **And the seat limit under all three: only the "
 "CONDUCTOR'S seat can write cloud memory** — a delegated wrap sub cannot reach the store at "
 "all, so every wrap's memory line arrives through `notes/_lanes/<n>/WRAP-MEMORY-HOOK.md` and "
 "is placed at the NEXT opener (`d7b8d72` placed #277's). Receipts: "
 "`_HANDOFF-129-the-cloud-move-and-the-seed.md` § WHAT MOVED · `knowledge/_RUNBOOK-capture-ritual.md` "
 "step 3, which took the pattern by ADDITION at this wrap · `notes/_lanes/278/WRAP-MEMORY-HOOK.md`.")

line = "> **residual → #279:** " + NEWITEM + " · " + aged[len("> **residual → #278:** "):]
after = len(cg._carry_items(line))

HEADER = (
 "---\n\n## residual → #279\n\n"
 "*Written straight here at the #278 wrap (✅ **NO DATE SPLIT — the session, its ritual and all "
 "of its commits are 2026-09-16**) under `s225-D2` clause (i). Ages +1, wording unchanged, "
 "nothing dropped for being old; ★ **ONE carry STRUCK, with its receipt.** #278 was a "
 "HOUSEKEEPING session — no graph work by design — so it mints ONE new carry, not thirteen.*\n\n"
 f"<!-- WRITTEN-FIRST: residual → #279 — the aged tail below the ONE new item is the #278 line "
 f"put through ONE programmatic pass (`notes/_lanes/278/W/carry279.py`): {n_num + n_new} age "
 f"brackets bumped ({n_new} of them `NEW — 0` → `1`), and EXACTLY ONE surgical edit — a STRIKE "
 f"carrying its `s183-D1`/`s188-D2` receipt, asserted as a count of one in the script rather "
 f"than left implicit. Probe count at write time: {after}. -->\n\n"
 + line + "\n\n")

if "--write" not in sys.argv:
    print(f"DRY: ages bumped {n_num + n_new} ({n_new} NEW→1) · 1 strike · 1 new item · "
          f"carries {before} → {after}")
    sys.exit(0)
MARK = "---\n\n## residual → #278\n"
assert text.count(MARK) == 1
text = text.replace(MARK, HEADER + MARK, 1)
open(CARRIES, "w", encoding="utf-8").write(text)
print(f"WROTE § residual → #279: ages bumped {n_num + n_new} ({n_new} NEW→1) · "
      f"1 strike · 1 new item · carries {before} → {after}")
