#!/usr/bin/env python3
"""
_validate_composition.py — rB's composition conditions (#234), driven against a REAL bento
artefact (never the library). Built at #245 L3 as `check_composition.py`; RULED and REGISTERED by
s245-D7 (Dave: "I'll go with all the recommendations" — Q4 (b), Q5 (b)).

  C9  SPAN LEGALITY   no grid leaves an ORPHAN CELL at any compiled band: the artefact's own tiles
                      are FLOWED into the artefact's own grid (its column count, its span rules, its
                      row spans) in SPARSE row-major order and every cell of every row must be filled —
                      leg 1 an empty cell ABOVE the last row (a tile that could not fit the columns
                      left in its row), leg 2 an empty cell IN the last row (spans not whole rows).
                      ⚠ #255, s255-D1: the old leg 1 asked `cols % span == 0` per tile, which reds
                      the 4+2 wall s248-D1 RULED legal (4+2 fills a 6-column row; 4 does not divide
                      6). The condition NAMED was always "orphan column"; the reader was computing a
                      proxy for it and lagging the rulings, so the reader is taught to flow the grid.
                      Nothing is exempted by name: a page whose tiles leave a real hole still reds.
                      ⚠ #255 after V-C §3(d) (conductor's call, Claude under s251-D15, Dave may
                      strike): `grid-auto-flow: dense` is READ and REPORTED but is NOT a source of
                      legality. Dense backfill fills a row only by rendering tiles out of DOM order
                      — a reorder C4 cannot see and C8's rendered leg leaves unproven — and s255-D1
                      never made it legal. The flow C9 judges is SPARSE at every band.
                      ⛔ BLOCKING (s245-D7 Q4 (b)) — a C9 red fails the screen in _validate_screen.py.
  C1  GAP LADDER      for every nested bento, gap(child) < gap(parent) STRICTLY (Polaris: equal is a
                      named defect), and every gap is on the ruled stop set {1,2,4,16,24,40} (s219-D1(4)).
                      ADVISORY in the chain (s245-D7 Q4 (b)); red standalone.
  C7  SECTION AIR     `neuro-003` — >=20px whitespace between sibling sections: the OUTER wall of a
                      bento-of-bentos resolves a gutter >= 20px. ADVISORY (s245-D7 Q5 (b)).
  C8  ADJACENCY       `ID-9` — related content stays adjacent: every group's members are CONTIGUOUS
                      tiles of ONE grid (no foreign element interleaved, no `order:` on a tile or
                      group). ADVISORY (s245-D7 Q5 (b)). ⚠ STATIC leg only: the per-band RENDERED
                      contiguity rB names needs the browser and is UNPROVEN here, said so in the output.
  C4  DOM = VISUAL    `CA-2` (WCAG 1.3.2) — the page's own <style> never reorders content away from
                      source order: no `order:`, no `flex-direction:*-reverse`, no `grid-row-start`/
                      `grid-area` line placement. ADVISORY (s245-D7 Q5 (b)).

Every arm reads the ARTEFACT: column counts and band clamps from its own @container blocks, gutters by
matching its own `--bento-gutter` rules against its own DOM (specificity-ranked). Nothing is read
from canon.css, the rails file or a meta — the page is judged by what it carries. A page with no
`.c-bento` is NOT APPLICABLE (exit 0, one line saying so).

C9's per-grid column count and per-tile span are CASCADED from the artefact's own rules (selector
specificity, then source order, band conditions honoured) — so a grid whose `grid-template-columns`
is written directly with a literal `repeat(<n>,…)` is <n> across at every band it applies to, and a
tile pinned `grid-column:1 / -1` inside a band takes that grid's whole row at that band. Both are
read as PROPERTIES, never as class names: no selector, group or template is exempted by name.

  python3 knowledge/_validate_composition.py <artefact.html>   -> report; exit 0 green, 1 red, 77 UNPROVEN
  python3 knowledge/_validate_composition.py --selftest        -> the real bento snippet + 14 mutants + 7 controls (22 arms)

WIRED: imported and called by _validate_screen.py (step 1b of its chain) — declared as its ARM in
_validate_wiring.py. ⚠ `--selftest` is not yet a _build_all.STEPS entry (a STEPS addition moves the
read chain's step count, the wrap's to regenerate) — a declared carry. The ruling that put it here is
s245-D7; which arm blocks is written beside each arm.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys

STOPS = (1, 2, 4, 16, 24, 40)
VOID = {"img", "input", "br", "hr", "meta", "link", "use", "path", "rect", "line", "circle", "polyline", "polygon", "stop", "source", "wbr", "col", "area", "base"}
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REAL = os.path.join(ROOT, "knowledge", "snippets", "Template-dashboard-bento.reference.html")


# ------------------------------------------------------------------ a small DOM (enough for this page)
class El:
    __slots__ = ("tag", "attrs", "parent", "children", "line")
    def __init__(self, tag, attrs, parent, line):
        self.tag, self.attrs, self.parent, self.children, self.line = tag, attrs, parent, [], line
    @property
    def classes(self): return set(self.attrs.get("class", "").split())
    def has(self, *cls): return set(cls) <= self.classes
    def ancestors(self):
        p = self.parent
        while p is not None: yield p; p = p.parent
    def descendants(self):
        for c in self.children: yield c; yield from c.descendants()


def parse_dom(html):
    html = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), html, flags=re.S)  # keep line numbers true
    root = El("#root", {}, None, 0)
    cur = root
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*?)(/?)>", html):
        closing, tag, raw, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if tag in ("script", "style") and not closing:
            # skip to the closing tag so CSS/JSON text cannot look like markup
            end = html.find("</%s" % tag, m.end())
            attrs = dict(re.findall(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)="([^"]*)"', raw))
            El(tag, attrs, cur, html.count("\n", 0, m.start()) + 1).parent.children.append(El(tag, attrs, cur, 0)) if False else None
            continue
        if closing:
            p = cur
            while p is not root and p.tag != tag: p = p.parent
            if p is not root: cur = p.parent
            continue
        attrs = dict(re.findall(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)="([^"]*)"', raw))
        el = El(tag, attrs, cur, html.count("\n", 0, m.start()) + 1)
        cur.children.append(el)
        if not selfclose and tag not in VOID: cur = el
    return root


def style_text(html):
    return "\n".join(re.sub(r"/\*.*?\*/", "", s, flags=re.S) for s in re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S))


# ------------------------------------------------------------------ the artefact's own band grammar
def bands(css):
    """-> [(label, cols, width)] read off the artefact: the base column count and each @container
    (max-width) block that rewrites --bento-cols-now. `width` is the width this band is EVALUATED
    at — the band's own max-width, and None for the base band (wider than every declared band) — so
    a rule's own @container condition can be tested against it. Per-tile spans are NOT read here
    any more (#255): they are cascaded from the artefact's own `grid-column` rules, which is what
    lets a `1 / -1` pin and a scoped `grid-template-columns` be seen at all."""
    base = re.search(r"--layout-bento-columns\s*:\s*(\d+)", css)
    out = [("base", int(base.group(1)), None)] if base else []
    for m in re.finditer(r"@container[^{]*\(max-width:\s*(\d+)px\)\s*{(.*?)}\s*}", css, flags=re.S):
        block = m.group(2) + "}"
        cols = re.search(r"--bento-cols-now\s*:\s*(\d+)", block)
        if not cols: continue
        out.append(("<=%spx" % m.group(1), int(cols.group(1)), int(m.group(1))))
    return out


# ------------------------------------------------------------------ every rule, with its band conditions
def _conds(prelude):
    """-> [('max'|'min', px)] for one @container prelude (the query, not the container name)."""
    return ([("max", int(v)) for v in re.findall(r"max-width:\s*(\d+)px", prelude)] +
            [("min", int(v)) for v in re.findall(r"min-width:\s*(\d+)px", prelude)])


def band_applies(conds, width):
    """Does a rule carrying `conds` apply at a band evaluated at `width` (None = the base band)?"""
    for kind, px in conds:
        if kind == "max" and (width is None or width > px): return False
        if kind == "min" and (width is not None and width < px): return False
    return True


def all_rules(css):
    """-> [(conds, selector, declarations, pos)] over the whole stylesheet, @container blocks
    INCLUDED and carrying their query as `conds`. `pos` is the absolute offset of the rule, so
    source order is comparable across the top level and every band block."""
    out, spans = [], []
    for m in re.finditer(r"@container([^{]*)\{", css):
        if any(s <= m.start() < e for s, e in spans): continue   # a nested @container, already taken
        i, depth = m.end(), 1
        while i < len(css) and depth:
            depth += 1 if css[i] == "{" else (-1 if css[i] == "}" else 0)
            i += 1
        spans.append((m.start(), i))
        conds = _conds(m.group(1))
        for r in re.finditer(r"([^{}]+)\{([^{}]*)\}", css[m.end():i - 1]):
            for sel in _split_top(r.group(1), ","):
                out.append((conds, sel.strip(), r.group(2), m.end() + r.start()))
    masked = list(css)
    for s, e in spans:
        for k in range(s, e): masked[k] = " "
    for r in re.finditer(r"([^{}]+)\{([^{}]*)\}", "".join(masked)):
        for sel in _split_top(r.group(1), ","):
            out.append(([], sel.strip(), r.group(2), r.start()))
    return out


def decls_of(rules, prop):
    """-> the subset of `rules` declaring `prop`, as (conds, selector, value, pos)."""
    rx = re.compile(r"(?:^|[;{\s])" + prop + r"\s*:\s*([^;]+)")
    out = []
    for conds, sel, decl, pos in rules:
        m = rx.search(decl)
        if m: out.append((conds, sel, m.group(1).strip(), pos))
    return out


def cascade(el, rules, width):
    """The winning value for one element at one band: highest (specificity, source order) among the
    rules whose selector matches it and whose @container query holds at `width`. None if none do."""
    best = None
    for conds, sel, val, pos in rules:
        if not band_applies(conds, width): continue
        ok, spec = match_selector(el, sel)
        if not ok: continue
        if best is None or (spec, pos) > best[0]: best = ((spec, pos), val)
    return best[1] if best else None


# ------------------------------------------------------------------ gutter resolution from the page's own CSS
def _split_top(s, sep):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([": depth += 1
        elif ch in ")]": depth -= 1
        if ch == sep and depth == 0: parts.append(cur); cur = ""
        else: cur += ch
    parts.append(cur); return [p.strip() for p in parts if p.strip()]


def _compounds(selector):
    """split on descendant/child combinators at top level -> [(combinator, compound)]"""
    toks, depth, cur, out, comb = selector.strip(), 0, "", [], " "
    i = 0
    while i < len(toks):
        ch = toks[i]
        if ch in "([": depth += 1
        elif ch in ")]": depth -= 1
        if depth == 0 and ch in " >":
            if cur: out.append((comb, cur)); cur = ""
            comb = ">" if ch == ">" else (comb if comb == ">" and not cur else " ")
            if ch == ">": comb = ">"
            i += 1; continue
        cur += ch; i += 1
    if cur: out.append((comb, cur))
    # normalise: first compound's combinator is meaningless
    return [(c if k else " ", cp) for k, (c, cp) in enumerate(out)]


def _match_compound(el, compound):
    """-> (matched, specificity_contrib) for one compound against one element; None = unsupported"""
    spec = 0
    rest = compound
    for cls in re.findall(r"\.([-_a-zA-Z0-9]+)", re.sub(r":has\(.*?\)$", "", compound)):
        if cls not in el.classes: return False, 0
        spec += 1
    for k, v in re.findall(r'\[([-a-zA-Z0-9]+)="([^"]*)"\]', compound):
        if el.attrs.get(k) != v: return False, 0
        spec += 1
    tagm = re.match(r"^([a-zA-Z][a-zA-Z0-9]*)", compound)
    if tagm and el.tag != tagm.group(1).lower(): return False, 0
    for pseudo in re.findall(r":(has|not|where|is)\((.*?)\)", compound):
        if pseudo[0] != "has": return None, 0
        inner = pseudo[1].strip()
        # only the relative form `> .a > .b` is supported (the bento-of-bentos detector)
        m = re.match(r"^>\s*\.([-_a-zA-Z0-9]+)\s*>\s*\.([-_a-zA-Z0-9]+)$", inner)
        if not m: return None, 0
        ok = any(m.group(1) in c.classes and any(m.group(2) in g.classes for g in c.children) for c in el.children)
        if not ok: return False, 0
        spec += 2  # :has() takes its most specific argument (two classes)
    return True, spec


def match_selector(el, sel):
    """-> (matched, specificity) for a whole descendant/child selector against one element.
    `matched` is None when the selector uses a construct this reader does not support (the caller
    SKIPS those, it never guesses). Extracted at #255 from gutter_of(), byte-for-byte the same walk,
    so the gutter arms and the new C9 readers share ONE matcher."""
    comps = _compounds(sel)
    if not comps: return False, 0
    ok, spec = _match_compound(el, comps[-1][1])
    if ok is None: return None, 0
    if not ok: return False, 0
    node = el
    for comb, comp in reversed(comps[:-1]):
        cands = [node.parent] if comb == ">" else list(node.ancestors())
        hit = None
        for a in cands:
            if a is None: continue
            r = _match_compound(a, comp)
            if r[0]: hit = a; spec += r[1]; break
        if hit is None: return False, 0
        node = hit
    return True, spec


def gutter_rules(css):
    """-> [(selector, value, order)] for every rule declaring --bento-gutter OUTSIDE @container blocks"""
    flat = re.sub(r"@container[^{]*{(?:[^{}]*{[^{}]*})*[^{}]*}", "", css, flags=re.S)
    rules = []
    for i, m in enumerate(re.finditer(r"([^{}]+)\{([^{}]*)\}", flat)):
        decl = re.search(r"--bento-gutter\s*:\s*([^;]+);", m.group(2))
        if decl:
            for sel in _split_top(m.group(1), ","):
                rules.append((sel.strip(), decl.group(1).strip(), i))
    return rules


def resolve_var(value, css):
    v = value.strip()
    for _ in range(6):
        m = re.match(r"^var\((--[-a-zA-Z0-9]+)(?:,(.*))?\)$", v)
        if not m: break
        decls = re.findall(re.escape(m.group(1)) + r"\s*:\s*([^;]+);", css)
        v = decls[-1].strip() if decls else (m.group(2) or "").strip()
    if v in ("", "auto"): return None
    mm = re.match(r"^(\d+(?:\.\d+)?)(px)?$", v)
    return float(mm.group(1)) if mm else None


def gutter_of(el, rules, css):
    best = None  # (spec, order, value)
    unsupported = 0
    for sel, val, order in rules:
        ok, spec = match_selector(el, sel)
        if ok is None: unsupported += 1; continue
        if not ok: continue
        key = (spec, order)
        if best is None or key > best[0]: best = (key, val, sel)
    if best is None: return None, None, unsupported
    return resolve_var(best[1], css), best[2], unsupported


# ------------------------------------------------------------------ C9's grid model, read off the page
REPEAT_N_RE = re.compile(r"repeat\(\s*(\d+)\s*,")           # a LITERAL count written on the property
FULL_BLEED_RE = re.compile(r"^1\s*/\s*-1$")                 # "the whole row", whatever the row is
SPAN_RE = re.compile(r"^span\s+(\d+)$")


def resolve_str(value, css):
    """Follow var() chains textually (the numeric resolve_var above only answers lengths)."""
    v = (value or "").strip()
    for _ in range(6):
        m = re.search(r"var\((--[-a-zA-Z0-9]+)(?:,([^()]*))?\)", v)
        if not m: break
        decls = re.findall(re.escape(m.group(1)) + r"\s*:\s*([^;}]+)", css)
        v = v[:m.start()] + (decls[-1].strip() if decls else (m.group(2) or "").strip()) + v[m.end():]
    return v.strip()


def grid_cols_at(g, gtc_rules, band):
    """-> (columns, source) for one grid at one band. A rule that writes the count as a LITERAL
    `repeat(<n>,…)` and wins the cascade IS the count at that band; a rule that writes it through a
    var() is canon's band machinery, so the band's own count stands. Nothing is keyed to a class."""
    label, cols, width = band
    val = cascade(g, gtc_rules, width)
    if val:
        m = REPEAT_N_RE.search(val)
        if m: return max(1, int(m.group(1))), "grid-template-columns:%s" % val.strip()
    return max(1, cols), "band"


def tile_span_at(t, gc_rules, band, cols):
    """-> (span, source) for one tile at one band, cascaded from the page's own `grid-column`
    rules: `1 / -1` is the whole row (so the row it lands on is filled by it alone), `span N` is N,
    and a tile no rule reaches falls back to its own data-c. Always clamped to the column count,
    which is what the browser does with a span wider than the explicit grid."""
    val = cascade(t, gc_rules, band[2])
    if val:
        v = val.strip()
        if FULL_BLEED_RE.match(v): return cols, "1 / -1"
        m = SPAN_RE.match(v)
        if m: return max(1, min(int(m.group(1)), cols)), "span %s" % m.group(1)
    return max(1, min(int(t.attrs.get("data-c", "1") or 1), cols)), "data-c"


def flow_grid(items, cols):
    """Flow (span, rowspan) items into `cols` columns as CSS grid auto-placement does in SPARSE
    row-major order: the cursor never moves back, so a hole left behind stays a hole.
    -> (rows, placements) where rows is a list of per-row occupancy lists. An EMPTY CELL is an
    orphan, wherever it is.

    ⚠ #255 (conductor's call after V-C §3(d), Claude under s251-D15, Dave may strike): the flow is
    SPARSE regardless of the page's `grid-auto-flow`. `dense` is READ and REPORTED but is NOT a
    source of legality — `s255-D1` ruled the 4+2 wall legal, it never ruled that dense backfill
    fills a row. A dense page whose sparse flow leaves a hole packs whole only by rendering its
    tiles out of DOM order, a reorder C4 does not see (it reads `order:`, `*-reverse` and explicit
    line placement, not `dense`) and C8's rendered leg leaves unproven. So C9 judges the sparse
    flow, and V-C's `[4,4,2,2]`-in-6 page reds again."""
    rows, placements, cur = [], [], (0, 0)
    def ensure(r):
        while len(rows) <= r: rows.append([False] * cols)
    for span, rs in items:
        span, rs = max(1, min(span, cols)), max(1, rs)
        r, c = cur
        while True:
            if c + span > cols: r, c = r + 1, 0; continue
            ensure(r + rs - 1)
            if all(not rows[r + dr][c + dc] for dr in range(rs) for dc in range(span)): break
            c += 1
        ensure(r + rs - 1)
        for dr in range(rs):
            for dc in range(span): rows[r + dr][c + dc] = True
        placements.append((r, c, span, rs))
        cur = (r, c + span) if c + span < cols else (r + 1, 0)
    return rows, placements


# ------------------------------------------------------------------ the two conditions
ORDER_RE = re.compile(r"(?:^|[;{\s])order\s*:", re.M)
REVERSE_RE = re.compile(r"flex-direction\s*:\s*(?:row|column)-reverse")
PLACE_RE = re.compile(r"(?:^|[;{\s])(grid-row-start|grid-area)\s*:", re.M)


def _rule_blocks(css):
    """-> [(selector-text, declarations)] over the flat CSS incl. inside @container blocks."""
    flat = re.sub(r"@container[^{]*{", "", css)
    return [(m.group(1).strip(), m.group(2)) for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", flat)]


def check_c7_c8_c4(dom, css, bentos, gaps, lines, reds, unproven):
    """The three composition-class guideline rules wired by s245-D7 Q5 (b). All ADVISORY."""
    # C7 · neuro-003 — the OUTER wall of a bento-of-bentos carries >= 20px between its sections
    outer = [b for b in bentos if not any("c-bento" in a.classes for a in b.ancestors())
             and any("c-bento" in d.classes for d in b.descendants())]
    for b in outer:
        g = gaps.get(id(b)); nm = b.attrs.get("aria-label", "?")
        if g is None:
            unproven.append("C7 outer wall '%s' (line %d): gap unresolved, section air not measured" % (nm, b.line)); continue
        lines.append("C7 · outer wall '%s' line %d: %gpx between sections (neuro-003 floor 20px)" % (nm, b.line, g))
        if g < 20:
            reds.append("C7 RED  outer wall '%s' line %d: %gpx between sibling sections is under the neuro-003 floor of 20px" % (nm, b.line, g))
    if not outer:
        lines.append("C7 · no bento-of-bentos on this page; section air not applicable")
    # C8 · ID-9 — a group's members are contiguous tiles of ONE grid; nothing reorders them
    groups = [b for b in bentos if any("c-bento" in a.classes for a in b.ancestors())]
    for b in groups:
        nm = b.attrs.get("aria-label", "?")
        grids = [c for c in b.children if "c-bento__grid" in c.classes]
        if len(grids) != 1:
            reds.append("C8 RED  group '%s' line %d: %d grids (a group is ONE grid of contiguous members)" % (nm, b.line, len(grids))); continue
        kids = [c for c in grids[0].children if c.tag not in ("script", "style")]
        foreign = [c for c in kids if "c-bento__tile" not in c.classes]
        if foreign:
            reds.append("C8 RED  group '%s' line %d: %d non-tile element(s) interleaved with its members (first: <%s> line %d) - related content is no longer adjacent (ID-9)" % (nm, b.line, len(foreign), foreign[0].tag, foreign[0].line))
        lines.append("C8 · group '%s' line %d: %d member tile(s), %d foreign" % (nm, b.line, len(kids) - len(foreign), len(foreign)))
    for sel, decl in _rule_blocks(css):
        if ORDER_RE.search(decl) and ("c-bento" in sel or "tpl-group" in sel or "tile" in sel):
            reds.append("C8 RED  `%s` declares `order:` - a group's members must keep source order at every band (ID-9)" % sel[:80])
    lines.append("C8 · %d group(s) checked for contiguity (STATIC leg; the per-band RENDERED leg is UNPROVEN here - needs the browser)" % len(groups))
    # C4 · CA-2 — DOM order equals visual order: the page's own CSS never reorders content
    hits = []
    for sel, decl in _rule_blocks(css):
        for rx, what in ((ORDER_RE, "order:"), (REVERSE_RE, "flex-direction:*-reverse"), (PLACE_RE, "explicit grid line placement")):
            if rx.search(decl):
                hits.append("`%s` uses %s" % (sel[:80], what))
    for h in hits:
        reds.append("C4 RED  %s - visual order departs from DOM order (CA-2 / WCAG 1.3.2)" % h)
    lines.append("C4 · %d reordering declaration(s) in the artefact's own <style>" % len(hits))


def check(html):
    """-> (lines, reds, unproven). reds are prefixed C9/C1/C7/C8/C4; `blocking_reds()` splits them."""
    css = style_text(html)
    dom = parse_dom(html)
    lines, reds, unproven = [], [], []
    if not any("c-bento" in e.classes for e in dom.descendants()):
        return ["composition: NOT APPLICABLE - no .c-bento on this page"], [], []
    bl = bands(css)
    if not bl:
        return ["UNPROVEN: the artefact declares neither a base column count nor any @container band; C9 cannot read its grammar"], [], ["C9 bands"]
    if bl[0][0] != "base":
        unproven.append("C9 base band: the artefact never declares `--layout-bento-columns:<n>` (its .c-bento reads "
                        "var(--layout-bento-columns) and nothing sets it) - the base column count is UNDECLARED, so the "
                        "widest band is not checked; the gate does not assume 6")
    lines.append("C9 · bands read off the artefact: " + " · ".join("%s=%d cols" % (b[0], b[1]) for b in bl))
    rules = all_rules(css)
    gtc_rules, gc_rules, gaf_rules = decls_of(rules, "grid-template-columns"), decls_of(rules, "grid-column"), decls_of(rules, "grid-auto-flow")
    lit = ["%s%s" % (s, "" if not cd else " @" + ",".join("%s-width:%dpx" % k for k in cd)) for cd, s, v, _ in gtc_rules if REPEAT_N_RE.search(v)]
    fb = ["%s%s" % (s, "" if not cd else " @" + ",".join("%s-width:%dpx" % k for k in cd)) for cd, s, v, _ in gc_rules if FULL_BLEED_RE.match(v.strip())]
    lines.append("C9 · column counts written as a literal repeat() on the grid property: %s" % (lit or "none"))
    lines.append("C9 · tiles pinned to the whole row by `grid-column:1 / -1`: %s" % (fb or "none"))
    grids = [e for e in dom.descendants() if "c-bento__grid" in e.classes]
    tiles_seen = 0
    for g in grids:
        tiles = [c for c in g.children if "c-bento__tile" in c.classes]
        owner = g.parent
        label = owner.attrs.get("aria-label", owner.attrs.get("class", "?")) if owner else "?"
        tiles_seen += len(tiles)
        shown = []
        for band in bl:
            name = band[0]
            cols, src = grid_cols_at(g, gtc_rules, band)
            dense = "dense" in resolve_str(cascade(g, gaf_rules, band[2]) or "row", css)
            items, srcs = [], []
            for t in tiles:
                sp, how = tile_span_at(t, gc_rules, band, cols)
                items.append((sp, max(1, int(t.attrs.get("data-r", "1") or 1)))); srcs.append(how)
            rows, placements = flow_grid(items, cols)   # SPARSE always — `dense` is reported, not honoured
            shown.append("%s: %d cols%s%s -> %s" % (name, cols, "" if src == "band" else " (%s)" % src,
                                                    " [declares dense; judged sparse]" if dense else "", [i[0] for i in items]))
            if not rows: continue
            holes = [(r, c) for r, row in enumerate(rows) for c, v in enumerate(row) if not v]
            above = [h for h in holes if h[0] < len(rows) - 1]
            if above:
                r0, c0 = above[0]
                i = next((k for k, p in enumerate(placements) if (p[0], p[1]) > (r0, c0)), None)
                if i is None:
                    reds.append("C9 RED  grid '%s' (line %d): %d empty cell(s) above the last row at band %s (%d cols) - an orphan column" % (label, g.line, len(above), name, cols))
                else:
                    reds.append("C9 RED  line %d data-c=%s in '%s': span %d cannot take the %d column(s) left in row %d at band %s (%d cols) - it wraps and leaves %d empty cell(s) behind it, an orphan column" % (
                        tiles[i].line, tiles[i].attrs.get("data-c", "1"), label, items[i][0], cols - c0, r0 + 1, name, cols, len(above)))
            tail = [c for c, v in enumerate(rows[-1]) if not v]
            if tail:
                reds.append("C9 RED  grid '%s' (line %d): spans leave %d empty column(s) in the last row at band %s (%d cols) - not whole rows, an orphan cell" % (label, g.line, len(tail), name, cols))
        lines.append("C9 · grid '%s' line %d: %d tile(s) data-c=%s -> %s" % (label, g.line, len(tiles), [int(t.attrs.get("data-c", "1")) for t in tiles], "; ".join(shown)))
    lines.append("C9 · %d grid(s), %d tile(s) flowed at %d band(s)" % (len(grids), tiles_seen, len(bl)))
    # C1
    rules = gutter_rules(css)
    lines.append("C1 · %d `--bento-gutter` rule(s) in the artefact's own <style>" % len(rules))
    bentos = [e for e in dom.descendants() if "c-bento" in e.classes]
    gaps = {}
    for b in bentos:
        val, sel, uns = gutter_of(b, rules, css)
        gaps[id(b)] = val
        nm = b.attrs.get("aria-label", "?")
        if val is None:
            unproven.append("C1 gap of '%s' (line %d) could not be resolved from the page's CSS" % (nm, b.line))
            lines.append("C1 · '%s' line %d: gap UNRESOLVED (%d unsupported selector(s) skipped)" % (nm, b.line, uns))
            continue
        lines.append("C1 · '%s' line %d: gap %gpx  <- %s" % (nm, b.line, val, sel))
        if int(val) != val or int(val) not in STOPS:
            reds.append("C1 RED  '%s' line %d: gap %gpx is not on the ruled stop set %s" % (nm, b.line, val, list(STOPS)))
    pairs = 0
    for b in bentos:
        parent_bento = next((a for a in b.ancestors() if "c-bento" in a.classes), None)
        if parent_bento is None: continue
        pairs += 1
        gc, gp = gaps.get(id(b)), gaps.get(id(parent_bento))
        if gc is None or gp is None: continue
        if not gc < gp:
            reds.append("C1 RED  '%s' (%gpx) inside '%s' (%gpx): gap(child) < gap(parent) FAILS%s" % (
                b.attrs.get("aria-label", "?"), gc, parent_bento.attrs.get("aria-label", "?"), gp, " - EQUAL, the Polaris flat-hierarchy defect" if gc == gp else ""))
    lines.append("C1 · %d nested pair(s) compared" % pairs)
    check_c7_c8_c4(dom, css, bentos, gaps, lines, reds, unproven)
    return lines, reds, unproven


BLOCKING_ARMS = ("C9",)          # s245-D7 Q4 (b): C9 blocks; C1 advisory; C7/C8/C4 advisory (Q5 (b))


def blocking_reds(reds):
    return [r for r in reds if r.split()[0] in BLOCKING_ARMS]


def advisory_reds(reds):
    return [r for r in reds if r.split()[0] not in BLOCKING_ARMS]


def run(path, out=sys.stdout):
    html = open(path, encoding="utf-8").read()
    lines, reds, unproven = check(html)
    for l in lines: print("  " + l, file=out)
    for r in reds: print("  " + r, file=out)
    for u in unproven: print("  UNPROVEN: " + u, file=out)
    verdict = "RED" if reds else ("UNPROVEN" if unproven else "GREEN")
    print("_validate_composition: %s  (%s) - C9 reds %d [BLOCKING] · C1 %d · C7 %d · C8 %d · C4 %d [advisory] · unproven %d" % (
          verdict, os.path.relpath(path, ROOT) if path.startswith(ROOT) else path,
          sum(r.startswith("C9") for r in reds), sum(r.startswith("C1") for r in reds), sum(r.startswith("C7") for r in reds),
          sum(r.startswith("C8") for r in reds), sum(r.startswith("C4") for r in reds), len(unproven)), file=out)
    return 1 if reds else (77 if unproven else 0)


def selftest():
    import tempfile
    real = open(REAL, encoding="utf-8").read()
    # L3 #245 finding 5: the snippet never declared its base column count, so this gate REFUSED (77) on
    # the one artefact it exists for. REPAIRED at #245 L5 (the two theme blocks now declare
    # `--layout-bento-columns:6`, the value the file's own comment and its meta always claimed). The
    # real artefact is driven as shipped (arm R, GREEN) and with the literal stripped (arm R0, UNPROVEN
    # 77, never green) - a gate that assumed 6 would have hidden the defect and would hide its return.
    DECL = "--layout-bento-gutter:0; --layout-bento-outer-padding:0; --layout-bento-row-unit:320px; --layout-bento-columns:6;"
    assert real.count(DECL) == 2, "the snippet's two theme blocks must declare the column count (L3 finding 5, repaired L5)"
    raw = real.replace(" --layout-bento-columns:6;", "")
    assert "--layout-bento-columns:" not in raw
    # anchors, each must be present exactly once so a mutant is a real one
    # ⚠ #255: the KPI anchor DRIFTED. This tile was `data-c="3"` when the anchors were written at
    # #245 (git show 5ae4d32:knowledge/snippets/Template-dashboard-bento.reference.html). #249/#251
    # (0979a9b / fc1209b, DP-08 + s247-D3/s251-D1) took the two status tiles out of the lead row and
    # page rule 10a pinned that grid to FOUR columns at every band, so its four true KPIs are now
    # `data-c="1"`. The anchor is re-pointed at the SAME tile, not weakened: still `== 1` below.
    KPI = '<div class="c-bento__tile kpi-tile has-cta" role="group" aria-label="Closing balance" data-c="1" data-r="1">'
    GROUP_GAP = '.tpl-page .c-bento.tpl-group[data-bento-role="dashboard"]{ --bento-gutter:4px; }'
    WALL_GAP = '--bento-gutter:40px; --bento-row-unit:auto; }'
    # #255, s255-D1: the two RULED declarations C9 was taught to read. Each is anchored so the arms
    # below can DELETE it from the page's CSS — the mutation that proves the reading is load-bearing
    # and that nothing is exempted by name: with the declaration gone the same tiles red again.
    RULE_10A = '.tpl-page .c-bento.tpl-group-lead > .c-bento__grid{ grid-template-columns:repeat(4,minmax(0,1fr)); }'
    RULE_6BI = '.tpl-page .c-bento__tile.tpl-group-context{ grid-column:1 / -1; }'
    EVIDENCE = 'data-c="4" data-r="1" aria-label="Spending analysis">'
    # #255 after V-C §3(d): a hand-built page, deliberately carrying NEITHER ruled declaration —
    # no literal repeat(), no `grid-column:1 / -1` — so the only thing under test is the flow.
    DENSE_TILES = '<div class="c-bento__tile" data-c="%d" data-r="1">%s</div>'
    def dense_page(order):
        return ('<html><body><main class="tpl-page">\n<style>\n'
                '.tpl-page{ --layout-bento-columns:6; }\n'
                '.tpl-page .c-bento{ --bento-gutter:4px; }\n'
                '.tpl-page .c-bento__grid{ display:grid; grid-auto-flow:row dense; }\n'
                '</style>\n<section class="c-bento" aria-label="Dense page">\n'
                '  <div class="c-bento__grid">\n'
                + "".join("  " + DENSE_TILES % (sp, nm) + "\n" for sp, nm in order)
                + '  </div>\n</section>\n</main></body></html>\n')
    DENSE_PAGE = dense_page([(4, "A"), (4, "B"), (2, "C"), (2, "D")])
    DENSE_PAGE_CTRL = dense_page([(4, "A"), (2, "B"), (4, "C"), (2, "D")])
    for a in (KPI, GROUP_GAP, WALL_GAP, RULE_10A, RULE_6BI, EVIDENCE): assert real.count(a) == 1, a
    arms = [
        ("R  · the REAL artefact as shipped (column count declared since #245 L5) -> GREEN", real, 0, None),
        ("R0 · the artefact with its column-count literal STRIPPED (L3 finding 5 as it was) -> UNPROVEN 77, never green", raw, 77, None),
        # M1/M2 keep their NAMED legs and are RE-DERIVED at #255 (s255-D1) against the flow model:
        # M1 is the ORPHAN-COLUMN leg (a tile that cannot take the columns left in its row, so it
        # wraps and leaves cells empty behind it), M2 is the WHOLE-ROWS leg (every row fills except
        # the last). The old mutations were `4 does not divide 6` and `3 divides but does not sum` —
        # arithmetic on a proxy; `s248-D1`'s ruled 4+2 wall is exactly the case where the proxy and
        # the render disagree, so each mutation is re-derived to produce a REAL empty cell.
        ("M1 · the wall's evidence tile data-c 4 -> 5 (5+2 cannot share a 6-column row: the rail wraps and one column stays empty)", real.replace(EVIDENCE, 'data-c="5" data-r="1" aria-label="Spending analysis">'), 1, "C9"),
        ("M2 · one KPI tile data-c 1 -> 3 (3+1 fills the lead row, the other two KPIs leave the last row half empty)", real.replace(KPI, KPI.replace('data-c="1"', 'data-c="3"')), 1, "C9"),
        # M1b/M1c — the two ruled declarations s255-D1 taught C9, each DELETED from the page's CSS.
        # These are the bite: if the reader were exempting a class name rather than reading the
        # property, the page would stay green with the declaration gone.
        ("M1b · rule 10a DELETED from the CSS (the lead grid falls back to the band count: four data-c=1 tiles in 6 / 3 / 2 columns)", real.replace(RULE_10A, ""), 1, "C9"),
        ("M1c · rule 6b(i) DELETED from the CSS (the context rail is 2 of 3 at <=1100px again - the orphan s248-D1 ruled a defect)", real.replace(RULE_6BI, ""), 1, "C9"),
        ("M3 · group gutter 4 -> 40 (EQUAL to the wall - the flat ladder)", real.replace(GROUP_GAP, GROUP_GAP.replace("4px", "40px")), 1, "C1"),
        ("M4 · wall gutter 40 -> 4 (child not strictly smaller)", real.replace(WALL_GAP, WALL_GAP.replace("40px", "4px")), 1, "C1"),
        ("M5 · group gutter 4 -> 5 (off the ruled stop set)", real.replace(GROUP_GAP, GROUP_GAP.replace("4px", "5px")), 1, "C1"),
        ("M6 · group gutter 4 -> 24 AND wall 40 -> 16 (both on stops, ladder inverted)", real.replace(GROUP_GAP, GROUP_GAP.replace("4px", "24px")).replace(WALL_GAP, WALL_GAP.replace("40px", "16px")), 1, "C1"),
        ("K1 · control: group gutter 4 -> 2 (still < 40, on a stop)", real.replace(GROUP_GAP, GROUP_GAP.replace("4px", "2px")), 0, None),
        ("K2 · control: wall gutter 40 -> 24 (still > 4, on a stop)", real.replace(WALL_GAP, WALL_GAP.replace("40px", "24px")), 0, None),
        # s245-D7 Q5 (b) — the three guideline-rule arms
        ("M7 · wall gutter 40 -> 16 (on a stop, > 4, but UNDER the neuro-003 20px section floor)", real.replace(WALL_GAP, WALL_GAP.replace("40px", "16px")), 1, "C7"),
        ("M8 · a foreign <div> interleaved between two KPI tiles (ID-9: members no longer adjacent)", real.replace(KPI, '<div class="tpl-stray">stray</div>' + KPI), 1, "C8"),
        ("M8b · `.c-bento__tile{order:2}` in the page's own CSS (ID-9: a member reordered)", real.replace(GROUP_GAP, GROUP_GAP + "\n.tpl-page .c-bento__tile.kpi-tile{ order:2; }"), 1, "C8"),
        ("M9 · `flex-direction:row-reverse` on a content container (CA-2: visual order departs from DOM)", real.replace(GROUP_GAP, GROUP_GAP + "\n.tpl-page .kpi-tile{ display:flex; flex-direction:row-reverse; }"), 1, "C4"),
        ("M9b · explicit `grid-row-start:1` line placement (CA-2)", real.replace(GROUP_GAP, GROUP_GAP + "\n.tpl-page .kpi-tile{ grid-row-start:1; }"), 1, "C4"),
        ("K3 · control: `border:` and `--border:` in CSS must NOT read as `order:` (the substring trap)", real.replace(GROUP_GAP, GROUP_GAP + "\n.tpl-page .kpi-tile{ border:1px solid var(--border); }"), 0, None),
        ("K4 · control: a page with no .c-bento is NOT APPLICABLE -> 0", "<html><body><main><p>no bento</p></main></body></html>", 0, None),
        # K5 · the reader must read the NUMBER on the property, not the rule's name. Two columns is
        # a different count from four and the four data-c=1 tiles still fill whole rows, so the page
        # stays GREEN — while M1b (the same rule deleted) goes RED. Together they prove the count is
        # DERIVED: neither `.tpl-group-lead` nor the literal 4 is known to the gate.
        ("K5 · control: rule 10a's repeat(4) -> repeat(2) (a different count, still whole rows: 4 tiles / 2 cols)",
         real.replace(RULE_10A, RULE_10A.replace("repeat(4,", "repeat(2,")), 0, None),
        # M10 / K6 — the conductor's call after V-C §3(d). A HAND-BUILT page (not the artefact):
        # six columns declared, no literal repeat(), no `1 / -1`, `grid-auto-flow: row dense`, and
        # tiles [4,4,2,2]. Dense backfill would pack that into two whole rows — but only by putting
        # tile C ahead of tile B on screen, a reorder C4 cannot see and C8's rendered leg leaves
        # unproven, and s255-D1 never made dense a source of legality. So C9 judges the SPARSE flow
        # and this page is RED. K6 is the SAME four tiles ordered [4,2,4,2], which fills both rows
        # sparse: the tiles are not the defect, the DOM order is — which is the point.
        ("M10 · six columns, tiles [4,4,2,2], `grid-auto-flow:row dense` (packs whole only by backfilling out of DOM order)", DENSE_PAGE, 1, "C9"),
        ("K6 · control: the same four tiles ordered [4,2,4,2] (fills both rows SPARSE, dense or not)", DENSE_PAGE_CTRL, 0, None),
    ]
    import io
    fails = 0
    d = tempfile.mkdtemp()
    for i, (name, html, want, cls) in enumerate(arms):
        p = os.path.join(d, "arm%d.html" % i); open(p, "w", encoding="utf-8").write(html)
        buf = io.StringIO(); rc = run(p, buf); txt = buf.getvalue()
        ok = rc == want and (cls is None or ("%s RED" % cls) in txt)
        fails += not ok
        print("%s  %s  (rc %d, want %d)" % ("GREEN" if ok else "RED  ", name, rc, want))
        if not ok: print(txt)
    print("selftest: %d arm(s) · %d failed" % (len(arms), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv: sys.exit(selftest())
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)  # help gate above already answers --help
    sys.exit(run(sys.argv[1]))
