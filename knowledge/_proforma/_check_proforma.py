#!/usr/bin/env python3
"""Enforcement gate for pro-forma tranche files. FAILS on: invented-but-unflagged icons,
hardcoded colour in component CSS, unresolved icon refs, icon-only buttons with no name."""
import re, json, sys
def check(path):
    html=open(path).read(); fails=[]; warns=[]
    # 1 — no hardcoded colour in COMPONENT css (strip theme token blocks + top-bar scaffold; sprite lives outside <style>)
    css=re.search(r"<style>(.*?)</style>",html,re.S).group(1)
    css=re.sub(r'\[data-theme="(light|dark)"\]\{[^}]*\}',"",css)
    for sel in ['.top','.tgl','.wctl','.ctrls','.wctl input']:
        css=re.sub(re.escape(sel)+r'[^{]*\{[^}]*\}',"",css)
    leaks=re.findall(r'#[0-9A-Fa-f]{3,8}\b|rgba?\([^)]*\)',css)
    if leaks: fails.append("hardcoded colour in component CSS: %s"%leaks)
    # 2 — icons: symbols vs manifest (real) vs provisional flag
    man=json.loads(re.search(r'id="icon-manifest">(.*?)</script>',html,re.S).group(1))
    real=set(man.get("icons",{}))
    syms=set(re.findall(r'<symbol id="([^"]+)"',html))
    prov=set(re.findall(r'<symbol id="([^"]+)"[^>]*data-provenance="provisional"',html))
    invented_unflagged=[s for s in syms if s not in real and s not in prov]
    if invented_unflagged: fails.append("INVENTED icon(s) not backed by an asset and not flagged provisional: %s"%invented_unflagged)
    # 3 — every <use href="#x"> resolves to a symbol
    refs=set(re.findall(r'<use href="#([^"]+)"',html))
    unresolved=[r for r in refs if r not in syms]
    if unresolved: fails.append("unresolved icon refs: %s"%unresolved)
    # 4 — icon-only buttons carry an accessible name
    for btn in re.findall(r'<button[^>]*class="ib[^"]*"[^>]*>',html):
        if 'aria-label' not in btn: fails.append("icon button with no aria-label: %s"%btn[:70])
    # report
    print("  real (asset-backed) icons :", len(real))
    print("  provisional icons         :", len(prov), (sorted(prov) if prov else "(none)"))
    print("  icon refs resolved        :", len(refs)-len(unresolved), "/", len(refs))
    print("  hardcode leaks            :", len(leaks))
    if fails:
        print("\n  RESULT: ✗ FAIL"); [print("   -",f) for f in fails]; return 1
    print("\n  RESULT: ✓ PASS — no invented/unflagged icons, no hardcoded colour, refs resolve, buttons named")
    return 0
sys.exit(check(sys.argv[1]))
