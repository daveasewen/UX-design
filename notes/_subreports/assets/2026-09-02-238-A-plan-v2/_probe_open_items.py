#!/usr/bin/env python3
"""_probe_open_items.py — #238 lane A. For each of the 28 items plan v2 §10 lists as OPEN, grep
knowledge/_rulings.json (`ruled` + `says`, every ruling, case-insensitive) for the item's terms and
write open-items-probe.json beside this script. A row is listed as open on the claim that no
ruling CLOSES it; this probe makes that claim falsifiable — the hits are printed so a reader can see
that every hit is the ruling that OPENS or NAMES the item, not one that answers it.

Usage: python3 _probe_open_items.py            (writes open-items-probe.json, prints the table)
"""
import datetime as _dt
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
STORE = os.path.join(REPO, "knowledge", "_rulings.json")

ITEMS = [
    (1, "the four ask-whens", r"ask.when"),
    (2, "the 21 FLOATED defaults", r"21 open polarit|derived defaults|factory mints"),
    (3, "which side is conservative", r"conservative"),
    (4, "the gestalt collision", r"gestalt"),
    (5, "L1 Q1 missing receipt blocking", r"receipt.strict|NO-RECEIPT|missing receipt"),
    (6, "L1 Q2 composed page CSS", r"gen_snippet_tokens|composed page.{0,40}css|spliced.{0,30}style"),
    (7, "L1 Q3 dashboards in screen-gate index", r"screen.gate index|dashboards/\*"),
    (8, "G Q1 movable borrow-matrix cells", r"borrow.matrix|P7/P|P10/M|matrix cell"),
    (9, "G Q2 pr-dsa25 refutation_probe", r"refutation_probe"),
    (10, "G Q3 ISO names-only depth", r"names.only|9241"),
    (11, "the 13 untiered families", r"untiered|13 untiered"),
    (12, "the 12 explainedBy touchpoints", r"touchpoint"),
    (13, "the bedrock question", r"bedrock"),
    (14, "pattern-first retrieval set", r"retrieval set"),
    (15, "intent that GENERATES the brief", r"intent artefact|GENERATES the brief"),
    (16, "P6a two-hook trial built", r"PreToolUse|two.{0,20}hooks"),
    (17, "P6e derived HELD file built", r"release.authorisation|HELD IS MACHINE"),
    (18, "P6f eval suite after L2", r"eval suite|FROZEN EVAL"),
    (19, "P6b band breach mints a row", r"breach mints|mints a row|band breach"),
    (20, "P6c edit the gate you are graded by", r"graded by"),
    (21, "P6d severity vocabulary for reviews", r"severity vocab|Important.vs.Nit|nit cap"),
    (22, "principle-node fields not ruled", r"scope_conditions|superseded_by|author_revised|known_misreadings|expiry"),
    (23, "Defaults used field capacity", r"Defaults used"),
    (24, "the eight backlog ideas", r"information scent|situation.awareness|Cleveland|comprehension harness|worktree|mock-diff|rails-file writer|shifts table"),
    (25, "reading the primaries", r"Crossref|read the paper|primaries read"),
    (26, "W-355 deadlock", r"W-355|CHAIN OVERTAKEN|SESSION_ACK"),
    (27, "v1.0.6 L3-L5", r"\bL3\b|\bL4\b|\bL5\b|row-height"),
    (28, "lane V launched", r"lane V\b|verifier lane|238-V"),
]


def main():
    d = json.load(open(STORE, encoding="utf-8"))["rulings"]
    out = {"$description": "plan v2 §10 open-items probe over knowledge/_rulings.json (ruled + says, all rulings, case-insensitive). Hits are LISTED, not judged: the claim is that none of them closes the item.",
           "generated_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "store_rulings": len(d), "rows": []}
    for n, name, pat in ITEMS:
        rx = re.compile(pat, re.I)
        hits = [e["id"] for e in d if rx.search((e.get("ruled") or "") + " " + (e.get("says") or ""))]
        out["rows"].append({"row": n, "item": name, "pattern": pat, "hits": hits})
        print(f"{n:2d} {name:42s} {pat[:38]:38s} -> {len(hits):2d} {hits}")
    json.dump(out, open(os.path.join(HERE, "open-items-probe.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
