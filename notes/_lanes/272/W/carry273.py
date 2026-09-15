#!/usr/bin/env python3
"""#272 wrap — build `_CARRIES.md` § `## residual → #273` from § `## residual → #272`.

ONE programmatic pass, the #261…#271 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ TWO SURGICAL EDITS, and BOTH are STRIKES with their `s188-D2` receipts, not rewords:
      · carried item ① of the #272 set ("import his harvest decisions and cut the rulings") is
        DISCHARGED — his export came back 115/115, the cut ran at `d1af846` and `s272-D1..D92`
        were inscribed at `b46ea90`.
      · carried item ② ("the '256' clause is ruling-shaped and was deliberately not inscribed")
        is DISCHARGED — he answered it at #272's opener and `s272-D93` is in the store. ⚠ The
        strike names what did NOT discharge with it: the ENACT is untouched and rides on as
        #273's item ①.
      A discharged carry is STRUCK with its discharge named, never re-typed (`s183-D1`,
      receipt requirement `s188-D2`).
  (c) the session's SIX NEW items written in front.

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
src = [l for l in lines if l.startswith("> **residual → #272:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the TWO surgical edits — both STRIKES, each with its receipt -------------------------
EDITS = []

OLD1 = "⬛ **① IMPORT HIS HARVEST DECISIONS AND CUT THE RULINGS** [1, DAVE'S]"
NEW1 = (
    "~~⬛ **① IMPORT HIS HARVEST DECISIONS AND CUT THE RULINGS** [1, DAVE'S]~~ ⛔ **STRUCK AT "
    "THE #272 WRAP — THE CLAIM IS DISCHARGED AND THE STRIKE CARRIES ITS RECEIPT (`s183-D1` "
    "strike, `s188-D2` receipt): his Export JSON came back **115/115 decided** (104 ratify · 3 "
    "option · 8 decline · 0 later) and was saved verbatim at "
    "`notes/_lanes/272/harvest-decisions-2026-09-14.json`; `knowledge/_cut_harvest_rulings.py` "
    "(12 selftest arms, `--inscribe` refusing without `--ratified`) cut it at `d1af846` into 92 "
    "proposed rulings, a 15-row when-patch and 8 undecided, reviewed on sight at 1280; and on "
    "his *\"were good, inscribe\"* **`s272-D1`…`s272-D92` were inscribed at `b46ea90`, taking "
    "`knowledge/_rulings.json` from 469 to 562**, with the 15 unanimous `when` predicates landed "
    "onto the metas by TEXTUAL SPAN. Correction inscribed at: "
    "`_DECISION-HISTORY/2026-09-15-272-the-cut-and-the-inscription.md` and the ⏱ LATEST DELTA "
    "for #272 in `_LIVE-STATE.md`.** The struck text stands verbatim above rather than being "
    "deleted, because a silently vanished carry is indistinguishable from a dropped one. ⚠ "
    "**WHAT DID NOT DISCHARGE WITH IT: the 8 DECLINES were not ruled** — they are parked as "
    "`P-272-1`…`P-272-4` and carry on as #273's item ②."
)
assert aged.count(OLD1) == 1, aged.count(OLD1)
aged = aged.replace(OLD1, NEW1, 1)
EDITS.append(("carry ① — IMPORT HIS HARVEST DECISIONS AND CUT THE RULINGS",
              "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (s272-D1..D92 / b46ea90)"))

OLD2 = ("⬛ **② THE \"256\" CLAUSE IS RULING-SHAPED AND WAS DELIBERATELY NOT INSCRIBED** "
        "[1, DAVE'S]")
NEW2 = (
    "~~⬛ **② THE \"256\" CLAUSE IS RULING-SHAPED AND WAS DELIBERATELY NOT INSCRIBED** "
    "[1, DAVE'S]~~ ⛔ **STRUCK AT THE #272 WRAP — THE CLAIM IS DISCHARGED AND THE STRIKE CARRIES "
    "ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt): the question was put in one word at "
    "#272's opener and he answered it — *\"we work until around 180, thats the safest but I wont "
    "loose any sleep over hitting 220 for example\"* — and **`s272-D93` is inscribed in "
    "`knowledge/_rulings.json`**: 180,000 is the WORKING figure (soft), an overrun to ~220,000 "
    "is TOLERATED without alarm, 256,000 stays HARD. Correction inscribed at: `b46ea90` · "
    "`notes/_lanes/272/DAVE-RULINGS-2026-09-15.md` § Opener.** The struck text stands verbatim "
    "above rather than being deleted. ⛔ **WHAT DID NOT DISCHARGE WITH IT, AND IT IS THE WHOLE "
    "OF #273's ITEM ①: NO CONSTANT MOVED AND NO ARM WAS WIRED** — `_gauge_tokens.STOP_LINE_TK` "
    "is still `180_000`, nothing in the machine knows the word \"220\", and whether the "
    "tolerance becomes a named arm (and at what tier) is UNRULED and his."
)
assert aged.count(OLD2) == 1, aged.count(OLD2)
aged = aged.replace(OLD2, NEW2, 1)
EDITS.append(("carry ② — THE \"256\" CLAUSE",
              "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (s272-D93 / b46ea90); the "
              "ENACT half explicitly NOT discharged and carried on as #273 item ①"))

assert len(EDITS) == 2

# ---- (c) this session's new items -------------------------------------------------------------
NEWITEMS = open(os.path.join(HERE, "carry273-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #273:** " + NEWITEMS + " · " + aged[len("> **residual → #272:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #273",
    "",
    "*Written straight here at the #272 wrap (⚠ **WRAP DATE SPLIT, FOURTH OCCURRENCE — the "
    "session opened 2026-09-14 evening, his answers and all four commits are 2026-09-15, and "
    "nothing was re-dated**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing "
    "dropped for being old; ★ **TWO carries STRUCK, and BOTH are DISCHARGES rather than "
    "retractions** — item ① of the #272 set (import his harvest decisions and cut the rulings) "
    "was closed by his 115/115 export, the cut at `d1af846` and the inscription at `b46ea90`, "
    "and item ② (the \"256\" clause, ruling-shaped and deliberately uninscribed) was closed by "
    "his answer at this session's opener and `s272-D93`. Each is struck with its "
    "`s183-D1`/`s188-D2` receipt rather than re-typed or deleted, and ⛔ **the ② strike names "
    "what did NOT discharge with it — no constant moved and no arm was wired, so the ENACT "
    "rides on as #273's item ①.** ⛔ **NO OTHER carry was re-worded: the three explorer hues, "
    "the 31 declared guesses, the `roles.json` drift, the HSBC ingestion gap, door v2, the "
    "compose-time door and every #119 open were all CARRIED THROUGH #272 UNTOUCHED — #272 spent "
    "itself on one lane, one cut and one inscription pass, and every one of those items ages "
    "with its wording intact.** ★★★ **Dave ruled NINETY-THREE times at #272 in the "
    "`_rulings.json` sense: the store moved 469 → 562, the largest single session in its "
    "history — `s272-D1`…`s272-D92` the harvest cut (79 of them accepted by a click that the "
    "`says` names as a click) and `s272-D93` the stop-line posture — and the 8 declines, the "
    "four P-272 sidequest shapes and the ~220 ENACT were all deliberately left unruled.***",
    "",
]

out = []
for ln in lines:
    if ln.strip() == "## residual → #272":
        out.extend(SECTION)
        out.append("<!-- WRITTEN-FIRST: residual → #273 — the aged tail below the SIX new "
                   "items is the #272 line put through ONE programmatic pass "
                   "(`notes/_lanes/272/W/carry273.py`): %d age brackets bumped (%d of them "
                   "`NEW — 0` → `1`), and EXACTLY TWO surgical edits, both strikes carrying "
                   "their receipts, asserted as a count of two in the script rather than left "
                   "implicit. Probe count at write time: %d. -->" % (n_new + n_num, n_new, after))
        out.append("")
        out.append(line)
        out.append("")
        out.append("---")
        out.append("")
    out.append(ln)

open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("CARRIES: #272 items %d → #273 items %d (+%d; %d NEW — 0 became countable, %d new items "
      "arrive uncounted)" % (before, after, after - before, n_new, 6))
print("ages bumped: %d numbered + %d NEW — 0 = %d" % (n_num, n_new, n_num + n_new))
for t, w in EDITS:
    print("SURGICAL EDIT: %s — %s" % (t, w))
