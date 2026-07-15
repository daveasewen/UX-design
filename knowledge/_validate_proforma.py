#!/usr/bin/env python3
"""PROMOTED pro-forma gate (the universal, MODE-AGNOSTIC rule subset) — runs inside
knowledge/_build_all.py so the pro-forma tranche files (a new surface upstream of the
snippets/components pipeline) are gated on every build, not just by hand.

Promotes the UNIVERSAL rules (hold in every mode): real-icons-only, no hardcoded colour
in component CSS, all icon refs resolve, icon-only buttons named. It ALSO strengthens the
hand check by verifying each manifest path resolves to a REAL asset file (closes the
"fabricated path data behind a real-looking manifest entry" hole `_check_proforma` left).

MODE rules (monochrome / near-black / colour=meaning / square corners) are deliberately
NOT here — they belong to the monochrome-base subset, not the promoted gate, because the
main pipeline also carries brand-mode components that legitimately re-add colour.

Discovers knowledge/_proforma/*.html files that declare a #icon-manifest (the pro-forma
signature) and gates each. Exit non-zero if any file fails. Writes _PROFORMA-GATE.md."""
import re, json, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROFORMA_DIR = os.path.join(HERE, "_proforma")
ICONS_ROOT = os.path.join(HERE, "assets", "icons")
SCAFFOLD_SELECTORS = ['.top', '.tgl', '.wctl', '.ctrls', '.wctl input']

def check_file(path):
    """Return (fails, warns, stats) for one pro-forma file. Mirrors _check_proforma.py
    (single-file dev tool) and adds the manifest-path-existence check."""
    html = open(path).read()
    fails, warns, stats = [], [], {}

    m = re.search(r"<style>(.*?)</style>", html, re.S)
    if not m:
        return (["no <style> block found — not a pro-forma surface?"], warns, stats)
    css = m.group(1)
    # strip theme token blocks + top-bar scaffold selectors (colour lives only there)
    css = re.sub(r'\[data-theme="(light|dark)"\]\{[^}]*\}', "", css)
    for sel in SCAFFOLD_SELECTORS:
        css = re.sub(re.escape(sel) + r'[^{]*\{[^}]*\}', "", css)
    # 1 — no hardcoded colour in component CSS (hex / rgb() / rgba())
    leaks = re.findall(r'#[0-9A-Fa-f]{3,8}\b|rgba?\([^)]*\)', css)
    if leaks:
        fails.append("hardcoded colour in component CSS: %s" % leaks[:12])
    stats['hardcode_leaks'] = len(leaks)

    # 2 — icons: symbols vs manifest (real) vs provisional flag
    mm = re.search(r'id="icon-manifest">(.*?)</script>', html, re.S)
    man = json.loads(mm.group(1)) if mm else {"icons": {}}
    real = set(man.get("icons", {}))
    syms = set(re.findall(r'<symbol id="([^"]+)"', html))
    prov = set(re.findall(r'<symbol id="([^"]+)"[^>]*data-provenance="provisional"', html))
    invented = [s for s in syms if s not in real and s not in prov]
    if invented:
        fails.append("INVENTED icon(s) not asset-backed and not flagged provisional: %s" % invented)
    stats['real_icons'] = len(real); stats['provisional'] = sorted(prov)

    # 3 — every <use href="#x"> resolves to a symbol
    refs = set(re.findall(r'<use href="#([^"]+)"', html))
    unresolved = [r for r in refs if r not in syms]
    if unresolved:
        fails.append("unresolved icon refs: %s" % unresolved)
    stats['refs'] = "%d/%d" % (len(refs) - len(unresolved), len(refs))

    # 4 — icon-only buttons carry an accessible name
    for btn in re.findall(r'<button[^>]*class="ib[^"]*"[^>]*>', html):
        if 'aria-label' not in btn:
            fails.append("icon button with no aria-label: %s" % btn[:70])

    # 5 (STRENGTHENED) — every manifest path resolves to a REAL asset file
    missing = []
    if os.path.isdir(ICONS_ROOT):
        for sid, rel in man.get("icons", {}).items():
            if sid in prov:
                continue
            if not os.path.isfile(os.path.join(ICONS_ROOT, rel)):
                missing.append("%s -> %s" % (sid, rel))
        if missing:
            fails.append("manifest path(s) with no real asset file: %s" % missing)
        stats['asset_paths'] = "%d/%d real" % (len(man.get("icons", {})) - len(missing), len(man.get("icons", {})))
    else:
        warns.append("assets dir not found (%s) — skipped path-existence check" % ICONS_ROOT)
        stats['asset_paths'] = "skipped"
    return (fails, warns, stats)

def main():
    files = sorted(f for f in glob.glob(os.path.join(PROFORMA_DIR, "*.html"))
                   if 'id="icon-manifest"' in open(f).read())
    lines = ["# Pro-forma universal gate — report", ""]
    if not files:
        lines.append("No pro-forma tranche files found (nothing to gate). PASS.")
        open(os.path.join(HERE, "_PROFORMA-GATE.md"), "w").write("\n".join(lines) + "\n")
        print("pro-forma gate: no tranche files found — PASS")
        return 0
    any_fail = False
    for path in files:
        name = os.path.relpath(path, HERE)
        fails, warns, stats = check_file(path)
        status = "PASS" if not fails else "FAIL"
        if fails:
            any_fail = True
        print(f"  [{status}] {name}  ({stats})")
        lines.append(f"## {'✓' if not fails else '✗'} {name} — {status}")
        lines.append(f"- stats: {stats}")
        for w in warns:
            lines.append(f"- ⚠ {w}")
        for f in fails:
            print("     -", f)
            lines.append(f"- ✗ {f}")
        lines.append("")
    lines.append("---")
    lines.append("Universal rules gated: real-icons-only · no-hardcode-colour · refs-resolve · icon-buttons-named · manifest-paths-real.")
    lines.append("Mode rules (monochrome/near-black/colour=meaning/square) are NOT gated here — they are the monochrome-base subset (see _proforma/_PROFORMA-RULES.md).")
    open(os.path.join(HERE, "_PROFORMA-GATE.md"), "w").write("\n".join(lines) + "\n")
    if any_fail:
        print("\n❌ pro-forma universal gate FAILED — see knowledge/_PROFORMA-GATE.md")
        return 1
    print(f"\n✅ pro-forma universal gate passed ({len(files)} tranche file(s)).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
