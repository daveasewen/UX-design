#!/usr/bin/env python3
"""#265-B — drive the NEWLY REGISTERED `knowledge/_tests/test_gates.py` case, both arms.

ARM A: the real case, unmutated tree -> must RECORD PASS.
ARM B: the SAME subprocess shape (`test_gates.CG_ARM_SRC`) pointed at a knowledge dir whose
       `_capture_gate.py` is fail-opened -> must RECORD FAIL. Without arm B the registration is
       an assertion that cannot fail [[mutation-tests-the-clause-not-the-feature]].

The mutant dir is SYMLINKS to knowledge/*.py plus one real mutated file — no copy of knowledge/,
which is the whole point of not using `fresh_copy` here (disk was at 89% when this was written).

⛔ ONLY the one case runs. `test_gates.main()` takes ~25 `fresh_copy` copytrees and is not run.
Run: python3 notes/_lanes/265/B/drive_test_gates_case.py
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
KNOW = os.path.join(ROOT, "knowledge")
sys.path.insert(0, os.path.join(KNOW, "_tests"))
import test_gates as tg  # noqa: E402

print("=== ARM A — the registered case, real tree")
tg.case_capture_gate_rulings_arm()
a_name, a_ok, a_detail = tg.RESULTS[-1]
print("   detail: " + a_detail)

print("\n=== ARM B — the same case shape against a FAIL-OPENED _capture_gate.py")
src = open(os.path.join(KNOW, "_capture_gate.py"), encoding="utf-8").read()
old = "    if rc != 0:\n        fails.append(f\"s263-D10 RULINGS PAGE STALE"
assert old in src, "mutation anchor gone — the check was edited; re-read it"
mutated = src.replace(old, old.replace("if rc != 0:", "if False:"), 1)

b_ok = None
with tempfile.TemporaryDirectory() as td:
    fake = os.path.join(td, "knowledge")
    os.makedirs(fake)
    for f in os.listdir(KNOW):
        if f.endswith(".py") and f != "_capture_gate.py":
            os.symlink(os.path.join(KNOW, f), os.path.join(fake, f))
    with open(os.path.join(fake, "_capture_gate.py"), "w", encoding="utf-8") as fh:
        fh.write(mutated)
    r = subprocess.run([sys.executable, "-c", tg.CG_ARM_SRC % fake],
                       capture_output=True, text=True, timeout=120)
    out = (r.stdout + r.stderr).strip()
    b_ok = r.returncode == 0 and "[FAIL]" not in out          # the case's own PASS predicate
    print("   subprocess exit=%d" % r.returncode)
    for line in out.splitlines():
        print("   | " + line)
    print("   case predicate would record: %s" % ("PASS" if b_ok else "FAIL"))

good = a_ok and not b_ok
print("\nVERDICT: %s" % ("the registered case PASSES on the real tree and FAILS on a fail-opened "
                         "check — the registration bites"
                         if good else "REGISTRATION DOES NOT BITE"))
sys.exit(0 if good else 1)
