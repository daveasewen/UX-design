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
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
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
    # _validate_state_contrast.py UN-EXEMPTED #125 (s125-D2, Dave). Its reason claimed the
    # chromium download was "blocked by sandbox TLS (UNABLE_TO_GET_ISSUER_CERT_LOCALLY on all
    # 3 CDNs)". DISPROVEN by direct observation, not by argument: _RUNBOOK-render-verify.md was
    # followed literally and the download SUCCEEDED (chromium_headless_shell-1234 in the cache),
    # chromium launched, and the validator ran and produced output. The installer's non-zero
    # exit is the __dirlock EPERM the runbook banks as "a failure message AFTER a success" —
    # the original diagnosis read that exit as a refusal. ⇒ an environmental fence is verified
    # against the thing itself, never carried forward from a prior session's banner.
    # EMPTY IS A LEGITIMATE STATE: selftest bites 3+4 use a SYNTHETIC exemption so they keep
    # biting with no real entries here — a bite that needs a real exemption to exist is a bite
    # that can silently stop existing.
}


def check(build_text: str, disk: list[str],
          exempt_map: dict[str, tuple[str, str]] | None = None) -> list[str]:
    """Return failure strings. Pure so the selftest can bite it.

    `exempt_map` defaults to the module's EXEMPT; passing it explicitly is what lets the
    selftest bite the exemption clauses with a SYNTHETIC entry instead of borrowing a real
    one (#125 — EXEMPT is legitimately empty now, and `next(iter(EXEMPT))` would have raised).
    """
    exempt_map = EXEMPT if exempt_map is None else exempt_map
    fails = []
    for name in sorted(disk):
        wired = re.search(r'["\']' + re.escape(name) + r'["\']', build_text)
        is_exempt = name in exempt_map
        if name == SELF:
            # the wiring gate itself must be wired — an unwired wiring gate is a joke
            if not wired:
                fails.append(f"ORPHAN (the gate itself): {name} has no STEPS entry in _build_all.py")
            continue
        if not wired and not is_exempt:
            fails.append(f"ORPHAN: {name} exists on disk but has no STEPS entry in _build_all.py "
                         f"and no named exemption. Wire it or exempt it BY NAME with a reason.")
        if wired and is_exempt:
            fails.append(f"STALE EXEMPTION: {name} is wired AND exempt "
                         f"({exempt_map[name][0]!r}, {exempt_map[name][1]}). Remove the exemption.")
    for name in exempt_map:
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
    # exemption (exempt AND wired) must fire, proving the exempt list can't absorb a fix silently.
    # SYNTHETIC name, not a borrowed real one (#125): these two bites used to read
    # `next(iter(EXEMPT))`, so emptying EXEMPT would have crashed the selftest — and "make the
    # crash go away" would have meant deleting the two bites that police the exemption list
    # exactly when nothing is exempt. The clause must be testable when the list is empty.
    synth = "_validate_synthetic_exemption.py"
    synth_map = {synth: ("SYNTHETIC — selftest fixture only, never a real exemption", "2026-08-07")}
    wired_plus = build_text + f'\n# ("x", "{synth}"),\n("x", "{synth}")'
    if not any("STALE EXEMPTION" in f and synth in f
               for f in check(wired_plus, disk + [synth], synth_map)):
        fails.append(f"bite 3 FAILED: stale exemption for {synth} did not fire")
    # bite 4: a dangling exemption (exempt, not on disk) must fire
    if not any("DANGLING EXEMPTION" in f and synth in f
               for f in check(build_text, disk, synth_map)):
        fails.append("bite 4 FAILED: dangling exemption did not fire")
    print(f"wiring selftest: 4 bites · {len(fails)} failure(s)")
    for f in fails:
        print(f"  ⛔ {f}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else run())
