"""Lane 304-M v2 build. Reuses build.py's logic unchanged (sources parsed from G2, overlay copied from
the house page) with v2 paths and a corrected Jev line, then inserts v1's CSS and diagram (step 1 relabelled)."""
import os, re
ROOT = os.getcwd()
HERE = os.path.join(ROOT, 'notes/_lanes/304/M')
V1SRC = open(os.path.join(HERE, 'page.src.html'), encoding='utf-8').read()

def rep(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)

def V2HOOK(page):
    css = V1SRC[V1SRC.index('<style>'):V1SRC.index('</style>') + len('</style>')]
    s0 = V1SRC.index('<div class="diag">'); e0 = V1SRC.index('<p class="diag-cap">')
    diag = V1SRC[s0:e0].rstrip() + '\n'
    diag = rep(diag, '>the right part</text>', '>rules shortlist,</text>')
    diag = rep(diag, '>by its when-rules</text>', '>a judge may rank</text>')
    diag = rep(diag, '>the right part, by its when-rules</text>', '>rules shortlist; Jev may rank it</text>')
    page = rep(page, '<!--CSS-->', css)
    page = rep(page, '<!--DIAG-->', '    ' + diag)
    return page

b = open(os.path.join(HERE, 'build.py'), encoding='utf-8').read()
b = rep(b, "SRC = os.path.join(HERE, 'page.src.html')", "SRC = os.path.join(HERE, 'page-v2.src.html')")
b = rep(b, "notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html')", "notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html')")
b = rep(b, "page:'proposal-apollo-mcp-v1', title:'Apollo-MCP, proposal v1', path:'notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html'",
           "page:'proposal-apollo-mcp-v2', title:'Apollo-MCP, proposal v2', path:'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'")
b = rep(b, "Jev dev-time only, 21 September: <code>s294-D10</code> in <code>knowledge/_rulings.json</code> (the rider keeps the option of full integration open).",
           "Jev at build time, 21 September: <code>s294-D10</code> in <code>knowledge/_rulings.json</code> holds Jev as a dev-time instrument, never a blocking dependency, and its rider keeps fuller integration open. Dave's 14:51 message (26 September) gives the reason, transferability, and says Jev is not ruled out for a GenUI project. v1 of this page read the ruling as a run-time ban; v2 corrects that. The 579 to 621 ms latency (three calls, one document, against a declared 70 to 500 ms) is quoted from the same ruling's text. Client: <code>knowledge/_jev.py</code> (Noul, Choice, Score); no caller in the build.")
b = rep(b, "Read them as order of size.</p>",
           "Read them as order of size. The four roles, their tools, scopes and the £500,000 limit are this lane's best guess on Dave's 14:52 instruction; no HSBC entitlement source was read.</p>")
b = rep(b, "Source template, build and render driver: <code>notes/_lanes/304/M/</code> (<code>page.src.html</code>, <code>build.py</code>, <code>render.py</code>); screenshots in <code>notes/_lanes/304/M/shots/</code>.",
           "v2 template, build and render driver: <code>notes/_lanes/304/M/</code> (<code>page-v2.src.html</code>, <code>build_v2.py</code>, <code>render_v2.py</code>, reusing v1's <code>page.src.html</code> for the CSS and diagram); screenshots in <code>notes/_lanes/304/M/shots/v2/</code>. v1 stays at <code>notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html</code>.")
b = rep(b, "open(OUT, 'w', encoding='utf-8').write(page)", "page = V2HOOK(page)\nopen(OUT, 'w', encoding='utf-8').write(page)")
exec(compile(b, 'build.py(v2)', 'exec'), {'__name__': '__main__', 'V2HOOK': V2HOOK})
