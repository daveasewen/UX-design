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
# s219-D5 (Q3): the canon generators SHIP with the designer pack, and a designer who
# reaches for one is warned first. NO-OP IN THIS REPO — the guard looks for the pack's
# own _MANIFEST.json marker, which only an unzipped pack has. Same bytes both sides.
from _helpgate import pack_gate as _pack_gate; _pack_gate(__file__, name=__name__, what='the theme cascade')
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
    if path.startswith(("border-radius/", "border-width/", "breakpoint/", "layout/", "focus-ring/",
                        "target/", "size/")):
        # s202-D1 (#202): size/segmented-control/* is minted in the BASE layout store (mono is the
        # base theme), so the three square themes resolve the segmented dimensions Console tuned.
        return _store("layout.json")
    if path.startswith("padding/") or path.startswith("gap/"):
        # s202-D1 (#202): padding/segmented-control/* lives in the base spacing store. Without this
        # route base_value() would look in semantic-colour.json and KeyError.
        return _store("spacing.json")
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
        # `columns` mirrors gen_canon_tokens.UNITLESS (#217): a track count is not a length.
        # No theme overrides a column count today, so this is a no-op on the emitted CSS —
        # it is here so the two formatters cannot disagree the first time one does.
        if path.startswith("motion/press/") or path.rsplit("/", 1)[-1] in ("press-travel", "press-darken", "alpha", "columns"):
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
                 "attrAliases": list(t.get("attrAliases") or []),
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

def theme_attrs(theme):
    """Every attribute value this theme answers to — the canonical one FIRST.

    s227-D8(a), the W5 SAFE PATH. Designers say "Common"; the code key is `legacy`, and
    every place the two names meet has carried a parenthetical to reconcile them. The full
    rename is its own lane (s227-D8(c), post-Sept-1) because canon keys its whole cascade on
    `[data-apollo-theme="legacy"]` — swapping the key would strip the theme off every page a
    designer has already saved, and off every page in the shipped pack, the moment canon
    updated. An ALIAS breaks nothing: both keys are emitted, the old one first and unchanged,
    so existing pages keep resolving and new work can use the name Dave actually says.
    Declared in tokens/themes/_themes.json as `attrAliases`, so this is a registry fact and
    not a special case buried in an emitter."""
    return [theme["attr"]] + list(theme.get("attrAliases") or [])


def sel_group(theme, *tails):
    """A selector LIST covering every alias × every tail. `tails` are the strings that follow
    the attribute selector, e.g. ('', ' .cn-button') or ('[data-theme="dark"] .cn-x',
    ' [data-theme="dark"] .cn-x'). Aliases multiply the list, they never replace an entry —
    the canonical selector is always present, verbatim, and always first."""
    out = []
    for tail in tails:
        for key in theme_attrs(theme):
            out.append('[data-apollo-theme="%s"]%s' % (key, tail))
    return ",\n".join(out)


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
    lines.append(sel_group(theme, "") + "{")
    lines.append(_decls(root_light, "light"))
    lines.append("}")
    if root_dark:
        lines.append(sel_group(theme, '[data-theme="dark"]', ' [data-theme="dark"]') + "{")
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
        lines.append(sel_group(theme, " " + sel) + "{")
        lines.append(_decls(hits, "light", comments=comments))
        lines += tail_light
        lines.append("}")
        for r in (g.get("rules") or []):
            lines += _comment_lines(r["$note"], "")
            lines.append(sel_group(theme, " " + r["selector"]) + "{" + r["body"] + "}")
        lines.append(sel_group(theme, '[data-theme="dark"] ' + sel,
                               ' [data-theme="dark"] ' + sel) + "{")
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
        css.append(sel_group(t, ' [data-theme="light"]', '[data-theme="light"]') + "{")
        css.append(_decls(hits, "light", comments=comments))
        css += tail_light
        css.append("}")
        for r in (g.get("rules") or []):
            css += _comment_lines(r["$note"], "")
            sel = r["selector"]
            if slug and sel.startswith(f".cn-{slug} "):
                sel = sel[len(f".cn-{slug} "):]          # the snippet doc IS the component
            css.append(sel_group(t, " " + sel) + "{" + r["body"] + "}")
        css.append(sel_group(t, ' [data-theme="dark"]', '[data-theme="dark"]') + "{")
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
    # step/complete: THE ASSERTION FOLLOWS ITS SUBJECT, TWICE.
    #   s175-D1 moved the override from progress/complete to step/complete (values unchanged) and
    #   this clause asserted supercharge light == "#B92F1E".
    #   s176 (WORKING, Dave's word, awaiting his eye) moved it again: step/complete now ALIASES
    #   rag/success — the success-ROUNDEL chain — and every theme but Legacy inherits it wholesale.
    #   Dave: "they can just inherit then wholesale. Except Legacy". So the SUPERCHARGE OVERRIDE WAS
    #   REMOVED, and #B92F1E/#CC4333 are retired (provenance preserved in the base token's $note).
    # Assert VALUES, not the absence: these dicts are alias-expanded, so an inherited alias still
    # resolves to a hex here — the inheritance is checkable, and a stray re-declared override would
    # show up as a value mismatch. Each theme must equal ITS OWN rag/success, not a hard-coded hex
    # for the other theme, so a palette move cannot pass by coincidence (a token NAME is not an
    # ADDRESS — the point of asserting the CHAIN and not the literal).
    for mode in ("light", "dark"):
        if base_value("step/complete", mode) != base_value("rag/success", mode):
            fails.append(f"base step/complete {mode} must inherit rag/success (the roundel chain, s176)")
        if base_value("step/complete", mode) != "#66CC8D":
            fails.append(f"base step/complete {mode} != #66CC8D (mono success roundel, s176)")
    # …AND ASSERT THE EMITTED CHAIN, NOT ONLY THE VALUE. base_value() reads $value; the CSS that
    # actually paints is emitted from $alias by gen_canon_tokens (a semantic-aliased token emits the
    # var() reference, not a baked hex). Those two can disagree silently — reverting the $alias to
    # the old ink pair leaves $value #66CC8D and every value clause above still passes. A green that
    # cannot fail is an assertion, so the reference itself is asserted in the built canon.css:
    # step/complete must carry the ROUNDEL'S OWN CHAIN, --step-complete -> var(--rag-success), which
    # is what makes "inherit wholesale" true per theme rather than a coincidence of hexes.
    try:
        _canon = open(CANON).read()
    except Exception as e:                      # fail LOUD and NAMED, never silently skip
        fails.append(f"selftest could not read canon.css to assert the step chain: {e}")
        _canon = ""
    if "--step-complete: var(--rag-success);" not in _canon:
        fails.append("canon.css must emit --step-complete: var(--rag-success) — the success-roundel "
                     "chain (s176). A baked hex here means the $alias was lost and the themes stopped inheriting.")
    # ⚠ DEFECT FIXED #176-refinement: the six clauses below were written INSIDE the `if ... not in
    # _canon:` branch above — i.e. they could only ever run when the chain assertion had ALREADY
    # failed — and they read `mode` after the earlier for-loop had ended, so they silently tested
    # one mode. A green that cannot fail is an assertion, not a test. They are dedented to module
    # flow and given their own loop over both modes.
    con = themes["apollo-console"]["overrides"]
    for mode in ("light", "dark"):
        if con.get("step/complete", {}).get(mode) != con.get("rag/success", {}).get(mode):
            fails.append(f"console step/complete {mode} must inherit its own rag/success (s176)")
        if con.get("step/complete", {}).get(mode) != "#5DAC7B":
            fails.append(f"console step/complete {mode} != #5DAC7B (s176)")
        if sc.get("step/complete", {}).get(mode) != sc.get("rag/success", {}).get(mode):
            fails.append(f"supercharge step/complete {mode} must inherit its own rag/success (s176)")
        if sc.get("step/complete", {}).get(mode) != "#5DAC7B":
            fails.append(f"supercharge step/complete {mode} != #5DAC7B (s176; retired #B92F1E/#CC4333)")
    # THE MARK. #176 refinement, Dave off the rendered page: "Apollo mono, in the same way as the
    # roundels, uses the dark ink colour for the glyphs." step/on-complete is minted for it. The
    # RETIRED policy, preserved: the mark KNOCKED TO THE PAGE (background/default, #FFFFFF light /
    # #1A1A1A dark). Assert the value AND the emitted var, because the snippet literal and the
    # store can disagree silently — the whole reason --step-complete painted nothing before #176.
    for mode in ("light", "dark"):
        if base_value("step/on-complete", mode) != "#1A1A1A":
            fails.append(f"base step/on-complete {mode} != #1A1A1A (s122-D2 mark camp, s176)")
    if "--step-on-complete: #1A1A1A;" not in _canon:
        fails.append("canon.css must emit --step-on-complete: #1A1A1A — the roundel mark ink (s176). "
                     "Missing means the token is minted but never painted.")
    if "--on-complete: var(--step-on-complete);" not in _canon:
        fails.append("the step components must BIND --on-complete to var(--step-on-complete) (s176); "
                     "a component-local literal would take the theme cascade out of the loop.")
    # NB these are EFFECTIVE overrides (alias-expanded), so "no declared override" does NOT show up
    # as absence — progress/complete now expands through the warm DNA tier. Assert the VALUE:
    # s175-D1 = the continuous-quantity bar is the theme's own ink, i.e. it tracks text/default.
    if sc.get("progress/complete", {}).get("light") != sc.get("text/default", {}).get("light"):
        fails.append("supercharge progress/complete must resolve to the theme ink (s175-D1)")
    # LEGACY IS THE ONE EXCEPTION AND MUST STAY ONE. Dave #175 made Legacy's step colour DEFINITE;
    # Dave #176 kept it definite and RE-VALUED it: "Except Legacy, it uses the red in light mode and
    # white in dark." PROVENANCE OF THE PREVIOUS ASSERTION, retired here not deleted: this clause
    # asserted "#DB0011" in BOTH modes (the R-D19 brand red, moved from progress/complete by s175-D1).
    # WHICH RED MATTERS: Dave said "the red", then "warning red", then corrected himself verbatim —
    # "Legacy error, sorry my mistake". So light is Legacy's ERROR red, asserted AGAINST ITS PALETTE
    # and not as a bare literal, and pinned to the literal too so a palette move is caught rather
    # than silently followed. Dark is the roundel policy's WHITE leg.
    # …AND THE SUBJECT MOVED A THIRD TIME. #176 refinement, Dave off the RENDERED v1 review page:
    # "Use the primary red for Legacy." A ruling made against the thing outranks one made against a
    # description, so light goes BACK to the primary/brand red. RETIRED ASSERTIONS, kept as trail,
    # not deleted: (a) s175-D1 asserted "#DB0011" both modes; (b) #176-chat asserted light ==
    # legacy rag/error == "#A8000B" — that clause is now WRONG and is replaced, deliberately.
    # Light is pinned to the theme's PRIMARY red by chain AND by literal; dark is the white leg,
    # which Dave did not revisit.
    if leg.get("step/complete", {}).get("light") != leg.get("button/primary/background/default", {}).get("light"):
        fails.append("legacy step/complete light must be the theme's PRIMARY red, not the error red (s176 refinement)")
    if leg.get("step/complete", {}).get("light") != "#DB0011":
        fails.append("legacy step/complete light != #DB0011 (Legacy PRIMARY red, s176 refinement; "
                     "NOT #A8000B — that was the withdrawn chat leg — and NOT #FFBB33)")
    if leg.get("step/complete", {}).get("dark") != "#FFFFFF":
        fails.append("legacy step/complete dark != #FFFFFF (roundel policy white leg, s176)")
    # LEGACY IS THE ONE THEME THAT MUST OVERRIDE THE MARK, because it is the one theme whose step
    # fill is not the success fill — the mark policy binds to the FILL, not the token name.
    # Light MATCHES Legacy's own roundel mark (marks/success == marks/error == #FFFFFF, s122-D5);
    # dark is a DECLARED EXCEPTION to #1A1A1A, flagged NOT-RULED, because Legacy's dark step fill
    # is itself #FFFFFF and an exact match renders a white tick on a white disc.
    if leg.get("step/on-complete", {}).get("light") != "#FFFFFF":
        fails.append("legacy step/on-complete light != #FFFFFF (its own roundel mark, s122-D5/s176)")
    if leg.get("step/on-complete", {}).get("dark") != "#1A1A1A":
        fails.append("legacy step/on-complete dark != #1A1A1A (declared exception vs the white dark "
                     "fill, s176 — NOT RULED by Dave, flagged for him)")
    if leg.get("step/on-complete", {}).get("dark") == leg.get("step/complete", {}).get("dark"):
        fails.append("legacy dark: the tick and its fill are the SAME colour — an invisible glyph. "
                     "Dave's doctrine: 'the label and the symbol must carry the contrast'.")
    # Legacy USED to declare nothing on progress/complete and fell through to the MONO ink #1A1A1A —
    # the fall-through class: a theme that MEANS a value must DECLARE it. s176 closes that: Legacy
    # declares its own ink pair. Assert the DECLARATION, not merely the effective value, because an
    # effective value cannot tell a declaration from an accident — that was the whole defect.
    for mode, ink in (("light", "#333333"), ("dark", "#FFFFFF")):
        got = (leg.get("progress/complete") or {}).get(mode)
        if got != ink:
            fails.append(f"legacy progress/complete {mode} must be DECLARED as the Legacy ink {ink}, got {got} (s176)")
    if leg.get("progress/complete", {}).get("light") != leg.get("text/default", {}).get("light"):
        fails.append("legacy progress/complete light must equal the theme's own body ink (Grey 8, col25-011)")
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
                if sel_group(t, " " + r["selector"]) + "{" + r["body"] + "}" not in block:
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
        if sel_group(themes[key], " .cn-tabs") + "{" not in block:
            fails.append(f"{key}: no .cn-tabs block to carry the badge guards")
    # 4c-alias. s227-D8(a) THE THEME-KEY ALIAS IS ADDITIVE — proven on the built CSS, in
    #     both directions. The whole safety argument for shipping an alias instead of the
    #     rename is "nothing existing breaks", and an alias that quietly REPLACED the old
    #     key would satisfy every other check in this file while breaking every saved page.
    # comments carry the canonical key too (each theme's own `/* ---- Label [attr] ---- */`
    # banner), and a comment is not a selector — count on the CSS only.
    block_sel_only = re.sub(r"/\*.*?\*/", "", block, flags=re.S)
    for t in themes.values():
        aliases = list(t.get("attrAliases") or [])
        if not aliases:
            continue
        canon_sel = '[data-apollo-theme="%s"]' % t["attr"]
        if canon_sel not in block:
            fails.append(f'{t["key"]}: the CANONICAL key {t["attr"]!r} vanished from the '
                         "cascade — an alias must ADD a key, never replace one")
        for al in aliases:
            alias_sel = '[data-apollo-theme="%s"]' % al
            if alias_sel not in block:
                fails.append(f'{t["key"]}: alias {al!r} is declared in _themes.json but '
                             "emits no selector — the alias is decoration")
            if block_sel_only.count(alias_sel) != block_sel_only.count(canon_sel):
                fails.append(
                    f'{t["key"]}: alias {al!r} appears {block_sel_only.count(alias_sel)} '
                    f'time(s) against {block_sel_only.count(canon_sel)} for {t["attr"]!r} — '
                    "every rule the "
                    "canonical key reaches must be reachable by the alias too, or a page "
                    "using the new name renders half-themed")
        # and the canonical selector must still come FIRST in its own group, so a reader
        # (and every literal grep in the repo) still finds the shape it has always found
        if not block.count(canon_sel + ",\n" + '[data-apollo-theme="%s"]' % aliases[0]):
            fails.append(f'{t["key"]}: the canonical key is not first in the selector group')
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
                if sel_group(t, " " + sel) + "{" + r["body"] + "}" not in snip:
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
