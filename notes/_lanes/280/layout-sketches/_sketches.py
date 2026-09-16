#!/usr/bin/env python3
"""Lane LS (#280) — the four layout SKETCHES, rendered as SVG from the REAL node data.

Not a build of the explorer: nothing under knowledge/ is read for anything but data, and nothing
outside notes/_lanes/280/layout-sketches/ is written. The node set, the edge set and every count
come from the page's own draw predicate (lane LY's `sim.py`, the EX2 §3 re-implementation) over the
KG embedded in notes/_KG-EXPLORER.html, with every family chip ON — the three views and THE
CONSTITUTION at once, which is the picture the layers question is about.

Coordinates are the builder's own: `x,y` (the 2D force layout) and `x3,y3,z3` (the 3D force layout).
No new layout is solved here; each sketch is a PROJECTION of what the file already carries.

  python3 notes/_lanes/280/layout-sketches/_sketches.py     # writes the SVGs + facts.json
"""
import json, math, os, random, sys, collections

ROOT = os.environ.get('LS_ROOT') or '/sessions/intelligent-serene-curie/mnt/UX-design'
HERE = os.path.join(ROOT, 'notes/_lanes/280/layout-sketches')
sys.path.insert(0, os.path.join(ROOT, 'notes/_lanes/280/layout'))
import sim  # noqa: E402

PAGE = os.path.join(ROOT, 'notes/_KG-EXPLORER.html')
ALLON = dict(sim.DEFAULT_FAM)
for c in ('assets', 'guidelines', 'guidelinerules', 'uxprinciples', 'governance'):
    ALLON[c] = 1

# ---------------------------------------------------------------- palette (the explorer's own)
LIGHT = dict(
    bg='#FFFFFF', ink='#111111', ink2='#555555', ink3='#8A8A8A', rule='#E3E3E3',
    t=dict(component='#DA1A00', snippet='#7A7A7A', pattern='#1F4FBF', context='#0E8A5F',
           ruling='#111111', session='#5E5E5E', artefact='#8A7A66', evidence='#A99C8B',
           sc='#7A4B00', guideline='#A06A16', principle='#4A3000', policy='#1F6B5B',
           standard='#2F5488', axe='#5B4B9E', rule='#2E6B1F', ux='#8A1A5C', polarity='#B03A7A',
           icon='#0B7285', iconGroup='#075A6A', logo='#4E6E8E'),
    f=dict(structure='#111111', usage='#1F4FBF', render='#7A7A7A', rules='#DA1A00',
           governance='#DA1A00', guidelines='#7A4B00', guidelinerules='#2E6B1F',
           uxprinciples='#8A1A5C', assets='#0B7285'))
DARK = dict(
    bg='#0C0C0C', ink='#F2F2F2', ink2='#B5B5B5', ink3='#7A7A7A', rule='#262626',
    t=dict(component='#F6604C', snippet='#9A9A9A', pattern='#6C94FF', context='#3FCB98',
           ruling='#F2F2F2', session='#8F8F8F', artefact='#C2AE92', evidence='#9E9384',
           sc='#E0A155', guideline='#D9A05B', principle='#F0C68A', policy='#4FC7AC',
           standard='#7FA6E8', axe='#A697E8', rule='#8FD67A', ux='#E68ABF', polarity='#F0B4D6',
           icon='#4FC3D9', iconGroup='#8BD3E3', logo='#9AB4D1'),
    f=dict(structure='#F2F2F2', usage='#6C94FF', render='#9A9A9A', rules='#F6604C',
           governance='#F6604C', guidelines='#D9A05B', guidelinerules='#8FD67A',
           uxprinciples='#E68ABF', assets='#4FC3D9'))

VIEWNAME = {'system': 'System', 'design': 'Design governance', 'explain': 'Explanation',
            'constitution': 'The Constitution'}
BANDFAM = {'system': 'structure', 'design': 'guidelines', 'explain': 'uxprinciples',
           'constitution': 'governance'}
ORDER = ['system', 'design', 'explain', 'constitution']

# ---------------------------------------------------------------- the data, sampled
QUOTA = {'system': 460, 'design': 542, 'explain': 171, 'constitution': 340}


def load():
    kg = sim.load(PAGE)
    byId = {n['id']: n for n in kg['nodes']}
    rep = sim.report(PAGE, ALLON)
    drawnN, drawnE = rep['drawnN'], rep['drawnE']
    deg = collections.Counter()
    cross = collections.Counter()
    for s, t, ty in drawnE:
        deg[s] += 1; deg[t] += 1
        if byId[s]['view'] != byId[t]['view']:
            cross[s] += 1; cross[t] += 1
    per = collections.defaultdict(list)
    for i in drawnN:
        per[byId[i]['view']].append(i)
    rng = random.Random(280)
    keep = set()
    for v, ids in per.items():
        q = min(QUOTA[v], len(ids))
        ids = sorted(ids)
        # the crossings are what the picture is for: the nodes that carry them are kept first,
        # then the busiest, then a seeded random fill so the cloud's bulk is honest.
        ids.sort(key=lambda i: (-cross[i], -deg[i], i))
        head = ids[:int(q * 0.6)]
        tail = [i for i in ids if i not in set(head)]
        rng.shuffle(tail)
        keep.update(head); keep.update(tail[:q - len(head)])
    edges = [(s, t, ty) for (s, t, ty) in sorted(drawnE) if s in keep and t in keep]
    return kg, byId, rep, keep, edges


# ---------------------------------------------------------------- svg helpers
def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


class Svg:
    def __init__(self, w, h, pal, title):
        self.w, self.h, self.pal = w, h, pal
        self.o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
                  f'width="100%" role="img" aria-label="{esc(title)}">',
                  f'<rect width="{w}" height="{h}" fill="{pal["bg"]}"/>']

    def dots(self, pts, colour, r, alpha=1.0):
        if not pts:
            return
        self.o.append(f'<g fill="{colour}" fill-opacity="{f(alpha)}">')
        self.o.append(''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y in pts))
        self.o.append('</g>')

    def lines(self, segs, colour, alpha, width):
        if not segs:
            return
        d = ''.join(f'M{f(a)} {f(b)}L{f(c)} {f(dd)}' for a, b, c, dd in segs)
        self.o.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-opacity="{f(alpha)}" '
                      f'stroke-width="{f(width)}"/>')

    def raw(self, s):
        self.o.append(s)

    def text(self, x, y, s, colour, size=11, weight=400, anchor='start', ls='.12em', alpha=1.0):
        self.o.append(
            f'<text x="{f(x)}" y="{f(y)}" fill="{colour}" fill-opacity="{f(alpha)}" '
            f'font-family="SF Mono,Menlo,Consolas,monospace" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" text-anchor="{anchor}">{esc(s)}</text>')

    def done(self):
        return '\n'.join(self.o) + '\n</svg>'


class Cam:
    """yaw about the world Y (up), then pitch about the camera X, then a mild perspective."""

    def __init__(self, yaw, pitch, scale, cx, cy, focal=2600):
        self.yaw, self.pitch, self.s, self.cx, self.cy, self.focal = yaw, pitch, scale, cx, cy, focal

    def cam(self, x, y, z):
        cy_, sy_ = math.cos(self.yaw), math.sin(self.yaw)
        X = x * cy_ + z * sy_
        Z = -x * sy_ + z * cy_
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        Y = y * cp - Z * sp
        Z2 = y * sp + Z * cp
        return X, Y, Z2

    def raw(self, x, y, z):
        X, Y, Z = self.cam(x, y, z)
        k = self.focal / (self.focal + Z)
        return X * k, -Y * k, Z

    def __call__(self, x, y, z):
        rx, ry, Z = self.raw(x, y, z)
        return self.cx + rx * self.s, self.cy + ry * self.s, Z

    def fit(self, pts, W, H, pad=54, extra_raw=()):
        """Second pass: scale and centre so everything the sketch draws is on the page."""
        r = [self.raw(*p) for p in pts] + [(x, y, 0) for x, y in extra_raw]
        x0 = min(p[0] for p in r); x1 = max(p[0] for p in r)
        y0 = min(p[1] for p in r); y1 = max(p[1] for p in r)
        self.s = min((W - 2 * pad) / max(1e-6, x1 - x0), (H - 2 * pad) / max(1e-6, y1 - y0))
        self.cx = W / 2 - (x0 + x1) / 2 * self.s
        self.cy = H / 2 - (y0 + y1) / 2 * self.s
        return self


def unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return [c / n for c in v] if n > 1e-9 else None


def fib(i, n):
    """Fibonacci-sphere point i of n — the fallback for a node whose 3D vector is degenerate."""
    y = 1 - 2 * (i + 0.5) / n
    r = math.sqrt(max(0.0, 1 - y * y))
    a = math.pi * (3 - math.sqrt(5)) * i
    return [math.cos(a) * r, y, math.sin(a) * r]


def norm(vals):
    """Percentile rank, not min–max. The force layout puts whole families in far-off columns (the
    assets column sits at x≈7,500 while the rest of System lives under x≈0), so a min–max squash
    would pile 95% of a view into one corner of its plate. Rank keeps the ORDER the force layout
    gave — left is still left, near is still near — and gives up only the spacing."""
    order = sorted(range(len(vals)), key=lambda k: vals[k])
    rank = {}
    for k, idx in enumerate(order):
        rank[vals[idx]] = k / max(1, len(vals) - 1)
    return lambda v: rank[v]


# ---------------------------------------------------------------- 2 · SHELLS
R = {'system': 150.0, 'design': 285.0, 'explain': 415.0}
PLINTH_Y = -560.0
PLINTH_R = 620.0


def shell_pos(byId, keep):
    """Every node put on its view's shell by Fibonacci-sphere placement — an even surface, which
    the raw 3D force directions are not — with the Fibonacci index handed out in the order of the
    node's own longitude in the 3D force layout, so the layout's neighbours stay neighbours in
    longitude. THE CONSTITUTION is laid flat on the plinth from its 2D force position."""
    pos = {}
    degenerate = 0
    per = collections.defaultdict(list)
    for i in keep:
        per[byId[i]['view']].append(i)
    for v, ids in per.items():
        ids = sorted(ids)
        if v == 'constitution':
            xs = norm([byId[i]['x'] for i in ids]); ys = norm([byId[i]['y'] for i in ids])
            for i in ids:
                a = (xs(byId[i]['x']) - .5) * 2 * PLINTH_R * .92
                b = (ys(byId[i]['y']) - .5) * 2 * PLINTH_R * .92
                rr = math.hypot(a, b)
                if rr > PLINTH_R * .95:
                    a *= PLINTH_R * .95 / rr; b *= PLINTH_R * .95 / rr
                pos[i] = (a, PLINTH_Y, b)
            continue
        def lon(i):
            n = byId[i]
            x3, z3 = n.get('x3') or 0.0, n.get('z3') or 0.0
            if abs(x3) + abs(z3) < 1e-9:
                return 9.9
            return math.atan2(z3, x3)
        degenerate += sum(1 for i in ids if lon(i) == 9.9)
        for k, i in enumerate(sorted(ids, key=lambda i: (lon(i), i))):
            pos[i] = tuple(c * R[v] for c in fib(k, len(ids)))
    return pos, degenerate


def sketch_shells(byId, keep, edges, pal, cutaway=False, yaw=0.62, pitch=0.30,
                  W=1120, H=720):
    pos, _ = shell_pos(byId, keep)
    cam = Cam(yaw, pitch, 1.0, 0, 0)
    ring0 = [(PLINTH_R * math.cos(2 * math.pi * k / 48), PLINTH_Y, PLINTH_R * math.sin(2 * math.pi * k / 48))
             for k in range(48)]
    rmax = R['explain']
    c0 = cam.raw(0, 0, 0)   # the shells project as circles of radius R about the centre
    sil = [(c0[0] + a * rmax, c0[1] + b * rmax) for a in (-1, 0, 1) for b in (-1, 0, 1)]
    cam.fit(ring0 + [(0, 0, 0)], W, H - 56, 60, extra_raw=sil)
    cam.cy += 28
    s = Svg(W, H, pal, 'Shells: the three views as concentric spheres')
    shown = set(keep)
    if cutaway:   # the front half of the two outer shells is taken away
        for i in keep:
            v = byId[i]['view']
            if v in ('design', 'explain') and cam.cam(*pos[i])[2] < 0:
                shown.discard(i)
    P = {i: cam(*pos[i]) for i in keep}

    # the plinth — a ground disc, dimmed, the shells sitting on it
    gov = pal['f']['governance']
    ring = []
    for k in range(97):
        a = 2 * math.pi * k / 96
        ring.append(cam(PLINTH_R * math.cos(a), PLINTH_Y, PLINTH_R * math.sin(a))[:2])
    d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in ring) + 'Z'
    s.raw(f'<path d="{d}" fill="{gov}" fill-opacity="0.05" stroke="{gov}" stroke-opacity="0.35" '
          f'stroke-width="1"/>')

    # the shells, back to front: silhouette circles at the radius the nodes sit on
    for v in ('explain', 'design', 'system'):
        cx, cy, _ = cam(0, 0, 0)
        rr = R[v] * cam.s
        col = pal['f'][BANDFAM[v]]
        a = 0.25 if v != 'system' else 0.6
        s.raw(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rr)}" fill="{col}" fill-opacity="0.035" '
              f'stroke="{col}" stroke-opacity="{f(a)}" stroke-width="1"'
              + ('' if (v == 'system' or cutaway) else ' stroke-dasharray="3 4"') + '/>')

    # the chords
    intra, crossing = collections.defaultdict(list), collections.defaultdict(list)
    for a, b, ty in edges:
        if a not in shown or b not in shown:
            continue
        fam = sim.FAMILY.get(ty)
        seg = (P[a][0], P[a][1], P[b][0], P[b][1])
        (crossing if byId[a]['view'] != byId[b]['view'] else intra)[fam].append(seg)
    for fam, segs in intra.items():
        s.lines(segs, pal['f'].get(fam, pal['ink3']), 0.07, 0.45)
    for fam, segs in crossing.items():
        s.lines(segs, pal['f'].get(fam, pal['ink3']), 0.20, 0.6)

    # the nodes, far ones first
    bytype = collections.defaultdict(list)
    for i in sorted(shown, key=lambda i: -P[i][2]):
        bytype[(byId[i]['type'], byId[i]['view'])].append(P[i][:2])
    for (ty, v), pts in bytype.items():
        dim = 1.0 if (v == 'system' or cutaway) else 0.55
        if v == 'constitution':
            dim = 0.45
        s.dots(pts, pal['t'].get(ty, pal['ink3']), 2.0 if v == 'system' else 1.8, dim)

    # labels
    y = 34
    for v in ORDER:
        col = pal['f'][BANDFAM[v]]
        s.text(28, y, VIEWNAME[v].upper(), col, 11, 700, alpha=1 if v != 'constitution' else .7)
        y += 20
    s.text(W - 28, H - 22, 'CUTAWAY — FRONT HALF OF THE OUTER TWO SHELLS REMOVED' if cutaway
           else 'THREE-QUARTER VIEW — OUTER SHELLS AT 25%', pal['ink3'], 10, 400, 'end')
    return s.done(), len(shown), sum(len(x) for x in crossing.values())


# ---------------------------------------------------------------- 3 · FLOORS
FLOOR_Y = {'system': 0.0, 'design': 300.0, 'explain': 600.0}
PLATE_W, PLATE_D = 700.0, 460.0
CONST_DX = 800.0


def floor_pos(byId, keep):
    pos = {}
    per = collections.defaultdict(list)
    for i in keep:
        per[byId[i]['view']].append(i)
    for v, ids in per.items():
        xs = norm([byId[i]['x'] for i in ids]); ys = norm([byId[i]['y'] for i in ids])
        dx = CONST_DX if v == 'constitution' else 0.0
        yy = 0.0 if v == 'constitution' else FLOOR_Y[v]
        for i in ids:
            pos[i] = ((xs(byId[i]['x']) - .5) * PLATE_W * .94 + dx, yy,
                      (ys(byId[i]['y']) - .5) * PLATE_D * .94)
    return pos


def sketch_floors(byId, keep, edges, pal, W=1180, H=700):
    pos = floor_pos(byId, keep)
    cam = Cam(0.50, 0.46, 1.0, 0, 0)
    box = [(dx + a * PLATE_W / 2, y, b * PLATE_D / 2)
           for dx, y in [(0, FLOOR_Y['system']), (0, FLOOR_Y['explain']), (CONST_DX, 0.0)]
           for a in (-1, 1) for b in (-1, 1)]
    cam.fit(box, W, H - 40, 58)
    P = {i: cam(*pos[i]) for i in keep}
    s = Svg(W, H, pal, 'Floors: the three views as stacked plates')

    def plate(dx, y, col, name, dim=1.0):
        c = [cam(dx - PLATE_W / 2, y, -PLATE_D / 2), cam(dx + PLATE_W / 2, y, -PLATE_D / 2),
             cam(dx + PLATE_W / 2, y, PLATE_D / 2), cam(dx - PLATE_W / 2, y, PLATE_D / 2)]
        d = 'M' + 'L'.join(f'{f(p[0])} {f(p[1])}' for p in c) + 'Z'
        s.raw(f'<path d="{d}" fill="{col}" fill-opacity="{f(0.05 * dim)}" stroke="{col}" '
              f'stroke-opacity="{f(0.45 * dim)}" stroke-width="1"/>')
        if dx:   # the plate beside the stack is labelled above its back edge, clear of the beams
            s.text(c[1][0] + 4, c[1][1] - 14, name.upper(), col, 11, 700, 'end', alpha=dim)
        else:
            s.text(c[3][0] - 10, c[3][1] + 18, name.upper(), col, 11, 700, 'end', alpha=dim)
        return c

    order = [('constitution', CONST_DX, 0.0, 0.55), ('system', 0.0, FLOOR_Y['system'], 1.0),
             ('design', 0.0, FLOOR_Y['design'], 1.0), ('explain', 0.0, FLOOR_Y['explain'], 1.0)]
    # the stack's corner posts, so the plates read as one building
    for xx in (-PLATE_W / 2, PLATE_W / 2):
        for zz in (-PLATE_D / 2, PLATE_D / 2):
            a = cam(xx, FLOOR_Y['system'], zz); b = cam(xx, FLOOR_Y['explain'], zz)
            s.lines([(a[0], a[1], b[0], b[1])], pal['ink3'], 0.35, 0.75)

    intra, crossing = collections.defaultdict(list), collections.defaultdict(list)
    for a, b, ty in edges:
        fam = sim.FAMILY.get(ty)
        seg = (P[a][0], P[a][1], P[b][0], P[b][1])
        (crossing if byId[a]['view'] != byId[b]['view'] else intra)[fam].append(seg)

    for v, dx, y, dim in order:
        plate(dx, y, pal['f'][BANDFAM[v]], VIEWNAME[v], dim)
    for fam, segs in intra.items():
        s.lines(segs, pal['f'].get(fam, pal['ink3']), 0.07, 0.45)
    for fam, segs in crossing.items():
        s.lines(segs, pal['f'].get(fam, pal['ink3']), 0.18, 0.6)
    bytype = collections.defaultdict(list)
    for i in sorted(keep, key=lambda i: -P[i][2]):
        bytype[(byId[i]['type'], byId[i]['view'])].append(P[i][:2])
    for (ty, v), pts in bytype.items():
        s.dots(pts, pal['t'].get(ty, pal['ink3']), 1.9, 0.5 if v == 'constitution' else 1.0)
    s.text(W - 28, H - 22, 'ISOMETRIC — THE CONSTITUTION IS THE PLATE BESIDE THE STACK',
           pal['ink3'], 10, 400, 'end')
    return s.done(), len(keep), sum(len(x) for x in crossing.values())


# ---------------------------------------------------------------- 4 · ORBITS
RING = {'system': (14.0, 150.0), 'design': (212.0, 300.0), 'explain': (346.0, 414.0)}
ARC = (458.0, 520.0)
ARC_SPAN = math.radians(52)


def sketch_orbits(byId, keep, edges, pal, W=1080, H=1080):
    cx, cy = W / 2, H / 2
    pos = {}
    per = collections.defaultdict(list)
    for i in keep:
        per[byId[i]['view']].append(i)
    for v, ids in per.items():
        ids = sorted(ids)
        # the force layout gives each view its own COLUMN, so its raw angles are a narrow fan. The
        # ring keeps the cyclic ORDER of those angles and equalises the spacing, so a ring reads as
        # a ring; the radius inside the ring is the node's own distance from the layout's centre.
        rad = {i: math.hypot(byId[i]['x'], byId[i]['y']) for i in ids}
        ang = {i: math.atan2(byId[i]['y'], byId[i]['x']) for i in ids}
        rk = {i: k for k, i in enumerate(sorted(ids, key=lambda i: rad[i]))}
        ak = {i: k for k, i in enumerate(sorted(ids, key=lambda i: (ang[i], i)))}
        nn = max(1, len(ids) - 1)
        for i in ids:
            t = rk[i] / nn
            u = ak[i] / max(1, len(ids))
            if v == 'constitution':
                a = -ARC_SPAN + u * 2 * ARC_SPAN
                r = ARC[0] + t * (ARC[1] - ARC[0])
            else:
                a = -math.pi + u * 2 * math.pi
                r = RING[v][0] + t * (RING[v][1] - RING[v][0])
            pos[i] = (cx + r * math.cos(a), cy + r * math.sin(a))
    s = Svg(W, H, pal, 'Orbits: the three views as concentric rings')
    for v in ('explain', 'design', 'system'):
        col = pal['f'][BANDFAM[v]]
        r0, r1 = RING[v]
        s.raw(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r1)}" fill="{col}" fill-opacity="0.04" '
              f'stroke="{col}" stroke-opacity="0.45" stroke-width="1"/>')
        if r0 > 20:
            s.raw(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r0)}" fill="{pal["bg"]}" '
                  f'fill-opacity="1" stroke="{col}" stroke-opacity="0.25" stroke-width="1"/>')
    gov = pal['f']['governance']
    pts = []
    for k in range(49):
        a = -ARC_SPAN + 2 * ARC_SPAN * k / 48
        pts.append((cx + ARC[1] * math.cos(a), cy + ARC[1] * math.sin(a)))
    for k in range(48, -1, -1):
        a = -ARC_SPAN + 2 * ARC_SPAN * k / 48
        pts.append((cx + ARC[0] * math.cos(a), cy + ARC[0] * math.sin(a)))
    d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z'
    s.raw(f'<path d="{d}" fill="{gov}" fill-opacity="0.05" stroke="{gov}" stroke-opacity="0.35" '
          f'stroke-width="1"/>')

    intra, crossing = collections.defaultdict(list), collections.defaultdict(list)
    for a, b, ty in edges:
        fam = sim.FAMILY.get(ty)
        seg = (pos[a][0], pos[a][1], pos[b][0], pos[b][1])
        (crossing if byId[a]['view'] != byId[b]['view'] else intra)[fam].append(seg)
    for fam, segs in intra.items():
        s.lines(segs, pal['f'].get(fam, pal['ink3']), 0.06, 0.45)
    for fam, segs in crossing.items():
        s.lines(segs, pal['f'].get(fam, pal['ink3']), 0.17, 0.6)
    bytype = collections.defaultdict(list)
    for i in sorted(keep):
        bytype[(byId[i]['type'], byId[i]['view'])].append(pos[i])
    for (ty, v), pts2 in bytype.items():
        s.dots(pts2, pal['t'].get(ty, pal['ink3']), 1.9, 0.55 if v == 'constitution' else 1.0)
    # ring labels, up the left
    for v in ('system', 'design', 'explain'):
        col = pal['f'][BANDFAM[v]]
        r0, r1 = RING[v]
        yy = cy - (r0 + r1) / 2
        s.text(cx + 8, yy + 4, VIEWNAME[v].upper(), col, 11, 700)
    s.text(cx + ARC[1] * math.cos(ARC_SPAN) + 12, cy + ARC[1] * math.sin(ARC_SPAN) + 8,
           'THE CONSTITUTION', gov, 11, 700, alpha=.8)
    s.text(W - 24, H - 20, 'FLAT — THE SHELLS SEEN FROM ABOVE', pal['ink3'], 10, 400, 'end')
    return s.done(), len(keep), sum(len(x) for x in crossing.values())


# ---------------------------------------------------------------- main
def main():
    kg, byId, rep, keep, edges = load()
    facts = dict(version=kg.get('version'), generated=kg.get('generated'),
                 drawnNodes=len(rep['drawnN']), drawnEdges=len(rep['drawnE']),
                 perView={v: sum(1 for i in rep['drawnN'] if byId[i]['view'] == v) for v in ORDER},
                 crossViewEdges=sum(1 for (s, t, ty) in rep['drawnE']
                                    if byId[s]['view'] != byId[t]['view']),
                 sample=dict(nodes=len(keep), edges=len(edges),
                             perView={v: sum(1 for i in keep if byId[i]['view'] == v)
                                      for v in ORDER}))
    out = {}
    out['shells-light'], n1, c1 = sketch_shells(byId, keep, edges, LIGHT)
    out['shells-cutaway-light'], n2, c2 = sketch_shells(byId, keep, edges, LIGHT, cutaway=True)
    out['shells-dark'], _, _ = sketch_shells(byId, keep, edges, DARK)
    out['floors-light'], n3, c3 = sketch_floors(byId, keep, edges, LIGHT)
    out['orbits-light'], n4, c4 = sketch_orbits(byId, keep, edges, LIGHT)
    facts['shown'] = dict(shells=n1, shellsCutaway=n2, floors=n3, orbits=n4)
    facts['crossShown'] = dict(shells=c1, shellsCutaway=c2, floors=c3, orbits=c4)
    _, facts['degenerate3D'] = shell_pos(byId, keep)
    for k, v in out.items():
        open(os.path.join(HERE, f'sketch-{k}.svg'), 'w').write(v)
    # the rotatable shells canvas gets the sampled points and their colours, nothing else
    pts = []
    spos, _ = shell_pos(byId, keep)
    for i in sorted(keep):
        n = byId[i]
        pts.append([round(spos[i][0], 1), round(spos[i][1], 1), round(spos[i][2], 1),
                    ORDER.index(n['view']), LIGHT['t'].get(n['type'], LIGHT['ink3'])])
    idx = {i: k for k, i in enumerate(sorted(keep))}
    ed = [[idx[a], idx[b], LIGHT['f'].get(sim.FAMILY.get(ty), LIGHT['ink3']),
           1 if byId[a]['view'] != byId[b]['view'] else 0] for a, b, ty in edges]
    json.dump(dict(pts=pts, edges=ed, R=[R['system'], R['design'], R['explain']],
                   plinth=[PLINTH_Y, PLINTH_R]),
              open(os.path.join(HERE, 'shells-live.json'), 'w'), separators=(',', ':'))
    json.dump(facts, open(os.path.join(HERE, 'facts.json'), 'w'), indent=1)
    print(json.dumps(facts, indent=1))


if __name__ == '__main__':
    main()
