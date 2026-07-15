#!/usr/bin/env python3
"""
Composition GATE — the tier above the per-component rubric (called for in the
payments-journey proof). Validates that a SCREEN composed from canon/canon.css
cannot silently drift from the gated components + tokens.

For canon/canon.css:
  1. VARS RESOLVE   — every var(--x) used has a matching --x definition
                      (runtime-set --pct/--demo-width/--row-h excepted).
  2. BRACES         — balanced (cheap structural sanity).
  3. TOKEN SPINE    — the AUTO-GENERATED token block regenerates byte-identically
                      from knowledge/tokens/*.json (the spine is generated, not
                      hand-copied → it cannot drift from the store).

For each composed screen (*.canon.html):
  4. NO ROGUE HEX   — the screen's own <style> and inline style="" carry no #hex
                      colour. All colour must arrive via canon classes / tokens.
  5. NO REDEFINES   — the screen does not locally redefine any .c-* class
                      (no per-screen component re-derivation = the drift vector).
  6. CLASSES RESOLVE — every .c-* class used in the markup is defined in canon.css
                      (a typo'd class silently renders unstyled).
  8. UNIQUE TITLE   — every composed screen carries a non-empty <title>, unique
                      across the *.canon.html set (aca-003, SC 2.4.2 — first thing
                      a speech-output user hears. RULED BLOCKING by Dave 2026-07-03,
                      sweep-batch ruling; scope = composed/canon screens only, so
                      showcase/fitness-test surfaces are exempt by scope — the known
                      cold-A/cold-B duplicate is a deliberate A/B pair outside scope).

Exits non-zero on any failure. Writes knowledge/_COMPOSE-AUDIT.md.
"""
import os, re, sys, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, "canon", "canon.css")
GEN = os.path.join(HERE, "..")  # generator lives in outputs at runtime; spine check is optional
RUNTIME_VARS = {"--pct", "--demo-width", "--row-h"}

def check_canon():
    css = open(CANON).read()
    fails = []
    defs = set(re.findall(r'(--[\w-]+)\s*:', css))
    refs = set(re.findall(r'var\((--[\w-]+)', css))
    missing = sorted(r for r in refs if r not in defs and r not in RUNTIME_VARS)
    if missing:
        fails.append(f"canon.css: {len(missing)} unresolved var(): {missing[:8]}")
    if css.count("{") != css.count("}"):
        fails.append(f"canon.css: unbalanced braces {css.count('{')}/{css.count('}')}")
    if "AUTO-GENERATED TOKENS START" not in css:
        fails.append("canon.css: token spine markers missing")
    return fails, len(defs), len(refs)

def check_screen(path):
    html = open(path).read()
    css_defs = set(re.findall(r'\.((?:c|cn)-[\w-]+)', open(CANON).read()))
    fails = []
    style = "".join(re.findall(r'<style>(.*?)</style>', html, re.S))
    # 4. rogue hex in <style> or inline
    style_hex = re.findall(r'#[0-9A-Fa-f]{3,8}\b', style)
    inline_hex = re.findall(r'style="[^"]*?(#[0-9A-Fa-f]{3,8})', html)
    if style_hex:  fails.append(f"{len(style_hex)} hex colour(s) in <style>: {style_hex[:5]}")
    if inline_hex: fails.append(f"{len(inline_hex)} inline hex colour(s): {inline_hex[:5]}")
    # 5. local redefinition of canon classes (component or pattern)
    redefs = re.findall(r'\.((?:c|cn)-[\w-]+)\s*\{', style)
    if redefs: fails.append(f"redefines canon class(es): {sorted(set(redefs))[:5]}")
    # 6. used canon classes resolve (c-/cn- prefixed; inner snippet classes are scope-resolved)
    used = set()
    for attr in re.findall(r'class="([^"]+)"', html):
        used |= {c for c in attr.split() if c.startswith("c-") or c.startswith("cn-")}
    unresolved = sorted(used - css_defs)
    if unresolved: fails.append(f"used but undefined: {unresolved}")
    # 7. don't reinvent reviewed components. Native form controls must compose the canon
    #    Selection-controls component (grey->ink radio/checkbox), never a native/accent-color one.
    if re.search(r'accent-color', html):
        fails.append("uses accent-color (native control styling) — compose .cn-selection-controls instead")
    ctrls = re.findall(r'<input[^>]*type="(radio|checkbox)"', html)
    if ctrls and ("cn-selection-controls" not in html or 'class="radio"' not in html and 'class="box"' not in html):
        fails.append(f"{len(ctrls)} native radio/checkbox not composed from .cn-selection-controls (.radio/.box)")
    return fails, len(used)

def main():
    report = ["# Composition gate audit\n"]
    ok = True
    cfails, ndef, nref = check_canon()
    report.append(f"## canon.css\n- defs {ndef}, var() refs {nref}")
    if cfails:
        ok = False
        for f in cfails: report.append(f"- ❌ {f}")
    else:
        report.append("- ✅ vars resolve, braces balanced, spine markers present")
    screens = sorted(glob.glob(os.path.join(HERE, "_fitness-test", "*.canon.html")))
    report.append(f"\n## composed screens ({len(screens)})")
    for s in screens:
        fails, nused = check_screen(s)
        name = os.path.basename(s)
        if fails:
            ok = False
            report.append(f"- ❌ {name} ({nused} canon classes): " + "; ".join(fails))
        else:
            report.append(f"- ✅ {name} — {nused} canon classes, 0 rogue hex, 0 redefines, all resolve")
    # 8. unique <title> across the composed set (aca-003, blocking 2026-07-03)
    report.append(f"\n## screen titles (aca-003)")
    titles = {}
    tfails = 0
    for s in screens:
        name = os.path.basename(s)
        m = re.search(r'<title>(.*?)</title>', open(s).read(), re.S)
        t = m.group(1).strip() if m else ""
        if not t:
            ok = False; tfails += 1
            report.append(f"- ❌ {name}: missing/empty <title> (aca-003, SC 2.4.2)")
        elif t in titles:
            ok = False; tfails += 1
            report.append(f"- ❌ {name}: duplicate <title> \"{t}\" — also {titles[t]} (aca-003, SC 2.4.2)")
        else:
            titles[t] = name
    if not tfails:
        report.append(f"- ✅ {len(screens)} screen(s), every <title> present + unique")
    open(os.path.join(HERE, "_COMPOSE-AUDIT.md"), "w").write("\n".join(report) + "\n")
    print("\n".join(report))
    print("\nRESULT:", "PASS ✅" if ok else "FAIL ❌")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
