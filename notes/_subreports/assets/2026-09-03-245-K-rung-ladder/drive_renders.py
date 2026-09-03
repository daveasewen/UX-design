#!/usr/bin/env python3
"""Lane K (#245) — render-proof of reviews/RUNG-LADDER-2026-09-03-v1.html.

Drives the page through page.goto("file://…") — NEVER set_content. Reads the page's own live
measurement (window.__K — what getComputedStyle resolved — and window.__Kprobe, the content heights
from the hidden rung-0 probe), asserts each ladder's claim per column per theme per mode, then two
mutation arms. Writes, beside this script:
  drive-transcript.txt   every assertion, one per line, PASS/FAIL, with the measured value
  measurements.json      the baseline __K table (fit view) + __Kprobe
  one-to-one.json        the same at 1:1 (the zoom caveat, declared with its size)
  counts.json            the counts quoted in the report
  render-<theme>-<mode>.png   one per frame (fit view) · col-<A..D>-mono-light-1to1.png · export-sample.txt

Usage (sandbox): LD_LIBRARY_PATH=<dir with libXdamage.so.1> python3 drive_renders.py
"""
import json, pathlib, time
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
PAGE = REPO / "reviews/RUNG-LADDER-2026-09-03-v1.html"
ledger = json.loads((HERE / "splice-ledger.json").read_text())
LAD = {L["id"]: L for L in ledger["ladders"]}
GAP = ledger["gap"]

T = []
counts = dict(assertions=0, fails=0, mutation_arms=0, mutation_bites=0, console_errors=0, renders=0)


def check(name, ok, value=""):
    counts["assertions"] += 1
    if not ok:
        counts["fails"] += 1
    T.append(f"{'PASS' if ok else 'FAIL'}  {name}  ->  {value}")
    return ok


def near(a, b, tol=0.6):
    return abs(a - b) <= tol


def assert_baseline(res, tag):
    """The per-render assertions — each column's own claim, in its own words. Returns FAILs contributed."""
    before = counts["fails"]
    for r in res:
        L = LAD[r["ladder"]]
        k = f"[{tag}] {r['theme']}/{r['mode']}/{L['id']}"
        c = r["content"]
        check(f"{k} outer wall grid-auto-rows is auto (level HELD)", r["outerAutoRows"] == "auto", r["outerAutoRows"])
        check(f"{k} 6-column band", r["cols"] == 6, r["cols"])
        G = {g["group"]: g for g in r["groups"]}
        for key in ("kpi", "chart", "rail"):
            g = G[key]; rung = L[key]; gk = f"{k} {key}"
            check(f"{gk} the ruled model: computed grid-auto-rows == minmax({rung}px, auto)", g["autoRows"] == f"minmax({rung}px, auto)", g["autoRows"])
            check(f"{gk} every row track >= rung (a floor never goes under)", all(t >= rung - 0.6 for t in g["tracks"]), g["tracks"])
            check(f"{gk} no tile overruns its row", g["tilesOverflowing"] == 0, g["tilesOverflowing"])
        kpi, chart, rail = G["kpi"], G["chart"], G["rail"]
        # the claim each column makes in its header sentence
        if L["id"] == "A":
            check(f"{k} A: KPI rows carry AIR — rows == 196 and 196 > content", all(near(t, 196) for t in kpi["tracks"]) and 196 > c["kpi"], f"rows {kpi['tracks']} vs content {c['kpi']}")
            check(f"{k} A: rail rung 184 is under content — rows lifted past it", all(t > 184 + 1 for t in rail["tracks"]) and c["rail"] > 184, f"rows {rail['tracks']} vs content {c['rail']}")
            check(f"{k} A: chart row is set by the rail stack, not by 380", chart["tracks"][0] > 380 + 1 and near(chart["tracks"][0], sum(rail["tracks"]) + GAP, 1.5), f"chart {chart['tracks']} rail-sum+gap {sum(rail['tracks']) + GAP:.1f}")
        elif L["id"] == "B":
            check(f"{k} B: every rung is under its content (no rung shows)", L["kpi"] < c["kpi"] and L["chart"] < c["chart"] and L["rail"] < c["rail"], f"rungs {L['kpi']}/{L['chart']}/{L['rail']} content {c['kpi']}/{c['chart']}/{c['rail']}")
            check(f"{k} B: KPI rows == content (within 1px)", near(max(kpi["tracks"]), c["kpi"], 1.0), f"rows {kpi['tracks']} content {c['kpi']}")
            check(f"{k} B: rail rows == content (within 1px)", near(max(rail["tracks"]), c["rail"], 1.0), f"rows {rail['tracks']} content {c['rail']}")
        elif L["id"] == "C":
            check(f"{k} C: rungs are content rounded DOWN to 8px on this machine (page's own check)", r.get("derivationHolds") is True, r.get("derivationHolds"))
            check(f"{k} C: the floor lifts KPI and rail rows at most 8px past the rung", all(t - L["kpi"] <= 8.6 for t in kpi["tracks"]) and all(t - L["rail"] <= 8.6 for t in rail["tracks"]), f"kpi {kpi['tracks']} rail {rail['tracks']}")
            check(f"{k} C: the rail's two rows are within 8px of each other (near level)", abs(rail["tracks"][0] - rail["tracks"][1]) <= 8.6, rail["tracks"])
        elif L["id"] == "D":
            check(f"{k} D: rungs are content rounded UP and chart == 2×rail + {GAP} (page's own check)", r.get("derivationHolds") is True and L["chart"] == 2 * L["rail"] + GAP, f"{L['kpi']}/{L['chart']}/{L['rail']}")
            check(f"{k} D: every row is exactly its rung — the floor idles", all(near(t, L["kpi"]) for t in kpi["tracks"]) and all(near(t, L["rail"]) for t in rail["tracks"]) and near(chart["tracks"][0], L["chart"]), f"kpi {kpi['tracks']} chart {chart['tracks']} rail {rail['tracks']}")
            check(f"{k} D: chart closes level with the rail stack — dead band 0 in both", chart["deadBand"] <= 0.6 and rail["deadBand"] <= 0.6 and near(chart["tracks"][0], sum(rail["tracks"]) + GAP, 0.6), f"chart {chart['tracks']} rail {rail['tracks']} dead {chart['deadBand']}/{rail['deadBand']}")
    return counts["fails"] - before


with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append(str(e)))
    url = PAGE.as_uri()
    T.append(f"goto {url}")
    pg.goto(url)
    pg.wait_for_function("window.__K && window.__K.length===32")
    pg.evaluate("document.fonts.ready.then(()=>window.__Kmeasure())")
    time.sleep(0.4)
    res = pg.evaluate("window.__Kmeasure()")
    probe = pg.evaluate("window.__Kprobe")
    (HERE / "measurements.json").write_text(json.dumps(dict(renders=res, probe=probe), indent=1))
    counts["renders"] = len(res)
    check("32 renders measured (4 themes × 2 modes × 4 ladders)", len(res) == 32, len(res))
    ff = pg.evaluate("getComputedStyle(document.querySelector('.tpl-group [class*=t-cm-figure], .tpl-group [class*=t-ed-]')).fontFamily")
    check("type.css composites resolve (font-family carries Univers Next)", "Univers" in ff, ff)
    same = pg.evaluate("""[...document.querySelectorAll('.frame')].map(f=>{const h=[...f.querySelectorAll('.cn-template-dashboard-bento')].map(e=>e.innerHTML); return h.every(x=>x===h[0]);})""")
    check("wall markup byte-identical across the 4 columns + probe of every frame (8 frames)", all(same), same)
    src = PAGE.read_text(encoding="utf-8")
    ext = [t for t in ('src="', 'href="../', "@import", "http://", "https://", "url(") if t in src]
    check("zero external references in the file", not ext, ext or "none")
    check("type.css spliced verbatim (byte-equal to knowledge/canon/type.css)", (REPO / "knowledge/canon/type.css").read_text(encoding="utf-8") in src, f"{len(src):,} B file")
    check("the probe's content heights agree across all 8 frames (theme does not move the content)", len({json.dumps(v, sort_keys=True) for v in probe.values()}) == 1, probe["mono/light"])
    check("build-time CONTENT constants == this run's probe (mono/light), within 1px", all(abs(probe["mono/light"][k] - ledger["content"][k]) < 1 for k in ("kpi", "chart", "rail")), f"probe {probe['mono/light']} vs built {ledger['content']}")
    T.append(f"probe content heights (rung 0, no stretch): {probe['mono/light']}")

    fails0 = assert_baseline(res, "baseline-fit")
    T.append(f"baseline (fit view): {fails0} FAIL")

    # 1:1 — the zoom caveat measured
    pg.check('input[name="view"][value="one"]')
    time.sleep(0.4)
    res1 = pg.evaluate("window.__Kmeasure()")
    (HERE / "one-to-one.json").write_text(json.dumps(res1, indent=1))
    fails1 = assert_baseline(res1, "baseline-1to1")
    T.append(f"baseline (1:1 view): {fails1} FAIL")
    diffs = [abs(x - y) for a, c in zip(res, res1) for i in range(3) for x, y in zip(a["groups"][i]["tracks"], c["groups"][i]["tracks"])]
    check("fit-vs-1:1 track deltas == 0 (the fit view is a transform of the 1:1 layout, not a zoom — first run with zoom measured 8.0px)", max(diffs) == 0, f"max |Δ| {max(diffs):.1f}px over {len(diffs)} tracks")
    T.append(f"fit-vs-1:1: max |Δ| {max(diffs):.1f}px over {len(diffs)} tracks")
    for L in ("A", "B", "C", "D"):
        pg.locator(f'.frame[data-theme-key="mono"][data-mode="light"] .col[data-ladder="{L}"]').screenshot(path=str(HERE / f"col-{L}-mono-light-1to1.png"))
    pg.check('input[name="view"][value="fit"]')
    time.sleep(0.3)
    pg.evaluate("window.__Kmeasure()")
    for th in ("mono", "supercharge", "legacy", "console"):
        for md in ("light", "dark"):
            pg.locator(f'.frame[data-theme-key="{th}"][data-mode="{md}"]').screenshot(path=str(HERE / f"render-{th}-{md}.png"))

    # the theme filter hides the two non-required themes and keeps the measurement whole
    pg.check('input[name="themes"][value="two"]')
    time.sleep(0.2)
    vis = pg.evaluate("[...document.querySelectorAll('.frame')].map(f=>[f.dataset.themeKey, getComputedStyle(f).display!=='none'])")
    check("themes=two shows exactly mono + supercharge (4 frames), hides legacy + console", all(v == (t in ("mono", "supercharge")) for t, v in vis), vis)
    pg.check('input[name="themes"][value="all"]')
    time.sleep(0.2)

    # two-red law on the chrome flag colour (the page paints no flag at baseline — inject one to read the token)
    reds = pg.evaluate("""[...document.querySelectorAll('.frame')].map(f=>{const e=document.createElement('span'); e.className='flag'; f.appendChild(e); const c=getComputedStyle(e).color; e.remove(); return [f.dataset.mode,c];})""")
    check("flag red is a canon red (#DA1A00 on the page's white ground; #F6604C if dark), never invented", all(c in ("rgb(218, 26, 0)", "rgb(246, 96, 76)") for _, c in reds), sorted(set(c for _, c in reds)))

    # ---- MUTATION 1 (CSS): column C's rail rung secretly swapped to 96px behind the header's numbers
    counts["mutation_arms"] += 1
    pg.add_style_tag(content='.col[data-ladder="C"] .cn-template-dashboard-bento .c-bento.tpl-group-rail{--bento-row-unit:96px !important;}')
    time.sleep(0.2)
    rm = pg.evaluate("window.__Kmeasure()")
    bites = assert_baseline([r for r in rm if r["ladder"] == "C"], "MUTATION-1 C rail=96 behind the label")
    counts["mutation_bites"] += bites
    counts["fails"] -= bites
    T.append(f"MUTATION 1 (column C's rail rung silently 96px): {bites} assertions bit (expected > 0)")
    check("MUTATION 1 bites (>0 column-C assertions fail when the CSS disagrees with the header)", bites > 0, bites)
    pg.evaluate("[...document.querySelectorAll('style')].pop().remove()")
    time.sleep(0.2)
    rr = pg.evaluate("window.__Kmeasure()")
    check("MUTATION 1 reverted — column C passes again", assert_baseline([r for r in rr if r["ladder"] == "C"], "post-M1") == 0, "0 FAIL")

    # ---- MUTATION 2 (control): point at column C in supercharge/dark — the export must name it and stay a question
    counts["mutation_arms"] += 1
    pg.locator('.frame[data-theme-key="supercharge"][data-mode="dark"] .col[data-ladder="C"] input[name^="pick-"]').check()
    time.sleep(0.1)
    out = pg.evaluate("document.getElementById('out').textContent")
    lines = out.splitlines()
    bite = (f"pointed at: column C — Content-fitted — KPI {LAD['C']['kpi']} / chart {LAD['C']['chart']} / rail {LAD['C']['rail']}" in out) and out.startswith("RULING-SHAPED — NOT A RULING") and any(l.startswith("question for Dave:") and l.rstrip().endswith("?") for l in lines)
    counts["mutation_bites"] += 1 if bite else 0
    check("MUTATION 2: the export names the pointed column with its three numbers, is ruling-SHAPED, and its question line ends in '?'", bite, lines[3] if len(lines) > 3 else out)
    (HERE / "export-sample.txt").write_text(out)
    n_checked = pg.evaluate("[...document.querySelectorAll('input[name^=\"pick-\"]:checked')].length")
    check("one pick is page-wide: every frame's column C radio is checked (8), no other", n_checked == 8 and pg.evaluate("[...document.querySelectorAll('input[name^=\"pick-\"]:checked')].every(i=>i.value==='C')"), n_checked)

    counts["console_errors"] = len(errors)
    check("console errors == 0", len(errors) == 0, errors)
    b.close()

(HERE / "drive-transcript.txt").write_text("\n".join(T) + "\n")
(HERE / "counts.json").write_text(json.dumps(counts, indent=1))
print(json.dumps(counts))
print("\n".join(l for l in T if not l.startswith("PASS") and not l.startswith("FAIL  [MUTATION")))
