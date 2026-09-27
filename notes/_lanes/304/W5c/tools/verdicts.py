#!/usr/bin/env python3
"""verdicts.py LOGDIR — #304 W5c: parse before_*/after_* survey chunk logs into label→verdict, compare BY NAME."""
import re, sys, glob, os, json, hashlib
d = sys.argv[1]
def read(tag):
    V, DET = {}, {}
    for f in sorted(glob.glob(os.path.join(d, tag + "_*.log"))):
        t = open(f, encoding="utf-8").read()
        for m in re.finditer(r"^  (✅|❌|⊘|⏱) \[\s*(\d+)\] (.+?)(?:  (?:exit \d+|COULD-NOT-ASK))?$", t, re.M):
            sym, n, lab = m.groups(); lab = lab.strip()
            V[lab] = {"✅": "pass", "❌": "FAIL", "⊘": "could-not-ask", "⏱": "timeout"}[sym]
        # failure detail blocks: "  [n] label\n      ...detail..." until blank line
        for m in re.finditer(r"^  \[(\d+)\] (.+)\n((?:      .*\n)+)", t, re.M):
            DET[m.group(2).strip()] = hashlib.sha256(re.sub(r"/sessions/\S+", "", m.group(3)).encode()).hexdigest()[:12]
    return V, DET
B, BD = read("before"); A, AD = read("after")
from collections import Counter
print("BEFORE", len(B), dict(Counter(B.values()))); print("AFTER ", len(A), dict(Counter(A.values())))
g2r = [l for l in B if B[l] == "pass" and A.get(l) != "pass"]
r2g = [l for l in B if B[l] != "pass" and A.get(l) == "pass"]
new = [l for l in A if l not in B]; gone = [l for l in B if l not in A]
print("green→red:", g2r); print("red→green:", r2g); print("new steps:", [(l, A[l]) for l in new]); print("gone steps:", gone)
print("non-pass both:", sorted((l[:60], B[l]) for l in B if B[l] != "pass"))
print("detail blocks differ:", [l[:60] for l in BD if l in AD and BD[l] != AD[l]])
json.dump({"before": B, "after": A}, open(os.path.join(d, "verdicts-before-after.json"), "w"), indent=1, ensure_ascii=False)
