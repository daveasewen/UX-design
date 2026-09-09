#!/usr/bin/env python3
"""#264 wrap — build `_CARRIES.md` § `## residual → #265` from § `## residual → #264`.

ONE programmatic pass, the #261/#262/#263 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) TWO surgical edits, each asserted UNIQUE before it is made, by ADDITION with an
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
src = [l for l in lines if l.startswith("> **residual → #264:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the TWO strikes, each asserted UNIQUE -------------------------------------------------
EDITS = [
    # ① the Stat card arrow seat — NOT open; it was ruled at #263 and the carry re-opened it.
    ("⬛ **② THE STAT CARD ARROW SEAT IS STILL UNASKED [2, DAVE'S]**",
     "⬛ **② ~~THE STAT CARD ARROW SEAT IS STILL UNASKED~~ [2, DAVE'S] ⛔ STRUCK AT #264 WITH ITS "
     "`s183-D1`/`s188-D2` RECEIPT: IT WAS NEVER OPEN — IT WAS RULED AT #263 AND THIS CARRY "
     "RE-OPENED A CLOSED ITEM.** Dave, at the #264 opener, put to him as the session's first "
     "question: *\"I thought this was ruled\"*. He is right. **`s263-D1`'s `governs` names "
     "`knowledge/snippets/Stat-card.reference.html`** alongside `Kpi-tile.reference.html`, and the "
     "P-01 recommendation he ACCEPTed says verbatim **\"Stat card moves with it, always.\"** ⇒ the "
     "arrow seat on Stat card is settled by `s263-D1` and **no ruling is owed**. ⚠ **The defect is "
     "recorded because it cost a question at the top of a session:** the #263 wrap read the same "
     "`governs` list, wrote *\"a `governs` list is a scope, not an answer\"*, and carried it anyway; "
     "the #264 opener then repeated it. ★ **A carry that survives a wrap on the strength of the "
     "wrap's own doubt is worth one grep of the ruling it doubts.** Receipts: `knowledge/_rulings.json` "
     "§ `s263-D1` · `_DECISION-HISTORY/2026-09-09-264-glyph-twins-and-derived-actives.md` §1. "
     "The original wording stands verbatim below."),
    # ② the sidebar chart glyph — the claim was FALSE; the defect was pairing, not provenance.
    ("⚠ **⑥ THE SIDEBAR `chart` LINE GLYPH IS HAND-BAKED RATHER THAN THE LIBRARY'S, AND ITS FILLED "
     "TWIN IS NAMED `insight-active` [2, DAVE'S]**",
     "⚠ **⑥ ~~THE SIDEBAR `chart` LINE GLYPH IS HAND-BAKED RATHER THAN THE LIBRARY'S~~, AND ITS "
     "FILLED TWIN IS NAMED `insight-active` [2, DAVE'S] ⛔ STRUCK AT #264 WITH ITS "
     "`s183-D1`/`s188-D2` RECEIPT: THE HAND-BAKED HALF IS FALSE. THE DEFECT WAS PAIRING, NOT "
     "PROVENANCE.** All **twelve** `<symbol>`s in `knowledge/snippets/Sidebar-nav.reference.html` "
     "are **byte-identical to `knowledge/assets/icons/` files by path data** — nothing in the "
     "sidebar is locally drawn. What was wrong was the TWINNING: **Spending** rested on "
     "`data-chart` and went current on `insight-active` (a bulb — a different concept), and "
     "**Transfers** rested on `balance-transfer` (which has **no `-active` twin in the library at "
     "all**) and went current on `transfer-active`, so the shape changed on selection. ⇒ Ruled and "
     "enacted the same evening: **`s264-D1`** (*\"Spending A\"* → `data-chart`/`data-chart-active`) "
     "and **`s264-D2`** (*\"Transfer D\"* → `transfer`/`transfer-active`), commit **`9bfacb9`**, off "
     "`notes/_REVIEW-264-sidebar-glyph.html`. ★ **The half that survives is GENERALISED, not "
     "vanished:** the class is now machine-checked — `knowledge/_validate_icons.py` grew a **TWIN "
     "ARM** (every `.ic-line`/`.ic-fill` pair resolved to library slugs, fill must be the line's "
     "`-active`/`-active-badge`, **MIS-TWINNED is BLOCKING**), bite-test `twin` "
     "(`mut_mistwinned_icon`) registered in `knowledge/_tests/test_gates.py` and driven RED→GREEN, "
     "and it immediately found a **THIRD** case the eye had missed (Tab-bar's Insights row carried "
     "`insight` in BOTH slots) — commit **`3d7def7`**. The original wording stands verbatim below."),
]
for find, repl in EDITS:
    assert aged.count(find) == 1, (aged.count(find), find[:80])
    aged = aged.replace(find, repl, 1)

# ---- (c) this session's new items -------------------------------------------------------------
NEW = open(os.path.join(HERE, "carry265-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #265:** " + NEW + " · " + aged[len("> **residual → #264:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #265",
    "",
    "*Written straight here at the #264 wrap (✅ **NO DATE SPLIT — session, ritual and commit are "
    "all 2026-09-09**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for "
    "being old; **two carries STRUCK, both by ADDITION and each with its `s183-D1`/`s188-D2` "
    "receipt**, the original wording standing verbatim beneath each — one because it was never "
    "open (ruled at `s263-D1`), one because its central claim was FALSE (the sidebar glyphs are "
    "library assets; the defect was the twinning) — and **the half of the second that survives the "
    "strike is generalised into a blocking gate arm rather than vanishing with it**.*",
    "",
    "<!-- WRITTEN-FIRST: residual → #265 — the aged tail below the FOUR new items is the #264 "
    "line put through ONE programmatic pass (`notes/_lanes/264/carry265.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), then 2 surgical edits each asserted UNIQUE before it was "
    "made (the two strikes: the Stat card arrow seat, ruled `s263-D1`; the sidebar `chart` glyph, "
    "false and repaired by `s264-D1`/`s264-D2`). Probe count at write time: %d. "
    "⚠ DECLARED, NOT DISCOVERED: a pairing pass of every #264 carry against this line leaves "
    "THREE unpaired — the two strikes, and the #264 item ① whose INLINE age pointers "
    "(`[1]`→`[2]`, references to items ② and ③ of its own list) were bumped by the same "
    "mechanical pass; that bump keeps the pointer TRUE and is not a re-wording of the carry. -->"
    % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #264")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
