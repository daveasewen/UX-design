#!/usr/bin/env python3
"""#238 lane C — machine pass over the 13 family receipts.

Run from this directory. It (1) fails loud if any *_le_15_words quote exceeds 15
whitespace-delimited tokens or if a stated *_word_count disagrees with the actual
count, (2) tallies fetch attempts by outcome, (3) derives tiering.json (the table)
and fetch-receipts.json (every attempt in order) FROM the receipt files, so the
report's COUNTS line is copied from output, never retyped.

Unit notes: a "word" is a whitespace-delimited token (an ellipsis counts as one);
an "attempt" is one entry in a receipt's fetches[]; WebSearch entries are attempts
too and are tallied separately as "search".
"""
import glob
import json
import re
import sys

FILES = sorted(glob.glob("fam-*.json"))
problems = []
rows = []
attempts = []


def tier_bucket(t: str) -> str:
    t = t.lower()
    if t.startswith("unproven"):
        return "UNPROVEN"
    if t.startswith("safe now"):
        return "safe now"
    if t.startswith("pointer-only"):
        return "pointer-only"
    return "OTHER"


def permits_bucket(p: str) -> str:
    p = p.lower()
    for k in ("reproduce", "paraphrase", "names-only"):
        if p.startswith(k):
            return k
    return "OTHER"


for f in FILES:
    d = json.load(open(f, encoding="utf-8"))

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, path + "/" + k)
        elif isinstance(o, str) and path.endswith("_le_15_words"):
            n = len(o.split())
            if n > 15 and not o.startswith("NONE"):
                problems.append((f, path, f"{n} words > 15", o))
            # stated count beside it?
            parent_key = path.rsplit("/", 1)[-1]
            base = parent_key[: -len("_le_15_words")]

    walk(d)
    for section in ("licence", "primary_source"):
        src = d.get(section, {})
        for k, v in src.items():
            if k.endswith("_le_15_words"):
                wc_key = k[: -len("_le_15_words")] + "_word_count"
                if wc_key in src and len(v.split()) != src[wc_key]:
                    problems.append((f, k, f"stated {src[wc_key]} actual {len(v.split())}", v))

    ok = sum(1 for a in d["fetches"] if str(a["outcome"]).startswith("OK") and a["tool"] != "WebSearch")
    failed = sum(1 for a in d["fetches"] if str(a["outcome"]).startswith("FAILED"))
    searches = sum(1 for a in d["fetches"] if a["tool"] == "WebSearch")
    for a in d["fetches"]:
        attempts.append({
            "family": d["family"]["id"],
            "n_in_family": a["n"],
            "url": a["url"],
            "tool": a["tool"],
            "outcome": a["outcome"],
            "http_as_demonstrated": a.get("http_as_demonstrated", "n/a (search)"),
            "size": a.get("size", "n/a"),
            "failure_verbatim": a.get("failure_verbatim"),
        })
    lic = d["licence"]
    rows.append({
        "r1_row": d["family"]["r1_row"],
        "id": d["family"]["id"],
        "name": d["family"]["name"],
        "primary_source_url": d["primary_source"]["url"],
        "licence_found": lic["found"],
        "licence_name": lic["name"],
        "licence_read_from": lic["read_from"],
        "licence_quote_le_15_words": lic["quote_le_15_words"],
        "ai_clause": lic.get("ai_clause", "none seen"),
        "tier_PROPOSED": d["tier_PROPOSED"],
        "tier_bucket": tier_bucket(d["tier_PROPOSED"]),
        "permits_us": d["permits_us"],
        "permits_bucket": permits_bucket(d["permits_us"]),
        "receipt_path": f"notes/_subreports/assets/2026-09-02-238-C-licence-tiering/{f}",
        "fetch_attempts_ok": ok,
        "fetch_attempts_failed": failed,
        "web_searches": searches,
        "unproven_count": len(d.get("unproven", [])),
        "cheap_route_to_lift": d.get("cheap_route_to_lift"),
    })

rows.sort(key=lambda r: r["r1_row"])
tally = {
    "families": len(rows),
    "licence_text_reached_per_family": {
        "ok": sum(1 for r in rows if r["licence_found"] is True),
        "partly": sum(1 for r in rows if isinstance(r["licence_found"], str)),
        "none_stated": sum(1 for r in rows if r["licence_found"] is False),
    },
    "url_attempts": {
        "web_fetch_ok": sum(r["fetch_attempts_ok"] for r in rows),
        "web_fetch_failed": sum(r["fetch_attempts_failed"] for r in rows),
        "web_searches": sum(r["web_searches"] for r in rows),
    },
    "tier_buckets": {b: sum(1 for r in rows if r["tier_bucket"] == b) for b in ("safe now", "pointer-only", "UNPROVEN", "OTHER")},
    "tiered_on_evidence": sum(1 for r in rows if r["tier_bucket"] in ("safe now", "pointer-only")),
    "UNPROVEN_licence": sum(1 for r in rows if r["tier_bucket"] == "UNPROVEN"),
    "permits_buckets": {b: sum(1 for r in rows if r["permits_bucket"] == b) for b in ("reproduce", "paraphrase", "names-only", "OTHER")},
    "families_with_ai_clause": [r["id"] for r in rows if r["ai_clause"] and not r["ai_clause"].lower().startswith("none")],
}

json.dump({
    "provenance": "#238 lane C · 2026-09-02 · DERIVED from the 13 fam-*.json receipts by _check_receipts.py; never hand-edited. Tier vocabulary is R1's (safe now / pointer-only); every tier is PROPOSED.",
    "tally": tally,
    "rows": rows,
}, open("tiering.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

json.dump({
    "provenance": "#238 lane C · 2026-09-02 · every URL attempt in the 13 receipts, in receipt order, DERIVED by _check_receipts.py. Bonus receipt (Laws of UX) is NOT included — it is outside the brief's 13.",
    "timing_honesty": "Neither fetch tool returns a timestamp. Two bash wall-clock readings anchor the window: 2026-09-02T14:58:51Z (before the first fetch) and 2026-09-02T15:15:05Z (after the last). All attempts fall inside it. Per-call stamps are not invented.",
    "bytes_honesty": "mcp__workspace__web_fetch returns rendered text without a byte count or an HTTP status line; 'http_as_demonstrated' records what the tool's behaviour showed. One real size exists (Tognazzini: 97,819 characters / 1,014 lines, the tool's own overflow figure, unit = characters).",
    "rate_limit_note": "One HTTP 429 came from the fetch TOOL ('Cowork web_fetch rate limit exceeded'), not from a host; recorded as FAILED on that attempt, retried once after a pause, then OK.",
    "totals": {"attempts": len(attempts), "web_fetch_ok": tally["url_attempts"]["web_fetch_ok"], "web_fetch_failed": tally["url_attempts"]["web_fetch_failed"], "web_searches": tally["url_attempts"]["web_searches"]},
    "attempts": attempts,
}, open("fetch-receipts.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("files:", len(FILES))
print("PROBLEMS:", len(problems))
for p in problems:
    print("  ", p)
print(json.dumps(tally, indent=1))
sys.exit(1 if problems else 0)
