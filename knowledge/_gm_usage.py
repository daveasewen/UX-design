#!/usr/bin/env python3
"""Section-usage instrumentation (#23, ruled Dave 2026-07-28 — lane 1 step 2).

WHAT THIS MEASURES (JIT note §7.3, `notes/2026-07-28-memento-jit-context-research.md`):
whether the cold-start chain's reference weight is actually USED. Every wrap, the session's
GM stratum block carries two lines beside the pre-flight stamp:

  > **section-usage #<N> (observed, self-report):** GM HDR:C LATEST:C ... · LS HDR:R SPIN:U ...
  > **section-sizes #<N> (<method>):** GM HDR:2410 LATEST:1187 ... · LS ... · totals GM:14332 LS:16762

Codes (ruled U/R/C, 3-state): U = unread this session · R = read (loaded into context) ·
C = cited (actually shaped a decision or an edit). Usage × size, accumulated in
`notes/_GAUGE-LOG.md` as strata roll (existing 2f mechanism, zero new plumbing), is the
dataset that answers LS-trim-vs-defer (P4b) and tests the JIT premise before any surgery.

HONESTY CONTRACT (the pre-flight-stamp precedent): the usage line is the session's own
TESTIMONY — this tool and the gate check FORM only (vocabulary complete, codes legal,
every section testified exactly once). Whether a `C` is honest is discipline, not
enforcement. The sizes line, by contrast, is CODE-MEASURED (measure_tokens, imported
from `_capture_gate.py` so the heal/fallback self-description is shared, never re-implemented).

FAIL-LOUD VOCABULARY (the dv-vocab / ds-016 lesson): the section vocabulary below is the
ONLY copy. An unregistered `## ` heading in _LIVE-STATE.md, or an unregistered numbered
queue heading in GOOD-MORNING.md, makes the sizes walk REFUSE — never enumerate-and-skip,
never a cheerful partial answer. Adding a section to either file means registering it here
(the accretion bite is deliberate).

TIER (ruled #23, trigger fired #24): O1′ started, so the promotion pair flipped —
SECTION_USAGE_BLOCKING=True in `_capture_gate.py` + its selftest pin, one deliberate
edit pair (M10's pattern). A missing/malformed stratum line now FAILS the wrap.

Usage:  python3 knowledge/_gm_usage.py --sizes --session 23   # print the code-measured sizes line
        python3 knowledge/_gm_usage.py --check-line "<line>"  # validate a usage line (exit 1 on malformed)
        python3 knowledge/_gm_usage.py --selftest             # bites — every check proves it can FAIL
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

CODES = ("U", "R", "C")

# --- THE VOCABULARY — only copy. (id, line-START pattern). Order = document order.
# GM: C1 deliberately starts at the `# §C` heading itself so the queue preamble has an owner.
GM_VOCAB = (
    ("HDR",     None),  # implicit: file start → first explicit marker
    ("LATEST",  re.compile(r"^>\s*##\s*★\s*LATEST\b")),
    ("PRIOR",   re.compile(r"^>\s*##\s*★\s*PRIOR\b")),
    ("DOFIRST", re.compile(r"^##\s*⬛\s*DO TH", re.I)),
    ("A",       re.compile(r"^#\s*§A\b")),
    ("C1",      re.compile(r"^#\s*§C\b|^##\s*1\.\s")),
    ("C2",      re.compile(r"^##\s*2\.\s")),
    ("C2b",     re.compile(r"^##\s*2b\.\s")),
    ("C3",      re.compile(r"^##\s*3\.\s")),
    ("C4",      re.compile(r"^##\s*4\.\s")),
    ("C4b",     re.compile(r"^##\s*4b\.\s")),
    ("C5",      re.compile(r"^##\s*5\.\s")),
    ("STRATA",  re.compile(r"^###\s*⏱\s*SESSION STRATA\b", re.I)),
)
# Any numbered queue heading must be registered above — `## 6.` is a structure change, refuse.
GM_NUMBERED_RE = re.compile(r"^##\s*\d+[a-z]?\.\s")

# LS: every `## ` heading must match a pattern here or the ⏱ continuation — else refuse.
LS_VOCAB = (
    ("HDR",       None),
    ("LANES",     re.compile(r"^##\s*🛤")),   # O1′ #24 — generated lane index (AUTO-LANES)
    ("SPIN",      re.compile(r"^##\s*🔀")),
    ("DELTAS",    re.compile(r"^##\s*⏱")),   # LATEST/PRIOR/OLDER all merge — one region
    ("WEBFONT",   re.compile(r"^##\s*🕓")),
    ("LIVE",      re.compile(r"^##\s*LIVE\b")),
    ("LIFECYCLE", re.compile(r"^##\s*DECISION-NODE LIFECYCLE\b")),
    ("DEAD",      re.compile(r"^##\s*SUPERSEDED\b")),
    ("OPEN",      re.compile(r"^##\s*OPEN\b")),
    ("TARGETS",   re.compile(r"^##\s*PLANNED\b")),
    ("SPINOFFS",  re.compile(r"^##\s*SPIN-OFF\b")),
)
LS_HEADING_RE = re.compile(r"^##\s")

# --- §A SUBSECTION VOCABULARY (worker lane `worker-a-subdivision`, cut at #33) ----------
# WHY THIS EXISTS: #32 cut the eager read chain, so §A became retrieval-on-demand via the
# Memento door. #33 then MEASURED the door and found `--fetch gm:A` returned the ENTIRE
# §A — 4,208 tk cl100k, all or nothing. A coarse door is not retrieval: it moves §A from
# *paid every window* to *paid in full on the first §A-shaped question* ("where does X
# live", "what are the four themes", "what's the build command" — the commonest questions
# there are). This vocabulary lets the door serve ONE subsection.
#
# ★ WHY IT IS SEPARATE FROM GM_VOCAB, AND MUST STAY SEPARATE:
#   GM_VOCAB is the SECTION-USAGE vocabulary. `validate_usage_line` demands testimony for
#   every id in it, and SECTION_USAGE_BLOCKING is True — so adding 11 ids to GM_VOCAB would
#   require editing the `> **section-usage #N:**` line INSIDE GOOD-MORNING.md, and would
#   fail every wrap until that happened. Retrieval granularity and testimony granularity
#   are DIFFERENT QUESTIONS at DIFFERENT COSTS; conflating them makes the cheap change
#   (a finer door) pay the expensive change's price (a wider testimony contract). Whether
#   usage testimony should also go per-subsection is #34's call, not this lane's.
#   ⇒ §A's usage testimony is still a single `A:<code>`. Unchanged by design, not by omission.
#
# Same dv-004 shape as its siblings: the vocabulary is the ONLY copy, order = document
# order, and an unregistered `## ` heading inside the §A span REFUSES (never
# enumerate-and-skip). Note this check is deliberately fence-UNAWARE, exactly like
# `_ls_unknown`: a `## ` at line start inside a code fence would refuse loudly rather than
# be silently normalised away. That refusal is correct — register it or reformat it.
GM_A_SUBVOCAB = (
    ("PRE",      None),  # implicit: the `# §A` heading + Memento framing + STANDING note
    ("WHAT",     re.compile(r"^##\s+What Apollo is\b")),
    ("THEMES",   re.compile(r"^##\s+★\s*ONE token store\b")),
    ("WHERE",    re.compile(r"^##\s+Where things live\b")),
    ("CMD",      re.compile(r"^##\s+The one command that matters\b")),
    ("RULES",    re.compile(r"^##\s+Rules that actually bite\b")),
    ("AGENT",    re.compile(r"^##\s+Standing instructions for the agent\b")),
    ("DOCS",     re.compile(r"^##\s+The other standing documents\b")),
    ("PARALLEL", re.compile(r"^##\s+Parallel-session model\b")),
    ("RENDERS",  re.compile(r"^##\s+Renders\b")),
    ("HOW",      re.compile(r"^##\s+How we work\b")),
)
GM_A_HEADING_RE = re.compile(r"^##\s")


def _gm_a_unknown(ln):
    if GM_A_HEADING_RE.match(ln) and not any(
            rx.match(ln) for _, rx in GM_A_SUBVOCAB if rx is not None):
        return ("unregistered `## ` subsection heading inside §A of GOOD-MORNING.md — "
                "register it in GM_A_SUBVOCAB (the only copy) so the Memento door can "
                "serve it; never index around a hole")
    return None


def split_gm_a(lines, span):
    """Subdivide the §A span into its subsections. `span` is the (start, end) the GM_VOCAB
    walk gave for id `A`. Returns (ordered [(subid, (abs_start, abs_end))], errors) with
    line numbers RE-BASED onto the whole file so records keep honest file:line provenance.
    Fails loud through `split_sections` — a missing/reordered/unregistered heading refuses."""
    start, end = span
    sub, errs = split_sections(lines[start:end], GM_A_SUBVOCAB, _gm_a_unknown)
    if errs:
        return None, [f"§A: {e}" for e in errs]
    ordered = sorted(sub.items(), key=lambda kv: kv[1][0])
    return [(sid, (start + a, start + b)) for sid, (a, b) in ordered], []


USAGE_RE = re.compile(
    r"^>\s*\*\*section-usage\s+#(\d+)\s*\(([^)]*)\):\*\*\s*GM\s+(.*?)\s*·\s*LS\s+(.*?)\s*$")
SIZES_RE = re.compile(
    r"^>\s*\*\*section-sizes\s+#(\d+)\s*\(([^)]*)\):\*\*\s*GM\s+(.*?)\s*·\s*LS\s+(.*?)(\s*·\s*totals.*)?$")
TOKEN_RE = re.compile(r"^([A-Za-z0-9]+):([A-Za-z0-9]+)$")


def _ids(vocab):
    return [i for i, _ in vocab]


def split_sections(lines, vocab, unknown_check=None):
    """(id → (start, end)) by document order, HDR implicit from 0. Fails LOUD (returns
    (None, [errors])) on: a registered marker missing, markers out of order, or an
    unregistered heading caught by unknown_check(line) → error-string-or-None."""
    errors, hits = [], []
    for vid, rx in vocab:
        if rx is None:
            continue
        pos = [i for i, ln in enumerate(lines) if rx.match(ln)]
        if not pos:
            errors.append(f"vocabulary marker not found: {vid} — structure changed? "
                          f"register or restore it (fail-loud, never skip)")
        else:
            hits.append((pos[0], vid))
    if unknown_check:
        claimed = set()
        for _, rx in vocab:
            if rx is None:
                continue
            claimed.update(i for i, ln in enumerate(lines) if rx.match(ln))
        for i, ln in enumerate(lines):
            msg = unknown_check(ln)
            if msg and i not in claimed:
                errors.append(f"line {i + 1}: {msg}: {ln.strip()[:70]}")
    if errors:
        return None, errors
    hits.sort()
    if [v for _, v in hits] != [v for v, rx in vocab if rx is not None]:
        return None, ["vocabulary markers out of document order — the registered order is "
                      "the contract; a reorder is a structure change, refuse and re-register"]
    # the implicit leading span is the vocabulary's FIRST entry when it declares no
    # pattern — named by the vocabulary, not hardcoded ("HDR" for GM/LS, "PRE" for §A).
    spans = {}
    if vocab and vocab[0][1] is None:
        spans[vocab[0][0]] = (0, hits[0][0])
    for n, (i, vid) in enumerate(hits):
        spans[vid] = (i, hits[n + 1][0] if n + 1 < len(hits) else len(lines))
    return spans, []


def _gm_unknown(ln):
    if GM_NUMBERED_RE.match(ln) and not any(
            rx.match(ln) for _, rx in GM_VOCAB if rx is not None):
        return "unregistered numbered queue heading in GOOD-MORNING.md"
    return None


def _ls_unknown(ln):
    if LS_HEADING_RE.match(ln) and not any(
            rx.match(ln) for _, rx in LS_VOCAB if rx is not None):
        return "unregistered `## ` section heading in _LIVE-STATE.md"
    return None


def measure_sizes(repo=REPO):
    """Code-measured per-section token sizes. Returns (rows, method, errors) where rows =
    [('GM', id, tk), ...]. measure_tokens is IMPORTED from the gate — one implementation
    of the heal/fallback contract, never a second copy."""
    sys.path.insert(0, HERE)
    from _capture_gate import measure_tokens  # function-level: breaks the import cycle
    rows, method, errors = [], None, []
    for group, fname, vocab, unknown in (
            ("GM", "GOOD-MORNING.md", GM_VOCAB, _gm_unknown),
            ("LS", "_LIVE-STATE.md", LS_VOCAB, _ls_unknown)):
        path = os.path.join(repo, fname)
        if not os.path.exists(path):
            errors.append(f"{fname}: missing")
            continue
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        spans, errs = split_sections(lines, vocab, unknown)
        if errs:
            errors += [f"{fname}: {e}" for e in errs]
            continue
        for vid, _ in vocab:
            s, e = spans[vid]
            tk, method = measure_tokens("\n".join(lines[s:e]))
            rows.append((group, vid, tk))
    return rows, method, errors


def sizes_line(session, repo=REPO):
    rows, method, errors = measure_sizes(repo)
    if errors:
        return None, errors
    parts, totals = {"GM": [], "LS": []}, {"GM": 0, "LS": 0}
    for group, vid, tk in rows:
        parts[group].append(f"{vid}:{tk}")
        totals[group] += tk
    return (f"> **section-sizes #{session} ({method}):** "
            f"GM {' '.join(parts['GM'])} · LS {' '.join(parts['LS'])} "
            f"· totals GM:{totals['GM']} LS:{totals['LS']}"), []


def validate_usage_line(line):
    """FORM check only (testimony stays the session's). Returns list of issues, [] = well-formed."""
    m = USAGE_RE.match(line.strip())
    if not m:
        return ["section-usage line does not match the contract "
                "`> **section-usage #<N> (<status>):** GM <ID:CODE ...> · LS <ID:CODE ...>`"]
    issues = []
    if "self-report" not in m.group(2):
        issues.append("status parenthetical must say self-report — the line is testimony "
                      "and must describe itself as such (confident-false-inscription guard)")
    for group, blob, vocab in (("GM", m.group(3), GM_VOCAB), ("LS", m.group(4), LS_VOCAB)):
        seen = {}
        for tok in blob.split():
            tm = TOKEN_RE.match(tok)
            if not tm:
                issues.append(f"{group}: malformed token `{tok}`")
                continue
            vid, code = tm.group(1), tm.group(2)
            if vid not in _ids(vocab):
                issues.append(f"{group}: unknown section id `{vid}` — vocabulary is the "
                              f"only copy (register it, never free-type)")
            elif vid in seen:
                issues.append(f"{group}: section `{vid}` testified twice")
            elif code not in CODES:
                issues.append(f"{group}: `{vid}` carries illegal code `{code}` (U/R/C only)")
            seen[vid] = code
        missing = [v for v in _ids(vocab) if v not in seen]
        if missing:
            issues.append(f"{group}: no testimony for {', '.join(missing)} — every section "
                          f"is testified exactly once, U is a statement too")
    return issues


def validate_stratum(text):
    """For the wrap gate: check the current stratum carries both well-formed lines.
    Returns list of issues; [] = green. Malformed is called out as WORSE than missing."""
    issues = []
    usage = [ln for ln in text.splitlines() if "section-usage" in ln and ln.lstrip().startswith(">")]
    if not usage:
        issues.append("section-usage line MISSING from the session stratum — write the "
                      "testimony (U/R/C per section) via _gm_usage.py; the dataset this "
                      "feeds is what LS-trim-vs-defer waits on")
    else:
        for problem in validate_usage_line(usage[0]):
            issues.append(f"section-usage line MALFORMED (worse than missing — a false "
                          f"inscription): {problem}")
    if not any("section-sizes" in ln for ln in text.splitlines()):
        issues.append("section-sizes line MISSING — emit via "
                      "`python3 knowledge/_gm_usage.py --sizes --session <N>` (code-measured)")
    return issues


# --- selftest — every bite proves the check can FAIL (green control included) ------------
GOOD_USAGE = ("> **section-usage #23 (observed, self-report):** "
              "GM HDR:C LATEST:C PRIOR:R DOFIRST:C A:C C1:C C2:R C2b:R C3:R C4:C C4b:R "
              "C5:R STRATA:R · LS HDR:R LANES:C SPIN:R DELTAS:C WEBFONT:R LIVE:R LIFECYCLE:R "
              "DEAD:R OPEN:R TARGETS:R SPINOFFS:R")


def selftest():
    fails, run = [], []

    def bite(name, cond):
        run.append(name)
        if not cond:
            fails.append(name)

    bite("good line must validate", validate_usage_line(GOOD_USAGE) == [])
    bite("missing id must fire", any("no testimony" in i for i in
         validate_usage_line(GOOD_USAGE.replace("C4b:R ", ""))))
    bite("unknown id must fire", any("unknown section id" in i for i in
         validate_usage_line(GOOD_USAGE.replace("C4b:R", "C4b:R C9:R"))))
    bite("illegal code must fire", any("illegal code" in i for i in
         validate_usage_line(GOOD_USAGE.replace("SPIN:R", "SPIN:X"))))
    bite("duplicate must fire", any("testified twice" in i for i in
         validate_usage_line(GOOD_USAGE.replace("DEAD:R", "DEAD:R DEAD:U"))))
    bite("missing self-report tag must fire", any("self-report" in i for i in
         validate_usage_line(GOOD_USAGE.replace("(observed, self-report)", "(observed)"))))
    bite("non-matching line must fire", validate_usage_line("> section-usage nonsense") != [])

    good_stratum = GOOD_USAGE + "\n> **section-sizes #23 (tiktoken):** GM HDR:1 · LS HDR:1"
    bite("good stratum quiet", validate_stratum(good_stratum) == [])
    bite("stratum missing usage fires", any("MISSING" in i for i in validate_stratum("> x")))
    bite("stratum malformed usage fires — and says MALFORMED", any(
        "MALFORMED" in i for i in validate_stratum(
            GOOD_USAGE.replace("SPIN:R", "SPIN:X") + "\n> **section-sizes #23 (t):** x")))

    gm_fx = ["head", "> ## ★ LATEST — x", "> ## ★ PRIOR — x", "## ⬛ DO THIS FIRST",
             "# §A · ORIENTATION", "# §C · QUEUE", "## 1. strands", "## 2. batch",
             "## 2b. wave", "## 3. eyeball", "## 4. enact", "## 4b. queued",
             "## 5. parked", "### ⏱ SESSION STRATA"]
    spans, errs = split_sections(gm_fx, GM_VOCAB, _gm_unknown)
    bite("gm fixture splits clean", errs == [] and spans is not None
         and spans["C5"] == (12, 13))
    _, errs = split_sections(gm_fx + ["## 6. surprise"], GM_VOCAB, _gm_unknown)
    bite("unregistered `## 6.` must refuse", any("unregistered numbered" in e for e in errs))
    _, errs = split_sections([ln for ln in gm_fx if "## 3." not in ln], GM_VOCAB, _gm_unknown)
    bite("missing GM marker must refuse", any("not found: C3" in e for e in errs))

    ls_fx = ["head", "## 🛤 LANES — generated index", "## 🔀 SPIN-OFF LANE",
             "## ⏱ LATEST DELTA", "## ⏱ PRIOR DELTA",
             "## 🕓 OPEN — webfont", "## LIVE — current truth", "## DECISION-NODE LIFECYCLE",
             "## SUPERSEDED / DEAD", "## OPEN — propagation", "## PLANNED / TARGET STATES",
             "## SPIN-OFF / GENERALISABLE"]
    spans, errs = split_sections(ls_fx, LS_VOCAB, _ls_unknown)
    bite("ls fixture splits clean (⏱ merges)", errs == [] and spans["DELTAS"] == (3, 5))
    _, errs = split_sections(ls_fx + ["## BRAND NEW SECTION"], LS_VOCAB, _ls_unknown)
    bite("unregistered LS heading must refuse", any("unregistered `## `" in e for e in errs))

    # --- §A subdivision (worker lane `worker-a-subdivision`) --------------------------
    # ★ PAIRED, and the POSITIVE ONE IS LOAD-BEARING (#32's lesson, learned expensively):
    # a failure-only suite survives a revert that deletes the whole subdivision — the
    # refusals would still fire on a vocabulary that split nothing. So the first bites
    # assert the RIGHT subsections on a GOOD file, and that they TILE the §A span with no
    # gap and no overlap. Delete the feature and these go red.
    a_fx = ["# §A · ORIENTATION", "> framing", "",
            "## What Apollo is", "w",
            "## ★ ONE token store · ONE baseline library · FOUR themes (R-D15)", "t",
            "## Where things live", "l",
            "## The one command that matters", "c",
            "## Rules that actually bite (core + this session's)", "r",
            "## Standing instructions for the agent", "a",
            "## The other standing documents (REACHABILITY-GATED)", "d",
            "## Parallel-session model (PROVEN 2026-07-21)", "p",
            "## Renders — REAL FONT, in-sandbox", "n",
            "## How we work", "h"]
    got, errs = split_gm_a(a_fx, (0, len(a_fx)))
    bite("§A fixture splits clean", errs == [] and got is not None)
    bite("§A fixture yields EVERY registered subsection, in document order",
         got is not None and [s for s, _ in got] == [i for i, _ in GM_A_SUBVOCAB])
    bite("§A fixture: PRE owns the heading+framing, WHAT starts at its own heading",
         got is not None and dict(got)["PRE"] == (0, 3) and dict(got)["WHAT"] == (3, 5))
    bite("§A fixture: spans TILE the section — no gap, no overlap, no lost line",
         got is not None
         and [sp for _, sp in got][0][0] == 0
         and [sp for _, sp in got][-1][1] == len(a_fx)
         and all(got[n][1][1] == got[n + 1][1][0] for n in range(len(got) - 1)))
    # offset re-basing: the door's file:line provenance must survive the slice
    got_off, errs_off = split_gm_a(["pad"] * 7 + a_fx, (7, 7 + len(a_fx)))
    bite("§A spans re-base onto the whole file (honest file:line)",
         errs_off == [] and got_off is not None and dict(got_off)["WHAT"] == (10, 12))
    # ...and the refusals, which must fire for the RIGHT reason
    _, errs = split_gm_a(a_fx + ["## Something brand new"], (0, len(a_fx) + 1))
    bite("§A: unregistered `## ` subsection REFUSES",
         any("unregistered `## ` subsection" in e for e in errs))
    trimmed = [ln for ln in a_fx if not ln.startswith("## Where things live")]
    _, errs = split_gm_a(trimmed, (0, len(trimmed)))
    bite("§A: a REMOVED registered heading REFUSES (structure change, never a quiet skip)",
         any("not found: WHERE" in e for e in errs))
    swapped = list(a_fx)
    i, j = swapped.index("## How we work"), swapped.index("## What Apollo is")
    swapped[i], swapped[j] = swapped[j], swapped[i]
    _, errs = split_gm_a(swapped, (0, len(swapped)))
    bite("§A: REORDERED headings REFUSE (registered order is the contract)",
         any("out of document order" in e for e in errs))
    # green control on the REAL file — this is the bite that proves the door actually
    # subdivides the shipping §A, not just a fixture that flatters the vocabulary.
    _gm_path = os.path.join(REPO, "GOOD-MORNING.md")
    if os.path.exists(_gm_path):
        with open(_gm_path, encoding="utf-8") as f:
            _gm_lines = f.read().splitlines()
        _spans, _errs = split_sections(_gm_lines, GM_VOCAB, _gm_unknown)
        bite("real GOOD-MORNING.md still splits at GM_VOCAB level", _errs == [])
        if not _errs:
            real, rerrs = split_gm_a(_gm_lines, _spans["A"])
            bite(f"real §A subdivides clean (got: {rerrs[:1]})", rerrs == [])
            bite("real §A yields every registered subsection",
                 real is not None and [s for s, _ in real] == [i for i, _ in GM_A_SUBVOCAB])
            bite("real §A: every subsection is NON-EMPTY (a zero-line record is a hole)",
                 real is not None and all(b > a for _, (a, b) in real))
            bite("real §A: no subsection is the WHOLE of §A (the hole this lane closed)",
                 real is not None and all(
                     (b - a) < (_spans["A"][1] - _spans["A"][0]) for _, (a, b) in real))
    else:
        bite("real GOOD-MORNING.md present", False)

    # green control on the REAL repo — the walk must complete and cover the whole vocabulary
    rows, method, errors = measure_sizes(REPO)
    bite(f"real-repo sizes walk clean (got: {errors[:2]})", errors == [])
    bite("real-repo covers full vocabulary",
         len(rows) == len(GM_VOCAB) + len(LS_VOCAB))
    bite("real-repo announces its method", bool(method))

    if fails:
        print("[_gm_usage selftest] FAIL:")
        for f in fails:
            print(f"  ✗ {f}")
        return 1
    print(f"[_gm_usage selftest] OK — {len(run)} bites, all fired or held as contracted "
          f"(sizes method: {method})")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--check-line" in argv:
        line = argv[argv.index("--check-line") + 1]
        issues = validate_usage_line(line)
        for i in issues:
            print(f"✗ {i}")
        if not issues:
            print("✓ well-formed (FORM only — honesty stays yours)")
        return 1 if issues else 0
    if "--sizes" in argv:
        session = argv[argv.index("--session") + 1] if "--session" in argv else "?"
        line, errors = sizes_line(session)
        if errors:
            for e in errors:
                print(f"✗ {e}")
            return 1
        print(line)
        return 0
    print(__doc__.split("Usage:")[1])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
