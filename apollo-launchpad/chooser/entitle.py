#!/usr/bin/env python3
"""Launchpad step four — role × tool × scope, the grant / refuse table (spec § 6).

Runs BEFORE the evaluator: a data item whose tool or scope is refused never reaches the chooser
("refused data never reaches the chooser", spec § 7), and every grant and every refusal is a row for the
screen's record ("role, tool, scope, allowed or refused", proposal § How it is enforced).

Refusal reasons are the spec's two: `tool-not-granted`, `scope-not-granted`.
`prepare_approval` prepares, never executes (s305-D49); above the mock limit it returns the
`second-approver` flag and is never prepared.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MOCK = os.path.abspath(os.path.join(HERE, "..", "mock"))


def _ld(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


ROLES_DOC = _ld(os.path.join(MOCK, "roles.json"))
TOOLS = ROLES_DOC["tools"]
ROLES = ROLES_DOC["roles"]
LIMIT = ROLES_DOC["limit"]


def grant(role, tool, scope=None):
    """One row: may `role` call `tool` (at `scope`, when the data asks for one)?"""
    grants = ROLES[role]["grants"]
    if tool not in grants:
        return {"tool": tool, "scope": None, "allowed": False, "reason": "tool-not-granted"}
    have = grants[tool]
    if scope is not None and have != scope:
        return {"tool": tool, "scope": have, "allowed": False, "reason": "scope-not-granted", "asked_scope": scope}
    return {"tool": tool, "scope": have, "allowed": True}


def matrix():
    """Every mock role × every tool: the 4 × 7 grant matrix (T4.4)."""
    return {r: {t: grant(r, t) for t in TOOLS} for r in sorted(ROLES)}


def entitle_items(role, item_ids, items):
    """Split the asked items into granted and refused, and the grant rows touched, in first-touch order.
    The `dashboard` call itself is always the first row. An item that names `actions` (a tool the screen
    offers on it, e.g. prepare_approval on the payments list) touches that tool's grant as well."""
    rows, seen = [], set()

    def touch(row):
        key = (row["tool"], row.get("asked_scope"))
        if key not in seen:
            seen.add(key)
            rows.append(row)

    touch(grant(role, "dashboard"))
    granted, refused = [], []
    for iid in item_ids:
        it = items[iid]
        row = grant(role, it["tool"], it.get("scope"))
        touch(row)
        if row["allowed"]:
            granted.append(iid)
            for act in it.get("actions", []):
                touch(grant(role, act))
        else:
            refused.append({"item": iid, "tool": it["tool"], "scope": it.get("scope"), "reason": row["reason"]})
    return {"grants": rows, "granted": granted, "refused": refused}


def approval_flag(role, amount):
    """prepare_approval at `up-to-limit`: within the limit it may be prepared; above it the payment is
    flagged `second-approver` and never prepared. A role without the tool gets the refusal row back."""
    g = grant(role, "prepare_approval")
    if not g["allowed"]:
        return {"allowed": False, "reason": g["reason"], "flag": None}
    if amount > LIMIT["amount"]:
        return {"allowed": True, "flag": LIMIT["above"], "prepared": False}
    return {"allowed": True, "flag": "within-limit", "prepared": False}


if __name__ == "__main__":
    m = matrix()
    print("%-22s " % "role \\ tool" + " ".join("%-18s" % t for t in TOOLS))
    for r in sorted(m):
        print("%-22s " % r + " ".join("%-18s" % ((m[r][t]["scope"] or "yes") if m[r][t]["allowed"] else "REFUSED") for t in TOOLS))
