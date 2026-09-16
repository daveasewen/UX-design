#!/usr/bin/env python3
"""_build_review.py — bake REVIEW-active-2026-09-16.html (#279 lane AR, P-277-3).

The manual review sheet for the icon bases that carry two or three "-active" drawings.
Everything on the page is DERIVED here from knowledge/_icon_nodes.json (the ratified
node file) and the SVG files it names: which bases, which candidates, the Figma name,
the group, the fill mode, the glyph markup. No integer is typed into the HTML.

  python3 notes/_lanes/279/active-review/_build_review.py

Refuses if a base or candidate has no node, if an SVG named by the manifest is not on
disk, or if the derived population is not the one the ruling names (15 bases / 31
drawings) — the ruling's figures are the ASSERTION, never the source.

Export envelope (matches lane RIF's v2 page mechanics — `page` + `at`, a JSON download
+ copy-to-clipboard + a <pre> on the page — with the per-base answer map this brief asks
for):

  {page, at, exportedAt, answers: {<base-slug>: {choice, twin, flags: [...], note}}}

  choice  "twin" | "none" | "flag" | null      twin  <candidate slug> | null
  flags   [<candidate slug>, ...]              note  ""
"""
import json
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
K = REPO / "knowledge"
NODES = K / "_icon_nodes.json"
ICONS = K / "assets" / "icons"
OUT = LANE / "REVIEW-active-2026-09-16.html"

PAGE_ID = "REVIEW-active-2026-09-16"
STORAGE_KEY = "apollo.review.active.2026-09-16"
EXPORT_FILENAME = "DAVE-EXPORT-active-2026-09-16.json"
RULING = "s277-D6"          # footer only — never in the body copy
DATE = "2026-09-16"

# --------------------------------------------------------------------------- derive
pay = json.loads(NODES.read_text(encoding="utf-8"))
N = {n["id"]: n for n in pay["nodes"] if n.get("type") == "icon"}
nulls = [u for u in pay["unresolved"] if u["type"] == "defaultActive"]
avo = {}
for e in pay["edges"]:
    if e["type"] == "activeVariantOf" and e.get("t"):
        avo[e["s"]] = e["t"]

bases = []
for u in nulls:
    bid = u["source"]
    head, _, tail = u["note"].partition(":")
    cands = [c.strip() for c in tail.split(",") if c.strip()]
    if bid not in N:
        raise SystemExit(f"REFUSED — {bid} has no icon node")
    if head.strip() != bid[len("icon:"):]:
        raise SystemExit(f"REFUSED — null note for {bid} names another base: {head!r}")
    for c in cands:
        cid = "icon:" + c
        if cid not in N:
            raise SystemExit(f"REFUSED — candidate {cid} has no icon node")
        if avo.get(cid) != bid:
            raise SystemExit(f"REFUSED — {cid} is not activeVariantOf {bid} in the edge list "
                             f"(got {avo.get(cid)})")
    bases.append((bid[len("icon:"):], cands))
bases.sort()

n_bases = len(bases)
n_cands = sum(len(c) for _, c in bases)
n_two = sum(1 for _, c in bases if len(c) == 2)
n_three = sum(1 for _, c in bases if len(c) == 3)
n_glyphs = n_bases + n_cands
_WORDS = {2: "two", 3: "three", 4: "four"}
sizes_words = " or ".join(_WORDS.get(k, str(k)) for k in sorted({len(c) for _, c in bases}))
groups = {}
for b, _ in bases:
    groups[N["icon:" + b]["group"]] = groups.get(N["icon:" + b]["group"], 0) + 1
names_per_base = {b: sorted({N["icon:" + c]["name"] for c in cands}) for b, cands in bases}
if any(len(v) != 1 for v in names_per_base.values()):
    raise SystemExit("REFUSED — a base's candidates do not share one Figma name: "
                     + json.dumps({k: v for k, v in names_per_base.items() if len(v) != 1}))

# The ruling's figures are asserted, not read.
assert n_bases == 15, f"expected 15 bases from the declared nulls, derived {n_bases}"
assert n_cands == 31, f"expected 31 candidates from the declared nulls, derived {n_cands}"

_IDRX = re.compile(r'(\bid="|url\(#)([A-Za-z0-9_:.\-]+)')


def svg_text(slug):
    rel = N["icon:" + slug]["file"]
    f = ICONS / rel
    if not f.is_file():
        raise SystemExit(f"REFUSED — {rel} named by the node file is not on disk")
    s = f.read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s).strip()
    if "currentColor" not in s:
        raise SystemExit(f"REFUSED — {rel} does not paint with currentColor; the chrome panes "
                         "could not invert it")
    return s


SVG = {}
for b, cands in bases:
    for s in [b] + cands:
        SVG[s] = svg_text(s)


def glyph(slug, px, tag):
    s = SVG[slug]
    s = _IDRX.sub(lambda m: m.group(1) + tag + "-" + m.group(2), s)
    s = re.sub(r'\s(?:width|height)="[^"]*"', "", s, count=2)
    s = s.replace("<svg", f'<svg class="g g{px}" width="{px}" height="{px}" aria-hidden="true" '
                          'focusable="false"', 1)
    return s


def pane(slug, chrome):
    tag = f"{slug}-{chrome}"
    return (f'<div class="pane {chrome}">'
            f'{glyph(slug, 48, tag + "-48")}{glyph(slug, 16, tag + "-16")}'
            f'</div>')


def chrome_pair(slug, alt):
    return (f'<div class="pair" role="img" aria-label="{alt}">'
            f'{pane(slug, "lt")}{pane(slug, "dk")}</div>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


CSS = """
:root{
 --accent:#DA1A00; --ink:#000; --paper:#fff;
 --g1:#F3F3F3; --g2:#EDEDED; --g3:#D7D8D6; --g6:#767676; --g7:#545454; --g8:#333;
 --rule:#EDEDED; --soft:#F3F3F3; --muted:#545454;
 --chrome-lt:#fff; --chrome-lt-ink:#333333; --chrome-dk:#111; --chrome-dk-ink:#F2F2F2;
 --max:1200px;
 --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
 --font:"Univers Next for HSBC","Univers Next","Helvetica Neue",Helvetica,Arial,sans-serif;
 --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
 color-scheme:light;
}
@media (prefers-color-scheme:dark){
 :root:not([data-theme="light"]){
  --accent:#F6604C; --ink:#F2F2F2; --paper:#111;
  --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g6:#9B9B9B; --g7:#B7B7B7; --g8:#D7D8D6;
  --rule:#2A2A2A; --soft:#1A1A1A; --muted:#B7B7B7; color-scheme:dark;
 }
}
:root[data-theme="dark"]{
 --accent:#F6604C; --ink:#F2F2F2; --paper:#111;
 --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g6:#9B9B9B; --g7:#B7B7B7; --g8:#D7D8D6;
 --rule:#2A2A2A; --soft:#1A1A1A; --muted:#B7B7B7; color-scheme:dark;
}
*{box-sizing:border-box}
html{scroll-padding-top:4.5rem}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font);
 font-size:1rem;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--max);margin:0 auto;padding-left:var(--s4);padding-right:var(--s4)}
@media (max-width:520px){.wrap{padding-left:var(--s2);padding-right:var(--s2)}}
p{margin:0 0 var(--s2);max-width:72ch}
code{font-family:var(--mono);font-size:.86em;background:var(--soft);padding:.08em .3em;
 border-radius:2px;overflow-wrap:anywhere}
a{color:var(--accent)}

/* nav — sticky, the progress lives here */
nav{position:sticky;top:0;z-index:5;background:var(--paper);border-bottom:1px solid var(--rule)}
nav .wrap{display:flex;align-items:center;gap:var(--s3);min-height:56px;flex-wrap:wrap;
 padding-top:.5rem;padding-bottom:.5rem}
.brand{font-size:.8125rem;letter-spacing:.06em;color:var(--g6);white-space:nowrap}
.prog{flex:1 1 auto;display:flex;align-items:center;gap:var(--s2);min-width:12rem}
.prog b{font-weight:500;font-variant-numeric:tabular-nums;white-space:nowrap;font-size:.9375rem}
.track{flex:1 1 auto;height:2px;background:var(--g2);position:relative;min-width:4rem}
.track i{position:absolute;left:0;top:0;bottom:0;background:var(--accent);width:0;
 transition:width .25s ease}
.navbtns{display:flex;gap:var(--s1)}
button{font:inherit;font-size:.8125rem;letter-spacing:.06em;text-transform:uppercase;font-weight:500;
 padding:.55rem 1rem;cursor:pointer;background:var(--paper);color:var(--ink);
 border:1px solid var(--ink);border-radius:0}
button.primary{background:var(--ink);color:var(--paper)}
button.primary:hover{background:var(--g8)}
button:hover{background:var(--ink);color:var(--paper)}
button.ghost{border-color:var(--g3);color:var(--muted)}
button.ghost:hover{background:var(--paper);color:var(--ink);border-color:var(--ink)}
@media (max-width:640px){.brand{display:none}nav .wrap{gap:var(--s2);flex-wrap:nowrap}.prog{min-width:0}
 button{padding:.5rem .75rem}}

/* hero */
header.hero{padding-block:var(--s6) var(--s5)}
.label{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;line-height:1.6;
 color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:0 0 20px}
h1{font-size:3.5625rem;line-height:1.08;font-weight:400;letter-spacing:0;margin:0 0 var(--s4);max-width:20ch}
@media (max-width:760px){h1{font-size:2.125rem}}
.lede{display:grid;grid-template-columns:3fr 1fr 4fr;gap:var(--s5);align-items:start}
.lede .div{border-left:1px solid var(--g3);min-height:120px}
.lede p{max-width:60ch}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g2);
 border:1px solid var(--g2);margin:var(--s4) 0 0}
.stat{background:var(--paper);padding:var(--s3);min-width:0}
.stat b{display:block;font-size:2.6875rem;font-weight:200;line-height:1.2;
 font-variant-numeric:tabular-nums;margin-bottom:var(--s1)}
.stat span{display:block;font-size:.8125rem;letter-spacing:.04em;line-height:1.5;color:var(--g6)}
@media (max-width:900px){.lede{grid-template-columns:1fr;gap:var(--s3)}.lede .div{display:none}}
@media (max-width:760px){.stats{grid-template-columns:repeat(2,1fr)}.stat b{font-size:1.875rem}}
.how{border-top:1px solid var(--g2);margin-top:var(--s4);padding-top:var(--s3);
 display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s3)}
.how div{font-size:.875rem;line-height:1.6;color:var(--muted)}
.how b{display:block;color:var(--ink);font-weight:500;margin-bottom:.2rem}
@media (max-width:760px){.how{grid-template-columns:1fr}}

/* rows */
section.base{border-top:1px solid var(--g3);padding-block:var(--s5)}
section.base:first-of-type{border-top:2px solid var(--ink)}
.row{display:grid;grid-template-columns:1fr 2fr;gap:var(--s5);align-items:start}
@media (max-width:900px){.row{grid-template-columns:1fr;gap:var(--s3)}}
.idx{font-size:2.6875rem;font-weight:200;line-height:1;color:var(--g3);font-variant-numeric:tabular-nums;
 margin:0 0 var(--s2)}
.bname{font-size:1.1875rem;font-weight:500;line-height:1.3;margin:0}
.bslug{font-family:var(--mono);font-size:.8125rem;color:var(--muted);display:block;margin:.15rem 0 var(--s2);
 overflow-wrap:anywhere}
.meta{font-size:.75rem;letter-spacing:.04em;line-height:1.6;color:var(--g6);margin:0}
.meta b{color:var(--ink);font-weight:500}
.state{display:inline-block;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;font-weight:500;
 color:var(--g6);margin-top:var(--s2)}
.state.done{color:var(--accent)}
.cands{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:var(--s2)}
.card{border:1px solid var(--g3);padding:var(--s2);min-width:0;background:var(--paper)}
.card.on{border-color:var(--ink)}
.card.chosen{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
.card .cap{margin-top:var(--s2);line-height:1.4}
.card .cs{display:block;font-family:var(--mono);font-size:.8125rem;font-weight:500;overflow-wrap:anywhere}
.card .cn{display:block;font-size:.75rem;color:var(--g6);letter-spacing:.02em;margin-top:.15rem}
.card .ck{display:block;font-size:.6875rem;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);
 margin-top:.35rem}
.card.base .ck{color:var(--ink)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--g3);border:1px solid var(--g3)}
.pane{display:flex;align-items:flex-end;justify-content:center;gap:12px;padding:14px 8px 12px}
.pane.lt{background:var(--chrome-lt);color:var(--chrome-lt-ink)}
.pane.dk{background:var(--chrome-dk);color:var(--chrome-dk-ink)}
svg.g{display:block;flex:0 0 auto}
svg.g48{width:48px;height:48px}
svg.g16{width:16px;height:16px;margin-bottom:1px}
.basecard{margin-top:var(--s2)}

/* the ask */
.ask{margin-top:var(--s3);border-top:1px solid var(--g2);padding-top:var(--s2)}
.ask ul{list-style:none;margin:0;padding:0}
.ask li{padding:.55rem 0;border-bottom:1px solid var(--rule)}
.ask li:last-child{border-bottom:0}
.opt{display:grid;grid-template-columns:auto 1fr;gap:var(--s2);align-items:start}
.opt input{margin-top:.45rem;accent-color:var(--accent);width:16px;height:16px;flex:0 0 16px}
.opt label{cursor:pointer}
.okey{font-family:var(--mono);font-weight:500}
.flags{margin:.4rem 0 0 calc(16px + var(--s2));display:flex;flex-wrap:wrap;gap:.3rem var(--s3)}
.flags label{display:inline-flex;align-items:center;gap:.5rem;font-size:.875rem;cursor:pointer}
.flags input{accent-color:var(--accent);width:15px;height:15px;margin:0}
.flags .okey{font-size:.8125rem}
.flaghint{font-size:.8125rem;color:var(--muted);margin:.2rem 0 0 calc(16px + var(--s2));max-width:60ch}
textarea{width:100%;max-width:100%;font:inherit;font-size:.875rem;margin-top:var(--s2);
 padding:var(--s1) var(--s2);border:1px solid var(--g3);background:var(--paper);
 color:var(--ink);border-radius:0;resize:vertical;min-height:2.6rem}
textarea:focus,button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

/* export */
section.export{border-top:2px solid var(--ink);padding-block:var(--s5)}
.bar{display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center}
.said{font-size:.8125rem;color:var(--g6)}
pre.exp{white-space:pre-wrap;word-break:break-word;background:var(--soft);border:1px solid var(--g2);
 padding:var(--s2);font-size:.8125rem;line-height:1.5;max-height:22rem;overflow:auto;margin-top:var(--s3);
 font-family:var(--mono)}
footer{border-top:1px solid var(--g3);padding-block:var(--s4);font-size:.8125rem;color:var(--muted)}
footer p{max-width:none}
"""

# --------------------------------------------------------------------------- rows
rows = []
for i, (b, cands) in enumerate(bases, 1):
    bn = N["icon:" + b]
    fig_name = names_per_base[b][0]
    cards = [
        '<div class="card base">'
        + chrome_pair(b, f"{b}, the base, on light and dark")
        + f'<div class="cap"><span class="cs">{esc(b)}</span>'
          f'<span class="cn">{esc(bn["name"])} &middot; {esc(bn["fillMode"])} &middot; {esc(bn["group"])}</span>'
          f'<span class="ck">the base &mdash; inactive</span></div></div>'
    ]
    for c in cands:
        cn = N["icon:" + c]
        cards.append(
            f'<div class="card on" data-cand="{esc(c)}">'
            + chrome_pair(c, f"{c}, a candidate, on light and dark")
            + f'<div class="cap"><span class="cs">{esc(c)}</span>'
              f'<span class="cn">{esc(cn["name"])} &middot; {esc(cn["fillMode"])} &middot; {esc(cn["group"])}</span>'
              f'<span class="ck">candidate {cands.index(c) + 1} of {len(cands)}</span></div></div>')

    opts = []
    for c in cands:
        oid = f"{b}--twin--{c}"
        opts.append(f'<li><div class="opt"><input type="radio" name="{esc(b)}" id="{esc(oid)}" '
                    f'value="twin" data-twin="{esc(c)}">'
                    f'<label for="{esc(oid)}"><span class="okey">{esc(c)}</span> is the active twin of '
                    f'<span class="okey">{esc(b)}</span>.</label></div></li>')
    opts.append(f'<li><div class="opt"><input type="radio" name="{esc(b)}" id="{esc(b)}--none" value="none">'
                f'<label for="{esc(b)}--none">None of these is the twin.</label></div></li>')
    boxes = "".join(
        f'<label><input type="checkbox" name="{esc(b)}--flag" value="{esc(c)}" data-base="{esc(b)}">'
        f'<span class="okey">{esc(c)}</span></label>' for c in cands)
    opts.append(f'<li><div class="opt"><input type="radio" name="{esc(b)}" id="{esc(b)}--flag" value="flag">'
                f'<label for="{esc(b)}--flag">Flag: a drawing here is its own icon and needs an inactive '
                f'version drawn.</label></div>'
                f'<div class="flags">{boxes}</div>'
                f'<p class="flaghint">Tick every drawing that is its own icon. Ticking one selects this answer.</p></li>')

    rows.append(f"""<section class="base" id="base-{esc(b)}" data-base="{esc(b)}">
<div class="wrap"><div class="row">
<div class="left">
<p class="idx">{i:02d}</p>
<h2 class="bname">{esc(bn["name"])}</h2>
<span class="bslug">{esc(b)}</span>
<p class="meta">{len(cands)} drawings exported as <b>&ldquo;{esc(fig_name)}&rdquo;</b><br>
{esc(bn["group"])} &middot; {esc(bn["fillMode"])}</p>
<span class="state" data-state="{esc(b)}">undecided</span>
</div>
<div class="right">
<div class="cands">{"".join(cards)}</div>
<div class="ask">
<ul>{"".join(opts)}</ul>
<textarea class="note" data-base="{esc(b)}" aria-label="Note for {esc(b)}" placeholder="Note for {esc(b)} &mdash; your words, optional"></textarea>
</div>
</div>
</div></div>
</section>""")

BASE_IDS = [b for b, _ in bases]
CANDS = {b: c for b, c in bases}
group_line = " &middot; ".join(f"{esc(g)} {c}" for g, c in sorted(groups.items(), key=lambda kv: (-kv[1], kv[0])))

JS = r"""
(function(){
 var KEY=__KEY__;
 var PAGE=__PAGE__;
 var FILE=__FILE__;
 var IDS=__IDS__;
 var CANDS=__CANDS__;
 var state={};
 var lastSaved=null;
 function el(id){return document.getElementById(id);}
 function q(s,r){return (r||document).querySelector(s);}
 function qa(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));}
 function load(){
  try{var raw=localStorage.getItem(KEY);
   if(raw){var o=JSON.parse(raw);
    if(o&&typeof o==="object"){state=o.answers||{};lastSaved=o.at||null;}}}
  catch(e){state={};}
  if(!state||typeof state!=="object")state={};
 }
 function save(){
  lastSaved=new Date().toISOString();
  try{localStorage.setItem(KEY,JSON.stringify({answers:state,at:lastSaved}));}catch(e){}
  paint();
 }
 function two(v){return (v<10?"0":"")+v;}
 function rec(b){
  var r=state[b]||{};
  return {choice:r.choice||null,twin:r.twin||null,flags:(r.flags||[]).slice(),note:r.note||""};
 }
 function decided(b){return !!rec(b).choice;}
 function paint(){
  var done=0;
  IDS.forEach(function(b){
   var d=decided(b);if(d)done++;
   var s=q('.state[data-state="'+b+'"]');
   if(s){var r=rec(b);
    s.textContent=!d?"undecided":(r.choice==="twin"?"twin: "+r.twin:(r.choice==="none"?"no twin":"flagged"+(r.flags.length?" · "+r.flags.length:"")));
    s.className="state"+(d?" done":"");}
   var sec=q('section[data-base="'+b+'"]');
   if(sec){qa(".card.on",sec).forEach(function(c){
     c.classList.toggle("chosen",r&&r.choice==="twin"&&c.dataset.cand===r.twin);});}
   var r=rec(b);
  });
  var t="";
  if(lastSaved){try{var d=new Date(lastSaved);t=" · saved "+two(d.getHours())+":"+two(d.getMinutes());}catch(e){}}
  var txt=done+" of "+IDS.length+" decided";
  el("prog").textContent=txt;
  el("bar").style.width=(IDS.length?Math.round(100*done/IDS.length):0)+"%";
  el("said").textContent=txt+t;
 }
 function put(b,k,v){
  var r=state[b]||{};r[k]=v;r.at=new Date().toISOString();
  if(!r.choice&&!r.note&&!(r.flags&&r.flags.length)){delete state[b];}else{state[b]=r;}
 }
 function restore(){
  IDS.forEach(function(b){
   var r=rec(b);
   if(r.choice==="twin"&&r.twin){var i=q('input[name="'+b+'"][value="twin"][data-twin="'+r.twin+'"]');if(i)i.checked=true;}
   else if(r.choice){var j=q('input[name="'+b+'"][value="'+r.choice+'"]');if(j)j.checked=true;}
   qa('input[name="'+b+'--flag"]').forEach(function(c){c.checked=r.flags.indexOf(c.value)>-1;});
   var ta=q('textarea.note[data-base="'+b+'"]');if(ta&&r.note)ta.value=r.note;
  });
 }
 function exportObj(){
  var now=new Date().toISOString();
  var answers={};
  IDS.forEach(function(b){answers[b]=rec(b);});
  return {page:PAGE,at:now,exportedAt:now,answers:answers};
 }
 function show(){
  var j=JSON.stringify(exportObj(),null,2);
  var p=el("exp");p.hidden=false;p.textContent=j;return j;
 }
 document.addEventListener("change",function(e){
  var t=e.target;
  if(t.type==="radio"&&IDS.indexOf(t.name)>-1){
   put(t.name,"choice",t.value||null);
   put(t.name,"twin",t.value==="twin"?(t.dataset.twin||null):null);
   save();return;
  }
  if(t.type==="checkbox"&&t.dataset.base){
   var b=t.dataset.base;
   var flags=qa('input[name="'+b+'--flag"]').filter(function(c){return c.checked;}).map(function(c){return c.value;});
   put(b,"flags",flags);
   if(flags.length){var fr=q('input[name="'+b+'"][value="flag"]');if(fr&&!fr.checked){fr.checked=true;}
    put(b,"choice","flag");put(b,"twin",null);}
   save();
  }
 });
 var timer=null;
 document.addEventListener("input",function(e){
  var t=e.target;
  if(t.classList&&t.classList.contains("note")){
   put(t.dataset.base,"note",t.value);
   clearTimeout(timer);timer=setTimeout(save,400);
  }
 });
 document.addEventListener("focusout",function(e){
  var t=e.target;
  if(t.classList&&t.classList.contains("note")){clearTimeout(timer);save();}
 });
 window.addEventListener("beforeunload",function(){clearTimeout(timer);save();});
 function doExport(){
  var j=show();
  try{
   var a=document.createElement("a");
   a.href=URL.createObjectURL(new Blob([j],{type:"application/json"}));
   a.download=FILE;
   document.body.appendChild(a);a.click();
   setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},1500);
  }catch(e){}
  el("exp").scrollIntoView({behavior:"smooth",block:"nearest"});
 }
 el("btnExport").addEventListener("click",doExport);
 el("btnExportTop").addEventListener("click",doExport);
 el("btnCopy").addEventListener("click",function(){
  var j=show();var b=el("btnCopy");
  function ok(){b.textContent="Copied";setTimeout(function(){b.textContent="Copy JSON";},1600);}
  try{
   if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(j).then(ok,function(){ok();});return;
   }
  }catch(e){}
  try{var t=el("exp");var r=document.createRange();r.selectNodeContents(t);
   var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand("copy");ok();}catch(e){}
 });
 el("btnClear").addEventListener("click",function(){
  if(!confirm("Clear every answer and note on this page?"))return;
  state={};try{localStorage.removeItem(KEY);}catch(e){}
  qa('input[type="radio"],input[type="checkbox"]').forEach(function(i){i.checked=false;});
  qa("textarea.note").forEach(function(t){t.value="";});
  el("exp").hidden=true;save();
 });
 window.__reviewExport=exportObj;
 load();restore();paint();
})();
"""
JS = (JS.replace("__KEY__", json.dumps(STORAGE_KEY))
        .replace("__PAGE__", json.dumps(PAGE_ID))
        .replace("__FILE__", json.dumps(EXPORT_FILENAME))
        .replace("__IDS__", json.dumps(BASE_IDS))
        .replace("__CANDS__", json.dumps(CANDS)))

measured = {
    "bases": n_bases, "candidates": n_cands, "glyphs": n_glyphs,
    "bases_with_two": n_two, "bases_with_three": n_three,
    "groups": groups, "page": PAGE_ID, "storage_key": STORAGE_KEY,
    "export_filename": EXPORT_FILENAME, "node_file": str(NODES.relative_to(REPO)),
    "ratified": pay.get("ratified"),
}

HTML = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Active twins review</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(measured, ensure_ascii=False)}</script>
<nav><div class="wrap">
<span class="brand">Icons &middot; active twins &middot; {DATE}</span>
<div class="prog" aria-live="polite"><b id="prog">0 of {n_bases} decided</b><div class="track"><i id="bar"></i></div></div>
<div class="navbtns"><button class="primary" id="btnExportTop">Export</button></div>
</div></nav>

<header class="hero"><div class="wrap">
<p class="label">Your review &middot; the active twins</p>
<h1>{n_bases} icons each have {sizes_words} &ldquo;active&rdquo; drawings. Which one is the twin?</h1>
<div class="lede">
<p>Every icon in the library is meant to have one inactive drawing and one active twin. For these
{n_bases}, the export brought back {n_cands} drawings all named &ldquo;&hellip;&nbsp;Active&rdquo; &mdash;
{n_two} icons with two, {n_three} with three. The file names below carry a <code>-2</code> or
<code>-3</code> only because two files could not share a name; the order says which one the
export met first, nothing more. Nobody has yet looked and said which drawing is the twin.</p>
<div class="div"></div>
<p>So this sheet makes no suggestion. Each row shows the base and its candidates at the two sizes
they are used at, on a light chrome and a dark one. You decide per row: name the twin, say none
of them is, or flag a drawing that is its own icon and needs an inactive version drawn. Answers
stay in this browser as you go; <b>Export</b> at the end writes a file to hand back.</p>
</div>
<div class="stats">
<div class="stat"><b>{n_bases}</b><span>icon bases to decide</span></div>
<div class="stat"><b>{n_cands}</b><span>&ldquo;active&rdquo; drawings, {n_two}&times;2 + {n_three}&times;3</span></div>
<div class="stat"><b>{n_glyphs}</b><span>glyphs on this sheet, live from the library</span></div>
<div class="stat"><b>0</b><span>defaults set until you decide</span></div>
</div>
<div class="how">
<div><b>Name the twin</b>The drawing that is the base pressed, hovered, or selected &mdash; the same
picture, filled or emphasised.</div>
<div><b>None of these</b>Every candidate is something other than this base&rsquo;s active state.
The base keeps no default.</div>
<div><b>Flag a drawing</b>It is a different icon under a wrong name and needs its own inactive
version. Tick the ones that are.</div>
</div>
<p class="meta" style="margin-top:var(--s3)">By group: {group_line}.</p>
</div></header>

{"".join(rows)}

<section class="export" id="export"><div class="wrap">
<p class="label">Hand it back</p>
<div class="bar">
<button class="primary" id="btnExport">Export JSON</button>
<button id="btnCopy">Copy JSON</button>
<button class="ghost" id="btnClear">Clear all</button>
<span class="said" id="said"></span>
</div>
<p style="margin-top:var(--s3);font-size:.875rem;color:var(--muted)">Export writes
<code>{EXPORT_FILENAME}</code> and shows the same text below. Rows you have not decided export
with an empty answer, so a partial review is still a valid file.</p>
<pre class="exp" id="exp" hidden></pre>
</div></section>

<footer><div class="wrap">
<p>Built by <code>notes/_lanes/279/active-review/_build_review.py</code> from
<code>{measured["node_file"]}</code> and the files under <code>knowledge/assets/icons/</code>.
Instrument for the manual review under <code>{RULING}</code>; nothing here is landed.</p>
</div></footer>

<script>{JS}</script>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")

# Gate: the inline script parses (node --check on an extracted copy, in a temp dir).
import subprocess
import tempfile
with tempfile.TemporaryDirectory() as td:
    js_path = Path(td) / "inline.js"
    js_path.write_text(JS, encoding="utf-8")
    r = subprocess.run(["node", "--check", str(js_path)], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("REFUSED — inline script does not parse:\n" + r.stderr)
print("node --check: inline script OK")
print(f"wrote {OUT.name} ({len(HTML):,} bytes) · {n_bases} bases · {n_cands} candidates "
      f"({n_two}×2 + {n_three}×3) · {n_glyphs} glyphs · groups {groups}")
