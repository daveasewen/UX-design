#!/usr/bin/env python3
"""_memory_cap_check.py — MECHANISE THE `MEMORY.md` CAP: the index stub has a ceiling and a check.

Built #244 lane C. Carried unbuilt from #242 and #243 ("the mechanised `MEMORY.md` cap NOT
built"). Lane F's #242 decomposition measured the pre-stub index at 3,569 cl100k tape — the
single largest line of OURS in a 70,710 boot — and `s243-D1` cut it to a STUB. Nothing then
stopped the stub growing straight back: a boot line with no ceiling regrows, and the regrowth is
invisible because it arrives one hook at a time.

★ WHY THIS IS A SEPARATE TOOL AND NOT A LINE IN `_boot_remeasure.py`: the file it grades LIVES
  OUTSIDE THE REPO. The auto-memory index is a Cowork surface (`<mount>/.auto-memory/MEMORY.md`),
  session-scoped, read-only from here, and absent entirely on any tree that is not a live Cowork
  mount. So the path is an ARGUMENT, never a repo-relative constant, and a missing path is
  DECLARED MISSING rather than graded 0 [[unmatched-grep-is-not-an-absence]].

⚠ UNIT DISCIPLINE — READ BEFORE QUOTING [[measure-dont-convert-units]]:
  Every figure this tool prints is a cl100k TAPE token count (tiktoken). TAPE IS NOT REAL. It is
  a proxy for SHAPE and MOVEMENT, and it is NEVER converted to, compared against, or summed with
  a `message.usage` real figure. The cap is expressed in tape and graded in tape, end to end.
  Refuses loudly without tiktoken — a measuring tool must not guess (the `ds-025` standard).

THE CAP AND ITS PROVENANCE — DERIVED, NOT PICKED (the `s240-D1`/`s241-D1` discipline):
  `MEMORY_CAP_TAPE = 1802` = the #244 measurement of the live post-`s243-D1` stub (1,502 tape,
  4,884 B, 33 lines) + 20% headroom, floored. The 20% is HEADROOM FOR ONE SESSION'S HOOKS, not a
  budget to spend: a stub at 1,800 tape is already at the ceiling and the next ⛔ hook breaches
  it. ⬛ THE NUMBER IS AN AGENT'S DERIVATION FROM A MEASURED BASE, NOT DAVE'S WORD — the base is
  reproducible (`--measure`), the multiplier is not ruled. Re-derive with `--derive PATH` after
  any deliberate stub restructure; do not nudge it to make a red run green.

CONSUMER (named, or this is a zombie [[instrument-without-a-consumer]]):
  `_capture_gate.py::memory_cap_check` wires it into the wrap as a WARN arm (tier constant
  `MEMORY_CAP_BLOCKING = False`; promotion to BLOCKING is DAVE'S WORD, flag and pin move as a
  pair). Second consumer: the conductor at the opener, beside `knowledge/_checkin.py`, whenever
  the boot-drift check reports movement — this says whether the index is the line that moved.

Usage:
  python3 knowledge/_memory_cap_check.py --measure --path PATH   # report tape, no verdict
  python3 knowledge/_memory_cap_check.py --check --path PATH     # exit 1 OVER cap
  python3 knowledge/_memory_cap_check.py --check                 # PATH resolved by mount glob
  python3 knowledge/_memory_cap_check.py --check --cap 1802 --path PATH
  python3 knowledge/_memory_cap_check.py --derive --path PATH    # what a +20% cap would be
  python3 knowledge/_memory_cap_check.py --selftest              # bites, incl. a break arm
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_sys.path.insert(0, _hg_os.path.dirname(_hg_os.path.abspath(__file__)))
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob
import os
import sys

# ⛔ The index is NOT in this repo. Session-scoped, so resolved by glob and never hard-coded to
# one session name — the same resolution `_boot_decompose.py` uses, for the same file.
MOUNT_GLOB = "/sessions/*/mnt"
MEMORY_REL = os.path.join(".auto-memory", "MEMORY.md")

# ★ DERIVED #244 from a measured base — see the docstring's provenance block. Move it only by
# re-deriving from a new measured base, and say so in the same breath.
MEMORY_CAP_TAPE = 1802
CAP_BASE_TAPE = 1502          # the live stub at #244, post-`s243-D1`
CAP_HEADROOM = 0.20
CAP_PROVENANCE = ("#244 measurement of the post-`s243-D1` stub: 1,502 cl100k tape "
                  "(4,884 B, 33 lines) + 20% headroom, floored → 1,802 tape. "
                  "Agent's derivation from a measured base; the multiplier is NOT ruled.")


def _enc():
    """Refuse loudly rather than approximate. A cap graded by a guess is not a cap."""
    try:
        import tiktoken
    except ImportError:
        print("REFUSED: tiktoken is not installed, so nothing here can be MEASURED. Install it "
              "(`pip install tiktoken --break-system-packages`) — this tool does not estimate a "
              "cap from bytes, because a guessed measurement is the defect it exists to catch.",
              file=sys.stderr)
        raise SystemExit(2)
    return tiktoken.get_encoding("cl100k_base")


def resolve_path(explicit=None):
    """(path, how) — an explicit --path always wins; otherwise the live Cowork mount.

    Returns (None, why) when there is nothing to measure. ⛔ NEVER returns a zero measurement
    for an absent file: absence is DECLARED, and the caller decides what a declaration costs.
    """
    if explicit:
        if not os.path.exists(explicit):
            return None, f"--path {explicit} does not exist"
        return explicit, "explicit --path"
    hits = sorted(glob.glob(MOUNT_GLOB))
    if not hits:
        return None, (f"no Cowork mount matched {MOUNT_GLOB} and no --path was given — the "
                      f"auto-memory index lives OUTSIDE this repo, so on a non-Cowork tree "
                      f"there is genuinely nothing to grade")
    p = os.path.join(hits[0], MEMORY_REL)
    if not os.path.exists(p):
        return None, f"mount {hits[0]} carries no {MEMORY_REL}"
    return p, f"resolved from mount {hits[0]}"


def measure(path, enc=None):
    """dict of TAPE figures for one file. Tape only — no real-token field exists here by design."""
    enc = enc or _enc()
    txt = open(path, encoding="utf-8", errors="replace").read()
    return {"path": path, "tape": len(enc.encode(txt)),
            "bytes": len(txt.encode()), "lines": txt.count("\n") + 1}


def grade(m, cap=MEMORY_CAP_TAPE):
    """(over: bool, line: str) — the verdict, in TAPE, with the margin stated either way."""
    over = m["tape"] > cap
    margin = m["tape"] - cap
    if over:
        line = (f"OVER CAP: MEMORY.md is {m['tape']:,} cl100k tape against a cap of {cap:,} "
                f"tape — {margin:+,} tape. Every session pays this in its boot, on every seat. "
                f"Prune the index to the ⛔/★★★ tier and push the rest to an overflow file "
                f"(the `s243-D1` shape); do NOT raise the cap to fit the file.")
    else:
        line = (f"WITHIN CAP: MEMORY.md is {m['tape']:,} cl100k tape against a cap of {cap:,} "
                f"tape — {abs(margin):,} tape of headroom. ⚠ TAPE, NOT REAL: a proxy for shape "
                f"and movement, never summed with a `message.usage` figure.")
    return over, line


def report(path=None, cap=MEMORY_CAP_TAPE, check=False, derive=False):
    enc = _enc()
    p, how = resolve_path(path)
    if p is None:
        print(f"DECLARED MISSING (not zeroed): {how}.", file=sys.stderr)
        # ⛔ 2 = COULD NOT MEASURE. Distinct from 1 = MEASURED AND OVER, so a caller can tell a
        # breach from an absence [[a-crash-is-not-a-fail]].
        return 2
    m = measure(p, enc)
    print(f"MEMORY.md CAP — cl100k TAPE only, never real [[measure-dont-convert-units]]")
    print(f"  file:  {m['path']}  ({how})")
    print(f"  size:  {m['tape']:,} tape · {m['bytes']:,} B · {m['lines']} lines")
    print(f"  cap:   {cap:,} tape")
    print(f"  prov:  {CAP_PROVENANCE}")
    if derive:
        d = int(m["tape"] * (1 + CAP_HEADROOM))
        print(f"  DERIVE: base {m['tape']:,} tape + {int(CAP_HEADROOM * 100)}% → {d:,} tape. "
              f"⛔ This PRINTS a candidate; it does not move MEMORY_CAP_TAPE. Moving the "
              f"constant is an edit with a stated reason, never a side effect of a run.")
        return 0
    over, line = grade(m, cap)
    print(f"  {'✗' if over else '✓'} {line}")
    return 1 if (over and check) else 0


def selftest():
    """Bites. ⛔ Every refusal must be shown able to FIRE, and the break arm must FAIL —
    a suite where nothing can go red proves only that the tool is silent."""
    import tempfile
    enc = _enc()
    fails, ran = [], []

    def bite(name, cond):
        ran.append(name)
        if not cond:
            fails.append(name)

    with tempfile.TemporaryDirectory() as td:
        small = os.path.join(td, "small.md")
        with open(small, "w", encoding="utf-8") as f:
            f.write("- one hook line\n")
        big = os.path.join(td, "big.md")
        with open(big, "w", encoding="utf-8") as f:
            f.write("- a hook line that is definitely long enough to blow a tiny cap\n" * 400)

        ms, mb = measure(small, enc), measure(big, enc)
        bite("measure returns a tape figure", isinstance(ms["tape"], int) and ms["tape"] > 0)
        bite("measure carries no real-token field", "real" not in ms and "real_tk" not in ms)
        bite("a small file is WITHIN a real cap", grade(ms, MEMORY_CAP_TAPE)[0] is False)
        bite("an oversized file is OVER the same cap", grade(mb, MEMORY_CAP_TAPE)[0] is True)
        bite("the OVER verdict refuses the raise-the-cap fix",
             "do NOT raise the cap" in grade(mb, MEMORY_CAP_TAPE)[1])
        bite("the WITHIN verdict states the unit", "TAPE, NOT REAL" in grade(ms)[1])

        # THE TIER BITE: --check is what turns a measurement into an exit code.
        bite("--check exits 1 over cap", report(big, cap=10, check=True) == 1)
        bite("no --check exits 0 over cap (measure-only is not a gate)",
             report(big, cap=10, check=False) == 0)
        bite("--check exits 0 within cap", report(small, cap=10_000, check=True) == 0)

        # ABSENCE IS DECLARED, NOT ZEROED — and it is a DIFFERENT exit code from a breach.
        missing = os.path.join(td, "nope.md")
        bite("a missing --path is DECLARED (exit 2), never graded 0",
             report(missing, check=True) == 2)
        bite("resolve_path refuses a missing explicit path",
             resolve_path(missing)[0] is None)
        bite("--derive prints a candidate and exits 0 without moving the constant",
             report(big, derive=True) == 0 and MEMORY_CAP_TAPE == 1802)

        # ★ THE BREAK ARM. A cap that cannot fire is decoration: prove the grader is load-bearing
        # by inverting the comparison and asserting the suite NOTICES.
        real_grade = globals()["grade"]
        try:
            globals()["grade"] = lambda m, cap=MEMORY_CAP_TAPE: (False, "always green")
            broken_caught = report(big, cap=10, check=True) != 1
        finally:
            globals()["grade"] = real_grade
        bite("BREAK ARM: an always-green grader is caught by the --check arm", broken_caught)

    print(f"[_memory_cap_check selftest] {'FAIL' if fails else 'OK'} — {len(ran)} bites"
          + (f"; RED: {fails}" if fails else "; every refusal fired, green controls held"))
    return 1 if fails else 0


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    path = args[args.index("--path") + 1] if "--path" in args else None
    cap = MEMORY_CAP_TAPE
    if "--cap" in args:
        cap = int(args[args.index("--cap") + 1].replace(",", "").replace("_", ""))
    return report(path, cap=cap, check="--check" in args, derive="--derive" in args)


if __name__ == "__main__":
    raise SystemExit(main())
