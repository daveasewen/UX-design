#!/usr/bin/env python3
"""#275 wrap — build `_CARRIES.md` § `## residual → #276` from § `## residual → #275`.

ONE programmatic pass, the #261…#274 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ TWO SURGICAL EDITS, both carrying their `s183-D1`/`s188-D2` receipts, never rewords:
      · #275's item ① (the 145 principles into the graph, then authoring pass two) is NOT
        discharged — `s273-D2` pass two still has not started — but its FIRST HALF is now
        false: the principles ARE in the graph. CORRECTION BY ADDITION, item rides on.
      · #275's item ② (`_rule_nodes.json`'s `$description` still says "PROPOSED … NOT
        RATIFIED") is DISCHARGED — `ef1213b` replaced that span with the ratifying id.
        STRUCK, with its receipt named.
  (c) the session's NINE NEW items written in front.

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
src = [l for l in lines if l.startswith("> **residual → #275:**")]
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

OLD1 = "⬛ **① THE 145 PRINCIPLES INTO THE GRAPH, THEN AUTHORING PASS TWO** [1, DAVE'S]"
NEW1 = (
    "⬛ **① THE 145 PRINCIPLES INTO THE GRAPH, THEN AUTHORING PASS TWO** [1, DAVE'S] ⛔ **THE "
    "FIRST HALF OF THIS CARRY IS DISCHARGED AT THE #275 WRAP AND THE SECOND HALF IS NOT, SO IT "
    "IS CORRECTED BY ADDITION WITH ITS RECEIPT (`s188-D2`) AND RIDES ON:** the **145 UX "
    "principles ARE in the graph** — `77b043f` proposed them read-only (dry-run 175 nodes / 111 "
    "edges / 27 declared nulls, selftest 15 bites, mutants 18/18), his export came back **RP-1"
    "…RP-6 all (a), no notes**, his *\"go\"* inscribed **`s275-D1`…`s275-D6`** at `ffcb029` "
    "(`_rulings.json` 578 → 584, by textual span), and `eb47a58` landed "
    "`knowledge/_ux_principle_nodes.json` at **175 nodes / 111 edges / 15 declared nulls** with "
    "the explorer reading it at **v1.12**. **`s269-D1` step 3 is DONE.** ⚠ **WHAT DID NOT "
    "DISCHARGE: `s273-D2` authoring pass two STILL HAS NOT STARTED** — 49 silent providers, "
    "3–4 lanes a session when the graph work pauses — and `s275-D5`'s authored lane is now "
    "blocked on one thing only, which components go first, carried as item ⑥ of the #276 set. "
    "Correction inscribed at: `77b043f` · `ffcb029` · `eb47a58` · `knowledge/_rulings.json` §§ "
    "`s275-D1`…`s275-D6` · `notes/_lanes/275/DAVE-RULINGS-2026-09-15.md` · "
    "`_DECISION-HISTORY/2026-09-15-275-the-principles-and-the-second-seat.md`."
)
assert aged.count(OLD1) == 1, aged.count(OLD1)
aged = aged.replace(OLD1, NEW1, 1)
EDITS.append(("carry ① — THE 145 PRINCIPLES INTO THE GRAPH",
              "CORRECTED BY ADDITION with its s188-D2 receipt (step 3 DONE: s275-D1..D6, "
              "77b043f + ffcb029 + eb47a58); authoring pass two NOT discharged, the carry "
              "rides on"))

OLD2 = ("⬛ **② THE `$description` ON `knowledge/_rule_nodes.json` STILL SAYS \"PROPOSED … NOT "
        "RATIFIED\", AND THE FILE IS NOW RATIFIED AND LANDED** [1]")
NEW2 = (
    "~~⬛ **② THE `$description` ON `knowledge/_rule_nodes.json` STILL SAYS \"PROPOSED … NOT "
    "RATIFIED\", AND THE FILE IS NOW RATIFIED AND LANDED** [1]~~ ⛔ **STRUCK AT THE #275 WRAP — "
    "THE CLAIM IS DISCHARGED AND THE STRIKE CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` "
    "receipt): `ef1213b` was #275's FIRST commit and it fixed the GENERATOR, not the file** — "
    "`gen_kg_rules.py:land()` now writes the ratifying ruling id into `$description`, the store "
    "was regenerated **byte-identical except that one span**, and the selftest and "
    "`_validate_kg.py` were re-run over it. The landed file now names `s274-D8` where it used to "
    "carry the dry-run's own words. Correction inscribed at: `ef1213b` · "
    "`knowledge/gen_kg_rules.py` · `knowledge/_rule_nodes.json` · "
    "`_DECISION-HISTORY/2026-09-15-275-the-principles-and-the-second-seat.md`.** The struck text "
    "stands verbatim above rather than being deleted, because a silently vanished carry is "
    "indistinguishable from a dropped one."
)
assert aged.count(OLD2) == 1, aged.count(OLD2)
aged = aged.replace(OLD2, NEW2, 1)
EDITS.append(("carry ② — _rule_nodes.json's $description",
              "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (ef1213b, the generator "
              "fixed and the store regenerated byte-identical except that span)"))

assert len(EDITS) == 2

# ---- (c) this session's new items -------------------------------------------------------------
NEWITEMS = open(os.path.join(HERE, "carry276-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #276:** " + NEWITEMS + " · " + aged[len("> **residual → #275:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #276",
    "",
    "*Written straight here at the #275 wrap (✅ **NO DATE SPLIT — the session, its ritual and "
    "all eight of its commits are 2026-09-15**) under `s225-D2` clause (i). Ages +1, wording "
    "unchanged, nothing dropped for being old; ★ **ONE carry CORRECTED and ONE carry STRUCK, "
    "and the difference between them is the point** — item ① of the #275 set (the 145 "
    "principles into the graph, then authoring pass two) is **NOT** discharged, because pass "
    "two has still not started, but its first half went true and it takes a correction BY "
    "ADDITION with its `s188-D2` receipt and rides on; item ② (`_rule_nodes.json`'s "
    "`$description` still reading *\"PROPOSED … NOT RATIFIED\"*) is **DISCHARGED**, because "
    "`ef1213b` fixed the generator and regenerated the store byte-identical except that span. "
    "⛔ **NO OTHER carry was re-worded: lane LCE's three proposals, the 99 two-layer rule edges, "
    "`P-274-1`…`P-274-3`, the `example` key, the four near-dupes, the `input` sub-roles, the 6 "
    "`data-grid` reds, the 108 stale showroom pages, the #243 double-count and every #119 open "
    "were all CARRIED THROUGH #275 UNTOUCHED and age with their wording intact.** ★★★ **Dave "
    "ruled six times at #275 — the store moved 578 → 584 — and the session's shape was one "
    "family admitted to the graph (`s275-D1`…`s275-D6`: 145 `ux:<id>` principles and 30 "
    "`polarity:<id>` nodes, 111 edges, six edge types ratified) and one hazard discovered "
    "(a second live session writing into this one's lane, healed by addition and NOT ruled). "
    "⛔ **The nine new items below are every question this session opened and did not close, "
    "and six of them are his.***",
    "",
]

out = []
for ln in lines:
    if ln.strip() == "## residual → #275":
        out.extend(SECTION)
        out.append("<!-- WRITTEN-FIRST: residual → #276 — the aged tail below the NINE new "
                   "items is the #275 line put through ONE programmatic pass "
                   "(`notes/_lanes/275/W/carry276.py`): %d age brackets bumped (%d of them "
                   "`NEW — 0` → `1`), and EXACTLY TWO surgical edits — ONE "
                   "correction-by-addition and ONE strike, both carrying their receipts, "
                   "asserted as a count of two in the script rather than left implicit. Probe "
                   "count at write time: %d. -->" % (n_new + n_num, n_new, after))
        out.append("")
        out.append(line)
        out.append("")
        out.append("---")
        out.append("")
    out.append(ln)

open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("CARRIES: #275 items %d → #276 items %d (+%d; %d NEW — 0 became countable, %d new items "
      "arrive uncounted)" % (before, after, after - before, n_new, 9))
print("ages bumped: %d numbered + %d NEW — 0 = %d" % (n_num, n_new, n_num + n_new))
for t, w in EDITS:
    print("SURGICAL EDIT: %s — %s" % (t, w))
