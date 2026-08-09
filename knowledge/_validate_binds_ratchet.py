#!/usr/bin/env python3
"""_validate_binds_ratchet.py — the BINDS SHRINK-ONLY RATCHET (s136-D1 axis A, staged by s140-D1 D3).

s136-D1 says every VISUAL prop declares a spine token binding. s140-D1 (D3) staged that
clause deliberately: "Permit now, enforce by gate later" — binds stays OPTIONAL in
meta.schema.json, and the mandatory clause lands HERE, as a ratchet, not as a schema
requirement. This is the "later".

WHAT A RATCHET IS (same shape as the type-composite debt ratchet)
  It does not demand a target. It forbids a REVERSAL. Coverage may rise freely; the
  floor rises with it (--rebase); coverage may never fall below the recorded floor.
  A ratchet is honest about a debt that cannot be paid in one session and still makes
  every backwards step a build failure.

WHAT IS COUNTED
  METAS carrying >= 1 props[].binds, over knowledge/components/*.meta.json,
  excluding EXAMPLE-*.meta.json (a teaching fixture, not the corpus).
  Counted at the META level, not the PROP level, on purpose: prop counts move when props
  are added or renamed for reasons that have nothing to do with binding coverage, so a
  prop-level floor would fire on unrelated edits. A meta either carries binding evidence
  or it does not.

  NOTE, DECLARED: this counts PRESENCE, not correctness. It cannot tell a good binding
  from a bad one, and it cannot see a visual prop that SHOULD have binds and does not.
  The correctness question is a different instrument (the binds draft + Dave's verdicts,
  reviews/BINDS-DRAFT-2026-08-09-s141-v1.json). Do not read a green here as "axis A is
  enacted" — read it as "axis A coverage has not gone backwards".

FLOOR
  knowledge/_binds-ratchet.json  {"floor": N, "measured": "YYYY-MM-DD", ...}
  The floor is only ever RAISED, and only by an explicit --rebase run. This gate never
  writes the floor down. If the file is missing the gate fails LOUD rather than
  inventing a floor of zero — an absent instrument must not read as a pass.

Usage:  python3 knowledge/_validate_binds_ratchet.py            # gate mode
        python3 knowledge/_validate_binds_ratchet.py --rebase   # raise the floor to today's count
        python3 knowledge/_validate_binds_ratchet.py --json
        python3 knowledge/_validate_binds_ratchet.py --corpus DIR --floor-file PATH
Exit non-zero when coverage is below the floor.
"""
import argparse
import datetime
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FLOOR_FILE = os.path.join(HERE, "_binds-ratchet.json")


class RatchetError(Exception):
    """A named failure of this gate's own machinery (not a coverage failure)."""


def metas(root):
    d = os.path.join(root, "components")
    if not os.path.isdir(d):
        raise RatchetError("component corpus not found: %s" % d)
    out = [p for p in sorted(glob.glob(os.path.join(d, "*.meta.json")))
           if not os.path.basename(p).startswith("EXAMPLE-")]
    if not out:
        raise RatchetError("component corpus is EMPTY — refusing to report a clean run")
    return out


def count(root):
    """Returns (count, [component names]). Fails LOUD and NAMED on an unreadable meta."""
    carrying = []
    total = 0
    for p in metas(root):
        b = os.path.basename(p)
        total += 1
        try:
            with open(p, encoding="utf-8") as fh:
                d = json.load(fh)
        except OSError as e:
            raise RatchetError("unreadable meta %s :: %s" % (b, e))
        except json.JSONDecodeError as e:
            raise RatchetError("meta %s is not JSON :: line %d col %d :: %s"
                               % (b, e.lineno, e.colno, e.msg))
        props = d.get("props")
        if props is None:
            continue
        if not isinstance(props, list):
            raise RatchetError("meta %s :: props is %s, expected a list"
                               % (b, type(props).__name__))
        for prop in props:
            if isinstance(prop, dict) and prop.get("binds") not in (None, "", [], {}):
                carrying.append(b[:-len(".meta.json")])
                break
    return len(carrying), carrying, total


def read_floor(path):
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
    except OSError:
        raise RatchetError("floor file missing: %s — an absent instrument must not read as a pass" % path)
    except json.JSONDecodeError as e:
        raise RatchetError("floor file %s is not JSON :: %s" % (path, e.msg))
    if not isinstance(d.get("floor"), int):
        raise RatchetError("floor file %s has no integer 'floor'" % path)
    return d


def main():
    ap = argparse.ArgumentParser(description="binds shrink-only ratchet (s136-D1 axis A)")
    ap.add_argument("--rebase", action="store_true", help="raise the floor to the measured count")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--corpus", default=HERE)
    ap.add_argument("--floor-file", default=FLOOR_FILE)
    a = ap.parse_args()
    try:
        n, carrying, total = count(a.corpus)
        floor_doc = read_floor(a.floor_file)
    except RatchetError as e:
        print("GATE ERROR (a crash is not a fail) :: %s" % e, file=sys.stderr)
        return 2
    floor = floor_doc["floor"]

    if a.rebase:
        if n < floor:
            print("REFUSED: --rebase cannot LOWER a ratchet floor (%d measured < %d floor)"
                  % (n, floor), file=sys.stderr)
            return 1
        floor_doc.update({"floor": n, "measured": str(datetime.date.today()),
                          "corpus": total, "carrying": sorted(carrying)})
        with open(a.floor_file, "w", encoding="utf-8") as fh:
            json.dump(floor_doc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print("REBASED floor -> %d of %d metas" % (n, total))
        return 0

    ok = n >= floor
    if a.json:
        print(json.dumps({"count": n, "floor": floor, "corpus": total,
                          "carrying": sorted(carrying), "pass": ok}, indent=2))
    else:
        print("BINDS RATCHET — s136-D1 axis A (staged by s140-D1 D3)")
        print("  metas carrying >=1 props[].binds : %d of %d" % (n, total))
        print("  floor (%s)                       : %d" % (floor_doc.get("measured", "?"), floor))
        if carrying:
            print("  carrying: %s" % ", ".join(sorted(carrying)))
        if not ok:
            print("FAIL BINDS-RATCHET  coverage %d is BELOW the floor %d — %d meta(s) lost their binds"
                  % (n, floor, floor - n))
        print("%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
