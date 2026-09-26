#!/usr/bin/env python3
"""render_kg.py EXPLORER.html OUTDIR — #304 R3: shoot the KG explorer with the tokens chip ON
(?fam=tokens) and OFF at 1440, via goto(file://) with the seat's RENDER_SHELL, and print the page's own
counts for the token family (nodes of type token, bindsToken edges, the chip's label and count text)."""
import os, sys, json
if any(a in ("-h", "--help") for a in sys.argv[1:]):
    print(__doc__); sys.exit(0)
from playwright.sync_api import sync_playwright
src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], headless=True,
                          args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
    for q, name in (("", "kg-default"), ("?fam=tokens", "kg-tokens-on"), ("?fam=tokens&layout=strata", "kg-tokens-strata")):
        pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + src + q); pg.wait_for_timeout(2500)
        facts = pg.evaluate("""() => {
          const tok = KG.nodes.filter(n=>n.type==='token'), bt = KG.edges.filter(e=>e.type==='bindsToken');
          const chip = [...document.querySelectorAll('[data-fam="tokens"]')].map(c=>c.textContent.trim()+' ['+c.className+']');
          return {version: KG.version, tokenNodes: tok.length, bindsToken: bt.length,
                  tiers: tok.reduce((a,n)=>(a[n.tier]=(a[n.tier]||0)+1,a),{}),
                  topBlast: tok.slice().sort((a,b)=>b.blast-a.blast).slice(0,3).map(n=>n.id+' '+n.blast),
                  xtra: {tokens: KG.extra.tokens, tokenEdges: KG.extra.tokenEdges}, chip,
                  header: (document.querySelector('header')||document.body).innerText.slice(0,300)};
        }""")
        facts["pageerrors"] = errs
        print(name, json.dumps(facts, ensure_ascii=False))
        pg.screenshot(path=os.path.join(out, name + "-1440.png")); pg.close()
    b.close()
