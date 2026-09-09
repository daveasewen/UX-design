#!/usr/bin/env python3
"""#263 wrap — build `_CARRIES.md` § `## residual → #264` from § `## residual → #263`.

ONE programmatic pass, the #261/#262 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ONE surgical edit, asserted UNIQUE before it is made, by ADDITION with an
      `s183-D1`/`s188-D2` receipt and the original wording left standing verbatim beneath;
  (c) the session's NEW items written in front.

⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause 1.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402  — the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
lines = text.split("\n")
src = [l for l in lines if l.startswith("> **residual → #263:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the ONE strike, asserted UNIQUE ------------------------------------------------------
EDITS = [
    ("⬛ **① THE ELEVEN PROPOSED DEFAULTS NEED A REVIEW PAGE AND A RULING PASS [1, DAVE'S]**",
     "⬛ **① ~~THE ELEVEN PROPOSED DEFAULTS NEED A REVIEW PAGE AND A RULING PASS~~ [1, DAVE'S] "
     "⛔ STRUCK AT #263 WITH ITS `s183-D1`/`s188-D2` RECEIPT: THEY GOT BOTH — A PAGE, AND ELEVEN "
     "RULINGS IN ONE PASS.** The review page is `notes/_PROPOSED-263.html` (lane P, generator "
     "`notes/_lanes/263-P-build.py`, report `notes/_lanes/263-P-proposed-review.md`); ⛔ **it ruled "
     "nothing itself — every row shipped empty and no default was pre-selected.** Dave ruled all "
     "eleven through its export block and they are inscribed as **`s263-D1` … `s263-D11`**, the "
     "store **423 → 434** (`cc875e9`, `7a0c020`). **EIGHT ARE STRAIGHT ACCEPTS** (P-01 the delta "
     "glyph ink seat · P-02 group-row by type · P-03 disabled-column alpha · P-04 adopting "
     "`data-apollo-filter-*` · P-05 the 1400px collapse · P-06 keeping the Tab-bar name · P-10 "
     "`--check` as a wrap gate · P-11 retiring the source-text aria arm). ★ **THE THREE THAT CAME "
     "BACK `LATER` WERE RULED ON HIS OWN SENTENCES RATHER THAN RECORDED AS DEFERRALS:** `s263-D7` "
     "the doormat is a **\"dormant variant\"** of Footer (*\"[p]ark — keep the doormat as a dormant "
     "variant of Footer so it stays one component\"*), which also discharges `s261-D3`'s "
     "*\"for now\"* hedge · `s263-D8` the chart legend **stays 44px** (*\"Is this teh legend for "
     "charts? if so leave it at 44 it works fine\"* → *\"accept\"* once confirmed) · `s263-D9` "
     "`data-dv-controls` **contract-only** (*\"accept contract-only, it's an interesting idea to "
     "wire one legend to multiple charts but not required at this stage\"*). **ENACTED:** D7 + D10 "
     "at `87c7187`, D11 + D12 at `27f0f46`, D13 at `5050b33`. ⛔ **THE HALVES THAT DO NOT DIE HERE "
     "ARE RE-CARRIED, NOT VANISHED:** the wider one-legend-to-many-charts idea is parked in his own "
     "words inside `s263-D9` and is NOT built; and the page was **never driven in a browser** — new "
     "item ⑤ above. Receipts: `notes/_subreports/2026-09-09-263-W-wrap.md` · "
     "`_DECISION-HISTORY/2026-09-09-263-eleven-defaults-and-the-tenth-gate.md` §§1,2. "
     "The original wording stands verbatim below. —"),
]
for find, repl in EDITS:
    assert aged.count(find) == 1, (aged.count(find), find[:80])
    aged = aged.replace(find, repl, 1)

# ---- (c) this session's new items -------------------------------------------------------------
NEW = open(os.path.join(HERE, "carry264-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #264:** " + NEW + " · " + aged[len("> **residual → #263:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #264",
    "",
    "*Written straight here at the #263 wrap (✅ **NO DATE SPLIT — session, ritual and commit are "
    "all 2026-09-09**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for "
    "being old; **one carry STRUCK, by ADDITION and with its `s183-D1`/`s188-D2` receipt**, the "
    "original wording standing verbatim beneath it, and **the half of it that survives the strike — "
    "the page was ruled off a file, never driven — re-carried as a new item rather than vanishing "
    "with it**.*",
    "",
    "<!-- WRITTEN-FIRST: residual → #264 — the aged tail below the SIX new items is the #263 "
    "line put through ONE programmatic pass (`notes/_lanes/263/carry264.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), then 1 surgical edit asserted UNIQUE before it was made "
    "(the strike: the eleven PROPOSED defaults, ruled `s263-D1`…`s263-D11`). Probe count at write "
    "time: %d. -->" % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #263")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
