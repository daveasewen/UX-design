"""#311 lane B — builds notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html from lane A's shell
(head styles and decision script, NEW key and path) and this lane's measured facts (img/facts-*.json)."""
import json, html
SRC='notes/_REVIEW-311-A-soft-white-and-tab-strip-2026-09-30-v1.html'
PAGE='notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html'
A=open(SRC).read()
head=A[:A.index('<body')].replace('<title>Soft white, tab strip</title>','<title>Icons, Supercharge page</title>')
assert '<title>Icons, Supercharge page</title>' in head
script=A[A.rindex('<script'):]
for a,b in [("review-311-A-soft-white-and-tab-strip-v1","review-311-B-icons-and-supercharge-page-v1"),
            ("notes/_REVIEW-311-A-soft-white-and-tab-strip-2026-09-30-v1.html",PAGE),
            ("Session 311 · The soft white and the tab strip, built · comments","Session 311 · The icons and Supercharge\\'s dark page, built · comments"),
            ("'4. Note on the page: '","'3. Note on the page: '"),
            ("review-311-A-soft-white-and-tab-strip.txt","review-311-B-icons-and-supercharge-page.txt")]:
    assert a in script, a; script=script.replace(a,b)
FC=json.load(open('notes/_lanes/311/B/img/facts-count.json')); FS=json.load(open('notes/_lanes/311/B/img/facts-scpage.json'))
def L(h):
    r=[int(h[i:i+2],16)/255 for i in (1,3,5)]; r=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in r]; return .2126*r[0]+.7152*r[1]+.0722*r[2]
def cr(a,b): x,y=L(a),L(b); return (max(x,y)+.05)/(min(x,y)+.05)
I="_lanes/311/B/img/"
def img(f,alt): return f'<img src="{I}{f}" alt="{html.escape(alt)}">'
def pair(a,b,ca,cb,alta,altb): return f'<div class="pair"><figure><figcaption>{ca}</figcaption>{img(a,alta)}</figure><figure><figcaption>{cb}</figcaption>{img(b,altb)}</figure></div>'
def one(a,c,alt): return f'<div class="pair one"><figure><figcaption>{c}</figcaption>{img(a,alt)}</figure></div>'
def f2(x): return f"{x:.2f}"
TH=[("mono","Mono"),("console","Console"),("common","Common"),("supercharge","Supercharge")]
def ctab_icons():
    h='<div class="scroll"><table class="ctab"><thead><tr><th>Theme, dark</th><th>Icons drawn</th><th>Pure white before</th><th>Pure white after</th><th>Header glass before → after</th><th>Toolbar glass before → after</th><th>Text ink</th></tr></thead><tbody>'
    for k,n in TH:
        b,a=FC[k+"-before"],FC[k+"-after"]
        hg=lambda f,x: f'{f[x]["icon"]} · {f2(f[x]["icon_cr"])}'
        h+=(f'<tr><td>{n}</td><td class="n">{a["icons"]}</td><td class="n">{b["white"]}</td><td class="n">{a["white"]}</td>'
            f'<td class="n">{hg(b,"header_glass")} → {hg(a,"header_glass")}</td><td class="n">{hg(b,"toolbar_glass")} → {hg(a,"toolbar_glass")}</td><td class="n">{a["text_default"].upper()}</td></tr>')
    return h+'</tbody></table></div>'
def ctab_sc():
    h='<div class="scroll"><table class="ctab"><thead><tr><th>Supercharge dark</th><th>Page</th><th>Section</th><th>Tile</th><th>Header band</th><th>Tile on page</th><th>Tile on section</th><th>Text on page</th><th>Text on tile</th></tr></thead><tbody>'
    for k,n in (("before","Before"),("after","After")):
        f=FS[k]; rc=' class="rec"' if k=="after" else ''
        h+=(f'<tr{rc}><td>{n}</td><td class="n">{f["page"]}</td><td class="n">{f["section"]}</td><td class="n">{f["tile"]}</td><td class="n">{f["nav"]}</td>'
            f'<td class="n">{f2(f["tile_on_page"])}</td><td class="n">{f2(f["tile_on_section"])}</td><td class="n">{f2(f["ink_on_page"])}</td><td class="n">{f2(f["ink_on_tile"])}</td></tr>')
    return h+'</tbody></table></div>'
C=FC["console-after"]; Cb=FC["console-before"]; B,S=FS["before"],FS["after"]
grey_opt=cr("#2A2621","#25211C")
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
body=f'''<body>
<a id="rv-back" href="../index.html" target="_self" style="position:fixed;top:12px;left:12px;z-index:2147483647;background:#000;color:#fff;font:500 13px/1 'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:.04em;padding:10px 14px;text-decoration:none;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.25)">&larr; All review pages</a>

<nav class="toc" aria-label="Sections"><div class="wrap">
  <a href="#icons">The icons</a>
  <a href="#scpage">Supercharge's dark page</a>
  <a href="#else">Anything else</a>
</div></nav>

<header id="top">
  <div class="wrap grid">
    <div>
      <p class="label">Session 311 · review page · The icons and Supercharge's dark page, built</p>
      <h1>Both of your 20:30 answers are built. Here they are, before and after, so you can say whether they stand.</h1>
      <p class="sub">In dark, the icons now take the same soft white as the text beside them. And Supercharge's dark page and section are its own warm/4, one step up from its tiles, so the tiles stand out on both.</p>
    </div>
    <div class="meta">
      <span>Wednesday 30 September 2026</span>
      <span>Before is the library as it stood when you answered; after is the library as built now.</span>
      <span>Neither counts as done until you say it stands.</span>
    </div>
  </div>
</header>

<section id="icons">
  <div class="wrap">
    <p class="label">01 · The icons follow the ink · built, does it stand?</p>
    <h2>In dark, the icons are now #E1E1E1, the same as the text, in Mono, Console and Common. Supercharge's stay its #F7F6F4.</h2>
    <p class="quote">"the icons should follow the ink colour"</p>
    <p class="lead">On the banking demo two icons were still pure white: the search glass in the header search bar and the one in the payments toolbar. Both now match the text. Pure white icons on the demo: {Cb["white"]} before, {C["white"]} after, in each of the three themes. Supercharge's icons were already its own #F7F6F4 and have not moved.</p>
    <p>The top of the banking demo at 1440, Console dark, with the header search bar open. Left is before, right is after.</p>
    {pair("01-console-before-top.png","01-console-after-top.png","Console dark · before, glass #FFFFFF","Console dark · after, glass #E1E1E1","The top of the banking demo in Console dark before: the two search glasses are pure white","The top of the banking demo in Console dark after: the two search glasses match the text")}
    <p>The two search glasses next to their words, enlarged four times. Top is the header search bar, bottom is the payments toolbar.</p>
    {one("01-crop-console-4x.png","Console dark · enlarged four times · before left, after right","Two search fields enlarged four times in Console dark: left the glass is white, right it is #E1E1E1")}
    <p>Mono and Common move the same way: the same two glasses, #FFFFFF to #E1E1E1, {FC["mono-before"]["white"]} to {FC["mono-after"]["white"]} in Mono and {FC["common-before"]["white"]} to {FC["common-after"]["white"]} in Common (measured, not pictured, because the pictures look the same as Console's).</p>
    <ul class="facts">
      <li><span class="k">The hint text</span><span>The words in a search box are a hint, drawn at about half strength on purpose, so the glass still reads a little brighter than them. It now matches full-strength text, such as the labels and figures.</span></li>
      <li><span class="k">What did not move</span><span><b>Icons that carry a status or a brand colour stay as they were:</b> the green and red trend arrows, the white icon on Common's red button, and the white status roundels in dark error and success messages (your 2 July rule: white shape, black mark). Say if you want those to follow too.</span></li>
      <li><span class="k">Found on the way</span><span>The two buttons at the top right of the demo's header show as small light boxes with no icon in them, before and after. The demo's header buttons are missing the class that sizes their icons, so the search and account icons are never drawn. Not fixed here.</span></li>
    </ul>
    {call("icons","1. The icons follow the ink, built","Does it stand?","",STAND)}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Built at the source, not canon.css by hand: <code>knowledge/tokens/semantic-colour.json</code> <code>icon/default</code> dark aliases <code>color/neutral/12</code> #E1E1E1 (was <code>color/neutral/15</code> #FFFFFF), with a note quoting the ruling. Supercharge's DNA tier would have rebound that to warm/12 #CDC8C6, so <code>themes/apollo-supercharge.overrides.json</code> pins <code>icon/default</code> to warm/15 #F7F6F4 dark (light restated warm/2 #13110E), the same as its <code>text/default</code>.</li>
      <li>Everything painting <code>--icon</code> / <code>--nav-icon</code> follows by projection (they bind <code>icon/default</code>). Not moved, by scope: <code>icon/default-reverse</code>, <code>icon/on-inverse</code>, <code>--pri-icon</code> and <code>--pri-glyph</code> (icons on the primary and red fills), <code>button/primary/icon/default</code> in Common, and the hard-coded dark RAG roundel rule <code>.ic{{color:#FFFFFF}}</code> in Notifications, Input fields, Amount input, Combobox, Date picker, Date range picker, File upload, Form layout and Multi-select.</li>
      <li>canon.css, compared line by line with the tree before this lane: outside Supercharge the one line that changed is <code>--icon-default: #FFFFFF</code> → <code>#E1E1E1</code> in the base dark block. Console and Common inherit it; neither overrides <code>icon/default</code>.</li>
      <li>Counted on the banking demo in dark, with the header search bar opened (an icon = a drawn <code>&lt;svg&gt;</code> outside the chart canvas; pure white = a shape in it filled or stroked #FFFFFF); contrast is against the ground the glass sits on:</li>
    </ol>
    {ctab_icons()}
    <ol start="5">
      <li>Regenerated in order: gen_canon_tokens, gen_snippet_tokens, gen_token_ramp, gen_canon_components, gen_theme_cascade, gen_showroom; dark-mode, text/icon, indicator contrast audits and the icon contrast delta rebuilt. Gates at the seat: snippets 0 failures, token tiers 0 strict, state-snap OK, dark surfaces 0, forks green, coverage 0, every generator check in sync. The icon contrast delta (advisory, every icon against every surface) now lists 44 exhaustive combinations under 4.5 (was 46); the declared dead-zone count stays 0.</li>
      <li>Driver <code>notes/_lanes/311/B/render_311B.py count|icons</code> (before = canon.css at 84bd8c93 served to a copy of the demo; after = the tree), facts <code>img/facts-count.json</code>.</li>
    </ol>
    </details>
  </div>
</section>

<section id="scpage" class="grey">
  <div class="wrap">
    <p class="label">02 · Supercharge's dark page · built, does it stand?</p>
    <h2>Supercharge's dark page and section are now warm/4 #25211C. The tile stays #13110E, one step below.</h2>
    <p class="quote">"Supercharge's dark page and section take warm/4 #25211C, one step up from its tile"</p>
    <p class="lead">Tiles now stand out on the page and on a section background by {f2(S["tile_on_page"])} to 1, as they do in Mono. Before, they sat {f2(B["tile_on_page"])} to 1 on a plain grey page and disappeared into the section ({f2(B["tile_on_section"])} to 1). Text on the page reads {f2(S["ink_on_page"])} to 1.</p>
    <p>A Supercharge page at 1440, dark, built from the banking demo's own header, title and metric tiles: first straight on the page, then on a section background.</p>
    {one("02-sc-before.png","Before · page #1A1A1A, section #13110E","Supercharge dark before: a neutral grey page, and on the section the tiles run together with the ground")}
    {one("02-sc-after.png","After · page and section warm/4 #25211C","Supercharge dark after: a warm page and section, with the tiles separate on both")}
    <ul class="facts">
      <li><span class="k">What moves with it</span><span><b>Everything in Supercharge dark that paints the page colour follows it:</b> menus, table cells, panels, search and field boxes, the QR code plate. On the banking demo that shows as the search box in the payments tile, now #25211C instead of #1A1A1A.</span></li>
      <li><span class="k">The header band</span><span>The header band stays #13110E, the tile colour, so it now sits a step darker than the page below it (you can see it in the after picture).</span></li>
      <li><span class="k">Other themes</span><span>Nothing moves in Mono, Console or Common. The library's style sheet was compared line by line.</span></li>
      <li><span class="k">One thing to know</span><span>warm/4 is also the interim pressed and active tile, so a pressed tile matches the page until your Figma specs arrive.</span></li>
      <li><span class="k">Grey tiles option</span><span>With the grey-tile option switched on in Supercharge, the tiles are #2A2621 on this page, only {f2(grey_opt)} to 1 apart. Not changed here; say if the option should be looked at.</span></li>
    </ul>
    {call("scpage","2. Supercharge's dark page, built","Does it stand?","",STAND)}
    <details class="tech"><summary>Technical</summary><ol>
      <li>The cause, fixed at its source: <code>knowledge/canon/gen_theme_cascade.py</code> <code>_expand_aliases</code> skipped any path already written (<code>if path in ov: continue</code>), so <code>background/default</code>, written in the pass where only its light target was overridden, kept the Mono base #1A1A1A for dark and was never revisited once <code>surface/digital-black</code> expanded. It now skips only the theme's own overrides and re-derives expanded paths until the fixed point. The generator's selftest gains a probe (a theme overriding only the two ladder steps must reach both legs of <code>background/default</code>); with the old line put back the selftest fails, so the clause is load-bearing. On its own the fix gives Supercharge's page #13110E, the tile colour.</li>
      <li>The ruling, in <code>themes/apollo-supercharge.overrides.json</code>: <code>background/default</code> and <code>surface/section</code> dark alias <code>color/warm/4</code> #25211C (light restated: warm/15 #F7F6F4 and warm/13 #DFDEDC, as rendered before). <code>surface/raised</code> dark stays warm/2 #13110E. The selftest checks both values. <code>surface/digital-black</code>'s note no longer says "SC dark page = warm/4": Supercharge's digital black is warm/2 #13110E, and its page is <code>background/default</code>, pinned by this ruling.</li>
      <li>canon.css, Supercharge block, 167 lines, all dark: <code>--background-default</code> and <code>--surface-section</code> → #25211C, and the component seats that project the page: <code>--page</code> ×135, <code>--menu-surface</code> ×10, <code>--cell</code> ×6, <code>--surface</code> ×4, <code>--nav-page</code> ×3, <code>--tbl-cell</code> ×2, <code>--panel</code>, <code>--pane</code>, <code>--stack-ring</code>, <code>--qr-plate-theme</code> (all #1A1A1A → #25211C), and Template-dashboard-bento's <code>--wall-ground</code> #13110E → #25211C. Supercharge light, Mono, Console, Common and the grey-tile option blocks: no change.</li>
      <li>Measured from the renders (WCAG):</li>
    </ol>
    {ctab_sc()}
    <ol start="5"><li>Composition: <code>notes/_lanes/311/B/sc-page.html</code>, the banking demo's masthead, page header and metric tiles copied verbatim, linked to the real canon.css with no overrides; the section is <code>--surface-section</code>, the tile <code>--surface-raised</code>. Driver <code>render_311B.py scpage</code>, facts <code>img/facts-scpage.json</code>.</li></ol>
    </details>
  </div>
</section>

<section id="else">
  <div class="wrap">
    <p class="label">03 · Anything else</p>
    <h2>Anything you want changed or looked at again.</h2>
    <div class="call" data-id="page" data-q="3. Note on the page" data-rec="">
      <p class="q">Anything else on this page?</p>
      <label class="field"><span>Your note</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>
  </div>
</section>

<footer><div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
  <span>Apollo · review page · The icons and Supercharge's dark page, built · v1 · 2026-09-30 · session 311 lane B</span>
  <span>Neither build stands until you say.</span>
</div></footer>

<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your decisions</b><span id="count">0 of 3 answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>

'''
out=head+body+script
open(PAGE,'w').write(out)
print(len(out), body.count('<img'))
