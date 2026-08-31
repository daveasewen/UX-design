#!/usr/bin/env python3
"""
gen_component_partials.py — the RULE half of the component-type tier (ADR-0013 ruling 2).

Atom retrieval was VALUE-level only: organisms bound the same tokens as the atoms but
re-implemented the atoms' RULES locally (13/40 snippets carried a local button recipe;
4 pressed with translateY(1px) — drifted physics). This generator makes rules
RETRIEVABLE: an atom declares a named rule-block between PARTIAL markers; consumers
carry AUTO-PARTIAL markers; the generator injects the atom's block into every consumer
(selector-mapped, provenance-commented). Snippets stay self-contained and remain the
source of truth — the projector contract extended from values to rules. Runtime
class-sharing stays REJECTED inside the KB (source-of-truth inversion; that pattern
belongs at the ADR-0008 adapter boundary).

Registry: knowledge/component-types.json (ONE registry, both halves — ADR-0013 ruling 3).
  component-type/<group>/$partials/<name>:
    source        atom snippet (declares the PARTIAL block)
    rootSelector  the atom's control selector, rewritten per-member
    requires      .vars — CSS custom props every consumer must declare
                  .matchValues — vars whose declared value must EQUAL the source atom's
                  .declarations — substrings the consumer's CSS must contain
    $manifestBinds  var -> token path bindings every member's #token-manifest must carry
  component-type/<group>/$members/<Name>: {role:"source"} | {selector:".their-control"}
    $scan         MEMBERSHIP COMPLETENESS (#229) — {selectors:[…], $exempt:{Name: reason}}.
                  A partial group holds its MEMBERS identical and is blind to a snippet that
                  grows the same control and never joins; that blindness shipped four square
                  segmented controls for three sessions (#227 A1's hand sweep missed them).
                  With $scan, every snippet declaring a live CSS rule on one of the selectors
                  must be a member or carry a reasoned exemption — fail-loud both ways, and
                  both staleness directions (rotted exemption / stale member) too.

Markers (single-line comments, inside <style>):
  source atom:  /* ===== PARTIAL <name> START ... ===== */   CSS   /* ===== PARTIAL <name> END ===== */
  consumers:    /* ===== AUTO-PARTIAL <name> START ... ===== */  (generated)  /* ===== AUTO-PARTIAL <name> END ===== */

BEHAVIOUR partials (ADR-0015, 2026-07-23 — retrieval reaches JS): a group may carry
$behaviour/<name> whose source is a hand-authored file under knowledge/ (e.g.
canon/dv-behaviour.js — the type.css precedent). The generator injects it into every
member snippet as a whole <script> element between HTML-comment markers:
  <!-- ===== AUTO-BEHAVIOUR <name> START (group) ===== -->  (generated)  <!-- ===== AUTO-BEHAVIOUR <name> END ===== -->
Same contract machinery (requires.vars / declarations / $manifestBinds), same --check
sync gate, byte-exact. Snippets stay portable AFTER generation — the block travels.
The performance contract on the SOURCE (≤16KB, banned patterns) is _validate_behaviour.py's.

Consumes-manifest (ADR-0015 Amendment 2, ruled Dave 2026-07-28 — superseded #66-D6, 2026-08-01,
PERMANENT STRICT FORM): a member OBJECT MUST declare "consumes": [<behaviour name>, ...]. There
is no universal default any more — ABSENT = FAIL LOUD, a named error identifying the group and
member, never a silent "consumes everything" and never a warning. PRESENT = the member carries
ONLY the listed behaviours' AUTO-BEHAVIOUR blocks and is held only to their contracts. An empty
list ([]) is the LEGAL form for "consumes none" — there is no form that means "everything" any
more, so declare every behaviour you actually consume, or [] if you consume none. Fail-loud
throughout: an absent key REFUSES · unknown names REFUSE · a non-consuming member carrying the
behaviour's markers REFUSES (declared-away payload present is a defect, not a warning).

Usage:
  python3 knowledge/gen_component_partials.py             # inject/refresh all consumers
  python3 knowledge/gen_component_partials.py --check     # verify in sync + contracts (build gate)
  python3 knowledge/gen_component_partials.py --selftest  # bite-test (ADR-0005 §5)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
REG  = os.path.join(HERE, "component-types.json")
TOK  = os.path.join(HERE, "tokens")

# ------------------------------------------------------------------ registry
def load_registry():
    return json.load(open(REG))

def groups(reg):
    return {k: v for k, v in reg.get("component-type", {}).items() if not k.startswith("$")}

def snippet_path(name):
    return os.path.join(SNIP, name + ".reference.html")

# ------------------------------------------------------------------ extraction
def source_block(html, pname):
    """CSS between the atom's PARTIAL markers (exclusive). None if absent.

    ⛔ LOCATED in the comment-masked copy (#211 lane R7) — a PARTIAL block written inside an
    HTML comment is dead CSS and must never be read as an atom's source of truth — but the
    payload is SLICED FROM THE ORIGINAL BYTES at that span, so masking can never corrupt the
    CSS it helped us find. Same locate-live / slice-raw discipline as manifest_vars (lane R6).
    """
    m = re.search(r'/\* ===== PARTIAL ' + re.escape(pname) + r' START[^\n]*===== \*/\n(.*?)\n\s*/\* ===== PARTIAL '
                  + re.escape(pname) + r' END ===== \*/', live_text(html), re.S)
    return html[m.start(1):m.end(1)] if m else None

# Both marker comments captured whole; group(2) = whatever sits between them (may be
# empty — a freshly-migrated file carries ADJACENT markers for the generator to fill).
AUTO_RE = lambda pname: re.compile(
    r'(/\* ===== AUTO-PARTIAL ' + re.escape(pname) + r' START[^\n]*===== \*/)(.*?)(/\* ===== AUTO-PARTIAL '
    + re.escape(pname) + r' END ===== \*/)', re.S)

# Behaviour markers are HTML comments (the payload is a whole <script> element, not CSS).
BEHAVIOUR_RE = lambda bname: re.compile(
    r'(<!-- ===== AUTO-BEHAVIOUR ' + re.escape(bname) + r' START[^\n]*===== -->)(.*?)(<!-- ===== AUTO-BEHAVIOUR '
    + re.escape(bname) + r' END ===== -->)', re.S)

# ------------------------------------------------------------------ MARKUP partials (#68, dv-lockup)
# The third injection type, deliberately symmetric with CSS (AUTO-PARTIAL) and JS (AUTO-BEHAVIOUR)
# above: a source atom declares a literal HTML fragment between MARKUP <name> START/END comment
# markers; consumers carry AUTO-MARKUP <name> START/END markers, one pair PER <figure> occurrence
# (markup is per-chart-block, not per-file — dataviz files hold multiple chart-blocks, e.g.
# Chart-bar's 5). A member's participation is a "markup" list declaration on its $members entry,
# A2 permanent-strict (absent key = named loud fail, same posture as "consumes" above). Each
# figure supplies its own instance data via data-lockup-* attributes on the <figure> tag itself
# (data-lockup-title, data-lockup-table) — the per-occurrence analogue of a CSS partial's
# per-member rootSelector rewrite.
FIGURE_RE = re.compile(r'<figure\b.*?</figure>', re.S)

def figure_attrs(fig_html):
    """data-lockup-* attributes declared on a <figure>'s opening tag."""
    m = re.match(r'<figure\b([^>]*)>', fig_html)
    attrs = {}
    if m:
        for am in re.finditer(r'(data-lockup-[a-z]+)="([^"]*)"', m.group(1)):
            attrs[am.group(1)] = am.group(2)
    return attrs

def markup_source_block(html, pname):
    """The literal HTML fragment between the source atom's MARKUP markers. None if absent."""
    m = re.search(r'<!-- ===== MARKUP ' + re.escape(pname) + r' START[^\n]*===== -->\n(.*?)\n\s*<!-- ===== MARKUP '
                  + re.escape(pname) + r' END ===== -->', html, re.S)
    return m.group(1) if m else None

AUTO_MARKUP_RE = lambda pname: re.compile(
    r'(<!-- ===== AUTO-MARKUP ' + re.escape(pname) + r' START[^\n]*===== -->)(.*?)(<!-- ===== AUTO-MARKUP '
    + re.escape(pname) + r' END ===== -->)', re.S)

def render_markup(src_inner, render_mode, value):
    """Per-occurrence value substitution: 'text' rewrites the outer tag's inner text (title);
    'attr:NAME' rewrites one attribute's value (the table toggle's aria-controls target)."""
    esc = value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    if render_mode == "text":
        m = re.match(r'^(\s*<[^>]+>)(.*?)(\s*</[a-zA-Z0-9]+>\s*)$', src_inner, re.S)
        return (m.group(1) + esc + m.group(3)) if m else None
    if render_mode.startswith("attr:"):
        attr = render_mode.split(":", 1)[1]
        new, n = re.subn(re.escape(attr) + r'="[^"]*"', attr + '="' + value + '"', src_inner, count=1)
        return new if n else None
    return None

def markup_provenance(pname, group, source):
    return (f"<!-- INJECTED from {source}.reference.html (markup \"{pname}\", group {group} —\n"
            f"     registry knowledge/component-types.json, dv-lockup extension #68). DO NOT hand-edit\n"
            f"     between the AUTO-MARKUP markers: edit the source MARKUP block in the atom and\n"
            f"     regenerate: python3 knowledge/gen_component_partials.py -->")

def behaviour_inner(js, bname, group, source):
    """The generated payload between AUTO-BEHAVIOUR markers: provenance + the script."""
    prov = (f"/* INJECTED from knowledge/{source} (behaviour \"{bname}\", group {group} —\n"
            f"   registry knowledge/component-types.json, ADR-0015). DO NOT hand-edit between the\n"
            f"   AUTO-BEHAVIOUR markers: edit the source and regenerate:\n"
            f"   python3 knowledge/gen_component_partials.py */")
    return "<script>\n" + prov + "\n" + js.rstrip("\n") + "\n</script>"

def consumes_behaviour(mconf, bname, bnames, gname, mname):
    """ADR-0015 Amendment 2, PERMANENT STRICT FORM (#66-D6, Dave 2026-08-01 — supersedes the
    2026-07-28 TENTATIVE universal default, now CLOSED). Returns (consuming, fails). EVERY
    member must declare "consumes" — an absent key is FAIL LOUD, never a silent "consumes
    everything" default. Unknown names and empty lists REFUSE too (fail loud on unknown —
    never enumerate-and-skip)."""
    cons = mconf.get("consumes")
    if cons is None:
        return False, [f'{gname}/{mname}: "consumes" is required (PERMANENT STRICT, #66-D6) — '
                       f'no absent-key default any more. Declare the behaviour(s) this member '
                       f'actually consumes, e.g. "consumes": {sorted(bnames)!r}, or [] if none.']
    if not isinstance(cons, list):
        return False, [f'{gname}/{mname}: "consumes" must be a list of behaviour names (or [] '
                       f'to consume none)']
    if not cons:
        return False, []
    unknown = sorted(set(cons) - set(bnames))
    if unknown:
        return False, [f'{gname}/{mname}: consumes unknown behaviour(s) {unknown} — '
                       f'group has {sorted(bnames)}']
    return bname in cons, []

def non_consumer_marker_fails(html, bname, gname, mname):
    """A member that declared this behaviour away must NOT carry its markers (inert payload
    is exactly what the manifest exists to retire)."""
    if BEHAVIOUR_RE(bname).search(html):
        return [f'{gname}/{bname}: {mname} does not consume this behaviour but carries its '
                f'AUTO-BEHAVIOUR markers — remove the pair, or add "{bname}" to its consumes list']
    return []

def rewrite_selectors(css, root_sel, member_sel):
    """Map the atom's root selector onto the member's. Word-boundary safe:
    '.btn' matches '.btn:hover' / '.btn.full' but never '.btn-x' or '--btn-grow'."""
    if member_sel == root_sel:
        return css
    return re.sub(re.escape(root_sel) + r'(?![\w-])', member_sel, css)

def provenance(pname, group, source):
    return (f"/* INJECTED from {source}.reference.html (partial \"{pname}\", group {group} —\n"
            f"   registry knowledge/component-types.json, ADR-0013). DO NOT hand-edit between the\n"
            f"   AUTO-PARTIAL markers: edit the source PARTIAL block in the atom and regenerate:\n"
            f"   python3 knowledge/gen_component_partials.py */")

def generated_inner(src_css, pname, group, source, root_sel, member_sel):
    return provenance(pname, group, source) + "\n" + rewrite_selectors(src_css, root_sel, member_sel)

# ------------------------------------------------------------------ comment mask (#211 lane R6)
# The CONTRACT readers below used to read RAW html, so a declaration, a required declaration
# substring or a whole #token-manifest sitting inside an HTML comment SATISFIED the contract.
# That is the same class lane R1 fixed in gen_token_ramp (#211): raw-text reading satisfied by
# content inside HTML comments, which there silently killed 120 declarations, and which ds-018's
# C2 gate was green over for its whole life.
#
# ⛔ THE MASK IS APPLIED TO THE CONTRACT READERS — declared_value, check_contracts'
# `declarations` substring test, and manifest_vars — AND, since #211 lane R7, to the three
# SPAN SELECTORS that pick an injection source or target out of the document (source_block,
# AUTO_RE via live_match, FIGURE_RE via live_figure_spans; see § live spans below). It is
# deliberately NOT applied to BEHAVIOUR_RE, AUTO_MARKUP_RE, markup_source_block or
# non_consumer_marker_fails, whose markers ARE HTML comments by design: masking there would
# blind the generator to its own injection sites. Selftest arms 5f and 5g drive that fence in
# both directions.
# ★ #218 (W-92 residual, "prefer the helper"): this function was a BYTE-IDENTICAL COPY of
# `gen_token_ramp.mask_comments`, and its docstring gave the reason — "duplicated rather than
# imported: importing a sibling generator runs its help gate". ⚠ THE PREMISE WAS FALSE:
# `help_gate` is a no-op on import. The true objection (a generator must not import a sibling
# generator) is answered by a side-effect-free module instead of a second copy — two copies with
# no comparing gate is a fix that lands on one side and is green on both.
from _htmlmask import COMMENT_OPEN, COMMENT_CLOSE, mask_comments  # noqa: E402,F401
from _htmlmask import selftest_mask as _htmlmask_selftest  # noqa: E402

_MASK_CACHE = {}

def live_text(html):
    """The document's LIVE bytes, comments blanked. Memoised — the contract readers ask the
    same handful of documents hundreds of times in one run."""
    got = _MASK_CACHE.get(html)
    if got is None:
        got = _MASK_CACHE[html] = mask_comments(html)
    return got

# ------------------------------------------------------------------ live spans (#211 lane R7)
# THE INJECTION-SITE half of R6's fix. R6 masked the three CONTRACT readers; the readers that
# SELECT A SOURCE OR TARGET SPAN out of raw text were left raw, and one of them was LATENT-live:
# Image-block.reference.html says "real <figure>/<figcaption> semantics" inside its prose header
# comment, and FIGURE_RE (non-greedy, DOTALL) therefore matched from THAT `<figure` to the first
# REAL `</figure>` — one span swallowing the whole comment AND the file's first real figure.
#
# ⛔ THE DISCIPLINE IS LOCATE-LIVE / SLICE-RAW, exactly as manifest_vars does it: the span is
# found in the comment-masked copy (so commented-out markup can never be selected), and the
# bytes handed on are the ORIGINAL ones at that span (so the AUTO-MARKUP / AUTO-BEHAVIOUR
# markers INSIDE a live figure — which ARE HTML comments by design — survive intact). Masking
# the CONTENTS instead of just the SELECTION would delete 80 AUTO-MARKUP injection sites.
# mask_comments' length-preservation is what makes a masked span address the same raw bytes.
#
# ⛔ THE R6 FENCE STILL BINDS AND IS NOT WIDENED HERE: BEHAVIOUR_RE, AUTO_MARKUP_RE,
# markup_source_block and non_consumer_marker_fails read markers that ARE HTML comments and
# keep reading RAW text. Selftest arms 5f (vi) and 5g drive that fence in both directions.
def live_match(rx, html):
    """`rx` matched against the document's LIVE bytes. Group SPANS transfer index-for-index to
    the original — the caller slices `html`, never the mask."""
    return rx.search(live_text(html))

def live_figure_spans(html):
    """(start, end) of every LIVE <figure>…</figure>, in document order. A <figure> named inside
    an HTML comment is prose, not markup, and is never an injection site."""
    return [m.span() for m in FIGURE_RE.finditer(live_text(html))]

def rewrite_live_figures(html, fn):
    """Rebuild `html` with `fn` applied to each LIVE figure, splicing the original bytes either
    side. ⛔ `fn` receives the figure's ORIGINAL bytes, never the mask — the AUTO-MARKUP markers
    inside a figure ARE HTML comments and would arrive blanked, so nothing would ever be injected.

    This is a NAMED function and not an inline loop in run() precisely so the selftest can drive
    the code the generator actually runs [[mutation-tests-the-clause-not-the-feature]]: an arm that
    only checked live_figure_spans left the splice itself untested, and a mutant that sliced from
    the mask survived it.
    """
    pieces, cursor = [], 0
    for a, b in live_figure_spans(html):
        pieces.append(html[cursor:a])
        pieces.append(fn(html[a:b]))
        cursor = b
    pieces.append(html[cursor:])
    return "".join(pieces)

# ------------------------------------------------------------------ contracts
def declared_value(html, var):
    """First declared value of --var anywhere in the document's LIVE CSS.

    ⛔ Asked of a COMMENT-MASKED copy (#211 lane R6): a `--var: value;` written inside an
    HTML comment is not a declaration, and must not satisfy `requires.vars` or supply a
    `matchValues` comparand.
    """
    m = re.search(re.escape(var) + r'\s*:\s*([^;]+);', live_text(html))
    return m.group(1).strip() if m else None

MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)

def manifest_vars(html):
    """The document's LIVE #token-manifest. ⛔ LOCATED in the comment-masked copy — a manifest
    inside an HTML comment is not the document's manifest — but PARSED from the ORIGINAL bytes
    at that span, so the mask can never corrupt the JSON it helped us find. This is the only
    consumer of mask_comments' length-preservation property, and the reason it is a property
    and not a convenience."""
    m = MANIFEST_RE.search(live_text(html))
    return json.loads(html[m.start(1):m.end(1)]).get("vars", {}) if m else {}

def check_contracts(name, html, partial, src_html, extra=None):
    """requires.vars / matchValues / declarations / $manifestBinds -> list of failures.
    extra: per-member capability contract — the ADR-0013 per-capability split (a member's
    $members[…].extraContract with keys vars / declarations / manifestBinds), MERGED with the
    universal partial contract. So a behaviour contract holds only the truly-universal hook
    (dataviz: popover data-tip=) while each member declares the capability chrome it actually
    carries — cartesian axis/grid roles are line/bar/combo, axis-only is donut, sparkline is
    axis-free (dataviz per-capability split, 2026-07-24)."""
    fails = []
    extra = extra or {}
    req = partial.get("requires", {})
    for var in list(req.get("vars", [])) + list(extra.get("vars", [])):
        if declared_value(html, var) is None:
            fails.append(f"{name}: required var {var} not declared")
    for var in req.get("matchValues", []):
        want = declared_value(src_html, var)
        have = declared_value(html, var)
        if want is not None and have is not None and have != want:
            fails.append(f"{name}: {var} = '{have}' != source atom's '{want}' (matchValues)")
    # ⛔ comment-masked (#211 lane R6): a required declaration that appears ONLY inside an HTML
    # comment is not carried by the consumer — same class as declared_value above.
    live = live_text(html)
    for needle in list(req.get("declarations", [])) + list(extra.get("declarations", [])):
        if needle not in live:
            fails.append(f"{name}: required declaration '{needle}' missing")
    mv = manifest_vars(html)
    binds = {**(partial.get("$manifestBinds") or {}), **(extra.get("manifestBinds") or {})}
    for var, path in binds.items():
        if mv.get(var) != path:
            fails.append(f"{name}: #token-manifest must bind {var} -> {path} (has: {mv.get(var)})")
    return fails

# ------------------------------------------------------------------ registry cache gate
def _resolve_semantic(path):
    """Resolve a $alias target's $value from its store (modeless or light)."""
    if path.startswith("motion/"):
        store = json.load(open(os.path.join(TOK, "motion.json")))
    elif path.startswith("color/"):
        store = json.load(open(os.path.join(TOK, "colour.json")))
    elif path.startswith(("border-radius/", "border-width/", "focus-ring/", "layout/", "breakpoint/", "target/")):
        store = json.load(open(os.path.join(TOK, "layout.json")))
    else:
        store = json.load(open(os.path.join(TOK, "semantic-colour.json")))
    node = store
    for k in path.split("/"):
        node = node[k]
    if "$value" in node:
        return node["$value"]
    if "light" in node and isinstance(node["light"], dict):
        return node["light"].get("$value")
    return None

def check_caches(reg):
    """Every component-type parameter's $value must equal its $alias target
    (the _STANDARDS.md §1 alias-source / cached-value contract)."""
    fails = []
    for gname, g in groups(reg).items():
        for pname, node in g.items():
            if pname.startswith("$") or not isinstance(node, dict):
                continue
            if "$alias" in node and "$value" in node:
                try:
                    want = _resolve_semantic(node["$alias"])
                except KeyError:
                    fails.append(f"component-type/{gname}/{pname}: $alias {node['$alias']} unresolvable")
                    continue
                if want != node["$value"]:
                    fails.append(f"component-type/{gname}/{pname}: cached $value {node['$value']} "
                                 f"!= alias target {node['$alias']} = {want}")
    return fails

# ------------------------------------------------------------------ membership scan (#229)
# THE SECOND HALF OF A PARTIAL GROUP, and the half the first three recurrences needed.
#
# A $partials group holds its MEMBERS byte-identical — and is completely blind to a snippet that
# grows the same control and never joins. That blindness is not hypothetical: #227's A1 sweep
# repaired the segmented radii in eight snippets BY HAND and missed four, which then rendered a
# square track, thumb AND hover in every rounded theme until Dave saw it at #229. A hand sweep is
# an instrument nobody is obliged to run twice; this one runs on every build.
#
# A group opts in with a "$scan": {selectors: [...], $exempt: {snippet: reason}} block. Every
# snippet declaring a LIVE CSS RULE on one of those selectors must be a registered member or carry
# a reasoned exemption. Fail-loud in both directions, and in BOTH staleness directions too: an
# exemption whose file no longer declares the selector refuses (a rotted exemption hides the next
# real one), and a member that declares no such rule refuses (a stale registry entry).
#
# ⛔ WHAT IT CANNOT SEE, stated so nobody mistakes green for correct: it is a TEXT scan of the
# snippet's CSS. It proves MEMBERSHIP, never geometry — it cannot tell you a thumb's inset is
# wrong, that two boxes are not actually coincident, or that a token's value is bad. Only a render
# and an eye do that.
STYLE_RE       = re.compile(r'<style[^>]*>(.*?)</style>', re.S)
CSS_COMMENT_RE = re.compile(r'/\*.*?\*/', re.S)
RULE_SEL_RE    = re.compile(r'([^{}]+)\{')

def declares_selector(html, selectors):
    """Which of `selectors` this document declares a LIVE CSS RULE on.

    ⛔ Read from the COMMENT-MASKED copy (#211 lane R6 discipline): a `<style>` block sitting
    inside an HTML comment is dead CSS and must not enrol a file in a group. CSS comments are
    stripped separately — the ds-008 lesson: prose naming a selector is not a rule (Data-grid's
    header says `.seg` is a blast radius it must not join, and it must not be enrolled for saying
    so). Only SELECTOR position counts, so `.seg` inside a JS string or in markup is invisible;
    word-boundary matching keeps `.dgseg` and `.seg-x` out.
    """
    found = set()
    for m in STYLE_RE.finditer(live_text(html)):
        css = CSS_COMMENT_RE.sub("", m.group(1))
        for sel in RULE_SEL_RE.findall(css):
            for s in selectors:
                if s not in found and re.search(re.escape(s) + r'(?![\w-])', sel):
                    found.add(s)
    return found

def scan_hits(selectors):
    """{snippet name: [selectors it declares]} across every snippet in the tree."""
    hits = {}
    for path in sorted(glob.glob(os.path.join(SNIP, "*.reference.html"))):
        got = declares_selector(open(path).read(), selectors)
        if got:
            hits[os.path.basename(path)[:-len(".reference.html")]] = sorted(got)
    return hits

def check_scan(gname, g, hits=None):
    """Membership completeness for one group. `hits` injectable so the selftest can drive the
    logic on a fixture without the live tree."""
    scan = g.get("$scan")
    if not scan:
        return []
    sels = scan.get("selectors") or []
    if not sels:
        return [f"{gname}/$scan: no selectors declared — a scan with nothing to look for cannot "
                f"fail, and an instrument that cannot fail is not one"]
    exempt = scan.get("$exempt") or {}
    if not isinstance(exempt, dict):
        return [f'{gname}/$scan: "$exempt" must be an object {{snippet: reason}}']
    members = set(g.get("$members") or {})
    fails = []
    both = sorted(members & set(exempt))
    if both:
        fails.append(f"{gname}/$scan: {both} are BOTH registered members and exempt — the two "
                     f"declarations contradict")
    for n, why in sorted(exempt.items()):
        if not (isinstance(why, str) and why.strip()):
            fails.append(f'{gname}/$scan: $exempt["{n}"] has no reason — an exemption without a '
                         f"stated reason is indistinguishable from the drift this scan exists to catch")
    if hits is None:
        hits = scan_hits(sels)
    for name, got in sorted(hits.items()):
        if name in members or name in exempt:
            continue
        fails.append(f"{gname}/$scan: {name} declares {got} but is NOT a member of the `{gname}` "
                     f"group and carries no $exempt entry. A control outside its group drifts "
                     f"silently — this is the #227 missed-sweep class, measured. Register it "
                     f"(AUTO-PARTIAL markers + requires.vars + manifest binds), or add a $exempt "
                     f"entry saying why it is not one of these.")
    for name in sorted(members):
        if name not in hits:
            fails.append(f"{gname}/$scan: member {name} declares none of {sels} — a member that "
                         f"carries no such rule is a stale registry entry")
    for name in sorted(exempt):
        if name not in hits:
            fails.append(f"{gname}/$scan: $exempt names {name}, which declares none of {sels} any "
                         f"more — a rotted exemption hides the next real one; remove it")
    return fails

# ------------------------------------------------------------------ main pass
def run(write):
    reg = load_registry()
    fails, out_of_sync, injected = [], [], 0
    fails += check_caches(reg)
    for gname, g in groups(reg).items():
        members = g.get("$members", {})
        fails += check_scan(gname, g)          # #229 — membership completeness, before injection
        for pname, partial in (g.get("$partials") or {}).items():
            source = partial["source"]
            root_sel = partial["rootSelector"]
            sp = snippet_path(source)
            if not os.path.exists(sp):
                fails.append(f"{gname}/{pname}: source snippet {source} missing"); continue
            src_html = open(sp).read()
            src_css = source_block(src_html, pname)
            if src_css is None:
                fails.append(f"{gname}/{pname}: source {source} has no PARTIAL block"); continue
            # the source atom must satisfy its own contracts too
            fails += check_contracts(source, src_html, partial, src_html)
            for mname, mconf in members.items():
                if mconf.get("role") == "source":
                    continue
                mp = snippet_path(mname)
                if not os.path.exists(mp):
                    fails.append(f"{gname}/{pname}: member snippet {mname} missing"); continue
                html = open(mp).read()
                fails += check_contracts(mname, html, partial, src_html, mconf.get("extraContract"))
                member_sel = mconf.get("selector", root_sel)
                inner = generated_inner(src_css, pname, gname, source, root_sel, member_sel)
                between = "\n" + inner + "\n  "     # canonical padding either side of the payload
                rx = AUTO_RE(pname)
                # ⛔ LOCATED LIVE (#211 lane R7): a marker pair sitting inside an HTML comment is
                # not an injection site — injecting there writes a payload the browser never sees.
                # Spans transfer index-for-index, so the payload is compared and REPLACED in the
                # ORIGINAL bytes.
                m = live_match(rx, html)
                if not m:
                    fails.append(f"{gname}/{pname}: {mname} is a member but carries no AUTO-PARTIAL "
                                 f"markers (membership is deliberate — add the marker pair to migrate)")
                    continue
                if html[m.start(2):m.end(2)] != between:
                    out_of_sync.append(f"{mname} ({pname})")
                    if write:
                        html = html[:m.start(2)] + between + html[m.end(2):]
                        open(mp, "w").write(html)
                        injected += 1
        # ---- behaviour partials (ADR-0015): source = a hand-authored JS file under knowledge/
        bnames = list((g.get("$behaviour") or {}).keys())
        for bname, beh in (g.get("$behaviour") or {}).items():
            src_path = os.path.join(HERE, beh["source"])
            if not os.path.exists(src_path):
                fails.append(f"{gname}/{bname}: behaviour source knowledge/{beh['source']} missing"); continue
            js = open(src_path).read()
            for mname, mconf in members.items():
                mp = snippet_path(mname)
                if not os.path.exists(mp):
                    fails.append(f"{gname}/{bname}: member snippet {mname} missing"); continue
                html = open(mp).read()
                # ADR-0015 Amendment 2: the consumes-manifest gates BOTH injection and contract
                consuming, cfails = consumes_behaviour(mconf, bname, bnames, gname, mname)
                if cfails:
                    fails += [f for f in cfails if f not in fails]; continue
                if not consuming:
                    fails += non_consumer_marker_fails(html, bname, gname, mname); continue
                fails += check_contracts(mname, html, beh, js, mconf.get("extraContract"))
                inner = behaviour_inner(js, bname, gname, beh["source"])
                between = "\n" + inner + "\n  "     # same canonical padding as CSS partials
                rx = BEHAVIOUR_RE(bname)
                m = rx.search(html)
                if not m:
                    fails.append(f"{gname}/{bname}: {mname} is a member but carries no AUTO-BEHAVIOUR "
                                 f"markers (membership is deliberate — add the marker pair to migrate)")
                    continue
                if m.group(2) != between:
                    out_of_sync.append(f"{mname} ({bname})")
                    if write:
                        html = rx.sub(lambda mm: mm.group(1) + between + mm.group(3), html, count=1)
                        open(mp, "w").write(html)
                        injected += 1
        # ---- markup partials (#68, dv-lockup): whole-HTML fragments injected per chart-block,
        # between HTML-comment AUTO-MARKUP markers, one pair per <figure>. See the block comment
        # above FIGURE_RE for the mechanism note.
        mk = g.get("$markup") or {}
        if mk:
            mandatory_names = [n for n, spec in mk.items() if spec.get("mandatory")]
            for mname, mconf in members.items():
                mp = snippet_path(mname)
                if not os.path.exists(mp):
                    fails.append(f"{gname}/markup: member snippet {mname} missing"); continue
                html = open(mp).read()
                markup_list = mconf.get("markup")
                if markup_list == "source":
                    continue    # the source atom is read from, never injected into
                if markup_list is None:
                    fails.append(f'{gname}/markup: {mname}: "markup" is required (A2 permanent-strict) — '
                                 f'declare the dv-lockup partial(s) this member carries, e.g. '
                                 f'{mandatory_names!r}, or [] if none')
                    continue
                if not isinstance(markup_list, list):
                    fails.append(f'{gname}/markup: {mname}: "markup" must be a list of markup partial names'); continue
                unknown = sorted(set(markup_list) - set(mk.keys()))
                if unknown:
                    fails.append(f"{gname}/markup: {mname}: unknown markup name(s) {unknown} — group has {sorted(mk)}")
                    continue
                # RULED EXEMPTION from a mandatory markup partial (s182-D2, #182 — the sparkline
                # atom sheds its title slot). Absence of a mandatory partial stays a LOUD FAIL by
                # default; the ONLY legal way out is an explicit "markupExempt": {name: reason}
                # naming the ruling. An empty/blank reason REFUSES — an exemption without a stated
                # ruling is indistinguishable from the drift this gate exists to catch. An exempt
                # name may NOT also sit in the markup list (the two declarations contradict).
                exempt = mconf.get("markupExempt") or {}
                if not isinstance(exempt, dict):
                    fails.append(f'{gname}/markup: {mname}: "markupExempt" must be an object {{name: reason}}'); continue
                bad_exempt = sorted(set(exempt) - set(mk.keys()))
                if bad_exempt:
                    fails.append(f"{gname}/markup: {mname}: markupExempt names unknown markup partial(s) {bad_exempt}")
                    continue
                for n, why in sorted(exempt.items()):
                    if not (isinstance(why, str) and why.strip()):
                        fails.append(f'{gname}/markup: {mname}: markupExempt["{n}"] has no reason — '
                                     f"an exemption must name the ruling that granted it")
                    if n in markup_list:
                        fails.append(f'{gname}/markup: {mname}: "{n}" is both declared in markup and '
                                     f"exempted — the two declarations contradict")
                missing_mandatory = [n for n in mandatory_names if n not in markup_list and n not in exempt]
                if missing_mandatory:
                    fails.append(f"{gname}/markup: {mname}: missing mandatory markup partial(s) {missing_mandatory}"
                                 f" — carry them, or declare a reasoned \"markupExempt\" entry naming the ruling")
                for pname in mk:
                    if pname not in markup_list and AUTO_MARKUP_RE(pname).search(html):
                        fails.append(f"{gname}/markup: {mname} does not declare {pname} but carries its "
                                     f"AUTO-MARKUP markers — remove the pair, or add \"{pname}\" to its markup list")
                seen = {n: 0 for n in markup_list}
                local_fails = []
                inj_count = [0]
                def process_fig(fig_html):
                    # fig_html is the ORIGINAL bytes of one LIVE figure (span located in the
                    # comment-masked copy, #211 lane R7). Everything below reads RAW inside it —
                    # the AUTO-MARKUP markers ARE HTML comments and must stay visible (R6 fence).
                    attrs = figure_attrs(fig_html)
                    for pname in markup_list:
                        spec = mk[pname]
                        rx = AUTO_MARKUP_RE(pname)
                        mm = rx.search(fig_html)
                        if not mm:
                            continue
                        seen[pname] += 1
                        source = spec["source"]
                        sp = snippet_path(source)
                        if not os.path.exists(sp):
                            local_fails.append(f"{gname}/markup/{pname}: source {source} missing"); continue
                        src_inner = markup_source_block(open(sp).read(), pname)
                        if src_inner is None:
                            local_fails.append(f"{gname}/markup/{pname}: source {source} has no MARKUP block"); continue
                        value = attrs.get(spec["dataAttr"])
                        if value is None:
                            local_fails.append(f"{gname}/markup/{pname}: {mname}: figure missing {spec['dataAttr']} "
                                               f"(required to render {pname})")
                            continue
                        rendered = render_markup(src_inner, spec["render"], value)
                        if rendered is None:
                            local_fails.append(f"{gname}/markup/{pname}: {mname}: template mismatch rendering markup")
                            continue
                        between = "\n      " + markup_provenance(pname, gname, source) + "\n" + rendered + "\n      "
                        if mm.group(2) != between:
                            out_of_sync.append(f"{mname} ({pname})")
                            inj_count[0] += 1
                            fig_html = rx.sub(lambda z: z.group(1) + between + z.group(3), fig_html, count=1)
                    return fig_html
                # ⛔ NOT FIGURE_RE.sub(…, html) any more (#211 lane R7): that walked RAW text, so a
                # <figure> named inside a prose comment was selected as an injection site — and
                # because FIGURE_RE is non-greedy over DOTALL, that span ran from the COMMENT to
                # the first REAL </figure>, swallowing a live figure whole. Rebuild from the live
                # spans instead, splicing the original bytes either side.
                new_html = rewrite_live_figures(html, process_fig)
                fails += local_fails
                for pname in markup_list:
                    if seen[pname] == 0:
                        fails.append(f"{gname}/markup/{pname}: {mname} declares this markup but no figure carries "
                                     f"its AUTO-MARKUP markers (membership is deliberate — add the marker pair to migrate)")
                if write and new_html != html:
                    open(mp, "w").write(new_html)
                injected += inj_count[0]
    return fails, out_of_sync, injected

# ------------------------------------------------------------------ selftest
def selftest():
    fails = []
    # 0. ★ #218 (W-92): ONE mask implementation. This file carried a byte-identical COPY of
    # `gen_token_ramp.mask_comments` with no gate comparing them; re-defining it locally makes
    # `__module__` this file and turns this arm RED. The mask's own property bites now live in
    # `_htmlmask.selftest_mask` so BOTH consumers inherit the same ones.
    if mask_comments.__module__ != "_htmlmask":
        fails.append(f"mask_comments came from `{mask_comments.__module__}`, not `_htmlmask` — "
                     f"a second copy of the comment mask is back (W-92). Import it, never "
                     f"re-implement it.")
    fails += [f"shared mask: {x}" for x in _htmlmask_selftest()]
    # 1. selector rewrite is word-boundary safe
    css = ".btn:hover{x} .btn.full:hover{y} .btn-x{z} /* --btn-grow */"
    got = rewrite_selectors(css, ".btn", ".iconbtn")
    if ".iconbtn:hover" not in got or ".iconbtn.full:hover" not in got:
        fails.append("selector rewrite missed a mapped selector")
    if ".btn-x" not in got or "--btn-grow" not in got.replace(".iconbtn", ""):
        fails.append("selector rewrite over-matched (.btn-x / --btn-grow must survive)")
    # 2. compound member selector
    if ".nav button:active" not in rewrite_selectors(".btn:active{a}", ".btn", ".nav button"):
        fails.append("compound member selector not substituted")
    # 3. source-block extraction + tamper detection via string compare
    doc = ("/* ===== PARTIAL p START (t) ===== */\n.btn:hover{transform:scale(1);}\n"
           "/* ===== PARTIAL p END ===== */")
    src = source_block(doc, "p")
    if src != ".btn:hover{transform:scale(1);}":
        fails.append("source_block extraction wrong: %r" % src)
    inner = generated_inner(src, "p", "g", "Button", ".btn", ".x")
    if inner == generated_inner(src + "/*tamper*/", "p", "g", "Button", ".btn", ".x"):
        fails.append("tampered source produced identical injection (no teeth)")
    # 4. contract checks bite
    html_missing = "<style>.x{color:red}</style>"
    p = {"requires": {"vars": ["--press-travel"], "matchValues": [], "declarations": ["transform var(--spring)"]},
         "$manifestBinds": {"--press-travel": "component-type/button-family/press-travel"}}
    got = check_contracts("T", html_missing, p, html_missing)
    if not any("required var --press-travel" in f for f in got):
        fails.append("missing required var not caught")
    if not any("required declaration" in f for f in got):
        fails.append("missing declaration not caught")
    if not any("#token-manifest must bind" in f for f in got):
        fails.append("missing manifest binding not caught")
    # 4b. per-member extraContract (ADR-0013 per-capability split) — teeth + no false positive
    uni = {"requires": {"vars": [], "matchValues": [], "declarations": ['data-tip="']}}
    have_tip = '<i data-tip="x"></i>'
    if check_contracts("T", have_tip, uni, have_tip):
        fails.append("universal-only contract wrongly failing when the universal hook is present")
    got = check_contracts("T", have_tip, uni, have_tip, {"declarations": ['class="dv-tablepanel']})
    if not any("required declaration 'class=\"dv-tablepanel' missing" in f for f in got):
        fails.append("per-member extraContract declaration not enforced (capability hook not caught)")
    if not any("required var --data-grid" in f
               for f in check_contracts("T", have_tip, uni, have_tip, {"vars": ["--data-grid"]})):
        fails.append("per-member extraContract var not enforced (capability chrome not caught)")
    # 5. matchValues bites on drift
    src_html = ":root{--spring:300ms cubic-bezier(.5,1.6,.4,1);}"
    bad_html = ":root{--spring:200ms linear;}"
    p2 = {"requires": {"vars": [], "matchValues": ["--spring"], "declarations": []}}
    if not any("matchValues" in f for f in check_contracts("T", bad_html, p2, src_html)):
        fails.append("matchValues drift not caught")
    # 5b. AUTO_RE sees an EMPTY (adjacent-line) marker pair — the fresh-migration shape
    empty = "  /* ===== AUTO-PARTIAL p START (g) ===== */\n  /* ===== AUTO-PARTIAL p END ===== */"
    if not AUTO_RE("p").search(empty):
        fails.append("empty AUTO-PARTIAL marker pair not matched (fresh migrations would fail)")
    filled = AUTO_RE("p").sub(lambda m: m.group(1) + "\nX\n  " + m.group(3), empty, count=1)
    if AUTO_RE("p").search(filled).group(2) != "\nX\n  ":
        fails.append("AUTO-PARTIAL injection not idempotent on re-read")
    # 5c. AUTO-BEHAVIOUR markers: empty pair matched, injection idempotent, tamper has teeth
    bempty = '  <!-- ===== AUTO-BEHAVIOUR b START (g) ===== -->\n  <!-- ===== AUTO-BEHAVIOUR b END ===== -->'
    if not BEHAVIOUR_RE("b").search(bempty):
        fails.append("empty AUTO-BEHAVIOUR marker pair not matched (fresh migrations would fail)")
    binner = behaviour_inner("var x=1;", "b", "g", "canon/x.js")
    bfilled = BEHAVIOUR_RE("b").sub(lambda m: m.group(1) + "\n" + binner + "\n  " + m.group(3), bempty, count=1)
    if BEHAVIOUR_RE("b").search(bfilled).group(2) != "\n" + binner + "\n  ":
        fails.append("AUTO-BEHAVIOUR injection not idempotent on re-read")
    if binner == behaviour_inner("var x=2;", "b", "g", "canon/x.js"):
        fails.append("tampered behaviour source produced identical injection (no teeth)")
    if "<script>" not in binner or "</script>" not in binner or "ADR-0015" not in binner:
        fails.append("behaviour payload malformed (script element + provenance expected)")
    # 5d. ADR-0015 Amendment 2, PERMANENT STRICT FORM (#66-D6) — consumes-manifest has teeth
    if not consumes_behaviour({}, "b", ["b", "c"], "g", "M")[1]:
        fails.append("absent consumes key not refused (PERMANENT STRICT: every member must declare)")
    ok, f = consumes_behaviour({"consumes": ["b"]}, "b", ["b", "c"], "g", "M")
    if not ok or f:
        fails.append("declared consumer not recognised as consuming")
    ok, f = consumes_behaviour({"consumes": ["c"]}, "b", ["b", "c"], "g", "M")
    if ok or f:
        fails.append("narrow manifest failed to opt the member out")
    ok, f = consumes_behaviour({"consumes": []}, "b", ["b", "c"], "g", "M")
    if ok or f:
        fails.append("empty consumes list must be legal (consumes none) and not refused")
    if not consumes_behaviour({"consumes": ["zz"]}, "b", ["b", "c"], "g", "M")[1]:
        fails.append("unknown behaviour name in consumes not refused (fail loud on unknown)")
    if not non_consumer_marker_fails(bfilled, "b", "g", "M"):
        fails.append("non-consumer carrying AUTO-BEHAVIOUR markers not refused (inert payload undetected)")
    if non_consumer_marker_fails("<style>clean</style>", "b", "g", "M"):
        fails.append("clean non-consumer wrongly refused (green control)")
    # 5e. MARKUP partials (#68, dv-lockup) — source extraction, per-occurrence render, tamper teeth
    msrc = ("<!-- ===== MARKUP dv-lockup-title START (dataviz) ===== -->\n"
            "<h3 class=\"dv-title t-cm-section-label\">Original title</h3>\n"
            "<!-- ===== MARKUP dv-lockup-title END ===== -->")
    got = markup_source_block(msrc, "dv-lockup-title")
    if got != '<h3 class="dv-title t-cm-section-label">Original title</h3>':
        fails.append("markup_source_block extraction wrong: %r" % got)
    r1 = render_markup(got, "text", "Member title A")
    r2 = render_markup(got, "text", "Member title B")
    if r1 == r2 or "Member title A" not in r1:
        fails.append("render_markup(text) not substituting per-occurrence value (no teeth)")
    tsrc = '<button class="dv-tbl-toggle" aria-controls="cc1-tbl">View as table</button>'
    ra = render_markup(tsrc, "attr:aria-controls", "cs1-tbl")
    if 'aria-controls="cs1-tbl"' not in ra or "cc1-tbl" in ra:
        fails.append("render_markup(attr:) did not rewrite the target attribute")
    mempty = ('<figure class="dv" data-lockup-title="X">'
              '<!-- ===== AUTO-MARKUP dv-lockup-title START (dataviz) ===== -->'
              '<!-- ===== AUTO-MARKUP dv-lockup-title END ===== -->'
              '</figure>')
    if not AUTO_MARKUP_RE("dv-lockup-title").search(mempty):
        fails.append("empty AUTO-MARKUP marker pair not matched (fresh migrations would fail)")
    if figure_attrs(mempty).get("data-lockup-title") != "X":
        fails.append("figure_attrs did not read data-lockup-title off the figure tag")
    if not FIGURE_RE.search(mempty):
        fails.append("FIGURE_RE did not match a <figure>...</figure> block")
    # 5f. #211 lane R6 — COMMENTED-OUT CONTENT MUST NOT SATISFY A CONTRACT.
    #     Six bites: three on the three contract readers, two on the mask's own properties,
    #     one on the FENCE (the mask must NOT reach the HTML-comment markers).
    #  (i) declared_value: a declaration inside an HTML comment is not a declaration
    commented = '<style>.x{color:red}</style>\n<!-- .y{--press-travel: 1px;} -->'
    if declared_value(commented, "--press-travel") is not None:
        fails.append("declared_value satisfied by a declaration inside an HTML comment (#211 class)")
    if declared_value('<style>.y{--press-travel: 1px;}</style>', "--press-travel") != "1px":
        fails.append("declared_value no longer sees a REAL declaration (mask over-reached)")
    p6 = {"requires": {"vars": ["--press-travel"], "matchValues": [], "declarations": []}}
    if not any("required var --press-travel" in f for f in check_contracts("T", commented, p6, commented)):
        fails.append("requires.vars satisfied by a commented-out declaration (#211 class)")
    #  (ii) matchValues must not read the SOURCE atom's commented-out value as its value
    src_c = '<!-- :root{--spring: 999ms;} -->\n<style>:root{--spring: 300ms;}</style>'
    p6b = {"requires": {"vars": [], "matchValues": ["--spring"], "declarations": []}}
    if check_contracts("T", '<style>:root{--spring: 300ms;}</style>', p6b, src_c):
        fails.append("matchValues compared against the source atom's COMMENTED-OUT value (#211 class)")
    #  (iii) the `declarations` substring test
    p6c = {"requires": {"vars": [], "matchValues": [], "declarations": ['data-tip="']}}
    if not any("required declaration" in f
               for f in check_contracts("T", '<!-- <i data-tip="x"></i> -->', p6c, "")):
        fails.append("required declaration satisfied by text inside an HTML comment (#211 class)")
    #  (iv) manifest_vars: a commented-out manifest is not the document's manifest
    real_mf = '<script id="token-manifest">{"vars":{"--a":"p/real"}}</script>'
    if manifest_vars('<!-- ' + real_mf.replace("real", "dead") + ' -->') != {}:
        fails.append("manifest_vars read a #token-manifest sitting inside an HTML comment (#211 class)")
    if manifest_vars(real_mf).get("--a") != "p/real":
        fails.append("manifest_vars no longer reads a REAL manifest (mask over-reached)")
    #  (v) mask properties: length preserved (manifest_vars' span depends on it) and an
    #      UNTERMINATED `<!--` masks to EOF, as a browser reads it
    for probe in (commented, src_c, '<a><!-- x --><b>', '<a><!-- never closed'):
        if len(mask_comments(probe)) != len(probe):
            fails.append("mask_comments stopped preserving length — manifest_vars' span misaligns")
        if mask_comments(probe).count("\n") != probe.count("\n"):
            fails.append("mask_comments ate a newline (line numbers would misalign)")
    if "unterminated" in mask_comments('<style>x</style><!-- unterminated'):
        fails.append("an unterminated <!-- did not mask to EOF (a browser reads it as a comment)")
    if manifest_vars('<!-- open\n' + real_mf) != {}:
        fails.append("a manifest after an UNTERMINATED <!-- was read as live (browser reads it dead)")
    #  (vi) THE FENCE — the mask must NOT reach the markers that ARE HTML comments.
    #       BEHAVIOUR/MARKUP/AUTO-MARKUP markers must still be found in the RAW text.
    if BEHAVIOUR_RE("b").search(live_text(bempty)):
        fails.append("marker fence broken: AUTO-BEHAVIOUR markers survive masking, so the "
                     "'do not mask the injection sites' fence would be untestable")
    if not (BEHAVIOUR_RE("b").search(bempty) and AUTO_MARKUP_RE("dv-lockup-title").search(mempty)
            and markup_source_block(msrc, "dv-lockup-title")):
        fails.append("HTML-comment markers no longer read from RAW text — the mask over-reached "
                     "into the injection sites (#211 lane R6 fence)")
    # 5g. #211 lane R7 — A COMMENTED-OUT SOURCE OR TARGET IS NEVER AN INJECTION SITE.
    #     The span selectors LOCATE LIVE and SLICE RAW. Five bites: the figure walk (the live
    #     defect), the swallow shape it caused, the raw-slice property the AUTO-MARKUP markers
    #     depend on, source_block, and AUTO_RE — plus green controls for each.
    #  (i) FIGURE_RE: a <figure> named inside a prose comment is not an injection site. This is
    #      Image-block.reference.html's exact shape (offset 368, "real <figure>/<figcaption>").
    real_fig = ('<figure class="dv" data-lockup-title="X">'
                '<!-- ===== AUTO-MARKUP dv-lockup-title START (dataviz) ===== -->'
                '<!-- ===== AUTO-MARKUP dv-lockup-title END ===== -->'
                '</figure>')
    doc_fig = '<!--\n  prose: uses real <figure>/<figcaption> semantics\n-->\n' + real_fig
    spans = live_figure_spans(doc_fig)
    if len(spans) != 1 or doc_fig[spans[0][0]:spans[0][1]] != real_fig:
        fails.append("live_figure_spans selected a <figure> named inside an HTML comment "
                     "(#211 lane R7) — got %r" % [doc_fig[a:b][:40] for a, b in spans])
    #      the SWALLOW is the reason it matters: read raw, that span starts in the comment and
    #      runs to the REAL </figure>, so the live figure disappears inside it.
    raw_spans = [m.span() for m in FIGURE_RE.finditer(doc_fig)]
    if raw_spans and raw_spans[0][0] >= doc_fig.index(real_fig):
        fails.append("the raw-text swallow this arm exists to prove no longer reproduces — "
                     "the arm has stopped testing anything (#211 lane R7)")
    #  (ii) SLICE RAW, never the mask — driven THROUGH rewrite_live_figures, the function run()
    #       actually calls, not through a re-implementation of it. The AUTO-MARKUP markers inside
    #       a live figure ARE HTML comments; if the splice handed the mask on, all 80 injection
    #       sites would arrive blanked and nothing would ever be injected (R6 fence).
    _seen_by_fn = []
    def _probe_fig(fig_bytes):
        _seen_by_fn.append(fig_bytes)
        return fig_bytes
    if rewrite_live_figures(doc_fig, _probe_fig) != doc_fig:
        fails.append("rewrite_live_figures is not byte-identity under an identity callback — "
                     "the splice is losing or duplicating bytes (#211 lane R7)")
    if len(_seen_by_fn) != 1 or _seen_by_fn[0] != real_fig:
        fails.append("rewrite_live_figures handed the callback the wrong figure bytes: %r"
                     % [s[:40] for s in _seen_by_fn])
    if not (_seen_by_fn and AUTO_MARKUP_RE("dv-lockup-title").search(_seen_by_fn[0])):
        fails.append("the figure reached the injection callback as MASKED bytes — its AUTO-MARKUP "
                     "markers are gone, so nothing would ever be injected (#211 lane R7 fence)")
    #       green control: a document with no commented figure is selected identically either way
    if live_figure_spans(real_fig) != [m.span() for m in FIGURE_RE.finditer(real_fig)]:
        fails.append("live_figure_spans moved a REAL figure's span (mask over-reached)")
    #  (iii) source_block: a PARTIAL block inside an HTML comment is dead CSS, not a source atom
    live_src = ("/* ===== PARTIAL q START (t) ===== */\n.btn{transform:scale(1);}\n"
                "/* ===== PARTIAL q END ===== */")
    if source_block("<!--\n" + live_src.replace("scale(1)", "scale(9)") + "\n-->", "q") is not None:
        fails.append("source_block read a PARTIAL block sitting inside an HTML comment as the "
                     "atom's source of truth (#211 lane R7)")
    if source_block(live_src, "q") != ".btn{transform:scale(1);}":
        fails.append("source_block no longer reads a REAL PARTIAL block (mask over-reached)")
    #       …and the payload must be the ORIGINAL bytes, not the mask's. Reachable shape: an HTML
    #       comment INSIDE the PARTIAL block — the markers are still live, so the block is found,
    #       but a masked payload would inject blanks where CSS bytes were. LATENT, not live: 0
    #       style blocks in the tree carry a literal '<!--' today (#211 lane R7 census).
    cdo_src = ("/* ===== PARTIAL q START (t) ===== */\n.a{x:1}<!-- note -->.b{y:2}\n"
               "/* ===== PARTIAL q END ===== */")
    if source_block(cdo_src, "q") != ".a{x:1}<!-- note -->.b{y:2}":
        fails.append("source_block returned MASKED bytes instead of the original CSS — the "
                     "injected payload would be blanked where the source held bytes (#211 lane R7)")
    #  (iv) AUTO_RE via live_match: a marker pair inside an HTML comment is not a target
    if live_match(AUTO_RE("p"), "<!--\n" + empty + "\n-->") is not None:
        fails.append("an AUTO-PARTIAL marker pair inside an HTML comment was selected as an "
                     "injection target — the payload would be written where no browser reads it")
    lm = live_match(AUTO_RE("p"), filled)
    if lm is None or filled[lm.start(2):lm.end(2)] != "\nX\n  ":
        fails.append("live_match lost a REAL AUTO-PARTIAL payload span (mask over-reached, or "
                     "the group span stopped addressing the original bytes)")
    # 5h. #229 — THE MEMBERSHIP SCAN. Every arm below is a MUTATION: the gate must go red on a
    #     planted defect and stay green on the control. An instrument that has never failed has
    #     never been tested [[instrument-without-a-consumer]].
    #  (i) declares_selector: a real rule counts; prose, dead CSS and a near-miss class do not
    live_css = '<style>\n.seg{border:1px solid red;}\n.seg .ind{width:0;}\n</style>'
    if declares_selector(live_css, [".seg"]) != {".seg"}:
        fails.append("declares_selector missed a REAL .seg rule (the scan would enrol nobody)")
    if declares_selector('<style>/* .seg{border:0} in prose */\n.x{color:red}</style>', [".seg"]):
        fails.append("declares_selector enrolled a file for naming .seg inside a CSS COMMENT "
                     "(ds-008 class) — Data-grid's header says .seg is a blast radius it must "
                     "NOT join, and would be enrolled for saying so")
    if declares_selector('<!-- ' + live_css + ' -->', [".seg"]):
        fails.append("declares_selector read a <style> block sitting inside an HTML comment as "
                     "live CSS (#211 lane R6 class)")
    if declares_selector('<style>.dgseg{x:1} .seg-x{y:2}</style>', [".seg"]):
        fails.append("declares_selector matched .dgseg / .seg-x — word-boundary matching is gone, "
                     "and Data-grid's deliberately namespaced control would be dragged in")
    if declares_selector('<script>document.querySelectorAll(".seg")</script>', [".seg"]):
        fails.append("declares_selector matched a .seg string in JS — only SELECTOR position in a "
                     "<style> block may enrol a file")
    if declares_selector('<style>@media (min-width:40em){ .seg .ind{transition:none;} }</style>',
                         [".seg"]) != {".seg"}:
        fails.append("declares_selector missed a rule nested in an @media block (View-options' "
                     "reduced-motion .seg .ind rule is exactly this shape)")
    #  (ii) the gate's logic, driven on a fixture (hits injected — no live tree needed)
    fixture = {"$members": {"A": {"role": "source"}, "B": {"selector": ".seg"}},
               "$scan": {"selectors": [".seg"], "$exempt": {"C": "a stated reason"}}}
    hits_ok = {"A": [".seg"], "B": [".seg"], "C": [".seg"]}
    if check_scan("g", fixture, hits_ok):
        fails.append("membership scan failing on a clean fixture: %s"
                     % "; ".join(check_scan("g", fixture, hits_ok)))
    #      an UNREGISTERED control must go red — the #227 missed-sweep class itself
    got = check_scan("g", fixture, dict(hits_ok, D=[".seg"]))
    if not any("D declares" in f and "NOT a member" in f for f in got):
        fails.append("membership scan did NOT catch an unregistered .seg (the whole point: this "
                     "is the defect that shipped square controls for three sessions)")
    #      a BLANK exemption reason must go red
    blank = {"$members": fixture["$members"],
             "$scan": {"selectors": [".seg"], "$exempt": {"C": "   "}}}
    if not any("has no reason" in f for f in check_scan("g", blank, hits_ok)):
        fails.append("membership scan accepted an exemption with no stated reason")
    #      member AND exempt at once must go red
    both = {"$members": dict(fixture["$members"], C={"selector": ".seg"}),
            "$scan": fixture["$scan"]}
    if not any("BOTH registered members and exempt" in f for f in check_scan("g", both, hits_ok)):
        fails.append("membership scan accepted a snippet that is both a member and exempt")
    #      a ROTTED exemption (file no longer declares the selector) must go red
    if not any("rotted exemption" in f
               for f in check_scan("g", fixture, {"A": [".seg"], "B": [".seg"]})):
        fails.append("membership scan accepted an exemption whose file no longer declares the "
                     "selector — a rotted exemption hides the next real one")
    #      a STALE member (registered, declares nothing) must go red
    if not any("stale registry entry" in f
               for f in check_scan("g", fixture, {"A": [".seg"], "C": [".seg"]})):
        fails.append("membership scan accepted a member that declares none of its selectors")
    #      a group with no $scan is untouched; a $scan with no selectors refuses
    if check_scan("g", {"$members": {}}, {}):
        fails.append("check_scan invented failures for a group that declares no $scan")
    if not check_scan("g", {"$members": {}, "$scan": {"selectors": []}}, {}):
        fails.append("a $scan with no selectors was accepted — an instrument that cannot fail")
    #  (iii) the LIVE registry must pass its own scan (same posture as arm 6 below)
    live_scan = [x for gn, gg in groups(load_registry()).items() for x in check_scan(gn, gg)]
    if live_scan:
        fails.append("live registry membership scan failing: %s" % "; ".join(live_scan))
    # 6. registry caches: live registry must pass; a poisoned cache must fail
    reg = load_registry()
    live = check_caches(reg)
    if live:
        fails.append("live registry cache check failing: %s" % "; ".join(live))
    poisoned = json.loads(json.dumps(reg))
    for g in groups(poisoned).values():
        for k, node in g.items():
            if not k.startswith("$") and isinstance(node, dict) and "$value" in node:
                node["$value"] = 999
    if not check_caches(poisoned):
        fails.append("poisoned registry cache NOT caught (gate has no teeth)")
    return fails

def main():
    if "--selftest" in sys.argv:
        f = selftest()
        if f:
            print("gen_component_partials SELFTEST FAIL:"); [print("  X " + x) for x in f]
            sys.exit(1)
        print("gen_component_partials selftest OK")
        return
    write = "--check" not in sys.argv
    fails, out_of_sync, injected = run(write)
    if fails:
        print("gen_component_partials CONTRACT FAILURES:"); [print("  X " + x) for x in fails]
    if "--check" in sys.argv:
        if out_of_sync:
            print("gen_component_partials --check: AUTO-PARTIAL blocks OUT OF SYNC: "
                  + ", ".join(out_of_sync))
            print("  Run: python3 knowledge/gen_component_partials.py")
        if fails or out_of_sync:
            sys.exit(1)
        print("gen_component_partials --check OK — all AUTO-PARTIAL blocks in sync, contracts hold.")
        return
    if fails:
        sys.exit(1)
    print(f"gen_component_partials: {injected} consumer block(s) injected/refreshed"
          + ("" if injected else " (all in sync)"))

if __name__ == "__main__":
    main()
