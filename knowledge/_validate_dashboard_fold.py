#!/usr/bin/env python3
"""_validate_dashboard_fold.py — the dashboard's fold: the cap, the fold row, and the group-action rule.

Three readings of `knowledge/snippets/Template-dashboard-bento.reference.html`, rendered at 1440 x 900
(light), one browser, one page load:

1. THE CAP (W-307y8, s307-D67). Dave, by click, 2026-09-28, verbatim: 'Cap it at today's count so it
   cannot grow without you', answering 'How many signals may sit above the fold on a dashboard?'.
   Today's count was 26 signals of 9 kinds at 1440 (#251 BUILD dp08, finding 8). The census is the
   #251 one, unchanged (notes/_subreports/assets/2026-09-06-251-BUILD-dp08/_render251.py): every
   painted element whose top is above y=900 and whose background, text colour, fill or stroke
   resolves to a status or direction colour (--success --warning --error --info --up --down
   --spark-up --spark-down and the four tints); its carrier is the nearest `.status` or `.kpi-tile`.
   BLOCKING: more than CAP_SIGNALS elements above the fold fails. Lowering the cap is Dave's, by eye;
   raising it is a ruling. The number of kinds (carriers) is printed, not capped: the row caps signals.

2. THE FOLD ROW (W-307ya, s307-D71). Dave, by click, verbatim: 'Yes: add the fold row', answering
   'Should the first scoring tool gain a row for what sits above the fold?'. The first scoring tool is
   instrument A of the dashboard measures (richness 0-3 x4: rich, full, persistent, interactive;
   notes/_briefs/2026-09-05-246-lane-B-baseline-brief.md measure 7). The fold row is printed as FACTS
   — KPI tiles above the fold, the first chart's top and whether its whole canvas is above the fold,
   the signal count — and written with `--row <path>`. It is NOT scored 0-3: no scale for it is ruled.

3. THE GROUP ACTION RULE (s313-D29, #313 call 10). The group header is a band inside the group
   (`.tpl-group-band`, the default) or on the wall (`data-group-header="wall"`, the designer's option).
   The page's rule 'a group's action and a tile's action never repeat' came with option A; whether it
   still holds under the band is DAVE'S OPEN QUESTION. The template states the answer in ONE place:
   `data-action-repeat` on the wall (`never` | `allowed`). `never` (written tonight, the page's rule,
   pending his word): a band action whose accessible name equals an action's inside the same group
   fails. `allowed`: the rule is not read. Flipping the answer is that one attribute.

Exit 0 pass · 1 fail · 77 COULD-NOT-ASK (no playwright / no chromium). `--selftest` plants three
mutants (signals over the cap, a repeated action under `never`, the same repeat under `allowed`).
Renders run in the cloud with fallback fonts unless the seat's RENDER_SHELL is set: the seat render
with the real font is the reading of record.
"""
import json, os, re, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "snippets", "Template-dashboard-bento.reference.html")
CAP_SIGNALS = 26          # s307-D67 'today's count' — #251 BUILD dp08 finding 8: 26 elements / 9 carriers at 1440
FOLD_Y = 900
WIDTH = 1440

PROBE = r"""() => {
const names=['--success','--warning','--error','--info','--up','--down','--spark-up','--spark-down','--success-tint','--warning-tint','--error-tint','--info-tint'];
const p=document.createElement('span'); document.body.appendChild(p);
const rag={}; for(const n of names){p.style.color=`var(${n})`; const v=getComputedStyle(p).color; if(v&&v!=='rgba(0, 0, 0, 0)') rag[v]=n;}
p.remove();
const isRag=v=>v&&rag[v]!==undefined;
const FOLD=%d;
const sig=[]; for(const e of document.querySelectorAll('.tpl-page *, .tpl-header *, .sh-masthead *')){
  const b=e.getBoundingClientRect(); if(b.width===0||b.height===0) continue; const top=b.top+window.scrollY; if(top>=FOLD) continue;
  const s=getComputedStyle(e); const hits=[];
  if(isRag(s.backgroundColor)) hits.push('bg:'+rag[s.backgroundColor]);
  if(isRag(s.color) && e.childNodes.length && [...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())) hits.push('color:'+rag[s.color]);
  if(e instanceof SVGElement){ if(isRag(s.fill)&&s.fill!=='none') hits.push('fill:'+rag[s.fill]); if(isRag(s.stroke)&&s.stroke!=='none') hits.push('stroke:'+rag[s.stroke]); }
  if(hits.length){ const car=e.closest('.status, .kpi-tile')||e; sig.push({y:Math.round(top),hits,carrier:(car.getAttribute('aria-label')||car.innerText||'').replace(/\s+/g,' ').slice(0,44)}); }
}
const carriers=[...new Set(sig.map(s=>s.carrier))];
const tiles=[...document.querySelectorAll('.tpl-group-lead .kpi-tile')];
const tilesAbove=tiles.filter(t=>{const b=t.getBoundingClientRect(); return b.bottom+scrollY<=FOLD;}).length;
const svg=document.querySelector('.tpl-group-evidence svg');
const sb=svg?svg.getBoundingClientRect():null;
const name=a=>(a.getAttribute('aria-label')||a.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
const wall=document.querySelector('.tpl-wall');
const repeatRule=wall?(wall.getAttribute('data-action-repeat')||'(unset)'):'(no wall)';
const groups=[...document.querySelectorAll('.tpl-group')].map(g=>{
  const band=g.querySelector(':scope > .c-bento__grid > .tpl-group-band');
  const bandActs=band?[...band.querySelectorAll('a, button')].map(name):[];
  const tileActs=[...g.querySelectorAll(':scope > .c-bento__grid > .c-bento__tile:not(.tpl-group-band) a, :scope > .c-bento__grid > .c-bento__tile:not(.tpl-group-band) button')].map(name);
  const bb=band?band.getBoundingClientRect():null;
  return {label:g.getAttribute('aria-label'), placement:band?(g.getAttribute('data-group-header')||'band'):'(none)',
          bandH:bb?Math.round(bb.height):null, bandActs, repeats:bandActs.filter(a=>tileActs.includes(a))};
});
return {signals:sig.length, kinds:carriers.length, carriers, tilesAbove, tiles:tiles.length,
        chartTop:sb?Math.round(sb.top+scrollY):null, chartWhole:sb?(sb.bottom+scrollY)<=FOLD:null,
        docH:document.documentElement.scrollHeight, repeatRule, groups};
}""" % FOLD_Y


def _browser():
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        print("COULD-NOT-ASK: playwright is not installed (the CI render job installs it)")
        sys.exit(77)
    return sync_playwright


def measure(html_path, sp):
    kw = {"args": ["--no-sandbox"]}
    if os.environ.get("RENDER_SHELL"):
        kw["executable_path"] = os.environ["RENDER_SHELL"]
    b = sp.chromium.launch(**kw)
    try:
        pg = b.new_page(viewport={"width": WIDTH, "height": FOLD_Y})
        pg.goto("file://" + html_path)
        pg.wait_for_timeout(600)
        return pg.evaluate(PROBE)
    finally:
        b.close()


def verdict(m):
    fails = []
    if m["signals"] > CAP_SIGNALS:
        fails.append("CAP: %d signals above the fold at %d, cap %d (s307-D67)" % (m["signals"], WIDTH, CAP_SIGNALS))
    if m["repeatRule"] == "never":
        for g in m["groups"]:
            if g["repeats"]:
                fails.append("REPEAT: group '%s' header and a tile both carry %s (data-action-repeat=never, s313-D29 open)"
                             % (g["label"], g["repeats"]))
    return fails


def report(m, fails):
    print("dashboard fold @%dx%d · signals %d of cap %d · kinds %d · KPI tiles above %d/%d · first chart top %s, whole canvas above: %s"
          % (WIDTH, FOLD_Y, m["signals"], CAP_SIGNALS, m["kinds"], m["tilesAbove"], m["tiles"], m["chartTop"], m["chartWhole"]))
    print("  carriers: %s" % m["carriers"])
    print("  group headers (action rule: %s): %s" % (m["repeatRule"],
          "; ".join("%s=%s h%s acts%s" % (g["label"], g["placement"], g["bandH"], g["bandActs"]) for g in m["groups"])))
    for f in fails:
        print("  FAIL " + f)
    print("PASS" if not fails else "FAIL (%d)" % len(fails))


def fold_row(m):
    return {"$row": "fold — instrument A's fifth row (W-307ya, s307-D71: 'Yes: add the fold row'). FACTS, not a 0-3 score: no scale is ruled.",
            "$page": "knowledge/snippets/Template-dashboard-bento.reference.html",
            "$at": "%dx%d light" % (WIDTH, FOLD_Y),
            "$render": "seat chromium (RENDER_SHELL)" if os.environ.get("RENDER_SHELL") else "playwright chromium, fallback fonts (not the reading of record)",
            "kpi_tiles_above_fold": "%d/%d" % (m["tilesAbove"], m["tiles"]),
            "first_chart_top": m["chartTop"], "first_chart_whole_above_fold": m["chartWhole"],
            "signals_above_fold": m["signals"], "signal_kinds_above_fold": m["kinds"], "cap": CAP_SIGNALS,
            "doc_height": m["docH"]}


def selftest(sp):
    src = open(PAGE, encoding="utf-8").read()
    ok = True
    tmpd = tempfile.mkdtemp(prefix="fold-selftest-")

    def run(label, html, want_fail_kind):
        nonlocal ok
        p = os.path.join(os.path.dirname(PAGE), ".fold-selftest-%d.html" % os.getpid())
        open(p, "w", encoding="utf-8").write(html)
        try:
            m = measure(p, sp)
        finally:
            os.remove(p)
        kinds = sorted({f.split(":")[0] for f in verdict(m)})
        good = kinds == want_fail_kind
        ok &= good
        print("  %s %s · got %s want %s" % ("ok " if good else "RED", label, kinds or ["PASS"], want_fail_kind or ["PASS"]))

    run("the page as it stands", src, [])
    # M1 — signals over the cap: five more status chips in the lead group's first tile (above the fold)
    chip = '<span class="status err" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">Planted</span></span>'
    anchor = '<p class="lbl16 t-cm-caption">Closing balance</p>'
    assert src.count(anchor) == 1
    run("M1 · 14 planted chips push signals over the cap", src.replace(anchor, anchor + chip * 14), ["CAP"])
    # M2 — the Position band gains the tile's own 'View all' under data-action-repeat=never
    band_h = '<h2 id="tpl-gh-position" class="t-cm-section-label">Position</h2>'
    assert src.count(band_h) == 1
    planted = src.replace(band_h, band_h + '\n                  <a class="tpl-link t-cm-caption" href="#">View all</a>')
    run("M2 · a repeated 'View all' under never", planted, ["REPEAT"])
    # M3 — the same plant, the one attribute flipped to allowed: the rule is not read
    run("M3 · the same plant under allowed (the one-line flip)",
        planted.replace('data-action-repeat="never"', 'data-action-repeat="allowed"'), [])
    print("SELFTEST " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    argv = sys.argv[1:]
    sp = _browser()
    with sp() as p:
        if "--selftest" in argv:
            return selftest(p)
        m = measure(PAGE, p)
    fails = verdict(m)
    report(m, fails)
    if "--row" in argv:
        out = argv[argv.index("--row") + 1]
        open(out, "w", encoding="utf-8").write(json.dumps(fold_row(m), indent=2, ensure_ascii=False) + "\n")
        print("fold row written: %s" % out)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
