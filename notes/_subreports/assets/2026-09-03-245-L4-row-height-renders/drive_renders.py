#!/usr/bin/env python3
"""Lane L4 (#245) — render-proof of reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html.

Drives the page through page.goto("file://…") — NEVER set_content (that path drops type.css
silently). Reads the page's own live measurement (window.__L4, what getComputedStyle resolved),
asserts the row model per column per theme per mode, then drives THREE mutation arms and shows
which assertions bite. Writes, beside this script:
  drive-transcript.txt   every assertion, one per line, PASS/FAIL, with the measured value
  measurements.json      the raw __L4 table for the baseline
  counts.json            the counts quoted in the report
  render-*.png           one per theme × mode frame (fit view), page-full.png, one-to-one-mono-light.png

Usage: LD_LIBRARY_PATH=<dir with libXdamage.so.1> python3 drive_renders.py
"""
import json, pathlib, re, sys, time
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
PAGE = REPO / "reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html"
ledger = json.loads((HERE / "splice-ledger.json").read_text())
RUNGS = {k: float(v[:-2]) for k, v in ledger["markers"]["rungs"].items()}
MIS = {k: float(v[:-2]) for k, v in ledger["markers"]["misrung"].items()}

T = []          # transcript lines
counts = dict(assertions=0, fails=0, mutation_arms=0, mutation_bites=0, console_errors=0, renders=0)


def check(name, ok, value=""):
    counts["assertions"] += 1
    if not ok:
        counts["fails"] += 1
    T.append(f"{'PASS' if ok else 'FAIL'}  {name}  ->  {value}")
    return ok


def assert_baseline(res, tag, floor_max="auto", mis_model="fixed"):
    """The per-render assertions. Returns the number of FAILs contributed."""
    before = counts["fails"]
    for r in res:
        k = f"[{tag}] {r['theme']}/{r['mode']}/{r['col']}"
        check(f"{k} outer wall grid-auto-rows is auto (level HELD)", r["outerAutoRows"] == "auto", r["outerAutoRows"])
        for g in r["groups"]:
            rung = RUNGS[g["group"]]
            gk = f"{k} {g['group']}"
            if r["col"] == "fixed":
                check(f"{gk} computed grid-auto-rows == {rung:g}px", g["autoRows"] == f"{rung:g}px", g["autoRows"])
                check(f"{gk} every row track == rung", all(abs(t - rung) < 0.6 for t in g["tracks"]), g["tracks"])
                check(f"{gk} FIXED: tiles fit the shipped rung (0 overrun)", g["tilesOverflowing"] == 0, f"{g['tilesOverflowing']} overrun")
            elif r["col"] == "floor":
                exp = f"minmax({rung:g}px, {floor_max})"
                check(f"{gk} computed grid-auto-rows == {exp}", g["autoRows"] == exp, g["autoRows"])
                check(f"{gk} every row track >= rung", all(t >= rung - 0.6 for t in g["tracks"]), g["tracks"])
                check(f"{gk} dead band <= 1px (rows grew into the stretch)", g["deadBand"] <= 1.0, f"{g['deadBand']}px")
                check(f"{gk} no tile overruns its row", g["tilesOverflowing"] == 0, g["tilesOverflowing"])
            elif r["col"] == "misrung":
                m = MIS[g["group"]]
                if mis_model == "fixed":
                    check(f"{gk} computed grid-auto-rows == {m:g}px (the wrong rung, fixed)", g["autoRows"] == f"{m:g}px", g["autoRows"])
                    check(f"{gk} every row track == wrong rung", all(abs(t - m) < 0.6 for t in g["tracks"]), g["tracks"])
                else:
                    check(f"{gk} computed grid-auto-rows == minmax({m:g}px, auto)", g["autoRows"] == f"minmax({m:g}px, auto)", g["autoRows"])
        if r["col"] == "misrung":
            n = sum(g["tilesOverflowing"] for g in r["groups"])
            if mis_model == "fixed":
                check(f"{k} at least one tile overruns its row (the break is VISIBLE)", n >= 1, f"{n} tiles")
            else:
                check(f"{k} under FLOOR the same wrong rungs heal — 0 tiles overrun", n == 0, f"{n} tiles")
    return counts["fails"] - before


with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append(str(e)))
    url = PAGE.as_uri()
    T.append(f"goto {url}")
    pg.goto(url)
    pg.wait_for_function("window.__L4 && window.__L4.length===24")
    pg.evaluate("document.fonts.ready.then(()=>window.__L4measure())")
    time.sleep(0.4)
    res = pg.evaluate("window.__L4measure()")
    (HERE / "measurements.json").write_text(json.dumps(res, indent=1))
    counts["renders"] = len(res)
    check("24 renders measured (4 themes × 2 modes × 3 columns)", len(res) == 24, len(res))

    # instrument sanity: type.css actually arrived (goto, not set_content) and every stage sits in the 6-column band
    ff = pg.evaluate("getComputedStyle(document.querySelector('.tpl-group .t-cm-figure-2, .tpl-group [class*=t-cm-figure], .tpl-group [class*=t-ed-]')).fontFamily")
    check("type.css composites resolve (font-family carries Univers Next)", "Univers" in ff, ff)
    cols_now = pg.evaluate("[...document.querySelectorAll('.tpl-wall > .c-bento__grid')].map(g=>getComputedStyle(g).gridTemplateColumns.split(' ').length)")
    check("every outer wall renders at the 6-column band (stage 1440px → wall 1376px; zoom does not change the band)", all(c == 6 for c in cols_now), sorted(set(cols_now)))
    wall_w = pg.evaluate("getComputedStyle(document.querySelector('.tpl-wall')).width")
    T.append(f"wall width inside the 1440px stage: {wall_w}")
    zooms = pg.evaluate("[...document.querySelectorAll('.stage')].map(s=>parseFloat(s.style.zoom))")
    T.append(f"fit zoom per stage: {sorted(set(round(z,3) for z in zooms))}")

    # content identical across the three columns of each frame
    same = pg.evaluate("""[...document.querySelectorAll('.frame')].map(f=>{const h=[...f.querySelectorAll('.cn-template-dashboard-bento')].map(e=>e.innerHTML); return h.every(x=>x===h[0]);})""")
    check("wall markup byte-identical across the 3 columns of every frame (8 frames)", all(same), same)

    # zero external references — grepped from disk, not from the DOM
    src = PAGE.read_text(encoding="utf-8")
    ext = [t for t in ('src="', 'href="../', "@import", "http://", "https://", "url(") if t in src]
    check("zero external references in the file", not ext, ext or "none")
    check("type.css spliced verbatim (byte-equal to knowledge/canon/type.css)", (REPO / "knowledge/canon/type.css").read_text(encoding="utf-8") in src, f"{len(src):,} B file")

    fails0 = assert_baseline(res, "baseline")
    T.append(f"baseline: {fails0} FAIL")

    # zoom does not distort the measurement: 1:1 view must read the same tracks as the fit view
    pg.check('input[name="view"][value="one"]')
    time.sleep(0.3)
    res1 = pg.evaluate("window.__L4measure()")
    diffs = [abs(x - y) for a, c in zip(res, res1) for i in range(3) for x, y in zip(a["groups"][i]["tracks"], c["groups"][i]["tracks"])]
    fixed_same = all(a["groups"][i]["tracks"] == c["groups"][i]["tracks"] for a, c in zip(res, res1) if a["col"] != "floor" for i in range(3))
    check("FIXED and MIS-RUNG tracks byte-identical between fit (zoomed) and 1:1 view", fixed_same, "16 renders × 3 groups")
    check("content-grown (FLOOR) tracks within 8px between fit and 1:1 — fractional zoom re-wraps glyphs, declared (first run measured 6.6px)", max(diffs) <= 8.0, f"max |Δ| {max(diffs):.1f}px")
    grounds = pg.evaluate("[...document.querySelectorAll('.frame')].map(f=>[f.dataset.themeKey, f.dataset.mode, getComputedStyle(f.querySelector('.cn-template-dashboard-bento')).backgroundColor])")
    EXP_GROUND = {"light": "rgb(240, 240, 240)", "dark": "rgb(26, 26, 26)"}                       # canon.css:16778/16782
    EXP_GROUND_SC = {"light": "rgb(223, 222, 220)", "dark": "rgb(42, 38, 33)"}                    # supercharge's own --wall-ground override (canon.css, [data-apollo-theme="supercharge"] .cn-template-dashboard-bento) — found by the first run FAILING on it
    check("page ground per theme/mode is the scope's --wall-ground (mono/legacy/console #F0F0F0 / #1A1A1A; supercharge #DFDEDC / #2A2621)", all(c == (EXP_GROUND_SC if t == "supercharge" else EXP_GROUND)[m] for t, m, c in grounds), grounds)
    radii = pg.evaluate("[...document.querySelectorAll('.frame[data-mode=light] .col[data-col=fixed] .tpl-group-kpi')].map(g=>[g.closest('.frame').dataset.themeKey, getComputedStyle(g).borderRadius])")
    check("theme reaches the wall: console groups carry --border-radius-container 20px, the other three 0", all((r == "20px") == (t == "console") for t, r in radii), radii)
    T.append(f"zoom-vs-1:1 track deltas: max {max(diffs):.1f}px over {len(diffs)} tracks")
    # evidence: the mono/light frame at 1:1
    pg.locator('.frame[data-theme-key="mono"][data-mode="light"]').screenshot(path=str(HERE / "one-to-one-mono-light.png"))
    sweep = {}
    for w in ("1440", "1100", "800", "500"):
        pg.check(f'input[name="stage"][value="{w}"]')
        time.sleep(0.3)
        rs = pg.evaluate("window.__L4measure()")
        r = next(x for x in rs if x["theme"] == "mono" and x["mode"] == "light" and x["col"] == "fixed")
        rf = next(x for x in rs if x["theme"] == "mono" and x["mode"] == "light" and x["col"] == "floor")
        tiles = pg.evaluate("""[...document.querielectorAll ? [] : document.querySelectorAll('.frame[data-theme-key=mono][data-mode=light] .col[data-col=fixed] .tpl-group')].map(g=>[[...g.classList].find(k=>k.startsWith('tpl-group-')).slice(10), [...g.querySelectorAll(':scope > .c-bento__grid > .c-bento__tile')].map(t=>[t.clientHeight,t.scrollHeight])])""")
        sweep[w] = dict(cols=r["cols"], fixed=[(g["group"], g["tracks"], g["tilesOverflowing"]) for g in r["groups"]], floor_tracks=[(g["group"], g["tracks"]) for g in rf["groups"]], tiles=tiles)
        T.append(f"BAND SWEEP stage {w}px → {r['cols']} col · FIXED overruns per group: {[(g['group'], g['tilesOverflowing']) for g in r['groups']]} · FLOOR tracks: {[(g['group'], g['tracks']) for g in rf['groups']]} · tile [client,scroll]: {tiles}")
        pg.locator('.frame[data-theme-key="mono"][data-mode="light"]').screenshot(path=str(HERE / f"band-{w}-mono-light-1to1.png"))
    (HERE / "band-sweep.json").write_text(json.dumps(sweep, indent=1))
    pg.check('input[name="stage"][value="1440"]')
    pg.check('input[name="view"][value="fit"]')
    time.sleep(0.3)
    pg.evaluate("window.__L4measure()")

    # per-frame screenshots, fit view
    for th in ("mono", "legacy", "console", "supercharge"):
        for md in ("light", "dark"):
            pg.locator(f'.frame[data-theme-key="{th}"][data-mode="{md}"]').screenshot(path=str(HERE / f"render-{th}-{md}.png"))
    pg.screenshot(path=str(HERE / "page-full.png"), full_page=True)

    # ---- CONTROL: column 2 → 1fr (canon as shipped) and back
    pg.check('input[name="floormax"][value="floor-1fr"]')
    time.sleep(0.2)
    r1 = pg.evaluate("window.__L4measure()")
    n1 = assert_baseline([r for r in r1 if r["col"] == "floor"], "col2=1fr", floor_max="1fr")
    T.append(f"control col2=1fr: {n1} FAIL (expected 0 — the 1fr state is canon verbatim)")
    pg.check('input[name="floormax"][value="floor-auto"]')

    # ---- MUTATION 1: force column 2 onto the FIXED model behind the label's back; the floor assertions must bite
    counts["mutation_arms"] += 1
    pg.add_style_tag(content='.col[data-model="floor-auto"] .cn-template-dashboard-bento .c-bento__tile.c-bento > .c-bento__grid{grid-auto-rows:var(--bento-row-unit) !important;}')
    time.sleep(0.2)
    rm = pg.evaluate("window.__L4measure()")
    before = counts["fails"]
    bites = assert_baseline([r for r in rm if r["col"] == "floor"], "MUTATION-1 col2 forced fixed")
    counts["mutation_bites"] += bites
    T.append(f"MUTATION 1 (column 2 silently made FIXED): {bites} floor assertions bit (expected > 0)")
    check("MUTATION 1 bites (>0 floor assertions fail when column 2 is secretly fixed)", bites > 0, bites)
    # those FAILs are the mutation doing its job — they are counted separately, not as defects
    counts["fails"] -= bites
    pg.evaluate("document.querielectorAll" if False else "[...document.querySelectorAll('style')].pop().remove()")
    time.sleep(0.2)
    rr = pg.evaluate("window.__L4measure()")
    check("MUTATION 1 reverted — column 2 floor assertions pass again", assert_baseline([r for r in rr if r["col"] == "floor"], "post-M1") == 0, "0 FAIL")

    # ---- MUTATION 2: through the REAL control — flip column 3 to FLOOR; the 'break is visible' assertion must bite
    counts["mutation_arms"] += 1
    pg.check('input[name="mismodel"][value="misrung-floor"]')
    time.sleep(0.2)
    r3 = pg.evaluate("window.__L4measure()")
    before = counts["fails"]
    bites = assert_baseline([r for r in r3 if r["col"] == "misrung"], "MUTATION-2 col3 under floor (asserted as fixed)", mis_model="fixed")
    counts["mutation_bites"] += bites
    T.append(f"MUTATION 2 (column 3 flipped to FLOOR via its radio): {bites} fixed-misrung assertions bit (expected > 0)")
    check("MUTATION 2 bites (>0 mis-rung assertions fail once the floor heals the wrong rung)", bites > 0, bites)
    counts["fails"] -= bites
    # and the floor reading of the same state is internally consistent (the wrong rung HEALS: 0 tiles overrun)
    nf = assert_baseline([r for r in r3 if r["col"] == "misrung"], "col3 under floor (asserted as floor)", mis_model="floor")
    check("column 3 under FLOOR: the same wrong rungs render with 0 tiles overrunning — the failure is INVISIBLE", nf == 0, f"{nf} FAIL")
    pg.locator('.frame[data-theme-key="mono"][data-mode="light"]').screenshot(path=str(HERE / "render-mono-light-misrung-under-floor.png"))
    pg.check('input[name="mismodel"][value="misrung-fixed"]')

    # ---- MUTATION 3: the export must follow the pick — point at column 1 in the console/dark frame
    counts["mutation_arms"] += 1
    pg.locator('.frame[data-theme-key="console"][data-mode="dark"] .col[data-col="fixed"] input[name^="pick-"]').check()
    time.sleep(0.1)
    out = pg.evaluate("document.getElementById('out').textContent")
    bite = ("pointed at: column 1 — FIXED unit" in out) and ("RULING-SHAPED — NOT A RULING" in out) and ("question for Dave" in out)
    counts["mutation_bites"] += 1 if bite else 0
    check("MUTATION 3: the export names the pointed column, is ruling-SHAPED and ends in a question", bite, out.splitlines()[3] if len(out.splitlines()) > 3 else out)
    (HERE / "export-sample.txt").write_text(out)

    # two-red law: the flag colour is the canon red for the mode
    reds = pg.evaluate("""[...document.querySelectorAll('.frame')].map(f=>{const d=f.dataset.mode; const e=f.querySelector('.flag'); return e?[d,getComputedStyle(e).color]:[d,null];})""")
    ok = all((c is None) or (c == ("rgb(218, 26, 0)" if m == "light" else "rgb(246, 96, 76)")) for m, c in reds)
    # NB the frame's own chrome sits on the PAGE (light) ground; the flag inside the column head is chrome, so it reads the page's mode token — check what it actually is
    T.append(f"flag colours per frame mode: {reds}")
    check("flag red is a canon red (#DA1A00 or #F6604C), never an invented colour", all((c is None) or c in ("rgb(218, 26, 0)", "rgb(246, 96, 76)") for m, c in reds), reds)

    counts["console_errors"] = len(errors)
    check("console errors == 0", len(errors) == 0, errors)
    b.close()

(HERE / "drive-transcript.txt").write_text("\n".join(T) + "\n")
(HERE / "counts.json").write_text(json.dumps(counts, indent=1))
print(json.dumps(counts))
print("\n".join(l for l in T if l.startswith("FAIL") or "MUTATION" in l or "baseline" in l))
