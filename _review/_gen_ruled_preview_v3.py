#!/usr/bin/env python3
"""Generator for _review/state-contrast-ruled-preview-v3.html (session #149, lane red 63, iter 3).

PREVIEW of RULED s130-D4 / s130-D5 — nothing here is a new choice.
Reuses the v2 embedded-snippet iframe machinery (<base> re-root, transition kill,
:hover/:active -> .fx-h/.fx-p rewrite, per-state clones).
No canon / token / gate file is touched. Nothing is committed.
"""
import base64, json, os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIPDIR = os.path.join(REPO, "knowledge", "snippets")
OUT = os.path.join(REPO, "_review", "state-contrast-ruled-preview-v3.html")

COMPS = {
    "Banner": "Banner.reference.html",
    "Selection": "Selection-controls.reference.html",
    "Tabs": "Tabs.reference.html",
}
SNIP = {}
for k, f in COMPS.items():
    with open(os.path.join(SNIPDIR, f), "rb") as fh:
        SNIP[k] = base64.b64encode(fh.read()).decode()


# ---------------------------------------------------------------- WCAG maths
def _lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def ratio(a, b):
    l1, l2 = _lum(a), _lum(b)
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + .05) / (lo + .05), 2)


def mix(fg, bg, p):
    f, b = fg.lstrip("#"), bg.lstrip("#")
    return "#" + "".join("%02X" % round(int(f[i:i + 2], 16) * p + int(b[i:i + 2], 16) * (1 - p))
                         for i in (0, 2, 4))


# ------------------------------------------------------------- ruled values
ERR_CUR = "#F6604C"       # canon.css --rag-error-background TODAY (mono, both modes)
ERR_RULED = "#B92F1E"     # s130-D4
WHITE, INK_D = "#FFFFFF", "#1A1A1A"
CUR_WASH = {"base": 0.0, "hover": 0.14, "pressed": 0.22}   # canon.css today
RULED_WASH = {"base": 0.0, "hover": 0.08, "pressed": 0.14}  # s130-D4
ERR_INK = {"light": "#DA1A00", "dark": "#F6604C"}          # rag/error-ink, s145-D1
TABS_BADGE = {"light": "#B92F1E", "dark": "#CC4333"}       # semantic-colour.json tabs/badge/background

banner_rows = []
for theme in ("light", "dark"):
    for variant, base, wash in (("current", ERR_CUR, CUR_WASH), ("ruled", ERR_RULED, RULED_WASH)):
        for st in ("base", "hover", "pressed"):
            s = mix(WHITE, base, wash[st])
            banner_rows.append({"theme": theme, "variant": variant, "state": st,
                                "fg": WHITE, "bg": s, "r": ratio(WHITE, s)})

sc_rows = []
for theme in ("light", "dark"):
    page = WHITE if theme == "light" else INK_D
    sc_rows.append({"theme": theme, "variant": "current", "part": "label",
                    "fg": ERR_CUR, "bg": page, "r": ratio(ERR_CUR, page)})
    sc_rows.append({"theme": theme, "variant": "current", "part": "message",
                    "fg": ERR_CUR, "bg": page, "r": ratio(ERR_CUR, page)})
    lab = INK_D if theme == "light" else WHITE
    sc_rows.append({"theme": theme, "variant": "ruled", "part": "label",
                    "fg": lab, "bg": page, "r": ratio(lab, page)})
    sc_rows.append({"theme": theme, "variant": "ruled", "part": "message",
                    "fg": ERR_INK[theme], "bg": page, "r": ratio(ERR_INK[theme], page)})
    sc_rows.append({"theme": theme, "variant": "ruled", "part": "box border",
                    "fg": ERR_CUR, "bg": page, "r": ratio(ERR_CUR, page)})

tabs_rows = [
    {"theme": "dark", "variant": "current", "fg": WHITE, "bg": WHITE, "r": ratio(WHITE, WHITE)},
    {"theme": "dark", "variant": "ruled", "fg": WHITE, "bg": TABS_BADGE["dark"],
     "r": ratio(WHITE, TABS_BADGE["dark"])},
    {"theme": "light", "variant": "ruled", "fg": WHITE, "bg": TABS_BADGE["light"],
     "r": ratio(WHITE, TABS_BADGE["light"])},
]

MEASURED = {"banner": banner_rows, "selection": sc_rows, "tabs": tabs_rows}

# ------------------------------------------------- per-iframe override layers
def banner_override(variant):
    if variant == "current":
        return ""
    return (
        "/* SCOPED PREVIEW OVERRIDE — s130-D4. Not written to canon.css. */\n"
        ".banner.err{--fill:%s !important}\n"
        ".banner .actions .abtn.fx-h{background:color-mix(in srgb, var(--ink) 8%%, transparent)!important}\n"
        ".banner .actions .abtn.fx-p{background:color-mix(in srgb, var(--ink) 14%%, transparent)!important}\n"
        % ERR_RULED)


def sc_override(variant, theme):
    if variant == "current":
        return ""
    return (
        "/* SCOPED PREVIEW OVERRIDE — s130-D5 (+ s145-D1 for the message ink). Not written to canon.css. */\n"
        ".field.is-error label{color:var(--label)!important}\n"
        ".field.is-error .box{border-color:var(--error)!important}\n"
        ".err-msg{color:%s !important}\n" % ERR_INK[theme])


def tabs_override(variant, theme):
    if variant == "current":
        return ""
    return ("/* SCOPED PREVIEW OVERRIDE — tabs/badge/background seating. Not written to canon.css. */\n"
            ".ovcount{background:%s !important; color:#FFFFFF !important}\n" % TABS_BADGE[theme])


FRAMES = []


def frame(card, comp, theme, variant, container, target, states, w, h, css, seed=""):
    FRAMES.append({"card": card, "comp": comp, "theme": theme, "variant": variant,
                   "container": container, "target": target, "states": states,
                   "w": w, "h": h, "css": css, "seed": seed,
                   "pair": ".err-msg" if card == "selection" else ""})


for theme in ("light", "dark"):
    for variant in ("current", "ruled"):
        frame("banner", "Banner", theme, variant, ".banner.err", ".abtn",
              ["base", "hover", "pressed"], 505, 500, banner_override(variant))
        frame("selection", "Selection", theme, variant, ".field.is-error", "label",
              ["base", "hover", "pressed"], 400, 380, sc_override(variant, theme))
for theme, variant in (("dark", "current"), ("dark", "ruled"), ("light", "ruled")):
    frame("tabs", "Tabs", theme, variant, ".overflow", ".overflow__trigger",
          ["base", "hover"], 300, 210, tabs_override(variant, theme), seed="ovcount")


def badge(r):
    ok = r >= 4.5
    return '<span class="b %s">%s:1 %s</span>' % ("pass" if ok else "fail", r, "PASS" if ok else "FAIL")


def sw(h):
    return '<span class="sw" style="background:%s"></span><span class="mono">%s</span>' % (h, h)


def banner_table():
    o = ['<table class="m"><tr><th>theme</th><th>side</th><th>state</th><th>ink</th>'
         '<th>surface under the ink</th><th>measured (WCAG)</th></tr>']
    for r in banner_rows:
        o.append('<tr class="%s"><td>%s</td><td>%s</td><td class="mono">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                 % ("vr" if r["variant"] == "ruled" else "vc", r["theme"],
                    "RULED" if r["variant"] == "ruled" else "current",
                    r["state"], sw(r["fg"]), sw(r["bg"]), badge(r["r"])))
    return "".join(o) + "</table>"


def sc_table():
    o = ['<table class="m"><tr><th>theme</th><th>side</th><th>part</th><th>colour</th>'
         '<th>ground</th><th>measured (WCAG)</th></tr>']
    for r in sc_rows:
        o.append('<tr class="%s"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                 % ("vr" if r["variant"] == "ruled" else "vc", r["theme"],
                    "RULED" if r["variant"] == "ruled" else "current",
                    r["part"], sw(r["fg"]), sw(r["bg"]), badge(r["r"])))
    return "".join(o) + "</table>"


def tabs_table():
    o = ['<table class="m"><tr><th>theme</th><th>side</th><th>numeral</th><th>badge fill</th>'
         '<th>measured (WCAG)</th></tr>']
    for r in tabs_rows:
        o.append('<tr class="%s"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                 % ("vr" if r["variant"] == "ruled" else "vc", r["theme"],
                    "RULED" if r["variant"] == "ruled" else "current",
                    sw(r["fg"]), sw(r["bg"]), badge(r["r"])))
    return "".join(o) + "</table>"


def specs(card):
    """Two rows: light pair, dark pair (tabs: whatever frames exist)."""
    out = []
    for theme in ("light", "dark"):
        fr = [f for f in FRAMES if f["card"] == card and f["theme"] == theme]
        if not fr:
            continue
        cells = []
        for f in fr:
            cls = "yes" if f["variant"] == "ruled" else "no"
            lab = ("RULED — scoped preview override" if f["variant"] == "ruled"
                   else "CURRENT — canon.css as-is")
            cells.append(
                '<div class="spec"><div class="hd %s">%s &middot; %s</div>'
                '<iframe data-frame="%s" width="%d" height="%d"></iframe></div>'
                % (cls, theme, lab, FRAMES.index(f), f["w"], f["h"]))
        out.append('<div class="specrow"><div class="rowlab">%s theme</div>'
                   '<div class="specs">%s</div></div>' % (theme, "".join(cells)))
    return "".join(out)


CSS = """
 :root{--pg:#F7F6F4;--ink:#13110E;--mut:#635750;--line:#CDC8C6;--card:#FFFFFF;--ok:#0F7A46;--bad:#B92F1E}
 *{box-sizing:border-box}
 body{margin:0;background:var(--pg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;padding:28px}
 .wrap{max-width:1180px;margin:0 auto}
 h1{font-size:26px;margin:0 0 6px} h2{font-size:19px;margin:0 0 4px}
 .sub{color:var(--mut);margin:0 0 22px;max-width:84ch}
 .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px;margin:0 0 22px}
 .ruledbar{background:#EAF1FA;border:1px solid #7FA6D4;border-radius:8px;padding:12px 14px;margin:0 0 18px;font-size:13.5px}
 .flag{background:#FFF4E5;border:1px solid #E0B978;border-radius:8px;padding:10px 12px;margin:12px 0;font-size:13.5px}
 .open{background:#F3EAFA;border:1px solid #A87FD4;border-radius:8px;padding:10px 12px;margin:12px 0;font-size:13.5px}
 .diag{font-size:14px;color:#2E2A25;margin:8px 0 14px;max-width:94ch}
 pre.rule{background:#13110E;color:#F2EFEA;padding:10px 12px;border-radius:8px;font-size:12.5px;overflow:auto;margin:0 0 14px;white-space:pre-wrap}
 table.m{border-collapse:collapse;font-size:13px;margin:0 0 16px}
 table.m th,table.m td{border:1px solid var(--line);padding:5px 9px;text-align:left}
 table.m th{background:#F2EFEA}
 tr.vr td{background:#F4FAF6} tr.vc td{background:#FFF9F8}
 .sw{display:inline-block;width:13px;height:13px;border:1px solid #999;vertical-align:-2px;margin-right:5px}
 .specrow{margin:0 0 14px}
 .rowlab{font:11px/1.4 ui-monospace,Menlo,monospace;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);margin:0 0 6px}
 .specs{display:flex;gap:16px;flex-wrap:wrap}
 .spec{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff}
 .spec > .hd{font-size:11.5px;padding:5px 9px;border-bottom:1px solid var(--line);letter-spacing:.04em;text-transform:uppercase}
 .spec > .hd.no{background:#FBE7E4;color:var(--bad)} .spec > .hd.yes{background:#E3F3EA;color:var(--ok)}
 iframe{border:0;display:block}
 .b{display:inline-block;padding:2px 7px;border-radius:999px;font-weight:600;font-size:12px}
 .b.pass{background:#E3F3EA;color:var(--ok)} .b.fail{background:#FBE7E4;color:var(--bad)}
 .mono{font-family:ui-monospace,Menlo,monospace}
 .pair{display:flex;gap:16px;flex-wrap:wrap;margin:6px 0 16px}
 .pairbox{border:1px solid var(--line);border-radius:8px;overflow:hidden;min-width:250px}
 .pairbox .hd{font-size:11.5px;padding:5px 9px;letter-spacing:.05em;text-transform:uppercase;border-bottom:1px solid var(--line)}
 .pairbox .hd.no{background:#FBE7E4;color:var(--bad)} .pairbox .hd.yes{background:#E3F3EA;color:var(--ok)}
 .pairbox .bd{padding:14px;background:#fff;font-size:14px}
 .chipm{display:inline-flex;align-items:center;gap:7px;border:1px solid #CDC8C6;border-radius:999px;padding:6px 13px;font-size:13.5px;background:#fff}
 label.lic{display:block;padding:9px 10px;border:1px solid var(--line);border-radius:8px;margin:0 0 8px;cursor:pointer;font-size:13.5px}
 label.lic:hover{background:#FAF9F7}
 label.lic input{margin-right:8px}
 button.act{appearance:none;border:0;background:var(--ink);color:#fff;padding:11px 18px;border-radius:8px;font-size:14px;cursor:pointer}
 textarea{width:100%;min-height:120px;font:12.5px/1.5 ui-monospace,Menlo,monospace;border:1px solid var(--line);border-radius:8px;padding:12px;background:#fff}
 #ruling{min-height:300px}
"""

INJ_JS = r"""
const INJ = (cfg)=>`<script>(function(){
var C=${JSON.stringify(cfg)};var d=document;
function collect(rs,out){for(var i=0;i<rs.length;i++){var r=rs[i];
 if(r.cssRules&&r.type!==1){try{var inner=[];collect(r.cssRules,inner);if(inner.length)out.push((r.conditionText?('@media '+r.conditionText):'@media all')+'{'+inner.join('\\n')+'}')}catch(e){}continue}
 if(!r.selectorText)continue;var s=r.selectorText;if(s.indexOf(':hover')<0&&s.indexOf(':active')<0)continue;
 out.push(s.split(':hover').join('.fx-h').split(':active').join('.fx-p')+'{'+r.style.cssText+'}')}}
function boot(){
 d.body.setAttribute('data-theme',C.theme);
 var s=d.createElement('style');s.textContent='*,*::before,*::after{transition:none!important;animation:none!important}';d.head.appendChild(s);
 var out=[];for(var i=0;i<d.styleSheets.length;i++){var rs;try{rs=d.styleSheets[i].cssRules}catch(e){continue}collect(rs,out)}
 var fs=d.createElement('style');fs.textContent=out.join('\\n');d.head.appendChild(fs);
 var host=d.querySelector(C.container);
 if(!host){d.body.innerHTML='<p style="font:12px monospace;color:#B92F1E">specimen not found: '+C.container+'</p>';return}
 var mate=C.pair?d.querySelector(C.pair):null;
 var wrap=d.createElement('div');wrap.style.cssText='padding:8px 10px';
 C.states.forEach(function(st){
  var box=d.createElement('div');box.style.cssText='margin:0 0 10px';
  var lab=d.createElement('div');lab.textContent=st;
  lab.style.cssText='font:10px/1.4 ui-monospace,monospace;letter-spacing:.09em;text-transform:uppercase;opacity:.5;margin:0 0 3px';
  var cl=host.cloneNode(true);cl.removeAttribute('hidden');cl.classList.add('sx-'+st);
  if(C.seed==='ovcount'){var tg2=cl.querySelector('.overflow__trigger');if(tg2){tg2.innerHTML='More <span class="ovcount">2</span>'}}
  var tg=(cl.matches&&cl.matches(C.target))?[cl]:[].slice.call(cl.querySelectorAll(C.target));
  tg.forEach(function(t){t.classList.add('fx-t');if(st==='hover'){t.classList.add('fx-h')}if(st==='pressed'){t.classList.add('fx-h');t.classList.add('fx-p')}});
  box.appendChild(lab);box.appendChild(cl);
  if(mate){var m=mate.cloneNode(true);m.removeAttribute('id');box.appendChild(m)}
  wrap.appendChild(box)});
 var th=d.body.getAttribute('data-theme');
 d.body.innerHTML='';d.body.style.padding='0';d.body.appendChild(wrap);d.body.setAttribute('data-theme',th);
 if(C.css){var ov=d.createElement('style');ov.textContent=C.css;d.head.appendChild(ov)}
 d.documentElement.setAttribute('data-preview-ready','1');
}
window.addEventListener('load',function(){setTimeout(boot,250)});
})();<\/script>`;
document.querySelectorAll('iframe[data-frame]').forEach(fr=>{
  const f = FRAMES[+fr.dataset.frame];
  const cfg = {container:f.container,target:f.target,states:f.states,theme:f.theme,css:f.css,pair:f.pair,seed:f.seed};
  let doc = b64utf8(SNIP[f.comp]);
  // srcdoc inherits THIS page's base URL (_review/), so the snippets' own
  // href="../canon/type.css" would 404. Re-base every relative URL onto knowledge/snippets/.
  doc = doc.replace('<head>', '<head><base href="' + new URL('../knowledge/snippets/', location.href).href + '">');
  doc = doc.replace('</body>', INJ(cfg) + '</body>');
  fr.srcdoc = doc;
});
"""

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RULED s130-D4 / s130-D5 &mdash; enactment preview v3 (session #149)</title>
<style>@@css@@</style></head><body><div class="wrap">

<h1>RULED treatment preview <span class="mono">v3</span></h1>
<div class="ruledbar"><b>THESE ARE ALREADY RULED. NOTHING ON THIS PAGE IS A NEW CHOICE.</b><br>
<span class="mono">s130-D4</span> (Dave, #130, 2026-08-08) &mdash; banner actions across ALL banners and RAG fills:
a ghost/tint treatment, <b>transparent at rest</b>, ink-derived wash, <b>hover 8%</b>, <b>pressed 14%</b>,
label rides <span class="mono">--ink</span>; and <span class="mono">--rag-error-background</span> moves
<span class="mono">#F6604C &rarr; #B92F1E</span>.<br>
<span class="mono">s130-D5</span> (Dave, #130) &mdash; check and selection-control labels are <b>always the ink colour</b>;
the error signal moves off the label onto the <b>box border plus the message</b> (ruled at 17.40:1).<br>
Both are <b>RULED, NOT ENACTED</b> &mdash; no value has moved in any token file. <b>This page exists so you can see
the ruled treatment before licensing enactment.</b> No alternatives are offered and none should be inferred.</div>

<p class="sub">Session #149, lane red 63, iteration 3. Specimens are the <b>real canon snippets</b>
(<span class="mono">knowledge/snippets/Banner.reference.html</span>,
<span class="mono">Selection-controls.reference.html</span>,
<span class="mono">Tabs.reference.html</span>) rendered live in iframes with their own canon CSS and the HSBC type layer.
The <b>CURRENT</b> side is canon.css exactly as it stands today. The <b>RULED</b> side applies the ruling as a
<b>scoped preview override layer injected into that iframe only</b> &mdash; every card states its override verbatim.
<b>No canon, token or gate file was edited to produce this page, and nothing was committed.</b>
All ratios are computed in-page by the WCAG 2.x relative-luminance formula from the hexes shown.
Hover and pressed are forced visible by rewriting <span class="mono">:hover</span>/<span class="mono">:active</span>
to classes, with transitions killed first.</p>

<div class="card" id="card-banner"><h2>1 &middot; Banner &mdash; error fill and its ghost actions <span class="mono">(s130-D4)</span></h2>
<div class="diag">Two things move together. The <b>fill</b> goes <span class="mono">#F6604C &rarr; #B92F1E</span>,
which is what carries the white label and the white action text over the 4.5 line. The <b>wash</b> on the ghost
actions is remapped from today's 14%/22% down to <b>8%/14%</b> &mdash; because on the darker fill a heavier
white wash lightens the surface faster than the label can afford. Transparent-at-rest and the
<span class="mono">--ink</span> label are already how the snippet is built; the ruling confirms them rather than
changing them.</div>
<pre class="rule">/* CURRENT — knowledge/canon/canon.css + Banner.reference.html, as they stand */
--rag-error-background: #F6604C;
.banner .actions .abtn        { background:transparent; color:var(--ink) }
.banner .actions .abtn:hover  { background:color-mix(in srgb, var(--ink) 14%, transparent) }
.banner .actions .abtn:active { background:color-mix(in srgb, var(--ink) 22%, transparent) }

/* RULED s130-D4 — applied HERE as a scoped preview override inside the iframe, NOT written to canon */
.banner.err                   { --fill:#B92F1E }
.banner .actions .abtn.fx-h   { background:color-mix(in srgb, var(--ink) 8%,  transparent) }
.banner .actions .abtn.fx-p   { background:color-mix(in srgb, var(--ink) 14%, transparent) }</pre>
@@banner_table@@
<div class="flag"><b>The ruled numbers reproduce.</b> Dave picked ~8% at #130 against a measured worst hover of
<b>5.29</b> and a binding-cell pressed of <b>4.75</b>. Computed fresh here from the hexes: hover <b>5.26:1</b>,
pressed <b>4.75:1</b>, base <b>6.02:1</b> &mdash; every state clears 4.5. The current side fails all three
(3.14 / 2.72 / 2.47) and gets <i>worse</i> as the wash gets heavier, because a white wash lightens a fill the
white label sits on.</div>
@@banner_specs@@
<div class="flag"><b>Mode-invariant by design.</b> RAG fills do not invert (s122-D1/D2/D3), so the light and dark
banner pairs above are expected to be <i>identical</i> in the fill and its wash &mdash; that sameness is the
ruling working, not a rendering fault. s130-D4's own <span class="mono">[BLOCK]</span> note says an enactor
must not quietly add a dark-mode inversion here.</div>
<div class="open"><b>OPEN &mdash; under-specified by the ruling, nothing picked here.</b>
<b>(a)</b> s130-D4 names <span class="mono">--rag-error-background</span> only. Canon binds
<span class="mono">--rag-error: var(--rag-error-glyph)</span> and <span class="mono">--rag-error-glyph</span> is
<i>also</i> <span class="mono">#F6604C</span> &mdash; the ruling does not say whether the glyph rung and the bare
<span class="mono">--rag-error</span> role follow the background to #B92F1E or stay. This preview moves the
<b>fill only</b>. <b>(b)</b> Canon declares no banner-scoped quaternary and quaternary has no pressed token
(hover == pressed), so 8%/14% is literally inexpressible in the current token shape &mdash; whether enactment
mints a pressed rung or scopes the wash locally is not stated. <b>(c)</b> The 8%/14% remap is ruled for
<i>banner actions across all banners and RAG fills</i>; the banner dismiss <span class="mono">.x</span> carries
the same 14%/22% pair and is not named. It is shown unchanged above.</div>
</div>

<div class="card" id="card-selection"><h2>2 &middot; Selection-controls &mdash; the error field <span class="mono">(s130-D5)</span></h2>
<div class="diag">Today the error state recolours <b>three</b> things: the label, the box border, and the message.
The ruling takes the label back to ink and leaves the signal on the border and the message. That is what moves
&ldquo;Accept terms &amp; conditions&rdquo; from <b>3.14:1</b> to the ruled <b>17.40:1</b> in light &mdash; the number
in the ruling text is exactly ink-on-page, and it reproduces in both modes.</div>
<pre class="rule">/* CURRENT — Selection-controls.reference.html */
.field.is-error label { color:var(--error) }   /* #F6604C */
.field.is-error .box  { border-color:var(--error) }
.err-msg              { color:var(--error) }

/* RULED s130-D5 — scoped preview override inside the iframe, NOT written to canon */
.field.is-error label { color:var(--label) }   /* ink: #1A1A1A light / #FFFFFF dark */
.field.is-error .box  { border-color:var(--error) }   /* UNCHANGED — the signal stays here */
.err-msg              { color:#DA1A00 light / #F6604C dark }   /* rag/error-ink, s145-D1 */</pre>
@@sc_table@@
<div class="flag"><b>Why the message ink is not <span class="mono">#F6604C</span> in light.</b> s130-D5 moves the
signal onto the message but does not restate a hex. Red <i>text</i> now has a minted rung &mdash;
<span class="mono">rag/error-ink</span>, named at s145-D1, values from s144-D1: light <span class="mono">#DA1A00</span>
(5.09:1), dark <span class="mono">#F6604C</span> (5.55:1). Using it is what makes the message clear 4.5 in light;
<span class="mono">#F6604C</span> on white is 3.14:1 and would keep the field failing after the label was fixed.</div>
@@sc_specs@@
<div class="open"><b>OPEN &mdash; under-specified by the ruling, nothing picked here.</b>
<b>(a)</b> The <b>box border</b> colour is not restated. This preview leaves it at
<span class="mono">--error #F6604C</span> (3.14:1 on white as a non-text boundary; 1.4.11 asks 3.0 for a UI
component boundary, so it passes <i>as a border</i> but not as text). Whether the border should also move to
<span class="mono">rag/error-ink</span> is not ruled. <b>(b)</b> The <span class="mono">&#9888;</span> glyph in the
message rides the message colour here because it is a text character in the markup, not an icon slot &mdash; not
addressed by the ruling. <b>(c)</b> s130-D5's <span class="mono">[WARN]</span> stands: the six 3.95:1 and two
3.66:1 selection-control records are <b>chip</b> failures, a different token
(<span class="mono">form/background/pressed</span>), and are <b>not</b> touched by this ruling or by this page.</div>
</div>

<div class="card" id="card-tabs"><h2>3 &middot; Tabs &mdash; the overflow count badge &ldquo;2&rdquo; in dark <span class="mono">(does D4 resolve the 1:1?)</span></h2>
<div class="diag"><b>Answer: no, not on its own &mdash; but the seat that fixes it already exists and already
carries D4's red.</b> The dark badge measures <b>1:1, literally invisible</b>, because
<span class="mono">Tabs.reference.html</span> line 100 paints <span class="mono">.ovcount</span> with
<span class="mono">background:var(--tabs-active)</span> and <span class="mono">color:var(--text-reverse)</span>,
and in dark both resolve to <span class="mono">#FFFFFF</span>. It is a <b>wrong-slot</b> defect, not a shade
defect: the badge is consuming the <i>bar's</i> active token instead of its own badge slot.</div>
<pre class="rule">/* CURRENT — Tabs.reference.html:100 */
.ovcount { background:var(--tabs-active); color:var(--text-reverse) }   /* dark: #FFFFFF on #FFFFFF = 1:1 */

/* THE SEAT THAT ALREADY EXISTS — knowledge/tokens/semantic-colour.json:1455-1463, tabs/badge/background */
tabs/badge/background : light #B92F1E · dark #CC4333   (aliased to badge/background, R-D23 part 2)
$note: "White numeral (type26-013: white is red-only; 6.02:1 on #B92F1E)."

/* RULED-ADJACENT — scoped preview override inside the iframe, NOT written to canon */
.ovcount { background: #CC4333 (dark) / #B92F1E (light); color:#FFFFFF }</pre>
@@tabs_table@@
<div class="flag"><b>What D4 does and does not do here.</b> D4 moves
<span class="mono">--rag-error-background</span> to <span class="mono">#B92F1E</span> &mdash; the same red the badge
slot already names, so after enactment the badge red and the banner red agree and the light badge is exactly the
<b>6.02:1</b> the token&rsquo;s own <span class="mono">$note</span> claims. But the dark 1:1 is <b>not</b> resolved by
D4, because <span class="mono">.ovcount</span> never reads the badge slot at all. <b>Re-pointing that one
declaration is the fix, and it is not what D4 says.</b> The dark badge slot is <span class="mono">#CC4333</span>,
not <span class="mono">#B92F1E</span>, and white on it measures <b>4.75:1</b> &mdash; a pass, but below the 6.02
the $note advertises.</div>
@@tabs_specs@@
<div class="open"><b>OPEN &mdash; not ruled, nothing picked here.</b> Re-pointing
<span class="mono">.ovcount</span> at <span class="mono">--tabs-badge-background</span> is a
<b>consumption</b> change in Tabs, outside both D4 and D5. It is shown so you can see the outcome; licensing it
is a separate word. Also unruled: the dark badge slot <span class="mono">#CC4333</span> is a legacy value that
D4 does not touch, so after D4 the error red forks &mdash; banner <span class="mono">#B92F1E</span> mode-invariant,
badge <span class="mono">#B92F1E</span>/<span class="mono">#CC4333</span> mode-forked.</div>
</div>

<div class="card" id="card-star"><h2>4 &middot; path.star &mdash; mark + red text is an ILLEGAL PAIRING <span class="mono">(carried from v2, unchanged)</span></h2>
<div class="diag">Carried forward from <span class="mono">state-contrast-controller-v2.html</span> exactly as it
stood, as one card. The audited composition puts a red star mark beside red error text; the pairing itself is the
defect, so the fix is compositional, not chromatic.</div>
<table class="m"><tr><th>theme</th><th>state</th><th>foreground</th><th>background</th><th>measured</th></tr>
<tr><td>dark</td><td>hover</td><td>@@sw333@@</td><td>@@sw000@@</td><td><span class="b fail">1.66:1 FAIL</span></td></tr>
<tr><td>dark</td><td>pressed</td><td>@@sw333@@</td><td>@@sw000@@</td><td><span class="b fail">1.66:1 FAIL</span></td></tr>
</table>
<div class="pair">
<div class="pairbox"><div class="hd no">Current specimen &mdash; ILLEGAL pairing</div><div class="bd">
<span class="chipm"><svg width="15" height="15" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14l-5-4.87 6.91-1.01L12 2z" fill="#DA1A00"/></svg>
<span style="color:#DA1A00">Favourite could not be saved</span></span>
<div style="font-size:12.5px;color:#635750;margin-top:8px">A red mark AND red text in the same lockup.</div></div></div>
<div class="pairbox"><div class="hd yes">Fix 1 &mdash; mark with the DARK INK, no red</div><div class="bd">
<span class="chipm"><svg width="15" height="15" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14l-5-4.87 6.91-1.01L12 2z" fill="#1A1A1A"/></svg>
<span style="color:#1A1A1A">Favourite could not be saved</span></span>
<div style="font-size:12.5px;color:#635750;margin-top:8px">Mark rides the ink; the red leaves the lockup entirely.</div></div></div>
<div class="pairbox"><div class="hd yes">Fix 2 &mdash; red text with NO mark</div><div class="bd">
<span style="color:#DA1A00">Favourite could not be saved</span>
<div style="font-size:12.5px;color:#635750;margin-top:8px">Red text alone, at <span class="mono">rag/error-ink</span> &mdash; 5.09:1 on white.</div></div></div>
</div>
<div class="flag"><b>WHAT THIS DOES NOT CLOSE.</b> Calling the pairing illegal removes the composition, not the
underlying number: <span class="mono">path.star</span> in dark still resolves <span class="mono">#333333</span> on
<span class="mono">#000000</span> = <b>1.66:1</b>, and that returns the moment a legal composition paints it.</div>
</div>

<div class="card" id="card-export"><h2>Licence enactment</h2>
<p class="diag">One block. This is not a colour pick &mdash; the colours are ruled. It records whether you are
licensing the <b>enactment lane</b> to move the values into the token files and regenerate canon.</p>
<div>
<label class="lic"><input type="radio" name="licence" value="D4"> <b>D4 only</b> &mdash; licence enactment of the banner actions ghost/tint remap and <span class="mono">--rag-error-background &rarr; #B92F1E</span>. Selection-controls stay as they are for now.</label>
<label class="lic"><input type="radio" name="licence" value="D5"> <b>D5 only</b> &mdash; licence enactment of the selection-control label/border/message split. Banner stays as it is for now.</label>
<label class="lic"><input type="radio" name="licence" value="BOTH"> <b>Both</b> &mdash; licence enactment of D4 and D5 together.</label>
<label class="lic"><input type="radio" name="licence" value="NEITHER"> <b>Neither yet</b> &mdash; hold; something above needs another look.</label>
</div>
<p class="diag" style="margin-top:14px"><b>Free text</b> &mdash; anything you want carried into the enactment brief,
including answers to any of the OPEN items above (each is named and nothing has been picked for you).</p>
<textarea id="free" placeholder="e.g. the box border should also move to rag/error-ink; leave the dismiss X alone; ..."></textarea>
<p style="margin:14px 0 0"><button class="act" id="copy">Copy licence block</button> <span id="copied" class="mono"></span></p>
<textarea id="ruling" readonly></textarea>
</div>

</div>
<script>
const SNIP = @@snip@@;
const FRAMES = @@frames@@;
const MEASURED = @@measured@@;
function b64utf8(b){const bin=atob(b);const u=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);return new TextDecoder('utf-8').decode(u)}
function lum(h){h=h.replace('#','');const c=[0,2,4].map(i=>parseInt(h.substr(i,2),16)/255).map(v=>v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4));return .2126*c[0]+.7152*c[1]+.0722*c[2]}
function ratio(a,b){const l1=lum(a),l2=lum(b),hi=Math.max(l1,l2),lo=Math.min(l1,l2);return Math.round((hi+.05)/(lo+.05)*100)/100}
@@inj@@
function ruling(){
  const pick=document.querySelector('input[name=licence]:checked');
  const L=['ENACTMENT LICENCE — session #149, from _review/state-contrast-ruled-preview-v3.html',
   'SUBJECT: s130-D4 and s130-D5 — RULED #130 (Dave, 2026-08-08), NOT ENACTED.',
   'This block licenses ENACTMENT of settled rulings. It is not a colour choice and picks nothing new.',
   '',
   'LICENCE: '+(pick?pick.value:'(none selected)'),
   ''];
  L.push('MEASURED ON THE RULED SIDE (WCAG 2.x, computed in-page from the hexes shown):');
  MEASURED.banner.filter(r=>r.variant==='ruled').forEach(r=>{
    L.push('  banner '+r.theme.padEnd(6)+' '+r.state.padEnd(8)+' '+r.fg+' on '+r.bg+'   '+r.r+':1 '+(r.r>=4.5?'PASS':'FAIL'));});
  MEASURED.selection.filter(r=>r.variant==='ruled').forEach(r=>{
    L.push('  selection '+r.theme.padEnd(6)+' '+r.part.padEnd(11)+' '+r.fg+' on '+r.bg+'   '+r.r+':1 '+(r.r>=4.5?'PASS':'FAIL'));});
  MEASURED.tabs.filter(r=>r.variant==='ruled').forEach(r=>{
    L.push('  tabs badge '+r.theme.padEnd(6)+' '+r.fg+' on '+r.bg+'   '+r.r+':1 '+(r.r>=4.5?'PASS':'FAIL'));});
  L.push('');
  L.push('OPEN ITEMS NAMED ON THE PAGE, NOTHING PICKED — answer any of these in the free text below:');
  L.push('  D4-a  does --rag-error-glyph / the bare --rag-error role follow the background to #B92F1E?');
  L.push('  D4-b  8%/14% is inexpressible in the current token shape (no banner quaternary, no pressed rung) — mint or scope?');
  L.push('  D4-c  the banner dismiss .x carries the same 14%/22% pair and is not named by the ruling.');
  L.push('  D5-a  the box border colour is not restated — stay at --error #F6604C, or move to rag/error-ink?');
  L.push('  D5-b  the warning glyph in the message rides the message colour (text char, not an icon slot).');
  L.push('  TABS  .ovcount reads --tabs-active, not the badge slot — re-pointing it is outside D4 and D5.');
  L.push('');
  L.push('FREE TEXT:');
  L.push((document.getElementById('free').value||'(none)'));
  L.push('');
  L.push('No canon.css / token / gate file was edited to produce this page, and nothing was committed.');
  document.getElementById('ruling').value=L.join('\\n');
}
document.addEventListener('change',ruling);
document.addEventListener('input',ruling);
ruling();
document.getElementById('copy').addEventListener('click',()=>{
  const t=document.getElementById('ruling'); t.select();
  try{document.execCommand('copy');document.getElementById('copied').textContent='copied'}catch(e){document.getElementById('copied').textContent='select + copy manually'}
});
</script></body></html>
"""

_SUBS = {
    "css": CSS,
    "banner_table": banner_table(),
    "sc_table": sc_table(),
    "tabs_table": tabs_table(),
    "banner_specs": specs("banner"),
    "sc_specs": specs("selection"),
    "tabs_specs": specs("tabs"),
    "sw333": sw("#333333"),
    "sw000": sw("#000000"),
    "snip": json.dumps(SNIP),
    "frames": json.dumps(FRAMES),
    "measured": json.dumps(MEASURED),
    "inj": INJ_JS,
}
page = HTML
for _k, _v in _SUBS.items():
    page = page.replace("@@" + _k + "@@", _v)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(page)
print("wrote", OUT, len(page), "bytes")
for k, rows in MEASURED.items():
    for r in rows:
        print(k, r)
