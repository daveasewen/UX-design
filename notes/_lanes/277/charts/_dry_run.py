#!/usr/bin/env python3
"""_dry_run.py — lane CO (#277). The gates that prove the proposal is safe to
land WITHOUT landing it. READ-ONLY on knowledge/.

Four things, all measured, none written into knowledge/:

  1. SCHEMA — every proposed meta validated against
     knowledge/components/meta.schema.json, including the obeysEdge `$why`
     REQUIRED / minLength 40 clause. A negative control runs too: a copy with
     one `$why` removed MUST fail, or the validation proves nothing.
  2. RESOLUTION — every proposed `rule:` ref must already be a node in
     knowledge/_rule_nodes.json, or the edge would land as a null.
  3. DRY RUN — how many new `obeys` edges enter the graph, against a SIMULATED
     tree: knowledge/ copied by symlink with components/ shadowed by the
     proposed metas, then knowledge/_validate_kg.py run against it.
  4. OWNERSHIP — git status shows changes only under this lane.

    python3 notes/_lanes/277/charts/_dry_run.py              # READ-ONLY: prints, writes nothing
    python3 notes/_lanes/277/charts/_dry_run.py --out DIR    # write the receipt into DIR
    python3 notes/_lanes/277/charts/_dry_run.py --write      # write it back into this lane (the #277 receipt)

READ-ONLY BY DEFAULT (lane CH, #277, CV's R-7: "a receipt that mutates when you
check it is not a receipt"). As shipped in 8c80aa2 this script wrote
dry-run.json / dry-run.txt into the very lane it audits, so a second seat
re-driving CO's receipt dirtied CO's committed files. The audit is unchanged —
same four sections, same figures, same exit code; only the writing is now opt-in.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
if _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_sys.path.insert(0, _hg_d)
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import copy
import glob
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
K = REPO / "knowledge"
PROPOSED = LANE / "proposed-metas"

# Where the receipt goes, if anywhere. Default: NOWHERE — this door is read-only
# unless asked (lane CH #277, R-7). `--write` restores the original destination.
_argv = sys.argv[1:]
if "--out" in _argv:
    _i = _argv.index("--out")
    if _i + 1 >= len(_argv):
        raise SystemExit("_dry_run: --out needs a directory")
    OUT_DIR = Path(_argv[_i + 1]).resolve()
elif "--write" in _argv:
    OUT_DIR = LANE
else:
    OUT_DIR = None
OUT = (OUT_DIR / "dry-run.json") if OUT_DIR else None


def _load(name):
    s = importlib.util.spec_from_file_location(name, LANE / (name + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


A = _load("_author_metas")
SCHEMA = json.loads((K / "components" / "meta.schema.json").read_text(encoding="utf-8"))
report = {}
lines = []


def say(s):
    print(s)
    lines.append(s)


# ---------------------------------------------------------------- 1. SCHEMA
say("== 1. SCHEMA — the three proposed metas against meta.schema.json ==")
V = jsonschema.Draft7Validator(SCHEMA)
fails = 0
for p in sorted(PROPOSED.glob("*.meta.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    errs = sorted(V.iter_errors(d), key=lambda e: list(e.path))
    n = len(d["edges"]["obeys"])
    say("  %-22s obeys=%2d  schema errors: %d" % (p.name, n, len(errs)))
    for e in errs[:3]:
        say("      %s: %s" % ("/".join(map(str, e.path)), e.message[:140]))
    fails += len(errs)
report["schema_errors"] = fails

# The negative control. A validator that cannot go red proves nothing
# (mutation-tests-the-clause: DRIVE THE THING).
neg = json.loads((PROPOSED / "chart-bar.meta.json").read_text(encoding="utf-8"))
ctl = {}
for name, mutate in [
    ("$why removed", lambda d: d["edges"]["obeys"][0].pop("$why")),
    ("$why under 40 chars", lambda d: d["edges"]["obeys"][0].update({"$why": "too short"})),
    ("ref not rule:/ux:", lambda d: d["edges"]["obeys"][0].update({"ref": "component:chart-bar"})),
    ("stray key in an entry", lambda d: d["edges"]["obeys"][0].update({"$when": "x"})),
]:
    bad = copy.deepcopy(neg)
    mutate(bad)
    ctl[name] = len(list(V.iter_errors(bad)))
    say("  NEGATIVE CONTROL  %-24s -> %d schema errors %s"
        % (name, ctl[name], "(RED, good)" if ctl[name] else "*** GREEN — THE CLAUSE IS NOT ENFORCED ***"))
report["negative_controls"] = ctl
say("  schema: %s" % ("OK — 0 errors on the proposal, every negative control red"
                      if fails == 0 and all(ctl.values()) else "FAIL"))

# ------------------------------------------------------------ 2. RESOLUTION
say("\n== 2. RESOLUTION — every proposed ref is already a node ==")
nodes = json.loads((K / "_rule_nodes.json").read_text(encoding="utf-8"))
ids = {n["id"] for n in nodes["nodes"]}
refs = [r for s in A.RULES for r, _ in A.RULES[s]]
missing = [r for r in refs if r not in ids]
say("  _rule_nodes.json nodes: %d  ·  rule: nodes: %d" % (len(ids), sum(1 for i in ids if i.startswith("rule:"))))
say("  proposed refs: %d  ·  unresolved: %d %s" % (len(refs), len(missing), missing or ""))
report["refs_proposed"] = len(refs)
report["refs_unresolved"] = len(missing)

# --------------------------------------------------------------- 3. DRY RUN
say("\n== 3. DRY RUN — the simulated tree ==")
live_obeys = 0
for f in glob.glob(str(K / "components" / "*.meta.json")):
    live_obeys += len(json.loads(Path(f).read_text(encoding="utf-8")).get("edges", {}).get("obeys", []))
say("  obeys edges in knowledge/components/ TODAY: %d" % live_obeys)
new = sum(len(A.RULES[s]) for s in A.RULES)
say("  obeys edges this lane proposes:             %d" % new)
say("  obeys edges after landing (simulated):      %d" % (live_obeys + new))
report["obeys_live_today"] = live_obeys
report["obeys_proposed"] = new
report["obeys_after"] = live_obeys + new

scratch = Path(tempfile.mkdtemp())
sim = scratch / "sim"
(sim / "knowledge").mkdir(parents=True)
for entry in os.listdir(K):
    if entry == "components":
        continue
    os.symlink(K / entry, sim / "knowledge" / entry)
shutil.copytree(K / "components", sim / "knowledge" / "components")
for p in PROPOSED.glob("*.meta.json"):
    shutil.copy2(p, sim / "knowledge" / "components" / p.name)
for entry in os.listdir(REPO):
    if entry not in ("knowledge",) and not entry.startswith("."):
        try:
            os.symlink(REPO / entry, sim / entry)
        except OSError:
            pass
r = subprocess.run([sys.executable, str(sim / "knowledge" / "_validate_kg.py")],
                   capture_output=True, text=True, cwd=str(sim), timeout=600)
tail = [x for x in (r.stdout + r.stderr).strip().split("\n") if x.strip()]
say("  _validate_kg.py against the SIMULATED tree (exit %d):" % r.returncode)
for x in tail[-3:]:
    say("    " + x)
report["sim_validate_kg_exit"] = r.returncode
report["sim_validate_kg_tail"] = tail[-1] if tail else ""
shutil.rmtree(scratch, ignore_errors=True)

# ------------------------------------------------------------- 4. OWNERSHIP
say("\n== 4. OWNERSHIP — git status ==")
g = subprocess.run(["git", "status", "--porcelain", "-z"], capture_output=True, text=True, cwd=str(REPO))
mine = "notes/_lanes/277/charts/"
paths = [x[3:] for x in g.stdout.split("\0") if len(x) > 3]
out = [p for p in paths if not p.startswith(mine) and not p.startswith("notes/_lanes/277/")]
say("  changed paths: %d  ·  outside notes/_lanes/277/: %d" % (len(paths), len(out)))
# A path outside the lane is only a finding if THIS lane touched it. mtime is
# the evidence: LANE_T0 is the moment this lane's first file was written.
t0 = min(os.path.getmtime(p) for p in glob.glob(str(LANE / "_*.py")))
for p in out:
    try:
        mt = os.path.getmtime(REPO / p)
    except OSError:
        mt = 0
    say("    OUTSIDE %-44s mtime %s  %s" % (
        p, __import__("time").strftime("%H:%M:%S", __import__("time").localtime(mt)),
        "*** NEWER THAN THIS LANE — INVESTIGATE ***" if mt > t0 else "predates this lane / another seat"))
report["paths_changed"] = len(paths)
report["paths_outside_lane"] = len(out)
report["paths_outside_newer_than_lane"] = sum(
    1 for p in out if os.path.exists(REPO / p) and os.path.getmtime(REPO / p) > t0)

report["verdict"] = ("OK" if (fails == 0 and all(ctl.values()) and not missing
                              and r.returncode == 0) else "FAIL")
say("\nVERDICT: %s" % report["verdict"])
if OUT_DIR is None:
    print("\nread-only (no --out DIR, no --write): nothing written. "
          "The audit above is the output.")
else:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT_DIR / "dry-run.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\nwrote %s and %s in %s" % (OUT.name, "dry-run.txt", OUT_DIR))
sys.exit(0 if report["verdict"] == "OK" else 1)
