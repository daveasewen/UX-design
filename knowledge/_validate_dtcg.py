#!/usr/bin/env python3
"""_validate_dtcg.py — the DTCG WIRE-FORMAT gate (s136-D1 axis A, wire-format clause).

s136-D1 (Dave, #136): "token spine wire format = W3C DTCG (stable Oct 2025)."
Until a rule is gated, assume it will be broken. This is the first gate that PARSES
the token spine IN THE CONSUMER'S GRAMMAR — i.e. it reads the files the way a DTCG
tool would, not the way a JSON linter would. A file can be perfect JSON and still be
illegal DTCG; that is exactly the class this gate exists to catch.

CORPUS
  knowledge/tokens/*.json  — excluding _-prefixed files (raw/working/sibling sets),
  EXAMPLE-*.json (teaching fixtures), and tokens/_proposals/ (not promoted).
  The excluded set is REPORTED at the end so the scope is visible, never silent.

CHECKS (blocking unless listed as a DEFERRAL below)
  DTCG-001  $type is a legal DTCG type. The legal set is the spec's, hardcoded and
            named below — "other" and "string" are NOT DTCG types.
  DTCG-002  every token (any node carrying $value) has a resolvable $type, either its
            own or inherited from the nearest ancestor group that declares one.
  DTCG-003  every alias reference "{a.b.c}" RESOLVES to a real node in the spine —
            cross-file, because the spine is one namespace split over files. A group
            with mode children (light/dark, scale-N) is a legal alias target; a path
            that hits nothing is a failure.
  DTCG-004  $type:"color" values are a hex string (#RGB/#RGBA/#RRGGBB/#RRGGBBAA) or a
            pure alias. Anything else (a bare number, a colour function, prose) fails.
  DTCG-005  value SHAPE matches $type: number->number, dimension/duration->string with
            a unit, cubicBezier->4 numbers, typography->object whose keys are all legal
            DTCG typography sub-values and which carries at least fontSize+fontWeight.

DEFERRALS — declared, named, non-blocking by default; BLOCKING under --strict.
  A deferral is not an exemption. Each one names a decision that belongs to Dave and
  must not be guessed by a gate or by an agent. They are printed on every run, so the
  debt cannot go quiet. --strict turns every deferral into a failure: that is the flag
  for the day the deferred decisions are ruled.
    DEF-COLOR-MISTYPE       8 nodes in semantic-colour.json are $type:"color" with an
                            integer $value (blur radii in px, image opacities in %).
                            Plainly the wrong $type, but the RIGHT $type (dimension?
                            number? a new blur token group?) is Dave's call.
    DEF-COMPONENT-LINEHEIGHT the Component composites carry no lineHeight — they are
                            seated by cap-trim into a 4px slot. Strict DTCG wants the
                            key; inventing a value would be inventing design intent.
    DEF-FIGMA-MODES         mode-keyed nodes (a $type, no $value, children scale-1/2/3
                            or scale-1-200) are the Figma variable-mode shape. DTCG has
                            no modes; the resolver treats them as alias-able groups.

RULED AND ENACTED — s141-D1 (Dave, #141). Two deferrals were retired here, not silenced:
    DEF-LAYOUT-SCALE      -> s141-D1 (B) DIMENSION-PLUS-EXTENSIONS. layout.json
                             scale.scale-{1,2,3} now carry the scale's min-width entry
                             viewport as $type:"dimension", with the breakpoint set
                             preserved VERBATIM under $extensions["com.apollo.sds"].
                             DTCG-001/005 gate them normally now; no deferral remains.
    DEF-NUMBER-DIMENSION  -> s141-D1 (A) MIGRATE-TICKED. All 104 unitless px number
                             tokens were migrated to $type:"dimension" with a "Npx"
                             string $value. The detector is KEPT and PROMOTED from a
                             deferral to a blocking check (DTCG-006) so the ruling
                             cannot silently regress: a NEW unitless number token
                             holding a px quantity is now a failure, not a note.

CSS KEYWORDS ARE NOT TOKENS — s217-D4 (Dave, #217), ds-051. `row dense` (grid-auto-flow) has
    NO legal W3C DTCG type, and there is no honest numeric or dimensional stand-in; minted as
    $type:"string" it was a guaranteed DTCG-001 failure (it blocked the build gate at the #217
    commit seam). Dave ruled the s141-D1 (B) PRECEDENT rather than a new deferral class or a
    validator exception: the keyword is preserved VERBATIM under $extensions["com.apollo.sds"]
    ["cssKeyword"] and the node carries NO $value — so it is a GROUP, and this gate correctly
    has no opinion about it. ⚠ NOTHING IS SILENCED HERE: no deferral was added, no path was
    exempted, and a keyword re-minted as a $type:"string" TOKEN still fails DTCG-001 exactly
    as before. The keyword still reaches CSS — canon/gen_canon_tokens.py reads the cssKeyword
    carrier and emits the var (canon.css was byte-identical across the move).

CHECKS (continued)
  DTCG-006  a $type:"number" token holding an integer px quantity (same conservative
            detector as before: named non-px exclusions only) is a FAILURE — s141-D1 (A).

FAILURE STYLE
  Loud and NAMED: "FAIL <check-id>  <file> :: <token.path> :: <why>". A crash is not a
  fail — every helper raises a named DtcgError with the file and path in the message, so
  an unreadable file is reported as an unreadable file and never as a clean run.

Usage:  python3 knowledge/_validate_dtcg.py            # gate mode
        python3 knowledge/_validate_dtcg.py --strict   # deferrals become failures
        python3 knowledge/_validate_dtcg.py --json     # machine-readable result
        python3 knowledge/_validate_dtcg.py --corpus DIR
Exit non-zero on any failure.
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


class DtcgError(Exception):
    """A named failure of this gate's own machinery (not a token failure)."""


# ---- the W3C DTCG type set (stable, Oct 2025). Hardcoded on purpose: the gate must
# ---- state the standard it enforces, not infer it from the data it is judging.
LEGAL_TYPES = {
    "color", "dimension", "fontFamily", "fontWeight", "duration", "cubicBezier",
    "number", "strokeStyle", "border", "transition", "shadow", "gradient", "typography",
}
TYPOGRAPHY_SUBVALUES = {"fontFamily", "fontSize", "fontWeight", "letterSpacing", "lineHeight"}
TYPOGRAPHY_REQUIRED = {"fontSize", "fontWeight"}

ALIAS_RE = re.compile(r"^\{([^{}]+)\}$")
ALIAS_ANY_RE = re.compile(r"\{([^{}]+)\}")
HEX_RE = re.compile(r"^#(?:[0-9A-Fa-f]{3,4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
DIMENSION_RE = re.compile(r"^-?\d+(?:\.\d+)?(px|rem|em|%|vh|vw|ch)$")
DURATION_RE = re.compile(r"^-?\d+(?:\.\d+)?(ms|s)$")
MODE_KEYS = {"scale-1", "scale-2", "scale-3", "scale-1-200", "light", "dark"}

# ---- named deferrals: (id, predicate on (file, path, node)) --------------------------
DEF_COLOR_MISTYPE = "DEF-COLOR-MISTYPE"
DEF_COMPONENT_LINEHEIGHT = "DEF-COMPONENT-LINEHEIGHT"
DEF_FIGMA_MODES = "DEF-FIGMA-MODES"
# DEF-LAYOUT-SCALE and DEF-NUMBER-DIMENSION were RULED AND ENACTED by s141-D1 and are
# deliberately absent: see the module docstring. Do not re-add them as deferrals.

DEFERRED_PATHS = {
    ("semantic-colour.json", "blur.overlay.light"): DEF_COLOR_MISTYPE,
    ("semantic-colour.json", "blur.overlay.dark"): DEF_COLOR_MISTYPE,
    ("semantic-colour.json", "blur.background-surface.light"): DEF_COLOR_MISTYPE,
    ("semantic-colour.json", "blur.background-surface.dark"): DEF_COLOR_MISTYPE,
    ("semantic-colour.json", "image.opacity.default.light"): DEF_COLOR_MISTYPE,
    ("semantic-colour.json", "image.opacity.default.dark"): DEF_COLOR_MISTYPE,
    ("semantic-colour.json", "image.opacity.disabled.light"): DEF_COLOR_MISTYPE,
    ("semantic-colour.json", "image.opacity.disabled.dark"): DEF_COLOR_MISTYPE,
}


def corpus_files(root):
    """The gated spine. Returns (included, excluded) — both, so scope is never silent."""
    tokdir = os.path.join(root, "tokens")
    if not os.path.isdir(tokdir):
        raise DtcgError("token corpus not found: %s" % tokdir)
    inc, exc = [], []
    for p in sorted(glob.glob(os.path.join(tokdir, "*.json"))):
        b = os.path.basename(p)
        if b.startswith("_") or b.startswith("EXAMPLE-") or b.endswith("-pre-s141.json"):
            exc.append(b)
        else:
            inc.append(p)
    if not inc:
        raise DtcgError("token corpus is EMPTY after exclusions — refusing to report a clean run")
    return inc, exc


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as e:
        raise DtcgError("unreadable token file %s :: %s" % (path, e))
    except json.JSONDecodeError as e:
        raise DtcgError("token file %s is not JSON :: line %d col %d :: %s"
                        % (path, e.lineno, e.colno, e.msg))


def is_group(node):
    return isinstance(node, dict) and "$value" not in node


def walk(node, path, file_name, inherited_type, out_tokens, out_groups):
    """Collect (path -> node) for tokens and for groups. Named failure on a bad shape."""
    if not isinstance(node, dict):
        raise DtcgError("%s :: %s :: expected an object, got %s"
                        % (file_name, ".".join(path) or "<root>", type(node).__name__))
    own = node.get("$type", inherited_type)
    if "$value" in node:
        out_tokens[".".join(path)] = (node, own)
        return
    if path:
        out_groups[".".join(path)] = (node, own)
    for key, child in node.items():
        if key.startswith("$"):
            continue
        if isinstance(child, dict):
            walk(child, path + [key], file_name, own, out_tokens, out_groups)
        else:
            # a scalar leaf under a group: the Figma mode shape (scale-1: 16). Recorded
            # as a resolvable path so aliases to it work; typed by the parent's $type.
            out_tokens[".".join(path + [key])] = ({"$value": child, "$modeLeaf": True}, own)


def build_spine(files):
    tokens, groups, per_file = {}, {}, {}
    for p in files:
        b = os.path.basename(p)
        t, g = {}, {}
        walk(load(p), [], b, None, t, g)
        per_file[b] = (t, g)
        for k, v in t.items():
            tokens.setdefault(k, (b,) + v)
        for k, v in g.items():
            groups.setdefault(k, (b,) + v)
    return tokens, groups, per_file


def check(root, strict=False):
    files, excluded = corpus_files(root)
    tokens, groups, per_file = build_spine(files)
    fails, deferrals, notes = [], [], []
    number_dimension_rows = []

    def fail(cid, f, path, why):
        fails.append({"check": cid, "file": f, "path": path, "why": why})

    def defer(did, f, path, why):
        deferrals.append({"deferral": did, "file": f, "path": path, "why": why})

    def resolve(ref):
        return ref in tokens or ref in groups

    for f, (toks, grps) in per_file.items():
        # DEF-FIGMA-MODES: groups that declare a $type but have only mode children
        for path, (node, _t) in grps.items():
            kids = {k for k in node if not k.startswith("$")}
            if "$type" in node and kids and kids <= MODE_KEYS:
                defer(DEF_FIGMA_MODES, f, path,
                      "mode-keyed node (%s) — Figma variable modes, no DTCG equivalent"
                      % ",".join(sorted(kids)))

        for path, (node, eff_type) in toks.items():
            deferred_as = DEFERRED_PATHS.get((f, path))
            value = node.get("$value")

            # ---- DTCG-002 : a resolvable $type
            if eff_type is None:
                fail("DTCG-002", f, path, "token has $value but no $type (own or inherited)")
                continue

            # ---- DTCG-001 : the $type is legal
            if eff_type not in LEGAL_TYPES:
                msg = '$type "%s" is not a W3C DTCG type' % eff_type
                if deferred_as:
                    defer(deferred_as, f, path, msg)
                else:
                    fail("DTCG-001", f, path, msg)
                continue

            # ---- DTCG-003 : alias references resolve (anywhere inside the value)
            bad_alias = False
            for ref in _alias_refs(value):
                if not resolve(ref):
                    fail("DTCG-003", f, path, 'alias "{%s}" resolves to nothing in the spine' % ref)
                    bad_alias = True
            if bad_alias:
                continue

            if _is_pure_alias(value):
                continue  # an alias inherits its target's shape; DTCG-003 already proved it

            # ---- DTCG-004 : colour values
            if eff_type == "color":
                if not (isinstance(value, str) and HEX_RE.match(value)):
                    msg = "color $value is not a hex string or alias: %r" % (value,)
                    if deferred_as:
                        defer(deferred_as, f, path, msg)
                    else:
                        fail("DTCG-004", f, path, msg)
                continue

            # ---- DTCG-005 : shape matches type
            if eff_type == "number":
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    fail("DTCG-005", f, path, "number $value is not numeric: %r" % (value,))
                elif _looks_like_px(f, path, value):
                    # DTCG-006 (s141-D1 (A), RULED AND ENACTED): a unitless number token
                    # holding a px quantity is now a FAILURE, not a deferral. Mode leaves
                    # (….scale-1) roll up to their parent token so one token = one row.
                    head = path.rsplit(".", 1)
                    row_path = head[0] if len(head) == 2 and head[1] in MODE_KEYS else path
                    if not any(r["file"] == f and r["path"] == row_path for r in number_dimension_rows):
                        number_dimension_rows.append({"file": f, "path": row_path, "value": value})
                        fail("DTCG-006", f, row_path,
                             'unitless $type:"number" holds a px quantity (%r) — s141-D1 (A) '
                             'requires $type:"dimension" with a "Npx" $value' % (value,))
            elif eff_type == "dimension":
                if not (isinstance(value, str) and DIMENSION_RE.match(value)):
                    fail("DTCG-005", f, path, "dimension $value has no legal unit: %r" % (value,))
            elif eff_type == "duration":
                if not (isinstance(value, str) and DURATION_RE.match(value)):
                    fail("DTCG-005", f, path, "duration $value has no ms/s unit: %r" % (value,))
            elif eff_type == "cubicBezier":
                ok = isinstance(value, list) and len(value) == 4 and all(
                    isinstance(x, (int, float)) and not isinstance(x, bool) for x in value)
                if not ok:
                    # this spine stores cubicBezier as {x1,y1,x2,y2} — accept that shape too,
                    # but only when all four are present and numeric.
                    ok = isinstance(value, dict) and set(value) >= {"x1", "y1", "x2", "y2"} and all(
                        isinstance(value[k], (int, float)) for k in ("x1", "y1", "x2", "y2"))
                if not ok:
                    fail("DTCG-005", f, path, "cubicBezier $value is not 4 numbers: %r" % (value,))
            elif eff_type == "typography":
                if not isinstance(value, dict):
                    fail("DTCG-005", f, path, "typography $value is not an object: %r" % (value,))
                    continue
                illegal = set(value) - TYPOGRAPHY_SUBVALUES
                if illegal:
                    fail("DTCG-005", f, path,
                         "typography $value has non-DTCG sub-values: %s" % ",".join(sorted(illegal)))
                missing_required = TYPOGRAPHY_REQUIRED - set(value)
                if missing_required:
                    fail("DTCG-005", f, path,
                         "typography $value missing required %s" % ",".join(sorted(missing_required)))
                missing_soft = TYPOGRAPHY_SUBVALUES - set(value) - TYPOGRAPHY_REQUIRED
                if missing_soft:
                    defer(DEF_COMPONENT_LINEHEIGHT, f, path,
                          "typography $value omits %s — supplying one is a design decision"
                          % ",".join(sorted(missing_soft)))
            elif eff_type in ("fontFamily", "fontWeight", "strokeStyle"):
                pass  # string/number/keyword forms all legal; nothing further to assert

    notes.append("corpus: %d files gated, %d excluded (%s)"
                 % (len(files), len(excluded), ", ".join(excluded) or "none"))
    notes.append("spine: %d tokens, %d groups" % (len(tokens), len(groups)))

    if strict:
        for d in deferrals:
            fails.append({"check": "STRICT:" + d["deferral"], "file": d["file"],
                          "path": d["path"], "why": d["why"]})
        deferrals = []
    return {"fails": fails, "deferrals": deferrals, "notes": notes,
            "numberDimensionRows": number_dimension_rows,
            "tokenCount": len(tokens), "files": [os.path.basename(f) for f in files]}


def _alias_refs(value):
    if isinstance(value, str):
        return ALIAS_ANY_RE.findall(value)
    if isinstance(value, dict):
        out = []
        for v in value.values():
            out += _alias_refs(v)
        return out
    if isinstance(value, list):
        out = []
        for v in value:
            out += _alias_refs(v)
        return out
    return []


def _is_pure_alias(value):
    return isinstance(value, str) and bool(ALIAS_RE.match(value))


_NON_PX_NUMBER = ("opacity", "alpha", "columns", "font-weight", "easing", "motion.press")


def _looks_like_px(f, path, value):
    """A number token that is really a px quantity. Conservative: named exclusions only."""
    if any(s in path for s in _NON_PX_NUMBER) or f == "opacity.json":
        return False
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    return float(value).is_integer() or f in ("typography.json",)


def main():
    ap = argparse.ArgumentParser(description="DTCG wire-format gate (s136-D1 axis A)")
    ap.add_argument("--strict", action="store_true",
                    help="treat every named deferral as a failure (for the day they are ruled)")
    ap.add_argument("--json", action="store_true", help="machine-readable result on stdout")
    ap.add_argument("--corpus", default=HERE, help="knowledge/ root to gate")
    a = ap.parse_args()
    try:
        r = check(a.corpus, strict=a.strict)
    except DtcgError as e:
        print("GATE ERROR (a crash is not a fail) :: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print("DTCG GATE — s136-D1 axis A wire format%s" % (" [--strict]" if a.strict else ""))
        for n in r["notes"]:
            print("  note: %s" % n)
        for d in r["deferrals"]:
            print("  DEFERRED %-24s %s :: %s :: %s" % (d["deferral"], d["file"], d["path"], d["why"]))
        for f in r["fails"]:
            print("FAIL %-10s %s :: %s :: %s" % (f["check"], f["file"], f["path"], f["why"]))
        print("%s — %d failure(s), %d declared deferral(s)"
              % ("FAIL" if r["fails"] else "PASS", len(r["fails"]), len(r["deferrals"])))
    return 1 if r["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
