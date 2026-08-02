#!/usr/bin/env python3
"""
_LIVE-STATE staleness gate (ADR-0007, lightweight-first slice) — the drift-killer.

WHY: context staleness = an unrecorded supersession edge (ADR-0007). A cold session once burned a
whole sitting reasoning from a retired artifact as if it were live; this session the ledger's own
"Last refreshed" stamp had silently drifted 5 days. The manual ledger retains state well but its
metadata rots quietly. This gate makes the hand-maintained `_LIVE-STATE.md` *trustworthy* by
checking it against reality — without the risky full-generation migration.

SCOPE. Two halves now, both live:
  - GENERATION (ADR-0007 part 2, added 2026-07-21): the decision-node lifecycle block in
    `_LIVE-STATE.md` (between the AUTO-DECISION-LIFECYCLE markers) is regenerated from the parsed
    decision graph (`_decision-graph.json`, produced by `_build_decision_graph.py`). This is the
    "walk the edges to regenerate the LIVE/DEAD blocks" half ADR-0007 §2 deferred until the edge
    convention (ADR-0012) existed and the edges were inscribed (both done 2026-07-21).
  - VALIDATION (the original 2026-07-10 slice): the staleness gate below still checks the
    hand-authored ledger against reality. Generation covers decision NODES; the gate still guards
    the prose (freshness stamp, artifact tombstones, ADR lifecycle) that generation doesn't own.

CHECKS (advisory — earns blocking by bite-test, ADR-0005 §5):
  1. Freshness drift   — `Last refreshed:` stamp vs the newest decision-bearing doc change
                         (git commit date, falling back to mtime). The exact bug we hit.
  2. Dead-node resurrection — a node listed in SUPERSEDED/DEAD that is still cited in the LIVE
                         section, or a tombstoned artifact still referenced (un-tombstoned) elsewhere.
  3. Tombstone consistency — each DEAD file entry actually exists AND carries a tombstone banner.
  4. Lifecycle contradiction — an ADR marked DEFERRED/superseded in its own audit banner but still
                         cited as current truth in the LIVE section.
  5. Orphan supersession edge — a DEAD "superseded-by X" whose X can't be found (ADR/§/file).

Writes `_LIVE-STATE-CHECK.md` + prints a summary. Non-zero exit = warning count (advisory in
_build_all.py; flip to blocking once it's been quiet for a few sessions).

Run:  python3 knowledge/_build_live_state.py
      python3 knowledge/_build_live_state.py --selftest   # bite-test the SPLICE WRITER (#78-D2):
        the spine's only mechanical writer was ungated (#77 periphery inventory). Every arm runs
        on COPIES inside a TemporaryDirectory — the selftest never opens the real _LIVE-STATE.md
        for writing, and asserts the real spine's bytes are untouched when it finishes.
"""
import os, re, sys, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIVE = os.path.join(ROOT, "_LIVE-STATE.md")
DECISIONS = os.path.join(ROOT, "docs", "decisions")
OUT = os.path.join(HERE, "_LIVE-STATE-CHECK.md")
GRAPH_JSON = os.path.join(HERE, "_decision-graph.json")  # produced by _build_decision_graph.py

# ADR-0007 part 2: the generation half. The decision-node lifecycle block in
# _LIVE-STATE.md is regenerated (not hand-kept) from the parsed decision graph, spliced
# between these markers. Deterministic — no volatile date in the body — so a clean build
# produces no spurious diff (same discipline as canon.css's AUTO markers).
BLOCK_START = "<!-- AUTO-DECISION-LIFECYCLE START"
BLOCK_END = "<!-- AUTO-DECISION-LIFECYCLE END -->"

TOMB_RE = re.compile(r"superseded|tombstone|retired|DEAD|do not build|do-not-build", re.I)
ADR_RE = re.compile(r"ADR-(\d{4})")
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
# file-ish tokens inside a bullet (paths + bare filenames)
FILE_RE = re.compile(r"`?([\w./-]+\.(?:md|html|json|py|css))`?")


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""


def split_sections(md):
    """Return {section_title: body} keyed by '## ' headers."""
    secs, cur, buf = {}, "_preamble", []
    for line in md.splitlines():
        m = re.match(r"^##\s+(.*)", line)
        if m:
            secs[cur] = "\n".join(buf)
            cur, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    secs[cur] = "\n".join(buf)
    return secs


def section(secs, *keywords):
    for k, v in secs.items():
        if all(kw.lower() in k.lower() for kw in keywords):
            return v
    return ""


def git_date(path):
    try:
        r = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs", "--", path],
                           capture_output=True, text=True, timeout=8)
        s = r.stdout.strip()
        if s:
            return s
    except Exception:
        pass
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    except Exception:
        return None


def bullets(body):
    out, cur = [], None
    for line in body.splitlines():
        if re.match(r"^\s*[-*]\s+", line):
            if cur is not None:
                out.append(cur)
            cur = line
        elif cur is not None and line.strip() and not line.startswith("#"):
            cur += " " + line.strip()
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return out


def _sort_key(nid):
    """Group by decision-family prefix (R-D, T-D, B-D, DV-D, ADR, …) then natural-ish."""
    head = nid.split("-")[0]
    m = re.search(r"(\d+)", nid)
    return (head, int(m.group(1)) if m else 0, nid)


def render_lifecycle_block(graph):
    """Build the markdown that goes between the AUTO-DECISION-LIFECYCLE markers, from the
    parsed decision graph JSON. Highest-value-for-cold-start ordering: DEAD (do-not-build-on)
    and AMENDED (live-but-a-claim-is-dead) first, then OPEN, then a compact LIVE roster.
    Supersession + dead-claim annotations are recovered from the edge list, matching what
    `_build_decision_graph.py` §② renders — this is the same view, surfaced on the spine so a
    cold session sees it without opening the graph doc."""
    nodes = graph.get("nodes", {})
    edges = graph.get("edges", [])
    state = graph.get("state", {})

    inbound = {}
    for e in edges:
        inbound.setdefault(e.get("to"), []).append(e)

    by_state = {}
    for nid, st in state.items():
        by_state.setdefault(st, []).append(nid)

    counts = {st: len(by_state.get(st, [])) for st in ("LIVE", "AMENDED", "DEAD", "OPEN")}
    L = [BLOCK_START + " — do NOT hand-edit between these markers.",
         "     Generated by `knowledge/_build_live_state.py` from `knowledge/_decision-graph.json`",
         "     (which `_build_decision_graph.py` produces from the audited seed + inscribed edges).",
         "     To change what appears here, change the ledgers/ADRs and re-run `_build_all.py`.",
         "     Consistency only, never validity (ADR-0007 §5): a clean ledger is not a vouched one. -->",
         "",
         f"**{len(nodes)} decision nodes — {counts['LIVE']} LIVE · {counts['AMENDED']} AMENDED · "
         f"{counts['DEAD']} DEAD · {counts['OPEN']} OPEN.** "
         "Full typed edges + what-touches-this map: `knowledge/_DECISION-GRAPH.md`.",
         ""]

    dead = sorted(by_state.get("DEAD", []), key=_sort_key)
    if dead:
        L.append(f"**☠ DEAD — do not build on ({len(dead)}):**")
        for nid in dead:
            sups = [e["from"] for e in inbound.get(nid, []) if e["type"] == "supersedes"]
            tail = f" — superseded by {', '.join(sups)}" if sups else ""
            L.append(f"- **{nid}** · {nodes[nid].get('title','')}{tail}")
        L.append("")

    amended = sorted(by_state.get("AMENDED", []), key=_sort_key)
    if amended:
        L.append(f"**◐ AMENDED — live, but a specific claim is dead ({len(amended)}):**")
        for nid in amended:
            claims = [e.get("claim") for e in inbound.get(nid, [])
                      if e["type"] == "supersedes" and e.get("claim")]
            tail = f" — dead claim(s): {'; '.join(c for c in claims if c)}" if claims else ""
            L.append(f"- **{nid}** · {nodes[nid].get('title','')}{tail}")
        L.append("")

    opn = sorted(by_state.get("OPEN", []), key=_sort_key)
    if opn:
        L.append(f"**○ OPEN / proposed ({len(opn)}):**")
        for nid in opn:
            L.append(f"- **{nid}** · {nodes[nid].get('title','')}")
        L.append("")

    live = sorted(by_state.get("LIVE", []), key=_sort_key)
    if live:
        L.append(f"**✓ LIVE ({len(live)})** — in force; titles in `_DECISION-GRAPH.md` §②:")
        L.append("  " + ", ".join(live))
        L.append("")

    L.append(BLOCK_END)
    return "\n".join(L)


def splice_block(md, block):
    """Replace everything between BLOCK_START and BLOCK_END (inclusive) with `block`.
    Returns (new_md, changed, error). If the markers are absent, returns an error rather
    than guessing a location — the section is seeded once by hand, then owned by the generator."""
    si = md.find(BLOCK_START)
    ei = md.find(BLOCK_END)
    if si == -1 or ei == -1 or ei < si:
        return md, False, "AUTO-DECISION-LIFECYCLE markers not found in _LIVE-STATE.md — block not generated."
    ei_end = ei + len(BLOCK_END)
    new_md = md[:si] + block + md[ei_end:]
    return new_md, (new_md != md), None


def generate_block(live_path=None, graph_path=None):
    """ADR-0007 part 2. Read the graph JSON, render the lifecycle block, splice it into
    _LIVE-STATE.md. Idempotent. Returns a short status string for the build log.

    Validate-then-write (#78-D2): every refusal path returns BEFORE any write, and the write
    itself is atomic (temp file + os.replace) so no failure mode half-writes the spine. The
    path parameters exist for the selftest, which must exercise this exact function on COPIES
    — a selftest of a lookalike would prove nothing (attribute-the-diff)."""
    live_path = live_path if live_path is not None else LIVE
    graph_path = graph_path if graph_path is not None else GRAPH_JSON
    if not os.path.isfile(graph_path):
        return "lifecycle block SKIPPED — _decision-graph.json not found (run _build_decision_graph.py first)."
    try:
        import json
        with open(graph_path, encoding="utf-8") as f:
            graph = json.load(f)
    except Exception as ex:
        return f"lifecycle block SKIPPED — could not read _decision-graph.json ({ex})."
    md = read(live_path)
    if not md:
        return "lifecycle block SKIPPED — no _LIVE-STATE.md."
    block = render_lifecycle_block(graph)
    new_md, changed, err = splice_block(md, block)
    if err:
        return err
    if changed:
        # atomic: the old non-atomic open(...,"w") could half-write the spine if killed
        # mid-write (the sandbox kills at the ~45s wall). Same-directory temp so os.replace
        # never crosses a device boundary (the git-lock mv lesson, #56).
        tmp = live_path + ".splice-tmp~"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(new_md)
        os.replace(tmp, live_path)
        return "lifecycle block REGENERATED in _LIVE-STATE.md (content changed)."
    return "lifecycle block up to date (no change)."


# ---------------------------------------------------------------------------
# SELFTEST (#78-D2, option-select 2026-08-02) — the splice writer was the spine's one
# UNGATED writer (#77 periphery inventory). House style: a bite list, each arm named,
# exit 0/1, failed arms printed; every green provably able to fail (mutation controls
# below doctor the splice OUTPUT and the fixture INPUT and assert red). All write-path
# work happens on copies inside tempfile.TemporaryDirectory — never the real spine.
# Consumer: _git_commit.sh (#74-D1 split — WARN mid-session, BLOCK on --wrap).
# ---------------------------------------------------------------------------

FIXTURE_GRAPH = {
    "nodes": {"R-D1": {"title": "alpha ruling"}, "T-D2": {"title": "beta ruling"}},
    "edges": [{"from": "T-D2", "to": "R-D1", "type": "supersedes"}],
    "state": {"R-D1": "DEAD", "T-D2": "LIVE"},
}

FIXTURE_LIVE = (
    "# _LIVE-STATE (selftest fixture)\n"
    "Last refreshed: **2026-08-02**\n"
    "\n"
    "prefix prose — must be byte-identical after any splice\n"
    "\n"
    + BLOCK_START + " — seeded by hand -->\n"
    "stale hand-seeded body, to be replaced\n"
    + BLOCK_END + "\n"
    "\n"
    "suffix prose — must be byte-identical after any splice\n"
)


def _splice_invariants(before_md, after_md):
    """Pure invariant checker for a splice: returns a list of violation messages (empty = hold).
    Invariants: exactly one START and one END marker; END after START; every byte OUTSIDE the
    marker region identical to `before_md`. The mutation arm feeds this DOCTORED output and
    asserts it goes red — otherwise the happy-path green is an assertion, not a test."""
    v = []
    n_start = after_md.count(BLOCK_START)
    n_end = after_md.count(BLOCK_END)
    if n_start != 1:
        v.append(f"expected exactly 1 START marker after splice, found {n_start}")
    if n_end != 1:
        v.append(f"expected exactly 1 END marker after splice, found {n_end}")
    if v:
        return v  # region indices are meaningless with duplicated/missing markers
    b_si, b_ei = before_md.find(BLOCK_START), before_md.find(BLOCK_END) + len(BLOCK_END)
    a_si, a_ei = after_md.find(BLOCK_START), after_md.find(BLOCK_END) + len(BLOCK_END)
    if b_si == -1 or before_md.find(BLOCK_END) == -1:
        v.append("fixture (before) lacks markers — invariants cannot be compared")
        return v
    if a_ei <= a_si:
        v.append("END marker precedes START in the spliced result")
    if after_md[:a_si] != before_md[:b_si]:
        v.append("bytes BEFORE the spliced region changed — splice leaked upstream")
    if after_md[a_ei:] != before_md[b_ei:]:
        v.append("bytes AFTER the spliced region changed — splice ate the suffix")
    return v


def _write_fixture(td, live_md=FIXTURE_LIVE, graph=FIXTURE_GRAPH):
    """Materialise a fixture spine + graph inside tempdir `td`; returns (live_path, graph_path).
    Fails LOUD on any IO error — a fixture that silently failed to land would green every arm."""
    import json
    live_p = os.path.join(td, "_LIVE-STATE.md")
    graph_p = os.path.join(td, "_decision-graph.json")
    with open(live_p, "w", encoding="utf-8") as f:
        f.write(live_md)
    with open(graph_p, "w", encoding="utf-8") as f:
        json.dump(graph, f)
    return live_p, graph_p


def selftest_happy_path():
    """Arm 1 — splice lands on a fixture copy, invariants hold, outside bytes identical."""
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as td:
        live_p, graph_p = _write_fixture(td)
        before = read(live_p)
        status = generate_block(live_p, graph_p)
        after = read(live_p)
        if "REGENERATED" not in status:
            fails.append(f"expected REGENERATED status on a stale fixture, got: {status}")
        if "superseded by T-D2" not in after:
            fails.append("rendered block missing the supersession annotation — splice did not "
                         "land real graph content")
        if "stale hand-seeded body" in after:
            fails.append("old block body survived the splice")
        fails += _splice_invariants(before, after)
    return fails


def selftest_idempotent():
    """Arm 2 — second run on unchanged inputs is a NO-OP: same status contract, same bytes."""
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as td:
        live_p, graph_p = _write_fixture(td)
        generate_block(live_p, graph_p)
        once = read(live_p)
        status2 = generate_block(live_p, graph_p)
        twice = read(live_p)
        if "no change" not in status2:
            fails.append(f"second run did not report a no-op, got: {status2}")
        if twice != once:
            fails.append("second run CHANGED the file — the splice is not idempotent")
    return fails


def selftest_refusal_missing_markers():
    """Arm 3 — malformed spine (no anchor markers) → refuses loud + named, file untouched."""
    import tempfile
    fails = []
    no_markers = "# _LIVE-STATE (fixture)\nno lifecycle markers anywhere in this file\n"
    with tempfile.TemporaryDirectory() as td:
        live_p, graph_p = _write_fixture(td, live_md=no_markers)
        status = generate_block(live_p, graph_p)
        if "markers not found" not in status:
            fails.append(f"expected a NAMED marker refusal, got: {status}")
        if read(live_p) != no_markers:
            fails.append("refusal TOUCHED the file — the marker-less spine changed on disk")
    return fails


def selftest_refusal_never_half_writes():
    """Arm 4 — every refusal path leaves the target byte-identical: END-before-START ordering,
    unparseable graph JSON, and a missing graph file. (Missing spine has no bytes to protect;
    generate_block returns its named SKIP for that path, asserted here too.)"""
    import tempfile
    fails = []
    inverted = ("# fixture\n" + BLOCK_END + "\nEND placed before START — ordering violation\n"
                + BLOCK_START + " -->\n")
    with tempfile.TemporaryDirectory() as td:
        # (a) END precedes START
        live_p, graph_p = _write_fixture(td, live_md=inverted)
        status = generate_block(live_p, graph_p)
        if "markers not found" not in status:
            fails.append(f"END-before-START: expected the marker refusal, got: {status}")
        if read(live_p) != inverted:
            fails.append("END-before-START refusal modified the file")
        # (b) unparseable graph JSON — refusal must name the cause, spine untouched
        live_p2 = os.path.join(td, "b", "_LIVE-STATE.md")
        os.makedirs(os.path.dirname(live_p2))
        with open(live_p2, "w", encoding="utf-8") as f:
            f.write(FIXTURE_LIVE)
        bad_graph = os.path.join(td, "b", "_decision-graph.json")
        with open(bad_graph, "w", encoding="utf-8") as f:
            f.write("{not json,")
        status = generate_block(live_p2, bad_graph)
        if "could not read" not in status:
            fails.append(f"bad graph JSON: expected the named read refusal, got: {status}")
        if read(live_p2) != FIXTURE_LIVE:
            fails.append("bad-graph refusal modified the spine fixture")
        # (c) graph file absent
        status = generate_block(live_p2, os.path.join(td, "b", "no-such.json"))
        if "not found" not in status:
            fails.append(f"missing graph: expected the named SKIP, got: {status}")
        if read(live_p2) != FIXTURE_LIVE:
            fails.append("missing-graph skip modified the spine fixture")
        # (d) spine file absent — named skip, nothing created. Uses the VALID graph from (a):
        # the graph is (rightly) read before the spine, so a bad graph here would mask this path.
        ghost = os.path.join(td, "b", "no-spine.md")
        status = generate_block(ghost, graph_p)
        if "no _LIVE-STATE.md" not in status:
            fails.append(f"missing spine: expected the named SKIP, got: {status}")
        if os.path.exists(ghost):
            fails.append("missing-spine path CREATED a file")
    return fails


def selftest_mutation_controls():
    """Arm 5 — prove the greens above can fail. (m1) doctored splice output that ate the
    suffix must red the invariant checker; (m2) doctored output with a duplicated END marker
    must red it; (m3) a byte injected INSIDE the region must make the idempotency no-op
    go red (REGENERATED, and restored to canonical form); (m4) a byte appended OUTSIDE the
    region must red the outside-bytes invariant."""
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as td:
        live_p, graph_p = _write_fixture(td)
        before = read(live_p)
        generate_block(live_p, graph_p)
        good = read(live_p)
        # m1 — splice that ate the suffix (truncate at END marker)
        ate_suffix = good[:good.find(BLOCK_END) + len(BLOCK_END)]
        if not _splice_invariants(before, ate_suffix):
            fails.append("m1: invariant checker stayed green on output whose suffix was eaten "
                         "— the happy-path green cannot fail")
        # m2 — duplicated END marker
        doubled = good + "\n" + BLOCK_END
        if not any("END marker" in x for x in _splice_invariants(before, doubled)):
            fails.append("m2: invariant checker stayed green on a duplicated END marker")
        # m3 — idempotency bite: corrupt one byte INSIDE the region, rerun, expect REGENERATED
        with open(live_p, "w", encoding="utf-8") as f:
            f.write(good.replace("superseded by T-D2", "superseded by X-D9", 1))
        status = generate_block(live_p, graph_p)
        if "REGENERATED" not in status:
            fails.append(f"m3: in-region drift did NOT trigger a regenerate (idempotency "
                         f"no-op green cannot fail), got: {status}")
        if read(live_p) != good:
            fails.append("m3: regenerate did not restore the canonical block")
        # m4 — outside-region drift must red the outside-bytes invariant
        if not any("AFTER the spliced region" in x for x in
                   _splice_invariants(before, good + "trailing-drift")):
            fails.append("m4: invariant checker stayed green on bytes appended after the region")
    return fails


def run_selftest():
    """Run every bite; print failed arms; exit 0 green / 1 red. Belt-and-braces: the real
    spine's bytes are hashed before and after — if any arm ever touches it, that IS a red."""
    import hashlib
    spine_before = hashlib.sha256(read(LIVE).encode("utf-8")).hexdigest() if os.path.isfile(LIVE) else None
    bites = [
        ("happy-path: splice lands on a fixture copy, invariants hold", selftest_happy_path),
        ("idempotency: second run is a no-op", selftest_idempotent),
        ("refusal: marker-less spine refused loud+named, untouched", selftest_refusal_missing_markers),
        ("refusal never half-writes: every failure path leaves the target byte-identical",
         selftest_refusal_never_half_writes),
        ("mutation controls: every green above provably able to fail", selftest_mutation_controls),
    ]
    failed = []
    for name, fn in bites:
        try:
            arm_fails = fn()
        except Exception as ex:  # a crash is not a fail — surface it LOUD and NAMED as one
            arm_fails = [f"CRASHED: {type(ex).__name__}: {ex}"]
        if arm_fails:
            failed.append((name, arm_fails))
            print(f"  ✗ {name}")
            for msg in arm_fails:
                print(f"      - {msg}")
        else:
            print(f"  ✓ {name}")
    if spine_before is not None:
        spine_after = hashlib.sha256(read(LIVE).encode("utf-8")).hexdigest()
        if spine_after != spine_before:
            failed.append(("spine-safety", ["the REAL _LIVE-STATE.md changed during the selftest"]))
            print("  ✗ spine-safety: the REAL _LIVE-STATE.md changed during the selftest")
        else:
            print("  ✓ spine-safety: real _LIVE-STATE.md untouched (sha256 identical)")
    if failed:
        print(f"_build_live_state --selftest: {len(failed)} arm(s) RED")
        return 1
    print("_build_live_state --selftest: all arms green")
    return 0


def main():
    # ADR-0007 part 2 — generation half: refresh the decision-node lifecycle block FIRST,
    # so the staleness checks below run against the freshly-generated spine.
    gen_status = generate_block()
    print(f"  [gen] {gen_status}")

    md = read(LIVE)
    if not md:
        print("no _LIVE-STATE.md found");  return 0
    secs = split_sections(md)
    live_body = section(secs, "LIVE")
    dead_body = section(secs, "SUPERSEDED") or section(secs, "DEAD")
    findings = []  # (severity, check, msg)

    # ---- 1. freshness drift ----
    # tolerate markdown around the date (e.g. bold `**2026-07-20**`): skip any
    # non-digit chars on the same line between the label and the date (fixes the
    # long-silent freshness blindness — the stamp is always bolded, 2026-07-20).
    m = re.search(r"Last refreshed:[^\d\n]*(\d{4}-\d{2}-\d{2})", md)
    stamp = m.group(1) if m else None
    tracked = []
    if os.path.isdir(DECISIONS):
        tracked += [os.path.join(DECISIONS, f) for f in os.listdir(DECISIONS) if f.endswith(".md")]
    for f in os.listdir(HERE):
        if f.startswith("_") and (f.endswith(".md")) and "FINDINGS" in f.upper():
            tracked.append(os.path.join(HERE, f))
    tracked.append(os.path.join(HERE, "_FIXED-FLEX-CHARTER.md"))
    newest, newest_f = None, None
    for f in tracked:
        d = git_date(f)
        if d and (newest is None or d > newest):
            newest, newest_f = d, os.path.relpath(f, ROOT)
    if stamp and newest and newest > stamp:
        findings.append(("⚠", "freshness",
            f"`Last refreshed: {stamp}` is older than the newest decision-doc change "
            f"({newest}, `{newest_f}`). Refresh the stamp + reconcile the ledger."))
    elif not stamp:
        findings.append(("⚠", "freshness", "No `Last refreshed:` stamp found in the header."))

    # ---- parse DEAD entries ----
    dead_entries = []
    for b in bullets(dead_body):
        # The dead node is only what's LEFT of the supersession arrow; files to the RIGHT are the
        # LIVE replacement (superseder) and must NOT be treated as dead.
        left = re.split(r"→|superseded[ -]?by|superseded by|\bretired\b", b, maxsplit=1, flags=re.I)[0]
        right = b[len(left):]
        files = [x for x in FILE_RE.findall(left) if not x.endswith("_LIVE-STATE.md")]
        node = files[0] if files else left.strip("-* ").split("—")[0].strip()[:70]
        sup = None
        sm = re.search(r"(?:superseded[ -]?by|→\s*superseded by|by)\s+([^\(.]+)", right, re.I)
        if sm:
            sup = sm.group(1).strip()
        dead_entries.append({"raw": b, "node": node, "files": files, "sup": sup,
                             "tombstoned": bool(re.search(r"tombstone", b, re.I))})

    # ---- 2. dead-node resurrection (LIVE cites a dead node) ----
    for d in dead_entries:
        for f in d["files"]:
            base = os.path.basename(f)
            if base in live_body:
                findings.append(("⚠", "resurrection",
                    f"DEAD node `{base}` is cited in the LIVE section — live truth points at a "
                    f"superseded artifact."))

    # dead artifacts still referenced (un-tombstoned) elsewhere in the corpus
    dead_files = [os.path.basename(f) for d in dead_entries for f in d["files"] if f.endswith((".html", ".md"))]
    if dead_files:
        scan_dirs = [HERE, os.path.join(HERE, "_fitness-test")]
        for base in sorted(set(dead_files)):  # sorted: deterministic report order (dream-pass v2 P2, 2026-07-26)
            hits = []
            for sd in scan_dirs:
                if not os.path.isdir(sd):
                    continue
                for fn in os.listdir(sd):
                    p = os.path.join(sd, fn)
                    if not os.path.isfile(p) or fn == "_LIVE-STATE-CHECK.md":
                        continue
                    if fn.endswith((".md", ".html")) and base in read(p) and fn != base:
                        body = read(p)
                        # only flag if the reference isn't itself marked dead near the mention
                        if not TOMB_RE.search(body[max(0, body.find(base) - 120): body.find(base) + 120]):
                            hits.append(os.path.relpath(p, ROOT))
            if hits:
                findings.append(("i", "reference",
                    f"DEAD artifact `{base}` is mentioned (no nearby tombstone) in: "
                    + ", ".join(f"`{h}`" for h in hits[:4]) + ("…" if len(hits) > 4 else "")))

    # ---- 3. tombstone consistency ----
    for d in dead_entries:
        for f in d["files"]:
            ap = os.path.join(ROOT, f) if not os.path.isabs(f) else f
            if not os.path.exists(ap):
                # try under knowledge/
                alt = os.path.join(HERE, f)
                ap = alt if os.path.exists(alt) else ap
            if not os.path.exists(ap):
                findings.append(("⚠", "tombstone", f"DEAD entry `{f}` — file not found (moved/renamed? edge is orphaned)."))
            elif not TOMB_RE.search(read(ap)[:1500]):
                findings.append(("⚠", "tombstone", f"DEAD file `{f}` exists but has NO tombstone banner in its first lines."))

    # ---- 4. lifecycle contradiction (ADR deferred/superseded but LIVE cites it) ----
    adr_state = {}
    if os.path.isdir(DECISIONS):
        for fn in sorted(os.listdir(DECISIONS)):
            if not fn.endswith(".md"):
                continue
            mnum = ADR_RE.search(fn)
            if not mnum:
                continue
            head = read(os.path.join(DECISIONS, fn))[:1600]
            aid = "ADR-" + mnum.group(1)
            state = "accepted"
            # lifecycle comes from the Status line, not stray 'superseded' mentions in prose
            sl = re.search(r"\*\*Status:\*\*\s*([^\n·|]+)", head)
            status_txt = (sl.group(1) if sl else "").lower()
            if "supersed" in status_txt or "retired" in status_txt:
                state = "superseded"
            # explicit audit-banner deferral (validation state), or a banner retiring THIS adr
            if re.search(r"\bDEFERRED\b|validation state\s*=\s*`?defer", head):
                state = "deferred"
            if re.search(aid + r"[^\n]{0,40}(superseded|retired)\b", head, re.I):
                state = "superseded"
            adr_state[aid] = state
    for adr in sorted(set(ADR_RE.findall(live_body))):  # sorted: deterministic (P2)
        aid = "ADR-" + adr
        st = adr_state.get(aid)
        if st in ("deferred", "superseded"):
            findings.append(("⚠", "lifecycle",
                f"LIVE section cites `{aid}` as current truth, but its own banner marks it **{st}**."))

    # ---- 5. orphan supersession edges ----
    known_files = set()
    for base_dir in (HERE, DECISIONS, os.path.join(HERE, "_fitness-test")):
        if os.path.isdir(base_dir):
            known_files.update(os.listdir(base_dir))
    for d in dead_entries:
        if d["sup"]:
            tgt = d["sup"]
            ok = ("§" in tgt or "ADR" in tgt or "git split" in tgt.lower()
                  or any(os.path.basename(x) in known_files for x in FILE_RE.findall(tgt))
                  or "GOOD-MORNING" in tgt or "charter" in tgt.lower())
            if not ok:
                findings.append(("i", "orphan-edge",
                    f"DEAD `{d['node']}` → superseded-by \"{tgt[:40]}\" — target not resolvable to a known ADR/§/file."))

    # ---- report ----
    warns = [f for f in findings if f[0] == "⚠"]
    infos = [f for f in findings if f[0] == "i"]
    L = ["# _LIVE-STATE staleness check", "",
         "*Generated by `_build_live_state.py` (ADR-0007 gate, advisory). Consistency only — "
         "**never implies validity** (a clean ledger is not a vouched one; see the audit banner in "
         "`_LIVE-STATE.md`).*", "",
         f"**{len(warns)} warning(s) · {len(infos)} note(s).** "
         + ("✅ ledger is internally consistent." if not warns else "⚠ drift detected — see below."),
         ""]
    by = {}
    for sev, chk, msg in findings:
        by.setdefault(chk, []).append((sev, msg))
    order = ["freshness", "resurrection", "lifecycle", "tombstone", "orphan-edge", "reference"]
    labels = {"freshness": "1 · Freshness drift", "resurrection": "2 · Dead-node resurrection",
              "tombstone": "3 · Tombstone consistency", "lifecycle": "4 · Lifecycle contradiction",
              "orphan-edge": "5 · Orphan supersession edge", "reference": "· Dead-artifact references (info)"}
    for chk in order:
        if chk in by:
            L.append(f"## {labels.get(chk, chk)}")
            for sev, msg in by[chk]:
                L.append(f"- {sev} {msg}")
            L.append("")
    if not findings:
        L.append("_Nothing flagged._")
    L += ["---",
          f"*Checked: {len(dead_entries)} DEAD entries · {len(adr_state)} ADRs · "
          f"LIVE section {len(bullets(live_body))} bullets.*"]
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")

    print(f"_LIVE-STATE check: {len(warns)} warning(s), {len(infos)} note(s) -> "
          + os.path.relpath(OUT, ROOT))
    for sev, chk, msg in findings:
        print(f"  {sev} [{chk}] {re.sub(chr(96),'',msg)[:110]}")
    return len(warns)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    warns = main()
    # Advisory by default (ADR-0005 §5: earns blocking by bite-test). `--strict` exits with the
    # warning count so it can gate once it's proven quiet. _build_all.py runs it without --strict.
    sys.exit(warns if "--strict" in sys.argv else 0)
