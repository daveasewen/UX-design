#!/usr/bin/env python3
"""#265-B — does the s263-D10 bite arm CATCH A FAIL-OPEN EDIT TO THE CHECK ITSELF?

[[mutation-tests-the-clause-not-the-feature]]: a bite arm that only ever sees a stale FIXTURE
proves the fixture, not the clause. So this drives the arm against MUTATED COPIES of
`_capture_gate.py` in which the freshness check has been fail-opened three different ways, and
asserts the arm turns RED each time — plus an unmutated CONTROL copy, loaded the same way, which
must stay GREEN.

No copy of knowledge/ is taken: one 638 KB source file per mutant, in a temp dir.
Run: python3 notes/_lanes/265/B/drive_meta_mutation.py
"""
import importlib.util
import io
import contextlib
import os
import shutil
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
KNOW = os.path.join(ROOT, "knowledge")
SRC = os.path.join(KNOW, "_capture_gate.py")

# Pre-import the REAL generator so the mutant's own `import _render_rulings` resolves off
# sys.modules (the mutant sits outside knowledge/ and must not be given a second copy).
sys.path.insert(0, KNOW)
import _render_rulings  # noqa: F401,E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def m_control(s):
    return s


def m_branch_dead(s):
    """FAIL-OPEN 1 — the STALE branch can never be taken."""
    old = "    if rc != 0:\n        fails.append(f\"s263-D10 RULINGS PAGE STALE"
    new = "    if False:\n        fails.append(f\"s263-D10 RULINGS PAGE STALE"
    assert old in s
    return s.replace(old, new, 1)


def m_demoted(s):
    """FAIL-OPEN 2 — the failure is re-routed to notes (advisory), which is how a BLOCKING
    check gets quietly demoted without deleting a line."""
    old = "        fails.append(f\"s263-D10 RULINGS PAGE STALE"
    new = "        notes.append(f\"s263-D10 RULINGS PAGE STALE"
    assert old in s
    return s.replace(old, new, 1)


def m_gutted(s):
    """FAIL-OPEN 3 — the whole check returns green before it reads anything."""
    old = ("    fails, notes = [], []\n"
           "    src = os.path.join(repo, \"knowledge\", \"_rulings.json\")")
    new = ("    fails, notes = [], []\n"
           "    return fails, notes\n"
           "    src = os.path.join(repo, \"knowledge\", \"_rulings.json\")")
    assert old in s
    return s.replace(old, new, 1)


MUTANTS = [("CONTROL (unmutated copy)", m_control, False),
           ("FAIL-OPEN 1: `if rc != 0` -> `if False`", m_branch_dead, True),
           ("FAIL-OPEN 2: fails.append -> notes.append (blocking -> advisory)", m_demoted, True),
           ("FAIL-OPEN 3: check returns green before reading anything", m_gutted, True)]

src = open(SRC, encoding="utf-8").read()
bad = []
tmp = tempfile.mkdtemp(prefix="265B-meta-")
try:
    for i, (name, mut, expect_red) in enumerate(MUTANTS):
        p = os.path.join(tmp, "cg_%d.py" % i)
        with open(p, "w", encoding="utf-8") as f:
            f.write(mut(src))
        mod = load(p, "cg_mutant_%d" % i)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            fails = mod.selftest_rulings_freshness()
        red = bool(fails)
        ok = (red == expect_red)
        print("=" * 78)
        print("%s  %s" % ("PASS" if ok else "**PROBLEM**", name))
        print("  arm expected %s, arm was %s" % ("RED" if expect_red else "GREEN",
                                                 "RED" if red else "GREEN"))
        for line in buf.getvalue().strip().splitlines():
            print("  | " + line)
        for x in fails:
            print("  ! " + x)
        if not ok:
            bad.append(name)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("=" * 78)
print("VERDICT: %s" % ("every fail-open mutant is CAUGHT and the control stays green"
                       if not bad else "UNCAUGHT: " + "; ".join(bad)))
sys.exit(1 if bad else 0)
