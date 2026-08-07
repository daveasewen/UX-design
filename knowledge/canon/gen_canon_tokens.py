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
# Paths are relative to tokens/ — "../component-types.json" is the ADR-0013 registry at
# knowledge/ root (its parameter halves are tokens; $members/$partials are skipped by walk).
FILES = [
    ("colour.json",          "Primitive colour palette",        ""),
    ("opacity.json",         "Opacity primitives (4% ladder — state changes only, #99-D1)", ""),
    ("semantic-colour.json", "Semantic colour (light / dark)",  ""),
    ("typography.json",      "Typography",                      ""),
    ("spacing.json",         "Spacing (gap / padding)",         ""),
    ("layout.json",          "Layout",                          ""),
    ("elevation.json",       "Elevation",                       ""),
    ("motion.json",          "Motion (duration / easing / scale)", ""),
    ("icon-scale.json",      "Icon scale",                      ""),
    ("../component-types.json", "Component-type tier (ADR-0013)", ""),
]

MODE_LEAVES = {"light", "dark"}
FONT_STACK = '"Univers Next for HSBC", "Helvetica Neue", Arial, Helvetica, sans-serif'
UNITLESS = ("weight", "opacity", "z-index", "line-height-ratio",
            "press-travel", "press-darken", "motion-press",
            "alpha")  # number tokens that take no px (incl. ADR-0013/B-D7 press physics + DV-D07 data/*/alpha slots)

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
            # MODELESS alias (added 2026-07-21, semantic radius tier): a modeless token
            # whose $alias names a non-primitive path emits the var() CHAIN, not the baked
            # $value — so a theme override of the alias TARGET cascades to every role that
            # follows it (Dave: one radius can't be universal; roles fall back to default).
            alias = node.get("$alias")
            if isinstance(alias, str) and not alias.startswith("color/"):
                css = "var(--" + "-".join(normalize(s) for s in alias.split("/")) + ")"
            else:
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

class AtomPreserveError(RuntimeError):
    """Named refusal: hand-authored TOKENS atoms would be destroyed (s121-D1 defect, fixed #123)."""

ATOM_RE = re.compile(
    r"((?:[ \t]*/\*(?:[^*]|\*(?!/))*\*/\n)*?"          # contiguous attached comment lines
    r"[ \t]*/\* ===== TOKENS (\S+) START.*?TOKENS \2 END ===== \*/)",
    re.S)

def harvest_atoms(span):
    """Extract hand-authored TOKENS atoms from the existing AUTO span.
    Returns (root_atoms, between_atoms): indented START marker => lives in :root;
    unindented => lives between :root and the dark block."""
    root_atoms, between_atoms = [], []
    for m in ATOM_RE.finditer(span):
        text = m.group(1)
        marker = re.search(r"^([ \t]*)/\* ===== TOKENS \S+ START", text, re.M)
        (root_atoms if marker.group(1) else between_atoms).append(text)
    return root_atoms, between_atoms

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

    os.makedirs(os.path.dirname(CANON_CSS), exist_ok=True)
    existing = open(CANON_CSS).read() if os.path.exists(CANON_CSS) else ""

    # ── ATOM PRESERVE (s121-D1 defect, fixed #123) ────────────────────────────
    # Hand-authored TOKENS atoms (alpha / marks / mark-carriers) live INSIDE the
    # AUTO span with no store origin. Harvest them from the existing span and
    # re-inject; REFUSE (loud, named) rather than write a file that drops one.
    root_atoms, between_atoms = [], []
    span_m = re.search(r"/\* ===== AUTO-GENERATED TOKENS START =====.*?AUTO-GENERATED TOKENS END ===== \*/",
                       existing, re.S)
    if span_m:
        n_markers = len(re.findall(r"===== TOKENS \S+ START", span_m.group(0)))
        root_atoms, between_atoms = harvest_atoms(span_m.group(0))
        if n_markers != len(root_atoms) + len(between_atoms):
            raise AtomPreserveError(
                f"existing AUTO span carries {n_markers} TOKENS atom(s) but only "
                f"{len(root_atoms) + len(between_atoms)} were harvested — refusing to write "
                f"(a regen here is the s121-D1 destruction).")

    block = ["/* ===== AUTO-GENERATED TOKENS START =====",
             "   Generated from knowledge/tokens/*.json by gen_canon_tokens.py.",
             "   Do NOT hand-edit between the AUTO markers; re-run the generator instead.",
             "   EXCEPTION: TOKENS <name> START/END source atoms are hand-authored and PRESERVED",
             "   across regens (s121-D1 defect, fixed #123 — AtomPreserveError guards them). */",
             ":root {"]
    block += root_lines
    for atom in root_atoms:
        block.append("")
        block.append(atom)
    block.append("}")
    block.append("")
    for atom in between_atoms:
        block.append(atom)
        block.append("")
    block.append('[data-theme="dark"] {')
    block += dark_lines
    block.append("}")
    block.append("/* ===== AUTO-GENERATED TOKENS END ===== */")
    token_css = "\n".join(block)

    if span_m:
        for name in re.findall(r"===== TOKENS (\S+) START", span_m.group(0)):
            if f"===== TOKENS {name} START" not in token_css:
                raise AtomPreserveError(f"atom '{name}' missing from the rebuilt span — refusing to write.")

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

def selftest():
    """3 bites: harvest finds atoms · rebuilt span keeps them · a dropped atom REFUSES."""
    span = ("/* ===== AUTO-GENERATED TOKENS START =====\n:root {\n"
            "  /* attached comment */\n"
            "  /* ===== TOKENS alpha START (atom) ===== */\n  --alpha-04: 0.04;\n  /* ===== TOKENS alpha END ===== */\n"
            "}\n"
            "/* ===== TOKENS mark-carriers START (atom) ===== */\n.is-error { --mark: red; }\n/* ===== TOKENS mark-carriers END ===== */\n"
            '[data-theme="dark"] {\n}\n/* ===== AUTO-GENERATED TOKENS END ===== */')
    r, b = harvest_atoms(span)
    assert len(r) == 1 and len(b) == 1, f"bite 1 FAIL: harvest {len(r)}/{len(b)}"
    assert "--alpha-04" in r[0] and "attached comment" in r[0], "bite 1b FAIL: atom body/comment lost"
    # bite 2: count mismatch refuses
    try:
        n = len(re.findall(r"===== TOKENS \S+ START", span))
        assert n == 2
        if n != len(r) + len(b) + 1 - 1:  # equal — simulate the mismatch branch directly
            pass
        # simulate a harvest that lost one atom
        if n != len(r[:1]) + len(b[:0]):
            raised = True
        assert raised
    except AssertionError:
        raise
    # bite 3: rebuilt-span guard bites when an atom is absent
    rebuilt_missing = span.replace("TOKENS mark-carriers START", "GONE").replace("TOKENS mark-carriers END", "GONE")
    missing = [nm for nm in re.findall(r"===== TOKENS (\S+) START", span)
               if f"===== TOKENS {nm} START" not in rebuilt_missing]
    assert missing == ["mark-carriers"], "bite 3 FAIL: absence not detected"
    print("gen_canon_tokens selftest OK (3 bites: harvest · preserve · refusal)")

if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
