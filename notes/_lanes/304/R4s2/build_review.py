"""build_review.py — R4s2 (#304): builds notes/_REVIEW-304-candidate-2-2026-09-27-v1.html.
House CSS = the R4s review page's head styles (themselves the proposal page's, plus the shots styles);
the decisions overlay = copied verbatim from notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html with only CFG swapped.
Every number is read from notes/_lanes/304/R4s2/ink-sets.json and the harness scorecards."""
import json, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); NOTES = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(NOTES, "_REVIEW-304-candidate-2-2026-09-27-v1.html")
r4s = open(os.path.join(NOTES, "_REVIEW-304-v1013-vs-candidate-2026-09-27-v1.html")).read()
prop = open(os.path.join(NOTES, "_PROPOSAL-apollo-mcp-2026-09-26-v2.html")).read()
head_css = r4s[r4s.index("<style>"):r4s.index("<body>")]
overlay = prop[prop.index("<!-- ===== DAVE'S DECISIONS"):]
overlay = overlay.replace("copied from the story proposal v2 (#289) at #304", "copied from the Apollo-MCP proposal v2 (#304) by R4s2")
cfg_new = """var CFG = {
    page:'review-304-candidate-2-v1', title:'Candidate 2 scored, review v1', path:'notes/_REVIEW-304-candidate-2-2026-09-27-v1.html',
    pageHost:'footer .wrap',
    targets:[
      { sel:'section[id]', kind:'Section', fallbackNum:'.label', title:'h2, .line', host:'.dd-host',
        skip:function(el){ return el.id==='tech' || el.id==='decide'; } },
      { sel:'.decide > li', kind:'Decision', title:'b', host:'div', prefix:'decision', count:true }
    ]
  };"""
overlay = re.sub(r"var CFG = \{.*?\n  \};", cfg_new, overlay, count=1, flags=re.S)
assert "review-304-candidate-2-v1" in overlay
D = json.load(open(os.path.join(HERE, "ink-sets.json")))
S = D["sets"]; ADJ = D["adjusted"]
def pv(setname, r): return "%.1f" % S[setname]["runs"][r]["per_view"]
SC = {r: json.load(open(os.path.join(HERE, "runs", "cold-" + r, "scorecard.json"))) for r in ("cand2-r1", "cand2-r2", "cand2-r3")}
e = html.escape
SH = "_lanes/304/R4s2/shots/"
def fig(img, cap, alt):
    return '<figure><a href="%s%s"><img src="%s%s" alt="%s" loading="lazy"></a><figcaption>%s</figcaption></figure>' % (SH, img, SH, img, e(alt), cap)

# ---- score table
C = ["dead", "cut", "collision", "size", "markers"]
rows = []
def row(r, setn, label, a_run=None):
    x = S[setn]["runs"][r]; n = x["n"]; a = x["aff"]
    old = pv("a_w4b_baseline", a_run) if a_run else "—"
    w4a = pv("b_w4a_patched", a_run) if a_run else "—"
    return ("<tr><td><b>%s</b></td><td class=n>%s</td><td class=n>%s</td><td class=n><b>%.1f</b></td><td class=n>%.1f</td>" % (label, old, w4a, x["per_view"], ADJ[r]["adj_per_view"])
            + "".join("<td class=n>%d</td>" % a[c] for c in C) + "</tr>")
def mean(g, setn, label):
    m = S[setn][g]; ao = S["a_w4b_baseline"].get(g, {}).get("per_view"); bo = S["b_w4a_patched"].get(g, {}).get("per_view")
    return ("<tr class=mean><td>%s</td><td class=n>%s</td><td class=n>%s</td><td class=n>%.2f</td><td class=n>%.2f</td>" % (label, ("%.2f" % ao) if ao else "—", ("%.2f" % bo) if bo else "—", m["per_view"], ADJ["_" + g]["adj"])
            + "".join("<td class=n>%.2f</td>" % m["by_class"][c] for c in C) + "</tr>")
for r in ("v1013-r1", "v1013-r2", "v1013-r3"): rows.append(row(r, "c_six_on_cand2_canon", r, r))
rows.append(mean("v1013", "c_six_on_cand2_canon", "v1.0.13 mean"))
for r in ("cand-r1", "cand-r2", "cand-r3"): rows.append(row(r, "c_six_on_cand2_canon", r, r))
rows.append(mean("cand1", "c_six_on_cand2_canon", "candidate 1 mean"))
for r in ("cand2-r1", "cand2-r2", "cand2-r3"): rows.append(row(r, "cand2", r))
rows.append(mean("cand2", "cand2", "candidate 2 mean"))
table = "".join(rows)

def judg(r):
    out = []
    for j in SC[r]["judgment_rows"]:
        ev = j["evidence"]
        if j["id"] == "three_questions": evs = " · ".join(e(x) for x in ev)
        else: evs = "; ".join("%s %s, tile %d%% of the content width" % (e(x["view"]), e(x["type"]), round(100 * x["tile_share_of_content_width"])) for x in ev) or "no ring chart"
        out.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>Dave: ______</td></tr>" % (r, e(j["row"]), evs))
    return "".join(out)
jrows = "".join(judg(r) for r in SC)

page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Review: candidate 2 scored</title>
""" + head_css + """<style>
.shots.two-col{grid-template-columns:repeat(2,1fr)}
.shots.one{grid-template-columns:1fr}
.pill{display:inline-block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding:.1rem .5rem;border:1px solid var(--grey-3);color:var(--grey-7);margin-right:6px;line-height:1.6}
.pill.k{border-color:var(--black);color:var(--black)}
@media(max-width:820px){.shots.two-col{grid-template-columns:1fr}}
</style></head>
<body>
<header>
  <div class="wrap">
    <div class="grid">
      <div>
        <p class="label">Apollo · review v1 · Run 4, candidate 2</p>
        <h1>Candidate 2, scored</h1>
        <p class="sub">Three new cold runs of the CEO Common prompt, measured on every view and set beside the six earlier runs.</p>
      </div>
      <p class="meta"><b>Review v1 · 27 September 2026</b><br>Session 304, seat R4s2<br>Candidate 2 built at 3100da99: the composing skill plus the wave three and four fixes.<br>Status: for you to judge by eye. Nothing here is decided.</p>
    </div>
  </div>
</header>

<section id="answer">
  <div class="wrap two">
    <p class="label">The answer</p>
    <div>
      <p class="line"><b>Candidate 2 carries less ink, and it looks better. Most of the gain is the chart engine, which lifts the old pages too.</b></p>
      <p style="margin-top:var(--s3)">Measured on all ten views, candidate 2's three runs read """ + "%.1f" % S["cand2"]["cand2"]["per_view"] + """ defects per view. The six earlier runs read """ + "%.2f" % S["a_w4b_baseline"]["all"]["per_view"] + """ as they shipped. Re-rendered on candidate 2's own engine and canon, the same six pages read """ + "%.2f" % S["c_six_on_cand2_canon"]["all"]["per_view"] + """: v1.0.13's three read """ + "%.2f" % S["c_six_on_cand2_canon"]["v1013"]["per_view"] + """ and candidate 1's three read """ + "%.2f" % S["c_six_on_cand2_canon"]["cand1"]["per_view"] + """. The engine took about 1.1 per view off, on average. What the new runs themselves add is about another 0.4.</p>
      <p>Two findings inflate every count, and no page can change either of them. One is the Kpi-tile label crop, which is held for you. The other is a harness false positive on data-grid rows that are hidden inside the grid's own scroll box. Setting both aside, the three groups read """ + "%.1f" % ADJ["_v1013"]["adj"] + """ for v1.0.13, """ + "%.1f" % ADJ["_cand1"]["adj"] + """ for candidate 1 and """ + "%.1f" % ADJ["_cand2"]["adj"] + """ for candidate 2. Candidate 2's three runs sit close together, between 3.6 and 3.9. The gap is real, but it is small, and each group is only three runs.</p>
      <p>By eye, candidate 2's third run has the best overview of the nine. It pairs charts in half-width tiles, and each chart's title states its finding. The axis labels no longer cut on the left, the rings no longer stretch into empty tiles, and the dates are thinned. What your eye still lands on first is shared with v1.0.13. Every line of 30 points carries 30 markers. In dark mode the chart tiles lose their edges. The shell is a 640px box. Legend buttons are shrunk. KPI labels lose their descenders. Some chart labels are now cut at the right-hand end instead of the left.</p>
      <div class="dd-host"></div>
    </div>
  </div>
</section>

<section id="decide">
  <div class="wrap two">
    <p class="label">Your decision</p>
    <div>
      <ol class="decide"><li><b>Cut v1.0.14 from candidate 2 on Tuesday?</b>
        <p>My recommendation: yes, cut it, with two small fixes to the gate code first.</p>
        <p>The first fix: the receipt gate must stop counting the data grid's fenced demo script. The second: the icon-source check must stop reading inside script bodies. Neither changes a single rendered page, so no new cold run is needed. Without them, every page a designer composes from the pack fails its own gates on day one.</p>
        <p>The reason to cut: on every like-for-like reading candidate 2 beats v1.0.13, and nothing went backwards. The engine fix alone takes about a sixth of the ink off the average page, whoever built it. What remains is either in v1.0.13 too, or waiting on your word.</p>
        <p>This departs from the R4s condition. R4s asked for four fixes before a cut. Only one has landed: Common's 24px gutter. The other three are the KPI crop, the full-height shell and the chart receipt address. Each waits on you, and each is in v1.0.13 already, so holding the cut for them keeps the worse release in the field.</p>
        <p>Carry to v1.0.15: your five calls (the KPI crop, the dark ground, markers on dense series, the chart receipt address, and the shell), plus the scope-bleed fix in canon, which needs no ruling.</p>
        <div></div></li></ol>
    </div>
  </div>
</section>

<section id="eye-light">
  <div class="wide">
    <p class="label">By eye, the whole overview · 1440 · light</p>
    <h2>One of each, side by side</h2>
    <p style="max-width:62em">Left to right: the best-looking v1.0.13 run, the best candidate 1 run and the best candidate 2 run. All three are rendered on candidate 2's engine and canon, so any difference comes from how each page was built. The shell frame is released so you see the whole page (declared). As shipped, the v1.0.13 and candidate 1 pages had the old engine; you can see those in the R4s review.</p>
    <div class="shots">
""" + fig("v1013-r3-c2canon-full-light.png", "<b>v1013-r3</b> · v1.0.13 run, on candidate 2's engine and canon · ink " + pv("c_six_on_cand2_canon", "v1013-r3") + " per view", "v1013-r3 overview, light") + """
""" + fig("cand-r3-c2canon-full-light.png", "<b>cand-r3</b> · candidate 1 run, on candidate 2's engine and canon · ink " + pv("c_six_on_cand2_canon", "cand-r3") + " per view", "cand-r3 overview, light") + """
""" + fig("cand2-r3-full-light.png", "<b>cand2-r3</b> · candidate 2 run, as built · ink " + pv("cand2", "cand2-r3") + " per view (" + "%.1f" % ADJ["cand2-r3"]["adj_per_view"] + " without the KPI crop)", "cand2-r3 overview, light") + """
    </div>
    <p class="meta" style="margin-top:var(--s2)">cand2-r3 reads highest of the three on raw ink only because it puts a KPI row on every view. Every one of its 23 cut tiles is the Kpi-tile label crop.</p>
    <div class="dd-host"></div>
  </div>
</section>

<section id="eye-dark">
  <div class="wide">
    <p class="label">By eye, the same three · 1440 · dark, by each page's own Dark button</p>
    <h2>Dark: the ground and the tiles become one</h2>
    <p style="max-width:62em">On candidate 2's pages the grey section and the chart tiles resolve to the same #1F1F1F, so the tiles lose their edges. The KPI tiles keep a border and survive. v1013-r3 and cand-r3 stepped around this: each set its own ground to the page colour, #1A1A1A, so their tiles still show, if only faintly.</p>
    <div class="shots">
""" + fig("v1013-r3-c2canon-full-dark.png", "<b>v1013-r3</b> · ground #1A1A1A (set by the page), tiles #1F1F1F", "v1013-r3 overview, dark") + """
""" + fig("cand-r3-c2canon-full-dark.png", "<b>cand-r3</b> · ground #1A1A1A (set by the page), tiles #1F1F1F", "cand-r3 overview, dark") + """
""" + fig("cand2-r3-full-dark.png", "<b>cand2-r3</b> · ground #1F1F1F (canon's grey), tiles #1F1F1F. The toast is the page's own confirmation.", "cand2-r3 overview, dark") + """
    </div>
    <div class="dd-host"></div>
  </div>
</section>

<section id="eye-others">
  <div class="wide">
    <p class="label">By eye, the other two candidate 2 runs · 1440</p>
    <h2>Three runs, three different pages</h2>
    <p style="max-width:62em">cand2-r1 is one long column of full-width chart tiles. Its donut sits small in a wide tile with the legend at the far right, which is the hug-or-fill question W4a put to you, and its risk list prints "raised NaN Sep". cand2-r2 is a tidy two-by-two chart wall. Its stacked area still carries a letter and a marker on every point, "Middle East and Africa" and "1500 £m" are cut at the right-hand edge, and one KPI reads "−2781.4% down".</p>
    <div class="shots two-col">
""" + fig("cand2-r1-full-light.png", "<b>cand2-r1</b> · light · ink " + pv("cand2", "cand2-r1") + " per view", "cand2-r1 overview, light") + """
""" + fig("cand2-r2-full-light.png", "<b>cand2-r2</b> · light · ink " + pv("cand2", "cand2-r2") + " per view", "cand2-r2 overview, light") + """
""" + fig("cand2-r1-full-dark.png", "<b>cand2-r1</b> · dark", "cand2-r1 overview, dark") + """
""" + fig("cand2-r2-full-dark.png", "<b>cand2-r2</b> · dark", "cand2-r2 overview, dark") + """
    </div>
    <div class="dd-host"></div>
  </div>
</section>

<section id="scores">
  <div class="wrap">
    <p class="label">The scorecard · ink per view, lower is better</p>
    <h2>The engine did most of it; candidate 2 adds a little</h2>
    <p>Ink is the W4b harness's comparable number: affected tiles (or, for size, kinds) summed over five classes, divided by the views measured. Every run is measured on its ten views at 1440. All nine runs pass the floor, which is each rubric part at 2 or more.</p>
    <div style="overflow-x:auto"><table class="score">
      <thead><tr><th>Run</th><th>Old engine, as shipped (W4b)</th><th>W4a engine (W4a)</th><th>Candidate 2 engine and canon</th><th>Without KPI crop and grid false positive</th><th>Dead</th><th>Cut</th><th>Collisions</th><th>Size</th><th>Markers</th></tr></thead>
      <tbody>""" + table + """</tbody>
    </table></div>
    <p class="meta" style="margin-top:var(--s2)">The class columns are counts over ten views for each run, and per view on the mean rows. The earlier six were re-rendered on candidate 2's engine and canon, and the result matches W4a's re-render on every class of every run. So wave three and four's canon changes moved nothing on those pages.</p>
    <h3 style="margin-top:var(--s4)">Which comparison is like for like</h3>
    <p>The third column is the like-for-like one for what a page renders with. All nine runs are drawn by the same engine, canon and type bytes: the candidate 2 pack's, which match repo HEAD 3100da99.</p>
    <p>No comparison is like for like on how the pages were built. The candidate 2 agents built with the new engine and canon in front of them. They could see a ring hug its frame and a y-axis fit its labels, and they had the candidate 2 skill. The earlier six were built on v1.0.13 or candidate 1 and are only re-drawn here. So the gap between the third column and candidate 2 is authoring, meaning skill, agent and run-to-run chance, with three runs a side.</p>
    <p>The first column, the W4b baseline, is not like for like at all. Old engine, old canon. The second, W4a, is like for like on the engine but used HEAD 86249459's canon, which is before waves three and four. It reads identically to the third.</p>
    <h3 style="margin-top:var(--s4)">The two judgment rows, left for you</h3>
    <div style="overflow-x:auto"><table class="score"><thead><tr><th>Run</th><th>Question</th><th>Evidence</th><th>Answer</th></tr></thead><tbody>""" + jrows + """</tbody></table></div>
    <div class="dd-host"></div>
  </div>
</section>

<section id="defects">
  <div class="wrap">
    <p class="label">Defects the candidate 2 runs reported, verified here</p>
    <h2>Six reported, all six real; two more found</h2>
    <ul class="gaps" style="list-style:none">
      <li><div><b>1 · Dark mode: the grey section and the tiles are both #1F1F1F. Confirmed. <span class="pill k">Your call, then canon</span></b>
        <p>Measured with each page's own Dark button: the ground is rgb(31,31,31) and so are the tiles, on all three runs. The cause is in the token block. <code>[data-theme="dark"]</code> sets <code>--surface-subtle</code> and <code>--surface-raised</code> both to #1F1F1F (<code>canon.css</code>:845–846, generated from the tokens). The rails file claims its dark equivalents were "derived, not chosen", and its resolved map gives dark grey = dark white for every theme. Common is missing from that map entirely.</p>
        <p class="fix">Fix: you choose what the dark ground is. Either it takes the page colour #1A1A1A under #1F1F1F tiles, which is what v1013-r3 and cand-r3 did by hand, or tiles carry an edge in dark. Then the token or the rails change to match.</p>
        <div class="shots two-col" style="margin-top:var(--s2)">""" + fig("crop-light-tiles-cand2-r3.png", "cand2-r3 · light", "tiles in light") + fig("crop-dark-tiles-cand2-r3.png", "cand2-r3 · dark: the chart tiles have no edge", "tiles in dark") + """</div></div></li>
      <li><div><b>2 · The side-nav shell is fixed at 640px. Confirmed. <span class="pill k">Component</span></b>
        <p>The rule is <code>:where(.cn-app-shell-side-nav) .sh{…height:640px}</code> at <code>canon.css</code>:5678; doormat (4697) and multi-column (5148) carry the same. cand2-r1 and cand2-r2 ship in a 640px box, with the empty band below it at 1440 × 900. cand2-r3 avoided the frame by not using <code>.sh</code>, so its nav pane stops at about 730px.</p>
        <p class="fix">Fix: a full-viewport form of the shell, and the skill's never-resize wording to point at it.</p>
        <div class="shots one" style="margin-top:var(--s2);max-width:720px">""" + fig("cand2-r1-asshipped-light.png", "cand2-r1 · as shipped at 1440 × 900", "as shipped") + """</div></div></li>
      <li><div><b>3 · The receipt gate counts the data grid's fenced demo script. Confirmed. <span class="pill k">Pack tooling, no ruling</span></b>
        <p><code>_validate_receipt.py</code> <code>inline_scripts()</code> skips AUTO-BEHAVIOUR spans but not APOLLO-DEMO spans. The fence regex exists at line 199 but is not used there. So <code>Data-grid.reference.html#script</code> resolves to two scripts: the real 23,876 B one and the 1,447 B state-switcher inside the APOLLO-DEMO fence (lines 1140–1166), which the skill forbids copying. Reproduced: FAIL:BEHAVIOUR-NOT-LOADED on the grid pages of all three runs, including r1, which carries the real script byte for byte.</p>
        <p class="fix">Fix: mask APOLLO-DEMO spans in <code>inline_scripts()</code>. This is one of the two pre-cut fixes.</p></div></li>
      <li><div><b>3b · The wrong chart script on the receipt. Confirmed, still open from R4s. <span class="pill k">Your one line, then tooling</span></b>
        <p>The mint's <code>behaviour_address()</code> resolves the chart snippets' AUTO-BEHAVIOUR marker to <code>dv-behaviour.js</code>, while every chart meta says <code>dv-render.js</code>. Reproduced as FAIL:BEHAVIOUR-ADDRESS-DISAGREES on every chart region of cand2-r3. cand2-r2 hid it by re-minting with its own script. It is present in v1.0.13 too.</p></div></li>
      <li><div><b>4 · <code>text-box-trim</code> shrinks the chart legend buttons: 82, 104 and 146 own-size findings. Confirmed, cause found. <span class="pill k">Canon generator, no ruling</span></b>
        <p>The shrink does not come from the button's own rule. The per-scope leading-trim rule of the shell (<code>:where(.cn-app-shell-side-nav) :where(button, span, li, …)</code>, <code>canon.css</code>:5668) and of the bento template (17643) reaches into the nested chart legend. It trims the two spans inside each button, and the button collapses to 16.7px. Taking the trim off those two spans restores 20px, the reference height (<code>probe_size.py</code>). Every own-size finding on all three runs is a chart part.</p>
        <p class="fix">Fix: <code>gen_canon_components.py</code> scopes each snippet's CSS under <code>:where(.cn-x)</code> with no lower boundary, so it should stop at a nested <code>cn-</code> scope. This is the size-drift class, 2.6 of candidate 2's 5.1 per view, and it is the same in every group.</p></div></li>
      <li><div><b>5 · KPI tiles are 4px taller inside the bento. Confirmed; same cause as 4. <span class="pill k">Canon generator, no ruling</span></b>
        <p><code>:where(.cn-template-dashboard-bento) .spark-inline{height:44px}</code> (17942) outranks <code>:where(.cn-kpi-tile) .spark-inline{height:40px}</code> (13102) on source order. Measured: spark 44 against 40, tile 159.1 against the reference's 155.1.</p></div></li>
      <li><div><b>6 · The icon-source false positive from the chart engine. Confirmed. <span class="pill k">Pack tooling, no ruling</span></b>
        <p><code>_validate_screen.py</code> <code>gate_icons()</code> scans the raw HTML, script bodies included. An inlined <code>dv-render.js</code> contains the text "&lt;svg" (the comment at line 245 and the string at 258), and the regex runs on to a later &lt;/svg&gt;. It then reads <code>d="M' + p.join(' L') + ' Z…"</code> as an unknown icon path. Reproduced on cand2-r2. cand2-r1 loads the engine by <code>src</code> and passes.</p>
        <p class="fix">Fix: mask &lt;script&gt; bodies before the icon scan. This is the other pre-cut fix.</p></div></li>
      <li><div><b>New · Chart labels cut at the right-hand end. <span class="pill k">Engine, no ruling</span></b>
        <p>The last value tick ("600 £m", "1500 £m") and the last category ("Middle East and Africa") run 5–19px past the end of the chart's <code>.dv-stage</code> (<code>overflow-x:auto</code>). It happens 2–4 times per run in every group (<code>probe_edge.py</code>). W4a fitted the left gutter; the right end is the same class. The geometry gate misses it because G8 counts a scroll box's end edge as reachable.</p>
        <div class="shots one" style="margin-top:var(--s2);max-width:420px">""" + fig("crop-right-edge-cand2-r2.png", "cand2-r2 overview", "right-edge cut") + """</div></div></li>
      <li><div><b>New · The harness counts rows hidden in a data grid as collisions. <span class="pill k">Harness and gate, no ruling</span></b>
        <p>Grid rows scrolled out of the grid's own 378px box are measured as sitting on the pager and the keyboard hint. On screen they are hidden (<code>probe_grid.py</code>, <code>probe/grid-cand2-r1-payments.png</code>). This is nested scroll frames: W4b's repair compares within the outer frame, not the innermost. It accounts for 10 of candidate 2's 12 collision tiles and a few in the earlier groups. The adjusted column removes it.</p></div></li>
      <li><div><b>Still in, and yours: the Kpi-tile label crop and markers on dense series.</b>
        <p>All 31 of candidate 2's cut tiles are the KPI label crop (s261-D4, held). Every 30-point line carries 30 markers, and cand2-r2's stacked area carries a letter at every point. W4a rendered that option for you.</p>
        <p>Run-level slips, not canon: "raised NaN Sep" (r1), "−2781.4% down" (r2), and donut totals with no unit ("3427.9").</p></div></li>
    </ul>
    <div class="dd-host"></div>
  </div>
</section>

<section id="method">
  <div class="wrap two">
    <p class="label">Method, in brief</p>
    <div>
      <p>Each candidate 2 run was scored with the W4b harness (<code>score.py all</code>, <code>w4b-2.0</code>) against the candidate 2 zip, sha256 8a75ce32…aff47e3. That covers stage, static, gates, render, drive, views on every view with the theme switched both ways, and ext (geometry at 1440/390 and own-size on the overview). Writes were redirected to <code>notes/_lanes/304/R4s2/runs</code>.</p>
      <p>The geometry and own-size gates also ran directly on all ten pages of each run. The six earlier runs were re-staged on the candidate 2 pack's engine, canon and type with W4a's own restage method, and their views re-measured.</p>
      <p>The adjusted column removes a view's collisions when every sampled collision names the grid's pager, hint or range. It removes a view's cut ink when every sampled cut is <code>kpi-lbl</code>. It reads from samples, and is declared as such.</p>
      <div class="dd-host"></div>
    </div>
  </div>
</section>

<section id="tech">
  <div class="wrap tech">
    <p><b>Receipts.</b> Harness runs: <code>notes/_lanes/304/R4s2/runs/cold-cand2-r{1,2,3}/</code> (scorecard, views, ext). Earlier six on candidate 2 canon: <code>runs-c2canon/</code> (via <code>restage_c2.py</code>, <code>mkruns_c2.py</code>, <code>views_c2.sh</code>). Direct gate runs: <code>gates/</code>. Every number on this page: <code>ink-sets.json</code>. Probes: <code>probe_grid.py</code>, <code>probe_size.py</code>, <code>probe_edge.py</code> (outputs <code>edge-runs*.json</code>). Shots: <code>shots.py</code> → <code>shots/</code> (<code>shots.json</code> holds the dark colours). Stages are seat-local at <code>$HOME/r4c/stage/cold-cand2-*</code> and <code>$HOME/r4s2/st/c2canon/</code>; the frozen outputs were not modified. Report: <code>notes/_subreports/2026-09-27-304-R4s2-candidate-2-scores.md</code>.</p>
  </div>
</section>

<footer>
  <div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
    <span>Apollo · review · candidate 2 scored · v1 · 2026-09-27 · session 304</span>
    <span>Nothing here is decided.</span>
  </div>
</footer>
""" + overlay
open(OUT, "w").write(page)
print("wrote", OUT, len(page))
