#!/usr/bin/env python3
"""#274 wrap — build `_CARRIES.md` § `## residual → #275` from § `## residual → #274`.

ONE programmatic pass, the #261…#273 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ TWO SURGICAL EDITS, both carrying their `s183-D1`/`s188-D2` receipts, never rewords:
      · #274's item ① (the four list-vs-card decisions are on the page and not one is ruled)
        is DISCHARGED — `s274-D1`…`s274-D5` ruled all four and the headers, `04c51c6`, and
        `58f56ef` enacted them onto `list-items.meta.json`.
      · #274's item ② (`s273-D2` authoring pass two is scoped, ruled and not started) is NOT
        discharged — pass two still has not started — but ONE CLAUSE inside it is now FALSE
        ("`record-list` waits on LC-1"), so the item takes a CORRECTION BY ADDITION naming
        the ruling ids and the commit, per `s188-D2`. The item itself is carried on.
  (c) the session's EIGHT NEW items written in front.

⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause 1.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402 — the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
lines = text.split("\n")
src = [l for l in lines if l.startswith("> **residual → #274:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the TWO surgical edits ---------------------------------------------------------------
EDITS = []

OLD1 = "⬛ **① THE FOUR LIST-vs-CARD DECISIONS ARE ON THE PAGE AND NOT ONE IS RULED** [1, DAVE'S]"
NEW1 = (
    "~~⬛ **① THE FOUR LIST-vs-CARD DECISIONS ARE ON THE PAGE AND NOT ONE IS RULED** "
    "[1, DAVE'S]~~ ⛔ **STRUCK AT THE #274 WRAP — THE CLAIM IS DISCHARGED AND THE STRIKE "
    "CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt): all four decisions were ruled "
    "at #274, and NOT by picking options off the page — he answered by describing a model "
    "nobody had proposed, two levels with the containers over the rows, and then corrected "
    "the read-back in one sentence. `04c51c6` inscribed `s274-D1` (**the line is SURFACE "
    "ALONE** — a record is a card when its container draws a bordered surface around it; "
    "actions are a row property legal in any container), `s274-D2` (one meta, variants = the "
    "three CONTAINERS), `s274-D3` (`account-card` stays `$not-a-provider`), `s274-D4` (no "
    "cardinality gate, the comparison test decides) and `s274-D5` (a list-level heading is "
    "optional on all three; a per-card title is a row field); `58f56ef` enacted every one of "
    "them onto `knowledge/components/list-items.meta.json` by textual span. Correction "
    "inscribed at: `04c51c6` · `58f56ef` · `knowledge/_rulings.json` §§ `s274-D1`…`s274-D5` · "
    "`notes/_lanes/274/DAVE-RULINGS-2026-09-15.md` · "
    "`_DECISION-HISTORY/2026-09-15-274-the-line-and-the-rules.md`.** The struck text stands "
    "verbatim above rather than being deleted, because a silently vanished carry is "
    "indistinguishable from a dropped one. ⚠ **WHAT DID NOT DISCHARGE WITH IT: `P-272-1` "
    "itself is not closed** — the modal, navigation and smaller-opens sidequests `P-272-2`…"
    "`P-272-4` are untouched, and the LANE'S OWN vocabulary on the enacted meta "
    "(`bordered-per-record`, `$level: \"typeset\"`) plus its three proposals are carried on "
    "as item ③ of the #275 set."
)
assert aged.count(OLD1) == 1, aged.count(OLD1)
aged = aged.replace(OLD1, NEW1, 1)
EDITS.append(("carry ① — THE FOUR LIST-vs-CARD DECISIONS",
              "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (s274-D1..D5, 04c51c6 + "
              "58f56ef); P-272-1 and the lane's vocabulary explicitly NOT discharged"))

OLD2 = ("⚠ **② `s273-D2` AUTHORING PASS TWO IS SCOPED, RULED AND NOT STARTED** [1]")
NEW2 = (
    "⚠ **② `s273-D2` AUTHORING PASS TWO IS SCOPED, RULED AND NOT STARTED** [1] ⛔ **ONE CLAUSE "
    "INSIDE THIS CARRY IS CORRECTED AT THE #274 WRAP, BY ADDITION AND WITH ITS RECEIPT "
    "(`s188-D2`) — THE ITEM ITSELF IS NOT DISCHARGED AND RIDES ON:** where the text below "
    "says *\"`record-list` waits on LC-1 and `input` waits on the sub-roles, so neither can be "
    "briefed yet\"*, **`record-list` NO LONGER WAITS** — `s274-D1`…`s274-D5` ruled the "
    "list/card line and `s274-D6` made `list-items` the default provider of `record-list` "
    "with table taking the comparison test. **`input` still waits on the sub-roles, and pass "
    "two still has not started.** Correction inscribed at: `04c51c6` · `3a752d1` · "
    "`knowledge/_rulings.json` §§ `s274-D1`…`s274-D6`."
)
assert aged.count(OLD2) == 1, aged.count(OLD2)
aged = aged.replace(OLD2, NEW2, 1)
EDITS.append(("carry ② — s273-D2 AUTHORING PASS TWO",
              "CORRECTED BY ADDITION with its s188-D2 receipt (record-list unblocked by "
              "s274-D1..D6); the carry is NOT discharged and is carried on"))

assert len(EDITS) == 2

# ---- (c) this session's new items -------------------------------------------------------------
NEWITEMS = open(os.path.join(HERE, "carry275-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #275:** " + NEWITEMS + " · " + aged[len("> **residual → #274:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #275",
    "",
    "*Written straight here at the #274 wrap (✅ **NO DATE SPLIT — the session, its ritual and "
    "all eight of its commits are 2026-09-15**) under `s225-D2` clause (i). Ages +1, wording "
    "unchanged, nothing dropped for being old; ★ **ONE carry STRUCK and ONE carry CORRECTED, "
    "and the difference between them is the point** — item ① of the #274 set (the four "
    "list-vs-card decisions are on the page and not one is ruled) is **DISCHARGED**, because "
    "`s274-D1`…`s274-D5` ruled all four and `58f56ef` enacted them; item ② (`s273-D2` "
    "authoring pass two is scoped, ruled and not started) is **NOT** discharged — pass two has "
    "still not started — but one clause inside it went false when `record-list` was unblocked, "
    "so it takes a correction BY ADDITION with its `s188-D2` receipt and rides on. ⛔ **NO "
    "OTHER carry was re-worded: the three explorer hues, the 31 declared guesses, the HSBC "
    "ingestion gap, the two blocking tiers, the 79 clicks, the #179 reformat class, the #243 "
    "double-count and every #119 open were all CARRIED THROUGH #274 UNTOUCHED and age with "
    "their wording intact.** ★★★ **Dave ruled twelve times at #274 — the store moved 566 → "
    "578 — and the session's shape was one line drawn (`s274-D1`…`s274-D6`, surface alone, "
    "list-items the default) and one family admitted to the graph (`s274-D7`…`s274-D12`, 470 "
    "guideline rules as `rule:<id>` nodes with four ratified edge types). ⛔ **The eight new "
    "items below are every question this session opened and did not close, and all but one of "
    "them are his.***",
    "",
]

out = []
for ln in lines:
    if ln.strip() == "## residual → #274":
        out.extend(SECTION)
        out.append("<!-- WRITTEN-FIRST: residual → #275 — the aged tail below the EIGHT new "
                   "items is the #274 line put through ONE programmatic pass "
                   "(`notes/_lanes/274/W/carry275.py`): %d age brackets bumped (%d of them "
                   "`NEW — 0` → `1`), and EXACTLY TWO surgical edits — ONE strike and ONE "
                   "correction-by-addition, both carrying their receipts, asserted as a count "
                   "of two in the script rather than left implicit. Probe count at write "
                   "time: %d. -->" % (n_new + n_num, n_new, after))
        out.append("")
        out.append(line)
        out.append("")
        out.append("---")
        out.append("")
    out.append(ln)

open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("CARRIES: #274 items %d → #275 items %d (+%d; %d NEW — 0 became countable, %d new items "
      "arrive uncounted)" % (before, after, after - before, n_new, 8))
print("ages bumped: %d numbered + %d NEW — 0 = %d" % (n_num, n_new, n_num + n_new))
for t, w in EDITS:
    print("SURGICAL EDIT: %s — %s" % (t, w))
