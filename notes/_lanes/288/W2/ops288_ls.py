#!/usr/bin/env python3
"""#288 wrap — step 1 + 2d ops for `_LIVE-STATE.md`, built for `_gm_move.py`.

SIX ops, all-or-nothing through the mover:
  1. `replace`  the `*Last refreshed:` line — the #288 summary goes in front, the WHOLE prior
     line is demoted behind `Previous:` VERBATIM, and #284's `Previous:` chain segment is
     EXCISED from it by a SLICE (located by marker search, never re-typed) with a trim note
     left in its place so the move is visible rather than silent.
  2. `insert`   that excised slice into `_LIVE-STATE-ARCHIVE.md` under a new § Rolled heading.
  3. `move`     the ⏱ PRIOR DELTA #285 block into the same archive section (2d boundary:
     LATEST + 2 PRIOR).
  4. `replace`  the #287 heading `⏱ LATEST DELTA` → `⏱ PRIOR DELTA`.
  5. `insert`   the new ⏱ LATEST DELTA #288 block above it.

⚠ EVERY PRE-CONDITION TESTS THE INPUT, NOT THE OUTPUT (#285's guard fired on correct
  behaviour because it tested the projection). The one POST-condition asserts the excised
  slice is ABSENT from the projected replacement — that is a property of the move, not a
  prediction of the result.

2d EXIT CHECK, run before the move: the #285 ⏱ delta's ⚠/⬛/AWAITING items must already live
in a standing section. Asserted below by grep against `_CARRIES.md` rather than by memory —
every one of #285's open items is in the carry set, which is the standing home `s225-D2` gives
them.
"""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")

lines = open(LS, encoding="utf-8").read().split("\n")
old = [l for l in lines if l.startswith("*Last refreshed: 2026-09-19 (Sat from `date` — **#287 wrap**")]
assert len(old) == 1, f"expected exactly one #287 Last-refreshed line, got {len(old)}"
old = old[0]

# ── the #284 `Previous:` chain segment — located by MARKER SEARCH, never by index ────────────
S = " Previous: 2026-09-18 (Fri from `date` — **#284 wrap**"
E = "*Last refreshed (#282, trimmed at the #286 wrap)"
assert old.count(S) == 1 and old.count(E) == 1, "the #284 slice markers are not unique"
i, j = old.index(S), old.index(E)
assert i < j, "the #284 slice markers are out of order"
slice284 = old[i:j]
assert len(slice284) > 5000, f"the #284 slice reads implausibly short ({len(slice284)} B)"

TRIMNOTE = (
 " *Last refreshed (#284, trimmed at the #288 wrap): #284's `Previous:` chain segment was moved "
 "VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-19 #288, in the same section as the #285 "
 "⏱ delta block this wrap rolled. Nothing was deleted — moved.* ")
trimmed = old[:i] + TRIMNOTE + old[j:]

HEAD = (
 "*Last refreshed: 2026-09-19 (Sat from `date` — **#288 wrap**. ✅ **NO DATE SPLIT: the session, "
 "its five lanes, this ritual and its own commit are ALL 2026-09-19** — `date` read at this seat "
 "at the ritual's open. ⛔★★★ **READ `_HANDOFF-139-apollo-composes-and-the-sloppiness-class-is-"
 "named.md` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT**, and it does NOT replace "
 "`_HANDOFF-130`…`-138`, whose open items ALL still stand — ⛔ **NOTHING WAS STRUCK TODAY, and "
 "the zero is a judgment with a reason rather than an oversight** (the one receiptable closure, "
 "the `s219-D3` arm being BUILT, is HALF of a carry headline whose other half — *Mono's 0 is "
 "doubted* — stays true, so it is said in a NEW carry item instead: `s271-D4`, *\"a strike that "
 "is wrong is worse than an item that is merely stale\"*). ⛔★★★ **NO RULING WAS INSCRIBED AND "
 "`knowledge/_rulings.json` STAYS AT 622**, verified at THIS seat by `json.load` over the "
 "`rulings` list with no `s288-` id present — **he did not say *\"inscribe\"* today**, so all TEN "
 "ruling-shaped things are carried as QUESTIONS PUT (`s271-D4`) and never as states of the world. "
 "★★★ **THE SESSION CHANGED SHAPE IN ONE MESSAGE AND THEN CHANGED BACK.** Wave 1 landed four Opus "
 "lanes — the strand map, the four-theme gutter sheet, the `s219-D3` generation arm and the "
 "template quality review — and then **Dave challenged the premise of the whole one-shot path on "
 "seeing the template**: *\"the template is a bit wonky and it's basically copied by the AI, what "
 "is the point of building the KG if the agent just traces an existing file\"* and *\"this isn't "
 "Apollo its a dot-to-dot book\"*. A fifth lane ran a **composition probe with the template "
 "FENCED OFF**, and ★★ **he ruled by eye that it composes**: *\"at least it's diverged from the "
 "tamplete\"* and *\"this looks like its working the way I'd have expected\"* — ⛔ **the METHOD is "
 "endorsed and the EXECUTION is not, and HE names the defect class: *\"its all about alignment "
 "spacing and dimensions\"*.** ⬛ **He writes the test brief for these probes HIMSELF — *\"I'll "
 "create a test brief for these tests\"* — owed by Dave, not by a lane.** ★★ **THE `s219-D3` "
 "GENERATION ARM IS BUILT, sixty-nine sessions after it was ruled**: lane A's new "
 "`knowledge/canon/gen_bento_role_vars.py` is the FIRST consumer of "
 "`knowledge/_render/_bento_edit_rails.json`, which had declared itself `$groundwork_only` and sat "
 "un-consumed since #219; per-theme `--bento-dashboard-main` and `--bento-dashboard-sub` are "
 "minted before `AUTO-THEMES START`, the snippet's two pinned literals become `var()` references, "
 "and every in-scope gate reads green with a four-theme rendered proof. ⛔ **AND IT DOES NOT "
 "SETTLE MONO'S 0** — the OUTER gutter has two readings (token 0/24/24/0 versus role default "
 "40/24/40/24) and the INNER gutter three (canon's literal 1px, `subSpacing` 4/4/4/2, the "
 "template's 4), **all published, no winner picked, and supercharge's 0 inherited and never "
 "decided**. ★★ **THREE DELIVERABLES ARE FILED FOR HIS EYE**: the strand map "
 "`notes/_STRAND-MAP-2026-09-19.html` (13 sections, 41 cited paths all existing, and **which "
 "event Friday 2026-09-25 is declared NOT ESTABLISHED on a band of its own**), the four-theme "
 "gutter sheet `notes/_lanes/288/B/four-themes.html` read at HEAD through `git show`, and the "
 "template quality review whose headline is that **the drawn page is sound and the paperwork is "
 "not** — four of the five claims in the meta's own `$status` block measured FALSE, with a "
 "six-question decision pack attached and unanswered. ⚠★★ **THE PROBE MEASURED THINGS NO GATE IN "
 "THE TREE CAN SEE**: canon's own instance-dial recipe **loses silently** on specificity "
 "((0,2,0) against the `:has()` rule's (0,4,0), measured at 0px instead of 40), canon **clips "
 "with `pageErrors: []`**, and **no gate reads the composition of a page that LINKS `canon.css`** "
 "— ten gaps named, none fixed, none ruled. ⛔ **The frozen demo prompt is NOT recoverable from "
 "the record and the two probe pages therefore answer DIFFERENT briefs**, printed on the sheet "
 "rather than buried. ⛔ **SIX BLOCKING GATE FAILS STOOD AT THE OPEN, ALL INHERITED, CARRIED IN "
 "THE `#243` DECLARED NOT-A-WRAP FORM — the FOURTEENTH consecutive wrap, and a wrap may not "
 "repair them.** ⚠ **#288 HAS NO LANE COMMIT — this wrap is the session's ONLY commit** and "
 "stages all five lanes plus three paths inherited dirty from #287, one of them "
 "`notes/_lanes/287/DAVE-RULINGS-2026-09-19.md` with six lines appended AFTER #287's commit, the "
 "wrong-order class for a THIRD consecutive session. **Detail — the gauge, the subs definitional "
 "split, the four declared lane judgments, every declared skip and the 5b addendum — is in the "
 "⏱ LATEST DELTA below, its sole home under `s241-D2`.** **WHY/HOW: "
 "`_DECISION-HISTORY/2026-09-19-288-apollo-composes-and-the-sloppiness-class-is-named.md`.** "
 "**His words verbatim: `notes/_lanes/288/DAVE-RULINGS-2026-09-19.md`.**)* "
 "Previous: "
)
new = HEAD + trimmed
assert slice284 not in new, "POST-CONDITION FAILED: the #284 slice survived into the replacement"
assert trimmed in new and old != new

ROLLHEAD = [
 "## Rolled 2026-09-19 #288 (2d, at the #288 wrap) — via the mover",
 "",
 "### #284's `Previous:` chain segment — moved VERBATIM at the #288 wrap (`Last refreshed` trim)",
 "",
 slice284.strip(),
 "",
]

delta = open(os.path.join(HERE, "delta288.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert delta[0].startswith("## ⏱ LATEST DELTA — 2026-09-19"), delta[0][:80]
assert delta[0].count("**#288**") == 1

gm_old_latest = [l for l in lines if l.startswith("## ⏱ LATEST DELTA — 2026-09-19 (Sat from `date`) (**#287**")]
assert len(gm_old_latest) == 1
old_latest = gm_old_latest[0]
demoted = old_latest.replace("## ⏱ LATEST DELTA —", "## ⏱ PRIOR DELTA —", 1)

p285 = [l for l in lines if l.startswith("## ⏱ PRIOR DELTA — 2026-09-18 (Fri from `date`) (**#285**")]
assert len(p285) == 1
assert sum(1 for l in lines if l.startswith("## 🕓 OPEN — Latin Univers")) == 1

# ── 2d EXIT CHECK — the rolling delta's Dave-owed items must already stand in a standing home ──
carries = open(os.path.join(ROOT, "_CARRIES.md"), encoding="utf-8").read()
for token in ("`INSEAT_WARN_TK`", "RESUME contract", "SCRATCH ARM"):
    assert token in carries, f"2d EXIT CHECK FAILED — #285's open item not in a standing home: {token!r}"
print("2d EXIT CHECK: #285's Dave-owed items stand in `_CARRIES.md` — safe to roll.")

ops = [
 {"op": "replace", "file": "_LIVE-STATE.md", "find": [old], "replace": [new]},
 {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
  "at": "# _LIVE-STATE archive — rolled PRIOR DELTAs", "where": "after",
  "lines": [""] + ROLLHEAD},
 {"op": "move", "src": "_LIVE-STATE.md", "start": p285[0][:80],
  "end": "## 🕓 OPEN — Latin Univers",
  "dst": "_LIVE-STATE-ARCHIVE.md",
  "at": "### #284's `Previous:` chain segment — moved VERBATIM at the #288 wrap",
  "where": "after"},
 {"op": "replace", "file": "_LIVE-STATE.md", "find": [old_latest], "replace": [demoted]},
 {"op": "insert", "file": "_LIVE-STATE.md", "at": demoted[:80], "where": "before",
  "lines": delta + [""]},
]

OPSF = os.path.join(HERE, f"ops-288-ls-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 5000
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
print(f"  #284 slice excised: {len(slice284):,} B  ·  Last-refreshed line {len(old):,} → {len(new):,} B")
print(f"  ⏱ delta #288: {len(delta)} lines")
