#!/usr/bin/env python3
"""_wrap_facts.py — measures every figure a wrap needs, in one command, and writes them as JSON.

Built #306 lane W1 for `s306-D4` phase 1 (Dave, 2026-09-28 16:58 BST, "go on both"). Phase 3 will
make its output `FACTS.json`, the one measured source every generated view copies from; for now it
writes to the path the caller names. It replaces the hand-typed figure blocks of the #303–#305
wrap seats (`names_30N.py`'s FILL_BOOT / FILL_WRAP / SHAS / RUNS, the one-liners in each W report's
REPLAY-THESE, and the hand sums in each stratum).

IT IS A READER. It writes ONE file, `--out`, and nothing else; git is read with
`--no-optional-locks` only. Every figure carries its unit and its source.

FIGURES:
  rulings  total · newest id (max by session, then D-number) · last id in the file · by status ·
           and, with --rulings-base SHA, the total there (the "638 → 699" pair)
  store    `_state.counts()` (IMPORTED): total, live, by state, by owner
  carries  `_wrap_carries.count_text()` → `_capture_gate._carry_items()` on the newest section
  sizes    bytes of the wrap's files (the unit is BYTES, named); with --session, also
           `_gm_usage.sizes_line()` (its own method label travels with it)
  git      HEAD, origin/master (the local ref — no network), commits ahead, and with --since SHA
           the commit count SHA..HEAD
  fill     from --transcript: the conductor's window FILL, a HAND SUM of input_tokens +
           cache_creation_input_tokens + cache_read_input_tokens (`_checkin.FILL_FIELDS`, IMPORTED)
           of the last record per distinct message.id, main thread only (sidechain and synthetic
           all-zero records skipped, as `_checkin.read_fill` skips them); boot, now, peak, turns,
           and the first message over each window line of `_gauge_tokens` (IMPORTED). `--until`
           cuts at an ISO time (the message that launched the wrap seat). Cross-checked against
           `_checkin.read_fill()` on the same file: a disagreement REFUSES, never averages.
  subs     from --subagents-dir: the final FILL of each sub transcript, summed. UNIT: real
           tokens, QUOTA not window FILL — never added to `fill`.

ds-021 (C) DECLARATION. This file counts NO cl100k tokens: the fill is the API's own usage
accounting, read off the transcript, the method `knowledge/_checkin.py` (MEASURERS: 'real')
already owns. It is therefore NOT a counting site under `_capture_gate.unit_vocabulary_audit`'s
test (a tiktoken encoding call for cl100k — the literal is not written here, because the audit reads
TEXT and this sentence would register as one; found by the wrap gate at this tool's first run),
and pinning it in MEASURERS would trip that audit's stale-pin bite. The unit is named on every line it prints instead. `sizes` are BYTES; the
section-sizes line is `_gm_usage`'s, carrying `_capture_gate.measure_tokens()`'s method label.

Usage:
  python3 knowledge/_wrap_facts.py --out F.json [--at SHA] [--rulings-base SHA] [--since SHA]
      [--session N] [--transcript T.jsonl [--until ISO]] [--subagents-dir D [--exclude NAME]]
  python3 knowledge/_wrap_facts.py --selftest
"""
import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SIZED = ["GOOD-MORNING.md", "_LIVE-STATE.md", "_CHAIN.md", "_CARRIES.md", "knowledge/_rulings.json",
         "knowledge/_state.json", "knowledge/_RUNBOOK-capture-ritual.md"]
RID = re.compile(r"^s(\d+)-D(\d+)$")
ENV = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}


class FactsError(Exception):
    """A named refusal: an UNKNOWN is declared, never defaulted to a number."""


def _git(repo, *a):
    r = subprocess.run(["git", "--no-optional-locks", *a], cwd=repo, capture_output=True, env=ENV)
    return r.returncode, r.stdout.decode("utf-8", "replace").strip()


def read(repo, rel, at=None):
    if at:
        rc, out = _git(repo, "show", f"{at}:{rel}")
        if rc:
            raise FactsError(f"git show {at}:{rel} failed")
        return out + "\n"
    with open(os.path.join(repo, rel), encoding="utf-8") as f:
        return f.read()


def rulings_facts(doc):
    rs = doc["rulings"] if isinstance(doc, dict) else doc
    ids = [r.get("id", "") for r in rs]
    keyed = [(int(m.group(1)), int(m.group(2)), i) for i in ids for m in [RID.match(i)] if m]
    st = {}
    for r in rs:
        st[r.get("status", "?")] = st.get(r.get("status", "?"), 0) + 1
    return {"total": len(rs), "newest": max(keyed)[2] if keyed else None, "last_in_file": ids[-1] if ids else None,
            "by_status": dict(sorted(st.items())), "unit": "rulings (entries in _rulings.json)"}


def store_facts(doc):
    import _state
    c = _state.counts(doc)
    return {k: c[k] for k in ("total", "live", "by_state", "by_owner")} | {"unit": "rows of _state.json"}


def git_facts(repo, since=None, at=None):
    tip = at or "HEAD"
    rc, head = _git(repo, "rev-parse", tip)
    if rc:
        raise FactsError(f"git rev-parse {tip} failed")
    _, om = _git(repo, "rev-parse", "--verify", "-q", "origin/master")
    out = {"head": head, "origin_master": om or None}
    if om and not at:
        out["ahead_of_origin"] = int(_git(repo, "rev-list", "--count", f"{om}..{head}")[1] or 0)
    if since:
        rc, n = _git(repo, "rev-list", "--count", f"{since}..{head}")
        if rc:
            raise FactsError(f"git rev-list {since}..{head} failed")
        _, s = _git(repo, "rev-parse", since)
        out["since"] = {"sha": s, "commits": int(n), "range": f"{s[:8]}..{head[:8]}"}
    return out


def size_facts(repo, at=None, session=None):
    b = {}
    for rel in SIZED:
        if at:
            rc, n = _git(repo, "cat-file", "-s", f"{at}:{rel}")
            b[rel] = int(n) if rc == 0 else None
        else:
            p = os.path.join(repo, rel)
            b[rel] = os.path.getsize(p) if os.path.exists(p) else None
    out = {"bytes": b, "unit": "bytes"}
    if session and not at:
        import _gm_usage
        line, errs = _gm_usage.sizes_line(session, repo=repo)
        out["section_sizes_line"] = line
        if errs:
            out["section_sizes_errors"] = errs
    return out


def _turns(path, until=None):
    """[(message_id, total, timestamp)] — main thread, last record per id, synthetic skipped."""
    import _checkin
    order, last = [], {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("isSidechain"):
                continue
            ts = rec.get("timestamp")
            if until and ts and ts > until:
                continue
            msg = rec.get("message") or {}
            u = msg.get("usage")
            if not isinstance(u, dict):
                continue
            tot = _checkin._total_in(u)
            if tot == 0 or "synthetic" in str(msg.get("model") or ""):
                continue
            mid = msg.get("id") or rec.get("uuid")
            if mid not in last:
                order.append(mid)
            last[mid] = (tot, ts)
    return [(m, last[m][0], last[m][1]) for m in order]


def fill_facts(path, until=None):
    import _checkin
    import _gauge_tokens as g
    t = _turns(path, until)
    if not t:
        raise FactsError(f"no usage record in {path} — an ABSENCE OF A MATCH, not a zero")
    lines = {"BUDGET_AMBER": g.BUDGET_AMBER, "STOP_LINE_TK": g.STOP_LINE_TK, "BUDGET_WORKING": g.BUDGET_WORKING,
             "TOLERATED_TK": g.TOLERATED_TK, "BUDGET_HARD": g.BUDGET_HARD}
    cross = {}
    for name, v in sorted(lines.items(), key=lambda kv: kv[1]):
        k = next((i for i, (_, tot, _) in enumerate(t) if tot > v), None)
        cross[f"{name} {v:,}"] = None if k is None else {"message": k + 1, "fill": t[k][1], "at": t[k][2]}
    out = {"unit": "real tokens — window FILL, API usage (input + cache_creation + cache_read), last record "
                   "per message.id, main thread; a hand sum, never throughput",
           "transcript": path, "until": until, "turns": len(t), "boot": t[0][1], "now": t[-1][1],
           "now_at": t[-1][2], "peak": max(x[1] for x in t), "crossings": cross,
           "boot_ceiling": {"BOOT_CEILING_TK": g.BOOT_CEILING_TK, "over_by": t[0][1] - g.BOOT_CEILING_TK}}
    if not until:
        rf = _checkin.read_fill(path)
        if rf.get("available") and (rf["boot"], rf["turns"]) != (out["boot"], out["turns"]):
            if rf["now"] != out["now"]:
                raise FactsError(f"two readings of one transcript disagree: _checkin.read_fill now {rf['now']:,} "
                                 f"vs this hand sum {out['now']:,} — refused, not averaged")
        out["read_fill_agrees"] = bool(rf.get("available")) and rf["now"] == out["now"] and rf["boot"] == out["boot"]
    return out


def subs_facts(d, exclude=()):
    import _checkin
    rows = []
    for p in sorted(glob.glob(os.path.join(d, "*.jsonl"))):
        if os.path.basename(p) in exclude:
            continue
        rf = _checkin.read_fill(p)
        if rf.get("available"):
            rows.append((os.path.basename(p), rf["now"]))
    if not rows:
        raise FactsError(f"no sub transcript with usage under {d}")
    return {"unit": "real tokens, QUOTA not window FILL — never added to `fill`", "n": len(rows),
            "total": sum(r[1] for r in rows), "largest": max(r[1] for r in rows), "smallest": min(r[1] for r in rows),
            "excluded": list(exclude)}


def measure(repo=REPO, at=None, rulings_base=None, since=None, session=None, transcript=None, until=None,
            subagents_dir=None, exclude=()):
    f = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
         "tree": at or "working tree", "tool": "knowledge/_wrap_facts.py"}
    f["rulings"] = rulings_facts(json.loads(read(repo, "knowledge/_rulings.json", at)))
    if rulings_base:
        f["rulings"]["base"] = {"sha": rulings_base,
                                "total": rulings_facts(json.loads(read(repo, "knowledge/_rulings.json", rulings_base)))["total"]}
    f["store"] = store_facts(json.loads(read(repo, "knowledge/_state.json", at)))
    import _wrap_carries
    f["carries"] = _wrap_carries.count_text(read(repo, "_CARRIES.md", at)) | {"unit": "carried items (`_carry_items`)"}
    f["sizes"] = size_facts(repo, at, session)
    f["git"] = git_facts(repo, since, at)
    if transcript:
        f["fill"] = fill_facts(transcript, until)
    if subagents_dir:
        f["subs"] = subs_facts(subagents_dir, exclude)
    return f


def lines(f):
    r = f["rulings"]
    out = [f"rulings: {r['total']:,} ({r['unit']}), newest {r['newest']}, last in file {r['last_in_file']}"
           + (f" · at {r['base']['sha']}: {r['base']['total']:,} → {r['total']:,}" if "base" in r else "")]
    s = f["store"]
    out.append(f"store: {s['total']:,} rows, {s['live']:,} live ({s['unit']})")
    c = f["carries"]
    out.append(f"carries #{c['section']}: {c['items']:,} ({c['unit']})")
    out.append("sizes (bytes): " + " · ".join(f"{k.rsplit('/', 1)[-1]} {v:,}" for k, v in f["sizes"]["bytes"].items() if v is not None))
    if f["sizes"].get("section_sizes_line"):
        out.append(f["sizes"]["section_sizes_line"].lstrip("> "))
    g = f["git"]
    out.append(f"git: HEAD {g['head'][:8]} · origin/master {(g['origin_master'] or '?')[:8]}"
               + (f" · {g['ahead_of_origin']} ahead" if "ahead_of_origin" in g else "")
               + (f" · {g['since']['commits']} commits {g['since']['range']}" if "since" in g else ""))
    if "fill" in f:
        x = f["fill"]
        out.append(f"FILL (real tokens, window FILL, API usage hand sum): boot {x['boot']:,} · now {x['now']:,} "
                   f"at {x['now_at']} · peak {x['peak']:,} · {x['turns']} messages")
    if "subs" in f:
        x = f["subs"]
        out.append(f"subs {x['total']:,} tokens (n={x['n']}) — real tokens, QUOTA not window FILL")
    return out


# ------------------------------------------------------------------------------------ selftest
def selftest():
    ok = True

    def bite(name, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok = ok and bool(cond)

    rf = rulings_facts({"rulings": [{"id": "s9-D2", "status": "ruled"}, {"id": "s10-D1", "status": "enacted"},
                                    {"id": "s9-D10", "status": "ruled"}]})
    bite("rulings: newest is max by session then D (s10-D1), not the last in the file (s9-D10)",
         rf["newest"] == "s10-D1" and rf["last_in_file"] == "s9-D10" and rf["total"] == 3
         and rf["by_status"] == {"enacted": 1, "ruled": 2})
    with tempfile.TemporaryDirectory() as td:
        u = lambda i, c, r, o=5: {"input_tokens": i, "cache_creation_input_tokens": c, "cache_read_input_tokens": r, "output_tokens": o}
        recs = [
            {"timestamp": "2026-01-01T10:00:00Z", "message": {"id": "m1", "model": "claude", "usage": u(10, 100, 0)}},
            {"timestamp": "2026-01-01T10:00:01Z", "message": {"id": "m1", "model": "claude", "usage": u(10, 100, 0, 50)}},
            {"timestamp": "2026-01-01T10:01:00Z", "isSidechain": True, "message": {"id": "sx", "model": "claude", "usage": u(1, 999999, 0)}},
            {"timestamp": "2026-01-01T10:02:00Z", "message": {"id": "m2", "model": "<synthetic>", "usage": u(0, 0, 0)}},
            {"timestamp": "2026-01-01T10:03:00Z", "message": {"id": "m3", "model": "claude", "usage": u(5, 170000, 110)}},
            {"timestamp": "2026-01-01T10:04:00Z", "message": {"id": "m4", "model": "claude", "usage": u(5, 1000, 330000)}},
            "not json",
        ]
        p = os.path.join(td, "t.jsonl")
        open(p, "w").write("\n".join(r if isinstance(r, str) else json.dumps(r) for r in recs) + "\n")
        x = fill_facts(p)
        bite("fill: boot 110 · now 331,005 · 3 messages (dup id once, sidechain + synthetic skipped)",
             x["boot"] == 110 and x["now"] == 331005 and x["turns"] == 3 and x["peak"] == 331005)
        bite("fill: the unit is named on the figure", x["unit"].startswith("real tokens — window FILL"))
        bite("fill agrees with _checkin.read_fill on the same file", x["read_fill_agrees"])
        bite("fill: the first message over BUDGET_AMBER is the 2nd (170,115)",
             next(v for k, v in x["crossings"].items() if k.startswith("BUDGET_AMBER"))["fill"] == 170115)
        y = fill_facts(p, until="2026-01-01T10:03:30Z")
        bite("fill --until cuts at the launch time (now 170,115, 2 messages)", y["now"] == 170115 and y["turns"] == 2)
        e = os.path.join(td, "empty.jsonl"); open(e, "w").write('{"message": {}}\n')
        try:
            fill_facts(e); bite("fill refuses a transcript with no usage (never 0)", False)
        except FactsError:
            bite("fill refuses a transcript with no usage (never 0)", True)
        sd = os.path.join(td, "subs"); os.makedirs(sd)
        for name, n in (("a.jsonl", 1000), ("b.jsonl", 2500), ("self.jsonl", 9)):
            open(os.path.join(sd, name), "w").write(json.dumps({"message": {"id": "q", "model": "c", "usage": u(0, n, 0)}}) + "\n")
        s = subs_facts(sd, exclude=("self.jsonl",))
        bite("subs: summed final FILL per sub, the named one excluded (3,500, n=2)", s["total"] == 3500 and s["n"] == 2)
        g = lambda *a: subprocess.run(["git", *a], cwd=td, capture_output=True, env={**ENV, "GIT_AUTHOR_NAME": "t",
                                      "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
        g("init", "-q")
        for i in range(3):
            open(os.path.join(td, "f.txt"), "w").write(str(i)); g("add", "f.txt"); g("commit", "-qm", f"c{i}")
        first = _git(td, "rev-list", "--max-parents=0", "HEAD")[1]
        gf = git_facts(td, since=first)
        bite("git: 2 commits since the root, HEAD read, no origin → None", gf["since"]["commits"] == 2 and gf["origin_master"] is None)
        before = sorted(os.listdir(td))
        _ = size_facts(td)
        bite("a reader: measuring wrote nothing", sorted(os.listdir(td)) == before)
    print("wrap-facts selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out"); ap.add_argument("--at"); ap.add_argument("--rulings-base"); ap.add_argument("--since")
    ap.add_argument("--session", type=int); ap.add_argument("--transcript"); ap.add_argument("--until")
    ap.add_argument("--subagents-dir"); ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--repo", default=REPO)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.out:
        ap.error("--out is required (the one file this reader writes)")
    try:
        f = measure(a.repo, a.at, a.rulings_base, a.since, a.session, a.transcript, a.until, a.subagents_dir, tuple(a.exclude))
    except FactsError as e:
        print("⛔ REFUSED:", e); return 1
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(f, fh, ensure_ascii=False, indent=1)
    for l in lines(f):
        print(l)
    print("→", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
