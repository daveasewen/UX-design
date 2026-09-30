"""#310 lane B — builds notes/_REVIEW-310-B-white-ink-and-tab-strip-2026-09-30-v1.html from lane A's shell
(head styles and decision script, new KEY and PATH) and this lane's measured facts."""
import json, re, html
A=open('notes/_REVIEW-310-A-dark-tiles-2026-09-30-v1.html').read()
head=A[:A.index('<body')]
head=head.replace('<title>The dark tiles, built</title>','<title>White ink, tab strip</title>')
head=head.replace('</style>','''.ctab{width:100%;border-collapse:collapse;font-size:14px;line-height:1.45;margin:var(--s3) 0 var(--s2);min-width:720px}
.ctab th,.ctab td{text-align:left;padding:.55rem .6rem;border-bottom:1px solid var(--g3);vertical-align:top}
.ctab th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);font-weight:500}
.ctab td.n{font-variant-numeric:tabular-nums;white-space:nowrap}
.ctab tr.rec td{background:var(--g1)}
.scroll{overflow-x:auto;max-width:100%}
.quote{border-left:2px solid var(--accent);padding:.2rem 0 .2rem 1rem;margin:0 0 var(--s3);font-size:18px;font-weight:300;line-height:1.5;max-width:40em}
</style>''')
script=A[A.rindex('<script'):]
script=script.replace("review-310-A-dark-tiles-v1","review-310-B-white-ink-and-tab-strip-v1")
script=script.replace("notes/_REVIEW-310-A-dark-tiles-2026-09-30-v1.html","notes/_REVIEW-310-B-white-ink-and-tab-strip-2026-09-30-v1.html")
script=script.replace("Session 310 · The dark tiles, built · comments","Session 310 · White ink and the tab strip · comments")
script=script.replace("'5. Note on the page: '","'3. Note on the page: '")
script=script.replace("review-310-A-dark-tiles.txt","review-310-B-white-ink-and-tab-strip.txt")
assert "review-310-B-white-ink-and-tab-strip-v1" in script and "3. Note on the page" in script
F=json.load(open('notes/_lanes/310/B/img/ink-facts.json'))
I="_lanes/310/B/img/"
def img(f,alt): return f'<img src="{I}{f}" alt="{html.escape(alt)}">'
rows=[("1-as-built","1 · As built","black tile, white #FFFFFF text",False),
      ("2a-n13","2a · Softer white, step 13","black tile, #F0F0F0 text",False),
      ("2b-n12","2b · Softer white, step 12","black tile, #E1E1E1 text",True),
      ("3-grey-tiles","3 · The reverse (your option)","grey #1F1F1F tile on a black ground, white text",False),
      ("4-n3-tile","4 · A near-black tile","#0F0F0F tile (ramp step 3), white text",False)]
def ctab():
    h='<div class="scroll"><table class="ctab"><thead><tr><th>Option</th><th>Tile</th><th>Main text</th><th>Secondary text (60%)</th><th>Green ink</th><th>Red ink</th><th>Green mark</th><th>Red dot</th><th>Text on the ground</th><th>Tile against ground</th></tr></thead><tbody>'
    for k,t,d,rec in rows:
        f=F[k]
        h+=f'<tr class="{"rec" if rec else ""}"><td>{t}</td><td class="n">{f["tile"]}</td><td class="n">{f["body"]} · <b>{f["body_cr"]:.2f}</b></td><td class="n">{f["secondary_eff"]} · <b>{f["secondary_eff_cr"]:.2f}</b></td><td class="n">{f["succ_cr"]:.2f}</td><td class="n">{f["err_cr"]:.2f}</td><td class="n">{f["sg_cr"]:.2f}</td><td class="n">{f["eg_cr"]:.2f}</td><td class="n">{f["ground_text_cr"]:.2f}</td><td class="n">{f["tile_on_ground"]:.2f}</td></tr>'
    return h+'</tbody></table></div>'
ink_rows=''.join(f'<div class="row" role="row"><div class="k">{t}<small>{d}<br>main text {F[k]["body_cr"]:.2f} : 1<br>secondary {F[k]["secondary_eff_cr"]:.2f} : 1</small></div>{img("02-"+k+"-top.png", t+": the top of the banking demo, Console dark, 1440 wide")}</div>' for k,t,d,_ in rows)
crop_rows=''.join(f'<div class="row" role="row"><div class="k">{t}<small>4x: a metric and a payment row</small></div>{img("02-"+k+"-crop.png", t+": a metric and a payment row enlarged four times")}</div>' for k,t,d,_ in rows)
def pair(a,b,ca,cb,alta,altb):
    return f'<div class="pair"><figure><figcaption>{ca}</figcaption>{img(a,alta)}</figure><figure><figcaption>{cb}</figcaption>{img(b,altb)}</figure></div>'
def one(a,c,alt): return f'<div class="pair one"><figure><figcaption>{c}</figcaption>{img(a,alt)}</figure></div>'
body=f'''<body>
<a id="rv-back" href="../index.html" target="_self" style="position:fixed;top:12px;left:12px;z-index:2147483647;background:#000;color:#fff;font:500 13px/1 'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:.04em;padding:10px 14px;text-decoration:none;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.25)">&larr; All review pages</a>

<nav class="toc" aria-label="Sections"><div class="wrap">
  <a href="#pressed">The pressed value</a>
  <a href="#ink">The white ink</a>
  <a href="#strip">The tab strip</a>
  <a href="#else">Anything else</a>
</div></nav>

<header id="top">
  <div class="wrap grid">
    <div>
      <p class="label">Session 310 · review page · White ink and the tab strip</p>
      <h1>Two calls: how white the text on black tiles should be, and whether the tab strip draws a band.</h1>
      <p class="sub">The pressed value is in and needs only a look. Then the white ink options, alive on the banking demo and measured, and the tab strip placed on every kind of ground Apollo composes, in light and dark.</p>
    </div>
    <div class="meta">
      <span>Wednesday 30 September 2026</span>
      <span>For your 16:24 answers to the dark tiles page, items 1, 2 and 3.</span>
      <span>Every picture is a fresh render at the seat from the tree as it stands. The options are shown live on the page, nothing in the library is changed for them.</span>
    </div>
  </div>
</header>

<section id="pressed">
  <div class="wrap">
    <p class="label">01 · The pressed value · done, look</p>
    <h2>A pressed or active Supercharge tile now shows, one step lighter than rest.</h2>
    <p class="quote">"lets do that for now, I have some proper specs for this but cant access the figma files at teh moment"</p>
    <p class="lead">Pressed and active move from #13110E, which had become the resting colour, to #25211C in dark. Light is unchanged. The token source says in its own note that this value is interim until your Figma specs replace it.</p>
    {one("01-sc-tile-states.png","Supercharge dark · rest, hover, pressed, active, page · before and after","Swatches: before, pressed and active equal rest at #13110E; after, pressed and active are #25211C")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Built at the source, not canon.css by hand: <code>knowledge/tokens/themes/apollo-supercharge.overrides.json</code> gains <code>tertiary/background/pressed</code> and <code>tertiary/background/active</code>, dark <code>color/warm/4</code> #25211C, light restating what Supercharge rendered (#493F39, #000000) because a per-mode override falls back to the Mono base. Each entry's note carries your words and the INTERIM marker; the s310-D4 note points at them.</li>
      <li>Regenerated in order: gen_canon_tokens, gen_snippet_tokens (0 projected), gen_token_ramp (0), gen_canon_components (no change), gen_theme_cascade, gen_showroom (12 pages). canon.css moves only the Supercharge dark pressed and active values and the component-tier literals that bake them. Dark-mode and icon-contrast audits unchanged.</li>
      <li>Measured after: rest #13110E, hover #2E2A25, pressed #25211C, active #25211C, page #1A1A1A. Commit 896b2b0e; s310-D5 stamped enacted with that sha.</li>
      <li>Driver: <code>notes/_lanes/310/B/render_states.py</code> (lane A's swatch page, before = canon.css at HEAD before the change).</li>
    </ol></details>
  </div>
</section>

<section id="ink" class="grey">
  <div class="wrap">
    <p class="label">02 · The white ink on black tiles · call</p>
    <h2>A softer white keeps your black tiles and takes the edge off. The reverse moves the glare to the header.</h2>
    <p class="quote">"we can avoid halation by choosing a different white ink maybe, of maybe we reverse the decision, I think we need a review of the options."</p>
    <p class="lead">Five options, each live on the top of the banking demo in Console dark at 1440, then the same metric and payment row enlarged four times. Every one passes contrast comfortably; the question is how far below the harshest possible edge, 21 to 1, to step.</p>
    <p>Halation is the glow a bright letter throws into a dark field. With astigmatism the eye focuses unevenly along different axes, so each bright stroke smears into the black around it, and a dark room widens the pupil, which makes it worse. The fix published dark themes use is to lower the brightest edge, either by softening the white or by lifting the black. Apollo already says this in its own words: the digital black note moves the page to #1A1A1A to bring white text down to 17.4 to 1 so it stops dancing.</p>
    <div class="agrid" role="table" aria-label="The top of the banking demo in Console dark under five white ink options">
      <div class="hd" role="row"><span>Option</span><span>Console dark · 1440</span></div>
      {ink_rows}
    </div>
    <div class="agrid" role="table" aria-label="Four times enlargements of a metric and a payment row under five options">
      <div class="hd" role="row"><span>Option</span><span>Enlarged four times (retina pixels, doubled)</span></div>
      {crop_rows}
    </div>
    <p>Measured on the tile, as WCAG ratios. Secondary text in this demo is the same ink at 60% (labels, "vs July", the chart title), so it is measured as it lands on the tile. It must reach 4.5 to 1 at its 12 px size; the lowest here is 5.85 to 1.</p>
    {ctab()}
    <ul class="facts">
      <li><span class="k">2b, the pick</span><span><b>#E1E1E1 is step 12 of Apollo's own grey ramp.</b> It brings the edge to 16 to 1, just under the 17.4 the digital black note asks for, and it is the same value Material's dark theme reaches with its 87% white. Secondary text stays at 5.85 to 1. The tiles stay black, as you chose them.</span></li>
      <li><span class="k">2a</span><span><b>#F0F0F0, step 13,</b> is gentler (18.4 to 1) but stays above the note's 17.4.</span></li>
      <li><span class="k">3, the reverse</span><span><b>Grey tiles on black</b> bring the tile text to 16.5 to 1, but the page ground turns black, so the header and anything else on the ground sit white on pure black at 21 to 1. The red status dot drops to 2.74 to 1 on the grey tile, under 3 to 1 (its label carries the meaning, as your roundel rule allows).</span></li>
      <li><span class="k">4</span><span><b>A #0F0F0F tile</b> is on the ramp and softens the edge to 19.2 to 1, but the tile separates less from its ground (1.16 against 1.27), which is what the black was for.</span></li>
      <li><span class="k">Supercharge</span><span>Already runs a softer white, #F7F6F4, on its #13110E tile (17.45 to 1). Recommend it keeps that ink rather than follow step 12 down its warm ramp (#CDC8C6, 11.4 to 1).</span></li>
    </ul>
    <div class="call" data-id="ink" data-q="1. The white ink on black tiles" data-rec="2b: text #E1E1E1 on black tiles (Mono, Console, Common); Supercharge keeps #F7F6F4">
      <p class="q">Which white should text be on the black tiles?</p>
      <p class="rec">Recommendation: 2b, #E1E1E1, because it keeps your black tiles and brings the edge under the digital black note's own 17.4 to 1 with every secondary line still passing. Supercharge keeps its #F7F6F4. Nothing is changed until you say.</p>
      <div class="chips">
        <button type="button" class="chip" data-v="2b: text #E1E1E1 on black tiles (Mono, Console, Common); Supercharge keeps #F7F6F4">2b · #E1E1E1 on black<em>recommended</em></button>
        <button type="button" class="chip" data-v="2a: text #F0F0F0 on black tiles">2a · #F0F0F0 on black</button>
        <button type="button" class="chip" data-v="3: reverse it, grey tiles on a black ground">3 · Reverse, grey tiles</button>
        <button type="button" class="chip" data-v="4: #0F0F0F tiles, white text">4 · #0F0F0F tiles</button>
        <button type="button" class="chip" data-v="Keep as built, white on black">Keep as built</button>
        <button type="button" class="chip" data-v="Something else, say below">Something else, say below</button>
      </div>
      <label class="field"><span>Your comment</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>
    <details class="tech"><summary>Technical</summary><ol>
      <li>How each option is shown: the live tree, with CSS custom properties set on the page only. Ink options set <code>--text-default</code> and <code>--text-secondary</code> on every dark element (the token a ruling would move: <code>text/default</code> and <code>text/secondary</code> dark, both <code>color/neutral/15</code> today). Option 3 is your registered <code>data-dark-tiles="grey"</code>. Option 4 sets the tile surfaces to <code>color/neutral/3</code> #0F0F0F. Driver <code>notes/_lanes/310/B/render_ink.py</code>, measurements in <code>img/ink-facts.json</code> (computed colours, opacity composited onto the tile).</li>
      <li>What the RAG inks are on this demo: the green up-arrow is <code>--rag-success-ink</code> #66CC8D; the status dots are the glyph colours (#5DAC7B green, #D5990B amber, #B92F1E red) beside a text label. The red ink #F6604C is not drawn on the tiles today; it is measured as a token.</li>
      <li>Building 2b would be one alias per mode in <code>knowledge/tokens/semantic-colour.json</code> (<code>text/default</code>, <code>text/secondary</code> dark to <code>color/neutral/12</code>) plus a Supercharge override pinning <code>color/warm/15</code>, then the full regen and the state-contrast sweep. It touches every dark text, not only tiles: text on the #1F1F1F ground goes from 16.5 to 12.6 to 1.</li>
      <li>Desk research, read 2026-09-30. Google, Material Design dark theme codelab (codelabs.developers.google.com/codelabs/design-material-darktheme): dark surfaces are #121212 not black, and "pure #FFFFFF text against a dark background can harm legibility since the light from that text appears to bleed or blur"; high-emphasis text is 87% white, medium 60%, disabled 38%. Level Access, "Accessibility for people with astigmatism" (levelaccess.com/blog/accessibility-for-people-with-astigmatism): almost half the population has at least 0.5 D of astigmatism; white on pure black produces a "fuzzing effect"; advice is to "avoid using white text on pure black backgrounds", which contrast checkers do not flag because it passes WCAG. Diana, a11ywithdiana on Substack, "What science says about black and white combinations in UI design": halation is stronger with astigmatism, small type and dim rooms; suggests pairs such as #EAEAEA on #121212 and #F1F1F1 on #1E1E1E.</li>
      <li>Counterpoint, not re-read today: Apple's dark mode starts from a true black base for OLED screens with white primary labels (Human Interface Guidelines, Dark Mode, named from a search listing). So pure black is a real published choice; the softening is carried by the ink.</li>
      <li>Apollo's own record: <code>surface/digital-black</code>'s note in <code>semantic-colour.json</code> ("#000 maximises the luminance step against white (21:1), which drives halation... #1A1A1A cuts that step ~17% to 17.4:1").</li>
      <li>Not fixed: two dropdown chevrons in the demo paint a literal white, so they would not follow a softer ink.</li>
    </ol></details>
  </div>
</section>

<section id="strip">
  <div class="wrap">
    <p class="label">03 · The tab strip in context · call</p>
    <h2>The strip is painted as a tile, so it bands wherever it sits on anything else, in light too.</h2>
    <p class="quote">"I need to see this, it gets complicated when we have page backgrounds and bento sections"</p>
    <p class="lead">The strip's colour is the tile colour: white in light, black in dark. Light looked right only because its page is also white. On a grey bento ground or a grey section, light draws a white bar exactly as dark draws a black one. Letting the strip take whatever it sits on removes the band everywhere; the track line and the underline still mark it.</p>
    <p>Four grounds, composed the way the banking demo composes: (a) the page, (b) a bento section on the demo's grey ground, (c) inside a tile, (d) a section background, the one Template-dashboard-bento uses. Left is as built, right is the strip taking its container's colour.</p>
    {pair("03-ctx-console-light-built.png","03-ctx-console-light-container.png","Console light · as built","Console light · takes its container","Light, as built: the strip is invisible on the white page and inside the tile, a white bar on the grey grounds","Light, container: no bar on any ground")}
    {pair("03-ctx-console-dark-built.png","03-ctx-console-dark-container.png","Console dark · as built","Console dark · takes its container","Dark, as built: a black band on the page, the bento ground and the section; invisible only inside the tile","Dark, container: no band on any ground")}
    {pair("03-ctx-supercharge-dark-built.png","03-ctx-supercharge-dark-container.png","Supercharge dark · as built","Supercharge dark · takes its container","Supercharge dark, as built: a near-black band on the page and bento ground","Supercharge dark, container: no band")}
    <p>The two real templates that carry the strip, as their reference pages stand (Mono dark): top as built, bottom taking its container.</p>
    {one("03-real-Template-detail-dark.png","Template-detail · dark · as built above, container below","Template-detail in dark: above, a black band behind the tabs on the page; below, the tabs sit on the page with only the track line")}
    {one("03-real-Page-header-lockup-dark.png","Page-header-lockup · dark · as built above, container below","Page header lockup in dark: above, a black band behind the tabs; below, no band")}
    <p>A third reading, a band only when the strip sits on a different surface than its panel, collapses into the second everywhere Apollo composes tabs today: in every template and context found, the panel sits on the same ground as the strip. It would only differ for a tab strip fused to the top of a card, which no snippet draws. So it is not shown.</p>
    <div class="call" data-id="strip" data-q="2. The tab strip's colour" data-rec="The strip takes its container's colour in both modes">
      <p class="q">Should the tab strip take the colour of whatever it sits on, in both modes?</p>
      <p class="rec">Recommendation: yes, in both modes, because it then never draws a band on any page, bento or section ground, and light and dark read the same. It changes light on grey grounds too (the white bar goes). Nothing is changed until you say.</p>
      <div class="chips">
        <button type="button" class="chip" data-v="The strip takes its container's colour in both modes">Takes its container, both modes<em>recommended</em></button>
        <button type="button" class="chip" data-v="Takes its container in dark only; light stays as it is">Dark only</button>
        <button type="button" class="chip" data-v="Keep the band as built">Keep the band</button>
        <button type="button" class="chip" data-v="Something else, say below">Something else, say below</button>
      </div>
      <label class="field"><span>Your comment</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>
    <details class="tech"><summary>Technical</summary><ol>
      <li>Where the band comes from: <code>tabs/background</code> aliases <code>surface/raised</code> (dark #000000 since s310-D3). Three canon scopes paint it: <code>.cn-tabs</code>, <code>.cn-page-header-lockup</code> and <code>.cn-template-detail</code>, each <code>.tablist{{background:var(--tabs-background)}}</code>.</li>
      <li>Measured strip and ground, Console dark as built: (a) #000 on page #1A1A1A, (b) #000 on #1F1F1F, (c) #000 on tile #000, (d) #000 on section #1A1A1A. Console light: (a) #FFF on #FFF, (b) #FFF on #F0F0F0, (c) #FFF on #FFF, (d) #FFF on #F0F0F0. Facts in <code>notes/_lanes/310/B/img/tabs-facts.json</code>.</li>
      <li>Composition: <code>notes/_lanes/310/B/tabs-context.html</code>, canon.css and type.css as the demo links them, Tabs markup from <code>knowledge/snippets/Tabs.reference.html</code> inside <code>.cn-tabs</code>, tiles as <code>.c-bento__tile.dashboard-tile</code> with the demo's own tile rules; grounds bound to <code>--background-default</code>, <code>--surface-subtle</code>, <code>--surface-section</code>. A few lines of script place the underline, which Tabs' own script does in the snippet. The two real templates are <code>knowledge/snippets/Template-detail.reference.html</code> and <code>Page-header-lockup.reference.html</code>, rendered as they stand in Mono (their native form). Drivers <code>render_tabs.py</code>, <code>render_real.py</code>. The container reading sets <code>--tabs-background: transparent</code> on the page only.</li>
      <li>Building it would re-alias <code>tabs/background</code> to <code>surface/transparent</code> in both modes, then regen. The Tabs manifest measures its text, underline and focus ring against <code>tabs/background</code>; with a transparent strip those pairs must be measured against the ground the strip sits on (the state-contrast sweep reads them). Tab labels at 72% on the lightest ground (#F0F0F0) measure 6.44 to 1. <code>tabs/overflow-background</code> (the More menu) stays a surface.</li>
    </ol></details>
  </div>
</section>

<section id="else" class="grey">
  <div class="wrap">
    <p class="label">04 · Anything else</p>
    <h2>One more thing the pictures turned up.</h2>
    <ul class="facts">
      <li><span class="k">Supercharge sections</span><span><b>In Supercharge dark, tiles vanish on a section background.</b> The section ground (<code>surface/section</code>, which follows the warm ramp's darkest) and the new tile are both #13110E. See picture (d) in the Supercharge pair above. Not changed here; it sits with lane A's open point that Supercharge's dark page is #1A1A1A rather than its own darkest.</span></li>
      <li><span class="k">Grey tiles, small things</span><span>With the reverse on, the avatar disc behind initials sits at 1.03 to 1 on the grey tile, so it disappears; the initials themselves stay legible.</span></li>
    </ul>
    <div class="call" data-id="page" data-q="3. Note on the page" data-rec="">
      <p class="q">Anything else on this page?</p>
      <label class="field"><span>Your note</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>
  </div>
</section>

<footer><div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
  <span>Apollo · review page · White ink and the tab strip · v1 · 2026-09-30 · session 310 lane B</span>
  <span>Nothing here is decided until you choose.</span>
</div></footer>

<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your decisions</b><span id="count">0 of 3 answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>

'''
open('notes/_REVIEW-310-B-white-ink-and-tab-strip-2026-09-30-v1.html','w').write(head+body+script)
print(len(head+body+script), (head+body).count('<img'))
