#!/usr/bin/env python3
"""305 B2 — open notes/_KG-EXPLORER.html (v1.30) from disk at 1440 and LOOK: the default canvas, a dug ruling
(canvas prints the code alone, the panel the full title), the sources layer on (?fam=sources), a component's
panel with its step-5 relations, and a search. Prints the page's own facts and every page error.
usage: render_explorer.py REPO_ROOT OUTDIR"""
import os, sys, json
from playwright.sync_api import sync_playwright
root, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
page = "file://" + os.path.join(root, "notes", "_KG-EXPLORER.html")
F = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], headless=True,
                          args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
    def open_(q=""):
        pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(page + q); pg.wait_for_timeout(3500)
        return pg, errs
    pg, errs = open_()
    F["version"] = pg.evaluate("KG.version")
    F["nodes_edges"] = pg.evaluate("[KG.nodes.length, KG.edges.length]")
    F["sample"] = pg.evaluate("""() => ['ruling:s133-D1','session:165','polarity:pl-02','guideline:1.4','artefact:ADR-0013','artefact:axs-003']
        .map(i => { const n = KG.nodes.find(x => x.id === i); return n ? [i, n.label, n.code || '(no code)'] : [i, 'ABSENT'] })""")
    F["famOn_sources_default"] = pg.evaluate("famOn.sources")
    F["chip_labels"] = pg.evaluate("() => [...document.querySelectorAll('button, label')].map(x=>x.innerText.trim()).filter(t=>/Sources|Tokens/.test(t)).slice(0,6)")
    pg.screenshot(path=os.path.join(out, "kg-default-1440.png"))
    def search(s):
        pg.fill("#q", ""); pg.type("#q", s, delay=15); pg.wait_for_timeout(700)
        return pg.evaluate("() => [...document.querySelectorAll('#hits .hit')].slice(0,6).map(h => h.innerText.replace(/\\s+/g,' ').trim())")
    F["search_s133-D1"] = search("s133-D1")
    pg.evaluate("() => { const h=[...document.querySelectorAll('#hits .hit')].find(x=>x.querySelector('small') && x.querySelector('small').textContent==='ruling'); h.click() }")
    pg.wait_for_timeout(2500)
    F["panel_head"] = pg.evaluate("() => { const a=document.querySelector('aside .head'); return a ? a.innerText.replace(/\\s+/g,' ').slice(0,220) : 'no aside head' }")
    F["panel_rows"] = pg.evaluate("() => [...document.querySelectorAll('aside .rel .n')].slice(0,6).map(x=>x.innerText.replace(/\\s+/g,' '))")
    pg.screenshot(path=os.path.join(out, "kg-dug-ruling-s133-D1-1440.png"))
    F["errors_default"] = errs; pg.close()
    pg, errs = open_("?fam=sources")
    F["famOn_sources_q"] = pg.evaluate("famOn.sources")
    pg.screenshot(path=os.path.join(out, "kg-sources-on-1440.png"))
    F["search_chart-bar"] = search("Bar chart")
    pg.evaluate("() => { const h=[...document.querySelectorAll('#hits .hit')].find(x=>x.querySelector('small') && x.querySelector('small').textContent==='component'); h.click() }")
    pg.wait_for_timeout(2500)
    F["component_panel_head"] = pg.evaluate("() => { const a=document.querySelector('aside .head'); return a ? a.innerText.replace(/\\s+/g,' ').slice(0,160) : 'none' }")
    F["component_panel_step5"] = pg.evaluate("() => [...document.querySelectorAll('aside')].map(a=>a.innerText).join(' ').match(/(is set in|takes its behaviour from|was captured from|accepts in a slot)[^\\n]{0,80}/g)")
    pg.screenshot(path=os.path.join(out, "kg-sources-chart-bar-1440.png"))
    F["search_capability"] = search("chart-dataset")
    F["errors_sources"] = errs; pg.close()
    b.close()
print(json.dumps(F, ensure_ascii=False, indent=1))
