#!/usr/bin/env python3
"""306 R: characters of hand-written wrap prose per wrap (#303-#305), from the added lines of the wrap + 5b
commits, by destination. Excludes: moved text (GM/LS archives, gauge log), generated files (_CHAIN, index,
titles receipt, mention map), other lanes' tails, the ops/staging vehicles, scripts and logs.
_CARRIES.md is shown apart: its new section is written by the seat's carries script, mostly a copy of
the previous section with ages bumped."""
import subprocess, collections, os, re
os.chdir(os.path.expanduser("~/mnt/Projects--UX-design"))
W={303:("efe3bb47","571d458c"),304:("9f9ff879","7cae0189"),305:("81bce363","eb2630bb")}
def added(c):
    out=subprocess.run(["git","--no-optional-locks","show","--format=","--unified=0",c],capture_output=True,text=True).stdout
    per=collections.Counter(); cur=None
    for l in out.splitlines():
        if l.startswith("+++ b/"): cur=l[6:]
        elif l.startswith("+") and not l.startswith("+++") and cur: per[cur]+=len(l)
    return per
def cat(p,n):
    if p=="GOOD-MORNING.md": return "banner + stratum (GOOD-MORNING)"
    if p=="_LIVE-STATE.md": return "delta + stamp (LIVE-STATE)"
    if p.startswith("_HANDOFF-"): return "handoff + old-handoff addenda"
    if p.startswith("_DECISION-HISTORY/"): return "dossier"
    if re.search(rf"_subreports/.*-{n}-W-wrap",p): return "wrap report"
    if p.endswith("WRAP-MEMORY-HOOK.md") or "/_work/memory_" in p: return "memory note (hook + payloads)"
    if p.endswith("NARRATIVE.md"): return "narrative"
    if p=="knowledge/_state.json": return "state rows"
    if p=="knowledge/_REVIEW-SIGNOFF.md": return "sign-off register"
    if p=="_CARRIES.md": return "CARRIES (scripted copy-forward)"
    return None
for n,cs in W.items():
    tot=collections.Counter()
    for c in cs:
        for p,v in added(c).items():
            k=cat(p,n)
            if k: tot[k]+=v
    for m in (f"notes/_lanes/{n}/W/_msg-W1.txt",f"notes/_lanes/{n}/W/_msg-W5b.txt"):
        tot["commit messages"]+=len(open(m).read())
    sb=f"notes/_lanes/{n}/W/SUMMARY-BULLETS.md"
    if os.path.exists(sb): tot["summary bullets"]+=len(open(sb).read())
    hand=sum(v for k,v in tot.items() if not k.startswith("CARRIES"))
    print(f"#{n}: hand-written prose {hand:,} chars (~{hand/3.53:,.0f} tokens at 3.53 chars/token) · carries copy-forward {tot['CARRIES (scripted copy-forward)']:,} chars")
    for k,v in tot.most_common(): print(f"    {v:>8,}  {k}")
