#!/usr/bin/env python3
"""_wrap_rows.py — the wrap's state-row writer: MINT, CLOSE, REOPEN and NOTE rows of
`knowledge/_state.json`, always BY ADDITION, always through `_state.py`'s own load → check → save.

Built #306 lane W1 for `s306-D4` phase 1 (Dave, 2026-09-28 16:58 BST, "go on both"). It replaces the
per-wrap `mint_30N.py` scripts (#303, #304, #305, each "modelled on" the last) and the per-lane
`store_batch.py` scripts (#305 H1, #306 T, U, V). What varied per wrap was only the rows; the code
was the same every time, and it lives here once.

THE RULES IT ENFORCES (each from the record, none new):
  · MINT of a document row is BORN CLOSED (`s305-D40`, `_state.DOC_BIRTH_FROM_SESSION`): state
    `done`, `closed_by` = "born closed (s305-D40): <home> filed at #<N> — the file is the record."
    A LIVE mint (`"live": true`) needs its own `closes_when` and is refused for a document home by
    `_state.check()` itself — this tool does not second-guess the store's gate, it runs it.
  · CLOSE sets `done` + `closed_by` and appends a dated body paragraph. It never edits `title`,
    `closes_when` or an earlier paragraph.
  · REOPEN sets `open` and appends a dated paragraph; `closed_by` is left as history.
  · NOTE appends a paragraph and changes nothing else.
  · Idempotent: a mint of an existing id, a close of a row already done, a reopen of a live row
    are SKIPPED and reported, never re-applied.
  · Every home and every non-row link must exist on disk (a row pointing at nothing is refused).
  · `_state.check()` must pass AFTER the batch or nothing is saved. DRY RUN unless `--write`.

SPEC (JSON):  {"session": 306, "by": "#306 W (2026-09-28)", "ops": [
   {"op": "mint",   "id": "W-306w", "title": "...", "home": "notes/_subreports/....md",
                    "links": [...], "body": "s218-D7 filed report. ...", "closes_when": "..."},
   {"op": "close",  "id": "W-305h", "closed_by": "...receipt...", "para": "optional"},
   {"op": "reopen", "id": "W-222",  "para": "why, with the ruling id"},
   {"op": "note",   "id": "W-305hr", "para": "..."} ]}

Usage:
  python3 knowledge/_wrap_rows.py --spec rows.json [--write] [--store PATH]
  python3 knowledge/_wrap_rows.py mint-doc --id W-306w1 --session 306 --home <report> --title T
          [--link P ...] [--body B] [--write]
  python3 knowledge/_wrap_rows.py --selftest
"""
import argparse
import copy
import datetime
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _state  # noqa: E402

LIVE = _state.LIVE_STATES


class RowError(Exception):
    """A named refusal. At the CLI it means: nothing was saved."""


def _para(it, p):
    it["body"] = ((it.get("body") or "").rstrip() + "\n\n" + p).lstrip()


def _exists(p, root):
    p = str(p).split("#", 1)[0].strip()
    return bool(p) and os.path.exists(os.path.join(root, p))


def apply(doc, spec, root=REPO):
    """Mutate `doc` in place; return the op receipts. Raises RowError on a malformed op."""
    n = spec.get("session")
    if not isinstance(n, int):
        raise RowError("spec.session must be the session number (int)")
    by = spec.get("by") or f"#{n} ({datetime.date.today().isoformat()})"
    rows = {i["id"]: i for i in doc["items"]}
    out = []
    for k, op in enumerate(spec.get("ops", [])):
        kind, iid = op.get("op"), op.get("id")
        if kind not in ("mint", "close", "reopen", "note") or not iid:
            raise RowError(f"op {k}: needs op in mint/close/reopen/note and an id — got {op!r}"[:200])
        if kind == "mint":
            if iid in rows:
                out.append((iid, "SKIP-exists", rows[iid]["state"])); continue
            if not _state.ID_RE.match(iid):
                raise RowError(f"{iid}: not a legal id ({_state.ID_RE.pattern})")
            for f in ("title", "home"):
                if not op.get(f):
                    raise RowError(f"{iid}: mint needs `{f}`")
            if not _exists(op["home"], root):
                raise RowError(f"{iid}: home `{op['home']}` does not exist")
            links = list(op.get("links") or [])
            bad = [l for l in links if not (l.startswith("W-") or l.startswith("G") and l[1:2].isdigit()) and not _exists(l, root)]
            if bad:
                raise RowError(f"{iid}: link(s) do not exist: {bad}")
            it = {"id": iid, "title": op["title"], "project": op.get("project", "apollo"),
                  "opened": n, "owner": op.get("owner", "claude"), "condition": "stated",
                  "home": op["home"], "links": links}
            if op.get("live"):
                if not op.get("closes_when"):
                    raise RowError(f"{iid}: a LIVE mint needs its own closes_when")
                it.update(state="open", closes_when=op["closes_when"])
            else:
                it.update(state="done", closes_when=op.get("closes_when", "the report is committed"),
                          closed_by=op.get("closed_by") or
                          f"born closed (s305-D40): {op['home']} filed at #{n} — the file is the record.")
            if op.get("body"):
                it["body"] = op["body"]
            doc["items"].append(it); rows[iid] = it
            out.append((iid, "minted-" + it["state"], it["title"][:70]))
            continue
        if iid not in rows:
            raise RowError(f"{iid}: no such row")
        it = rows[iid]
        if kind == "close":
            if not op.get("closed_by"):
                raise RowError(f"{iid}: close needs `closed_by` (the receipt)")
            if it["state"] not in LIVE and it["state"] != "parked":
                out.append((iid, "SKIP-already-" + it["state"], "")); continue
            was = it["state"]
            it["state"] = "done"; it["closed_by"] = op["closed_by"]
            _para(it, f"✅ CLOSED BY ADDITION {by} ({was} → done): {op.get('para') or op['closed_by']}")
            out.append((iid, "closed", was))
        elif kind == "reopen":
            if not op.get("para"):
                raise RowError(f"{iid}: reopen needs `para` (why, with its ruling or his words)")
            if it["state"] in LIVE:
                out.append((iid, "SKIP-already-live", it["state"])); continue
            was = it["state"]
            it["state"] = "open"
            _para(it, f"▶ REOPENED BY ADDITION {by} ({was} → open): {op['para']}")
            out.append((iid, "reopened", was))
        else:
            if not op.get("para"):
                raise RowError(f"{iid}: note needs `para`")
            if op["para"] in (it.get("body") or ""):
                out.append((iid, "SKIP-note-present", "")); continue
            _para(it, f"✎ {by} — BY ADDITION: {op['para']}")
            out.append((iid, "noted", it["state"]))
    return out


def run(spec, store=_state.STORE, write=False, root=REPO):
    doc = _state.load(store)
    before = _state.counts(doc)
    ok0, fails0, _ = _state.check(copy.deepcopy(doc))
    receipts = apply(doc, spec, root)
    ok, fails, notes = _state.check(doc)
    after = _state.counts(doc)
    res = {"write": write, "ops": receipts, "check_ok": ok, "fails": fails[:10],
           "pre_existing_fails": (not ok0), "before": {"total": before["total"], "live": before["live"]},
           "after": {"total": after["total"], "live": after["live"]}}
    if write:
        if not ok:
            raise RowError("`_state.check()` FAILS after the batch — nothing saved: " + "; ".join(fails[:3]))
        _state.save(doc, store)
    return res


# ------------------------------------------------------------------------------------ selftest
def selftest():
    ok_all = True

    def bite(name, cond):
        nonlocal ok_all
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok_all = ok_all and bool(cond)

    home_doc = "notes/_subreports/2026-09-28-306-V-limits-and-phase2.md"
    home_code = "knowledge/_state.py"
    real = _state.load()
    with tempfile.TemporaryDirectory() as td:
        store = os.path.join(td, "_state.json")
        _state.save(copy.deepcopy(real), store)
        live_id = next(i["id"] for i in real["items"] if i["state"] == "open")
        done_id = next(i["id"] for i in real["items"] if i["state"] == "done")
        spec = {"session": 306, "by": "#306 SELFTEST", "ops": [
            {"op": "mint", "id": "W-999z", "title": "fixture report", "home": home_doc, "links": [home_code, "W-306t"],
             "body": "s218-D7 filed report."},
            {"op": "close", "id": live_id, "closed_by": "fixture receipt"},
            {"op": "reopen", "id": done_id, "para": "fixture reason `s306-D4`"},
            {"op": "note", "id": live_id, "para": "a fixture note"}]}
        r = run(spec, store, write=False)
        bite("dry run: check passes on a copy of the real store", r["check_ok"])
        bite("dry run writes nothing", _state.load(store) == _state.load(store) and
             "W-999z" not in {i["id"] for i in _state.load(store)["items"]})
        r = run(spec, store, write=True)
        d = {i["id"]: i for i in _state.load(store)["items"]}
        bite("mint is BORN CLOSED with the s305-D40 receipt",
             d["W-999z"]["state"] == "done" and d["W-999z"]["closed_by"].startswith("born closed (s305-D40): " + home_doc))
        bite("close sets done + closed_by and appends, title untouched",
             d[live_id]["state"] == "done" and d[live_id]["closed_by"] == "fixture receipt"
             and "✅ CLOSED BY ADDITION #306 SELFTEST" in d[live_id]["body"]
             and d[live_id]["title"] == {i["id"]: i for i in real["items"]}[live_id]["title"])
        bite("reopen sets open and appends; closed_by kept as history",
             d[done_id]["state"] == "open" and "▶ REOPENED BY ADDITION" in d[done_id]["body"]
             and d[done_id].get("closed_by") == {i["id"]: i for i in real["items"]}[done_id].get("closed_by"))
        bite("earlier body text survives (by addition)",
             (({i["id"]: i for i in real["items"]}[live_id].get("body") or "").rstrip() in d[live_id]["body"]))
        r2 = run(spec, store, write=True)
        kinds = [k for _, k, _ in r2["ops"]]
        bite("a second run is idempotent (every op SKIPped)", all(k.startswith("SKIP") for k in kinds))
        for name, bad in [
            ("refuses a home that does not exist", {"op": "mint", "id": "W-998z", "title": "t", "home": "notes/nope-xyz.md"}),
            ("refuses a link that does not exist", {"op": "mint", "id": "W-998z", "title": "t", "home": home_doc, "links": ["nope/x.md"]}),
            ("refuses an illegal id", {"op": "mint", "id": "X-1", "title": "t", "home": home_doc}),
            ("refuses a close without a receipt", {"op": "close", "id": done_id}),
            ("refuses a reopen without a reason", {"op": "reopen", "id": live_id}),
            ("refuses a live mint without closes_when", {"op": "mint", "id": "W-998z", "title": "t", "home": home_code, "live": True}),
            ("refuses an unknown row", {"op": "note", "id": "W-997z", "para": "x"}),
        ]:
            try:
                run({"session": 306, "ops": [bad]}, store, write=True); bite(name, False)
            except RowError:
                bite(name, True)
        # a LIVE document row from #306 on is refused by _state.check() itself (s305-D40), not by us
        try:
            run({"session": 306, "ops": [{"op": "mint", "id": "W-996z", "title": "t", "home": home_doc,
                                          "live": True, "closes_when": "never"}]}, store, write=True)
            bite("a LIVE document row is refused by _state.check() (s305-D40) and nothing saved", False)
        except RowError as e:
            bite("a LIVE document row is refused by _state.check() (s305-D40) and nothing saved",
                 "W-996z" not in {i["id"] for i in _state.load(store)["items"]})
    print("wrap-rows selftest:", "PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--spec"); ap.add_argument("--store", default=_state.STORE)
    ap.add_argument("--write", action="store_true")
    sub = ap.add_subparsers(dest="verb")
    m = sub.add_parser("mint-doc")
    m.add_argument("--id", required=True); m.add_argument("--session", type=int, required=True)
    m.add_argument("--home", required=True); m.add_argument("--title", required=True)
    m.add_argument("--link", action="append", default=[]); m.add_argument("--body")
    m.add_argument("--write", action="store_true", dest="write2")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.verb == "mint-doc":
        spec = {"session": a.session, "ops": [{"op": "mint", "id": a.id, "title": a.title, "home": a.home,
                                                "links": a.link, "body": a.body or "s218-D7 filed report."}]}
        write = a.write or a.write2
    elif a.spec:
        spec = json.load(open(a.spec, encoding="utf-8")); write = a.write
    else:
        ap.print_help(); return 2
    try:
        r = run(spec, a.store, write=write)
    except (RowError, _state.StateError) as e:
        print("⛔ REFUSED:", e); return 1
    print(("WRITE" if write else "DRY-RUN"), "ops:", len(r["ops"]), "· check ok:", r["check_ok"],
          "· rows", r["before"]["total"], "→", r["after"]["total"], "· live", r["before"]["live"], "→", r["after"]["live"])
    for o in r["ops"]:
        print("  ", *o)
    for f in r["fails"]:
        print("   FAIL", f[:240])
    return 0 if r["check_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
