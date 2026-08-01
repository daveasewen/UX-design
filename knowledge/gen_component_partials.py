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
import json, os, re, sys

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
    """CSS between the atom's PARTIAL markers (exclusive). None if absent."""
    m = re.search(r'/\* ===== PARTIAL ' + re.escape(pname) + r' START[^\n]*===== \*/\n(.*?)\n\s*/\* ===== PARTIAL '
                  + re.escape(pname) + r' END ===== \*/', html, re.S)
    return m.group(1) if m else None

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

# ------------------------------------------------------------------ contracts
def declared_value(html, var):
    """First declared value of --var anywhere in the document's CSS."""
    m = re.search(re.escape(var) + r'\s*:\s*([^;]+);', html)
    return m.group(1).strip() if m else None

MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)

def manifest_vars(html):
    m = MANIFEST_RE.search(html)
    return (json.loads(m.group(1)).get("vars", {})) if m else {}

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
    for needle in list(req.get("declarations", [])) + list(extra.get("declarations", [])):
        if needle not in html:
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

# ------------------------------------------------------------------ main pass
def run(write):
    reg = load_registry()
    fails, out_of_sync, injected = [], [], 0
    fails += check_caches(reg)
    for gname, g in groups(reg).items():
        members = g.get("$members", {})
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
                m = rx.search(html)
                if not m:
                    fails.append(f"{gname}/{pname}: {mname} is a member but carries no AUTO-PARTIAL "
                                 f"markers (membership is deliberate — add the marker pair to migrate)")
                    continue
                if m.group(2) != between:
                    out_of_sync.append(f"{mname} ({pname})")
                    if write:
                        html = rx.sub(lambda mm: mm.group(1) + between + mm.group(3), html, count=1)
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
                missing_mandatory = [n for n in mandatory_names if n not in markup_list]
                if missing_mandatory:
                    fails.append(f"{gname}/markup: {mname}: missing mandatory markup partial(s) {missing_mandatory}")
                for pname in mk:
                    if pname not in markup_list and AUTO_MARKUP_RE(pname).search(html):
                        fails.append(f"{gname}/markup: {mname} does not declare {pname} but carries its "
                                     f"AUTO-MARKUP markers — remove the pair, or add \"{pname}\" to its markup list")
                seen = {n: 0 for n in markup_list}
                local_fails = []
                inj_count = [0]
                def process_fig(fm):
                    fig_html = fm.group(0)
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
                new_html = FIGURE_RE.sub(process_fig, html)
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
