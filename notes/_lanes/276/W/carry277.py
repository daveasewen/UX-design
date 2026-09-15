#!/usr/bin/env python3
"""#276 wrap — build `_CARRIES.md` § `## residual → #277` from § `## residual → #276`.

ONE programmatic pass, the #261…#275 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ FIVE SURGICAL EDITS, every one carrying its `s183-D1`/`s188-D2` receipt, never a reword:
      · #275's ② (two sessions on one repo — one word owed) — CORRECTED BY ADDITION: his word
        CAME (`s276-D6`), and the RULE still did not; the carry rides on as item ② of the new set.
      · #275's ⑥ (`s275-D5`'s lane waits on which components go first) — DISCHARGED by
        `s276-D4` (six named) and `s276-D5` (the three charts next). STRUCK.
      · #275's ⑨ (the push — 29 local, 30 after) — DISCHARGED: he pushed, `2740d3b`…`3b9d89b`.
        STRUCK.
      · #274's ⑤ (`P-274-1`/`P-274-2`/`P-274-3` parked, none ruled) — CORRECTED BY ADDITION:
        `P-274-2` and `P-274-3` are CLOSED by `s276-D1`…`s276-D4`, rows kept; `P-274-1` (edit
        mode) is untouched and rides on.
      · #274's ⑧ (the push — 20 local, 21 after) — DISCHARGED by the same push. STRUCK.
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
src = [l for l in lines if l.startswith("> **residual → #276:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the FIVE surgical edits ---------------------------------------------------------------
EDITS = []

def edit(old, new, title, what):
    global aged
    assert aged.count(old) == 1, (title, aged.count(old))
    aged = aged.replace(old, new, 1)
    EDITS.append((title, what))

edit(
    "⬛ **② TWO SESSIONS ON ONE REPO — ONE WORD IS OWED AND THE HAZARD IS NOT RULED** [1, DAVE'S]",
    "⬛ **② TWO SESSIONS ON ONE REPO — ONE WORD IS OWED AND THE HAZARD IS NOT RULED** [1, DAVE'S] "
    "⛔ **HIS WORD CAME AT #276 AND THE RULE DID NOT, SO THIS CARRY IS CORRECTED BY ADDITION WITH "
    "ITS RECEIPT (`s188-D2`) AND RIDES ON:** he answered *\"1. fix\"* — read back as *make it "
    "impossible* — and then **REFUSED both durable options** when they were read back to him "
    "(*\"this has gone from a patch to a hack, not sure I like this unless its not permanent\"*), so "
    "the **seat lock and the worktree-per-session were BOTH DROPPED**; his *\"go\"* took an "
    "ADVISORY guard with a removal date (`knowledge/_validate_lane_ownership.py`, `s276-D6`, "
    "parked as `P-276-1`). ⚠ **WHAT DID NOT DISCHARGE: `s276-D6` records a GUARD and a NORM (one "
    "seat at a time, by his #57 word) and inscribes NO LAW** — whether two sessions may share one "
    "repo at all is still unanswered, and his own note on the decision stands in the ruling: "
    "*\"Okay but I don't think this is durable, feels like we're patching just to get it done\"*. "
    "The question rides on as item ② of the #277 set. Correction inscribed at: `6beedef` · "
    "`knowledge/_rulings.json` § `s276-D6` · `notes/_lanes/276/DAVE-RULINGS-2026-09-15.md` · "
    "`_DECISION-HISTORY/2026-09-15-276-the-loose-ends-tied-off.md`.",
    "carry ② — TWO SESSIONS ON ONE REPO",
    "CORRECTED BY ADDITION with its s188-D2 receipt (his word came, s276-D6; the RULE did not) — "
    "rides on")

edit(
    "⬛ **⑥ `s275-D5`'s AUTHORED LANE WAITS ON WHICH COMPONENTS GO FIRST** [1, DAVE'S]",
    "~~⬛ **⑥ `s275-D5`'s AUTHORED LANE WAITS ON WHICH COMPONENTS GO FIRST** [1, DAVE'S]~~ "
    "⛔ **STRUCK AT THE #276 WRAP — THE CLAIM IS DISCHARGED AND THE STRIKE CARRIES ITS RECEIPT "
    "(`s183-D1` strike, `s188-D2` receipt): `s276-D4` NAMED them and they landed** — tags · "
    "tags-input · notifications · links · button · icon-button, **six and not the brief's four** "
    "(the chips half of the tags spec covers `tags-input` and the buttons spec names icon-only as "
    "one of its three structural variations; `split-button` is not covered and was not authored), "
    "**81 `edges.obeys` entries, 67 `rule:` + 14 `ux:`, every one with its own `$why`**, and "
    "`s276-D5` names the NEXT three — chart-line, chart-pie, chart-bar — which is where the "
    "question goes on. Correction inscribed at: `577c82d` · `knowledge/_rulings.json` §§ "
    "`s276-D4`/`s276-D5` · `knowledge/components/*.meta.json` · "
    "`notes/_lanes/276/tie-off/LAND-REPORT.md`.** The struck text stands verbatim above rather "
    "than being deleted, because a silently vanished carry is indistinguishable from a dropped one.",
    "carry ⑥ — s275-D5's AUTHORED LANE",
    "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (s276-D4 named six components, "
    "s276-D5 names the next three)")

edit(
    "⬛ **⑨ THE PUSH — TWENTY-NINE LOCAL COMMITS BEFORE THIS WRAP, THIRTY AFTER** [1, DAVE'S]",
    "~~⬛ **⑨ THE PUSH — TWENTY-NINE LOCAL COMMITS BEFORE THIS WRAP, THIRTY AFTER** [1, DAVE'S]~~ "
    "⛔ **STRUCK AT THE #276 WRAP — THE CLAIM IS DISCHARGED AND THE STRIKE CARRIES ITS RECEIPT "
    "(`s183-D1` strike, `s188-D2` receipt): HE PUSHED.** His second word of the day was *\"2. "
    "push\"* and the range `2740d3b`…`3b9d89b` went out, taking every one of those thirty commits "
    "with it; `git log origin/master..HEAD` at this seat reads **five** local afterwards, all of "
    "them #276's own. The push carries on as item ⑨ of the #277 set at its NEW figures. "
    "Correction inscribed at: `git log origin/master..HEAD` · "
    "`notes/_lanes/276/DAVE-RULINGS-2026-09-15.md` · `_HANDOFF-127-the-loose-ends-tied-off.md`.** "
    "The struck text stands verbatim above rather than being deleted.",
    "carry ⑨ — THE PUSH (29/30)",
    "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (his \"2. push\", 2740d3b..3b9d89b)")

edit(
    "⬛ **⑤ `P-274-1`, `P-274-2` AND `P-274-3` ARE PARKED WITH TRIPWIRES AND NOT ONE OF THEM IS "
    "RULED** [2, DAVE'S]",
    "⬛ **⑤ `P-274-1`, `P-274-2` AND `P-274-3` ARE PARKED WITH TRIPWIRES AND NOT ONE OF THEM IS "
    "RULED** [2, DAVE'S] ⛔ **TWO OF THE THREE ARE CLOSED AT THE #276 WRAP AND ONE IS NOT, SO THIS "
    "CARRY IS CORRECTED BY ADDITION WITH ITS RECEIPT (`s188-D2`) AND RIDES ON:** **`P-274-2`** (the "
    "compliance-corpus fix behind the 19 declared `cites` nulls) is **CLOSED by `s276-D1`/`s276-D2`** "
    "— 17 criteria landed, `sc:` **38 → 55**, nulls **19 → 0** — and **`P-274-3`** (rule → component "
    "authored the other way) is **CLOSED by `s276-D3`/`s276-D4`** — `edges.obeys` with `$why` "
    "REQUIRED, 81 entries across six metas. **Both rows were KEPT in `knowledge/_parked.json` with "
    "`status` `parked` → `enacted` and a new `closed_by` string; nothing was deleted.** ⚠ **WHAT DID "
    "NOT DISCHARGE: `P-274-1` — edit mode presenting the alternatives, from his own *\"note that in "
    "edit mode, when we build it, the user can be presented with the alternatives we have "
    "defined.\"* — is UNTOUCHED**, still tripwired on `_compose_slice.py`, and he confirmed the "
    "parking at #276 in his own words: *\"edit mode can wait until we do edit mode, park it has a "
    "tripwire\"*. Correction inscribed at: `577c82d` · `7cc7cd9` · `knowledge/_parked.json` · "
    "`knowledge/_rulings.json` §§ `s276-D1`…`s276-D4` · "
    "`notes/_lanes/276/tie-off/LAND-REPORT.md` § (f).",
    "carry ⑤ — P-274-1/2/3 PARKED",
    "CORRECTED BY ADDITION with its s188-D2 receipt (P-274-2 and P-274-3 CLOSED by s276-D1..D4, "
    "rows kept; P-274-1 untouched and riding on)")

edit(
    "⬛ **⑧ THE PUSH — TWENTY LOCAL COMMITS BEFORE THIS WRAP, TWENTY-ONE AFTER** [2, DAVE'S]",
    "~~⬛ **⑧ THE PUSH — TWENTY LOCAL COMMITS BEFORE THIS WRAP, TWENTY-ONE AFTER** [2, DAVE'S]~~ "
    "⛔ **STRUCK AT THE #276 WRAP — THE CLAIM IS DISCHARGED AND THE STRIKE CARRIES ITS RECEIPT "
    "(`s183-D1` strike, `s188-D2` receipt): the same push that discharged the #275 carry above "
    "carried these too.** *\"2. push\"*, `2740d3b`…`3b9d89b`; `git log origin/master..HEAD` reads "
    "**five** at this seat. ⚠ **Two push carries stood at once because each wrap wrote its own with "
    "that wrap's figures, and BOTH are struck by the one event rather than one being left to age "
    "quietly beside a discharged twin.** Correction inscribed at: `git log origin/master..HEAD` · "
    "`notes/_lanes/276/DAVE-RULINGS-2026-09-15.md`.** The struck text stands verbatim above.",
    "carry ⑧ — THE PUSH (20/21)",
    "STRUCK as DISCHARGED, same receipt as ⑨ — one push discharged both carries")

assert len(EDITS) == 5

# ---- (c) this session's new items -------------------------------------------------------------
NEWITEMS = open(os.path.join(HERE, "carry277-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #277:** " + NEWITEMS + " · " + aged[len("> **residual → #276:** "):]
after = len(cg._carry_items(line))
n_this = 9

SECTION = [
    "## residual → #277",
    "",
    "*Written straight here at the #276 wrap (✅ **NO DATE SPLIT — the session, its ritual and all "
    "five of its commits are 2026-09-15**) under `s225-D2` clause (i). Ages +1, wording unchanged, "
    "nothing dropped for being old; ★ **TWO carries CORRECTED and THREE STRUCK, and the difference "
    "between them is the point** — item ② of the #276 set (two sessions on one repo) is **NOT** "
    "discharged, because his word came and the RULE did not, so it takes a correction BY ADDITION "
    "with its `s188-D2` receipt and rides on; item ⑤ of the #274 set (`P-274-1`/`P-274-2`/"
    "`P-274-3`) is corrected the same way, two of the three CLOSED by `s276-D1`…`s276-D4` and "
    "`P-274-1` untouched; and three are **DISCHARGED** — `s275-D5`'s waiting lane (`s276-D4` named "
    "the six, `s276-D5` names the next three) and **both** standing push carries, because he pushed "
    "(*\"2. push\"*, `2740d3b`…`3b9d89b`). ⛔ **NO OTHER carry was re-worded: lane LCE's three "
    "proposals, the 99 two-layer rule edges, the `example` key, the four near-dupes, the `input` "
    "sub-roles, the 6 `data-grid` reds, the 108 stale showroom pages, `--land --ratified`'s id-only "
    "unlock, `renderPanel()`'s missing `statement`, RP-4's four joins, the #243 double-count and "
    "every #119 open were all CARRIED THROUGH #276 UNTOUCHED and age with their wording intact.** "
    "★★★ **Dave ruled six times at #276 — the store moved 584 → 590 — and the session's shape was "
    "one instruction of his own (*\"maybe we just tie off these loose ends first\"*) turning a "
    "planned icons-and-logos day into the closing of three debts: the 19 WCAG criteria he had not "
    "known were missing, the authored rule→component direction `s274-D12` had refused to draw by "
    "machine, and the two-seat hazard #275 discovered. ⛔ **The nine new items below are every "
    "question this session opened and did not close, and seven of them are his.***",
    "",
]

out = []
for ln in lines:
    if ln.strip() == "## residual → #276":
        out.extend(SECTION)
        out.append("<!-- WRITTEN-FIRST: residual → #277 — the aged tail below the NINE new "
                   "items is the #276 line put through ONE programmatic pass "
                   "(`notes/_lanes/276/W/carry277.py`): %d age brackets bumped (%d of them "
                   "`NEW — 0` → `1`), and EXACTLY FIVE surgical edits — TWO "
                   "corrections-by-addition and THREE strikes, all five carrying their "
                   "receipts, asserted as a count of five in the script rather than left "
                   "implicit. Probe count at write time: %d. -->" % (n_new + n_num, n_new, after))
        out.append("")
        out.append(line)
        out.append("")
        out.append("---")
        out.append("")
    out.append(ln)

open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("CARRIES: #276 items %d → #277 items %d (+%d; %d NEW — 0 became countable, %d new items "
      "arrive uncounted)" % (before, after, after - before, n_new, n_this))
print("ages bumped: %d numbered + %d NEW — 0 = %d" % (n_num, n_new, n_num + n_new))
for t, w in EDITS:
    print("SURGICAL EDIT: %s — %s" % (t, w))
