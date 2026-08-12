#!/usr/bin/env python3
"""Embed the compliance KG diagram into the knowledge-usage trace as a NATIVE fragment.

Replaces the iframe embed with an inline, fully-namespaced fragment (everything scoped under
`#kg`, vars renamed `--kg-*`): no duplicate controls, themes WITH the dossier (`body.dark #kg`),
and bursts full-width out of the `.wrap` parent. Re-run after regenerating the diagram.

Usage:  python3 knowledge/compliance/_embed_kg_fragment.py <trace.html>
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "graph-index.json")))
by_sc = d["by_sc"]; ver = d["verification"]["by_sc"]; ext = d["external_automatable_refs"]["by_sc"]
PRIN = {"1": "Perceivable", "2": "Operable", "3": "Understandable", "4": "Robust"}
def sckey(s): return [int(x) for x in s.split(".")]
scs = [{"id": sc, "principle": PRIN.get(sc.split(".")[0], "?"),
        "verified": ver.get(sc) is not None, "axe": bool(ext.get(sc)),
        "n": len(by_sc[sc])} for sc in sorted(by_sc, key=sckey)]
comps = sorted(d["by_component"])
edges = [[c, sc] for sc in by_sc for c in by_sc[sc]]
stats = {"nsc": len(scs), "ncomp": len(comps), "nedge": len(edges),
         "verified": sum(1 for s in scs if s["verified"]),
         "axe": sum(1 for s in scs if s["axe"] and not s["verified"])}
DATA = {"scs": scs, "comps": comps, "edges": edges, "stats": stats}

FRAG = r"""<style id="kg-style">
#kg{--kg-tx:#111;--kg-mut:#5b6770;--kg-ln:#e6e8ea;--kg-sf:#f6f7f8;--kg-pg:#fff;--kg-accent:#db0011;
  --kg-edge:#c9ced3;--kg-edgehi:#0d99ff;--kg-ok:#2B7E4F;--kg-axe:#C58900;--kg-none:#9aa0a6;
  width:100vw;margin-left:calc(50% - 50vw);padding:8px 40px 0;box-sizing:border-box;color:var(--kg-tx);}
body.dark #kg{--kg-tx:#f2f2f2;--kg-mut:#9aa4ad;--kg-ln:#2c2c2c;--kg-sf:#1a1a1a;--kg-pg:#111;--kg-edge:#333;--kg-edgehi:#4aa8ff;}
#kg .kg-stats{display:flex;gap:10px;flex-wrap:wrap;margin:2px auto 6px;max-width:1120px}
#kg .kg-chip{font-size:12px;border:1px solid var(--kg-ln);border-radius:999px;padding:5px 12px;background:var(--kg-sf);color:var(--kg-tx)}
#kg .kg-chip b{font-variant-numeric:tabular-nums}
#kg .kg-chip .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}
#kg .kg-legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12px;color:var(--kg-mut);margin:6px auto 8px;max-width:1120px}
#kg .kg-legend .dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
#kg svg{display:block;width:100%;height:auto;background:transparent}
#kg .grouphdr{font-size:11px;font-weight:600;fill:var(--kg-mut);text-transform:uppercase;letter-spacing:.05em}
#kg .nlabel{font-size:11px;fill:var(--kg-tx);font-variant-numeric:tabular-nums}
#kg .nlabel.comp{font-size:10.5px}
#kg .colhdr{font-size:12px;font-weight:600;fill:var(--kg-tx)}
#kg .edge{stroke:var(--kg-edge);stroke-width:1;fill:none;opacity:.5}
#kg .edge.hi{stroke:var(--kg-edgehi);stroke-width:1.6;opacity:1}
#kg .edge.dim{opacity:.06}
#kg .node{cursor:pointer}
#kg .node circle{stroke:var(--kg-pg);stroke-width:1.5}
#kg .node.dim{opacity:.18}
#kg .node.hi .nlabel{font-weight:700}
#kg .kg-note{font-size:12px;color:var(--kg-mut);max-width:82ch;margin:12px auto 0;line-height:1.5}
#kg .kg-tip{position:fixed;pointer-events:none;background:var(--kg-tx);color:var(--kg-pg);font-size:11.5px;padding:6px 9px;border-radius:5px;max-width:260px;opacity:0;transition:opacity .1s;z-index:99;line-height:1.4}
</style>
<div id="kg">
  <div class="kg-stats" id="kgstats"></div>
  <div class="kg-legend">
    <span><span class="dot" style="background:var(--kg-ok)"></span>verified_by — a check runs &amp; passes</span>
    <span><span class="dot" style="background:var(--kg-axe)"></span>unverified · axe-core available (easy win)</span>
    <span><span class="dot" style="background:var(--kg-none)"></span>unverified · no OSS check</span>
  </div>
  <svg id="kgsvg" viewBox="0 0 1080 1000" preserveAspectRatio="xMidYMin meet"></svg>
  <p class="kg-note"><b>Reading it:</b> green SC nodes are the 4 with a live <code>verified_by</code> edge; amber + grey are the 27 that ride on the claimed edge alone (amber = an axe-core rule exists; grey = no OSS check, or already covered by a bespoke gate). Hover any node to trace its edges.</p>
</div>
<script id="kg-script">
(function(){
  const DATA = __DATA__;
  const NS='http://www.w3.org/2000/svg';
  const svg=document.getElementById('kgsvg'), root=document.getElementById('kg');
  const tip=document.createElement('div'); tip.className='kg-tip'; root.appendChild(tip);
  const W=1080, PADT=54, ROW=24, LX=250, RX=830, R=6;
  const s=DATA.stats;
  document.getElementById('kgstats').innerHTML=
    `<span class="kg-chip"><b>${s.nsc}</b> success criteria</span>`+
    `<span class="kg-chip"><b>${s.ncomp}</b> components</span>`+
    `<span class="kg-chip"><b>${s.nedge}</b> applies_to edges</span>`+
    `<span class="kg-chip"><span class="dot" style="background:var(--kg-ok)"></span>verified_by <b>${s.verified}/${s.nsc}</b></span>`+
    `<span class="kg-chip"><span class="dot" style="background:var(--kg-axe)"></span>axe available <b>${s.axe}</b></span>`;
  const order=["Perceivable","Operable","Understandable","Robust"];
  let scPos={}, y=PADT, groups=[];
  order.forEach(p=>{ const inGrp=DATA.scs.filter(x=>x.principle===p); if(!inGrp.length) return;
    groups.push({p, y:y-14}); inGrp.forEach(sc=>{ scPos[sc.id]={x:LX,y}; y+=ROW; }); y+=14; });
  const Hleft=y; let compPos={}, cy=PADT;
  DATA.comps.forEach(c=>{ compPos[c]={x:RX,y:cy}; cy+=ROW; });
  const H=Math.max(Hleft,cy)+20; svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
  function state(sc){ return sc.verified?'var(--kg-ok)':(sc.axe?'var(--kg-axe)':'var(--kg-none)'); }
  const edgeEls=[];
  DATA.edges.forEach(([c,sc])=>{ if(!scPos[sc]||!compPos[c]) return;
    const a=compPos[c], b=scPos[sc], p=document.createElementNS(NS,'path'), mx=(a.x+b.x)/2;
    p.setAttribute('d',`M${b.x+R},${b.y} C${mx},${b.y} ${mx},${a.y} ${a.x-R},${a.y}`);
    p.setAttribute('class','edge'); p.dataset.sc=sc; p.dataset.comp=c; svg.appendChild(p); edgeEls.push(p); });
  const ch1=document.createElementNS(NS,'text'); ch1.setAttribute('x',LX-R); ch1.setAttribute('y',28); ch1.setAttribute('text-anchor','end'); ch1.setAttribute('class','colhdr'); ch1.textContent='WCAG success criteria'; svg.appendChild(ch1);
  const ch2=document.createElementNS(NS,'text'); ch2.setAttribute('x',RX+R); ch2.setAttribute('y',28); ch2.setAttribute('class','colhdr'); ch2.textContent='Components'; svg.appendChild(ch2);
  groups.forEach(g=>{ const t=document.createElementNS(NS,'text'); t.setAttribute('x',LX-R); t.setAttribute('y',g.y); t.setAttribute('text-anchor','end'); t.setAttribute('class','grouphdr'); t.textContent=g.p; svg.appendChild(t); });
  function mkNode(id,x,yy,fill,label,anchor,cls){
    const g=document.createElementNS(NS,'g'); g.setAttribute('class','node '+cls); g.dataset.id=id;
    const c=document.createElementNS(NS,'circle'); c.setAttribute('cx',x); c.setAttribute('cy',yy); c.setAttribute('r',R); c.setAttribute('fill',fill);
    const t=document.createElementNS(NS,'text'); t.setAttribute('x',anchor==='end'?x-R-6:x+R+6); t.setAttribute('y',yy+3.5); t.setAttribute('text-anchor',anchor); t.setAttribute('class','nlabel '+(cls==='comp'?'comp':'')); t.textContent=label;
    g.appendChild(c); g.appendChild(t); svg.appendChild(g); return g;
  }
  DATA.scs.forEach(sc=>{ const p=scPos[sc.id]; mkNode(sc.id,p.x,p.y,state(sc),sc.id+'  ('+sc.n+')','end','sc'); });
  DATA.comps.forEach(c=>{ const p=compPos[c]; mkNode(c,p.x,p.y,'var(--kg-edgehi)',c,'start','comp'); });
  const nodes=[...svg.querySelectorAll('.node')];
  function clearHi(){ edgeEls.forEach(e=>e.classList.remove('hi','dim')); nodes.forEach(n=>n.classList.remove('hi','dim')); }
  function hi(id){ clearHi(); const isSC=!!scPos[id];
    edgeEls.forEach(e=>{ const on=isSC? e.dataset.sc===id : e.dataset.comp===id; e.classList.add(on?'hi':'dim'); });
    const linked=new Set([id]); DATA.edges.forEach(([c,sc])=>{ if(isSC&&sc===id) linked.add(c); if(!isSC&&c===id) linked.add(sc); });
    nodes.forEach(n=>n.classList.add(linked.has(n.dataset.id)?'hi':'dim')); }
  function showTip(id,e){ let html=''; const sc=DATA.scs.find(x=>x.id===id);
    if(sc){ html=`<b>${sc.id}</b> · ${sc.principle}<br>${sc.n} components claim it<br>`+(sc.verified?'✓ verified_by':(sc.axe?'○ unverified · axe-core available':'○ unverified · no OSS check')); }
    else { const scz=DATA.edges.filter(x=>x[0]===id).map(x=>x[1]); html=`<b>${id}</b><br>claims ${scz.length} SC: ${scz.join(', ')}`; }
    tip.innerHTML=html; tip.style.opacity=1; moveTip(e); }
  function moveTip(e){ tip.style.left=Math.min(window.innerWidth-270,e.clientX+14)+'px'; tip.style.top=(e.clientY+14)+'px'; }
  nodes.forEach(n=>{ n.addEventListener('mouseenter',e=>{ hi(n.dataset.id); showTip(n.dataset.id,e); });
    n.addEventListener('mousemove',moveTip); n.addEventListener('mouseleave',()=>{ clearHi(); tip.style.opacity=0; }); });
})();
</script>"""

FRAG = FRAG.replace("__DATA__", json.dumps(DATA))

trace = sys.argv[1]
doc = open(trace).read()
s = doc.index('<iframe title="Compliance KG edges diagram"')
e = doc.index('</iframe>', s) + len('</iframe>')
doc = doc[:s] + FRAG + doc[e:]
open(trace, "w").write(doc)
print("embedded native fragment into", trace, "· replaced iframe (", e - s, "bytes ) with", len(FRAG), "bytes ·", stats)
