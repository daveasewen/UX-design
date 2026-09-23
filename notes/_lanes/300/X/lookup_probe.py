#!/usr/bin/env python3
"""X #300 — does a LOOK-UP find the answer a lean opener dropped?  Read-only.
Compares hit@3 of (a) today's _search_core ranking over the Memento index, (b) the same with the
newest handoff + _CHAIN.md cut into '##' sections and added, (c) BM25 (unigram+bigram) over (b).
Usage: python3 notes/_lanes/300/X/lookup_probe.py"""
import json,re,glob,math,sys,collections
sys.path.insert(0,'knowledge'); import _search_core as core
Q=[("what session is this and what is the chat title",r"#300: the ask on slide 15"),
("status of the ask on slide 15 before friday",r"(stamped|still) DRAFT"),
("when does the demo brief come",r"do that last|demo brief \(last\)"),
("which drawings rest at -27 and what did he rule",r"ruled only on 09|ruled on 09 only"),
("how do I push to github",r"plain `?git push"),
("what does _git_commit.sh need before a commit",r"SESSION_N=300"),
("stranded index.lock what do I do",r"_orphan-locks"),
("which deck build script must never be run",r"never `?build_e\.py|Never run `?notes/_lanes/296/E/build_e\.py"),
("where are the rail chapter labels set",r"rail labels are in `?build_c\.py|rail's chapter titles live in `?build_c"),
("what was the 299 wrap commit",r"f8321215"),
("Dave's ruling on the chain",r"REJECTED dropping it"),
("which paths are dirty by declaration",r"dirty by declaration"),
("_state.add refuses a row",r"refuses a row whose `?home"),
("demo brief source file",r"GRILL-SOURCE-2026-09-18"),
("how many open items are Dave's",r"415 Dave"),
("lane R reconciliation of his decided changes",r"42 decided"),
("boot reading at 299",r"126,178"),
("what is the retrieval door",r"_memento_search\.py")]
idx=json.load(open('knowledge/_memento-index.json'))['records']
def sections(path,kind):
    s=open(path).read(); parts=re.split(r'(?m)^(?=## )',s); out=[]
    for i,p in enumerate(parts):
        head=p.splitlines()[0][:80] if p.strip() else ''
        out.append({'id':f'{kind}:{i}','kind':kind,'file':path,'head':head,'text':p})
    return out
extra=sections(sorted(glob.glob('_HANDOFF-150-*.md'))[0],'handoff-section')+sections('_CHAIN.md','chain-section')
lex=json.load(open('knowledge/_consult-lexicon.json'))
def core_top(recs,q,k=3):
    b,_,_,_=core.search(recs,q,lex,lambda r:'all',{'all':k})
    return b.get('all',[])[:k]
def toks(s):
    t=core.tokenize(s); return t+[a+'_'+b for a,b in zip(t,t[1:])]
def bm25_build(recs):
    docs=[toks(core.record_blob(r)) for r in recs]; N=len(docs); avg=sum(map(len,docs))/N
    df=collections.Counter(); [df.update(set(d)) for d in docs]
    tf=[collections.Counter(d) for d in docs]; return docs,N,avg,df,tf
def bm25_top(recs,model,q,k=3,k1=1.2,b=0.75):
    docs,N,avg,df,tf=model; qt=toks(q); sc=[]
    for i,d in enumerate(docs):
        s=0.0
        for t in qt:
            if t in tf[i]:
                idf=math.log(1+(N-df[t]+0.5)/(df[t]+0.5)); f=tf[i][t]
                s+=idf*f*(k1+1)/(f+k1*(1-b+b*len(d)/avg))
        if s>0: sc.append((s,i))
    sc.sort(reverse=True); return [recs[i] for s,i in sc[:k]]
full=idx+extra; model=bm25_build(full)
res={'core(index only)':0,'core(+handoff,+chain)':0,'bm25(+handoff,+chain)':0}
rows=[]
for q,key in Q:
    a=any(re.search(key,r.get('text','')+r.get('head','')) for r in core_top(idx,q))
    b_=any(re.search(key,r.get('text','')+r.get('head','')) for r in core_top(full,q))
    c=any(re.search(key,r.get('text','')+r.get('head','')) for r in bm25_top(full,model,q))
    res['core(index only)']+=a; res['core(+handoff,+chain)']+=b_; res['bm25(+handoff,+chain)']+=c
    rows.append((q[:48],a,b_,c))
for r in rows: print('%-50s core:%s core+:%s bm25+:%s'%(r[0],*['Y' if x else '-' for x in r[1:]]))
print('hit@3 of %d:'%len(Q),res, '| index records',len(idx),'+ sections',len(extra))
