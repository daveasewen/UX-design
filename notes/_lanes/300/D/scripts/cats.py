import re,collections
rows=[l.rstrip('\n').split('\t') for l in open('/mnt/user-data/outputs/D-store-census.tsv')][1:]
def cat(r):
    s,p=r[0],r[1]
    if s=='account': return 'account'
    if p=='index.md': return 'index.md'
    if p.startswith('MEMORY-ARCHIVE'): return 'archive-shards'
    if p.startswith('wrap-') and re.match(r'wrap-\d{3}-',p): return 'wrap-NNN'
    if p.startswith('hook-overflow'): return 'hook-overflow'
    if p.startswith('areas/'): return 'areas/'
    if p.startswith('feedback-'): return 'feedback-*'
    return 'topic/ruling notes'
agg=collections.OrderedDict()
for r in rows:
    c=cat(r); a=agg.setdefault(c,[0,0,0,collections.Counter()]); a[0]+=1; a[1]+=int(r[2]); a[2]+=int(r[4]); a[3][r[5] or '-']+=1
for c,(n,b,ins,src) in agg.items(): print(f'{c:20s} files {n:3d} bytes {b:7d} in-boot-listing {ins:3d} src-tags(in listing) {dict(src)}')
print('TOTAL',sum(a[0] for a in agg.values()),sum(a[1] for a in agg.values()))
# updated-date distribution for project files
d=collections.Counter(r[3][:10] for r in rows if r[0]=='project'); print(sorted(d.items()))
