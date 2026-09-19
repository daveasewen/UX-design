#!/usr/bin/env python3
"""#287 wrap — step 1 + 2d ops for `_LIVE-STATE.md`, built for `_gm_move.py`.

FOUR ops, all-or-nothing through the mover:
  1. `replace`  the `*Last refreshed:` line — the #287 summary goes in front, the WHOLE prior
     line is demoted behind `Previous:` VERBATIM, and #283's `Previous:` chain segment is
     EXCISED from it by a SLICE (located by marker search, never re-typed).
  2. `insert`   that excised slice into `_LIVE-STATE-ARCHIVE.md` under a new § Rolled heading.
  3. `move`     the ⏱ PRIOR DELTA #284 block into the same archive section (2d boundary:
     LATEST + 2 PRIOR).
  4. `replace`  the #286 heading `⏱ LATEST DELTA` → `⏱ PRIOR DELTA`, and
  5. `insert`   the new ⏱ LATEST DELTA #287 block above it.

⚠ EVERY PRE-CONDITION TESTS THE INPUT, NOT THE OUTPUT (#285's guard fired on correct
  behaviour because it tested the projection). The one POST-condition asserts the excised
  slice is ABSENT from the projected replacement — that is a property of the move, not a
  prediction of the result.
"""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")

lines = open(LS, encoding="utf-8").read().split("\n")
old = [l for l in lines if l.startswith("*Last refreshed: 2026-09-18 (Fri from `date` — **#286 wrap**")]
assert len(old) == 1, f"expected exactly one #286 Last-refreshed line, got {len(old)}"
old = old[0]

# ── the #283 `Previous:` chain segment — located by MARKER SEARCH, never by index ────────────
S = " Previous: 2026-09-18 (Fri from `date` — **#283 wrap**"
E = "*Last refreshed (#282, trimmed at the #286 wrap)"
i, j = old.index(S), old.index(E)
assert old.count(S) == 1 and old.count(E) == 1, "the #283 slice markers are not unique"
assert i < j, "the #283 slice markers are out of order"
slice283 = old[i:j]
assert len(slice283) > 5000, f"the #283 slice reads implausibly short ({len(slice283)} B)"
trimmed = old[:i] + " " + old[j:]

HEAD = (
 "*Last refreshed: 2026-09-19 (Sat from `date` — **#287 wrap**. ✅ **NO DATE SPLIT: the session, "
 "its lane commit `75a490cd`, this ritual and its own commit are ALL 2026-09-19** — `date` read "
 "at this seat at the ritual's open. ⛔★★★ **READ `_HANDOFF-138-the-rulings-land-and-the-strand-"
 "map-is-ordered.md` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT**, and it does NOT "
 "replace `_HANDOFF-130`…`-137`, whose open items still stand except the four closed today, each "
 "with a receipt. ★★★ **THE RULINGS STORE MOVED FOR THE FIRST TIME IN SEVEN SESSIONS: 620 → 622**, "
 "verified at THIS seat by `json.load` over the `rulings` list — **`s287-D1`** and **`s287-D2`**, "
 "both present, no duplicate, inscribed through the sanctioned writer with its reconstruction "
 "proof PASSED. **His whole reply at the opener, verbatim: *\"1. inscribe · 2. keep `sizes` and "
 "rebuild. · 3. do it\"*.** ⇒ the eight standing lines are RATIFIED AS WRITTEN and `_standing.md` "
 "is out of DRAFT by HIS word rather than the conductor's reading of it; a per-size master is a "
 "SIZE FIELD on its lockup's existing node and the node count does not move; the key name `sizes` "
 "is now his; and the 58 prose locations calling 256,000 a wall are amended. ★★ **THE EXPLORER "
 "NOW READS THE FIELD** — `notes/_KG-EXPLORER.html` rebuilt at builder `VERSION 1.27`, all 8 "
 "`logo:` nodes carrying `sizes` with 5 keys, 40 entries byte-identical to "
 "`knowledge/_logo_nodes.json`, **parsed out of the built page and compared rather than "
 "eyeballed**. ★★ **THE WALL WORDING IS SWEPT — 58 → 42, and ZERO of the 42 assert that 256,000 "
 "is a wall**; no number moved (`BUDGET_HARD` is still `256_000`), Dave's `says` fields were not "
 "touched, and six ruling records were ANNOTATED by an appended clause rather than re-worded. "
 "★★★ **THE SECOND COLD BOOT LANDED: 74,120 real against #286's 73,832, Δ +288** — two readings "
 "within 300 tokens on a setup whose prior seven-reading spread was 11,526 wide, ⇒ **the −7,031 "
 "connector lever is a MEASURED EFFECT (n=2), no longer a direction**, meeting the acceptance "
 "test #286 wrote for itself. ⛔ **74,120 is the TWELFTH post-diet reading over `BOOT_CEILING_TK` "
 "70,000 — SHRINK-ONLY (`s240-D2`/`s241-D1`), NOT a re-base, and raising the literal is Dave's "
 "word alone**; the figure is stated ONCE, in the `post-mortem #287:` line (`s241-D2`). "
 "⛔★★★ **AND THE AFTERNOON CHANGED WHAT #288 IS FOR.** A GPT-6 handoff from Apollo Spider "
 "v1.0.13 on his work machine was saved into the repo and tested claim by claim (5 of 6 VERIFIED, "
 "1 PARTLY); the conductor framed the result as *\"two ruled spacing sources disagree\"* and "
 "**Dave CORRECTED the framing** — *\"the gutters are also different for the inner and outer "
 "bentos we essentially have a structural bento and embedded bentos or tile groupings\"* ⇒ **two "
 "deliberate quantities, not a contradiction**, and the real defect is that **the `s219-D3` "
 "generation arm was never built**. ⬛ **HIS WRAP CALL ORDERS THREE THINGS AND #288 OPENS ON THE "
 "THIRD: a proper review of Mono's 0 with the `s219-D3` arm BUILT (*\"I just need the one-shot "
 "design to not disappoint\"*), a review of the bento template's QUALITY, and A STRAND MAP OF "
 "APOLLO WITH A CLEAR PATH TO A COHESIVE PRESENTATION ON FRIDAY 2026-09-25.** ⛔ **Two decisions "
 "were put and NOT answered and they carry: an inline-style rule (88 raw values, zero rulings on "
 "inline styles across all 622) and the template's status (meta `PROPOSED` versus showroom "
 "`beta`).** ⛔ **SIX BLOCKING GATE FAILS STOOD AT THE OPEN, ALL INHERITED, CARRIED IN THE `#243` "
 "DECLARED NOT-A-WRAP FORM — the THIRTEENTH consecutive wrap, and a wrap may not repair them.** "
 "**Detail — the gauge, the subs definitional split, the three declared lane judgments, every "
 "declared skip and the 5b addendum — is in the ⏱ LATEST DELTA below, its sole home under "
 "`s241-D2`.** **WHY/HOW: `_DECISION-HISTORY/2026-09-19-287-the-rulings-land-and-the-strand-map-"
 "is-ordered.md`.** **His words verbatim: `notes/_lanes/287/DAVE-RULINGS-2026-09-19.md`.**)* "
 "Previous: "
)
new = HEAD + trimmed
assert slice283 not in new, "POST-CONDITION FAILED: the #283 slice survived into the replacement"
assert trimmed in new and old != new

ROLLHEAD = [
 "## Rolled 2026-09-19 #287 (2d, at the #287 wrap) — via the mover",
 "",
 "### #283's `Previous:` chain segment — moved VERBATIM at the #287 wrap (`Last refreshed` trim)",
 "",
 slice283.strip(),
 "",
]

delta = open(os.path.join(HERE, "delta287.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert delta[0].startswith("## ⏱ LATEST DELTA — 2026-09-19"), delta[0][:80]

gm_old_latest = [l for l in lines if l.startswith("## ⏱ LATEST DELTA — 2026-09-18 (Fri from `date`) (**#286**")]
assert len(gm_old_latest) == 1
old_latest = gm_old_latest[0]
demoted = old_latest.replace("## ⏱ LATEST DELTA —", "## ⏱ PRIOR DELTA —", 1)

p284 = [l for l in lines if l.startswith("## ⏱ PRIOR DELTA — 2026-09-18 (Fri from `date`) (**#284**")]
assert len(p284) == 1
assert sum(1 for l in lines if l.startswith("## 🕓 OPEN — Latin Univers")) == 1

ops = [
 {"op": "replace", "file": "_LIVE-STATE.md", "find": [old], "replace": [new]},
 {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
  "at": "# _LIVE-STATE archive — rolled PRIOR DELTAs", "where": "after",
  "lines": [""] + ROLLHEAD},
 {"op": "move", "src": "_LIVE-STATE.md", "start": p284[0][:80],
  "end": "## 🕓 OPEN — Latin Univers",
  "dst": "_LIVE-STATE-ARCHIVE.md",
  "at": "### #283's `Previous:` chain segment — moved VERBATIM at the #287 wrap",
  "where": "after"},
 {"op": "replace", "file": "_LIVE-STATE.md", "find": [old_latest], "replace": [demoted]},
 {"op": "insert", "file": "_LIVE-STATE.md", "at": demoted[:80], "where": "before",
  "lines": delta + [""]},
]

OPSF = os.path.join(HERE, f"ops-287-ls-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 5000
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
print(f"  #283 slice excised: {len(slice283):,} B  ·  Last-refreshed line {len(old):,} → {len(new):,} B")
print(f"  ⏱ delta #287: {len(delta)} lines")
