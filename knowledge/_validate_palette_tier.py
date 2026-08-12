#!/usr/bin/env python3
"""_validate_palette_tier.py — the NAMED-PALETTE TIER gate (s157-D2, ruled #157, built #158).

THE CLASS THIS GATE CLOSES. Console and Supercharge carried TWELVE hex-identical RAG
keys in two separate ratified override files with NOTHING declaring that they were
meant to be the same. Nothing was red; nothing could go red. Change one and the other
does not follow, and no instrument notices — the sharing lived only in a $note. Dave,
#157: "rather than patching and hacking it we need a solid, best practice solution...
solid but flexible in the future". s157-D2 makes the sharing STRUCTURAL: a palette is a
named file, a theme DECLARES which palette it consumes, and this gate holds the join.

It is the same mechanism ADR-0014 gave the neutral ramp (`neutralRamp` on each theme),
extended to a second family (`ragPalette`) — deliberately NOT a parallel mechanism.

PARSE IN THE CONSUMER'S GRAMMAR (#122 ds-039): every check below RESOLVES against
parsed JSON — registry -> palette file -> override set -> base store. Nothing here
greps for a hex. A grep would pass on a file whose key was renamed out of the way.

SIX CHECK GROUPS (A, B, C/D, E, F, G):
  A. DECLARATION — every theme in tokens/themes/_themes.json declares BOTH family
     fields, `ragPalette` and `neutralRamp`. A missing declaration is the defect
     s157-D2 names: consumption that is real but undeclared.
  B. DECLARATION RESOLVES — each `ragPalette` names a file that EXISTS under
     tokens/ and parses; each `neutralRamp` ("color/<family>/<a>-<b>") names a
     family that exists in tokens/colour.json AND whose endpoint steps exist.
  C. PALETTE SHAPE — every palette declares $coreKeys; every core key is EITHER
     declared with a DTCG light+dark $value pair OR named in $partialKeys.keys.
     Silence is not permitted: an absent rung must be DECLARED absent. (This is the
     #157 catch generalised — no theme overrode rag/*-ink, so non-mono themes fell
     through to mono's values with nothing saying so.)
  D. TINTS ARE NOT PALETTE-OWNED — no palette may declare a `-tint` key. Tints
     derive from per-theme grounds (s123-D3: console = tuned opacity over its own
     background, supercharge = solids) and stay in each override set. A tint in a
     palette would share a value that must NOT be shared.
  E. NO HAND-CARRIED DIVERGENCE — for every theme, every palette-declared key must
     agree hex-for-hex with what that theme actually resolves to today:
       * base theme (Mono): against tokens/semantic-colour.json rag/<key>
       * override themes:   against overrides/rag/<key> in the theme's override set,
                            for every key the override set declares
     This is the IN-PLACE-VERIFY posture. It preserves the ratified override files
     and their $notes intact (ADD-never-trim) while making divergence loud. The
     alternative posture — the override files become GENERATED from the palette and
     the palette-owned keys leave them — is Dave's call, NOT this gate's; run with
     --strict-absence to measure what that posture would require (it asserts the
     override files carry NO palette-owned key). Default is verify.
  F. SHARING IS DECLARED, NOT COINCIDENTAL — if two themes' palette-owned values are
     identical across the ENTIRE core roster, they must name the SAME palette file.
     This is the exact console/supercharge defect, gated: duplicate-by-accident can
     no longer sit undeclared. (Divergence is always allowed — this only forbids
     silent duplication.)
  G. CONSUMED RUNGS ARE DECLARED PER PALETTE (#145 lane ② + #157 union) — every
     rag rung bound by a CONSUMER, in EITHER consumer grammar, that is part of the
     palette vocabulary must be either declared or explicitly $partialKeys-declared
     in EVERY palette. A rung a consumer binds must not fall through a theme in
     silence. Both grammars are walked, and the second one is load-bearing:
       * component metas   — props[].binds, dot form ("rag.success"); str/list/dict
       * snippet manifests — vars{}, slash form ("rag/success-ink")
     `rag/success-ink` — the one ruled green-text seat (s155-D1) — is bound by NO
     component meta (amount-display.meta.json binds rag.success / rag.error on its
     `sign` prop). A meta-only walk reads GREEN on it. Measured #158 by driving the
     gate, not by reading it; selftest bite 10 carries the mutation AND the negative
     control that proves the manifest arm is what catches it.
     NOTE, measured #158 and NOT duplicated here: plain address->store EXISTENCE for
     meta binds is ALREADY held by _validate_binds_resolve.py check C (its _walk_binds
     handles dict-shaped binds; `rag.*` routes to tokens/semantic-colour.json via
     DEFAULT_STORES). Mutation-verified at #158. Check G is the part that gate cannot
     see: not "does the address exist in the base", but "does every THEME have a
     value for it, or say it does not".

WHAT THIS GATE CANNOT SEE, DECLARED HONESTLY:
  * It proves values AGREE and consumption is DECLARED. It does not rule whether a
    value is right — that stays with Dave and the controllers.
  * Palette FILE NAMES are placeholders (s157-D2 open item). The gate reads the name
    from the registry, so renaming a palette is a two-file edit and stays green.
  * It does not check the -tint derivations themselves (per-theme, out of scope by D).
  * It says nothing about non-mono -ink rungs beyond "declared absent". No green or
    red fork for them is governed (s151-D1 / s155-D1 scope those MONO ONLY).

Usage:  python3 knowledge/_validate_palette_tier.py                  # gate mode
        python3 knowledge/_validate_palette_tier.py --strict-absence # price the generate posture
        python3 knowledge/_validate_palette_tier.py --selftest       # 10 mutation bites
Exit non-zero on any failure. An absent corpus fails LOUD — an absent instrument must
never read as a pass (_validate_binds_ratchet.py's rule, kept).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(HERE, "tokens")
THEMES = os.path.join(TOK, "themes", "_themes.json")
COMP = os.path.join(HERE, "components")
MODES = ("light", "dark")
MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)
RAMP_RE = re.compile(r"^color/([A-Za-z0-9_-]+)/([0-9]+)-([0-9]+)$")


class GateError(Exception):
    """A named failure of this gate's own machinery (never a silent pass)."""


# ---------------------------------------------------------------- loading
def load_json(path):
    if not os.path.exists(path):
        raise GateError(f"required file missing: {path}")
    with open(path) as fh:
        return json.load(fh)


def palette_core(pal):
    """The palette's declared core vocabulary."""
    core = pal.get("$coreKeys")
    if not isinstance(core, list) or not core:
        raise GateError("palette has no $coreKeys list — its vocabulary is undeclared")
    return core


def palette_pairs(pal):
    """{key: {mode: hex}} for every key the palette DECLARES with a full pair."""
    out = {}
    for key, node in (pal.get("keys") or {}).items():
        pair = {}
        for m in MODES:
            v = node.get(m) if isinstance(node, dict) else None
            if isinstance(v, dict) and "$value" in v:
                pair[m] = v["$value"]
        out[key] = pair
    return out


def declared_absent(pal):
    return set((pal.get("$partialKeys") or {}).get("keys") or [])


def _walk_binds(value, out):
    """Same shape-walk as _validate_binds_resolve._walk_binds — binds may be a
    string, a list, or a dict of variant -> address (all three occur in the corpus)."""
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, list):
        for v in value:
            _walk_binds(v, out)
    elif isinstance(value, dict):
        for v in value.values():
            _walk_binds(v, out)


# ---------------------------------------------------------------- pure checks
def check_declarations(themes):
    """A. Both family fields present on every theme."""
    fails = []
    for key, t in sorted(themes.items()):
        for field in ("ragPalette", "neutralRamp"):
            if not t.get(field):
                fails.append(
                    f"{key}: no '{field}' declaration in _themes.json — this theme "
                    f"consumes a {field.replace('Palette', ' palette').replace('Ramp', ' ramp')} "
                    f"in fact but declares none (s157-D2: consumption must be declared)")
    return fails


def check_declarations_resolve(themes, palettes, colour):
    """B. Each declaration reaches a real artefact."""
    fails = []
    for key, t in sorted(themes.items()):
        rel = t.get("ragPalette")
        if rel and rel not in palettes:
            fails.append(f"{key}: ragPalette '{rel}' does not resolve to a palette file "
                         f"under tokens/ — dangling declaration")
        ramp = t.get("neutralRamp")
        if ramp:
            m = RAMP_RE.match(ramp)
            if not m:
                fails.append(f"{key}: neutralRamp '{ramp}' is not of the form "
                             f"color/<family>/<lo>-<hi>")
            else:
                fam, lo, hi = m.group(1), m.group(2), m.group(3)
                node = (colour.get("color") or {}).get(fam)
                if node is None:
                    fails.append(f"{key}: neutralRamp family 'color/{fam}' does not exist "
                                 f"in tokens/colour.json")
                else:
                    for step in (lo, hi):
                        if step not in node:
                            fails.append(f"{key}: neutralRamp endpoint 'color/{fam}/{step}' "
                                         f"does not exist in tokens/colour.json")
    return fails


def check_palette_shape(palettes):
    """C + D. Every core key declared-or-declared-absent; no tints."""
    fails = []
    for rel, pal in sorted(palettes.items()):
        core = palette_core(pal)
        pairs = palette_pairs(pal)
        absent = declared_absent(pal)
        for key in core:
            if key in pairs:
                missing = [m for m in MODES if m not in pairs[key]]
                if missing:
                    fails.append(f"{rel}: key '{key}' is missing {'/'.join(missing)} "
                                 f"$value — a half-declared rung leaks the other mode")
            elif key not in absent:
                fails.append(f"{rel}: core key '{key}' is NEITHER declared NOR listed in "
                             f"$partialKeys.keys — silent absence is the fall-through class "
                             f"(#157); declare the value or declare the absence")
        for key in pairs:
            if key.endswith("-tint"):
                fails.append(f"{rel}: '{key}' is a TINT and must not be palette-owned — "
                             f"tints derive from per-theme grounds (s123-D3) and stay in "
                             f"each override set")
    return fails


def check_agreement(themes, palettes, base_rag, override_sets, strict_absence=False):
    """E. Palette values agree with what each theme resolves to today."""
    fails = []
    for key, t in sorted(themes.items()):
        rel = t.get("ragPalette")
        if not rel or rel not in palettes:
            continue                       # already reported by A/B
        pairs = palette_pairs(palettes[rel])
        if t.get("status") == "base":
            for k, pair in sorted(pairs.items()):
                node = base_rag.get(k)
                if node is None:
                    fails.append(f"{key}: palette {rel} declares '{k}' but the BASE store "
                                 f"has no rag/{k} — the base theme's palette is a VIEW of "
                                 f"the base store, not a second copy")
                    continue
                for m in MODES:
                    have = (node.get(m) or {}).get("$value")
                    if have != pair.get(m):
                        fails.append(f"{key}: rag/{k} {m} — palette {rel} says "
                                     f"{pair.get(m)!r}, base store says {have!r}")
            continue
        ov = override_sets.get(key) or {}
        for k, pair in sorted(pairs.items()):
            node = ov.get(f"rag/{k}")
            if node is None:
                continue                   # palette supplies it; nothing to disagree with
            if strict_absence:
                fails.append(f"{key}: override set hand-carries palette-owned key rag/{k} "
                             f"(--strict-absence: the GENERATE posture forbids it)")
                continue
            for m in MODES:
                have = (node.get(m) or {}).get("$value")
                if have != pair.get(m):
                    fails.append(f"{key}: rag/{k} {m} — palette {rel} says {pair.get(m)!r}, "
                                 f"override set {t.get('overrideSet')} says {have!r}. The "
                                 f"palette is the shared source; a theme that must differ "
                                 f"needs its OWN palette, not a divergent copy")
    return fails


def check_sharing_declared(themes, palettes):
    """F. Identical-across-the-roster => must name the same palette."""
    fails = []
    keys = sorted(themes)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            ra, rb = themes[a].get("ragPalette"), themes[b].get("ragPalette")
            if not ra or not rb or ra == rb:
                continue
            if ra not in palettes or rb not in palettes:
                continue
            pa, pb = palette_pairs(palettes[ra]), palette_pairs(palettes[rb])
            shared = sorted(set(pa) & set(pb))
            if not shared:
                continue
            if all(pa[k] == pb[k] for k in shared):
                fails.append(
                    f"{a} and {b} name DIFFERENT palettes ({ra} / {rb}) whose values are "
                    f"IDENTICAL across all {len(shared)} shared key(s). That is duplication "
                    f"with nothing declaring it — the exact s157-D2 defect. Point both at "
                    f"one palette, or make the divergence real.")
    return fails


def check_consumed_rungs(metas, palettes, manifests=None):
    """G. A rung a consumer binds must be declared (present or absent) everywhere.

    TWO consumer grammars, both walked — measured #158, and the second one is the
    reason this check has its final shape. `rag/success-ink` (the one ruled green-text
    seat, s155-D1) is bound by NO component meta: amount-display.meta.json binds
    rag.success / rag.error on its `sign` prop, while the SNIPPET token-manifest binds
    "--success-ink" -> "rag/success-ink". A check reading only metas measures the wrong
    artefact and reports a green it has not earned (first draft of this gate did exactly
    that at #158 — caught by driving it, not by reading it).
      * component metas   — props[].binds, dot form   ("rag.success")
      * snippet manifests — vars{}, slash form        ("rag/success-ink")
    """
    fails = []
    vocab = set()
    for pal in palettes.values():
        vocab |= set(palette_core(pal))
    bound = {}
    for name, meta in sorted(metas.items()):
        for prop in meta.get("props", []):
            addrs = []
            _walk_binds(prop.get("binds"), addrs)
            for addr in addrs:
                if not addr.startswith("rag."):
                    continue
                k = addr.split(".", 1)[1]
                if k in vocab:
                    bound.setdefault(k, set()).add(f"{name}::{prop.get('name', '?')}")
    for name, varmap in sorted((manifests or {}).items()):
        for cssvar, path in varmap.items():
            if not str(path).startswith("rag/"):
                continue
            k = str(path).split("/", 1)[1]
            if k in vocab:
                bound.setdefault(k, set()).add(f"{name}::{cssvar}")
    for k, consumers in sorted(bound.items()):
        for rel, pal in sorted(palettes.items()):
            if k in palette_pairs(pal) or k in declared_absent(pal):
                continue
            fails.append(
                f"palette {rel} neither declares nor declares-absent rag/{k}, which IS "
                f"consumed by {', '.join(sorted(consumers))}. A bound rung that falls "
                f"through a theme in silence is the #145/#157 class.")
    return fails


# ---------------------------------------------------------------- corpus + main
def load_corpus():
    reg = load_json(THEMES)
    themes = reg.get("themes") or {}
    if not themes:
        raise GateError("_themes.json declares zero themes — an empty registry is not a pass")
    palettes = {}
    for f in sorted(glob.glob(os.path.join(TOK, "palettes", "**", "*.json"), recursive=True)):
        rel = os.path.relpath(f, TOK).replace(os.sep, "/")
        palettes[rel] = load_json(f)
    if not palettes:
        raise GateError("zero palette files under tokens/palettes/ — an empty corpus is "
                        "not a pass (s157-D2 declares this tier exists)")
    colour = load_json(os.path.join(TOK, "colour.json"))
    base_rag = load_json(os.path.join(TOK, "semantic-colour.json")).get("rag") or {}
    if not base_rag:
        raise GateError("tokens/semantic-colour.json has no rag/* family — cannot verify "
                        "the base theme's palette against anything")
    override_sets = {}
    for key, t in themes.items():
        oset = t.get("overrideSet")
        if oset:
            override_sets[key] = load_json(os.path.join(TOK, oset)).get("overrides") or {}
    metas = {os.path.basename(f): load_json(f)
             for f in sorted(glob.glob(os.path.join(COMP, "*.meta.json")))
             if "EXAMPLE-" not in os.path.basename(f)}
    if not metas:
        raise GateError("zero meta.json files — an empty corpus is not a pass")
    manifests = {}
    for f in sorted(glob.glob(os.path.join(HERE, "snippets", "*.reference.html"))):
        m = MANIFEST_RE.search(open(f).read())
        if not m:
            continue          # presence is _validate_binds_resolve.py check A's job
        try:
            manifests[os.path.basename(f)] = json.loads(m.group(1)).get("vars", {}) or {}
        except ValueError:
            continue          # parseability is that same gate's job — one gate per class
    if not manifests:
        raise GateError("zero parseable snippet token-manifests — an empty corpus is not "
                        "a pass (check G would read green on nothing)")
    return themes, palettes, colour, base_rag, override_sets, metas, manifests


def run(strict_absence=False):
    themes, palettes, colour, base_rag, override_sets, metas, manifests = load_corpus()
    groups = [
        ("A declaration", check_declarations(themes)),
        ("B declaration resolves", check_declarations_resolve(themes, palettes, colour)),
        ("C/D palette shape", check_palette_shape(palettes)),
        ("E value agreement", check_agreement(themes, palettes, base_rag, override_sets,
                                              strict_absence)),
        ("F sharing declared", check_sharing_declared(themes, palettes)),
        ("G consumed rungs declared", check_consumed_rungs(metas, palettes, manifests)),
    ]
    fails = [(g, f) for g, fs in groups for f in fs]
    n_keys = sum(len(palette_pairs(p)) for p in palettes.values())
    print(f"palette-tier gate: {len(themes)} theme(s), {len(palettes)} palette(s), "
          f"{n_keys} declared key(s), {len(metas)} component meta(s), "
          f"{len(manifests)} snippet manifest(s)"
          + ("  [--strict-absence: GENERATE posture]" if strict_absence else ""))
    if fails:
        print(f"\n❌ palette-tier gate: {len(fails)} failure(s)")
        for g, f in fails:
            print(f"  [{g}] {f}")
        return 1
    print("OK — every theme declares a palette per family; every declaration resolves; "
          "no theme hand-carries a divergent palette-owned value; no undeclared duplication.")
    return 0


# ---------------------------------------------------------------- selftest
def _selftest():
    """10 bites. Each mutates a PARSED corpus and asserts the matching check reddens —
    a green that cannot fail is an assertion, not a test (#104)."""
    bites = 0
    themes, palettes, colour, base_rag, override_sets, metas, manifests = load_corpus()

    def clone(o):
        return json.loads(json.dumps(o))

    # 1 — a theme drops its ragPalette declaration
    t = clone(themes); t["apollo-console"].pop("ragPalette")
    assert any("no 'ragPalette' declaration" in f for f in check_declarations(t)), "bite 1"
    bites += 1

    # 2 — a theme drops its neutralRamp declaration
    t = clone(themes); t["apollo-supercharge"].pop("neutralRamp")
    assert any("no 'neutralRamp' declaration" in f for f in check_declarations(t)), "bite 2"
    bites += 1

    # 3 — ragPalette points at a file that does not exist
    t = clone(themes); t["apollo-legacy"]["ragPalette"] = "palettes/rag/ghost.json"
    assert any("does not resolve to a palette file" in f
               for f in check_declarations_resolve(t, palettes, colour)), "bite 3"
    bites += 1

    # 4 — neutralRamp names a family the colour store does not have
    t = clone(themes); t["apollo-mono"]["neutralRamp"] = "color/nosuch/1-15"
    assert any("does not exist in tokens/colour.json" in f
               for f in check_declarations_resolve(t, palettes, colour)), "bite 4"
    bites += 1

    # 5 — a core key silently vanishes (neither declared nor declared-absent)
    p = clone(palettes); rel = "palettes/rag/legacy.json"
    p[rel]["keys"].pop("warning-glyph")
    assert any("NEITHER declared NOR listed" in f for f in check_palette_shape(p)), "bite 5"
    bites += 1

    # 6 — a tint sneaks into a palette
    p = clone(palettes); rel = "palettes/rag/console-supercharge.json"
    p[rel]["keys"]["success-tint"] = {m: {"$value": "#D2E8DA", "$type": "color"} for m in MODES}
    p[rel]["$coreKeys"].append("success-tint")
    assert any("must not be palette-owned" in f for f in check_palette_shape(p)), "bite 6"
    bites += 1

    # 7 — the palette and an override file disagree on a hex. RE-BASED #158 (s158-D4): the
    # ratified override sets no longer HAND-CARRY palette-owned keys — Option B made the
    # palette the single source and trimmed all 36 — so this arm must re-introduce the key
    # to have anything to disagree with. That is exactly the regression it guards: a theme
    # that re-grows a divergent copy of a palette-owned rung.
    p = clone(palettes); o = clone(override_sets)
    assert "rag/error" not in (o.get("apollo-console") or {}), \
        ("bite 7 premise — apollo-console hand-carries rag/error again; s158-D4 trimmed it. "
         "Either the trim was reverted or a copy re-grew: investigate, do not re-base.")
    o["apollo-console"]["rag/error"] = {"light": {"$value": "#000000", "$type": "color"},
                                        "dark": {"$value": "#000000", "$type": "color"}}
    assert any("override set" in f for f in
               check_agreement(themes, p, base_rag, o)), "bite 7"
    # ...and the BASE arm of the same check bites too
    p = clone(palettes)
    p["palettes/rag/mono.json"]["keys"]["success-ink"]["dark"]["$value"] = "#000000"
    assert any("base store says" in f for f in
               check_agreement(themes, p, base_rag, override_sets)), "bite 7b"
    bites += 1

    # 8 — two themes given DIFFERENT palettes holding IDENTICAL values
    p = clone(palettes); t = clone(themes)
    p["palettes/rag/twin.json"] = clone(p["palettes/rag/console-supercharge.json"])
    t["apollo-supercharge"]["ragPalette"] = "palettes/rag/twin.json"
    assert any("IDENTICAL across all" in f for f in check_sharing_declared(t, p)), "bite 8"
    bites += 1

    # 9 — a consumed rung is dropped from one palette's vocabulary entirely
    p = clone(palettes); rel = "palettes/rag/legacy.json"
    p[rel]["keys"].pop("success")
    assert any("consumed by" in f for f in check_consumed_rungs(metas, p, manifests)), "bite 9"
    bites += 1

    # 10 — the SNIPPET-manifest arm. Needs a rung consumed ONLY by a manifest and by no
    # component meta, so the control below can prove the manifest grammar is load-bearing.
    # RE-BASED #158: the original subject was rag/success-ink, true at the moment this
    # gate was written and FALSE the same day — s158-D2 re-keyed amount-display's positive
    # seat onto rag.success-ink and s158-D3 did the same for negative -> rag.error-ink, so
    # the meta walk now DOES see the -ink rungs and the control could no longer fail. The
    # subject moves to rag/error-background (Banner's --err-bg; no meta binds any
    # *-background rung), which restores the control's meaning. If a meta ever binds a
    # -background rung this control will start passing for the wrong reason — re-base it
    # again against the manifest-only set, do not delete it.
    manifest_only = "error-background"
    assert not any(manifest_only in str(a)
                   for m in metas.values() for prop in m.get("props", [])
                   for a in [prop.get("binds")]), \
        (f"bite 10 premise — a component meta now binds rag/{manifest_only}; this control "
         f"needs a MANIFEST-ONLY rung, re-base it")
    p = clone(palettes); rel = "palettes/rag/console-supercharge.json"
    p[rel]["keys"].pop(manifest_only)
    hits = check_consumed_rungs(metas, p, manifests)
    assert any(f"rag/{manifest_only}" in f and "Banner" in f for f in hits), \
        f"bite 10 — manifest arm did not bite: {hits}"
    # ...and the CONTROL: with metas alone (no manifests) the same mutation is INVISIBLE.
    # This is the arm that proves the manifest grammar is load-bearing, not decorative.
    assert not any(f"rag/{manifest_only}" in f for f in check_consumed_rungs(metas, p)), \
        f"bite 10 control — meta-only walk should NOT see {manifest_only}"
    bites += 1

    print(f"palette-tier selftest OK — {bites} bites, all red when mutated")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        if "--selftest" in argv:
            return _selftest()
        return run("--strict-absence" in argv)
    except GateError as e:
        print(f"\n❌ palette-tier gate MACHINERY failure: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
