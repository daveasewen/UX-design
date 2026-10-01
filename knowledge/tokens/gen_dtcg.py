#!/usr/bin/env python3
"""
gen_dtcg.py — the ONE generator that moves Apollo's token spine to W3C DTCG 2025.10
(s311-D8, Dave 2026-10-01: "Now, one generator, extras under $extensions"; built #312 lane J).

WHAT MOVES, FILE BY FILE (knowledge/tokens/<name>.json, the ten gated base files)
  * `$alias` becomes the token's `$value` as a `{group.token}` reference — ONLY when the
    alias target resolves, in that mode, to the very hex/number the file already carried.
    An alias that disagrees with its target (there is one: primary/border/hover dark says
    color/red/700 but holds #D61412, not #BA1110) keeps its literal `$value` and the alias
    is preserved VERBATIM under `$extensions.apollo.alias`; nothing is silently re-coloured.
  * light / dark leave the path. The base file carries the LIGHT value (DTCG has no modes;
    light is the default context) and `modes/dark/<name>.json` carries the dark value of
    every token that had one. `apollo.resolver.json` (DTCG Resolver Module, 2025.10) binds
    them: set `base` = the ten files, modifier `color-scheme` = {light: [], dark: [...]}.
  * every non-standard `$` key — `$note`, `$contrast`, `$confidence`, `$label`, `$darkNote`,
    `$webStack`, `$metrics`, `$siblingSet`, … — moves under `$extensions.apollo.<key>`
    (the `$` dropped). `$description`, `$type`, `$deprecated`, `$extensions` stay where
    the spec puts them. A pre-existing vendor key under `$extensions` (`com.apollo.sds`
    from s141-D1 (B) / s217-D4, and `apollo.state` from ADR-0009) is left untouched; the
    inverse knows them by name (KEEP_IN_APOLLO) and never "restores" them as `$` keys.
  * `$type:"dimension"` strings become value objects: "16px" -> {"value": 16, "unit": "px"};
    `$type:"duration"` likewise ("120ms" -> {"value": 120, "unit": "ms"}); cubicBezier
    {x1,y1,x2,y2} becomes the spec's [x1, y1, x2, y2].

WHAT DOES NOT MOVE TODAY (named, not hidden — each is a line in the J report)
  * the three theme override sets + _themes.json (flat slash keys, marks, guards): owed as
    a `theme` modifier of the same resolver; proof 4 reports UNMEASURED until then.
  * the Figma `scale-1/2/3/1-200` leaves (DEF-FIGMA-MODES in _validate_dtcg.py): a second
    modifier, `scale`, of the same shape as `color-scheme`; not ruled today.
  * colour values stay hex strings (2025.10's colour OBJECT is a separate move; Style
    Dictionary v4 reads hex; the alpha nibble of #RRGGBBAA has no lossless object form
    without a ruling on precision).
  * knowledge/component-types.json (the ADR-0013 registry gen_canon_tokens also reads) is
    not a tokens/ file and keeps its shape; the inverse is a no-op on legacy-shaped data.

THE INVERSE IS THE PROOF AND THE SEAM. `to_legacy()` turns a DTCG base file (+ its dark
file) back into the exact pre-s311 shape; `knowledge/_dtcg_load.py` hands that view to
every reader that used to `json.load` a token file (gen_canon_tokens, gen_snippet_tokens,
gen_theme_cascade and the twenty-odd gates and audits), so the spine in canon.css and the
137 snippet theme blocks are byte-equal BY CONSTRUCTION and `_validate_tokens_dtcg.py`
re-proves it on every run. The same precedent as _dtcg_units.py (s141-D1 (A)): one seam,
at the read site, instead of twenty-five hand ports. Readers go native in phase 1.

    python3 knowledge/tokens/gen_dtcg.py               # DRY RUN: plan + round-trip verdict
    python3 knowledge/tokens/gen_dtcg.py --write        # rewrite tokens/*.json in place,
                                                       #   write modes/dark/*.json + the resolver
    python3 knowledge/tokens/gen_dtcg.py --selftest     # the bites (fold rule, mismatch, keys)
    python3 knowledge/tokens/gen_dtcg.py --receipt DIR  # compare to_legacy(current) against a
                                                       #   directory of pre-s311 files

Idempotent: running --write on files already in DTCG shape changes nothing (the forward
transform passes DTCG-shaped data through, and the writer compares bytes before writing).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # knowledge/tokens
DARK_DIR = os.path.join(HERE, "modes", "dark")
RESOLVER = os.path.join(HERE, "apollo.resolver.json")

# The ten gated base files, in the order gen_canon_tokens.py reads them. The corpus rule is
# the same as _validate_dtcg.corpus_files: tokens/*.json minus _-prefixed, EXAMPLE-, -pre-s141.
BASE_FILES = ["colour.json", "opacity.json", "semantic-colour.json", "typography.json",
              "spacing.json", "layout.json", "elevation.json", "motion.json",
              "icon-scale.json", "typography-composites.json"]

# DTCG 2025.10 reserved token/group properties. Anything else that starts with `$` is Apollo's.
STANDARD_KEYS = {"$value", "$type", "$description", "$extensions", "$deprecated"}
# Vendor sub-keys of $extensions.apollo that were ALREADY there before this move and must not
# be mistaken for a moved `$` key by the inverse. ADR-0009's state mechanism (4 tokens).
KEEP_IN_APOLLO = {"state"}
MODES = ("light", "dark")

_PX_RE = re.compile(r"^(-?\d+(?:\.\d+)?)(px|rem)$")
_DUR_RE = re.compile(r"^(-?\d+(?:\.\d+)?)(ms|s)$")
_REF_RE = re.compile(r"^\{([^{}]+)\}$")


class DtcgMoveError(RuntimeError):
    """Named refusal: the move would lose or re-colour something. Never a silent fallback."""


# ---------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------
def _num(s):
    f = float(s)
    return int(f) if f.is_integer() else f


def _is_token(node):
    return isinstance(node, dict) and "$value" in node


def _is_mode_token(node):
    """The legacy mode shape: light AND dark token children and no other non-$ child."""
    if not isinstance(node, dict) or "$value" in node:
        return False
    kids = [k for k in node if not k.startswith("$")]
    return (sorted(kids) == ["dark", "light"] and _is_token(node["light"])
            and _is_token(node["dark"]))


def slash_to_ref(path):
    """'color/neutral/15' -> '{color.neutral.15}' (segments never contain '.', asserted)."""
    segs = path.split("/")
    for s in segs:
        if "." in s or "{" in s or "}" in s:
            raise DtcgMoveError("token segment %r in %r cannot be a DTCG reference" % (s, path))
    return "{" + ".".join(segs) + "}"


def ref_to_slash(ref):
    m = _REF_RE.match(ref)
    if not m:
        raise DtcgMoveError("not a DTCG reference: %r" % (ref,))
    return m.group(1).replace(".", "/")


def is_ref(v):
    return isinstance(v, str) and bool(_REF_RE.match(v))


# ---------------------------------------------------------------------------------------
# value shapes, both directions (by $type)
# ---------------------------------------------------------------------------------------
def value_to_dtcg(val, ttype):
    if ttype == "dimension" and isinstance(val, str):
        m = _PX_RE.match(val.strip())
        if m and "%s%s" % (_num(m.group(1)), m.group(2)) == val.strip():
            return {"value": _num(m.group(1)), "unit": m.group(2)}
        return val                       # not a lossless px/rem literal: left as it was
    if ttype == "duration" and isinstance(val, str):
        m = _DUR_RE.match(val.strip())
        if m and "%s%s" % (_num(m.group(1)), m.group(2)) == val.strip():
            return {"value": _num(m.group(1)), "unit": m.group(2)}
        return val
    if ttype == "cubicBezier" and isinstance(val, dict) and set(val) == {"x1", "y1", "x2", "y2"}:
        return [val["x1"], val["y1"], val["x2"], val["y2"]]
    if ttype == "typography" and isinstance(val, dict):
        out = {}
        for k, v in val.items():
            if k in ("fontSize", "letterSpacing"):
                out[k] = value_to_dtcg(v, "dimension")
            else:
                out[k] = v
        return out
    return val


def value_to_legacy(val, ttype):
    if ttype in ("dimension", "duration") and isinstance(val, dict) and set(val) == {"value", "unit"}:
        return "%s%s" % (val["value"], val["unit"])
    if ttype == "cubicBezier" and isinstance(val, list) and len(val) == 4:
        return {"x1": val[0], "y1": val[1], "x2": val[2], "y2": val[3]}
    if ttype == "typography" and isinstance(val, dict):
        out = {}
        for k, v in val.items():
            if k in ("fontSize", "letterSpacing"):
                out[k] = value_to_legacy(v, "dimension")
            else:
                out[k] = v
        return out
    return val


# ---------------------------------------------------------------------------------------
# the spine, for alias folding and reference resolution
# ---------------------------------------------------------------------------------------
class Spine:
    """Path -> token lookup over the LEGACY shape of all base files, mode-aware.

    `files` maps name -> legacy dict. resolve('color/neutral/15', 'light') returns the
    $value a DTCG resolver would give for {color.neutral.15} in the light context.
    """

    def __init__(self, files):
        self.index = {}
        for name, doc in files.items():
            self._walk(doc, [], name)

    def _walk(self, node, path, name):
        if not isinstance(node, dict):
            return
        if _is_mode_token(node):
            self.index["/".join(path)] = (name, node)
            return
        if "$value" in node:
            self.index["/".join(path)] = (name, node)
            return
        for k, v in node.items():
            if not k.startswith("$"):
                self._walk(v, path + [k], name)

    def resolve(self, path, mode):
        hit = self.index.get(path)
        if hit is None:
            return None
        node = hit[1]
        if _is_mode_token(node):
            return node[mode]["$value"]
        return node["$value"]


# ---------------------------------------------------------------------------------------
# FORWARD: legacy -> DTCG 2025.10 (base, dark)
# ---------------------------------------------------------------------------------------
def _move_extras(node, ext, path):
    """Every non-standard `$` key of `node` -> ext[key-without-$]. Refuses a collision."""
    for k, v in node.items():
        if k.startswith("$") and k not in STANDARD_KEYS and k != "$alias":
            key = k[1:]
            if key in ext:
                raise DtcgMoveError("%s: moved key %s collides with an existing "
                                    "$extensions.apollo.%s" % ("/".join(path), k, key))
            ext[key] = copy.deepcopy(v)


def _with_ext(out, node, ext):
    """Attach `$extensions` = existing vendor keys + apollo (merged), in a stable order."""
    existing = copy.deepcopy(node.get("$extensions", {})) if isinstance(node.get("$extensions"), dict) else {}
    apollo = existing.get("apollo", {})
    if not isinstance(apollo, dict):
        raise DtcgMoveError("$extensions.apollo is not an object")
    for k, v in ext.items():
        if k in apollo:
            raise DtcgMoveError("moved key %r collides with $extensions.apollo.%s" % (k, k))
        apollo[k] = v
    if apollo:
        existing["apollo"] = apollo
    if existing:
        out["$extensions"] = existing


def _fold_alias(alias_path, literal, mode, spine):
    """Return ('{ref}', None) when the alias target resolves to `literal` in `mode`,
    else (literal, alias_path) — the alias is kept as data, the value stays literal."""
    target = spine.resolve(alias_path, mode) if spine else None
    if target is not None and target == literal:
        return slash_to_ref(alias_path), None
    return literal, alias_path


def to_dtcg(legacy, spine, name=""):
    """legacy base-file dict -> (base, dark). `dark` is None when no token had a dark leaf."""
    dark_holder = {"doc": None}

    def dark_put(path, token):
        if dark_holder["doc"] is None:
            dark_holder["doc"] = {}
        node = dark_holder["doc"]
        for seg in path[:-1]:
            node = node.setdefault(seg, {})
        node[path[-1]] = token

    def group(node, path):
        out = {}
        ext = {}
        for k, v in node.items():
            if k in ("$description", "$type", "$deprecated"):
                out[k] = copy.deepcopy(v)
            elif k.startswith("$"):
                continue                       # extras / $extensions handled below
            else:
                out[k] = convert(v, path + [k])
        _move_extras(node, ext, path)
        _with_ext(out, node, ext)
        # keep the spec keys first for readability: $description/$type, then children, then ext
        ordered = {}
        for k in ("$description", "$type", "$deprecated"):
            if k in out:
                ordered[k] = out[k]
        for k, v in out.items():
            if k not in ordered and k != "$extensions":
                ordered[k] = v
        if "$extensions" in out:
            ordered["$extensions"] = out["$extensions"]
        return ordered

    def token(node, path):
        ttype = node.get("$type")
        out = {}
        ext = {}
        val = node["$value"]
        alias = node.get("$alias")
        if isinstance(alias, str):
            val, kept = _fold_alias(alias, val, "light", spine)
            if kept is not None:
                ext["alias"] = kept
        elif alias is not None:
            raise DtcgMoveError("%s: modeless token with a non-string $alias" % "/".join(path))
        out["$value"] = value_to_dtcg(val, ttype) if not is_ref(val) else val
        if "$type" in node:
            out["$type"] = node["$type"]
        if "$description" in node:
            out["$description"] = node["$description"]
        if "$deprecated" in node:
            out["$deprecated"] = node["$deprecated"]
        _move_extras(node, ext, path)
        _with_ext(out, node, ext)
        return out

    def mode_token(node, path):
        light, darkleaf = node["light"], node["dark"]
        for m, leaf in (("light", light), ("dark", darkleaf)):
            extra = [k for k in leaf if k not in ("$value", "$type")]
            if extra:
                raise DtcgMoveError("%s.%s carries %s on the mode leaf — not a shape this "
                                    "generator moves" % ("/".join(path), m, extra))
        alias = node.get("$alias")
        if alias is not None and not isinstance(alias, dict):
            raise DtcgMoveError("%s: mode token with a non-dict $alias" % "/".join(path))
        alias = alias or {}
        kept_alias = {}
        lv, lk = _fold_alias(alias["light"], light["$value"], "light", spine) if "light" in alias else (light["$value"], None)
        dv, dk = _fold_alias(alias["dark"], darkleaf["$value"], "dark", spine) if "dark" in alias else (darkleaf["$value"], None)
        if lk is not None:
            kept_alias["light"] = lk
        if dk is not None:
            kept_alias["dark"] = dk
        # base = light
        out = {"$value": lv}
        if "$type" in light:
            out["$type"] = light["$type"]
        if "$description" in node:
            out["$description"] = node["$description"]
        if "$deprecated" in node:
            out["$deprecated"] = node["$deprecated"]
        ext = {}
        if kept_alias:
            ext["alias"] = kept_alias
        _move_extras(node, ext, path)
        _with_ext(out, node, ext)
        # dark context
        dtok = {"$value": dv}
        if "$type" in darkleaf:
            dtok["$type"] = darkleaf["$type"]
        dark_put(path, dtok)
        return out

    def convert(node, path):
        if not isinstance(node, dict):
            return copy.deepcopy(node)             # Figma scale-N scalar leaf: untouched today
        if _is_mode_token(node):
            return mode_token(node, path)
        if "$value" in node:
            return token(node, path)
        return group(node, path)

    base = group(legacy, [])
    dark = dark_holder["doc"]
    if dark is not None:
        dark = {"$description": "Dark colour-scheme context for %s — the DTCG 2025.10 resolver "
                                "(knowledge/tokens/apollo.resolver.json, modifier color-scheme) "
                                "lays these over the base set. One token per entry that carried "
                                "a dark value before s311-D8; every other token keeps its base "
                                "(light) value in dark." % (name or "the base file"), **dark}
    return base, dark


# ---------------------------------------------------------------------------------------
# INVERSE: DTCG 2025.10 (base, dark) -> legacy
# ---------------------------------------------------------------------------------------
class DtcgResolver:
    """Reference resolution over DTCG-shaped files: base set + the dark context."""

    def __init__(self, bases, darks):
        self.base = {}
        self.dark = {}
        for name, doc in bases.items():
            self._walk(doc, [], self.base)
        for name, doc in darks.items():
            if doc is not None:
                self._walk(doc, [], self.dark)

    def _walk(self, node, path, index):
        if not isinstance(node, dict):
            return
        if "$value" in node:
            index["/".join(path)] = node
            return
        for k, v in node.items():
            if not k.startswith("$"):
                self._walk(v, path + [k], index)

    def resolve(self, ref, mode, _depth=0):
        if _depth > 16:
            raise DtcgMoveError("reference loop at %r" % ref)
        path = ref_to_slash(ref)
        node = None
        if mode == "dark":
            node = self.dark.get(path)
        if node is None:
            node = self.base.get(path)
        if node is None:
            raise DtcgMoveError("reference %s resolves to nothing in the spine" % ref)
        val = node["$value"]
        if is_ref(val):
            return self.resolve(val, mode, _depth + 1)
        return value_to_legacy(val, node.get("$type"))


def _split_ext(node):
    """-> (moved: {'$key': v}, remaining $extensions or None)."""
    ext = node.get("$extensions")
    if not isinstance(ext, dict):
        return {}, None
    ext = copy.deepcopy(ext)
    apollo = ext.get("apollo")
    moved = {}
    if isinstance(apollo, dict):
        for k in list(apollo):
            if k in KEEP_IN_APOLLO:
                continue
            moved["$" + k] = apollo.pop(k)
        if not apollo:
            ext.pop("apollo")
    return moved, (ext or None)


def to_legacy(base, dark, resolver):
    """(base, dark, resolver) -> the pre-s311 shape. No-op on data that was never moved."""
    def dark_node(path):
        node = dark
        for seg in path:
            if not isinstance(node, dict) or seg not in node:
                return None
            node = node[seg]
        return node if _is_token(node) else None

    def token(node, path):
        ttype = node.get("$type")
        moved, ext = _split_ext(node)
        alias_kept = moved.pop("$alias", None)
        # every `$` key the node still carries (legacy-shaped data, or a standard key) passes
        # through verbatim — the inverse is a NO-OP on data that was never moved.
        passthru = {k: copy.deepcopy(v) for k, v in node.items()
                    if k.startswith("$") and k not in ("$value", "$extensions")}
        dnode = dark_node(path) if dark is not None else None
        if dnode is not None:
            # a mode token: light = base, dark = the context file
            out = {}
            if "$deprecated" in passthru:
                out["$deprecated"] = passthru.pop("$deprecated")
            lval = node["$value"]
            dval = dnode["$value"]
            alias = {}
            if is_ref(lval):
                alias["light"] = ref_to_slash(lval)
                lval = resolver.resolve(lval, "light")
            else:
                lval = value_to_legacy(lval, ttype)
            if is_ref(dval):
                alias["dark"] = ref_to_slash(dval)
                dval = resolver.resolve(dval, "dark")
            else:
                dval = value_to_legacy(dval, dnode.get("$type"))
            light = {"$value": lval}
            if "$type" in node:
                light["$type"] = passthru.pop("$type")
            darkleaf = {"$value": dval}
            if "$type" in dnode:
                darkleaf["$type"] = dnode["$type"]
            out["light"] = light
            out["dark"] = darkleaf
            if isinstance(alias_kept, dict):
                alias.update(alias_kept)
            if alias:
                out["$alias"] = {m: alias[m] for m in MODES if m in alias}
            for k, v in moved.items():
                out[k] = v
            for k, v in passthru.items():
                out[k] = v
            if ext:
                out["$extensions"] = ext
            return out
        out = {}
        val = node["$value"]
        if is_ref(val):
            out["$value"] = resolver.resolve(val, "light")
            alias = ref_to_slash(val)
        else:
            out["$value"] = value_to_legacy(val, ttype)
            alias = alias_kept
        for k in ("$type", "$description", "$deprecated"):
            if k in passthru:
                out[k] = passthru.pop(k)
        if alias is not None:
            out["$alias"] = alias
        for k, v in moved.items():
            out[k] = v
        for k, v in passthru.items():
            out[k] = v
        if ext:
            out["$extensions"] = ext
        return out

    def group(node, path):
        out = {}
        moved, ext = _split_ext(node)
        for k, v in node.items():
            if k == "$extensions":
                continue
            if k.startswith("$"):
                out[k] = copy.deepcopy(v)
            elif isinstance(v, dict):
                out[k] = token(v, path + [k]) if "$value" in v else group(v, path + [k])
            else:
                out[k] = copy.deepcopy(v)
        for k, v in moved.items():
            out[k] = v
        if ext:
            out["$extensions"] = ext
        return out

    return group(base, [])


# ---------------------------------------------------------------------------------------
# files
# ---------------------------------------------------------------------------------------
def dumps(doc):
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dark_path_for(base_path):
    return os.path.join(os.path.dirname(os.path.abspath(base_path)), "modes", "dark",
                        os.path.basename(base_path))


def resolver_doc(dark_names):
    return {
        "$schema": "https://www.designtokens.org/schemas/2025.10/resolver.json",
        "name": "Apollo token spine",
        "version": "2025.10",
        "description": ("DTCG Resolver Module for knowledge/tokens (s311-D8, #312). The base set "
                        "is the ten gated files; the color-scheme modifier lays modes/dark/*.json "
                        "over it for dark. Light is the default context and adds nothing. OWED, "
                        "named in notes/_subreports/2026-10-01-312-J-tokens-dtcg.md: a `theme` "
                        "modifier (console / legacy / supercharge from themes/*.overrides.json) "
                        "and a `scale` modifier for the Figma scale-1/2/3/1-200 leaves."),
        "sets": {
            "base": {
                "description": "The Apollo spine: primitives, semantic colour (light), typography, "
                               "spacing, layout, elevation, motion, opacity, icon scale, composites.",
                "sources": [{"$ref": n} for n in BASE_FILES],
            }
        },
        "modifiers": {
            "color-scheme": {
                "description": "light (default, no sources) or dark.",
                "contexts": {
                    "light": [],
                    "dark": [{"$ref": "modes/dark/" + n} for n in dark_names],
                },
                "default": "light",
            }
        },
        "resolutionOrder": [{"$ref": "#/sets/base"}, {"$ref": "#/modifiers/color-scheme"}],
    }


def plan(tokdir=HERE):
    """Compute the move for every base file. Returns {name: (legacy, base, dark)} + stats."""
    files = {n: load(os.path.join(tokdir, n)) for n in BASE_FILES if os.path.exists(os.path.join(tokdir, n))}
    # the spine for alias folding is the LEGACY view of everything, which is what the files
    # are before the move and what to_legacy() gives after it (idempotence).
    existing_darks = {}
    for n in files:
        dp = os.path.join(tokdir, "modes", "dark", n)
        existing_darks[n] = load(dp) if os.path.exists(dp) else None
    pre_resolver = DtcgResolver(files, existing_darks)
    legacy = {n: to_legacy(files[n], existing_darks[n], pre_resolver) for n in files}
    spine = Spine(legacy)
    out = {}
    for n in files:
        base, dark = to_dtcg(legacy[n], spine, n)
        out[n] = (legacy[n], base, dark)
    return out


def _count_dollar(doc):
    """(moved-candidate keys, refs, mode tokens) over a legacy doc — for the dry-run report."""
    c = {"extra": 0, "alias": 0, "modes": 0, "dims": 0}

    def w(node):
        if not isinstance(node, dict):
            return
        if _is_mode_token(node):
            c["modes"] += 1
        for k, v in node.items():
            if k == "$alias":
                c["alias"] += 1
            elif k.startswith("$") and k not in STANDARD_KEYS:
                c["extra"] += 1
            if k == "$type" and v in ("dimension", "duration") and isinstance(node.get("$value"), str):
                c["dims"] += 1
            if not k.startswith("$") or k == "$extensions":
                w(v)
    w(doc)
    return c


def run(write=False, tokdir=HERE, quiet=False):
    moves = plan(tokdir)
    bases = {n: b for n, (_l, b, _d) in moves.items()}
    darks = {n: d for n, (_l, _b, d) in moves.items()}
    resolver = DtcgResolver(bases, darks)
    bad = []
    changed = []
    for n, (legacy, base, dark) in moves.items():
        back = to_legacy(base, dark, resolver)
        if back != legacy:
            bad.append(n)
        c = _count_dollar(legacy)
        if not quiet:
            print("  %-28s %3d mode tokens -> modes/dark · %3d $alias -> refs/ext · "
                  "%3d extra $keys -> $extensions.apollo · %3d dims/durations -> objects · "
                  "round-trip %s" % (n, c["modes"], c["alias"], c["extra"], c["dims"],
                                     "OK" if back == legacy else "FAIL"))
        for path, doc in ((os.path.join(tokdir, n), base), (dark_path_for(os.path.join(tokdir, n)), dark)):
            if doc is None:
                continue
            new = dumps(doc)
            old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
            if old != new:
                changed.append(path)
                if write:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(new)
    dark_names = [n for n in BASE_FILES if darks.get(n) is not None]
    rdoc = dumps(resolver_doc(dark_names))
    rpath = os.path.join(tokdir, "apollo.resolver.json")
    if (open(rpath, encoding="utf-8").read() if os.path.exists(rpath) else None) != rdoc:
        changed.append(rpath)
        if write:
            with open(rpath, "w", encoding="utf-8") as fh:
                fh.write(rdoc)
    if bad:
        raise DtcgMoveError("round-trip FAILED for %s — nothing written" % ", ".join(bad))
    if not quiet:
        print("%s %d file(s)%s" % ("WROTE" if write else "DRY RUN — would write",
                                   len(changed), ":" if changed else " (already in DTCG shape)."))
        for p in changed:
            print("    " + os.path.relpath(p, os.path.dirname(tokdir)))
        if not write and changed:
            print("  --write to land. Nothing was written.")
    return changed


def receipt(fixture_dir, tokdir=HERE):
    """Compare to_legacy(current files) against a directory of pre-s311 files, by parse."""
    moves = plan(tokdir)
    bases = {n: b for n, (_l, b, _d) in moves.items()}
    darks = {n: d for n, (_l, _b, d) in moves.items()}
    resolver = DtcgResolver(bases, darks)
    ok = 0
    fails = []
    for n in BASE_FILES:
        fp = os.path.join(fixture_dir, n)
        if not os.path.exists(fp):
            fails.append("%s: no fixture" % n)
            continue
        fixture = load(fp)
        back = to_legacy(bases[n], darks[n], resolver)
        if back == fixture:
            ok += 1
        else:
            fails.append("%s: to_legacy(current) != fixture" % n)
    print("receipt: %d/%d files equal their pre-s311 fixture (by parse)" % (ok, len(BASE_FILES)))
    for f in fails:
        print("  FAIL " + f)
    return 0 if not fails else 1


# ---------------------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------------------
def selftest():
    prim = {"color": {"neutral": {"15": {"$value": "#FFFFFF", "$type": "color"},
                                  "4": {"$value": "#1A1A1A", "$type": "color"}},
                      "red": {"700": {"$value": "#BA1110", "$type": "color"}}}}
    sem = {"$description": "sem", "$siblingSet": "x",
           "background": {"$note": "group note",
                          "default": {"light": {"$value": "#FFFFFF", "$type": "color"},
                                      "dark": {"$value": "#1A1A1A", "$type": "color"},
                                      "$alias": {"light": "color/neutral/15", "dark": "color/neutral/4"},
                                      "$note": "n", "$contrast": {"a": 1},
                                      "$extensions": {"apollo": {"state": {"mechanism": ["colour"]}}}},
                          "bad": {"light": {"$value": "#D61412", "$type": "color"},
                                  "dark": {"$value": "#D61412", "$type": "color"},
                                  "$alias": {"light": "color/red/700", "dark": "color/red/700"}}},
           "radius": {"role": {"$value": 4, "$type": "number", "$alias": "radius/default"},
                      "default": {"$value": 4, "$type": "number"}},
           "gap": {"$value": "16px", "$type": "dimension", "$label": "g"},
           "dur": {"$value": "120ms", "$type": "duration"},
           "ease": {"$value": {"x1": 0.4, "y1": 0, "x2": 0.2, "y2": 1}, "$type": "cubicBezier"}}
    spine = Spine({"colour.json": prim, "semantic-colour.json": sem})
    base, dark = to_dtcg(sem, spine, "semantic-colour.json")
    # bite 1: alias folds to a reference when it resolves to the same value
    assert base["background"]["default"]["$value"] == "{color.neutral.15}", base["background"]["default"]
    assert dark["background"]["default"]["$value"] == "{color.neutral.4}"
    # bite 2: a disagreeing alias stays literal + kept under $extensions.apollo.alias
    assert base["background"]["bad"]["$value"] == "#D61412"
    assert base["background"]["bad"]["$extensions"]["apollo"]["alias"] == {"light": "color/red/700", "dark": "color/red/700"}
    # bite 3: extras moved, standard keys kept, pre-existing apollo.state kept
    e = base["background"]["default"]["$extensions"]["apollo"]
    assert e["note"] == "n" and e["contrast"] == {"a": 1} and e["state"] == {"mechanism": ["colour"]}, e
    assert base["background"]["$extensions"]["apollo"]["note"] == "group note"
    assert base["$extensions"]["apollo"]["siblingSet"] == "x" and base["$description"] == "sem"
    # bite 4: value objects
    assert base["gap"]["$value"] == {"value": 16, "unit": "px"}
    assert base["dur"]["$value"] == {"value": 120, "unit": "ms"}
    assert base["ease"]["$value"] == [0.4, 0, 0.2, 1]
    assert base["radius"]["role"]["$value"] == "{radius.default}"
    # bite 5: no non-standard $ key survives anywhere in base or dark
    def keys(node, acc):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.startswith("$"):
                    acc.add(k)
                if k != "$extensions":
                    keys(v, acc)
    acc = set()
    keys(base, acc)
    keys(dark, acc)
    assert acc <= STANDARD_KEYS, acc - STANDARD_KEYS
    # bite 6: the inverse is exact
    pb, _ = to_dtcg(prim, spine, "colour.json")
    res = DtcgResolver({"colour.json": pb, "semantic-colour.json": base}, {"semantic-colour.json": dark})
    back = to_legacy(base, dark, res)
    assert back == sem, json.dumps(back, indent=1)
    assert to_legacy(pb, None, res) == prim
    # bite 7: a moved key made unrecoverable (deleted from $extensions) is a round-trip FAIL
    mut = copy.deepcopy(base)
    del mut["background"]["default"]["$extensions"]["apollo"]["note"]
    assert to_legacy(mut, dark, res) != sem
    # bite 8: a collision between a moved key and an existing vendor key REFUSES
    coll = copy.deepcopy(sem)
    coll["background"]["default"]["$extensions"]["apollo"]["note"] = "already here"
    try:
        to_dtcg(coll, spine)
        raise AssertionError("bite 8: collision did not refuse")
    except DtcgMoveError:
        pass
    # bite 9: idempotent — forward on an already-moved file is the same file
    res2 = DtcgResolver({"colour.json": pb, "semantic-colour.json": base}, {"semantic-colour.json": dark})
    again, dagain = to_dtcg(to_legacy(base, dark, res2), spine, "semantic-colour.json")
    assert again == base and dagain == dark
    print("gen_dtcg selftest OK (9 bites: fold · mismatch stays literal · extras+state · value "
          "objects · no stray $keys · exact inverse · unrecoverable key FAILS · collision "
          "REFUSES · idempotent)")


KNOWN_FLAGS = ("--write", "--selftest", "--receipt", "--quiet")

if __name__ == "__main__":
    args = sys.argv[1:]
    unknown = [a for a in args if a.startswith("-") and a not in KNOWN_FLAGS]
    if unknown:
        print("gen_dtcg: unknown argument(s) %s — nothing was written. Known: %s"
              % (", ".join(unknown), ", ".join(KNOWN_FLAGS)), file=sys.stderr)
        sys.exit(2)
    if "--selftest" in args:
        selftest()
        sys.exit(0)
    if "--receipt" in args:
        i = args.index("--receipt")
        if i + 1 >= len(args):
            print("gen_dtcg: --receipt needs a directory of pre-s311 files", file=sys.stderr)
            sys.exit(2)
        sys.exit(receipt(args[i + 1]))
    try:
        run(write="--write" in args, quiet="--quiet" in args)
    except DtcgMoveError as e:
        print("REFUSED (gen_dtcg): %s" % e, file=sys.stderr)
        sys.exit(1)
