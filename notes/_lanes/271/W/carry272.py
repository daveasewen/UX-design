#!/usr/bin/env python3
"""#271 wrap — build `_CARRIES.md` § `## residual → #272` from § `## residual → #271`.

ONE programmatic pass, the #261…#270 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ ONE SURGICAL EDIT, and it is a STRIKE with its `s188-D2` receipt, not a reword: carried
      item ① of the #271 set claimed "the four edge types are at the door of the closed
      vocabulary and ONE WORD lands them". That claim is FALSE as of #271: Dave gave the word
      ("ratify"), `s270-D2` was inscribed, and `gen_kg_roles_desk.py --land --ratified` put 115
      edges / 45 nodes across 26 metas into the graph at `23f7d16`. A discharged carry is STRUCK
      with its discharge named, never re-typed (`s183-D1`, receipt requirement `s188-D2`).
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
src = [l for l in lines if l.startswith("> **residual → #271:**")]
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
OLD = "⬛ **① RATIFY THE ATOMS, WIDEN THE NET** [1, DAVE'S]"
NEW = ("~~⬛ **① RATIFY THE ATOMS, WIDEN THE NET** [1, DAVE'S]~~ ⛔ **STRUCK AT THE #271 WRAP — "
       "THE CLAIM IS DISCHARGED AND THE STRIKE CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` "
       "receipt): Dave gave the one word at #271's opener (*\"1. ratify\"*), `s270-D2` is "
       "inscribed in `knowledge/_rulings.json`, and `gen_kg_roles_desk.py --land --ratified` "
       "put **115 edges / 45 nodes across 26 metas** into the graph at `23f7d16` — the four "
       "edge types `providesRole` / `answersIntent` / `hasDataShape` / `yieldsTo` and the node "
       "kinds `role:` / `intent:` / `shape:` ARE in the closed vocabulary now, `meta.schema.json` "
       "carries the enum, `_validate_kg.py` is OK and the explorer regenerated at 935 nodes / "
       "1,292 relations. Correction inscribed at: `notes/_subreports/2026-09-14-271-W-wrap.md` "
       "§ What was done, and the ⏱ LATEST DELTA for #271 in `_LIVE-STATE.md`.** The struck text "
       "stands verbatim above rather than being deleted, because a silently vanished carry is "
       "indistinguishable from a dropped one. ⚠ **WHAT DID NOT DISCHARGE WITH IT: the roles.json "
       "membership drift (108 vs 24) was RE-REPORTED by the landing and is carried on as a new "
       "item, and the WIDEN-THE-NET half (handoff-121 § C, door v2) was never a ruling and is "
       "untouched.**")
assert aged.count(OLD) == 1, aged.count(OLD)
aged = aged.replace(OLD, NEW, 1)
EDITS = [("carry ① — RATIFY THE ATOMS, WIDEN THE NET",
          "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (s270-D2 / 23f7d16)")]
assert len(EDITS) == 1

# ---- (c) this session's new items -------------------------------------------------------------
NEWITEMS = open(os.path.join(HERE, "carry272-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #272:** " + NEWITEMS + " · " + aged[len("> **residual → #271:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #272",
    "",
    "*Written straight here at the #271 wrap (✅ **NO DATE SPLIT — the session, its ritual and "
    "its commits are all 2026-09-14**) under `s225-D2` clause (i). Ages +1, wording unchanged, "
    "nothing dropped for being old; ★ **ONE carry STRUCK, and it is a DISCHARGE rather than a "
    "retraction** — carried item ① of the #271 set (the four edge types waiting at the door of "
    "the closed vocabulary) was closed by Dave's one word at this session's opener and by the "
    "landing at `23f7d16`, and it is struck with its `s183-D1`/`s188-D2` receipt rather than "
    "re-typed or deleted. ⛔ **NO OTHER carry was re-worded: the compose-time door, door v2, the "
    "`when` predicates, the three selection-control boundaries and the HSBC ingestion gap were "
    "all CARRIED THROUGH #271 UNTOUCHED — #271 spent itself on the harvest and on enacting dream "
    "pass 12, and every one of those items ages with its wording intact.** ★★★ **Dave ruled FIVE "
    "times at #271 in the `_rulings.json` sense: the store moved 464 → 469 (`s270-D2` landing the "
    "edge types, `s271-D1` the single stop line, `s271-D2` the FILL warn arm, `s271-D3` the demo "
    "dates NONE DECIDED, `s271-D4` the re-checked open list), and the 69 harvest decisions, the "
    "15 unanimous and the \"256\" clause were all deliberately left unruled.***",
    "",
]

out = []
for ln in lines:
    if ln.strip() == "## residual → #271":
        out.extend(SECTION)
        out.append("<!-- WRITTEN-FIRST: residual → #272 — the aged tail below the EIGHT new "
                   "items is the #271 line put through ONE programmatic pass "
                   "(`notes/_lanes/271/W/carry272.py`): %d age brackets bumped (%d of them "
                   "`NEW — 0` → `1`), and EXACTLY ONE surgical edit, a strike carrying its "
                   "receipt, asserted as a count of one in the script rather than left implicit. "
                   "Probe count at write time: %d. -->" % (n_new + n_num, n_new, after))
        out.append("")
        out.append(line)
        out.append("")
        out.append("---")
        out.append("")
    out.append(ln)

open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("CARRIES: #271 items %d → #272 items %d (+%d; %d NEW — 0 became countable, %d new items "
      "arrive uncounted)" % (before, after, after - before, n_new, 8))
print("ages bumped: %d numbered + %d NEW — 0 = %d" % (n_num, n_new, n_num + n_new))
for t, w in EDITS:
    print("SURGICAL EDIT (1): %s — %s" % (t, w))
