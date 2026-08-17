#!/usr/bin/env python3
"""
_gate_harness_stubs.py — the blind-harness-class detector (W-33, built #192).

WHY: _test_git_commit.py runs the REAL _git_commit.sh inside a fixture repo that contains only
the helper scripts the fixture builder writes stubs for. When a new gate is wired into
_git_commit.sh and no stub is added, every commit-path arm stops testing the script and starts
crashing on `can't open file .../<gate>.py` — and the crash READS AS A RESULT
[[a-crash-is-not-a-fail]]. That is not hypothetical: it happened at #188 (the doc-row gate, blind
for three sessions) and RECURRED at #191 (the s191-D1 showroom gate, found blind at #192 with 14
arms down and three mutation controls green for the wrong reason). Twice is a class, so gate the
condition rather than write a third reminder [[gate-dont-patch]].

WHAT IT CHECKS: every `python3 knowledge/<script>` invocation in _git_commit.sh has a
corresponding `write(os.path.join(know, "<script>"), ...)` fixture stub in _test_git_commit.py.

CONSUMER: it is an ARM of _test_git_commit.py (`harness_stub_coverage_W33`), so it runs on every
selftest. It is not a standalone script nobody calls [[instrument-without-a-consumer]].

Run:  python3 knowledge/_gate_harness_stubs.py        (exit 0 green / 1 red, list printed)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "_git_commit.sh")
HARNESS = os.path.join(HERE, "_test_git_commit.py")


def unstubbed(script_path=SCRIPT, harness_path=HARNESS):
    """Return sorted [(script_name, invocation_line)] invoked by the shell script but never
    written as a fixture stub by the harness. Fails LOUD if either file is unreadable."""
    for p in (script_path, harness_path):
        if not os.path.exists(p):
            raise RuntimeError("_gate_harness_stubs: cannot read %s — nothing to check" % p)
    with open(script_path, encoding="utf-8") as f:
        script = f.read()
    with open(harness_path, encoding="utf-8") as f:
        harness = f.read()
    stubbed = set(re.findall(r'write\(os\.path\.join\(know,\s*"([^"]+)"\)', harness))
    missing, seen = [], set()
    for line in script.splitlines():
        if line.lstrip().startswith("#"):
            continue          # comments discuss gates; they do not invoke them
        for name in re.findall(r'python3\s+knowledge/([A-Za-z0-9_\-]+\.py)', line):
            if name not in stubbed and name not in seen:
                seen.add(name)
                missing.append((name, line.strip()))
    return sorted(missing)


def main():
    try:
        missing = unstubbed()
    except RuntimeError as e:
        print("✗ %s" % e, file=sys.stderr)
        return 1
    if missing:
        print("✗ BLIND HARNESS (W-33): _git_commit.sh invokes gate script(s) that "
              "_test_git_commit.py's fixture never stubs. Every commit-path arm will CRASH on "
              "them, and the crash reads as a result [[a-crash-is-not-a-fail]]:", file=sys.stderr)
        for name, line in missing:
            print("    %s   ← invoked at: %s" % (name, line[:110]), file=sys.stderr)
        print("  Fix: add a STUB_TMPL stub + its STUB_*_EXIT env default in build_fixture(), and "
              "give the gate an arm that drives the stub non-zero.", file=sys.stderr)
        return 1
    print("— harness stub coverage complete (W-33): every knowledge/*.py gate invoked by "
          "_git_commit.sh has a fixture stub.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
