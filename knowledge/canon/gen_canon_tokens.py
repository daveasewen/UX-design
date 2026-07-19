#!/usr/bin/env python3
"""
Generate the AUTO-GENERATED TOKENS section of canon.css from knowledge/tokens/*.json.

Anti-drift principle: the token->CSS-var layer is GENERATED, never hand-copied.
Re-run any time tokens change. Only the block between the AUTO markers is touched,
so hand-authored component classes below the marker are preserved.

Var naming = token path with the mode leaf (light/dark) stripped, joined by '-'.
  semantic-colour.json  primary/background/hover/{light,dark} -> --primary-background-hover
  colour.json           color/red/60                          -> --color-red-60
Light values populate :root; dark values populate [data-theme="dark"].
"""
import json, os, sys, re

TOKENS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tokens")
CANON_CSS  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon.css")

# file -> (section label, var prefix). Prefix '' means use the token's own top keys.
FILES = [
    ("colour.json",          "Primitive colour palette",        ""),
    ("semantic-colour.json", "Semantic colour (light / dark)",  ""),
    ("typography.json",      "Typography",                      ""),
    ("spacing.json",         "Spacing (gap / padding)",         ""),
    ("layout.json",          "Layout",                          ""),
    ("elevation.json",       "Elevation",                       ""),
    ("motion.json",          "Motion (duration / easing)",      ""),
    ("icon-scale.json",      "Icon scale",                      ""),
]

MODE_LEAVES = {"light", "dark"}
FONT_STACK = '"Univers Next for HSBC", "Helvetica Neue", Arial, Helvetica, sans-serif'
UNITLESS = ("weight", "opacity", "z-index", "line-height-ratio")  # number tokens that take no px

def fmt_value(var, val, ttype):
    """Render a DTCG value as a CSS value string, by $type and path."""
    # DTCG alias reference {a.b.c} -> var(--a-b-c)
    if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
        return f"var(--{val[1:-1].replace('.', '-')})"
    if ttype == "cubicBezier" and isinstance(val, dict):
        return f"cubic-bezier({val['x1']}, {val['y1']}, {val['x2']}, {val['y2']})"
    if ttype == "cubicBezier" and isinstance(val, list):
        return f"cubic-bezier({', '.join(str(x) for x in val)})"
    if ttype == "string" and "font-family" in var:
        return FONT_STACK
    if ttype == "number" and isinstance(val, (int, float)):
        if val == 0:
            return "0"
        if any(k in var for k in UNITLESS) or "letter-spacing" in var:
            return str(val)
        return f"{val}px"            # font-size, line-height, spacing, blur, offsets, layout
    if isinstance(val, (list, dict)):
        return None                  # skip non-renderable composites ($type 'other')
    return str(val)

def walk(node, path, out):
    """Collect (var_name, mode_or_None, css_value) from a DTCG tree."""
    if isinstance(node, dict):
        # Three-tier reference: a token that $alias-references a SEMANTIC token (not a
        # primitive color/*) emits the var() chain, so canon.css carries the reference at
        # runtime instead of a baked hex. Primitive-aliased tokens keep emitting their $value.
        if "$alias" in node and ("light" in node or "dark" in node):
            var = "--" + "-".join(path)
            alias = node["$alias"] if isinstance(node.get("$alias"), dict) else {}
            for mode in ("light", "dark"):
                m = node.get(mode)
                if not isinstance(m, dict):
                    continue
                tgt = alias.get(mode)
                if isinstance(tgt, str) and not tgt.startswith("color/"):
                    css = "var(--" + "-".join(normalize(s) for s in tgt.split("/")) + ")"
                else:
                    css = fmt_value(var, m.get("$value"), m.get("$type"))
                if css is not None:
                    out.append((var, mode, css))
            return
        if "$value" in node:
            segs = path[:]
            mode = None
            if segs and segs[-1] in MODE_LEAVES:
                mode = segs[-1]
                segs = segs[:-1]
            var = "--" + "-".join(segs)
            css = fmt_value(var, node["$value"], node.get("$type"))
            if css is not None:
                out.append((var, mode, css))
            return
        for k, v in node.items():
            if k.startswith("$"):
                continue
            walk(v, path + [normalize(k)], out)

def normalize(k):
    return re.sub(r"[^a-z0-9]+", "-", str(k).lower()).strip("-")

def collect(fname):
    d = json.load(open(os.path.join(TOKENS_DIR, fname)))
    out = []
    for k, v in d.items():
        if k.startswith("$"):
            continue
        walk(v, [normalize(k)], out)
    return out

def main():
    root_lines, dark_lines = [], []
    seen_root, seen_dark = {}, {}
    summary = []
    for fname, label, _ in FILES:
        toks = collect(fname)
        root_lines.append(f"\n  /* ---- {label}  ({fname}) ---- */")
        nroot = ndark = 0
        for var, mode, val in toks:
            decl = f"  {var}: {val};"
            if mode == "dark":
                if seen_dark.get(var) != val:
                    dark_lines.append(decl)
                    seen_dark[var] = val
                    ndark += 1
            else:  # light or modeless -> :root
                if var not in seen_root:
                    root_lines.append(decl)
                    seen_root[var] = val
                    nroot += 1
        summary.append(f"  {fname:24s} -> {nroot:3d} root vars, {ndark:3d} dark overrides")

    block = ["/* ===== AUTO-GENERATED TOKENS START =====",
             "   Generated from knowledge/tokens/*.json by gen_canon_tokens.py.",
             "   Do NOT hand-edit between the AUTO markers; re-run the generator instead. */",
             ":root {"]
    block += root_lines
    block.append("}")
    block.append("")
    block.append('[data-theme="dark"] {')
    block += dark_lines
    block.append("}")
    block.append("/* ===== AUTO-GENERATED TOKENS END ===== */")
    token_css = "\n".join(block)

    os.makedirs(os.path.dirname(CANON_CSS), exist_ok=True)
    existing = open(CANON_CSS).read() if os.path.exists(CANON_CSS) else ""
    if "AUTO-GENERATED TOKENS START" in existing and "AUTO-GENERATED TOKENS END" in existing:
        new = re.sub(r"/\* ===== AUTO-GENERATED TOKENS START =====.*?AUTO-GENERATED TOKENS END ===== \*/",
                     token_css, existing, flags=re.S)
    else:
        new = token_css + "\n\n" + existing
    open(CANON_CSS, "w").write(new)

    print("Generated token layer:")
    print("\n".join(summary))
    print(f"\n  TOTAL: {len(seen_root)} root vars, {len(seen_dark)} dark overrides")
    print(f"  Wrote {CANON_CSS}")

if __name__ == "__main__":
    main()
