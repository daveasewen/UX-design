#!/usr/bin/env python3
"""Build notes/_SITTING-307-reopened-78-2026-09-28-v1.html from cards-*.txt.
CSS and chrome copied from the approved check page; checks every card against lane S's
check file and every quote against knowledge/_rulings.json. Run from the repo root."""
import json, re, html, sys, collections
A='notes/_lanes/307/A/'
SRC='notes/_CHECK-306-parked-superseded-2026-09-28-v1.html'
OUT='notes/_SITTING-307-reopened-78-2026-09-28-v1.html'
chk={r['id']:r for r in json.load(open('notes/_lanes/306/S/parked-102-check.json'))}
RUL={x['id']:x for x in json.load(open('knowledge/_rulings.json'))['rulings']}
themes=[]; cards=[]; cur=None
for fn in ['cards-1.txt','cards-2.txt','cards-3.txt']:
    for line in open(A+fn, encoding='utf-8'):
        line=line.rstrip('\n')
        if not line.strip(): continue
        if line.startswith('# '):
            k,n,i=[s.strip() for s in line[2:].split('|')]
            themes.append({'k':k,'n':n,'i':i,'ids':[]}); continue
        if line.startswith('@ '):
            cur={'id':line[2:].strip(),'t':themes[-1]['k'],'opts':[]}; cards.append(cur); themes[-1]['ids'].append(cur['id']); continue
        m=re.match(r'^([*-]) ([a-d]): (.*)$',line)
        if m:
            cur['opts'].append((m.group(2),m.group(3)))
            if m.group(1)=='*': cur['rec']=m.group(2)
            continue
        m=re.match(r'^([A-Z]): (.*)$',line)
        if not m: sys.exit('bad line: '+line)
        cur[m.group(1)]=m.group(2)
# ---- checks
errs=[]
ids=[c['id'] for c in cards]
want={i for i,r in chk.items() if r['verdict']!='SUPERSEDED'}
dup=[i for i,n in collections.Counter(ids).items() if n>1]
if dup: errs.append('dup '+str(dup))
if set(ids)!=want: errs.append('set mismatch: extra %s missing %s'%(set(ids)-want, want-set(ids)))
for c in cards:
    r=chk[c['id']]; c['v']=r['verdict']; c['by']=r['by']; c['op']=r['opened']
    if 'rec' not in c: errs.append(c['id']+' no rec')
    if c['v'] in ('PARTLY','UNSURE') and not ('S' in c and 'O' in c): errs.append(c['id']+' missing S/O')
    if c['v']=='LIVE' and 'C' not in c: errs.append(c['id']+' missing C')
    if 'X' in c:
        kind,rid=c['K'].split()
        c['qk'],c['qr']=kind,rid
        t=RUL[rid]['ruled']+' '+RUL[rid]['says']
        if c['X'] not in t: errs.append(c['id']+' quote not verbatim in '+rid)
if errs: print('\n'.join(errs)); sys.exit(1)
E=lambda s: html.escape(s, quote=True)
VK={'PARTLY':'Partly settled','UNSURE':'Likely settled','LIVE':'Still open'}
VN={'PARTLY':'partly answered','UNSURE':'unsure','LIVE':'still live'}
def quote(c):
    if 'X' not in c: return ''
    who='your words' if c['qk']=='d' else "the record's words"
    if c.get('Y'): who+=', '+c['Y']
    return '<br><span class="qt">“%s”</span><span class="qs">%s</span>'%(E(c['X']),who)
def card(c):
    v=c['v']; kind=VK[v]
    if c.get('N'): kind='Newly settled'
    h=['<li class="pr v-%s" id="c-%s" data-id="%s" data-t="%s" data-rec="%s">'%(v.lower(),E(c['id']),E(c['id']),c['t'],c['rec']),
       '<p class="kind"><span class="kl">%s</span><span class="ka">Answered</span></p><div>'%kind,
       '<p class="qq">%s</p>'%E(c['Q'])]
    if v=='PARTLY':
        h.append('<p class="by"><span class="k">Already settled</span> %s%s</p>'%(E(c['S']),quote(c)))
        h.append('<p class="left"><span class="k">Still open</span> %s</p>'%E(c['O']))
    elif v=='UNSURE':
        h.append('<p class="by"><span class="k">Likely settled by</span> %s%s</p>'%(E(c['S']),quote(c)))
        h.append('<p class="left"><span class="k">Unless</span> %s</p>'%E(c['O']))
    else:
        if c.get('N'):
            h.append('<p class="by v-new"><span class="k">Newly settled</span> %s%s</p>'%(E(c['N']),quote(c)))
        h.append('<p class="nt">%s</p>'%E(c['C']))
    w=c['W'][0].upper()+c['W'][1:]
    h.append('<p class="rec"><span class="k">Why we recommend it</span> %s</p>'%E(w))
    h.append('<div class="opts" data-q="%s">'%E(c['id']))
    for k,l in c['opts']:
        tag='<span class="rt">Recommended</span>' if k==c['rec'] else ''
        h.append('<button type="button" class="opt" data-a="%s">%s%s</button>'%(k,E(l),tag))
    h.append('</div><textarea class="cn" data-g="%s" placeholder="Your note, if any" aria-label="Your note on this question"></textarea>'%E(c['id']))
    rul=', '.join(c['by']+([c['qr']] if c.get('qr') and c['qr'] not in c['by'] else []))
    h.append('<p class="rid">%s · %s · opened at #%s · lane S: %s</p></div></li>'%(E(c['id']), ('rulings '+rul) if rul else 'no ruling', c['op'], VN[v]))
    return ''.join(h)
src=open(SRC,encoding='utf-8').read()
css=src[src.index('<style>')+7:src.index('</style>')]
css=css.replace('<title>Parked questions checked</title>','')
css+='''
.pr .kind{margin:0;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);line-height:1.5;padding-top:3px}
.pr .kind .ka{display:none}
.pr.done{box-shadow:inset 3px 0 0 var(--accent);padding-left:10px}
.pr.done .kind .kl{display:none}.pr.done .kind .ka{display:inline;color:var(--accent);font-weight:500}
.v-partly .by .k,.v-unsure .by .k,.v-new .k{color:var(--ok)}
.qs{font-size:12px;color:var(--ink-3);margin-left:8px}
.rec{margin:12px 0 8px;font-size:15px;line-height:1.5}
.rec .k{color:var(--accent)}
.opts{display:flex;flex-direction:column;align-items:flex-start;gap:6px;margin:0 0 8px}
.opt{font:inherit;font-size:14px;line-height:1.45;text-align:left;padding:7px 12px;border:1px solid var(--rule);background:transparent;color:var(--ink);cursor:pointer;border-radius:0;max-width:100%}
.opt:hover{border-color:var(--ink)}
.opt.on{background:var(--ink);color:var(--ground);border-color:var(--ink)}
.opt .rt{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-left:10px;white-space:nowrap}
.opt.on .rt{color:inherit;opacity:.7}
textarea.cn{min-height:44px;font-size:14px;padding:8px 10px;margin:0 0 6px;display:block}
.tk{display:flex;gap:1rem;align-items:center;flex-wrap:wrap;margin:0 0 1.25rem}
.tcount{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);line-height:1.5}
.dec a{color:inherit}
'''
n=len(cards); cnt=collections.Counter(c['v'] for c in cards)
parts=['<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n<title>The 78 reopened questions</title>\n<style>',css,'</style></head>\n<body><a id="rv-back" href="../index.html" target="_self">&larr; All review pages</a>\n']
parts.append('<header><div class="wrap">\n<p class="label">Apollo · sitting page · session 307 · Monday 28 September</p>\n<h1>The 78 reopened questions</h1>\n<p class="sub">Grouped by theme. Where a ruling of yours already settles part of a question, it is shown, so you rule only on what is left. Every card carries a recommendation.</p>\n<div class="tally">\n<a href="#how"><b id="tl-done">0</b><span>Answered of %d</span></a>\n<a href="#how"><b>%d</b><span>Partly settled</span></a>\n<a href="#how"><b>%d</b><span>Likely settled</span></a>\n<a href="#how"><b>%d</b><span>Still open</span></a>\n</div></div></header>\n'%(n,cnt['PARTLY'],cnt['UNSURE'],cnt['LIVE']))
parts.append('<section class="grey" id="how"><div class="wrap">\n<p class="label">How this sitting works</p><h2>Ten themes, quickest first</h2>\n<p class="sd">The themes run from the quickest to settle to the ones that most need your eye. The first four are mostly old machinery that can close in a click. The last six are design calls: colours, sizes, parts, charts and the dashboard.</p>\n<ol class="dec">')
for i,t in enumerate(themes):
    parts.append('<li><div><b><a href="#t-%s">%s</a></b><p>%d questions. %s</p></div></li>'%(t['k'],E(t['n']),len(t['ids']),E(t['i'])))
parts.append('</ol>\n<div class="tk"><button type="button" class="chip" id="take-page">Take all recommendations</button><span class="tcount">Fills every card you have not answered. You can change any of them.</span></div>\n</div></section>\n')
byid={c['id']:c for c in cards}
for i,t in enumerate(themes):
    parts.append('<section id="t-%s"><div class="wrap"><p class="label">Theme %d of %d · %d questions</p><h2>%s</h2><p class="sd">%s</p>'%(t['k'],i+1,len(themes),len(t['ids']),E(t['n']),E(t['i'])))
    parts.append('<div class="tk"><button type="button" class="chip take" data-t="%s">Take all recommendations in this theme</button><span class="tcount" data-t="%s"></span></div><ol class="rows">'%(t['k'],t['k']))
    parts.extend(card(byid[x]) for x in t['ids'])
    parts.append('</ol></div></section>\n')
parts.append('<section class="grey"><div class="wrap"><p class="label">Last</p><h2>Anything else</h2><label><span class="k">In your words</span><textarea data-g="page" placeholder="Optional."></textarea></label></div></section>\n')
parts.append('<footer><div class="wrap">Built from lane S\'s check at #306 (notes/_lanes/306/S/parked-102-check.json) and knowledge/_rulings.json (%d rulings, newest s306-D10). The 78 are the rows you kept open at #306; all 78 are open in the store. Every quote was checked word for word against the ruling it names. Record: notes/_subreports/2026-09-28-307-A-sitting-78.md.</div></footer>\n'%len(RUL))
rows={c['id']:{'q':c['Q'],'v':c['v'],'s':c['op'],'t':c['t'],'rec':c['rec'],'o':dict(c['opts'])} for c in cards}
th=[{'k':t['k'],'n':t['n'],'ids':t['ids']} for t in themes]
js=open(A+'page.js',encoding='utf-8').read()
js=js.replace('__ROWS__',json.dumps(rows,ensure_ascii=False)).replace('__THEMES__',json.dumps(th,ensure_ascii=False))
parts.append('<script>\n'+js+'\n</script>\n</body></html>\n')
open(OUT,'w',encoding='utf-8').write(''.join(parts))
print('wrote',OUT,n,'cards',dict(cnt),[(t['n'],len(t['ids'])) for t in themes])
