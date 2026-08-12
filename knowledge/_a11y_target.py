#!/usr/bin/env python3
"""
_a11y_target.py — the MARKUP-DRIVEN target-size measurement engine (s114-D5).

WHY THIS FILE EXISTS (read before touching the gate that consumes it).

`_validate_a11y.py` used to answer "is this a control?" by pattern-matching CSS
SELECTOR TEXT against a hand-maintained name list (`CTRL`), and "how big is it?"
by regexing `width:Npx` out of the same rule body. That single design choice
produced FOUR symptom sets that were reported as four separate problems:

  (a) SIX PHANTOM FAILURES (#114-D3). `.as-trigger .chev` (16x16) was flagged as
      an under-floor control. `.chev` is a `<span aria-hidden="true">` chevron
      inside `<button class="as-trigger">` whose own box is `min-height:44px`.
      The selector matched because `is_ctrl()` tested EVERY class token in the
      selector, ancestors included — so any decoration of an interactive parent
      was classified as the control. Same for `.card.opt .radio`, `.sort .ic`,
      `.opt .tick`, `.fu-remove .icn`, `.tp-opt .tick`.

  (b) THE axs-003 DETECTOR QUIRK. The mirror image of (a): a real control whose
      selector shape was not on the list was never checked at all. `.dv-vt` and
      `.dv-tbl-toggle` (the chart toolbar) and EVERY `<summary>` in the library
      passed by omission, not by measurement.

  (c) LITERAL-PX BLINDNESS. `.dv-vt{height:var(--control-h)}` is 32px and was
      invisible, because the regex could only read a literal `Npx`.

  (d) A BLIND EXEMPTION. Any selector with a `::before` rule was exempted from
      both tiers and reported "NOT MEASURED", because static CSS supposedly could
      not size an expander. It can, once var() resolves: `min-width:var(--hit,44px)`
      is a number.

ALL FOUR ARE ONE CAUSE: the gate measured CSS TEXT, and a control is a MARKUP
ELEMENT. So this module builds a real (small) DOM, a real (small) cascade, and
asks each ELEMENT its own question. (a) and (b) cannot recur independently
because they are no longer independent code paths [[conflated-fix-guarantees-recurrence]].

DECLARED GAPS — these are UNMEASURED, and saying so is the point:
  * `@media`-conditioned sizes are not used for sizing. A base rule is measured;
    a narrow-viewport override is not. Reported as a residual, never as a pass.
  * Elements with no declared width/height are LAYOUT-DETERMINED and come back
    `unmeasured`, never `pass` and never `fail` — a static parse must not guess
    [[measuring-tool-must-not-guess]].
  * `transform` is not applied. The Chart-line diamond swatch stands a 12x12 box
    on its corner; that is a render-axis fact, not a CSS-text fact.
  * SVG marks are measured in USER UNITS scaled by the svg's own width/viewBox
    ratio. A `.dv-fit-on` chart is re-scaled at runtime by dv-behaviour.js; that
    axis is not measured here.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re, math
from html.parser import HTMLParser

# ---------------------------------------------------------------- thresholds
TARGET_CONTROL = 44      # HSBC default (aid-009 / axs-003 / ID-26)
TARGET_MARK = 24         # WCAG 2.5.8 dense-case minimum (Dave, s116-D1: marks are
                         # exempt from 44, NOT exempt from the check)
FLOOR = 24               # blocking floor for either tier (aid-009, 2026-07-03)

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr", "use", "stop"}

# Roles the corpus uses. A role outside BOTH sets fails loud (dv-vocab shape,
# ds-014/ds-015): an unknown must never default to "not a control".
INTERACTIVE_ROLES = {
    "button", "checkbox", "combobox", "link", "menuitem", "option", "radio",
    "slider", "switch", "tab", "textbox",
}
NON_INTERACTIVE_ROLES = {
    "alert", "dialog", "grid", "group", "img", "list", "listbox", "listitem",
    "menu", "none", "presentation", "progressbar", "radiogroup", "region",
    "separator", "status", "table", "tablist", "tabpanel", "timer", "tooltip",
    "row", "cell", "columnheader", "rowheader", "note", "figure", "document",
    "banner", "main", "navigation", "complementary", "contentinfo", "search",
    "form", "heading", "term", "definition", "toolbar", "marquee", "log",
}
# Native tags that ARE controls regardless of role. This is EXACTLY the ruled
# control set (2026-07-25 brief, rule text): "a control is any `button`,
# `summary`, `a[href]`, or `[role=button|checkbox|switch|tab|option]`".
NATIVE_CONTROL_TAGS = {"button", "summary"}
# DECLARED SCOPE BOUNDARY — form FIELDS (`input`, `textarea`, `select`) are NOT in
# the ruled control set and are NOT swept here. Two reasons, both measured: their
# box is layout-determined (`width:100%`), and the corpus's native checkboxes and
# radios are deliberately 0x0 visually-hidden proxies behind a styled `.sc-box`
# (Selection-controls). Sweeping them reproduces the phantom-failure shape this
# rebuild exists to remove. UNSWEPT, not clean — a named residual for Dave.
FIELD_TAGS = {"input", "textarea", "select", "option", "optgroup"}


# =============================================================== the tiny DOM
class El:
    __slots__ = ("tag", "attrs", "parent", "children", "classes", "line")

    def __init__(self, tag, attrs, parent, line):
        self.tag = tag.lower()
        self.attrs = attrs
        self.parent = parent
        self.children = []
        self.classes = set((attrs.get("class") or "").split())
        self.line = line

    def ancestors(self):
        p = self.parent
        while p is not None:
            yield p
            p = p.parent

    def descr(self):
        bits = [self.tag]
        if self.attrs.get("id"):
            bits.append("#" + self.attrs["id"])
        for c in sorted(self.classes):
            bits.append("." + c)
        return "".join(bits)


class _DOM(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = El("#document", {}, None, 0)
        self.cur = self.root
        self.styles = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v if v is not None else "") for k, v in attrs}
        el = El(tag, d, self.cur, self.getpos()[0])
        self.cur.children.append(el)
        if tag.lower() == "style":
            self._in_style = True
        if tag.lower() not in VOID:
            self.cur = el

    def handle_startendtag(self, tag, attrs):
        d = {k.lower(): (v if v is not None else "") for k, v in attrs}
        self.cur.children.append(El(tag, d, self.cur, self.getpos()[0]))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "style":
            self._in_style = False
        node = self.cur
        while node is not None and node.tag != tag:
            node = node.parent
        if node is not None and node.parent is not None:
            self.cur = node.parent

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)


def walk(el):
    for c in el.children:
        yield c
        for g in walk(c):
            yield g


# ================================================================ tiny CSS
def _split_top(s, sep):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [p for p in out]


def parse_decls(body):
    d = {}
    for part in _split_top(body, ";"):
        part = part.strip()
        if not part:
            continue
        i = part.find(":")
        if i < 0:
            continue
        k = part[:i].strip()
        v = part[i + 1:].strip()
        d[k if k.startswith("--") else k.lower()] = v
    return d


def parse_rules(css, out, media=""):
    """Flatten a stylesheet to [(selector_text, decls, media)]. @keyframes and
    @font-face are dropped; conditional groups recurse carrying their condition."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        prelude = css[i:j]
        prelude = prelude.rsplit(";", 1)[-1].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if prelude.startswith("@"):
            if re.match(r"@(media|supports|layer|container|scope)\b", prelude):
                parse_rules(body, out, (media + " " + prelude).strip())
        elif prelude:
            out.append((prelude, parse_decls(body), media))
        i = k
    return out


# ---- compound-selector matching (SUBJECT-aware, which is the (a) fix) -------
_STATE_PSEUDO = re.compile(
    r":(hover|active|focus|focus-visible|focus-within|visited|target|"
    r"checked|disabled|indeterminate|placeholder-shown|invalid|valid)\b")
_PSEUDO_EL = re.compile(r"::(before|after|marker|placeholder|backdrop|"
                        r"selection|first-line|first-letter|-webkit-[\w-]+)")
_COMBINATOR = re.compile(r"\s*([>+~])\s*|\s+")


class Compound:
    __slots__ = ("tag", "classes", "id", "attrs", "extra_spec", "universal")

    def __init__(self, text):
        self.tag, self.classes, self.id, self.attrs = None, set(), None, []
        self.extra_spec = 0
        self.universal = False
        t = text
        # attribute selectors
        for m in re.finditer(r'\[([\w:-]+)(?:([~^$*|]?=)"?([^\]"]*)"?)?\]', t):
            self.attrs.append((m.group(1).lower(), m.group(2), m.group(3)))
        t = re.sub(r"\[[^\]]*\]", "", t)
        # functional / state pseudo-classes contribute specificity, not matching
        self.extra_spec += len(re.findall(r"(?<!:):[\w-]+", t))
        t = re.sub(r"::?[\w-]+(\([^)]*\))?", "", t)
        for m in re.finditer(r"\.([\w-]+)", t):
            self.classes.add(m.group(1))
        m = re.search(r"#([\w-]+)", t)
        if m:
            self.id = m.group(1)
        t = re.sub(r"[.#][\w-]+", "", t).strip()
        if t == "*":
            self.universal = True
        elif t:
            self.tag = t.lower()

    def matches(self, el):
        if self.tag and self.tag != el.tag:
            return False
        if self.id and el.attrs.get("id") != self.id:
            return False
        if not self.classes <= el.classes:
            return False
        for name, op, val in self.attrs:
            if name not in el.attrs:
                return False
            if op == "=" and el.attrs[name] != val:
                return False
            if op == "~=" and val not in el.attrs[name].split():
                return False
        return True

    def specificity(self):
        return ((1 if self.id else 0),
                len(self.classes) + len(self.attrs) + self.extra_spec,
                (1 if self.tag else 0))


class Selector:
    """A single complex selector, kept as [(combinator, Compound), ...] with the
    SUBJECT last. `pseudo_el` is the ::before/::after tail, if any."""
    __slots__ = ("parts", "pseudo_el", "has_state", "spec", "text")

    def __init__(self, text):
        self.text = text.strip()
        m = _PSEUDO_EL.search(self.text)
        self.pseudo_el = m.group(1) if m else None
        self.has_state = bool(_STATE_PSEUDO.search(self.text))
        body = _PSEUDO_EL.sub("", self.text)
        toks, cur, comb = [], "", " "
        i = 0
        depth = 0
        while i < len(body):
            ch = body[i]
            if ch in "([":
                depth += 1
            elif ch in ")]":
                depth -= 1
            if depth == 0 and (ch.isspace() or ch in ">+~"):
                m2 = re.match(r"\s*([>+~])?\s*", body[i:])
                nxt = m2.group(1) or " "
                if cur.strip():
                    toks.append((comb, Compound(cur.strip())))
                    cur, comb = "", nxt
                else:
                    comb = nxt
                i += m2.end()
                continue
            cur += ch
            i += 1
        if cur.strip():
            toks.append((comb, Compound(cur.strip())))
        self.parts = toks
        a = b = c = 0
        for _, cp in toks:
            s = cp.specificity()
            a, b, c = a + s[0], b + s[1], c + s[2]
        self.spec = (a, b, c)

    def matches(self, el):
        if not self.parts:
            return False
        if not self.parts[-1][1].matches(el):
            return False
        # walk the ancestor chain right-to-left. `+`/`~` are not modelled: the
        # subject match stands alone for them (declared over-match, never an
        # under-match, and no sibling rule in the corpus sets a target size).
        node = el
        for comb, cp in reversed(self.parts[:-1]):
            if comb == ">":
                node = node.parent
                if node is None or not cp.matches(node):
                    return False
            elif comb in ("+", "~"):
                return True
            else:
                found = None
                p = node.parent
                while p is not None:
                    if cp.matches(p):
                        found = p
                        break
                    p = p.parent
                if found is None:
                    return False
                node = found
        return True


def compile_sheet(styles):
    raw = []
    for css in styles:
        parse_rules(css, raw)
    out = []
    for order, (sel_text, decls, media) in enumerate(raw):
        for one in _split_top(sel_text, ","):
            one = one.strip()
            if not one:
                continue
            try:
                s = Selector(one)
            except Exception:
                continue
            if s.parts:
                out.append((s, decls, media, order))
    return out


# ------------------------------------------------------------- the cascade
class Sheet:
    def __init__(self, styles):
        self.rules = compile_sheet(styles)
        self._cache = {}

    def matched(self, el, pseudo=None, allow_state=False, allow_media=False):
        key = (id(el), pseudo, allow_state, allow_media)
        if key in self._cache:
            return self._cache[key]
        hits = []
        for s, decls, media, order in self.rules:
            if s.pseudo_el != pseudo:
                continue
            if s.has_state and not allow_state:
                continue
            if media and not allow_media:
                continue
            if s.matches(el):
                hits.append((s.spec, order, decls, s))
        hits.sort(key=lambda h: (h[0], h[1]))
        self._cache[key] = hits
        return hits

    def declared(self, el, pseudo=None, allow_media=False):
        d = {}
        for _, _, decls, _ in self.matched(el, pseudo, allow_media=allow_media):
            d.update(decls)
        if pseudo is None and el.attrs.get("style"):
            d.update(parse_decls(el.attrs["style"]))
        return d

    def has_media_size_rule(self, el):
        for _, _, decls, _ in self.matched(el, None, allow_media=True):
            if any(k in decls for k in ("width", "height", "min-width", "min-height")):
                return True
        return False

    # ---- custom properties: nearest declaring ancestor wins ---------------
    def custom(self, el, name, depth=0):
        if depth > 12:
            return None
        node = el
        while node is not None:
            if node.attrs.get("style"):
                v = parse_decls(node.attrs["style"]).get(name)
                if v is not None:
                    return v
            for _, _, decls, _ in reversed(self.matched(node, None)):
                if name in decls:
                    return decls[name]
            node = node.parent
        return None


_VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\)[^()]*)*))?\)")


def resolve(sheet, el, value, depth=0):
    """Expand var() against the element's own cascade. Returns None if a
    referenced property is undefined and has no fallback."""
    if value is None or depth > 10:
        return value
    out = value
    for _ in range(10):
        m = _VAR.search(out)
        if not m:
            break
        name, fallback = m.group(1), m.group(2)
        got = sheet.custom(el, name)
        if got is None:
            got = fallback
        if got is None:
            return None
        got = resolve(sheet, el, got.strip(), depth + 1)
        if got is None:
            return None
        out = out[:m.start()] + got + out[m.end():]
    return out


_LEN = re.compile(r"^(-?\d*\.?\d+)(px|rem|em|pt|)$")


def to_px(value, root_font=16.0, font=16.0):
    if value is None:
        return None
    v = value.strip().lower()
    v = v.split("!")[0].strip()
    m = _LEN.match(v)
    if not m:
        return None
    n = float(m.group(1))
    unit = m.group(2)
    if unit == "px" or unit == "":
        return n if (unit == "px" or n == 0) else None
    if unit == "rem":
        return n * root_font
    if unit == "em":
        return n * font
    if unit == "pt":
        return n * 4 / 3
    return None


# ==================================================== classification (b) fix
def is_hidden(el):
    node = el
    while node is not None:
        if node.attrs.get("aria-hidden") == "true":
            return True
        if "hidden" in node.attrs and node.tag != "input":
            # a <details> panel is `hidden` only while closed; that is state, not
            # a permanent hide, so it does not remove its contents from scope.
            pass
        node = node.parent
    return False


def is_data_mark(el):
    if el.classes & {"dv-series", "dv-marker"}:
        return True
    if el.tag in {"rect", "path", "circle", "polygon", "polyline", "line", "g"} \
            and "data-series-group" in el.attrs:
        return True
    return False


def is_control(el):
    if is_hidden(el):
        return False
    role = (el.attrs.get("role") or "").strip().lower()
    if role in NON_INTERACTIVE_ROLES:
        return False
    if el.tag in FIELD_TAGS:
        return False
    if el.tag in NATIVE_CONTROL_TAGS:
        return True
    if el.tag == "a" and "href" in el.attrs:
        return True
    if role in INTERACTIVE_ROLES:
        return True
    ti = el.attrs.get("tabindex")
    if ti is not None:
        try:
            if int(ti) >= 0:
                return True
        except ValueError:
            return False
    return False


def unknown_roles(root):
    bad = set()
    for el in walk(root):
        r = (el.attrs.get("role") or "").strip().lower()
        if r and r not in INTERACTIVE_ROLES and r not in NON_INTERACTIVE_ROLES:
            bad.add(r)
    return sorted(bad)


# ================================================== measurement of a control
class Result:
    __slots__ = ("el", "kind", "verdict", "w", "h", "detail", "target")

    def __init__(self, el, kind, verdict, w, h, detail, target):
        self.el, self.kind, self.verdict = el, kind, verdict
        self.w, self.h, self.detail, self.target = w, h, detail, target


def _wh(w, h):
    f = lambda v: ("%g" % v) if v is not None else "auto"
    return "%sx%s" % (f(w), f(h))


def _dim(sheet, el, decls, base, mini):
    vals = []
    for prop in (base, mini):
        if prop in decls:
            px = to_px(resolve(sheet, el, decls[prop]))
            if px is None:
                continue
            # `min-width:0` / `min-height:0` are RESETS (the flexbox overflow idiom),
            # not a declared target size. Reading them as "this control is 0px" is the
            # phantom-failure shape all over again, one layer down.
            if prop == mini and px == 0:
                continue
            vals.append(px)
    return max(vals) if vals else None


def expander_box(sheet, el):
    """Read the canon invisible hit-expander on ::before/::after. This is (d):
    once var() resolves, `min-width:var(--hit,44px)` is a NUMBER, so the
    expander is MEASURED rather than blanket-exempted."""
    best = None
    for pseudo in ("before", "after"):
        decls = sheet.declared(el, pseudo)
        if not decls or "content" not in decls:
            continue
        if decls.get("position", "").strip().lower() not in ("absolute", "fixed"):
            continue
        w = _dim(sheet, el, decls, "width", "min-width")
        h = _dim(sheet, el, decls, "height", "min-height")
        if w is None and h is None:
            continue
        cand = (pseudo, w, h)
        if best is None or (min(w or 0, h or 0) > min(best[1] or 0, best[2] or 0)):
            best = cand
    return best


EXCEPTION_ATTR = "data-a11y-target-exception"


def measure_control(sheet, el, target=TARGET_CONTROL):
    reason = (el.attrs.get(EXCEPTION_ATTR) or '').strip()
    if reason:
        return Result(el, "control", "exception", None, None,
                      "claimed 2.5.8 exception: %s" % reason.strip(), target)

    exp = expander_box(sheet, el)
    decls = sheet.declared(el)
    w = _dim(sheet, el, decls, "width", "min-width")
    h = _dim(sheet, el, decls, "height", "min-height")

    if exp:
        pseudo, ew, eh = exp
        ew = ew if ew is not None else w
        eh = eh if eh is not None else h
        if ew is None or eh is None:
            return Result(el, "control", "unmeasured", ew, eh,
                          "::%s expander declared but one dimension is layout-determined"
                          % pseudo, target)
        m = min(ew, eh)
        if m >= target:
            return Result(el, "control", "pass", ew, eh,
                          "::%s hit-expander %gx%g (MEASURED, var() resolved)" % (pseudo, ew, eh),
                          target)
        if m < FLOOR:
            return Result(el, "control", "fail", ew, eh,
                          "::%s hit-expander is only %gx%g — under the %d floor. An expander "
                          "that does not reach the floor is not a remediation."
                          % (pseudo, ew, eh, FLOOR), target)
        return Result(el, "control", "warn", ew, eh,
                      "::%s hit-expander %gx%g — under the %d default"
                      % (pseudo, ew, eh, target), target)

    # EITHER-dimension semantics (aid-009, 2026-07-03): a single resolved axis under
    # the floor is already a failure, whatever the other axis turns out to be. So a
    # half-measured box is only "unmeasured" when the half we CAN read is compliant.
    known = [v for v in (w, h) if v is not None]
    if known and min(known) < FLOOR:
        return Result(el, "control", "fail", w, h,
                      "%s is under the %d floor (2.5.8) — enlarge, add a ::before/::after "
                      "hit-expander, or claim an exception via %s"
                      % (_wh(w, h), FLOOR, EXCEPTION_ATTR), target)
    if w is None or h is None:
        if known and min(known) < target:
            return Result(el, "control", "warn", w, h,
                          "%s — the declared axis is under the %d default (aid-009); "
                          "the other axis is layout-determined" % (_wh(w, h), target), target)
        return Result(el, "control", "unmeasured", w, h,
                      ("one axis declared (%s), the other layout-determined" % _wh(w, h))
                      if known else
                      "no declared box (layout-determined) and no hit-expander — "
                      "this gate must not guess a size", target)
    m = min(w, h)
    if m < FLOOR:
        return Result(el, "control", "fail", w, h,
                      "%gx%g is under the %d floor (2.5.8) — enlarge, add a ::before/::after "
                      "hit-expander, or claim an exception via %s"
                      % (w, h, FLOOR, EXCEPTION_ATTR), target)
    if m < target:
        return Result(el, "control", "warn", w, h,
                      "%gx%g is under the %d default (aid-009)" % (w, h, target), target)
    return Result(el, "control", "pass", w, h, "%gx%g" % (w, h), target)


# ======================================================== data-mark geometry
def _svg_scale(el):
    node = el.parent
    while node is not None and node.tag != "svg":
        node = node.parent
    if node is None:
        return 1.0, 1.0, None
    vb = node.attrs.get("viewbox") or node.attrs.get("viewBox")
    w = to_px(node.attrs.get("width", "").replace("px", "") + "px") if node.attrs.get("width") else None
    h = to_px(node.attrs.get("height", "").replace("px", "") + "px") if node.attrs.get("height") else None
    if not vb:
        return 1.0, 1.0, node
    nums = [float(x) for x in re.findall(r"-?\d*\.?\d+", vb)]
    if len(nums) < 4 or nums[2] == 0 or nums[3] == 0:
        return 1.0, 1.0, node
    sx = (w / nums[2]) if w else 1.0
    sy = (h / nums[3]) if h else 1.0
    return sx, sy, node


def _num(el, name):
    try:
        return float(el.attrs[name])
    except (KeyError, ValueError, TypeError):
        return None


def mark_geometry(el):
    """(w, h, how) in CSS px, or (None, None, why) when the shape's geometry is
    not statically derivable."""
    sx, sy, _svg = _svg_scale(el)
    tag = el.tag

    if tag == "g":
        # the focusable wrapper: its target is the union of its shape children.
        best = None
        for c in el.children:
            w, h, how = mark_geometry(c)
            if w is None:
                continue
            if best is None or min(w, h) > min(best[0], best[1]):
                best = (w, h, "<g> wrapper measured from its %s child (%s)" % (c.tag, how))
        return best if best else (None, None, "<g> wrapper with no statically sized child")

    if tag == "rect":
        w, h = _num(el, "width"), _num(el, "height")
        if w is None or h is None:
            return None, None, "rect with no width/height attribute"
        return w * sx, h * sy, "rect w/h attrs"

    if tag == "circle":
        r = _num(el, "r")
        if r is None:
            return None, None, "circle with no r"
        return 2 * r * sx, 2 * r * sy, "circle diameter 2r"

    if tag == "ellipse":
        rx, ry = _num(el, "rx"), _num(el, "ry")
        if rx is None or ry is None:
            return None, None, "ellipse with no rx/ry"
        return 2 * rx * sx, 2 * ry * sy, "ellipse diameters"

    if tag == "path" and all(k in el.attrs for k in ("data-ro", "data-ri", "data-a1", "data-a2")):
        ro, ri = _num(el, "data-ro"), _num(el, "data-ri")
        a1, a2 = _num(el, "data-a1"), _num(el, "data-a2")
        if None in (ro, ri, a1, a2):
            return None, None, "arc segment with unreadable data-ro/ri/a1/a2"
        thickness = (ro - ri) * sx
        rm = (ro + ri) / 2.0
        arc = abs(math.radians(a2 - a1)) * rm * sx
        return max(thickness, arc), min(thickness, arc), \
            "arc segment: radial thickness %.1f, mid-radius arc length %.1f" % (thickness, arc)

    if tag in ("polygon", "polyline"):
        pts = [float(x) for x in re.findall(r"-?\d*\.?\d+", el.attrs.get("points", ""))]
        if len(pts) < 4:
            return None, None, "%s with unreadable points" % tag
        xs, ys = pts[0::2], pts[1::2]
        w = (max(xs) - min(xs)) * sx
        h = (max(ys) - min(ys)) * sy
        if tag == "polyline":
            # a trend line's operable target is its stroke band, not its bbox.
            return None, None, ("polyline (trend line): its target is stroke width x hit band, "
                                "which is a render-axis fact")
        return w, h, "polygon bbox"

    if tag == "path":
        return None, None, "path with a free-form `d` — bbox not statically derived"

    return None, None, "%s: no static geometry rule" % tag


def measure_mark(el):
    reason = (el.attrs.get(EXCEPTION_ATTR) or '').strip()
    if reason:
        return Result(el, "mark", "exception", None, None,
                      "claimed 2.5.8 exception: %s" % reason.strip(), TARGET_MARK)
    w, h, how = mark_geometry(el)
    if w is None:
        return Result(el, "mark", "unmeasured", None, None, how, TARGET_MARK)
    m = min(w, h)
    if m < TARGET_MARK:
        return Result(el, "mark", "under", w, h,
                      "%.1fx%.1f — under the %d dense-case minimum (%s)"
                      % (w, h, TARGET_MARK, how), TARGET_MARK)
    return Result(el, "mark", "pass", w, h, "%.1fx%.1f (%s)" % (w, h, how), TARGET_MARK)


# ================================================================== top level
def analyse(html):
    p = _DOM()
    p.feed(html)
    p.close()
    sheet = Sheet(p.styles)
    controls, marks = [], []
    for el in walk(p.root):
        if is_data_mark(el):
            if is_control(el) or "tabindex" in el.attrs:
                marks.append(measure_mark(el))
            continue
        if is_control(el):
            r = measure_control(sheet, el)
            if r.verdict == "unmeasured" and sheet.has_media_size_rule(el):
                r.detail += " (a @media-conditioned size exists and is NOT measured)"
            controls.append(r)
    return p.root, sheet, controls, marks
