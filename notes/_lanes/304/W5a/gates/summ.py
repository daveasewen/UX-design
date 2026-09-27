import re,glob,os,collections
for T in ('before','after'):
    print('=====',T)
    for r in (1,2,3):
        rc=collections.Counter(); pages=0; fails=0
        for f in sorted(glob.glob('g-%s/receipt-c2r%d-*.txt'%(T,r))):
            s=open(f).read(); pages+=1
            codes=set(re.findall(r'FAIL:([A-Z-]+) —',s))
            if 'RESULT: FAIL' in s: fails+=1
            for c in codes: rc[c]+=1
        s=open('g-%s/screen-c2r%d.txt'%(T,r)).read()
        st=collections.Counter()
        for step in ('receipt','compose','composition','icon-source','a11y'):
            for m in re.finditer(r'^- %s: (.)'%step,s,re.M): st[(step,m.group(1))]+=1
        print('c2r%d receipt: %d/%d pages FAIL; pages per code %s'%(r,fails,pages,dict(rc)))
        print('      screen:',' '.join('%s%s=%d'%(k[0],k[1],v) for k,v in sorted(st.items())), '| RESULT FAIL' if 'RESULT: FAIL' in s else '| RESULT PASS')
