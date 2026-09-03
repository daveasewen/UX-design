#!/usr/bin/env python3
"""Lane K (#245) — assembles reviews/RUNG-LADDER-2026-09-03-v1.html.  SPLICE HEAD (lines 1-127) IS L4'S build_surface.py VERBATIM; only the page tail below is K's.

Every canon region is SPLICED VERBATIM from disk (type.css, canon.css, the bento snippet);
the splice ledger (file · line range · byte length · sha256 prefix) is printed and written into
the surface as an HTML comment. The only CSS that is NOT a splice is the surface's own chrome
the floor rule, the four ladders and the probe — marked `K CHROME` / `K MODEL` in the file.

Run from anywhere:  python3 build_surface.py
Reads  ../../../../knowledge/…   (repo-relative from this file)
Writes ../../../../reviews/RUNG-LADDER-2026-09-03-v1.html
Touches nothing else.
"""
import hashlib, pathlib, re, sys, json

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
CANON = REPO / "knowledge/canon/canon.css"
TYPE = REPO / "knowledge/canon/type.css"
SNIP = REPO / "knowledge/snippets/Template-dashboard-bento.reference.html"
OUT = REPO / "reviews/RUNG-LADDER-2026-09-03-v1.html"

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


# =============================================================================================
# LANE K — the page tail. Everything above this line is L4's splice head, verbatim.
# The FOUR rung ladders (KPI / chart / rail). C and D derive from the content heights measured
# by K's probe (1:1, 1440 stage, sandbox fallback font — see the report's UNPROVEN): KPI 156 ·
# chart 344 · rail 271. "down" = floor to the 8px grid, "up" = ceil to the 8px grid.
CONTENT = {"kpi": 156, "chart": 344, "rail": 271}
MIS = {"kpi": "120px", "chart": "240px", "rail": "96px"}  # L4's column-3 rungs — the ones Dave pointed at ("I do prefer the spacing on 3")
GAP = 4  # the dashboard sub-gutter, canon.css `--bento-gutter:4px` on tpl-group
def down8(v): return (v // 8) * 8
def up8(v): return -((-v) // 8) * 8
LADDERS = [
  dict(id="A", name="Canon today", kpi=int(rungs["kpi"][:-2]), chart=int(rungs["chart"][:-2]), rail=int(rungs["rail"][:-2]),
       sentence="Today's numbers. The KPI rows carry about 40px of air above their content; the rail rung sits under its content and the chart row follows the rail stack, so the floor — not the rung — sets those rows.",
       how="canon.css:%s, as shipped" % ",".join(map(str, rung_lines))),
  dict(id="B", name="Tight", kpi=int(MIS["kpi"][:-2]), chart=int(MIS["chart"][:-2]), rail=int(MIS["rail"][:-2]),
       sentence="All three rungs sit under their content, so no rung ever shows — the content alone sets every row. What you pointed at on the L4 page (column 3 under the floor).",
       how="L4's column-3 rungs; every one below content"),
  dict(id="C", name="Content-fitted", kpi=down8(CONTENT["kpi"]), chart=down8(CONTENT["chart"]), rail=down8(CONTENT["rail"]),
       sentence="Each rung is its group's tallest content rounded DOWN to the 8px grid, so the floor lifts at most 7px and the rung is never doing silent work — the rail's two rows come almost level.",
       how="tallest content per group (KPI %d · chart %d · rail %d) rounded down to 8px" % (CONTENT["kpi"], CONTENT["chart"], CONTENT["rail"])),
  dict(id="D", name="2:1 level ladder", kpi=up8(CONTENT["kpi"]), chart=2 * up8(CONTENT["rail"]) + GAP, rail=up8(CONTENT["rail"]),
       sentence="Each rung is the tallest content rounded UP to the 8px grid and the chart rung is exactly two rail rungs plus the 4px gutter — every row is exactly its rung, the floor idles, and the chart closes level with the rail stack by arithmetic.",
       how="content rounded up to 8px; chart = 2 × rail + %dpx gutter" % GAP),
]

html = []
A = html.append
A("<!DOCTYPE html>\n<html lang=\"en\" data-view=\"fit\" data-themes=\"all\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
A("<title>Rung ladder — four candidates, one dashboard, under the ruled FLOOR (K, #245, 2026-09-03) — RULES NOTHING</title>")
A("<!--\n  RUNG LADDER v1 · lane K · session #245 · 2026-09-03\n  ⛔ THIS PAGE RULES NOTHING. It renders four rung ladders (KPI / chart / rail row units) on identical\n     content under the row-height model Dave ruled tonight — the FLOOR minmax(var(--bento-row-unit),auto)\n     on the NESTED tile grid (canon.css:%d); the OUTER wall stays at --bento-row-unit:auto (canon.css:%d).\n     Which ladder wins is his.\n  SPLICE LEDGER (verbatim regions; file · lines · bytes · sha256[:16]):\n%s\n  The only non-spliced CSS is marked `K CHROME` (this page's own frame) and `K MODEL` (the floor rule,\n  the four ladders and the probe). Nothing in canon.css, any meta, any generator or any snippet was changed.\n-->" % (floor_line, outer_auto_line,
       "\n".join(f"    · {r['region']:<58} {r['file']}:{r['lines']:<13} {r['bytes']:>7} B  {r['sha256_16']}" for r in ledger)))
A("<style id=\"type-css\">\n/* ===== SPLICE · knowledge/canon/type.css · whole file · VERBATIM ===== */\n" + type_css + "\n</style>")
A("<style id=\"canon-tokens\">\n/* ===== SPLICE · knowledge/canon/canon.css · lines 1-%d · VERBATIM ===== */\n" % tok_end + tokens + "\n</style>")
A("<style id=\"canon-auto-bento\">\n/* ===== SPLICE · knowledge/canon/canon.css · lines %d-%d · the top-level AUTO-BENTO block · VERBATIM ===== */\n" % (ab_start, ab_end) + auto_bento + "\n</style>")
A("<style id=\"canon-scope\">\n/* ===== SPLICE · knowledge/canon/canon.css · lines %d-%d · the .cn-template-dashboard-bento scope · VERBATIM ===== */\n" % (sc_start, sc_end) + scope + "\n</style>")
for th in ("legacy", "console", "supercharge"):
    A(f"<style id=\"theme-{th}\">\n/* ===== SPLICE · knowledge/canon/canon.css · {th} root overrides + .cn-template-dashboard-bento overrides · VERBATIM ===== */\n" + theme_root[th] + "\n" + theme_scope[th] + "\n</style>")

ladder_css = "\n".join(
    f".col[data-ladder=\"{L['id']}\"] .cn-template-dashboard-bento .c-bento.tpl-group-kpi{{--bento-row-unit:{L['kpi']}px;}}\n"
    f".col[data-ladder=\"{L['id']}\"] .cn-template-dashboard-bento .c-bento.tpl-group-chart{{--bento-row-unit:{L['chart']}px;}}\n"
    f".col[data-ladder=\"{L['id']}\"] .cn-template-dashboard-bento .c-bento.tpl-group-rail{{--bento-row-unit:{L['rail']}px;}}"
    for L in LADDERS)
A("""<style id="k-model">
/* ===== K MODEL — the ONLY rules that act on the bento and are not a splice. =====
   THE RULED MODEL (Dave, #245, in chat): the FLOOR on the NESTED tile grid — option 2 of the L4 page.
   Selector mirrors canon.css's own `.c-bento__tile.c-bento > .c-bento__grid` with the column in front
   (0,5,0 over canon's 0,3,0). The OUTER wall grid is NOT touched: it keeps the shipped `--bento-row-unit:auto`. */
.col .cn-template-dashboard-bento .c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:minmax(var(--bento-row-unit),auto);}
/* THE FOUR LADDERS — KPI / chart / rail row units, one triple per column. Canon ships %(kpi)s / %(chart)s / %(rail)s at canon.css:%(rl)s. */
%(ladders)s
/* THE PROBE — a hidden fifth stage per frame with rung 0 and no stretch anywhere: it measures the CONTENT height
   of every tile on THIS machine (with THIS font), so C and D can be checked against what is actually painted. */
.col[data-ladder="probe"] .cn-template-dashboard-bento .c-bento.tpl-group{--bento-row-unit:0px;}
.col[data-ladder="probe"] .cn-template-dashboard-bento .c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:auto;align-content:start;}
.col[data-ladder="probe"] .cn-template-dashboard-bento .tpl-wall > .c-bento__grid{align-items:start;}
</style>""" % dict(kpi=rungs["kpi"], chart=rungs["chart"], rail=rungs["rail"], rl=",".join(map(str, rung_lines)), ladders=ladder_css))

A("""<style id="k-chrome">
/* ===== K CHROME — this page's own frame. Colours are canon tokens only (var(--…) from the spliced
   :root); the flag red is var(--rag-error-ink) = #DA1A00 on white / #F6604C in dark (s151-D1). ===== */
*{box-sizing:border-box;}
html{background:var(--page);}
body{margin:0;background:var(--page);color:var(--text);-webkit-font-smoothing:antialiased;}
.pg{max-width:1880px;margin:0 auto;padding:32px 32px 96px;}
.hd{display:grid;grid-template-columns:1fr 1fr;gap:32px;border-top:2px solid var(--text);padding-top:16px;margin-bottom:24px;}
.hd h1{margin:0 0 8px;}
.hd p{margin:0 0 8px;max-width:64ch;}
.kicker{display:block;margin-bottom:12px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;}
.rules{border-top:1px solid var(--divider);margin:0;}
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
html[data-themes="two"] .frame:not([data-theme-key="mono"]):not([data-theme-key="supercharge"]){display:none;}
.frame-cap{display:flex;gap:16px;align-items:baseline;margin-bottom:12px;flex-wrap:wrap;}
.frame-cap .n{color:var(--muted);}
.frame-cap .probe-read{color:var(--muted);margin-left:auto;}
.cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:auto auto;gap:0 20px;align-items:start;}
.col{display:grid;grid-template-rows:subgrid;grid-row:span 2;min-width:0;}
html[data-view="one"] .cols{grid-template-columns:1fr;}
.col[data-ladder="probe"]{position:absolute;visibility:hidden;height:0;overflow:hidden;width:1440px;left:-99999px;}  /* rendered, measured, never seen */
.col-h{display:flex;flex-direction:column;gap:6px;padding:8px 0 10px;border-bottom:1px solid var(--divider);margin-bottom:8px;}
.col-h .t{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;}
.col-h .nums{display:flex;gap:10px;align-items:baseline;white-space:nowrap;margin-top:4px;}
.col-h .nums .sep{color:var(--muted);}
.col-h .nums small{display:block;color:var(--muted);}
.col-h .sent{max-width:52ch;}
.read{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;}
.read b{font-weight:500;}
.flag{color:var(--rag-error-ink);}
.ok{color:var(--muted);}
.point{display:inline-flex;gap:8px;align-items:center;min-height:36px;padding:0 12px;border:1px solid var(--text);cursor:pointer;border-radius:var(--border-radius-control);user-select:none;white-space:nowrap;}
.point:has(input:checked){background:var(--text);color:var(--page);}
.point input{margin:0;}
.viewport{overflow:hidden;border:1px solid var(--divider);align-self:start;}
.stage{width:1440px;transform-origin:0 0;}
/* the page ground the snippet paints on <body> (s219-D1 pageBg) — --wall-ground is declared INSIDE the scope, so it is read there */
.stage .cn-template-dashboard-bento{background:var(--wall-ground);padding-top:24px;}
.cn-template-dashboard-bento .tpl-page{padding-bottom:24px;}
html[data-view="one"] .stage{transform:none !important;}
html[data-view="one"] .viewport{width:1440px;max-width:100%;overflow-x:auto;}
.exp{border-top:2px solid var(--text);padding-top:16px;margin-top:48px;display:grid;grid-template-columns:1fr 1fr;gap:32px;}
.exp textarea{width:100%;min-height:96px;border:1px solid var(--divider);background:var(--page);color:var(--text);padding:8px;resize:vertical;}
.exp pre{border:1px solid var(--divider);padding:12px;min-height:180px;background:var(--surface);}
.foot{margin-top:48px;padding-top:12px;border-top:1px solid var(--divider);color:var(--muted);}
@media (max-width:1200px){.hd,.exp{grid-template-columns:1fr;}.cols{grid-template-columns:1fr 1fr;}}
@media (max-width:760px){.cols{grid-template-columns:1fr;}}
</style>
</head>
<body>""")

A("<template id=\"wall\">" + main_html + "</template>")
A(sprite)

ladders_js = json.dumps([dict(id=L["id"], name=L["name"], kpi=L["kpi"], chart=L["chart"], rail=L["rail"], sentence=L["sentence"], how=L["how"]) for L in LADDERS])
A(f"""<div class="pg">
<header class="hd">
  <div>
    <span class="kicker t-cm-section-label">K · #245 · 2026-09-03 · decision surface · rules nothing</span>
    <h1 class="t-ed-heading-2">Four rung ladders, one dashboard, under the floor you ruled</h1>
    <p class="t-ed-body">Same wall four times — <code>Template-dashboard-bento</code>, the real snippet's <code>&lt;main&gt;</code>, spliced byte-for-byte. Every column runs the row-height model you ruled tonight (the <b>floor</b>, rows never shorter than their rung, free to grow). <b>Only the three rung numbers differ</b> — KPI / chart / rail. Look, point at one, paste the export.</p>
    <p class="t-ed-body-small"><b>How to read a column:</b> the three big numbers are the rungs. Under them, grey text is measured live off the render: what each row actually painted, and whether the rung or the content decided it. <b>Air</b> = the rung is taller than the content (the row shows empty space). <b>Floor lift</b> = the content is taller than the rung (the rung never shows). Red = a tile overrunning its row, which the floor should never allow. The side-by-side view is the 1:1 layout painted smaller (a transform, not a zoom), so the numbers under a column are the same in both views.</p>
  </div>
  <dl class="rules t-ed-body-small">
    <dt class="t-cm-section-label">Held constant</dt><dd>the model: <code>grid-auto-rows:minmax(var(--bento-row-unit),auto)</code> on the nested tile grid (canon.css:{floor_line}) — your option 2 · the outer wall at <code>--bento-row-unit:auto</code> (canon.css:{outer_auto_line}) · the 4px sub-gutter · the content · the stage (1440px, the 6-column band).</dd>
    <dt class="t-cm-section-label">What ships today</dt><dd>column A's numbers: {rungs['kpi']} / {rungs['chart']} / {rungs['rail']} at canon.css:{','.join(map(str, rung_lines))}, under a floor whose max is <code>1fr</code>.</dd>
    <dt class="t-cm-section-label">Not decided here</dt><dd>which ladder wins · the role-name words · anything in <code>_CARRIES.md</code>. The export is a question until you say otherwise.</dd>
  </dl>
</header>

<div class="ctl t-ed-body-small">
  <fieldset><legend>View</legend>
    <label><input type="radio" name="view" value="fit" checked> side by side (scaled to fit)</label>
    <label><input type="radio" name="view" value="one"> 1:1, stacked</label>
  </fieldset>
  <fieldset><legend>Themes</legend>
    <label><input type="radio" name="themes" value="all" checked> all four</label>
    <label><input type="radio" name="themes" value="two"> mono + supercharge only</label>
  </fieldset>
  <span class="ok" id="summary"></span>
</div>
<div id="frames"></div>

<section class="exp" id="export">
  <div>
    <span class="kicker t-cm-section-label">Dave points here → ruling-shaped export</span>
    <p class="t-ed-body-small">Pick a column with its <b>point here</b> control (one pick, page-wide). Add a note if you like. The text on the right is plain and pasteable; it ends in a question until you say otherwise.</p>
    <textarea id="note" class="t-ed-body-small" placeholder="optional note — a number to change, a doubt, a condition"></textarea>
    <p><button class="b t-cm-button" id="copy">Copy export</button> <span class="ok t-ed-caption" id="copied"></span></p>
  </div>
  <pre id="out" class="t-ed-caption"></pre>
</section>
<p class="foot t-ed-caption">Single file · zero external references · type.css + canon.css bento regions spliced verbatim (ledger in the source comment) · driven through <code>page.goto("file://…")</code>, never <code>set_content</code> · filed report <code>notes/_subreports/2026-09-03-245-K-rung-ladder.md</code> · sibling surface <code>reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html</code> (L4).</p>
</div>""")

A("""<script>
(function(){
const THEMES=[["mono","Mono"],["supercharge","Supercharge"],["legacy","Legacy"],["console","Console"]];
const MODES=["light","dark"];
const LADDERS=%(ladders)s;
const GAP=%(gap)d;
const tpl=document.getElementById("wall");
const frames=document.getElementById("frames");
let pick=null; try{pick=localStorage.getItem("k-pick");}catch(e){}
function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;");}
function mkcol(tk,md,L){
  const col=document.createElement("div"); col.className="col"; col.dataset.ladder=L.id;
  if(L.id!=="probe"){
    col.innerHTML='<div class="col-h"><div class="t"><div><span class="t-ed-body"><b>'+L.id+' · '+L.name+'</b></span>'
      +'<div class="nums"><span class="t-ed-heading-1">'+L.kpi+'<small class="t-ed-caption">KPI</small></span><span class="sep t-ed-heading-3">/</span><span class="t-ed-heading-1">'+L.chart+'<small class="t-ed-caption">chart</small></span><span class="sep t-ed-heading-3">/</span><span class="t-ed-heading-1">'+L.rail+'<small class="t-ed-caption">rail</small></span></div></div>'
      +'<label class="point t-cm-button"><input type="radio" name="pick-'+tk+'-'+md+'" value="'+L.id+'"'+(pick===L.id?' checked':'')+'> point here</label></div>'
      +'<span class="sent t-ed-body-small">'+esc(L.sentence)+'</span>'
      +'<span class="t-ed-caption ok">rungs: '+esc(L.how)+'</span>'
      +'<div class="read t-ed-caption"></div></div>';
  }
  col.insertAdjacentHTML("beforeend",'<div class="viewport"><div class="stage"><div data-apollo-theme="'+tk+'" data-theme="'+md+'"><div class="cn-template-dashboard-bento"></div></div></div></div>');
  col.querySelector(".cn-template-dashboard-bento").appendChild(tpl.content.cloneNode(true));
  return col;
}
for(const [tk,tn] of THEMES) for(const md of MODES){
  const f=document.createElement("section"); f.className="frame"; f.dataset.themeKey=tk; f.dataset.mode=md;
  f.innerHTML='<div class="frame-cap"><span class="t-ed-heading-4">'+tn+'</span><span class="n t-ed-body-small">'+md+'</span><span class="probe-read t-ed-caption"></span></div><div class="cols"></div>';
  const cols=f.querySelector(".cols");
  for(const L of LADDERS) cols.appendChild(mkcol(tk,md,L));
  cols.appendChild(mkcol(tk,md,{id:"probe"}));
  frames.appendChild(f);
}
function fit(){
  // transform:scale, NOT css zoom — zoom re-lays out at the fractional size and re-wraps glyphs (L4 measured 6.6px;
  // K's first run measured 8.0px on the tall rail tile). A transform paints the 1:1 layout smaller, so the readouts
  // under a column are the SAME numbers in both views.
  const one=document.documentElement.dataset.view==="one";
  document.querySelectorAll('.col:not([data-ladder="probe"])').forEach(col=>{
    const vp=col.querySelector(".viewport"), st=col.querySelector(".stage");
    const s=one?1:Math.min(1,vp.clientWidth/1440);
    st.style.transform=s===1?"none":"scale("+s+")";
    vp.style.height=s===1?"auto":(st.offsetHeight*s)+"px";
  });
}
function px(s){return s.split(/\\s+/).map(v=>parseFloat(v));}
function r1(v){return Math.round(v*10)/10;}
function groupsOf(col){
  const out=[];
  col.querySelectorAll(".tpl-group").forEach(g=>{
    const grid=g.querySelector(":scope > .c-bento__grid"), cs=getComputedStyle(grid);
    const key=[...g.classList].find(k=>k.startsWith("tpl-group-")).slice(10);
    const tracks=px(cs.gridTemplateRows).map(r1), gap=parseFloat(cs.rowGap)||0;
    const rung=parseFloat(getComputedStyle(g).getPropertyValue("--bento-row-unit"));
    const tiles=[...g.querySelectorAll(":scope > .c-bento__grid > .c-bento__tile")].map(t=>[t.clientHeight,t.scrollHeight]);
    const occupied=tracks.reduce((a,b)=>a+b,0)+gap*(tracks.length-1);
    out.push({group:key,autoRows:cs.gridAutoRows,rung:rung,tracks:tracks,gap:gap,gridHeight:grid.clientHeight,deadBand:r1(grid.clientHeight-occupied),tiles:tiles,tilesOverflowing:tiles.filter(t=>t[1]>t[0]+1).length});
  });
  return out;
}
function measure(){
  const res=[], probes={};
  document.querySelectorAll(".frame").forEach(fr=>{
    const p=fr.querySelector('.col[data-ladder="probe"]'), pg=groupsOf(p), pc={};
    pg.forEach(g=>{pc[g.group]=Math.max(...g.tracks);});
    probes[fr.dataset.themeKey+"/"+fr.dataset.mode]=pc;
    fr.querySelector(".probe-read").textContent="content measures on this machine — KPI "+Math.round(pc.kpi)+" · chart "+Math.round(pc.chart)+" · rail "+Math.round(pc.rail)+" px (rung 0, no stretch)";
    fr.querySelectorAll('.col:not([data-ladder="probe"])').forEach(col=>{
      const L=LADDERS.find(x=>x.id===col.dataset.ladder), read=col.querySelector(".read");
      const wall=col.querySelector(".tpl-wall > .c-bento__grid");
      const r={theme:fr.dataset.themeKey,mode:fr.dataset.mode,ladder:L.id,rungs:{kpi:L.kpi,chart:L.chart,rail:L.rail},content:pc,
               outerAutoRows:getComputedStyle(wall).gridAutoRows,cols:getComputedStyle(wall).gridTemplateColumns.split(" ").length,groups:groupsOf(col)};
      let html='<b>outer wall</b><span>grid-auto-rows <code>'+r.outerAutoRows+'</code> · '+r.cols+' columns · nested model <code>'+r.groups[0].autoRows+'</code></span>';
      r.groups.forEach(g=>{
        const c=pc[g.group]; const air=g.rung-c, lifts=g.tracks.map(t=>r1(t-g.rung));
        let what;
        if(g.group==="chart"){
          // the chart sits beside the rail stack in the outer row, so its one row is always the taller of (its rung, the rail stack)
          const railG=r.groups.find(x=>x.group==="rail"), stack=railG?r1(railG.tracks.reduce((a,b)=>a+b,0)+railG.gap*(railG.tracks.length-1)):null;
          const t=g.tracks[0];
          what=(stack!==null&&Math.abs(t-stack)<=1?'level with the rail stack ('+railG.tracks.join(' + ')+' + '+railG.gap+')':'')
            +(t-g.rung>=1?' · rung '+g.rung+' never shows':' · <b>row is exactly the rung</b>')
            +' · chart content '+Math.round(c)+' → '+Math.round(t-c)+' px of <b>air</b> inside the tile';
          what=what.replace(/^ · /,'');
        }
        else if(air>=1) what='rung above content by '+r1(air)+' px — <b>air</b>';
        else if(lifts.some(l=>l>=1)) what='floor lifted the rows '+lifts.map(l=>Math.max(0,l)).join(' / ')+' px past the rung — <b>content decides</b>';
        else what='rows are exactly the rung';
        html+='<b>'+g.group+'</b><span>rows painted '+g.tracks.join(' / ')+' px · '+what
          +(g.deadBand>1?' · dead band '+g.deadBand+' px':'')
          +(g.tilesOverflowing?' · <span class="flag">'+g.tilesOverflowing+' tile'+(g.tilesOverflowing>1?'s':'')+' overrun'+(g.tilesOverflowing>1?'':'s')+' its row — BREAKS</span>':'')+'</span>';
      });
      // C and D are derived from content: say so live, and flag if this machine's content moves them off their derivation
      if(L.id==="C"){const want={kpi:Math.floor(pc.kpi/8)*8,chart:Math.floor(pc.chart/8)*8,rail:Math.floor(pc.rail/8)*8}; const ok=want.kpi===L.kpi&&want.chart===L.chart&&want.rail===L.rail; r.derivationHolds=ok;
        html+='<b>check</b><span>'+(ok?'rungs = content rounded down on this machine':'<span class="flag">on this machine content-down would be '+want.kpi+' / '+want.chart+' / '+want.rail+' — the font moved it</span>')+'</span>';}
      if(L.id==="D"){const up=v=>Math.ceil(v/8)*8; const want={kpi:up(pc.kpi),rail:up(pc.rail)}; want.chart=2*want.rail+GAP; const ok=want.kpi===L.kpi&&want.chart===L.chart&&want.rail===L.rail; r.derivationHolds=ok;
        html+='<b>check</b><span>'+(ok?'rungs = content rounded up, chart = 2 × rail + '+GAP:'<span class="flag">on this machine it would be '+want.kpi+' / '+want.chart+' / '+want.rail+' — the font moved it</span>')+'</span>';}
      read.innerHTML=html; res.push(r);
    });
  });
  window.__K=res; window.__Kprobe=probes;
  const broken=res.filter(r=>r.groups.some(g=>g.tilesOverflowing)).length, airy=res.filter(r=>r.groups.some(g=>g.rung-r.content[g.group]>=1)).length;
  document.getElementById("summary").textContent=res.length+" renders · "+broken+" with a tile overrunning its row · "+airy+" where some rung is taller than its content (air)";
  render();
  return res;
}
window.__Kmeasure=measure;
document.querySelectorAll('input[name="view"]').forEach(i=>i.addEventListener("change",e=>{document.documentElement.dataset.view=e.target.value; fit(); measure();}));
document.querySelectorAll('input[name="themes"]').forEach(i=>i.addEventListener("change",e=>{document.documentElement.dataset.themes=e.target.value; fit(); measure();}));
document.querySelectorAll('input[name^="pick-"]').forEach(i=>i.addEventListener("change",e=>{pick=e.target.value; try{localStorage.setItem("k-pick",pick);}catch(_){}; document.querySelectorAll('input[name^="pick-"]').forEach(o=>{o.checked=(o.value===pick);}); render();}));
document.getElementById("note").addEventListener("input",render);
document.getElementById("copy").addEventListener("click",()=>{const t=document.getElementById("out").textContent; (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{document.getElementById("copied").textContent="copied";},()=>{document.getElementById("copied").textContent="select the text and copy";});});
function render(){
  const L=LADDERS.find(x=>x.id===pick);
  const res=window.__K||[];
  const seen=THEMES.map(t=>t[0]).join(", ")+" × light, dark";
  const note=document.getElementById("note").value.trim();
  let out="RULING-SHAPED — NOT A RULING UNTIL DAVE SAYS SO\\n";
  out+="subject: the rung ladder (KPI / chart / rail --bento-row-unit) of Template-dashboard-bento, under the ruled FLOOR minmax(rung, auto) on the nested tile grid; outer wall held at auto\\n";
  out+="surface: reviews/RUNG-LADDER-2026-09-03-v1.html (K, #245) · themes seen: "+seen+" · stage 1440px = 6-column band\\n";
  if(!L){ out+="pointed at: (nothing yet — use a column's 'point here' control)\\n"; }
  else{
    out+="pointed at: column "+L.id+" — "+L.name+" — KPI "+L.kpi+" / chart "+L.chart+" / rail "+L.rail+"\\n";
    out+="css it would mean: .c-bento.tpl-group-kpi{--bento-row-unit:"+L.kpi+"px} .c-bento.tpl-group-chart{--bento-row-unit:"+L.chart+"px} .c-bento.tpl-group-rail{--bento-row-unit:"+L.rail+"px}\\n";
    const rs=res.filter(r=>r.ladder===L.id);
    if(rs.length){ const m=rs[0]; out+="measured (mono/light on this machine): "+m.groups.map(g=>g.group+" rows "+g.tracks.join("/")+" px").join(" · ")+" · content KPI "+m.content.kpi+" / chart "+m.content.chart+" / rail "+m.content.rail+"\\n"; }
  }
  out+="question for Dave: is this the rung ladder the dashboard bento carries under the floor — A 196/380/184 (canon) · B 120/240/96 (tight) · C "+LADDERS[2].kpi+"/"+LADDERS[2].chart+"/"+LADDERS[2].rail+" (content-fitted) · D "+LADDERS[3].kpi+"/"+LADDERS[3].chart+"/"+LADDERS[3].rail+" (2:1 level) · other?\\n";
  if(note) out+="note: "+note+"\\n";
  out+="carried open (not touched here): the role-name words · everything in _CARRIES.md";
  document.getElementById("out").textContent=out;
}
new ResizeObserver(()=>{fit();}).observe(document.body);
fit(); requestAnimationFrame(()=>{fit(); measure(); fit();});
document.fonts&&document.fonts.ready.then(()=>{fit(); measure(); fit();});
})();
</script>
</body>
</html>""" % dict(ladders=ladders_js, gap=GAP))

out = "\n".join(html)
for bad in ('src="', "@import", 'href="../', "https://", "http://", "url("):
    n = out.count(bad)
    if n:
        print(f"WARN external-looking token {bad!r} × {n}", file=sys.stderr)
OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT.relative_to(REPO)}  {len(out.encode('utf-8')):,} B")
print(f"markers: floor rule canon.css:{floor_line} · outer auto canon.css:{outer_auto_line} · rungs {rungs} at {rung_lines}")
for L in LADDERS:
    print(f"  {L['id']} {L['name']:<18} {L['kpi']:>4} / {L['chart']:>4} / {L['rail']:>4}   {L['how']}")
for r in ledger:
    print(f"  {r['region']:<58} {r['file']}:{r['lines']:<13} {r['bytes']:>7} B  {r['sha256_16']}")
(HERE / "splice-ledger.json").write_text(json.dumps(dict(ledger=ledger, markers=dict(floor=floor_line, fixed=fixed_line, outer_auto=outer_auto_line, rungs=rungs, rung_lines=rung_lines), content=CONTENT, gap=GAP,
    ladders=[dict(id=L["id"], name=L["name"], kpi=L["kpi"], chart=L["chart"], rail=L["rail"], how=L["how"]) for L in LADDERS]), indent=1), encoding="utf-8")
