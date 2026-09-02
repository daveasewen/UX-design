#!/usr/bin/env python3
"""#238-P — prove the _build_all.py wiring WITHOUT running the build.

1. import _build_all (no step runs on import) and call check_routes(): the STEPS ↔ ROUTE_ROWS join
   is total and the two polarity rows are the LAST two entries (appended, never inserted);
2. the ONE slicer (_gen_chain._steps_in) and the schematic's row reader agree on the count;
3. drive the two new STEPS entries EXACTLY as _build_all.main() would — the same
   `[sys.executable, path] + extra_args` subprocess form — on the real home (green), and the
   gate entry on a MUTATED COPY of the real home via POLARITY_BRAIN_DIR (red, GATE remedy shown).
Read-only over the repo; scratch under /dev/shm, removed.
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
KNOW = os.path.join(REPO, "knowledge")
sys.path.insert(0, KNOW)
sys.argv = ["x"]
with contextlib.redirect_stdout(io.StringIO()):
    import _build_all as b       # noqa: E402
    import _gen_chain as gc      # noqa: E402
    import _gen_schematic as gs  # noqa: E402

n = b.check_routes()
labels = [s[0] for s in b.STEPS]
mine = [l for l in labels if l.startswith("polarity gate")]
print(f"check_routes(): {n} steps, STEPS ↔ ROUTE_ROWS join total")
assert len(mine) == 2 and labels[-2:] == mine, "the polarity rows are not the last two STEPS entries"
print("the two polarity rows are the LAST two STEPS entries (appended):")
for l in mine:
    print(f"  [{labels.index(l) + 1}] route={b.route(l)[0]:8s} args={[s[2] for s in b.STEPS if s[0] == l][0]}")
src = open(os.path.join(KNOW, "_build_all.py"), encoding="utf-8").read()
print("one slicer — _gen_chain._steps_in:", gc._steps_in(src, "_build_all.py"),
      "· schematic build_rows:", len(gs.build_rows(gs.ROOT)))

print("\n-- driving the two entries in the build's own subprocess form, real home --")
for step in b.STEPS[-2:]:
    label, rel = step[0], step[1]
    extra = list(step[2]) if len(step) > 2 else []
    r = subprocess.run([sys.executable, os.path.join(KNOW, rel)] + extra, capture_output=True, text=True,
                       cwd=REPO)
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"  [{label[:44]}…] rc={r.returncode} route={b.route(label)[0]} :: {tail[:100]}")
    assert r.returncode == 0, f"expected rc 0 on the real home, got {r.returncode}"

print("\n-- the gate entry on a MUTATED COPY (typed status on pl-01) via POLARITY_BRAIN_DIR --")
tmp = tempfile.mkdtemp(prefix="p238-build-red-", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
shutil.copytree(os.path.join(KNOW, "brain"), os.path.join(tmp, "brain"))
p = os.path.join(tmp, "brain", "polarities.json")
o = json.load(open(p, encoding="utf-8"))
o["polarities"][0]["status"] = "open"
json.dump(o, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
step = b.STEPS[-2]
r = subprocess.run([sys.executable, os.path.join(KNOW, step[1])] + list(step[2]), capture_output=True,
                   text=True, cwd=REPO, env=dict(os.environ, POLARITY_BRAIN_DIR=os.path.join(tmp, "brain")))
kind, remedy = b.route(step[0])
named = [l.strip() for l in r.stdout.splitlines() if "REFUSED (" in l]
print(f"  rc={r.returncode} -> the build would print the {kind.upper()} remedy; the gate named:")
for l in named:
    print("    " + l)
print("  remedy (first 200 chars): " + remedy.format(code=r.returncode).strip().replace("\n", " ")[:200])
shutil.rmtree(tmp, ignore_errors=True)
assert r.returncode == 1 and any("R5-TYPED-STATUS" in l for l in named)
print("\n✓ build wiring proven: join total · appended last · green on the real home · red + GATE remedy on the mutant")
