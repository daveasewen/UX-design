#!/usr/bin/env python3
"""#277 wrap — build `_CARRIES.md` § `## residual → #278` from § `## residual → #277`.

ONE programmatic pass, the #261…#276 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ THREE SURGICAL EDITS, every one carrying its `s183-D1`/`s188-D2` receipt:
      · #277's ① (the three charts, then the icons) — CORRECTED BY ADDITION: the CHARTS half
        is discharged (`s277-D1..D3` ruled AND enacted at `bedf383`); the ICONS half is RULED
        and NOT ENACTED, so the carry rides on as item ① of the #278 set.
      · #277's ⑥ (chart-donut + the 19 family rules, one word each) — DISCHARGED by
        `s277-D2` and `s277-D3`. STRUCK.
      · #277's ⑨ (the push — five local, six after) — NOT discharged; he did not push, and the
        figure moved. CORRECTED BY ADDITION with its receipt; rides on as item ⑪.
  (c) the session's THIRTEEN NEW items written in front.

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
src = [l for l in lines if l.startswith("> **residual → #277:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the THREE surgical edits ---------------------------------------------------------------
EDITS = []

def edit(old, new, title, what):
    global aged
    assert aged.count(old) == 1, (title, aged.count(old))
    aged = aged.replace(old, new, 1)
    EDITS.append((title, what))

edit(
    "⬛ **① THE THREE CHARTS, THEN THE ICONS — `s276-D5` FIRST, THEN `s269-D1` STEP 4** [1, DAVE'S]",
    "⬛ **① THE THREE CHARTS, THEN THE ICONS — `s276-D5` FIRST, THEN `s269-D1` STEP 4** [1, DAVE'S] "
    "⛔ **HALF OF THIS CARRY IS DISCHARGED AND HALF IS NOT, SO IT IS CORRECTED BY ADDITION WITH ITS "
    "RECEIPT (`s188-D2`) AND RIDES ON:** the CHARTS half is **CLOSED** — his export (a / a / b, "
    "2026-09-16T07:20:00.078Z, no notes) and his *\"go\"* inscribed **`s277-D1`…`s277-D3`** at "
    "`407f20b`, and `bedf383` **ENACTED** them: 87 `obeys` spliced insert-only across the four "
    "chart metas, the corpus **81 → 168** over 10 metas, explorer **v1.14**, all measured at the "
    "#277 wrap seat. ⚠ **WHAT DID NOT DISCHARGE: the ICONS half.** `s269-D1` STEP 4 was RULED at "
    "#277 — `s277-D4`…`s277-D7` at `08ef58d`, 688 asset nodes, `usesIcon` 371 from the byte-match, "
    "NO default for the 15 multi-active bases, 12 logos in — and **NOT ONE NODE OF IT IS IN THE "
    "TREE**; the land is #278's first lane and stands as item ① of the #278 set. Correction "
    "inscribed at: `407f20b` · `bedf383` · `08ef58d` · `knowledge/_rulings.json` §§ "
    "`s277-D1`…`s277-D7` · `_HANDOFF-128-the-constitution-and-the-thin-slice.md`.",
    "carry ① — THE THREE CHARTS, THEN THE ICONS",
    "CORRECTED BY ADDITION with its s188-D2 receipt (charts RULED + ENACTED bedf383; icons RULED "
    "s277-D4..D7 and NOT enacted) — rides on")

edit(
    "⬛ **⑥ `chart-donut` AND THE 19 FAMILY-LEVEL RULES IN `data-visualisation.md` ARE ONE WORD "
    "EACH, OWED TO THE NEXT LANE** [1, DAVE'S]",
    "~~⬛ **⑥ `chart-donut` AND THE 19 FAMILY-LEVEL RULES IN `data-visualisation.md` ARE ONE WORD "
    "EACH, OWED TO THE NEXT LANE** [1, DAVE'S]~~ ⛔ **STRUCK AT THE #277 WRAP — BOTH WORDS CAME "
    "AND THE STRIKE CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt).** His export on "
    "`REVIEW-charts-2026-09-15-v2.html` answered **D-2 (a)** ⇒ **`s277-D2`: `chart-donut` SHARES "
    "THE PIE FILE**, 11 rules on the donut, `dv-pie-003` donut-only; and **D-3 (b)** ⇒ "
    "**`s277-D3`: the 19 family-level rules land as a PER-COMPONENT AUTHORED SUBSET of 47 family "
    "edges, with `dv-013` off `chart-bar`.** Both were enacted at `bedf383` in the same splice. "
    "⚠ **`dv-013`'s exclusion rests on his SILENCE — the export carried no note on it — and that "
    "residue rides on as item ⑦ of the #278 set rather than being counted as closed here.** "
    "Correction inscribed at: `407f20b` · `bedf383` · `knowledge/_rulings.json` §§ "
    "`s277-D2`/`s277-D3` · `notes/_lanes/277/land/LAND-REPORT.md`.** The struck text stands "
    "verbatim above rather than being deleted, because a silently vanished carry is "
    "indistinguishable from a dropped one.",
    "carry ⑥ — chart-donut + THE 19 FAMILY RULES",
    "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (s277-D2 and s277-D3, enacted bedf383)")

edit(
    "⬛ **⑨ THE PUSH — FIVE LOCAL COMMITS BEFORE THIS WRAP, SIX AFTER** [1, DAVE'S]",
    "⬛ **⑨ THE PUSH — FIVE LOCAL COMMITS BEFORE THIS WRAP, SIX AFTER** [1, DAVE'S] ⛔ **NOT "
    "DISCHARGED — HE DID NOT PUSH, AND THE FIGURE THIS CARRY STATES IS NO LONGER TRUE, SO IT IS "
    "CORRECTED BY ADDITION WITH ITS RECEIPT (`s188-D2`) RATHER THAN STRUCK OR LEFT TO AGE AT A "
    "STALE NUMBER:** `git log origin/master..HEAD` at the #277 wrap seat reads **23**, every one "
    "of them #277's own — the six of 2026-09-15 (`f84eb78` · `8c80aa2` · `d84eb72` · `66fdc49` · "
    "`81e845a` · `ca294b4`) and the seventeen of 2026-09-16 — and **24 stand after this wrap**. "
    "The push carries on as item ⑪ of the #278 set at its new figures. Correction inscribed at: "
    "`git log origin/master..HEAD` · `_HANDOFF-128-the-constitution-and-the-thin-slice.md`.",
    "carry ⑨ — THE PUSH (5/6)",
    "CORRECTED BY ADDITION with its s188-D2 receipt (he did NOT push; 5/6 is now 23/24) — rides on")

assert len(EDITS) == 3

# ---- (c) this session's new items -------------------------------------------------------------
raw = open(os.path.join(HERE, "carry278-new.txt"), encoding="utf-8").read().strip()
NEWITEMS = " ".join(l.strip() for l in raw.split("\n") if l.strip())
assert "\n" not in NEWITEMS
line = "> **residual → #278:** " + NEWITEMS + " · " + aged[len("> **residual → #277:** "):]
after = len(cg._carry_items(line))
n_this = 13

SECTION = [
    "## residual → #278",
    "",
    "*Written straight here at the #277 wrap (⚠ **DATE SPLIT — the session opened 2026-09-15 in "
    "the evening and six of its commits carry that date; the work, the rulings and this ritual are "
    "2026-09-16 and seventeen commits carry THAT one. Nothing was re-dated: the split is recorded "
    "BY ADDITION in the GOOD-MORNING idiom and every key, filename and stamp keeps the date it was "
    "born with**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for being "
    "old; ★ **TWO carries CORRECTED BY ADDITION and ONE STRUCK.** Item ① of the #277 set is HALF "
    "discharged — the three charts were ruled (`s277-D1`…`s277-D3`, `407f20b`) AND enacted "
    "(`bedf383`, 87 `obeys`, corpus 81 → 168), while the icons half was RULED (`s277-D4`…`s277-D7`, "
    "`08ef58d`) and **not one node of it is in the tree** — so it takes a correction and rides on. "
    "Item ⑨ (the push) is corrected the same way and for the opposite reason: **he did not push**, "
    "so the carry is not discharged, but its figure moved from five-and-six to **twenty-three and "
    "twenty-four** and a carry may not age at a number the repo disproves. The ONE strike is item "
    "⑥ — `chart-donut` and the 19 family-level rules, both of which got their word (`s277-D2` / "
    "`s277-D3`) and both of which landed. ⛔ **NO OTHER carry was re-worded:** one-seat-as-law, "
    "RP-4's four joins, lane LCE's three proposals, the `example` key, the four near-dupes, the six "
    "`data-grid` reds, the 108 stale showroom pages, `--land --ratified`'s id-only unlock, "
    "`renderPanel()`'s missing `statement`, the #243 double-count and every #119 open were all "
    "CARRIED THROUGH #277 UNTOUCHED and age with their wording intact. ★★★ **Dave ruled thirteen "
    "times at #277 — the store moved 590 → 603 in three commits with `205  0` on `_rulings.json` — "
    "and only three of the thirteen are enacted.** The session's shape was his own instruction to "
    "*\"rip through this work\"* and his switch to Fable; what it produced was a KG audit that "
    "measured what he had felt, a ruling record he named THE CONSTITUTION, and a thin slice ruled "
    "into step 1 and not yet wired. ⛔ **The thirteen new items below are every question this "
    "session opened and did not close, and nine of them are his.***",
    "",
]

out = []
for ln in lines:
    if ln.strip() == "## residual → #277":
        out.extend(SECTION)
        out.append("<!-- WRITTEN-FIRST: residual → #278 — the aged tail below the THIRTEEN new "
                   "items is the #277 line put through ONE programmatic pass "
                   "(`notes/_lanes/277/W/carry278.py`): %d age brackets bumped (%d of them "
                   "`NEW — 0` → `1`), and EXACTLY THREE surgical edits — TWO "
                   "corrections-by-addition and ONE strike, all three carrying their "
                   "receipts, asserted as a count of three in the script rather than left "
                   "implicit. Probe count at write time: %d. -->" % (n_new + n_num, n_new, after))
        out.append("")
        out.append(line)
        out.append("")
        out.append("---")
        out.append("")
    out.append(ln)

open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("CARRIES: #277 items %d → #278 items %d (+%d; %d NEW — 0 became countable, %d new items "
      "arrive uncounted)" % (before, after, after - before, n_new, n_this))
print("ages bumped: %d numbered + %d NEW — 0 = %d" % (n_num, n_new, n_num + n_new))
for t, w in EDITS:
    print("SURGICAL EDIT: %s — %s" % (t, w))
