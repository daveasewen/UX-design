#!/usr/bin/env python3
"""Wiring gate (#119, bucket D) — every `_validate_*.py` on disk must be WIRED or EXEMPT.

#118's finding: building an instrument is gated; WIRING it is not. A validator can be
written, reviewed, committed, remembered, and cited in memory without ever entering
`_build_all.py`'s STEPS — four orphans on disk proved it, each unwired for a different
reason. This gate closes that seam: it fails LOUD, naming the orphan, the moment a
`_validate_*.py` lands on disk with no STEPS entry and no named exemption.

Exemptions are EXPLICIT and NAMED in EXEMPT below — each carries a reason and a date.
An exemption for a file that IS wired, or that does not exist, is itself a FAIL
(a stale exemption is the same rot class as a stale constant).

Unit note: this gate COUNTS presence, it does not measure. A count finds orphans;
only RUNNING them sorts oversight from rot (#118). This gate's job is only the seam.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "_build_all.py"
SELF = "_validate_wiring.py"

# name -> (reason, date). May only shrink without a new declared reason.
EXEMPT: dict[str, tuple[str, str]] = {
    # _validate_screen.py UN-EXEMPTED #120 — the #118 "ROTTED" verdict was a drifted
    # a11y.check() call signature; repaired, bite-tested, WIRED in _build_all.py same pass.
    "_validate_state_contrast.py": (
        "ENVIRONMENTAL, re-diagnosed #120 — playwright module installs, but chromium download "
        "is blocked by sandbox TLS (UNABLE_TO_GET_ISSUER_CERT_LOCALLY on all 3 CDNs); needs an "
        "env with CA trust to playwright's CDN or a pre-cached browser. Not rot: never exercised.",
        "2026-08-07"),
}


def check(build_text: str, disk: list[str]) -> list[str]:
    """Return failure strings. Pure so the selftest can bite it."""
    fails = []
    for name in sorted(disk):
        wired = re.search(r'["\']' + re.escape(name) + r'["\']', build_text)
        exempt = name in EXEMPT
        if name == SELF:
            # the wiring gate itself must be wired — an unwired wiring gate is a joke
            if not wired:
                fails.append(f"ORPHAN (the gate itself): {name} has no STEPS entry in _build_all.py")
            continue
        if not wired and not exempt:
            fails.append(f"ORPHAN: {name} exists on disk but has no STEPS entry in _build_all.py "
                         f"and no named exemption. Wire it or exempt it BY NAME with a reason.")
        if wired and exempt:
            fails.append(f"STALE EXEMPTION: {name} is wired AND exempt "
                         f"({EXEMPT[name][0]!r}, {EXEMPT[name][1]}). Remove the exemption.")
    for name in EXEMPT:
        if name not in disk:
            fails.append(f"DANGLING EXEMPTION: {name} is exempt but not on disk. Remove it.")
    return fails


def run() -> int:
    build_text = BUILD.read_text(encoding="utf-8")
    disk = [p.name for p in HERE.glob("_validate_*.py")]
    fails = check(build_text, disk)
    n_wired = sum(1 for n in disk if re.search(r'["\']' + re.escape(n) + r'["\']', build_text))
    print(f"wiring gate: {len(disk)} validator(s) on disk · {n_wired} wired · "
          f"{len(EXEMPT)} exempt by name · {len(fails)} failure(s)")
    for f in fails:
        print(f"  ⛔ {f}")
    return 1 if fails else 0


def selftest() -> int:
    build_text = BUILD.read_text(encoding="utf-8")
    disk = [p.name for p in HERE.glob("_validate_*.py")]
    fails = []
    # bite 1 (DETECTION, remove a REAL entry): strip a wired validator from the build text
    wired_real = next(n for n in disk
                      if n not in EXEMPT and n != SELF
                      and re.search(r'["\']' + re.escape(n) + r'["\']', build_text))
    mutated = build_text.replace(wired_real, wired_real + ".MUTATED")
    if not any("ORPHAN" in f and wired_real in f for f in check(mutated, disk)):
        fails.append(f"bite 1 FAILED: removing {wired_real}'s entry did not fire")
    # bite 2 (DETECTION, other direction): add a fake orphan to disk
    if not any("_validate_fake_orphan.py" in f
               for f in check(build_text, disk + ["_validate_fake_orphan.py"])):
        fails.append("bite 2 FAILED: a fake orphan on disk did not fire")
    # bite 3 (REMEDIATION clause, not just detection — #104's lesson): a stale
    # exemption (exempt AND wired) must fire, proving the exempt list can't absorb a fix silently
    exempt_name = next(iter(EXEMPT))
    wired_plus = build_text + f'\n# ("x", "{exempt_name}"),\n("x", "{exempt_name}")'
    if not any("STALE EXEMPTION" in f and exempt_name in f for f in check(wired_plus, disk)):
        fails.append(f"bite 3 FAILED: stale exemption for {exempt_name} did not fire")
    # bite 4: a dangling exemption (exempt, not on disk) must fire
    disk_minus = [n for n in disk if n != exempt_name]
    if not any("DANGLING EXEMPTION" in f for f in check(build_text, disk_minus)):
        fails.append("bite 4 FAILED: dangling exemption did not fire")
    print(f"wiring selftest: 4 bites · {len(fails)} failure(s)")
    for f in fails:
        print(f"  ⛔ {f}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else run())
