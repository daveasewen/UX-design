#!/usr/bin/env python3
"""_build_ask.py — bake ASK-2026-09-16.html: the rows of Dave's active review that are not his sentence.

  python3 notes/_lanes/280/inscribe-active/_build_ask.py

Nine of his fifteen rows were inscribed by `_inscribe.py` because his tick, his note and the twin he
named all said the same thing. Six did not: on those his note says one thing and his tick another, or
he wrote that he was not certain. Nothing was written down from them. This page puts each of those six
back to him as ONE question with his own words quoted beside it.

Everything on the page is DERIVED here — which rows are asked, which drawings, the glyph markup, the
Figma name, the group, his flag, his twin and his note — from knowledge/_icon_nodes.json (the rows
still in its `unresolved` ledger), his export, and the SVG files the node file names. The question and
its answers are the only authored copy, and each answer names the drawings it would write down.

Export envelope: the #279 sheet's, unchanged —
  {page, at, exportedAt, answers: {<base>: {choice, twin, flags: [...], note}}}
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _inscribe  # noqa: E402  (the classifier is the single source of which rows are asked)

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
K = REPO / "knowledge"
ICONS = K / "assets" / "icons"
OUT = LANE / "ASK-2026-09-16.html"

PAGE_ID = "ASK-active-2026-09-16"
STORAGE_KEY = "apollo.ask.active.2026-09-16"
EXPORT_FILENAME = "DAVE-EXPORT-ask-active-2026-09-16.json"
RULING = "s277-D6"          # footer only — never in the body copy
DATE = "2026-09-16"

pay, ex, cands, verdicts = _inscribe.derive()
ASK = [b for b in sorted(verdicts) if verdicts[b]["verdict"] == "ASK"]
INSCRIBED = [b for b in sorted(verdicts) if verdicts[b]["verdict"] == "INSCRIBE"]
N = {n["id"]: n for n in pay["nodes"] if n.get("type") == "icon"}
AT = ex.get("exportedAt") or ex.get("at")

# every asked row must still be a declared null in the file — this page is the proof nothing moved
_nulls = {u["source"] for u in pay["unresolved"] if u["type"] == "defaultActive"}
assert _nulls == {"icon:" + b for b in ASK}, "the asked rows and the file's declared nulls differ"


# --------------------------------------------------------------------------- the questions
def Q(base):
    """(question, [(key, answer copy, twin|None, [flags])]) — authored, with the slugs derived."""
    v = verdicts[base]
    c = v["cands"]
    twin = v["twin"]
    flags = v["flags"]
    wrong = v["wrong"]
    other = [x for x in c if x != twin]

    if base == "jade-lifestyle":
        return ("You named <b>%s</b> as the active twin, and then wrote that you were not certain and "
                "that both the base drawing and <b>%s</b> are mislabelled — does that twin stand, "
                "or is this row still open?" % (twin, twin),
                [("twin-" + twin, "<b>%s</b> is the twin after all." % twin, twin, []),
                 ("twin-" + other[0], "<b>%s</b> is the twin, not %s." % (other[0], twin), other[0], []),
                 ("own-icon", "Neither is a twin: the base drawing and <b>%s</b> are a different icon "
                              "under the wrong name, and both go on the list of drawings that need an "
                              "inactive version." % twin, None, [twin]),
                 ("open", "Still open — leave this row alone, I want to look at it again.", None, [])])

    if base == "electricity":
        return ("You named <b>%s</b> as the twin and then ticked that same drawing as one that is its "
                "own icon, while your note names <b>%s</b> as the mislabelled one — which did you "
                "mean?" % (twin, wrong[0]),
                [("note", "My note: <b>%s</b> is the twin, and <b>%s</b> is the one that is its own "
                          "icon and needs an inactive version drawn." % (twin, wrong[0]), twin, [wrong[0]]),
                 ("tick", "My tick: <b>%s</b> is itself a different icon, so this base has no twin yet "
                          "and <b>%s</b> is fine as it is." % (twin, wrong[0]), None, [twin]),
                 ("both", "Both of them are their own icon — this base has no active twin at all.",
                  None, list(c)),
                 ("open", "Neither — leave this row alone, I want to look at it again.", None, [])])

    if base == "traditional-chinese-medicine":
        tick = flags[0]
        return ("You ticked <b>%s</b> as a drawing that is its own icon, but your note says that one is "
                "correctly labelled and that the base drawing and <b>%s</b> — the twin you named "
                "— are the mislabelled ones; which reading is right?" % (tick, twin),
                [("note", "My note: <b>%s</b> is correctly labelled and is the twin; the base drawing "
                          "and <b>%s</b> are a different icon under the wrong name." % (tick, twin),
                  tick, [twin]),
                 ("tick", "My tick: <b>%s</b> is the twin as I first said, and <b>%s</b> is its own "
                          "icon and needs an inactive version drawn." % (twin, tick), twin, [tick]),
                 ("open", "Neither — leave this row alone, I want to look at it again.", None, [])])

    # the note-only rows: a twin named, a mislabel written, nothing ticked
    w = wrong[0]
    return ("You named <b>%s</b> as the twin and wrote that <b>%s</b> is mislabelled, but you did not "
            "tick it — should <b>%s</b> be written down as its own icon that needs an inactive "
            "version drawn?" % (twin, w, w),
            [("yes", "Yes: <b>%s</b> is the twin, and <b>%s</b> is its own icon — put it on the "
                     "list." % (twin, w), twin, [w]),
             ("name-only", "No: <b>%s</b> is the twin, and <b>%s</b> is the right picture under a wrong "
                           "name — nothing new needs drawing." % (twin, w), twin, []),
             ("open", "Neither — leave this row alone, I want to look at it again.", None, [])])


QUESTIONS = {b: Q(b) for b in ASK}
assert all(len(opts) >= 3 for _, opts in QUESTIONS.values())

# --------------------------------------------------------------------------- glyphs
_IDRX = re.compile(r'(\bid="|url\(#)([A-Za-z0-9_:.\-]+)')


def svg_text(slug):
    rel = N["icon:" + slug]["file"]
    f = ICONS / rel
    if not f.is_file():
        raise SystemExit("REFUSED — %s named by the node file is not on disk" % rel)
    s = re.sub(r"<\?xml[^>]*\?>", "", f.read_text(encoding="utf-8")).strip()
    if "currentColor" not in s:
        raise SystemExit("REFUSED — %s does not paint with currentColor" % rel)
    return s


SVG = {s: svg_text(s) for b in ASK for s in [b] + verdicts[b]["cands"]}
n_glyphs = len(SVG)
n_cands = sum(len(verdicts[b]["cands"]) for b in ASK)


def glyph(slug, px, tag):
    s = _IDRX.sub(lambda m: m.group(1) + tag + "-" + m.group(2), SVG[slug])
    s = re.sub(r'\s(?:width|height)="[^"]*"', "", s, count=2)
    return s.replace("<svg", '<svg class="g g%d" width="%d" height="%d" aria-hidden="true" '
                             'focusable="false"' % (px, px, px), 1)


def pane(slug, chrome):
    tag = "%s-%s" % (slug, chrome)
    return ('<div class="pane %s">%s%s</div>'
            % (chrome, glyph(slug, 48, tag + "-48"), glyph(slug, 16, tag + "-16")))


def chrome_pair(slug, alt):
    return ('<div class="pair" role="img" aria-label="%s">%s%s</div>'
            % (alt, pane(slug, "lt"), pane(slug, "dk")))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


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
b{font-weight:500}
nav{position:sticky;top:0;z-index:5;background:var(--paper);border-bottom:1px solid var(--rule)}
nav .wrap{display:flex;align-items:center;gap:var(--s3);min-height:56px;flex-wrap:nowrap;
 padding-top:.5rem;padding-bottom:.5rem}
.brand{font-size:.8125rem;letter-spacing:.06em;color:var(--g6);white-space:nowrap}
.prog{flex:1 1 auto;display:flex;align-items:center;gap:var(--s2);min-width:0}
.prog b{font-weight:500;font-variant-numeric:tabular-nums;white-space:nowrap;font-size:.9375rem}
.track{flex:1 1 auto;height:2px;background:var(--g2);position:relative;min-width:3rem}
.track i{position:absolute;left:0;top:0;bottom:0;background:var(--accent);width:0;transition:width .25s ease}
button{font:inherit;font-size:.8125rem;letter-spacing:.06em;text-transform:uppercase;font-weight:500;
 padding:.55rem 1rem;cursor:pointer;background:var(--paper);color:var(--ink);
 border:1px solid var(--ink);border-radius:0;white-space:nowrap}
button.primary{background:var(--ink);color:var(--paper)}
button.primary:hover{background:var(--g8)}
button:hover{background:var(--ink);color:var(--paper)}
button.ghost{border-color:var(--g3);color:var(--muted)}
button.ghost:hover{background:var(--paper);color:var(--ink);border-color:var(--ink)}
@media (max-width:640px){.brand{display:none}nav .wrap{gap:var(--s2)}button{padding:.5rem .75rem}}
header.hero{padding-block:var(--s6) var(--s5)}
.label{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;line-height:1.6;
 color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:0 0 20px}
h1{font-size:3.5625rem;line-height:1.08;font-weight:400;margin:0 0 var(--s4);max-width:20ch}
@media (max-width:760px){h1{font-size:2.125rem}}
.lede{display:grid;grid-template-columns:3fr 1fr 4fr;gap:var(--s5);align-items:start}
.lede .div{border-left:1px solid var(--g3);min-height:120px}
.lede p{max-width:60ch}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--g2);
 border:1px solid var(--g2);margin:var(--s4) 0 0}
.stat{background:var(--paper);padding:var(--s3);min-width:0}
.stat b{display:block;font-size:2.6875rem;font-weight:200;line-height:1.2;
 font-variant-numeric:tabular-nums;margin-bottom:var(--s1)}
.stat span{display:block;font-size:.8125rem;letter-spacing:.04em;line-height:1.5;color:var(--g6)}
@media (max-width:900px){.lede{grid-template-columns:1fr;gap:var(--s3)}.lede .div{display:none}}
@media (max-width:760px){.stats{grid-template-columns:1fr}.stat b{font-size:1.875rem}}
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
.meta b{color:var(--ink)}
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
.said-you{margin-top:var(--s3);border-left:2px solid var(--g3);padding:0 0 0 var(--s2)}
.said-you dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:.2rem var(--s2)}
.said-you dt{font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);
 padding-top:.15rem;white-space:nowrap}
.said-you dd{margin:0;font-size:.9375rem;overflow-wrap:anywhere}
.said-you .quote{white-space:pre-wrap;font-style:italic}
@media (max-width:520px){.said-you dl{grid-template-columns:1fr}.said-you dt{padding-top:.5rem}}
.qn{margin-top:var(--s3);border-top:1px solid var(--g2);padding-top:var(--s3)}
.qn .q{font-size:1.1875rem;line-height:1.5;margin:0 0 var(--s2);max-width:62ch}
.qn ul{list-style:none;margin:0;padding:0}
.qn li{padding:.55rem 0;border-bottom:1px solid var(--rule)}
.qn li:last-child{border-bottom:0}
.opt{display:grid;grid-template-columns:auto 1fr;gap:var(--s2);align-items:start}
.opt input{margin-top:.45rem;accent-color:var(--accent);width:16px;height:16px;flex:0 0 16px}
.opt label{cursor:pointer}
textarea{width:100%;max-width:100%;font:inherit;font-size:.875rem;margin-top:var(--s2);
 padding:var(--s1) var(--s2);border:1px solid var(--g3);background:var(--paper);
 color:var(--ink);border-radius:0;resize:vertical;min-height:2.6rem}
textarea:focus,button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
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
for i, b in enumerate(ASK, 1):
    v = verdicts[b]
    bn = N["icon:" + b]
    fig = sorted({N["icon:" + c]["name"] for c in v["cands"]})[0]
    cards = ['<div class="card base">' + chrome_pair(b, "%s, the base, on light and dark" % b)
             + '<div class="cap"><span class="cs">%s</span><span class="cn">%s &middot; %s</span>'
               '<span class="ck">the base &mdash; inactive</span></div></div>'
             % (esc(b), esc(bn["name"]), esc(bn["group"]))]
    for j, c in enumerate(v["cands"], 1):
        cn = N["icon:" + c]
        cards.append('<div class="card on" data-cand="%s">%s'
                     '<div class="cap"><span class="cs">%s</span><span class="cn">%s &middot; %s</span>'
                     '<span class="ck">drawing %d of %d</span></div></div>'
                     % (esc(c), chrome_pair(c, "%s, a drawing, on light and dark" % c),
                        esc(c), esc(cn["name"]), esc(cn["fillMode"]), j, len(v["cands"])))

    q, opts = QUESTIONS[b]
    lis = []
    for key, copy, twin, flags in opts:
        oid = "%s--%s" % (b, key)
        lis.append('<li><div class="opt"><input type="radio" name="%s" id="%s" value="%s" '
                   'data-twin="%s" data-flags="%s"><label for="%s">%s</label></div></li>'
                   % (esc(b), esc(oid), esc(key), esc(twin or ""), esc(",".join(flags)),
                      esc(oid), copy))

    ticked = ", ".join("<code>%s</code>" % esc(f) for f in v["flags"]) or "nothing ticked"
    note = v["note"].strip() or "(no note)"
    rows.append("""<section class="base" id="base-%s" data-base="%s">
<div class="wrap"><div class="row">
<div class="left">
<p class="idx">%02d</p>
<h2 class="bname">%s</h2>
<span class="bslug">%s</span>
<p class="meta">%d drawings exported as <b>&ldquo;%s&rdquo;</b><br>%s &middot; %s</p>
<span class="state" data-state="%s">unanswered</span>
<div class="said-you"><dl>
<dt>You named</dt><dd><code>%s</code> as the twin</dd>
<dt>You ticked</dt><dd>%s</dd>
<dt>You wrote</dt><dd class="quote">%s</dd>
</dl></div>
</div>
<div class="right">
<div class="cands">%s</div>
<div class="qn">
<p class="q">%s</p>
<ul>%s</ul>
<textarea class="note" data-base="%s" aria-label="Note for %s" placeholder="Anything else about %s &mdash; your words, optional"></textarea>
</div>
</div>
</div></div>
</section>""" % (esc(b), esc(b), i, esc(bn["name"]), esc(b), len(v["cands"]), esc(fig),
                 esc(bn["group"]), esc(bn["fillMode"]), esc(b),
                 esc(v["twin"] or "—"), ticked, esc(note),
                 "".join(cards), q, "".join(lis), esc(b), esc(b), esc(b)))

JS = r"""
(function(){
 var KEY=__KEY__, PAGE=__PAGE__, FILE=__FILE__, IDS=__IDS__;
 var state={}, lastSaved=null, timer=null;
 function el(i){return document.getElementById(i);}
 function q(s,r){return (r||document).querySelector(s);}
 function qa(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));}
 function rec(b){var r=state[b]||{};return {choice:r.choice||null,twin:r.twin||null,
   flags:(r.flags||[]).slice(),note:r.note||""};}
 function load(){try{var raw=localStorage.getItem(KEY);if(raw){var o=JSON.parse(raw);
   if(o&&typeof o==="object"){state=o.answers||{};lastSaved=o.at||null;}}}catch(e){state={};}
  if(!state||typeof state!=="object")state={};}
 function save(){lastSaved=new Date().toISOString();
  try{localStorage.setItem(KEY,JSON.stringify({answers:state,at:lastSaved}));}catch(e){}paint();}
 function put(b,k,v){var r=state[b]||{};r[k]=v;r.at=new Date().toISOString();
  if(!r.choice&&!r.note&&!(r.flags&&r.flags.length)){delete state[b];}else{state[b]=r;}}
 function two(v){return (v<10?"0":"")+v;}
 function paint(){
  var done=0;
  IDS.forEach(function(b){
   var r=rec(b); if(r.choice)done++;
   var s=q('.state[data-state="'+b+'"]');
   if(s){s.textContent=r.choice?("answered"+(r.twin?" · twin: "+r.twin:"")):"unanswered";
    s.className="state"+(r.choice?" done":"");}
   var sec=q('section[data-base="'+b+'"]');
   if(sec){qa(".card.on",sec).forEach(function(c){
    c.classList.toggle("chosen",!!r.twin&&c.dataset.cand===r.twin);});}
  });
  var t="";
  if(lastSaved){try{var d=new Date(lastSaved);t=" · saved "+two(d.getHours())+":"+two(d.getMinutes());}catch(e){}}
  var txt=done+" of "+IDS.length+" answered";
  el("prog").textContent=txt;
  el("bar").style.width=(IDS.length?Math.round(100*done/IDS.length):0)+"%";
  el("said").textContent=txt+t;
 }
 function restore(){IDS.forEach(function(b){var r=rec(b);
  if(r.choice){var i=q('input[name="'+b+'"][value="'+r.choice+'"]');if(i)i.checked=true;}
  var ta=q('textarea.note[data-base="'+b+'"]');if(ta&&r.note)ta.value=r.note;});}
 function exportObj(){var now=new Date().toISOString(),answers={};
  IDS.forEach(function(b){answers[b]=rec(b);});
  return {page:PAGE,at:now,exportedAt:now,answers:answers};}
 function show(){var j=JSON.stringify(exportObj(),null,2);
  var p=el("exp");p.hidden=false;p.textContent=j;return j;}
 document.addEventListener("change",function(e){
  var t=e.target;
  if(t.type==="radio"&&IDS.indexOf(t.name)>-1){
   put(t.name,"choice",t.value||null);
   put(t.name,"twin",t.dataset.twin||null);
   put(t.name,"flags",t.dataset.flags?t.dataset.flags.split(","):[]);
   save();
  }
 });
 document.addEventListener("input",function(e){var t=e.target;
  if(t.classList&&t.classList.contains("note")){put(t.dataset.base,"note",t.value);
   clearTimeout(timer);timer=setTimeout(save,400);}});
 document.addEventListener("focusout",function(e){var t=e.target;
  if(t.classList&&t.classList.contains("note")){clearTimeout(timer);save();}});
 window.addEventListener("beforeunload",function(){clearTimeout(timer);save();});
 function doExport(){var j=show();
  try{var a=document.createElement("a");
   a.href=URL.createObjectURL(new Blob([j],{type:"application/json"}));a.download=FILE;
   document.body.appendChild(a);a.click();
   setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},1500);}catch(e){}
  el("exp").scrollIntoView({behavior:"smooth",block:"nearest"});}
 el("btnExport").addEventListener("click",doExport);
 el("btnExportTop").addEventListener("click",doExport);
 el("btnCopy").addEventListener("click",function(){var j=show(),b=el("btnCopy");
  function ok(){b.textContent="Copied";setTimeout(function(){b.textContent="Copy JSON";},1600);}
  try{if(navigator.clipboard&&navigator.clipboard.writeText){
   navigator.clipboard.writeText(j).then(ok,function(){ok();});return;}}catch(e){}
  try{var t=el("exp"),r=document.createRange();r.selectNodeContents(t);
   var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand("copy");ok();}catch(e){}});
 el("btnClear").addEventListener("click",function(){
  if(!confirm("Clear every answer and note on this page?"))return;
  state={};try{localStorage.removeItem(KEY);}catch(e){}
  qa('input[type="radio"]').forEach(function(i){i.checked=false;});
  qa("textarea.note").forEach(function(t){t.value="";});
  el("exp").hidden=true;save();});
 window.__askExport=exportObj;
 load();restore();paint();
})();
"""
JS = (JS.replace("__KEY__", json.dumps(STORAGE_KEY))
        .replace("__PAGE__", json.dumps(PAGE_ID))
        .replace("__FILE__", json.dumps(EXPORT_FILENAME))
        .replace("__IDS__", json.dumps(ASK)))

measured = {"asked": len(ASK), "inscribed": len(INSCRIBED), "reviewed": len(verdicts),
            "drawings": n_cands, "glyphs": n_glyphs, "page": PAGE_ID,
            "storage_key": STORAGE_KEY, "export_filename": EXPORT_FILENAME,
            "his_export_at": AT, "node_file": "knowledge/_icon_nodes.json",
            "bases": ASK}

HTML = """<!doctype html>
<html lang="en">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Six rows to settle</title>
<style>%(css)s</style>
<script type="application/json" id="measured">%(measured)s</script>
<nav><div class="wrap">
<span class="brand">Icons &middot; active twins &middot; %(date)s</span>
<div class="prog" aria-live="polite"><b id="prog">0 of %(n)d answered</b><div class="track"><i id="bar"></i></div></div>
<div class="navbtns"><button class="primary" id="btnExportTop">Export</button></div>
</div></nav>

<header class="hero"><div class="wrap">
<p class="label">Your review &middot; the rows that need one more word</p>
<h1>%(nword)s of your %(all)d rows say two things at once.</h1>
<div class="lede">
<p>You went through the %(all)d icons that came back with more than one &ldquo;active&rdquo; drawing and
named a twin on every one. On %(ins)d of them your tick, your note and the twin you named all agreed,
and those %(ins)d are now written into the library: the twin is the default, and the drawings you called
wrongly labelled are on the list of icons that need an inactive version drawn.</p>
<div class="div"></div>
<p>These %(n)d are the rest. On each one the drawing you ticked and the drawing your note names are not
the same drawing, or you wrote that you were not certain &mdash; so nothing was written down from them
and nothing about them has changed. Each row below shows the drawings again, quotes back exactly what
you said, and asks one question. <b>Export</b> at the end writes a file to hand back.</p>
</div>
<div class="stats">
<div class="stat"><b>%(ins)d</b><span>rows written into the library from your review</span></div>
<div class="stat"><b>%(n)d</b><span>rows waiting on one more word from you</span></div>
<div class="stat"><b>%(g)d</b><span>glyphs below, live from the library</span></div>
</div>
</div></header>

%(rows)s

<section class="export" id="export"><div class="wrap">
<p class="label">Hand it back</p>
<div class="bar">
<button class="primary" id="btnExport">Export JSON</button>
<button id="btnCopy">Copy JSON</button>
<button class="ghost" id="btnClear">Clear all</button>
<span class="said" id="said"></span>
</div>
<p style="margin-top:var(--s3);font-size:.875rem;color:var(--muted)">Export writes
<code>%(file)s</code> and shows the same text below. Rows you have not answered export with an empty
answer, so a partial file is still a valid one.</p>
<pre class="exp" id="exp" hidden></pre>
</div></section>

<footer><div class="wrap">
<p>Built by <code>notes/_lanes/280/inscribe-active/_build_ask.py</code> from
<code>%(nodes)s</code>, your export of %(at)s and the files under
<code>knowledge/assets/icons/</code>. The rows on this page are the ones still carrying a declared
null in the node file; the other %(ins)d were inscribed under <code>%(ruling)s</code>.</p>
</div></footer>

<script>%(js)s</script>
</html>
""" % {"css": CSS, "measured": json.dumps(measured, ensure_ascii=False), "date": DATE,
       "n": len(ASK), "all": len(verdicts), "ins": len(INSCRIBED), "g": n_glyphs,
       "nword": {4: "Four", 5: "Five", 6: "Six", 7: "Seven"}.get(len(ASK), str(len(ASK))),
       "rows": "".join(rows), "file": EXPORT_FILENAME, "nodes": measured["node_file"],
       "at": AT, "ruling": RULING, "js": JS}

# --------------------------------------------------------------------------- gates
assert RULING not in HTML.split("<footer>")[0], "a ruling id leaked into the body copy"
for b in ASK:
    assert verdicts[b]["note"].strip() in HTML or not verdicts[b]["note"].strip(), \
        "his note for %s is not quoted verbatim on the page" % b
assert HTML.count('class="card') == n_glyphs, "a glyph card is missing"
assert HTML.count("<svg") == n_glyphs * 4, "every glyph must be drawn at two sizes on two chromes"

OUT.write_text(HTML, encoding="utf-8")
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "inline.js"
    p.write_text(JS, encoding="utf-8")
    r = subprocess.run(["node", "--check", str(p)], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("REFUSED — inline script does not parse:\n" + r.stderr)
print("node --check: inline script OK")
print("wrote %s (%d bytes) · %d asked rows · %d drawings · %d glyphs × 4 renders"
      % (OUT.name, len(HTML), len(ASK), n_cands, n_glyphs))
