"""#313 lane AC4 — apply every wave-3 lane's notes/_lanes/313/<LANE>/rows.json to knowledge/_state.json.

The lanes wrote their row changes in five shapes (a list of {op,...}; a list of {action,...}; a dict with
`ops`; rows wrapped in `row`; a committer-mint placeholder). This normalises them and applies them through the
store's own load / add / check / save, all or nothing:
  add · mint · born-closed · add born-closed → _state.add() (report rows under notes/_subreports are closed at
      birth in the s305-D40 legal form; a `live` mint stays open)
  close · close_on_land → state done, closed_by the lane's own sentence + where it landed
  progress · note · note (by addition) → the lane's text appended to the row's body after a blank line, marked ✎
Usage: python3 notes/_lanes/313/AC4/apply_rows.py [--dry-run] LANE [LANE ...]
"""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state as S  # noqa: E402

LANDED = "landed by #313 lane AC4 in the wave-3 commits (2026-10-01)"
BORN = "born closed (s305-D40): %s filed at #313 — the file is the record."
# the store's id pattern allows at most two characters after the number (^W-[0-9]{1,3}([a-z][a-z0-9]?)?$);
# these lane ids broke it and are renumbered here, in the row and in every link that names them
RENUMBER = {"W-313gs1": "W-313g1", "W-313ch1": "W-313k1", "W-313b5b": "W-313b5", "W-313b5q": "W-313bq",
            "W-313b5n": "W-313bn", "W-313b4a": "W-313b4", "W-313b4b": "W-313bd", "W-313a2b": "W-313ab",
            "W-313a2c": "W-313ac", "W-313a2d": "W-313ad", "W-313b123": "W-313b1"}


def ops_of(lane):
    d = json.load(open(os.path.join(ROOT, "notes/_lanes/313", lane, "rows.json"), encoding="utf-8"))
    ops = d["ops"] if isinstance(d, dict) else d
    for o in ops:
        kind = (o.get("op") or o.get("action") or "").lower()
        yield kind, o


def new_row(lane, kind, o):
    r = dict(o.get("row") or {k: v for k, v in o.items() if k not in ("op", "action", "how", "$note", "live", "stays")})
    if not r.get("id") or r["id"].startswith("("):
        r["id"] = "W-313" + lane.lower()
    r["id"] = RENUMBER.get(r["id"], r["id"])
    if isinstance(r.get("links"), list):
        r["links"] = [RENUMBER.get(x, x) for x in r["links"]]
    r.setdefault("project", "apollo")
    r.setdefault("opened", 313)
    r.setdefault("owner", "claude")
    r.setdefault("condition", "stated")
    if r.get("home") == "notes/_subreports/2026-08-27-220-audit-L2.md#9":
        # A6's live row: '#9' occurs 56x in that report (not an address), and a live row may not live in a
        # report (s305-D40). Its home becomes the registry its close condition names; the report stays a link.
        r["home"] = "knowledge/tokens/themes/_themes.json"
        r["links"] = r.get("links", []) + ["notes/_subreports/2026-08-27-220-audit-L2.md"]
    home = r.get("home", "")
    report = home.startswith("notes/_subreports/2026-10-01-313-")            # this wave's own report rows
    if o.get("live") or kind == "open" or r.get("state") in ("open", "blocked", "ruled"):
        r.setdefault("state", "open")
        if r.get("home", "").startswith("notes/_subreports/"):
            # a live row may not live in a report (s305-D40): it homes on the lane's rows file, report linked
            r["links"] = r.get("links", []) + [r["home"]]
            r["home"] = "notes/_lanes/313/%s/rows.json" % lane
    elif report or "born" in kind or r.get("state") == "done":
        r["state"] = "done"
        r.setdefault("closes_when", "the report is committed")
        r["closed_by"] = BORN % home
    r.setdefault("state", "open")
    r.setdefault("closes_when", "")
    return r


def main(argv):
    dry = "--dry-run" in argv
    lanes = [a for a in argv if not a.startswith("--")]
    doc = S.load()
    byid = {i["id"]: i for i in doc["items"]}
    log = []
    for lane in lanes:
        for kind, o in ops_of(lane):
            if kind in ("add", "mint", "open", "born-closed", "add born-closed (s305-d40 form)"):
                r = new_row(lane, kind, o)
                if r["id"] in byid:
                    raise SystemExit("REFUSED: %s %s already in the store" % (lane, r["id"]))
                try:
                    S.add(doc, **r)
                except S.StateError as e:
                    if "UNRESOLVABLE" not in str(e) or "#" not in r.get("home", ""):
                        raise
                    # the anchor is not unique in its file (not an address): home on the file, anchor kept as a link
                    r["links"] = r.get("links", []) + [r["home"]]
                    r["home"] = r["home"].split("#")[0]
                    S.add(doc, **r)
                    log.append("%s %s home anchor not unique; homed on %s" % (lane, r["id"], r["home"]))
                byid[r["id"]] = doc["items"][-1]
                log.append("%s add %s (%s)" % (lane, r["id"], r["state"]))
            elif kind in ("close", "close_on_land"):
                it = byid[o["id"]]
                why = o.get("closed_by") or o.get("close_note") or ""
                it["state"] = "done"
                it["closed_by"] = (why + " — " if why else "") + LANDED
                log.append("%s close %s" % (lane, o["id"]))
            elif kind in ("progress", "note", "note (by addition)"):
                it = byid[o["id"]]
                text = o.get("note") or o.get("para") or o.get("body_addition") or o.get("append") or ""
                text = text if text.lstrip().startswith("✎") else "✎ " + text
                it["body"] = (it.get("body", "").rstrip() + "\n\n" + text).lstrip()
                log.append("%s progress %s" % (lane, o["id"]))
            else:
                raise SystemExit("REFUSED: %s op %r not understood" % (lane, kind))
    ok, fails, _ = S.check(doc)
    if not ok:
        raise SystemExit("REFUSED by the store gate:\n  " + "\n  ".join(fails[:12]))
    print("renumbered: " + ", ".join("%s -> %s" % kv for kv in RENUMBER.items()))
    print("\n".join(log))
    print("%d change(s) across %d lane(s); store gate OK%s" % (len(log), len(lanes), " (dry run, nothing written)" if dry else ""))
    if not dry:
        S.save(doc)


if __name__ == "__main__":
    main(sys.argv[1:])
