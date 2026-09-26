"""Lane 304-M v2 render: render.py unchanged, pointed at the v2 page and shots/v2/."""
import os
HERE = os.path.join(os.getcwd(), 'notes/_lanes/304/M')
r = open(os.path.join(HERE, 'render.py'), encoding='utf-8').read()
a = "notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html"; assert r.count(a) == 1
r = r.replace(a, "notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html")
a = "'notes/_lanes/304/M/shots'"; assert r.count(a) == 1
r = r.replace(a, "'notes/_lanes/304/M/shots/v2'")
r = r.replace("'apollo-mcp-v1-%s-full.png'", "'apollo-mcp-v2-%s-full.png'")
exec(compile(r, 'render.py(v2)', 'exec'), {'__name__': '__main__'})
