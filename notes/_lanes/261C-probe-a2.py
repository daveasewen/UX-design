#!/usr/bin/env python3
"""#261 C — mutation probe for #260 A2 (scope the ZERO CLAMP). Drives the committed
knowledge/_tests/chart-engine/bar.html: same figure, same spec, clamp on and off."""
import os, sys
from playwright.sync_api import sync_playwright
P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                 "knowledge", "_tests", "chart-engine", "bar.html"))
JS = """(off) => {
  const f = document.getElementById('fig-column');
  const spec = { type:'column', categories:['Mon','Tue','Wed','Thu'],
                 series:[{name:'Close', values:[90.41,101.2,97.8,108.52]}] };
  const fn = window.dvRender.types.column;
  if (off) { fn.zeroBaseline = false; } else { delete fn.zeroBaseline; }
  window.dvRender(f, spec);
  const t = [...f.querySelectorAll('text.dv-axis')].map(e => parseFloat(e.textContent));
  return { lo: Math.min(...t), hi: Math.max(...t), ticks: t.length };
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto("file://" + P)
    on, off, back = pg.evaluate(JS, False), pg.evaluate(JS, True), pg.evaluate(JS, False)
    b.close()
for k, v in (("clamped (default)", on), ("zeroBaseline:false", off), ("default again", back)):
    print(f"  {k:19} axis {v['lo']}–{v['hi']} ({v['ticks']} ticks)")
ok = on["lo"] == 0 and off["lo"] >= 80 and off["hi"] <= 120 and back == on
print("A2 clamp scope:", "PROVED" if ok else "FAILED")
sys.exit(0 if ok else 1)
