#!/usr/bin/env python3
"""#261 C — mutation probe for #260 A1 (the furniture dial). Drives the COMMITTED test page
knowledge/_tests/chart-engine/bar.html in Chromium and counts .dv-grid / .dv-axis per dial
position, re-rendering the same figure with the same spec. Proves the CLAUSE, not the feature."""
import os, sys, json
from playwright.sync_api import sync_playwright
P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                 "knowledge", "_tests", "chart-engine", "bar.html"))
JS = """(pos) => {
  const f = document.getElementById('fig-column');
  const spec = { type:'column', categories:['Q1','Q2','Q3','Q4'],
                 series:[{name:'Savings', values:[40,45,52,61]}] };
  const fn = window.dvRender.types.column;
  if (pos === 'default') { delete fn.furniture; delete fn.axis; }
  else if (pos === 'none-axis') { delete fn.furniture; fn.axis = 'none'; }
  else { fn.furniture = pos; delete fn.axis; }
  window.dvRender(f, spec);
  const svg = f.querySelector('svg');
  return { grid: svg.querySelectorAll('.dv-grid').length,
           tick: svg.querySelectorAll('text.dv-axis').length,
           base: svg.querySelectorAll('line.dv-axis').length,
           marks: svg.querySelectorAll('rect').length };
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto("file://" + P)
    out = {k: pg.evaluate(JS, k) for k in ["default", "axis", False, "none-axis", "default"]}
    b.close()
for k, v in out.items():
    print(f"  {str(k):10} grid={v['grid']:2} tick={v['tick']:2} baseline={v['base']} marks={v['marks']}")
d, a, off = out["default"], out["axis"], out[False]
ok = (d["grid"] > 0 and a["grid"] == 0 and a["tick"] == d["tick"] and a["base"] == d["base"]
      and off["grid"] == 0 and off["tick"] == 0 and off["base"] == 0
      and out["none-axis"] == off and d["marks"] == off["marks"] == a["marks"] > 0)
print("A1 dial:", "PROVED" if ok else "FAILED")
sys.exit(0 if ok else 1)
