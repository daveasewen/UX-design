#!/usr/bin/env python3
"""
test_gates.py — the gate that gates the gates (bite-tests, made permanent).

WHY (ADR-0005 / review 2026-07-02): a gate that silently stops looking is
indistinguishable from a gate with nothing to report — both print green. The
state-contrast blind spot was exactly this failure class. This suite feeds every
blocking validator a deliberately-broken input and asserts the validator BITES
(non-zero exit + the expected complaint). If a gate swallows a defect it was
built to catch, THIS suite turns the build red.

Method: for each case, copy knowledge/ to a temp dir, apply one surgical
mutation, run one validator there, assert (exit != 0) and (marker in output).
A control case first asserts the pristine copy passes every static gate, so a
bite can never be confused with pre-existing breakage.

Zero dependencies (stdlib only), same as the validators themselves.

Run:  python3 knowledge/_tests/test_gates.py
Exits non-zero on any test failure.

NOT covered here (documented, deliberate):
  * _validate_state_contrast.py / _validate_screen.py --render — require a
    browser engine; run them via the render path where chromium is available.
    Their un-testedness in CI is a known gap, not a green light.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)                      # knowledge/
IGNORE = shutil.ignore_patterns("__pycache__", "_tests", ".DS_Store")

RESULTS = []


def fresh_copy(tmp_root, tag):
    dst = os.path.join(tmp_root, tag)
    shutil.copytree(KNOW, dst, ignore=IGNORE)
    return dst


def run_gate(kdir, script):
    """Run one validator inside the copied knowledge dir; return (exit, output)."""
    r = subprocess.run([sys.executable, os.path.join(kdir, script)],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout + r.stderr)


def record(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(("  PASS  " if ok else "  FAIL  ") + name + (f" — {detail}" if detail and not ok else ""))


# ---------- mutation helpers ----------

def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def first_snippet_with_manifest(kdir, need=lambda man, html: True):
    """Return (path, html, manifest) of the first snippet satisfying `need`."""
    for f in sorted(os.listdir(os.path.join(kdir, "snippets"))):
        if not f.endswith(".reference.html"):
            continue
        p = os.path.join(kdir, "snippets", f)
        html = read(p)
        m = re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', html, re.S)
        if not m:
            continue
        try:
            man = json.loads(m.group(1))
        except Exception:
            continue
        if need(man, html):
            return p, html, man
    raise RuntimeError("no snippet satisfies the mutation precondition")


def replace_manifest(html, man):
    return re.sub(r'(<script[^>]*id="token-manifest"[^>]*>).*?(</script>)',
                  lambda m: m.group(1) + json.dumps(man, indent=2) + m.group(2),
                  html, flags=re.S)


# ---------- cases ----------

def case_control(tmp):
    """Pristine copy: every static gate must pass (so later bites are meaningful)."""
    k = fresh_copy(tmp, "control")
    gates = ["_validate_snippets.py", "_validate_icons.py", "_validate_a11y.py",
             "_validate_coverage.py", "_validate_dark_surfaces.py", "_validate_compose.py"]
    bad = []
    for g in gates:
        code, out = run_gate(k, g)
        if code != 0:
            bad.append(f"{g} exit {code}")
    record("control: pristine copy passes all 6 static gates", not bad, "; ".join(bad))


def bite(tmp, name, tag, gate, mutate, marker):
    """Copy → mutate → run gate → assert it bites with the expected complaint."""
    k = fresh_copy(tmp, tag)
    try:
        mutate(k)
    except Exception as e:
        record(name, False, f"mutation failed: {e}")
        return
    code, out = run_gate(k, gate)
    ok = (code != 0) and (marker in out)
    detail = f"exit={code}, marker {'found' if marker in out else 'MISSING: ' + marker!r}"
    record(name, ok, detail)


def mut_token_drift(k):
    def need(man, html):
        return bool(man.get("vars"))
    p, html, man = first_snippet_with_manifest(k, need)
    var = next(iter(man["vars"]))
    # change the var's value in the LIGHT theme block only
    def sub_block(m):
        return m.group(0).replace(m.group(2), "#123456", 1)
    pat = re.compile(r'(\[data-theme="light"\]\s*\{[^}]*?' + re.escape(var) +
                     r'\s*:\s*)(#[0-9A-Fa-f]{6,8})')
    new, n = pat.subn(lambda m: m.group(1) + "#123456", html, count=1)
    if not n:
        raise RuntimeError(f"var {var} not found in light block of {os.path.basename(p)}")
    write(p, new)


def mut_missing_aria(k):
    """Remove the required ARIA from the MARKUP but leave the manifest's
    declaration intact. (First attempt removed it everywhere — which silently
    deleted the requirement itself and the gate passed. That is a real,
    documented caveat: the gate enforces author-DECLARED requirements living in
    the same file it validates. Hardening idea: cross-check requiredAria
    against the component meta, coverage-style.)"""
    def need(man, html):
        return bool(man.get("requiredAria")) and man["requiredAria"][0] in html
    p, html, man = first_snippet_with_manifest(k, need)
    span = re.search(r'<script[^>]*id="token-manifest"[^>]*>.*?</script>', html, re.S).span()
    body = html[:span[0]].replace(man["requiredAria"][0], "") \
        + html[span[0]:span[1]] \
        + html[span[1]:].replace(man["requiredAria"][0], "")
    write(p, body)


def mut_bad_contrast(k):
    # use a token the snippet already binds (guaranteed to resolve in the store),
    # as both fg and bg -> ratio 1.0 -> a true CONTRAST failure, not an unresolved token
    def need(man, html):
        return bool(man.get("vars"))
    p, html, man = first_snippet_with_manifest(k, need)
    tok = next(iter(man["vars"].values()))
    man.setdefault("contrastPairs", []).append(
        {"fg": tok, "bg": tok, "context": "text"})
    write(p, replace_manifest(html, man))


def mut_no_focus(k):
    def need(man, html):
        return "<button" in html and ":focus-visible" in html
    p, html, man = first_snippet_with_manifest(k, need)
    write(p, html.replace(":focus-visible", ":focus-hidden"))


def mut_reduced_motion(k):
    def need(man, html):
        return ("prefers-reduced-motion" in html
                and re.search(r'transition\s*:|animation\s*:|@keyframes', html, re.I))
    p, html, man = first_snippet_with_manifest(k, need)
    write(p, html.replace("prefers-reduced-motion", "prefers-reduced-nothing"))


def mut_allcaps_css(k):
    """type26-019 promotion (Dave ruling 2026-07-02): uppercase transform must bite."""
    p, html, man = first_snippet_with_manifest(k, lambda m, h: "</head>" in h)
    write(p, html.replace("</head>", "<style>.zz-caps{text-transform:uppercase}</style></head>", 1))


def mut_allcaps_text(k):
    """A visible non-acronym ALL-CAPS run must bite (acronym-only runs are exempt)."""
    p, html, man = first_snippet_with_manifest(k, lambda m, h: "</body>" in h)
    write(p, html.replace("</body>", "<p>FINAL WARNING NOTICE</p></body>", 1))


def mut_unknown_icon(k):
    p, html, man = first_snippet_with_manifest(k, lambda m, h: "</body>" in h)
    rogue = '<svg viewBox="0 0 24 24"><path d="M1 1 L23 23 L1 23 Z"/></svg>'
    write(p, html.replace("</body>", rogue + "</body>", 1))


def mut_shape_only_icon(k):
    p, html, man = first_snippet_with_manifest(k, lambda m, h: "</body>" in h)
    rogue = '<svg viewBox="0 0 24 24"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>'
    write(p, html.replace("</body>", rogue + "</body>", 1))


def mut_orphan_snippet(k):
    write(os.path.join(k, "snippets", "Zz-orphan.reference.html"),
          '<!DOCTYPE html><html><head><script type="application/json" id="token-manifest">'
          '{"component": "Zz orphan"}</script></head><body></body></html>')


def mut_ghost_meta(k):
    write(os.path.join(k, "components", "zz-ghost.meta.json"),
          json.dumps({"name": "Zz ghost"}))


def mut_flat_white_dark(k):
    p = os.path.join(k, "tokens", "semantic-colour.json")
    sem = json.load(open(p))

    def walk(node, path=""):
        if not isinstance(node, dict):
            return False
        if "light" in node and "dark" in node and isinstance(node.get("light"), dict):
            name = path.strip("/")
            if (any(c in name for c in ("background", "surface", "border", "divider"))
                    and not any(x in name for x in ("reverse", "on-light", "on-dark"))):
                node["dark"] = {"$value": "#FFFFFF"}
                node.pop("$darkNote", None)
                return True
        for key, v in node.items():
            if not key.startswith("$") and walk(v, path + "/" + key):
                return True
        return False

    if not walk(sem):
        raise RuntimeError("no qualifying surface token found")
    json.dump(sem, open(p, "w"), indent=2)


def _first_canon_screen(k):
    ft = os.path.join(k, "_fitness-test")
    for f in sorted(os.listdir(ft)):
        if f.endswith(".canon.html"):
            return os.path.join(ft, f)
    raise RuntimeError("no *.canon.html screen found")


def mut_rogue_hex(k):
    p = _first_canon_screen(k)
    html = read(p)
    write(p, html.replace("</head>", "<style>.zz-rogue{color:#FF0000;}</style></head>", 1))


def mut_undefined_class(k):
    p = _first_canon_screen(k)
    html = read(p)
    write(p, html.replace("</body>", '<div class="cn-zz-nonexistent"></div></body>', 1))


def mut_redefine_class(k):
    p = _first_canon_screen(k)
    html = read(p)
    write(p, html.replace("</head>", "<style>.cn-button{opacity:.5}</style></head>", 1))


CASES = [
    ("snippet gate bites on token drift",        "drift",    "_validate_snippets.py",     mut_token_drift,     "DRIFT"),
    ("snippet gate bites on missing ARIA",       "aria",     "_validate_snippets.py",     mut_missing_aria,    "required ARIA missing"),
    ("snippet gate bites on failing contrast",   "contrast", "_validate_snippets.py",     mut_bad_contrast,    "CONTRAST"),
    ("snippet gate bites on missing focus",      "focus",    "_validate_snippets.py",     mut_no_focus,        ":focus-visible"),
    ("snippet gate bites on uppercase CSS",      "caps-css", "_validate_snippets.py",     mut_allcaps_css,     "ALL-CAPS text-transform"),
    ("snippet gate bites on ALL-CAPS text run",  "caps-txt", "_validate_snippets.py",     mut_allcaps_text,    "ALL-CAPS text run"),
    ("a11y gate bites on missing reduced-motion","motion",   "_validate_a11y.py",         mut_reduced_motion,  "2.3.3"),
    ("icon gate bites on invented path",         "icon",     "_validate_icons.py",        mut_unknown_icon,    "UNKNOWN"),
    ("icon gate bites on shape-only icon",       "shape",    "_validate_icons.py",        mut_shape_only_icon, "UNKNOWN"),
    ("coverage gate bites on orphan snippet",    "orphan",   "_validate_coverage.py",     mut_orphan_snippet,  "no meta"),
    ("coverage gate bites on meta w/o snippet",  "ghost",    "_validate_coverage.py",     mut_ghost_meta,      "no gated snippet"),
    ("dark-surface gate bites on flat white",    "flat",     "_validate_dark_surfaces.py",mut_flat_white_dark, "#FFFFFF"),
    ("compose gate bites on rogue hex",          "hex",      "_validate_compose.py",      mut_rogue_hex,       "hex colour"),
    ("compose gate bites on undefined class",    "undef",    "_validate_compose.py",      mut_undefined_class, "used but undefined"),
    ("compose gate bites on class redefinition", "redef",    "_validate_compose.py",      mut_redefine_class,  "redefines canon class"),
]


def main():
    print("gate self-test: does every gate BITE what it was built to catch?\n")
    tmp = tempfile.mkdtemp(prefix="gate-tests-")
    try:
        case_control(tmp)
        for name, tag, gate, mutate, marker in CASES:
            bite(tmp, name, tag, gate, mutate, marker)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    nfail = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"\n{len(RESULTS)} test(s), {nfail} failure(s)")
    print("skipped by design: state-contrast / screen --render (need a browser; see docstring)")
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
