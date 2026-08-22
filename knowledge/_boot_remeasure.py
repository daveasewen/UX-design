#!/usr/bin/env python3
"""_boot_remeasure.py — measure the DISK-RESIDENT half of boot, per session, in REAL-proxy units.

ORDERED by s214-D5 (2026-08-21, Dave). Discharges the warning that stood unactioned ~72
sessions at _gauge_tokens.py:104 ("RE-MEASURE WHEN THE SESSION SHAPE CHANGES") and the
"cheap first step" priced at _DS-IMPROVEMENTS.md:1789 — the disk half is "a variable this
programme shrinks, and nobody has ever watched it move."

CONSUMER (named, or this is a zombie [[instrument-without-a-consumer]]): the conductor at
the opener (beside _checkin.py) and the boot-band re-base sitting (s208-D1 rider material).
The wrap quotes the figures when the boot ran out of band.

⚠ UNIT DISCIPLINE — READ BEFORE QUOTING:
  This tool counts in cl100k tape tokens (tiktoken), a PROXY for SHAPE and MOVEMENT, never
  the real thing. It must NEVER be summed with, scaled to, or substituted for a
  `message.usage` real figure [[measure-dont-convert-units]]. Its job is the DELTA: the
  same file measured by the same proxy across sessions shows growth/shrinkage honestly.
  Every output line carries the unit. Refuses loudly without tiktoken (a measuring tool
  must not guess — the ds-025 standard).

Usage:
  python3 knowledge/_boot_remeasure.py            # measure + print
  python3 knowledge/_boot_remeasure.py --log      # also append one JSONL row to notes/_BOOT-DISK-LOG.jsonl
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_sys.path.insert(0, _hg_os.path.dirname(_hg_os.path.abspath(__file__)))
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, sys, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The disk-resident boot inputs this seat is known to load (mount paths where they differ).
TARGETS = [
    ("_CHAIN.md (turn-2 additive)", os.path.join(REPO, "_CHAIN.md")),
    ("MEMORY.md (auto-memory index)", "/sessions/upbeat-compassionate-darwin/mnt/.auto-memory/MEMORY.md"),
]

def main():
    try:
        import tiktoken
    except ImportError:
        print("REFUSING TO GUESS: tiktoken is not installed.\n"
              "  pip install tiktoken --break-system-packages\n"
              "  A measuring tool that estimates silently is the ds-025 defect.", file=sys.stderr)
        return 2
    enc = tiktoken.get_encoding("cl100k_base")
    rows, missing = [], []
    for label, path in TARGETS:
        if not os.path.exists(path):
            missing.append((label, path)); continue
        text = open(path, encoding="utf-8", errors="replace").read()
        rows.append({"label": label, "path": path, "tape_tk": len(enc.encode(text)),
                     "bytes": len(text.encode())})
    print("BOOT DISK RE-MEASURE — unit: cl100k TAPE tokens (PROXY — shape/delta only, NEVER real)")
    for r in rows:
        print(f"  {r['tape_tk']:>8,} tape  {r['bytes']:>9,} B   {r['label']}")
    for label, path in missing:
        print(f"  MISSING (declared, not zeroed): {label} — {path}")
    total = sum(r["tape_tk"] for r in rows)
    print(f"  {total:>8,} tape  TOTAL of the files found ({len(rows)}/{len(TARGETS)})")
    print("  ⚠ compare THIS session's figures to LAST session's figures — the delta is the datum.")
    if "--log" in sys.argv:
        row = {"at": datetime.datetime.now().isoformat(timespec="seconds"),
               "unit": "cl100k_tape_proxy", "files": rows,
               "missing": [p for _, p in missing]}
        log = os.path.join(REPO, "notes", "_BOOT-DISK-LOG.jsonl")
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"  logged → {log}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
