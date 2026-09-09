#!/usr/bin/env python3
# #263 lane P — generator for notes/_PROPOSED-263.html. Lane fragment, not canon.
import html, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parents[2]
TYPECSS = (ROOT / "knowledge/canon/type.css").read_text(encoding="utf-8")

ITEMS = [
 dict(id="P-01", title="The delta glyph's colour seat — ink, not fill", lane="K — KPI tile",
  quote="The delta glyph’s colour seat — <code>ink</code> or <code>fill</code>? <em>Recommend <code>ink</code>.</em>",
  reason="Bind the glyph to <code>rag/success-ink</code> · <code>rag/error-ink</code> so it matches the spark stroke and clears the 3:1 floor in all four themes; three of the four currently put the light-mode glyph under it. Stat card moves with it, always.",
  current="knowledge/snippets/Kpi-tile.reference.html:151–152",
  currentnote="Shipped on the INK seat: <code>--pos-ink:#137F3C</code> / <code>--neg-ink:#DA1A00</code> light, <code>#66CC8D</code> / <code>#F6604C</code> dark — arrow now theme-invariant, mode-forked.",
  alt="<b>fill</b> — keep the glyph on <code>rag/success</code> / <code>rag/error</code> as inherited byte-for-byte from the gated Stat-card manifest (1.980:1 for that green on a white card, measured at #203). Two seats side by side, which is the state #203 left.",
  thin="⚠ OVERLAPS AN ANSWER HE ALREADY GAVE. The K3 review carries his verbatim <em>“We need to use the dark versions of the colours on the arrows”</em>, and the snippet header calls the two-seat question CLOSED on it — but no ruling <code>s261-D*</code> states the seat, and <code>s261-D4</code>’s text is the layout/arrow/dot answer. Confirm or correct.",
  src="notes/_subreports/2026-09-08-261-K-kpi-tile.md:102–104"),

 dict(id="P-02", title="Group row stays a typographic distinction — type, not split", lane="G — data-grid header",
  quote="The group row has no ground of its own. … Either a theme splits the two tokens, or the group row stays a typographic distinction. <b>split</b> or <b>type</b>.",
  reason="<code>--grouphdr</code> binds <code>table/column/background</code>, which resolves to the same hex as <code>table/header/background</code> in all four themes today, so the row reads by caption type and its rule rather than by ground.",
  current="knowledge/snippets/Data-grid.reference.html:129, 138, 211",
  currentnote="<code>--grouphdr:#F0F0F0</code> light / <code>#1F1F1F</code> dark — the same value as the header bone; <code>background:var(--grouphdr)</code> at :211. No visual split today.",
  alt="<b>split</b> — a theme (or all four) gives <code>table/column/background</code> its own value so the group row carries a distinct ground. Costs a token decision per theme and a fresh four-theme contrast measurement.",
  thin="", src="notes/_subreports/2026-09-08-261-G-grid-header.md:56–58"),

 dict(id="P-03", title="Disabled column muted with alpha, not text/disabled", lane="G — data-grid header",
  quote="The disabled column is muted with alpha, not <code>text/disabled</code>. That token is #E1E1E1, illegible on the #F0F0F0 header ground; <code>.pbtn[disabled]</code> only works because pagination sits on the page. <b>alpha</b> or <b>token</b>.",
  reason="The ruled disabled token cannot be read on the header’s own ground, so the lane muted with opacity instead of inventing a value. Reference (the editable column) is not sortable — re-ordering rows under an open editor is the bug — and the state is doubled by <code>aria-disabled</code>, no <code>aria-sort</code>, and no glyph.",
  current="knowledge/snippets/Data-grid.reference.html:249",
  currentnote="<code>th[data-disabled] .sort{cursor:default; opacity:var(--alpha-48);}</code> with the comment naming the reason: the disabled ink #E1E1E1 is illegible on the header ground.",
  alt="<b>token</b> — use <code>text/disabled</code> as ruled and accept the contrast, or mint a header-ground disabled value (a new token, four themes).",
  thin="", src="notes/_subreports/2026-09-08-261-G-grid-header.md:59–60"),

 dict(id="P-04", title="Adopt the <code>data-apollo-filter-*</code> marker contract", lane="F — filter/toolbar bar",
  quote="Marker: <code>data-apollo-filter-bar</code> on the driver · <code>data-apollo-filter-target=\"&lt;selector&gt;\"</code> optional · <code>data-apollo-filter-consumer</code> on anything that renders a result set.",
  reason="Under <code>s258-D1</code> the bar must drive something. The three markers name the driver, its optional target and any consumer; the bar emits <code>apollo:filter-change</code> / <code>-clear</code> / <code>-export</code> and writes <code>data-apollo-view</code> / <code>-density</code> onto the consumer so a CSS-only consumer needs no script. The read-back leg (<code>data-apollo-result-count</code> / <code>-total</code> / <code>-state</code>) is the point: the bar never sets its own state from the request it just made.",
  current="knowledge/snippets/Filter-toolbar-bar.reference.html:433 · knowledge/components/filter-toolbar-bar.meta.json:119–123",
  currentnote="Shipped and consumed: <code>&lt;div class=\"ftb-outer\" data-apollo-filter-bar data-apollo-filter-target=\"#demo-consumer\"&gt;</code>; five meta edges are already conditioned on <code>the consumer declares data-apollo-filter-consumer</code>.",
  alt="Do not adopt as a system-wide naming convention — keep the markers local to this component, or rename them under a different prefix before five meta edges and the data-grid / table / list / tile / chart consumers depend on them.",
  thin="⚠ THIN SOURCE. The F subreport documents the contract (edges.$contract in the meta) but contains NO “ruling-shaped” ask for it — the wording quoted here is the review page’s own spec table, not a recommendation sentence. The item is on the eleven-list; its stated recommendation is not in the report.",
  src="notes/_lanes/261-F-filter-toolbar-review.html:153–155 · notes/_subreports/2026-09-08-261-F-filter-toolbar.md:10–16"),

 dict(id="P-05", title="Two rows collapse to one at 1400px", lane="F — filter/toolbar bar",
  quote="Two rows collapse to one at a container width of 1400px; 680px gives the search its own row; 400px stacks everything (375px verified, no horizontal scroll).",
  reason="All container queries, so the bar is legal inside a bento tile (<code>s248-D3</code>). Sticky with an EARNED shadow — an IntersectionObserver sentinel, not a permanent drop shadow.",
  current="knowledge/snippets/Filter-toolbar-bar.reference.html — container queries at 1400 / 680 / 400",
  currentnote="Measured in Chromium @1400px during the lane: view 38→48, density 34→48, <code>.trigger</code> and search field 48.",
  alt="A different collapse width (the footer lane’s one-row width moved 1440→1600 for the same class of reason), or media queries instead of container queries — which would forfeit the bento legality.",
  thin="⚠ SOURCE IS A BUILD NOTE, NOT AN ASK. 1400 is stated as what was built; the F report lists no alternative and no recommendation sentence for it.",
  src="notes/_subreports/2026-09-08-261-F-filter-toolbar.md:29–32"),

 dict(id="P-06", title="Keep the name Tab-bar for the app-level bottom bar", lane="N — nav family",
  quote="Tab bar means the bottom bar, not section tabs — KEEP or RENAME? … <b>Recommend KEEP.</b>",
  reason="The lane brief described Tab-bar as in-page section tabs with overflow fade and underline; that is the gated <b>Tabs</b> component, and Tab-bar’s own meta has said <em>“app-level BOTTOM navigation, NOT the in-page Tabs component”</em> since it was surfaced. Redefining it would make two components mean one thing and leave the mobile bottom bar homeless.",
  current="knowledge/components/tab-bar.meta.json · knowledge/snippets/Tab-bar.reference.html",
  currentnote="Built to the canon meaning: bottom bar, counts riding the glyph, smallest visible <code>.nv-item</code> 81×46. The section-tab reading is drawn on the same tokens inside the review page’s app frame.",
  alt="<b>RENAME</b> — give the bottom bar a new name (e.g. Bottom-nav) and free “Tab-bar”, at the cost of a rename across the nav family, the manifest and the showroom.",
  thin="", src="notes/_subreports/2026-09-08-261-N-nav.md:93–98"),

 dict(id="P-07", title="Retire the doormat rather than park it", lane="Ft — footer",
  quote="Doormat: retire or park? → <b>Retire.</b> Out of scope by Dave’s words, recipe and findings preserved under <code>$retired</code>; it returns as its own component when a marketing pass needs it.",
  reason="Your scope for the pass, verbatim: <em>“App footer for now”</em>. The doormat / mega-footer is a marketing and servicing artefact and sits outside it. Retiring keeps the findings so a later marketing pass restores rather than re-derives.",
  current="knowledge/components/footer.meta.json:100–103",
  currentnote="<code>$retired</code> holds <em>“variant / prop value: doormat (the mega-footer), and the props groups[] and backToTop that served it”</em>, <code>retiredAt: “#261”</code>. The prop <code>form</code> (doormat | slim) is gone, replaced by <code>variant</code>.",
  alt="<b>park</b> — keep the doormat as a dormant variant of Footer so it stays one component, at the cost of a prop that no app footer ever uses.",
  thin="", src="notes/_subreports/2026-09-08-261-Ft-footer.md:82–83"),

 dict(id="P-08", title="Legend hit targets stay 44px — no dense 24px floor", lane="L — legend",
  quote="Dense legend at the 24px floor — no / yes. Recommend <b>no</b>: 2026-07-25 already ruled 44 everywhere and explicitly reversed the 24px dense proposal. The lane brief asked for 24; the ruling outranks the brief, so 44 shipped and nothing was re-litigated.",
  reason="The swatch is ONE component and your 2026-07-25 ruling reads <em>“44 EVERYWHERE … reverses the 24px dense-case proposal”</em>. A lane does not re-open a ruling; 24 is recorded in the meta as the floor a dense variant <em>would</em> sit on.",
  current="knowledge/snippets/Legend.reference.html — 44px via an invisible <code>::before</code>",
  currentnote="44px everywhere. The footer lane, on the same question, sits at the ruled 24px dial-down floor and asked to mint <code>target/floor</code> = 24px — so the two lanes ship different answers to one floor.",
  alt="<b>yes</b> — a dense legend variant at the 24px floor, which needs the 44-everywhere ruling amended by addition, not a lane’s judgment.",
  thin="", src="notes/_subreports/2026-09-08-261-L-legend.md:47–50, 86–88"),

 dict(id="P-09", title="<code>data-dv-controls</code> ships contract-only, unwired", lane="L — legend",
  quote="<code>data-dv-controls</code> — contract / wire. Recommend <b>contract</b> (as shipped): wiring it means editing canon <code>dv-legend.js</code> for all ten chart consumers, which is an engine ruling, not a component’s.",
  reason="dv-legend resolves its marks with <code>host.closest('figure')</code>, so one legend + three canvases in one <code>&lt;figure&gt;</code> is already a shared legend by construction. Widening resolution from <code>closest('figure')</code> to a document-wide id lookup changes what all ten chart legends control — an engine change with a blast radius.",
  current="knowledge/canon/dv-legend.js — resolution is <code>host.closest('figure')</code>; the attribute is declared and not read",
  currentnote="<code>data-dv-controls=\"&lt;chart id&gt; …\"</code> ships as a contract only; the engine does not read it.",
  alt="<b>wire</b> — make dv-legend honour the attribute with a document-wide id lookup, i.e. an engine change touching all ten chart consumers. ⚠ An attribute nothing reads is the <em>instrument-without-a-consumer</em> shape; leaving it declared is not cost-free either.",
  thin="", src="notes/_subreports/2026-09-08-261-L-legend.md:52–57, 90–92"),

 dict(id="P-10", title="<code>_render_rulings.py --check</code> as a wrap-ritual gate", lane="R — rulings page",
  quote="Should <code>--check</code> become a WRAP-RITUAL GATE — wrap fails if <code>_RULINGS.html</code> is STALE? The hook exists and exits 1; wiring it into the wrap is HIS ruling, not mine.",
  reason="The generator already proves the page against the store’s sha256, and the RED path was DRIVEN, not assumed — one byte mutated inside a <code>says</code> value made <code>--check</code> exit 1 with the two digests named; the control run exited 0. So the gate works; only the ritual wiring is missing.",
  current="knowledge/_render_rulings.py (<code>--check</code> exists, exit 1 on stale) — not referenced by the wrap ritual",
  currentnote="Receipt verbatim: <code>FRESH _RULINGS.html matches _rulings.json sha256 e69957c57eeb…</code> (exit 0); mutated source → <code>STALE _RULINGS.html embeds e69957… but mut.json is now 16a87b…</code> (exit 1).",
  alt="Leave it a hook a conductor may run. ⚠ Weight against <code>s261-D9</code>, your own words on this page: <em>“this is a lot and will impede our progress”</em> — a new wrap gate is a new way for a wrap to fail.",
  thin="", src="notes/_subreports/2026-09-08-261-R-rulings-page.md — “Open questions for Dave”, item 1"),

 dict(id="P-11", title="Retire <code>_validate_snippets.py</code>’s source-text aria arm", lane="D3 — driver scope",
  quote="<code>_validate_snippets.py</code> is outside the lane fence. Its <code>requiredAria</code> arm still reads SOURCE TEXT and still fails open on its own; the DOM-reading arm had to be built in <code>_validate_dataviz.py</code> instead. Two gates now answer the same rule from different evidence — ruling-shaped: fold the source-text arm into the driven one, or delete it.",
  reason="The fail-open is live, not hypothetical: six shipped snippets satisfy a <code>requiredAria</code> string ONLY from a JS string literal — <code>role=\"img\"</code> in Chart-boxplot, -bullet, -candlestick, -scatter, -sparkline; <code>aria-pressed</code> in Chart-histogram. Strip every role at runtime and the source-text arm still reads 0 blocking, GREEN, while the driven arm reads 1 hit, RED.",
  current="knowledge/_validate_snippets.py — <code>requiredAria</code> reads source text · knowledge/_validate_dataviz.py — <code>driven_aria</code> reads the rendered DOM",
  currentnote="Both arms live. The six literal passes are DETECTED, not fixed — the driven arm passes them because the engine really does emit those strings; only the source-text gate was lying about why.",
  alt="<b>fold</b> — keep one arm and make it the driven one; or keep both and accept two gates answering one rule from different evidence.",
  thin="", src="notes/_subreports/2026-09-08-261-D3-driver-scope.md:95–99, 28–30"),
]
assert len(ITEMS) == 11

def esc(s): return html.escape(s, quote=True)

cards = []
for n, it in enumerate(ITEMS, 1):
    thin = ('<p class="thin">%s</p>' % it["thin"]) if it["thin"] else ""
    cards.append(f"""
<article class="card" id="{it['id']}" data-pid="{it['id']}">
  <div class="chead">
    <span class="pid">{it['id']}</span>
    <h2 class="ctitle">{it['title']}</h2>
  </div>
  <div class="cbody">
    <p class="lane"><span class="k">Lane</span>{esc(it['lane'])}</p>
    <blockquote class="rec">{it['quote']}</blockquote>
    <p class="reason"><span class="k">Reason given</span>{it['reason']}</p>
    <p class="cur"><span class="k">Current default</span><code class="path">{it['current']}</code><br>{it['currentnote']}</p>
    <p class="alt"><span class="k">Alternative</span>{it['alt']}</p>
    {thin}
    <p class="src"><span class="k">Source</span><code class="path">{it['src']}</code></p>
  </div>
  <div class="rule-row">
    <span class="k">Your ruling</span>
    <div class="btns" role="radiogroup" aria-label="Ruling for {it['id']}">
      <button type="button" class="rb" data-v="ACCEPT" role="radio" aria-checked="false">Accept</button>
      <button type="button" class="rb" data-v="REJECT" role="radio" aria-checked="false">Reject</button>
      <button type="button" class="rb" data-v="LATER"  role="radio" aria-checked="false">Later</button>
    </div>
    <label class="notew"><span class="vh">Note for {it['id']}</span>
      <input type="text" class="note" placeholder="one line — your words, optional" maxlength="240"></label>
  </div>
</article>""")

TITLES = {it["id"]: it["title"] for it in ITEMS}
titles_json = json.dumps({k: html.unescape(__import__("re").sub("<[^>]+>", "", v)) for k, v in TITLES.items()}, ensure_ascii=False)

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eleven proposed defaults — #263</title>
<!-- #263 lane P. Self-contained: everything inline, no external resources of any kind. -->
<style>
/* ==========================================================================
   BAKED IN VERBATIM: knowledge/canon/type.css  (LABEL CROP PATTERN — review
   pages bake type.css in rather than link it, so the crop travels with the page).
   The component crop rule IS present in type.css and is named here:
     `text-box: trim-both cap alphabetic;`  on the control/label list
     (.btn, .chip, .seg button, .tabbar .tabbar__item, nav.main a, …),
   with the @supports-not fallback pair
     `.t-cm-slot::before/.btn::before` + `.t-cm-slot::after/.btn::after`
   using calc((0.5 - 0.65 + …)*-1em) against --cap / --desc.
   ========================================================================== */
{TYPECSS}
/* ===================== end baked type.css ===================== */

:root{{
  --accent:#DA1A00;            /* TWO-RED LAW s151-D1: on white */
  --bg:#FFFFFF; --panel:#F3F3F3; --rule:#E2E2E2; --rule-2:#D0D0D0;
  --ink:#000000; --ink-2:#333333; --ink-3:#545454; --ink-4:#767676;
  --quote-bg:#F7F7F5; --pill:#EDEDED;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Helvetica,Arial,sans-serif;
  --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem;
  --max:760px;
}}
@media (prefers-color-scheme:dark){{
  :root{{
    --accent:#F6604C;          /* TWO-RED LAW s151-D1: the light red everywhere else */
    --bg:#0C0C0C; --panel:#161616; --rule:#2A2A2A; --rule-2:#3A3A3A;
    --ink:#F2F2F2; --ink-2:#DCDCDC; --ink-3:#B8B8B8; --ink-4:#8E8E8E;
    --quote-bg:#141414; --pill:#222222;
  }}
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--ink);
  font:400 16px/1.7 var(--sans);overflow-wrap:break-word;overflow-x:hidden}}
.wrap{{max-width:var(--max);margin:0 auto;padding:0 var(--s3)}}
code{{font-family:var(--mono);font-size:.875em}}
code.path{{color:var(--ink-2);overflow-wrap:anywhere}}
.vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
.k{{display:block;font-size:11px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);margin:0 0 4px}}

/* Masthead */
header.mast{{padding:var(--s5) 0 var(--s3);border-bottom:1px solid var(--rule)}}
.eyebrow{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s2)}}
.eyebrow::before{{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:none}}
h1{{font-size:clamp(2rem,6vw,3rem);font-weight:500;line-height:1.05;margin:0 0 var(--s3)}}
.standfirst{{max-width:52ch;color:var(--ink-2);margin:0 0 var(--s3);font-size:15px}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s2);
  border-top:1px solid var(--rule);padding-top:var(--s3)}}
.stat b{{display:block;font-size:clamp(1.5rem,5vw,2.25rem);font-weight:200;line-height:1.05;
  font-variant-numeric:tabular-nums}}
.stat span{{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-4);margin-top:4px}}

/* Sticky control bar */
.bar{{position:sticky;top:0;z-index:10;background:var(--bg);
  border-bottom:1px solid var(--rule);padding:var(--s1) 0}}
.bar .wrap{{display:flex;flex-wrap:wrap;gap:var(--s1) var(--s2);align-items:center}}
.tally{{font-family:var(--mono);font-size:13px;color:var(--ink-4);white-space:nowrap}}
.tally b{{color:var(--accent);font-weight:500}}
.bar button,.bar label.tog{{font:400 13px/1.4 var(--sans);color:var(--ink);background:var(--bg);
  border:1px solid var(--rule-2);border-radius:0;padding:7px 12px;cursor:pointer;
  letter-spacing:.04em;white-space:nowrap}}
.bar label.tog{{display:flex;align-items:center;gap:6px}}
.bar button:hover{{border-color:var(--accent)}}

/* Cards */
main{{padding-bottom:var(--s6)}}
article.card{{border-top:1px solid var(--rule);padding:var(--s4) 0}}
.chead{{display:flex;gap:var(--s2);align-items:baseline;flex-wrap:wrap;margin:0 0 var(--s2)}}
.pid{{font-family:var(--mono);font-size:14px;color:var(--ink-4);flex:none}}
h2.ctitle{{font-size:20px;font-weight:500;line-height:1.3;margin:0;flex:1 1 240px;min-width:0}}
.cbody>p{{margin:0 0 var(--s2);font-size:15px;color:var(--ink-2)}}
.cbody .lane{{color:var(--ink-3);font-size:14px}}
blockquote.rec{{margin:0 0 var(--s2);background:var(--quote-bg);
  border-left:2px solid var(--accent);padding:var(--s2) var(--s3);
  font-size:16px;line-height:1.6;color:var(--ink)}}
.thin{{border-left:1px solid var(--rule-2);padding-left:var(--s2);font-size:14px;color:var(--ink-3)}}
.src{{font-size:13px;color:var(--ink-4)}}

/* Ruling row */
.rule-row{{border-top:1px solid var(--rule);padding-top:var(--s2);margin-top:var(--s2);
  display:flex;flex-wrap:wrap;gap:var(--s1) var(--s2);align-items:center}}
.rule-row .k{{flex:0 0 100%;margin-bottom:2px}}
.btns{{display:flex;gap:0;flex:none}}
button.rb{{font:400 14px/1.2 var(--sans);color:var(--ink-2);background:var(--bg);
  border:1px solid var(--rule-2);border-radius:0;padding:10px 16px;min-height:44px;
  margin-left:-1px;cursor:pointer;letter-spacing:.04em}}
button.rb:first-child{{margin-left:0}}
button.rb:hover{{border-color:var(--accent);position:relative;z-index:1}}
button.rb[aria-checked="true"]{{border-color:var(--accent);color:var(--ink);
  box-shadow:inset 0 -3px 0 0 var(--accent);position:relative;z-index:2;font-weight:500}}
label.notew{{flex:1 1 220px;min-width:0;max-width:100%}}
input.note{{width:100%;min-width:0;max-width:100%;font:400 14px/1.4 var(--sans);
  color:var(--ink);background:var(--bg);border:0;border-bottom:1px solid var(--rule-2);
  border-radius:0;padding:10px 2px;min-height:44px}}
input.note:focus{{outline:none;border-bottom-color:var(--accent)}}
article.card[data-ruled="1"] .pid{{color:var(--ink)}}
article.card[data-ruled="1"] .chead::after{{content:"";display:block;flex:0 0 100%;height:0}}

/* Export */
section.export{{border-top:1px solid var(--rule);padding-top:var(--s3);margin-top:var(--s4)}}
section.export h2{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);margin:0 0 var(--s2)}}
pre.out{{background:var(--panel);border:1px solid var(--rule);margin:var(--s2) 0 0;
  padding:var(--s2);font-family:var(--mono);font-size:12.5px;line-height:1.6;
  white-space:pre-wrap;overflow-wrap:anywhere;color:var(--ink-2)}}
footer{{border-top:1px solid var(--rule);padding:var(--s3) 0;font-size:13px;color:var(--ink-4)}}

/* Dave's decision only */
body.decide .cbody{{display:none}}
body.decide article.card{{padding:var(--s3) 0}}

@media (max-width:760px){{
  .wrap{{padding:0 var(--s2)}}
  .stats{{grid-template-columns:repeat(2,1fr)}}
  blockquote.rec{{padding:var(--s2)}}
  .btns{{flex:1 1 100%}}
  button.rb{{flex:1 1 0;padding:10px 8px}}
}}
@media print{{.bar{{display:none!important}}
  body{{background:#fff;color:#000;font-size:11pt}}
  article.card{{break-inside:avoid;page-break-inside:avoid}}
  blockquote.rec{{background:transparent;border-left:2px solid #DA1A00}}}}
</style>
</head>
<body>
<header class="mast"><div class="wrap">
  <p class="eyebrow">#263 · carried from #261, never ruled</p>
  <h1>Eleven proposed defaults — #263 · rule each</h1>
  <p class="standfirst">Eleven lane recommendations the #261 conductor defaulted to without you.
  They are carried as PROPOSED and are not in the ledger. Nothing below is pre-selected — every
  ruling row is empty until you touch it. A recommendation a conductor defaults to is a decision
  made without you, and writing it into the ledger would make it look like yours.</p>
  <div class="stats">
    <div class="stat"><b>11</b><span>proposed</span></div>
    <div class="stat"><b>0</b><span>ruled at #261</span></div>
    <div class="stat"><b>7</b><span>lanes</span></div>
    <div class="stat"><b id="sRuled">0</b><span>ruled here</span></div>
  </div>
</div></header>

<div class="bar"><div class="wrap">
  <span class="tally"><b id="tallyN">0</b> of 11 ruled</span>
  <label class="tog"><input type="checkbox" id="decide"> Dave&rsquo;s decision only</label>
  <button type="button" id="exportBtn">Export rulings</button>
  <button type="button" id="clearBtn">Clear all</button>
</div></div>

<main><div class="wrap">
{"".join(cards)}

<section class="export">
  <h2>Export — for the wrap to inscribe verbatim</h2>
  <p class="src">One line per ruled item, in card order. <code class="path">knowledge/_rulings.json</code>
  is written through <code class="path">_inscribe_ruling.py</code>; nothing here is inscribed by this page.</p>
  <pre class="out" id="out">Press &ldquo;Export rulings&rdquo;.</pre>
</section>
</div></main>

<footer><div class="wrap">#263 lane P · built from
<code class="path">notes/_subreports/2026-09-08-261-*.md</code> and
<code class="path">_DECISION-HISTORY/2026-09-09-261-six-components-and-a-false-premise.md</code>.
Selections are stored in this browser only (localStorage), never sent anywhere.</div></footer>

<script>
(function(){{
  var KEY = 'apollo-proposed-263';
  var TITLES = {titles_json};
  var cards = Array.prototype.slice.call(document.querySelectorAll('article.card'));
  var state = {{}};
  function load(){{
    try {{ var raw = localStorage.getItem(KEY); if (raw) state = JSON.parse(raw) || {{}}; }}
    catch (e) {{ state = {{}}; }}
    if (!state || typeof state !== 'object') state = {{}};
  }}
  function save(){{ try {{ localStorage.setItem(KEY, JSON.stringify(state)); }} catch (e) {{}} }}
  function tally(){{
    var n = 0;
    cards.forEach(function(c){{ var s = state[c.dataset.pid]; if (s && s.v) n++; }});
    document.getElementById('tallyN').textContent = n;
    document.getElementById('sRuled').textContent = n;
  }}
  function paint(c){{
    var s = state[c.dataset.pid] || {{}};
    c.setAttribute('data-ruled', s.v ? '1' : '0');
    c.querySelectorAll('button.rb').forEach(function(b){{
      b.setAttribute('aria-checked', (s.v === b.dataset.v) ? 'true' : 'false');
    }});
    var note = c.querySelector('input.note');
    if (note && document.activeElement !== note) note.value = s.note || '';
  }}
  cards.forEach(function(c){{
    c.querySelectorAll('button.rb').forEach(function(b){{
      b.addEventListener('click', function(){{
        var id = c.dataset.pid, s = state[id] || {{}};
        s.v = (s.v === b.dataset.v) ? '' : b.dataset.v;   /* click again to unset */
        state[id] = s; save(); paint(c); tally();
      }});
    }});
    var note = c.querySelector('input.note');
    note.addEventListener('input', function(){{
      var id = c.dataset.pid, s = state[id] || {{}};
      s.note = note.value; state[id] = s; save();
    }});
  }});
  document.getElementById('decide').addEventListener('change', function(){{
    document.body.classList.toggle('decide', this.checked);
  }});
  document.getElementById('clearBtn').addEventListener('click', function(){{
    state = {{}}; save(); cards.forEach(paint); tally();
    document.getElementById('out').textContent = 'Cleared.';
  }});
  document.getElementById('exportBtn').addEventListener('click', function(){{
    var lines = [], d = 0;
    cards.forEach(function(c){{
      var id = c.dataset.pid, s = state[id] || {{}};
      if (!s.v) return;
      d++;
      lines.push('s263-D' + d + ' \\u00b7 ' + id + ' \\u00b7 ' + s.v + ' \\u00b7 ' +
                 TITLES[id] + ' \\u00b7 note: ' + ((s.note || '').trim() || '\\u2014'));
    }});
    var missing = cards.filter(function(c){{ return !(state[c.dataset.pid] || {{}}).v; }})
                       .map(function(c){{ return c.dataset.pid; }});
    var out = lines.length ? lines.join('\\n') : '(nothing ruled yet)';
    if (missing.length) out += '\\n\\nNOT RULED (' + missing.length + '): ' + missing.join(' ');
    document.getElementById('out').textContent = out;
  }});
  load(); cards.forEach(paint); tally();
}})();
</script>
</body></html>
"""

out = ROOT / "notes/_PROPOSED-263.html"
out.write_text(page, encoding="utf-8")
print("wrote", out, len(page.encode("utf-8")), "bytes")
