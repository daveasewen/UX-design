#!/usr/bin/env python3
"""
gen_theme_cascade.py — generate the [data-apollo-theme] override cascade (ADR-0011).

THE THEME-RESOLUTION LAYER (build-out Phase 0, 2026-07-21). One baseline library,
four themes as override sets at the semantic tier (ADR-0011 + ADR-0010). This
generator renders those override sets into CSS so that switching theme is ONE
attribute — components stay theme-blind.

    resolve(role, mode, theme): theme override wins; else base (Mono).

Sources (never hand-typed, so it cannot rot):
  * tokens/themes/_themes.json                the registry (attr names, file paths)
  * tokens/themes/<theme>.overrides.json      the override sets (per-mode values)
  * snippets/*.reference.html #token-manifest each component's var -> token-path map

Emits into canon/canon.css between AUTO-THEMES markers (appended at EOF — AFTER
the token spine, aliases and components, so equal-specificity theme-light
declarations beat base :root by order):

  1. ROOT tier — canonical vars (--<token-path-joined>) per theme:
       [data-apollo-theme="legacy"]{ --rag-success:#00847F; ... }
       [data-apollo-theme="legacy"][data-theme="dark"],
       [data-apollo-theme="legacy"] [data-theme="dark"]{ ...dark values... }
     Serves every consumer of spine vars + semantic aliases (composed screens).
     Modeless tokens (e.g. --border-radius-default) emit in the root block only.

  2. COMPONENT tier — the projected-literal problem: .cn-<slug> blocks carry
     per-mode LITERALS (gen_snippet_tokens project_canon), which no root var can
     reach. So for every snippet-manifest var whose token path a theme overrides,
     re-project the override at higher specificity:
       [data-apollo-theme="legacy"] .cn-button{ --pri-default:#DB0011; ... }
       [data-apollo-theme="legacy"][data-theme="dark"] .cn-button,
       [data-apollo-theme="legacy"] [data-theme="dark"] .cn-button{ ... }

Specificity proof (why this cascade is correct in both modes):
  base .cn-x{--v:lit}                      (0,1,0)
  [data-theme=dark] .cn-x{--v:lit}         (0,2,0)
  [theme] .cn-x{--v:o}                     (0,2,0) + LATER in file  -> wins light
  [theme][data-theme=dark] .cn-x{--v:o}    (0,3,0)                  -> wins dark
  Both modes are ALWAYS emitted for an overridden path (missing mode falls back
  to the base store value) so a theme-light value can never leak into dark.

Also exports snippet_theme_css(manifest) for gen_showroom.py — the same override
projection scoped for a STANDALONE snippet document (bare [data-theme] blocks on
<body>, data-apollo-theme set on <html> by the harness chrome).

Usage:
  python3 knowledge/canon/gen_theme_cascade.py             # write canon.css block
  python3 knowledge/canon/gen_theme_cascade.py --check     # verify in-sync (build gate)
  python3 knowledge/canon/gen_theme_cascade.py --selftest  # invariant bite-test
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, re, sys, glob

HERE   = os.path.dirname(os.path.abspath(__file__))
KNOW   = os.path.dirname(HERE)
TOK    = os.path.join(KNOW, "tokens")
SNIP   = os.path.join(KNOW, "snippets")
sys.path.insert(0, KNOW)
from _dtcg_units import px_number            # s141-D1 (A) unit-strip seam
CANON  = os.path.join(HERE, "canon.css")
START  = "/* ===== AUTO-THEMES START ===== */"
END    = "/* ===== AUTO-THEMES END ===== */"
MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)
MODES  = ("light", "dark")

# ---------------------------------------------------------------- token stores
_STORES = {}
def _store(fname):
    if fname not in _STORES:
        # "../component-types.json" = the ADR-0013 registry at knowledge/ root — a token
        # store for its parameter halves ($members/$partials are structural, never walked).
        _STORES[fname] = json.load(open(os.path.join(TOK, fname)))
    return _STORES[fname]

def _store_for(path):
    if path.startswith("color/"):
        return _store("colour.json")
    if path.startswith(("border-radius/", "border-width/", "breakpoint/", "layout/", "focus-ring/", "target/")):
        return _store("layout.json")
    if path.startswith("motion/"):
        return _store("motion.json")
    if path.startswith("component-type/"):
        return _store("../component-types.json")
    return _store("semantic-colour.json")

def base_value(path, mode, _depth=0):
    """Resolve a token path + mode from the BASE (Mono) stores. Fail loud.
    Chain-aware (ADR-0014): a pure-$alias node (no cached $value, e.g. the
    color/neutral DNA tier before its cache is stamped) resolves through its
    target, bounded against loops."""
    node = _store_for(path)
    for key in path.split("/"):
        node = node[key]                      # KeyError = fail loud in caller
    if mode in node and isinstance(node[mode], dict) and "$value" in node[mode]:
        return node[mode]["$value"]
    if "$value" in node:
        return node["$value"]
    if "$alias" in node and isinstance(node["$alias"], str):
        if _depth > 8:
            raise KeyError(f"alias loop resolving {path}")
        return base_value(node["$alias"], mode, _depth + 1)
    raise KeyError(f"{path} has no '{mode}' value in base store")

# ---------------------------------------------------------------- alias map
def _walk_aliases(node, path, out):
    if not isinstance(node, dict):
        return
    if "$alias" in node:
        a = node["$alias"]
        if isinstance(a, str):
            out[path] = {"modeless": a}
        elif isinstance(a, dict):
            out[path] = {m: a[m] for m in MODES if a.get(m)}
        return
    if "$value" in node:
        return
    for k, v in node.items():
        if not k.startswith("$"):
            _walk_aliases(v, f"{path}/{k}" if path else k, out)

def alias_map():
    """{path: {'modeless': target} | {'light': t, 'dark': t}} across all stores.
    The base store's OWN $alias edges — what lets a theme override of an alias
    TARGET cascade to every path that follows it (semantic radius tier, Dave
    2026-07-21 evening: roles fall back to default unless dialed themselves).
    Includes the ADR-0013 registry: component-type/<group>/<param> aliases its
    semantic home (e.g. motion/scale/press-grow), so a theme override of the
    semantic role cascades to every type-group parameter that follows it — the
    component -> type-group -> semantic role -> default hop."""
    out = {}
    for f in ("colour.json", "semantic-colour.json", "layout.json", "../component-types.json"):
        for k, v in _store(f).items():
            if not k.startswith("$"):
                _walk_aliases(v, k, out)
    return out

def _expand_aliases(entry, amap):
    """Materialise EFFECTIVE overrides: any aliased path not itself overridden,
    whose target (transitively) is, inherits the theme value — unless the result
    equals the base value (no-op emissions are skipped, keeps blocks minimal).
    A path's own override always wins (checked first). Fixed-point for chains."""
    ov = entry["overrides"]
    if not ov:
        return
    for _ in range(len(amap) + 1):
        changed = False
        for path, al in amap.items():
            if path in ov:
                continue
            if "modeless" in al:
                t = ov.get(al["modeless"])
                if t:
                    base = css_value(path, base_value(path, "light"))
                    val = t.get("modeless") or t.get("light")
                    if val != base:
                        ov[path] = dict(t)
                        changed = True
            else:
                pair, hit = {}, False
                for m in MODES:
                    t = ov.get(al.get(m)) if al.get(m) else None
                    if t:
                        pair[m] = t.get(m) or t.get("modeless")
                        hit = True
                if hit:
                    for m in MODES:
                        pair.setdefault(m, css_value(path, base_value(path, m)))
                    if any(pair[m] != css_value(path, base_value(path, m)) for m in MODES):
                        ov[path] = pair
                        changed = True
        if not changed:
            break

# ---------------------------------------------------------------- themes
def normalize(seg):
    return re.sub(r"[^a-z0-9]+", "-", str(seg).lower()).strip("-")

def var_name(path):
    return "--" + "-".join(normalize(s) for s in path.split("/"))

def css_value(path, val):
    """Format an override $value for CSS. Numbers are px except 0 and the
    unitless namespaces — motion scale factors, the component-type parameters
    that cache them, and the DV-D07 data/*/alpha slots (matches gen_canon_tokens
    fmt_value / gen_snippet_tokens)."""
    # s141-D1 (A) unit-strip seam: migrated tokens arrive as "Npx"; strip back to the
    # number so the SAME rules below apply and the emitted CSS is unchanged. Without
    # this a base "0px" no longer equals an override 0 and the cascade emits spurious
    # overrides for every theme that merely restates the base value.
    val = px_number(val)
    if isinstance(val, (int, float)):
        if path.startswith("motion/press/") or path.rsplit("/", 1)[-1] in ("press-travel", "press-darken", "alpha"):
            return str(val)
        return "0" if val == 0 else f"{val}px"
    return str(val)

def palette_values(rel, _cache={}):
    """s157-D2 — the NAMED-PALETTE TIER (shared-by-reference projection).

    `rel` is a registry `ragPalette` path relative to knowledge/tokens/
    (e.g. "palettes/rag/console-supercharge.json"). Returns
    {token_path: {'light': cssval, 'dark': cssval}} for every key the palette
    DECLARES. Two themes naming the SAME file get the SAME dict — that is the
    sharing, expressed once, instead of two hand-kept hex copies (console +
    supercharge carried 12 hex-identical duplicate keys with nothing declaring it).

    Keys the palette does not declare (its $partialKeys) are NOT emitted: absence
    is a fall-through the palette file records explicitly, never a value invented
    here. -tint keys are not in the palette vocabulary at all — they derive from
    per-theme grounds (s123-D3) and stay in each override set.
    """
    if rel not in _cache:
        pal = json.load(open(os.path.join(TOK, rel)))
        out = {}
        for key, node in (pal.get("keys") or {}).items():
            path = f"rag/{key}"
            pair = {}
            for m in MODES:
                if m in node and isinstance(node[m], dict) and "$value" in node[m]:
                    pair[m] = css_value(path, node[m]["$value"])
                else:
                    pair[m] = css_value(path, base_value(path, m))   # fall back, never leak
            out[path] = pair
        _cache[rel] = out
    return dict(_cache[rel])


def load_themes():
    """Registry -> ordered list of {key, attr, label, status, overrides} where
    overrides = {path: {'light': cssval, 'dark': cssval} | {'modeless': cssval}}.
    Base theme (Mono) carries no overrides. Null override values (ADR-0010
    declared-but-unset) are skipped: declared, no emission."""
    reg = json.load(open(os.path.join(TOK, "themes", "_themes.json")))
    out = []
    for key, t in sorted(reg["themes"].items(), key=lambda kv: kv[1].get("order", 99)):
        entry = {"key": key, "attr": t.get("attr") or key.replace("apollo-", ""),
                 "label": t.get("label", key), "status": t.get("status"), "overrides": {},
                 "marks": {}, "guards": {}}
        # s157-D2: the named-palette tier projects BEFORE the override set, so a shared
        # palette reaches a theme even where no override file line carries the hex. The
        # override set still loads on top (below) — today every palette-owned key is
        # ALSO declared in the ratified override files, so this projection is a proven
        # no-op on the emitted CSS (gen_theme_cascade --check byte-identical, #158) and
        # the ADD-never-trim posture on those files is untouched. Divergence between the
        # two sources is not resolved here — it is FORBIDDEN, by _validate_palette_tier.py.
        pal = t.get("ragPalette")
        if pal and t.get("status") != "base":
            entry["overrides"].update(palette_values(pal))
        oset = t.get("overrideSet")
        if oset and t.get("status") != "base":
            data = json.load(open(os.path.join(TOK, oset)))
            for path, node in data.get("overrides", {}).items():
                if node is None:
                    continue                          # ADR-0010 declared-but-unset
                if "light" in node or "dark" in node:
                    pair = {}
                    for m in MODES:
                        if m in node and isinstance(node[m], dict) and "$value" in node[m]:
                            pair[m] = css_value(path, node[m]["$value"])
                        else:
                            pair[m] = css_value(path, base_value(path, m))  # fall back, never leak
                    entry["overrides"][path] = pair
                elif "$alias" in node and isinstance(node["$alias"], str):
                    # ADR-0014: an override may point at a base-store primitive (e.g. supercharge
                    # binds color/neutral/N -> color/warm/N). Resolved to literals at load so the
                    # primitive stays the single source (retrieval-not-recall); emission shape is
                    # modeless when both modes agree.
                    tgt = node["$alias"]
                    vl = css_value(path, base_value(tgt, "light"))
                    vd = css_value(path, base_value(tgt, "dark"))
                    entry["overrides"][path] = {"modeless": vl} if vl == vd else {"light": vl, "dark": vd}
                elif "$value" in node:
                    entry["overrides"][path] = {"modeless": css_value(path, node["$value"])}
            # MARKS (s121-D1 mechanism, extended #122 for s122-D3): --mark-* is NOT a store
            # token — its source atom lives in canon.css (TOKENS marks) and is distributed by
            # gen_token_ramp.py. A theme that re-rules the knockout carries it in a sibling
            # "marks" key here, so the override set stays the ONE source for that theme.
            for status, node in (data.get("marks") or {}).items():
                if node is None:
                    continue                          # ADR-0010 declared-but-unset
                pair = {}
                for m in MODES:
                    if isinstance(node.get(m), dict) and "$value" in node[m]:
                        pair[m] = str(node[m]["$value"])
                if len(pair) != len(MODES):
                    raise KeyError(f"{key}: marks/{status} must declare BOTH modes "
                                   f"(no base --mark-* token exists to fall back to)")
                entry["marks"][status] = pair
            # GUARDS (s158-D1, Dave #158: "the generator learns to emit these"). A guard is
            # NOT a token override — it is a declaration that this theme KEEPS a paint a
            # later mono-only ruling moved (s149-D1 banner ink + tab badge seat, s151-D1's
            # no-op --error-atom fork guard). They were hand-edited into canon.css's
            # "do NOT hand-edit" block, which is why --check went red; they live HERE now,
            # in the same file that is already the ONE source for this theme (like marks).
            entry["guards"] = data.get("guards") or {}
        out.append(entry)
    amap = alias_map()
    for entry in out:
        _expand_aliases(entry, amap)
    return out

# ---------------------------------------------------------------- manifests
def snippet_manifests():
    """[(slug, {cssvar: tokenpath})] for every reference snippet with a manifest."""
    out = []
    for f in sorted(glob.glob(os.path.join(SNIP, "*.reference.html"))):
        mm = MANIFEST_RE.search(open(f).read())
        if not mm:
            continue
        slug = re.sub(r"[^a-z0-9]+", "-",
                      os.path.basename(f).replace(".reference.html", "").lower()).strip("-")
        out.append((slug, json.loads(mm.group(1)).get("vars", {})))
    return out

def component_overrides(varmap, theme):
    """{cssvar: {'light': v, 'dark': v}} for manifest vars whose token path the
    theme overrides. Modeless overrides project into both modes."""
    hits = {}
    for cssvar, path in varmap.items():
        ov = theme["overrides"].get(path)
        if not ov:
            continue
        if "modeless" in ov:
            hits[cssvar] = {"light": ov["modeless"], "dark": ov["modeless"]}
        else:
            hits[cssvar] = {"light": ov["light"], "dark": ov["dark"]}
    return hits

# ---------------------------------------------------------------- CSS emission
def _decls(pairs, mode, indent="  ", comments=None):
    comments = comments or {}
    out = []
    for v, vals in sorted(pairs.items()):
        line = f"{indent}{v}: {vals[mode]};"
        if v in comments:
            line += f"  /* {comments[v]} */"
        out.append(line)
    return "\n".join(out)

# ---------------------------------------------------------------- guards (s158-D1)
def _comment_lines(note, indent):
    """A CSS comment from a list of authored lines. Continuations align under the
    opener's text column (indent + 3), which is how the hand-edits were written."""
    out, cont = [], indent + "   "
    for i, ln in enumerate(note):
        pre = indent + "/* " if i == 0 else cont
        out.append(pre + ln + (" */" if i == len(note) - 1 else ""))
    return out

def _guard_tail(gd, comments, note, indent="  "):
    """Appended (unsorted) guard declarations, optionally preceded by a note.
    Authored order is preserved — these are STATEMENTS about what a theme keeps,
    not values in the override set's sorted namespace."""
    lines = []
    if note:
        lines += _comment_lines(note, indent)
    for v, n in gd.items():
        line = f"{indent}{v}: {n['value']};"
        if v in comments:
            line += f"  /* {comments[v]} */"
        lines.append(line)
    return lines

def theme_block(theme, manifests):
    """Full canon.css cascade for one theme ('' for the base theme)."""
    ov = theme["overrides"]
    mk = theme.get("marks") or {}
    if not ov and not mk:
        return ""
    a = theme["attr"]
    lines = [f'/* ---- {theme["label"]}  [data-apollo-theme="{a}"]  '
             f'({len(ov)} override path(s)'
             + (f", {len(mk)} mark(s)" if mk else "")
             + f', {theme["key"]}.overrides) ---- */']
    # ROOT tier
    root_light, root_dark = {}, {}
    for path, vals in sorted(ov.items()):
        vn = var_name(path)
        if "modeless" in vals:
            root_light[vn] = {"light": vals["modeless"]}
        else:
            root_light[vn] = {"light": vals["light"]}
            root_dark[vn] = {"dark": vals["dark"]}
    for status, vals in sorted(mk.items()):
        vn = f"--mark-{normalize(status)}"
        root_light[vn] = {"light": vals["light"]}
        root_dark[vn] = {"dark": vals["dark"]}
    lines.append(f'[data-apollo-theme="{a}"]{{')
    lines.append(_decls(root_light, "light"))
    lines.append("}")
    if root_dark:
        lines.append(f'[data-apollo-theme="{a}"][data-theme="dark"],')
        lines.append(f'[data-apollo-theme="{a}"] [data-theme="dark"]{{')
        lines.append(_decls(root_dark, "dark"))
        lines.append("}")
    # COMPONENT tier (projected-literal re-binding)
    guards = theme.get("guards") or {}
    for slug, varmap in manifests:
        hits = component_overrides(varmap, theme)
        g = guards.get(slug) or {}
        if not hits:
            if g:
                raise KeyError(f'{theme["key"]}: guard for .cn-{slug} but the theme '
                               f"projects no component vars there — guard would be dropped")
            continue
        gd = g.get("declarations") or {}
        comments = {v: n["$comment"] for v, n in gd.items() if n.get("$comment")}
        tail_light, tail_dark = [], []
        if g.get("placement") == "sorted":
            for v, n in gd.items():                      # joins the sorted namespace
                hits[v] = {"light": n["value"], "dark": n["value"]}
        elif gd:
            tail_light = _guard_tail(gd, comments, g.get("$noteLight"))
            tail_dark = _guard_tail(gd, comments, None)
        sel = f".cn-{slug}"
        lines.append(f'[data-apollo-theme="{a}"] {sel}{{')
        lines.append(_decls(hits, "light", comments=comments))
        lines += tail_light
        lines.append("}")
        for r in (g.get("rules") or []):
            lines += _comment_lines(r["$note"], "")
            lines.append(f'[data-apollo-theme="{a}"] {r["selector"]}{{{r["body"]}}}')
        lines.append(f'[data-apollo-theme="{a}"][data-theme="dark"] {sel},')
        lines.append(f'[data-apollo-theme="{a}"] [data-theme="dark"] {sel}{{')
        lines.append(_decls(hits, "dark", comments=comments))
        lines += tail_dark
        lines.append("}")
    return "\n".join(lines) + "\n"

def build_block():
    themes = load_themes()
    manifests = snippet_manifests()
    body = [START,
            "/* Generated by canon/gen_theme_cascade.py from tokens/themes/*.json +",
            "   snippet #token-manifests (ADR-0011 + ADR-0010). Do NOT hand-edit —",
            "   edit the override sets and re-run. Theme attr goes on <html> or any",
            "   ancestor of the [data-theme] element; Mono is the base (no block).",
            f"   Attrs: " + ", ".join(f'{t["attr"]}={t["key"]}' for t in themes) + " */"]
    n_paths = n_comp = 0
    for t in themes:
        blk = theme_block(t, manifests)
        if blk:
            body.append(blk)
            n_paths += len(t["overrides"])
            n_comp += sum(1 for _, vm in manifests if component_overrides(vm, t))
    body.append(END)
    return "\n".join(body), n_paths, n_comp

# ------------------------------------------------- standalone-snippet export
def snippet_theme_css(manifest_vars, slug=None):
    """The same override projection for ONE standalone snippet document (used by
    gen_showroom.py). Bare [data-theme] blocks live on <body>; the harness sets
    data-apollo-theme on <html>. Emits nothing for themes with no hits.

    GUARDS PARITY (#158, closing the gap the s158-D1 sub declared open): the same
    `guards` vocabulary theme_block() folds into canon.css is emitted here from the
    SAME data source (tokens/themes/*.overrides.json § guards[slug]). Without it a
    showroom pane / Open-↗ standalone doc rendered PRE-GUARD — i.e. a theme that
    explicitly declares it keeps its own paint (Legacy/Console/Supercharge banner
    ink, tabs badge seat, selection-controls --error-atom) would inherit mono's
    instead, in exactly the surface Dave reviews by eye.

    The one deliberate difference is the SELECTOR: canon.css scopes a component to
    `.cn-<slug>` because every component shares one stylesheet; a standalone snippet
    document IS the component, so the `.cn-<slug> ` prefix is stripped from guard
    rule selectors. Declarations ride the same [data-theme] blocks as the projection.
    `slug=None` keeps the pre-#158 behaviour for callers that have no slug."""
    themes = load_themes()
    css = []
    for t in themes:
        hits = component_overrides(manifest_vars, t)
        if not hits:
            continue
        g = ((t.get("guards") or {}).get(slug) or {}) if slug else {}
        gd = g.get("declarations") or {}
        comments = {v: n["$comment"] for v, n in gd.items() if n.get("$comment")}
        tail_light, tail_dark = [], []
        if gd and g.get("placement") == "sorted":
            for v, n in gd.items():                      # joins the sorted namespace
                hits[v] = {"light": n["value"], "dark": n["value"]}
        elif gd:
            tail_light = _guard_tail(gd, comments, g.get("$noteLight"))
            tail_dark = _guard_tail(gd, comments, None)
        a = t["attr"]
        css.append(f'[data-apollo-theme="{a}"] [data-theme="light"],')
        css.append(f'[data-apollo-theme="{a}"][data-theme="light"]{{')
        css.append(_decls(hits, "light", comments=comments))
        css += tail_light
        css.append("}")
        for r in (g.get("rules") or []):
            css += _comment_lines(r["$note"], "")
            sel = r["selector"]
            if slug and sel.startswith(f".cn-{slug} "):
                sel = sel[len(f".cn-{slug} "):]          # the snippet doc IS the component
            css.append(f'[data-apollo-theme="{a}"] {sel}{{{r["body"]}}}')
        css.append(f'[data-apollo-theme="{a}"] [data-theme="dark"],')
        css.append(f'[data-apollo-theme="{a}"][data-theme="dark"]{{')
        css.append(_decls(hits, "dark", comments=comments))
        css += tail_dark
        css.append("}")
    return "\n".join(css)

# ---------------------------------------------------------------- selftest
def selftest():
    fails = []
    themes = {t["key"]: t for t in load_themes()}
    # 1. base emits nothing; every non-base emission is attribute-fenced
    if themes["apollo-mono"]["overrides"]:
        fails.append("base theme (mono) must carry no overrides")
    block, _, _ = build_block()
    for line in block.splitlines():
        if line.endswith("{") and "data-apollo-theme" not in line:
            fails.append(f"unfenced selector in AUTO-THEMES: {line.strip()}")
    # 2. dark tier always combines both attributes (no light->dark leak path)
    for m in re.finditer(r'^([^\n{]*\[data-theme="dark"\][^\n{]*)\{', block, re.M):
        if "data-apollo-theme" not in m.group(1):
            fails.append(f"dark selector without theme fence: {m.group(1)}")
    # 3. both modes emitted for every per-mode override (leak-proof by construction)
    for t in themes.values():
        for path, vals in t["overrides"].items():
            if "modeless" not in vals and ("light" not in vals or "dark" not in vals):
                fails.append(f'{t["key"]}:{path} missing a mode')
    # 4. the ruled facts (ADR-0014 supersedes the pre-R-D22 "supercharge empty" assertion):
    #    Legacy carries the CTA red + as-built tabs; Console rounds INSIDE its sibling fence;
    #    Supercharge rides the warm DNA with the anchor remapped to its ink.
    leg = themes["apollo-legacy"]["overrides"]
    if leg.get("button/primary/background/default", {}).get("light") != "#DB0011":
        fails.append("legacy button/primary default light != #DB0011")
    if leg.get("tabs/active", {}).get("modeless") != "#DB0011":
        fails.append("legacy tabs/active must stay the as-built red #DB0011 (R-D23)")
    cr = themes["apollo-console"]["overrides"].get("border-radius/default", {})
    if not cr or cr.get("modeless") in (None, "0"):
        fails.append("console border-radius/default must be a non-zero modeless value")
    sc = themes["apollo-supercharge"]["overrides"]
    if sc.get("color/neutral/2", {}).get("modeless") != "#13110E":
        fails.append("supercharge neutral/2 must bind the warm ramp (#13110E, ADR-0014)")
    if sc.get("color/neutral/4", {}).get("modeless") != "#13110E":
        fails.append("supercharge ANCHOR remap neutral/4 -> warm/2 #13110E (Dave 2026-07-22) missing")
    if sc.get("text/default", {}).get("light") != "#13110E":
        fails.append("supercharge effective ink must expand to #13110E through the DNA tier")
    if sc.get("progress/complete", {}).get("light") != "#B92F1E":
        fails.append("supercharge progress/complete light != #B92F1E (R-D22)")
    # 4b. the sibling fence (ADR-0014, LOCKED): Console may not diverge on DNA/status/dataviz paths
    reg = json.load(open(os.path.join(TOK, "themes", "_themes.json")))
    fence = (reg["themes"]["apollo-console"].get("fencedPaths") or {}).get("prefixes", [])
    for path in themes["apollo-console"]["overrides"]:
        if any(path.startswith(p) for p in fence):
            fails.append(f"console override '{path}' breaches the sibling fence {fence}")
    # 4c. s158-D1 guards: every declared guard must REACH the emitted block. A guard that
    #     silently vanishes is exactly the failure that put these lines into canon.css by
    #     hand — so assert presence in the built CSS, not merely in the loaded dict.
    for t in themes.values():
        for slug, g in (t.get("guards") or {}).items():
            for v, n in (g.get("declarations") or {}).items():
                if f"{v}: {n['value']};" not in block:
                    fails.append(f'{t["key"]}: guard {v} for .cn-{slug} not emitted')
            for r in (g.get("rules") or []):
                if f'[data-apollo-theme="{t["attr"]}"] {r["selector"]}{{{r["body"]}}}' not in block:
                    fails.append(f'{t["key"]}: guard rule {r["selector"]} not emitted')
    #     The RULED SET, named here so deleting a guard cannot delete its own check
    #     (a check derived only from the data can never fail): s149-D1 is MONO ONLY, so
    #     legacy/console/supercharge each keep the banner ink + both badge seats, and
    #     s151-D1's atom fork is fenced off all three by the no-op guard.
    for key in ("apollo-legacy", "apollo-console", "apollo-supercharge"):
        gs = themes[key].get("guards") or {}
        a = themes[key]["attr"]
        if not (gs.get("banner") or {}).get("rules"):
            fails.append(f"{key}: s149-D1 mono-only banner-ink guard missing (.cn-banner .banner.err)")
        for v in ("--badge-bg", "--badge-ink"):
            if v not in ((gs.get("tabs") or {}).get("declarations") or {}):
                fails.append(f"{key}: s149-D1 mono-only tab-badge guard {v} missing")
        if "--error-atom" not in ((gs.get("selection-controls") or {}).get("declarations") or {}):
            fails.append(f"{key}: s151-D1 --error-atom no-op guard missing")
        if f'[data-apollo-theme="{a}"] .cn-tabs{{' not in block:
            fails.append(f"{key}: no .cn-tabs block to carry the badge guards")
    # 4d. #158 GUARDS PARITY — the standalone-snippet export must carry the SAME guards.
    #     Before #158 it did not: theme_block() folded them into canon.css while
    #     snippet_theme_css() still emitted the PRE-GUARD projection, so every showroom
    #     pane and Open-↗ document rendered the mono default the guard exists to refuse.
    #     Driven on the REAL manifests, not a fixture [[green-tests-cannot-see-scope]].
    mans = dict(snippet_manifests())
    for t in themes.values():
        for slug, g in (t.get("guards") or {}).items():
            if slug not in mans:
                continue
            snip = snippet_theme_css(mans[slug], slug)
            for v, n in (g.get("declarations") or {}).items():
                if f"{v}: {n['value']};" not in snip:
                    fails.append(f'{t["key"]}: guard {v} for {slug} missing from snippet_theme_css')
            for r in (g.get("rules") or []):
                sel = r["selector"]
                sel = sel[len(f".cn-{slug} "):] if sel.startswith(f".cn-{slug} ") else sel
                if f'[data-apollo-theme="{t["attr"]}"] {sel}{{{r["body"]}}}' not in snip:
                    fails.append(f'{t["key"]}: guard rule {sel} missing from snippet_theme_css')
            if snippet_theme_css(mans[slug]) == snip:
                fails.append(f'{t["key"]}: snippet guards for {slug} are a NO-OP '
                             f"(slug-less call emits the same CSS — the guard is not reaching the doc)")
    # 5. idempotency
    if build_block()[0] != block:
        fails.append("generator is not deterministic")
    return fails

# ---------------------------------------------------------------- main
def main():
    if "--selftest" in sys.argv:
        fails = selftest()
        if fails:
            print("gen_theme_cascade SELFTEST FAIL:")
            [print("  X " + f) for f in fails]
            sys.exit(1)
        print("gen_theme_cascade selftest OK")
        return
    block, n_paths, n_comp = build_block()
    css = open(CANON).read()
    if START in css and END in css:
        new = css[:css.index(START)] + block + css[css.index(END) + len(END):]
    else:
        new = css.rstrip("\n") + "\n\n\n" + block + "\n"
    if "--check" in sys.argv:
        if new != css:
            print("gen_theme_cascade --check: canon.css AUTO-THEMES block is OUT OF SYNC "
                  "with tokens/themes/*.json (+ manifests). Run: python3 knowledge/canon/gen_theme_cascade.py")
            sys.exit(1)
        print(f"gen_theme_cascade --check OK — {n_paths} override path(s), "
              f"{n_comp} component projection(s) in sync.")
        return
    if new != css:
        open(CANON, "w").write(new)
        print(f"gen_theme_cascade: wrote AUTO-THEMES block — {n_paths} override path(s), "
              f"{n_comp} component projection(s).")
    else:
        print("gen_theme_cascade: no change (in sync).")

if __name__ == "__main__":
    main()
