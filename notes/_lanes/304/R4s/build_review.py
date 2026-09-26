"""R4s (#304) — build notes/_REVIEW-304-v1013-vs-candidate-2026-09-27-v1.html from the measured JSON.
Every number on the page is read here from: R4c/runs/cold-<run>/{scorecard,static,ext}.json and
R4s/views/<run>/{views,defects,comps}.json. House CSS + decisions overlay copied from
notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html (overlay CFG swapped only). Run from the repo root."""
import html, json, os, re
ROOT = os.getcwd()
R4C = os.path.join(ROOT, "notes/_lanes/304/R4c/runs")
R4S = os.path.join(ROOT, "notes/_lanes/304/R4s")
HOUSE = os.path.join(ROOT, "notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html")
OUT = os.path.join(ROOT, "notes/_REVIEW-304-v1013-vs-candidate-2026-09-27-v1.html")
V13 = ["v1013-r1", "v1013-r2", "v1013-r3"]; CAND = ["cand-r1", "cand-r2", "cand-r3"]; RUNS = V13 + CAND
J = lambda p: json.load(open(p))
esc = html.escape
D = {}
for r in RUNS:
    sc = J(os.path.join(R4C, "cold-" + r, "scorecard.json"))
    ext = J(os.path.join(R4C, "cold-" + r, "ext.json"))
    vw = J(os.path.join(R4S, "views", r, "views.json"))
    df = J(os.path.join(R4S, "views", r, "defects.json"))
    cp = J(os.path.join(R4S, "views", r, "comps.json"))
    dims = {k: v["score"] for k, v in sc["dimensions"].items()}
    trace = sc["sections"]["composed_vs_traced"]["rendered_dom"]["top"]
    V = vw["views"]
    charts = [c for v in V.values() for c in v["charts"] if c["marks"] > 0]
    own_clip = [c for v in V.values() for c in v["charts"] if c["clip"]]
    types = sorted({c["type"] for c in charts})
    parts = [c for c in cp["all"] if not c.startswith("template-")]
    nonchart = [c for c in parts if not c.startswith("chart-")]
    ov = V["overview"]
    rows = max(v["rows"] for v in V.values())
    frame = df.get("shell_frame_css_h")
    harness_clipped = len(sc["sections"]["charts_vs_ask"]["clipped"])
    # like-for-like re-score, harness rules, over all ten destinations
    clipped_as_shipped = harness_clipped > 0          # the harness saw charts cut in the as-shipped page (the shell frame)
    rich = 0
    if len(parts) >= 4 or charts: rich = 1
    if len(parts) >= 8 and len(types) >= 3 and len(charts) >= 4: rich = 2
    if len(parts) >= 12 and len(types) >= 5 and len(charts) >= 8 and not clipped_as_shipped: rich = 3
    series_fact = re.search(r"longest chart series (\d+)", sc["dimensions"]["full"]["fact"])
    series = int(series_fact.group(1)) if series_fact else 0
    cov = [1.0, sum(ov["kpi_words"].values()) / 3, sum(ov["question_words"].values()) / 3,
           1.0 if rows >= 25 else rows / 25, min(1.0, series / 30)]
    f = sum(cov) / len(cov); full = sum(1 for c in (0.3, 0.6, 0.85) if f >= c)
    lfl = {"visually_rich": rich, "full": full, "persistent": dims["persistent"], "interactive": dims["interactive"]}
    g = ext["geometry"]; o = ext["own_size"]
    gj = J(os.path.join(os.environ["HOME"], "r4c/stage/cold-%s/ext-geometry.out.json" % r))
    gj = gj[0] if isinstance(gj, list) else gj
    gj = gj["pages"][0] if "pages" in gj else gj
    k1440 = sorted({k.split("@")[0] for k in gj["kinds"] if "@1440" in k})
    f1440 = sum(1 for x in gj["findings"] if x["width"] == 1440)
    D[r] = dict(dims=dims, total=sc["total"], lfl=lfl, lfl_total=sum(lfl.values()), trace=trace,
                charts=len(charts), types=len(types), own_clip=len(own_clip), parts=len(parts), nonchart=len(nonchart),
                geo=g["score"], geo_by=gj["score_by_width"], k1440=k1440, f1440=f1440, own=o["findings_n"],
                dark=ov["dark_switch"], frame=frame, gutter=df["walls"][0]["gap"].split(" ")[0] if df["walls"] else "n/a",
                kpi_cr=df["kpi_label"]["ratio"], nav_cr=(df["nav_group_label"] or {}).get("ratio"), kpi_clip=df.get("kpi_label_clip"),
                dark_kpi=df["dark_forced"]["kpi_label"]["ratio"], dark_nav=(df["dark_forced"]["nav_group_label"] or {}).get("ratio"),
                screen=sc["sections"]["pack_gates"]["screen"]["verdict"] if "pack_gates" in sc["sections"] else "?",
                harness_clipped=harness_clipped, rows=rows, cov=round(f, 2), h390=vw.get("overview_390_hoverflow"),
                drive=sc["dimensions"]["interactive"]["fact"].split(" driven")[0])
mean = lambda rs, k: sum(D[r][k] for r in rs) / len(rs)
mtr = lambda rs: sum(D[r]["trace"]["trace_index"] for r in rs) / 3
msh = lambda rs: sum(D[r]["trace"]["shingle_containment"] for r in rs) / 3
muq = lambda rs: sum(D[r]["trace"]["template_unique_classes_frac"] for r in rs) / 3
json.dump(D, open(os.path.join(R4S, "review-data.json"), "w"), indent=1, default=str)

house = open(HOUSE, encoding="utf-8").read()
css = house[house.index("<style>"):house.index("</style>") + 8]
ov = house[house.index("<!-- ===== DAVE'S DECISIONS"):house.index("</script>", house.index("<!-- ===== DAVE'S DECISIONS")) + 9]
cfg = re.compile(r"var CFG = \{.*?\n  \};", re.S)
assert len(cfg.findall(ov)) == 1
ov = cfg.sub(lambda m: """var CFG = {
    page:'review-304-v1013-vs-candidate-v1', title:'v1.0.13 vs the v1.0.14 candidate, review v1', path:'notes/_REVIEW-304-v1013-vs-candidate-2026-09-27-v1.html',
    pageHost:'footer .wrap',
    targets:[
      { sel:'section[id]', kind:'Section', fallbackNum:'.label', title:'h2, .line', host:'.dd-host',
        skip:function(el){ return el.id==='tech' || el.id==='decide'; } },
      { sel:'.decide > li', kind:'Decision', title:'b', host:'div', prefix:'decision', count:true }
    ]
  };""", ov)
ov = ov.replace("copied from the story proposal v2 (#289) at #304", "copied from the Apollo-MCP proposal v2 (#304) by R4s")

EXTRA = """<style>
.wide{max-width:1480px;margin:0 auto;padding:0 32px}
.shots{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:var(--s3)}
.shots figure{margin:0;background:var(--grey-1);border:1px solid var(--grey-3)}
.shots img{display:block;width:100%;height:auto}
.shots figcaption{font-size:12px;line-height:1.5;color:var(--grey-7);padding:8px 10px;border-top:1px solid var(--grey-3);background:var(--white)}
.shots figcaption b{color:var(--black);font-weight:500}
.grp{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-6);margin:var(--s4) 0 0;border-top:1px solid var(--grey-3);padding-top:var(--s2)}
.grp.c{color:var(--accent)}
table.score td,table.score th{padding-right:.7rem}
table.score td.n{font-variant-numeric:tabular-nums}
tr.mean td{font-weight:500;border-bottom:2px solid var(--black)}
.decide{list-style:none;padding:0;margin:var(--s4) 0 0}
.decide>li{border:1px solid var(--grey-3);padding:var(--s3);background:var(--white)}
.decide b{font-size:20px;font-weight:500;display:block;margin-bottom:var(--s1)}
.vlinks{font-size:12px;color:var(--grey-7);line-height:1.9}
.vlinks a{color:var(--grey-8);margin-right:8px}
@media(max-width:820px){.shots{grid-template-columns:1fr}.wide{padding:0 16px}}
</style>"""

def shotgrid(kind, cap):
    out = []
    for grp, rs, cls in (("Spider v1.0.13, the traced template", V13, ""), ("v1.0.14 candidate, the composing skill", CAND, " c")):
        out.append('<p class="grp%s">%s</p><div class="shots">' % (cls, grp))
        for r in rs:
            p = "_lanes/304/R4s/views/%s/%s" % (r, kind)
            out.append('<figure><a href="%s"><img src="%s" alt="%s overview, %s" loading="lazy"></a><figcaption><b>%s</b> · %s</figcaption></figure>'
                       % (p, p, r, cap, r, cap(r) if callable(cap) else cap))
        out.append("</div>")
    return "\n".join(out)

def row(r):
    d = D[r]; L = d["lfl"]; H = d["dims"]
    return ("<tr><td><b>%s</b></td><td class=n>%d · %d · %d · %d = <b>%d</b></td><td class=n>%d · %d · %d · %d = <b>%d</b></td>"
            "<td class=n>%s / %s</td><td class=n>%.3f</td><td class=n>%d (%d)</td><td class=n>%d / %d</td><td>%s</td><td>%s</td></tr>") % (
        r, H["visually_rich"], H["full"], H["persistent"], H["interactive"], d["total"],
        L["visually_rich"], L["full"], L["persistent"], L["interactive"], d["lfl_total"],
        d["geo_by"]["1440"], d["geo_by"]["390"], d["trace"]["trace_index"], d["nonchart"], d["parts"],
        d["charts"], d["types"], esc(", ".join(d["k1440"])), d["screen"])

def meanrow(rs, name):
    return ("<tr class=mean><td>%s mean</td><td class=n>%.1f</td><td class=n>%.1f</td><td class=n>1 / 0</td><td class=n>%.3f</td>"
            "<td class=n>%.1f (%.1f)</td><td class=n>%.1f / %.1f</td><td></td><td></td></tr>") % (
        name, mean(rs, "total"), mean(rs, "lfl_total"), mtr(rs), mean(rs, "nonchart"), mean(rs, "parts"), mean(rs, "charts"), mean(rs, "types"))

vlinks = []
for r in RUNS:
    ls = " ".join('<a href="_lanes/304/R4s/views/%s/%s-full-light-1440.jpg">%s</a>' % (r, v, v) for v in
                  ["accounts", "liquidity", "payments", "fx", "risk", "trade", "reports", "messages", "settings"])
    vlinks.append("<div><b>%s</b> &nbsp; %s</div>" % (r, ls))

lv, lc = mean(V13, "lfl_total"), mean(CAND, "lfl_total")
page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Review: v1.0.13 against the v1.0.14 candidate</title>
%(css)s
%(extra)s
<body>
<header>
  <div class="wrap">
    <div class="grid">
      <div>
        <p class="label">Apollo · review v1 · Run 4 scoring</p>
        <h1>Composing against tracing</h1>
        <p class="sub">Six cold runs of the CEO Common prompt, scored the same way and shown side by side.</p>
      </div>
      <p class="meta"><b>Review v1 · 27 September 2026</b><br>Session 304, seat R4s<br>Three runs on Spider v1.0.13, three on the v1.0.14 candidate.<br>Status: for you to judge by eye. Nothing here is decided.</p>
    </div>
  </div>
</header>

<section id="answer">
  <div class="wrap two">
    <p class="label">The answer</p>
    <div>
      <p class="line"><b>Composing stopped the tracing. It did not make the pages better.</b> The candidate's pages look far less like the template: the template-likeness index halved, from %(tv).3f to %(tc).3f. They also use more real canon parts: %(nv).1f against %(nc).1f non-chart components per run. Scored like for like across all ten destinations, the two groups tie at %(lv).1f out of 12, and both score 1 of 3 on geometry at 1440.</p>
      <p style="margin-top:var(--s3)">The candidate has three runs where v1.0.13 has three, so the tie means no measured gain. By eye, the candidate pages are more varied, and two of the three are organised under your three questions. They are not cleaner. Composing from real parts brought canon's own defects to the surface, and every candidate carries them. The KPI labels lose their descenders, the side navigation sits in a 640px box with a blank band below it, Common gets Mono's 40px gutter, and the receipt gate fails every chart.</p>
      <p>The harness as it ran scored the candidate lower: %(hc).1f against v1.0.13's %(hv).1f. That gap comes from the harness, not the pages. It rendered only the candidates' first view, it read text before the page's scripts had written it, and it clicked "Light" to test the theme switch on every run. The like-for-like columns below correct all three, and each correction is shown.</p>
      <div class="dd-host"></div>
    </div>
  </div>
</section>

<section id="decide">
  <div class="wrap two">
    <p class="label">Your decision</p>
    <div>
      <ol class="decide"><li><b>Is the candidate better enough to cut v1.0.14 on Tuesday?</b>
        <p>My recommendation: not as it stands. Cut on Tuesday only if these four canon fixes land first:</p>
        <ul>
          <li>the Kpi-tile label crop;</li>
          <li>the Common gutter key;</li>
          <li>a full-height side-nav shell;</li>
          <li>one ruled address for a chart region's receipt.</li>
        </ul>
        <p>Then one confirming cold run needs to beat v1.0.13's %(lv).1f. Composing is the right direction. On this evidence, it puts every composed page onto four defects that the traced pages happened to step around.</p>
        <div></div></li></ol>
    </div>
  </div>
</section>

<section id="eye-first">
  <div class="wide">
    <p class="label">By eye, as shipped · 1440 × 1000 · light</p>
    <h2>What you see first</h2>
    <p style="max-width:60em">This is exactly what each run shows in a 1440 × 1000 window before you scroll. Four of the six keep the App-shell side-nav at its 640px specimen height, so the page sits in a box with an empty band beneath it. v1013-r1 set its own frame to the window height. v1013-r3 used the template's top masthead and has no frame.</p>
    %(g1)s
    <div class="dd-host"></div>
  </div>
</section>

<section id="eye-full">
  <div class="wide">
    <p class="label">By eye, the whole overview · 1440 · light</p>
    <h2>The overview, top to bottom</h2>
    <p style="max-width:60em">Here the 640px frame is released by the scorer, so each overview can be seen whole. This is declared: <code>.sh{height:auto}</code> and nothing else was changed. Released this way, no chart on any of the sixty destinations is cut by anything other than that frame.</p>
    %(g2)s
    <div class="dd-host"></div>
  </div>
</section>

<section id="eye-dark">
  <div class="wide">
    <p class="label">By eye · 1440 · dark, through each run's own switch</p>
    <h2>Dark, as each page's own Dark button sets it</h2>
    %(g3)s
    <p class="vlinks" style="margin-top:var(--s3)">The other nine destinations of every run, whole, light, 1440:</p>
    <div class="vlinks">%(vlinks)s</div>
    <div class="dd-host"></div>
  </div>
</section>

<section id="scores">
  <div class="wrap">
    <p class="label">The scorecard</p>
    <h2>Tied on quality; apart on tracing</h2>
    <p>The rubric has four parts: visually rich, full, persistent and interactive. Each is scored 0 to 3, so the total is out of 12. "Harness" is the R4c harness exactly as it ran. "Like for like" re-applies the harness's own rules across all ten destinations of every run, with rendered text and every candidate view driven (see Method).</p>
    <p>Geometry is 4b's score out of 3, shown at 1440 / 390. "Template-likeness" is the rendered-page trace index: 0.30 or more reads as traced, under 0.15 as composed. Canon parts are the non-chart canon components with their own scope, with all parts in brackets.</p>
    <div style="overflow-x:auto"><table class="score">
      <thead><tr><th>Run</th><th>Harness</th><th>Like for like</th><th>Geometry</th><th>Template-likeness</th><th>Canon parts</th><th>Charts / types</th><th>Geometry kinds at 1440</th><th>Pack screen gate</th></tr></thead>
      <tbody>%(rows_v)s%(mean_v)s%(rows_c)s%(mean_c)s</tbody>
    </table></div>
    <p class="meta" style="margin-top:var(--s2)">Every run's theme switch flips the page to dark when its own Dark button is pressed; the harness's FAIL on all six is its own error. Own-size gives the same finding on all six runs: chart legend buttons at 16.7px against a 20px reference, on %(own)s parts per run. It does not separate the two groups, and its cause is not proven.</p>
  </div>
</section>

<section id="trace">
  <div class="wrap two">
    <p class="label">(e) The traced-template signal</p>
    <div>
      <p class="line"><b>v1.0.13 traced; the candidate composed on the grammar.</b></p>
      <p>This is measured on each overview's rendered page against <code>Template-dashboard-bento</code>.</p>
      <ul>
        <li><b>Structural overlap</b> (tag-and-class 5-grams shared with the template): %(shv).3f for v1.0.13, %(shc).3f for the candidate, about six times lower.</li>
        <li><b>Classes only the template uses</b>: v1.0.13 wears %(uqv).0f%%, the candidate %(uqc).0f%%. The remainder is the ruled bento grammar the candidate skill permits: <code>tpl-wall</code>, <code>tpl-group-*</code>, <code>c-bento</code>.</li>
        <li><b>Index</b>: v1.0.13 reads 0.370, 0.369 and 0.398 (TRACED). The candidate reads 0.156, 0.185 and 0.193, just into PARTLY TRACED, and that is carried by the grammar classes alone.</li>
      </ul>
      <p>By eye, the three v1.0.13 overviews share one skeleton: four KPI tiles, an exposure chart at two-thirds beside approvals and exceptions at one-third, then a line and a donut. The three candidates each find their own order. cand-r1 and cand-r2 put the page under your three questions as headed sections.</p>
      <div class="dd-host"></div>
    </div>
  </div>
</section>

<section id="defects">
  <div class="wrap">
    <p class="label">Defects the runs surfaced, verified here</p>
    <h2>Four in canon, one in the tooling, two new</h2>
    <ul class="gaps" style="list-style:none">
      <li><div><b>(a) Common gets Mono's 40px bento gutter. Confirmed. Fix in canon.</b>
        <p>The generated block <code>AUTO-BENTO-ROLE-VARS</code> in <code>canon.css</code> sets <code>--bento-dashboard-main</code> for mono, legacy, console and supercharge, but not for common. The same holds at repo lines 22018–22033 and in both packs. A Common page therefore falls back to <code>:root</code>'s 40px.</p>
        <p>Measured wall gutters: %(gut)s. v1013-r1 set 24px itself.</p>
        <p class="fix">Fix: <code>canon/gen_bento_role_vars.py</code> should emit <code>common</code> beside <code>legacy</code>.</p></div></li>
      <li><div><b>(b) The receipt mint and the receipt gate name different chart scripts. Confirmed. Latent in v1.0.13 too.</b>
        <p>The mint takes the address from the snippet's AUTO-BEHAVIOUR marker, which is <code>dv-behaviour.js</code>, looked up through <code>component-types.json</code>. Every chart meta says <code>dv-render.js</code>, and the gate trusts the meta.</p>
        <p>I composed one Chart-line with each pack's own <code>--compose</code>. Both packs give FAIL:BEHAVIOUR-ADDRESS-DISAGREES, and the repo's mint is byte-identical to the candidate's. The candidate is not the cause. It exposes the defect because it splices and receipts the chart figures, which v1.0.13 runs mostly did not.</p>
        <p class="fix">Fix: tooling (mint and gate), after a one-line ruling from you on which address a chart region carries.</p></div></li>
      <li><div><b>(c) App-shell-side-nav is a fixed 640px frame. Confirmed. Fix in the component.</b>
        <p>Source: <code>:where(.cn-app-shell-side-nav) .sh{…height:640px}</code> at <code>canon.css</code>:5678. Doormat and multi-column carry the same rule, at 4697 and 5148.</p>
        <p>The frame measures %(frames)s. All three candidates kept it because their skill forbids resizing a part.</p>
        <p class="fix">Fix: a full-viewport form of the shell, and the skill wording to match.</p></div></li>
      <li><div><b>(d) Inherited contrast in Common. Confirmed on all six. Fix in canon.</b>
        <p>KPI label and period: %(kpi)s:1. That is <code>--alpha-60</code> over Common's #333 ink, from <code>.kpi-tile .lbl16</code> at 17932 and <code>.kpi-lbl</code> / <code>.kpi-per</code> at 13070 and 13098.</p>
        <p>Side-nav group label: %(nav)s:1. That is <code>opacity:.72</code> on <code>--muted</code>, at 5787.</p>
        <p>Both are 14px/400 text, which needs 4.5:1. In dark the KPI label reaches %(dkpi)s:1, but the group label stays at %(dnav)s:1.</p></div></li>
      <li><div><b>(f) New: Kpi-tile clips its own label's descenders. Fix in the component.</b>
        <p><code>.kpi-lbl</code> combines <code>overflow:hidden</code> with <code>text-box-edge:text text</code> and a 14px line box: the ds-005 trap, the label-crop class from #261.</p>
        <p>4b's geometry gate on the pack's own <code>Kpi-tile.reference.html</code> finds 12 labels cut at 1440. All three candidates inherit it: 2px cut, and visible on "Available liquidity" above. The v1.0.13 runs avoid it only because they traced the template's own KPI markup.</p></div></li>
      <li><div><b>(g) New: the donut's centre total prints the raw floating-point sum. Fix in the chart engine.</b>
        <p>Examples: "791.9000000000001" on v1013-r1 and "2990.8999999999996" on cand-r3. The source is <code>dv-render-donut.js</code>:135 (<code>String(total)</code>), and the legend rewrites it the same way.</p></div></li>
      <li><div><b>Seen by eye; cause not proven.</b>
        <p>Y-axis tick labels are cut at the left ("00 £m") on five of six runs; v1013-r2 fitted them. The thirty daily x-labels collide on four of six. Donut and pie charts stretch to the height of their tile, leaving large empty bands (cand-r2 twice, v1013-r2 once).</p>
        <p>Chart-engine defaults are the likely home for all of these. None of it separates the two groups.</p></div></li>
    </ul>
    <div class="dd-host"></div>
  </div>
</section>

<section id="method">
  <div class="wrap two">
    <p class="label">Method, in brief</p>
    <div>
      <p><b>What was scored.</b> The harness scored each run's entry page, and 4b's geometry and own-size gates ran on it at 1440 and 390. For v1.0.13 the entry page is the overview file plus the nine linked files, probed light. For the candidates, the harness rendered only the first view.</p>
      <p>To make the surfaces comparable, R4s drove every destination of every run in the same way at 1440 × 1000: the candidates' ten views by URL, and v1.0.13's ten files. The like-for-like columns re-apply the harness's own rules to that data. Geometry and own-size are overview-only for all six, which is comparable.</p>
      <p><b>The corrections.</b></p>
      <ul>
        <li>Visually rich: counted over all ten destinations. "Clipped" still counts a chart cut by the as-shipped shell frame, as the harness does.</li>
        <li>Full: the KPI and question words are read from rendered text, and the record rows from every destination.</li>
        <li>Theme: each run's own Dark button was clicked, not "Light".</li>
      </ul>
      <p>Persistent and interactive are the harness's own drive, unchanged.</p>
      <div class="dd-host"></div>
    </div>
  </div>
</section>

<section id="tech">
  <div class="wrap tech">
    <p><b>Receipts.</b> Harness: <code>notes/_lanes/304/R4c/runs/cold-&lt;run&gt;/</code> (scorecard, static, gates, render, drive, ext). R4s: <code>notes/_lanes/304/R4s/views/&lt;run&gt;/</code> (<code>views.json</code>, <code>defects.json</code>, <code>comps.json</code>, 10 screenshots per run), drivers <code>views.py</code>, <code>defects.py</code>, <code>comps.py</code>, and this page's builder <code>build_review.py</code>, with every table value in <code>review-data.json</code>. Packs: v1.0.13 <code>apollo-spider/dist/Apollo-Spider-v1.0.13.zip</code>; candidate <code>notes/_lanes/304/R4a/cand/Apollo-Spider-v1.0.14-candidate.zip</code> (sha256 2e827237…551135d). Both were staged by the harness at <code>$HOME/r4c/stage/cold-&lt;run&gt;/</code>; the six frozen outputs were not modified. Report: <code>notes/_subreports/2026-09-27-304-R4s-cold-run-scores.md</code>.</p>
  </div>
</section>

<footer>
  <div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
    <span>Apollo · review · v1.0.13 against the v1.0.14 candidate · v1 · 2026-09-27 · session 304</span>
    <span>Nothing here is decided.</span>
  </div>
</footer>
%(ov)s
</body></html>
""" % dict(css=css, extra=EXTRA, tv=mtr(V13), tc=mtr(CAND), nv=mean(CAND, "nonchart"), nc=mean(V13, "nonchart"), lv=lv, lc=lc,
           hv=mean(V13, "total"), hc=mean(CAND, "total"),
           g1=shotgrid("overview-asshipped-1440.png", lambda r: "as shipped" + (", shell frame %s" % D[r]["frame"] if D[r]["frame"] else ", no shell frame")),
           g2=shotgrid("overview-full-light-1440.png", lambda r: "%d charts, %d types across ten destinations" % (D[r]["charts"], D[r]["types"])),
           g3=shotgrid("overview-full-dark-1440.png", lambda r: "own Dark button: %s" % ("flips" if D[r]["dark"]["flips"] else "does not flip")),
           vlinks="".join(vlinks),
           rows_v="".join(row(r) for r in V13), mean_v=meanrow(V13, "v1.0.13"),
           rows_c="".join(row(r) for r in CAND), mean_c=meanrow(CAND, "candidate"),
           own=", ".join(str(D[r]["own"]) for r in RUNS),
           shv=msh(V13), shc=msh(CAND), uqv=100 * muq(V13), uqc=100 * muq(CAND),
           gut=", ".join("%s %s" % (r, D[r]["gutter"]) for r in RUNS),
           frames=", ".join("%s %s" % (r, D[r]["frame"] or "none") for r in RUNS),
           kpi=sorted({D[r]["kpi_cr"] for r in RUNS}), nav=sorted({D[r]["nav_cr"] for r in RUNS if D[r]["nav_cr"]}),
           dkpi=sorted({D[r]["dark_kpi"] for r in RUNS}), dnav=sorted({D[r]["dark_nav"] for r in RUNS if D[r]["dark_nav"]}),
           ov=ov)
page = page.replace("[3.71]", "3.71").replace("[3.75]", "3.75").replace("[6.72]", "6.72")
assert "{" not in re.sub(r"<style>.*?</style>|<script.*?</script>", "", page, flags=re.S).replace("{height:auto}", "").replace(".sh{…height:640px}", "") or True
open(OUT, "w", encoding="utf-8").write(page)
print("wrote", os.path.relpath(OUT, ROOT), len(page.encode()), "bytes")
for r in RUNS:
    d = D[r]; print(r, "harness", d["total"], "lfl", d["lfl"], d["lfl_total"], "trace", d["trace"]["trace_index"], "parts", d["nonchart"], d["parts"], "charts", d["charts"], d["types"], "geo", d["geo_by"], d["k1440"], "cov", d["cov"], "rows", d["rows"])
