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
  NOT a failure (declared, counted, never hidden):
    * an s210-D5 alias seat (aliasOf) — drawn by its owner's snippet;
    * a MEMBER of a family (#314 lane SW, s313-D56: switch, checkbox, radio and chip are four parts of the
      selection-controls family) — a meta whose own `edges.renderedBy` names a snippet that exists and whose
      manifest names a FAMILY meta (`covers: family`) that lists this member in its `$split.into`. A member
      whose renderedBy names a missing snippet, a non-family snippet, or a family that does not list it,
      still fails as "no gated snippet".
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

ALIAS_SEATS = set()   # names of s210-D5 alias seats: they hold no spec, so no snippet of their own
MEMBERS = {}          # #314 SW (s313-D56): member name -> (stem, the snippet its renderedBy names)
FAMILIES = {}         # family meta name -> the member stems its $split.into lists

def real_metas():
    out = {}
    for f in glob.glob(os.path.join(HERE, "components", "*.meta.json")):
        b = os.path.basename(f).replace(".meta.json", "")
        if b.startswith("EXAMPLE"):
            continue
        try:
            d = json.load(open(f))
            out[d.get("name", b)] = b + ".meta.json"
            if d.get("aliasOf"):
                ALIAS_SEATS.add(d.get("name", b))
            if d.get("covers") == "family" and isinstance(d.get("$split"), dict):
                FAMILIES[d.get("name", b)] = {str(r).split(":", 1)[-1] for r in d["$split"].get("into") or []}
            for e in ((d.get("edges") or {}).get("renderedBy") or []):
                ref = e.get("ref") if isinstance(e, dict) else None
                if isinstance(ref, str) and ref.startswith("snippet:") and d.get("$memberOf"):
                    MEMBERS[d.get("name", b)] = (b, ref[len("snippet:"):])
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
    # meta but no snippet. An alias seat (aliasOf) is drawn by its owner's snippet - #309 lane C, s308-D42:
    # kpi-tile.meta.json is an alias of Metric and its snippet became Metric.reference.html.
    missing = sorted(n for n in mset - sset if n not in ALIAS_SEATS)
    # a family member (#314 SW, s313-D56) is drawn by its family's snippet: proven, not assumed
    by_file = {v: k for k, v in snips.items()}
    members = []
    for n in list(missing):
        if n not in MEMBERS:
            continue
        stem, snip = MEMBERS[n]
        fam = by_file.get(snip)
        if fam in FAMILIES and stem in FAMILIES[fam]:
            members.append(f"{n} ({stem}.meta.json) -> {snip} of family {fam}")
            missing.remove(n)
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
    if members:
        lines += ["", f"_{len(members)} family member(s) drawn by their family's snippet (s313-D56):_"] + [f"- {m}" for m in members]
    open(os.path.join(HERE, "_COVERAGE-GATE.md"), "w").write("\n".join(lines) + "\n")

    print(f"coverage gate: {len(mset)} meta(s) / {len(sset)} snippet(s), {len(fails)} failure(s)"
          + (f" · {len(members)} family member(s) drawn by the family's snippet" if members else ""))
    for f in fails:
        print("  FAIL", re.sub(r"\*\*", "", f))
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
