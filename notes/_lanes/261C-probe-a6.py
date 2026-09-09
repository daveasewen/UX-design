#!/usr/bin/env python3
"""#261 C — mutation probe for #260 A6 (a type contributes its own accessible name).
Drives the committed knowledge/_tests/chart-engine/bar.html; same figure, same spec."""
import os, sys
from playwright.sync_api import sync_playwright
P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                 "knowledge", "_tests", "chart-engine", "bar.html"))
JS = """(mode) => {
  const f = document.getElementById('fig-column');
  const spec = { type:'column', caption:'Sessions', categories:['Mon','Tue','Wed','Thu'],
                 series:[{name:'Close', values:[90.41,101.2,97.8,108.52]}] };
  const fn = window.dvRender.types.column;
  if (mode === 'off') { delete fn.label; }
  else { fn.label = s => s.caption + '. 4 sessions, 90.41 to 108.52.'; }
  if (mode === 'authored') { spec.label = 'The author had the last word.'; }
  window.dvRender(f, spec);
  return f.querySelector('svg').getAttribute('aria-label');
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto("file://" + P)
    out = {m: pg.evaluate(JS, m) for m in ["off", "fn", "authored", "off"]}
    b.close()
for k in ["off", "fn", "authored"]:
    print(f"  {k:9} {out[k][:78]}")
ok = ("Mon 90.41" in out["off"] and out["fn"].endswith("90.41 to 108.52.")
      and out["authored"] == "The author had the last word." and len(out["fn"]) < len(out["off"]))
print("A6 fn.label:", "PROVED" if ok else "FAILED")
sys.exit(0 if ok else 1)
