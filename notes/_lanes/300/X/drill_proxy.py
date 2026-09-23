#!/usr/bin/env python3
"""X #300 — mechanical PROXY for the cold-seat drill: does each source CONTAIN the answer?
It is not the drill itself (a model seat is); it bounds what the seat can know without a fetch.
Usage: python3 notes/_lanes/300/X/drill_proxy.py"""
import re,glob
card=open('notes/_lanes/300/C/BOOT-CARD-300-prototype.md').read()
ho=open(sorted(glob.glob('_HANDOFF-150-*.md'))[0]).read()
ch=open('_CHAIN.md').read()
# (question, answer-key regex) — Q1-Q14 from _HANDOFF-150 lines 72-112, Q15-Q18 from _CHAIN.md; keys wording-agnostic across the two
Q=[
 ("Q1 session number + chat title", r"#300: the ask on slide 15"),
 ("Q2 status of the ask: still stamped DRAFT, Friday two days out", r"(stamped|still) DRAFT"),
 ("Q3 has he ruled WHEN the demo brief comes (last)", r"do that last|demo brief \(last\)"),
 ("Q4 which drawing did he rule to -27 (only 09)", r"ruled only on 09|ruled on 09 only"),
 ("Q5 how to push (plain git push; --push arm runs git status)", r"plain `?git push"),
 ("Q6 what _git_commit.sh needs (SESSION_N=300)", r"SESSION_N=300"),
 ("Q7 stranded index.lock: where to move it", r"_orphan-locks"),
 ("Q8 which deck build never to run (build_e.py)", r"never `?build_e\.py"),
 ("Q9 where the rail labels are set (build_c.py)", r"rail labels are in `?build_c\.py"),
 ("Q10 #299 wrap commit + path", r"f8321215"),
 ("Q11 his ruling on the chain (REJECTED dropping it)", r"REJECTED dropping it"),
 ("Q12 paths dirty by declaration (do not clean)", r"dirty by declaration"),
 ("Q13 _state.add refuses a row whose home does not exist", r"refuses a row whose `?home"),
 ("Q14 demo brief source file (HSBC grill source)", r"GRILL-SOURCE-2026-09-18"),
 ("Q15 how many open items are his (415)", r"415 Dave"),
 ("Q16 lane R's reconciliation (42 decided, 40 enacted)", r"42 decided"),
 ("Q17 #299 boot reading (126,178)", r"126,178"),
 ("Q18 retrieval door named (_memento_search.py)", r"_memento_search\.py"),
]
print("%-62s %5s %8s %6s"%("question","card","handoff","chain"))
tot=[0,0,0]
for q,k in Q:
    r=[bool(re.search(k,s)) for s in (card,ho,ch)]
    for i,x in enumerate(r): tot[i]+=x
    print("%-62s %5s %8s %6s"%(q,*['yes' if x else '-' for x in r]))
print("TOTAL of %d: card %d · handoff %d · chain %d · card+chain %d"%(len(Q),tot[0],tot[1],tot[2],
      sum(1 for q,k in Q if re.search(k,card) or re.search(k,ch))))
