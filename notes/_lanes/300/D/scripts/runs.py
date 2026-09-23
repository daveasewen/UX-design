PRJ='/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/'
L=open('snap_18.txt').read().split('\n'); S=set(l.split(' ',1)[0] for l in L[28:178])
store={s.split('\t')[0]:(int(s.split('\t')[1]),s.split('\t')[2]) for s in open('store_listing.tsv').read().strip().split('\n')}
prj=sorted(p for p in store if p.startswith(PRJ))
runs=[];cur=None
for p in prj:
    f=p in S
    if cur and cur[0]==f: cur[2]=p; cur[3]+=1
    else:
        cur=[f,p,p,1]; runs.append(cur)
for f,a,b,n in runs: print('IN ' if f else 'OUT',n,a.replace(PRJ,''),'->',b.replace(PRJ,''))
