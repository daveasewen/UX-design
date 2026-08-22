#!/usr/bin/env python3
"""Generate the local placeholder "photographs" for bento-gallery-showcase-v1.html.

WHY THESE EXIST: the showcase must not fetch anything external (no picsum, no CDN), and it
needs real photographic VARIANCE — portrait / landscape / square — because the whole point of
the aspect-ratio control is that `object-fit: cover` crops portraits differently from
landscapes. Flat grey boxes would hide exactly the thing Dave is being asked to rule on.

PALETTE NOTE (deliberate, and it is a constraint not a taste): these are decorative
photographic stand-ins, so they carry NO semantic token. They are drawn from BLUES, TEALS,
GREENS, VIOLETS and SLATES only. Red and yellow are avoided outright -- the two-red law
(`s151-D1`) reserves #DA1A00 / #F6604C, and red+yellow are the recorded unstable hues.
Nothing here may be mistaken for an error or success signal.

Deterministic: same seed -> same bytes. Re-run to regenerate.
"""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent

# name, width, height  -- a real photographic spread, not one shape repeated
SPECS = [
    ("p01-harbour",      1600, 1067),  # 3:2 landscape
    ("p02-ridge",        1600,  900),  # 16:9 landscape
    ("p03-atrium",        800, 1200),  # 2:3 portrait
    ("p04-still-life",   1200, 1200),  # 1:1 square
    ("p05-terrace",      1600, 1200),  # 4:3 landscape
    ("p06-figure",        900, 1350),  # 2:3 portrait
    ("p07-canopy",       1200,  900),  # 4:3 landscape
    ("p08-tideline",     1600,  640),  # 5:2 panorama
    ("p09-stairwell",     900, 1600),  # 9:16 tall portrait
    ("p10-estuary",      1500, 1000),  # 3:2 landscape
    ("p11-glasshouse",   1100, 1100),  # 1:1 square
    ("p12-dunes",        1600, 1067),  # 3:2 landscape
    ("p13-portico",       960, 1280),  # 3:4 portrait
    ("p14-lagoon",       1400,  875),  # 8:5 landscape
]

# Duotone pairs: (shadow, light). Cool only -- see PALETTE NOTE.
DUOS = [
    ("#12233A", "#7FB0C9"),   # deep navy -> haze blue
    ("#0F2E2B", "#8CC7B4"),   # pine -> sea green
    ("#1B1F3B", "#9AA3D8"),   # ink violet -> periwinkle
    ("#0E2A33", "#6FBFC7"),   # petrol -> teal
    ("#232A31", "#A9B6C0"),   # slate -> stone
    ("#14324A", "#79A8D0"),   # dusk blue -> sky
    ("#182B22", "#A3C69B"),   # moss -> sage
    ("#26203A", "#B0A2CE"),   # aubergine -> lilac
]

SCENES = ["horizon", "ridge", "architecture", "figure", "objects", "waves", "canopy", "windows"]


def scene_svg(kind, w, h, dark, light, rnd):
    """Return the inner SVG body for one composition."""
    b = []
    mid = f"url(#g)"
    if kind == "horizon":
        hz = h * rnd.uniform(0.52, 0.68)
        b.append(f'<rect width="{w}" height="{hz:.0f}" fill="{mid}"/>')
        b.append(f'<rect y="{hz:.0f}" width="{w}" height="{h-hz:.0f}" fill="{dark}"/>')
        b.append(f'<circle cx="{w*rnd.uniform(.2,.8):.0f}" cy="{hz*rnd.uniform(.35,.7):.0f}" '
                 f'r="{min(w,h)*0.09:.0f}" fill="{light}" opacity="0.85"/>')
        b.append(f'<rect y="{hz:.0f}" width="{w}" height="{(h-hz)*.18:.0f}" fill="{light}" opacity="0.18"/>')
    elif kind == "ridge":
        b.append(f'<rect width="{w}" height="{h}" fill="{mid}"/>')
        for i, op in enumerate([0.28, 0.5, 0.8]):
            base = h * (0.55 + i * 0.14)
            pts = [f"0,{h}"]
            x = 0
            y = base
            while x < w:
                x += w * rnd.uniform(0.09, 0.2)
                y = base - min(w, h) * rnd.uniform(-0.1, 0.26)
                pts.append(f"{min(x,w):.0f},{y:.0f}")
            pts.append(f"{w},{h}")
            b.append(f'<polygon points="{" ".join(pts)}" fill="{dark}" opacity="{op}"/>')
    elif kind == "architecture":
        b.append(f'<rect width="{w}" height="{h}" fill="{mid}"/>')
        cols = rnd.randint(4, 7)
        cw = w / cols
        for c in range(cols):
            ch = h * rnd.uniform(0.3, 0.95)
            b.append(f'<rect x="{c*cw+cw*0.08:.0f}" y="{h-ch:.0f}" width="{cw*0.84:.0f}" '
                     f'height="{ch:.0f}" fill="{dark}" opacity="{rnd.uniform(.35,.85):.2f}"/>')
        b.append(f'<rect y="0" width="{w}" height="{h*0.22:.0f}" fill="{light}" opacity="0.16"/>')
    elif kind == "figure":
        b.append(f'<rect width="{w}" height="{h}" fill="{mid}"/>')
        cx, cy = w * 0.5, h * 0.36
        r = min(w, h) * 0.17
        b.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{dark}" opacity="0.9"/>')
        b.append(f'<path d="M{cx-r*2.1:.0f},{h} C{cx-r*1.9:.0f},{cy+r*1.3:.0f} '
                 f'{cx+r*1.9:.0f},{cy+r*1.3:.0f} {cx+r*2.1:.0f},{h} Z" fill="{dark}" opacity="0.9"/>')
        b.append(f'<circle cx="{w*0.78:.0f}" cy="{h*0.18:.0f}" r="{min(w,h)*0.1:.0f}" '
                 f'fill="{light}" opacity="0.35"/>')
    elif kind == "objects":
        b.append(f'<rect width="{w}" height="{h}" fill="{mid}"/>')
        b.append(f'<rect y="{h*0.66:.0f}" width="{w}" height="{h*0.34:.0f}" fill="{dark}" opacity="0.55"/>')
        for _ in range(rnd.randint(3, 5)):
            rr = min(w, h) * rnd.uniform(0.08, 0.2)
            b.append(f'<circle cx="{rnd.uniform(.15,.85)*w:.0f}" cy="{h*0.66-rr*rnd.uniform(.2,.9):.0f}" '
                     f'r="{rr:.0f}" fill="{rnd.choice([dark,light])}" opacity="{rnd.uniform(.45,.9):.2f}"/>')
    elif kind == "waves":
        b.append(f'<rect width="{w}" height="{h}" fill="{mid}"/>')
        for i in range(5):
            y = h * (0.3 + i * 0.14)
            amp = h * 0.05
            b.append(f'<path d="M0,{y:.0f} Q{w*.25:.0f},{y-amp:.0f} {w*.5:.0f},{y:.0f} '
                     f'T{w},{y:.0f} L{w},{h} L0,{h} Z" fill="{dark}" opacity="{0.16+i*0.15:.2f}"/>')
    elif kind == "canopy":
        b.append(f'<rect width="{w}" height="{h}" fill="{light}"/>')
        b.append(f'<rect width="{w}" height="{h}" fill="{mid}" opacity="0.7"/>')
        for _ in range(rnd.randint(10, 16)):
            cx, cy = rnd.uniform(0, w), rnd.uniform(0, h * 0.8)
            rr = min(w, h) * rnd.uniform(0.08, 0.22)
            b.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rr:.0f}" ry="{rr*0.72:.0f}" '
                     f'fill="{dark}" opacity="{rnd.uniform(.25,.6):.2f}"/>')
    else:  # windows
        b.append(f'<rect width="{w}" height="{h}" fill="{dark}"/>')
        cols, rows = rnd.randint(5, 8), rnd.randint(6, 10)
        cw, chh = w / cols, h / rows
        for c in range(cols):
            for r_ in range(rows):
                if rnd.random() < 0.42:
                    b.append(f'<rect x="{c*cw+cw*.22:.0f}" y="{r_*chh+chh*.22:.0f}" '
                             f'width="{cw*.56:.0f}" height="{chh*.56:.0f}" fill="{light}" '
                             f'opacity="{rnd.uniform(.3,.95):.2f}"/>')
    return "\n  ".join(b)


def build(name, w, h, i):
    rnd = random.Random(1000 + i * 37)
    dark, light = DUOS[i % len(DUOS)]
    kind = SCENES[i % len(SCENES)]
    ang = rnd.choice([(0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 0)])
    body = scene_svg(kind, w, h, dark, light, rnd)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="Placeholder photograph: {kind}">\n'
        f'  <defs><linearGradient id="g" x1="{ang[0]}" y1="{ang[1]}" x2="{ang[2]}" y2="{ang[3]}">\n'
        f'    <stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{dark}"/>\n'
        f'  </linearGradient>\n'
        f'  <linearGradient id="v" x1="0" y1="0" x2="0" y2="1">\n'
        f'    <stop offset="0" stop-color="{dark}" stop-opacity="0.35"/>\n'
        f'    <stop offset="0.5" stop-color="{dark}" stop-opacity="0"/>\n'
        f'    <stop offset="1" stop-color="{dark}" stop-opacity="0.45"/>\n'
        f'  </linearGradient></defs>\n'
        f'  {body}\n'
        f'  <rect width="{w}" height="{h}" fill="url(#v)"/>\n'
        f'</svg>\n'
    )


if __name__ == "__main__":
    for i, (name, w, h) in enumerate(SPECS):
        (OUT / f"{name}.svg").write_text(build(name, w, h, i), encoding="utf-8")
    print(f"wrote {len(SPECS)} placeholder photographs to {OUT}")
