import re, glob, os
D='notes/_lanes/300/D/sample/'
def body(t):
    if t.startswith('---\n'):
        k=t.find('\n---\n',4); t=t[k+5:] if k>0 else t
    return t
def sh(t,n=8):
    w=re.findall(r'\w+',t.lower()); return set(tuple(w[i:i+n]) for i in range(max(0,len(w)-n+1)))
hooks={int(re.search(r'_lanes/(\d+)/',p).group(1)):open(p,encoding='utf-8',errors='ignore').read() for p in glob.glob('notes/_lanes/*/WRAP-MEMORY-HOOK*.md')}
allhooks='\n'.join(hooks.values())
def cov(a,b):
    A=sh(a); B=sh(b); return (len(A&B)/len(A)) if A else 0, len(A)
for fn in sorted(os.listdir(D)):
    t=body(open(D+fn,encoding='utf-8',errors='ignore').read())
    m=re.match(r'wrap-(\d{3})-',fn)
    tgt={}
    if m:
        n=int(m.group(1))
        if n in hooks: tgt['own hook']=hooks[n]
        h=glob.glob(f'_HANDOFF-*.md')
    tgt['all hooks']=allhooks
    res={k:'%.0f%%'%(100*cov(t,v)[0]) for k,v in tgt.items()}
    print(f'{fn[:60]:60s} 8gram-n={cov(t,allhooks)[1]:5d} {res}')
