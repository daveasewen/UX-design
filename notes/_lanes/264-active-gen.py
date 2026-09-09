#!/usr/bin/env python3
"""#264 EXPERIMENT — derive an `-active` (filled) glyph from a line glyph, geometrically.

Rule read off the library's own pairs (16 rendered at #264):
  S  = silhouette   = union of every contour of the line ink, filled            (outer shape, solid)
  B  = border band  = S minus erode(S, w)                                       (the outline stroke's own ink)
  I  = interior ink = L minus B                                                 (detail drawn INSIDE the shape)
  K  = knockout     = erode(I, t)                                               (the detail, thinner, as a hole)
  A  = active       = S minus K
Two variants are emitted: A1 as above; A2 additionally EMPTIES any region I fully encloses
(settings' hub) — the pairs disagree on that, so both are shown and the eye decides.
Curves are preserved: every op is a Skia path op, nothing is rasterised.
"""
import os, re, sys, glob, json
import skia
from svgpathtools import parse_path, Line, CubicBezier, QuadraticBezier, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, "..", "..", "knowledge", "assets", "icons")
W_BORDER = 1.25   # library line weight is 1.2px on an 18px grid
T_THIN   = 0.0    # the human knockouts sit at the line weight or heavier — calibrated at #264 (0.12 read too thin)

def to_skia(d, evenodd):
    p = skia.Path()
    for sub in parse_path(d).continuous_subpaths():
        s = sub[0].start; p.moveTo(s.real, s.imag)
        for seg in sub:
            e = seg.end
            if isinstance(seg, Line): p.lineTo(e.real, e.imag)
            elif isinstance(seg, CubicBezier): p.cubicTo(seg.control1.real, seg.control1.imag, seg.control2.real, seg.control2.imag, e.real, e.imag)
            elif isinstance(seg, QuadraticBezier): p.quadTo(seg.control.real, seg.control.imag, e.real, e.imag)
            elif isinstance(seg, Arc): p.arcTo(seg.radius.real, seg.radius.imag, seg.rotation, skia.Path.kLarge_ArcSize if seg.large_arc else skia.Path.kSmall_ArcSize, skia.PathDirection.kCW if seg.sweep else skia.PathDirection.kCCW, e.real, e.imag)
        if sub.isclosed() or abs(sub[-1].end - sub[0].start) < 1e-6: p.close()
    p.setFillType(skia.PathFillType.kEvenOdd if evenodd else skia.PathFillType.kWinding)
    return p

def load(svg_text):
    ink = None
    for m in re.finditer(r'<path\b([^>]*)>', svg_text):
        attrs = m.group(1); d = re.search(r'\bd="([^"]+)"', attrs)
        if not d: continue
        eo = 'evenodd' in attrs
        p = to_skia(d.group(1), eo)
        ink = p if ink is None else skia.Op(ink, p, skia.kUnion_PathOp)
    return skia.Simplify(ink)

def contours(p):
    out, cur = [], None
    it = skia.Path.Iter(p, False)
    while True:
        verb, pts = it.next()
        if verb == skia.Path.kDone_Verb: break
        if verb == skia.Path.kMove_Verb:
            if cur is not None: out.append(cur)
            cur = skia.Path(); cur.moveTo(pts[0])
        elif verb == skia.Path.kLine_Verb: cur.lineTo(pts[1])
        elif verb == skia.Path.kQuad_Verb: cur.quadTo(pts[1], pts[2])
        elif verb == skia.Path.kConic_Verb: cur.conicTo(pts[1], pts[2], it.conicWeight())
        elif verb == skia.Path.kCubic_Verb: cur.cubicTo(pts[1], pts[2], pts[3])
        elif verb == skia.Path.kClose_Verb: cur.close()
    if cur is not None: out.append(cur)
    return out

def silhouette(L):
    S = skia.Path()
    for c in contours(L):
        c.setFillType(skia.PathFillType.kWinding)
        f = skia.Simplify(c)
        S = f if S.isEmpty() else skia.Op(S, f, skia.kUnion_PathOp)
    return S

def erode(P, r):
    if P is None or P.isEmpty() or r <= 0: return P
    paint = skia.Paint(); paint.setStyle(skia.Paint.kStroke_Style); paint.setStrokeWidth(2*r); paint.setStrokeJoin(skia.Paint.kRound_Join)
    ring = skia.Path(); paint.getFillPath(P, ring)
    return skia.Op(P, ring, skia.kDifference_PathOp)

def derive(L):
    S = silhouette(L)
    B = skia.Op(S, erode(S, W_BORDER), skia.kDifference_PathOp)
    I = skia.Op(L, B, skia.kDifference_PathOp)
    K = erode(I, T_THIN)
    A1 = skia.Op(S, K, skia.kDifference_PathOp)
    # A2: empty every region the interior ink encloses (its own silhouette)
    K2 = skia.Op(silhouette(I), skia.Path(), skia.kUnion_PathOp) if not I.isEmpty() else I
    K2 = erode(K2, T_THIN)
    A2 = skia.Op(S, K2, skia.kDifference_PathOp)
    return S, I, A1, A2

def to_d(p):
    out = []
    it = skia.Path.Iter(p, False)
    f = lambda v: ('%.3f' % v).rstrip('0').rstrip('.')
    while True:
        verb, pts = it.next()
        if verb == skia.Path.kDone_Verb: break
        if verb == skia.Path.kMove_Verb: out.append(f'M{f(pts[0].x())} {f(pts[0].y())}')
        elif verb == skia.Path.kLine_Verb: out.append(f'L{f(pts[1].x())} {f(pts[1].y())}')
        elif verb == skia.Path.kQuad_Verb: out.append(f'Q{f(pts[1].x())} {f(pts[1].y())} {f(pts[2].x())} {f(pts[2].y())}')
        elif verb == skia.Path.kConic_Verb:
            # conic → two quads (exact enough at icon scale)
            q = skia.Path(); q.moveTo(pts[0]); q.conicTo(pts[1], pts[2], it.conicWeight())
            pow2 = skia.Path.ConvertConicToQuads(pts[0], pts[1], pts[2], it.conicWeight(), 1)
            for i in range(0, len(pow2)-1, 2):
                out.append(f'Q{f(pow2[i+1].x())} {f(pow2[i+1].y())} {f(pow2[i+2].x())} {f(pow2[i+2].y())}')
        elif verb == skia.Path.kCubic_Verb: out.append(f'C{f(pts[1].x())} {f(pts[1].y())} {f(pts[2].x())} {f(pts[2].y())} {f(pts[3].x())} {f(pts[3].y())}')
        elif verb == skia.Path.kClose_Verb: out.append('Z')
    return ' '.join(out)

def svg(p):
    return f'<svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="{to_d(p)}" fill="currentColor"/></svg>'

if __name__ == "__main__":
    slugs = {os.path.basename(f)[:-4]: f for f in glob.glob(os.path.join(ICONS, "**", "*.svg"), recursive=True)}
    res = {}
    for name in sys.argv[1:]:
        L = load(open(slugs[name]).read())
        S, I, A1, A2 = derive(L)
        res[name] = dict(line=open(slugs[name]).read(), real=open(slugs[name+'-active']).read() if name+'-active' in slugs else None,
                         a1=svg(A1), a2=svg(A2))
    json.dump(res, open(os.path.join(HERE, "264-active-gen.json"), "w"))
    print("derived", len(res))
