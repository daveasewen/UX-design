#!/usr/bin/env python3
"""
_validate_coverage.py — coverage / consistency gate.

Verification = enforcement. This gate fails the build if the gated-snippet layer and the
component-meta layer drift apart:

  FAIL (gating):
    * a real component meta (components/*.meta.json, excluding EXAMPLE-* templates) has NO
      gated reference snippet whose manifest `component` matches its `name`;
    * a snippet manifest names a `component` with no corresponding meta (orphan snippet);
    * a snippet is missing/!=parseable token-manifest JSON.

Keeps "32/32 gated" honest — a new meta with no snippet, or a renamed component, turns the build red.
Writes _COVERAGE-GATE.md and exits non-zero on any failure.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import glob, os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def real_metas():
    out = {}
    for f in glob.glob(os.path.join(HERE, "components", "*.meta.json")):
        b = os.path.basename(f).replace(".meta.json", "")
        if b.startswith("EXAMPLE"):
            continue
        try:
            out[json.load(open(f)).get("name", b)] = b + ".meta.json"
        except Exception as e:
            out[b] = f"UNPARSEABLE ({e})"
    return out

def snippet_manifests():
    out, bad = {}, []
    for f in glob.glob(os.path.join(HERE, "snippets", "*.reference.html")):
        s = open(f).read()
        m = re.search(r'id="token-manifest"[^>]*>(.*?)</script>', s, re.S)
        base = os.path.basename(f)
        if not m:
            bad.append(f"{base}: no token-manifest block")
            continue
        try:
            comp = json.loads(m.group(1)).get("component")
            if not comp:
                bad.append(f"{base}: manifest has no `component`")
            else:
                out[comp] = base
        except Exception as e:
            bad.append(f"{base}: manifest JSON invalid ({e})")
    return out, bad

def main():
    metas = real_metas()
    snips, bad = snippet_manifests()
    mset, sset = set(metas), set(snips)
    missing = sorted(mset - sset)     # meta but no snippet
    orphan = sorted(sset - mset)      # snippet but no meta

    fails = []
    for n in missing:
        fails.append(f"component **{n}** ({metas[n]}) has no gated snippet")
    for n in orphan:
        fails.append(f"snippet **{snips[n]}** names component '{n}' with no meta")
    fails += [f"malformed manifest — {b}" for b in bad]

    lines = ["# Coverage / consistency gate — _validate_coverage.py", "",
             f"**{len(mset)} real component meta(s)** · **{len(sset)} snippet manifest(s)** · **{len(fails)} failure(s)**",
             ""]
    if fails:
        lines += [f"- 🔴 {f}" for f in fails]
    else:
        lines.append(f"_All {len(mset)} real components are gated and names match. No orphans._")
    open(os.path.join(HERE, "_COVERAGE-GATE.md"), "w").write("\n".join(lines) + "\n")

    print(f"coverage gate: {len(mset)} meta(s) / {len(sset)} snippet(s), {len(fails)} failure(s)")
    for f in fails:
        print("  FAIL", re.sub(r"\*\*", "", f))
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
