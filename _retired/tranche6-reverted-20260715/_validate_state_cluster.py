#!/usr/bin/env python3
"""Pro-forma STATE-CLUSTER gate (DEF-001) — enforces _PROFORMA-RULES.md rule 11: every
interactive atom in the shared cluster (.btn, .card-link, plus a brightness check on .ib)
binds to the ONE canonical Button scale-physics — width-derived var(--hs)/var(--ps) set by
sizeScale() JS, brightness(.85) on press — never a bespoke/flat/variant-only hover or a
different press-brightness. This is the recurring bug tracked as DEF-001 in
knowledge/_PROFORMA-DEFECTS.md (the original T1/T4 scaffold bug: hover-grow only on
.btn.pri at a flat 2px, and .btn:active at brightness(.94) instead of .85).

Mirrors the idiom of _validate_proforma.py: auto-discover knowledge/_proforma/*.html files
that carry an #icon-manifest, check the COMPONENT <style> block of each, print per-file
PASS/FAIL, write knowledge/_STATE-CLUSTER-GATE.md, sys.exit(1) if any fail.

DOES NOT flag .ib/.av/.chip-x/.pb-action literal scale() values — those are approved
constant-px pops. ONLY the brightness on .ib:active and the .btn/.card-link canonical
var(--hs)/var(--ps) bindings are gated here.
"""
import re, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROFORMA_DIR = os.path.join(HERE, "_proforma")

RULE_RE = re.compile(r'([^{}]+)\{([^}]*)\}', re.S)

# A "base" selector is exactly the bare atom + pseudo-class (no extra class/attr qualifier).
BASE_HOVER_RE = re.compile(r'^\.(btn|card-link)(:hover)$')
BASE_ACTIVE_RE = re.compile(r'^\.(btn|card-link)(:active)$')
IB_ACTIVE_RE = re.compile(r'^\.ib(:active)$')
# A "variant" selector carries an extra class qualifier before the pseudo-class, e.g. .btn.pri:hover
VARIANT_HOVER_RE = re.compile(r'^\.btn\.[\w-]+:hover$')

TRANSFORM_RE = re.compile(r'transform\s*:\s*([^;]+)')
BRIGHTNESS_RE = re.compile(r'filter\s*:\s*[^;]*brightness\(\s*([^)]+?)\s*\)')

def parse_rules(css):
    """Split a CSS block into (individual_selector, declaration, raw_selector_group) triples."""
    out = []
    for m in RULE_RE.finditer(css):
        sel_group, decl = m.group(1), m.group(2)
        for sel in sel_group.split(','):
            out.append((sel.strip(), decl.strip(), sel_group.strip()))
    return out

def is_literal_scale(transform_val):
    """True if the transform value contains a scale(...) call that is NOT bound to
    var(--hs...) or var(--ps...) — i.e. a bespoke/flat literal (number or calc())."""
    for call in re.findall(r'scale\(([^)]*)\)', transform_val):
        if 'var(--hs' not in call and 'var(--ps' not in call:
            return True
    return False

def has_scale_call(transform_val):
    return 'scale(' in transform_val

def has_var_hs(transform_val):
    return bool(re.search(r'scale\([^)]*var\(--hs', transform_val))

def has_var_ps(transform_val):
    return bool(re.search(r'scale\([^)]*var\(--ps', transform_val))

def check_file(path):
    """Return (fails, warns, stats) for one pro-forma file."""
    html = open(path).read()
    fails, warns, stats = [], [], {}

    m = re.search(r"<style>(.*?)</style>", html, re.S)
    if not m:
        return (["no <style> block found — not a pro-forma surface?"], warns, stats)
    css = m.group(1)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)  # strip CSS comments so they don't leak into selectors

    rules = parse_rules(css)
    has_btn = bool(re.search(r'(?<![\w-])\.btn(?![\w-])', css))
    stats['btn_present'] = has_btn

    # ---- base .btn:hover (check 1 + gathers for check 2) ----
    base_hover_rules = [(sel, decl, raw) for sel, decl, raw in rules if BASE_HOVER_RE.match(sel) and sel.startswith('.btn')]
    base_hover_var_ok = False
    for sel, decl, raw in base_hover_rules:
        tm = TRANSFORM_RE.search(decl)
        if tm:
            tval = tm.group(1)
            if has_scale_call(tval):
                if is_literal_scale(tval):
                    fails.append(
                        "DEF-001 (1): base .btn:hover has a literal/bespoke transform:scale() "
                        "instead of scale(var(--hs...)) — %s{%s}" % (raw, decl))
                elif has_var_hs(tval):
                    base_hover_var_ok = True
    stats['btn_hover_binds_hs'] = base_hover_var_ok

    # ---- check 2: hover-grow only on a variant, no canonical base hover ----
    if not base_hover_var_ok:
        variant_hover_scale = [(sel, decl, raw) for sel, decl, raw in rules
                                if VARIANT_HOVER_RE.match(sel) and TRANSFORM_RE.search(decl)
                                and has_scale_call(TRANSFORM_RE.search(decl).group(1))]
        for sel, decl, raw in variant_hover_scale:
            fails.append(
                "DEF-001 (2): hover-grow only on variant '%s' (no canonical base .btn:hover{scale(var(--hs...))}) "
                "— %s{%s}" % (sel, raw, decl))

    # ---- check 3: .btn:active / .card-link:active brightness + scale binding ----
    active_ok = {'.btn': False, '.card-link': False}
    active_rules = [(sel, decl, raw) for sel, decl, raw in rules if BASE_ACTIVE_RE.match(sel)]
    for sel, decl, raw in active_rules:
        atom = sel.split(':')[0]
        bm = BRIGHTNESS_RE.search(decl)
        ok_brightness = False
        if bm:
            val = bm.group(1).strip()
            if val not in ('.85', '0.85'):
                fails.append(
                    "DEF-001 (3): %s uses filter:brightness(%s) — must be .85 — %s{%s}" % (sel, val, raw, decl))
            else:
                ok_brightness = True
        else:
            fails.append("DEF-001 (3): %s has no filter:brightness(.85) — %s{%s}" % (sel, raw, decl))
        tm = TRANSFORM_RE.search(decl)
        ok_scale = False
        if tm:
            tval = tm.group(1)
            if has_scale_call(tval):
                if is_literal_scale(tval):
                    fails.append(
                        "DEF-001 (3): %s transform:scale() is a literal, not var(--ps...) — %s{%s}" % (sel, raw, decl))
                elif has_var_ps(tval):
                    ok_scale = True
        else:
            fails.append("DEF-001 (3): %s has no transform:scale(var(--ps...)) — %s{%s}" % (sel, raw, decl))
        if atom in active_ok:
            active_ok[atom] = ok_brightness and ok_scale
    stats['btn_active_binds_ps_085'] = active_ok['.btn']
    if any(sel.startswith('.card-link') for sel, _, _ in rules):
        stats['card_link_active_binds_ps_085'] = active_ok['.card-link']

    # ---- check 4: .ib:active brightness (if present) ----
    ib_active_rules = [(sel, decl, raw) for sel, decl, raw in rules if IB_ACTIVE_RE.match(sel)]
    if ib_active_rules:
        for sel, decl, raw in ib_active_rules:
            bm = BRIGHTNESS_RE.search(decl)
            if bm:
                val = bm.group(1).strip()
                if val not in ('.85', '0.85'):
                    fails.append(
                        "DEF-001 (4): .ib:active uses filter:brightness(%s) — must be .85 — %s{%s}" % (val, raw, decl))
            else:
                fails.append("DEF-001 (4): .ib:active has no filter:brightness(.85) — %s{%s}" % (raw, decl))
        stats['ib_active_present'] = True
    else:
        stats['ib_active_present'] = False

    # ---- check 5: sizeScale() wired in a <script>, setting both --hs and --ps ----
    size_scale_ok = False
    for sm in re.finditer(r"<script>(.*?)</script>", html, re.S):
        body = sm.group(1)
        if 'sizeScale(' in body and "'--hs'" in body and "'--ps'" in body:
            size_scale_ok = True
            break
    if not size_scale_ok:
        fails.append("DEF-001 (5): sizeScale( not found in a <script>, or it does not set both --hs and --ps")
    stats['sizescale_wired'] = size_scale_ok

    return (fails, warns, stats)

def main():
    files = sorted(f for f in glob.glob(os.path.join(PROFORMA_DIR, "*.html"))
                   if 'id="icon-manifest"' in open(f).read())
    lines = ["# Pro-forma state-cluster gate (DEF-001) — report", "",
             "Enforces rule 11: `.btn`/`.card-link` bind the canonical `var(--hs)`/`var(--ps)` scale-physics",
             "(via `sizeScale()`), press = `brightness(.85)`; `.ib:active` also holds `brightness(.85)`.",
             "Approved literal `scale()` on `.ib`/`.av`/`.chip-x`/`.pb-action` (constant-px pops) is NOT flagged.",
             ""]
    if not files:
        lines.append("No pro-forma tranche files found (nothing to gate). PASS.")
        open(os.path.join(HERE, "_STATE-CLUSTER-GATE.md"), "w").write("\n".join(lines) + "\n")
        print("state-cluster gate: no tranche files found — PASS")
        return 0
    any_fail = False
    for path in files:
        name = os.path.relpath(path, HERE)
        fails, warns, stats = check_file(path)
        status = "PASS" if not fails else "FAIL"
        if fails:
            any_fail = True
        print(f"  [{status}] {name}  (.btn present={stats.get('btn_present')}, "
              f"hover binds --hs={stats.get('btn_hover_binds_hs')}, "
              f"active binds --ps+.85={stats.get('btn_active_binds_ps_085')}, "
              f"sizeScale wired={stats.get('sizescale_wired')})")
        lines.append(f"## {'✓' if not fails else '✗'} {name} — {status}")
        lines.append(f"- .btn present: {stats.get('btn_present')}")
        lines.append(f"- .btn:hover binds var(--hs): {stats.get('btn_hover_binds_hs')}")
        lines.append(f"- .btn:active binds var(--ps) + brightness(.85): {stats.get('btn_active_binds_ps_085')}")
        if 'card_link_active_binds_ps_085' in stats:
            lines.append(f"- .card-link:active binds var(--ps) + brightness(.85): {stats.get('card_link_active_binds_ps_085')}")
        lines.append(f"- .ib:active present: {stats.get('ib_active_present')}")
        lines.append(f"- sizeScale() wired (sets --hs and --ps): {stats.get('sizescale_wired')}")
        for w in warns:
            lines.append(f"- ⚠ {w}")
        for f in fails:
            print("     -", f)
            lines.append(f"- ✗ {f}")
        lines.append("")
    lines.append("---")
    lines.append("Floor: canonical Button scale-physics only — width-derived var(--hs)/var(--ps) via sizeScale(), "
                 "press brightness(.85). Bespoke/flat/variant-only hover or a different press-brightness = FAIL (DEF-001).")
    open(os.path.join(HERE, "_STATE-CLUSTER-GATE.md"), "w").write("\n".join(lines) + "\n")
    if any_fail:
        print("\n❌ pro-forma state-cluster gate FAILED (DEF-001) — see knowledge/_STATE-CLUSTER-GATE.md")
        return 1
    print(f"\n✅ pro-forma state-cluster gate passed ({len(files)} tranche file(s)).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
