#!/usr/bin/env python3
"""Build `_state.json` from the two live sources. GENERATED — nothing here is hand-typed.

⚠ WHY THIS IS A SCRIPT AND NOT A ONE-OFF PASTE
-----------------------------------------------
A hand-typed inventory is the defect this whole rebuild is aimed at: #86 measured a handoff's
"118 markers" against reality and found ~40, and #85's proposal quotes "95 item-slots / 84
distinct" which no probe in the repo reproduces. A count that a human or an agent typed wears a
measurement's clothes [[measure-dont-convert-units]]. So the store is BUILT from its sources by
this file, re-runnable, and the row count IS the count.

THE TWO SOURCES
---------------
1. `knowledge/_GOVERNING-RECORDS.md` — 17 table rows, each with a `closes_when` Dave RATIFIED at
   #86 ("Yes, firm — record them"). These arrive CONDITIONED. This register is not superseded by
   the store; it stays the human-readable face, and this script is what keeps the two honest.
2. `GOOD-MORNING.md` DOFIRST lines via `_capture_gate.DOFIRST_ITEM_RE` — the 19 inherited
   worklist items. These have no close condition and arrive UNCONDITIONED, which is a DECLARED
   debt, frozen at birth by `_state.LEGACY_IDS`.

⛔ WHAT THIS SCRIPT REFUSES TO DO
---------------------------------
**It does not close anything, and it does not invent a close condition.** Several inherited items
carry ✅/CLOSED/LANDED in their own text while still occupying the worklist — that is the
immortality defect made visible, and it is exactly the population an agent would be tempted to
tidy. Promotion and closure are Dave's alone (`derivation-governance`, STANDING), so those items
are REPORTED as closure candidates and entered as `open`. A migration that quietly closed nine
items would produce a smaller, wronger list and no receipt.

**Owner is INFERRED for the inherited 19, and says so.** The DOFIRST prose has no owner field. The
inference is one rule — a `⬛` marker or a literal "DAVE'S" means Dave's — and every inferred item
carries `owner_inferred: true` so a later reader can tell a measurement from a guess
[[feedback-measuring-tool-must-not-guess]]. The 17 governing rows are NOT inferred: the register
exists precisely because every one of them is Dave-owed.
"""

from __future__ import annotations
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import _state  # noqa: E402

GOV = os.path.join(HERE, "_GOVERNING-RECORDS.md")
GM = os.path.join(ROOT, "GOOD-MORNING.md")

GOV_ROW_RE = re.compile(r"^\|\s*(G\d{1,2}[a-z]?)\s*\|(.+?)\|(.+?)\|(.+?)\|\s*$")
CLOSED_HINT_RE = re.compile(r"✅|\bCLOSED\b|\bLANDED\b|\bCONSUMED\b")


def _plain(s: str) -> str:
    """Strip markdown decoration for a title. Keeps the words, drops the shouting."""
    s = re.sub(r"`([^`]*)`", r"\1", s)
    # ⛔ Underscores are NOT stripped. They were, for one render, and it turned
    # `DOFIRST_INDEX_TK_MAX` into `DOFIRSTINDEXTKMAX` — a corrupted symbol name published to the
    # boot path, where a reader would grep for it and find nothing [[unmatched-grep-is-not-an-absence]].
    # Markdown emphasis via `_` is vanishingly rare in this corpus; mangled identifiers are not.
    s = re.sub(r"\*\*|\*", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _title_of(body: str, limit: int = 72) -> str:
    """First clause, not a byte-truncation. The old index cut at 46 chars mid-word because the
    renderer had to carry the body; the store carries the body, so the title can end on a word."""
    head = re.split(r"\s+[—–]\s+|\.\s+|:\s+", _plain(body), maxsplit=1)[0]
    if len(head) > limit:
        head = head[:limit].rsplit(" ", 1)[0] + "…"
    return head


def governing_items():
    out = []
    with open(GOV, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            m = GOV_ROW_RE.match(line.rstrip("\n"))
            if not m:
                continue
            gid, item, cw, status = (g.strip() for g in m.groups())
            out.append({
                "id": gid,
                "title": _title_of(item),
                "body": _plain(item),
                "state": "blocked" if "blocked on" in status.lower() else "open",
                "opened": 86,
                "owner": "dave",
                "condition": _state.CONDITIONED,
                "closes_when": _plain(cw),
                "links": [],
                "home": f"knowledge/_GOVERNING-RECORDS.md:{ln}",
                "provenance": "#86 triage, 19/19 ratified — Dave: 'Yes, firm — record them'",
            })
    return out


def worklist_items():
    import _capture_gate as cg
    out, inferred, closure_candidates = [], [], []
    with open(GM, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for ln, line in enumerate(lines, 1):
        m = cg.DOFIRST_ITEM_RE.match(line)
        if not m:
            continue
        num, body = m.group(1), m.group(2)
        wid = f"W-{num}" if not num.isdigit() else f"W-{int(num):02d}"
        owner = "dave" if ("⬛" in body or "DAVE'S" in body.upper()) else "claude"
        if owner == "dave":
            inferred.append(wid)
        if CLOSED_HINT_RE.search(body):
            closure_candidates.append((wid, _title_of(body)))
        out.append({
            "id": wid,
            "title": _title_of(body),
            "body": _plain(body)[:400],
            "state": "open",
            "opened": 0,                      # UNKNOWN — the prose carries no birth session for
                                              # most items. NOT defaulted to a plausible number.
            "owner": owner,
            "owner_inferred": True,
            "condition": _state.UNCONDITIONED,
            "closes_when": None,
            "links": [],
            "home": f"GOOD-MORNING.md:{ln}",
            "provenance": "inherited DOFIRST prose, migrated #88 — no close condition existed",
        })
    return out, inferred, closure_candidates


def main():
    gov = governing_items()
    work, inferred, candidates = worklist_items()
    items = gov + work

    doc = {
        "_README": [
            "THE TASK STORE. Generated by _migrate_state.py from _GOVERNING-RECORDS.md +",
            "GOOD-MORNING.md's DOFIRST region. Validated by _state.check() — BLOCKING.",
            "An item cannot be opened without a checkable `closes_when`. The 19 inherited",
            "items are exempt as a FROZEN set (_state.LEGACY_IDS) and that set may only shrink.",
            "`opened: 0` means the birth session is UNKNOWN — it is not defaulted to a guess.",
        ],
        "meta": {"schema": _state.SCHEMA, "built_by": "_migrate_state.py", "built_at": "#88"},
        "items": items,
    }

    ok, fails, notes = _state.check(doc)
    if not ok:
        print("⛔ MIGRATION REFUSED — the store it built does not pass its own gate:")
        for f in fails:
            print(f"   {f}")
        return 1

    _state.save(doc)
    c = _state.counts(doc)
    print(f"✅ _state.json BUILT — {c['total']} items "
          f"({len(gov)} governing, {len(work)} inherited worklist)")
    print(f"   live {c['live']} · conditioned {c['conditioned']} · "
          f"UNCONDITIONED {c['unconditioned']} (frozen set {len(_state.LEGACY_IDS)})")
    print(f"   by state: {c['by_state']}")
    print(f"   live by owner: {c['by_owner']}")
    for n in notes:
        print(f"   ⚠ {n}")
    print(f"   ⚠ owner INFERRED for {len(inferred)} inherited item(s): {', '.join(inferred)} "
          f"— flagged `owner_inferred`, never presented as measured")
    if candidates:
        print(f"   ⬛ {len(candidates)} inherited item(s) carry ✅/CLOSED/LANDED in their own text "
              f"and are STILL on the worklist — entered as `open`, NOT auto-closed "
              f"(closure is Dave's). This is the immortality defect, itemised:")
        for wid, t in candidates:
            print(f"      {wid}  {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
