#!/usr/bin/env python3
"""Lane LS (#280) — builds SKETCHES-2026-09-16.html from the SVGs `_sketches.py` rendered.

  python3 notes/_lanes/280/layout-sketches/_sketches.py
  python3 notes/_lanes/280/layout-sketches/_build_page.py
"""
import json, os

ROOT = os.environ.get('LS_ROOT') or '/sessions/intelligent-serene-curie/mnt/UX-design'
HERE = os.path.join(ROOT, 'notes/_lanes/280/layout-sketches')
OUT = os.path.join(HERE, 'SKETCHES-2026-09-16.html')
F = json.load(open(os.path.join(HERE, 'facts.json')))


def svg(name):
    return open(os.path.join(HERE, f'sketch-{name}.svg')).read()


def n(v):
    return f'{v:,}'


S = F['sample']
CAP = (f"{n(S['nodes'])} of the {n(F['drawnNodes'])} nodes the explorer draws with every chip on "
       f"({n(S['perView']['system'])} of {n(F['perView']['system'])} System, all "
       f"{n(S['perView']['design'])} Design governance, all {n(S['perView']['explain'])} Explanation, "
       f"{n(S['perView']['constitution'])} of {n(F['perView']['constitution'])} The Constitution), and "
       f"the {n(S['edges'])} relations that run between them — {n(F['crossShown']['shells'])} of those "
       f"cross a view boundary.")

SKETCHES = [
    dict(k='strata', num='1', name='Strata',
         sub='Three horizontal bands, the Constitution as bedrock below',
         s1='Three bands stacked top to bottom, so a node’s layer is simply how high it sits on one '
            'flat stage — and every line that leaves a band is a claim crossing from one kind of '
            'knowledge to another.',
         s2='It is the cheapest of the four: a switch in the page, built and shipped today behind '
            'LAYOUT · FORCE / STRATA, with the old force layout still what the page opens with.',
         figs=[('img', '../layout/shots/kg-117-strata-all-light.png',
                'Strata, every layer on · light · 1280×800, a fresh never-driven context — 4,611 nodes, '
                '8,084 relations, 53 edge types. The band order is Explanation, Design governance, '
                'System, then The Constitution as the bedrock.')]),
    dict(k='shells', num='2', name='Shells',
         sub='Concentric spheres — the layers as shells, not rows',
         s1='System is the solid core, Design governance the shell wrapped round it, Explanation the '
            'shell round that, and the Constitution the ground disc all three stand on, so depth '
            'rather than height tells you which layer you are in and a citation from the record reads '
            'as a line climbing off the floor into the core.',
         s2='It costs its own lane: the file already carries a 3D position for every node, but shells, '
            'a plinth, a cutaway and a rotation the mouse can drive are a new way of placing and '
            'drawing them, not a setting.',
         figs=[('svg', 'shells-light',
                'Three-quarter view, light · the two outer shells at 25% so the core reads through them. '
                + CAP),
               ('svg', 'shells-cutaway-light',
                f'Cutaway · the front half of Design governance and Explanation removed, leaving '
                f'{n(F["shown"]["shellsCutaway"])} nodes drawn, so the core is seen through the opening.'),
               ('svg', 'shells-dark', 'The same three-quarter view, dark.'),
               ('live', '', 'Live · drag inside the frame to turn it. Same nodes, same shells, drawn on a '
                            'canvas the way the explorer draws its 3D view.')]),
    dict(k='floors', num='3', name='Floors',
         sub='Stacked translucent plates, like an exploded building',
         s1='Three translucent plates in an exploded stack, each floor carrying its own view’s force '
            'layout laid flat on it, so every layer stays a readable map of itself while the '
            'cross-floor lines show the traffic between them — and the Constitution is a fourth plate '
            'standing beside the building rather than under it.',
         s2='It costs a new projection, the cheaper one: the plates reuse the x and y the builder '
            'already computes, so the work is the isometric and the plate furniture, not a new layout.',
         figs=[('svg', 'floors-light',
                'Isometric, slight rotation, light · the plates are System, Design governance and '
                'Explanation from the ground up, with The Constitution beside the stack. ' + CAP)]),
    dict(k='orbits', num='4', name='Orbits',
         sub='The shells flattened into rings — 2D, phone and print',
         s1='The shells seen from above: System at the centre, Design governance the middle ring, '
            'Explanation the outer ring and the Constitution an arc parked outside them, each ring '
            'keeping the order the force layout gave it so neighbours stay neighbours.',
         s2='It costs a switch in the page, the same class of change as strata — only each node’s '
            'radius and angle move — and it is the one of the four that survives at phone width and '
            'on paper.',
         figs=[('svg', 'orbits-light',
                'Flat, light · ring radius is the view, angle is the order the force layout gave the '
                'node, and distance within a ring is its distance from the layout’s centre. ' + CAP)]),
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
h2{font-size:2.125rem;line-height:1.15;font-weight:400;margin:0 0 var(--s1)}
.label{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
 display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s2)}
.label::before{content:'';display:inline-block;width:20px;height:1px;background:var(--accent)}
.lede{font-size:1.1875rem;line-height:1.6;max-width:64ch;color:var(--grey-8)}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s2);border-top:1px solid var(--black);
 padding-top:var(--s3);margin-top:var(--s5)}
.three p{margin:0}
.three i{display:block;font-style:normal;font-size:12px;letter-spacing:.14em;color:var(--grey-6);
 text-transform:uppercase;margin-bottom:var(--s1)}
section{padding:var(--s7) 0;border-top:1px solid var(--grey-2)}
.head{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);align-items:start;margin-bottom:var(--s5)}
.idx{font-size:5.25rem;line-height:1;font-weight:200;color:var(--grey-3)}
.sub{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-6);margin:var(--s1) 0 0}
.head p.body{margin:0 0 var(--s3);max-width:70ch}
.cost{border-top:1px solid var(--grey-2);padding-top:var(--s2);color:var(--grey-7);max-width:70ch;margin:0}
figure{margin:0 0 var(--s4)}
figure img,figure svg{width:100%;height:auto;display:block;border:1px solid var(--grey-2);background:#fff}
figcaption{font-size:12px;line-height:1.5;color:var(--grey-6);padding-top:var(--s1);letter-spacing:.02em;
 max-width:86ch}
#live{width:100%;height:auto;display:block;border:1px solid var(--grey-2);cursor:grab;touch-action:none}
.ask{background:var(--grey-1);padding:var(--s7) 0}
.opts{display:grid;gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin:var(--s4) 0}
.opts label{background:var(--white);padding:var(--s3);display:grid;grid-template-columns:auto 1fr;
 gap:var(--s2);align-items:start;cursor:pointer}
.opts label:hover{background:#FAFAFA}
.opts b{font-weight:500;display:block}
.opts small{color:var(--grey-7);font-size:14px;line-height:1.6;display:block}
.keep{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--grey-3);
 border:1px solid var(--grey-3);margin:var(--s4) 0}
.keep label{background:var(--white);padding:var(--s2) var(--s3);display:flex;gap:var(--s1);
 align-items:center;cursor:pointer;font-size:14px}
textarea{width:100%;min-height:110px;border:1px solid var(--grey-3);padding:var(--s2);font:inherit;
 font-size:15px;border-radius:0;background:var(--white)}
button{font:inherit;font-size:13px;letter-spacing:.06em;text-transform:uppercase;font-weight:500;
 padding:14px 22px;border:1px solid var(--black);background:var(--black);color:var(--white);cursor:pointer;
 border-radius:0}
button.ghost{background:var(--white);color:var(--black)}
.row{display:flex;gap:var(--s2);align-items:center;flex-wrap:wrap;margin-top:var(--s3)}
pre{background:var(--white);border:1px solid var(--grey-3);padding:var(--s3);overflow:auto;font-size:12px;
 line-height:1.6;max-height:320px}
footer{border-top:1px solid var(--grey-2);padding:var(--s4) 0 var(--s7);font-size:12px;color:var(--grey-6)}
@media (max-width:820px){.head,.three,.keep{grid-template-columns:1fr}h1{font-size:2.6875rem}
 .idx{font-size:3.5rem}}
"""

JS = """
var PAGE="SKETCHES-2026-09-16";
function state(){
 var r=document.querySelector('input[name=layout]:checked');
 var keep=[].slice.call(document.querySelectorAll('input[name=keep]:checked')).map(function(c){return c.value});
 return {choice:r?r.value:null,keep:keep,note:document.getElementById('note').value||""};
}
function envelope(){return {exportedAt:new Date().toISOString(),page:PAGE,answers:{layout:state()}}}
function show(){var j=JSON.stringify(envelope(),null,2);var p=document.getElementById('exp');
 p.hidden=false;p.textContent=j;return j}
document.getElementById('dl').onclick=function(){var j=show();var a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([j],{type:'application/json'}));a.download=PAGE+'-export.json';a.click();
 document.getElementById('msg').textContent='downloaded'};
document.getElementById('cp').onclick=function(){var j=show();
 try{if(navigator.clipboard&&navigator.clipboard.writeText){
  var w=navigator.clipboard.writeText(j);if(w&&w.catch)w.catch(function(){})}}catch(e){}
 document.getElementById('msg').textContent='copied — the JSON is below too'};
document.addEventListener('change',function(){if(!document.getElementById('exp').hidden)show()});

/* the shells, live — the same sampled nodes, drawn on a canvas, drag to turn */
(function(){
 var D=JSON.parse(document.getElementById('livedata').textContent);
 var cv=document.getElementById('live'),ctx=cv.getContext('2d');
 var W=1120,H=620,yaw=0.62,pitch=0.30,FOCAL=2600,drag=null;
 function size(){var dpr=Math.min(2,window.devicePixelRatio||1);
  cv.width=W*dpr;cv.height=H*dpr;cv.style.aspectRatio=W+'/'+H;ctx.setTransform(dpr,0,0,dpr,0,0)}
 function proj(p){
  var cyw=Math.cos(yaw),syw=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
  var X=p[0]*cyw+p[2]*syw,Z=-p[0]*syw+p[2]*cyw,Y=p[1]*cp-Z*sp,Z2=p[1]*sp+Z*cp;
  var k=FOCAL/(FOCAL+Z2);return [X*k,-Y*k,Z2]}
 function draw(){
  var pts=D.pts,ed=D.edges,i,p,r=[],x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;
  var rmax=D.R[2],pl=D.plinth,ring=[],a;
  for(i=0;i<=48;i++){a=2*Math.PI*i/48;ring.push(proj([pl[1]*Math.cos(a),pl[0],pl[1]*Math.sin(a)]))}
  var c0=proj([0,0,0]);
  var probe=ring.concat([[c0[0]-rmax,c0[1]-rmax],[c0[0]+rmax,c0[1]+rmax]]);
  for(i=0;i<probe.length;i++){x0=Math.min(x0,probe[i][0]);x1=Math.max(x1,probe[i][0]);
   y0=Math.min(y0,probe[i][1]);y1=Math.max(y1,probe[i][1])}
  var s=Math.min((W-90)/(x1-x0),(H-90)/(y1-y0)),cx=W/2-(x0+x1)/2*s,cy=H/2-(y0+y1)/2*s;
  var SX=function(q){return [cx+q[0]*s,cy+q[1]*s,q[2]]};
  for(i=0;i<pts.length;i++){r.push(SX(proj(pts[i])))}
  ctx.clearRect(0,0,W,H);ctx.fillStyle='#fff';ctx.fillRect(0,0,W,H);
  var g=ring.map(SX);
  ctx.beginPath();for(i=0;i<g.length;i++){ctx[i?'lineTo':'moveTo'](g[i][0],g[i][1])}
  ctx.closePath();ctx.fillStyle='#DA1A00';ctx.globalAlpha=0.05;ctx.fill();
  ctx.globalAlpha=0.35;ctx.strokeStyle='#DA1A00';ctx.lineWidth=1;ctx.stroke();
  var cen=SX(c0),tint=['#111111','#7A4B00','#8A1A5C'];
  for(i=2;i>=0;i--){ctx.beginPath();ctx.arc(cen[0],cen[1],D.R[i]*s,0,7);
   ctx.globalAlpha=0.035;ctx.fillStyle=tint[i];ctx.fill();
   ctx.globalAlpha=i?0.25:0.6;ctx.strokeStyle=tint[i];ctx.stroke()}
  for(i=0;i<ed.length;i++){var e=ed[i],A=r[e[0]],B=r[e[1]];
   ctx.globalAlpha=e[3]?0.20:0.07;ctx.strokeStyle=e[2];ctx.lineWidth=e[3]?0.6:0.45;
   ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.lineTo(B[0],B[1]);ctx.stroke()}
  var ord=pts.map(function(_,k){return k}).sort(function(a,b){return r[b][2]-r[a][2]});
  for(i=0;i<ord.length;i++){var k=ord[i];p=pts[k];var v=p[3];
   ctx.globalAlpha=v===0?1:(v===3?0.45:0.55);ctx.fillStyle=p[4];
   ctx.beginPath();ctx.arc(r[k][0],r[k][1],v===0?2:1.8,0,7);ctx.fill()}
  ctx.globalAlpha=1;
  var names=['SYSTEM','DESIGN GOVERNANCE','EXPLANATION','THE CONSTITUTION'],
      cols=['#111111','#7A4B00','#8A1A5C','#DA1A00'];
  ctx.font='700 11px "SF Mono",Menlo,Consolas,monospace';ctx.textBaseline='top';
  for(i=0;i<4;i++){ctx.fillStyle=cols[i];ctx.globalAlpha=i===3?0.7:1;ctx.fillText(names[i],28,24+i*20)}
  ctx.globalAlpha=1;ctx.fillStyle='#8A8A8A';ctx.font='400 10px "SF Mono",Menlo,Consolas,monospace';
  ctx.textAlign='right';ctx.fillText('DRAG TO TURN',W-24,H-26);ctx.textAlign='left'}
 function pt(ev){var t=ev.touches?ev.touches[0]:ev;return {x:t.clientX,y:t.clientY}}
 cv.addEventListener('pointerdown',function(ev){drag=pt(ev);cv.setPointerCapture(ev.pointerId)});
 cv.addEventListener('pointermove',function(ev){if(!drag)return;var q=pt(ev);
  yaw+=(q.x-drag.x)*0.006;pitch=Math.max(-1.2,Math.min(1.2,pitch+(q.y-drag.y)*0.004));
  drag=q;draw()});
 cv.addEventListener('pointerup',function(){drag=null});
 cv.addEventListener('pointercancel',function(){drag=null});
 window.addEventListener('resize',function(){size();draw()});
 size();draw();
})();
"""


def figure(kind, ref, cap):
    if kind == 'img':
        return (f'<figure><img src="{ref}" alt="" loading="lazy">'
                f'<figcaption>{cap}</figcaption></figure>')
    if kind == 'svg':
        return f'<figure>{svg(ref)}<figcaption>{cap}</figcaption></figure>'
    return (f'<figure><canvas id="live" width="1120" height="620"></canvas>'
            f'<figcaption>{cap}</figcaption></figure>')


def main():
    live = open(os.path.join(HERE, 'shells-live.json')).read()
    body = []
    for s in SKETCHES:
        figs = '\n'.join(figure(*f) for f in s['figs'])
        body.append(f"""<section id="{s['k']}">
<div class="head"><div><div class="idx">{s['num']}</div><h2>{s['name']}</h2>
<p class="sub">{s['sub']}</p></div>
<div><p class="body">{s['s1']}</p><p class="cost">{s['s2']}</p></div></div>
{figs}
</section>""")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Four layout sketches — the graph as three visible layers</title>
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap"><b>Apollo · knowledge graph</b>
<span>Four sketches · 2026-09-16 · not built, drawn — for your eye</span></div></header>

<div class="wrap">
<p class="label" style="margin-top:var(--s6)">The idea, four ways</p>
<h1>Three visible layers.<br>Four shapes to put them in.</h1>
<p class="lede">You said the layers were shells rather than rows, and that you needed to see ideas
rather than have one built. So here are four, each drawn from the real graph — the same nodes and the
same relations the explorer draws — and none of them is in the tool yet except the first. Pick one at
the bottom, and mark any you want kept as a second view.</p>

<div class="three">
<p><i>What is a layer</i>System is what exists, Design governance is what a design must do, Explanation
is why. Those are the three views.</p>
<p><i>What is beside them</i>The Constitution — the ruling record — is not a fourth view. In every
sketch it is drawn as ground, plate or arc: beside the three, never one of them.</p>
<p><i>What is real here</i>Every dot is a node and every line a relation, taken from the page itself
with every chip switched on. Where a sketch is sampled for legibility, the caption says the numbers.</p>
</div>
</div>

<div class="wrap">
{''.join(body)}
</div>

<div class="ask"><div class="wrap">
<p class="label">Your call</p>
<h2>Which shape should the graph stand up in?</h2>
<div class="opts">
 <label><input type="radio" name="layout" value="strata"><span><b>1 · Strata</b>
  <small>Horizontal bands. Already built — this would make it the shape the page is about.</small></span></label>
 <label><input type="radio" name="layout" value="shells"><span><b>2 · Shells</b>
  <small>Concentric spheres with the Constitution as the ground. The crowd-pleaser, and the most work.</small></span></label>
 <label><input type="radio" name="layout" value="floors"><span><b>3 · Floors</b>
  <small>Stacked plates, each layer a flat map of itself, the Constitution beside the stack.</small></span></label>
 <label><input type="radio" name="layout" value="orbits"><span><b>4 · Orbits</b>
  <small>Rings. The only one that holds up on a phone and on paper.</small></span></label>
 <label><input type="radio" name="layout" value="other"><span><b>5 · Something else</b>
  <small>None of these is it — say what you had in mind in the note.</small></span></label>
</div>
<p class="sub" style="color:var(--grey-7);letter-spacing:.14em">Keep as a second view</p>
<div class="keep">
 <label><input type="checkbox" name="keep" value="strata"> Strata</label>
 <label><input type="checkbox" name="keep" value="shells"> Shells</label>
 <label><input type="checkbox" name="keep" value="floors"> Floors</label>
 <label><input type="checkbox" name="keep" value="orbits"> Orbits</label>
</div>
<textarea id="note" placeholder="What works, what does not, what you actually pictured."></textarea>
<div class="row">
 <button id="dl">Download the answer</button>
 <button class="ghost" id="cp">Copy to clipboard</button>
 <span id="msg" style="font-size:13px;color:var(--grey-6)"></span>
</div>
<pre id="exp" hidden></pre>
</div></div>

<footer><div class="wrap">Sketches, not a build — nothing in the explorer changed to make this page.
Drawn 2026-09-16 from explorer {F['version']} ({F['generated']}); the three views and the Constitution
are s277-D8. Sketch 1's photograph is lane LY's, taken at 1280×800 in a fresh, never-driven context.
</div></footer>

<script type="application/json" id="livedata">{live}</script>
<script>{JS}</script>
</body>
</html>
"""
    open(OUT, 'w').write(html)
    print(OUT, len(html), 'bytes')


if __name__ == '__main__':
    main()
