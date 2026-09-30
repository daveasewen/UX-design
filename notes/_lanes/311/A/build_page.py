"""#311 lane A — builds notes/_REVIEW-311-A-soft-white-and-tab-strip-2026-09-30-v1.html from #310 lane B's shell
(head styles and decision script, NEW key and path) and this lane's measured facts (img/facts-*.json, bloom_311A.txt)."""
import json, html
SRC='notes/_REVIEW-310-B-white-ink-and-tab-strip-2026-09-30-v1.html'
PAGE='notes/_REVIEW-311-A-soft-white-and-tab-strip-2026-09-30-v1.html'
A=open(SRC).read()
head=A[:A.index('<body')].replace('<title>White ink, tab strip</title>','<title>Soft white, tab strip</title>')
assert '<title>Soft white, tab strip</title>' in head
script=A[A.rindex('<script'):]
for a,b in [("review-310-B-white-ink-and-tab-strip-v1","review-311-A-soft-white-and-tab-strip-v1"),
            ("notes/_REVIEW-310-B-white-ink-and-tab-strip-2026-09-30-v1.html",PAGE),
            ("Session 310 · White ink and the tab strip · comments","Session 311 · The soft white and the tab strip, built · comments"),
            ("'3. Note on the page: '","'4. Note on the page: '"),
            ("review-310-B-white-ink-and-tab-strip.txt","review-311-A-soft-white-and-tab-strip.txt")]:
    assert a in script, a; script=script.replace(a,b)
FI=json.load(open('notes/_lanes/311/A/img/facts-ink.json')); FT=json.load(open('notes/_lanes/311/A/img/facts-tabs.json')); FS=json.load(open('notes/_lanes/311/A/img/facts-scpage.json'))
BLOOM=open('notes/_lanes/311/A/bloom_311A.txt').read()
I="_lanes/311/A/img/"
def img(f,alt): return f'<img src="{I}{f}" alt="{html.escape(alt)}">'
def pair(a,b,ca,cb,alta,altb): return f'<div class="pair"><figure><figcaption>{ca}</figcaption>{img(a,alta)}</figure><figure><figcaption>{cb}</figcaption>{img(b,altb)}</figure></div>'
def one(a,c,alt): return f'<div class="pair one"><figure><figcaption>{c}</figcaption>{img(a,alt)}</figure></div>'
def f2(x): return f"{x:.2f}"
TH=[("mono","Mono"),("console","Console"),("common","Common")]
ink_pairs=''.join(pair(f"01-{k}-before-top.png",f"01-{k}-after-top.png",f"{n} dark · before, white #FFFFFF",f"{n} dark · after, #E1E1E1",
    f"The top of the banking demo in {n} dark, before: white text",f"The top of the banking demo in {n} dark, after: text #E1E1E1") for k,n in TH)
def ctab_ink():
    h='<div class="scroll"><table class="ctab"><thead><tr><th>Theme · ink</th><th>Colour</th><th>On the black tile</th><th>On the grey ground</th><th>On the page</th><th>Floor</th></tr></thead><tbody>'
    for k,n in TH+[("supercharge","Supercharge")]:
        f=FI[k+"-after"]
        for p,v in f["pairs"].items():
            floor=4.5 if p.startswith('text') or p.endswith('-ink') else 3.0
            low=[g for g in ('tile','ground','page') if v[g]<floor]
            cls=' class="rec"' if low else ''
            h+=f'<tr{cls}><td>{n} · {p}</td><td class="n">{v["ink"]}</td>'+''.join(f'<td class="n">{"<b>" if v[g]<floor else ""}{f2(v[g])}{"</b>" if v[g]<floor else ""}</td>' for g in ('tile','ground','page'))+f'<td class="n">{floor}</td></tr>'
        h+=f'<tr><td>{n} · the demo\'s secondary lines (the ink at 60%)</td><td class="n">{f["secondary60"]}</td><td class="n">{f2(f["secondary60_cr"])}</td><td class="n">–</td><td class="n">–</td><td class="n">4.5</td></tr>'
    return h+'</tbody></table></div>'
def ctab_tabs():
    h='<div class="scroll"><table class="ctab"><thead><tr><th>Reading</th><th>Context</th><th>Strip</th><th>Ground</th><th>Unselected label (72%)</th><th>Underline</th></tr></thead><tbody>'
    for k,v in FT.items():
        for c in v: h+=f'<tr><td>{k}</td><td>{c["ctx"]}</td><td class="n">{c["strip"]}</td><td class="n">{c["ground"]}</td><td class="n">{c["label"]} · {f2(c["label_cr"])}</td><td class="n">{c["bar"]} · {f2(c["bar_cr"])}</td></tr>'
    return h+'</tbody></table></div>'
def ctab_sc():
    h='<div class="scroll"><table class="ctab"><thead><tr><th>Supercharge dark page</th><th>Page</th><th>Section</th><th>Tile</th><th>Tile on page</th><th>Tile on section</th><th>Text on page</th></tr></thead><tbody>'
    for k,n,rec in (("warm4-25211C-ctx","Its own one-step-up, warm/4 #25211C",True),("fix-13110E-ctx","The generator fixed as it stands: #13110E",False),("asis-ctx","As it is: #1A1A1A",False)):
        f=FS[k]; rc=' class="rec"' if rec else ''; h+=f'<tr{rc}><td>{n}</td><td class="n">{f["bg_default"]}</td><td class="n">{f["section"]}</td><td class="n">{f["tile"]}</td><td class="n">{f2(f["tile_on_page"])}</td><td class="n">{f2(f["tile_on_section"])}</td><td class="n">{f2(f["ink_on_page"])}</td></tr>'
    return h+'</tbody></table></div>'
C,M,S=FI["console-after"],FI["mono-after"],FI["supercharge-after"]
def call(cid,q,question,rec_text,chips,rec_v=""):
    ch=''.join(f'<button type="button" class="chip" data-v="{html.escape(v)}">{html.escape(l)}</button>' for v,l in chips)
    r=f'<p class="rec">{rec_text}</p>' if rec_text else ''
    return f'''<div class="call" data-id="{cid}" data-q="{html.escape(q)}" data-rec="{html.escape(rec_v)}">
      <p class="q">{question}</p>{r}
      <div class="chips">{ch}</div>
      <label class="field"><span>Your comment</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>'''
STAND=[("Yes, it stands","Yes, it stands"),("Change it (comment)","Change it (say how below)")]
SC_REC="Supercharge's dark page and section take warm/4 #25211C, one step up from its tile"
body=f'''<body>
<a id="rv-back" href="../index.html" target="_self" style="position:fixed;top:12px;left:12px;z-index:2147483647;background:#000;color:#fff;font:500 13px/1 'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:.04em;padding:10px 14px;text-decoration:none;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.25)">&larr; All review pages</a>

<nav class="toc" aria-label="Sections"><div class="wrap">
  <a href="#white">The soft white</a>
  <a href="#strip">The tab strip</a>
  <a href="#scpage">Supercharge's dark page</a>
  <a href="#else">Anything else</a>
</div></nav>

<header id="top">
  <div class="wrap grid">
    <div>
      <p class="label">Session 311 · review page · The soft white and the tab strip, built</p>
      <h1>Both of your 17:35 choices are built. Here they are, before and after, so you can say whether they stand.</h1>
      <p class="sub">The softer white on the banking demo in Mono, Console and Common, with Supercharge left as it was. The tab strip on every kind of ground Apollo composes, in light and dark. And one decision that is still yours: what colour Supercharge's dark page should be.</p>
    </div>
    <div class="meta">
      <span>Wednesday 30 September 2026</span>
      <span>For your page note: "i need to see this".</span>
      <span>Before is the library as it stood at your choice; after is the library as built now. Neither choice counts as done until you say it stands. Section 03 is pictures only: nothing is built.</span>
    </div>
  </div>
</header>

<section id="white">
  <div class="wrap">
    <p class="label">01 · The soft white · built, does it stand?</p>
    <h2>All dark text is now #E1E1E1 in Mono, Console and Common. Supercharge keeps its own #F7F6F4.</h2>
    <p class="quote">"2b: text #E1E1E1 on black tiles (Mono, Console, Common); Supercharge keeps #F7F6F4"</p>
    <p class="lead">Text on the black tiles comes down from 21 to 1 to 16 to 1, just under the 17.4 the digital black note asks for. The change moves all dark text, not only text on tiles: the header text on the grey ground goes from 16.5 to 12.6 to 1. The lightest secondary line on a tile still measures {f2(C["secondary60_cr"])} to 1.</p>
    <p>The top of the banking demo at 1440, dark, in each theme. Left is before, right is after.</p>
    {ink_pairs}
    <p>A metric and a payment row, enlarged four times so you can see the edge of each letter against the black.</p>
    {one("01-crop-console.png","Console dark · enlarged four times · before left, after right","A metric and a payment row enlarged four times in Console dark: left white, right #E1E1E1")}
    <p>Supercharge is unchanged: its text stays #F7F6F4 on its #13110E tile (17.45 to 1), measured the same before and after.</p>
    {one("01-supercharge-after-top.png","Supercharge dark · after · unchanged","The top of the banking demo in Supercharge dark, text still #F7F6F4")}
    <p>The two filter chevrons were the only text left in pure white. They now take the colour of the words beside them.</p>
    {one("01-chevrons-console.png","The two filter chevrons · Console dark · enlarged four times","Two dropdown triggers enlarged: before, the chevrons are brighter than their labels; after, they match")}
    <ul class="facts">
      <li><span class="k">Nothing left in white</span><span><b>No text on the demo is pure white any more</b> in Mono, Console or Common: {FI["console-before"]["pure_white_text_nodes"]} text elements before, 0 after.</span></li>
      <li><span class="k">Common's quieter text</span><span>Common already had a dimmer secondary grey in dark, #9B9B9B. It stays as it is. It is not the white your choice softens, and moving it to #E1E1E1 would make it brighter.</span></li>
      <li><span class="k">Icons stay white</span><span>Icons (the search glass in the header, for example) are still #FFFFFF. Your choice was about text, so they were not moved. They now sit a touch brighter than the words next to them. Say if you want them to follow.</span></li>
    </ul>
    {call("white","1. The soft white, built","Does it stand?","",STAND)}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Built at the source, not canon.css by hand: <code>knowledge/tokens/semantic-colour.json</code> <code>text/default</code> and <code>text/secondary</code> dark alias <code>color/neutral/12</code> #E1E1E1 (was <code>color/neutral/15</code> #FFFFFF), with the two cached followers re-stamped (<code>button/tertiary/label/default</code>, <code>button/quaternary/label/default</code>). Common: <code>apollo-legacy.overrides.json</code> <code>text/default</code> dark #E1E1E1; its <code>text/secondary</code> dark stays #9B9B9B. Supercharge: <code>apollo-supercharge.overrides.json</code> pins <code>text/default</code> and <code>text/secondary</code> to <code>color/warm/15</code> #F7F6F4 dark (its neutral/12 is warm/12 #CDC8C6), light restated #13110E.</li>
      <li>Everything bound to the text ink follows, by projection: tertiary and quaternary button labels, nav text, the flat sparkline, the neutral status, the filled rating star, the QR modules in dark, and similar component seats (all #FFFFFF to #E1E1E1 in canon.css).</li>
      <li>The chevrons: <code>.chev</code> in <code>Filter-toolbar-bar.reference.html</code> and <code>Dropdown.reference.html</code> painted <code>--icon</code> (<code>icon/default</code>, #FFFFFF in dark); the ▾ is a text glyph in the trigger, so it now takes <code>--text</code> (<code>text/default</code>). In light, Mono and Console do not move (both #1A1A1A); in Common light the chevron follows its #333333 label.</li>
      <li>Regenerated in order: gen_canon_tokens, gen_snippet_tokens, gen_token_ramp, gen_canon_components, gen_theme_cascade, gen_showroom; dark-mode, icon-delta, text and indicator contrast audits rebuilt; every generator's check is in sync.</li>
      <li>Measured contrast after the build, from the rendered demo (WCAG). Text floor 4.5, marks 3. Rows shaded carry a value under its floor, in bold.</li>
    </ol>
    {ctab_ink()}
    <ol start="6">
      <li>Every text pair clears 4.5 to 1 after the change; the lowest is the demo's 60% secondary line at {f2(C["secondary60_cr"])} to 1. The pairs under their floor are all status marks, not text, and none of them moved: the red mark in Console and Supercharge (#B92F1E, 2.5 to 2.9 to 1 on the grounds) and Common's red and blue marks (#A8000B, #305A85). They sit beside a word that carries the meaning, which your roundel rule allows. The build changes the ink and nothing else, so no ground and no mark changed.</li>
      <li>The bloom model (<code>reviews/_rag_bloom_model.py</code>, loaded without its prints by <code>notes/_lanes/311/A/bloom_311A.py</code>; relative scores, 100 = a 40 px white fill on #1A1A1A):</li>
    </ol>
    <pre style="white-space:pre;overflow-x:auto;font-size:12px;line-height:1.5">{html.escape(BLOOM)}</pre>
    <ol start="8"><li>Drivers: <code>notes/_lanes/311/A/render_311A.py</code> (before = canon.css at the commit before the build, served to a copy of the demo; after = the tree), facts in <code>img/facts-ink.json</code>.</li></ol>
    </details>
  </div>
</section>

<section id="strip" class="grey">
  <div class="wrap">
    <p class="label">02 · The tab strip · built, does it stand?</p>
    <h2>The strip now takes the colour of whatever it sits on. The band is gone in light and dark.</h2>
    <p class="quote">"The strip takes its container's colour in both modes"</p>
    <p class="lead">Four grounds, composed the way the banking demo composes: (a) straight on the page, (b) above tiles on a bento ground, (c) inside a tile, (d) above tiles on a section background. Left is before, right is after. Only the track line and the underline mark the strip now.</p>
    {pair("02-ctx-console-light-before.png","02-ctx-console-light-after.png","Console light · before","Console light · after","Light before: a white bar behind the tabs on the grey grounds","Light after: no bar on any ground")}
    {pair("02-ctx-console-dark-before.png","02-ctx-console-dark-after.png","Console dark · before","Console dark · after","Dark before: a black band behind the tabs on the page, the bento ground and the section","Dark after: no band on any ground")}
    {pair("02-ctx-supercharge-dark-before.png","02-ctx-supercharge-dark-after.png","Supercharge dark · before","Supercharge dark · after","Supercharge dark before: a near-black band on the page and the bento ground","Supercharge dark after: no band")}
    <ul class="facts">
      <li><span class="k">Legibility</span><span><b>The quiet tab labels still pass everywhere.</b> The lowest is on the light grey ground, 6.44 to 1; in dark the lowest is 7.18 to 1 (the labels are the softer #E1E1E1 at 72%).</span></li>
      <li><span class="k">The More menu</span><span>The overflow menu that drops from the strip keeps its own surface, as before.</span></li>
      <li><span class="k">Found on the way</span><span><b>The inactive tab's stored grey had to follow the softer white.</b> The tab labels you see are the text ink at 72%, so they softened with it. But the library also stores a plain grey for tools that cannot do transparency, and it was worked out from white: #B7B7B7. It is now #9D9D9D, the step that keeps the same share of the new ink (6.42 to 1 on the page). To make it land on that step, its stored fade moves from 70% to 67%. Nothing on screen paints this grey, but the 70% was set when you ruled the tab states, so say if you want it otherwise. Common's inactive tab was white in dark and now follows its text to #E1E1E1.</span></li>
    </ul>
    {call("strip","2. The tab strip, built","Does it stand?","",STAND)}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Built at the source: <code>tabs/background</code> aliases <code>surface/transparent</code> in both modes (was <code>surface/raised</code>). The three canon scopes that paint it (<code>.cn-tabs</code>, <code>.cn-page-header-lockup</code>, <code>.cn-template-detail</code>) now paint nothing; the Supercharge and grey-tile option blocks drop their <code>--tabs-background</code> lines. <code>tabs/overflow-background</code> is unchanged.</li>
      <li>Contrast pairs re-pointed: Tabs' manifest measures its text, underline and focus ring against <code>background/default</code>, <code>surface/section</code> and <code>surface/raised</code> (the grounds it sits on) instead of <code>tabs/background</code>; Page header's underline against <code>background/default</code> (its text pair on the page was already there). <code>_validate_token_tiers.py</code> learns the new alias. Snippet gate 0 failures, fork-ban gate green, token tiers 0 strict failures.</li>
      <li>Measured, from the renders (strip colour, the ground under it, the unselected label composited at its opacity, the underline):</li>
    </ol>
    {ctab_tabs()}
    <ol start="4"><li>Composition: <code>notes/_lanes/311/A/tabs-context.html</code>, copied from #310 lane B's, canon.css and type.css linked as the demo links them, the real Tabs markup inside <code>.cn-tabs</code>, tiles as <code>.c-bento__tile.dashboard-tile</code>. Driver <code>render_311A.py tabs</code>, facts <code>img/facts-tabs.json</code>.</li></ol>
    </details>
  </div>
</section>

<section id="scpage">
  <div class="wrap">
    <p class="label">03 · Supercharge's dark page · pictures only, nothing built · call</p>
    <h2>Supercharge's dark page is a plain grey, #1A1A1A, by accident, and its section ground already swallows the tiles.</h2>
    <p class="lead">Supercharge was meant to carry its own warm darks, but the generator fixes its dark page to Mono's #1A1A1A. Fixing the generator as it stands would put the page on #13110E, the same colour as the tile, so tiles placed straight on the page would vanish. Its section background is #13110E already, so tiles vanish there today: see (d) in the first picture.</p>
    <p>Three readings on the same four grounds. The banking demo is not affected by this: its whole page is the bento ground, #2A2621.</p>
    {one("03-sc-warm4-25211C-ctx.png","Its own one step up · page and section warm/4 #25211C · (the recommendation)","Supercharge dark with the page and section at #25211C: tiles stand out on both")}
    {one("03-sc-fix-13110E-ctx.png","The generator fixed as it stands · page #13110E","Supercharge dark with the page at #13110E: the page, the section and the tiles are all one colour")}
    {one("03-sc-asis-ctx.png","As it is · page #1A1A1A, section #13110E","Supercharge dark as it is: a neutral grey page, and tiles lost on the section background")}
    <ul class="facts">
      <li><span class="k">Why warm/4</span><span><b>It mirrors Mono.</b> In Mono the tile is the darkest (#000) and the page one step up (#1A1A1A); in Supercharge the tile is its darkest (#13110E) and warm/4 is the step up. Tiles separate from the page and the section by 1.18 to 1, close to Mono's 1.21. Text on the page reads 14.8 to 1.</span></li>
      <li><span class="k">One thing to know</span><span>warm/4 is also the interim pressed and active tile colour you set this afternoon, pending your Figma specs, so a pressed tile would match the page until those arrive.</span></li>
    </ul>
    {call("scpage","3. Supercharge's dark page","What should Supercharge's dark page and section be?","Recommendation: its own one step up, warm/4 #25211C, for the page and the section, because tiles then stand out on both, as they do in Mono. Nothing is built until you say.",
      [(SC_REC,"warm/4 #25211C, page and section (the recommendation)"),("Fix the generator as it stands: page #13110E, the same as the tile","#13110E, the same as the tile"),("Leave it at #1A1A1A","Leave it at #1A1A1A"),("Something else, say below","Something else, say below")],SC_REC)}
    <details class="tech"><summary>Technical</summary><ol>
      <li>The cause: <code>knowledge/canon/gen_theme_cascade.py</code> <code>_expand_aliases</code> materialises <code>background/default</code> in the pass where only its light target (<code>color/neutral/15</code>) is overridden, fills dark from the Mono base before <code>surface/digital-black</code> has expanded, and never revisits it. So Supercharge dark reads #1A1A1A while its own digital black is #13110E.</li>
      <li><code>surface/section</code> dark aliases <code>color/neutral/4</code>, which Supercharge binds to warm/2 #13110E, the same as the s310-D4 tile. <code>surface/digital-black</code>'s note says "SC dark page = warm/4", written before the anchor moved to warm/2.</li>
      <li>How these were drawn: a scratch style on the page only sets <code>--background-default</code>, <code>--page</code>, <code>--nav-page</code> and <code>--surface-section</code> with <code>!important</code> (Supercharge's dark block out-specifies a plain override). Nothing in the library is changed. Building the recommendation would be the generator fix plus Supercharge overrides for <code>background/default</code> and <code>surface/section</code> dark at <code>color/warm/4</code>, then the full regen.</li>
    </ol>
    {ctab_sc()}
    </details>
  </div>
</section>

<section id="else" class="grey">
  <div class="wrap">
    <p class="label">04 · Anything else</p>
    <h2>Anything you want changed or looked at again.</h2>
    <div class="call" data-id="page" data-q="4. Note on the page" data-rec="">
      <p class="q">Anything else on this page?</p>
      <label class="field"><span>Your note</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>
  </div>
</section>

<footer><div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
  <span>Apollo · review page · The soft white and the tab strip, built · v1 · 2026-09-30 · session 311 lane A</span>
  <span>Neither build stands until you say.</span>
</div></footer>

<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your decisions</b><span id="count">0 of 4 answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>

'''
out=head+body+script
open(PAGE,'w').write(out)
print(len(out), body.count('<img'))
