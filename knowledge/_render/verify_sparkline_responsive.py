import sys
#!/usr/bin/env python3
"""RENDER-PROOF — the sparkline atom is RESPONSIVE TO ITS ENCLOSURE (s184-D1, #184).

Dave, verbatim (#184): "the line should be responsive to its enclosure by default";
readback confirmed "this is all correct".

WHY THIS IS A RENDER-PROOF AND NOT A `_validate_*.py`
-----------------------------------------------------
DRIVEN AND MEASURED #184: the ruling was mutated back into the file (a fixed `width:340px`
on `.spark-standalone`) and `_validate_snippets.py`, `_validate_dataviz.py`,
`_validate_partials.py` and `_validate_grid.py` ALL still returned rc=0. No gate in the repo
can see a used width — the fact is a property of a LAID-OUT BOX, so only a browser can see it.

WHAT IT ASSERTS, at viewports 420 / 900 / 1440, with JS ON *and* JS OFF:
  A · the standalone spark's used width == its enclosure's CONTENT width (not its border box —
      comparing against a padded parent's border box was a false failure when this was written)
  B · the empty-state frame tracks its enclosure the same way
  C · the inline KPI spark fills its slot (.spark-kpi-slot, a SPECIMEN-only enclosure)
  D · the width actually VARIES across all three viewports (a constant that happens to match
      one enclosure would otherwise pass)
  E · HEIGHTS ARE UNCHANGED — 64px standalone / 44px inline. s184-D1 ruled WIDTH ONLY. The
      4px-grid height-snap is OPEN DIRECTION, NOT RULED; this proof PINS the heights so that
      nobody enacts a height ruling that was never made.

THE JS-OFF LEG IS THE LOAD-BEARING ONE — it is what makes this a proof of "BY DEFAULT".
Mutation-driven #184: restoring the pre-#184 shape (fixed 340px + a JS-gated
`figure.dv-fit-on{width:100%}` release) PASSES the JS-on leg and FAILS the JS-off leg alone.

HOW TO RUN (sandbox recipe, knowledge/_RUNBOOK-render-verify.md):
  export PYTHONPATH=/var/tmp/pylibs TMPDIR=/var/tmp \
         PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-<session> \
         LD_LIBRARY_PATH=/var/tmp/chromelibs-<session>/root/usr/lib/aarch64-linux-gnu \
         PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1
  python3 knowledge/_render/verify_sparkline_responsive.py
Uses goto("file://...") — set_content() is BANNED in render proofs.
"""
import os
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(REPO, "knowledge", "snippets", "Chart-sparkline.reference.html")
MEAS="""() => {
  const out={};
  const cw=(el)=>{const c=getComputedStyle(el);
    return el.getBoundingClientRect().width - parseFloat(c.paddingLeft) - parseFloat(c.paddingRight)
           - parseFloat(c.borderLeftWidth) - parseFloat(c.borderRightWidth);};
  const s=document.querySelector('.spark-standalone');
  out.spark=s.getBoundingClientRect().width;
  out.slot=cw(s.parentElement);
  out.h=s.getBoundingClientRect().height;
  const i=document.querySelector('.spark-inline');
  out.inline=i.getBoundingClientRect().width;
  out.inlineSlot=cw(i.parentElement);
  out.inlineH=i.getBoundingClientRect().height;
  const e=document.querySelector('.dv-empty-frame');
  out.empty=e.getBoundingClientRect().width;
  out.emptySlot=cw(e.parentElement);
  return out;
}"""
def run(js_enabled):
  fails=[];seen=[]
  with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(java_script_enabled=js_enabled)
    pg=ctx.new_page()
    for w in (420,900,1440):
      pg.set_viewport_size({"width":w,"height":800})
      pg.goto("file://"+PATH); pg.wait_for_timeout(120)
      m=pg.evaluate(MEAS); seen.append((w,m))
      tag=f"js={'on' if js_enabled else 'off'} vw={w}"
      if abs(m['spark']-m['slot'])>1: fails.append(f"{tag}: standalone {m['spark']:.1f} != enclosure {m['slot']:.1f}")
      if abs(m['empty']-m['emptySlot'])>1: fails.append(f"{tag}: empty-frame {m['empty']:.1f} != enclosure {m['emptySlot']:.1f}")
      if abs(m['inline']-m['inlineSlot'])>1: fails.append(f"{tag}: inline {m['inline']:.1f} != its slot {m['inlineSlot']:.1f}")
      if abs(m['h']-64)>0.5: fails.append(f"{tag}: standalone height {m['h']} != 64 (height must NOT change)")
      if abs(m['inlineH']-44)>0.5: fails.append(f"{tag}: inline height {m['inlineH']} != 44 (height must NOT change)")
    ws={round(x[1]['spark']) for x in seen}
    if len(ws)<3: fails.append(f"js={'on' if js_enabled else 'off'}: standalone width did not track viewport across 420/900/1440 -> {sorted(ws)}")
    b.close()
  return fails,seen
allf=[]
for je in (True,False):
  f,s=run(je); allf+=f
  for w,m in s: print(f"  js={'on ' if je else 'off'} vw={w:>4}  spark={m['spark']:7.1f}/{m['slot']:7.1f}  h={m['h']:.0f}  inline={m['inline']:6.1f}/{m['inlineSlot']:6.1f} h={m['inlineH']:.0f}  empty={m['empty']:7.1f}/{m['emptySlot']:7.1f}")
if allf:
  print("PROOF FAIL:"); [print("   "+x) for x in allf]; sys.exit(1)
print("PROOF PASS: enclosure-responsive at every width, JS-on and JS-off; heights unchanged (64/44)")
