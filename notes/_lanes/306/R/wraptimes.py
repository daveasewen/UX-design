#!/usr/bin/env python3
"""306 R: the last three wraps measured from the record (read-only).
Launch times are the conductor-transcript times each W report quotes (BST, converted to UTC);
every other time is a file mtime at the seat (UTC) or a git commit time."""
import os, subprocess, datetime as dt, glob, re
os.chdir(os.path.expanduser("~/mnt/Projects--UX-design"))
W = {303: ("2026-09-26 12:47:24", "efe3bb47", "571d458c"),
     304: ("2026-09-27 11:16:59", "9f9ff879", "7cae0189"),
     305: ("2026-09-28 09:09:46", "81bce363", "eb2630bb")}
def mt(p): return dt.datetime.utcfromtimestamp(os.path.getmtime(p)) if os.path.exists(p) else None
def ct(c): return dt.datetime.strptime(subprocess.run(["git","--no-optional-locks","show","-s","--format=%cI",c],capture_output=True,text=True).stdout.strip()[:19],"%Y-%m-%dT%H:%M:%S")
def files(c): return [l for l in subprocess.run(["git","--no-optional-locks","show","--name-only","--format=",c],capture_output=True,text=True).stdout.split("\n") if l]
OTHER = re.compile(r"notes/_lanes/\d+/(C\d|K|C6)/|dashboard/|-(R1|C4|C6)-|MEMENTO-SCHEMATIC|_graph-|_REHEARSAL|/_ci-gates-\d+")
m = lambda a,b: f"{(b-a).total_seconds()/60:5.1f}"
for n,(launch,c1,c2) in W.items():
    d=f"notes/_lanes/{n}/W"; L=dt.datetime.strptime(launch,"%Y-%m-%d %H:%M:%S")
    g=mt(f"{d}/_gate-open.log"); p1=mt(f"{d}/_push-W1-plain.log"); ci1=mt(glob.glob(f"{d}/_ci-runs-{c1}*.txt")[0])
    p2=mt(f"{d}/_push-W5b-plain.log"); ci2=mt(f"{d}/_ci-gates-W5b.log"); h=mt(f"{d}/_4c-hygiene.log")
    f1=[f for f in files(c1)+files(c2)]
    own=sorted(set(f for f in f1 if not OTHER.search(f)))
    lanework=[f for f in own if f.startswith(f"notes/_lanes/{n}/W/")]
    record=[f for f in own if f not in lanework]
    print(f"#{n} launch {L:%H:%M:%S}Z · first gate {g:%H:%M} · push1 {p1:%H:%M:%S} · CI1 read {ci1:%H:%M} · push2 {p2:%H:%M:%S} · CI2 read {ci2:%H:%M}" + (f" · 4c {h:%H:%M}" if h else ""))
    print(f"   minutes: to first gate {m(L,g)} | gate→push1 {m(g,p1)} | CI1 wait {m(p1,ci1)} | 5b {m(ci1,p2)} | CI2 wait {m(p2,ci2)} | TOTAL launch→last CI {m(L,ci2)}")
    print(f"   commits: 2 landed ({c1} {ct(c1):%H:%M:%S}, {c2} {ct(c2):%H:%M:%S})" + ("  + 1 refused (mention map)" if glob.glob(f"{d}/*refused*") else ""))
    print(f"   local gate runs: {len(glob.glob(d+'/_gate-*.log'))+len(glob.glob(d+'/_gitcommit-W*.log'))-len(glob.glob(d+'/*refused*.log'))} · regen logs {len(glob.glob(d+'/_regen*.log'))} · _gm_move ops files {len(glob.glob(d+'/_ops-*.json'))} · CI runs read 2")
    print(f"   record files written (outside W/): {len(record)} · W/ scratch+scripts committed: {len(lanework)}")
    for f in record: print("      ",f)
