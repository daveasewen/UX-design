#!/usr/bin/env python3
"""#261 C — mutation probe for #260 A7 (a re-render never re-runs a type partial).
Drives the committed knowledge/_tests/chart-engine/bar.html: counts how many times the type
partial runs across a resize (re-FIT) and across dvRender.redraw (re-DRAW)."""
import os, sys
from playwright.sync_api import sync_playwright
P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                 "knowledge", "_tests", "chart-engine", "bar.html"))
JS = """() => {
  const f = document.getElementById('fig-column');
  const fn = window.dvRender.types.column, orig = fn;
  let runs = 0, widths = [];
  const spy = ctx => { runs++; widths.push(ctx.plotW); return orig(ctx); };
  spy.axis = orig.axis; spy.domain = orig.domain;
  window.dvRender.types.column = spy;
  window.dvRender(f, { type:'column', categories:['Q1','Q2','Q3','Q4'],
                       series:[{name:'Savings', values:[40,45,52,61]}] });
  const first = runs;
  window.dispatchEvent(new Event('resize'));
  const afterResize = runs;
  let threw = '';
  try { window.dvRender.redraw(document.createElement('figure')); }
  catch (e) { threw = e.message; }
  window.dvRender.redraw(f);
  const afterRedraw = runs;
  window.dvRender.types.column = orig;
  return { first, afterResize, afterRedraw, threw, sameSpec: widths.length > 0 };
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto("file://" + P)
    r = pg.evaluate(JS); b.close()
print(f"  partial runs: first render {r['first']} · after a resize {r['afterResize']} · after redraw {r['afterRedraw']}")
print(f"  un-rendered figure refuses: {r['threw']!r}")
ok = (r["first"] == 1 and r["afterResize"] == 1 and r["afterRedraw"] == 2
      and "has not been rendered" in r["threw"])
print("A7 redraw:", "PROVED" if ok else "FAILED")
sys.exit(0 if ok else 1)
