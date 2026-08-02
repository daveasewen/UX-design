#!/usr/bin/env python3
"""`_state.json` — the task store. THE substrate change (#88, on Dave's #85-D1).

WHAT THIS REPLACES, precisely
-----------------------------
`_capture_gate.dofirst_index()` (`:1416`) runs `DOFIRST_ITEM_RE` over `GOOD-MORNING.md`'s prose
and renders a presence index. That is a RENDERER, not a store: an item's identity is its position
in a document, and it has no state, no owner, no age, and — the decisive omission — no stated
condition under which it would be finished. An item with no close condition cannot be closed; it
can only be DELETED, and deletion is correctly forbidden by [[home-by-addition-then-cut]] until a
probe proves the fact lives elsewhere. Items are therefore structurally immortal.

This module gives items identity and a close condition, and gates the condition on the way in.

⛔ WHAT THE #88 PROBE KILLED, AND WHY THIS FILE IS SMALLER THAN THE PROPOSAL ASKED FOR
--------------------------------------------------------------------------------------
`_MEMENTO-REBUILD-PROPOSAL-2026-08-02-v1.md` is #85's, and #88 probed it before building on it.
Three of its premises did not survive, and the survivors are what this file implements:

1. **"`closes_when` is the missing field" — FALSE as of #87.** `knowledge/_GOVERNING-RECORDS.md`
   already carries 17 rows, each with a ratified `closes_when`, ruled at #86-D1/D2 (Dave: "Yes,
   firm — record them"). So this store ABSORBS that register rather than inventing its concept.
   The register stays the human-readable face; this file is the machine-readable one, and
   `_migrate_state.py` GENERATES one from the other so they cannot disagree.

2. **"The list only grows" — UNPROVEN, and the reproducible series says otherwise.** The
   proposal's "95 item-slots over 12 sessions, 84 distinct" is not reproducible by any probe
   (same defect class as #86's "118 markers" → ~40). Replaying `DOFIRST_ITEM_RE` over the newest
   GM commit of each of the last 12 sessions gives 19 distinct item numbers, and the per-session
   series is 18,18,18,19,19,19,19,19,19,19,19,19 — FLAT, not accreting.
   ⇒ The case for this store is NOT "the list grows". It is that a flat list of 19 items which
   can never close is worse than a list that moves: immortality, not growth, is the defect.
   Stating this here because a rebuild justified by a dead number is how the next session
   inherits a false premise [[premise-ages-faster-than-rule]].

3. **"Extend `_decision-graph.json` with a `process` node type — same shape it already has" —
   FALSE.** Nodes have NO `type` field at all (100/100 absent), no node-level `state`, and the
   file runs TWO disagreeing lifecycle vocabularies: node `status` (accepted 85 · superseded 8 ·
   amended 6 · proposed 1) and a separate top-level `state` map (LIVE 84 · DEAD 8 · AMENDED 7 ·
   OPEN 1) — 85 vs 84 for the same population. Edge types have drifted to NINE, not the six the
   standing open item names.
   ⇒ #88 does NOT fold the graph. Reconciling two lifecycle vocabularies is a RULING, Dave's, and
   an agent quietly picking one is exactly the class of move the governing register exists to
   catch. This store LINKS to graph node ids (`links`) and leaves the graph alone. The
   reconciliation enters the register as its own row with its own `closes_when`.

THE GATE, AND WHY IT IS SHAPED THIS WAY
---------------------------------------
`check()` enforces: **you cannot open an item without stating what would end it.**

The 19 inherited DOFIRST items have no close condition and cannot be given one by an agent —
inventing a close condition for Dave's open work is the same overreach as inventing his ruling.
So they enter as `closes_when: null` with `condition: "UNCONDITIONED"`, and the gate treats them
as a DECLARED debt: a declared gap passes, a silent one fails [[instrument-without-a-consumer]].

⛔ The debt is FROZEN, not tolerated. `LEGACY_IDS` pins the exact inherited set at birth. Any id
outside that frozen set MUST carry a `closes_when` — so the unconditioned population can only
ever shrink. This is [[gate-inside-the-growth-loop]]: gate the PRESENCE of the defect, not its
drift, or the exemption becomes the new default and the store inherits the disease it replaces.

⚠ `check()` is BLOCKING by design and says so. A gate that only warns cannot make items mortal,
and a gate that does not run cannot fail [[instrument-without-a-consumer]] — its call site in
the capture ritual is the thing that makes this file real, not the code here.
"""

from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "_state.json")

SCHEMA = 1

# ---- the vocabulary. ONE lifecycle, unlike the graph's two. ------------------------------------
# ⚠ Deliberately NOT reusing the decision-graph's `status` words (`accepted`/`superseded`/...).
# Those describe a DESIGN DECISION's life; these describe a PIECE OF WORK's life. Borrowing the
# vocabulary would fuse two domains that close for different reasons — and the graph is already
# the cautionary tale, running two vocabularies that disagree by one.
STATES = ("open", "blocked", "ruled", "done", "dropped")
LIVE_STATES = ("open", "blocked", "ruled")      # still costs a session something
OWNERS = ("dave", "claude")

CONDITIONED = "stated"
UNCONDITIONED = "UNCONDITIONED"

REQUIRED = ("id", "title", "state", "opened", "owner", "condition", "closes_when", "links", "home")

# ⛔ THE FROZEN LEGACY SET — the inherited DOFIRST items, pinned at birth (#88).
# These 19 may carry `closes_when: null`. NOTHING ELSE MAY, EVER. Do not add to this tuple:
# growing it is the one edit that would turn a bounded debt back into an unbounded exemption,
# which is the exact failure mode this store exists to end.
LEGACY_IDS = (
    "W-0b", "W-0c", "W-0d", "W-01", "W-02", "W-03", "W-04", "W-05", "W-06", "W-07",
    "W-08", "W-09", "W-10", "W-11", "W-12", "W-13", "W-14", "W-15", "W-16",
)

ID_RE = re.compile(r"^(?:W-[0-9]{1,2}[a-z]?|G[0-9]{1,2}[a-z]?)$")


class StateError(Exception):
    """Raised loud and NAMED. A crash is not a fail [[a-crash-is-not-a-fail]] — callers that
    cannot distinguish a malformed store from a store with no items will report the wrong thing,
    so the two paths are different exception surfaces, not one silent empty list."""


# ---- load / save -------------------------------------------------------------------------------

def load(path=STORE):
    if not os.path.exists(path):
        raise StateError(f"{os.path.basename(path)} is MISSING — the store is not assumed empty")
    with open(path, encoding="utf-8") as f:
        try:
            doc = json.load(f)
        except json.JSONDecodeError as e:
            raise StateError(f"{os.path.basename(path)} is not valid JSON ({e}) — REFUSING to "
                             f"treat a parse failure as an empty worklist")
    if doc.get("meta", {}).get("schema") != SCHEMA:
        raise StateError(f"schema mismatch: store says {doc.get('meta', {}).get('schema')!r}, "
                         f"this module implements {SCHEMA}")
    return doc


def save(doc, path=STORE):
    doc["items"] = sorted(doc["items"], key=_sort_key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _sort_key(it):
    m = re.match(r"^([A-Z])-?([0-9]+)([a-z]?)$", it["id"])
    if not m:
        return (9, 0, "", it["id"])
    fam = {"W": 0, "G": 1}.get(m.group(1), 9)
    return (fam, int(m.group(2)), m.group(3), it["id"])


# ---- the gate ----------------------------------------------------------------------------------

def check(doc=None, path=STORE):
    """Return `(ok: bool, failures: list[str], notes: list[str])`.

    BLOCKING. Every failure names the item and quotes the offending value — a gate that reports
    "3 items invalid" cannot be acted on, and one that reports a count instead of the thing it
    forbids is [[gate-must-quote-what-it-forbids]].
    """
    if doc is None:
        doc = load(path)
    fails, notes = [], []
    items = doc.get("items")
    if not isinstance(items, list):
        raise StateError("store has no `items` list")

    seen = {}
    for it in items:
        iid = it.get("id", "<no id>")

        missing = [k for k in REQUIRED if k not in it]
        if missing:
            fails.append(f"{iid}: missing required field(s) {', '.join(missing)}")
            continue

        if not ID_RE.match(iid):
            fails.append(f"{iid}: id does not match {ID_RE.pattern!r}")
        if iid in seen:
            fails.append(f"{iid}: duplicate id — ids are stable and NEVER reused")
        seen[iid] = it

        if it["state"] not in STATES:
            fails.append(f"{iid}: state {it['state']!r} not in {STATES}")
        if it["owner"] not in OWNERS:
            fails.append(f"{iid}: owner {it['owner']!r} not in {OWNERS}")
        if not isinstance(it["opened"], int):
            fails.append(f"{iid}: opened {it['opened']!r} is not a session number")
        if not str(it.get("title", "")).strip():
            fails.append(f"{iid}: title is empty")

        # ---- THE CLOSE CONDITION. This is the whole point of the file. ----
        cond, cw = it["condition"], it["closes_when"]
        if cond == CONDITIONED:
            if not isinstance(cw, str) or not cw.strip():
                fails.append(f"{iid}: condition={CONDITIONED!r} but closes_when is {cw!r} — "
                             f"claiming a condition without stating one is worse than admitting "
                             f"there is none, because it passes")
            elif len(cw.strip()) < 12:
                fails.append(f"{iid}: closes_when {cw!r} is too short to be checkable — a "
                             f"condition that cannot be checked cannot fire")
        elif cond == UNCONDITIONED:
            if cw is not None:
                fails.append(f"{iid}: condition={UNCONDITIONED!r} but closes_when is {cw!r} — "
                             f"say which it is")
            if iid not in LEGACY_IDS:
                fails.append(
                    f"{iid}: UNCONDITIONED and NOT in the frozen legacy set. You cannot open an "
                    f"item without stating what would end it. The 19 inherited items are "
                    f"exempt because an agent may not invent Dave's close conditions; a NEW "
                    f"item has no such excuse.")
        else:
            fails.append(f"{iid}: condition {cond!r} must be {CONDITIONED!r} or {UNCONDITIONED!r}")

        if it["state"] in ("done", "dropped") and not str(it.get("closed_by", "")).strip():
            fails.append(f"{iid}: state={it['state']!r} with no `closed_by` — a close is a "
                         f"claim and carries its receipt")

    # ---- the declared debt, REPORTED not hidden ----
    unconditioned = [i["id"] for i in items if i.get("condition") == UNCONDITIONED]
    stale_legacy = [i for i in LEGACY_IDS if i not in seen]
    if unconditioned:
        notes.append(f"DECLARED DEBT: {len(unconditioned)} item(s) carry no close condition "
                     f"({', '.join(unconditioned)}). Frozen set size {len(LEGACY_IDS)} — this "
                     f"number may only fall. Each needs Dave's word, not an agent's guess.")
    if stale_legacy:
        notes.append(f"legacy ids retired since birth: {', '.join(stale_legacy)} "
                     f"(frozen set may shrink; it may never grow)")

    return (not fails), fails, notes


def add(doc, **fields):
    """Add an item. REFUSES without a close condition — the refusal is the feature."""
    it = {"links": [], "home": "", **fields}
    it.setdefault("condition", CONDITIONED if it.get("closes_when") else UNCONDITIONED)
    doc["items"].append(it)
    ok, fails, _ = check(doc)
    if not ok:
        mine = [f for f in fails if f.startswith(str(it.get("id")))]
        if mine:
            doc["items"].remove(it)
            raise StateError("REFUSED: " + "; ".join(mine))
    return it


# ---- queries the chain renders from ------------------------------------------------------------

def live(doc):
    return [i for i in doc["items"] if i["state"] in LIVE_STATES]


def counts(doc):
    """The counts the chain prints. GENERATED — never typed into prose.

    ★ #88's whole reason for existing: a typed count lies (#86 measured "118 markers" → ~40; the
    proposal's "95/84" is not reproducible by any probe). This function IS the count."""
    items = doc["items"]
    by_state = {s: sum(1 for i in items if i["state"] == s) for s in STATES}
    return {
        "total": len(items),
        "live": len(live(doc)),
        "by_state": by_state,
        "by_owner": {o: sum(1 for i in live(doc) if i["owner"] == o) for o in OWNERS},
        "unconditioned": sum(1 for i in items if i["condition"] == UNCONDITIONED),
        "conditioned": sum(1 for i in items if i["condition"] == CONDITIONED),
    }


def render_index(doc, width=None):
    """One-line presence index for the chain. No bodies, no truncation to 46 chars —
    the store holds the body, so the index does not have to carry it."""
    ls = live(doc)
    return " · ".join(f"`{i['id']}` {i['title']}" for i in ls)


# ---- selftest: MUTATION-TESTED, both directions ------------------------------------------------

def selftest():
    """Re-enact the defect the gate exists to catch. A green that cannot fail is an assertion,
    not a test [[gate-must-quote-what-it-forbids]] — so every bite below asserts BOTH that the
    healthy form passes AND that the mutated form fails, with the reason named."""
    fails = []

    def bite(name, doc, want_ok, want_substr=None):
        try:
            ok, fs, _ = check(doc)
        except StateError as e:
            ok, fs = False, [f"StateError: {e}"]
        if ok != want_ok:
            fails.append(f"[{name}] expected ok={want_ok}, got ok={ok} ({fs})")
            return
        if want_substr and not any(want_substr in f for f in fs):
            fails.append(f"[{name}] failed as expected but for the WRONG reason — "
                         f"wanted {want_substr!r} in {fs}")

    def healthy():
        return {"meta": {"schema": SCHEMA}, "items": [dict(
            id="G1", title="a governing item", state="open", opened=86, owner="dave",
            condition=CONDITIONED, closes_when="Dave ratifies 700 or names his own number",
            links=[], home="knowledge/_GOVERNING-RECORDS.md")]}

    # 1. control
    bite("control/healthy passes", healthy(), True)

    # 2. THE CENTRAL BITE — a new item with no close condition must be REFUSED
    d = healthy(); d["items"][0]["condition"] = UNCONDITIONED; d["items"][0]["closes_when"] = None
    bite("new item, no condition, REFUSED", d, False, "frozen legacy set")

    # 3. a legacy id may be unconditioned — the exemption is real, and bounded
    d = healthy(); d["items"][0].update(id=LEGACY_IDS[0], condition=UNCONDITIONED, closes_when=None)
    bite("legacy id, unconditioned, ALLOWED", d, True)

    # 4. claiming a condition without stating one — the worst case, because it passes a naive gate
    d = healthy(); d["items"][0]["closes_when"] = "   "
    bite("condition claimed, none stated", d, False, "worse than admitting")

    # 5. an uncheckable stub condition
    d = healthy(); d["items"][0]["closes_when"] = "later"
    bite("condition too short to check", d, False, "too short to be checkable")

    # 6. condition + closes_when disagreeing the other way
    d = healthy(); d["items"][0]["condition"] = UNCONDITIONED
    bite("unconditioned but carries a condition", d, False, "say which it is")

    # 7. vocabulary drift — an unknown condition word must not be waved through
    d = healthy(); d["items"][0]["condition"] = "pending"
    bite("unknown condition word", d, False, "must be")

    # 8. duplicate ids
    d = healthy(); d["items"].append(dict(d["items"][0]))
    bite("duplicate id", d, False, "NEVER reused")

    # 9. a close with no receipt
    d = healthy(); d["items"][0]["state"] = "done"
    bite("closed with no closed_by", d, False, "carries its receipt")

    # 10. missing field
    d = healthy(); del d["items"][0]["closes_when"]
    bite("missing required field", d, False, "missing required field")

    # 11. a malformed store must RAISE, not read as empty
    try:
        check({"meta": {"schema": SCHEMA}})
        fails.append("[malformed store] expected StateError, got a clean read")
    except StateError:
        pass

    # 12. counts are computed, not stored — mutate an item, the count must move
    d = healthy()
    before = counts(d)["live"]
    d["items"][0]["state"] = "done"
    if counts(d)["live"] != before - 1:
        fails.append("[counts move] counts() did not follow the data — it is not a measurement")

    return fails


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        fs = selftest()
        print("\n".join(fs) if fs else f"_state selftest: {12} bites, all GREEN")
        sys.exit(1 if fs else 0)
    ok, fails, notes = check()
    d = load()
    c = counts(d)
    print(f"items {c['total']} · live {c['live']} · conditioned {c['conditioned']} · "
          f"UNCONDITIONED {c['unconditioned']}")
    print(f"  by state: {c['by_state']}")
    print(f"  live by owner: {c['by_owner']}")
    for n in notes:
        print(f"  ⚠ {n}")
    for f in fails:
        print(f"  ⛔ {f}")
    sys.exit(0 if ok else 1)
