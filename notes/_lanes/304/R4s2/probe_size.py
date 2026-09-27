"""probe_size.py — R4s2: verify two size defects the cand2 runs reported.
(1) chart legend buttons 16.7px vs 20px: which ancestor's text-box-trim reaches them, and does removing
    it restore the reference height? (2) KPI tile 4px taller inside the bento: spark-inline height and the
    rule that sets it, page vs the Kpi-tile reference. Prints JSON; writes nothing."""
import json, os, sys
from playwright.sync_api import sync_playwright
PAGES = sys.argv[1:]
LEG = r"""() => {
 const b = document.querySelector('button.dv-leg-item'); if (!b) return null;
 const h0 = b.getBoundingClientRect().height; const cs = getComputedStyle(b);
 const chain = []; for (let a = b; a; a = a.parentElement) { const s = getComputedStyle(a);
   const t = s.textBoxTrim || s.getPropertyValue('text-box-trim'); const e = s.textBoxEdge || s.getPropertyValue('text-box-edge');
   if (t && t !== 'none') chain.push({el: a.tagName.toLowerCase()+'.'+[...a.classList].slice(0,3).join('.'), trim: t, edge: e}); }
 return {h: h0, trim: cs.textBoxTrim, edge: cs.textBoxEdge, lh: cs.lineHeight, pad: cs.paddingTop+' '+cs.paddingBottom, trim_chain: chain.slice(0,6)};
}"""
FIX = r"""() => { const st = document.createElement('style'); st.textContent = 'button.dv-leg-item, button.dv-leg-reset{text-box-trim:none !important}'; document.head.appendChild(st);
 return new Promise(r => requestAnimationFrame(() => r(document.querySelector('button.dv-leg-item').getBoundingClientRect().height))); }"""
KPI = r"""() => {
 const t = [...document.querySelectorAll('.kpi-tile')].slice(0,4).map(k => { const s = k.querySelector('.spark-inline, svg.spark, .kpi-spark');
   return {h: Math.round(k.getBoundingClientRect().height*10)/10, spark: s ? {cls: s.getAttribute('class'), h: s.getBoundingClientRect().height, cssH: getComputedStyle(s).height} : null}; });
 return t;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for f in PAGES:
        pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce"); pg.goto("file://" + os.path.abspath(f)); pg.wait_for_timeout(1500)
        out = {"legend": pg.evaluate(LEG), "kpi": pg.evaluate(KPI)}
        if out["legend"]: out["legend_after_trim_none"] = pg.evaluate(FIX)
        print(os.path.basename(os.path.dirname(os.path.dirname(f))) + "/" + os.path.basename(f), json.dumps(out))
        pg.close()
    b.close()
