"""R1 lane 1b: give the four bare s282-D2..D5 evidence strings their legal `commit <sha>` pointer,
through the sanctioned writer (_inscribe_ruling.py --amend-evidence). Idempotent: an entry that
already starts with `commit ` is left alone. Usage: python3 s282_pointers.py <repo> [--write]"""
import json, subprocess, sys, os
repo = sys.argv[1]; write = "--write" in sys.argv
# sha = the commit that inscribed the measured text (git log -S on knowledge/_rulings.json)
SHA = {"s282-D2": ("bb016c69", "col26-012 override cross-ref measured present"),
       "s282-D3": ("c143a1bf", "sheet re-rendered: 60 .sz blocks"),
       "s282-D4": ("da9f824e", "regen diff measured: removed 4 governedBy-null"),
       "s282-D5": ("eaf12365", "notes/_lanes/282/logo-land/ - the lane's evidence dir")}
rul = {r["id"]: r for r in json.load(open(os.path.join(repo, "knowledge/_rulings.json")))["rulings"]}
for rid, (sha, span) in SHA.items():
    ev = list(rul[rid]["evidence"])
    hits = [i for i, e in enumerate(ev) if e.startswith(span)]
    if not hits:
        done = [e for e in ev if e.startswith(f"commit {sha} - ") and span in e]
        print(rid, "ALREADY POINTED" if done else "SPAN NOT FOUND — STOP"); continue
    i = hits[0]; ev[i] = f"commit {sha} - " + ev[i]
    cmd = ["python3", "knowledge/_inscribe_ruling.py", "--amend-evidence", "--id", rid, "--write" if write else "--dry-run"]
    p = subprocess.run(cmd, cwd=repo, input=json.dumps(ev, ensure_ascii=False), capture_output=True, text=True)
    print(rid, "rc", p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1][:200])
