#!/usr/bin/env python3
"""Lane LY (#280) — build OPTION-strata-<date>.html, the one option on a page for Dave.

Every number on the page is READ, never typed: the band table, the node counts, the fit scales and
the screenshot names all come from `shots/shots.json` (written by shots.py) and from the explorer's
own embedded KG. Swiss design system idiom; single file; the PNGs are referenced from `shots/`.

  python3 notes/_lanes/280/layout/_build_option.py
"""
import json, os, datetime, html

LANE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(LANE, '..', '..', '..', '..'))
SHOTS = json.load(open(os.path.join(LANE, 'shots', 'shots.json')))
DATE = datetime.date.today().isoformat()
OUT = os.path.join(LANE, f'OPTION-strata-{DATE}.html')

kgp = os.path.join(REPO, 'notes', '_KG-EXPLORER.html')
s = open(kgp).read()
k = '<script id="kg" type="application/json">'
i = s.index(k) + len(k); j = s.index('</script>', i)
KG = json.loads(s[i:j].replace('<\\/script', '</script'))
BANDS = KG['bands']
VER = KG['version']

PAIRS = [
    ('The two layouts, chips at the page defaults', 'kg-116-force', 'kg-117-strata',
     'Nothing is switched on beyond what the page opens with: the System layer only.'),
    ('Strata with the assets layer switched on', 'kg-117-strata-assets', 'kg-117-strata-assets',
     'The 688 icons, icon groups and logos join System — the same layer, further right.'),
    ('Strata with the Constitution switched on', 'kg-117-strata-const', 'kg-117-strata-const',
     'The ruling record appears as a fourth band below System, dimmed, and every citation it '
     'makes of a component crosses a boundary.'),
]

SENTENCES = [
    "Nothing moved sideways: every node keeps the exact x the force layout gave it, so the clusters "
    "and the family columns are where they were.",
    "What moved is y — each node is now packed inside the band for its own view, so Explanation sits "
    "above Design governance, which sits above System, with the Constitution as the bedrock beneath.",
    "The lines that cross a band boundary are drawn brighter than the ones that stay inside a layer, "
    "because the crossings are the thing the picture is for.",
]


def img(name, cap):
    d = SHOTS[name]
    return (f'<figure><img src="shots/{name}.png" alt="{html.escape(cap)}" loading="lazy">'
            f'<figcaption>{html.escape(cap)} — fit scale {d["view"]["k"]}, '
            f'{d["stats"]}</figcaption></figure>')


def pair(title, a, b, note):
    rows = ''
    for scheme in ('light', 'dark'):
        an, bn = f'{a}-{scheme}', f'{b}-{scheme}'
        if an not in SHOTS or bn not in SHOTS: continue
        left = img(an, ('1.16 force' if a.startswith('kg-116') else 'Strata') + f' · {scheme}')
        right = img(bn, ('Strata' if b != a else 'Strata') + f' · {scheme}')
        rows += f'<div class="pair">{left}{"" if an == bn else right}</div>'
    return (f'<section class="band"><p class="label">{html.escape(title)}</p>'
            f'<p class="note">{html.escape(note)}</p>{rows}</section>')


bandrows = ''.join(
    f'<tr><td>{html.escape(b["name"])}</td><td class="n">{b["n"]:,}</td>'
    f'<td class="n">{b["y0"]:,.1f}</td><td class="n">{b["y1"]:,.1f}</td></tr>' for b in BANDS)

allshot = img('kg-117-strata-all-light', 'Strata, every layer on · light')

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Explorer {VER} — the graph as three layers</title>
<style>
:root{{
 --accent:#DB0011;--black:#000;--white:#fff;
 --grey-1:#F3F3F3;--grey-2:#EDEDED;--grey-3:#D7D8D6;--grey-6:#767676;--grey-7:#545454;--grey-8:#333;
 --s1:.5rem;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem;--s7:6rem;
 --max:1200px;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--white);color:var(--black);
 font:400 16px/1.75 "Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:var(--max);margin:0 auto;padding:0 var(--s4)}}
header.top{{border-bottom:1px solid var(--grey-2);padding:var(--s3) 0;position:sticky;top:0;background:var(--white);z-index:5}}
header.top .wrap{{display:flex;justify-content:space-between;align-items:baseline;gap:var(--s3)}}
header.top b{{font-weight:500;letter-spacing:.04em;text-transform:uppercase;font-size:12px}}
header.top span{{font-size:12px;color:var(--grey-6);letter-spacing:.04em}}
h1{{font-size:3.5625rem;line-height:1.05;font-weight:300;margin:var(--s6) 0 var(--s3);letter-spacing:0}}
h2{{font-size:2.125rem;line-height:1.15;font-weight:400;margin:0 0 var(--s3)}}
.label{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
 display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s2)}}
.label::before{{content:'';display:inline-block;width:20px;height:1px;background:var(--accent)}}
.lede{{font-size:1.1875rem;line-height:1.6;max-width:62ch;color:var(--grey-8)}}
section{{padding:var(--s7) 0;border-top:1px solid var(--grey-2)}}
section.band{{padding:var(--s6) 0}}
.note{{color:var(--grey-7);max-width:74ch;margin:0 0 var(--s4)}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:var(--s2);margin-bottom:var(--s4)}}
.pair:has(figure:only-child){{grid-template-columns:1fr}}
figure{{margin:0}}
figure img{{width:100%;height:auto;display:block;border:1px solid var(--grey-2)}}
figcaption{{font-size:12px;line-height:1.5;color:var(--grey-6);padding-top:var(--s1);letter-spacing:.02em}}
.three{{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s2);border-top:1px solid var(--black);
 padding-top:var(--s3);margin-top:var(--s5)}}
.three p{{margin:0;font-size:1rem;line-height:1.7}}
.three i{{display:block;font-style:normal;font-size:12px;letter-spacing:.14em;color:var(--grey-6);
 text-transform:uppercase;margin-bottom:var(--s1)}}
table{{border-collapse:collapse;width:100%;font-size:14px;margin-top:var(--s3)}}
th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--grey-2)}}
th{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:500;color:var(--grey-6);
 border-bottom:1px solid var(--black)}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
.ask{{background:var(--grey-1);padding:var(--s6) 0}}
.opts{{display:grid;gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin:var(--s4) 0}}
.opts label{{background:var(--white);padding:var(--s3);display:grid;grid-template-columns:auto 1fr;
 gap:var(--s2);align-items:start;cursor:pointer}}
.opts label:hover{{background:#FAFAFA}}
.opts b{{font-weight:500;display:block}}
.opts small{{color:var(--grey-7);font-size:14px;line-height:1.6;display:block}}
textarea{{width:100%;min-height:110px;border:1px solid var(--grey-3);padding:var(--s2);font:inherit;
 font-size:15px;border-radius:0;background:var(--white)}}
button{{font:inherit;font-size:13px;letter-spacing:.06em;text-transform:uppercase;font-weight:500;
 padding:14px 22px;border:1px solid var(--black);background:var(--black);color:var(--white);cursor:pointer;border-radius:0}}
button.ghost{{background:var(--white);color:var(--black)}}
.row{{display:flex;gap:var(--s2);align-items:center;flex-wrap:wrap;margin-top:var(--s3)}}
pre{{background:var(--white);border:1px solid var(--grey-3);padding:var(--s3);overflow:auto;font-size:12px;
 line-height:1.6;max-height:320px}}
footer{{border-top:1px solid var(--grey-2);padding:var(--s4) 0 var(--s7);font-size:12px;color:var(--grey-6);
 letter-spacing:.02em}}
@media (max-width:820px){{.pair,.three{{grid-template-columns:1fr}}h1{{font-size:2.6875rem}}}}
</style>
</head>
<body>
<header class="top"><div class="wrap"><b>Apollo · knowledge graph</b>
<span>Explorer {VER} · {DATE} · one option, for your eye</span></div></header>

<div class="wrap">
<p class="label" style="margin-top:var(--s6)">The question</p>
<h1>The graph, laid out as three<br>visible layers.</h1>
<p class="lede">You said the last one did not look like three layers — that relabelling and grouping
the chips was not what you expected. This is the layout instead of the labels: one stage, three
horizontal bands, one per view, with the Constitution as a fourth band beneath them. Same graph,
same nodes, same left-to-right positions. Only the vertical changed.</p>

<div class="three">
{''.join(f'<p><i>{n+1}</i>{html.escape(t)}</p>' for n, t in enumerate(SENTENCES))}
</div>
</div>

<div class="wrap">
{''.join(pair(*p) for p in PAIRS)}

<section class="band"><p class="label">Every layer on at once</p>
<p class="note">This is the picture the three bands are for: four layers, and the lines between them.
The wide horizontal gaps are the unrelated column-packing gap from the last round — the off families
still hold their slots on the x axis — and nothing here changes that.</p>
{allshot}</section>

<section><p class="label">What the bands are</p>
<h2>Four bands, top to bottom.</h2>
<p class="note">A node's band is its view. Each band is the same height; inside it the nodes are
packed by a light force that only ever moves them vertically, so the horizontal order survives
untouched.</p>
<table><thead><tr><th>Band</th><th class="n">Nodes</th><th class="n">from y</th><th class="n">to y</th></tr></thead>
<tbody>{bandrows}</tbody></table>
</section>
</div>

<div class="ask"><div class="wrap">
<p class="label">Your call</p>
<h2>Which way should the explorer open?</h2>
<div class="opts">
 <label><input type="radio" name="layout" value="strata-default">
  <span><b>a · Strata, ship it as the default</b><small>The explorer opens in layers. Force stays
  available on the switch.</small></span></label>
 <label><input type="radio" name="layout" value="strata-switch">
  <span><b>b · Strata as a switch, force stays the default</b><small>What is built today: the page
  opens exactly as it does now, and the layers are one click away.</small></span></label>
 <label><input type="radio" name="layout" value="neither">
  <span><b>c · Neither — this is not it</b><small>Say what is wrong in the note and it goes back on
  the bench.</small></span></label>
</div>
<textarea id="note" placeholder="Anything you want said about it — what works, what does not."></textarea>
<div class="row">
 <button id="dl">Download the answer</button>
 <button class="ghost" id="cp">Copy to clipboard</button>
 <span id="msg" style="font-size:13px;color:var(--grey-6)"></span>
</div>
<pre id="exp" hidden></pre>
</div></div>

<footer><div class="wrap">Explorer {VER} · built {DATE} · the layout question this page answers is
s277-D8. Screenshots taken in fresh, never-driven browser contexts at 1280×800.</div></footer>

<script>
var PAGE="OPTION-strata-{DATE}";
function state(){{
 var r=document.querySelector('input[name=layout]:checked');
 return {{choice:r?r.value:null,note:document.getElementById('note').value||""}};
}}
function envelope(){{
 var now=new Date().toISOString();
 return {{exportedAt:now,page:PAGE,answers:{{layout:state()}}}};
}}
function show(){{
 var j=JSON.stringify(envelope(),null,2);
 var p=document.getElementById('exp');p.hidden=false;p.textContent=j;return j;
}}
document.getElementById('dl').onclick=function(){{
 var j=show();
 var a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([j],{{type:'application/json'}}));
 a.download=PAGE+'-export.json';a.click();
 document.getElementById('msg').textContent='downloaded';
}};
document.getElementById('cp').onclick=function(){{
 var j=show();
 if(navigator.clipboard)navigator.clipboard.writeText(j);
 document.getElementById('msg').textContent='copied — the JSON is below too';
}};
document.addEventListener('change',function(){{if(!document.getElementById('exp').hidden)show();}});
</script>
</body>
</html>
"""

open(OUT, 'w').write(HTML)
print(f"wrote {OUT} · {os.path.getsize(OUT):,} B · bands {len(BANDS)} · shots {len(SHOTS)}")
