#!/usr/bin/env python3
"""#264 — review page for the active-glyph experiment. Generated from 264-active-gen.json; do not hand-edit."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "..", "..")
r = json.load(open(os.path.join(HERE, "264-active-gen.json")))
CAL = ['home','transfer','block','alert','settings','insight','card','account','data-chart','aeroplane']
NEW = [k for k in r if k not in CAL]
def sym(sid, svg):
    inner = re.sub(r'^.*?<svg[^>]*>', '', svg, flags=re.S).replace('</svg>', '').strip()
    return f'<symbol id="{sid}" viewBox="0 0 18 18">{inner}</symbol>'
symbols = []
for n, v in r.items():
    symbols.append(sym(f'{n}-line', v['line'])); symbols.append(sym(f'{n}-a1', v['a1'])); symbols.append(sym(f'{n}-a2', v['a2']))
    if v['real']: symbols.append(sym(f'{n}-real', v['real']))
def ic(sid, big=False): return f'<svg class="{"big" if big else ""}" viewBox="0 0 18 18"><use href="#{sid}"/></svg>'
def navrow(theme, n, sid):
    label = n.replace('-', ' ').capitalize()
    return (f'<div class="sn" data-theme="{theme}"><a class="nv-item" href="#"><span class="nv-ic">{ic(n+"-line")}</span><span class="nv-label">{label}</span></a>'
            f'<a class="nv-item" href="#" aria-current="page"><span class="nv-ic">{ic(sid)}</span><span class="nv-label">{label}</span></a></div>')
def cal_row(n):
    v = r[n]
    return f'<tr><td class="nm">{n}</td><td>{ic(n+"-line",1)}</td><td>{ic(n+"-real",1)}</td><td>{ic(n+"-a1",1)}</td><td>{ic(n+"-a2",1)}</td></tr>'
def new_block(i, n):
    return f'''<section class="cand"><div class="ch"><span class="idx">{i:02d}</span><h3>{n}</h3>
    <div class="trio"><div><span class="cap">line</span>{ic(n+"-line",1)}</div><div><span class="cap">A1 · knockout</span>{ic(n+"-a1",1)}</div><div><span class="cap">A2 · emptied</span>{ic(n+"-a2",1)}</div></div></div>
    <div class="panels">{navrow("light",n,n+"-a1")}{navrow("dark",n,n+"-a1")}{navrow("light",n,n+"-a2")}{navrow("dark",n,n+"-a2")}</div>
    <div class="grade"><span class="cap">grade</span> <label><input type="radio" name="{n}" value="A1">A1</label> <label><input type="radio" name="{n}" value="A2">A2</label> <label><input type="radio" name="{n}" value="neither">neither</label> <input class="note" placeholder="note" data-for="{n}"></div></section>'''
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>#264 · Active-glyph experiment</title>
<style>
:root{{--accent:#DB0011;--g1:#F3F3F3;--g2:#EDEDED;--g3:#D7D8D6;--g6:#767676;--g8:#333333;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem}}
*{{box-sizing:border-box}} body{{margin:0;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;color:#000;background:#fff;font-size:16px;line-height:1.7}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 var(--s4)}} header{{padding:var(--s5) 0 var(--s4);border-bottom:1px solid var(--g2)}}
.label{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:8px;margin:0 0 var(--s2)}} .label::before{{content:'';width:20px;height:1px;background:var(--accent)}}
h1{{font-size:34px;font-weight:400;line-height:1.15;margin:0 0 var(--s2);letter-spacing:-.01em}} h2{{font-size:19px;font-weight:500;margin:0 0 var(--s2)}} h3{{font-size:19px;font-weight:500;margin:0}}
p{{margin:0 0 var(--s2)}} .lede{{max-width:66ch}} code{{font-family:Menlo,monospace;font-size:13px}}
.rule{{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);padding:var(--s5) 0;border-bottom:1px solid var(--g2)}}
pre{{font:13px/1.6 Menlo,monospace;background:var(--g1);padding:var(--s2);margin:0;overflow-x:auto}}
table{{border-collapse:collapse;margin:var(--s2) 0}} th,td{{text-align:center;padding:6px 18px;border-bottom:1px solid var(--g2)}} th{{font-weight:500;color:var(--g6);font-size:12px;letter-spacing:.08em;text-transform:uppercase}} td.nm{{text-align:left;font-size:14px}}
svg{{width:18px;height:18px;fill:#1A1A1A;color:#1A1A1A}} svg.big{{width:40px;height:40px}}
.cand{{padding:var(--s4) 0;border-bottom:1px solid var(--g2)}} .ch{{display:flex;gap:var(--s3);align-items:center;margin-bottom:var(--s3)}}
.idx{{font-size:43px;font-weight:200;line-height:1;color:var(--g3);min-width:56px}} .trio{{display:flex;gap:var(--s4);margin-left:auto}} .trio div{{display:flex;flex-direction:column;align-items:center;gap:4px}}
.cap{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6)}}
.panels{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g2);margin-bottom:var(--s2)}}
.grade{{font-size:14px;display:flex;gap:var(--s2);align-items:center}} .note{{border:0;border-bottom:1px solid var(--g3);font:inherit;padding:2px 0;flex:1}}
.sn{{--nav-row:44px;padding:4px 0}} .sn[data-theme=light]{{--nav-surface:#FFF;--nav-text:#1A1A1A;--nav-icon:#1A1A1A;background:var(--nav-surface)}} .sn[data-theme=dark]{{--nav-surface:#1F1F1F;--nav-text:#FFF;--nav-icon:#FFF;background:var(--nav-surface)}}
.nv-item{{display:flex;align-items:center;gap:12px;min-height:var(--nav-row);padding:0 16px;color:var(--nav-text);text-decoration:none;font-size:15px}} .nv-ic{{display:inline-flex;width:18px;height:18px;color:var(--nav-icon)}} .nv-ic svg{{fill:currentColor;color:inherit}}
.nv-item[aria-current=page]{{box-shadow:inset 3px 0 0 #DB0011}} .nv-item[aria-current=page] .nv-label{{font-weight:500}}
#export{{margin:var(--s4) 0;font:13px/1.6 Menlo,monospace;background:var(--g1);padding:var(--s2);white-space:pre-wrap;min-height:3em}}
footer{{padding:var(--s4) 0 var(--s6);font-size:14px;color:var(--g6)}}
</style></head><body><svg width="0" height="0" style="position:absolute">{"".join(symbols)}</svg>
<div class="wrap">
<header><p class="label">#264 · experiment · active glyphs by geometry</p>
<h1>Can the filled twin be derived from the line glyph? Ten known pairs say mostly; thirteen orphans are yours to grade.</h1>
<p class="lede">207 of the library's 432 line icons have no <code>-active</code> twin. The rule below was read off the human-made pairs and run as pure path operations — curves kept, nothing rasterised, nothing drawn by hand. Two variants are shown because the human pairs disagree on one point: whether a region the detail fully encloses (the gear's hub) is emptied or left solid.</p></header>

<section class="rule"><div><h2>The rule</h2><p style="font-size:14px;color:var(--g6)">Line weight 1.2px on an 18px grid. Border band 1.25. Knockout at line weight.</p></div>
<pre>S  = silhouette   = every contour of the line ink, filled and unioned
B  = border band  = S − erode(S, 1.25)
I  = interior ink = L − B          (detail drawn inside the shape)
A1 = S − I                         (detail becomes a hole, same weight)
A2 = S − silhouette(I)             (…and anything the detail encloses is emptied)</pre></section>

<section style="padding:var(--s5) 0;border-bottom:1px solid var(--g2)"><h2>Calibration — ten pairs the library already has</h2>
<p class="lede" style="font-size:15px">Column three is the designer's; four and five are the machine's from column two alone.</p>
<table><tr><th></th><th>line</th><th>real active</th><th>A1</th><th>A2</th></tr>{"".join(cal_row(n) for n in CAL)}</table>
<p class="lede" style="font-size:15px">Where it misses: <strong>card</strong> — the designer dropped a stripe and widened the other; <strong>alert</strong> — the clapper is separated by a gap the line never drew; <strong>insight</strong> — the filament became a slit. Those are edits, not geometry, and no rule recovers them. <strong>settings</strong> is the A2 case; <strong>home, transfer, block, aeroplane, account, data-chart</strong> are within a designer's tolerance or need one weight tweak.</p></section>

<h2 style="padding-top:var(--s5)">Thirteen orphans — no human twin exists</h2>
<p class="lede" style="font-size:15px">Each shows both variants in a real nav row, at rest and current, light and dark. Grade each; the export block collects your words.</p>
{"".join(new_block(i+1, n) for i, n in enumerate(NEW))}
<div id="export">— nothing graded yet —</div>
<footer>Generated by <code>notes/_lanes/264-active-page.py</code> from <code>264-active-gen.py</code> (skia path ops) · 2026-09-09 #264</footer></div>
<script>
const out=document.getElementById('export');
function upd(){{const rows=[];document.querySelectorAll('.cand').forEach(c=>{{const n=c.querySelector('h3').textContent;const g=c.querySelector('input[type=radio]:checked');const note=c.querySelector('.note').value.trim();if(g)rows.push(n+' → '+g.value+(note?' — '+note:''));}});const notr=document.querySelectorAll('.cand').length-rows.length;out.textContent=(rows.join('\\n')||'— nothing graded yet —')+(notr?'\\nNOT GRADED ('+notr+')':'');}}
document.addEventListener('change',upd);document.addEventListener('input',upd);
</script></body></html>'''
out = os.path.join(R, "notes", "_REVIEW-264-active-glyphs.html"); open(out, "w").write(html); print(out, len(html))
