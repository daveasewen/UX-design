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

★ PHASE 3 (#312 lane E-build, 2026-10-01, by addition; `s306-D4`, design `notes/_lanes/312/E/DESIGN.md` § 3):
the keys the generated views (`_wrap_views.py`) read, each a small reader, none typed:
  dates    from the transcript: `opened_at` (the first record), `wrap_at` (the `--until` record, else the
           last usage record), both with a `_local` form (`Wed 2026-09-30 14:02 BST`, zone `--tz`,
           default Europe/London); `ritual_date` from the clock at the seat, never the session's belief;
           `split` = null when the ritual is the opening day, else {opened_day, ritual_day, resumed_at
           (the first user record after a gap of more than 4 h, or null for a run that never paused),
           ordinal = 1 + the `WRAP DATE SPLIT` lines in GOOD-MORNING.md + _GM-ARCHIVE.md}.
  git      + `commits[]` = {sha8, at, subject} over `since.range` (git log) · `pushed_through` (origin/master, sha8)
  handoff  `prev_no`, `prev_name` (the newest `_HANDOFF-*.md` by number), `no` = prev_no + 1
  ci       `owed` parsed from `--ci-owed FILE` (a saved `_ci_readback.py` summary: run id, verdict, sha8);
           `reds[]` from `--ci-red SHA8:STEP:FIXED_BY` (the story seat names them; each sha is checked
           against `git.commits` and refused when absent)
  chain    cl100k of `_CHAIN.md` by `_capture_gate.measure_tokens()` (IMPORTED, its method label travels),
           with `warn`/`block` from `CHAIN_BUDGET_TK`
  gate     `open` = the last `capture gate [wrap]: … in scope · … fail · … warn` line of `--gate-log`
  post     `--post --facts F.json …` ADDS the post-commit block to an existing file: wrap_sha, seat_sha,
           gate_wrap (from `--gate-log`), push_range, pushed_at, minutes_to_push (from `--launched-at`),
           ci {run_id, verdict, jobs} (from `--ci-runs FILE`), prepush {pass, fail, advisory,
           could_not_ask, tests} (summed from `--prepush-dir`'s `_prepush-survey-*.txt` SURVEY lines and
           `_prepush-test-gates.txt`), chain_tk_after_regen (`_CHAIN.md` at `--wrap-sha`), titles
           {brief from `--title-brief`, derived from `knowledge/_gen_titles_receipt.json`}. The pre-commit
           keys are checked byte-identical before the file is saved: `post` is the only second write.

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
      [--ci-owed FILE] [--ci-red SHA8:STEP:FIXED_BY ...] [--gate-log PATH] [--tz ZONE]
  python3 knowledge/_wrap_facts.py --post --facts F.json --wrap-sha S --seat-sha S --gate-log P --push-range A..B
      --pushed-at ISO --launched-at ISO --ci-runs FILE [--prepush-dir D] [--title-brief T]
  python3 knowledge/_wrap_facts.py --extend --facts OLD.json --out NEW.json [--at SHA] [--transcript T] [--ritual-at ISO] …
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


# ------------------------------------------------------------------------------ phase-3 readers
SPLIT_GAP_S = 4 * 3600          # a resumed session: the first user record after a gap of more than 4 h
SPLIT_FILES = ["GOOD-MORNING.md", "_GM-ARCHIVE.md"]
HANDOFF_RE = re.compile(r"^_HANDOFF-(\d+)-(.+)\.md$")
SPLIT_LINE_RE = re.compile(r"^> ⚠ \*\*WRAP DATE SPLIT", re.M)   # the LINE form; prose mentions do not count
GATE_LINE_RE = re.compile(r"capture gate \[[^\]]*\]:\s*(\d+) in scope · (\d+) fail · (\d+) warn")
SURVEY_RE = re.compile(r"SURVEY:\s*(\d+) pass · (\d+) FAIL · (\d+) ADVISORY-warn · (\d+) COULD-NOT-ASK")
TESTS_RE = re.compile(r"(\d+) test\(s\), (\d+) failure\(s\)")
CI_RUN_RE = re.compile(r"^RUN (\d+) \S+ \S+ \S+ sha ([0-9a-f]{7,40})")
CI_JOB_RE = re.compile(r"^\s+job (\S+) (\S+)")
CI_VERDICT_RE = re.compile(r"^VERDICT ([0-9a-f]{7,40}): (GREEN|RED)")


def _tenths(x):
    """Half-up to one decimal (21.65 → 21.7, the form the handoffs print), never float round's 21.6."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def _iso(ts):
    return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _local(ts, tz):
    """`Wed 2026-09-30 14:02 BST` — the form the handoffs and banners use."""
    from zoneinfo import ZoneInfo
    t = _iso(ts).astimezone(ZoneInfo(tz))
    return t.strftime("%a %Y-%m-%d %H:%M ") + t.tzname()


def _records(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("isSidechain") or not rec.get("timestamp"):
                continue
            yield rec


def dates_facts(path, until=None, repo=REPO, tz="Europe/London", at=None, now=None):
    from zoneinfo import ZoneInfo
    zone = ZoneInfo(tz)
    first, last_usage, users = None, None, []
    for rec in _records(path):
        ts = rec["timestamp"]
        if until and ts > until:
            continue
        first = first or ts
        if rec.get("type") == "user":
            users.append(ts)
        if isinstance((rec.get("message") or {}).get("usage"), dict):
            last_usage = ts
    if not first:
        raise FactsError(f"no timestamped record in {path} — an ABSENCE, not a date")
    wrap_at = until or last_usage or first
    ritual = now or datetime.datetime.now(zone)
    ritual = ritual.astimezone(zone)
    opened_day = _iso(first).astimezone(zone).date()
    out = {"tz": tz, "opened_at": first, "opened_local": _local(first, tz), "wrap_at": wrap_at,
           "wrap_local": _local(wrap_at, tz), "ritual_date": ritual.date().isoformat(),
           "ritual_local": ritual.strftime("%a %Y-%m-%d %H:%M ") + ritual.tzname(),
           "unit": "ISO 8601 UTC, and the local form in `tz`; the ritual date is the clock at the seat"}
    if opened_day == ritual.date():
        out["split"] = None
        return out
    resumed = None
    for a, b in zip(users, users[1:]):
        if (_iso(b) - _iso(a)).total_seconds() > SPLIT_GAP_S:
            resumed = b
            break
    n = 0
    for rel in SPLIT_FILES:
        try:
            n += len(SPLIT_LINE_RE.findall(read(repo, rel, at)))
        except (FactsError, FileNotFoundError):
            pass
    out["split"] = {"opened_day": opened_day.isoformat(), "ritual_day": ritual.date().isoformat(),
                    "resumed_at": resumed, "resumed_local": _local(resumed, tz) if resumed else None,
                    "ordinal": n + 1, "rule": f"resumed = first user record after a gap > {SPLIT_GAP_S // 3600} h; "
                    f"ordinal = 1 + `> ⚠ **WRAP DATE SPLIT` lines in {' + '.join(SPLIT_FILES)}"}
    return out


def commits_facts(repo, rng, at=None):
    rc, out = _git(repo, "log", "--reverse", "--no-merges", "--format=%h%x1f%aI%x1f%s", "--abbrev=8", rng)
    if rc:
        raise FactsError(f"git log {rng} failed — the range must be reachable (a shallow clone is refused, never guessed)")
    rows = []
    for ln in out.split("\n"):
        if not ln.strip():
            continue
        sha, ts, subj = ln.split("\x1f", 2)
        rows.append({"sha8": sha[:8], "at": ts, "subject": subj})
    return rows


def handoff_facts(repo, at=None):
    if at:
        rc, out = _git(repo, "ls-tree", "--name-only", at)
        names = out.split("\n") if rc == 0 else []
    else:
        names = os.listdir(repo)
    hs = sorted((int(m.group(1)), n) for n in names for m in [HANDOFF_RE.match(n)] if m)
    if not hs:
        raise FactsError("no `_HANDOFF-*.md` at the root — the handoff number cannot be derived")
    no, name = hs[-1]
    return {"prev_no": no, "prev_name": name, "no": no + 1, "unit": "the newest handoff by number, +1"}


def ci_summary(path):
    """{run_id, sha8, verdict, jobs{name: status}} from a saved `_ci_readback.py` summary."""
    out = {"file": path, "run_id": None, "sha8": None, "verdict": None, "jobs": {}}
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            m = CI_RUN_RE.match(ln)
            if m and not out["run_id"]:
                out["run_id"], out["sha8"] = m.group(1), m.group(2)[:8]
            m = CI_JOB_RE.match(ln)
            if m:
                out["jobs"][m.group(1)] = m.group(2)
            m = CI_VERDICT_RE.match(ln)
            if m:
                out["sha8"], out["verdict"] = m.group(1)[:8], m.group(2)
    if not out["verdict"]:
        raise FactsError(f"{path}: no `VERDICT <sha>: GREEN|RED` line — not a `_ci_readback.py` summary")
    return out


def ci_facts(owed_file=None, reds=(), commits=None, owed_typed=None):
    owed = ci_summary(owed_file) if owed_file else None
    if owed is None and owed_typed:
        parts = owed_typed.split(":")
        if len(parts) < 2 or parts[1] not in ("GREEN", "RED"):
            raise FactsError(f"--ci-owed-typed wants SHA8:GREEN|RED[:RUN_ID], got {owed_typed!r}")
        owed = {"sha8": parts[0][:8], "verdict": parts[1], "run_id": parts[2] if len(parts) > 2 else None,
                "jobs": {}, "source": "typed by the seat (no saved summary)"}
    out = {"owed": owed, "reds": [],
           "unit": "the opener's owed read (parsed from its saved summary, or typed and marked so); reds typed by the seat, shas checked"}
    known = {c["sha8"] for c in (commits or [])}
    for r in reds:
        parts = r.split(":", 2)
        if len(parts) != 3:
            raise FactsError(f"--ci-red wants SHA8:STEP:FIXED_BY, got {r!r}")
        sha, step, fixed = parts
        for x in (sha, fixed):
            if commits is not None and x[:8] not in known:
                raise FactsError(f"--ci-red names `{x}`, which is not in git.commits {len(known)} — refused")
        out["reds"].append({"sha8": sha[:8], "step": step, "fixed_by": fixed[:8]})
    return out


def chain_facts(repo, at=None):
    import _capture_gate as cg
    n, method = cg.measure_tokens(read(repo, "_CHAIN.md", at))
    warn, block = cg.CHAIN_BUDGET_TK
    return {"tk": n, "method": method, "warn": warn, "block": block, "unit": "cl100k by `_capture_gate.measure_tokens`"}


def gate_facts(gate_log):
    last = None
    with open(gate_log, encoding="utf-8") as fh:
        for ln in fh:
            m = GATE_LINE_RE.search(ln)
            if m:
                last = m
    if not last:
        raise FactsError(f"{gate_log}: no `capture gate [..]: N in scope · N fail · N warn` line")
    return {"open": f"{last.group(1)} in scope · {last.group(2)} fail · {last.group(3)} warn",
            "in_scope": int(last.group(1)), "fail": int(last.group(2)), "warn": int(last.group(3)), "log": gate_log}


def prepush_facts(d):
    tot = {"pass": 0, "fail": 0, "advisory": 0, "could_not_ask": 0, "tests": None, "test_failures": None, "surveys": 0}
    for p in sorted(glob.glob(os.path.join(d, "_prepush-survey-*.txt"))):
        for ln in open(p, encoding="utf-8"):
            m = SURVEY_RE.search(ln)
            if m:
                tot["surveys"] += 1
                for k, g in zip(("pass", "fail", "advisory", "could_not_ask"), m.groups()):
                    tot[k] += int(g)
    tg = os.path.join(d, "_prepush-test-gates.txt")
    if os.path.exists(tg):
        for ln in open(tg, encoding="utf-8"):
            m = TESTS_RE.search(ln)
            if m:
                tot["tests"], tot["test_failures"] = int(m.group(1)), int(m.group(2))
    if not tot["surveys"]:
        raise FactsError(f"no SURVEY line under {d}/_prepush-survey-*.txt — the pre-push check is not on record")
    return tot | {"dir": d, "unit": "summed SURVEY lines (pass · FAIL · ADVISORY · COULD-NOT-ASK) and the test count"}


def post_facts(repo, facts, wrap_sha, seat_sha, gate_log, push_range, pushed_at, launched_at, ci_runs,
               prepush_dir=None, title_brief=None, gate_wrap=None):
    if "post" in facts:
        raise FactsError("`post` is already in the file — it is written once, by addition")
    post = {"wrap_sha": wrap_sha[:8], "seat_sha": (seat_sha or "")[:8] or None, "push_range": push_range,
            "pushed_at": pushed_at, "launched_at": launched_at,
            "minutes_to_push": _tenths((_iso(pushed_at) - _iso(launched_at)).total_seconds() / 60)
            if pushed_at and launched_at else None}
    post["gate_wrap"] = gate_facts(gate_log)["open"] if gate_log else gate_wrap
    if gate_wrap and not GATE_LINE_RE.search("capture gate [wrap]: " + gate_wrap):
        raise FactsError(f"--gate-wrap wants `N in scope · N fail · N warn`, got {gate_wrap!r}")
    post["gate_wrap_source"] = "parsed from --gate-log" if gate_log else ("typed by the seat from the committer's log" if gate_wrap else None)
    ci = ci_summary(ci_runs)
    post["ci"] = {"run_id": ci["run_id"], "verdict": ci["verdict"], "jobs": ci["jobs"], "sha8": ci["sha8"]}
    if prepush_dir:
        post["prepush"] = prepush_facts(prepush_dir)
    post["chain_tk_after_regen"] = chain_facts(repo, wrap_sha)["tk"]
    post["chain_tk_after_5b"] = None      # not re-taken at this write (the #241 rule); declared
    derived = None
    try:
        t = json.loads(read(repo, "knowledge/_gen_titles_receipt.json", wrap_sha)).get("next_title", "")
        m = re.search(r"`([^`]+)`", t)
        derived = m.group(1) if m else t
    except (FactsError, FileNotFoundError, json.JSONDecodeError):
        derived = None      # the receipt at the wrap sha, or nothing: never the working tree's
    post["titles"] = {"brief": title_brief, "derived": derived}
    post["unit"] = "post-commit facts, by addition; `chain_tk_after_5b` null = not re-taken"
    return post


def add_post(path, **kw):
    """Add `post` to an existing FACTS.json; the pre-commit keys must survive byte-identical."""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    facts = json.loads(raw)
    before = json.dumps(facts, ensure_ascii=False, indent=1)
    facts["post"] = post_facts(facts=facts, **kw)
    again = dict(facts); again.pop("post")
    if json.dumps(again, ensure_ascii=False, indent=1) != before:
        raise FactsError("the pre-commit keys changed under the post write — refused")
    return facts


def measure(repo=REPO, at=None, rulings_base=None, since=None, session=None, transcript=None, until=None,
            subagents_dir=None, exclude=(), ci_owed=None, ci_reds=(), gate_log=None, tz="Europe/London", ci_owed_typed=None):
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
    return extend_facts(f, repo, at, transcript, until, ci_owed, ci_reds, gate_log, tz, None, ci_owed_typed)


def extend_facts(f, repo=REPO, at=None, transcript=None, until=None, ci_owed=None, ci_reds=(), gate_log=None,
                 tz="Europe/London", now=None, ci_owed_typed=None):
    """★ phase 3, by addition: the keys the views read. Also the `--extend` path for a FACTS.json measured
    before these readers existed (the #309–#311 fixtures): the old keys are kept byte-identical."""
    if f["git"].get("since"):
        f["git"]["commits"] = commits_facts(repo, f["git"]["since"]["range"], at)
    if f["git"].get("origin_master"):
        f["git"]["pushed_through"] = f["git"]["origin_master"][:8]
    if transcript:
        f["dates"] = dates_facts(transcript, until or f.get("fill", {}).get("until"), repo, tz, at, now)
    f["handoff"] = handoff_facts(repo, at)
    if ci_owed or ci_reds or ci_owed_typed:
        f["ci"] = ci_facts(ci_owed, ci_reds, f["git"].get("commits"), ci_owed_typed)
    f["chain"] = chain_facts(repo, at)
    if gate_log:
        f["gate"] = gate_facts(gate_log)
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
    if "dates" in f:
        d = f["dates"]
        out.append(f"dates: opened {d['opened_local']} · wrap {d['wrap_local']} · ritual {d['ritual_date']} · "
                   + ("no date split" if not d["split"] else f"DATE SPLIT (ordinal {d['split']['ordinal']}, resumed {d['split']['resumed_local']})"))
    if "handoff" in f:
        out.append(f"handoff: prev {f['handoff']['prev_no']} → {f['handoff']['no']}")
    if "chain" in f:
        out.append(f"chain: {f['chain']['tk']:,} ({f['chain']['method']}) · warn {f['chain']['warn']:,} · block {f['chain']['block']:,}")
    if "gate" in f:
        out.append("gate at open: " + f["gate"]["open"])
    if "ci" in f and f["ci"].get("owed"):
        out.append(f"ci owed: {f['ci']['owed']['sha8']} run {f['ci']['owed']['run_id']} {f['ci']['owed']['verdict']}")
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
        # ★ phase 3 readers
        tr = os.path.join(td, "tr.jsonl")
        recs = [{"timestamp": "2026-09-29T19:47:31Z", "type": "queue-operation"},
                {"timestamp": "2026-09-29T19:47:40Z", "type": "user", "message": {"usage": u(1, 2, 3)}},
                {"timestamp": "2026-09-29T21:02:00Z", "type": "user"},
                {"timestamp": "2026-09-30T06:07:11Z", "type": "user", "message": {"usage": u(1, 2, 3)}},
                {"timestamp": "2026-09-30T11:08:00Z", "type": "user", "message": {"usage": u(1, 2, 3)}}]
        open(tr, "w").write("\n".join(json.dumps(r) for r in recs) + "\n")
        open(os.path.join(td, "GOOD-MORNING.md"), "w").write("> ⚠ **WRAP DATE SPLIT** a\n> ⚠ **WRAP DATE SPLIT** b\nprose: a WRAP DATE SPLIT mention\n")
        now = datetime.datetime(2026, 9, 30, 12, 0, tzinfo=datetime.timezone.utc)
        d = dates_facts(tr, "2026-09-30T11:08:00Z", repo=td, now=now)
        bite("dates: opened Tue 20:47 BST, wrap Wed 12:08 BST, ritual 09-30",
             d["opened_local"] == "Tue 2026-09-29 20:47 BST" and d["wrap_local"] == "Wed 2026-09-30 12:08 BST"
             and d["ritual_date"] == "2026-09-30")
        bite("dates: a DATE SPLIT with the resumed record after the > 4 h gap and ordinal 3 (two LINES + 1; the prose mention not counted)",
             d["split"] and d["split"]["resumed_at"] == "2026-09-30T06:07:11Z" and d["split"]["ordinal"] == 3)
        d2 = dates_facts(tr, "2026-09-29T21:02:00Z", repo=td, now=datetime.datetime(2026, 9, 29, 22, 0, tzinfo=datetime.timezone.utc))
        bite("dates: same-day ritual → split null", d2["split"] is None and d2["wrap_at"] == "2026-09-29T21:02:00Z")
        for n in ("_HANDOFF-160-a.md", "_HANDOFF-9-z.md"):
            open(os.path.join(td, n), "w").write("x")
        h = handoff_facts(td)
        bite("handoff: newest by NUMBER (160, not 9) → no 161", h["prev_no"] == 160 and h["no"] == 161 and h["prev_name"] == "_HANDOFF-160-a.md")
        ci = os.path.join(td, "ci.txt")
        open(ci, "w").write("RUN 36748452503 gates completed/success 2026-09-30T17:01:33Z sha 4ece47a5\n   job gates completed/success x\n"
                            "   job render completed/success y\n   job release completed/success z\nVERDICT 4ece47a5: GREEN — every run completed and passed\n")
        c = ci_summary(ci)
        bite("ci: run id, sha8, GREEN and three jobs parsed", c["run_id"] == "36748452503" and c["sha8"] == "4ece47a5"
             and c["verdict"] == "GREEN" and len(c["jobs"]) == 3)
        try:
            ci_facts(None, ("93cdb12a:88:7e4602db",), [{"sha8": "93cdb12a"}]); bite("ci: a red's fix sha not in git.commits is refused", False)
        except FactsError:
            bite("ci: a red's fix sha not in git.commits is refused", True)
        r = ci_facts(None, ("93cdb12a:88:7e4602db",), [{"sha8": "93cdb12a"}, {"sha8": "7e4602db"}])
        bite("ci: a red with both shas known is recorded", r["reds"] == [{"sha8": "93cdb12a", "step": "88", "fixed_by": "7e4602db"}])
        gl = os.path.join(td, "g.log")
        open(gl, "w").write("noise\ncapture gate [wrap]: 247 in scope · 0 fail · 33 warn\n")
        bite("gate: the last verdict line parsed", gate_facts(gl)["open"] == "247 in scope · 0 fail · 33 warn")
        pd = os.path.join(td, "pp"); os.makedirs(pd)
        open(os.path.join(pd, "_prepush-survey-1.txt"), "w").write("SURVEY: 11 pass · 0 FAIL · 1 ADVISORY-warn · 2 COULD-NOT-ASK (x)\n")
        open(os.path.join(pd, "_prepush-survey-2.txt"), "w").write("SURVEY: 42 pass · 1 FAIL · 2 ADVISORY-warn · 7 COULD-NOT-ASK (x)\n")
        open(os.path.join(pd, "_prepush-test-gates.txt"), "w").write("32 test(s), 0 failure(s)\n")
        pp = prepush_facts(pd)
        bite("prepush: SURVEY lines summed (53 pass, 1 FAIL, 3 advisory, 9 could-not-ask) and 32 tests",
             (pp["pass"], pp["fail"], pp["advisory"], pp["could_not_ask"], pp["tests"]) == (53, 1, 3, 9, 32))
        fp = os.path.join(td, "F.json")
        base = {"measured_at": "x", "git": {"head": "h"}, "fill": {"now": 5}}
        json.dump(base, open(fp, "w"), ensure_ascii=False, indent=1)
        g("init", "-q", td)
        open(os.path.join(td, "_CHAIN.md"), "w").write("chain text here\n"); g("add", "_CHAIN.md"); g("commit", "-qm", "chain")
        wsha = _git(td, "rev-parse", "HEAD")[1]
        f2 = add_post(fp, repo=td, wrap_sha=wsha, seat_sha=None, gate_log=gl, push_range="a..b", pushed_at="2026-09-30T17:01:30Z",
                      launched_at="2026-09-30T16:39:51Z", ci_runs=ci, prepush_dir=pd, title_brief="T")
        bite("post: added by addition — minutes_to_push 21.7, gate_wrap, CI GREEN, chain tk measured, pre-commit keys kept",
             f2["post"]["minutes_to_push"] == 21.7 and f2["post"]["gate_wrap"].startswith("247") and f2["post"]["ci"]["verdict"] == "GREEN"
             and f2["post"]["chain_tk_after_regen"] > 0 and {k: f2[k] for k in base} == base)
        json.dump(f2, open(fp, "w"))
        try:
            add_post(fp, repo=td, wrap_sha=wsha, seat_sha=None, gate_log=gl, push_range="a..b", pushed_at=None, launched_at=None, ci_runs=ci)
            bite("post: a second post write is refused", False)
        except FactsError:
            bite("post: a second post write is refused", True)
    print("wrap-facts selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out"); ap.add_argument("--at"); ap.add_argument("--rulings-base"); ap.add_argument("--since")
    ap.add_argument("--session", type=int); ap.add_argument("--transcript"); ap.add_argument("--until")
    ap.add_argument("--subagents-dir"); ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--ci-owed"); ap.add_argument("--ci-red", action="append", default=[])
    ap.add_argument("--ci-owed-typed", help="SHA8:GREEN|RED[:RUN_ID] when the opener's read was not saved (marked typed)")
    ap.add_argument("--gate-log"); ap.add_argument("--tz", default="Europe/London")
    ap.add_argument("--post", action="store_true", help="add the post-commit block to --facts (phase 3)")
    ap.add_argument("--facts"); ap.add_argument("--wrap-sha"); ap.add_argument("--seat-sha"); ap.add_argument("--push-range")
    ap.add_argument("--pushed-at"); ap.add_argument("--launched-at"); ap.add_argument("--ci-runs")
    ap.add_argument("--prepush-dir"); ap.add_argument("--title-brief")
    ap.add_argument("--gate-wrap", help="--post: the wrap commit's gate verdict `N in scope · N fail · N warn`, typed from the committer's log when no --gate-log was saved")
    ap.add_argument("--extend", action="store_true", help="add the phase-3 keys to --facts (an older FACTS.json), written to --out")
    ap.add_argument("--ritual-at", help="--extend only: the ritual's clock (ISO), for a fixture measured after the day")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.post:
        if not (a.facts and a.wrap_sha and a.ci_runs):
            ap.error("--post needs --facts, --wrap-sha and --ci-runs")
        try:
            f = add_post(a.facts, repo=a.repo, wrap_sha=a.wrap_sha, seat_sha=a.seat_sha, gate_log=a.gate_log,
                         push_range=a.push_range, pushed_at=a.pushed_at, launched_at=a.launched_at,
                         ci_runs=a.ci_runs, prepush_dir=a.prepush_dir, title_brief=a.title_brief, gate_wrap=a.gate_wrap)
        except FactsError as e:
            print("⛔ REFUSED:", e); return 1
        with open(a.facts, "w", encoding="utf-8") as fh:
            json.dump(f, fh, ensure_ascii=False, indent=1)
        p = f["post"]
        print(f"post: wrap {p['wrap_sha']} · seat {p['seat_sha']} · CI {p['ci']['verdict']} run {p['ci']['run_id']} · "
              f"chain {p['chain_tk_after_regen']:,} cl100k · pushed {p['push_range']} at {p['pushed_at']}")
        print("→", a.facts, "(post added by addition)")
        return 0
    if not a.out:
        ap.error("--out is required (the one file this reader writes)")
    if a.extend:
        if not a.facts:
            ap.error("--extend needs --facts")
        try:
            now = _iso(a.ritual_at) if a.ritual_at else None
            f = extend_facts(json.load(open(a.facts, encoding="utf-8")), a.repo, a.at, a.transcript, a.until,
                             a.ci_owed, tuple(a.ci_red), a.gate_log, a.tz, now, a.ci_owed_typed)
        except FactsError as e:
            print("⛔ REFUSED:", e); return 1
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(f, fh, ensure_ascii=False, indent=1)
        for l in lines(f):
            print(l)
        print("→", a.out, "(extended by addition)")
        return 0
    try:
        f = measure(a.repo, a.at, a.rulings_base, a.since, a.session, a.transcript, a.until, a.subagents_dir,
                    tuple(a.exclude), a.ci_owed, tuple(a.ci_red), a.gate_log, a.tz, a.ci_owed_typed)
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
