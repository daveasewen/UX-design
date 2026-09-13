#!/usr/bin/env python3
"""#268 wrap — build `_CARRIES.md` § `## residual → #269` from § `## residual → #268`.

ONE programmatic pass, the #261…#267 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ONE surgical edit, asserted UNIQUE before it is made, by ADDITION with an
      `s183-D1`/`s188-D2` receipt and the original wording left standing verbatim beneath;
  (c) the session's EIGHT NEW items written in front.

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
src = [l for l in lines if l.startswith("> **residual → #268:**")]
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
    # The #268 lead named three things. TWO were discharged and the THIRD was not: the
    # run-of-show was FILLED but never REHEARSED with Dave. The strike is therefore PARTIAL
    # and says so — a whole-headline strike here would retire a rehearsal that never happened.
    ("⬛ **① REHEARSE THE RUN-OF-SHOW, v1.0.11 CANON, THE ISLANDS** [1, DAVE'S]",
     "⬛ **① ~~REHEARSE THE RUN-OF-SHOW~~, ~~v1.0.11 CANON~~, ~~THE ISLANDS~~ — ⚠ PARTIAL "
     "STRIKE** [1, DAVE'S] ⛔ **STRUCK AT #268 WITH ITS `s183-D1`/`s188-D2` RECEIPT, AND THE "
     "STRIKE IS PARTIAL BECAUSE ONE OF THE THREE DID NOT HAPPEN.** **(a) THE RUN-OF-SHOW WAS "
     "FILLED, NOT REHEARSED.** `notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html` gained plot "
     "points **03** (the gearbox metaphor, Dave verbatim + a two-sentence spoken draft, "
     "`2ec4a28`), **04** (reframed on `s268-D8` — 15% HSBC / 47% IBM Carbon / the 6→6 "
     "hypothesis, `ae54cfd`) and **05** (K1–K5 off the evidence page); the `tr.beat`/`div.beat` "
     "selector collision was fixed (`011fb34`) and **Risks 1/2/5/7 were RETIRED ON "
     "MEASUREMENT** with Risk 3 closed on Dave's word (`ee864de`, `bfa2a77`). ⚠ **NOBODY "
     "REHEARSED IT OUT LOUD WITH HIM** — the carry's own verb is still owed and is re-carried "
     "in front of this line as this session's ① and ⑥. **(b) v1.0.11 CANON: DISCHARGED, AND "
     "THEN TWICE MORE.** v1.0.11 shipped the regenerated canon.css (`s268-D1`) and its own "
     "version sweep went red on three literals ⇒ **v1.0.12** (`s268-D2`) ⇒ the descender crop "
     "survived into the shipped zip ⇒ **v1.0.13** (`s268-D3`), **cold-run-9 14/14, `--check` "
     "GREEN, 10/10 release gates**. **(c) THE ISLANDS: DISCHARGED, AS A PICTURE.** The three "
     "KG islands are now the deck's title card — a fly-through, white pinprick nodes, "
     "mouse-nudged, no return-to-path (`74bb582`…`8916639`), and card 2 reverses the same "
     "animation out through a difference blend (`eb820ce`). Where the correction is inscribed: "
     "`_LIVE-STATE.md` ⏱ LATEST DELTA #268, the ★ LATEST #268 banner, and "
     "`_HANDOFF-119-the-designer-pack-and-the-deck.md`. The original wording stands verbatim "
     "below."),
]
for find, repl in EDITS:
    assert aged.count(find) == 1, (aged.count(find), find[:90])
    aged = aged.replace(find, repl, 1)

# ---- (c) this session's new items -------------------------------------------------------------
NEW = open(os.path.join(HERE, "carry269-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #269:** " + NEW + " · " + aged[len("> **residual → #268:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #269",
    "",
    "*Written straight here at the #268 wrap (✅ **NO DATE SPLIT — the wrap ritual and its commit "
    "are both 2026-09-13**; ⚠ the SESSION itself spans 2026-09-11 → 2026-09-13 and its commits "
    "carry their own true dates, which is a multi-day session and not the #241 shape) under "
    "`s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for being old; **ONE carry "
    "PARTIALLY STRUCK, by ADDITION and with its `s183-D1`/`s188-D2` receipt**, the original "
    "wording standing verbatim beneath — the #268 LEAD, two of whose three items were discharged "
    "and one of which (the REHEARSAL itself) was not. ★★★ **Dave ruled EIGHT times at #268 in the "
    "`_rulings.json` sense: the store moved 445 → 453 (`s268-D1` … `s268-D8`), and `s268-D7` was "
    "SUPERSEDED by `s268-D8` the same day on a vocabulary collision.***",
    "",
    "<!-- WRITTEN-FIRST: residual → #269 — the aged tail below the EIGHT new items is the #268 "
    "line put through ONE programmatic pass (`notes/_lanes/268/W/carry269.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), then 1 surgical edit asserted UNIQUE before it was "
    "made (the PARTIAL strike above). Probe count at write time: %d. "
    "⚠ DECLARED, NOT DISCOVERED: the strike is PARTIAL and says so in its own headline, because "
    "the carry's verb was REHEARSE and no rehearsal took place — filling the page is not "
    "performing it. -->"
    % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #268")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
