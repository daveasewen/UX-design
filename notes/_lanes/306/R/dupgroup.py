#!/usr/bin/env python3
"""306 R: fold dupmap.json into reader-facing destinations. Staging vehicles (ops json, delta/stratum txt,
signoff_row) are dropped because they are copied into GM/LS/signoff; WRAP-BRIEF is the conductor's input.
GM archive / LS archive / gauge log are dropped too: 2c/2d/2f MOVE earlier sessions' text there, so a hit is an old line, not a new write."""
import json, os
os.chdir(os.path.expanduser("~/mnt/Projects--UX-design"))
d=json.load(open("notes/_lanes/306/R/dupmap.json"))
DROP=lambda k: k.startswith("_ops-") or k in ("GM archive","LS archive","gauge log","delta_305.txt","stratum_305.txt","signoff_row.txt","sizes_305.txt","preflight_305.txt","WRAP-BRIEF.md","step6-parse.txt")
def grp(k):
    if k.startswith("memory_") or k=="WRAP-MEMORY-HOOK.md": return "memory note"
    if k.startswith("_msg-"): return "commit messages"
    if k.startswith("addendum"): return "old-handoff addenda"
    return {"NARRATIVE.md":"narrative","SUMMARY-BULLETS.md":"summary bullets","_REVIEW-SIGNOFF.md":"sign-off register"}.get(k,k)
GEN={"_CHAIN (gen)","titles (gen)"}
out=[]
for r in d["rows"]:
    g={}
    for k,v in r["hits"].items():
        if DROP(k): continue
        g[grp(k)]=g.get(grp(k),0)+v
    hand=[k for k in g if k not in GEN]; gen=[k for k in g if k in GEN]
    out.append((r["fact"],len(hand),len(gen),sum(g.values()),sorted(hand),gen))
out.sort(key=lambda x:(-x[1],-x[3]))
tot_h=sum(x[1] for x in out); 
for f,h,gn,occ,hl,gl in out: print(f"{h:>2} hand · {gn} gen · {occ:>3} occurrences  {f:<38} {', '.join(hl)}" + (f"  [+gen: {', '.join(gl)}]" if gl else ""))
print("facts:",len(out)," mean hand-written homes per fact:",round(tot_h/len(out),1)," facts in 5+ hand homes:",sum(1 for x in out if x[1]>=5))
json.dump(out,open("notes/_lanes/306/R/dupgroup.json","w"),indent=0)
