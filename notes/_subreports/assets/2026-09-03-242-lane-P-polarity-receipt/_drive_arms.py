#!/usr/bin/env python3
"""#242 lane P — the s240-D3 mutation arms at the CLI, each driven BOTH WAYS.

For every refusal the brief names: a GREEN CONTROL that must pass, and a BREAK ARM that must go
RED BY NAME. Same door the build and the commit seam use (`--check` / `--write --brain DIR`), so
the transcript below is the command a reader can retype. Seat-bound only by REPO.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = "/sessions/eager-wizardly-lovelace/mnt/UX-design"
OUT = os.path.join(REPO, "notes/_subreports/assets/2026-09-03-242-lane-P-polarity-receipt")
VAL = os.path.join(REPO, "knowledge", "_validate_polarities.py")
BRAIN = os.path.join(REPO, "knowledge", "brain")
PY = sys.executable
ROOT = tempfile.mkdtemp(prefix="p242-arms-", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
LOG = []
SEED = "s240-D3"
REAL = json.loads(open(os.path.join(BRAIN, "polarities.json"), encoding="utf-8").read())["polarities"]
PARTIES = [{k: v for k, v in p.items() if k != "note"} for p in REAL[0]["parties"]]


def say(s=""):
    print(s)
    LOG.append(s)


def fresh(slug):
    d = os.path.join(ROOT, slug)
    shutil.copytree(BRAIN, d, ignore=shutil.ignore_patterns("__pycache__", ".*.tmp"))
    return d


def jmut(path, fn):
    o = json.loads(open(path, encoding="utf-8").read())
    fn(o)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(o, indent=1, ensure_ascii=False) + "\n")


def seed_node(nid="pl-31", **over):
    n = {"id": nid, "parties": json.loads(json.dumps(PARTIES)),
         "mediating_variable": "target count", "links": [], "$seed": SEED}
    n.update(over)
    return n


def drive(label, d, expect, want=None, write=False):
    mode = "--write" if write else "--check"
    r = subprocess.run([PY, VAL, mode, "--brain", d], capture_output=True, text=True, cwd=REPO)
    out = r.stdout + r.stderr
    names = sorted(set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)", out)))
    line = next((ln.strip() for ln in out.splitlines()
                 if "REFUSED (" in ln and "POLARITY GATE REFUSED" not in ln), "")
    if expect == "green":
        ok = r.returncode == 0
    else:
        ok = r.returncode == 1 and (want is None or want in names)
    say(f"  {'OK ' if ok else '!! '}{label}")
    say(f"     $ python3 knowledge/_validate_polarities.py {mode} --brain <copy>   → rc {r.returncode}"
        + (f"  names {names}" if names else "  GREEN"))
    if line:
        say(f"     {line[:200]}")
    return ok


say("#242 lane P — the s240-D3 mutation arms, driven BOTH WAYS at the CLI")
say("=" * 100)

say("")
say("PIN — SCHEMA_SHA256 is a pin, not a decoration (the brief's own arm)")
d = fresh("pin-green")
drive("GREEN CONTROL: the schema as committed, pin c2c165ac…", d, "green")
d = fresh("pin-red")
jmut(os.path.join(d, "schema", "polarity.schema.json"),
     lambda s: s.__setitem__("title", "Polarity node (edited, pin NOT moved)"))
drive("BREAK ARM: schema touched, SCHEMA_SHA256 not moved", d, "red", "SCHEMA-PIN-MISMATCH")

say("")
say("(a) a `$seed` / `retiredBy` naming an id ABSENT from knowledge/_rulings.json → R1-DANGLING")
d = fresh("seed-green")
jmut(os.path.join(d, "polarities.json"), lambda o: o["polarities"].append(seed_node()))
drive("GREEN CONTROL: `$seed` = s240-D3, a real ruling id", d, "green", write=True)
d = fresh("seed-red")
jmut(os.path.join(d, "polarities.json"),
     lambda o: o["polarities"].append(seed_node(**{"$seed": "s999-D9"})))
drive("BREAK ARM: `$seed` = s999-D9", d, "red", "R1-DANGLING")
d = fresh("retired-green")
jmut(os.path.join(d, "polarities.json"),
     lambda o: o["polarities"][-1].__setitem__("retiredBy", SEED))
drive("GREEN CONTROL: `retiredBy` = s240-D3, re-derived with --write", d, "green", write=True)
d = fresh("retired-red")
jmut(os.path.join(d, "polarities.json"),
     lambda o: o["polarities"][-1].__setitem__("retiredBy", "s999-D9"))
drive("BREAK ARM: `retiredBy` = s999-D9", d, "red", "R1-DANGLING")

say("")
say("(b) TWO receipts on one node — the receipt is ONE POINTER PER NODE → S-SOURCE")
d = fresh("two-green")
drive("GREEN CONTROL: all 30 nodes carry exactly one receipt (their R1 row)", d, "green")
d = fresh("two-red")
jmut(os.path.join(d, "polarities.json"),
     lambda o: o["polarities"][0].__setitem__("$seed", SEED))
drive("BREAK ARM: pl-01 carries its R1 `sources` AND a `$seed`", d, "red", "S-SOURCE")
d = fresh("none-red")
jmut(os.path.join(d, "polarities.json"),
     lambda o: o["polarities"].append({k: v for k, v in seed_node("pl-32").items() if k != "$seed"}))
drive("BREAK ARM: a node with NEITHER receipt", d, "red", "S-SOURCE")

say("")
say("(c) a RETIRED node still present under knowledge/brain/_generated/ → R4-RETIRED-GENERATED")
d = fresh("leak-red")
jmut(os.path.join(d, "polarities.json"),
     lambda o: o["polarities"][-1].__setitem__("retiredBy", SEED))
drive("BREAK ARM: pl-30 retired, _generated/ NOT re-derived", d, "red", "R4-RETIRED-GENERATED")
subprocess.run([PY, VAL, "--write", "--brain", d], capture_output=True, text=True, cwd=REPO)
drive("GREEN CONTROL: the same tree after --write (the node dropped out)", d, "green")
sys.path.insert(0, os.path.join(REPO, "knowledge"))
from _validate_polarities import generated_node_ids   # noqa: E402 — the gate's own structural reader
named = set()
for n in ("polarity-status.json", "polarity-edges.json", "defaults-declaration.txt"):
    named |= generated_node_ids(n, open(os.path.join(d, "_generated", n), encoding="utf-8").read())
rows = json.loads(open(os.path.join(d, "polarities.json"), encoding="utf-8").read())["polarities"]
say(f"     drop-out: polarities.json still carries pl-30 = {any(r['id'] == 'pl-30' for r in rows)} · "
    f"_generated/ names pl-30 = {'pl-30' in named} · rows in polarity-status.json = {len(named)}")

say("")
say("=" * 100)
say("Every arm above is also a --selftest arm (see selftest.txt, arms 104-114 and 99).")
with open(os.path.join(OUT, "mutation-arms.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
shutil.rmtree(ROOT, ignore_errors=True)
