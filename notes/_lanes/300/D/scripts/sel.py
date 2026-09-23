PRJ='/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/'
L=open('snap_18.txt').read().split('\n')
lst=L[28:178]
paths=[l.split(' ',1)[0] for l in lst]
S=set(paths)
store={s.split('\t')[0]:(int(s.split('\t')[1]),s.split('\t')[2]) for s in open('store_listing.tsv').read().strip().split('\n')}
prj={p:v for p,v in store.items() if p.startswith(PRJ)}
inc={p:v for p,v in prj.items() if p in S}; exc={p:v for p,v in prj.items() if p not in S}
print('in listing but not in store:',[p for p in paths if p not in store])
def rng(d): 
    us=sorted(v[1] for v in d.values()); bs=sorted(v[0] for v in d.values()); return us[0][:19],us[-1][:19],bs[0],bs[-1]
print('included: date min/max, bytes min/max',rng(inc))
print('excluded: date min/max, bytes min/max',rng(exc))
# display order check: is listing order sorted?
print('listing displayed sorted?',paths==sorted(paths))
# order by updated desc?
byrec=sorted(prj,key=lambda p:prj[p][1],reverse=True)
print('included == 150 most recent?', set(byrec[:150])==S)
# excluded names short
ex=sorted(p.replace(PRJ,'') for p in exc)
print('excluded (first 12):',ex[:12]); print('excluded (last 12):',ex[-12:])
# position of excluded in sorted order
srt=sorted(prj)
pos=[srt.index(p) for p in exc]
print('excluded sorted positions min',min(pos),'max',max(pos))
import collections
print('excluded by first letter',collections.Counter(p.replace(PRJ,'')[0] for p in exc))
print('included by first letter',collections.Counter(p.replace(PRJ,'')[0] for p in inc))
