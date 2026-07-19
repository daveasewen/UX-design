#!/usr/bin/env python3
"""Compliance KG DIAGRAM — a node-edge visual built from graph-index.json.

The graph has only ever existed as DATA (graph-index.json) + tables (_GRAPH-REPORT,
_VERIFICATION-EDGES). This renders it: Success Criteria ↔ Components, with the three
edge states made visible — the point being the verified_by gap (only 4/31 SCs verified).

Usage:  python3 knowledge/compliance/_build_kg_diagram.py [OUT.html]
Writes a self-contained, data-inlined HTML (light/dark + responsive; no deps).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "graph-index.json")))
by_sc = d["by_sc"]; by_comp = d["by_component"]
ver = d["verification"]["by_sc"]; ext = d["external_automatable_refs"]["by_sc"]
PRIN = {"1": "Perceivable", "2": "Operable", "3": "Understandable", "4": "Robust"}

def sckey(s): return [int(x) for x in s.split(".")]
scs = []
for sc in sorted(by_sc, key=sckey):
    scs.append({
        "id": sc, "principle": PRIN.get(sc.split(".")[0], "?"),
        "verified": ver.get(sc) is not None, "axe": bool(ext.get(sc)),
        "n": len(by_sc[sc]), "comps": sorted(by_sc[sc]),
    })
comps = sorted(by_comp)
edges = [[c, sc] for sc in by_sc for c in by_sc[sc]]
stats = {"nsc": len(scs), "ncomp": len(comps), "nedge": len(edges),
         "verified": sum(1 for s in scs if s["verified"]),
         "axe": sum(1 for s in scs if s["axe"] and not s["verified"])}
DATA = {"scs": scs, "comps": comps, "edges": edges, "stats": stats}

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "_KG-COMPLIANCE-DIAGRAM.html")
HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compliance KG — Success Criteria ↔ Components</title>
<style>
  :root{--uf:"Univers Next HSBC","HSBC_MtUnivers_Latin","Helvetica Neue",Arial,sans-serif;
    --ui:-apple-system,"Segoe UI",Roboto,sans-serif;
    --pg:#fff;--tx:#111;--mut:#5b6770;--ln:#e6e8ea;--sf:#f6f7f8;--accent:#db0011;
    --edge:#c9ced3;--edgehi:#0d99ff;--ok:#2B7E4F;--axe:#C58900;--none:#9aa0a6;}
  body.dark{--pg:#111;--tx:#f2f2f2;--mut:#9aa4ad;--ln:#2c2c2c;--sf:#1a1a1a;--edge:#333;--edgehi:#4aa8ff;}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:var(--ui);color:var(--tx);background:var(--pg);transition:background .16s,color .16s}
  .wrap{max-width:1120px;margin:0 auto;padding:0 32px 80px}
  .docbar{position:sticky;top:0;z-index:50;display:flex;gap:16px;align-items:center;flex-wrap:wrap;
    background:var(--pg);border-bottom:1px solid var(--ln);padding:12px 0;margin-bottom:18px}
  .docbar button{font:inherit;font-size:12px;padding:7px 12px;border:1px solid var(--tx);background:transparent;color:var(--tx);cursor:pointer}
  .docbar button.on{background:var(--tx);color:var(--pg)}
  .docbar .grp{display:flex;gap:8px;align-items:center;font-size:12px;color:var(--mut)}
  .docbar .rd{font-variant-numeric:tabular-nums;font-weight:600;color:var(--tx);min-width:48px}
  .eyebrow{font-family:var(--uf);font-size:12px;font-weight:500;color:var(--accent);margin:6px 0}
  h1{font-family:var(--uf);font-size:26px;font-weight:300;margin-bottom:6px}
  .lede{font-size:13.5px;color:var(--mut);max-width:80ch;line-height:1.5;margin-bottom:12px}
  .stats{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 6px}
  .chip{font-size:12px;border:1px solid var(--ln);border-radius:999px;padding:5px 12px;background:var(--sf)}
  .chip b{font-variant-numeric:tabular-nums}
  .chip .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}
  .legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12px;color:var(--mut);margin:8px 0 4px}
  .legend .dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
  svg{display:block;width:100%;height:auto;border:1px solid var(--ln);border-radius:4px;background:var(--pg)}
  .grouphdr{font-family:var(--uf);font-size:11px;font-weight:600;fill:var(--mut);text-transform:uppercase;letter-spacing:.05em}
  .nlabel{font-size:11px;fill:var(--tx);font-variant-numeric:tabular-nums}
  .nlabel.comp{font-size:10.5px}
  .colhdr{font-family:var(--uf);font-size:12px;font-weight:600;fill:var(--tx)}
  .edge{stroke:var(--edge);stroke-width:1;fill:none;opacity:.5}
  .edge.hi{stroke:var(--edgehi);stroke-width:1.6;opacity:1}
  .edge.dim{opacity:.06}
  .node{cursor:pointer}
  .node circle{stroke:var(--pg);stroke-width:1.5}
  .node.dim{opacity:.18}
  .node text.nlabel{font-weight:400}
  .node.hi text.nlabel{font-weight:700}
  .tip{position:fixed;pointer-events:none;background:var(--tx);color:var(--pg);font-size:11.5px;
    padding:6px 9px;border-radius:5px;max-width:260px;opacity:0;transition:opacity .1s;z-index:99;line-height:1.4}
  .note{font-size:12px;color:var(--mut);max-width:80ch;margin:14px 0;line-height:1.5}
  code{font-family:ui-monospace,Menlo,monospace;font-size:.9em;background:var(--sf);padding:1px 5px}
</style></head><body><div class="wrap">
  <div class="docbar">
    <button type="button" id="theme">◐ Light / dark</button>
    <div class="grp">Width <input type="range" id="vw" min="640" max="1120" value="1120" step="20"><span class="rd" id="vwr">full</span></div>
    <div class="grp" style="margin-left:6px">Edges:
      <button type="button" class="flt on" data-f="all">all</button>
      <button type="button" class="flt" data-f="verified">verified only</button>
      <button type="button" class="flt" data-f="unverified">unverified only</button>
    </div>
  </div>
  <div class="eyebrow">Apollo · compliance knowledge graph</div>
  <h1>Success Criteria ↔ Components — the edges</h1>
  <p class="lede">Every edge is a component's <code>applies_to</code> claim on a WCAG success criterion, derived from the
     component metas. SC nodes are coloured by <b>whether an executable check actually verifies the claim</b> in our build.
     Hover any node to trace its edges.</p>
  <div class="stats" id="stats"></div>
  <div class="legend">
    <span><span class="dot" style="background:var(--ok)"></span>verified_by — a check runs &amp; passes</span>
    <span><span class="dot" style="background:var(--axe)"></span>unverified · axe-core available (easy win)</span>
    <span><span class="dot" style="background:var(--none)"></span>unverified · no OSS check</span>
  </div>
  <svg id="svg" viewBox="0 0 1080 1000" preserveAspectRatio="xMidYMin meet"></svg>
  <p class="note"><b>Reading it:</b> green SC nodes are the 4 with a live <code>verified_by</code> edge; the amber + grey are
     the 27 that ride on the <i>claimed</i> edge alone. Amber = an off-the-shelf axe-core rule exists (candidate to wire);
     grey = no OSS check, would need a bespoke gate (or is already covered by one of ours, e.g. 1.4.11 / 2.3.3).</p>
</div>
<div class="tip" id="tip"></div>
<script>
const DATA = __DATA__;
const svg=document.getElementById('svg'), NS='http://www.w3.org/2000/svg';
const tip=document.getElementById('tip');
const W=1080, PADT=54, ROW=24, LX=250, RX=830, R=6;
// stats chips
const s=DATA.stats;
document.getElementById('stats').innerHTML=
  `<span class="chip"><b>${s.nsc}</b> success criteria</span>`+
  `<span class="chip"><b>${s.ncomp}</b> components</span>`+
  `<span class="chip"><b>${s.nedge}</b> applies_to edges</span>`+
  `<span class="chip"><span class="dot" style="background:var(--ok)"></span>verified_by <b>${s.verified}/${s.nsc}</b></span>`+
  `<span class="chip"><span class="dot" style="background:var(--axe)"></span>axe available <b>${s.axe}</b></span>`;
// layout — SCs grouped by principle on the left, components on the right
const order=["Perceivable","Operable","Understandable","Robust"];
let scPos={}, y=PADT, groups=[];
order.forEach(p=>{
  const inGrp=DATA.scs.filter(x=>x.principle===p);
  if(!inGrp.length) return;
  groups.push({p, y:y-14});
  inGrp.forEach(sc=>{ scPos[sc.id]={x:LX,y}; y+=ROW; });
  y+=14;
});
const Hleft=y;
let compPos={}, cy=PADT;
DATA.comps.forEach(c=>{ compPos[c]={x:RX,y:cy}; cy+=ROW; });
const H=Math.max(Hleft,cy)+20;
svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
function state(sc){ return sc.verified?'var(--ok)':(sc.axe?'var(--axe)':'var(--none)'); }
// edges
const edgeEls=[];
DATA.edges.forEach(([c,sc])=>{
  if(!scPos[sc]||!compPos[c]) return;
  const a=compPos[c], b=scPos[sc];
  const p=document.createElementNS(NS,'path');
  const mx=(a.x+b.x)/2;
  p.setAttribute('d',`M${b.x+R},${b.y} C${mx},${b.y} ${mx},${a.y} ${a.x-R},${a.y}`);
  p.setAttribute('class','edge'); p.dataset.sc=sc; p.dataset.comp=c;
  const scObj=DATA.scs.find(x=>x.id===sc);
  p.dataset.verified=scObj.verified?'1':'0';
  svg.appendChild(p); edgeEls.push(p);
});
// group headers + column headers
const ch1=document.createElementNS(NS,'text'); ch1.setAttribute('x',LX-R); ch1.setAttribute('y',28); ch1.setAttribute('text-anchor','end'); ch1.setAttribute('class','colhdr'); ch1.textContent='WCAG success criteria'; svg.appendChild(ch1);
const ch2=document.createElementNS(NS,'text'); ch2.setAttribute('x',RX+R); ch2.setAttribute('y',28); ch2.setAttribute('class','colhdr'); ch2.textContent='Components'; svg.appendChild(ch2);
groups.forEach(g=>{ const t=document.createElementNS(NS,'text'); t.setAttribute('x',LX-R); t.setAttribute('y',g.y); t.setAttribute('text-anchor','end'); t.setAttribute('class','grouphdr'); t.textContent=g.p; svg.appendChild(t); });
// nodes
function mkNode(id,x,yy,fill,label,anchor,cls){
  const g=document.createElementNS(NS,'g'); g.setAttribute('class','node '+cls); g.dataset.id=id;
  const c=document.createElementNS(NS,'circle'); c.setAttribute('cx',x); c.setAttribute('cy',yy); c.setAttribute('r',R); c.setAttribute('fill',fill);
  const t=document.createElementNS(NS,'text'); t.setAttribute('x',anchor==='end'?x-R-6:x+R+6); t.setAttribute('y',yy+3.5); t.setAttribute('text-anchor',anchor); t.setAttribute('class','nlabel '+(cls==='comp'?'comp':''));
  t.textContent=label; g.appendChild(c); g.appendChild(t); svg.appendChild(g); return g;
}
DATA.scs.forEach(sc=>{ const pmap=scPos[sc.id]; mkNode(sc.id,pmap.x,pmap.y,state(sc),sc.id+'  ('+sc.n+')','end','sc'); });
DATA.comps.forEach(c=>{ const pmap=compPos[c]; mkNode(c,pmap.x,pmap.y,'var(--edgehi)',c,'start','comp'); });
// interactions
const nodes=[...svg.querySelectorAll('.node')];
function clearHi(){ edgeEls.forEach(e=>e.classList.remove('hi','dim')); nodes.forEach(n=>n.classList.remove('hi','dim')); }
function hi(id){
  clearHi();
  const isSC=!!scPos[id];
  edgeEls.forEach(e=>{
    const on=isSC? e.dataset.sc===id : e.dataset.comp===id;
    e.classList.add(on?'hi':'dim');
  });
  const linked=new Set([id]);
  DATA.edges.forEach(([c,sc])=>{ if((isSC&&sc===id)) linked.add(c); if((!isSC&&c===id)) linked.add(sc); });
  nodes.forEach(n=>n.classList.add(linked.has(n.dataset.id)?'hi':'dim'));
}
nodes.forEach(n=>{
  n.addEventListener('mouseenter',e=>{ hi(n.dataset.id); showTip(n.dataset.id,e); });
  n.addEventListener('mousemove',e=>moveTip(e));
  n.addEventListener('mouseleave',()=>{ clearHi(); tip.style.opacity=0; });
});
function showTip(id,e){
  let html='';
  const sc=DATA.scs.find(x=>x.id===id);
  if(sc){ html=`<b>${sc.id}</b> · ${sc.principle}<br>${sc.n} components claim it<br>`+
    (sc.verified?'✓ verified_by (a check runs & passes)':(sc.axe?'○ unverified · axe-core rule available':'○ unverified · no OSS check')); }
  else { const cs=DATA.comps.includes(id); const scz=DATA.edges.filter(x=>x[0]===id).map(x=>x[1]); html=`<b>${id}</b><br>claims ${scz.length} SC: ${scz.join(', ')}`; }
  tip.innerHTML=html; tip.style.opacity=1; moveTip(e);
}
function moveTip(e){ tip.style.left=Math.min(window.innerWidth-270,e.clientX+14)+'px'; tip.style.top=(e.clientY+14)+'px'; }
// filters
document.querySelectorAll('.flt').forEach(b=>b.addEventListener('click',function(){
  document.querySelectorAll('.flt').forEach(x=>x.classList.remove('on')); this.classList.add('on');
  const f=this.dataset.f;
  edgeEls.forEach(e=>{ e.style.display=(f==='all')?'':(f==='verified'? (e.dataset.verified==='1'?'':'none') : (e.dataset.verified==='0'?'':'none')); });
}));
// theme + width
document.getElementById('theme').addEventListener('click',()=>document.body.classList.toggle('dark'));
const vw=document.getElementById('vw'),vwr=document.getElementById('vwr');
vw.addEventListener('input',function(){var v=+vw.value;var w=document.querySelector('.wrap');if(v>=1120){w.style.maxWidth='';vwr.textContent='full';}else{w.style.maxWidth=v+'px';vwr.textContent=v+'px';}});
</script></body></html>"""
open(OUT, "w", encoding="utf-8").write(HTML.replace("__DATA__", json.dumps(DATA)))
print("wrote", OUT, "·", stats)
