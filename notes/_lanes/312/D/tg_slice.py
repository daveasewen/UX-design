"""#311 lane D1-D3: run knowledge/_tests/test_gates.py in slices (the seat's call wall cuts the whole suite).
usage: python3 tg_slice.py pre | <lo>:<hi>   ('pre' = control + the four preamble cases; lo:hi slices CASES)"""
import sys, os, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'knowledge', '_tests'))
import test_gates as T
arg = sys.argv[1]
tmp = tempfile.mkdtemp(prefix='gate-tests-')
try:
    if arg == 'pre':
        T.case_control(tmp); T.case_write_gate(tmp); T.case_selftest_arms(); T.case_capture_gate_rulings_arm()
    else:
        lo, hi = (int(x) for x in arg.split(':'))
        if lo == 0: T.case_control(tmp)
        for c in T.CASES[lo:hi]: T.bite(tmp, *c)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
nf = sum(1 for _, ok, _ in T.RESULTS if not ok)
print(f"SLICE {arg}: {len(T.RESULTS)} test(s), {nf} failure(s) of {len(T.CASES)} cases total")
