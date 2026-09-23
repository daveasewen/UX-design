import tiktoken, re
enc=tiktoken.get_encoding('cl100k_base')
def tk(s): return len(enc.encode(s, disallowed_special=()))
PRJ='/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/'
L=open('snap_18.txt').read().split('\n')
head='\n'.join(L[0:27])+'\n'+L[27]   # preamble+profile+preferences+<memory_listing>+header line
tail=L[179]+'\n'+L[180]
lines={l.split(' ',1)[0]:l for l in L[28:178]}
rows=[l.rstrip('\n').split('\t') for l in open('/mnt/user-data/outputs/D-store-census-v2.tsv')][1:]
prev={((PRJ+r[1]) if r[0]=='project' else r[1]):r[8] for r in rows}
# average description-token ratio listing(160ch) vs preview(80ch) from files present in both
ratios=[]
for p,l in lines.items():
    d=l.split(' — ',1)[1] if ' — ' in l else ''
    pv=prev.get(p,'')
    if d and pv and pv.endswith('…') and d.endswith('…'): ratios.append(tk(d)/max(1,tk(pv)))
k=sum(ratios)/len(ratios); print('listing-desc/preview token ratio (truncated both) mean %.2f n=%d'%(k,len(ratios)))
def est_line(p,tag=''):
    if p in lines: return tk(lines[p])
    pv=prev[p]; d=tk(pv)*(k if pv.endswith('…') else 1.0)
    return tk(p+tag+' — ')+round(d)
fixed=tk(head+'\n'+tail); print('fixed part (preamble+profile+preferences+listing frame) cl100k',fixed, '| full snapshot now',tk('\n'.join(L)))
five=[PRJ+'index.md',PRJ+'MEMORY-ARCHIVE-3.md',PRJ+'areas/presentation-friday-25th-288.md',PRJ+'memory-brain-is-the-repo-278.md',PRJ+'wrap-299-his-last-changes-are-in-the-deck-and-the-ask-is-what-is-left.md']
fl=[est_line(p) for p in five]; print('five candidate lines',fl,'sum',sum(fl))
acc=[r[1] for r in rows if r[0]=='account' and r[1] not in('/profile.md','/preferences.md')]
al=[est_line(p) for p in acc]; print('14 account lines est',sum(al),'mean %.0f'%(sum(al)/len(al)))
one=[PRJ+'index.md']
for name,ls in [('store cut to 5 project files',fl),('5 files + 14 account lines if they surface',fl+al),('1 pointer file',[est_line(one[0])]),('project subtree emptied, account lines hidden',[]),('project subtree emptied, 14 account lines surface',al)]:
    t=fixed+sum(ls)+len(ls)
    print(f'{name:48s} cl100k {t:6d}  real@1.531 {t*1.531:7.0f}  real@1.634 {t*1.634:7.0f}')
now=tk('\n'.join(L)); print(f"{'NOW (150 lines + truncation line)':48s} cl100k {now:6d}  real@1.531 {now*1.531:7.0f}  real@1.634 {now*1.634:7.0f}")
# what a full (uncapped) listing would cost: 234 project lines est
allp=[p for p in prev if p.startswith(PRJ)]
tot=fixed+sum(est_line(p) for p in allp)+len(allp)
print('hypothetical uncapped listing of all 234 project files cl100k',tot)
