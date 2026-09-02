#!/usr/bin/env python3
"""WAVE 4 — symlinked homes (gate sees X, commit carries Y), argv ambiguities, the selftest's
cleanup path, an unreceipted resolvedBy, swapped source pointers, duplicate polarity bodies,
and the live --selftest as a control."""
import glob
import json
import os
import shutil
import sys

sys.path.insert(0, "/sessions/wonderful-adoring-euler/mnt/outputs/v238")
from _v_attack import *  # noqa: E402,F401,F403

LOG = os.path.join(V, "logs")
lines = []


def say(s=""):
    print(s)
    lines.append(s)


# ---- harness arms -----------------------------------------------------------------------------------
arm(400, "resolvedBy-without-any-quote", "red",
    pol(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1"})), None,
    basis="s238-D6 migration: 'the quote that justifies the type'; a resolvedBy with NO quote closes pl-01 as resolved on no receipt (quote is optional in the schema)")
arm(401, "sources-id-swapped-to-another-row", "red",
    pol(lambda o: o["polarities"][3]["sources"][0].__setitem__("id", "tn-02")), None,
    basis="pl-04 now claims tn-02 as its source: polarity-status.json copies tn-02's factory_default/ask_when onto pl-04 (r1_id is taken from sources[0].id)")
arm(402, "duplicate-polarity-body-under-new-id", "red",
    pol(lambda o: o["polarities"].append(dict(o["polarities"][0], id="pl-31"))), None,
    basis="the same parties, roles, links and sources twice under two ids — no dedupe; the derived edges double")


def symlink_home(d):
    p = os.path.join(d, "polarities.json")
    shutil.move(p, os.path.join(d, "..", "polarities-moved.json"))
    os.symlink(os.path.join(d, "..", "polarities-moved.json"), p)
arm(403, "polarities.json-is-a-symlink-outside-the-home", "red", symlink_home, None, decisive="as-is",
    basis="the gate reads THROUGH a symlink; a commit would carry the symlink (dangling at any other seat) while every door is green here")

say(table())
dump(os.path.join(LOG, "wave4-arms.json"))

# what did 401 derive for pl-04?
try:
    s = json.load(open(os.path.join(ARMS, "401-sources-id-swapped-to-another-row", "brain-w", "_generated", "polarity-status.json")))
    r = [x for x in s["rows"] if x["id"] == "pl-04"][0]
    say(f"  [401] pl-04 derived with r1_id={r['r1_id']} factory_default={str(r.get('factory_default'))[:90]!r}")
    e = json.load(open(os.path.join(ARMS, "402-duplicate-polarity-body-under-new-id", "brain-w", "_generated", "polarity-edges.json")))
    say(f"  [402] edges after the duplicate: {e['counts']}")
except Exception as ex:  # noqa: BLE001
    say(f"  (401/402 readback: {ex!r})")

# ---- argv ambiguities ------------------------------------------------------------------------------------
say("\n== ARGV: flags that contradict each other")
d = os.path.join(ARMS, "410-argv-dry-run-and-write")
if os.path.exists(d):
    shutil.move(d, os.path.join(GRAVE, "410-" + str(os.getpid())))
os.makedirs(d)
brain = fresh_copy(os.path.join(d, "brain"))
ep = os.path.join(d, "entry.json")
json.dump({"id": "pl-90", "parties": [{"ref": "pr-fitts", "role": "side_a"}, {"ref": "pr-hick", "role": "side_b"}],
           "mediating_variable": "x", "links": [], "sources": [{"path": "x", "id": "y"}]}, open(ep, "w"))
h0 = sha(os.path.join(brain, "polarities.json"))
rc, out = run([PY, VALIDATOR, "--add-polarity", ep, "--dry-run", "--write", "--brain", brain])
h1 = sha(os.path.join(brain, "polarities.json"))
say(f"  --add-polarity FILE --dry-run --write : rc={rc} polarities.json changed={h0 != h1}  (a dry run that writes)")
brain2 = fresh_copy(os.path.join(d, "brain2"))
g0 = tree(os.path.join(brain2, "_generated"))
rc, out = run([PY, VALIDATOR, "--check", "--write", "--brain", brain2])
g1 = tree(os.path.join(brain2, "_generated"))
say(f"  --check --write                        : rc={rc} _generated changed={g0 != g1}  (a check that writes)")

# ---- the selftest's cleanup path ---------------------------------------------------------------------------
say("\n== SELFTEST cleanup: P pitfall 9 says 'the tempdir is removed on every path'")
before = set(glob.glob("/dev/shm/polarity-selftest-*"))
rc, out = run([PY, VALIDATOR, "--selftest", "--brain", os.path.join(V, "no-such-home")])
after = set(glob.glob("/dev/shm/polarity-selftest-*"))
left = sorted(after - before)
say(f"  --selftest --brain <absent>: rc={rc} traceback={'Traceback' in out} leftover tempdirs={left}")
say("  (the rmtree at the end of selftest() is not in a finally: an exception before the table skips it)")
for p in left:
    shutil.rmtree(p, ignore_errors=True)

# ---- the live tree's own --selftest, as a control at this seat --------------------------------------------
say("\n== CONTROL: --selftest on the LIVE home (read-only over knowledge/brain; copies under /dev/shm)")
rc, out = run([PY, VALIDATOR, "--selftest"])
tail = [ln for ln in out.splitlines() if ln.startswith("arms ") or ln.startswith("✓ selftest") or ln.startswith("✗")]
say(f"  rc={rc} :: {tail}")
with open(os.path.join(LOG, "live-selftest.txt"), "w", encoding="utf-8") as f:
    f.write(out)

# ---- is the seam a consumer of EVERY commit? -------------------------------------------------------------------
say("\n== 'A gate that is not a consumer of every commit is not a gate' — where does a raw `git commit` go?")
hooks = sorted(os.listdir(os.path.join(REPO, ".git", "hooks"))) if os.path.isdir(os.path.join(REPO, ".git", "hooks")) else []
live_hooks = [h for h in hooks if not h.endswith(".sample")]
say(f"  .git/hooks live entries (non-.sample): {live_hooks}")
grep = [ln.strip()[:120] for h in live_hooks for ln in open(os.path.join(REPO, ".git", "hooks", h), errors="replace") if "polarit" in ln.lower()]
say(f"  hook lines mentioning the polarity gate: {grep}")

with open(os.path.join(LOG, "wave4.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
