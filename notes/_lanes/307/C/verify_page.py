"""Verify the #307 lane C review page: every image loads (naturalWidth > 0), no console errors,
no sideways scroll, Copy as text carries every call (clipboard stubbed by an init script), at 1440
and 390 wide, light and dark. Screenshots per section for looking."""
import sys, json; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _lib import *
PAGE = "notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html"
V = OUT.parent / "verify"; V.mkdir(exist_ok=True)
STUB = "window.__copied=[]; Object.defineProperty(navigator,'clipboard',{value:{writeText:function(t){window.__copied.push(t);return Promise.resolve();}},configurable:true}); window.confirm=function(){return true;};"
rec = {}
with sync_playwright() as p:
    b = launch(p)
    for w, h, scheme in [(1440, 1000, "light"), (390, 844, "light"), (1440, 1000, "dark")]:
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, color_scheme=scheme)
        ctx.add_init_script(STUB)
        pg = ctx.new_page()
        cons = []; pg.on("console", lambda m: cons.append((m.type, m.text)) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: cons.append(("pageerror", str(e))))
        failed = []; pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.goto(url(PAGE)); pg.wait_for_load_state("load")
        pg.wait_for_function("() => Array.from(document.images).every(i => i.complete)", timeout=20000)
        imgs = pg.evaluate("() => Array.from(document.images).map(i => [i.getAttribute('src'), i.naturalWidth, i.getBoundingClientRect().width])")
        broken = [i for i in imgs if i[0] and i[1] == 0]   # the lightbox img has no src until opened
        sideways = pg.evaluate("() => [document.documentElement.scrollWidth, window.innerWidth]")
        # overflowing boxes: an element wider than its parent section's wrap
        over = pg.evaluate("""() => { const out=[]; const W=document.documentElement.clientWidth;
            document.querySelectorAll('body *').forEach(el => { const r=el.getBoundingClientRect();
              if (r.width>0 && r.right > W+1 && !el.closest('.fk-wrap') && getComputedStyle(el).position!=='fixed') out.push(el.tagName+'.'+(el.className||'')+' '+Math.round(r.right)); });
            return out.slice(0,10); }""")
        key = f"{w}-{scheme}"
        r = {"images": len(imgs), "broken": broken, "scrollWidth_vs_viewport": sideways, "overflow": over}
        if key == "1440-light":
            n_calls = pg.evaluate("() => document.querySelectorAll('.dd-call').length")
            # answer every call by its recommended button, type a note in the first and last
            recs = pg.evaluate("() => Array.from(document.querySelectorAll('.dd-chip.rec')).length")
            pg.evaluate("() => document.querySelectorAll('.dd-chip.rec').forEach(b => b.click())")
            tas = pg.locator(".dd-box textarea[data-f=comment]")
            tas.first.fill("test note one"); tas.last.fill("test note on the page")
            pg.click("#dd-copy"); pg.wait_for_timeout(300)
            txt = pg.evaluate("() => window.__copied.slice(-1)[0] || ''")
            titles = pg.evaluate("() => Array.from(document.querySelectorAll('.dd-call .q')).map(q => q.textContent.replace(/\\s+/g,' ').trim())")
            missing = [t for t in titles if t not in txt]
            chose = txt.count("**Chose:**"); therec = txt.count("· the recommendation")
            (V / "copied-text-1440.md").write_text(txt)
            r.update(calls=n_calls, rec_buttons=recs, copied_chars=len(txt), titles_missing=missing, chose_lines=chose,
                     chose_is_rec=therec, notes_in_copy=("test note one" in txt and "test note on the page" in txt),
                     msg=pg.evaluate("() => document.getElementById('dd-msg').textContent"),
                     count=pg.evaluate("() => document.getElementById('dd-count').textContent"))
            # clear, so the stored state does not leak into the next context (separate context anyway)
            pg.click("#dd-clear")
        # section pictures for looking
        for sec in ["answer", "item-1", "item-2", "item-3", "item-4", "item-5", "item-6"]:
            top, hgt = pg.evaluate(f"() => {{ const r=document.getElementById('{sec}').getBoundingClientRect(); return [r.top+window.scrollY, r.height]; }}")
            n = 0; y = top
            while y < top + hgt:   # tall sections in 5000px pieces, page coordinates
                pg.screenshot(path=str(V / f"{key}-{sec}-{n}.png"), clip={"x": 0, "y": y, "width": w, "height": min(5000, top + hgt - y)}, full_page=True)
                y += 5000; n += 1
        r["console"] = cons; r["failed_requests"] = failed
        r["page_height"] = pg.evaluate("() => document.documentElement.scrollHeight")
        rec[key] = r
        ctx.close()
    b.close()
(V / "verify-receipt.json").write_text(json.dumps(rec, indent=1))
for k, v in rec.items():
    print(k, {kk: vv for kk, vv in v.items() if kk not in ("overflow",)}, "overflow:", v["overflow"][:5])
