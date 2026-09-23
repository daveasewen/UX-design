import re, tiktoken
enc=tiktoken.get_encoding('cl100k_base')
PRJ='/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/'
L=open('snap_18.txt').read().split('\n')
lst=L[28:178]  # 150 entries
paths=[l.split(' ',1)[0] for l in lst]
print('entries',len(lst),'non-project in listing',sum(1 for p in paths if not p.startswith(PRJ)))
store=[l.split('\t') for l in open('store_listing.tsv').read().strip().split('\n')]
prj=sorted([s[0] for s in store if s[0].startswith(PRJ)])
print('listing == first 150 sorted project paths:', paths==prj[:150])
# which project files are NOT in listing
missing=[p for p in prj if p not in set(paths)]
print('project files not in snapshot listing:',len(missing),'first',missing[0].replace(PRJ,''),'last',missing[-1].replace(PRJ,''))
# is wrap-299 (placed this session) in listing?
print('wrap-299 in listing:', any('wrap-299' in p for p in paths), '| index.md in listing:', any(p.endswith('/index.md') for p in paths))
# per-line token stats
tk=[len(enc.encode(l)) for l in lst]
import statistics
print('per-line cl100k: mean %.1f median %d min %d max %d sum %d'%(statistics.mean(tk),statistics.median(tk),min(tk),max(tk),sum(tk)))
pref=len(enc.encode(PRJ))
print('path prefix tokens',pref,'| x150 =',pref*150)
# token share of components
tags=sum(len(enc.encode(m)) for l in lst for m in re.findall(r' \[sources: [^\]]*\]',l))
alias=sum(len(enc.encode(m)) for l in lst for m in re.findall(r' \[aliases: [^\]]*\]',l))
print('sources-tag tokens',tags,'aliases tokens',alias)
print('lines with [sources: cowork]',sum(1 for l in lst if '[sources: cowork]' in l),'lines with any sources tag',sum(1 for l in lst if '[sources:' in l),'aliases',sum(1 for l in lst if '[aliases:' in l))
srcs=set(m for l in lst for m in re.findall(r'\[sources: ([^\]]*)\]',l)); print('distinct source values',srcs)
desc_chars=[len(l.split(' — ',1)[1]) if ' — ' in l else 0 for l in lst]
print('desc chars: max',max(desc_chars),'ellipsis-truncated lines',sum(1 for l in lst if l.endswith('…')))
