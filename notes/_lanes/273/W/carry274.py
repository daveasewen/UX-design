#!/usr/bin/env python3
"""#273 wrap — build `_CARRIES.md` § `## residual → #274` from § `## residual → #273`.

ONE programmatic pass, the #261…#272 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ TWO SURGICAL EDITS, both STRIKES with their `s188-D2` receipts, never rewords:
      · #273's item ① (enact the ~220 tolerance, or leave `s272-D93` a ruling only) is
        DISCHARGED — Dave answered in two words and `4294b60` wired the advisory arm.
      · #272's item ⑤ (`roles.json` membership drift, re-reported and still not fixed) is
        DISCHARGED — `s273-D1` at `0d98a34` addressed 84 silent metas and the drift reads
        108/108 agree, 0 silent, 0 roles at zero.
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
src = [l for l in lines if l.startswith("> **residual → #273:**")]
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

OLD1 = "⬛ **① ENACT THE ~220 TOLERANCE, OR LEAVE `s272-D93` A RULING ONLY** [1, DAVE'S]"
NEW1 = (
    "~~⬛ **① ENACT THE ~220 TOLERANCE, OR LEAVE `s272-D93` A RULING ONLY** [1, DAVE'S]~~ ⛔ "
    "**STRUCK AT THE #273 WRAP — THE CLAIM IS DISCHARGED AND THE STRIKE CARRIES ITS RECEIPT "
    "(`s183-D1` strike, `s188-D2` receipt): the question was put in one word at #273's opener "
    "and he answered it in two — *\"1. advisory arm\"* — and `4294b60` wired exactly that: "
    "`gauge.TOLERATED_TK = 220_000`, `STOP_LINE_TK` UNCHANGED at `180_000`, no wall touched, "
    "`_checkin.py`'s budget line saying TOLERATED between the two figures and PAST TOLERANCE "
    "above, driven at 170K / 195K / 220K / 230K with an 8/8 selftest block. Correction "
    "inscribed at: `4294b60` · `notes/_lanes/273/DAVE-RULINGS-2026-09-15.md` § Opener · the "
    "⏱ LATEST DELTA for #273 in `_LIVE-STATE.md`.** The struck text stands verbatim above "
    "rather than being deleted, because a silently vanished carry is indistinguishable from a "
    "dropped one. ⚠ **WHAT DID NOT DISCHARGE WITH IT: the arm is ADVISORY BY HIS WORD and "
    "nothing here rules whether it may ever BLOCK** — that tier question is carried on "
    "unchanged as item ⑦ of the #273 set below, alongside `s271-D2` and `s271-D4`."
)
assert aged.count(OLD1) == 1, aged.count(OLD1)
aged = aged.replace(OLD1, NEW1, 1)
EDITS.append(("carry ① — ENACT THE ~220 TOLERANCE",
              "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (4294b60, advisory arm); "
              "the BLOCKING-TIER half explicitly NOT discharged"))

OLD2 = ("⚠ **⑤ `roles.json` MEMBERSHIP DRIFT WAS RE-REPORTED BY THE LANDING ITSELF AND STILL "
        "NOT FIXED** [2]")
NEW2 = (
    "~~⚠ **⑤ `roles.json` MEMBERSHIP DRIFT WAS RE-REPORTED BY THE LANDING ITSELF AND STILL "
    "NOT FIXED** [2]~~ ⛔ **STRUCK AT THE #273 WRAP — THE CLAIM IS DISCHARGED AND THE STRIKE "
    "CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt): `s273-D1` ruled that the "
    "address is written, and `0d98a34` wrote `provides: <role>` onto **84 silent metas BY "
    "TEXTUAL SPAN, reconstruction-proven per file** (`knowledge/_enact_s273_d1_address.py`). "
    "`knowledge/_roles_drift.py` — the measured instrument, selftest 12/12 — then reads "
    "**108/108 agree, 0 silent, 0 roles at zero**, and `gen_kg_roles_desk.py --land "
    "--ratified s270-D2` took `providesRole` from **24 to 108** across **207 edges / 85 "
    "metas** with `_validate_kg.py` OK. Correction inscribed at: `0d98a34` · "
    "`knowledge/_rulings.json` § `s273-D1` · "
    "`_DECISION-HISTORY/2026-09-15-273-the-address-and-the-registry.md` § 3.** The struck text "
    "stands verbatim above rather than being deleted. ⚠ **WHAT DID NOT DISCHARGE WITH IT: the "
    "DESK gates were NOT authored** — `s273-D2`'s pass two covers 49 silent providers across "
    "8 roles and has not started; it rides on as item ② of the #274 set."
)
assert aged.count(OLD2) == 1, aged.count(OLD2)
aged = aged.replace(OLD2, NEW2, 1)
EDITS.append(("carry ⑤ — roles.json MEMBERSHIP DRIFT",
              "STRUCK as DISCHARGED, s183-D1 + s188-D2 receipt named (s273-D1 / 0d98a34); the "
              "DESK-gate authoring half explicitly NOT discharged"))

assert len(EDITS) == 2

# ---- (c) this session's new items -------------------------------------------------------------
NEWITEMS = open(os.path.join(HERE, "carry274-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #274:** " + NEWITEMS + " · " + aged[len("> **residual → #273:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #274",
    "",
    "*Written straight here at the #273 wrap (✅ **NO DATE SPLIT — the session, its ritual and "
    "all six of its commits are 2026-09-15**) under `s225-D2` clause (i). Ages +1, wording "
    "unchanged, nothing dropped for being old; ★ **TWO carries STRUCK, and BOTH are DISCHARGES "
    "rather than retractions** — item ① of the #273 set (enact the ~220 tolerance, or leave "
    "`s272-D93` a ruling only) was closed by his two-word answer *\"1. advisory arm\"* and the "
    "arm at `4294b60`, and item ⑤ of the #272 set (the `roles.json` membership drift, "
    "re-reported by the landing itself and still not fixed) was closed by `s273-D1` and the "
    "84-meta address pass at `0d98a34`. Each is struck with its `s183-D1`/`s188-D2` receipt "
    "rather than re-typed or deleted, and ⛔ **each strike names what did NOT discharge with "
    "it** — the arm's BLOCKING tier is still unruled, and the DESK gates of `s273-D2` are still "
    "unauthored. ⛔ **NO OTHER carry was re-worded: the three explorer hues, the 31 declared "
    "guesses, the HSBC ingestion gap (now also parked as `P-273-1` on his *\"i cant get access "
    "to the common library specs right now, we'll have to park it\"*), the two blocking tiers, "
    "the 79 clicks, the #179 reformat class, the #243 double-count and every #119 open were all "
    "CARRIED THROUGH #273 UNTOUCHED and age with their wording intact.** ★★★ **Dave ruled four "
    "times at #273 in the `_rulings.json` sense — the store moved 562 → 566 — and the session's "
    "shape was one drift fixed (`s273-D1`, 84 metas addressed), one vocabulary decided "
    "(`s273-D4`, a REGISTRY and not a whitelist), one sidequest pulled forward as research "
    "(`s273-D3`), and one posture turned into an advisory arm (`s272-D93` enacted). ⛔ **The "
    "eight new items below are every question this session opened and did not close, and all "
    "but two are his.***",
    "",
]

out = []
for ln in lines:
    if ln.strip() == "## residual → #273":
        out.extend(SECTION)
        out.append("<!-- WRITTEN-FIRST: residual → #274 — the aged tail below the EIGHT new "
                   "items is the #273 line put through ONE programmatic pass "
                   "(`notes/_lanes/273/W/carry274.py`): %d age brackets bumped (%d of them "
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
print("CARRIES: #273 items %d → #274 items %d (+%d; %d NEW — 0 became countable, %d new items "
      "arrive uncounted)" % (before, after, after - before, n_new, 8))
print("ages bumped: %d numbered + %d NEW — 0 = %d" % (n_num, n_new, n_num + n_new))
for t, w in EDITS:
    print("SURGICAL EDIT: %s — %s" % (t, w))
