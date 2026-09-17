#!/usr/bin/env python3
"""#280 wrap — write a UNIQUELY-NAMED, SESSION-OWNED ops file, assert it exists with a size
floor IN THIS PROCESS, then hand it to `knowledge/_gm_move.py` (dry-run first, then the write)
and print the receipts back for reading against the ops that were meant to run.

⛔ This exists because of the #166 defect the runbook inscribes: a heredoc to a shared fixed
`/var/tmp` path failed with PermissionError while the command chain continued, and the mover
consumed a STALE ops file from #139 and printed green receipts for someone else's ops.

Usage: run_ops.py <name> <ops-builder-module-or-json-literal-file> [--write]
Here it is imported by the per-step scripts instead; see `ops280.py`.
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def run(name, ops, write=False, min_bytes=100):
    path = os.path.join(HERE, f"ops-281-{name}-{int(time.time())}.json")
    blob = json.dumps(ops, ensure_ascii=False, indent=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(blob)
    # assertions IN THIS PROCESS, before the mover is allowed to read anything
    assert os.path.exists(path), f"REFUSED — ops file was not written: {path}"
    size = os.path.getsize(path)
    assert size >= min_bytes, f"REFUSED — ops file is {size} B, under the {min_bytes} B floor"
    with open(path, encoding="utf-8") as f:
        assert json.load(f) == ops, "REFUSED — ops file does not read back as what was meant"
    print(f"OPS {path} — {size} B / {len(ops)} op(s), asserted before the mover reads it")
    cmd = [sys.executable, "knowledge/_gm_move.py", "--ops", path, "--repo", ROOT]
    if not write:
        cmd.append("--dry-run")
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.rstrip())
    if r.stderr.strip():
        print("STDERR:", r.stderr.rstrip())
    print(f"mover exit={r.returncode}")
    return r.returncode
