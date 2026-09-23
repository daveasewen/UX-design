# Build fixed-string needles from each PROJECT store file's preview line (description or first body line).
import re
W='notes/_lanes/300/D/'
rows=[l.rstrip('\n').split('\t') for l in open(W+'store-census.tsv')]
hdr=rows[0]; rows=rows[1:]
out=[]
for r in rows:
    if r[0]!='project': continue
    p=r[-1]
    s=p.replace('\\"','"').rstrip('…').strip()
    if s.startswith('"'): s=s[1:]
    s=re.sub(r'^[\s★⛔✅#\-\*]+','',s).strip()
    # take the first 48 chars on a word boundary-ish
    n=s[:48]
    if len(n)<24: n=s  # short previews stay whole
    out.append((r[1],n))
open(W+'needles.txt','w').write('\n'.join(n for _,n in out)+'\n')
open(W+'needles-map.tsv','w').write('\n'.join(f'{a}\t{b}' for a,b in out)+'\n')
print('needles',len(out),'shortest',min(len(n) for _,n in out))
