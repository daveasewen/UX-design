"""W4b: patch _validate_geometry.py — part 2, the Python side (clauses, judge, model, selftest, main)."""
P = "knowledge/_validate_geometry.py"
s = open(P).read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:100])
    s = s.replace(old, new)

rep('''CLAUSES = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"]''',
    '''CLAUSES = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12"]
# CAUSE LEVERS (W4b #304): not clauses — each restores one repaired blind spot, so the selftest can
# prove the repair is load-bearing. X-scroll: scroll boxes read as R4b read them (inner-scroll
# content dropped by G7, a scroll box's start edge never a clip for G8). X-lone: the panel of a
# one-panel group is not measured by G6.
LEVERS = {"X-scroll": "legacyScroll", "X-lone": "legacyLone"}''')
rep('''    "G10": "stretched part",
}''', '''    "G10": "stretched part", "G11": "marks on every point", "G12": "chart lost in its box",
}''')
rep('''STRETCH_TOL = 0.10
''', '''STRETCH_TOL = 0.10
MARK_MAX = 12          # G11: the kit's marker proforma was authored at twelve points (dv-render-line.js)
LOST_MIN = 0.35        # G12: a chart's ink must cover at least 35% of its own box
''')

# judge: tile attribution + G6 leaves + G11 + G12
rep('''    def add(clause, where, measured, expected, fix, planted=None):
        if clause in off:
            return
        F.append({"clause": clause, "name": NAMES[clause],
                  "severity": "major" if clause in MAJOR else "minor", "width": width,
                  "where": where, "measured": measured, "expected": expected, "fix": fix,
                  "planted": planted})''',
'''    def add(clause, where, measured, expected, fix, planted=None, tile=None):
        if clause in off:
            return
        F.append({"clause": clause, "name": NAMES[clause],
                  "severity": "major" if clause in MAJOR else "minor", "width": width,
                  "where": where, "measured": measured, "expected": expected, "fix": fix,
                  "planted": planted, "tile": tile})''')
rep('''    # G6 dead space in a leaf tile
    for t in tiles:
        if t["group"] or not t.get("ink"):
            continue''', '''    # G6 dead space in a leaf tile — and in the lone panel of a one-panel group (W4b #304)
    for t in [t for t in tiles if not t["group"]] + list(model.get("leaves") or []):
        if not t.get("ink"):
            continue''')
rep('''                "Let the tile hug its content, fill it (a chart that fills its tile), or give the row a shorter tile.",
                planted=t.get("planted"))''', '''                "Let the tile hug its content, fill it (a chart that fills its tile), or give the row a shorter tile.",
                planted=t.get("planted"), tile=t.get("key"))''')
rep('''            "text never sits on other text", "Give the labels room (wrap, shorten, or move one).",
            planted=o.get("planted"))''', '''            "text never sits on other text", "Give the labels room (wrap, shorten, or move one).",
            planted=o.get("planted"), tile=o.get("tile"))''')
rep('''        add("G8", "'%s' in %s (clipped by %s)" % (c["text"], c["sel"], c["clipper"]),
            "glyph ink cut: %s%s%s" % (cuts, trap, "" if c.get("ink") else " (line-box reading: no ink metric)"),
            "no glyph cut by an overflow box",
            "Add `text-box-edge: text text` to a truncating label, or drop `overflow:hidden` / the fixed height.",
            planted=c.get("planted"))''', '''        if c.get("scroll"):
            add("G8", "'%s' in %s (cut at the start edge of scroll box %s)" % (c["text"], c["sel"], c["clipper"]),
                "glyph ink cut: %s — past the scroll origin, where no scrolling can reach it" % cuts,
                "no glyph cut by an overflow box",
                "Give the label room inside its box (a chart: fit the axis gutter to the widest label, data-pl-fit).",
                planted=c.get("planted"), tile=c.get("tile"))
            continue
        add("G8", "'%s' in %s (clipped by %s)" % (c["text"], c["sel"], c["clipper"]),
            "glyph ink cut: %s%s%s" % (cuts, trap, "" if c.get("ink") else " (line-box reading: no ink metric)"),
            "no glyph cut by an overflow box",
            "Add `text-box-edge: text text` to a truncating label, or drop `overflow:hidden` / the fixed height.",
            planted=c.get("planted"), tile=c.get("tile"))''')
rep('''            "Let the chart re-derive its geometry for the box (the fit engine) instead of preserveAspectRatio=\\"none\\"; for images use object-fit:cover.",
            planted=s.get("planted"))
    return F''', '''            "Let the chart re-derive its geometry for the box (the fit engine) instead of preserveAspectRatio=\\"none\\"; for images use object-fit:cover.",
            planted=s.get("planted"))
    # G11 marks on every point of a dense series (W4b #304)
    for d in model.get("dense") or []:
        what = "point markers" if d["kind"] == "marker" else "copies of the letter key '%s'" % d.get("letter", "")
        add("G11", "%s in '%s'" % (d["sel"], d["name"][:36]),
            "%d %s on one series of %d points" % (d["n"], what, d["points"]),
            "at most %d marks of one kind on one series (above that, one end key and no point markers)" % MARK_MAX,
            "Drop the per-point markers above %d points; key each series once, at the line's end." % MARK_MAX,
            planted=d.get("planted"), tile=d.get("tile"))
    # G12 a chart lost in its own box (W4b #304)
    for x in model.get("lost") or []:
        add("G12", "%s in '%s'" % (x["sel"], x["name"][:36]),
            "the chart's ink covers %d%% of its box (ink %gx%g in a %gx%g box)" % (round(100 * x["frac"]), x["iw"], x["ih"], x["w"], x["h"]),
            "a chart's ink covers at least %d%% of its own box" % round(100 * LOST_MIN),
            "Size the chart's box from the chart (a ring's box is its diameter), or put it in a tile of its own shape.",
            planted=x.get("planted"), tile=x.get("tile"))
    return F''')

# model: levers, inner-scroll walk
rep('''    def model(self, path, width):
        pg = self.b.new_page(viewport={"width": width, "height": 900})''', '''    def model(self, path, width, levers=()):
        pg = self.b.new_page(viewport={"width": width, "height": 900})''')
rep('''                        " window.scrollTo(0, 0); }")''', '''                        " window.scrollTo(0, 0); }")
            # …and every INNER scroll box too (an app shell scrolls its content box, not the window),
            # then return each to its origin (W4b #304)
            pg.evaluate(INNER_WALK_JS)''')
rep('''            return pg.evaluate(COLLECT_JS)
        finally:
            pg.close()''', '''            return pg.evaluate(COLLECT_JS, collect_opts(levers))
        finally:
            pg.close()''')
rep('''def _r(v):''', '''INNER_WALK_JS = r"""
async () => { for (const e of document.querySelectorAll('body *')) {
    const c = getComputedStyle(e); if (!/auto|scroll/.test(c.overflowY) || e.scrollHeight <= e.clientHeight + 50) continue;
    for (let y = 0; y < e.scrollHeight; y += 700) { e.scrollTop = y; await new Promise(r => requestAnimationFrame(() => r())); }
    e.scrollTop = 0; } }
"""


def collect_opts(levers=()):
    o = {"markMax": MARK_MAX, "lostMin": LOST_MIN}
    for lv in levers:
        o[LEVERS[lv]] = True
    return o


def _r(v):''')
rep('''def run_pages(h, paths, widths, off=(), stops=None, quiet=False):
    out = []
    for p in paths:
        t0 = time.time()
        rec = {"gate": "geometry", "page": os.path.relpath(p, ROOT), "widths": {}, "findings": []}
        for w in widths:
            m = h.model(p, w)''', '''def run_pages(h, paths, widths, off=(), stops=None, quiet=False):
    levers = [x for x in off if x in LEVERS]
    off = {x for x in off if x not in LEVERS}
    out = []
    for p in paths:
        t0 = time.time()
        rec = {"gate": "geometry", "page": os.path.relpath(p, ROOT), "widths": {}, "findings": []}
        for w in widths:
            m = h.model(p, w, levers)''')
rep('''            rec["widths"][str(w)] = {"docW": m["docW"], "docH": m["docH"], "walls": len(m["walls"]),
                                     "tiles": len(m["tiles"]), "tables": len(m["tables"]),''', '''            rec["widths"][str(w)] = {"docW": m["docW"], "docH": m["docH"], "walls": len(m["walls"]),
                                     "tiles": len(m["tiles"]), "leaves": len(m.get("leaves") or []),
                                     "leaf_tiles": sum(1 for t in m["tiles"] if not t["group"]) + len(m.get("leaves") or []),
                                     "tables": len(m["tables"]),''')
rep('''    bad = off - set(CLAUSES)''', '''    bad = off - set(CLAUSES) - set(LEVERS)''')
open(P, "w").write(s)
print("PY patched")
