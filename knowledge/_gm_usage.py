#!/usr/bin/env python3
"""Section-usage instrumentation (#23, ruled Dave 2026-07-28 — lane 1 step 2).

WHAT THIS MEASURES (JIT note §7.3, `notes/2026-07-28-memento-jit-context-research.md`):
whether the cold-start chain's reference weight is actually USED. Every wrap, the session's
GM stratum block carries two lines beside the pre-flight stamp:

  > **section-usage #<N> (observed, self-report):** GM HDR:C LATEST:C ... · LS HDR:R SPIN:U ...
  > **section-sizes #<N> (<method>):** GM HDR:2410 LATEST:1187 ... · LS ... · totals GM:14332 LS:16762

★ UNMEASURED IS A LEGAL VALUE (#62 — the #61 finding "two correct behaviours colliding").
#55's wrap wrote an HONEST refusal for #54 (`9ca96e1`) and the vocabulary refused it, because
nobody had taught the format that not-measuring is something a session may truthfully say.
The legal form is EXACTLY:

  > **section-usage #<N>:** ⛔ **NOT CAPTURED — UNMEASURED.**

Scope is the quoted form and nothing wider (a gate must quote what it permits): a near-miss
still REFUSES, a session may not testify BOTH codes and UNMEASURED, and an UNMEASURED session
contributes NO column to the series — same convention as a session absent from the record,
but named separately in notes, never flattened into a gap.

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

Usage:  python3 knowledge/_gm_usage.py --usage-template --session 23  # ★ #218: the usage line's
                                                              #   FORM from the vocabulary, codes
                                                              #   left blank (`?`) for you to fill
        python3 knowledge/_gm_usage.py --sizes --session 23   # print the code-measured sizes line
        python3 knowledge/_gm_usage.py --check-line "<line>"  # validate a usage line (exit 1 on malformed)
        python3 knowledge/_gm_usage.py --history              # #35: read the ACCUMULATED testimony as a series
        python3 knowledge/_gm_usage.py --selftest             # bites — every check proves it can FAIL
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

CODES = ("U", "R", "C")

# --- THE VOCABULARY — only copy. (id, line-START pattern). Order = document order.
# GM: C1 deliberately starts at the `# §C` heading itself so the queue preamble has an owner.
# ⬛ RETIRED #35 (2026-07-29) on Dave's ruling: C2b · C3 · C4b · C5 were OFFLOADED VERBATIM to
# `_GM-ARCHIVE.md` — never cited in eleven sessions of testimony, and the archive IS in the
# retrieval corpus, so they stay reachable and are simply no longer carried. Their ids survive in
# the historical `section-usage` lines, where `usage_streaks` reports them as `retired` — which is
# why the #35 reader was built to tolerate ids the vocabulary no longer knows. Register (what was
# offloaded, where, and that `C4b` is still LIVE WORK): `GOOD-MORNING.md` §C·4 ⬛ DEFERRED REGISTER.
GM_VOCAB = (
    ("HDR",     None),  # implicit: file start → first explicit marker
    ("LATEST",  re.compile(r"^>\s*##\s*★\s*LATEST\b")),
    ("PRIOR",   re.compile(r"^>\s*##\s*★\s*PRIOR\b")),
    ("DOFIRST", re.compile(r"^##\s*⬛\s*DO TH", re.I)),
    ("A",       re.compile(r"^#\s*§A\b")),
    ("C1",      re.compile(r"^#\s*§C\b|^##\s*1\.\s")),
    ("C2",      re.compile(r"^##\s*2\.\s")),
    ("C4",      re.compile(r"^##\s*4\.\s")),
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
# ★ The honest-refusal form, first-class since #62. EXACT — anchored both ends, no free text:
# legality is scoped to the quoted form, and a near-miss is still a REFUSAL, never a skip.
UNMEASURED_RE = re.compile(
    r"^>\s*\*\*section-usage\s+#(\d+):\*\*\s*⛔\s*\*\*NOT CAPTURED — UNMEASURED\.\*\*\s*$")
SIZES_RE = re.compile(
    r"^>\s*\*\*section-sizes\s+#(\d+)\s*\(([^)]*)\):\*\*\s*GM\s+(.*?)\s*·\s*LS\s+(.*?)(\s*·\s*totals.*)?$")
TOKEN_RE = re.compile(r"^([A-Za-z0-9]+):([A-Za-z0-9]+)$")

# ★★ #218 — THE SCAFFOLD, AND THE ARCHAEOLOGY THAT SAYS WHY IT IS A SCAFFOLD AND NOT A LOOSENING.
#
# WHAT HAPPENED AT THE #218 WRAP: the gate refused the stratum twice, with two fails —
# `LS: unknown section id \`WEATHER\`` and `LS: no testimony for WEBFONT, LIVE, LIFECYCLE, …`
# (7 ids). The obvious reading — "#217's line passed, #218's failed, so the vocabulary tightened
# between the two wraps" — IS FALSE, and it was checked before anything was changed
# [[premise-ages-faster-than-rule]]:
#   · `git diff e6a1fe5 080204a -- knowledge/_gm_usage.py` is EMPTY. `GM_VOCAB`/`LS_VOCAB` have
#     not been touched since `2bc83b4` (#158, 2026-08-12) — 60 sessions.
#   · `_LIVE-STATE.md`'s `## ` headings are structurally IDENTICAL at both wraps (11 sections).
#   · Both committed #218 versions of `GOOD-MORNING.md` carry the CORRECT line; the refusal is
#     in `notes/_REHEARSAL-LOG.jsonl` at wrap-open only.
# ⇒ NOTHING TIGHTENED. A HAND-TYPED LINE DRIFTED: `WEATHER` for `WEBFONT`, and seven ids simply
# not typed. The gate did its job, the wrap sub repaired the line, and the whole cost was paid at
# the seam where a wrap is most expensive. ⛔ So the vocabulary is NOT loosened here, and no id
# is added: `WEATHER` is not a section, it is a typo, and registering it would inscribe a false
# fact in the one copy the sizes walk depends on.
#
# ★ WHAT THE CLASS ACTUALLY IS: the `section-sizes` line is CODE-MEASURED (`--sizes`), while its
# sibling `section-usage` — 20 ids that must match two vocabularies exactly — is typed by hand
# every wrap, from memory or by copying last session's line. The IDS are FORM (this file already
# holds the only copy of them); only the CODES are testimony. Making a human retype the form
# guarantees exactly this defect, on a schedule.
# ⇒ `--usage-template` emits the FORM from the vocabulary and leaves the TESTIMONY blank. The
# placeholder is illegal on purpose: a pasted-but-unfilled template REFUSES, loudly and by name,
# so the scaffold can never become machine-authored testimony. The honesty contract is untouched
# — no code is ever written by this tool.
USAGE_PLACEHOLDER = "?"


def _ids(vocab):
    return [i for i, _ in vocab]


def usage_template(session):
    """The section-usage line as a SCAFFOLD: every id, in document order, from the ONLY copy of
    the vocabulary, with `?` where the session's own testimony goes. Refused until filled."""
    def blob(vocab):
        return " ".join(f"{v}:{USAGE_PLACEHOLDER}" for v in _ids(vocab))
    return (f"> **section-usage #{session} (self-report):** "
            f"GM {blob(GM_VOCAB)} · LS {blob(LS_VOCAB)}")


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
    """FORM check only (testimony stays the session's). Returns list of issues, [] = well-formed.
    ★ #62: the exact UNMEASURED form is well-formed too — an honest refusal is legal testimony,
    and a wrap that cannot capture must be able to say so without being called MALFORMED."""
    if UNMEASURED_RE.match(line.strip()):
        return []
    m = USAGE_RE.match(line.strip())
    if not m:
        return ["section-usage line does not match the contract "
                "`> **section-usage #<N> (<status>):** GM <ID:CODE ...> · LS <ID:CODE ...>`"]
    issues = []
    if "self-report" not in m.group(2):
        issues.append("status parenthetical must say self-report — the line is testimony "
                      "and must describe itself as such (confident-false-inscription guard)")
    # ★ #218 — the SCAFFOLD, unfilled. Named as its own refusal rather than left to fall out as
    # N malformed tokens: the remedy ("write your own U/R/C") is different from every other
    # failure here, and a refusal that names the wrong remedy costs a wrap seam.
    blanks = [t for t in (m.group(3) + " " + m.group(4)).split()
              if t.endswith(":" + USAGE_PLACEHOLDER)]
    if blanks:
        issues.append(f"{len(blanks)} section(s) still carry the `{USAGE_PLACEHOLDER}` "
                      f"placeholder ({', '.join(blanks[:4])}…) — `--usage-template` emits the "
                      f"FORM, never the testimony. Replace every `{USAGE_PLACEHOLDER}` with "
                      f"U (unread) / R (read) / C (cited) yourself; a machine-authored code "
                      f"would be a false inscription, which is what this line exists to prevent.")
    for group, blob, vocab in (("GM", m.group(3), GM_VOCAB), ("LS", m.group(4), LS_VOCAB)):
        seen = {}
        for tok in blob.split():
            tm = TOKEN_RE.match(tok)
            if not tm:
                if tok.endswith(":" + USAGE_PLACEHOLDER):
                    seen[tok.split(":")[0]] = USAGE_PLACEHOLDER   # counted, already reported
                    continue
                issues.append(f"{group}: malformed token `{tok}`")
                continue
            vid, code = tm.group(1), tm.group(2)
            if vid not in _ids(vocab):
                issues.append(f"{group}: unknown section id `{vid}` — vocabulary is the "
                              f"only copy (register it, never free-type). ⚠ #218's `WEATHER` "
                              f"was a TYPO for `WEBFONT`, not a new section: generate the line "
                              f"with `python3 knowledge/_gm_usage.py --usage-template --session "
                              f"<N>` and fill in the codes, rather than retyping 20 ids")
            elif vid in seen:
                issues.append(f"{group}: section `{vid}` testified twice")
            elif code not in CODES:
                issues.append(f"{group}: `{vid}` carries illegal code `{code}` (U/R/C only)")
            seen[vid] = code
        missing = [v for v in _ids(vocab) if v not in seen]
        if missing:
            issues.append(f"{group}: no testimony for {', '.join(missing)} — every section "
                          f"is testified exactly once, U is a statement too. ⚠ Ids are FORM, not "
                          f"testimony: `python3 knowledge/_gm_usage.py --usage-template "
                          f"--session <N>` emits all {len(_ids(vocab))} of this group's from the "
                          f"vocabulary itself, so only the codes are yours to write (#218)")
    return issues


def validate_stratum(text):
    """For the wrap gate: check the current stratum carries both well-formed lines.
    Returns list of issues; [] = green. Malformed is called out as WORSE than missing."""
    issues = []
    usage = [ln for ln in text.splitlines() if "section-usage" in ln and ln.lstrip().startswith(">")]
    if not usage:
        issues.append("section-usage line MISSING from the session stratum — start from "
                      "`python3 knowledge/_gm_usage.py --usage-template --session <N>` (the "
                      "ids come from the vocabulary, the U/R/C codes are yours to write); the "
                      "dataset this feeds is what LS-trim-vs-defer waits on")
    else:
        for problem in validate_usage_line(usage[0]):
            issues.append(f"section-usage line MALFORMED (worse than missing — a false "
                          f"inscription): {problem}")
    if not any("section-sizes" in ln for ln in text.splitlines()):
        issues.append("section-sizes line MISSING — emit via "
                      "`python3 knowledge/_gm_usage.py --sizes --session <N>` (code-measured)")
    return issues


# --- THE READER (#35) — the dataset accumulates; until now NOTHING read it ---------------
# ds-024's exact class, and the instrument's own author wrote the consumer's absence into
# the docstring above ("the dataset that answers LS-trim-vs-defer") without ever building
# the thing that answers it. Eleven sessions of testimony (#23–#34) sat in `_GAUGE-LOG.md`
# being FORM-checked one line at a time and never once read as a series.
#
# ★ WHAT CHANGED THE JOB, MEASURED #35: the brief said these sections were "~3,275 tape
#   carried dead every window". They are NOT — #33 cut the read chain to
#   header → ★ LATEST → the LS LATEST delta, and every id named below sits OUTSIDE it.
#   The window cost was already banked. What the series actually shows is a RECORD
#   question, not a window question: twelve sections nobody has cited in eleven sessions,
#   still carried in `GOOD-MORNING.md` / `_LIVE-STATE.md`, still rolled, still gated.
#
# ★ THIS READER PROPOSES NOTHING. It publishes a measurement and names candidates.
#   Whether a candidate is OFFLOADED (moved to the retrieval index, reachable, not carried),
#   TRIMMED (it is duplicated somewhere durable, so the copy here is the redundant one) or
#   KEPT is Dave's ruling — derivation governance, the engine never derives-and-promotes.
# ⚠ FOUND AT #35's OWN WRAP, by the probe firing on the banner that describes it: detecting
# testimony by the SUBSTRING `section-usage` refuses every blockquoted line that merely MENTIONS
# it — and a banner announcing "eleven sessions of `section-usage` testimony" is prose, not
# testimony. Same class as #33's bite matching a phrase two messages happened to share. The
# marker is the `**section-usage #<N>` OPENING, which prose does not imitate; a line that opens
# this way and then fails to parse is still a REFUSAL, so nothing is loosened, only aimed.
USAGE_MARKER_RE = re.compile(r"^>\s*\*\*section-usage\b")
HISTORY_SOURCES = (os.path.join("notes", "_GAUGE-LOG.md"), "GOOD-MORNING.md")

# AGENT-PROPOSED, ADVISORY, AWAITING DAVE. Chosen to sit one below the smallest
# never-consumed streak measured at #35 (6), so the headline names the settled cases and
# not the marginal ones. ⚠ A threshold nobody ruled must never read as a ruling: the probe
# publishes the FULL table whatever this is set to, so the number moves the headline only.
DEFER_STREAK = 6
DEFER_STREAK_STATUS = "AGENT-PROPOSED, ADVISORY — awaiting Dave (#35)"


def usage_history(repo=REPO):
    """Read EVERY `section-usage` line in the corpus as a SERIES.

    Returns `(rows, refusals, notes)` — `rows` is `[(session_n, {id: code}), ...]` oldest
    first, `refusals` is fatal (a line that looks like testimony and is not well-formed),
    `notes` is everything observed that is not an error.

    ⚠ IT REFUSES RATHER THAN SKIPS. A line containing `section-usage` that does not parse
    is a REFUSAL, never a quiet omission: a reader that silently drops the lines it cannot
    understand reports a cleaner history than the record contains, which is the
    confident-false-inscription failure with extra steps.

    ⚠ THE SAME SESSION APPEARS TWICE BY DESIGN — its stratum lives in `GOOD-MORNING.md`
    until the next wrap's `roll_2f` moves it to the log. Identical duplicates are collapsed
    silently; DISAGREEING duplicates are a REFUSAL, because one of the two is false and this
    reader cannot know which.
    """
    rows, refusals, notes = {}, [], []
    seen_src, unmeasured = {}, {}
    for rel in HISTORY_SOURCES:
        path = os.path.join(repo, rel)
        if not os.path.exists(path):
            notes.append(f"history source missing: {rel} — UNREAD, not assumed empty")
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for ln in text.splitlines():
            if not USAGE_MARKER_RE.match(ln.strip()):
                continue
            um = UNMEASURED_RE.match(ln.strip())
            if um:
                # ★ FIRST-CLASS (#62): present testimony that no measurement exists. No table
                # column — the same convention as a session absent from the record (a column of
                # invented `?`s would flatten "refused to measure" into "not yet registered").
                un = int(um.group(1))
                if un in rows:
                    refusals.append(
                        f"session #{un} testifies with codes in {seen_src[un]} and UNMEASURED "
                        f"in {rel} — one of them is false and this reader cannot tell which. "
                        f"REFUSED.")
                    continue
                unmeasured.setdefault(un, rel)   # identical duplicates collapse silently
                continue
            m = USAGE_RE.match(ln.strip())
            if not m:
                refusals.append(f"{rel}: a `section-usage` line does not parse — "
                                f"REFUSED, not skipped: {ln.strip()[:90]}")
                continue
            n = int(m.group(1))
            if n in unmeasured:
                refusals.append(
                    f"session #{n} testifies UNMEASURED in {unmeasured[n]} and with codes in "
                    f"{rel} — one of them is false and this reader cannot tell which. REFUSED.")
                continue
            testimony = {}
            for group, blob in (("GM", m.group(3)), ("LS", m.group(4))):
                for tok in blob.split():
                    tm = TOKEN_RE.match(tok)
                    if tm:
                        testimony[f"{group}:{tm.group(1)}"] = tm.group(2)
            if n in rows and rows[n] != testimony:
                refusals.append(
                    f"session #{n} testifies DIFFERENTLY in {seen_src[n]} and {rel} — "
                    f"one of them is false and this reader cannot tell which. REFUSED.")
                continue
            rows[n] = testimony
            seen_src[n] = rel
    ordered = sorted(rows.items())
    if ordered:
        span = [n for n, _ in ordered]
        gaps = [n for n in range(span[0], span[-1] + 1)
                if n not in rows and n not in unmeasured]
        if gaps:
            notes.append(f"sessions inside the range with NO testimony at all: "
                         f"{', '.join('#%d' % g for g in gaps)} — absent from the dataset, "
                         f"which is a claim about the RECORD, not about those sessions")
    if unmeasured:
        # ★ Named separately, never flattened into the gap note: these sessions DID testify.
        notes.append(f"sessions testifying UNMEASURED (an honest refusal, first-class #62): "
                     f"{', '.join('#%d' % u for u in sorted(unmeasured))} — present in the "
                     f"record, absent from the table by their own declaration")
    return ordered, refusals, notes


def usage_streaks(rows):
    """Per section id: the sequence, the trailing unread-streak, and whether it was EVER cited.

    Returns `{id: {"seq", "u_streak", "unknown", "ever_consumed", "sessions"}}`, ids in
    vocabulary order with any retired id appended after them.

    ⚠ UNKNOWN IS NEVER COUNTED AS UNREAD. An id absent from a session's line (a section
    registered after that session testified) is `?`, and a `?` STOPS the streak instead of
    extending it. The opposite convention — treating silence as an unread — would let a
    reader manufacture the very evidence it is looking for. A count is not a measurement.
    """
    live = [f"GM:{i}" for i, _ in GM_VOCAB] + [f"LS:{i}" for i, _ in LS_VOCAB]
    retired = []
    for _, d in rows:
        for k in d:
            if k not in live and k not in retired:
                retired.append(k)
    out = {}
    for key in live + retired:
        seq = "".join(d.get(key, "?") for _, d in rows)
        streak = 0
        for ch in reversed(seq):
            if ch == "U":
                streak += 1
            else:
                break
        out[key] = {
            "seq": seq,
            "u_streak": streak,
            "unknown": seq.count("?"),
            "ever_consumed": "C" in seq,
            "sessions": len(seq),
            "retired": key in retired,
        }
    return out


def deferral_candidates(streaks, min_streak=DEFER_STREAK):
    """ADVISORY. Sections never once CITED and unread for `min_streak` consecutive testified
    sessions. Sorted longest-streak first. It names them; it does not say what to do."""
    return sorted(
        [(k, v) for k, v in streaks.items()
         if not v["ever_consumed"] and v["u_streak"] >= min_streak and not v["retired"]],
        key=lambda kv: (-kv[1]["u_streak"], kv[0]))


def history_report(repo=REPO, min_streak=DEFER_STREAK):
    """The published measurement — one text block, used by the CLI and by the gate probe."""
    rows, refusals, notes = usage_history(repo)
    if refusals:
        return ("USAGE HISTORY — REFUSED, no table published:\n  "
                + "\n  ".join(refusals)), rows, refusals
    if not rows:
        return ("USAGE HISTORY — no `section-usage` testimony found anywhere. UNMEASURED, "
                "not assumed clean."), rows, refusals
    st = usage_streaks(rows)
    sessions = ", ".join("#%d" % n for n, _ in rows)
    lines = [f"USAGE HISTORY — {len(rows)} sessions of testimony ({sessions})",
             "  (U unread · R read · C cited · ? not yet registered — UNKNOWN, never an unread)",
             f"  {'id':<14} {'oldest → newest':<{max(14, len(rows))}} {'U-streak':>8}  note"]
    for k, v in st.items():
        note = []
        if v["retired"]:
            note.append("RETIRED id — testified but no longer in the vocabulary")
        if not v["ever_consumed"]:
            note.append("NEVER CITED")
        if v["unknown"]:
            note.append(f"{v['unknown']} unknown")
        lines.append(f"  {k:<14} {v['seq']:<{max(14, len(rows))}} {v['u_streak']:>8}  "
                     + " · ".join(note))
    cands = deferral_candidates(st, min_streak)
    lines.append("")
    if cands:
        lines.append(f"  ⬛ CANDIDATES FOR DAVE — never cited in {len(rows)} sessions AND "
                     f"unread {min_streak}+ running ({DEFER_STREAK_STATUS}):")
        for k, v in cands:
            lines.append(f"     {k:<14} unread {v['u_streak']} running, cited 0 times")
        lines.append("  ⚠ The remedy is UNRULED. Three are open and they are not the same: "
                     "OFFLOAD (move to the retrieval index — reachable, not carried) · "
                     "TRIM (it is durably recorded elsewhere, so this copy is the redundant "
                     "one) · KEEP (rarely consulted is not the same as not needed). "
                     "This reader must never pick one.")
    else:
        lines.append(f"  ✓ no section is both never-cited and unread {min_streak}+ running.")
    return "\n".join(lines), rows, refusals


# --- selftest — every bite proves the check can FAIL (green control included) ------------
# ⚠ re-pointed #35 with the vocabulary: C2b/C3/C4b/C5 were offloaded and retired, so a fixture
# still naming them would test a vocabulary that no longer exists — the stale-fixture class.
GOOD_USAGE = ("> **section-usage #23 (observed, self-report):** "
              "GM HDR:C LATEST:C PRIOR:R DOFIRST:C A:C C1:C C2:R C4:C "
              "STRATA:R · LS HDR:R LANES:C SPIN:R DELTAS:C WEBFONT:R LIVE:R LIFECYCLE:R "
              "DEAD:R OPEN:R TARGETS:R SPINOFFS:R")


def selftest():
    fails, run = [], []

    def bite(name, cond):
        run.append(name)
        if not cond:
            fails.append(name)

    bite("good line must validate", validate_usage_line(GOOD_USAGE) == [])
    bite("missing id must fire", any("no testimony" in i for i in
         validate_usage_line(GOOD_USAGE.replace("C4:C ", ""))))
    bite("unknown id must fire", any("unknown section id" in i for i in
         validate_usage_line(GOOD_USAGE.replace("C4:C", "C4:C C9:R"))))
    bite("illegal code must fire", any("illegal code" in i for i in
         validate_usage_line(GOOD_USAGE.replace("SPIN:R", "SPIN:X"))))
    bite("duplicate must fire", any("testified twice" in i for i in
         validate_usage_line(GOOD_USAGE.replace("DEAD:R", "DEAD:R DEAD:U"))))
    bite("missing self-report tag must fire", any("self-report" in i for i in
         validate_usage_line(GOOD_USAGE.replace("(observed, self-report)", "(observed)"))))
    bite("non-matching line must fire", validate_usage_line("> section-usage nonsense") != [])

    # ---- ★ #218 — THE HAND-TYPED-LINE CLASS, driven on the ACTUAL #218 wrap-open failure and on
    # the scaffold that removes it. The defect line below is reconstructed from the two refusals
    # recorded in `notes/_REHEARSAL-LOG.jsonl` (2026-08-24, kind `wrap-open`): `unknown section
    # id WEATHER` + `no testimony for WEBFONT, LIVE, LIFECYCLE, …` (7 ids).
    defect_218 = ("> **section-usage #218 (self-report, delegated OPUS wrap sub):** "
                  "GM HDR:C LATEST:C PRIOR:R DOFIRST:U A:U C1:R C2:U C4:U STRATA:C "
                  "· LS HDR:C LANES:R SPIN:U DELTAS:C WEATHER:U")
    d_issues = validate_usage_line(defect_218)
    bite("#218 defect: `WEATHER` must be refused as an unknown id (NOT registered — it is a "
         "typo for WEBFONT, and registering it would inscribe a false section)",
         any("unknown section id `WEATHER`" in i for i in d_issues))
    bite("#218 defect: the 7 untyped LS ids must be named one by one",
         any("no testimony for" in i and "WEBFONT" in i and "SPINOFFS" in i for i in d_issues))
    bite("#218 defect: both refusals must NAME THE SCAFFOLD (a refusal that does not carry its "
         "remedy costs the same wrap seam twice)",
         all(any("--usage-template" in i for i in d_issues) for _ in (0,)))

    # ---- the scaffold itself: FORM from the vocabulary, TESTIMONY refused until written.
    tmpl = usage_template(219)
    # ⚠ PARSED IN THE CONSUMER'S GRAMMAR (USAGE_RE — the same reader the gate uses), never by
    # substring: a template that merely CONTAINS the ids could still be malformed, and a check
    # that raises on a mutation is a crash, not a fail [[a-crash-is-not-a-fail]].
    _tm = USAGE_RE.match(tmpl.strip())
    _toks = (lambda blob: [t.split(":")[0] for t in blob.split()])
    bite("template parses as a section-usage line at all", _tm is not None)
    bite("template carries EVERY id of BOTH vocabularies, in document order, and nothing else "
         "— it is DERIVED from GM_VOCAB/LS_VOCAB, so a vocabulary change flows into it and "
         "cannot be forgotten by a typist",
         bool(_tm) and _toks(_tm.group(3)) == _ids(GM_VOCAB)
         and _toks(_tm.group(4)) == _ids(LS_VOCAB))
    t_issues = validate_usage_line(tmpl)
    bite("an UNFILLED template REFUSES — a scaffold may never become testimony by accident",
         any("placeholder" in i for i in t_issues))
    bite("…and it says so ONCE, as its own remedy, not as 20 malformed tokens",
         len([i for i in t_issues if "malformed token" in i]) == 0)
    filled = tmpl.replace(f":{USAGE_PLACEHOLDER}", ":U")
    bite("a template with the codes WRITTEN IN validates — the scaffold's whole point",
         validate_usage_line(filled) == [])
    bite("a template with ONE id deleted still fires the missing-testimony bite (the scaffold "
         "helps, it does not replace the check)",
         any("no testimony" in i for i in
             validate_usage_line(filled.replace(" SPINOFFS:U", ""))))

    good_stratum = GOOD_USAGE + "\n> **section-sizes #23 (tiktoken):** GM HDR:1 · LS HDR:1"
    bite("good stratum quiet", validate_stratum(good_stratum) == [])
    bite("stratum missing usage fires", any("MISSING" in i for i in validate_stratum("> x")))
    bite("stratum malformed usage fires — and says MALFORMED", any(
        "MALFORMED" in i for i in validate_stratum(
            GOOD_USAGE.replace("SPIN:R", "SPIN:X") + "\n> **section-sizes #23 (t):** x")))

    # ⚠ fixture re-pointed #35 — C2b/C3/C4b/C5 were offloaded and retired from the vocabulary.
    gm_fx = ["head", "> ## ★ LATEST — x", "> ## ★ PRIOR — x", "## ⬛ DO THIS FIRST",
             "# §A · ORIENTATION", "# §C · QUEUE", "## 1. strands", "## 2. batch",
             "## 4. enact", "### ⏱ SESSION STRATA"]
    spans, errs = split_sections(gm_fx, GM_VOCAB, _gm_unknown)
    bite("gm fixture splits clean", errs == [] and spans is not None
         and spans["C4"] == (8, 9))
    _, errs = split_sections(gm_fx + ["## 6. surprise"], GM_VOCAB, _gm_unknown)
    bite("unregistered `## 6.` must refuse", any("unregistered numbered" in e for e in errs))
    _, errs = split_sections([ln for ln in gm_fx if "## 4." not in ln], GM_VOCAB, _gm_unknown)
    bite("missing GM marker must refuse", any("not found: C4" in e for e in errs))

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

    # --- THE READER (#35) — bites -----------------------------------------------------
    # ★ The positive ones are load-bearing (#32's lesson): a refusal-only suite survives a
    # revert that deletes the reader entirely, because refusals still fire on a series that
    # was never built. So the first bites assert a REAL candidate list off a real series.
    _mk = lambda seqs: [(23 + n, {k: v[n] for k, v in seqs.items() if v[n] != "?"})
                        for n in range(len(next(iter(seqs.values()))))]

    st = usage_streaks(_mk({"GM:C3": "RRRUUUUU", "GM:HDR": "CCCCCCCC"}))
    bite("reader: a never-cited run is counted", st["GM:C3"]["u_streak"] == 5
         and st["GM:C3"]["ever_consumed"] is False)
    bite("reader: GREEN CONTROL — a cited section is never a candidate",
         st["GM:HDR"]["ever_consumed"] is True
         and "GM:HDR" not in dict(deferral_candidates(st, 1)))
    bite("reader: a long unread run that was EVER cited is not a candidate",
         "GM:C4" not in dict(deferral_candidates(
             usage_streaks(_mk({"GM:C4": "CUUUUUUU"})), 6)))
    # ⚠ ids here must be LIVE vocabulary — `deferral_candidates` excludes retired ids by
    # design, so a fixture naming an offloaded section tests the retirement path, not the
    # boundary. C3 was offloaded at #35's wrap and this bite went red the moment it was.
    bite("reader: BOUNDARY — streak one short of the threshold is NOT named",
         dict(deferral_candidates(usage_streaks(_mk({"GM:C2": "RRUUUUU"})), 6)) == {}
         and "GM:C2" in dict(deferral_candidates(
             usage_streaks(_mk({"GM:C2": "RUUUUUU"})), 6)))
    # ★ THE ONE THAT MATTERS MOST: silence must not manufacture the evidence being sought.
    st_q = usage_streaks(_mk({"GM:C3": "UUU?UU"}))
    bite("reader: UNKNOWN STOPS the streak, never extends it (a count is not a measurement)",
         st_q["GM:C3"]["u_streak"] == 2 and st_q["GM:C3"]["unknown"] == 1)
    bite("reader: an id in testimony but not in the vocabulary is RETIRED, not a candidate",
         usage_streaks(_mk({"GM:GONE": "UUUUUUUU"}))["GM:GONE"]["retired"] is True
         and dict(deferral_candidates(
             usage_streaks(_mk({"GM:GONE": "UUUUUUUU"})), 1)) == {})

    # file-level refusals — these need a repo shape, so build a throwaway one
    import tempfile
    _good = GOOD_USAGE.replace("#23", "#40")
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"))
        _log = os.path.join(td, "notes", "_GAUGE-LOG.md")
        _gm = os.path.join(td, "GOOD-MORNING.md")
        open(_log, "w", encoding="utf-8").write(_good + "\n")
        open(_gm, "w", encoding="utf-8").write(_good + "\n")
        r, ref, _n = usage_history(td)
        bite("reader: the SAME session in both sources collapses silently",
             ref == [] and len(r) == 1)
        open(_gm, "w", encoding="utf-8").write(_good.replace("SPIN:R", "SPIN:U") + "\n")
        _r, ref, _n = usage_history(td)
        bite("reader: DISAGREEING duplicates REFUSE (one is false, and it cannot tell which)",
             any("testifies DIFFERENTLY" in e for e in ref))
        open(_gm, "w", encoding="utf-8").write("> **section-usage #41 (observed):** garbled\n")
        _r, ref, _n = usage_history(td)
        bite("reader: an unparseable testimony line REFUSES, never skips",
             any("does not parse" in e for e in ref))
        open(_gm, "w", encoding="utf-8").write(_good.replace("#40", "#43") + "\n")
        _r, _ref, nts = usage_history(td)
        bite("reader: a session with NO testimony inside the range is NAMED as a record gap",
             any("#41, #42" in n for n in nts))
        r0, ref0, n0 = usage_history(os.path.join(td, "nope"))
        bite("reader: a missing source is UNREAD, never assumed empty",
             r0 == [] and any("UNREAD, not assumed empty" in n for n in n0))

    # --- UNMEASURED is first-class (#62) — and its legality is SCOPED to the exact form ---
    _unm = "> **section-usage #41:** ⛔ **NOT CAPTURED — UNMEASURED.**"
    bite("UNMEASURED form is well-formed at the wrap gate (an honest refusal is legal testimony)",
         validate_usage_line(_unm) == [])
    bite("a NEAR-UNMEASURED form still fires at the wrap gate — legality is the quoted form only",
         validate_usage_line(_unm.replace("UNMEASURED.", "UNMEASURED")) != [])
    with tempfile.TemporaryDirectory() as td3:
        os.makedirs(os.path.join(td3, "notes"))
        _log3 = os.path.join(td3, "notes", "_GAUGE-LOG.md")
        _gm3 = os.path.join(td3, "GOOD-MORNING.md")
        open(_gm3, "w", encoding="utf-8").write(GOOD_USAGE.replace("#23", "#40") + "\n")
        open(_log3, "w", encoding="utf-8").write(
            _unm + "\n" + GOOD_USAGE.replace("#23", "#43") + "\n")
        r3, ref3u, n3 = usage_history(td3)
        bite("reader: an UNMEASURED line is FIRST-CLASS — read, never a refusal",
             ref3u == [] and len(r3) == 2)
        bite("reader: an UNMEASURED session is NOT a record gap — the gap note names #42 only",
             any("NO testimony" in n and "#42" in n and "#41" not in n for n in n3))
        bite("reader: UNMEASURED sessions are NAMED in notes, never flattened",
             any("UNMEASURED" in n and "#41" in n for n in n3))
        # disagreement, both orders — a session may not testify codes AND UNMEASURED
        open(_log3, "w", encoding="utf-8").write(
            GOOD_USAGE.replace("#23", "#41") + "\n" + _unm + "\n")
        _r3, ref3d, _n3d = usage_history(td3)
        bite("reader: codes-then-UNMEASURED for the SAME session REFUSES",
             any("cannot tell which" in e for e in ref3d))
        open(_log3, "w", encoding="utf-8").write(
            _unm + "\n" + GOOD_USAGE.replace("#23", "#41") + "\n")
        _r3, ref3e, _n3e = usage_history(td3)
        bite("reader: UNMEASURED-then-codes for the SAME session REFUSES too",
             any("cannot tell which" in e for e in ref3e))
        # scope mutation: a near-miss in the CORPUS still refuses, never quietly skips
        open(_log3, "w", encoding="utf-8").write(
            _unm.replace(" — ", " - ") + "\n")
        _r3, ref3f, _n3f = usage_history(td3)
        bite("reader: a NEAR-UNMEASURED corpus line still REFUSES (nothing was loosened, only taught)",
             any("does not parse" in e for e in ref3f))

    _prose = ("> **★ the usage data:** eleven sessions of `section-usage` testimony were read "
              "as a SERIES — this line is PROSE and must not be mistaken for testimony")
    with tempfile.TemporaryDirectory() as td2:
        os.makedirs(os.path.join(td2, "notes"))
        open(os.path.join(td2, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8").write(
            GOOD_USAGE.replace("#23", "#50") + "\n")
        open(os.path.join(td2, "GOOD-MORNING.md"), "w", encoding="utf-8").write(_prose + "\n")
        r2, ref2, _n2 = usage_history(td2)
        bite("reader: a BANNER MENTIONING `section-usage` is prose, not testimony (found #35)",
             ref2 == [] and len(r2) == 1)
        open(os.path.join(td2, "GOOD-MORNING.md"), "w", encoding="utf-8").write(
            "> **section-usage #51 (observed):** garbled\n")
        _r2, ref3, _n3 = usage_history(td2)
        bite("reader: ...but a line that OPENS as testimony and fails to parse still REFUSES",
             any("does not parse" in e for e in ref3))

    # --- the deferral boundary on a WHOLE-FILE corpus (#78) ---------------------------
    # ★ RE-HOMED #78: these two intents were pinned to the REAL repo's candidate list
    # ("LS:DEAD/SPINOFFS/TARGETS are still never-cited") — a LIVE fact, and it died
    # honestly at #74's wrap, whose ratified testimony CITED all three
    # (notes/_GAUGE-LOG.md, section-usage #74). Two arms red, ONE cause, and the red
    # was the reader WORKING. The LS:LIFECYCLE note below already documented this exact
    # class; the pin outlived its premise anyway. The intents now live on a corpus where
    # the candidate exists BY CONSTRUCTION, with the mutation control in the same block.
    with tempfile.TemporaryDirectory() as td4:
        os.makedirs(os.path.join(td4, "notes"))
        _log4 = os.path.join(td4, "notes", "_GAUGE-LOG.md")
        _mkline = lambda n, code: GOOD_USAGE.replace("#23", "#%d" % n).replace(
            "DEAD:R", "DEAD:" + code)
        # seven straight sessions in which LS:DEAD is never cited and always unread
        open(_log4, "w", encoding="utf-8").write(
            "\n".join(_mkline(n, "U") for n in range(40, 47)) + "\n")
        _rep4, _rows4, _refs4 = history_report(td4)
        bite(f"fixture: a never-cited section unread 6+ IS named a candidate "
             f"(got: {_refs4[:1]})",
             _refs4 == [] and "LS:DEAD" in _rep4 and "CANDIDATES FOR DAVE" in _rep4)
        bite("fixture: the report publishes the remedy as UNRULED (it must never pick one)",
             "The remedy is UNRULED" in _rep4)
        # mutation control — ONE citation and both greens above must be able to flip
        open(_log4, "w", encoding="utf-8").write(
            "\n".join(_mkline(n, "U") for n in range(40, 46))
            + "\n" + _mkline(46, "C") + "\n")
        _rep4c, _, _refs4c = history_report(td4)
        bite("fixture MUTATION: one citation empties the candidate set and takes the "
             "UNRULED line with it (the green can fail)",
             _refs4c == [] and "The remedy is UNRULED" not in _rep4c
             and "no section is both never-cited" in _rep4c)

    # green control on the REAL repo — the series must read; candidate assertions are
    # MONOTONIC deltas only (testimony accumulates, ever_consumed never un-flips), so
    # these cannot age the way the #35 pin did.
    # ⚠ LS:LIFECYCLE stays out of every set here: #35 CITED it (the de-materialise
    # ruling rests on it), so the reader correctly dropped it — the founding precedent
    # for the class that took the #35 pin too.
    _rep, _rows, _refs = history_report(REPO)
    bite(f"real-repo usage history reads clean (got: {_refs[:1]})", _refs == [])
    bite("real-repo history covers every session that testified", len(_rows) >= 11)
    _st_real = usage_streaks(_rows)
    _real = deferral_candidates(_st_real)
    bite("real-repo: the #35 LS candidates have since been CITED and left the set the "
         "honest way (#74's sweep — assert the DELTA, not the dead pin)",
         all(_st_real[k]["ever_consumed"]
             for k in ("LS:DEAD", "LS:SPINOFFS", "LS:TARGETS"))
         and not ({k for k, _ in _real} & {"LS:DEAD", "LS:SPINOFFS", "LS:TARGETS"}))
    bite("real-repo: the #35 offloads have LEFT the candidate set (retired, not cited)",
         not ({k for k, _ in _real} & {"GM:C2b", "GM:C3", "GM:C4b", "GM:C5"}))
    bite("real-repo report closes in exactly ONE of its two legal states, never a "
         "remedy choice",
         ("The remedy is UNRULED" in _rep) != ("no section is both never-cited" in _rep))

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
    if "--history" in argv:
        report, _rows, refusals = history_report()
        print(report)
        return 1 if refusals else 0
    if "--usage-template" in argv:
        # ★ #218 — the FORM, generated; the TESTIMONY, blank and refused until you write it.
        session = argv[argv.index("--session") + 1] if "--session" in argv else "?"
        line = usage_template(session)
        print(line)
        print(f"# ⚠ NOT VALID YET, ON PURPOSE: replace every `:{USAGE_PLACEHOLDER}` with U "
              f"(unread) / R (read) / C (cited). The ids are FORM (from GM_VOCAB/LS_VOCAB, the "
              f"only copy); the codes are TESTIMONY and no tool may write them for you.",
              file=sys.stderr)
        return 0
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
