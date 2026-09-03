#!/usr/bin/env python3
"""Lane L4 (#245) — assembles reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html.

Every canon region is SPLICED VERBATIM from disk (type.css, canon.css, the bento snippet);
the splice ledger (file · line range · byte length · sha256 prefix) is printed and written into
the surface as an HTML comment. The only CSS that is NOT a splice is the surface's own chrome
and the five row-model override rules — both are marked `L4 CHROME` / `L4 MODEL` in the file.

Run from anywhere:  python3 build_surface.py
Reads  ../../../../knowledge/…   (repo-relative from this file)
Writes ../../../../reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html
Touches nothing else.
"""
import hashlib, pathlib, re, sys, json

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
CANON = REPO / "knowledge/canon/canon.css"
TYPE = REPO / "knowledge/canon/type.css"
SNIP = REPO / "knowledge/snippets/Template-dashboard-bento.reference.html"
OUT = REPO / "reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html"

canon = CANON.read_text(encoding="utf-8").split("\n")
ledger = []


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def splice(name, path, a, b, text=None):
    """a..b are 1-based inclusive line numbers into `path`; returns the verbatim text."""
    if text is None:
        lines = path.read_text(encoding="utf-8").split("\n")
        text = "\n".join(lines[a - 1:b])
    ledger.append(dict(region=name, file=str(path.relative_to(REPO)), lines=f"{a}-{b}",
                       bytes=len(text.encode("utf-8")), sha256_16=sha(text)))
    return text


def find_line(pred, start=1, end=None):
    end = end or len(canon)
    for i in range(start, end + 1):
        if pred(canon[i - 1]):
            return i
    raise SystemExit(f"marker not found from {start}")


def brace_block_end(start):
    """start = 1-based line holding the first selector; returns the 1-based line of the closing brace."""
    depth = 0; opened = False
    for i in range(start, len(canon) + 1):
        for ch in canon[i - 1]:
            if ch == "{": depth += 1; opened = True
            elif ch == "}": depth -= 1
        if opened and depth == 0:
            return i
    raise SystemExit("unbalanced")


# ---- 1 · canon tokens: line 1 up to the line before `.canon, .canon *`
tok_end = find_line(lambda l: l.startswith(".canon, .canon *")) - 1
tokens = splice("canon tokens (:root, [data-theme=dark], semantic aliases)", CANON, 1, tok_end)

# ---- 2 · the top-level AUTO-BENTO block (the rules the brief names: fixed at ~1091, floor at ~1124)
ab_start = find_line(lambda l: l.startswith("/* ===== AUTO-BENTO START"))
ab_end = find_line(lambda l: l.startswith("/* ===== AUTO-BENTO END"), ab_start)
auto_bento = splice("AUTO-BENTO block, top level", CANON, ab_start, ab_end)
fixed_line = find_line(lambda l: "grid-auto-rows:var(--bento-row-unit);" in l, ab_start, ab_end)
floor_line = find_line(lambda l: "grid-auto-rows:minmax(var(--bento-row-unit),1fr);" in l, ab_start, ab_end)

# ---- 3 · the .cn-template-dashboard-bento scope (the snippet as canon carries it)
sc_hdr = find_line(lambda l: "Template-dashboard-bento  (from snippets/Template-dashboard-bento.reference.html)" in l)
sc_start = sc_hdr - 1  # the `/* =====` line above the header
assert canon[sc_start - 1].startswith("/* ====")
nxt_hdr = find_line(lambda l: l.startswith("   Template-dashboard  (from snippets/Template-dashboard.reference.html)"), sc_hdr)
sc_end = nxt_hdr - 2  # line before that block's `/* =====` line
scope = splice(".cn-template-dashboard-bento scope", CANON, sc_start, sc_end)
outer_auto_line = find_line(lambda l: "--bento-gutter:40px; --bento-row-unit:auto;" in l, sc_start, sc_end)
rung_lines = [find_line(lambda l, k=k: f".c-bento.tpl-group-{k}{{--bento-row-unit:" in l, sc_start, sc_end) for k in ("kpi", "chart", "rail")]
rungs = {k: re.search(r"--bento-row-unit:(\d+px)", canon[i - 1]).group(1) for k, i in zip(("kpi", "chart", "rail"), rung_lines)}

# ---- 4 · per-theme ROOT token overrides (legacy · console · supercharge) up to their first component rule
theme_root = {}
for th, stop in (("legacy", '[data-apollo-theme="legacy"] .cn-accordion'),
                 ("console", '[data-apollo-theme="console"] .cn-account-card{'),
                 ("supercharge", '[data-apollo-theme="supercharge"] .cn-accordion{')):
    h = find_line(lambda l, th=th: l.startswith(f"/* ---- Apollo") and f'[data-apollo-theme="{th}"]' in l)
    e = find_line(lambda l, stop=stop: l.startswith(stop), h) - 1
    theme_root[th] = splice(f"{th} theme root overrides", CANON, h, e)

# ---- 5 · per-theme .cn-template-dashboard-bento overrides (brace-matched blocks)
theme_scope = {}
for th in ("legacy", "console", "supercharge"):
    blocks = []
    i = 1
    while True:
        try:
            # legacy's rule lists `[data-apollo-theme="legacy"] …,` then `[data-apollo-theme="common"] …{` — the brace line may carry either name
            s = find_line(lambda l, th=th: (l.startswith(f'[data-apollo-theme="{th}"]') or (th == "legacy" and l.startswith('[data-apollo-theme="common"]')))
                          and ".cn-template-dashboard-bento" in l and l.rstrip().endswith("{"), i)
        except SystemExit:
            break
        # walk back over preceding selector lines of the same rule
        s0 = s
        while s0 > 1 and canon[s0 - 2].rstrip().endswith(","):
            s0 -= 1
        e = brace_block_end(s0)
        blocks.append(splice(f"{th} .cn-template-dashboard-bento override", CANON, s0, e))
        i = e + 1
    theme_scope[th] = "\n".join(blocks)

# ---- 6 · type.css, whole file
type_css = splice("type.css (whole file)", TYPE, 1, len(TYPE.read_text(encoding='utf-8').split("\n")))

# ---- 7 · the snippet's markup: the svg symbol sprite + <main class="tpl-page"> … </main>
snip = SNIP.read_text(encoding="utf-8").split("\n")
sp_s = next(i for i, l in enumerate(snip, 1) if l.startswith('<svg width="0" height="0"'))
sp_e = next(i for i, l in enumerate(snip, 1) if i > sp_s and l.startswith("</svg>"))
sprite = splice("snippet svg symbol sprite", SNIP, sp_s, sp_e)
m_s = next(i for i, l in enumerate(snip, 1) if l.startswith('  <main class="tpl-page"'))
m_e = next(i for i, l in enumerate(snip, 1) if i > m_s and l.startswith("  </main>"))
main_html = splice("snippet <main class=tpl-page> wall", SNIP, m_s, m_e)
for bad in ('src="', "url(", "@import", 'href="../', "http"):
    if bad in main_html or bad in sprite:
        raise SystemExit(f"external reference in spliced markup: {bad!r}")

MIS = {"kpi": "120px", "chart": "240px", "rail": "96px"}  # deliberately WRONG rungs — off the ladder on purpose

# ---------------------------------------------------------------------------------------------
html = []
A = html.append
A("<!DOCTYPE html>\n<html lang=\"en\" data-view=\"fit\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
A("<title>Row-height renders — three models side by side (L4, #245, 2026-09-03) — RULES NOTHING</title>")
A("<!--\n  ROW-HEIGHT RENDERS v1 · lane L4 · session #245 · 2026-09-03\n  ⛔ THIS PAGE RULES NOTHING. It renders the three bento row-height models side by side on identical\n     content so Dave's eye can pick one. The choice is his (carried open since #233).\n  LEVEL VARIED: the NESTED tile grid (`.c-bento__tile.c-bento > .c-bento__grid`, canon.css:%d).\n  LEVEL HELD:   the OUTER wall grid (canon.css:%d fixed rule, but the dashboard sets `--bento-row-unit:auto`\n                at canon.css:%d, so the outer row is INTRINSIC in every column here).\n  SPLICE LEDGER (verbatim regions; file · lines · bytes · sha256[:16]):\n%s\n  The only non-spliced CSS is marked `L4 CHROME` (this page's own frame) and `L4 MODEL` (the five\n  row-model overrides, one per column state). Nothing in canon.css, any meta, any generator or any\n  snippet was changed.\n-->" % (floor_line, fixed_line, outer_auto_line,
       "\n".join(f"    · {r['region']:<58} {r['file']}:{r['lines']:<13} {r['bytes']:>7} B  {r['sha256_16']}" for r in ledger)))
A("<style id=\"type-css\">\n/* ===== SPLICE · knowledge/canon/type.css · whole file · VERBATIM ===== */\n" + type_css + "\n</style>")
A("<style id=\"canon-tokens\">\n/* ===== SPLICE · knowledge/canon/canon.css · lines 1-%d · VERBATIM ===== */\n" % tok_end + tokens + "\n</style>")
A("<style id=\"canon-auto-bento\">\n/* ===== SPLICE · knowledge/canon/canon.css · lines %d-%d · the top-level AUTO-BENTO block · VERBATIM ===== */\n" % (ab_start, ab_end) + auto_bento + "\n</style>")
A("<style id=\"canon-scope\">\n/* ===== SPLICE · knowledge/canon/canon.css · lines %d-%d · the .cn-template-dashboard-bento scope · VERBATIM ===== */\n" % (sc_start, sc_end) + scope + "\n</style>")
for th in ("legacy", "console", "supercharge"):
    A(f"<style id=\"theme-{th}\">\n/* ===== SPLICE · knowledge/canon/canon.css · {th} root overrides + .cn-template-dashboard-bento overrides · VERBATIM ===== */\n" + theme_root[th] + "\n" + theme_scope[th] + "\n</style>")

A("""<style id="l4-model">
/* ===== L4 MODEL — the ONLY rules that act on the bento and are not a splice. =====
   LEVEL VARIED: the NESTED tile grid. Selector mirrors canon.css's own
   `.c-bento__tile.c-bento > .c-bento__grid` (the FLOOR rule) with the column's model in front,
   so it wins on specificity (0,5,0 over canon's 0,3,0) and on nothing else.
   The OUTER wall grid is NOT touched: it keeps the shipped `--bento-row-unit:auto`. */
.col[data-model="fixed"]         .cn-template-dashboard-bento .c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:var(--bento-row-unit);}
.col[data-model="floor-auto"]    .cn-template-dashboard-bento .c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:minmax(var(--bento-row-unit),auto);}
.col[data-model="floor-1fr"]     .cn-template-dashboard-bento .c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:minmax(var(--bento-row-unit),1fr);}  /* == canon verbatim; the toggle's reference state */
.col[data-model="misrung-fixed"] .cn-template-dashboard-bento .c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:var(--bento-row-unit);}
.col[data-model="misrung-floor"] .cn-template-dashboard-bento .c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:minmax(var(--bento-row-unit),auto);}
/* the MIS-RUNG: deliberately WRONG rungs (canon ships %(kpi)s / %(chart)s / %(rail)s at canon.css:%(rl)s). Not tokens — a mis-rung is off the ladder by definition. */
.col[data-model^="misrung"] .cn-template-dashboard-bento .c-bento.tpl-group-kpi{--bento-row-unit:%(mkpi)s;}
.col[data-model^="misrung"] .cn-template-dashboard-bento .c-bento.tpl-group-chart{--bento-row-unit:%(mchart)s;}
.col[data-model^="misrung"] .cn-template-dashboard-bento .c-bento.tpl-group-rail{--bento-row-unit:%(mrail)s;}
</style>""" % dict(kpi=rungs["kpi"], chart=rungs["chart"], rail=rungs["rail"], rl=",".join(map(str, rung_lines)),
                  mkpi=MIS["kpi"], mchart=MIS["chart"], mrail=MIS["rail"]))

A("""<style id="l4-chrome">
/* ===== L4 CHROME — this page's own frame. Colours are canon tokens only (var(--…) from the spliced
   :root); the flag red is var(--rag-error-ink) = #DA1A00 on white / #F6604C in dark (s151-D1). ===== */
*{box-sizing:border-box;}
html{background:var(--page);}
body{margin:0;background:var(--page);color:var(--text);-webkit-font-smoothing:antialiased;}
.pg{max-width:1600px;margin:0 auto;padding:32px 32px 96px;}
.hd{display:grid;grid-template-columns:1fr 1fr;gap:32px;border-top:2px solid var(--text);padding-top:16px;margin-bottom:32px;}
.hd h1{margin:0 0 8px;}
.hd p{margin:0 0 8px;max-width:64ch;}
.kicker{display:block;margin-bottom:12px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;}
.rules{border-top:1px solid var(--divider);}
.rules dt{color:var(--muted);margin-top:12px;}
.rules dd{margin:2px 0 0;}
code,pre{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;font-size:12px;line-height:16px;}
code{background:var(--surface-hover);padding:1px 4px;}
pre{margin:0;white-space:pre-wrap;word-break:break-word;}
.ctl{display:flex;flex-wrap:wrap;gap:24px 32px;align-items:center;padding:16px 0;border-top:1px solid var(--divider);border-bottom:1px solid var(--divider);margin-bottom:32px;}
.ctl fieldset{border:0;margin:0;padding:0;display:flex;gap:12px;align-items:center;}
.ctl legend{float:left;margin-right:8px;color:var(--muted);}
.ctl label{display:inline-flex;gap:6px;align-items:center;min-height:28px;cursor:pointer;}
button.b{min-height:36px;padding:0 16px;border:1px solid var(--text);background:var(--page);color:var(--text);cursor:pointer;border-radius:var(--border-radius-control);}
button.b:hover{background:var(--surface-hover);}
.frame{margin:0 0 48px;padding-top:12px;border-top:1px solid var(--text);}
.frame-cap{display:flex;gap:16px;align-items:baseline;margin-bottom:12px;}
.frame-cap .n{color:var(--muted);}
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:auto auto;gap:0 24px;align-items:start;}
.col{display:grid;grid-template-rows:subgrid;grid-row:span 2;}  /* heads share one row so the three viewports start level */
html[data-view="one"] .cols{grid-template-columns:1fr;}
.col{min-width:0;}
.col-h{display:flex;flex-direction:column;gap:6px;padding:8px 0 10px;border-bottom:1px solid var(--divider);margin-bottom:8px;}
.col-h .t{display:flex;justify-content:space-between;gap:12px;align-items:baseline;}
.col-h .lvl{color:var(--muted);}
.col-h pre{color:var(--text);}
.read{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;}
.read b{font-weight:500;}
.flag{color:var(--rag-error-ink);}
.ok{color:var(--muted);}
.point{display:inline-flex;gap:8px;align-items:center;min-height:36px;padding:0 12px;border:1px solid var(--text);cursor:pointer;border-radius:var(--border-radius-control);user-select:none;}
.point:has(input:checked){background:var(--text);color:var(--page);}
.point input{margin:0;}
.sub{display:flex;gap:12px;flex-wrap:wrap;align-items:center;min-height:28px;}
.sub label{display:inline-flex;gap:4px;align-items:center;cursor:pointer;}
.viewport{overflow:hidden;border:1px solid var(--divider);align-self:start;}
.stage{width:var(--stage-w,1440px);}
/* the page ground the snippet paints on <body> (s219-D1 pageBg) — --wall-ground is declared INSIDE the scope, so it is read there */
.stage .cn-template-dashboard-bento{background:var(--wall-ground);padding-top:24px;}
.cn-template-dashboard-bento .tpl-page{padding-bottom:24px;}  /* trims the snippet's 48px page foot so the wall reads alone */
html[data-view="one"] .stage{zoom:1 !important;}
.exp{border-top:2px solid var(--text);padding-top:16px;margin-top:48px;display:grid;grid-template-columns:1fr 1fr;gap:32px;}
.exp textarea{width:100%;min-height:96px;border:1px solid var(--divider);background:var(--page);color:var(--text);padding:8px;resize:vertical;}
.exp pre{border:1px solid var(--divider);padding:12px;min-height:180px;background:var(--surface);}
.foot{margin-top:48px;padding-top:12px;border-top:1px solid var(--divider);color:var(--muted);}
@media (max-width:1000px){.hd,.exp{grid-template-columns:1fr;}.cols{grid-template-columns:1fr;}}
</style>
</head>
<body>""")

# the wall, once, as a template — cloned into every column by script so the 3 columns are identical by construction
A("<template id=\"wall\">" + main_html + "</template>")
A(sprite)

A(f"""<div class="pg">
<header class="hd">
  <div>
    <span class="kicker t-cm-section-label">L4 · #245 · 2026-09-03 · decision surface · rules nothing</span>
    <h1 class="t-ed-heading-2">Three row-height models, one dashboard, side by side</h1>
    <p class="t-ed-body">The same bento wall — <code>Template-dashboard-bento</code>, the real snippet's <code>&lt;main&gt;</code>, spliced byte-for-byte — rendered three times per theme. Only the <b>row-height model</b> of the nested tile grids differs between the columns. Nothing on this page is ruled; the column you point at is exported as a ruling-shaped line for you to paste.</p>
    <p class="t-ed-body-small"><b>Level varied:</b> the <b>nested tile grid</b> (<code>.c-bento__tile.c-bento &gt; .c-bento__grid</code>, canon.css:{floor_line}), where the literal rungs {rungs['kpi']} / {rungs['chart']} / {rungs['rail']} live (canon.css:{','.join(map(str, rung_lines))}). <b>Level held:</b> the outer wall grid — canon's fixed rule at canon.css:{fixed_line} is real, but the dashboard sets <code>--bento-row-unit:auto</code> on the wall (canon.css:{outer_auto_line}), so the outer row is intrinsic in every column. rB's warning (#234) — a matrix that does not say which level it varies compares two things that both already ship — is why this line exists.</p>
  </div>
  <dl class="rules t-ed-body-small">
    <dt class="t-cm-section-label">What ships today</dt><dd>outer wall: <code>grid-auto-rows:var(--bento-row-unit)</code> with the unit set to <code>auto</code> · nested groups: <code>grid-auto-rows:minmax(var(--bento-row-unit),1fr)</code> — a FLOOR whose max is <code>1fr</code>. Column 2's toggle can show that exact state.</dd>
    <dt class="t-cm-section-label">How to read a column</dt><dd>Every stage is a real desktop width (1440px by default, the 6-column band; the wall inside it is 1376px after the template's 32px page padding) scaled to fit its column — switch to <b>1:1, stacked</b> to see it unscaled, or change the stage width to see the other bands. Grey text under each column head is measured live from the rendered DOM: the computed <code>grid-auto-rows</code> of each group's grid, the resolved row tracks in px, and the <b>dead band</b> — container height minus what the rows actually occupy. Red text is a break: a tile whose content is taller than its row.</dd>
    <dt class="t-cm-section-label">What is NOT decided here</dt><dd>the model itself · whether the outer level should ever be fixed again · what the rung ladder is · the role-name words. These are questions in the filed report, not answers on this page.</dd>
  </dl>
</header>

<div class="ctl t-ed-body-small">
  <fieldset><legend>View</legend>
    <label><input type="radio" name="view" value="fit" checked> side by side (scaled to fit)</label>
    <label><input type="radio" name="view" value="one"> 1:1, stacked</label>
  </fieldset>
  <fieldset><legend>Stage width · band</legend>
    <label><input type="radio" name="stage" value="1440" checked> 1440 → 6 columns</label>
    <label><input type="radio" name="stage" value="1100"> 1100 → 3</label>
    <label><input type="radio" name="stage" value="800"> 800 → 2</label>
    <label><input type="radio" name="stage" value="500"> 500 → 1</label>
  </fieldset>
  <fieldset><legend>Column 2 max</legend>
    <label><input type="radio" name="floormax" value="floor-auto" checked> <code>auto</code> (the brief's floor)</label>
    <label><input type="radio" name="floormax" value="floor-1fr"> <code>1fr</code> (canon, as shipped)</label>
  </fieldset>
  <fieldset><legend>Column 3 mis-rung under</legend>
    <label><input type="radio" name="mismodel" value="misrung-fixed" checked> fixed (breaks visibly)</label>
    <label><input type="radio" name="mismodel" value="misrung-floor"> floor (heals silently)</label>
  </fieldset>
  <span class="ok" id="summary"></span>
</div>
<div id="frames"></div>

<section class="exp" id="export">
  <div>
    <span class="kicker t-cm-section-label">Dave points here → ruling-shaped export</span>
    <p class="t-ed-body-small">Pick a column with its <b>point here</b> control (one pick, page-wide). Add a note if you like. The text on the right is plain and pasteable; it is phrased as a question until you say otherwise.</p>
    <textarea id="note" class="t-ed-body-small" placeholder="optional note — a condition, a rung, a doubt"></textarea>
    <p><button class="b t-cm-button" id="copy">Copy export</button> <span class="ok t-ed-caption" id="copied"></span></p>
  </div>
  <pre id="out" class="t-ed-caption"></pre>
</section>
<p class="foot t-ed-caption">Single file · zero external references · type.css + canon.css bento regions spliced verbatim (ledger in the source comment) · driven through <code>page.goto("file://…")</code>, never <code>set_content</code> · filed report <code>notes/_subreports/2026-09-03-245-L4-row-height-renders.md</code>.</p>
</div>""")

A("""<script>
(function(){
const THEMES=[["mono","Mono"],["legacy","Legacy"],["console","Console"],["supercharge","Supercharge"]];
const MODES=["light","dark"];
const RUNGS=%(rungs)s, MIS=%(mis)s;
const COLS=[
 {id:"fixed",   n:"1", name:"FIXED unit",  model:"fixed",
  css:".c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:var(--bento-row-unit);}",
  note:"rows are exactly the rung; the group container is stretched by the outer row, the rows are not — the slack is a dead band"},
 {id:"floor",   n:"2", name:"FLOOR minmax(rung, auto)", model:"floor-auto",
  css:".c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:minmax(var(--bento-row-unit),auto);}",
  note:"rows are at least the rung and grow into the stretched container; a too-small rung is invisible"},
 {id:"misrung", n:"3", name:"MIS-RUNG (deliberately wrong)", model:"misrung-fixed",
  css:".c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:var(--bento-row-unit);}\\n.tpl-group-kpi{--bento-row-unit:"+MIS.kpi+"} .tpl-group-chart{--bento-row-unit:"+MIS.chart+"} .tpl-group-rail{--bento-row-unit:"+MIS.rail+"}",
  note:"the same wall with rungs one step too small — under FIXED the content overruns its row; flip the control above to see FLOOR heal it silently"}
];
const tpl=document.getElementById("wall");
const frames=document.getElementById("frames");
let pick=null; try{pick=localStorage.getItem("l4-pick");}catch(e){}
function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;");}
for(const [tk,tn] of THEMES) for(const md of MODES){
  const f=document.createElement("section"); f.className="frame"; f.dataset.themeKey=tk; f.dataset.mode=md;
  f.innerHTML='<div class="frame-cap"><span class="t-ed-heading-4">'+tn+'</span><span class="n t-ed-body-small">'+md+'</span></div><div class="cols"></div>';
  const cols=f.querySelector(".cols");
  for(const c of COLS){
    const col=document.createElement("div"); col.className="col"; col.dataset.col=c.id; col.dataset.model=c.model;
    col.innerHTML='<div class="col-h"><div class="t"><span class="t-ed-body"><b>'+c.n+' · '+c.name+'</b></span>'
      +'<label class="point t-cm-button"><input type="radio" name="pick-'+tk+'-'+md+'" value="'+c.id+'"'+(pick===c.id?' checked':'')+'> point here</label></div>'
      +'<span class="lvl t-ed-caption">level varied: nested tile grid · outer wall held at auto</span>'
      +'<pre class="css">'+esc(c.css)+'</pre>'
      +'<span class="t-ed-caption ok">'+c.note+'</span>'
      +'<div class="read t-ed-caption"></div></div>'
      +'<div class="viewport"><div class="stage"><div data-apollo-theme="'+tk+'" data-theme="'+md+'"><div class="cn-template-dashboard-bento"></div></div></div></div>';
    col.querySelector(".cn-template-dashboard-bento").appendChild(tpl.content.cloneNode(true));
    cols.appendChild(col);
  }
  frames.appendChild(f);
}
// ---- fit: the stage is 1120 CSS px wide (the 6-column band); zoom it to the column width
function fit(){
  const one=document.documentElement.dataset.view==="one";
  document.querySelectorAll(".col").forEach(col=>{
    const vp=col.querySelector(".viewport"), st=col.querySelector(".stage");
    const w=parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--stage-w"))||1440;
    st.style.zoom=one?"1":String(Math.min(1,vp.clientWidth/w));
  });
}
// ---- measure: what the browser actually resolved, per group grid, per column
function px(s){return s.split(/\\s+/).map(v=>parseFloat(v));}
function measure(){
  const res=[];
  document.querySelectorAll(".col").forEach(col=>{
    const fr=col.closest(".frame"), read=col.querySelector(".read");
    const wall=col.querySelector(".tpl-wall > .c-bento__grid");
    const r={theme:fr.dataset.themeKey,mode:fr.dataset.mode,col:col.dataset.col,model:col.dataset.model,
             outerAutoRows:getComputedStyle(wall).gridAutoRows,cols:getComputedStyle(wall).gridTemplateColumns.split(" ").length,stageWidth:col.querySelector(".stage").getBoundingClientRect().width/(parseFloat(col.querySelector(".stage").style.zoom)||1),groups:[]};
    let html='<b>outer wall grid</b><span>grid-auto-rows: <code>'+r.outerAutoRows+'</code> · band: '+r.cols+' column'+(r.cols>1?'s':'')+' at stage '+Math.round(r.stageWidth)+' px</span>';
    col.querySelectorAll(".tpl-group").forEach(g=>{
      const grid=g.querySelector(":scope > .c-bento__grid"), cs=getComputedStyle(grid);
      const key=[...g.classList].find(k=>k.startsWith("tpl-group-")).slice(10);
      const tracks=px(cs.gridTemplateRows), gap=parseFloat(cs.rowGap)||0;
      const rung=parseFloat(getComputedStyle(g).getPropertyValue("--bento-row-unit"));
      const occupied=tracks.reduce((a,b)=>a+b,0)+gap*(tracks.length-1);
      const dead=Math.round((grid.clientHeight-occupied)*10)/10;
      let overflow=0; g.querySelectorAll(":scope > .c-bento__grid > .c-bento__tile").forEach(t=>{ if(t.scrollHeight>t.clientHeight+1) overflow++; });
      const gr={group:key,autoRows:cs.gridAutoRows,rung:rung,tracks:tracks.map(v=>Math.round(v*10)/10),gap:gap,gridHeight:grid.clientHeight,deadBand:dead,tilesOverflowing:overflow};
      r.groups.push(gr);
      html+='<b>'+key+'</b><span>auto-rows <code>'+gr.autoRows+'</code> · rows '+gr.tracks.join(" / ")+' px'
        +(dead>1?' · <span class="flag">dead band '+dead+' px</span>':' · dead band '+dead+' px')
        +(overflow?' · <span class="flag">'+overflow+' tile'+(overflow>1?'s':'')+' overrun'+(overflow>1?'':'s')+' its row — BREAKS</span>':'')+'</span>';
    });
    read.innerHTML=html; res.push(r);
  });
  window.__L4=res;
  const broken=res.filter(r=>r.groups.some(g=>g.tilesOverflowing)).length, dead=res.filter(r=>r.groups.some(g=>g.deadBand>1)).length;
  document.getElementById("summary").textContent=res.length+" renders · "+broken+" with a tile overrunning its row · "+dead+" with a dead band";
  render();
  return res;
}
window.__L4measure=measure;
// ---- controls
document.querySelectorAll('input[name="stage"]').forEach(i=>i.addEventListener("change",e=>{document.documentElement.style.setProperty("--stage-w",e.target.value+"px"); fit(); measure();}));
document.querySelectorAll('input[name="view"]').forEach(i=>i.addEventListener("change",e=>{document.documentElement.dataset.view=e.target.value; fit(); measure();}));
document.querySelectorAll('input[name="floormax"]').forEach(i=>i.addEventListener("change",e=>{document.querySelectorAll('.col[data-col="floor"]').forEach(c=>{c.dataset.model=e.target.value; c.querySelector(".css").textContent=".c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:minmax(var(--bento-row-unit),"+(e.target.value==="floor-1fr"?"1fr":"auto")+");}";}); measure();}));
document.querySelectorAll('input[name="mismodel"]').forEach(i=>i.addEventListener("change",e=>{document.querySelectorAll('.col[data-col="misrung"]').forEach(c=>{c.dataset.model=e.target.value; c.querySelector(".css").textContent=(e.target.value==="misrung-fixed"?".c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:var(--bento-row-unit);}":".c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:minmax(var(--bento-row-unit),auto);}")+"\\n.tpl-group-kpi{--bento-row-unit:"+MIS.kpi+"} .tpl-group-chart{--bento-row-unit:"+MIS.chart+"} .tpl-group-rail{--bento-row-unit:"+MIS.rail+"}";}); measure();}));
document.querySelectorAll('input[name^="pick-"]').forEach(i=>i.addEventListener("change",e=>{pick=e.target.value; try{localStorage.setItem("l4-pick",pick);}catch(_){}; document.querySelectorAll('input[name^="pick-"]').forEach(o=>{o.checked=(o.value===pick);}); render();}));
document.getElementById("note").addEventListener("input",render);
document.getElementById("copy").addEventListener("click",()=>{const t=document.getElementById("out").textContent; (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{document.getElementById("copied").textContent="copied";},()=>{document.getElementById("copied").textContent="select the text and copy";});});
// ---- the export: ruling-SHAPED, never a ruling
function render(){
  const c=COLS.find(x=>x.id===pick);
  const floor=document.querySelector('input[name="floormax"]:checked').value, mis=document.querySelector('input[name="mismodel"]:checked').value;
  const res=window.__L4||[];
  const seen=THEMES.map(t=>t[0]).join(", ")+" × light, dark";
  const note=document.getElementById("note").value.trim();
  let out="RULING-SHAPED — NOT A RULING UNTIL DAVE SAYS SO\\n";
  out+="subject: bento row-height model, NESTED tile grid (.c-bento__tile.c-bento > .c-bento__grid); outer wall held at --bento-row-unit:auto\\n";
  const stage=document.querySelector('input[name="stage"]:checked').value, band=(res[0]&&res[0].cols)||"?";
  out+="surface: reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html (L4, #245) · themes seen: "+seen+" · stage "+stage+"px = "+band+"-column band\\n";
  if(!c){ out+="pointed at: (nothing yet — use a column's 'point here' control)\\n"; }
  else{
    let model=c.model; if(c.id==="floor") model=floor; if(c.id==="misrung") model=mis;
    out+="pointed at: column "+c.n+" — "+c.name+"\\n";
    out+="css: "+c.css.split("\\n")[0].replace("var(--bento-row-unit),auto",model==="floor-1fr"?"var(--bento-row-unit),1fr":"var(--bento-row-unit),auto")+"\\n";
    if(c.id==="misrung") out+="⚠ column 3 is the deliberately-wrong control; pointing here reads as 'neither of 1/2 — say why' \\n";
    if(c.id==="floor") out+="floor max as pointed: "+(model==="floor-1fr"?"1fr (what canon ships today)":"auto (the brief's form)")+"\\n";
    const rs=res.filter(r=>r.col===c.id);
    if(rs.length){ const dead=rs.filter(r=>r.groups.some(g=>g.deadBand>1)).length, brk=rs.filter(r=>r.groups.some(g=>g.tilesOverflowing)).length;
      out+="measured on this page: "+rs.length+" renders of this column · dead band in "+dead+" · tile overrun in "+brk+"\\n"; }
  }
  out+="question for Dave: is this the row-height model for the nested tile grid, and does the outer wall stay at auto? (options: 1 fixed · 2 floor/auto · 2' floor/1fr as shipped · other)\\n";
  if(note) out+="note: "+note+"\\n";
  out+="carried open (not touched here): the rung ladder · the role-name words (L3) · everything in _CARRIES.md";
  document.getElementById("out").textContent=out;
}
new ResizeObserver(()=>{fit();}).observe(document.body);
fit(); requestAnimationFrame(()=>{fit(); measure();});
document.fonts&&document.fonts.ready.then(()=>{fit(); measure();});
})();
</script>
</body>
</html>""" % dict(rungs=json.dumps(rungs), mis=json.dumps(MIS)))

out = "\n".join(html)
for bad in ('src="', "@import", 'href="../', "https://", "http://", "url("):
    n = out.count(bad)
    if n:
        print(f"WARN external-looking token {bad!r} × {n}", file=sys.stderr)
OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT.relative_to(REPO)}  {len(out.encode('utf-8')):,} B")
print(f"markers: fixed rule canon.css:{fixed_line} · floor rule canon.css:{floor_line} · outer auto canon.css:{outer_auto_line} · rungs {rungs} at {rung_lines}")
for r in ledger:
    print(f"  {r['region']:<58} {r['file']}:{r['lines']:<13} {r['bytes']:>7} B  {r['sha256_16']}")
(HERE / "splice-ledger.json").write_text(json.dumps(dict(ledger=ledger, markers=dict(fixed=fixed_line, floor=floor_line, outer_auto=outer_auto_line, rungs=rungs, rung_lines=rung_lines, misrung=MIS)), indent=1), encoding="utf-8")
