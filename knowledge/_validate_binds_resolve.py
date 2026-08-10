#!/usr/bin/env python3
"""_validate_binds_resolve.py — the ADDRESS-RESOLVE GATE (#146; the gate #145 named).

THE CLASS THIS GATE CLOSES (the #146 finding, "stopped matching, stopped failing"):
a correspondence between two artefacts held by NOTHING — an address or discriminator
that can stop matching, where the non-match path is a silent fall-through, so a rename
upstream turns work off without turning anything red. Prior bites of the class:
  - #122 ds-039 (no gate parses the artefact — the named ancestor)
  - s141-D1(B): a token sat at $type "other" and was silently skipped by
    gen_canon_tokens fmt_value (its own line-140 comment records this)
  - #145: fmt_value's `ttype == "string"` branch stopped firing when the type
    tightened to "fontFamily" — canon.css silently lost the font fallback stack
  - #145 lane ②: no validator resolves a meta `binds` address against the colour
    spine — alert.meta.json::status $status carries the full finding, quoted:
    "rename the rung and every gate stays green"

THREE CHECKS, ONE SEAM (address → store):
  A. MANIFEST PRESENCE — every knowledge/snippets/*.reference.html carries a
     parseable <script id="token-manifest"> block with a "vars" dict. Measured at
     build time (#146): 75/75 carry one, so presence is ABSOLUTE, not ratcheted.
     A snippet whose manifest block is malformed or renamed silently drops out of
     BOTH gen_snippet_tokens sync AND gen_theme_cascade projection
     (`if not mm: continue`, both generators) — this check makes that loud.
  B. MANIFEST VARS RESOLVE — every manifest var's token path resolves through
     gen_snippet_tokens.resolve() (ONE router, imported, never re-implemented —
     re-implementing it is how the alpha/* route was missed once already, s121-D1)
     in at least one mode.
  C. BINDS ADDRESSES RESOLVE — every props[].binds address in
     knowledge/components/*.meta.json (excluding EXAMPLE-*) reaches an existing
     node in a declared store. EXISTENCE, not value-resolution, because binds
     addresses may deliberately point at GROUPS (address-intent: "icon",
     "border-radius", "alpha", "typography.font-size"). An address exists if its
     dot-path walks to a node in ANY store declared for its first segment —
     "icon.default" is a colour in semantic-colour.json while "icon.small" is a
     size in icon-scale.json; both are real, the stores just differ.
  D. CANON BLOCK PRESENCE (s147-D2) — every snippet carrying a token-manifest must
     match at least one `.cn-<slug>{` block in canon/canon.css. gen_snippet_tokens'
     project_canon substitutes via that regex; rename a component file and the sub
     finds nothing — projection turns off, nothing goes red. Same held-by-nothing
     correspondence as A–C, homed here per the one-gate-per-class design Dave
     ratified (#147 opener). Measured at build time: 75/75, absolute, no allowlist.

WHAT THIS GATE CANNOT SEE, DECLARED: it proves addresses point at SOMETHING, not
at the RIGHT thing. Correctness of a binding stays with the binds draft + Dave's
verdicts (reviews/BINDS-AUTHORING-VERDICTS-*). A green here reads "no address
dangles", never "axis A is correct".

Usage:  python3 knowledge/_validate_binds_resolve.py             # gate mode
        python3 knowledge/_validate_binds_resolve.py --selftest  # 6 bites
Exit non-zero on any failure. Absent corpus fails LOUD — an absent instrument
must not read as a pass (_validate_binds_ratchet.py's rule, kept).
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
COMP = os.path.join(HERE, "components")
TOK = os.path.join(HERE, "tokens")

MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)

# First path segment -> ordered candidate stores. An address EXISTS if its full
# dot-path walks to a node in any one of them. Paths are relative to knowledge/.
# NOTE the two-store segments: "icon" is a colour family in semantic-colour.json
# AND a size ladder in icon-scale.json; both routes are deliberate.
STORES = {
    "color":          ["tokens/colour.json"],
    "border-radius":  ["tokens/layout.json"],
    "border-width":   ["tokens/layout.json"],
    "focus-ring":     ["tokens/layout.json"],
    "layout":         ["tokens/layout.json"],
    "breakpoint":     ["tokens/layout.json"],
    "target":         ["tokens/layout.json"],
    "scale":          ["tokens/layout.json"],
    "motion":         ["tokens/motion.json"],
    "component-type": ["component-types.json"],
    "alpha":          ["tokens/opacity.json"],
    "typography":     ["tokens/typography.json"],
    "icon":           ["tokens/semantic-colour.json", "tokens/icon-scale.json"],
}
DEFAULT_STORES = ["tokens/semantic-colour.json"]


class GateError(Exception):
    """A named failure of this gate's own machinery (never a silent pass)."""


_store_cache: dict = {}


def _load_store(rel):
    if rel not in _store_cache:
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            raise GateError(f"declared store missing: {rel}")
        _store_cache[rel] = json.load(open(p))
    return _store_cache[rel]


def address_exists(addr, load=_load_store):
    """True if dot-address `addr` walks to an existing node in any declared store."""
    parts = addr.split(".")
    for rel in STORES.get(parts[0], DEFAULT_STORES):
        node = load(rel)
        ok = True
        for k in parts:
            if isinstance(node, dict) and k in node:
                node = node[k]
            else:
                ok = False
                break
        if ok:
            return True
    return False


# ---------------------------------------------------------------- pure checks
def check_manifests(pages):
    """pages: {name: html_text}. Returns (failures, {name: vars_dict})."""
    fails, vars_by_page = [], {}
    for name, html in sorted(pages.items()):
        m = MANIFEST_RE.search(html)
        if not m:
            fails.append(f"{name}: NO token-manifest block — this snippet is invisible "
                         f"to gen_snippet_tokens sync AND gen_theme_cascade projection")
            continue
        try:
            manifest = json.loads(m.group(1))
        except ValueError as e:
            fails.append(f"{name}: token-manifest is UNPARSEABLE ({e}) — same silent "
                         f"drop as a missing block")
            continue
        vars_by_page[name] = manifest.get("vars", {})
    return fails, vars_by_page


def check_vars(vars_by_page, resolver):
    """resolver(path, mode) raises KeyError when unresolvable. A var must resolve
    in at least one mode."""
    fails = []
    for name, varmap in sorted(vars_by_page.items()):
        for cssvar, path in varmap.items():
            errs = []
            for mode in ("light", "dark"):
                try:
                    resolver(path, mode)
                    errs = []
                    break
                except KeyError as e:
                    errs.append(f"{mode}: {e}")
            if errs:
                fails.append(f"{name}: {cssvar} -> {path} UNRESOLVED in both modes "
                             f"({'; '.join(errs)})")
    return fails


def _walk_binds(value, out):
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, list):
        for v in value:
            _walk_binds(v, out)
    elif isinstance(value, dict):
        for v in value.values():
            _walk_binds(v, out)


def check_binds(metas, exists):
    """metas: {name: parsed_meta}. Returns (failures, address_count)."""
    fails, count = [], 0
    for name, meta in sorted(metas.items()):
        for prop in meta.get("props", []):
            addrs = []
            _walk_binds(prop.get("binds"), addrs)
            for addr in addrs:
                count += 1
                if not exists(addr):
                    fails.append(f"{name}::{prop.get('name', '?')}: binds address "
                                 f"'{addr}' resolves to NOTHING in any declared store "
                                 f"— a renamed rung, or a store this gate's router "
                                 f"must be taught (teach STORES, never widen silently)")
    return fails, count


def check_canon_blocks(names_with_manifest, css, slugger):
    """Check D (s147-D2). names_with_manifest: iterable of snippet filenames that
    carry a parseable manifest. A slug with zero `.cn-<slug>{` matches in the css
    means project_canon's substitution silently finds nothing — loud here."""
    fails = []
    for name in sorted(names_with_manifest):
        slug = slugger(name)
        if not re.search(r'\.cn-' + re.escape(slug) + r'\{', css):
            fails.append(f"{name}: no .cn-{slug} block in canon.css — "
                         f"project_canon projection is silently OFF for this snippet "
                         f"(renamed component file, or block never authored)")
    return fails


# ---------------------------------------------------------------- corpus + main
def run():
    if not os.path.isdir(SNIP):
        raise GateError(f"snippet corpus not found: {SNIP}")
    if not os.path.isdir(COMP):
        raise GateError(f"component corpus not found: {COMP}")
    sys.path.insert(0, HERE)
    import gen_snippet_tokens as gst   # the ONE router (s121-D1 lesson)

    pages = {os.path.basename(f): open(f).read()
             for f in glob.glob(os.path.join(SNIP, "*.reference.html"))}
    if not pages:
        raise GateError("zero reference.html files — an empty corpus is not a pass")
    metas = {os.path.basename(f): json.load(open(f))
             for f in glob.glob(os.path.join(COMP, "*.meta.json"))
             if "EXAMPLE-" not in os.path.basename(f)}
    if not metas:
        raise GateError("zero meta.json files — an empty corpus is not a pass")

    canon_path = os.path.join(HERE, "canon", "canon.css")
    if not os.path.exists(canon_path):
        raise GateError(f"canon.css not found: {canon_path} — check D cannot read as a pass")
    css = open(canon_path).read()

    f1, vars_by_page = check_manifests(pages)
    f2 = check_vars(vars_by_page, gst.resolve)
    f3, n_addr = check_binds(metas, address_exists)
    f4 = check_canon_blocks(vars_by_page.keys(), css, gst.slug_of)
    fails = f1 + f2 + f3 + f4
    nvars = sum(len(v) for v in vars_by_page.values())
    print(f"binds-resolve gate: {len(pages)} snippets ({len(vars_by_page)} with "
          f"manifests, {nvars} vars) · {len(metas)} metas ({n_addr} binds addresses) "
          f"· {len(vars_by_page) - len(f4)}/{len(vars_by_page)} canon blocks "
          f"· {len(fails)} failure(s)")
    for f in fails:
        print(f"  ⛔ {f}")
    return 1 if fails else 0


def selftest():
    """Six bites. Each drives a SYNTHETIC breakage through the pure checks —
    the clause under test is the one that must fail (never only the feature)."""
    good_page = '<script type="application/json" id="token-manifest">{"vars": {"x-a": "rag/error"}}</script>'

    # bite 1: missing manifest block MUST fail
    fails, _ = check_manifests({"a.reference.html": "<html>no manifest</html>"})
    assert fails and "NO token-manifest" in fails[0], "bite 1: missing manifest did not fail"

    # bite 2: unparseable manifest MUST fail
    fails, _ = check_manifests({"b.reference.html":
                                '<script id="token-manifest">{not json</script>'})
    assert fails and "UNPARSEABLE" in fails[0], "bite 2: bad JSON did not fail"

    # bite 3: unresolvable var path MUST fail; resolvable must not
    def rz(path, mode):
        if path != "rag/error":
            raise KeyError(path)
        return "#FFF"
    _, vp = check_manifests({"c.reference.html": good_page})
    assert check_vars(vp, rz) == [], "bite 3a: good var failed"
    fails = check_vars({"c": {"--x": "rag/gone"}}, rz)
    assert fails and "UNRESOLVED" in fails[0], "bite 3b: bogus var did not fail"

    # bite 4: dangling binds address MUST fail, across str/dict/list shapes
    ex = lambda a: a in ("rag.error", "icon.small")
    meta = {"m.meta.json": {"props": [
        {"name": "status", "binds": {"error": "rag.error", "warning": "rag.gone"}}]}}
    fails, n = check_binds(meta, ex)
    assert n == 2 and len(fails) == 1 and "rag.gone" in fails[0], \
        "bite 4: dangling address did not fail (or count wrong)"

    # bite 5: the ANY-STORE clause — an address absent from the first store but
    # present in the second must PASS (the icon.small shape). Injected loader so
    # the bite owns both stores.
    stores = {"tokens/semantic-colour.json": {"icon": {"default": {"$value": "#000"}}},
              "tokens/icon-scale.json": {"icon": {"small": {"$value": 16}}}}
    assert address_exists("icon.small", load=lambda r: stores[r]), \
        "bite 5a: second-store address read as dangling"
    assert not address_exists("icon.tiny", load=lambda r: stores[r]), \
        "bite 5b: absent-in-both address read as existing"

    # bite 6 (s147-D2): a manifest snippet whose slug matches no .cn- block MUST
    # fail; one that matches must not. Regex-metachar slug guards the escaping.
    css6 = ".cn-alert-banner{--x:#000;}"
    slugger = lambda n: n.replace(".reference.html", "")
    assert check_canon_blocks(["alert-banner.reference.html"], css6, slugger) == [], \
        "bite 6a: present block read as missing"
    fails = check_canon_blocks(["alert-toast.reference.html"], css6, slugger)
    assert fails and ".cn-alert-toast" in fails[0], "bite 6b: absent block did not fail"

    print("binds-resolve selftest: 6 bites PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(selftest() if "--selftest" in sys.argv else run())
    except GateError as e:
        print(f"⛔ GATE MACHINERY FAILURE (named, never silent): {e}")
        sys.exit(2)
