#!/usr/bin/env python3
"""#264 — second-pass review page (two-body class). Generated from 264-active-gen2.json; do not hand-edit."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "..", "..")
r = json.load(open(os.path.join(HERE, "264-active-gen2.json"))); r1 = json.load(open(os.path.join(HERE, "264-active-gen.json")))
CAL = [n for n in r if r[n]["real"]]; NEW = [n for n in r if not r[n]["real"]]
NOTE = {"balance-transfer": "the whole card should be filled not just the top, but the overlap exclusion are need to be kept",
        "tax": "the document icon half should be filled, if you look at teh document icon as a guide",
        "workspace": "we have to fill teh otehr part of teh icon too", "digital-statements": "need both parts filled",
        "global-money": "thsi is quite ahard one to get right"}
def sym(sid, svg): return f'<symbol id="{sid}" viewBox="0 0 18 18">{re.sub(r"^.*?<svg[^>]*>", "", svg, flags=re.S).replace("</svg>", "").strip()}</symbol>'
symbols = []
for n, v in r.items():
    symbols += [sym(f'{n}-line', v['line']), sym(f'{n}-v2', v['a'])]
    if v['real']: symbols.append(sym(f'{n}-real', v['real']))
    if n in r1: symbols.append(sym(f'{n}-v1', r1[n]['a1']))
def ic(sid, big=False): return f'<svg class="{"big" if big else ""}" viewBox="0 0 18 18"><use href="#{sid}"/></svg>'
def navrow(theme, n, sid):
    label = n.replace('-', ' ').capitalize()
    return (f'<div class="sn" data-theme="{theme}"><a class="nv-item" href="#"><span class="nv-ic">{ic(n+"-line")}</span><span class="nv-label">{label}</span></a>'
            f'<a class="nv-item" href="#" aria-current="page"><span class="nv-ic">{ic(sid)}</span><span class="nv-label">{label}</span></a></div>')
def block(i, n):
    v1 = f'<div><span class="cap">v1 · rejected</span>{ic(n+"-v1",1)}</div>' if n in r1 else ''
    return f'''<section class="cand"><div class="ch"><span class="idx">{i:02d}</span><div><h3>{n}</h3><p class="q">“{NOTE.get(n,"")}”</p></div>
    <div class="trio"><div><span class="cap">line</span>{ic(n+"-line",1)}</div>{v1}<div><span class="cap">v2</span>{ic(n+"-v2",1)}</div></div></div>
    <div class="panels">{navrow("light",n,n+"-v2")}{navrow("dark",n,n+"-v2")}</div>
    <div class="grade"><span class="cap">grade</span> <label><input type="radio" name="{n}" value="accept">accept</label> <label><input type="radio" name="{n}" value="reject">reject</label> <input class="note" placeholder="note" data-for="{n}"></div></section>'''
cal = ''.join(f'<tr><td class="nm">{n}</td><td>{ic(n+"-line",1)}</td><td>{ic(n+"-real",1)}</td><td>{ic(n+"-v2",1)}</td></tr>' for n in CAL)
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>#264 · Active-glyph experiment, second pass</title>
<style>
:root{{--accent:#DB0011;--g1:#F3F3F3;--g2:#EDEDED;--g3:#D7D8D6;--g6:#767676;--g8:#333333;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem}}
*{{box-sizing:border-box}} body{{margin:0;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;color:#000;background:#fff;font-size:16px;line-height:1.7}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 var(--s4)}} header{{padding:var(--s5) 0 var(--s4);border-bottom:1px solid var(--g2)}}
.label{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:8px;margin:0 0 var(--s2)}} .label::before{{content:'';width:20px;height:1px;background:var(--accent)}}
h1{{font-size:34px;font-weight:400;line-height:1.15;margin:0 0 var(--s2);letter-spacing:-.01em}} h2{{font-size:19px;font-weight:500;margin:0 0 var(--s2)}} h3{{font-size:19px;font-weight:500;margin:0}}
p{{margin:0 0 var(--s2)}} .lede{{max-width:66ch}} code{{font-family:Menlo,monospace;font-size:13px}} .q{{font-size:14px;color:var(--g6);margin:0}}
.rule{{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);padding:var(--s5) 0;border-bottom:1px solid var(--g2)}} pre{{font:13px/1.6 Menlo,monospace;background:var(--g1);padding:var(--s2);margin:0;overflow-x:auto}}
table{{border-collapse:collapse;margin:var(--s2) 0}} th,td{{text-align:center;padding:6px 18px;border-bottom:1px solid var(--g2)}} th{{font-weight:500;color:var(--g6);font-size:12px;letter-spacing:.08em;text-transform:uppercase}} td.nm{{text-align:left;font-size:14px}}
svg{{width:18px;height:18px;fill:#1A1A1A;color:#1A1A1A}} svg.big{{width:40px;height:40px}}
.cand{{padding:var(--s4) 0;border-bottom:1px solid var(--g2)}} .ch{{display:flex;gap:var(--s3);align-items:center;margin-bottom:var(--s3)}} .idx{{font-size:43px;font-weight:200;line-height:1;color:var(--g3);min-width:56px}}
.trio{{display:flex;gap:var(--s4);margin-left:auto}} .trio div{{display:flex;flex-direction:column;align-items:center;gap:4px}} .cap{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6)}}
.panels{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--g2);margin-bottom:var(--s2)}} .grade{{font-size:14px;display:flex;gap:var(--s2);align-items:center}} .note{{border:0;border-bottom:1px solid var(--g3);font:inherit;padding:2px 0;flex:1}}
.sn{{--nav-row:44px;padding:4px 0}} .sn[data-theme=light]{{--nav-surface:#FFF;--nav-text:#1A1A1A;--nav-icon:#1A1A1A;background:var(--nav-surface)}} .sn[data-theme=dark]{{--nav-surface:#1F1F1F;--nav-text:#FFF;--nav-icon:#FFF;background:var(--nav-surface)}}
.nv-item{{display:flex;align-items:center;gap:12px;min-height:var(--nav-row);padding:0 16px;color:var(--nav-text);text-decoration:none;font-size:15px}} .nv-ic{{display:inline-flex;width:18px;height:18px;color:var(--nav-icon)}} .nv-ic svg{{fill:currentColor;color:inherit}}
.nv-item[aria-current=page]{{box-shadow:inset 3px 0 0 #DB0011}} .nv-item[aria-current=page] .nv-label{{font-weight:500}}
#export{{margin:var(--s4) 0;font:13px/1.6 Menlo,monospace;background:var(--g1);padding:var(--s2);white-space:pre-wrap;min-height:3em}} footer{{padding:var(--s4) 0 var(--s6);font-size:14px;color:var(--g6)}}
</style></head><body><svg width="0" height="0" style="position:absolute">{"".join(symbols)}</svg><div class="wrap">
<header><p class="label">#264 · experiment · second pass</p><h1>The five you rejected were one class. Four of them now fill; the fifth is still hard.</h1>
<p class="lede">Your notes all said the same thing — the second body was not filled. The cause was mechanical: a rear body cut by a front one has no closed outline, so "fill every contour" filled only the front. The second pass finds the silhouette the other way round: it is whatever the outside cannot reach once the front body is grown by the width of the exclusion gap. The gap you asked to keep is kept by construction.</p></header>
<section class="rule"><div><h2>The rule, revised</h2><p class="q">Front bodies are found, not declared: every closed ring is tried, and the ones whose sealing gains silhouette area are fronts. Open bodies (a shoulder line) close across their opening.</p></div>
<pre>front  = rings whose sealing GAINS area (the rear gains; the front never does)
seal   = L ∪ grow(frontSil, gap 1.0)
S_all  = holes of the exterior of seal          (everything the outside cannot reach)
A      = (S_all − grow(frontSil, gap) − rear interior ink) ∪ (frontSil − front interior ink)</pre></section>
<section style="padding:var(--s5) 0;border-bottom:1px solid var(--g2)"><h2>Calibration — two human pairs of this class</h2>
<table><tr><th></th><th>line</th><th>real active</th><th>v2</th></tr>{cal}</table></section>
<h2 style="padding-top:var(--s5)">The five, again</h2>
{"".join(block(i+1, n) for i, n in enumerate(NEW))}
<div id="export">— nothing graded yet —</div>
<footer>Generated by <code>notes/_lanes/264-active-page2.py</code> from <code>264-active-gen2.py</code> · 2026-09-09 #264</footer></div>
<script>const out=document.getElementById('export');function upd(){{const rows=[];document.querySelectorAll('.cand').forEach(c=>{{const n=c.querySelector('h3').textContent;const g=c.querySelector('input[type=radio]:checked');const note=c.querySelector('.note').value.trim();if(g)rows.push(n+' → '+g.value+(note?' — '+note:''));}});const k=document.querySelectorAll('.cand').length-rows.length;out.textContent=(rows.join('\\n')||'— nothing graded yet —')+(k?'\\nNOT GRADED ('+k+')':'');}}document.addEventListener('change',upd);document.addEventListener('input',upd);</script></body></html>'''
out = os.path.join(R, "notes", "_REVIEW-264-active-glyphs-2.html"); open(out, "w").write(html); print(len(html))
