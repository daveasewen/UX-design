#!/usr/bin/env python3
"""Launchpad step four — `choose(role, context)`, the chooser the agent calls (spec § 6, § 7).

One request (a mock role, a question, a clock, the items the agent asks to show, the screen's intent
context) in; the screen's parts out, with the reasons, the grant and refusal rows, and the ranker's record.

The order of work, each step a sentence of the proposal or a ruling:
  1. entitle  — role × tool × scope for every asked item, BEFORE any data is read; a refused item never
                reaches the chooser and is a `not_chosen` row naming the part it would have taken (entitle.py).
  2. fetch    — the mock tools return each granted item's data (mock/data.json); the payments list is
                checked against the £500,000 limit (prepare, never execute: s305-D49).
  3. context  — each item's intent context: its declared facts, its shape, and the counts read off its data.
  4. evaluate — the when-rules of the catalogue's parts over that context, variant B (when_eval.py).
  5. rank     — the seam (rank.py): rules order unless the switch is on; Jev is never imported.
  6. place    — the part chosen for the data is a tile only if it provides one of the four kinds the
                bento wall accepts, read from the wall's own `tiles` slot (s305-D18; Dave kept the four,
                s313-D41 "Keep the four"); otherwise it is a `not_chosen` row.
The frame (the page-frame part and the wall) is chosen from the request's own context.

Deterministic: no clock is read (the request carries `asked_at`), nothing is written, no socket is opened.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import when_eval as W  # noqa: E402
import entitle as E  # noqa: E402
import rank as R  # noqa: E402

MOCK = os.path.abspath(os.path.join(HERE, "..", "mock"))
SHAPE_SET = set(W.SHAPES)


def _ld(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


DATA = _ld(os.path.join(MOCK, "data.json"))
REQUESTS = _ld(os.path.join(MOCK, "requests.json"))
_CAT = {}


def catalogue(path=W.CATALOGUE):
    if path not in _CAT:
        cat = W.load_catalogue(path)
        _CAT[path] = (cat, W.parts_from_catalogue(cat))
    return _CAT[path]


_READ = {}


def _readings():
    if "r" not in _READ:
        _READ["r"] = W.alias_readings()
    return _READ["r"]


def the_wall(parts):
    """The part whose `tiles` slot accepts parts by what they provide (s305-D18), and that list."""
    for slug, p in sorted(parts.items()):
        acc = ((p.get("slots") or {}).get("tiles") or {}).get("accepts") or {}
        if acc.get("provides"):
            return slug, list(acc["provides"])
    return None, []


# ------------------------------------------------------------------ 2 · fetch (the mock tools)
def _cutoff_words(asked_at):
    a = datetime.datetime.fromisoformat(asked_at)
    c = datetime.datetime.fromisoformat(DATA["clock"]["cutoff"])
    mins = int((c - a).total_seconds() // 60)
    if mins <= 0:
        return "Cut-off passed"
    if mins % 60 == 0:
        h = mins // 60
        return "Cut-off in %d hour%s" % (h, "" if h == 1 else "s")
    return "Cut-off in %d min" % mins


def fetch(role, iid, asked_at):
    """What the granted tool returns for this item (mock). Only ever called after entitle granted it."""
    it = DATA["items"][iid]
    data = json.loads(json.dumps(it["data"]))
    settings = dict(it.get("settings") or {})
    flags = None
    if iid == "cut-off":  # time triggers act on what is shown, derived from the request's clock (spec § 6)
        settings["label"] = _cutoff_words(asked_at)
    if "prepare_approval" in it.get("actions", []):
        flags = []
        for rec in data.get("records", []):
            f = E.approval_flag(role, rec["amount"])
            rec["approval"] = f
            flags.append(f["flag"] if f["allowed"] else "refused")
    return data, settings, flags


# ------------------------------------------------------------------ 3 · the intent context
def item_context(it, data=None):
    """Declared facts + the shape + what the data says of itself. With data=None it is the item's contract
    only (used to name the part a refused item would have taken, without reading refused data)."""
    ctx = dict(it.get("facts") or {})
    if it.get("shape") in SHAPE_SET:
        ctx["shape"] = it["shape"]
    if data is not None:
        if isinstance(data.get("records"), list):
            ctx["records"] = len(data["records"])
        if isinstance(data.get("rows"), list):
            ctx["rows"] = len(data["rows"])
        if isinstance(data.get("series"), list):
            ctx["series"] = len(data["series"])
        if "delta" in data:
            ctx["delta"] = "present" if data["delta"] not in (None, 0) else "none"
    return ctx


# ------------------------------------------------------------------ the parts
def content_pool(parts):
    """Every published part that provides a role: the data picks its part from these, then the wall decides."""
    return sorted(s for s, p in parts.items() if p.get("provides"))


def _row(r, rank_no=None):
    out = {"part": r["slug"], "true_claims": r["trues"], "priority": r["priority"], "reasons": r["reasons"]}
    if rank_no is not None:
        out = {"part": r["slug"], "rank": rank_no, "true_claims": r["trues"], "priority": r["priority"],
               "reasons": r["reasons"]}
    return out


def choose(role, context, asks, question=None, asked_at=None, switch="off", catalogue_path=W.CATALOGUE):
    cat, parts = catalogue(catalogue_path)
    xc = (cat.get("x-apollo") or {}).get("catalogue") or {}
    wall, accepts = the_wall(parts)
    readings = _readings()
    items = DATA["items"]
    pool = content_pool(parts)

    ent = E.entitle_items(role, asks, items)
    not_chosen, tiles, flat, ranker_rows = [], [], [], []

    for ref in ent["refused"]:  # 1 · refused data never reaches the chooser: name the part by the contract only
        it = items[ref["item"]]
        guess = W.evaluate(item_context(it, None), parts, pool=pool)["pick"]
        why = ("%s refused for this role" % ref["tool"]) if ref["reason"] == "tool-not-granted" else (
            "%s at scope %s refused for this role" % (ref["tool"], ref["scope"]))
        not_chosen.append({"item": ref["item"], "part": guess, "why": why, "reason": ref["reason"]})

    for iid in asks:
        if iid not in ent["granted"]:
            continue
        it = items[iid]
        data, settings, flags = fetch(role, iid, asked_at)  # 2
        ctx = item_context(it, data)  # 3
        res = W.evaluate(ctx, parts, pool=pool)  # 4
        order, rrec = R.rank([r["slug"] for r in res["eligible"]], ctx, switch)  # 5
        ranker_rows.append(rrec)
        byslug = {r["slug"]: r for r in res["eligible"]}
        ranked = [byslug[s] for s in order]
        if not ranked:
            not_chosen.append({"item": iid, "part": None, "why": "no part's rule admits this data"})
            continue
        pick = ranked[0]
        prov = parts[pick["slug"]]["provides"]
        if prov not in accepts:  # 6 · the wall accepts parts by what they provide, and only the four
            not_chosen.append({"item": iid, "part": pick["slug"], "provides": prov,
                               "why": "not a tile: the bento wall accepts %s only (s305-D18, s313-D41)" % ", ".join(accepts)})
            continue
        p = parts[pick["slug"]]
        tile = {"item": iid, "tool": it["tool"], "scope": it.get("scope"), "context": ctx,
                "part": pick["slug"], "component": p["component"], "provides": prov, "proposal": p["proposal"],
                "true_claims": pick["trues"], "priority": pick["priority"], "reasons": pick["reasons"]}
        if p.get("aliases"):  # stat-card / kpi-tile resolve to metric: the reading is the spark slot, empty or filled
            has_series = bool(ctx.get("series")) and ctx.get("series") not in ("none", 0)
            want = "with trend" if has_series else "without trend"
            alias = [a for a in p["aliases"] if (readings.get(a) or {}).get("reading") == want]
            tile["reading"] = {"reading": want, "alias": alias[0] if alias else None,
                               "spark": "filled" if has_series else "empty"}
        if settings:
            bad = [k for k in settings if k not in p["settings"] or k in p["slots"]]
            tile["settings"] = {k: v for k, v in sorted(settings.items()) if k not in bad}
            if bad:
                tile["unknown_settings"] = sorted(bad)
        if flags is not None:
            tile["flags"] = flags
        tile["eligible"] = [_row(r, i + 1) for i, r in enumerate(ranked)]
        tile["excluded"] = [{"part": r["slug"], "why": r["why"]} for r in res["excluded"]]
        tiles.append(tile)
        for i, r in enumerate(ranked):
            row = _row(r, i + 1)
            row["item"] = iid
            flat.append(row)

    shell_pool = sorted(s for s, p in parts.items() if p.get("provides") == "page-frame")
    shell = W.evaluate(dict(context), parts, pool=shell_pool)
    wres = W.evaluate(dict(context), parts, pool=[wall]) if wall else {"pick": None, "eligible": [], "excluded": []}
    frame = {"shell": shell["pick"], "shell_reasons": shell["eligible"][0]["reasons"] if shell["eligible"] else [],
             "wall": wres["pick"], "wall_reasons": wres["eligible"][0]["reasons"] if wres["eligible"] else [],
             "accepts": accepts, "accepts_source": "the wall's tiles slot in the catalogue (s305-D18; kept by s313-D41)"}

    off = all(r["switch"] == "off" for r in ranker_rows)
    ranker = {"switch": "off" if (off and switch != "on") else "on", "answer": None, "fallback": "rules-order"}
    errs = sorted({r["error"] for r in ranker_rows if r.get("error")})
    if errs:
        ranker["error"] = errs
    if not errs and switch == "on" and ranker_rows and all(r.get("fallback") is None for r in ranker_rows):
        ranker = {"switch": "on", "answer": [r["answer"] for r in ranker_rows], "fallback": None}

    return {"role": role, "question": question, "asked_at": asked_at, "context": dict(context), "asks": list(asks),
            "catalogue": {"id": cat.get("catalogId"), "version": xc.get("version"), "sha256": xc.get("sha256"),
                          "metas_sha": xc.get("metas_sha")},
            "frame": frame, "chosen": [t["part"] for t in tiles], "tiles": tiles,
            "eligible": flat, "not_chosen": not_chosen, "grants": ent["grants"], "ranker": ranker}


def choose_request(req, switch="off", catalogue_path=W.CATALOGUE):
    return choose(req["role"], req.get("context") or {}, req["asks"], req.get("question"), req.get("asked_at"),
                  switch=switch, catalogue_path=catalogue_path)


def find_request(rid):
    for r in REQUESTS["worked_example"] + REQUESTS["fixtures"]:
        if r["id"] == rid:
            return r
    raise KeyError(rid)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Run the chooser on a mock request and print choose()'s JSON.")
    ap.add_argument("request", nargs="?", default="treasurer-0910",
                    help="a request id from mock/requests.json (default treasurer-0910)")
    ap.add_argument("--switch", default="off", choices=["off", "on"])
    ap.add_argument("--brief", action="store_true", help="print the parts and refusals only")
    a = ap.parse_args()
    out = choose_request(find_request(a.request), switch=a.switch)
    if a.brief:
        print("%s · frame %s + %s · tiles %s" % (a.request, out["frame"]["shell"], out["frame"]["wall"], out["chosen"]))
        for n in out["not_chosen"]:
            print("  not chosen:", n["item"], "->", n["part"], "·", n["why"])
        for g in out["grants"]:
            print("  grant:", g)
    else:
        print(json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True))
