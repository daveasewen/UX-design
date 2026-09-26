"""Lane 304-M build: fill page.src.html -> notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html.
Sources 1-40 are parsed from lane G2's filed report (never retyped); 41-42 are this lane's.
The decisions overlay is copied from the house reference page and only its CFG is swapped."""
import html, os, re, sys

ROOT = os.getcwd()
HERE = os.path.join(ROOT, 'notes/_lanes/304/M')
SRC = os.path.join(HERE, 'page.src.html')
G2 = os.path.join(ROOT, 'notes/_subreports/2026-09-26-303-G2-agent-ui-landscape.md')
REF = os.path.join(ROOT, 'notes/_PROPOSAL-apollo-story-2026-09-20-v2.html')
OUT = os.path.join(ROOT, 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html')

RECHECKED = {3, 5, 6, 7, 12, 16, 17, 20}
NEW = [
    (41, 'MCP, "Extension Support Matrix" (client matrix)', 'https://modelcontextprotocol.io/extensions/client-matrix',
     'community-maintained, undated. Lists ChatGPT, Cursor and PostHog Code as MCP Apps hosts; extension id io.modelcontextprotocol/ui. Checked 26 Sept 2026.'),
    (42, 'MCP, "Enterprise-Managed Authorization" extension', 'https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization',
     'io.modelcontextprotocol/enterprise-managed-authorization; spec in ext-auth under specification/stable. Checked 26 Sept 2026.'),
]

def link_line(txt):
    out, pos = [], 0
    for m in re.finditer(r'https?://[^\s,]+', txt):
        out.append(html.escape(txt[pos:m.start()]))
        u = m.group(0)
        out.append('<a href="%s">%s</a>' % (html.escape(u, quote=True), html.escape(u)))
        pos = m.end()
    out.append(html.escape(txt[pos:]))
    return ''.join(out)

# ---- sources ---------------------------------------------------------
g2 = open(G2, encoding='utf-8').read()
sec = g2.split('## Sources', 1)[1]
items = []
for line in sec.splitlines():
    m = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
    if m:
        items.append((int(m.group(1)), m.group(2)))
nums = [n for n, _ in items]
assert nums == list(range(1, 41)), ('G2 sources not 1..40', nums)
lis = []
for n, t in items:
    extra = ' <span class="re">Re-checked 26 Sept 2026.</span>' if n in RECHECKED else ''
    lis.append('      <li value="%d">%s%s</li>' % (n, link_line(t), extra))
for n, title, url, note in NEW:
    lis.append('      <li value="%d">%s, <a href="%s">%s</a>, %s <span class="re">New.</span></li>'
               % (n, html.escape(title), url, html.escape(url), html.escape(note)))
sources_html = '    <ol class="src">\n' + '\n'.join(lis) + '\n    </ol>'

# ---- technical footer ------------------------------------------------
TECH = r'''
      <p><b>What this page is built from.</b> Lane G1, the GenUI archaeology and run-time reuse inventory: <code>notes/_subreports/2026-09-26-303-G1-genui-archaeology.md</code>. Lane G2, the agent-UI landscape with sources 1 to 40: <code>notes/_subreports/2026-09-26-303-G2-agent-ui-landscape.md</code>. The June note: <code>notes/_VISION-contextual-dashboard_2026-06-29.md</code>. North star and iteration machine: <code>notes/_VISION-northstar-front-end_2026-07-02.html</code>, <code>notes/_VISION-iteration-machine_2026-07-03.html</code>. Strategy lock: <code>archive/_SESSION-BRIEF-2026-06-20-strategy.md</code>. Gates as a service (14 July): <code>_retired/agent-memory-snapshot-2026-07-18/store/agentic-loop-gates-as-service.md</code> and <code>_LIVE-STATE.md</code> line 1343. The 19 September quote: <code>_HANDOFF-139</code> (session 288). His Friday and Saturday asks: <code>_HANDOFF-154-the-deck-was-finished-for-friday-and-apollo-mcp-was-asked-for.md</code>. "It can run hot": the retired memory note <code>iteration-machine-mock.md</code>, as G1 records it.</p>
      <p><b>Rulings and decisions referred to.</b> Jev dev-time only, 21 September: <code>s294-D10</code> in <code>knowledge/_rulings.json</code> (the rider keeps the option of full integration open). The selector as step 1 of generate-from-canon: <code>s277-D10</code>; its typed-question door: <code>s277-D13</code>. The chart renderer <code>window.dvRender(figureEl, spec)</code> in <code>knowledge/canon/dv-render.js</code>: <code>s249-D4</code>. Params, variants, slots: <code>s136-D1</code>. Architecture decisions: ADR-0002 (MCP for live tool and data access), ADR-0003, ADR-0006 (the flexing engine), ADR-0008 (Apollo is the canonical core; consumers by adapters), ADR-0015 (behaviour as light generated JS). Jev at compose time: <code>notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md</code>. The revisit triggers and "the one shared investment": the June note, last two sections.</p>
      <p><b>Counts this lane re-probed</b> at HEAD <code>571d458c</code>, 26 September 2026, read-only: <code>knowledge/components/*.meta.json</code> = 138; metas carrying <code>when</code> 39, <code>slots</code> 35, <code>answers</code> 26, <code>shape</code> 26, <code>provides</code> 108, <code>priority</code> 25. <code>showroom/index.json</code>: <code>$component_count</code> 137, <code>$foundation_count</code> 8, <code>$count</code> 145. <code>knowledge/snippets/*.reference.html</code> = 137, with 0 <code>&lt;template&gt;</code>, 0 <code>{{</code>, 0 <code>customElements.define</code>, 1 <code>data-slot</code>; folder 5.0 MB on disk. G1 reported 139 snippets: the folder also holds two <code>_REVIEW-66-*.html</code> files, which is the likely difference.</p>
      <p><b>Figures taken from G1 without re-measuring</b> (G1, HEAD <code>683f4cca</code>, 26 September 2026): <code>knowledge/_compose_slice.py</code> on "treasury dashboard showing cash position, payments awaiting approval and a balance trend" = 0.82 s, 115 KB JSON, 14 components including <code>Chart-candlestick</code>. <code>knowledge/_validate_screen.py</code> static steps on <code>knowledge/_fitness-test/nio-dash-console-v2.canon.html</code> = 0.68 s wall, PASS (receipt UNPROVEN:NO-RECEIPT, non-blocking); the <code>--render</code> state-contrast leg unmeasured. <code>knowledge/_build_kg_explorer.py</code> = 107 s, 4,888 nodes, 8,756 edges. <code>knowledge/shapes.json</code> 23 shapes; <code>knowledge/when-fields.json</code> 39 predicate fields; <code>knowledge/roles.json</code> 12 roles; <code>knowledge/chart-intents.json</code> 14 intents; <code>canon/canon.css</code> 1,022 custom properties, four themes; <code>_rulings.json</code> 638; <code>guidelines/_rules-index.json</code> 474; 51 <code>_validate_*.py</code>.</p>
      <p><b>Estimates.</b> The session counts on the build path are this lane's estimates, unmeasured, with no prior Apollo run-time work to calibrate against. Read them as order of size.</p>
      <p><b>Research re-check, 26 September 2026.</b> Opened again: a2ui.org home, catalogs, roadmap and "A2UI in the World"; Google's A2UI and MCP Apps post (17 June 2026); the MCP Apps overview; the MCP client matrix; mcpui.dev; the 2026-07-28 MCP spec post; the enterprise-managed authorization page. What moved is listed on the page under "Re-checked today". Not re-checked: sources 1, 2, 4, 8 to 11, 13 to 15, 18, 19, 21 to 40.</p>
      <p><b>This page.</b> Source template, build and render driver: <code>notes/_lanes/304/M/</code> (<code>page.src.html</code>, <code>build.py</code>, <code>render.py</code>); screenshots in <code>notes/_lanes/304/M/shots/</code>. Report: <code>notes/_subreports/2026-09-26-304-M-apollo-mcp-proposal.md</code>. The decisions overlay is copied from <code>notes/_PROPOSAL-apollo-story-2026-09-20-v2.html</code> with only its settings changed; it saves in this browser and exports markdown for <code>notes/_lanes/304/</code>.</p>'''

# ---- overlay: copy from the house page, swap only the CFG ------------
ref = open(REF, encoding='utf-8').read()
start = ref.index("<!-- ===== DAVE'S DECISIONS")
end = ref.index('</script>', start) + len('</script>')
ov = ref[start:end]
cfg_re = re.compile(r"var CFG = \{.*?\n  \};", re.S)
assert len(cfg_re.findall(ov)) == 1
NEWCFG = """var CFG = {
    page:'proposal-apollo-mcp-v1', title:'Apollo-MCP, proposal v1', path:'notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html',
    pageHost:'footer .wrap',
    targets:[
      { sel:'section[id]', kind:'Section', fallbackNum:'.label', title:'h2, .line', host:'.dd-host',
        skip:function(el){ return el.id==='tech' || el.id==='sources'; } },
      { sel:'.decide > li', kind:'Decision', title:'b', host:'div', prefix:'decision', count:true }
    ]
  };"""
ov = cfg_re.sub(lambda m: NEWCFG, ov)
ov = ov.replace('added #289', 'copied from the story proposal v2 (#289) at #304')
ov = ov.replace('drop it in notes/_lanes/289/', 'drop it in notes/_lanes/304/')
assert 'notes/_lanes/289' not in ov

page = open(SRC, encoding='utf-8').read()
for tok, val in (('<!--SOURCES-->', sources_html), ('<!--TECH-->', TECH), ('<!--OVERLAY-->', ov)):
    assert page.count(tok) == 1, tok
    page = page.replace(tok, val)
open(OUT, 'w', encoding='utf-8').write(page)
print('wrote', os.path.relpath(OUT, ROOT), len(page.encode('utf-8')), 'bytes;', len(lis), 'sources')
