#!/usr/bin/env python3
"""_parked.py — PARKED WITH A TRIPWIRE: work that is not queued, and must not be missed.

WHY (Dave, 2026-09-13 #269: "store them for future sake, can they be triggered, or can we
have a hook so they don't get missed at the appropriate time"; the shape is s181-D1's
"a park with a tripwire, not a queue entry"): `_CARRIES.md` carries 420 residual items and a
parked item in there is a needle. A parked item has a MOMENT — the next pack cut, the next
edge generation, the next dream pass — and the hook belongs at that moment, not in a list.

THE REGISTER: `knowledge/_parked.json` — hand-authored, one entry per parked item:
  id · parked {date, session, at_version, at_commit} · what · why · owner · status
  trigger — one of:
    {"kind": "pack-version-bump"}            due when the pack manifest version ≠ at_version
    {"kind": "file-changed", "path": "…"}    due when the path has a commit after at_commit
    {"kind": "event", "name": "dream-pass"}  due whenever that named event asks (--due <name>)
  status — "parked" (live) · "enacted" · "dropped" (both keep the row; history is data)

THE HOOKS (advisory, print-only, never change a verdict or an exit code):
  `_release/_gate_release_audit.py --check`  prints DUE items after its own verdict
  `gen_kg_edges.py`                          prints DUE items before it generates
  `_RUNBOOK-dream-pass.md` step              `python3 knowledge/_parked.py --due dream-pass`
Each hook imports `notice(event)` inside a try/except: a broken register can never break
the tool that hosts the hook. This door never writes.

Usage:
  python3 knowledge/_parked.py --check               # every live item, DUE or WAITING, with why
  python3 knowledge/_parked.py --due release-cut     # only what is due at that moment
  python3 knowledge/_parked.py --list                # the register, all statuses
  python3 knowledge/_parked.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
REGISTER = os.path.join(HERE, "_parked.json")
MANIFEST = os.path.join(HERE, "_release", "_pack_manifest.json")
MARK = "PARKED DUE"
EVENT_OF_KIND = {"pack-version-bump": "release-cut", "file-changed": None, "event": None}


def load(path=REGISTER):
    if not os.path.exists(path):
        raise SystemExit(f"parked: no register at {path} — REFUSING to report on nothing")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])
    for it in items:
        for k in ("id", "parked", "what", "trigger", "status"):
            if k not in it:
                raise SystemExit(f"parked: item {it.get('id', '?')} lacks '{k}' — closed form, REFUSING")
    return items


def pack_version(manifest=MANIFEST):
    with open(manifest, encoding="utf-8") as f:
        return json.load(f).get("version")


def commits_after(path, since, repo=REPO):
    """Commits touching `path` after commit `since` (exclusive). [] on any git trouble."""
    try:
        out = subprocess.run(["git", "log", "--format=%h", f"{since}..HEAD", "--", path],
                             cwd=repo, capture_output=True, text=True, timeout=20)
        return [l for l in out.stdout.split() if l]
    except Exception:
        return []


def evaluate(item, event=None, manifest=None, repo=None):
    """(due: bool, why: str). `event` is the moment asking, or None for a plain --check.
    `manifest`/`repo` default to the module globals AT CALL TIME (a drive may repoint them)."""
    manifest = manifest or MANIFEST
    repo = repo or REPO
    t = item["trigger"]
    kind = t.get("kind")
    if kind == "pack-version-bump":
        now = pack_version(manifest)
        was = item["parked"].get("at_version")
        if event not in (None, "release-cut"):
            return False, f"waits for release-cut (pack is {now}, parked at {was})"
        return (now != was), (f"pack version {was} → {now}" if now != was else f"pack still {was}")
    if kind == "file-changed":
        path, since = t["path"], item["parked"].get("at_commit")
        hits = commits_after(path, since, repo)
        ev = t.get("event")
        if event is not None and ev is not None and event != ev:
            return False, f"waits for {ev}"
        return bool(hits), (f"{path} changed in {len(hits)} commit(s) since {since}" if hits
                            else f"{path} unchanged since {since}")
    if kind == "event":
        name = t["name"]
        if event is None:
            return False, f"waits for the {name} event"
        return event == name, (f"the {name} event is now" if event == name else f"waits for {name}")
    raise SystemExit(f"parked: unknown trigger kind {kind!r} on {item['id']} — REFUSING")


def report(items, event=None, only_due=False, manifest=None, repo=None):
    live = [i for i in items if i["status"] == "parked"]
    rows = [(i, *evaluate(i, event, manifest, repo)) for i in live]
    due = [r for r in rows if r[1]]
    head = f"{MARK} — {len(due)} of {len(live)} parked item(s) due" + (f" at {event}" if event else "")
    print(head)
    for i, is_due, why in rows:
        if only_due and not is_due:
            continue
        flag = "⏰" if is_due else "…"
        print(f"  {flag} {i['id']} — {i['what']}\n       {why} · owner {i.get('owner', '?')} · parked {i['parked'].get('date')} #{i['parked'].get('session')}")
    return len(due)


def notice(event):
    """The hook other tools call: prints due items for `event`, swallows every error."""
    try:
        items = load()
        n = sum(1 for i in items if i["status"] == "parked" and evaluate(i, event)[0])
        if n:
            print(f"\n{MARK} — {n} parked item(s) are due at {event} — "
                  f"python3 knowledge/_parked.py --due {event}")
    except BaseException as e:  # a broken register must never break its host
        print(f"parked: notice skipped ({e.__class__.__name__})", file=sys.stderr)


def selftest():
    import tempfile
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    with tempfile.TemporaryDirectory() as d:
        man = os.path.join(d, "m.json")
        json.dump({"version": "v1.0.13"}, open(man, "w"))
        it = {"id": "P-1", "what": "x", "status": "parked", "owner": "Dave",
              "parked": {"date": "2026-09-13", "session": 269, "at_version": "v1.0.13"},
              "trigger": {"kind": "pack-version-bump"}}
        bite("pack-version-bump WAITS while the version is unchanged", evaluate(it, None, man)[0] is False)
        json.dump({"version": "v1.0.14"}, open(man, "w"))
        bite("…and is DUE once the manifest moves", evaluate(it, None, man)[0] is True)
        bite("…but not when a different event asks", evaluate(it, "dream-pass", man)[0] is False)
        ev = {"id": "P-2", "what": "y", "status": "parked", "parked": {"date": "d", "session": 1},
              "trigger": {"kind": "event", "name": "dream-pass"}}
        bite("event trigger fires only on its own event",
             evaluate(ev, "dream-pass")[0] and not evaluate(ev, "release-cut")[0] and not evaluate(ev, None)[0])
        fc = {"id": "P-3", "what": "z", "status": "parked", "parked": {"date": "d", "session": 1, "at_commit": "HEAD"},
              "trigger": {"kind": "file-changed", "path": "knowledge/_ruling_edges.json"}}
        bite("file-changed WAITS when nothing is after at_commit (HEAD..HEAD)", evaluate(fc, None)[0] is False)
        fc2 = dict(fc, parked={"date": "d", "session": 1, "at_commit": "HEAD~50"})
        bite("mutation: file-changed goes DUE when at_commit is 50 back and the file moved",
             evaluate(fc2, None)[0] is True or not commits_after("knowledge/_ruling_edges.json", "HEAD~50"))
        bad = dict(ev, trigger={"kind": "moon-phase"})
        try:
            evaluate(bad); bite("unknown trigger kind REFUSES", False)
        except SystemExit:
            bite("unknown trigger kind REFUSES", True)
        reg = os.path.join(d, "r.json")
        json.dump({"items": [{"id": "P-9", "status": "parked"}]}, open(reg, "w"))
        try:
            load(reg); bite("a malformed item REFUSES at load", False)
        except SystemExit:
            bite("a malformed item REFUSES at load", True)
        real = load()
        bite("the real register loads and every item has a legal trigger",
             all(i["trigger"].get("kind") in EVENT_OF_KIND for i in real))
        src = open(__file__, encoding="utf-8").read().split("def selftest")[0]
        bite("door has no write path", '"w"' not in src and "'w'" not in src)
    print("parked selftest:", "FAIL " + ", ".join(fails) if fails else "OK")
    return 1 if fails else 0


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    items = load()
    if "--list" in a:
        for i in items:
            print(f"  [{i['status']}] {i['id']} — {i['what']} · trigger {json.dumps(i['trigger'])}")
        return
    if "--due" in a:
        ev = a[a.index("--due") + 1] if a.index("--due") + 1 < len(a) else None
        if not ev:
            raise SystemExit("parked: --due needs an event name (release-cut · kg-edge-gen · dream-pass)")
        report(items, ev, only_due=True)
        return
    if "--check" in a or not a:
        report(items, None)
        return
    raise SystemExit(f"parked: unknown argument(s) {a} — see --help")


if __name__ == "__main__":
    main()
