#!/usr/bin/env python3
"""#270 wrap — build `_CARRIES.md` § `## residual → #271` from § `## residual → #270`.

ONE programmatic pass, the #261…#269 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ ONE SURGICAL EDIT, and it is a STRIKE with its `s188-D2` receipt, not a reword: carried
      item ⑦ of the #270 set claimed "THE #269 MEMORY HOOK IS OWED — 0 BYTES WERE WRITTEN … the
      wrap sub's memory filesystem is READ-ONLY". That claim is FALSE as of #270: the #269 hook
      `wrap-269-graph-gets-its-atoms.md` exists in the store and is indexed on `MEMORY.md`, and
      the #270 wrap sub WROTE both its own hook and an index line from the same kind of seat. A
      retracted carry is STRUCK with its retraction named, never re-typed (`s183-D1`, and the
      receipt requirement is `s188-D2`).
  (c) the session's NINE NEW items written in front.

⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause 1.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402  — the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
lines = text.split("\n")
src = [l for l in lines if l.startswith("> **residual → #270:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the ONE surgical edit — a STRIKE, with its receipt -----------------------------------
OLD = ("⚠ **⑦ THE #269 MEMORY HOOK IS OWED — 0 BYTES WERE WRITTEN AT THIS WRAP AND THE REASON IS "
       "A SEAT LIMIT, DECLARED NOT SKIPPED** [1]")
NEW = ("~~⚠ **⑦ THE #269 MEMORY HOOK IS OWED — 0 BYTES WERE WRITTEN AT THIS WRAP AND THE REASON "
       "IS A SEAT LIMIT, DECLARED NOT SKIPPED** [1]~~ ⛔ **STRUCK AT THE #270 WRAP — THE CLAIM IS "
       "FALSE NOW AND THE STRIKE CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt): the "
       "#269 hook `wrap-269-graph-gets-its-atoms.md` EXISTS in the store and is indexed on "
       "`MEMORY.md` (the #269 conductor wrote it), and the #270 delegated wrap sub WROTE BOTH its "
       "own hook `wrap-270-the-door-and-the-cutoff.md` AND a `★★★` index line from the same kind "
       "of seat — so the read-only seat limit #269 declared did NOT recur and ritual step 3 is "
       "NOT open for #269. Correction inscribed at: `notes/_subreports/2026-09-14-270-W-wrap.md` "
       "§ What was done, step 3, and the ⏱ LATEST DELTA for #270 in `_LIVE-STATE.md`.** The "
       "struck text stands verbatim above rather than being deleted, because a silently vanished "
       "carry is indistinguishable from a dropped one.")
assert aged.count(OLD) == 1, aged.count(OLD)
aged = aged.replace(OLD, NEW, 1)
EDITS = [("carry ⑦ — #269 memory hook OWED", "STRUCK, s183-D1 + s188-D2 receipt named")]
assert len(EDITS) == 1

# ---- (c) this session's new items -------------------------------------------------------------
NEWITEMS = open(os.path.join(HERE, "carry271-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #271:** " + NEWITEMS + " · " + aged[len("> **residual → #270:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #271",
    "",
    "*Written straight here at the #270 wrap (✅ **NO DATE SPLIT — the session, its ritual and its "
    "commit are all 2026-09-14**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing "
    "dropped for being old; ★ **ONE carry STRUCK, and it is the first strike since #260** — "
    "carried item ⑦ of the #270 set (the #269 memory hook, OWED on a declared read-only seat "
    "limit) is FALSE as of this wrap and is struck with its `s183-D1`/`s188-D2` receipt rather "
    "than re-typed or deleted. ⛔ **NO OTHER carry was re-worded: the roles/DESK and "
    "compose-time-door carries were CONSUMED by #270's lanes but NOT DISCHARGED — both came back "
    "as proposals awaiting Dave's word — so they age with their wording intact and #270's own "
    "new items carry the moved state.** ★★★ **Dave ruled ONCE at #270 in the `_rulings.json` "
    "sense: the store moved 463 → 464 (`s270-D1`, the dropdown cut-off, PROVISIONAL), and "
    "everything in `_HANDOFF-121-the-door-and-the-cutoff.md` § D was deliberately left "
    "unruled.***",
    "",
    "<!-- WRITTEN-FIRST: residual → #271 — the aged tail below the NINE new items is the #270 "
    "line put through ONE programmatic pass (`notes/_lanes/270/W/carry271.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), and EXACTLY ONE surgical edit, a strike carrying its "
    "receipt, asserted as a count of one in the script rather than left implicit. Probe count at "
    "write time: %d. -->"
    % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #270")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · 1 STRIKE · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
