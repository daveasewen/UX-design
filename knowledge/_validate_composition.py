#!/usr/bin/env python3
"""
_validate_composition.py — rB's composition conditions (#234), driven against a REAL bento
artefact (never the library). Built at #245 L3 as `check_composition.py`; RULED and REGISTERED by
s245-D7 (Dave: "I'll go with all the recommendations" — Q4 (b), Q5 (b)).

  C9  SPAN LEGALITY   every tile's effective span divides the column count at EVERY compiled band
                      (clamp = min(data-c, cols), exactly as the artefact's own band CSS clamps), AND
                      every grid's effective spans sum to whole rows at every band (no orphan cell).
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

  python3 knowledge/_validate_composition.py <artefact.html>   -> report; exit 0 green, 1 red, 77 UNPROVEN
  python3 knowledge/_validate_composition.py --selftest        -> the real bento snippet + 11 mutants + 5 controls (17 arms)

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
    """-> [(label, cols, {data_c: span})] read off the artefact: the base column count and each
    @container (max-width) block that rewrites --bento-cols-now and clamps spans."""
    base = re.search(r"--layout-bento-columns\s*:\s*(\d+)", css)
    out = [("base", int(base.group(1)), {})] if base else []
    for m in re.finditer(r"@container[^{]*\(max-width:\s*(\d+)px\)\s*{(.*?)}\s*}", css, flags=re.S):
        block = m.group(2) + "}"
        cols = re.search(r"--bento-cols-now\s*:\s*(\d+)", block)
        if not cols: continue
        clamp = {}
        for sel, span in re.findall(r"((?:\.c-bento__grid\s*>\s*\.c-bento__tile\[data-c=\"\d\"\]\s*,?\s*)+)\{grid-column:span (\d+);\}", block):
            for c in re.findall(r'data-c="(\d)"', sel): clamp[int(c)] = int(span)
        out.append(("<=%spx" % m.group(1), int(cols.group(1)), clamp))
    return out


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
        comps = _compounds(sel)
        ok, spec = _match_compound(el, comps[-1][1])
        if ok is None: unsupported += 1; continue
        if not ok: continue
        # ancestors: each earlier compound must match some ancestor (child combinator = the parent)
        node, good = el, True
        for comb, comp in reversed(comps[:-1]):
            cands = [node.parent] if comb == ">" else list(node.ancestors())
            hit = None
            for a in cands:
                if a is None: continue
                r = _match_compound(a, comp)
                if r[0]: hit = a; spec += r[1]; break
            if hit is None: good = False; break
            node = hit
        if not good: continue
        key = (spec, order)
        if best is None or key > best[0]: best = (key, val, sel)
    if best is None: return None, None, unsupported
    return resolve_var(best[1], css), best[2], unsupported


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
    grids = [e for e in dom.descendants() if "c-bento__grid" in e.classes]
    tiles_seen = 0
    for g in grids:
        tiles = [c for c in g.children if "c-bento__tile" in c.classes]
        owner = g.parent
        label = owner.attrs.get("aria-label", owner.attrs.get("class", "?")) if owner else "?"
        spans = []
        for t in tiles:
            c = int(t.attrs.get("data-c", "1")); tiles_seen += 1
            per_band = []
            for name, cols, clamp in bl:
                eff = clamp.get(c, min(c, cols))
                per_band.append((name, cols, eff))
                if cols % eff != 0:
                    reds.append("C9 RED  line %d data-c=%d in '%s': span %d does not divide %d columns at band %s (orphan column)" % (t.line, c, label, eff, cols, name))
            spans.append(per_band)
        for i, (name, cols, _) in enumerate(bl):
            total = sum(s[i][2] for s in spans)
            if total % cols != 0:
                reds.append("C9 RED  grid '%s' (line %d): spans sum to %d at band %s (%d cols) - not whole rows, an orphan cell" % (label, g.line, total, name, cols))
        lines.append("C9 · grid '%s' line %d: %d tile(s) data-c=%s -> %s" % (label, g.line, len(tiles), [int(t.attrs.get("data-c", "1")) for t in tiles],
                     "; ".join("%s: %s" % (b[0], [s[i][2] for s in spans]) for i, b in enumerate(bl))))
    lines.append("C9 · %d grid(s), %d tile(s) checked at %d band(s)" % (len(grids), tiles_seen, len(bl)))
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
    KPI = '<div class="c-bento__tile kpi-tile has-cta" role="group" aria-label="Closing balance" data-c="3" data-r="1">'
    GROUP_GAP = '.tpl-page .c-bento.tpl-group[data-bento-role="dashboard"]{ --bento-gutter:4px; }'
    WALL_GAP = '--bento-gutter:40px; --bento-row-unit:auto; }'
    for a in (KPI, GROUP_GAP, WALL_GAP): assert real.count(a) == 1, a
    arms = [
        ("R  · the REAL artefact as shipped (column count declared since #245 L5) -> GREEN", real, 0, None),
        ("R0 · the artefact with its column-count literal STRIPPED (L3 finding 5 as it was) -> UNPROVEN 77, never green", raw, 77, None),
        ("M1 · one KPI tile data-c 3 -> 2 (orphan at the 3-column band)", real.replace(KPI, KPI.replace('data-c="3"', 'data-c="2"')), 1, "C9"),
        ("M2 · one KPI tile data-c 3 -> 6 (divides, but the grid no longer sums to whole rows at 6 cols)", real.replace(KPI, KPI.replace('data-c="3"', 'data-c="6"')), 1, "C9"),
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
