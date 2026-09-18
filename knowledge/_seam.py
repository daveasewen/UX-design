#!/usr/bin/env python3
"""_seam.py — THE LANE-SEAM CHECK. Three lines, run before every lane is cut and after every
lane lands. Born #283 on Dave's two words at the opener.

WHY (measured, three sessions). #277 crossed the 256,000 hard line under pressure. #281 read
the gauge every turn and overruled it every turn. #282 did not read it at all between two
lanes and breached by 81,559 — the largest on record. The arc points AWAY from the instrument.
The check-in exists and is law at the OPENER; nothing made it law at the SEAM, which is where
the lanes are cut and where the fill actually moves. Dave, #283 opener, on "I'll read it at
every lane seam and say the number in chat": *"can we do this in every session"*. On clearing
scratch before a lane at 99% disk: *"good, maybe we make this a regular check- more mechanical"*.

WHAT IT PRINTS — three lines, quotable verbatim in chat, nothing else:
  FILL  <now> real / <turns> turns · boot <boot> · <verdict against the three lines>
  DISK  /sessions <pct>% · <free> KB free · <verdict>
  SCRATCH <n> own entries · <removed|kept> · <kept-list>

VERDICTS are the ruled lines, imported from `_gauge_tokens.py`, never restated here:
  STOP_LINE_TK 180,000 (s260-D2/s271-D1) → past it: "STOP LINE PASSED — wrap before the next lane"
  TOLERATED_TK 220,000 (s272-D93)       → past it: "OUTSIDE TOLERANCE — no more lanes"
  BUDGET_HARD  256,000                  → past it: "HARD LINE BREACHED"

SCRATCH is cleaned MECHANICALLY (the current user's own top-level entries under /tmp and
/var/tmp — the only litter anyone can ever remove, see `_gate_scratch_hygiene.py`), with ONE
keep-list: the git shim the mount needs (`/tmp/gitshim`), which ritual step 4c deleted at #282.
Anything on the keep-list is named as kept, never silently skipped.

⚠ ADVISORY, DELIBERATELY. It reports; it never blocks and never exits non-zero on a reading.
The obligation it carries is the CONDUCTOR'S: quote the FILL line in chat at every seam. A
seam that runs it and does not quote it has not run it. Promotion to blocking is Dave's.

Usage:
  python3 knowledge/_seam.py              # the three lines; own scratch IS cleaned
  python3 knowledge/_seam.py --no-clean   # read only
  python3 knowledge/_seam.py --selftest   # verdict + keep-list arms
"""
import os, sys, json, subprocess, argparse

_d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import _gauge_tokens as G
import _gate_scratch_hygiene as H

KEEP = ("/tmp/gitshim",)          # the mount's git shim — deleted by 4c at #282, never again
DISK_WARN_PCT = 90                # same PICKED figure as _checkin.DISK_WARN_PCT


def fill_verdict(now: int) -> str:
    if now >= G.BUDGET_HARD:
        return f"⛔⛔ HARD LINE BREACHED (+{now - G.BUDGET_HARD:,} over {G.BUDGET_HARD:,})"
    if now >= G.TOLERATED_TK:
        return f"⛔ OUTSIDE TOLERANCE {G.TOLERATED_TK:,} — no more lanes, wrap"
    if now >= G.STOP_LINE_TK:
        return f"⚠ STOP LINE {G.STOP_LINE_TK:,} PASSED — tolerated to {G.TOLERATED_TK:,}; wrap before the next lane"
    return f"✅ {G.STOP_LINE_TK - now:,} real under the {G.STOP_LINE_TK:,} stop line"


def disk_verdict(pct: float) -> str:
    return "⛔ NEAR FULL — no render lane until cleared" if pct >= DISK_WARN_PCT else "✅"


def checkin_json(window: int) -> dict:
    r = subprocess.run([sys.executable, os.path.join(_d, "_checkin.py"), "--window", str(window),
                        "--no-block", "--no-rehearse", "--no-grades", "--json"],
                       capture_output=True, text=True, timeout=300)
    return json.loads(r.stdout)


def scratch_line(clean: bool) -> str:
    own = H.mine()
    kept = [p for p in own if p in KEEP]
    rm = [p for p in own if p not in KEEP]
    if not own:
        return "SCRATCH 0 own entries · clean"
    done = []
    if clean:
        done = [p for p in rm if H._rm(p)]
    parts = [f"SCRATCH {len(own)} own entr{'y' if len(own) == 1 else 'ies'}"]
    parts.append(f"removed {len(done)}/{len(rm)}" if clean else f"{len(rm)} removable (--no-clean)")
    if kept:
        parts.append("kept " + ", ".join(kept))
    return " · ".join(parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--window", type=int, default=G.BUDGET_WORKING)
    ap.add_argument("--no-clean", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        d = checkin_json(a.window)
        f = d["fill"]
        if f.get("available"):
            print(f"FILL  {f['now']:,} real / {f['turns']} turns · boot {f['boot']:,} · "
                  f"{fill_verdict(f['now'])}")
        else:
            print("FILL  UNREADABLE — the check-in could not read the transcript; say so, do not guess")
        for r in d["disk"]:
            if r["mount"] == "/sessions":
                if r["available"]:
                    print(f"DISK  /sessions {r['pct']:.1f}% · {r['free_kb']:,} KB free · "
                          f"{disk_verdict(r['pct'])}")
                else:
                    print(f"DISK  /sessions UNREADABLE — {r['reason']}")
    except Exception as e:          # the reading failed — named, never defaulted
        print(f"FILL  UNREADABLE — {type(e).__name__}: {e}")
    print(scratch_line(clean=not a.no_clean))
    return 0


def selftest() -> int:
    fails = []
    arms = [(0, "under"), (G.STOP_LINE_TK, "STOP LINE"), (G.TOLERATED_TK, "OUTSIDE TOLERANCE"),
            (G.BUDGET_HARD, "HARD LINE BREACHED")]
    for now, expect in arms:
        v = fill_verdict(now)
        if expect not in v:
            fails.append(f"[fill {now}] expected '{expect}' in '{v}'")
    if "NEAR FULL" not in disk_verdict(DISK_WARN_PCT) or "NEAR FULL" in disk_verdict(DISK_WARN_PCT - 1):
        fails.append("[disk edge] warn threshold wrong")
    # keep-list arm: a path on KEEP is never in the removable set
    own = list(KEEP) + ["/tmp/x-litter"]
    rm = [p for p in own if p not in KEEP]
    if KEEP[0] in rm or "/tmp/x-litter" not in rm:
        fails.append(f"[keep-list] {rm}")
    print("\n".join(fails) if fails else f"seam selftest: {len(arms) + 2} arms, all GREEN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
