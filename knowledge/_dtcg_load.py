#!/usr/bin/env python3
"""_dtcg_load.py — the READ-SITE seam for the s311-D8 DTCG 2025.10 move (#312 lane J).

knowledge/tokens/*.json are DTCG 2025.10 since s311-D8: `$alias` is a `{group.token}`
reference in `$value`, dark values live in tokens/modes/dark/<name>.json under the resolver
(tokens/apollo.resolver.json), the Apollo-only `$` keys live under `$extensions.apollo`, and
dimensions/durations are {value, unit} objects. Twenty-five scripts read those files in the
OLD shape (light/dark leaves, `$alias`, `$note`, "16px"). This module is the one place
they go through:

    from _dtcg_load import load_legacy
    doc = load_legacy(os.path.join(TOK, "semantic-colour.json"))   # the pre-s311 shape

`load_legacy(path)` is `json.load` for any file that is not one of the ten gated base
files, and the EXACT pre-s311 shape (tokens/gen_dtcg.to_legacy) for one that is — proven
by `knowledge/_validate_tokens_dtcg.py` on every run (round-trip, spine byte-equal, snippet
theme blocks byte-equal). Same precedent as _dtcg_units.py (s141-D1 (A)): one seam at the
read site, so the wire format moves and no consumer's output does. Readers go native in
phase 1 of `notes/_PROPOSAL-311-apollo-for-other-libraries-2026-10-01-v1.html`; until
then every `json.load` of a base token file is a defect (the DTCG shape is NOT what the
old walkers expect: a `{ref}` is not a hex, and `light`/`dark` leaves are gone).

    load_legacy(path)      -> dict in the pre-s311 shape (cached per path + mtime)
    load_dtcg(path)        -> dict exactly as on disk (plain json.load, cached)
    legacy_spine(tokdir)   -> {name: legacy dict} for every base file
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS_DIR = os.path.join(HERE, "tokens")


def _gen():
    """Import tokens/gen_dtcg.py by path (tokens/ is not a package)."""
    mod = globals().get("_GEN")
    if mod is None:
        spec = importlib.util.spec_from_file_location(
            "gen_dtcg", os.path.join(TOKENS_DIR, "gen_dtcg.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        globals()["_GEN"] = mod
    return mod


_RAW = {}        # abs path -> (mtime, doc)
_LEGACY = {}     # abs path -> (signature, doc)


def _mtime(path):
    try:
        return os.stat(path).st_mtime_ns
    except OSError:
        return None


def load_dtcg(path):
    """json.load with a per-path mtime cache. Raises like open()/json.load would."""
    path = os.path.abspath(path)
    mt = _mtime(path)
    hit = _RAW.get(path)
    if hit is not None and hit[0] == mt:
        return hit[1]
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    _RAW[path] = (mt, doc)
    return doc


def _is_base_file(path):
    g = _gen()
    d = os.path.dirname(os.path.abspath(path))
    return (os.path.basename(path) in g.BASE_FILES
            and os.path.basename(d) == "tokens"
            and not os.path.basename(os.path.dirname(d)).startswith("modes"))


def _resolver_for(tokdir):
    """A DtcgResolver over every base file (+ dark) in `tokdir`, rebuilt when any changes."""
    g = _gen()
    sig = []
    bases, darks = {}, {}
    for n in g.BASE_FILES:
        bp = os.path.join(tokdir, n)
        if not os.path.exists(bp):
            continue
        bases[n] = load_dtcg(bp)
        dp = os.path.join(tokdir, "modes", "dark", n)
        darks[n] = load_dtcg(dp) if os.path.exists(dp) else None
        sig.append((n, _mtime(bp), _mtime(dp)))
    sig = tuple(sig)
    cache = globals().setdefault("_RES", {})
    hit = cache.get(tokdir)
    if hit is not None and hit[0] == sig:
        return sig, hit[1]
    res = g.DtcgResolver(bases, darks)
    cache[tokdir] = (sig, res)
    return sig, res


def load_legacy(path):
    """The pre-s311 shape of a base token file; plain json.load for anything else."""
    path = os.path.abspath(path)
    if not _is_base_file(path):
        return load_dtcg(path)
    g = _gen()
    tokdir = os.path.dirname(path)
    sig, res = _resolver_for(tokdir)
    hit = _LEGACY.get(path)
    if hit is not None and hit[0] == sig:
        return hit[1]
    base = load_dtcg(path)
    dp = os.path.join(tokdir, "modes", "dark", os.path.basename(path))
    dark = load_dtcg(dp) if os.path.exists(dp) else None
    doc = g.to_legacy(base, dark, res)
    _LEGACY[path] = (sig, doc)
    return doc


def legacy_spine(tokdir=TOKENS_DIR):
    g = _gen()
    return {n: load_legacy(os.path.join(tokdir, n)) for n in g.BASE_FILES
            if os.path.exists(os.path.join(tokdir, n))}


def selftest():
    import copy
    g = _gen()
    sem = load_legacy(os.path.join(TOKENS_DIR, "semantic-colour.json"))
    raw = load_dtcg(os.path.join(TOKENS_DIR, "semantic-colour.json"))
    # bite 1: the legacy view has light/dark leaves where the file has one token
    bd = sem["background"]["default"]
    assert "light" in bd and "dark" in bd and "$alias" in bd, bd
    assert "light" not in raw["background"]["default"] or "$value" in raw["background"]["default"]
    # bite 2: a non-base file is a plain json.load (no transform)
    ct = os.path.join(HERE, "component-types.json")
    if os.path.exists(ct):
        assert load_legacy(ct) == json.load(open(ct, encoding="utf-8"))
    # bite 3: the view is cached and returned by identity until the file changes
    assert load_legacy(os.path.join(TOKENS_DIR, "semantic-colour.json")) is sem
    # bite 4: the view is a round-trip: forward(view) == file
    spine = g.Spine(legacy_spine())
    base, dark = g.to_dtcg(copy.deepcopy(sem), spine, "semantic-colour.json")
    assert base == raw, "forward(legacy view) != the file on disk"
    print("_dtcg_load selftest OK (4 bites: mode leaves restored · non-base passthrough · "
          "cache identity · forward(view) == disk)")


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
    else:
        print(__doc__)
