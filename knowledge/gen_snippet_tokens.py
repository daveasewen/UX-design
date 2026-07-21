#!/usr/bin/env python3
"""
gen_snippet_tokens.py — project the semantic tokens INTO each snippet's theme blocks.

Anti-drift principle (Dave 2026-07-19: "the snippets need to be styled by the tokens").
Each snippet's `[data-theme="light"]{...}` / `[data-theme="dark"]{...}` var values are
GENERATED from knowledge/tokens/*.json via the snippet's OWN `#token-manifest`
(var -> token path). They are never hand-typed, so they cannot drift. Re-run after any
token change; the _validate_snippets.py fidelity gate then passes BY CONSTRUCTION.

This is the generator side of the guard: _validate_snippets.py checks the invariant,
this script establishes it.

ALSO projects knowledge/_proforma/Tranche-1..8-interactive.html (2026-07-19 worker task,
notes/_BRIEF-tranche-tokenize-T1-T8.md). The tranches carry the same bare
`[data-theme="mode"]{ }` block shape and the same `#token-manifest` mechanism as
snippets, so `process()`/`selfcheck()` apply unchanged — only the file glob differs.
Scoped to Tranche-1..8 ONLY (bracket range, not a bare `*`) so a future Tranche-9 is not
silently swept in before it is ready. project_canon() stays snippet-only (tranches have
no `.cn-<slug>` canon.css block to project into).

Robust by design:
  * FAILS LOUD (exit non-zero) if a manifest token path does not resolve in the stores.
  * Respects `driftAllow` {var:[modes]} in the manifest — those declarations are an
    intentional, documented deviation and are left exactly as authored.
  * Rewrites ONLY the value after `--var:` inside a bare `[data-theme="mode"]{ }` block.
    Comments, ordering, spacing, and every non-manifest (local) var are preserved.
  * Idempotent — a second run makes zero changes.
  * Self-verifies after writing: every non-drift manifest var declared in a theme block
    must equal its resolved token, or the script exits non-zero.
  * `--check` verifies without writing (CI / pre-commit use).

Usage:  python3 knowledge/gen_snippet_tokens.py [--check] [--quiet]
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
TOK  = os.path.join(HERE, "tokens")
SNIP = os.path.join(HERE, "snippets")
PROFORMA = os.path.join(HERE, "_proforma")
CANON = os.path.join(HERE, "canon", "canon.css")
SPINE_END = "AUTO-GENERATED TOKENS END ===== */"
THEMES_START = "/* ===== AUTO-THEMES START ===== */"

_STORES = {}
def store(fname):
    if fname not in _STORES:
        _STORES[fname] = json.load(open(os.path.join(TOK, fname)))
    return _STORES[fname]

def _fmt(val):
    """CSS-format a resolved token value: numbers are px except 0 (matches
    gen_canon_tokens fmt_value for the layout namespace); strings pass through."""
    if isinstance(val, (int, float)):
        return "0" if val == 0 else f"{val}px"
    return val

def resolve(path, mode):
    """token path + mode -> resolved hex/value. Raises KeyError if unresolvable.
    Routes color/* to colour.json, the layout namespaces (border-radius/*, …) to
    layout.json (Phase-0 shape de-hardcode — snippets bind radius via manifest),
    everything else to semantic-colour.json."""
    if path.startswith("color/"):
        src = "colour.json"
    elif path.startswith(("border-radius/", "border-width/", "focus-ring/", "layout/", "breakpoint/")):
        src = "layout.json"
    else:
        src = "semantic-colour.json"
    node = store(src)
    for key in path.split("/"):
        node = node[key]                      # KeyError => caught by caller (fail loud)
    # leaf may be {light:{$value}, dark:{$value}} or a modeless {$value}
    if mode in node and isinstance(node[mode], dict) and "$value" in node[mode]:
        return _fmt(node[mode]["$value"])
    if "$value" in node:
        return _fmt(node["$value"])
    raise KeyError(f"{path} has no '{mode}' value")

MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)
# a BARE theme block: [data-theme="mode"]{ ... }  (no selector after the attribute)
def block_re(mode):
    return re.compile(r'(\[data-theme="' + mode + r'"\]\s*\{)([^}]*)(\})')

def var_sub(body, cssvar, newval):
    """Replace the value of --cssvar within a block body; preserve trailing comment/`;`.
    Returns (new_body, changed_bool, found_bool)."""
    pat = re.compile(r'(--' + re.escape(cssvar.lstrip('-')) + r'\s*:\s*)([^;]*?)(\s*;)')
    found = {"hit": False, "changed": False}
    def repl(m):
        found["hit"] = True
        if m.group(2).strip() != newval:
            found["changed"] = True
            return m.group(1) + newval + m.group(3)
        return m.group(0)
    new = pat.sub(repl, body, count=1)
    return new, found["changed"], found["hit"]

def process(path, write):
    html = open(path).read()
    name = os.path.basename(path)
    mm = MANIFEST_RE.search(html)
    if not mm:
        return {"name": name, "warn": ["no #token-manifest"], "changed": 0, "checks": 0, "fails": []}
    manifest = json.loads(mm.group(1))
    varmap = manifest.get("vars", {})
    drift  = manifest.get("driftAllow", {})
    warns, fails = [], []
    changed = checks = 0
    seen_anywhere = {v: False for v in varmap}

    for mode in ("light", "dark"):
        brx = block_re(mode)
        def block_repl(bm):
            nonlocal changed, checks
            head, body, tail = bm.group(1), bm.group(2), bm.group(3)
            for cssvar, tokenpath in varmap.items():
                if mode in drift.get(cssvar, []):
                    # intentional deviation: leave as authored, but note it's seen
                    if re.search(r'--' + re.escape(cssvar.lstrip('-')) + r'\s*:', body):
                        seen_anywhere[cssvar] = True
                    continue
                try:
                    val = resolve(tokenpath, mode)
                except KeyError as e:
                    fails.append(f"{cssvar} -> {tokenpath} ({mode}): UNRESOLVED {e}")
                    continue
                body, ch, hit = var_sub(body, cssvar, val)
                if hit:
                    seen_anywhere[cssvar] = True
                    checks += 1
                    if ch:
                        changed += 1
            return head + body + tail
        html = brx.sub(block_repl, html)

    for v, seen in seen_anywhere.items():
        if not seen:
            warns.append(f"manifest var {v} declared in no theme block")

    if write and changed:
        open(path, "w").write(html)
    return {"name": name, "warn": warns, "changed": changed, "checks": checks,
            "fails": fails, "html": html, "manifest": manifest}

def selfcheck(path, html, manifest):
    """After projection: every non-drift manifest var present in a theme block must
    equal its resolved token. Returns list of drift failures."""
    drift = manifest.get("driftAllow", {})
    out = []
    for mode in ("light", "dark"):
        bm = block_re(mode).search(html)
        if not bm:
            continue
        body = bm.group(2)
        for cssvar, tokenpath in manifest.get("vars", {}).items():
            if mode in drift.get(cssvar, []):
                continue
            m = re.search(r'--' + re.escape(cssvar.lstrip('-')) + r'\s*:\s*([^;]*?)\s*;', body)
            if not m:
                continue
            try:
                want = resolve(tokenpath, mode)
            except KeyError:
                out.append(f"{os.path.basename(path)}: {cssvar} {tokenpath} ({mode}) UNRESOLVED")
                continue
            if m.group(1).strip() != want:
                out.append(f"{os.path.basename(path)}: {cssvar} ({mode}) = {m.group(1).strip()} != token {want}")
    return out

def slug_of(fname):
    return re.sub(r'[^a-z0-9]+', '-', os.path.basename(fname).replace('.reference.html', '').lower()).strip('-')

def project_canon(write):
    """Project tokens into canon.css .cn-<slug> component blocks, driven by each
    snippet's manifest. Touches LITERAL hex declarations only — var(--token) refs
    are left to the AUTO spine. Never touches the spine (only the body after the
    marker). Returns (changed, fails)."""
    if not os.path.exists(CANON):
        return 0, ["canon.css not found"]
    css = open(CANON).read()
    i = css.find(SPINE_END)
    if i < 0:
        return 0, ["canon.css spine marker missing"]
    cut = i + len(SPINE_END)
    spine, body = css[:cut], css[cut:]
    # AUTO-THEMES fence (Phase 0, 2026-07-21): gen_theme_cascade.py re-projects the SAME
    # manifest vars inside [data-apollo-theme] blocks at THEME-OVERRIDE values. The bare
    # `.cn-<slug>{` in those selectors also matches this function's regex (optional-prefix),
    # so an unfenced run stomps Legacy red back to Mono ink — caught live 2026-07-21
    # (order-dependence bite: cascade --check failed after a projection re-run). Everything
    # from the AUTO-THEMES marker on is the cascade generator's output — never touch it.
    tstart = body.find(THEMES_START)
    themes_tail = ""
    if tstart >= 0:
        body, themes_tail = body[:tstart], body[tstart:]
    changed = 0
    for f in sorted(glob.glob(os.path.join(SNIP, "*.reference.html"))):
        mm = MANIFEST_RE.search(open(f).read())
        if not mm:
            continue
        manifest = json.loads(mm.group(1))
        varmap = manifest.get("vars", {}); drift = manifest.get("driftAllow", {})
        slug = slug_of(f)
        brx = re.compile(r'(\[data-theme="(?:dark|light)"\]\s*)?(\.cn-' + re.escape(slug) + r'\{)([^}]*)(\})')
        def repl(bm):
            nonlocal changed
            prefix, head, blk, tail = bm.group(1) or "", bm.group(2), bm.group(3), bm.group(4)
            mode = "dark" if "dark" in prefix else "light"
            for cssvar, token in varmap.items():
                if mode in drift.get(cssvar, []):
                    continue
                try:
                    val = resolve(token, mode)
                except KeyError:
                    continue
                pat = re.compile(r'(--' + re.escape(cssvar.lstrip('-')) + r'\s*:\s*)(#[0-9A-Fa-f]{3,8})(\s*;)')
                def r2(m2):
                    nonlocal changed
                    if m2.group(2).upper() != val.upper():
                        changed += 1
                        return m2.group(1) + val + m2.group(3)
                    return m2.group(0)
                blk = pat.sub(r2, blk)
            return prefix + head + blk + tail
        body = brx.sub(repl, body)
    if write and changed:
        open(CANON, "w").write(spine + body + themes_tail)
    return changed, []

def main():
    check_only = "--check" in sys.argv
    quiet = "--quiet" in sys.argv
    snip_files = sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))
    # bracket range, not a bare `Tranche-*` — deliberately enumerated so a stray
    # copy/backup file can never be swept in. Tranche-9 (secure entry) added by the
    # conductor 2026-07-19 once it landed with its own #token-manifest.
    tranche_files = sorted(glob.glob(os.path.join(PROFORMA, "Tranche-[1-9]-interactive.html")))
    files = snip_files + tranche_files
    tot_changed = tot_checks = 0
    all_fails, all_warns, drift_fails = [], [], []
    for f in files:
        r = process(f, write=not check_only)
        tot_changed += r["changed"]; tot_checks += r.get("checks", 0)
        for w in r["warn"]:  all_warns.append(f"{r['name']}: {w}")
        for x in r["fails"]: all_fails.append(f"{r['name']}: {x}")
        if "html" in r:
            drift_fails += selfcheck(f, r["html"], r["manifest"])
        if not quiet and r["changed"]:
            print(f"  {r['name']:32s} {r['changed']:3d} value(s) projected")

    canon_changed, canon_fails = project_canon(write=not check_only)
    all_fails += canon_fails

    print(f"\ngen_snippet_tokens: {tot_checks} manifest bindings across {len(snip_files)} snippets + "
          f"{len(tranche_files)} tranches; {tot_changed} value(s) {'would change' if check_only else 'projected'}; "
          f"{canon_changed} canon.css literal(s) {'would change' if check_only else 'projected'}.")
    if all_warns:
        print("WARNINGS:"); [print("  ! " + w) for w in all_warns]
    if all_fails:
        print("UNRESOLVED (fail):"); [print("  X " + x) for x in all_fails]
    if drift_fails:
        print("SELF-CHECK DRIFT (fail):"); [print("  X " + x) for x in drift_fails]
    if all_fails or drift_fails:
        sys.exit(1)
    if check_only and (tot_changed or canon_changed):
        print("--check: snippets/tranches/canon are OUT OF SYNC with tokens (run without --check).")
        sys.exit(1)
    print("OK — snippets + tranches + canon.css in sync with tokens.")

if __name__ == "__main__":
    main()
