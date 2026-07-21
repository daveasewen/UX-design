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
import json, os, re, sys, glob

HERE   = os.path.dirname(os.path.abspath(__file__))
KNOW   = os.path.dirname(HERE)
TOK    = os.path.join(KNOW, "tokens")
SNIP   = os.path.join(KNOW, "snippets")
CANON  = os.path.join(HERE, "canon.css")
START  = "/* ===== AUTO-THEMES START ===== */"
END    = "/* ===== AUTO-THEMES END ===== */"
MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)
MODES  = ("light", "dark")

# ---------------------------------------------------------------- token stores
_STORES = {}
def _store(fname):
    if fname not in _STORES:
        _STORES[fname] = json.load(open(os.path.join(TOK, fname)))
    return _STORES[fname]

def _store_for(path):
    if path.startswith("color/"):
        return _store("colour.json")
    if path.startswith(("border-radius/", "border-width/", "breakpoint/", "layout/", "focus-ring/")):
        return _store("layout.json")
    return _store("semantic-colour.json")

def base_value(path, mode):
    """Resolve a token path + mode from the BASE (Mono) stores. Fail loud."""
    node = _store_for(path)
    for key in path.split("/"):
        node = node[key]                      # KeyError = fail loud in caller
    if mode in node and isinstance(node[mode], dict) and "$value" in node[mode]:
        return node[mode]["$value"]
    if "$value" in node:
        return node["$value"]
    raise KeyError(f"{path} has no '{mode}' value in base store")

# ---------------------------------------------------------------- themes
def normalize(seg):
    return re.sub(r"[^a-z0-9]+", "-", str(seg).lower()).strip("-")

def var_name(path):
    return "--" + "-".join(normalize(s) for s in path.split("/"))

def css_value(path, val):
    """Format an override $value for CSS. Numbers are px except 0 (matches
    gen_canon_tokens fmt_value for the layout namespace)."""
    if isinstance(val, (int, float)):
        return "0" if val == 0 else f"{val}px"
    return str(val)

def load_themes():
    """Registry -> ordered list of {key, attr, label, status, overrides} where
    overrides = {path: {'light': cssval, 'dark': cssval} | {'modeless': cssval}}.
    Base theme (Mono) carries no overrides. Null override values (ADR-0010
    declared-but-unset) are skipped: declared, no emission."""
    reg = json.load(open(os.path.join(TOK, "themes", "_themes.json")))
    out = []
    for key, t in sorted(reg["themes"].items(), key=lambda kv: kv[1].get("order", 99)):
        entry = {"key": key, "attr": t.get("attr") or key.replace("apollo-", ""),
                 "label": t.get("label", key), "status": t.get("status"), "overrides": {}}
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
                elif "$value" in node:
                    entry["overrides"][path] = {"modeless": css_value(path, node["$value"])}
        out.append(entry)
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
def _decls(pairs, mode, indent="  "):
    return "\n".join(f"{indent}{v}: {vals[mode]};" for v, vals in sorted(pairs.items()))

def theme_block(theme, manifests):
    """Full canon.css cascade for one theme ('' for the base theme)."""
    ov = theme["overrides"]
    if not ov:
        return ""
    a = theme["attr"]
    lines = [f'/* ---- {theme["label"]}  [data-apollo-theme="{a}"]  '
             f'({len(ov)} override path(s), {theme["key"]}.overrides) ---- */']
    # ROOT tier
    root_light, root_dark = {}, {}
    for path, vals in sorted(ov.items()):
        vn = var_name(path)
        if "modeless" in vals:
            root_light[vn] = {"light": vals["modeless"]}
        else:
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
    for slug, varmap in manifests:
        hits = component_overrides(varmap, theme)
        if not hits:
            continue
        sel = f".cn-{slug}"
        lines.append(f'[data-apollo-theme="{a}"] {sel}{{')
        lines.append(_decls(hits, "light"))
        lines.append("}")
        lines.append(f'[data-apollo-theme="{a}"][data-theme="dark"] {sel},')
        lines.append(f'[data-apollo-theme="{a}"] [data-theme="dark"] {sel}{{')
        lines.append(_decls(hits, "dark"))
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
def snippet_theme_css(manifest_vars):
    """The same override projection for ONE standalone snippet document (used by
    gen_showroom.py). Bare [data-theme] blocks live on <body>; the harness sets
    data-apollo-theme on <html>. Emits nothing for themes with no hits."""
    themes = load_themes()
    css = []
    for t in themes:
        hits = component_overrides(manifest_vars, t)
        if not hits:
            continue
        a = t["attr"]
        css.append(f'[data-apollo-theme="{a}"] [data-theme="light"],')
        css.append(f'[data-apollo-theme="{a}"][data-theme="light"]{{')
        css.append(_decls(hits, "light"))
        css.append("}")
        css.append(f'[data-apollo-theme="{a}"] [data-theme="dark"],')
        css.append(f'[data-apollo-theme="{a}"][data-theme="dark"]{{')
        css.append(_decls(hits, "dark"))
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
    # 4. the ruled facts: Legacy carries the CTA red; Console rounds; Supercharge = Mono
    if themes["apollo-legacy"]["overrides"].get("button/primary/background/default", {}).get("light") != "#DB0011":
        fails.append("legacy button/primary default light != #DB0011")
    cr = themes["apollo-console"]["overrides"].get("border-radius/default", {})
    if not cr or cr.get("modeless") in (None, "0"):
        fails.append("console border-radius/default must be a non-zero modeless value")
    if themes["apollo-supercharge"]["overrides"]:
        fails.append("supercharge must be an EMPTY override set (renders as Mono)")
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
