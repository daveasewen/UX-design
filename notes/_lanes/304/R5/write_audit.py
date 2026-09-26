#!/usr/bin/env python3
"""R5 — run one probe script under a sys.addaudithook and list every file it opened for WRITING
(or mutated). Proves the probe writes only inside notes/_lanes/304/R5/.
Usage: <python> notes/_lanes/304/R5/write_audit.py notes/_lanes/304/R5/<script>.py"""
import sys, os, runpy
LANE = os.path.dirname(os.path.abspath(__file__))
W = []
FL = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC
def hook(ev, a):
    if ev == "open":
        p, m, f = (list(a) + [None] * 3)[:3]
        if (isinstance(m, str) and any(c in m for c in "wax+")) or (isinstance(f, int) and f & FL):
            W.append(str(p))
    elif ev in ("os.remove", "os.rename", "os.replace", "os.mkdir", "os.rmdir", "os.truncate", "shutil.rmtree"):
        W.append("%s %s" % (ev, a[:1]))
sys.addaudithook(hook)
script = os.path.abspath(sys.argv[1]); sys.argv = sys.argv[1:]
try:
    runpy.run_path(script, run_name="__main__")
except SystemExit:
    pass
outside = [w for w in W if not os.path.abspath(w.split(" ")[-1].strip("(),'")).startswith(LANE) and not w.startswith("/dev/")]
print("WRITE-AUDIT %s: %d write-opens, %d outside the lane folder %s" % (os.path.basename(script), len(W), len(outside), outside[:10]))
