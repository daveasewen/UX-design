"""L3 #245 — render probe of the REAL bento snippet, standalone via file:// (no canon.css is linked —
0 of 137 snippets do). Reads the wall grid's computed columns, the custom-property chain, and the
four KPI tiles' boxes, for the artefact AS SHIPPED and for a FIXTURE that declares the literal
`--layout-bento-columns:6` the meta's $tokenGaps[0] says the file carries. Writes render-probe.json
+ two full-page PNGs beside this script. Recipe: `source knowledge/_render/seat_env.sh` first."""
import asyncio, json, os
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SNIP = os.path.join(ROOT, "knowledge", "snippets", "Template-dashboard-bento.reference.html")
DECL = "--layout-bento-gutter:0; --layout-bento-outer-padding:0; --layout-bento-row-unit:320px;"
JS = """()=>{const w=document.querySelector('.tpl-wall > .c-bento__grid');const cs=getComputedStyle(w);
  const kpi=[...document.querySelectorAll('.tpl-group-kpi .kpi-tile')].map(t=>{const r=t.getBoundingClientRect();return {label:t.getAttribute('aria-label'),x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}});
  const gs=[...document.querySelectorAll('.tpl-group')].map(s=>{const g=getComputedStyle(s.querySelector('.c-bento__grid'));return {label:s.getAttribute('aria-label'),w:Math.round(s.getBoundingClientRect().width),gap:g.gap,tracks:g.gridTemplateColumns.split(' ').length,flow:g.gridAutoFlow}});
  return {wall_tracks:cs.gridTemplateColumns.split(' ').length, wall_gridTemplateColumns:cs.gridTemplateColumns, wall_gap:cs.gap, wall_gridAutoFlow:cs.gridAutoFlow,
     var_bento_cols_now:cs.getPropertyValue('--bento-cols-now').trim()||'(empty)', var_layout_bento_columns:cs.getPropertyValue('--layout-bento-columns').trim()||'(empty)',
     var_layout_bento_packing:cs.getPropertyValue('--layout-bento-packing').trim()||'(empty)', groups:gs, kpi_tiles:kpi,
     kpi_layout: (new Set(kpi.map(k=>k.y))).size===2 && (new Set(kpi.map(k=>k.x))).size===2 ? '2x2' : ((new Set(kpi.map(k=>k.x))).size===1 ? 'stacked 4x1' : 'other')}}"""
async def main():
    raw = open(SNIP, encoding="utf-8").read()
    assert raw.count(DECL) == 2 and "--layout-bento-columns:" not in raw
    fixed = raw.replace(DECL, DECL + " --layout-bento-columns:6;")
    fx = os.path.join(os.environ.get("TMPDIR", "/tmp"), "bento-fixture-cols6.html"); open(fx, "w", encoding="utf-8").write(fixed)
    out = {"artefact": "knowledge/snippets/Template-dashboard-bento.reference.html", "fixture": "the artefact + `--layout-bento-columns:6` in both theme blocks (in sandbox scratch, not the repo)", "viewports": {}}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL") or None)
        for w in (1440, 1000, 390):
            out["viewports"][w] = {}
            for name, path in (("as_shipped", SNIP), ("fixture_cols6", fx)):
                pg = await b.new_page(viewport={"width": w, "height": 1000})
                await pg.goto("file://" + path); await pg.wait_for_timeout(300)
                out["viewports"][w][name] = await pg.evaluate(JS)
                if w == 1440:
                    await pg.screenshot(path=os.path.join(HERE, "render-%s-1440.png" % name.replace("_", "-")), full_page=True)
                await pg.close()
        await b.close()
    open(os.path.join(HERE, "render-probe.json"), "w", encoding="utf-8").write(json.dumps(out, indent=1) + "\n")
    for w, d in out["viewports"].items():
        for k, v in d.items():
            print("%5s %-14s wall tracks %d  --bento-cols-now=%s  --layout-bento-columns=%s  packing=%s/%s  KPI %s  groups tracks %s" % (
                w, k, v["wall_tracks"], v["var_bento_cols_now"], v["var_layout_bento_columns"], v["var_layout_bento_packing"], v["wall_gridAutoFlow"], v["kpi_layout"], [g["tracks"] for g in v["groups"]]))
asyncio.run(main())
