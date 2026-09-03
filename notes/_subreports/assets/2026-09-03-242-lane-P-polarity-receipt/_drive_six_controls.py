#!/usr/bin/env python3
"""#242 lane P — re-drive lane F (#239)'s SEVEN green controls against the s240-D3 gate.

Six of V's (#238) seven green controls read FALSE-RED after #239 lane F closed Q3 (the quote
oracle: a node may not name its own oracle). Lane F's `green-controls-recut.txt` drove the LEGAL
ANALOGUE of each; two of them — (d) a retired polarity and (e) a brand-new one — had NO legal form
until `s240-D3`. This script drives, for each control: (1) the control LITERALLY, exactly as V
wrote it, against the built gate, and (2) its s240-D3 LEGAL FORM. Both verdicts are printed, so a
reader can see which refusals are CORRECT (the node naming its own oracle — untouched by s240-D3)
and which are now GREEN because the receipt widened to a ruling id.

Seat-bound only by REPO/OUT below.
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
VALIDATOR = os.path.join(REPO, "knowledge", "_validate_polarities.py")
BRAIN = os.path.join(REPO, "knowledge", "brain")
R1 = os.path.join(REPO, "notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json")
PY = sys.executable
ROOT = tempfile.mkdtemp(prefix="p242-controls-", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
LOG = []


def say(s=""):
    print(s)
    LOG.append(s)


def run(args):
    r = subprocess.run([PY, VALIDATOR] + args, capture_output=True, text=True, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def names(out):
    return sorted(set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)", out)))


def fresh(slug):
    d = os.path.join(ROOT, slug)
    shutil.copytree(BRAIN, d, ignore=shutil.ignore_patterns("__pycache__", ".*.tmp"))
    return d


def jmut(path, fn):
    o = json.loads(open(path, encoding="utf-8").read())
    fn(o)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(o, indent=1, ensure_ascii=False) + "\n")


def pol(d, fn):
    jmut(os.path.join(d, "polarities.json"), fn)


def stubs(d, fn):
    jmut(os.path.join(d, "stubs.json"), fn)


def drive(label, d, write=False, expect="green"):
    rc, out = run((["--write"] if write else ["--check"]) + ["--brain", d])
    verdict = "GREEN" if rc == 0 else ("RED " + ",".join(names(out)))
    mark = "OK " if ((rc == 0) == (expect == "green")) else "!! "
    say(f"  {mark}{label:<58} rc={rc}  {verdict}")
    return rc, out


def add(d, entry, write=True):
    ep = os.path.join(ROOT, "entry.json")
    with open(ep, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)
    return run(["--add-polarity", ep, "--write" if write else "--dry-run", "--brain", d])


REAL = json.loads(open(os.path.join(BRAIN, "polarities.json"), encoding="utf-8").read())["polarities"]
PARTIES = [{k: v for k, v in p.items() if k != "note"} for p in REAL[0]["parties"]]
SEED = "s240-D3"


def seed_node(nid="pl-31", **over):
    n = {"id": nid, "parties": json.loads(json.dumps(PARTIES)),
         "mediating_variable": "target count", "links": [], "$seed": SEED}
    n.update(over)
    return n


# V's own shapes, copied from notes/_subreports/assets/2026-09-02-239-F-polarity-fix/_wave{1,2,3}.py
NEW31 = {"id": "pl-31", "parties": [{"ref": "pr-fitts", "role": "side_a"},
                                    {"ref": "pr-hick", "role": "side_b"}],
         "mediating_variable": "target count", "links": [],
         "sources": [{"path": "notes/nowhere.json", "id": "tn-31"}]}
GOOD = {"id": "pl-90", "parties": [{"ref": "pr-fitts", "role": "side_a"},
                                   {"ref": "pr-hick", "role": "side_b"}],
        "mediating_variable": "target count", "links": [], "sources": [{"path": "selftest", "id": "x"}]}
GOOD_SEED = {k: v for k, v in GOOD.items() if k != "sources"}
GOOD_SEED["$seed"] = SEED

say("#242 lane P — lane F's seven green controls, LITERAL vs their s240-D3 LEGAL FORM")
say("=" * 100)

# ---- 120: unchanged, still green ------------------------------------------------------------
say("[120] links-empty-array — GREEN-OK at #238 and #239; unchanged by s240-D3")
d = fresh("120")
pol(d, lambda o: o["polarities"][0].__setitem__("links", []))
drive("120 literal (--write)", d, write=True)

# ---- 100: a 31st row with a FICTIONAL source path --------------------------------------------
say("")
say("[100] row31-no-stub-fictional-source — FALSE-RED at #239 (S-SOURCE: the node named its own oracle)")
d = fresh("100-literal")
pol(d, lambda o: o["polarities"].append(dict(NEW31)))
drive("100 literal: a fictional R1 path (still REFUSED, correctly)", d, write=True, expect="red")
d = fresh("100-legal")
pol(d, lambda o: o["polarities"].append(seed_node()))
drive("100 s240-D3: the same new node with `$seed` = a ruling id", d, write=True)

# ---- 225: sources.path = /etc/hostname --------------------------------------------------------
say("")
say("[225] sources-path-absolute-outside-repo — FALSE-RED at #239 (S-ID + S-SOURCE)")
d = fresh("225-literal")
pol(d, lambda o: o["polarities"][0]["sources"].append({"path": "/etc/hostname", "id": "x"}))
drive("225 literal: a second, foreign receipt (still REFUSED, correctly)", d, expect="red")
d = fresh("225-two-receipts")
pol(d, lambda o: o["polarities"][0].__setitem__("$seed", SEED))
drive("225 s240-D3: an R1 row AND a `$seed` — one pointer per node", d, expect="red")
d = fresh("225-legal")
pol(d, lambda o: o["polarities"].append(seed_node(nid="pl-33")))
drive("225 s240-D3 LEGAL: the node names ONE legal receipt (the ruling id)", d, write=True)

# ---- 235: an orphan stub ----------------------------------------------------------------------
say("")
say("[235] orphan-stub-declared-never-used — FALSE-RED at #239 (phrase not verbatim in R1)")
reg = json.loads(open(R1, encoding="utf-8").read())["tensions"]
row_text = " ".join(str(v) for v in reg[0].values() if isinstance(v, str))
phrase = " ".join(row_text.split()[:4])
d = fresh("235-literal")
stubs(d, lambda o: o["stubs"].append({"id": "st-orphan-phrase", "phrase": "an orphan phrase"}))
drive("235 literal: an invented phrase (still REFUSED, correctly)", d, expect="red")
d = fresh("235-legal")
stubs(d, lambda o: o["stubs"].append({"id": "st-orphan-verbatim", "phrase": phrase}))
drive(f"235 #239-F (a): orphan stub, phrase VERBATIM {phrase[:34]!r}", d)

# ---- 248: a node whose parties are two stubs ---------------------------------------------------
say("")
say("[248] node-all-parties-are-stubs — FALSE-RED at #239 (S-SOURCE on the fake path 'x')")
ALLSTUB = {"id": "pl-40",
           "parties": [{"ref": "st-brand-palette", "role": "side_a"},
                       {"ref": "st-consistency-of-investment-across-a-journey", "role": "side_b"}],
           "mediating_variable": "x", "links": [], "sources": [{"path": "x", "id": "y"}]}
d = fresh("248-literal")
pol(d, lambda o: o["polarities"].append(dict(ALLSTUB)))
drive("248 literal: source path 'x' (still REFUSED, correctly)", d, write=True, expect="red")
d = fresh("248-legal")
ALLSTUB_SEED = {k: v for k, v in ALLSTUB.items() if k != "sources"}
ALLSTUB_SEED["$seed"] = SEED
pol(d, lambda o: o["polarities"].append(dict(ALLSTUB_SEED)))
drive("248 s240-D3: the same all-stub node with `$seed`", d, write=True)

# ---- 321: the writer into an EMPTY polarities array ---------------------------------------------
say("")
say("[321] writer-append-into-empty-array — FALSE-RED at #239 (#239-F (d): 29 frozen rows unclaimed;")
say("      lane F: 'RULING-SHAPED: retiring rows needs a legal form'. s240-D3 IS that legal form:")
say("      a retired node KEEPS its row and carries `retiredBy`; deletion is still refused.")
d = fresh("321-literal")
pol(d, lambda o: o.__setitem__("polarities", []))
rc, out = add(d, GOOD_SEED)
say(f"  {'OK ' if rc != 0 else '!! '}321 literal: 30 rows DELETED, then the writer      rc={rc}  "
    f"{'GREEN' if rc == 0 else 'RED ' + ','.join(names(out))}")
d = fresh("321-legal")
pol(d, lambda o: [n.__setitem__("retiredBy", SEED) for n in o["polarities"]])
rc_w, _ = drive("321 s240-D3 step 1: all 30 RETIRED, --write", d, write=True)
rc, out = add(d, GOOD_SEED)
say(f"  {'OK ' if rc == 0 else '!! '}321 s240-D3 step 2: writer appends the `$seed` node  rc={rc}  "
    f"{'GREEN' if rc == 0 else 'RED ' + ','.join(names(out))}")
sys.path.insert(0, os.path.join(REPO, "knowledge"))
from _validate_polarities import generated_node_ids   # noqa: E402 — the gate's own structural reader
named = set()
for n in ("polarity-status.json", "polarity-edges.json", "defaults-declaration.txt"):
    named |= generated_node_ids(n, open(os.path.join(d, "_generated", n), encoding="utf-8").read())
leaks = sorted({r["id"] for r in REAL} & named)
kept = len(json.loads(open(os.path.join(d, "polarities.json"), encoding="utf-8").read())["polarities"])
say(f"  {'OK ' if not leaks and kept == 31 else '!! '}321 s240-D3 drop-out: rows kept in "
    f"polarities.json = {kept} (30 retired + 1 new) · retired ids leaking into _generated/ = {leaks}")

# ---- 326: the writer on a 2-space-indented file --------------------------------------------------
say("")
say("[326] writer-on-2-space-indented-file — FALSE-RED at #239 (S-SOURCE on the entry's fake receipt;")
say("      the FORMAT tolerance V found was never the thing refused)")
d = fresh("326-literal")
o = json.loads(open(os.path.join(d, "polarities.json"), encoding="utf-8").read())
open(os.path.join(d, "polarities.json"), "w", encoding="utf-8").write(
    json.dumps(o, indent=2, ensure_ascii=False) + "\n")
rc, out = add(d, GOOD)
say(f"  {'OK ' if rc != 0 else '!! '}326 literal: entry cites 'selftest'               rc={rc}  "
    f"{'GREEN' if rc == 0 else 'RED ' + ','.join(names(out))}")
d = fresh("326-legal")
o = json.loads(open(os.path.join(d, "polarities.json"), encoding="utf-8").read())
open(os.path.join(d, "polarities.json"), "w", encoding="utf-8").write(
    json.dumps(o, indent=2, ensure_ascii=False) + "\n")
rc, out = add(d, GOOD_SEED)
n_rows = len(json.loads(open(os.path.join(d, "polarities.json"), encoding="utf-8").read())["polarities"])
say(f"  {'OK ' if rc == 0 else '!! '}326 s240-D3: the same entry with `$seed`, 2-space   rc={rc}  "
    f"{'GREEN' if rc == 0 else 'RED ' + ','.join(names(out))} · rows {n_rows}")

say("")
say("=" * 100)
say("SUMMARY — all seven controls have a GREEN form under s240-D3:")
say("  120 green literally (unchanged) · 235 green in #239-F's form (a), unchanged by s240-D3")
say("  100 · 225 · 248 · 326 green once the node's receipt is the RULING ID instead of an oracle")
say("      the node invented — the Q3 refusal that made them FALSE-RED is CORRECT and stays")
say("  321 green once the 30 rows are RETIRED rather than DELETED — the legal form s240-D3 adds")
with open(os.path.join(OUT, "six-controls-s240-D3.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
shutil.rmtree(ROOT, ignore_errors=True)
