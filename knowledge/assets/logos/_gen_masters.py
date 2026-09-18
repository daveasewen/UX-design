#!/usr/bin/env python3
"""
Per-size logo masters — 8 lockups x 5 raw-pixel height steps = 40 SVG files.

Reads the 8 Figma exports in this directory and emits masters/<name>-<h>.svg for
h in 24 28 32 36 40 (s282-D3).  Each master carries its raw pixel width/height as
width=/height= and has NO viewBox: coordinates are literal pixels.  The hexagon is
placed exactly on the pixel grid.  The wordmark is moved RIGIDLY — one uniform scale
(the file's own h/85) plus a translation that lands its left edge on an integer column
and its cap line on an integer row.  NOTHING inside a glyph is snapped: no node, no
control point, no stem.  (#285: per-node snapping plus a non-uniform x/y scale kinked
the B's bowls and stretched the wordmark up to 4.4% wider than tall.)

    python3 _gen_masters.py            # write the 40 masters
    python3 _gen_masters.py --check    # regenerate to memory, diff against disk (exit 1 on drift)
    python3 _gen_masters.py --report   # write, and print the measured snapping table as JSON
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "masters")
STEPS = [24, 28, 32, 36, 40]
NAMES = [f"{lock}-{theme}-{mode}"
         for lock in ("hexagon", "masterbrand")
         for theme in ("light", "dark")
         for mode in ("colour", "mono")]

SRC_H = 85.0
HEX_X = [0.0, 42.5, 85.0, 127.5, 170.0]   # canonical hexagon grid, x
HEX_Y = [0.0, 42.5, 85.0]                 # canonical hexagon grid, y
TOL = 0.25                                # Figma float noise is < 0.2 from the true vertex

PATH_RE = re.compile(r'<path\b([^>]*)/>')
ATTR_RE = re.compile(r'(\w[\w-]*)="([^"]*)"')
CMD_RE = re.compile(r'([MLHVCZmlhvcz])([^MLHVCZmlhvcz]*)')
NUM_RE = re.compile(r'-?\d*\.?\d+(?:[eE][-+]?\d+)?')


def rnd(v):
    """Half-up rounding — python's round() is banker's."""
    return int(math.floor(v + 0.5))


def fmt(v):
    r = round(v, 4)
    if abs(r - round(r)) < 1e-9:
        return str(int(round(r)))
    return ("%.4f" % r).rstrip("0").rstrip(".")


# ---------------------------------------------------------------- path model

class Path:
    """A path as an ordered list of segments; each segment owns its on-path end
    node index plus (for C) two control points.  Nodes are shared between the
    segment that ends on them and the segment that starts from them."""

    def __init__(self, d):
        self.nodes = []          # [x, y] on-path points, in order of first use
        self.segs = []           # (cmd, [controls...], node_index or None for Z)
        self._parse(d)

    def _add(self, x, y):
        self.nodes.append([x, y])
        return len(self.nodes) - 1

    def _parse(self, d):
        cx = cy = 0.0
        start = None
        for cmd, args in CMD_RE.findall(d):
            if cmd.islower():
                raise ValueError("relative command %r not supported" % cmd)
            n = [float(t) for t in NUM_RE.findall(args)]
            if cmd == "M":
                for i in range(0, len(n), 2):
                    cx, cy = n[i], n[i + 1]
                    idx = self._add(cx, cy)
                    self.segs.append(("M" if i == 0 else "L", [], idx))
                    if i == 0:
                        start = idx
            elif cmd == "L":
                for i in range(0, len(n), 2):
                    cx, cy = n[i], n[i + 1]
                    self.segs.append(("L", [], self._add(cx, cy)))
            elif cmd == "H":
                for v in n:
                    cx = v
                    self.segs.append(("H", [], self._add(cx, cy)))
            elif cmd == "V":
                for v in n:
                    cy = v
                    self.segs.append(("V", [], self._add(cx, cy)))
            elif cmd == "C":
                for i in range(0, len(n), 6):
                    ctl = [[n[i], n[i + 1]], [n[i + 2], n[i + 3]]]
                    cx, cy = n[i + 4], n[i + 5]
                    self.segs.append(("C", ctl, self._add(cx, cy)))
            elif cmd == "Z":
                # A closed subpath whose last on-path point coincides with its M
                # must SHARE that node, or snapping moves the two apart and tears
                # the shape open.  Fold the duplicate back onto the start node.
                if start is not None and self.segs:
                    last = self.segs[-1]
                    if (last[2] is not None and last[2] != start
                            and self.nodes[last[2]] == self.nodes[start]):
                        dup = last[2]
                        self.segs[-1] = (last[0], last[1], start)
                        if dup == len(self.nodes) - 1:
                            self.nodes.pop()
                self.segs.append(("Z", [], None))
                if start is not None:
                    cx, cy = self.nodes[start]

    def coords(self):
        for nd in self.nodes:
            yield nd
        for _, ctl, _ in self.segs:
            for c in ctl:
                yield c

    def emit(self):
        out = []
        for cmd, ctl, idx in self.segs:
            if cmd == "Z":
                out.append("Z")
                continue
            x, y = self.nodes[idx]
            if cmd in ("M", "L"):
                out.append("%s%s %s" % (cmd, fmt(x), fmt(y)))
            elif cmd == "H":
                out.append("H%s" % fmt(x))
            elif cmd == "V":
                out.append("V%s" % fmt(y))
            elif cmd == "C":
                out.append("C%s %s %s %s %s %s" % (fmt(ctl[0][0]), fmt(ctl[0][1]),
                                                   fmt(ctl[1][0]), fmt(ctl[1][1]),
                                                   fmt(x), fmt(y)))
        return "".join(out)


# ---------------------------------------------------------------- source read

def read_src(name):
    raw = open(os.path.join(HERE, name + ".svg")).read()
    paths = []
    for attrs in PATH_RE.findall(raw):
        a = dict(ATTR_RE.findall(attrs))
        paths.append({"fill": a.get("fill", "black"), "d": a["d"], "p": Path(a["d"])})
    return paths


def is_hexagon(entry):
    return max(c[0] for c in entry["p"].coords()) <= 170.0 + TOL


# ---------------------------------------------------------------- hexagon

def snap_hex(p, h, tally):
    """Every hexagon coordinate is a multiple of 42.5 in source; at h even this maps
    to an exact integer (k*h/2).  Figma float noise is normalised first, then any
    node that collapses onto its predecessor (the 42.3107 84.9311 kink) is dropped."""
    def grid(v, table, axis):
        for g in table:
            if abs(v - g) <= TOL:
                if v != g:
                    tally["hex_floats"] += 1
                return int(round(g / 42.5))
        raise ValueError("off-grid hexagon coordinate %r on %s" % (v, axis))

    half = h // 2
    for nd in p.nodes:
        nd[0] = grid(nd[0], HEX_X, "x") * half
        nd[1] = grid(nd[1], HEX_Y, "y") * half
    # drop segments whose endpoint is already the current point
    kept, cur = [], None
    for cmd, ctl, idx in p.segs:
        if cmd == "Z":
            kept.append((cmd, ctl, idx)); cur = None; continue
        pt = tuple(p.nodes[idx])
        if cmd != "M" and cur == pt:
            tally["hex_kinks"] += 1
            continue
        kept.append((cmd, ctl, idx)); cur = pt
    p.segs = kept


# ---------------------------------------------------------------- wordmark

def wordmark_box(entries):
    """Anchors measured off the artwork: L/R are the wordmark's extreme x; T/B are
    the cap line and baseline, read off the H — the one glyph made of H/V only."""
    xs = [c[0] for e in entries for c in e["p"].coords()]
    hpath = None
    for e in entries:
        if all(cmd in ("M", "H", "V", "Z") for cmd, _, _ in e["p"].segs):
            hpath = e
    if hpath is None:
        raise ValueError("no all-orthogonal H glyph found")
    ys = [nd[1] for nd in hpath["p"].nodes]
    return min(xs), max(xs), min(ys), max(ys), hpath


def snap_wordmark(entries, h, tally):
    """RIGID MOVE ONLY (#285).

    One uniform scale — s = h/85, the same factor the hexagon is drawn at, so the
    wordmark keeps the hexagon's size relationship and its own aspect ratio exactly
    — plus one translation shared by every coordinate of every wordmark glyph.  No
    coordinate is moved relative to any other coordinate.  Curves therefore cannot
    kink and the B's bowls cannot squash; that is the whole point.

    The translation is chosen so the wordmark's left edge lands on an integer column
    and its cap line on an integer row.  The baseline then falls at cap_top + 35.5668*s,
    which is NOT an integer at any of the five steps: with one uniform scale the cap
    line and the baseline cannot both be pinned.  See the report — the two ways to pin
    both (rescale y, or rescale both by capH/(B-T)) are distortion and over-width
    respectively, and are declined."""
    s = h / SRC_H
    L, R, T, B = wordmark_box(entries)[:4]
    W = rnd(315.0 * s)
    Lx = float(rnd(L * s))                 # left edge → integer column
    # W is rounded from 315*s, so at some steps the artwork's own right edge already
    # sits a fraction past W; rounding Lx UP can add half a pixel on top and flatten
    # the C's right terminal.  Step Lx down to the next integer column when that push
    # exceeds TOL (the same quarter-pixel tolerance the hexagon uses).
    if Lx + (R - L) * s - W > TOL:
        Lx -= 1.0
    capS = (B - T) * s                     # cap-height at the file's own scale, undistorted
    top = float(rnd((h - capS) / 2.0))     # cap line → integer row; box centred on h/2
    base = top + capS
    dx = Lx - L * s
    dy = top - T * s

    for e in entries:
        p = e["p"]
        for c in p.coords():               # nodes AND control points, one rigid map
            c[0] = c[0] * s + dx
            c[1] = c[1] * s + dy
        tally["rigid_nodes"] += len(p.nodes)
        tally["rigid_controls"] += sum(len(ctl) for _, ctl, _ in p.segs)
    tally["box"] = {"left": Lx, "right": Lx + (R - L) * s, "cap_top": top,
                    "baseline": base, "cap_height": capS, "width": W,
                    "scale": s, "uniform": True}
    return W


# ---------------------------------------------------------------- one master

def build(name, h):
    entries = read_src(name)
    tally = {"hex_floats": 0, "hex_kinks": 0, "rigid_nodes": 0,
             "rigid_controls": 0, "snapped_nodes": 0, "box": None}
    hexes = [e for e in entries if is_hexagon(e)]
    words = [e for e in entries if not is_hexagon(e)]
    for e in hexes:
        snap_hex(e["p"], h, tally)
    if words:
        W = snap_wordmark(words, h, tally)
    else:
        W = 2 * h
    body = "\n".join(
        '<path fill-rule="evenodd" clip-rule="evenodd" d="%s" fill="%s"/>' % (e["p"].emit(), e["fill"])
        for e in entries)
    svg = ('<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">\n%s\n</svg>\n'
           % (W, h, body))
    return svg, tally


def generate():
    out = {}
    tallies = {}
    for name in NAMES:
        for h in STEPS:
            svg, tally = build(name, h)
            out["%s-%d.svg" % (name, h)] = svg
            tallies["%s-%d" % (name, h)] = tally
    return out, tallies


def main():
    check = "--check" in sys.argv
    report = "--report" in sys.argv
    out, tallies = generate()
    if check:
        drift = []
        for fn, svg in sorted(out.items()):
            p = os.path.join(OUT, fn)
            if not os.path.exists(p):
                drift.append(fn + ": missing")
            elif open(p).read() != svg:
                drift.append(fn + ": differs")
        extra = sorted(set(os.listdir(OUT)) - set(out)) if os.path.isdir(OUT) else []
        for fn in extra:
            drift.append(fn + ": unexpected")
        if drift:
            print("DRIFT (%d):" % len(drift))
            for d in drift:
                print("  " + d)
            return 1
        print("clean — %d masters match disk" % len(out))
        return 0
    os.makedirs(OUT, exist_ok=True)
    for fn, svg in sorted(out.items()):
        open(os.path.join(OUT, fn), "w").write(svg)
    print("wrote %d masters to %s" % (len(out), OUT))
    if report:
        print(json.dumps(tallies, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
