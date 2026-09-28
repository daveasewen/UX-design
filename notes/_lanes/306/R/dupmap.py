#!/usr/bin/env python3
"""306 R: map the facts the #305 wrap wrote in more than one place.
Reads ADDED lines of the wrap commit 81bce363 and 5b eb2630bb per file (git show),
plus the #305 W files written outside git diffs. Read-only."""
import subprocess, re, json, collections, os, sys
os.chdir(os.path.expanduser("~/mnt/Projects--UX-design"))
def added(c):
    out = subprocess.run(["git","--no-optional-locks","show","--format=","--unified=0",c],capture_output=True,text=True).stdout
    per = collections.defaultdict(list); cur=None
    for l in out.splitlines():
        if l.startswith("+++ b/"): cur=l[6:]
        elif l.startswith("+") and not l.startswith("+++") and cur: per[cur].append(l[1:])
    return per
per = collections.defaultdict(list)
for c in ("81bce363","eb2630bb"):
    for k,v in added(c).items(): per[k]+=v
SKIP = re.compile(r"notes/_lanes/305/(C2|C4|K)/|/_work/.*\.(py|sh)$|_ci-|_gitcommit|_push|\.log$|\.term$|t3-rendered|dashboard/|MEMENTO-SCHEMATIC|R1-hub|C4-commit|_graph-|_REHEARSAL|_memento-index|carries_count|paths_w1")
files = {k:"\n".join(v) for k,v in per.items() if not SKIP.search(k)}
for extra in ["notes/_lanes/305/W/SUMMARY-BULLETS.md","notes/_lanes/305/W/_msg-W1.txt","notes/_lanes/305/W/_msg-W5b.txt"]:
    files[extra]=open(extra).read()
def short(p):
    m={"GOOD-MORNING.md":"GM banner","_LIVE-STATE.md":"LS delta","_CHAIN.md":"_CHAIN (gen)","_CARRIES.md":"carries",
       "notes/_GAUGE-LOG.md":"gauge log","knowledge/_state.json":"state rows","_GM-ARCHIVE.md":"GM archive",
       "_LIVE-STATE-ARCHIVE.md":"LS archive","knowledge/_gen_titles_receipt.json":"titles (gen)"}
    if p in m: return m[p]
    if p.startswith("_HANDOFF-156"): return "handoff 156"
    if p.startswith("_HANDOFF-15"): return "addendum "+p[9:12]
    if p.startswith("_DECISION-HISTORY"): return "dossier"
    if "W-wrap.md" in p: return "W report"
    b=os.path.basename(p); return b
FACTS = {
 "headline 'he took the sitting'": r"(?i)he took the sitting|you took the (tuesday )?sitting",
 "rulings total 699": r"\b699\b",
 "rulings delta 638 → 699": r"638\s*(→|->|to)\s*699",
 "newest ruling s305-D61": r"s305-D61|D61\b",
 "40 enacted / 20 ruled": r"\b40\b[^\n]{0,20}(enacted|built)",
 "wrap sha 81bce363": r"81bce363",
 "5b sha eb2630bb": r"eb2630bb",
 "HEAD at open cd16f7ec": r"cd16f7ec",
 "wrap CI run 36404496114": r"36404496114",
 "CI verdict 154 of 154 / 69 pass": r"154 of 154|69 pass",
 "date split line": r"(?i)date split",
 "ritual clock 09:10:17": r"09:10:17",
 "fill at wrap 450,794": r"450,794|451,000",
 "boot 131,040": r"131,040",
 "boot ceiling breach 131,130": r"131,130",
 "sub spend 6,250,083": r"6,250,083",
 "his words 'set in ink'": r"set in ink",
 "his words 'okay go for it'": r"okay go for it",
 "his words 'only designers'": r"(?i)only designers",
 "his words 'images can't be viewed'": r"images can.t be viewed|refused to connect",
 "carries 401": r"\b401\b",
 "12 carries struck": r"(?i)\b(12|twelve)\b[^\n]{0,30}(struck|carries)",
 "next beat: 102 parked questions": r"102 parked",
 "v1.0.14 cut": r"v1\.0\.14",
 "git 2.55 CI cause": r"2\.55",
 "Launchpad": r"Launchpad",
 "kind-5 s212-D1 / s256-D1": r"s212-D1",
}
rows=[]
for fact,rx in FACTS.items():
    hits={short(p):len(re.findall(rx,t)) for p,t in files.items() if re.search(rx,t)}
    rows.append({"fact":fact,"n_files":len(hits),"hits":hits})
rows.sort(key=lambda r:-r["n_files"])
json.dump({"files":{short(p):len(t) for p,t in files.items()},"rows":rows},open("notes/_lanes/306/R/dupmap.json","w"),indent=1)
print("FILES (chars added):"); 
for p,t in sorted(files.items(),key=lambda x:-len(x[1])): print(f"  {len(t):>7}  {short(p)}  [{p}]")
print()
for r in rows: print(f"{r['n_files']:>2}  {r['fact']:<38} "+" · ".join(f"{k}×{v}" for k,v in r['hits'].items()))
