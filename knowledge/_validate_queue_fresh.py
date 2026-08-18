#!/usr/bin/env python3
"""_validate_queue_fresh.py — the STALE-QUEUE check (#196).

WHAT THIS IS. GOOD-MORNING.md §C·1 is prose that makes WORK-STATE CLAIMS: this
strand is open, that step landed. Prose cannot be re-measured, so it outlives
reality — §C·1(a) STEP 2 read as an open divvy plan for TWELVE sessions after the
wave actually LANDED (`df44e51`, #95), the second recurrence on that exact line
(#26 was the first). Sister defects: the 7-vs-14 meta count (#195) and the
standing-44-measured-4 (#194). This script turns each queue item's state into a
PROBEABLE claim and re-measures it every build.

MIRROR OF THE DOC-ROW GATE. That one catches documents with no store row. This
one catches rows that have outlived their documents.

THE GRAMMAR. Every live §C·1 item carries ONE machine tail, an HTML comment so
GM's rendered prose is untouched:

  <!-- qprobe: state=open expects-absent=knowledge/snippets/Chart-foo.reference.html,... -->
  <!-- qprobe: state=landed receipt=df44e51 -->
  <!-- qprobe: state=partial declared="lane B open; lanes A landed" expects-absent=... -->

THE CLAUSES, each refusing loud and named:
  * state=open       — every path in `expects-absent` must be ABSENT. An "open"
                       item whose deliverables are already on disk IS the defect;
                       the refusal quotes the path AND the queue line
                       [[gate-must-quote-what-it-forbids]]. An EMPTY list is legal
                       only with `declared=` saying why — a DECLARED gap passes,
                       a silent one fails.
  * state=landed     — `receipt=<sha>` must be a well-formed hex sha that RESOLVES
                       to a commit. A landed claim with no receipt, or a receipt
                       git cannot find, is a claim with nothing behind it.
  * state=partial    — the legal form for an honest in-between state
                       [[honest-refusal-needs-a-legal-form]]: `declared="…"` is
                       required, `expects-absent` optional and checked if given.
                       A declared partial is NEVER refused for its partialness.
  * PRESENCE         — an item with NO tail FAILS. Gate the presence, not the
                       drift: an unannotated item is invisible to this gate
                       forever, the exact [[instrument-without-a-consumer]] trap.
  * UNPARSEABLE      — a malformed tail is a NAMED refusal with rc=2, never a
                       silent skip [[a-crash-is-not-a-fail]].

WHAT AN ITEM IS (the scope, deliberately narrow — pitfall (a) of the #196 brief:
an over-eager presence rule would nag every prose line in §C·1). Exactly two
shapes, inside §C·1 only:
  (1) a strand heading — a line starting `**(a)` … `**(e)`
  (2) a `**STEP N` clause anywhere inside a strand
Struck-through spans (`~~ … ~~`) are BLANKED before detection: struck text is a
period record, not a live item (§C·1(a) carries a struck STEP 2 divvy plan).
Every other line of §C·1 — the ROUTING line, lane prose, continuations — is NOT
an item and must not trigger. The selftest pins that.

WHAT THIS CANNOT SEE, DECLARED. It proves a stated state is CONSISTENT with the
disk and with git. It does not prove the state is the RIGHT one, and it cannot
read the item's meaning: what is open, what it means, and when it closes are
Dave's and the conductor's. A green reads "no queue item's claim is contradicted
by measurement", never "the queue is correct".

Usage:  python3 knowledge/_validate_queue_fresh.py             # check mode
        python3 knowledge/_validate_queue_fresh.py --selftest  # 13 bites (docstring said 6 until #199 — the count grew, the prose did not)
Exit 0 clean · 1 findings · 2 unparseable (a refusal, not a verdict).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GM = os.path.join(REPO, "GOOD-MORNING.md")

# SEVERITY — this gate is routed GATE (BLOCKING) in _build_all.py. The promotion
# condition of s197-D1 was "stay WARN until it survives one real banner roll, then
# flip at the following session": MET by the #197 roll (commit 5b77cce, recorded
# GOOD-MORNING.md:522), and Dave gave the word at #198. BLOCKING is the repo's GATE
# tier — red + remedy, caught at the commit seam; the build itself keeps running,
# it is NOT ABORT. This constant is display-only (printed at main()); the routing
# truth is the ROUTE_ROWS entry in _build_all.py, and the two must move together.
SEVERITY = "blocking"

SECTION_START_RE = re.compile(r"^##\s*1\.\s*★\s*NEXT STRANDS")
NEXT_HEADING_RE = re.compile(r"^##\s")
STRAND_RE = re.compile(r"^\*\*\(([a-e])\)")
STEP_RE = re.compile(r"\*\*STEP\s+(\d+)")
STRIKE_RE = re.compile(r"~~.*?~~")
QPROBE_RE = re.compile(r"<!--\s*qprobe:(.*?)-->", re.S)
FIELD_RE = re.compile(r'([A-Za-z][A-Za-z-]*)=("[^"]*"|\S*)')
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
LEGAL_STATES = ("open", "landed", "partial")
LEGAL_KEYS = ("state", "expects-absent", "receipt", "declared")


class Unparseable(Exception):
    """A refusal, not a verdict — rc=2. Named, never swallowed."""


def _blank_strikes(line):
    """Blank struck spans to spaces so column offsets are PRESERVED (a length-
    changing strip would silently reorder items and tails)."""
    return STRIKE_RE.sub(lambda m: " " * len(m.group(0)), line)


def section(text):
    """Return (lines, first_line_no) for §C·1, or raise. An absent section is a
    refusal: an absent instrument must not read as a pass."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if SECTION_START_RE.match(ln):
            start = i
            break
    if start is None:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md — no `## 1. ★ NEXT STRANDS` "
                          "heading; §C·1 has moved or been renamed")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if NEXT_HEADING_RE.match(lines[j]):
            end = j
            break
    return lines[start + 1:end], start + 2   # 1-based line number of the first body line


def items(lines, first_line_no):
    """The two item shapes, in document order. Returns dicts with a (row, col)
    key so a tail can be attributed positionally and unambiguously."""
    found, strand = [], None
    for idx, raw in enumerate(lines):
        live = _blank_strikes(raw)
        m = STRAND_RE.match(live)
        if m:
            strand = m.group(1)
            found.append({"id": "(%s)" % strand, "key": (idx, m.start()),
                          "line_no": first_line_no + idx, "line": raw.strip()})
        for sm in STEP_RE.finditer(live):
            found.append({"id": "(%s) STEP %s" % (strand or "?", sm.group(1)),
                          "key": (idx, sm.start()),
                          "line_no": first_line_no + idx, "line": raw.strip()})
    found.sort(key=lambda d: d["key"])
    return found


def tails(lines, first_line_no):
    out = []
    for idx, raw in enumerate(lines):
        for m in QPROBE_RE.finditer(raw):
            out.append({"key": (idx, m.start()), "line_no": first_line_no + idx,
                        "body": m.group(1).strip(), "raw": m.group(0)})
    out.sort(key=lambda d: d["key"])
    return out


def parse_tail(t):
    """Strict field parse. Anything unrecognised is UNPARSEABLE, never a skip."""
    body = t["body"]
    fields, consumed = {}, 0
    for m in FIELD_RE.finditer(body):
        k, v = m.group(1), m.group(2)
        if k not in LEGAL_KEYS:
            raise Unparseable("UNPARSEABLE — GOOD-MORNING.md:%d — qprobe carries unknown key "
                              "%r; legal keys: %s | %s"
                              % (t["line_no"], k, ", ".join(LEGAL_KEYS), t["raw"][:120]))
        if k in fields:
            raise Unparseable("UNPARSEABLE — GOOD-MORNING.md:%d — qprobe repeats key %r"
                              % (t["line_no"], k))
        fields[k] = v[1:-1] if v.startswith('"') else v
        consumed += len(m.group(0))
    if not fields:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md:%d — qprobe carries no `key=value` "
                          "fields at all | %s" % (t["line_no"], t["raw"][:120]))
    residue = FIELD_RE.sub("", body).strip()
    if residue:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md:%d — qprobe carries text that is not a "
                          "`key=value` field: %r" % (t["line_no"], residue[:80]))
    state = fields.get("state")
    if state is None:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md:%d — qprobe has no `state=`; every tail "
                          "states one of %s" % (t["line_no"], "/".join(LEGAL_STATES)))
    if state not in LEGAL_STATES:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md:%d — qprobe state=%r is not one of %s"
                          % (t["line_no"], state, "/".join(LEGAL_STATES)))
    return fields


def _paths(fields):
    v = fields.get("expects-absent")
    if v is None:
        return None
    return [p.strip() for p in v.split(",") if p.strip()]


def _git_sha_exists(sha, repo=REPO):
    try:
        r = subprocess.run(["git", "-C", repo, "cat-file", "-e", "%s^{commit}" % sha],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return r.returncode == 0
    except OSError:
        return False


def check(gm_path=GM, repo=REPO, sha_exists=None):
    """Returns (fails, n_items). Raises Unparseable (rc=2) on a malformed surface."""
    sha_exists = _git_sha_exists if sha_exists is None else sha_exists
    if not os.path.exists(gm_path):
        raise Unparseable("UNPARSEABLE — %s — file not found (an absent instrument is not a "
                          "pass)" % gm_path)
    lines, first = section(open(gm_path, encoding="utf-8").read())
    its, tls = items(lines, first), tails(lines, first)
    if not its:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md — §C·1 matched ZERO queue items; the "
                          "strand grammar has drifted and this gate is now blind")
    fails = []
    # attribute each tail to the item it follows (positional, offsets preserved)
    bounds = [it["key"] for it in its] + [(10 ** 9, 0)]
    for n, it in enumerate(its):
        mine = [t for t in tls if bounds[n] < t["key"] < bounds[n + 1]]
        if not mine:
            fails.append("FAIL — §C·1 item %s at GOOD-MORNING.md:%d carries NO qprobe tail. An "
                         "unannotated item is invisible to this gate forever. Line: %s"
                         % (it["id"], it["line_no"], it["line"][:140]))
            continue
        if len(mine) > 1:
            raise Unparseable("UNPARSEABLE — GOOD-MORNING.md:%d — item %s carries %d qprobe "
                              "tails; exactly one per item"
                              % (it["line_no"], it["id"], len(mine)))
        f = parse_tail(mine[0])
        state, paths = f["state"], _paths(f)
        if state == "open":
            if paths is None:
                fails.append("FAIL — §C·1 item %s (GOOD-MORNING.md:%d) is state=open with no "
                             "`expects-absent=` field. An open claim with nothing probeable is "
                             "the silent gap; declare an empty list plus declared=\"…\" instead."
                             % (it["id"], it["line_no"]))
            elif not paths and not f.get("declared"):
                fails.append("FAIL — §C·1 item %s (GOOD-MORNING.md:%d) is state=open with an "
                             "EMPTY expects-absent and no declared=\"…\". A DECLARED gap passes, "
                             "a silent one fails." % (it["id"], it["line_no"]))
        elif state == "landed":
            sha = f.get("receipt")
            if not sha:
                fails.append("FAIL — §C·1 item %s (GOOD-MORNING.md:%d) claims state=landed with "
                             "NO receipt=<sha>. A landed claim carries its receipt."
                             % (it["id"], it["line_no"]))
            elif not SHA_RE.match(sha):
                fails.append("FAIL — §C·1 item %s (GOOD-MORNING.md:%d) receipt=%r is not a "
                             "7–40 char lowercase hex sha." % (it["id"], it["line_no"], sha))
            elif not sha_exists(sha):
                fails.append("FAIL — §C·1 item %s (GOOD-MORNING.md:%d) claims state=landed "
                             "receipt=%s, but git cannot resolve that sha to a commit. Line: %s"
                             % (it["id"], it["line_no"], sha, it["line"][:120]))
        elif state == "partial":
            if not f.get("declared"):
                fails.append("FAIL — §C·1 item %s (GOOD-MORNING.md:%d) is state=partial with no "
                             "declared=\"…\". partial is the LEGAL FORM for an honest in-between "
                             "state — it must say what is done and what is not."
                             % (it["id"], it["line_no"]))
        for p in (paths or []):
            if os.path.exists(os.path.join(repo, p)):
                fails.append("FAIL — §C·1 item %s (GOOD-MORNING.md:%d) states state=%s and "
                             "expects %s to be ABSENT — IT EXISTS ON DISK. An 'open' item whose "
                             "deliverable is already built is the stale-queue defect (#196; the "
                             "12-session miss on this very strand). Queue line: %s"
                             % (it["id"], it["line_no"], state, p, it["line"][:140]))
    return fails, len(its)


def main():
    try:
        fails, n = check()
    except Unparseable as e:
        print("%s" % e)
        print("RESULT: REFUSED (rc=2) — the surface could not be read honestly; this is a "
              "refusal, not a verdict.")
        return 2
    print("queue freshness — §C·1 items measured: %d (severity: %s)" % (n, SEVERITY))
    if fails:
        print("\n".join(fails))
        print("RESULT: FAIL (%d)" % len(fails))
        return 1
    print("RESULT: PASS — no §C·1 item's stated state is contradicted by disk or git. This "
          "proves no claim is STALE; it does not prove the queue is RIGHT.")
    return 0


def selftest():
    """13 bites (was 6; corrected #199). Each must land its verdict for the NAMED reason, or the gate is
    decorative [[mutation-tests-the-clause-not-the-feature]]."""
    import shutil
    import tempfile
    ok = True
    KNOWN = {"df44e51", "00abdf3"}

    def fake_sha(s):
        return s in KNOWN

    def bite(name, expect, body, plant=()):
        """expect: 'green' | 'fail' | 'refuse'."""
        nonlocal ok
        tmp = tempfile.mkdtemp()
        try:
            for rel in plant:
                p = os.path.join(tmp, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "w").write("x")
            gm = os.path.join(tmp, "GOOD-MORNING.md")
            open(gm, "w", encoding="utf-8").write(
                "# §C · QUEUE\n\n## 1. ★ NEXT STRANDS (pick one)\n" + body +
                "\n## 2. ★ DAVE: THE RULING BATCH\nnot in scope\n")
            try:
                fails, n = check(gm, tmp, sha_exists=fake_sha)
                got = "fail" if fails else "green"
                detail = fails[0] if fails else "(%d items, green)" % n
            except Unparseable as e:
                got, detail = "refuse", str(e)
            good = got == expect
            ok = ok and good
            print("  %s %-40s -> %-6s | %s" % ("PASS" if good else "BITE-MISSED", name, got,
                                               detail[:120]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    LANDED = "<!-- qprobe: state=landed receipt=df44e51 -->"
    print("selftest — _validate_queue_fresh.py")
    bite("control: landed + open + partial green", "green",
         "**(a) Strand a.** " + LANDED + "\n"
         "**STEP 1 done.** " + LANDED + "\n"
         "**(b) Strand b.** <!-- qprobe: state=open expects-absent=knowledge/snippets/Nope.html -->\n"
         "**(c) Strand c.** <!-- qprobe: state=partial declared=\"lane B open; A landed\" -->\n")
    bite("open item whose artefact EXISTS refuses", "fail",
         "**(a) Strand a.** <!-- qprobe: state=open expects-absent=knowledge/snippets/Chart-pie.reference.html -->\n",
         plant=["knowledge/snippets/Chart-pie.reference.html"])
    bite("landed with unresolvable receipt refuses", "fail",
         "**(a) Strand a.** <!-- qprobe: state=landed receipt=0000000 -->\n")
    bite("item with NO tail refuses (presence rule)", "fail",
         "**(a) Strand a.** " + LANDED + "\n**(b) Strand b, unannotated.**\n")
    bite("partial WITH declared passes, absent paths unchecked", "green",
         "**(a) Strand a.** <!-- qprobe: state=partial declared=\"legacy half enacted; rest owed\" -->\n")
    bite("partial without declared refuses", "fail",
         "**(a) Strand a.** <!-- qprobe: state=partial -->\n")
    bite("empty expects-absent WITHOUT declared refuses", "fail",
         "**(a) Strand a.** <!-- qprobe: state=open expects-absent= -->\n")
    bite("empty expects-absent WITH declared passes", "green",
         "**(a) Strand a.** <!-- qprobe: state=open expects-absent= declared=\"no probeable artefact\" -->\n")
    bite("malformed tail is a REFUSAL, not a skip", "refuse",
         "**(a) Strand a.** <!-- qprobe: state=whatever -->\n")
    bite("unknown key is a REFUSAL", "refuse",
         "**(a) Strand a.** <!-- qprobe: state=open expects-absent= sha=deadbee -->\n")
    # SCOPE bites — pitfall (a): an over-eager presence rule would nag every prose line
    bite("non-item prose lines do NOT trigger", "green",
         "**⛔ ROUTING (records: knowledge/_lanes.json): ACTIVE lane-2.**\n"
         "**(a) Strand a.** " + LANDED + "\n"
         "**lane 1** butterfly-h + histogram, continuation prose.\n"
         "plain prose line naming STEP fours and things.\n")
    bite("STRUCK step clause is not a live item", "green",
         "**(a) Strand a.** " + LANDED + "\n"
         "~~**STEP 2 (wave) — DIVVY PLAN**~~ period record only.\n")
    bite("§2 items are out of scope (section bound)", "green",
         "**(a) Strand a.** " + LANDED + "\n")
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
