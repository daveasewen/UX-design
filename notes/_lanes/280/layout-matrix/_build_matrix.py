#!/usr/bin/env python3
"""Lane LM (#280) — builds MATRIX-2026-09-16.html, the CONTACT SHEET of the six cells.

One page, 3×2: layout by row (force · strata · shells), dimension by column (2D · 3D), each cell its
own never-driven 1280 light screenshot and one sentence. No radios — it is for looking, not ruling.
The images are REFERENCED from `shots/`, never copied.

  python3 notes/_lanes/280/layout-matrix/_build_matrix.py
"""
import json, os

ROOT = os.environ.get('LM_ROOT') or '/sessions/intelligent-serene-curie/mnt/UX-design'
HERE = os.path.join(ROOT, 'notes/_lanes/280/layout-matrix')
OUT = os.path.join(HERE, 'MATRIX-2026-09-16.html')
SHOTS = json.load(open(os.path.join(HERE, 'shots/shots.json')))

CELLS = [
    ('force', '2d', 'Force · 2D', 'the default',
     "The graph as it has always stood: one red hub of components with the families fanning out "
     "around it, the shape found by the force itself and nothing placed by hand."),
    ('force', '3d', 'Force · 3D', '',
     "The same cloud lifted off the page and turned, so the depth between the clusters is visible "
     "and the hub reads as a solid centre rather than a blot."),
    ('strata', '2d', 'Strata · 2D', 'sketch 1',
     "Three horizontal bands with the Constitution as bedrock below them, so a node's layer is "
     "simply how high it sits, and every line crossing a boundary is a claim leaving one kind of "
     "knowledge for another."),
    ('strata', '3d', 'Strata · 3D', 'the sketch called FLOORS',
     "The same three layers as translucent plates in an exploded stack, each floor carrying its own "
     "view's map laid flat on it, with the Constitution a fourth plate standing beside the building "
     "rather than under it."),
    ('shells', '2d', 'Shells · 2D', 'the sketch called ORBITS',
     "The layers seen from above as concentric rings — System the core, Design governance the middle "
     "ring, Explanation the outer one, the Constitution an arc parked outside them — the one cell "
     "that survives at phone width and on paper."),
    ('shells', '3d', 'Shells · 3D', 'sketch 2',
     "System as a solid core sphere inside two dimmed shells, standing on the Constitution's plinth "
     "disc, so a ruling's citation reads as a line climbing off the floor into the core."),
]

CSS = """
:root{--accent:#DB0011;--black:#000;--white:#fff;--grey-1:#F3F3F3;--grey-2:#EDEDED;--grey-3:#D7D8D6;
 --grey-6:#767676;--grey-7:#545454;--grey-8:#333;--s1:.5rem;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;
 --s6:4rem;--s7:6rem;--max:1200px}
*{box-sizing:border-box}
body{margin:0;background:var(--white);color:var(--black);
 font:400 16px/1.75 "Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--s4)}
header.top{border-bottom:1px solid var(--grey-2);padding:var(--s3) 0;position:sticky;top:0;
 background:var(--white);z-index:5}
header.top .wrap{display:flex;justify-content:space-between;align-items:baseline;gap:var(--s3)}
header.top b{font-weight:500;letter-spacing:.04em;text-transform:uppercase;font-size:12px}
header.top span{font-size:12px;color:var(--grey-6);letter-spacing:.04em}
h1{font-size:3.5625rem;line-height:1.05;font-weight:300;margin:var(--s6) 0 var(--s3)}
.label{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
 display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s2)}
.label::before{content:'';display:inline-block;width:20px;height:1px;background:var(--accent)}
.lede{font-size:1.1875rem;line-height:1.6;max-width:64ch;color:var(--grey-8)}
.cols{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--s1) var(--s4);border-top:1px solid var(--black);
 padding-top:var(--s2);margin:var(--s5) 0 0;font-size:12px;letter-spacing:.14em;text-transform:uppercase;
 color:var(--grey-6)}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--s5) var(--s4);margin:var(--s3) 0 var(--s7)}
figure{margin:0}
figure img{width:100%;height:auto;display:block;border:1px solid var(--grey-2);background:#fff}
figcaption{padding-top:var(--s2)}
figcaption b{display:block;font-weight:500;font-size:12px;letter-spacing:.14em;text-transform:uppercase}
figcaption em{font-style:normal;color:var(--accent)}
figcaption span{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-6);
 margin-bottom:var(--s1)}
figcaption p{margin:var(--s1) 0 0;color:var(--grey-7);max-width:56ch;font-size:15px;line-height:1.6}
figcaption code{font:12px/1.6 "SF Mono",Menlo,Consolas,monospace;color:var(--grey-6)}
footer{border-top:1px solid var(--grey-2);padding:var(--s4) 0 var(--s7);font-size:12px;color:var(--grey-6)}
@media (max-width:820px){.grid,.cols{grid-template-columns:1fr}h1{font-size:2.6875rem}}
"""


def fig(l, d, name, tag, sent):
    key = f'kg-118-{l}-{d}-light'
    s = SHOTS.get(key, {})
    stats = (s.get('stats') or '').replace(' declared, unresolved', ' unresolved')
    return f"""<figure>
  <img src="shots/{key}.png" alt="{name} — the explorer at 1280×800, light, never driven" loading="lazy">
  <figcaption><span>{'Layout ' + l} · {d.upper()}{' · ' + tag if tag else ''}</span>
    <b>{name}{' <em>· default</em>' if (l, d) == ('force', '2d') else ''}</b>
    <p>{sent}</p>
    <p><code>?layout={l}&amp;dim={d}</code> · {stats}</p>
  </figcaption>
</figure>"""


HTML = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The layout matrix — six cells</title>
<style>{CSS}</style></head>
<body>
<header class="top"><div class="wrap"><b>Apollo · knowledge graph</b>
<span>Contact sheet · #280 · 2026-09-16 · explorer v1.18</span></div></header>
<main class="wrap">
<p class="label" style="margin-top:var(--s6)">Six cells, one switch</p>
<h1>All of them, in 2D and 3D,<br>with force still the default.</h1>
<p class="lede">Three layouts down the page — force, strata, shells — and two dimensions across it.
Every picture below is the real explorer at 1280×800, light, in a fresh context that was never
clicked: the cell was chosen by its URL flag. The page still opens in force · 2D, pixel for pixel
the view you already have.</p>
<div class="cols"><div>2D</div><div>3D</div></div>
<div class="grid">
{chr(10).join(fig(*c) for c in CELLS)}
</div>
</main>
<footer><div class="wrap">Screenshots: <code>notes/_lanes/280/layout-matrix/shots/</code> — referenced, not copied.
Ruled at <code>s280-D1</code>; the three views and THE CONSTITUTION are <code>s277-D8</code>.</div></footer>
</body></html>
"""

open(OUT, 'w').write(HTML)
print('wrote', OUT, f'{os.path.getsize(OUT):,} B')
