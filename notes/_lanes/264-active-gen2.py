#!/usr/bin/env python3
"""#264 second pass — the TWO-BODY class Dave's five rejections named.

Why v1 failed: a rear body cut by a front body (overlap exclusion) has no closed outline of its own,
so 'fill every contour' filled the front and left the rear as a band.
v2: the silhouette is what the EXTERIOR cannot reach. Ink ∪ (front silhouette grown by the gap)
seals the rear's opening; every hole of the exterior region is a body. Then:
  A = (S_all − interior ink) ∪ FrontSil − Gap − FrontDetail
Front = the closed-ring component whose sealing gains the most silhouette area (the rear gains
area when the front seals it; the front gains none).
"""
import os, sys, glob, json, importlib
import skia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
g = importlib.import_module("264-active-gen")
W = g.W_BORDER; GAP = 1.0; CANVAS = skia.Rect(-2, -2, 20, 20)

def area(p, res=16):
    if p is None or p.isEmpty(): return 0.0
    surf = skia.Surface(18*res, 18*res); c = surf.getCanvas(); c.clear(skia.ColorWHITE); c.scale(res, res)
    c.drawPath(p, skia.Paint(Color=skia.ColorBLACK, AntiAlias=False))
    img = surf.makeImageSnapshot(); arr = img.toarray()
    return float((arr[..., 0] < 128).sum()) / (res*res)

def dilate(P, r):
    paint = skia.Paint(); paint.setStyle(skia.Paint.kStroke_Style); paint.setStrokeWidth(2*r); paint.setStrokeJoin(skia.Paint.kRound_Join)
    ring = skia.Path(); paint.getFillPath(P, ring); return skia.Op(P, ring, skia.kUnion_PathOp)

def components(L):
    """Group contours into (outer, [holes]) by containment. Returns list of dicts."""
    cs = [skia.Simplify(c) or c for c in g.contours(L)]
    for c in cs: c.setFillType(skia.PathFillType.kWinding)
    def fill(c): f = skia.Path(c); f.setFillType(skia.PathFillType.kWinding); return f
    fills = [fill(c) for c in cs]
    def inside(i, j):  # contour i inside contour j
        b = cs[i].getBounds(); pt = (b.left() + b.width()*0.5, b.top())  # a boundary point of i
        return i != j and cs[j].getBounds().contains(b) and fills[j].contains(pt[0]+1e-3, pt[1]+1e-3)
    depth = [sum(1 for j in range(len(cs)) if inside(i, j)) for i in range(len(cs))]
    comps = []
    for i, d in enumerate(depth):
        if d % 2 == 0:
            holes = [cs[j] for j in range(len(cs)) if depth[j] == d+1 and inside(j, i)]
            comps.append(dict(outer=cs[i], holes=holes, sil=fills[i], ink=skia.Op(L, fills[i], skia.kIntersect_PathOp)))
    return comps

def exterior_holes(ink):
    """Silhouette = everything the exterior cannot reach."""
    canvas = skia.Path(); canvas.addRect(CANVAS)
    P = skia.Op(canvas, ink, skia.kDifference_PathOp)
    cs = g.contours(skia.Simplify(P) or P)
    S = skia.Path()
    for c in cs:
        b = c.getBounds()
        if b.width() > 20 and b.height() > 20: continue   # the canvas boundary itself
        f = skia.Path(c); f.setFillType(skia.PathFillType.kWinding)
        S = f if S.isEmpty() else skia.Op(S, f, skia.kUnion_PathOp)
    return S

MIN_GAIN = 3.0   # px² — a ring whose sealing gains less than this is detail, not a front body

def close(P, r):
    return g.erode(dilate(P, r), r)

def derive2(L):
    comps = components(L)
    # open bands (no hole) that sit in no other silhouette are BODIES drawn open (avatar shoulders):
    # their silhouette is the band closed across its opening — a morphological close at half its size.
    for c in comps:
        if not c["holes"]:
            b = c["outer"].getBounds()
            in_other = any(o is not c and o["sil"].contains(b.centerX(), b.centerY()) for o in comps)
            if not in_other and min(b.width(), b.height()) > 4:
                c["sil"] = close(c["sil"], min(b.width(), b.height()) / 2)
                c["open"] = True
    base_area = area(exterior_holes(L))
    fronts = []
    for c in [c for c in comps if c["holes"]]:
        sealed = exterior_holes(skia.Op(L, dilate(c["sil"], GAP), skia.kUnion_PathOp))
        gain = area(sealed) - base_area
        if gain > MIN_GAIN: fronts.append((gain, c))
    fronts.sort(key=lambda t: -t[0])
    front_sil = skia.Path(); front_ink = skia.Path()
    for _, c in fronts:
        front_sil = skia.Op(front_sil, c["sil"], skia.kUnion_PathOp); front_ink = skia.Op(front_ink, c["ink"], skia.kUnion_PathOp)
    seal = skia.Op(L, dilate(front_sil, GAP), skia.kUnion_PathOp)
    for c in comps:
        if c.get("open"): seal = skia.Op(seal, c["sil"], skia.kUnion_PathOp)
    S_all = exterior_holes(seal)
    S_all = skia.Op(S_all, dilate(front_sil, GAP), skia.kDifference_PathOp)   # rear + others, minus the fronts' gapped discs
    B = skia.Op(S_all, g.erode(S_all, W), skia.kDifference_PathOp)
    I = skia.Op(skia.Op(L, front_ink, skia.kDifference_PathOp), B, skia.kDifference_PathOp)   # rear interior ink
    A = skia.Op(S_all, I, skia.kDifference_PathOp)
    if not front_sil.isEmpty():
        FB = skia.Op(front_sil, g.erode(front_sil, W), skia.kDifference_PathOp)
        FI = skia.Op(front_ink, FB, skia.kDifference_PathOp)
        A = skia.Op(A, skia.Op(front_sil, FI, skia.kDifference_PathOp), skia.kUnion_PathOp)
    return A, [round(gn, 1) for gn, _ in fronts]

if __name__ == "__main__":
    slugs = {os.path.basename(f)[:-4]: f for f in glob.glob(os.path.join(g.ICONS, "**", "*.svg"), recursive=True)}
    res = {}
    for name in sys.argv[1:]:
        L = g.load(open(slugs[name]).read())
        A, gain = derive2(L)
        res[name] = dict(line=open(slugs[name]).read(), real=open(slugs[name+'-active']).read() if name+'-active' in slugs else None, a=g.svg(A), gain=gain)
        print(name, "gain", gain)
    json.dump(res, open(os.path.join(g.HERE, "264-active-gen2.json"), "w"))
