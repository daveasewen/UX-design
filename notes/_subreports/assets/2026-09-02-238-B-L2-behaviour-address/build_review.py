#!/usr/bin/env python3
"""
build_review.py — #238 lane B. Renders `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` (repo
root) FROM behaviour-migration.json + the drive evidence — the 20 side-by-sides are derived, never
retyped, so the page cannot disagree with the proposal file. Swiss idiom, light + dark, 1440 + 390.

  python3 build_review.py <repo>
"""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1]
OUT = os.path.join(REPO, "_REVIEW-L2-behaviour-address-2026-09-02-v1.html")
mig = json.load(open(os.path.join(HERE, "behaviour-migration.json"), encoding="utf-8"))
drives = json.load(open(os.path.join(HERE, "drive-arms-summary.json"), encoding="utf-8"))
C = mig["counts"]
E = html.escape

passive = [i for i in mig["items"] if i["proposed"]["script"] is None]
scripted = [i for i in mig["items"] if i["proposed"]["script"]]
with_unproven = [i for i in mig["items"] if i["unproven"]]
gate_arms = sum(1 for ln in open(os.path.join(HERE, "selftest-validate-receipt.txt"), encoding="utf-8") if ln.strip().startswith("✅"))
gen_mutants = open(os.path.join(HERE, "selftest-gen-component-partials-mutants.txt"), encoding="utf-8").read().count("SELFTEST FAIL")
gate_mutants = open(os.path.join(HERE, "selftest-validate-receipt-mutants.txt"), encoding="utf-8").read().count("SELFTEST: FAIL")
schema_arms = sum(1 for ln in open(os.path.join(HERE, "schema-arms.txt"), encoding="utf-8") if ln.strip().startswith("✅") and ("RED" in ln or "GREEN" in ln))
drives_ok = sum(1 for d in drives if d["as_expected"])


def prose_html(old):
    if isinstance(old, str):
        return "<p class=\"prose\">%s</p>" % E(old)
    rows = []
    for k, v in old.items():
        rows.append("<dt>%s</dt><dd>%s</dd>" % (E(k), E(v)))
    return "<dl class=\"prose\">%s</dl>" % "".join(rows)


def basis_chip(b):
    cls = {"prose": "p", "measured": "m", "UNPROVEN": "u"}[b]
    return '<span class="chip %s">%s</span>' % (cls, E(b))


def item_block(i):
    p = i["proposed"]
    prov = i["provenance"]
    show = {k: p[k] for k in ("script", "partial", "events", "fallback")}
    if p.get("$unproven"):
        show["$unproven"] = p["$unproven"]
    show["$note"] = "… the prose on the left, verbatim …"
    js = json.dumps(show, indent=2, ensure_ascii=False)
    fields = []
    for f in ("script", "partial", "events", "fallback"):
        pv = prov[f]
        bits = [basis_chip(pv["basis"])]
        if pv.get("quote"):
            bits.append('<span class="qt">“%s”</span>' % E(pv["quote"]))
        if pv["basis"] == "measured" and pv.get("probe"):
            bits.append('<span class="pr">%s</span>' % E(pv["probe"]))
        if f == "events":
            qs = pv.get("quotes") or {}
            if qs:
                bits.append('<span class="pr">prose corroborates: %s</span>' % E("; ".join("%s ← “%s”" % (k, v) for k, v in qs.items())))
            bits.append('<span class="pr">rC Q3 open — field floated</span>')
        if pv["basis"] == "UNPROVEN":
            if pv.get("candidate"):
                bits.append('<span class="cand"><b>Candidate reading, for your eye only:</b> %s</span>' % E(pv["candidate"]))
            if pv.get("measured_hint"):
                bits.append('<span class="pr">measured hint: %s</span>' % E(pv["measured_hint"]))
            if pv.get("what_would_prove"):
                bits.append('<span class="pr">what would prove it: %s</span>' % E(pv["what_would_prove"]))
        fields.append('<div class="fld"><span class="fk">%s</span><span class="fv">%s</span></div>' % (E(f), "".join(bits)))
    kind = "passive" if p["script"] is None else "scripted"
    tags = [kind]
    if i["unproven"]:
        tags.append("unproven")
    flag = ('<p class="flagline">%s</p>' % E(i["flag"])) if i.get("flag") else ""
    meas = i["measured"] or {}
    meas_line = "snippet: %s · inline executable scripts %d%s · AUTO-BEHAVIOUR %s · listeners %s%s" % (
        E(os.path.basename(i["snippet"] or "—")), meas.get("inline_executable_scripts", 0),
        (" (%s bytes)" % ", ".join("{:,}".format(b) for b in meas.get("inline_bytes", []))) if meas.get("inline_bytes") else "",
        meas.get("auto_behaviour") or "none",
        ", ".join(meas.get("component_events") or []) or "none",
        (" · page-level modality tracker present (%s), excluded" % ", ".join(meas["modality_tracker_events"])) if meas.get("modality_tracker_events") else "")
    return '''
<article class="item" data-tags="%(tags)s" id="m-%(slug)s">
  <div class="ihead">
    <h3>%(name)s <span class="mono muted">%(slug)s</span></h3>
    <span class="kind %(kind)s">%(kindlabel)s</span>
  </div>
  <p class="small muted">%(meta)s · old value is a JSON %(otype)s</p>
  <div class="pair">
    <div class="col n">
      <div class="colhead a">Old — the prose, kept verbatim under <code>$note</code></div>
      %(old)s
    </div>
    <div class="col">
      <div class="colhead b">Proposed — typed address (not written)</div>
      <pre>%(js)s</pre>
      %(fields)s
    </div>
  </div>
  <p class="small muted measline">%(meas)s</p>
  %(flag)s
</article>''' % dict(tags=" ".join(tags), slug=E(i["slug"]), name=E(i["name"] or i["slug"]), kind=kind,
                     kindlabel="no script" if kind == "passive" else "carries a script",
                     meta=E(i["meta"]), otype=E(i["old_json_type"]), old=prose_html(i["old"]), js=E(js),
                     fields="".join(fields), meas=meas_line, flag=flag)


items_html = "".join(item_block(i) for i in mig["items"])
drive_rows = "".join('<tr><td class="id">%s</td><td>%s</td><td class="id">rc=%d</td><td>%s</td></tr>'
                     % (E(d["arm"]), E(d["title"]), d["rc"], "as expected" if d["as_expected"] else "NOT as expected")
                     for d in drives)

page = r'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>#238-B — The behaviour address</title>
<style>
:root{
  --accent:#DA1A00;            /* s151-D1 two-red law: red ink ON WHITE */
  --ink:#000000; --bg:#FFFFFF;
  --g1:#F3F3F3; --g2:#EDEDED; --g3:#D7D8D6; --g5:#9B9B9B; --g6:#767676; --g7:#545454; --g8:#333333;
  --rule:var(--g2); --panel:#F3F3F3;
  --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
  --max:1200px; --gut:2rem;
  --mono:ui-monospace,Menlo,"SF Mono",Consolas,monospace;
}
html[data-theme="dark"]{
  --accent:#F6604C;            /* s151-D1: everything-else red */
  --ink:#FFFFFF; --bg:#0E0E0E;
  --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g5:#7A7A7A; --g6:#9A9A9A; --g7:#B8B8B8; --g8:#D8D8D8;
  --rule:#2A2A2A; --panel:#161616;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0; background:var(--bg); color:var(--ink); font-family:"Helvetica Neue",Helvetica,Arial,sans-serif; font-size:16px; line-height:1.75; font-weight:400; overflow-x:hidden}
.wrap{max-width:var(--max); margin:0 auto; padding:0 var(--gut)}
nav{position:sticky; top:0; z-index:50; background:var(--bg); border-bottom:1px solid var(--rule)}
nav .wrap{display:flex; align-items:center; gap:var(--s3); min-height:54px}
.brand{font-size:12px; font-weight:500; letter-spacing:.14em; text-transform:uppercase; white-space:nowrap}
.navlinks{display:flex; gap:var(--s3); margin-left:auto; flex-wrap:wrap}
.navlinks a{font-size:14px; color:var(--g6); text-decoration:none; letter-spacing:.04em}
.navlinks a:hover{color:var(--ink)}
button.tt{font:inherit; font-size:12px; font-weight:500; letter-spacing:.06em; text-transform:uppercase; background:none; color:var(--ink); border:0; border-bottom:1px solid var(--accent); padding:4px 0; cursor:pointer; white-space:nowrap; margin-left:auto}
.navlinks + button.tt{margin-left:0}
h1{font-size:clamp(2.4rem,6vw,5.25rem); font-weight:300; line-height:1.02; letter-spacing:0; margin:0}
h2{font-size:clamp(1.6rem,3.4vw,2.6875rem); font-weight:400; line-height:1.14; margin:0 0 var(--s3)}
h3{font-size:1.1875rem; font-weight:500; line-height:1.2; margin:0 0 var(--s2)}
h4{font-size:14px; font-weight:500; letter-spacing:.1em; text-transform:uppercase; margin:0 0 var(--s2)}
p{margin:0 0 var(--s2); max-width:68ch}
.lede{font-size:1.1875rem; line-height:1.6}
.label{font-size:12px; font-weight:500; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); display:flex; align-items:center; gap:var(--s1); margin:0 0 var(--s3)}
.label::before{content:''; display:inline-block; width:20px; height:1px; background:var(--accent); flex:none}
.muted{color:var(--g7)}
.small{font-size:14px; line-height:1.6}
.mono{font-family:var(--mono); font-size:13px}
code{font-family:var(--mono); font-size:.88em; background:var(--g1); padding:1px 4px; overflow-wrap:anywhere}
b,strong{font-weight:700}
a{color:var(--ink)}
section{padding:var(--s7) 0; border-bottom:1px solid var(--rule)}
section.tight{padding:var(--s5) 0}
section.band{background:var(--panel)}
.hdr{display:grid; grid-template-columns:2fr 1fr; gap:var(--s6); align-items:end}
.meta dt{font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:var(--g6); margin-top:var(--s2)}
.meta dd{margin:0; font-size:14px; overflow-wrap:anywhere}
.flag{display:inline-block; font-size:12px; font-weight:500; letter-spacing:.12em; text-transform:uppercase; border:1px solid var(--accent); color:var(--accent); padding:3px 9px; margin-bottom:var(--s3)}
.stats{display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--rule); border:1px solid var(--rule); margin-top:var(--s4)}
.stat{background:var(--bg); padding:var(--s3)}
.stat .n{font-size:clamp(2rem,4.4vw,2.6875rem); font-weight:200; line-height:1; display:block}
.stat .k{font-size:12px; letter-spacing:.1em; text-transform:uppercase; color:var(--g6); display:block; margin-top:var(--s1)}
.stat.hi .n{color:var(--accent)}
.dim{display:grid; grid-template-columns:1fr 2fr; gap:var(--s6); align-items:start}
.idx{font-size:clamp(3rem,7vw,5.25rem); font-weight:200; line-height:.9; color:var(--g5); display:block}
.dim>*, .pair>*, .cards>*, .stats>*, .hdr>*, .col>*, .card>*, .item>*{min-width:0}
.scroll{overflow-x:auto; -webkit-overflow-scrolling:touch; max-width:100%; min-width:0}
table{border-collapse:collapse; width:100%; min-width:640px; font-size:14px; line-height:1.5}
th,td{text-align:left; vertical-align:top; padding:10px 14px 10px 0; border-bottom:1px solid var(--rule)}
th{font-size:12px; letter-spacing:.1em; text-transform:uppercase; font-weight:500; color:var(--g6); white-space:nowrap}
td.id,th.id{font-family:var(--mono); white-space:nowrap; padding-right:var(--s3)}
.pair{display:grid; grid-template-columns:1fr 1fr; gap:1px; background:var(--rule); border:1px solid var(--rule); margin-top:var(--s3)}
.col{background:var(--bg); padding:var(--s3)}
.col.n{background:var(--panel)}
.colhead{font-size:12px; font-weight:500; letter-spacing:.12em; text-transform:uppercase; margin-bottom:var(--s2); padding-bottom:var(--s1); border-bottom:1px solid var(--rule)}
.colhead.a{color:var(--g7)}
.colhead.b{color:var(--accent)}
pre{font-family:var(--mono); font-size:12px; line-height:1.5; margin:0 0 var(--s2); background:var(--g1); padding:var(--s2); overflow-x:auto; border-left:2px solid var(--g3); white-space:pre; min-width:0; max-width:100%}
html[data-theme="dark"] pre{background:#111}
.prose{font-size:14px; line-height:1.6; margin:0; overflow-wrap:anywhere}
dl.prose dt{font-family:var(--mono); font-size:12px; color:var(--g6); margin-top:var(--s2)}
dl.prose dt:first-child{margin-top:0}
dl.prose dd{margin:2px 0 0}
.fld{display:grid; grid-template-columns:88px 1fr; gap:var(--s2); font-size:13px; line-height:1.55; padding:var(--s1) 0; border-top:1px solid var(--rule)}
.fld .fk{font-family:var(--mono); color:var(--g6)}
.fld .fv{display:flex; flex-direction:column; gap:4px; min-width:0}
.chip{display:inline-block; font-size:11px; font-weight:500; letter-spacing:.1em; text-transform:uppercase; padding:1px 7px; border:1px solid var(--g3); color:var(--g7); align-self:flex-start}
.chip.m{border-color:var(--g8); color:var(--ink)}
.chip.u{border-color:var(--accent); color:var(--accent)}
.qt{font-style:normal}
.pr{color:var(--g7); overflow-wrap:anywhere}
.cand{background:var(--panel); padding:var(--s1) var(--s2); border-left:2px solid var(--accent)}
.item{padding:var(--s5) 0; border-top:1px solid var(--rule); scroll-margin-top:64px}
section{scroll-margin-top:56px}
.item:first-of-type{border-top:0}
.ihead{display:flex; align-items:baseline; gap:var(--s3); flex-wrap:wrap}
.ihead h3{margin:0}
.kind{font-size:11px; letter-spacing:.12em; text-transform:uppercase; padding:2px 8px; border:1px solid var(--g3); color:var(--g7)}
.kind.scripted{border-color:var(--g8); color:var(--ink)}
.flagline{font-size:14px; border-left:2px solid var(--accent); padding-left:var(--s2); margin-top:var(--s2)}
.measline{margin-top:var(--s2); overflow-wrap:anywhere}
.ctl{display:flex; flex-wrap:wrap; gap:var(--s1); margin:var(--s3) 0}
.ctl button{font:inherit; font-size:12px; font-weight:500; letter-spacing:.08em; text-transform:uppercase; background:none; color:var(--g7); border:1px solid var(--g3); padding:6px 12px; cursor:pointer}
.ctl button[aria-pressed="true"]{color:var(--ink); border-color:var(--ink)}
.item[hidden]{display:none}
.cards{display:grid; grid-template-columns:repeat(2,1fr); gap:1px; background:var(--rule); border:1px solid var(--rule)}
.card{background:var(--bg); padding:var(--s3)}
.card .n{font-size:12px; font-weight:500; letter-spacing:.12em; color:var(--accent); display:block; margin-bottom:var(--s1)}
.card h3{font-size:16px; margin-bottom:var(--s1)}
.card p{font-size:14px; line-height:1.55; margin:0 0 var(--s1)}
.own{font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--g6)}
.qq{border-top:1px solid var(--rule); padding-top:var(--s3); margin-top:var(--s4)}
.qq:first-of-type{border-top:0; margin-top:0}
.qq .num{font-size:12px; letter-spacing:.12em; color:var(--accent); font-weight:500}
.rec{border-left:2px solid var(--accent); padding-left:var(--s2); margin-top:var(--s2); font-size:15px}
.note{background:var(--panel); padding:var(--s3); border-left:2px solid var(--g3); font-size:14px; line-height:1.6}
.note p:last-child{margin-bottom:0}
ol,ul{padding-left:1.15rem; max-width:68ch}
li{margin-bottom:var(--s1); font-size:15px; line-height:1.6}
footer{padding:var(--s5) 0 var(--s7); font-size:13px; color:var(--g6)}
footer p{max-width:none; overflow-wrap:anywhere}
@media (max-width:900px){
  .hdr,.dim{grid-template-columns:1fr; gap:var(--s4)}
  .pair,.cards{grid-template-columns:1fr}
  .stats{grid-template-columns:repeat(2,1fr)}
  .fld{grid-template-columns:1fr; gap:2px}
  :root{--s7:3.5rem; --s6:2.5rem; --gut:1.25rem}
  .navlinks{display:none}
}
@media (prefers-color-scheme:dark){
  html:not([data-theme="light"]){
    --accent:#F6604C; --ink:#FFFFFF; --bg:#0E0E0E;
    --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g5:#7A7A7A; --g6:#9A9A9A; --g7:#B8B8B8; --g8:#D8D8D8;
    --rule:#2A2A2A; --panel:#161616;
  }
}
</style>
</head>
<body>

<nav>
  <div class="wrap">
    <span class="brand">#238 · Lane B</span>
    <span class="navlinks">
      <a href="#answer">Answer</a>
      <a href="#shape">The shape</a>
      <a href="#twenty">The 20</a>
      <a href="#proof">Proof</a>
      <a href="#l1">L1's three</a>
      <a href="#mine">This lane's</a>
      <a href="#risk">Consequences</a>
    </span>
    <button class="tt" id="tt" type="button">Dark</button>
  </div>
</nav>

<section id="top">
  <div class="wrap">
    <span class="flag">Proposed — no meta was written</span>
    <div class="hdr">
      <div>
        <p class="label">The behaviour address · s234-D5</p>
        <h1>Prose becomes<br>an address</h1>
      </div>
      <dl class="meta">
        <dt>Session</dt><dd>#238 · 2026-09-02 · lane B (L2 of the v1.0.6 brief)</dd>
        <dt>Data</dt><dd>the 20 <code>behaviour</code> values in <code>knowledge/components/*.meta.json</code>, unedited, beside probes on their 20 snippets</dd>
        <dt>Binding rulings</dt><dd class="mono">s234-D5 · s235-D1 · s235-D2</dd>
        <dt>Register</dt><dd>Every value below is <b>proposed</b>. The metas are untouched until you say so (v1.0.6 brief, line 47).</dd>
      </dl>
    </div>
  </div>
</section>

<section id="answer">
  <div class="wrap">
    <p class="label">The answer, before the argument</p>
    <div class="dim">
      <div><span class="idx">01</span></div>
      <div>
        <h2>Twenty metas describe behaviour in words. None says where the script is. A typed address does — and the machinery to read it is built and bites.</h2>
        <p class="lede">Six of the twenty say <b>passive — no states</b>, and their snippets agree (no script). Fourteen carry a real inline <code>&lt;script&gt;</code> that the prose describes but never names. The proposal types all twenty: <code>script</code> · <code>partial</code> · <code>events</code> · <code>fallback</code>, with the old prose kept verbatim under <code>$note</code>. Nothing is deleted.</p>
        <p>Fourteen have one honest gap: <b>what the component does with JavaScript off</b>. No prose settles it, so those <code>fallback</code> values are <code>null</code>, marked <code>$unproven</code>, with a candidate reading shown for your eye and kept out of the proposal.</p>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><span class="n">@@n_metas@@</span><span class="k">metas with behaviour</span></div>
      <div class="stat"><span class="n">@@n_passive@@</span><span class="k">passive · script null</span></div>
      <div class="stat"><span class="n">@@n_scripted@@</span><span class="k">carry a script</span></div>
      <div class="stat hi"><span class="n">@@n_unproven_metas@@</span><span class="k">with an unproven field</span></div>
      <div class="stat"><span class="n">@@f_prose@@</span><span class="k">fields settled by prose</span></div>
      <div class="stat"><span class="n">@@f_meas@@</span><span class="k">fields settled by a probe</span></div>
      <div class="stat hi"><span class="n">@@f_unp@@</span><span class="k">fields unproven (all fallback)</span></div>
      <div class="stat"><span class="n">@@gate_arms@@</span><span class="k">gate arms green · @@gate_mut@@ mutants caught</span></div>
    </div>
    <p class="small muted" style="margin-top:var(--s3)">Bases: <b>prose</b> = the meta's own words, quoted · <b>measured</b> = a probe on the reviewed snippet (script count, bytes, listeners) · <b>UNPROVEN</b> = neither. The address itself is never in the prose (the s234-D5 census: “addressing the script in none”), so <code>script</code> is settled by measurement wherever a script exists.</p>
  </div>
</section>

<section id="shape" class="band">
  <div class="wrap">
    <p class="label">The shape</p>
    <div class="dim">
      <div><span class="idx">02</span></div>
      <div>
        <h2>One object, four fields, three legal address forms.</h2>
        <pre>"behaviour": {
  "script":   null | "knowledge/&lt;path&gt;.js" | "knowledge/snippets/&lt;Slug&gt;.reference.html#script",
  "partial":  null | "&lt;name registered in component-types.json $behaviour&gt;",
  "events":   ["click", "keydown", …],        // OPTIONAL — rC Q3 is open
  "fallback": "what it does with JS off" | null, // null = not declared (unproven), never "none"
  "$note":    … the old prose, verbatim …,
  "$unproven": ["fallback"]                    // only when a field is null for want of evidence
}</pre>
        <ol>
          <li><b><code>script: null</code> is a positive statement</b> — “this component carries no script.” It is never “unknown”.</li>
          <li><b><code>#script</code> means the snippet's own inline script</b>, outside any <code>AUTO-BEHAVIOUR</code> markers, matched byte-for-byte (the s235-D1 posture: the bytes are the key). It must name the component's <b>own</b> snippet — shared behaviour is a registered partial, never a pointer into another component's file.</li>
          <li><b><code>fallback: null</code> means undeclared.</b> A passive component says it in words: “identical — the component carries no script”.</li>
          <li><b>The meta is the one home.</b> <code>gen_component_partials.py</code> derives a <code>#behaviour-manifest</code> block into the snippet beside <code>#token-manifest</code>; <code>_validate_receipt.py</code> reads the meta and checks the page loads what it names. Neither copies the other.</li>
        </ol>
        <div class="pair">
          <div class="col n">
            <div class="colhead a">(b) Node-id grammar — not taken</div>
            <pre>"script": "snippet:Date-picker.reference.html#script"</pre>
            <p class="small">Matches the KG edge grammar (<code>component:</code> · <code>snippet:</code> · <code>ruling:</code>). But the receipt's <code>script</code> field and the registry's <code>source</code> already use repo paths (<code>knowledge/canon/dv-behaviour.js</code>) — two grammars for one field, and a file address has no node-id prefix.</p>
          </div>
          <div class="col">
            <div class="colhead b">(a) Path + fragment — proposed</div>
            <pre>"script": "knowledge/snippets/Date-picker.reference.html#script"
"script": "knowledge/canon/dv-behaviour.js"</pre>
            <p class="small">One grammar with the receipt and the registry; <code>os.path.isfile</code> resolves the file half, and <code>#script</code> is the only fragment. The schema refuses (b) on sight (schema arm: “node-id grammar” goes red).</p>
          </div>
        </div>
        <p class="small muted" style="margin-top:var(--s2)">Schema change, by addition: a <code>behaviourAddress</code> definition and a discriminated <code>behaviour</code> property (an object carrying <code>script</code> must be an address; anything else is the pre-s234-D5 prose, legal during migration, closed later by a ratchet gate — never by the schema). All 136 live metas still validate; the 20 proposals validate; @@schema_arms@@ schema arms behave (15 red, 6 green). Diff: <code>notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/meta.schema.proposed.diff</code>.</p>
      </div>
    </div>
  </div>
</section>

<section id="twenty">
  <div class="wrap">
    <p class="label">The twenty, side by side</p>
    <div class="dim">
      <div><span class="idx">03</span></div>
      <div>
        <h2>Old on the left, proposed on the right. Every field says where it came from.</h2>
        <p>Read the chips: <span class="chip p">prose</span> the meta's own words · <span class="chip m">measured</span> a probe on the snippet · <span class="chip u">unproven</span> nothing settles it. A candidate reading sits in a red-ruled box and is <b>not in the proposal</b>.</p>
        <div class="ctl" role="group" aria-label="Filter the twenty">
          <button type="button" data-f="all" aria-pressed="true">All 20</button>
          <button type="button" data-f="passive" aria-pressed="false">Passive · @@n_passive@@</button>
          <button type="button" data-f="scripted" aria-pressed="false">Carry a script · @@n_scripted@@</button>
          <button type="button" data-f="unproven" aria-pressed="false">With an unproven field · @@n_unproven_metas@@</button>
        </div>
      </div>
    </div>
    <div id="items">@@items@@</div>
  </div>
</section>

<section id="proof" class="band">
  <div class="wrap">
    <p class="label">Proof, on a real page</p>
    <div class="dim">
      <div><span class="idx">04</span></div>
      <div>
        <h2>Driven on a fixture copy — never the live tree — with the brief's three arms and nine more.</h2>
        <p>A copy of <code>knowledge/</code> under <code>/dev/shm</code> took the proposed schema and the 20 typed objects; the generator injected 20 <code>#behaviour-manifest</code> blocks (only those 20 snippets differ from the live tree, and <code>--check</code> is green again); L1's mint composed one page from Date-picker, Textarea and Stat-card with the two scripts spliced verbatim. Then the gate was driven, and its inputs mutated:</p>
        <div class="scroll"><table>
          <thead><tr><th class="id">Arm</th><th>What was planted</th><th class="id">Result</th><th>Verdict</th></tr></thead>
          <tbody>@@drive_rows@@</tbody>
        </table></div>
        <p class="small muted" style="margin-top:var(--s2)">@@drives_ok@@ of @@n_drives@@ as expected. Each transcript is a file: <code>notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/drive-*.txt</code>. Beside them: @@gate_arms@@ gate self-test arms green with @@gate_mut@@ gate mutants caught, and @@gen_mut@@ generator mutants caught. The live regen serial is untouched: 0 metas are typed today, so the pass emits nothing and <code>--check</code> on the live tree is OK.</p>
      </div>
    </div>
  </div>
</section>

<section id="l1">
  <div class="wrap">
    <p class="label">The three questions L1 left behind</p>
    <div class="dim">
      <div><span class="idx">05</span></div>
      <div>
        <h2>Carried, not ruled. Options priced, one recommendation each.</h2>

        <div class="qq">
          <p class="num">L1 question 1</p>
          <h3>When does a missing receipt start blocking?</h3>
          <p>Today the chained step reports <code>UNPROVEN:NO-RECEIPT</code> and does not block; <code>--receipt-strict</code> blocks now. Flipping the default reds <b>7 of 7</b> screens in the default population (re-measured on the fixture today: 7 × <code>UNPROVEN:NO-RECEIPT</code>, <code>RESULT: PASS</code>).</p>
          <ol>
            <li>(a) leave advisory until pages are re-minted — cheap, the ADR-0013 ratchet posture;</li>
            <li>(b) block now and mint receipts onto all 7 — but those pages were hand-composed, so their “spliced regions” would be invented, the exact defect the gate exists to catch;</li>
            <li>(c) block for new pages only, by date or folder — needs a rule about which, and folder globs are what s234-D6 refused to widen.</li>
          </ol>
          <p class="rec"><b>Recommend (a) now, (b) by regeneration later</b> — same as L1. What this lane adds: the behaviour-address step is a <b>second</b> ratchet under the first, and it needs its own date — see this lane's question 3.</p>
        </div>

        <div class="qq">
          <p class="num">L1 question 2</p>
          <h3>What does a composed page do about CSS?</h3>
          <p>Splicing snippet <code>&lt;style&gt;</code> verbatim carries hex into the page and reds <code>_validate_compose</code>; hand-writing CSS passes compose but cannot carry a receipt. <b>Reproduced on this lane's fixture: 98 hex colours, compose ❌</b>, while the receipt step (with the new behaviour check) was ✅ on the same page.</p>
          <ol>
            <li>(a) the composer projects theme values through <code>gen_snippet_tokens</code>'s resolution instead of copying the block — real work; the CSS region becomes a derived artefact whose hash still holds;</li>
            <li>(b) composed pages link <code>canon/canon.css</code> — 0 of 136 snippets have ever done it;</li>
            <li>(c) exempt spliced style regions from the hex check — a loosened gate.</li>
          </ol>
          <p class="rec"><b>Recommend (a)</b>, as a lane of its own. Until it lands, a page is composable or provable, not both.</p>
        </div>

        <div class="qq">
          <p class="num">L1 question 3</p>
          <h3>Should <code>dashboards/*.html</code> be permanent subjects of the screen-gate index?</h3>
          <p>Running the chain minted two dashboard rows into <code>_SCREEN-GATE.md</code> beside the seven fitness screens. This lane <b>did not add a third</b>: the chain was driven on the fixture copy, so the live index is unchanged.</p>
          <ol>
            <li>(a) keep — one home per subject is the gate's design (#230 T5);</li>
            <li>(b) drop the two rows before commit — the index stays the fitness-test roll;</li>
            <li>(c) a second index for composed pages — one more generated surface to keep honest.</li>
          </ol>
          <p class="rec"><b>Recommend (a)</b> — a gate that forgets what it gated is the read-chain staleness class; if the roll must stay small, that is a rule about subjects, not about the index.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="mine" class="band">
  <div class="wrap">
    <p class="label">This lane's questions</p>
    <div class="dim">
      <div><span class="idx">06</span></div>
      <div>
        <h2>Five things the proposal had to choose, put back to you.</h2>

        <div class="qq">
          <p class="num">Question 1</p>
          <h3>The address grammar — (a) path + fragment or (b) node-id?</h3>
          <p>Shown side by side under <a href="#shape">The shape</a>. The schema pattern, the resolver and the generator all encode (a); switching to (b) is one pattern and one regex.</p>
          <p class="rec"><b>Recommend (a)</b> — one grammar with the receipt and the registry.</p>
        </div>

        <div class="qq">
          <p class="num">Question 2</p>
          <h3><code>partial</code> — one name, or a list?</h3>
          <p>The brief's shape is a single id. Measured today: <b>14 dataviz snippets carry registry partials, 9 of them two or three</b> (Chart-donut: dv-behaviour · dv-donut-sweep · dv-legend), and none of their 14 metas has a <code>behaviour</code> key at all. For the 20 in scope <code>partial</code> is null everywhere, so the shape does not bite yet.</p>
          <ol>
            <li>(a) keep the singular now; widen when the dataviz population is typed;</li>
            <li>(b) <code>string | string[] | null</code> today, by addition;</li>
            <li>(c) rename to <code>partials: []</code>.</li>
          </ol>
          <p class="rec"><b>Recommend (b)</b> — the widening is free now and forced later; the 14 dataviz metas are then a mechanical second migration (registry → meta), priced at ~2K tokens.</p>
        </div>

        <div class="qq">
          <p class="num">Question 3</p>
          <h3>When does a PROSE meta start blocking the gate?</h3>
          <p>Today a region whose meta is prose (or has no <code>behaviour</code>) is one <code>UNPROVEN:behaviour-address</code> line, never red. After you ratify the 20, the honest next ratchet is: a meta with a <code>behaviour</code> key that is still prose blocks. 0 metas would go red the day the 20 land.</p>
          <p class="rec"><b>Recommend: block prose <code>behaviour</code> the same day the 20 are written</b> (a <code>--behaviour-strict</code> switch exists in spirit — one flag, ~300 tokens). Metas with <b>no</b> <code>behaviour</code> key stay UNPROVEN until rC Q3 and the dataviz migration settle what “none” means.</p>
        </div>

        <div class="qq">
          <p class="num">Question 4</p>
          <h3><code>events</code> — is the field wanted at all? (rC Q3, still yours)</h3>
          <p>The brief's shape includes it; rC Q3 is open. The proposal fills it from the snippet's <code>addEventListener</code> names (the page-level modality tracker excluded) and marks the whole field floated. The schema makes it optional.</p>
          <p class="rec"><b>Recommend keeping it, optional, measured never authored</b> — it is the line a developer wiring the page reads first, and a generator can mint it from the snippet so nobody types it.</p>
        </div>

        <div class="qq">
          <p class="num">Question 5</p>
          <h3>The 14 candidate <code>fallback</code> readings — accept, reject, or render?</h3>
          <p>Each is one sentence in a red-ruled box. What would prove them is a JS-off render of each snippet (rA's resilience criterion), ~3K tokens for the set, or your word.</p>
          <p class="rec"><b>Recommend the render</b> — a candidate promoted on my reading alone is the “likeliest reading” pitfall the brief named.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="rule2a">
  <div class="wrap">
    <p class="label">Rule 2a, proposed text — not written into the pack</p>
    <div class="dim">
      <div><span class="idx">07</span></div>
      <div>
        <h2>Beside rule 2, never re-wording it.</h2>
        <pre>2a. **Copy the script address with the markup; author no JS.** Every snippet whose
    component carries behaviour declares its ADDRESS in `knowledge/components/&lt;slug&gt;.meta.json`
    (`behaviour.script`) and carries the same address in a `#behaviour-manifest` block beside
    `#token-manifest`. Take the snippet's own `&lt;script&gt;` (or its `AUTO-BEHAVIOUR` block)
    verbatim — the bytes are the key — and carry the address into the page's receipt. Never
    write a handler yourself, never paraphrase the script, never point at another component's
    script: shared behaviour is a registered partial. `fallback` says what the component does
    with JavaScript off; if it is null, say so in the Gaps list rather than inventing one.
    `_validate_receipt.py` reads the meta and checks the page loads what it names.</pre>
        <p class="small muted">Rule 2's sentence is untouched (header-wins-over-audit); 2a sits beside it as 8a sits beside 8. v1.0.5 is held and no version is bumped by this page.</p>
      </div>
    </div>
  </div>
</section>

<section id="risk" class="band">
  <div class="wrap">
    <p class="label">Consequences, replayed</p>
    <div class="dim">
      <div><span class="idx">08</span></div>
      <div>
        <h2>What could go wrong with what was built, and who owns each.</h2>
      </div>
    </div>
    <div class="cards" style="margin-top:var(--s4)">
      <div class="card"><span class="n">01</span><h3>A `#script` address rots when a snippet gains a second script</h3><p>`#script` denotes every inline executable script outside AUTO-BEHAVIOUR markers. A second script changes the resolved set; the gate then demands both and a page carrying one goes red with a named hint.</p><p class="own">owner: the snippet author; caught by the generator's --check</p></div>
      <div class="card"><span class="n">02</span><h3>A whitespace-shifted copy is red</h3><p>By design (s235-D1). An agent that re-indents the script fails BEHAVIOUR-NOT-LOADED with the hint “matches after whitespace normalisation — copy verbatim”. If that reads as friction, it is a ruling about the key, not a bug.</p><p class="own">owner: Dave (the key)</p></div>
      <div class="card"><span class="n">03</span><h3>The L1 mint has no `kind: script`</h3><p>`gen_provenance_receipt.py --compose` splices markup, style and AUTO-BEHAVIOUR blocks, not a snippet's plain inline script. The fixture spliced by hand; the mint needs one more kind (~1K tokens) or composed pages cannot carry the 14 scripts receipted.</p><p class="own">owner: L1's file, next lane</p></div>
      <div class="card"><span class="n">04</span><h3>The mint's `$scriptNote` goes stale</h3><p>It says meta behaviour is untyped prose. Once the 20 are typed the note is false for 20 snippets; the mint should read the meta through the gate's resolver (one import, ~500 tokens).</p><p class="own">owner: L1's file, next lane</p></div>
      <div class="card"><span class="n">05</span><h3>`partial` is singular; the dataviz population is not</h3><p>Typing Chart-donut needs three names. Question 2 above.</p><p class="own">owner: Dave</p></div>
      <div class="card"><span class="n">06</span><h3>The regen serial, if the 20 are applied</h3><p>Writing the 20 metas puts 20 snippets out of sync until `gen_component_partials.py` runs — whole serial per wave, ramp first, index last (#210). Never `_build_all.py` from a sub.</p><p class="own">owner: the conductor at apply time</p></div>
      <div class="card"><span class="n">07</span><h3>Candidate readings look like values</h3><p>They sit in a red-ruled box and in `provenance`, never in `proposed`. A copy-paste of the box into a meta is the “likeliest reading” defect.</p><p class="own">owner: whoever applies the migration</p></div>
      <div class="card"><span class="n">08</span><h3>A gate that is not a consumer of every commit is not a gate</h3><p>The new checks run inside `_validate_receipt.py`, which `_validate_screen.py` chains and `--check` reads — but only pages that carry a receipt reach them. Until L1's question 1 flips, the population under this gate is one fixture and one dashboard.</p><p class="own">owner: Dave (the blocking date)</p></div>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <p>#238 lane B · derived from <code>notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/behaviour-migration.json</code> · schema fragment, diff, drives and self-tests in the same directory · report at <code>notes/_subreports/2026-09-02-238-B-L2-behaviour-address.md</code></p>
    <p>Everything on this page is <b>proposed</b>. No meta was written, no ruling inscribed, no pack version bumped.</p>
  </div>
</footer>

<script>
(function(){
  var b=document.getElementById('tt'), r=document.documentElement;
  if(window.matchMedia && window.matchMedia('(prefers-color-scheme:dark)').matches){r.setAttribute('data-theme','dark');}
  function sync(){b.textContent = r.getAttribute('data-theme')==='dark' ? 'Light' : 'Dark';}
  sync();
  b.addEventListener('click',function(){ r.setAttribute('data-theme', r.getAttribute('data-theme')==='dark'?'light':'dark'); sync(); });
  var ctl=document.querySelectorAll('.ctl button'), items=document.querySelectorAll('.item');
  ctl.forEach(function(btn){ btn.addEventListener('click',function(){
    var f=btn.getAttribute('data-f');
    ctl.forEach(function(x){ x.setAttribute('aria-pressed', x===btn ? 'true' : 'false'); });
    items.forEach(function(it){ it.hidden = !(f==='all' || it.getAttribute('data-tags').split(' ').indexOf(f)>=0); });
  }); });
})();
</script>
</body>
</html>
'''
_subs = dict(n_metas=C["metas_with_behaviour"], n_passive=len(passive), n_scripted=len(scripted),
           n_unproven_metas=C["metas_with_any_unproven"], f_prose=C["fields_by_basis"]["prose"],
           f_meas=C["fields_by_basis"]["measured"], f_unp=C["fields_by_basis"]["UNPROVEN"],
           gate_arms=gate_arms, gate_mut=gate_mutants, gen_mut=gen_mutants, schema_arms=schema_arms,
           items=items_html, drive_rows=drive_rows, drives_ok=drives_ok, n_drives=len(drives))
for _k, _v in _subs.items():
    page = page.replace('@@%s@@' % _k, str(_v))

open(OUT, "w", encoding="utf-8").write(page)
print("wrote", os.path.relpath(OUT, REPO), len(page.encode("utf-8")), "bytes;",
      "items", len(mig["items"]), "gate arms", gate_arms, "gate mutants", gate_mutants, "gen mutants", gen_mutants,
      "schema arms", schema_arms, "drives", drives_ok, "/", len(drives))
