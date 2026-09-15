#!/usr/bin/env python3
"""_validate_lane_ownership.py — ADVISORY BY DECLARATION. Warns when a commit
stages a path under notes/_lanes/<M>/ for a session M that is not this one.

#275 had two sessions open on one repo: the still-open #274 seat committed
5dd19ee into notes/_lanes/275/ and overwrote a lane input. This is Dave's "fix"
(#276, "1. fix") — it makes the collision VISIBLE. It does not make it
impossible: exit is always 0, nothing is blocked. The blocking tier, and the
rule itself (one-seat vs own-lane-only), are Dave's and are NOT ruled here.

  python3 knowledge/_validate_lane_ownership.py            # warn on staged paths
  python3 knowledge/_validate_lane_ownership.py --selftest # fixture, no git
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re, subprocess, sys

REPO = _hg_os.path.dirname(_hg_os.path.abspath(__file__)).rsplit("/knowledge", 1)[0]
LANE, SESSION = re.compile(r"^notes/_lanes/(\d+)/"), re.compile(r"YOU ARE #(\d+)")


def this_session(chain=None):
    """The session number _CHAIN.md declares; None if it cannot be read."""
    try:
        m = SESSION.search(open(chain or _hg_os.path.join(REPO, "_CHAIN.md"), encoding="utf-8").read())
    except OSError:
        return None
    return int(m.group(1)) if m else None


def offenders(paths, n):
    """(path, M) for every staged path under another session's lane."""
    hits = [(p.strip(), LANE.match(p.strip())) for p in paths]
    return [(p, int(m.group(1))) for p, m in hits if m and n is not None and int(m.group(1)) != n]


def staged():
    r = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=REPO,
                       capture_output=True, text=True)
    return [x for x in r.stdout.splitlines() if x.strip()]


def selftest():
    fix = ["notes/_lanes/276/tie-off/REPORT.md", "notes/_lanes/275/principles-kg/x.json",
           "knowledge/_rulings.json", "notes/_lanes/9/a.md"]
    ok = [("session parsed out of the _CHAIN.md line shape", this_session() == 276),
          ("own lane passes, two foreign lanes warn, non-lane path ignored",
           offenders(fix, 276) == [("notes/_lanes/275/principles-kg/x.json", 275),
                                   ("notes/_lanes/9/a.md", 9)]),
          ("unreadable _CHAIN.md means no session and NO false warning",
           this_session("/nonexistent") is None and offenders(fix, None) == [])]
    for claim, good in ok:
        print("  %s — %s" % ("OK  " if good else "FAIL", claim))
    print("selftest: %d/%d" % (sum(1 for _, g in ok if g), len(ok)))
    return 0 if all(g for _, g in ok) else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    n = this_session()
    if n is None:
        return print("LANE OWNERSHIP: _CHAIN.md carries no 'YOU ARE #N' line — nothing to check.")
    bad = offenders(staged(), n)
    if not bad:
        return print("LANE OWNERSHIP: OK — no staged path under another session's lane (this is #%d)." % n)
    print("LANE OWNERSHIP: WARNING — this is #%d and %d staged path(s) belong to another session's "
          "lane. ADVISORY (unruled): nothing is blocked." % (n, len(bad)))
    for p, m in bad:
        print("  #%s  %s" % (m, p))


if __name__ == "__main__":
    main()
